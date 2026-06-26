# Ingestion & Storage source map

> Seed citations gathered during brainstorming (verify during M2/M3 authoring).

- ClickHouse wide-event tables (ReplacingMergeTree(event_ts,is_deleted), monthly partitions,
  ORDER BY project_id…id, bloom_filter indexes, ZSTD on input/output, Map columns for
  metadata/usage_details/cost_details):
  - `packages/shared/clickhouse/migrations/unclustered/0001_traces.up.sql`
  - `packages/shared/clickhouse/migrations/unclustered/0002_observations.up.sql`
  - `packages/shared/clickhouse/migrations/unclustered/0003_scores.up.sql`
  - event log: `0007_add_event_log.up.sql`; blob log: `0011_add_blob_storage_file_log.up.sql`;
    dataset run items: `0022_/0024_dataset_run_items.up.sql`; aggregating MTs: `0023_*`.
- Postgres (Prisma) models: `packages/shared/prisma/schema.prisma` (Organization, Project, ApiKey,
  Membership/Role, Prompt, Dataset/DatasetItem/DatasetRuns/DatasetRunItems, ScoreConfig,
  AnnotationQueue, Model/Price/PricingTier, EvalTemplate/JobConfiguration/JobExecution,
  *Integration, BatchExport/BatchAction, Media/*Media, LlmApiKeys, LlmSchema, SsoConfig, AuditLog).
- Queues (BullMQ): `packages/shared/src/server/queues.ts` (QueueName enum) — Ingestion (+secondary),
  OtelIngestion (+secondary), EvaluationExecution (+secondary, LLMAsJudge, CodeEval),
  DatasetRunItemUpsert, BatchExport, ExperimentCreate, {PostHog,Mixpanel,BlobStorage}Integration,
  CoreDataS3Export, DataRetention, BatchAction, Webhook, EntityChange, EventPropagation,
  Notification, Monitor, CloudUsageMetering/SpendAlert, deletes (Trace/Score/Project/Dataset).
- Worker services: `worker/src/services/IngestionService/*`, `worker/src/services/ClickhouseWriter/*`,
  `worker/src/queues/{ingestionQueue,otelIngestionQueue,shardedQueueRegistry}.ts`.
- Repositories: `packages/shared/src/server/repositories/*` (traces/observations/scores + converters).
