# Langfuse Internals — Subsystem Map for a Visual Guide

**Architecture spine (cite once, reuse everywhere):** `web/` is a Next.js app (tRPC routers + public REST API under `web/src/pages/api/public/`). `worker/` is a BullMQ consumer process; queues→processors are wired in `worker/src/app.ts` (37 `WorkerManager.register(...)` calls, e.g. lines 145, 312, 467, 607). `packages/shared/` holds domain Zod schemas (`src/domain/`), ClickHouse/Postgres repositories (`src/server/repositories/`), queue definitions (`src/server/queues.ts`), and services. **Two datastores:** Postgres (Prisma) for config/metadata; ClickHouse for high-volume traces/observations/scores/dataset-run-items. Most write paths to ClickHouse go through the **IngestionQueue** (`processEventBatch`), except annotation scores which write direct.

---

## Subsystem 1 — EVALS / LLM-as-a-Judge (DEEPEST)

**(a) Purpose:** Automatically score traces/observations/dataset-items by running configurable evaluators (LLM-as-judge or sandboxed code) and writing the result back as a `source=EVAL` score.

**(b) Key files**
- Web tRPC: `web/src/features/evals/server/router.ts` — `createJob` mutation (creates `jobConfiguration`) at `:941-1069`; `createTemplate` at `:1109`; `updateEvalJob` at `:1381`; historical-backfill enqueue to BatchActionQueue at `:1039-1065`.
- Web server helpers: `web/src/features/evals/server/evaluatorRepository.ts`, `evalTemplateCreation.ts`, `defaultEvalModelRouter.ts`, `codeEvalJobConfigValidation.ts`, `evaluator-preflight.ts`; public API under `web/src/features/evals/server/unstable-public-api/`.
- Queue/processors: `worker/src/queues/evalQueue.ts` — `evalJobTraceCreatorQueueProcessor` `:24`, `evalJobDatasetCreatorQueueProcessor` `:45`, `evalJobCreatorQueueProcessor` `:97`, `evalJobExecutorQueueProcessorBuilder` `:117` (LLM-rate-limit retry/backoff state machine `:178-268`), `llmAsJudgeExecutionQueueProcessorBuilder` `:272` (observation evals).
- Worker core: `worker/src/features/evaluation/evalService.ts` — `createEvalJobs` `:180` (config fetch `:192`, internal-trace loop guard `:243`, trace cache `:263`, sampling `:621`, dedup/cancel `:599-703`, job creation + enqueue `:635-678`); `runLLMAsJudgeEvaluation` `:735` (compile prompt `:784`, structured-output schema `:800-813`, model config `:824`, LLM call `:863`, validate+normalize `:926-950`); `toNormalizedScores` `:963`; `evaluate` (trace-level entry) `:1038`; `extractVariablesFromTracingData` `:1152`.
- Score writing: `worker/src/features/evaluation/evalCompletion.ts` `completeEvalExecution` `:21` → `evalScoreEvent.ts` `buildEvalScoreWritePayloads` `:16` (emits `SCORE_CREATE` ingestion events, `source=EVAL` `:52`).
- Dependency injection seam: `worker/src/features/evaluation/evalExecutionDeps.ts` — `createProductionEvalExecutionDeps` `:137` (`uploadScore` `:146`, `enqueueScoreIngestion` `:159`, `callLLM` `:193`, `fetchModelConfig` `:228`).
- Code evals: `packages/shared/src/server/evals/{codeEvalDispatchers,awsLambdaCodeEvalDispatcher,localCodeEvalDispatcher,codeEvalExecution}.ts`; worker `worker/src/features/evaluation/codeBased/executeCodeBasedEvaluation.ts`; queue `worker/src/queues/codeEvalQueue.ts`.
- Observation-level (newer): `worker/src/features/evaluation/observationEval/` (`observationEvalProcessor.ts`, `scheduleObservationEvals.ts`, `shouldSampleObservation.ts`).
- Shared types: `packages/shared/src/features/evals/types.ts` (`EvalTargetObject` `:28`, `variableMapping` `:88`, `TimeScopeSchema` `:227`, `availableTraceEvalVariables` `:133`), `outputDefinition.ts` (numeric/categorical/boolean output schema).
- Caching: `packages/shared/src/server/evalJobConfigCache.ts` (the "no eval configs for project" negative cache, set at `evalService.ts:218`).

