# Langfuse Internals — Visual Guide Map (Web App + Read Path)

Monorepo layout: `web/` (Next.js app), `worker/` (background jobs), `packages/shared/` (DB + ClickHouse + domain + query engine, imported as `@langfuse/shared`), `fern/` (API contract), `ee/` (enterprise). Storage tiers: **Postgres** (config/metadata via Prisma) + **ClickHouse** (analytical traces/observations/scores/events) + **Redis** (cache/queues) + **S3** (media/exports).

---

# PART A — WEB APP ARCHITECTURE
# PART A — WEB APP ARCHITECTURE

## Lesson 1 — Next.js surfaces & the `web/src` layout
**Purpose:** Understand what renders where; Langfuse is overwhelmingly **Pages Router**, with App Router used only for a few raw route handlers.

- **Pages Router (primary):** `web/src/pages/**`. UI routes live under `web/src/pages/project/[projectId]/...` (e.g. `traces/index.tsx`, `traces/[traceId].tsx`, `dashboards/[dashboardId]/index.tsx`, `sessions/[sessionId].tsx`, `observations/index.tsx`). API routes under `web/src/pages/api/**`.
- **App Router (minimal):** only 4 files — `web/src/app/layout.tsx` and 3 route handlers (`api/billing/stripe-webhook/route.ts`, `api/chatCompletion/route.ts`, `api/in-app-agent/route.ts`). Everything else is Pages Router.
- **`web/src` key dirs:** `features/` (vertical slices, ~80 features), `components/` (shared UI incl. `components/table/`), `server/` (auth + tRPC), `hooks/`, `utils/`, `ee/`.
- **Three API styles coexist:** (1) tRPC at `pages/api/trpc/[trpc].ts` for the UI; (2) REST at `pages/api/public/**` for SDKs; (3) a couple of App-Router handlers + one streaming SSE endpoint (`pages/api/dashboard/execute-query-stream.ts`).

**Tradeoff:** The app standardized on Pages Router + tRPC long before App Router maturity; App Router is reserved for endpoints needing raw `Request`/streaming/webhook semantics.

---

## Lesson 2 — The tRPC backbone (context, middleware, procedures, routers)
**Purpose:** The type-safe UI↔server contract. One root router aggregates ~64 feature routers; a small set of "procedure" builders enforce auth/RBAC.

**Key files:**
- Root router: `web/src/server/api/root.ts:70` — `appRouter = createTRPCRouter({...})` mounts 64 routers (imports `root.ts:1-63`). Exposed `AppRouter` type at `root.ts:136`.
- tRPC init/context/middleware: `web/src/server/api/trpc.ts`
  - Context: `createTRPCContext` `trpc.ts:57` → injects `{ session, headers, prisma }` (`createInnerTRPCContext` `:43`). Session from NextAuth `getServerAuthSession` (`web/src/server/auth.ts`).
  - Init w/ superjson + Zod error formatting + ClickHouse error tagging: `trpc.ts:103-124`.
  - `withErrorHandling` `:175` (maps errors, hides 5xx detail/stacks, special-cases `ClickHouseResourceError` → `UNPROCESSABLE_CONTENT` w/ advice `:179-192`).
  - `withOtelInstrumentation` `:218` (OTel baggage: surface=`trpc`, route, projectId).
  - **Procedure types:** `publicProcedure` `:249`; `authenticatedProcedure` `:272` (`enforceUserIsAuthed` `:252`); `protectedProjectProcedure` `:379` (`enforceUserIsAuthedAndProjectMember` `:288` — flattens `session.user.organizations→projects`, admin webhook path `:311-347`); `protectedOrganizationProcedure` `:464`; `protectedGetTraceProcedure` (via `enforceTraceAccess` `:483`, allows public traces, prefetches trace into `ctx.trace` using `getTraceById` `:503` with `verbosity` `:480`). Gates: `requireFeatureFlag(flag)` `:384`, `requireLangfuseCloud` `:401`.

