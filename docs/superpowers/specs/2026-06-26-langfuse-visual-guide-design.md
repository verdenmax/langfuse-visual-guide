# Langfuse Visual Guide — Design Spec / 设计规格

**Date:** 2026-06-26
**Status:** Approved (autonomous execution granted by @verdenmax)
**Author:** @verdenmax (driven autonomously by the agent)

## 1. Purpose / 目的

A **visual, bilingual (中文 + English)** learning guide that explains the **internals of
[Langfuse](https://github.com/langfuse/langfuse)** — the open-source **LLM engineering / observability
platform** (Next.js + TypeScript monorepo, backed by Postgres + ClickHouse + Redis + S3). The guide
takes a reader from *"what is LLM observability"* all the way to *"how the ingestion / query paths
work inside the code"* and *"how to build, test and contribute a PR"*.

It is modeled **directly** on the two sibling projects `~/course/milvus-visual-guide` and
`~/course/hermes-agent-visual-guide`: same zero-dependency Python-generator architecture, the same
visual design system, the same per-lesson pedagogy (life analogy → macro picture → diagrams → cited
code → self-test quiz), the same bilingual in-page toggle, and the same GitHub-Pages delivery.

### Audience & depth / 受众与深度
- Primary: engineers who want to **understand Langfuse internals** and eventually **contribute**.
- Starts from first principles (what is LLM observability, the wide-event model, traces /
  observations / scores) so a motivated newcomer can follow.
- Builds up to deep internals: the **ingestion (write) path** (SDK → public API → Redis queue →
  worker `IngestionService` → `ClickhouseWriter`), the **storage layer** (ClickHouse wide events +
  Postgres metadata + S3 event log), the **read / query path** (tRPC + repositories + ClickHouse),
  and the major **feature subsystems** (evals, datasets/experiments, prompt management, playground,
  dashboards, automations), plus auth/RBAC, EE/entitlements, ops, and the contribution workflow.

### Non-goals / 非目标
- Not a user manual / API reference (langfuse.com/docs already does that). We cite the SDK and public
  API only as the **entry points** into the internals.
- Not a fork or mirror of Langfuse source. We **quote small, cited snippets only** (with `file:line`
  attribution) and explain them.
- Not cloud-operations documentation: we explain stable, public, in-repo architecture, **not**
  private production topology, account details, secret names, or incident runbooks.

### Hard quality bar / 硬性质量底线
Every lesson's technical claims and code snippets MUST correspond to the **real Langfuse source**
(cited as `path:line`), **never AI-invented**. Each milestone ends with an **audit** that verifies
(a) content completeness, (b) SVG correctness/rendering, and (c) source-fidelity (citations actually
exist and say what the lesson claims). This bar is non-negotiable and is the spine of the workflow.

## 2. Architecture (tech) — cloned from the references, retargeted to Langfuse

Pure **Python 3, zero runtime dependencies**. Generators under `src/` emit committed static HTML.

```
langfuse-visual-guide/
  src/
    part1.py .. partN.py    bilingual lesson content; one module per Part; each exports
                            LESSON_NN = {"zh": <html>, "en": <html>}
    quizzes.py              per-lesson self-test (mcq + open); deterministic option shuffle
    shell.py                CSS design system + PAGES list + bi()/esc()/head_meta() + page()/index_page()
    registry.py             ordered filename -> content map (single source of truth)
    build.py                builds index.html + lessons/*.html
    build_print.py          builds print_zh.html + print_en.html (one page per lesson)
    check_html.py           structural HTML validation (CI gate)
    check_links.py          internal link validation (CI gate)
  lessons/        generated lesson pages (committed, kept in sync)
  index.html      generated table of contents (committed)
  print_*.html    generated print editions (committed)
  docs/superpowers/{specs,plans}/   design spec + per-milestone specs/plans
  .github/workflows/{ci,deploy}.yml build+validate gate and GitHub-Pages deploy
  LICENSE (MIT, code) + LICENSE-CONTENT (CC BY 4.0, lessons)
```

The infrastructure (`shell.py` CSS/JS, `build*.py`, `check_*.py`) is copied from
`milvus-visual-guide` (the richer component set) and retargeted: branding/favicon, the `PAGES`
list, the language-toggle function names (`mvg*` → `lvg*`), `MAX_LESSON`, and the index/landing
copy. The CSS design system and bilingual mechanism are reused near-verbatim.

## 3. Curriculum / 课程大纲 — 55 lessons, 11 parts

One Part = one `partN.py` module = one milestone (small parts are grouped). Lessons are numbered
L01–L55. Each row lists the lesson and its primary in-repo source anchors (verified during the
milestone's deep-dive; the maps in `docs/superpowers/plans/source-maps/` seed them).

### Part 1 · 宏观全景 · The Big Picture (L01–L05)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L01 | 什么是 Langfuse | What is Langfuse | `README.md`, `web/`, `worker/`, `packages/shared/` |
| L02 | 可观测性 2.0 与宽事件 | Observability 2.0 & wide events | `.agents/ARCHITECTURE_PRINCIPLES.md` |
| L03 | 三大支柱：trace / observation / score | The three pillars | `packages/shared/src/domain/{traces,observations,scores}.ts` |
| L04 | 项目全景地图（monorepo 与窄腰） | Project map (monorepo & narrow waist) | `pnpm-workspace.yaml`, `turbo.json`, `AGENTS.md` |
| L05 | 一条 trace 的一生·鸟瞰 | Life of a trace (bird's-eye) | ingestion→storage→read overview |

### Part 2 · 前置基础 · Foundations (L06–L11)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L06 | 给 LLM 应用埋点（OTel/span/generation） | Instrumenting an LLM app | SDK/OTel entry; `web/src/pages/api/public/otel/*` |
| L07 | 双存储架构（PG·CH·Redis·S3） | The dual-store architecture | `packages/shared/src/server/{clickhouse,redis,s3}/*`, `db.ts` |
| L08 | ClickHouse 与宽事件表 | ClickHouse & the wide-event tables | `packages/shared/clickhouse/migrations/unclustered/0001-0003*` |
| L09 | 元数据 schema（Postgres/Prisma） | The metadata schema (Postgres) | `packages/shared/prisma/schema.prisma` |
| L10 | 多租户：org → project → environment | Multi-tenancy | Prisma `Organization`/`Project`; `environments.ts` |
| L11 | 部署拓扑与依赖 | Deployment topology | `docker-compose*.yml`, `.env.*.example` |

### Part 3 · 摄取链路 · The Ingestion / Write Path (L12–L19)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L12 | 摄取 API（/ingestion·批·鉴权·Zod） | The ingestion API | `web/src/pages/api/public/ingestion.ts` |
| L13 | 事件类型与合并语义 | Event types & the merge model | `packages/shared/src/server/ingestion/*` |
| L14 | 摄取队列（BullMQ·分片·S3 事件日志） | The ingestion queue | `queues.ts`, `worker/src/queues/ingestionQueue.ts`, `shardedQueueRegistry.ts` |
| L15 | IngestionService（合并聚合） | The IngestionService | `worker/src/services/IngestionService/*` |
| L16 | Token 计数与成本计算 | Token counting & cost | `IngestionService/calculateTokenCost*`, `worker/src/features/tokenisation/*` |
| L17 | ClickhouseWriter（批量·upsert） | The ClickhouseWriter | `worker/src/services/ClickhouseWriter/*` |
| L18 | OpenTelemetry 摄取 | OpenTelemetry ingestion | `web/src/pages/api/public/otel/*`, `worker/src/queues/otelIngestionQueue.ts` |
| L19 | 媒体与 blob 存储 | Media & blob storage | `web/src/features/media/*`, `s3/*`, CH `0011_add_blob_storage_file_log` |

### Part 4 · 查询链路 · The Read / Query Path (L20–L27)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L20 | web 应用架构（Next.js·Pages·三种 API） | The web app architecture | `web/src/pages/**`, `web/src/app/*` |
| L21 | tRPC 骨架（context·中间件·procedure） | The tRPC backbone | `web/src/server/api/{root,trpc}.ts` |
| L22 | 仓储层：从 ClickHouse 读 | The repository layer | `packages/shared/src/server/repositories/*` |
| L23 | 过滤·搜索栏·查询构建 | Filtering & the search bar | `web/src/features/{filters,search-bar}/*`, `filterToPrisma.ts` |
| L24 | 列表与表格（compact·分页·预设） | Lists & tables | `web/src/features/{tracing-tables,table}/*`, `components/table/*` |
| L25 | trace 详情与观测树 | Trace detail & the observation tree | `web/src/features/{traces,trace-graph-view}/*` |
| L26 | sessions | Sessions | `web/src/server/api/routers/sessions.ts`, `trace-sessions.ts` |
| L27 | 公共 REST API（路由工厂·版本·Fern） | The public REST API | `web/src/features/public-api/server/createAuthedProjectAPIRoute.ts`, `fern/apis/*` |

### Part 5 · 评估与评分 · Evaluation & Scoring (L28–L33)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L28 | 评分模型（数值/分类/布尔·score config） | The scoring model | `packages/shared/src/domain/{scores,score-configs}.ts` |
| L29 | LLM-as-a-judge（模板·evaluator·变量提取） | LLM-as-a-judge | `web/src/features/evals/*`, `shared/src/server/evals/*` |
| L30 | eval 执行流水线（job·队列） | The eval execution pipeline | `worker/src/features/evaluation/*`, `worker/src/queues/evalQueue.ts` |
| L31 | 代码 eval（Lambda/本地 dispatcher） | Code evals | `shared/src/server/evals/{awsLambda,local}CodeEval*`, `worker/src/queues/codeEvalQueue.ts` |
| L32 | 人工标注（annotation queue·comments） | Human annotation | `web/src/features/{annotation-queues,comments,corrections}/*` |
| L33 | 监控器与告警（monitors） | Monitors & alerting | `web/src/features/monitors/*`, `worker/src/queues/monitorQueue.ts` |

### Part 6 · 数据集与实验 · Datasets & Experiments (L34–L36)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L34 | 数据集与数据项 | Datasets & items | `web/src/features/datasets/*`, Prisma `Dataset`/`DatasetItem` |
| L35 | dataset run 与 run item | Dataset runs & run items | `shared/src/server/repositories/dataset-run-items*`, CH `dataset_run_items` |
| L36 | 实验与对比 | Experiments & comparison | `web/src/features/experiments/*`, `worker/src/queues/experimentQueue.ts` |

### Part 7 · Prompt 管理与 Playground · Prompts & Playground (L37–L39)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L37 | Prompt 管理（版本·label·依赖） | Prompt management | `web/src/features/prompts/*`, `shared/src/domain/prompts.ts`, Prisma `Prompt`/`PromptDependency` |
| L38 | Prompt 服务与缓存 | Prompt serving & caching | `web/src/pages/api/public/prompts.ts`, prompt cache |
| L39 | Playground 与 LLM 连接（加密·schema·tool） | Playground & LLM connections | `web/src/features/{playground,llm-api-key,llm-schemas,llm-tools}/*`, `shared/src/server/llm/*` |

### Part 8 · 仪表盘·指标·成本 · Dashboards, Metrics & Cost (L40–L43)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L40 | 仪表盘/widget 系统 | Dashboards & widgets | `web/src/features/{dashboard,widgets}/*`, `dashboardWidgets.ts` |
| L41 | 查询引擎（features/query·聚合） | The query engine | `packages/shared/src/features/query/*` |
| L42 | 模型与定价 | Models & pricing | `web/src/features/models/*`, `shared/src/server/pricing-tiers/*`, `worker/src/constants/default-model-prices.json` |
| L43 | 云用量计量与花费 | Cloud usage metering & spend | `worker/src/queues/{cloudUsageMetering,cloudSpendAlert}Queue.ts` |

### Part 9 · 自动化与集成 · Automation & Integrations (L44–L47)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L44 | 自动化与 webhook | Automations & webhooks | `web/src/features/automations/*`, `worker/src/queues/webhooks.ts`, `shared/src/server/webhooks/*` |
| L45 | Slack 与通知 | Slack & notifications | `web/src/features/slack/*`, `worker/src/queues/notificationQueue.ts` |
| L46 | 分析集成（PostHog·Mixpanel·blob 导出） | Analytics integrations | `worker/src/queues/{postHog,mixpanel,blobStorage}IntegrationQueue.ts` |
| L47 | 批量导出与批量操作 | Batch exports & actions | `web/src/features/{batch-exports,batch-actions}/*`, `worker/src/queues/{batchExport,batchAction}Queue.ts` |

### Part 10 · 平台与运维 · Platform & Operations (L48–L53)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L48 | 鉴权与会话（NextAuth·SSO） | Auth & sessions | `web/src/features/{auth,auth-credentials}/*`, `web/src/server/auth.ts` |
| L49 | RBAC·API key·SCIM | RBAC, API keys, SCIM | `web/src/features/rbac/*`, `shared/src/server/auth/apiKeys*`, `web/src/pages/api/public/scim/*` |
| L50 | 开源核与权益（EE·entitlement·license） | Open-core & entitlements | `ee/src/*`, `web/src/features/entitlements/*`, `shared/src/server/ee/*` |
| L51 | 自我可观测·配置（OTel·日志·env） | Self-observability & config | `shared/src/server/{instrumentation,otel}/*`, `logger.ts`, `env.ts` |
| L52 | 数据生命周期与删除（保留·删除·后台迁移） | Data lifecycle & deletion | `worker/src/queues/{dataRetention,traceDelete,projectDelete}.ts`, `backgroundMigrations/*` |
| L53 | 构建·测试·开发流（pnpm/turbo·vitest·seed） | Build, test & dev workflow | `package.json`, `turbo.json`, `packages/shared/scripts/seeder/*` |

### Part 11 · 设计专题与终章 · Design Themes & Capstone (L54–L55)
| # | 中文 | English | Primary source anchors |
| --- | --- | --- | --- |
| L54 | 设计专题综合（宽事件·不可变·异步·双存储·多租户·成本） | Design themes synthesis | cross-cutting; `.agents/ARCHITECTURE_PRINCIPLES.md` |
| L55 | 终章·一条 trace 的完整一生 | Capstone: the full life of a trace | end-to-end synthesis of L05–L53 |

## 4. Design system & per-lesson pedagogy / 设计系统与每课范式

The CSS design system is reused from `milvus-visual-guide/src/shell.py` (the richer component set):
light + dark theme via CSS variables; bilingual toggle via `html[data-lang]`. Component vocabulary
available to lesson HTML:

- **Callout cards:** `.card.macro` (蓝·宏观), `.card.detail` (紫·源码细节), `.card.analogy`
  (琥珀·生活类比), `.card.key` (主色·本课要点), `.card.warn` (红·坑/陷阱), `.card.spark` (设计取舍 🎯).
- **Code:** `.codefile` (带 `path:line` 头) and `pre.code` with `.cm/.kw/.fn/.st/.nb` token spans.
- **Schematics (HTML, count toward the visual-block minimum):** `.flow` / `.vflow` / `.layers` /
  `.cols` / `table.t` / `.cellgroup` / `.timeline` / `.trace`.
- **Hand-drawn figures:** `.fig` + inline `<svg viewBox=…>` + `.figcap`. SVG fills/strokes MUST use
  CSS variables (`var(--blue)`, `var(--accent-soft)`, …) and text inherits `var(--ink)` so figures
  theme correctly in light AND dark mode. **This is where the "尽量多画 SVG" requirement lives.**
- **Quiz:** `.selftest` + `.quiz` (rendered by `quizzes.py`).

Each lesson follows the proven arc:
1. `<p class="lead">` — one-paragraph hook framing the problem.
2. `.card.analogy` — a concrete life analogy (🔌).
3. Macro picture — an SVG / `.flow` / `.layers` overview before details.
4. Body sections (`<h2>`) — each pairs prose with a diagram and **cited real code** (`.codefile`
   with `path:line`). Design tradeoffs go in `.card.spark` (🎯).
5. `.card.key` — "本课要点 / Key points".
6. Self-test quiz (`quizzes.py`): 3–5 design-insight MCQs (with `why`) + 1–2 open questions.

**Per-lesson quantitative floor** (enforced/encouraged by `check_html.py`, tightened for this guide):
- ≥ ~4000 CJK chars in zh (authoring target; soft floor 3000).
- ≥ 6 HTML visual blocks (≥ 3 per language) AND **≥ 2 hand-drawn `.fig` SVGs per language**
  (new `MIN_SVGS` check added — see §6).
- key-points card + analogy card present; bilingual parity; nav chain intact.

## 5. Milestone roadmap / 里程碑路线图

Each milestone runs the full loop: **write M-spec → write M-plan → subagent execution → audit →
fix → commit**. Milestones map to parts (small parts grouped). One `partN.py` module per part.

| M | Scope | Lessons | Module(s) |
| --- | --- | --- | --- |
| **M0** | Infrastructure & design system: scaffold repo, retarget `shell.py` (branding, `PAGES`, `lvg*` toggle, `MAX_LESSON`), `build*.py` / `check_*.py` (+ `MIN_SVGS`), README, CI/deploy, index builds clean; ship **L01** as the visual baseline. | L01 | part1 |
| **M1** | Part 1 · 宏观全景 (finish) | L02–L05 | part1 |
| **M2** | Part 2 · 前置基础 | L06–L11 | part2 |
| **M3** | Part 3 · 摄取链路 | L12–L19 | part3 |
| **M4** | Part 4 · 查询链路 | L20–L27 | part4 |
| **M5** | Part 5 · 评估与评分 | L28–L33 | part5 |
| **M6** | Parts 6+7 · 数据集/实验 + Prompt/Playground | L34–L39 | part6, part7 |
| **M7** | Parts 8+9 · 仪表盘/成本 + 自动化/集成 | L40–L47 | part8, part9 |
| **M8** | Part 10 · 平台与运维 | L48–L53 | part10 |
| **M9** | Part 11 · 设计专题与终章 + 全局打磨（print/covers/README 终稿） | L54–L55 | part11 |

Sequencing rationale: foundations before paths; the **write path (M3)** before the **read path
(M4)** because reads query what writes produce; feature subsystems (M5–M7) build on both paths;
platform/ops (M8) is cross-cutting; synthesis/capstone (M9) last so it can reference everything.

## 6. Audit process / 审计流程 — the quality spine

Every milestone ends with a **mandatory audit** before commit. The audit has automated gates plus
subagent reviews. Nothing merges with a failing automated gate or an unresolved source-fidelity
finding.

### 6.1 Automated gates (must be green)
- `python3 build.py && python3 build_print.py` — regenerate site + print editions, no error.
- `python3 check_html.py` — 0 ERROR (structural: tag balance, single `<h1>`, bilingual blocks,
  no unescaped `<` in `<pre>`, nav chain, TOC/count, **every CSS class defined in `shell.CSS`**,
  registry↔PAGES alignment). WARN reviewed.
- `python3 check_links.py` — all internal links resolve.
- `git diff --exit-code` after a rebuild — committed HTML is in sync with sources.
- **`MIN_SVGS`** (added to `check_html.py`): every non-exempt lesson has ≥ 2 `<svg` per language.

### 6.2 Content-completeness audit (subagent)
Verifies each lesson in the milestone: has the full pedagogical arc (lead → analogy → macro →
cited-code body → key-points → quiz); meets CJK/visual-block/SVG floors; bilingual zh/en parity
(no missing or stub translation); quizzes present with answers + explanations.

### 6.3 SVG-correctness audit (subagent)
For every `.fig` SVG: well-formed (balanced tags, valid `viewBox`); no overflow/overlap obvious in
the markup (coordinates within viewBox; text not colliding); uses CSS variables for theming (no
hard-coded `#fff` text that breaks dark mode); the figure actually depicts what its `.figcap`
claims; `role="img"` + `aria-label` present.

### 6.4 Source-fidelity audit (subagent) — **highest priority**
The defining check: **every technical claim and every cited `path:line` must correspond to the
real Langfuse source, never AI-invented.** The auditor:
- Opens each cited file in `/home/verden/course/langfuse` and confirms the path exists and the
  referenced symbol/behavior is actually there (line numbers approximate is OK; the *claim* must be
  true).
- Flags any statement about behavior/architecture not grounded in the codebase (hallucination),
  any wrong file path, any code snippet that misrepresents the source.
- Confirms the lesson does not over-claim (e.g. invented metrics, fabricated config names).
Findings here block the milestone until fixed.

### 6.5 Dual review (per user convention)
On top of the above, run the standard two-stage review on **every** milestone (including trivial
ones): a **spec-compliance** subagent (does the output match this design spec + the M-spec?) then a
**code-quality** subagent (Python generator code + HTML/SVG quality). Use the strongest available
review model (Opus 4.8, max reasoning, long-context). Fix findings, then a brief final re-review.

### 6.6 Audit logging
Each milestone writes `docs/superpowers/plans/<date>-mN-audit.md` recording: automated-gate output,
each subagent's findings, fixes applied, and final sign-off. This is the paper trail proving the
"content corresponds to real source" guarantee.

## 7. Key decisions, risks & mitigations / 关键决策与风险

- **Bilingual cost.** zh+en doubles authoring. Mitigation: write zh first as the source of truth,
  then a faithful en rendering in the same lesson; `check_html.py` enforces both are non-empty and
  near-parity in structure.
- **Hallucination risk** (the central risk for a code-explainer). Mitigation: §6.4 source-fidelity
  audit with real-file verification; cite `path:line`; prefer quoting short real snippets over
  paraphrase; when unsure, the authoring subagent must open the file rather than guess.
- **Scale / drift across milestones.** 55 lessons span many sessions. Mitigation: the source maps in
  `docs/superpowers/plans/source-maps/` + per-M specs keep citations consistent; `registry.py` +
  `check_html.py` keep PAGES/TOC/nav in lockstep; rebuild-and-diff gate prevents stale HTML.
- **Subagent model.** Per user preference, subagents run on the current main model (Opus 4.8), not a
  downgraded default; review/audit subagents use max reasoning + long context.
- **SVG quality at scale.** Many hand-drawn SVGs risk overlap/overflow. Mitigation: §6.3 SVG audit +
  the `.fig svg{max-width:100%}` rule + authoring guidance (generous viewBox, no fixed heights).
- **Langfuse version pinning.** Cite against the checked-out tree at `/home/verden/course/langfuse`
  (record the commit in each M-spec) so citations are reproducible.

## 8. Definition of done / 完成标准
All 55 lessons built & committed; `build*/check_html/check_links` green; `MIN_SVGS` satisfied;
every milestone audited with a logged sign-off; `index.html`, `lessons/*.html`, `print_*.html` in
sync; README + CI/deploy in place; GitHub Pages publishes. The guide reads end-to-end from "what is
LLM observability" to "how to contribute", every technical claim grounded in real Langfuse source.