**(c) Data flow**
1. **Config creation (UI/API):** `createJob` writes a `jobConfiguration` (Postgres) with `evalTemplateId`, `scoreName`, `targetObject` (TRACE/DATASET/EVENT/EXPERIMENT), `filter`, `variableMapping`, `sampling`, `delay`, `timeScope` (`["NEW"]`/`["EXISTING"]`). If `EXISTING`, a BatchAction job backfills historical data.
2. **Trigger:** When a trace is upserted (TraceUpsert queue) or a dataset-run-item is created (DatasetRunItemUpsert queue), `createEvalJobs` runs. It loads ACTIVE non-blocked configs, applies in-memory or DB filter matching, dedups against existing `jobExecution` rows, applies probabilistic **sampling**, then creates a `jobExecution` (status `PENDING`) and enqueues to **EvalExecutionQueue** with `delay` (sharded by `projectId-jobExecutionId`).
3. **Execution:** `evaluate()` loads job/config/template, extracts variables from ClickHouse trace/observation/dataset data via the `variableMapping`, compiles the prompt, validates an output-definition schema, calls the LLM with **structured output** (`deps.callLLM` → `fetchLLMCompletion`, traced internally with `environment=langfuse-...` to avoid eval-of-eval loops), validates/normalizes to scores.
4. **Score persistence:** `completeEvalExecution` builds deterministic score IDs and emits `SCORE_CREATE` events into the **IngestionQueue** (not a direct ClickHouse write), then marks `jobExecution` COMPLETED with `jobOutputScoreId`. Errors set status DELAYED (retryable 429/5xx, 120-min backoff) or ERROR.

**(d) Tradeoffs**
- Deterministic execution trace IDs (`createW3CTraceId(jobExecutionId)`) make retries idempotent and link each eval to its own trace.
- Negative caching + batched job-existence queries reduce ClickHouse/Postgres load when no/many configs exist.
- Internal-trace environment prefix guard (`evalService.ts:243`) is a load-bearing safety net against infinite eval recursion; enforced dually in `fetchLLMCompletion`.
- Eval scores route through ingestion (async, eventually consistent) for uniform processing, unlike annotation scores (direct write) — a deliberate consistency-vs-throughput split.
- DI deps object (`EvalExecutionDeps`) trades a little indirection for testability (mock LLM/score writes).

**(e) Lesson split:** **L1 — "Evaluator config & job creation"** (templates, target objects, variable mapping, filters, sampling, time scopes, the createEvalJobs dedup/cancel logic, negative cache). **L2 — "Eval execution & scoring"** (queue retry state machine, structured-output LLM call, output-definition→score normalization, deterministic IDs, ingestion-based score write, code-evals + observation-evals as variants).

> Note on **monitors** (`web/src/features/monitors/*`): despite being grouped here, it's a *separate metric-alerting* subsystem — `worker/src/queues/monitorQueue.ts` runs `MonitorProcessor` (`@langfuse/shared/monitors/server`) that evaluates metric thresholds and **publishes alerts to the WebhookQueue** (`monitorQueue.ts:27-37`). Best taught alongside Automations (Subsystem 6), not evals. **llm-schemas** (`web/src/features/llm-schemas/`) and **llm-tools** (`web/src/features/llm-tools/`) are small CRUD routers for reusable structured-output JSON schemas and tool definitions consumed by the Playground/evals.

---

## Subsystem 2 — PROMPT MANAGEMENT (DEEP)

**(a) Purpose:** Versioned prompt registry with labels, composition/dependencies, caching, and a public SDK-facing API.

**(b) Key files**
- Actions: `web/src/features/prompts/server/actions/createPrompt.ts` — `createPrompt` `:75` (type/variable-placeholder conflict checks `:99`, auto `latest` label `:111`, dependency graph build `:122`, transactional create `:204`, cache invalidation `:210`, change events `:219`); `duplicatePrompt` `:237`, `duplicateFolder` `:396`; `getPromptByName.ts`, `updatePrompts.ts`, `deletePrompt.ts`.
- Service/cache/composition: `packages/shared/src/server/services/PromptService/index.ts` — `getPrompt` `:49`, epoch-based `invalidateCache` `:179`, cache key with project epoch `:194-214`, `buildAndResolvePromptGraph` `:236` (max nesting depth `:19`/`:260`, circular-dep detection `:267`, `@@@langfusePrompt:...@@@` tag substitution `:359-373`).
- tRPC: `web/src/features/prompts/server/routers/promptRouter.ts`. Public REST: `web/src/pages/api/public/prompts.ts` (GET by name/version, POST legacy create, rate-limited via `RateLimitService`), `web/src/pages/api/public/v2/prompts/...` with `promptsHandler.ts`/`promptNameHandler.ts`/`promptVersionHandler.ts`.
- Domain: `packages/shared/src/domain/prompts.ts` (`PromptDomainSchema`). Labels: `web/src/features/prompts/server/utils/{updatePromptLabels,checkHasProtectedLabels,updatePromptTags}.ts`.
- Change events: `web/src/features/prompts/server/promptChangeEventSourcing.ts` → enqueues to **EntityChangeQueue** `:42` (entityType `"prompt-version"`).