**Main routers & what they serve** (`root.ts:71-132`): `traces`, `sessions`, `observations`, `generations`, `scores`/`scoreAnalytics`/`scoreConfigs`, `dashboard` + `dashboardWidgets`, `datasets`, `experiments`, `evals`/`monitors`/`automations`, `prompts`, `models`, `comments`/`commentReactions`, `annotationQueues*`, `media`, `batchExport`, `batchAction`, `table` + `TableViewPresets`, `public` (share links), `projects`/`organizations`/`members`/`users`, `projectApiKeys`/`organizationApiKeys`, `auditLogs`, `naturalLanguageFilters` + `searchBar`, `v4Transition`, plus integrations (posthog/mixpanel/blobstorage/slack/llmApiKey).

**Data flow:** React Query hook (`api.traces.all.useQuery`) → `pages/api/trpc/[trpc].ts` → middleware chain → router resolver → `@langfuse/shared` repository/service → ClickHouse/Postgres.

**Tradeoff:** `getRawInput()` is parsed in middleware to extract `projectId` *before* the handler runs, so RBAC is enforced uniformly without each router re-checking membership.

---

## Lesson 3 — Public REST API: route factory, versioning, auth/caching, Fern contract
**Purpose:** The stable SDK-facing surface. A single factory standardizes auth, rate-limit, Zod validation, OTel, and error contracts.

**The route factory** — `web/src/features/public-api/server/createAuthedProjectAPIRoute.ts`:
- Config type `:38` (querySchema/bodySchema/responseSchema, `rateLimitResource`, `allowedAccessLevels`, `isAdminApiKeyAuthAllowed`, `rejectInEventsOnlyMode` `:76-83`).
- Handler `:300`: rejects legacy-table routes in `events_only` mode `:312-321`; `verifyAuth` `:267` (regular API-key `:107` or self-hosted admin-key `:165`); rate limit `:368`; Zod-parse query/body `:391/:413`; runs `fn` inside OTel ctx (surface=`publicapi`) `:433-442`; validates response in dev `:453`; handles oversized JSON → `PayloadTooLargeError` `:471`.
- Wrapped by `withMiddlewares` (`features/public-api/server/withMiddlewares.ts`) for CORS + ClickHouse-resource error messaging.

**Resource endpoints** (`web/src/pages/api/public/**`): `traces/`, `observations/`, `sessions/`, `scores/` + `score-configs/`, `prompts.ts`, `datasets/` + `dataset-items/` + `dataset-run-items.ts`, `metrics/` (`daily.ts` + `index.ts`), `models/`, `comments/`, `annotation-queues/`, `media/`, `llm-connections/`, `organizations/` + `projects/`, `ingestion.ts` + `events.ts` + `generations.ts` + `spans.ts` (legacy ingest), `otel/v1/{traces,metrics}` (OTLP), `scim/`, `health.ts`/`ready.ts`, `mcp/`, `unstable/` (evaluators/evaluation-rules).

**Versioning** (folders encode versions): default = v1 at root; `v2/` (`observations`, `scores`, `prompts`, `datasets`, `metrics`); `v3/scores`. Example design rationale visible in `v3/scores/index.ts:7-24`: v3 drops `userId`/`traceTags` filters *because they require a trace JOIN* ("use v2"), and uses **cursor pagination** (`EncodedScoresCursorV3`). v1 metrics runs the QueryBuilder on legacy tables (`metrics/index.ts:19-21,34`), v2 metrics targets `events_full`.

**Auth + caching** — `web/src/features/public-api/server/apiAuth.ts`:
- `ApiAuthService.verifyAuthHeaderAndReturnScope` `:75` parses Basic (public+secret) / Bearer (public-only → `scores` access level).
- Redis cache: `fetchApiKeyAndAddToRedis` `:311` reads Redis first (resets TTL), falls back to Postgres by `fastHashedSecretKey`, then re-caches; negative caching with `API_KEY_NON_EXISTENT` `:117-123` to stop brute-force DB hits. (See `features/public-api/README.md`: key `api-key:<secret>:`, TTL reset on read, no update path → invalidate on delete.)

**Fern contract & codegen** — `fern/apis/{server,client,organizations}/definition/*.yml`:
- Contract is hand-written Fern YAML (e.g. `fern/apis/server/definition/trace.yml` defines GET/LIST/DELETE traces, the `fields` field-group param, and the giant `filter` JSON-string grammar doc `:74-120`).
- `fern/apis/server/generators.yml` generates the **Python SDK → `generated/python`** and **TS SDK → `generated/typescript`** (Fern generators v4.46 / v2.12). OpenAPI spec is exported to `web/public/generated/api/openapi.yml` (referenced in `api.yml`).

