# Langfuse Internals — Visual Guide Source Map

Monorepo: pnpm workspaces (`web`, `worker`, `packages/**`, `ee`) orchestrated by Turbo. Version 3.199.0, Node 24. Three runtime tiers: **web** (Next.js UI + REST/tRPC), **worker** (BullMQ background processing), **packages/shared** (Prisma, ClickHouse, Redis, S3, auth, instrumentation shared by both).

---

## AREA 1 — AUTH & MULTI-TENANCY

**(a) Purpose:** User authentication (NextAuth + SSO + credentials), API-key auth for the public API, and a two-level Organization→Project tenancy model with role-based access.

**(b) Key files**
- `web/src/server/auth.ts` — NextAuth config (1137 lines). Providers `:24-39, :69-150`; JWT session strategy `:742-744`; **session callback** `:747-938`; **signIn callback** `:939+`; Prisma adapter `:1050`; `getServerAuthSession` `:1120`.
- `web/src/features/auth-credentials/lib/credentialsServerUtils.ts` — bcrypt `hashPassword`/`verifyPassword`; `signupApiHandler.ts`, `server/credentialsRouter.ts`.
- `packages/shared/src/server/auth/apiKeys.ts` — key generation/hashing (`:13` bcrypt `hashSecretKey`, `:19` `generateKeySet`, `:31` `createShaHash`, `:41` `createAndAddApiKeysToDb`).
- `web/src/features/public-api/server/apiAuth.ts` — `ApiAuthService.verifyAuthHeaderAndReturnScope` `:75`; Basic-auth path `:92-198`; Bearer path `:200-244`.
- `packages/shared/src/server/auth/userProjectRoleAuth.ts:6-19` — `resolveProjectRole` (project role overrides org role).
- `web/src/features/rbac/constants/projectAccessRights.ts` / `organizationAccessRights.ts` — scope lists + `Role→scopes[]` maps.
- `web/src/server/api/trpc.ts:288-381` — `enforceUserIsAuthedAndProjectMember` + `protectedProjectProcedure`; `:416-466` org procedure.
- `packages/shared/prisma/schema.prisma` — `Organization:95`, `Project:124`, `ApiKey:193`, `OrganizationMembership:323`, `ProjectMembership:340`, `MembershipInvitation:358`, `Role enum:379`.
- `web/src/pages/api/public/scim/Users/index.ts` — SCIM provisioning.

**(c) How it works**
- **Login:** `staticProviders` includes `CredentialsProvider` (email/password, bcrypt) plus ~14 OAuth/SSO providers (Google, GitHub, Okta, Azure AD, Keycloak, WorkOS, Auth0, Cognito…). Sessions are **JWT** (`strategy:"jwt"`, `maxAge = AUTH_SESSION_MAX_AGE*60`). The **session callback** (`auth.ts:747`) re-queries Postgres on each call, loading `organizationMemberships → organization → projects` + `ProjectMemberships`, and projects each org/project into `session.user.organizations[].projects[]` with an **effective role** computed by `resolveProjectRole` and filtered to projects where the role grants `project:read`. It also injects `plan` per org and `selfHostedInstancePlan` into `session.environment`.
- **Tenancy model:** `Organization 1—* Project`. Users join an org via `OrganizationMembership` (carries an org-level `Role`); a `ProjectMembership` (keyed `@@id([projectId,userId])`, linked to the org membership) optionally **overrides** the role for a single project. `resolveProjectRole` returns the project-specific role if present, else the org role. SQL version with priority/hierarchy in `userProjectRoleAuth.ts:43-96`.
- **API keys:** `generateKeySet` mints `pk-lf-<uuid>` / `sk-lf-<uuid>`. DB stores three derivatives (`apiKeys.ts:61-75`): `hashedSecretKey` (bcrypt, cost 11), `fastHashedSecretKey` (SHA-256 of secret + salted-SHA-256, via `createShaHash`), and `displaySecretKey` (`sk-lf-…abcd`). **Verification** (`apiAuth.ts`): Basic auth → compute SHA-256 fast hash → Redis cache lookup → Postgres fast-hash lookup; legacy keys without a fast hash fall back to bcrypt `compare` then **lazily upgrade** to a fast hash (`:141-150`). Returns a `scope` with `projectId/orgId/plan/accessLevel`. **Bearer** auth = public key only → `accessLevel:"scores"` (limited). `ApiKeyScope` is `PROJECT` or `ORGANIZATION`.
- **RBAC enforcement:** scopes are `resource:action` strings (e.g. `prompts:CUD`, `traces:delete`); `projectRoleAccessRights[Role]` lists allowed scopes for OWNER/ADMIN/MEMBER/VIEWER/NONE. tRPC `protectedProjectProcedure` validates project membership and injects `orgId/orgRole/projectId/projectRole` into ctx; resolvers call `throwIfNoProjectAccess` (`checkProjectAccess.ts:28`). UI mirrors with `useHasProjectAccess`. `admin:true` users bypass everything (with `sendAdminAccessWebhook` audit). REST routes enforce via `createAuthedProjectAPIRoute`→`verifyApiKeyAuth` (`:107-147`) which checks `allowedAccessLevels`.
- **SCIM:** `/api/public/scim/Users` requires an **organization-scoped** API key (`accessLevel:"organization"`) and is gated by the `admin-api` entitlement (`index.ts:62-73`); supports user CRUD + membership management (used for IdP provisioning).