**(c) Data flow**
- **Write:** `createPrompt` computes next `version` (max+1), forces unique labels (`latest`, optionally `production`), parses `@@@langfusePrompt@@@` dependency tags, validates the resolved dependency graph (depth ≤5, no cycles), then in one Postgres transaction creates the `Prompt` row + `PromptDependency` rows and **removes the moved labels from prior versions** (labels are unique per name). After commit it **rotates the project's cache epoch** and fires prompt-change events to EntityChangeQueue (→ webhook/slack automations, Subsystem 6).
- **Read (SDK):** `GET /api/public/prompts` → `getPromptByName` → `PromptService.getPrompt`. Cache lookup uses `prompt:<projectId>:<epoch>:<name>:<version|label>`. On miss, DB fetch + recursive dependency resolution, then cache `SET ... EX ttl`. `isActive` is derived from the `production` label.

**(d) Tradeoffs**
- **Epoch-token cache invalidation** (`invalidateCache` rotates a project-scoped token) is O(1) and avoids scanning/deleting many keys; old keys expire by TTL. Project-scoped (not prompt-scoped) because resolved prompts can transitively include other prompts.
- Labels-as-pointers (unique per name) make "production"/"latest" cheap to move but require multi-row updates on every publish.
- Recursive text substitution for composition is simple but bounded (depth 5) and text-only dependencies to keep resolution deterministic.

**(e) Lesson split:** **L1 — "Versioning, labels & the public API"** (version bumping, label uniqueness/protection, tags, REST contract, `isActive`). **L2 — "PromptService: caching & composition"** (epoch invalidation, dependency tags, graph resolution, change-event sourcing into EntityChangeQueue). *Prompt-experiments* bridge into Subsystem 3.

---

## Subsystem 3 — DATASETS & EXPERIMENTS (DEEP)

**(a) Purpose:** Curated dataset items + "runs" that execute a prompt/model (or external system) over items, producing dataset-run-items linked to traces for side-by-side comparison.

**(b) Key files**
- Web tRPC: `web/src/features/datasets/server/dataset-router.ts` (2434 lines — datasets/items/runs CRUD), `web/src/features/datasets/server/service.ts`, `createDataset.ts`, `publicDatasetService.ts`.
- Experiments tRPC: `web/src/features/experiments/server/router.ts` — `validateConfig` `:111`, `createExperiment` `:208` (creates `datasetRuns` row `:250`, enqueues **ExperimentCreateQueue** `:264-282`), `items`/`metrics`/comparison queries.
- Queue/processor: `worker/src/queues/experimentQueue.ts` — `experimentCreateQueueProcessor` (LLM-rate-limit retry on `dataset_runs.runId` `:24-36`).
- Worker core: `worker/src/features/experiments/experimentServiceClickhouse.ts` — `createExperimentJobClickhouse` `:287` (validate/setup `:306`, fetch items `:325`, per-item loop `:343`); `processItem` `:68` (emits `DATASET_RUN_ITEM_CREATE` ingestion event `:78-107`, then LLM call, then enqueues DatasetRunItemUpsert for evals `:134-149`); `processLLMCall` `:154` (variable substitution `:163`, internal-traced `fetchLLMCompletion` `:209`, observation-eval scheduling `:201-205`); `scheduleExperimentEvals.ts`.
- Shared: `packages/shared/src/server/repositories/dataset-run-items.ts` (ClickHouse reads: `getDatasetRunItemsCh` `:902`, `getDatasetRunsTableMetricsCh` `:500`, `getDatasetItemIdsByTraceIdCh` `:985`); `packages/shared/src/server/datasets/{schemaTypes,schemaValidation,executeWithDatasetServiceStrategy}.ts`; `packages/shared/src/domain/{dataset-items,dataset-run-items}.ts`; `packages/shared/src/server/dataset-run-items/addToDeleteQueue.ts`.