**Tradeoff:** REST handlers and Fern YAML are maintained in parallel (contract drift risk), but Zod response-validation in dev (`createAuthedProjectAPIRoute.ts:453`) catches mismatches early.

---

# PART B — QUERY / READ PATH
# PART B — QUERY / READ PATH

## Lesson 4 — The ClickHouse access layer (executor, tags, retries, look-back windows)
**Purpose:** Every analytical read funnels through a small set of executor functions with OTel spans, query tags, retries, and resource-error wrapping.

**Key files:** `packages/shared/src/server/repositories/clickhouse.ts`
- `queryClickhouse<T>()` `:639` — asserts no legacy-events read `:642`, OTel span w/ query text `:647`, exponential backoff retry on network errors `:649-694` (`isRetryableError` `:620`), wraps resource errors `:696`.
- `sendClickhouseQuery` `:580` — sets `clickhouse_settings.log_comment = JSON(tags)` `:600` (so every query carries `projectId`/surface/route tags for attribution), records CH summary headers onto span `:552`.
- Streaming variants: `queryClickhouseStream` `:249`, `queryClickhouseWithProgress` `:705` (used by SSE dashboards), `queryClickhouseExecRaw` `:405` (parquet/blob export), `commandClickhouse` `:755`.
- `ClickHouseResourceError` `:58` — memory/timeout guardrail surfaced to users with advice.
- `measureAndReturn` (`packages/shared/src/server/clickhouse/measureAndReturn.ts:25`) wraps a query fn in an `experiment-<op>` span; currently single-execution but designed for A/B/canary query rollouts (`:39-46`).

**Time-bounded scans (critical perf idea)** — `repositories/README.md`: traces↔observations↔scores live in separate CH tables joined by time-correlation, so reads use **look-back windows** instead of full scans: `OBSERVATIONS_TO_TRACE_INTERVAL` (~obs.start_time ≥ trace.timestamp − window; 98% within 5 min, 2-day cap), `SCORE_TO_TRACE_OBSERVATIONS_INTERVAL` (1h). These constants are injected into WHERE clauses (see Lesson 6).

**Tradeoff:** Correctness vs. cost — windows can miss extreme long-tail rows but keep joins from scanning months of partitions.

---

## Lesson 5 — Filters & orderBy → SQL (the two translation stacks)
**Purpose:** A single UI `FilterState` (array of typed conditions) compiles to either ClickHouse or Postgres SQL, always parameterized.

**ClickHouse stack** (`packages/shared/src/server/queries/clickhouse-sql/`):
- Filter classes implementing `Filter` interface: `clickhouse-filter.ts:20` — `StringFilter` `:36`, `DateTimeFilter`, `NumberFilter`, `StringOptionsFilter`, `CategoryOptionsFilter`, `ArrayOptionsFilter`, `BooleanFilter`, `NumberObjectFilter`/`StringObjectFilter` (metadata), `NullFilter`, `FilterList`. Each `apply()` emits `{query, params}` with random param names (`stringFilter<rnd>`) to prevent injection; metadata ngram-accelerated operators `:32-34`.
- Compiler: `factory.ts:37` `createFilterFromFilterState(filter, columnMapping, columnDefinitions)` — verifies each filter column against the CH schema (`matchAndVerifyTracesUiColumn` `:189`, `isValidTableName`), checks type compatibility (`COMPATIBLE_FILTER_TYPES`), switches on filter type → filter class. `getProjectIdDefaultFilter` `:217` seeds the mandatory `project_id` filters.
- OrderBy: `orderby-factory.ts` `orderByToClickhouseSql` / `orderByToEntries`. Search: `search.ts` `clickhouseSearchCondition` (ILIKE `%q%`) + full-text-search helpers `fts.ts`.
- Public-API mapping: `public-api-filter-builder.ts` (`createPublicApiTracesColumnMapping` `:88`, `convertApiProvidedFilterToClickhouseFilter`, `deriveFilters`) maps SDK query params/`filter` JSON → CH filters.

**Postgres stack** (parallel, for Prisma-backed tables like evals/audit/scoresTable defs):
- `packages/shared/src/server/filterToPrisma.ts:25` `tableColumnsToSqlFilterAndPrefix` / `tableColumnsToSqlFilter` (operator map `:8-21`, returns `Prisma.Sql`).
- `packages/shared/src/server/orderByToPrisma.ts:15` `orderByToPrismaSql` (defaults `ORDER BY t.timestamp DESC`).