**(d) Tradeoffs**
- JWT sessions but a **DB read on every `session()`** — trades token-self-containment for always-fresh roles/plan (latency + DB load, wrapped in OTel span).
- Dual key hashing: bcrypt is slow-but-safe for storage; SHA-256 fast hash + Redis makes per-request auth cheap. Lazy migration avoids a backfill but means mixed-state rows.
- Project role override design is powerful but requires the two-query UNION (`userProjectRoleAuth.ts`) to list members correctly.

**(e) Lessons:** **Lesson 1 — "Who are you?" Authentication & sessions (NextAuth, SSO, credentials, JWT session callback).** **Lesson 2 — "What can you touch?" Multi-tenancy & RBAC (org/project/membership model, scopes, tRPC/REST enforcement, API keys, SCIM).**

---

## AREA 2 — EE / ENTITLEMENTS / LICENSING

**(a) Purpose:** Gate enterprise/cloud features by *plan* (entitlements) while keeping commercial code legally isolated under a separate license.

**(b) Key files**
- `ee/src/ee-license-check/index.ts` — `isEeAvailable` (`:3-5`, cloud region OR `LANGFUSE_EE_LICENSE_KEY`). `ee/src/env.ts`, `ee/src/index.ts` (empty barrel), package `@langfuse/ee`.
- `packages/shared/src/server/ee/licenseCheck/index.ts:11-26` — `isEnterpriseLicenseAvailable` (cloud OR key prefix `langfuse_ee_`; **pro doesn't count**).
- `packages/shared/src/features/entitlements/plans.ts` — `planLabels` (8 plans), `Plan` type, `isCloudPlan/isSelfHostedPlan/isPlan`.
- `web/src/features/entitlements/server/getPlan.ts` — `getOrganizationPlanServerSide` (cloudConfig.plan/stripe `:9-55`), `getSelfHostedInstancePlanServerSide` (license prefix → `self-hosted:enterprise|pro` `:57-67`).
- `web/src/features/entitlements/constants/entitlements.ts` — `entitlements[]`, `entitlementLimits[]`, and the **`entitlementAccess: Record<Plan,{entitlements,entitlementLimits}>`** matrix (`:54-182`).
- `web/src/features/entitlements/server/hasEntitlement.ts` / `hasEntitlementLimit.ts` (server); `hooks.ts` (`usePlan`, `useHasEntitlement`, `useEntitlementLimit`).
- EE code: `web/src/ee/features/*` (admin-api, billing, multi-tenant-sso, sso-settings, ui-customization, verified-domains, in-app-agent, audit-log-viewer, sfdc-sync) and `worker/src/ee/*` (cloudUsageMetering, cloudSpendAlerts, dataRetention, usageThresholds). `ee/LICENSE`.
- `web/src/features/feature-flags/available-flags.ts` + `trpc.ts:384 requireFeatureFlag`; `web/src/features/feature-previews/*`.

**(c) How it works**
- **Plans → entitlements:** `Plan` is one of `oss`, `cloud:{hobby,core,pro,team,enterprise}`, `self-hosted:{pro,enterprise}`. The org's plan is derived server-side: on **Cloud** from `organization.cloudConfig.plan` or the Stripe product id; **self-hosted** from the license-key prefix (`langfuse_ee_`→enterprise, `langfuse_pro_`→pro), else `oss`. Plan is baked into the JWT (per-org `plan` + `environment.selfHostedInstancePlan`).
- **Gating:** `entitlementAccess` maps each plan to a set of binary `Entitlement`s (e.g. `rbac-project-roles`, `audit-logs`, `data-retention`, `cloud-multi-tenant-sso`, `admin-api`, `prompt-protected-labels`, `in-app-agent`) and numeric `EntitlementLimit`s (`organization-member-count`, `data-access-days`, `annotation-queue-count`, `monitor-count`…, where `false` = unlimited). `hasEntitlement`/`throwIfNoEntitlement` (server) and `useHasEntitlement` (client) check membership; `admin` users always pass.
- **Two gating mechanisms coexist:** *entitlements* (per-org plan, fine-grained feature/limit) vs *license availability* (`isEnterpriseLicenseAvailable`, coarse on/off for whole EE subsystems like multi-tenant SSO).
- **Legal isolation:** all commercial logic lives in `/ee` folders (separate `ee/LICENSE`); MIT core only references it through narrow server functions (comments in `auth.ts:825-826, :923-924` warn against inlining). `@langfuse/ee` has no MIT license field.
- **Feature flags vs previews vs entitlements:** flags (`available-flags.ts`, per-user, `requireFeatureFlag` middleware + experimental override) are for staged rollouts; feature previews are user-opt-in modals; entitlements are billing/plan-driven.

**(d) Tradeoffs**
- Plan→entitlement matrix is a **static table** (no DB lookup) → simple, fast, but plan changes require code edits/redeploys (acceptable since plans change rarely).
- License-key *prefix* parsing (no cryptographic signature visible here) keeps self-hosting friction low but is weak DRM by design (honor-system + cloud enforcement).
- Splitting "is EE available" (binary) from "entitlements" (granular) means two code paths to reason about.

**(e) Lessons:** **Lesson 3 — Open-core economics: Plans, entitlements, license keys, and the `/ee` boundary (cloud vs self-hosted gating; feature flags vs previews vs entitlements).**

---

## AREA 3 — CONFIG & ENVIRONMENT / DEPLOYMENT TOPOLOGY

**(a) Purpose:** Validate all configuration via Zod at process start and define the multi-service deployment.

**(b) Key files**
- `packages/shared/src/env.ts` — `EnvSchema` (516 lines), `env = DOCKER_BUILD?process.env:EnvSchema.parse(removeEmptyEnvVariables(process.env))` (`:513-516`). Validates Redis/TLS (`:33-73`), `ENCRYPTION_KEY` must be 64 hex chars (`:74-80`), S3, EE license (`:488`), ingestion masking (`:490-508`).
- `web/src/env.mjs` — `@t3-oss/env-nextjs createEnv` (`:40`), server/client split, SSO provider env schemas (`:4-38`).
- `worker/src/env.ts` (567 lines) — worker/queue/ClickHouse config.
- `.env.dev.example`, `.env.prod.example`, `.env.test.example`, `.env.dev-azure/oci/redis-cluster.example`.
- `docker-compose.yml` (prod-like) + `docker-compose.dev.yml` (infra only) + build/azure/redis-cluster variants.

**(c) How it works**
- Every service imports a typed `env` whose module-eval **throws on invalid/missing config** (fail-fast). `DOCKER_BUILD=1` bypasses parsing during image builds (env not yet present). Empty strings are stripped to let defaults apply.
- **Topology** (`docker-compose.yml`): `langfuse-web` (`langfuse/langfuse:3`, port 3000) + `langfuse-worker` (`langfuse/langfuse-worker:3`, 3030) + **Postgres 17** (OLTP: orgs/projects/users/keys/prompts/configs) + **ClickHouse** (OLAP: traces/observations/scores events) + **Redis 7** (BullMQ queues, caches, rate limits) + **MinIO/S3** (event blobs, media, exports). Dev compose (`docker-compose.dev.yml`) runs ClickHouse 25.12, MinIO, Redis 7.2.4, Postgres, plus `floci`, expecting web/worker to run on host.
- `.env.dev.example` wires `DATABASE_URL`, `CLICKHOUSE_URL`, `REDIS_*`, three S3 buckets (event/media/batch-export), `NEXTAUTH_SECRET`, `SALT`, `NEXT_PUBLIC_LANGFUSE_CLOUD_REGION="DEV"`.

**(d) Tradeoffs**
- Zod-at-boot gives strong guarantees but means many env vars must be set correctly (large surface; mitigated by defaults + example files).
- Splitting OLTP (Postgres) from OLAP (ClickHouse) + blob store + queue is operationally heavy for self-hosters but essential for trace-volume scale.

**(e) Lessons:** **Lesson 4 — Configuration as a contract & the five-engine topology (Zod env validation; web/worker/postgres/clickhouse/redis/s3; docker-compose variants; self-host config).**

---

## AREA 4 — OBSERVABILITY OF LANGFUSE ITSELF

**(a) Purpose:** Self-instrument the platform with OpenTelemetry traces, structured logs, and metrics (Datadog/CloudWatch).

**(b) Key files**
- `packages/shared/src/server/instrumentation/index.ts` — `instrumentAsync/instrumentSync` (`:54,:98`), `traceException` (`:142`), `addUserToSpan` (`:191`, baggage), `recordGauge/Increment/Histogram/Distribution` (`:328-368`), CloudWatch batching (`:265-307`), `ioredisRequestHook` (`:17`, secret redaction), `convertQueueNameToMetricName` (`:376`).
- `packages/shared/src/server/logger.ts` — winston; `tracingFormat` (`:6-25`) injects `dd.trace_id/span_id`+baggage; JSON vs text via `LANGFUSE_LOG_FORMAT` (`:48`).
- `worker/src/instrumentation.ts` — `NodeSDK` + OTLP proto exporter (`:40`), instrumentations for ioredis/http/undici/express/prisma/aws/winston/bullmq (`:43-101`), `dd.init({runtimeMetrics:true})` (`:22`), resource detectors.
- `packages/shared/src/server/otel/*` — `OtelIngestionProcessor` (ingest, not self-obs).

**(c) How it works**
- Code wraps units of work in `instrumentAsync({name},async span=>…)` which starts an OTel active span, supports `startNewTrace`/`traceContext` propagation, copies baggage→span attributes, and auto-records exceptions. `addUserToSpan` stamps `user.id/langfuse.project.id/org.id/org.plan/api_key.id` onto both the span **and baggage** so downstream spans + logs inherit tenant context. Worker boots `instrumentation.ts` first (`index.ts:1`), starting a `NodeSDK` exporting OTLP to `OTEL_EXPORTER_OTLP_ENDPOINT/v1/traces` with auto-instrumentation of HTTP/Redis/Prisma/Express/BullMQ; health checks are filtered out. Logs are winston JSON (prod) with injected trace ids for log↔trace correlation. Metrics go to Datadog dogstatsd and optionally CloudWatch (`ENABLE_AWS_CLOUDWATCH_METRIC_PUBLISHING`).

**(d) Tradeoffs**
- Datadog-shaped trace ids in logs (`dd.trace_id`) couples format to DD but works generically. Dual metric sinks (dogstatsd + CloudWatch) add config branches. `ioredisRequestHook` must manually redact API-key cache values — a maintenance burden but prevents secret leakage into spans.

**(e) Lessons:** **Lesson 5 — Observing the observability platform (OTel spans, baggage-based tenant context, structured logging with trace correlation, Datadog/CloudWatch metrics).**

---

## AREA 5 — BUILD / TEST / DEV WORKFLOW

**(a) Purpose:** Coordinate builds/tests/migrations across the workspace and provide one-command dev bootstrapping + deterministic seed data.

**(b) Key files**
- Root `package.json` scripts: `dx`/`dx-f` (infra up + DB resets + seed + dev), `dev`/`build`/`typecheck`/`lint`/`test` (all `turbo run …`), `seed`→`pnpm --filter=shared run seed:scenario`.
- `turbo.json` — `build` dependsOn `db:generate`+`^build`; `db:generate` **cache:false** (Prisma writes into node_modules); `dev` persistent; `typecheck`/`lint`/`test` cached.
- `pnpm-workspace.yaml` — members `web,worker,packages/**,ee`; `minimumReleaseAge:7200` (supply-chain delay); pinned `overrides`.
- `vitest.workspace.ts` = `["web","worker"]`. `web/package.json` test projects: `server, server-isolated, server-unit, in-source, client, storybook, e2e-server` + Playwright `test:e2e`. `worker` vitest.
- Seed: `packages/shared/scripts/seeder/` (`cli.ts`, `seed-postgres.ts`, `seed-clickhouse.ts`, `scenarios/*.ts`); shared scripts `db:seed`, `db:seed:examples`, `ch:seed`, `ch:reset`.
- Background migrations: `web/src/features/background-migrations/server/background-migrations-router.ts` (`denyOnLangfuseCloud`); `worker/src/backgroundMigrations/` (`backgroundMigrationManager.ts`, `IBackgroundMigration.ts`, `migrate{Traces,Observations,Scores,DatasetRunItems}FromPostgresToClickhouse*.ts`, `encryptBlobStorageSecrets.ts`). Tracked in Prisma `backgroundMigration` table.

**(c) How it works**
- Turbo builds the dependency graph: `^build` ensures `packages/shared` compiles before `web`/`worker`; `db:generate` (Prisma client) runs first and is never cached so node_modules side-effects always materialize on fresh CI. `dx` does: install → reset infra → `pnpm-filter shared db:reset(:test)` + `ch:reset` + `db:seed:examples` → `dev`.
- **Tests** are layered: web splits server vs client vs in-source vs storybook vs e2e; worker has its own vitest suite (with an LLM-connection carve-out). Playwright covers browser e2e.
- **Seeding:** Postgres seed (`prisma db seed`) + ClickHouse seed + scenario-based generator (`seed:scenario` → CLI with scenarios like `many-traces`, `long-session`, `scored-traces`, `trace-tree`) for realistic load/test data.
- **Background migrations** are long-running data moves (notably Postgres→ClickHouse backfills) run by the worker's `backgroundMigrationManager`, surfaced in the UI router; disabled on Cloud (Cloud is migrated centrally).

**(d) Tradeoffs**
- Turbo caching accelerates CI but Prisma generate had to be explicitly **un-cached** (comment in `turbo.json`) — a sharp edge. The seeder's scenario system adds code but yields reproducible perf/test data. Background migrations decouple schema evolution from data movement at the cost of operational tracking.

**(e) Lessons:** **Lesson 6 — The monorepo machine: Turbo/pnpm task graph, build/typecheck/lint pipeline, and the `dx` one-command bootstrap.** **Lesson 7 — Testing & data lifecycle: vitest project layout, Playwright e2e, the scenario seeder, and Postgres→ClickHouse background migrations.**

---

## AREA 6 — SDK / INTEGRATION SURFACE (entry points)

**(a) Purpose:** Accept telemetry from external SDKs/OTel, expose a generated public API, anonymous product telemetry, and an MCP server for AI assistants.

**(b) Key files**
- `web/src/pages/api/public/ingestion.ts` — native batch ingestion (validate→S3→queue→sync fallback, `processEventBatch`, `:38-53`).
- `web/src/pages/api/public/otel/v1/traces/index.ts` — OTLP traces (protobuf/JSON, `OtelIngestionProcessor.publishToOtelIngestionQueue` `:173-189`); `otel/v1/metrics/index.ts`; proto root `otel/otlp-proto/generated/root.ts`.
- `fern/apis/{server,client,organizations}/definition/*.yml` — API contracts (auth `basic`, `api.yml`); `fern/apis/server/generators.yml` → **fern-python-sdk** + **fern-typescript-node-sdk** output to `fern/apis/generated/{python,typescript}`; OpenAPI at `web/public/generated/{api,api-client,organizations-api}/openapi.yml`.
- `web/src/features/telemetry/index.ts` — anonymous self-host usage → PostHog (`:20-53`).
- `web/src/pages/api/public/mcp/index.ts` — MCP server endpoint; `web/src/features/mcp/*` (tools for prompts, datasets, annotation queues, comments…).

**(c) How it works**
- **Ingestion in:** SDKs POST event batches to `/api/public/ingestion` (Basic auth). The handler authenticates, rate-limits, validates, **uploads each event to S3** as durable cache, enqueues to BullMQ for the worker, and falls back to synchronous processing on queue errors. OTel SDKs/collectors POST OTLP to `/api/public/otel/v1/traces`; the route decodes protobuf/JSON, reads `x-langfuse-sdk-name/version/ingestion-version` headers to pick a write path, marks the project an OTel user, and publishes to the OTel ingestion queue. The worker consumes these queues (`worker/src/queues/ingestionQueue.ts`, `otelIngestionQueue.ts`) and writes to ClickHouse.
- **Public API + Fern:** API surface is defined declaratively in Fern YAML (server, browser client, organizations admin) and the Fern generators emit the Python/TS SDKs and OpenAPI specs that the SDKs/users consume — single source of truth for REST contracts (Basic auth, `X-Langfuse-Sdk-*` headers).
- **Telemetry (self-obs of installs):** a 12-hour cron (`telemetry()`) sends anonymized counts to PostHog; **disabled** on Cloud, CI, dev, and when `TELEMETRY_ENABLED=false` (unless EE).
- **MCP:** stateless-per-request server over Streamable HTTP; authenticates with project-scoped Basic-auth keys, rate-limits, builds a `ServerContext`, and exposes Langfuse tools (prompts/datasets/etc.) to Claude/Cursor.

**(d) Tradeoffs**
- S3-first ingestion + async queue decouples write latency from ClickHouse and gives replayability, at the cost of eventual consistency and a sync fallback path to maintain. Fern codegen guarantees client/server parity but adds a generation step. Stateless MCP (fresh server per request) simplifies scaling but precludes server-side session state.

**(e) Lessons:** **Lesson 8 — Getting data in: native + OTLP ingestion, the S3→queue→ClickHouse pipeline.** **Lesson 9 — The contract surface: Fern-generated public API/SDKs + OpenAPI; product telemetry; the MCP server for AI assistants.**

---

## Suggested 8–12 Lesson Arc
1. Authentication & sessions (NextAuth/SSO/credentials/JWT). 2. Multi-tenancy & RBAC (org/project/membership, scopes, API keys, SCIM). 3. Open-core gating (plans/entitlements/license, `/ee`). 4. Config & topology (Zod env, 5-engine docker-compose). 5. Self-observability (OTel/logging/metrics). 6. Monorepo build system (Turbo/pnpm, `dx`). 7. Testing & data migrations (vitest/Playwright/seeder/bg-migrations). 8. Ingestion pipeline (native+OTLP→S3→queue→ClickHouse). 9. Public API & SDK surface (Fern, telemetry, MCP). *(Optionally split 2 and 8 for 10–11 lessons.)*

All findings cite concrete files/lines above; let me know which area you want expanded into per-file walkthroughs for the guide.