**(c) Data flow**
- **Create experiment:** UI calls `createExperiment` → creates a `datasetRuns` row in Postgres with `metadata` (prompt_id, provider, model, params, structured-output schema, dataset_version) → enqueues **ExperimentCreate**.
- **Run (worker):** `createExperimentJobClickhouse` validates the prompt+model+LLM key (config errors short-circuit into per-item error run-items), fetches not-yet-processed dataset items, and for each item: (1) emits a `DATASET_RUN_ITEM_CREATE` event through `processEventBatch` (ClickHouse via ingestion) with a **unified deterministic trace id** (`createW3CTraceId(runId-itemId)`), (2) substitutes item input into the prompt and runs `fetchLLMCompletion` (streamed into the user's project as a `langfuse-prompt-experiments` trace), (3) enqueues **DatasetRunItemUpsert** so evals can score the produced trace.
- **Compare:** Comparison tables read dataset-run-items + their linked traces/scores from ClickHouse via the `dataset-run-items` repository.

**(d) Tradeoffs**
- **DRI (dataset-run-item) migration to ClickHouse**: run-items are now written via ingestion to ClickHouse rather than Postgres; comment at `experimentServiceClickhouse.ts:364-366` notes deliberate write-inconsistency (config-error traces) accepted during migration.
- Deterministic trace IDs prevent duplicate traces across PG/CH and make experiments idempotent/resumable (skips already-processed items).
- Per-item sequential loop (`:343`) is simple and rate-limit-friendly but slower than parallel; failures isolated per item.
- Reuses the same trace→eval trigger path (DatasetRunItemUpsert) as production traces, so experiments get evaluators "for free."

**(e) Lesson split:** **L1 — "Datasets & items"** (dataset/item CRUD, schema validation, media in items, versioning via `validFrom`). **L2 — "Experiments end-to-end"** (run creation, ExperimentCreateQueue, per-item LLM execution, deterministic traces, run-item→eval handoff, comparison queries).

---

## Subsystem 4 — SCORES & ANNOTATION (DEEP)

**(a) Purpose:** The unified scoring model (numeric/categorical/boolean/text/correction) across three sources (API/EVAL/ANNOTATION), plus the human annotation workflow (queues, configs, comments, corrections).

**(b) Key files**
- Domain: `packages/shared/src/domain/scores.ts` — `ScoreSourceEnum` `:5` (API/EVAL/ANNOTATION), `ScoreDataTypeEnum` `:53` (NUMERIC/CATEGORICAL/BOOLEAN/CORRECTION/TEXT), discriminated `ScoreSchema` `:124`, `CORRECTION_NAME="output"` `:42`, annotation-requires-configId rule `:33`. Config domain: `packages/shared/src/domain/score-configs.ts` (`ScoreConfigCategory` `:5`, numeric/categorical/boolean field validation `:18-86`).
- Web tRPC: `web/src/server/api/routers/scores.ts` — `createAnnotationScore` `:485` (resolves trace/session existence in ClickHouse, dedups existing annotation, **direct `upsertScore`** `:584`), `updateAnnotationScore` `:616`, `deleteAnnotationScore` `:878`, `upsertCorrection` `:914`, `deleteMany` (batch) `:413`.
- Repository: `packages/shared/src/server/repositories/scores.ts` — `upsertScore` `:163` (→ `upsertClickhouse`, direct write), `getScoreById` `:128`, `deleteScores` `:1571`; converters in `scores_converters.ts`, `score-configs.ts`.
- Annotation queues: `web/src/features/annotation-queues/server/{annotationQueuesRouter,annotationQueueItemsRouter,annotationQueueAssignmentsRouter,publicAnnotationQueueService}.ts` (`createMany` `:280`, `complete` `:419`).
- Score analytics: `web/src/features/score-analytics/server/{scoreAnalyticsRouter,buildScoreComparisonQuery,buildEstimateQuery}.ts` (ClickHouse aggregation/heatmaps).
- Comments: `web/src/features/comments/server/publicCommentService.ts`, repo `packages/shared/src/server/repositories/comments.ts`. Corrections: `web/src/features/corrections/` (UI-side, stored as `CORRECTION` scores). Worker delete: `worker/src/features/scores/processClickhouseScoreDelete.ts`.

**(c) Data flow**
- **Scoring model:** every score is a discriminated union on `dataType`. Annotation scores **require a `configId`** (`isAnnotationScoreMissingConfigId`) that defines bounds/categories; corrections are a special `CORRECTION` score named `output`.
- **Annotation write path (direct):** `createAnnotationScore` verifies the target trace/session exists in ClickHouse, looks for an existing annotation to upsert, then calls `upsertScore` which writes **straight to the ClickHouse `scores` table** (`upsertClickhouse`) — bypassing the ingestion queue for immediate UI feedback. Audit-logged.
- **Annotation queues:** `createMany` adds items (or a batch-action query) to a queue; reviewers open items, submit scores against the queue's score-configs, and `complete` marks them done (`completedAt`).
- **EVAL vs API scores:** EVAL scores arrive via the ingestion queue (Subsystem 1); API scores via the public ingestion API — both land in the same `scores` table; analytics queries unify them by `source`.

**(d) Tradeoffs**
- **Direct ClickHouse write for annotations** (vs ingestion for EVAL/API) trades pipeline uniformity for low-latency human-in-the-loop UX; dedupe logic must search existing scores first.
- Single discriminated `scores` table with `source` keeps analytics uniform but pushes type-safety into Zod discriminated unions + config validation.
- Categorical/boolean configs store `categories` with value↔label mapping; boolean enforced to exactly 2 categories (`score-configs.ts:32`).

**(e) Lesson split:** **L1 — "The scoring model"** (data types, sources, score-configs, correction scores, where each source writes, ClickHouse schema, analytics/heatmaps). **L2 — "Human annotation workflow"** (annotation queues + items + assignments, direct-write upsert path, comments/reactions/mentions, batch enqueue).

---

## Subsystem 5 — PLAYGROUND & LLM CONNECTIONS (DEEP)

**(a) Purpose:** In-app multi-provider chat playground; secure storage/use of customer LLM provider credentials.

**(b) Key files**
- Playground: `web/src/features/playground/server/chatCompletionHandler.ts` (`:23` handler — auth `:24`, blocked-user check `:28`, key lookup `:50`, `LLMApiKeySchema` parse `:62`, `fetchLLMCompletion` with PostHog callback `:75`, structured-output vs tools branches); `validateChatCompletionBody.ts`, `authorizeRequest.ts`, `analytics/posthogCallback.ts`; UI `web/src/features/playground/page/`.
- LLM keys: `web/src/features/llm-api-key/server/router.ts` — `getDisplaySecretKey` `:47`, Bedrock/Vertex default-creds validation `:59-92`, `testLLMConnection` `:103`, `create` mutation with `encrypt(secretKey)` `:262-280`, extra-header encryption `:266-271`, `ENCRYPTION_KEY` presence guard `:247`.
- Encryption: `packages/shared/src/encryption/encryption.ts` — AES-256-GCM `encrypt` `:18` / `decrypt` `:36` (IV:cipher:authTag hex format), `keyGen` `:8`.
- Provider abstraction: `packages/shared/src/server/llm/fetchLLMCompletion.ts` — `decrypt(llmConnection.secretKey)` `:369`, `decryptAndParseExtraHeaders` `:370`, adapter switch building LangChain models (`ChatAnthropic` `:469`, `ChatOpenAI` `:491`, `AzureChatOpenAI` `:520`, `ChatBedrockConverse` `:541`, `ChatGoogle`/VertexAI `:567`), `resolveBedrockAuth` `:260`. Also `compileChatMessages.ts`, `secureLlmFetch.ts`, `baseUrlValidation.ts`, `googleSecureApiClient.ts`, `getInternalTracingHandler.ts`, `types.ts` (`LLMAdapter`, `LangfuseInternalTraceEnvironment`).

**(c) Data flow**
- **Store key:** `create` validates adapter-specific constraints, requires `ENCRYPTION_KEY`, then persists `llmApiKeys` row with `secretKey = encrypt(...)`, `extraHeaders = encrypt(JSON)`, plus a non-sensitive `displaySecretKey` (last 4 chars) for the UI. Bedrock/Vertex can use sentinel "default credentials" (self-hosted only).
- **Use key:** Playground `POST` → `chatCompletionHandler` authorizes the project, loads the matching `llmApiKeys` row by `provider`, parses via `LLMApiKeySchema`, and calls `fetchLLMCompletion`, which **decrypts the secret at call time** (never logged), builds the right LangChain chat model per `adapter`, attaches proxy/baseURL/extra-headers, and streams/returns. PostHog callback records playground analytics. Same `fetchLLMCompletion` powers evals and experiments.

**(d) Tradeoffs**
- **AES-256-GCM at rest** with authenticated encryption (IV+authTag) and decrypt-only-at-use minimizes secret exposure; `displaySecretKey` lets UI show a masked hint without decrypting.
- One unified `fetchLLMCompletion` (LangChain) abstracts five providers but concentrates provider-specific quirks (reasoning support, required user message, Bedrock/Vertex auth) into one large switch.
- Default-credentials sentinels are gated to self-hosted to avoid cross-tenant credential leakage on cloud.
- `secureLlmFetch`/`baseUrlValidation`/ip-blocking guard against SSRF via custom `baseURL`.

**(e) Lesson split:** **L1 — "LLM connections & encryption"** (key schema, AES-GCM encrypt/decrypt, displaySecretKey, adapter/default-creds validation, base-URL SSRF guards). **L2 — "The playground & fetchLLMCompletion"** (request validation, key resolution, the multi-adapter LangChain factory, structured output + tools, internal tracing, shared use by evals/experiments).

---

## Subsystem 6 — AUTOMATIONS & INTEGRATIONS (lighter)

**(a) Purpose:** React to entity changes / metric alerts by firing webhooks, Slack messages, or GitHub dispatches; periodically export trace data to PostHog/Mixpanel/blob storage.

**(b) Key files**
- Domain: `packages/shared/src/domain/automations.ts` — `TriggerEventSource` `:5`, `ActionTypeSchema` (WEBHOOK/SLACK/GITHUB_DISPATCH) `:43`, `WebhookActionConfigSchema` `:55`, `SlackActionConfigSchema` `:84`, `GitHubDispatchActionConfigSchema` `:93`. Repo: `packages/shared/src/server/repositories/automation-repository.ts`; helpers `packages/shared/src/server/automations.ts`, `webhooks/{validation,ipBlocking}.ts`.
- Web tRPC: `web/src/features/automations/server/{router,webhookHelpers,githubDispatchHelpers}.ts`.
- Trigger path: prompt changes → `promptChangeEventSourcing.ts` → **EntityChangeQueue** → `worker/src/features/entityChange/{entityChangeWorker,promptVersionProcessor}.ts` (`promptVersionProcessor` `:26`: loads ACTIVE triggers `:38`, `matchesTriggerFilter` `:53`, creates `automationExecution` row `:156`, enqueues **WebhookQueue** `:180`).
- Execution: `worker/src/queues/webhooks.ts` — `webhookProcessor` `:115`, `executeWebhook` `:127`, `executeWebhookAction` `:460` (HMAC signature via `decrypt(secretKey)` + `createSignatureHeader` `:528-531`, `executeHttpAction` `:541`), `executeGitHubDispatchAction` `:559`; monitor-alert envelope path `:86`/`:878`.
- Slack: `web/src/features/slack/server/{router,oauth-handlers,slack-webhook}.ts`; `packages/shared/src/server/services/SlackService.ts` (`WebClient` `:10`, OAuth install store `:129-287`, `SLACK_BOT_SCOPES` `:32`); worker `worker/src/features/slack/`.
- Integration queues (schedule→fan-out→per-project): `worker/src/queues/{postHogIntegrationQueue,mixpanelIntegrationQueue,blobStorageIntegrationQueue}.ts`, each with a `*Processor` (cron schedule) and `*ProcessingProcessor` (per-project); handlers in `worker/src/features/{posthog,mixpanel,blobstorage}/handle*IntegrationSchedule.ts` + `handle*IntegrationProjectJob.ts`.

**(c) Data flow**
- **Automations:** A trigger (prompt-version change via EntityChangeQueue, or a monitor metric alert via MonitorQueue) is matched against ACTIVE `trigger` rows; matching actions create an `automationExecution` (PENDING) and enqueue to **WebhookQueue**. The webhook processor dispatches by action type: WEBHOOK (signed HTTP POST, SSRF-guarded), SLACK (via SlackService WebClient using stored OAuth installation), or GITHUB_DISPATCH; execution status/response recorded.
- **Analytics/blob integrations:** A scheduled job fans out one processing job per enabled project; the per-project handler streams trace/observation data from ClickHouse, transforms it (`transformers.ts`), and ships to the destination (PostHog/Mixpanel API, or gzipped files to S3/GCS/Azure blob).

**(d) Tradeoffs**
- All action types funnel through one WebhookQueue for unified retry/observability.
- HMAC-signed payloads + per-action secret encryption + IP/URL blocking secure outbound calls.
- Schedule/processing two-tier queue pattern isolates per-project failures and parallelizes cleanly (same pattern reused by data-retention).

**(e) Lesson split:** **L1 — "Automations (triggers→actions)"** (trigger/action model, EntityChange + Monitor sources, WebhookQueue dispatch, signing, Slack OAuth, GitHub dispatch). **L2 — "Analytics & blob export integrations"** (schedule→per-project fan-out, ClickHouse streaming, transformers, destinations).

---

## Subsystem 7 — DASHBOARDS/WIDGETS & MODELS/PRICING (lighter)

**(a) Purpose:** Custom dashboards built from reusable widgets backed by a universal ClickHouse query engine; model-pricing/cost & usage computation.

**(b) Key files**
- Dashboards/widgets: `web/src/features/dashboard/server/dashboard-router.ts` (uses `executeQuery` from `@langfuse/shared/query/server` `:23`, calls at `:222`, `:285`, `:418-433`); UI `web/src/features/widgets/components/{DashboardWidget,WidgetForm,WidgetTable}.tsx`, `web/src/features/widgets/utils/{pivot-table-utils,import-export-utils}.ts`. Persistence: Prisma `DashboardWidget` model (`packages/shared/prisma/schema.prisma:1536`, chart types `:1524`).
- **Query engine:** `packages/shared/src/features/query/server/queryBuilder.ts` (`QueryBuilder` class), `queryExecutor.ts` (`prepareExecuteQuery` `:21` → `new QueryBuilder(...).build()` `:37-39`, `executeQuery` `:91` → `queryClickhouse`), `dataModel.ts` (views/dimensions/metrics), `validateQuery.ts`, `types.ts`. Service `packages/shared/src/server/services/DashboardService/`.
- Models/pricing: `web/src/features/models/server/publicApiModelService.ts`, `isValidPostgresRegex.ts`; seed `worker/src/constants/default-model-prices.json` (model `matchPattern` regex, `tokenizerConfig`, `pricingTiers[].conditions/prices`); seeding script `worker/src/scripts/upsertDefaultModelPrices.ts`. Matching/cost: `packages/shared/src/server/pricing-tiers/{matcher,index,types}.ts` (`matchPricingTier` `:88`, AND-condition eval `:59`, priority sort `:95`), `packages/shared/src/server/ingestion/modelMatch.ts` (`findModel`). **Cost computed at ingestion:** `worker/src/services/IngestionService/index.ts` — `findModel` `:1085`, `matchPricingTier` `:1102`, `calculateUsageCosts` `:1121`/`:1283`.

**(c) Data flow**
- **Widgets:** A `DashboardWidget` row stores a declarative query shape (view, dimensions, metrics, filters, chartType). The frontend calls the `dashboard.executeQuery` tRPC procedure → `QueryBuilder.build()` compiles parameterized ClickHouse SQL from the declarative `dataModel` → `queryClickhouse` runs it (v2 path) → results rendered (incl. pivot tables).
- **Cost/usage:** During trace/observation **ingestion**, IngestionService resolves the model via regex `findModel`, selects the applicable **pricing tier** by evaluating tier `conditions` against usage details (first match by ascending priority; default tier fallback), converts tier prices, and `calculateUsageCosts` writes `cost_details` onto the observation in ClickHouse. Dashboards then aggregate cost/tokens from ClickHouse.

**(d) Tradeoffs**
- A single declarative query model + universal `QueryBuilder` lets users compose arbitrary widgets without hand-written SQL, at the cost of a constrained metric/dimension vocabulary and a complex builder.
- **Pricing tiers** (priority-ordered, condition-gated) support volume/cached-token/context pricing but add matching complexity; cost is computed **once at ingestion** (denormalized onto observations) for fast dashboard aggregation rather than at query time.
- Regex model matching is flexible but order/precedence-sensitive (validated via `isValidPostgresRegex`).

**(e) Lesson split:** **L1 — "Custom dashboards & the universal query engine"** (widget persistence, dataModel views/dimensions/metrics, QueryBuilder→ClickHouse, pivot tables, import/export). **L2 — "Models, pricing tiers & cost computation"** (model regex matching, tiered prices, ingestion-time `calculateUsageCosts`, default-prices seeding).

---

## Subsystem 8 — BATCH EXPORTS / ACTIONS / MEDIA / DATA RETENTION (lighter)

**(a) Purpose:** Large table exports to files; bulk mutating actions over filtered selections; binary media handling; and time-based deletion of old data.

**(b) Key files**
- Batch exports: `web/src/features/batch-exports/server/batchExport.ts`; queue `worker/src/queues/batchExportQueue.ts` (`batchExportQueueProcessor` `:14`); worker `worker/src/features/batchExport/handleBatchExportJob.ts` (`:34`; status guards `:73-121`, paginated CH read stream `:197`, S3 upload + filename `:240-241`); read stream `worker/src/features/database-read-stream/getDatabaseReadStream.ts`.
- Batch actions: `web/src/features/batch-actions/server/{batchActionRouter,addToDatasetRouter,runEvaluationRouter}.ts`; queue `worker/src/queues/batchActionQueue.ts`; worker `worker/src/features/batchAction/handleBatchActionJob.ts` (`:149`; chunked processor `:62` switch over `trace-delete`/`*-add-to-annotation-queue`/`score-delete`/`dataset-delete` `:68-102`), plus `processAddObservationsToDataset.ts`, `processBatchedObservationEval.ts`, `processAddToQueue.ts`.
- Media: `web/src/features/media/server/{mediaService,getMediaStorageClient,datasetItemMediaReferences}.ts` (`createMediaUploadUrl` `:27` — sha256 dedup `:68`, presigned PUT URL `:99-122`); public API `web/src/pages/api/public/media/{index.ts,[mediaId].ts}`; worker cleaner `worker/src/features/media-retention-cleaner/`; repo `packages/shared/src/server/repositories/dataset-item-media.ts`; `media-deletion.ts`.
- Data retention: queue `worker/src/queues/dataRetentionQueue.ts` (`dataRetentionProcessor` schedule `:11`, `dataRetentionProcessingProcessor` per-project `:23`); EE handlers `worker/src/ee/dataRetention/{handleDataRetentionSchedule,handleDataRetentionProcessingJob}.ts`; cleaners `worker/src/features/batch-data-retention-cleaner/`, `deleted-mask-cleaner/`.
- Core-data S3 export: `worker/src/queues/coreDataS3ExportQueue.ts` (paginated multipart prompt export to S3 `:11-30`).
- Deletes: `worker/src/queues/{traceDelete,scoreDelete,datasetDelete,projectDelete}.ts`; `packages/shared/src/server/traceDeletionProcessor.ts`, `deletionGuard.ts`, `data-deletion/`.

**(c) Data flow**
- **Batch export:** UI creates a `batchExport` (Postgres, QUEUED) → BatchExport queue → worker marks PROCESSING, opens a **paginated ClickHouse read stream** for the table/filter, serializes to CSV/JSON, uploads to S3/blob, marks COMPLETED with the file URL (emails the user). 30-day expiry + cancellation guards.
- **Batch action:** A filtered selection (or explicit IDs) is chunked; each chunk is processed **idempotently** by action type (delete traces/scores/datasets, add to annotation queue, add observations to dataset, run evals on historical data). Idempotency matters because retries may reprocess chunks.
- **Media:** SDK requests an upload URL with a **sha256 hash**; `createMediaUploadUrl` dedups by `(projectId, sha256)` — returns existing `mediaId` (no upload) or a **presigned PUT URL** to object storage and links the media to its trace/observation/dataset-item. A retention cleaner removes unreferenced media.
- **Data retention:** Scheduled job fans out per-project processing jobs (same two-tier pattern as integrations) that delete ClickHouse/Postgres/blob data older than the project's retention window.

**(d) Tradeoffs**
- **Streaming + pagination** keeps memory bounded for huge exports/actions; chunked + idempotent design tolerates retries.
- Content-addressed (sha256) media gives automatic dedup and cheap "already uploaded" short-circuits; presigned URLs offload bytes directly to object storage (never through app servers).
- Schedule/processing fan-out (retention, integrations) localizes per-project failure and parallelizes; deletes are spread across dedicated queues with guards (`deletionGuard.ts`) to avoid accidental mass deletion.

**(e) Lesson split:** **L1 — "Batch exports & batch actions"** (export lifecycle, paginated CH read streams, file serialization/upload, chunked idempotent actions, run-evaluation backfill). **L2 — "Media & data lifecycle"** (sha256 dedup + presigned uploads, media references/cleanup, schedule→per-project retention deletion, the delete-queue family + guards, core-data S3 export).

---

### Suggested overall course shape (15 lessons)
1–2 Evals · 3–4 Prompts · 5–6 Datasets/Experiments · 7–8 Scores/Annotation · 9–10 Playground/LLM-connections · 11 Automations & monitors · 12 Analytics/blob integrations · 13 Dashboards/widgets/query-engine · 14 Models/pricing/cost · 15 Batch exports/actions/media/retention. (Add a **Lesson 0** on the web↔worker↔shared spine: tRPC, the BullMQ queue registry in `worker/src/app.ts`, the IngestionQueue, and the Postgres-vs-ClickHouse split — every later lesson references it.)