**Shared abstraction:** both consume `FilterState` + `ColumnDefinition`/`UiColumnMappings` (`packages/shared/src/tableDefinitions/*`, `server/tableMappings/*`) and require **zod-verified inputs** (explicit security comments).

**Tradeoff:** The UI label ("User ID") vs internal id ("userId") dual lookup (`orderByToPrisma.ts:24`) is flagged as tech-debt; mapping tables are the single source of truth that keeps SQL decoupled from UI strings.

---

## Lesson 6 — The trace list read model (compact rows vs. lazy metrics)
**Purpose:** The flagship list query. One generic function serves four "shapes" so the table paints fast and defers expensive aggregation.

**Key file:** `packages/shared/src/server/services/traces-ui-table-service.ts`
- `getTracesTableGeneric(props)` `:206` with `select: "count" | "rows" | "metrics" | "identifiers"` (`:164`, type-safe overloads `:185-204`).
- Builds default + user filters (`getProjectIdDefaultFilter` + `createFilterFromFilterState`) `:222-231`; **propagates the trace-id and timestamp filters down into the scores/observations CTEs** to prune before join `:233-269` (uses `OBSERVATIONS_TO_TRACE_INTERVAL` `:308`, `SCORE_TO_TRACE_OBSERVATIONS_INTERVAL` `:337`).
- **Conditional joins:** `requiresScoresJoin` / `requiresObservationsJoin` `:271-280` — only LEFT JOIN the `observations_stats`/`scores_avg` CTEs when a filter/orderBy needs them or `select==="metrics"` `:456-457`.
- **FINAL tradeoff** (explicit comment `:443-448`): default ordering = `toDate(timestamp), event_ts DESC` + `LIMIT 1 BY id` (no `FINAL`) so CH reads only the latest partition and dedups in memory; non-default ordering falls back to `FROM traces t FINAL` `:455`. OTel/immutable-span projects skip dedup entirely (`shouldSkipObservationsFinal` `:220`).
- `select:"count"` uses `uniqExact(t.id)` `:359` for correct pagination counts.
- Public wrappers: `getTracesTableCount` `:491`, `getTracesTableMetrics` `:512`, `getTracesTable` (rows) `:529`, `getTraceIdentifiers` `:564`. Compact row type = 12 trace columns only (`TracesTableReturnType` `:33`); metrics type carries cost/latency/level counts/score aggregates (`TracesTableMetricsClickhouseReturnType` `:147`).

**Data flow:** UI → tRPC `traces.all` (rows) + `traces.metrics` (metrics) in parallel → `getTracesTableGeneric` → CTE+join SQL → `queryClickhouse`.

**Tradeoff (the central lesson):** **compact list model** (cheap, always-needed columns) is decoupled from **metrics** (cost/latency/scores requiring 2 joins). The table renders rows immediately; metrics stream in and are merged client-side (Lesson 11).

---

## Lesson 7 — tRPC traces router → service, and the v4 "events" unification
**Purpose:** How the UI's table view orchestrates the split queries, applies comment filters, and the ongoing migration to a single `events` table.

**Key file:** `web/src/server/api/routers/traces.ts`
- `all` `:129` → `getTracesTable` (rows). `countAll` `:163` → `getTracesTableCount`. `metrics` `:196` → `getTracesTableMetrics` + `getScoresForTraces` then `aggregateScores` `:271-276` (metrics keyed by the already-fetched `traceIds` `:241-253`).
- `applyCommentFilters` `:138/:172/:207` resolves Postgres comment filters to a trace-id set, short-circuits with `hasNoMatches` `:145`, and intersects ids — a nice example of **cross-store (PG↔CH) filtering**.
- `filterOptions` `:278` (distinct names/tags for facets). Detail procedures in Lesson 8.
- Search sanitation: `sanitizeLegacyTracingSearch` `:132` + `normalizeOrderByForTable` `:154`.

**The v4 unified `events` table:** `packages/shared/src/server/repositories/events.ts` (95 KB) is the new read model — `getTraceById` `:1073` (dispatcher), `getTraceByIdFromEventsTable` `:944`, `getObservationsForTraceFromEventsTable` `:404`, and **public-API readers** `getTracesFromEventsTableForPublicApi` `:1735` / `getObservationsV2FromEventsTableForPublicApi` `:1446`. The big event query compiler is `queries/clickhouse-sql/event-query-builder.ts` (60 KB). Routes toggle between legacy traces table and events table via `query.useEventsTable` (e.g. `pages/api/public/traces/index.ts:133`) and the server-side beta flag snapshot.

**Tradeoff:** During migration both code paths exist (legacy `traces`/`observations`/`scores` tables vs unified `events`/`events_full`). `rejectInEventsOnlyMode` (Lesson 3) prevents serving stale data from legacy tables once a deployment is `events_only`.

---

## Lesson 8 — Trace detail + trace-graph-view (full fetch vs compact)
**Purpose:** The detail page deliberately fetches *everything* for one trace — the opposite end of the compact-list tradeoff.

**Key files:**
- `web/src/server/api/routers/traces.ts`: `byId` `:348` (returns `ctx.trace` already prefetched by `enforceTraceAccess` w/ `verbosity` `:355`), `byIdWithObservationsAndScores` `:368` — parallel `getObservationsForTrace` + `getScoresAndCorrectionsForTraces` `:385-397`, derives latency from observation start/end spans `:410-426`, splits CORRECTION scores via `partition` `:405`.
- **Verbosity** levels `"compact" | "truncated" | "full"` (`trpc.ts:480`, `byId:355`) control whether IO is parsed/truncated server-side — caps payload for huge traces.
- Agent graph: `getAgentGraphData` (router `:610`) → `getAgentGraphDataFromEventsTable` (`events.ts:2183`); client builders in `web/src/features/trace-graph-view/` (`buildGraphCanvasData.ts`, `buildStepData.ts`, `components/TraceGraphCanvas.tsx`), types/schema `types.ts`.

**Data flow:** trace page (`pages/project/[projectId]/traces/[traceId].tsx`) → `traces.byIdWithObservationsAndScores` (tree + scores) + `traces.getAgentGraphData` (graph) → events/CH.

**Tradeoff:** Full detail fetch is acceptable for one trace (bounded), but IO is returned **unparsed/optionally truncated** to bound memory; observation IO is *not* fetched in the tree call (`:440-441`) and lazy-loaded per node.

---

## Lesson 9 — Dashboards & widgets: the declarative query engine
**Purpose:** Custom dashboards/metrics are powered by a semantic-layer query model (views→dimensions/measures) compiled to ClickHouse SQL — not hand-written per chart.

**Key files** (`packages/shared/src/features/query/`):
- **Model/contract** `types.ts`: `viewDeclaration` `:9` (baseCte, dimensions, measures, tableRelations, segments, timeDimension, rootEventCondition); `views` enum `:85` (`traces`, `observations`, `scores-numeric`, `scores-categorical`); `QueryType` `query` `:167` (view, dimensions[], metrics[{measure,aggregation}], filters[], `timeDimension.granularity`, `entityDimension`, from/to, orderBy, chartConfig). Aggregations `:108`, granularities incl. monitor windows `:146`. Mutual-exclusion + cardinality guard comments `:180-220`.
- **View definitions** `dataModel.ts` (1505 lines): e.g. `traceView` `:13` maps logical dims/measures → CH SQL (`traces.user_id`, etc.), per `ViewVersion` (v1 legacy tables / v2 events).
- **Compiler** `server/queryBuilder.ts`: `class QueryBuilder` `:119`, `build()` `:1517` — maps dims/measures, validates filters `:319`, builds joins (with per-relation `FINAL` skip for OTEL) `:775-797`, time bucketing/`WITH FILL` `:949-1252`, single-level optimization `:735`. FINAL handling `:1533-1546` (events table never needs FINAL).
- **Executor** `server/queryExecutor.ts`: `prepareExecuteQuery` `:21` (compiles, routes to `EventsReadOnly` CH pool if query touches `events_core/events_full` `:49-54`, sets `max_bytes_before_external_group_by`, optional query-condition-cache `:58-66`); `executeQuery` `:91`.
- **UI binding** `web/src/features/widgets/hooks/useWidgetQuery.ts:110` — builds `QueryType` from `WidgetConfig`, picks v1/v2 (`requiresV2` `:120`, beta toggle `:133`), enforces top-N for breakdown charts `:152`, maps legacy UI filters→view fields `:176`, then `validateQuery` `:202`.
- **Exposure:** tRPC `dashboard` router (`web/src/features/dashboard/server/dashboard-router.ts:23` imports `executeQuery`) + REST `pages/api/public/metrics/index.ts:34` (`executeQuery`) + **SSE streaming** `pages/api/dashboard/execute-query-stream.ts` (`text/event-stream`, `:25-42`/`:122-128`; `queryClickhouseWithProgress` `:144`; v4-only `:108`).

**Tradeoff:** A semantic layer (vs ad-hoc SQL) gives validation, cardinality guards, and reuse, at the cost of a 1700-line compiler. High-cardinality `entityDimension` requires callers to pre-filter (`types.ts:180-189`) or risk OOM `GROUP BY`.

---

## Lesson 10 — Search bar grammar, filter state, and AI filters
**Purpose:** A keyboard-driven `key:value` query language over the same `FilterState`, plus optional LLM-generated filters — all converging on one source of truth.

**Key files** (`web/src/features/search-bar/` — read `README.md`):
- **Single source of truth = URL `FilterState`** (facet sidebar `useSidebarFilterState`) + `searchQuery/searchType`; the bar is a *controlled editor* that derives committed text and never stores a second copy (README "Data flow", one effect `resetTo`).
- Grammar: `lib/langQ.ts` (serialize/parse), `lib/ast.ts`, `lib/completions.ts`, `lib/fields.ts`, `lib/adapter.ts`; **reverse adapter** `lib/filter-state-to-query.ts:1` (FilterState→text, round-trips, reports `skipped` for non-grammar filters like `positionInTrace`). Hook `hooks/useEventsSearchBar.ts`; store `store/searchBarStore.ts`.
- Full-text search lowers to CH `ILIKE %q%` (`clickhouse-sql/search.ts`); scopes `id`/`content` (README "Full-text search").
- **AI filter generation** `server/router.ts:45` `searchBar.generateFilter` — builds prompt from the v4 field registry (`buildFilterPrompt.ts`), calls Bedrock, then **round-trips model output through `filterStateToQueryText` and drops any hallucinated/non-representable column** `:178-191` (cloud-only, entitlement-gated). Legacy equivalent: `web/src/features/natural-language-filters/server/router.ts:26` (uses a remotely-managed Langfuse prompt targeting old columns).

**Tradeoff:** Grammar intentionally mirrors only what flat `FilterState` can express; unsupported shapes (cross-field OR, groups) become **commit-blocking diagnostics, not silent drops**. AI output is validated by construction (round-trip), so it can never inject an unknown column.

---

# PART C — CROSS-CUTTING UI / TABLE SYSTEM
# PART C — CROSS-CUTTING UI / TABLE SYSTEM

## Lesson 11 — The list/table system (how it stays fast)
**Purpose:** A reusable `DataTable` plus a family of state hooks gives every list consistent filtering, sorting, pagination, column control, presets, and peek — while keeping queries compact.

**Key files & concepts:**
- **Core+metrics merge:** `web/src/components/table/utils/joinTableCoreAndMetrics.ts:1` — joins compact rows with lazily-loaded metrics by `id`, returning `success` even when metrics absent (`:17-27`), so the grid paints from `traces.all` before `traces.metrics` resolves. (Controller: `components/table/use-cases/traces.tsx`.)
- **Column visibility/order:** `web/src/features/column-visibility/hooks/useColumnVisibility.ts` + `useColumnOrder.ts`; UI `components/table/data-table-column-visibility-filter.tsx`. Persisted per table.
- **Table view presets** (saved views): `components/table/table-view-presets/README.md` — persists column visibility/order + filters + orderBy + search via **URL `viewId` (sharing) + session storage (nav) + DB (permanent)**, with permalinks and **graceful degradation** (invalid columns/filters dropped + warning toast; deleted view → defaults). Server: `packages/shared/src/server/services/TableViewService/`, types `domain/table-view-presets.ts`, tRPC `routers/tableViewPresets.ts`.
- **Filters UI/state:** `web/src/features/filters/` — `hooks/useSidebarFilterState.tsx` (canonical), `useFilterState.ts`, `lib/filter-query-encoding.ts` (URL codec), `config/*-config.ts` per table; `components/table/data-table-ai-filters.tsx`.
- **Peek (detail-in-panel) state:** `components/table/peek/README.md` — `PeekTableStateProvider` persists table state across K/J navigation while only `key={itemId}` content remounts; peek-aware hooks (`usePaginationState`, `useFullTextSearch`, `useOrderByState`) auto-detect peek; `useSidebarFilterState` wired explicitly.
- **Global time range:** `web/src/features/global-time-range/README.md` — Zustand `globalDateRangeStore` (per-project default, persisted) ⊕ URL `?dateRange` (explicit), resolved by pure `resolveTimeRange` XOR; consumed via `useTableDateRange`/`useDashboardDateRange`. The time range becomes the mandatory `timestamp` filter that bounds CH scans (ties to Lessons 4/6).
- **Selection stores (large feature pattern):** `web/src/features/tracing-tables/README.md` — per-mount vanilla Zustand `observationsTableStore.ts:38` owns row selection / select-all / page-row derivation; passed to shared `DataTable`/`TableSelectionManager` explicitly via `selectionStore` prop so nested tables (scores in a peek) don't collide. Generic store: `components/table/table-selection-store.ts`.
- **Pagination:** token/cursor in public API (`v3/scores` `EncodedScoresCursorV3`); page/offset in tRPC list queries (`paginationZod`).

**Tradeoff:** Heavy use of URL/session/Zustand layering keeps tables shareable and remount-safe, but state ownership is split across many hooks (the READMEs exist precisely to document those boundaries).

---

## Lesson 12 — Batch exports & batch actions (enqueue → stream → S3)
**Purpose:** Large reads (export "all rows", run-eval-on-all, add-to-dataset) never run in the request; they're enqueued and streamed by the worker.

**Key files:**
- **Enqueue (tRPC):** `web/src/features/batch-exports/server/batchExport.ts:23` `create` — RBAC + entitlement checks, **snapshots `v4BetaEnabled` into the persisted query** so the worker reads from a dispatch-time snapshot `:38-42`, then pushes a `BatchExportQueue` job. Batch actions: `web/src/features/batch-actions/server/batchActionRouter.ts` (+ `addToDatasetRouter.ts`, `runEvaluationRouter.ts`); generic `createBatchActionJob` (`features/table/server/`).
- **Worker (the actual export):** `worker/src/features/batchExport/handleBatchExportJob.ts:34` — guards (S3 enabled `:37`, cancelled `:72`, >30d stale `:80`), selects a **paginated DB read stream** per table (`getDatabaseReadStreamPaginated` `:197`; events/traces/observations variants `:175-197`), `pipeline()`s rows through `streamTransformations[format]()` (CSV/JSON/JSONL) `:220-223`, **buffered multipart upload to S3** (`StorageServiceFactory` `:263`, `uploadFileBuffered` `:265`, part size `BATCH_EXPORT_S3_PART_SIZE_MIB`), then emails a time-limited signed link `:265-311`.
- Types live in `@langfuse/shared`, logic in worker (`features/batch-exports/README.md`).

**Data flow:** UI "Export" → tRPC enqueue (Redis/BullMQ) → worker streams ClickHouse/Postgres → S3 → signed URL email.

**Tradeoff:** Streaming + pagination + multipart upload bounds worker memory for arbitrarily large exports; the v4-flag snapshot avoids races where a user's live flag changes mid-job.

---

## Suggested lesson ordering for the guide
1. Surfaces & repo layout → 2. tRPC backbone → 3. Public REST + Fern → 4. ClickHouse access layer → 5. Filter/orderBy→SQL → 6. Trace list read model → 7. Trace router + v4 events → 8. Trace detail + graph → 9. Dashboard query engine → 10. Search bar + AI filters → 11. Table system/cross-cutting state → 12. Batch exports/actions.

Recurring **design themes** to thread through every lesson: (a) one `FilterState`/`ColumnDefinition` abstraction → many SQL backends; (b) compact list vs. full/metrics fetch; (c) time-bounded CH scans + look-back windows + conditional `FINAL`; (d) zod-verified, parameterized inputs everywhere; (e) URL-as-source-of-truth for table state; (f) heavy reads deferred to the worker + streaming.
