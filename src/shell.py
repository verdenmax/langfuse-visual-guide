"""Shared HTML shell (CSS design system + navigation) for the Langfuse visual guide."""

import base64

# ---- favicon (inline SVG, base64) ----
_FAVICON_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
    "<rect width='32' height='32' rx='7' fill='#059669'/>"
    "<path d='M9 16 L22 8.5 M9 16 L22 23.5' stroke='#fff' stroke-width='1.7' fill='none'/>"
    "<circle cx='9' cy='16' r='3' fill='#fff'/>"
    "<circle cx='22' cy='8.5' r='3' fill='#fff'/>"
    "<circle cx='22' cy='23.5' r='3' fill='#fff'/></svg>"
)
FAVICON = "data:image/svg+xml;base64," + base64.b64encode(_FAVICON_SVG.encode()).decode()


def esc(s):
    """Escape plain text for an HTML text/attribute context.

    For chrome/meta strings that are NOT meant to carry inline markup (page
    titles, descriptions). Do NOT use on lesson body content or bi() inputs,
    which may legitimately contain inline tags.
    """
    return (
        str(s).replace("&", "&amp;").replace("<", "&lt;")
        .replace(">", "&gt;").replace('"', "&quot;")
    )


def head_meta(title, description, og_type="website"):
    """SEO / social meta tags + favicon for a page <head>."""
    t = esc(title)
    d = esc(description)
    return (
        f'<meta name="description" content="{d}">\n'
        f'<meta name="theme-color" content="#059669">\n'
        f'<link rel="icon" type="image/svg+xml" href="{FAVICON}">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:site_name" content="Langfuse 图解教程">\n'
        f'<meta property="og:title" content="{t}">\n'
        f'<meta property="og:description" content="{d}">\n'
        f'<meta name="twitter:card" content="summary">\n'
        f'<meta name="twitter:title" content="{t}">\n'
        f'<meta name="twitter:description" content="{d}">'
    )


# Ordered list of all pages:
# (filename, title_zh, title_en, part_zh, part_en)
# Grows one Part per milestone; M0 ships only L01 to prove the pipeline.
PAGES = [
    ("01-what-is-langfuse.html", "Langfuse 是什么", "What is Langfuse",
     "第一部分 · 宏观全景", "Part 1 · The Big Picture"),
    ("02-observability-2-and-wide-events.html", "可观测性 2.0 与宽事件", "Observability 2.0 & wide events",
     "第一部分 · 宏观全景", "Part 1 · The Big Picture"),
    ("03-three-pillars-deep.html", "三大支柱深入：trace/observation/score", "The three pillars in depth",
     "第一部分 · 宏观全景", "Part 1 · The Big Picture"),
    ("04-project-map-monorepo.html", "项目全景地图（monorepo 与窄腰）", "Project map (monorepo & narrow waist)",
     "第一部分 · 宏观全景", "Part 1 · The Big Picture"),
    ("05-life-of-a-trace.html", "一条 trace 的一生·鸟瞰", "Life of a trace (bird's-eye)",
     "第一部分 · 宏观全景", "Part 1 · The Big Picture"),
    ("06-instrumenting-an-llm-app.html", "给 LLM 应用埋点", "Instrumenting an LLM app",
     "第二部分 · 前置基础", "Part 2 · Foundations"),
    ("07-dual-store-architecture.html", "双存储架构", "The dual-store architecture",
     "第二部分 · 前置基础", "Part 2 · Foundations"),
    ("08-clickhouse-wide-events.html", "ClickHouse 与宽事件表", "ClickHouse & the wide-event tables",
     "第二部分 · 前置基础", "Part 2 · Foundations"),
    ("09-postgres-metadata-schema.html", "元数据 schema（Postgres/Prisma）", "The metadata schema (Postgres)",
     "第二部分 · 前置基础", "Part 2 · Foundations"),
    ("10-multi-tenancy.html", "多租户：org → project → environment", "Multi-tenancy",
     "第二部分 · 前置基础", "Part 2 · Foundations"),
    ("11-deployment-topology.html", "部署拓扑与依赖", "Deployment topology",
     "第二部分 · 前置基础", "Part 2 · Foundations"),
    ("12-ingestion-api.html", "摄取 API", "The ingestion API",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("13-event-types-merge.html", "事件类型与合并语义", "Event types & merge semantics",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("14-ingestion-queue.html", "摄取队列", "The ingestion queue",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("15-ingestion-service.html", "IngestionService：合并的心脏", "IngestionService: the merge heart",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("16-token-counting-cost.html", "Token 计数与成本", "Token counting & cost",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("17-clickhouse-writer.html", "ClickhouseWriter：批量落盘", "ClickhouseWriter: batched persistence",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("18-opentelemetry-ingestion.html", "OpenTelemetry 摄取", "OpenTelemetry ingestion",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("19-media-blob-storage.html", "媒体与 blob 存储", "Media & blob storage",
     "第三部分 · 摄取链路", "Part 3 · The Ingestion Path"),
    ("20-web-app-architecture.html", "web 应用架构", "The web app architecture",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("21-trpc-backbone.html", "tRPC 骨架", "The tRPC backbone",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("22-repository-layer.html", "仓储层：从 ClickHouse 读", "The repository layer",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("23-filtering-search-bar.html", "过滤·搜索栏·查询构建", "Filtering & the search bar",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("24-lists-and-tables.html", "列表与表格", "Lists & tables",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("25-trace-detail-tree.html", "trace 详情与观测树", "Trace detail & the observation tree",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("26-sessions.html", "sessions", "Sessions",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("27-public-rest-api.html", "公共 REST API", "The public REST API",
     "第四部分 · 查询链路", "Part 4 · The Read Path"),
    ("28-scoring-model.html", "评分模型", "The scoring model",
     "第五部分 · 评估与评分", "Part 5 · Evaluation & Scoring"),
    ("29-llm-as-a-judge.html", "LLM 当裁判", "LLM-as-a-judge",
     "第五部分 · 评估与评分", "Part 5 · Evaluation & Scoring"),
    ("30-eval-execution-pipeline.html", "eval 执行流水线", "The eval execution pipeline",
     "第五部分 · 评估与评分", "Part 5 · Evaluation & Scoring"),
    ("31-code-based-evaluation.html", "代码 eval", "Code-based evaluation",
     "第五部分 · 评估与评分", "Part 5 · Evaluation & Scoring"),
    ("32-human-annotation.html", "人工标注", "Human annotation",
     "第五部分 · 评估与评分", "Part 5 · Evaluation & Scoring"),
    ("33-monitors-and-alerting.html", "监控器与告警", "Monitors & alerting",
     "第五部分 · 评估与评分", "Part 5 · Evaluation & Scoring"),
    ("34-datasets-and-items.html", "数据集与数据项", "Datasets & items",
     "第六部分 · 数据集与实验", "Part 6 · Datasets & Experiments"),
    ("35-dataset-runs.html", "数据集运行与运行项", "Dataset runs & run items",
     "第六部分 · 数据集与实验", "Part 6 · Datasets & Experiments"),
    ("36-experiments-and-comparison.html", "实验与对比", "Experiments & comparison",
     "第六部分 · 数据集与实验", "Part 6 · Datasets & Experiments"),
    ("37-prompt-management.html", "Prompt 管理", "Prompt management",
     "第七部分 · Prompt 与 Playground", "Part 7 · Prompts & Playground"),
    ("38-prompt-serving-caching.html", "Prompt 服务与缓存", "Prompt serving & caching",
     "第七部分 · Prompt 与 Playground", "Part 7 · Prompts & Playground"),
    ("39-playground-llm-connections.html", "Playground 与 LLM 连接", "Playground & LLM connections",
     "第七部分 · Prompt 与 Playground", "Part 7 · Prompts & Playground"),
    ("40-dashboards-and-widgets.html", "仪表盘与 widget 系统", "Dashboards & widgets",
     "第八部分 · 仪表盘·指标·成本", "Part 8 · Dashboards, Metrics & Cost"),
    ("41-query-engine.html", "查询引擎", "The query engine",
     "第八部分 · 仪表盘·指标·成本", "Part 8 · Dashboards, Metrics & Cost"),
    ("42-models-and-pricing.html", "模型与定价", "Models & pricing",
     "第八部分 · 仪表盘·指标·成本", "Part 8 · Dashboards, Metrics & Cost"),
    ("43-cloud-usage-metering.html", "云用量计量与花费", "Cloud usage metering & spend",
     "第八部分 · 仪表盘·指标·成本", "Part 8 · Dashboards, Metrics & Cost"),
    ("44-automations-webhooks.html", "自动化与 webhook", "Automations & webhooks",
     "第九部分 · 自动化与集成", "Part 9 · Automation & Integrations"),
    ("45-slack-and-notifications.html", "Slack 与通知", "Slack & notifications",
     "第九部分 · 自动化与集成", "Part 9 · Automation & Integrations"),
    ("46-analytics-integrations.html", "分析集成", "Analytics integrations",
     "第九部分 · 自动化与集成", "Part 9 · Automation & Integrations"),
    ("47-batch-exports-and-actions.html", "批量导出与批量操作", "Batch exports & actions",
     "第九部分 · 自动化与集成", "Part 9 · Automation & Integrations"),
    ("48-auth-and-sessions.html", "鉴权与会话", "Auth & sessions",
     "第十部分 · 平台与运维", "Part 10 · Platform & Operations"),
    ("49-rbac-apikeys-scim.html", "RBAC · API key · SCIM", "RBAC, API keys & SCIM",
     "第十部分 · 平台与运维", "Part 10 · Platform & Operations"),
    ("50-open-core-and-entitlements.html", "开源核与权益", "Open-core & entitlements",
     "第十部分 · 平台与运维", "Part 10 · Platform & Operations"),
    ("51-self-observability-and-config.html", "自我可观测与配置", "Self-observability & config",
     "第十部分 · 平台与运维", "Part 10 · Platform & Operations"),
    ("52-data-lifecycle-and-deletion.html", "数据生命周期与删除", "Data lifecycle & deletion",
     "第十部分 · 平台与运维", "Part 10 · Platform & Operations"),
    ("53-build-test-dev-workflow.html", "构建·测试·开发流", "Build, test & dev workflow",
     "第十部分 · 平台与运维", "Part 10 · Platform & Operations"),
    ("54-design-themes-synthesis.html", "设计专题综合", "Design themes synthesis",
     "第十一部分 · 设计专题与终章", "Part 11 · Design Themes & Capstone"),
    ("55-capstone-trace-life.html", "终章·一条 trace 的完整一生", "Capstone: the full life of a trace",
     "第十一部分 · 设计专题与终章", "Part 11 · Design Themes & Capstone"),
]


def bi(zh, en):
    """Inline bilingual pair; only the active language is shown (CSS-controlled)."""
    return f'<span class="lang-zh">{zh}</span><span class="lang-en">{en}</span>'


INDEX_FILE = "index.html"

CSS = r"""
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #f6f7f9; --panel: #ffffff; --panel-2: #f0f2f5; --ink: #1d2129;
  --muted: #5b6470; --faint: #8a939f; --line: #e1e5ea;
  --accent: #059669; --accent-soft: #d1fae5; --accent-ink: #047857;
  --blue: #2563eb; --blue-soft: #e7efff; --amber: #b4690e; --amber-soft: #fdf1dd;
  --purple: #7c3aed; --purple-soft: #f0e9ff; --red: #d23f3f; --red-soft: #fbe6e6;
  --teal: #0891b2; --teal-soft: #cffafe;
  --code-bg: #0f172a; --code-ink: #e2e8f0; --code-line: #1e293b;
  --shadow: 0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06);
  --radius: 14px;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0e1116; --panel: #161b22; --panel-2: #1c232c; --ink: #e6edf3;
    --muted: #9aa6b2; --faint: #6e7a86; --line: #2a323c;
    --accent: #34d399; --accent-soft: #064e3b; --accent-ink: #6ee7b7;
    --blue: #6ea8fe; --blue-soft: #16243f; --amber: #e0a44a; --amber-soft: #33270f;
    --purple: #b794f6; --purple-soft: #271a40; --red: #f08080; --red-soft: #3a1a1a;
    --teal: #22d3ee; --teal-soft: #083344;
    --code-bg: #0a0f1a; --code-ink: #d8e2f0; --code-line: #14202f;
    --shadow: 0 1px 2px rgba(0,0,0,.4), 0 10px 30px rgba(0,0,0,.35);
  }
}
html { scroll-behavior: smooth; overflow-x: hidden; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
    "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  background: var(--bg); color: var(--ink); line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
code, .mono { font-family: "SF Mono", "JetBrains Mono", "Fira Code", ui-monospace, Menlo, Consolas, monospace; overflow-wrap: break-word; }

/* ---- top progress bar ---- */
.topbar {
  position: sticky; top: 0; z-index: 50; background: var(--panel);
  border-bottom: 1px solid var(--line); backdrop-filter: blur(8px);
}
.topbar-inner {
  max-width: 960px; margin: 0 auto; padding: .7rem 1.25rem;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem;
}
.topbar .home { font-size: .82rem; color: var(--muted); font-weight: 600; display:flex; gap:.5rem; align-items:center; }
.topbar .home b { color: var(--accent); }
.topbar .pill { font-size: .72rem; color: var(--muted); background: var(--panel-2);
  padding: .2rem .6rem; border-radius: 999px; border: 1px solid var(--line); white-space: nowrap; }
.progress { height: 3px; background: var(--panel-2); }
.progress > span { display: block; height: 100%; background: linear-gradient(90deg, var(--accent), var(--purple)); }

.wrap { max-width: 820px; margin: 0 auto; padding: 2.4rem 1.25rem 5rem; }

/* ---- hero ---- */
.hero { margin-bottom: 2rem; }
.hero .part { font-size: .76rem; letter-spacing: .08em; text-transform: uppercase;
  color: var(--accent); font-weight: 700; margin-bottom: .55rem; }
.hero h1 { font-size: 2.05rem; line-height: 1.2; letter-spacing: -.01em; font-weight: 750; }
.hero .lead { margin-top: .9rem; font-size: 1.06rem; color: var(--muted); }

h2 { font-size: 1.32rem; margin: 2.4rem 0 .9rem; letter-spacing: -.01em;
  display: flex; align-items: center; gap: .55rem; }
h2::before { content: ""; width: 4px; height: 1.05em; background: var(--accent); border-radius: 3px; display: inline-block; }
h3 { font-size: 1.05rem; margin: 1.4rem 0 .5rem; }
p { margin: .7rem 0; }
ul, ol { margin: .6rem 0 .6rem 1.3rem; }
li { margin: .3rem 0; }
strong { color: var(--ink); font-weight: 680; }
.inline { background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px;
  padding: .08em .4em; font-size: .9em; color: var(--accent-ink); }

/* ---- callout cards ---- */
.card { border-radius: var(--radius); padding: 1.05rem 1.2rem; margin: 1.2rem 0;
  border: 1px solid var(--line); background: var(--panel); box-shadow: var(--shadow); }
.card .tag { font-size: .72rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;
  display: inline-flex; align-items: center; gap: .4rem; margin-bottom: .5rem; }
.card.macro { border-left: 4px solid var(--blue); }
.card.macro .tag { color: var(--blue); }
.card.detail { border-left: 4px solid var(--purple); }
.card.detail .tag { color: var(--purple); }
.card.analogy { border-left: 4px solid var(--amber); background: var(--amber-soft); }
.card.analogy .tag { color: var(--amber); }
.card.key { border-left: 4px solid var(--accent); background: var(--accent-soft); }
.card.key .tag { color: var(--accent-ink); }
.card.warn { border-left: 4px solid var(--red); background: var(--red-soft); }
.card.warn .tag { color: var(--red); }
.card.spark { border-left: 4px solid #e0a000;
  background: linear-gradient(100deg, rgba(224,160,0,.12), transparent 70%); }
.card.spark .tag { color: #c98a00; }
@media (prefers-color-scheme: dark) { .card.spark .tag { color: #f0c050; } }

/* ---- code file callout ---- */
.codefile { margin: 1.2rem 0; border-radius: 12px; overflow: hidden; border: 1px solid var(--line);
  box-shadow: var(--shadow); }
.codefile .cf-head { display: flex; align-items: center; gap: .55rem; padding: .5rem .85rem;
  background: var(--panel-2); border-bottom: 1px solid var(--line); font-size: .8rem; }
.codefile .cf-head .dot { width: 9px; height: 9px; border-radius: 50%; background: var(--accent); flex-shrink:0; }
.codefile .cf-head .path { font-family: ui-monospace, monospace; color: var(--ink); font-weight: 600; }
.codefile .cf-head .ln { margin-left: auto; color: var(--faint); font-size: .72rem; }
.codefile pre { background: var(--code-bg); color: var(--code-ink); padding: .9rem 1rem;
  overflow-x: auto; font-size: .82rem; line-height: 1.6; }
.codefile pre .cm { color: #7d8aa3; }
.codefile pre .kw { color: #c792ea; }
.codefile pre .fn { color: #82aaff; }
.codefile pre .st { color: #c3e88d; }
.codefile pre .nb { color: #f78c6c; }

pre.code { background: var(--code-bg); color: var(--code-ink); padding: .9rem 1rem; border-radius: 12px;
  overflow-x: auto; font-size: .83rem; line-height: 1.6; margin: 1.1rem 0; box-shadow: var(--shadow); }
pre.code .cm { color: #7d8aa3; } pre.code .kw { color: #c792ea; }
pre.code .fn { color: #82aaff; } pre.code .st { color: #c3e88d; } pre.code .nb { color: #f78c6c; }

/* ---- collapsible accordion (details/summary) ---- */
.accordion { border: 1px solid var(--line); border-radius: 12px; background: var(--panel);
  margin: .7rem 0; box-shadow: var(--shadow); overflow: hidden; }
.accordion > summary { cursor: pointer; padding: .85rem 1.1rem; font-weight: 650; font-size: .96rem;
  list-style: none; display: flex; align-items: center; gap: .6rem; user-select: none; }
.accordion > summary::-webkit-details-marker { display: none; }
.accordion > summary::after { content: "▶"; font-size: .68rem; color: var(--accent);
  margin-left: auto; transition: transform .15s ease; }
.accordion[open] > summary::after { transform: rotate(90deg); }
.accordion > summary:hover { background: var(--panel-2); }
.accordion[open] > summary { border-bottom: 1px solid var(--line); }
.accordion .badge-num { background: var(--accent-soft); color: var(--accent-ink);
  width: 1.6rem; height: 1.6rem; border-radius: 7px; display: inline-flex; align-items: center;
  justify-content: center; font-size: .82rem; font-weight: 700; flex-shrink: 0; }
.accordion .hint { font-size: .72rem; color: var(--faint); font-weight: 400; }
.acc-body { padding: .9rem 1.1rem 1.1rem; }
.acc-intro { color: var(--muted); font-size: .9rem; margin: .2rem 0 .4rem; }
.qa { margin: 1rem 0; }
.qa:first-child { margin-top: .3rem; }
.qa .q { font-weight: 680; font-size: .9rem; display: flex; gap: .45rem; align-items: center; margin-bottom: .3rem; }
.qa .a { color: var(--muted); font-size: .9rem; }
.qa .a strong { color: var(--ink); }
.qa pre.code { margin: .5rem 0 0; font-size: .78rem; }

/* ---- flow diagram ---- */
.flow { display: flex; align-items: stretch; gap: 0; flex-wrap: wrap; margin: 1.3rem 0;
  background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 1.2rem 1rem; box-shadow: var(--shadow); }
.flow .node { flex: 1 1 0; min-width: 110px; text-align: center; padding: .7rem .5rem;
  border-radius: 10px; background: var(--panel-2); border: 1px solid var(--line); }
.flow .node .nt { font-weight: 700; font-size: .92rem; }
.flow .node .nd { font-size: .76rem; color: var(--muted); margin-top: .2rem; }
.flow .node.hl { background: var(--accent-soft); border-color: var(--accent); }
.flow .arrow { align-self: center; color: var(--faint); font-size: 1.3rem; padding: 0 .35rem; }

/* vertical flow */
.vflow { margin: 1.3rem 0; }
.vflow .step { display: flex; gap: .9rem; position: relative; padding-bottom: 1.1rem; }
.vflow .step:not(:last-child)::before { content:""; position:absolute; left: 15px; top: 34px; bottom: -2px;
  width: 2px; background: var(--line); }
.vflow .num { width: 32px; height: 32px; border-radius: 50%; background: var(--accent); color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .85rem; flex-shrink: 0; z-index:1; }
.vflow .sc h4 { margin: .25rem 0 .2rem; font-size: 1rem; }
.vflow .sc p { margin: .15rem 0; font-size: .92rem; color: var(--muted); }
.vflow .sc .mono { font-size: .8rem; color: var(--accent-ink); }

/* layered architecture */
.layers { margin: 1.3rem 0; display: flex; flex-direction: column; gap: .55rem; }
.layer { border-radius: 12px; padding: .85rem 1.1rem; border: 1px solid var(--line); background: var(--panel);
  box-shadow: var(--shadow); }
.layer .lh { display: flex; align-items: center; gap: .6rem; }
.layer .lh .badge { font-size: .7rem; font-weight: 700; padding: .12rem .5rem; border-radius: 999px; }
.layer .lh .name { font-weight: 700; font-family: ui-monospace, monospace; }
.layer .ld { font-size: .85rem; color: var(--muted); margin-top: .35rem; }
.layer.l-core { border-left: 4px solid var(--accent); } .layer.l-core .badge { background: var(--accent-soft); color: var(--accent-ink); }
.layer.l-main { border-left: 4px solid var(--blue); } .layer.l-main .badge { background: var(--blue-soft); color: var(--blue); }
.layer.l-part { border-left: 4px solid var(--purple); } .layer.l-part .badge { background: var(--purple-soft); color: var(--purple); }
.layer.l-app { border-left: 4px solid var(--amber); } .layer.l-app .badge { background: var(--amber-soft); color: var(--amber); }

/* two-column compare */
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1.2rem 0; }
@media (max-width: 640px) { .cols { grid-template-columns: 1fr; } }
.col { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 1rem 1.1rem; box-shadow: var(--shadow); min-width: 0; }
.col h4 { margin: 0 0 .4rem; font-size: .95rem; }

table.t { width: 100%; border-collapse: collapse; margin: 1.1rem 0; font-size: .9rem;
  background: var(--panel); border-radius: 12px; overflow: hidden; box-shadow: var(--shadow); }
table.t th, table.t td { padding: .6rem .8rem; text-align: left; border-bottom: 1px solid var(--line); }
table.t th { background: var(--panel-2); font-size: .8rem; letter-spacing: .02em; }
table.t tr:last-child td { border-bottom: none; }
table.t td.mono, table.t td .mono { font-family: ui-monospace, monospace; font-size: .82rem; color: var(--accent-ink); }
@media (max-width: 640px) {
  /* Wide multi-column tables: scroll within their own box instead of
     forcing page-level horizontal overflow (which clipped right columns). */
  table.t { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  table.t th, table.t td { padding: .5rem .6rem; }
}
.selftest { margin: 2.2rem 0 0; border-top: 2px dashed var(--line); padding-top: 1.2rem; }
.selftest > h2 { margin-top: .2rem; }
.quiz { background: var(--panel); border: 1px solid var(--line); border-left: 4px solid var(--blue);
  border-radius: 12px; padding: .9rem 1.1rem; margin: 1rem 0; box-shadow: var(--shadow); }
.quiz .qn { font-weight: 650; }
.quiz ol.opts { list-style: upper-alpha; margin: .55rem 0 .6rem 1.5rem; padding: 0; }
.quiz ol.opts li { margin: .3rem 0; padding-left: .15rem; }
.quiz details.accordion { margin: .5rem 0 0; }
.selftest code { font-family: ui-monospace, monospace; font-size: .9em; color: var(--accent-ink);
  background: var(--accent-soft); padding: 0 .28em; border-radius: 4px; }

/* footer nav */
.footnav { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem;
  padding-top: 1.4rem; border-top: 1px solid var(--line); }
.footnav a { flex: 1; padding: .85rem 1.1rem; border-radius: 12px; border: 1px solid var(--line);
  background: var(--panel); box-shadow: var(--shadow); transition: .15s; }
.footnav a:hover { border-color: var(--accent); transform: translateY(-1px); }
.footnav a.next { text-align: right; }
.footnav .dir { font-size: .72rem; color: var(--faint); text-transform: uppercase; letter-spacing: .05em; }
.footnav .ttl { font-weight: 700; color: var(--ink); margin-top: .15rem; }
.footnav a.disabled { opacity: .35; pointer-events: none; }

/* index page */
.toc { display: grid; gap: .7rem; margin-top: 1.6rem; }
.toc-part { font-size: .78rem; font-weight: 700; letter-spacing: .05em; text-transform: uppercase;
  color: var(--accent); margin: 1.4rem 0 .2rem; }
.toc a { display: flex; align-items: center; gap: .9rem; padding: .85rem 1.05rem; border-radius: 12px;
  background: var(--panel); border: 1px solid var(--line); box-shadow: var(--shadow); transition: .15s; }
.toc a:hover { border-color: var(--accent); transform: translateX(3px); }
.toc .n { width: 30px; height: 30px; border-radius: 8px; background: var(--accent-soft); color: var(--accent-ink);
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: .85rem; flex-shrink: 0; }
.toc .tt { font-weight: 650; color: var(--ink); }
.toc .ts { font-size: .8rem; color: var(--muted); margin-left: auto; text-align: right; }
.toc-search { position: relative; margin: 1.6rem 0 -.4rem; }
.toc-search input { width: 100%; box-sizing: border-box; padding: .75rem 2.8rem .75rem 1rem;
  border-radius: 12px; border: 1px solid var(--line); background: var(--panel); color: var(--ink);
  font-size: .98rem; box-shadow: var(--shadow); }
.toc-search input:focus { outline: none; border-color: var(--accent); }
.toc-search .qcount { position: absolute; right: 1rem; top: 50%; transform: translateY(-50%);
  color: var(--faint); font-size: .8rem; pointer-events: none; }
.toc a.hide, .toc .toc-part.hide { display: none; }
.t tr.hide, table.t.hide, h2.hide { display: none; }
.toc-empty { display: none; color: var(--muted); padding: 1rem; text-align: center; }
.toc-empty.show { display: block; }
.hero.index h1 { font-size: 2.3rem; }
.legend { display:flex; gap:1.2rem; flex-wrap:wrap; margin-top:1rem; font-size:.8rem; color:var(--muted); }
.legend span { display:flex; align-items:center; gap:.4rem; }
.legend i { width:12px; height:12px; border-radius:3px; display:inline-block; }
.pdf-btn { display:inline-flex; align-items:center; gap:.4rem; padding:.55rem 1.1rem;
  background:var(--accent); color:#fff; border-radius:10px; font-size:.9rem; font-weight:650;
  box-shadow:var(--shadow); transition:.15s; }
.pdf-btn:hover { background:var(--accent-ink); transform:translateY(-1px); }

/* ---- bilingual language switch ----
   Contract: <html> must carry data-lang="zh" (default) or "en".
   page()/index_page() hard-code data-lang="zh"; LANG_BOOT may switch to "en". */
html[data-lang="en"] .lang-zh { display: none !important; }
html[data-lang="zh"] .lang-en { display: none !important; }
.langtoggle { font-size:.72rem; font-weight:700; color:var(--accent-ink);
  background:var(--accent-soft); border:1px solid var(--accent); border-radius:999px;
  padding:.22rem .7rem; cursor:pointer; line-height:1.4; white-space:nowrap; }
.langtoggle:hover { background:var(--accent); color:#fff; }

/* ---- schematic: cell strips (vector rows / quant blocks / KV columns) ---- */
.cellgroup { margin: 1.2rem 0; background: var(--panel); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 1rem 1.1rem; box-shadow: var(--shadow); }
.cellgroup .cg-cap { font-size: .82rem; color: var(--muted); margin-bottom: .55rem; }
.cellgroup .cg-cap b { color: var(--ink); }
.cells { display: flex; flex-wrap: wrap; gap: .35rem; align-items: center; }
.cells + .cells { margin-top: .5rem; }
.cell { min-width: 2.1rem; padding: .38rem .5rem; text-align: center; border-radius: 8px;
  background: var(--panel-2); border: 1px solid var(--line); font-size: .78rem;
  font-family: ui-monospace, monospace; white-space: nowrap; }
.cell.scale { background: var(--amber-soft); border-color: var(--amber); color: var(--amber); font-weight: 700; }
.cell.hl    { background: var(--accent-soft); border-color: var(--accent); color: var(--accent-ink); font-weight: 700; }
.cell.q     { background: var(--blue-soft); border-color: var(--blue); color: var(--blue); }
.cell.dim   { opacity: .45; }
.cells .lab { font-size: .76rem; color: var(--faint); padding: 0 .35rem; }
.cells .sep { color: var(--faint); padding: 0 .1rem; }

/* ---- schematic: timeline lanes (write vs read, step-by-step) ---- */
.timeline { margin: 1.2rem 0; display: flex; flex-direction: column; gap: .5rem;
  background: var(--panel); border: 1px solid var(--line); border-radius: var(--radius);
  padding: 1rem 1.1rem; box-shadow: var(--shadow); }
.timeline .lane { display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; }
.timeline .lane-label { min-width: 6rem; font-size: .8rem; font-weight: 700; color: var(--muted); }
.timeline .tslot { padding: .4rem .6rem; border-radius: 8px; background: var(--panel-2);
  border: 1px solid var(--line); font-size: .78rem; text-align: center; font-family: ui-monospace, monospace; }
.timeline .tslot.span { flex: 1; min-width: 8rem; background: var(--blue-soft); border-color: var(--blue);
  color: var(--blue); font-weight: 700; }
.timeline .tslot.now { background: var(--accent-soft); border-color: var(--accent); color: var(--accent-ink); font-weight: 700; }
.timeline .tl-row { display: flex; align-items: flex-start; gap: .6rem; padding: .12rem 0; }
.timeline .tl-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent); flex-shrink: 0; margin-top: .45rem; }
.timeline .tl-t { font-family: ui-monospace, monospace; font-weight: 700; color: var(--accent-ink); min-width: 2.4rem; font-size: .82rem; flex-shrink: 0; margin-top: .18rem; }
.timeline .tl-c { font-size: .9rem; color: var(--muted); }

/* ---- worked-example trace: one concrete input, stepped through ---- */
.trace { margin: 1.3rem 0; background: var(--panel); border: 1px solid var(--line);
  border-left: 4px solid var(--accent); border-radius: var(--radius); padding: 1rem 1.1rem; box-shadow: var(--shadow); }
.trace .tcap { font-size: .82rem; color: var(--muted); margin-bottom: .7rem; }
.trace .tcap b { color: var(--accent-ink); }
.trace .stations { display: flex; align-items: stretch; gap: 0; flex-wrap: wrap; }
.trace .stn { flex: 1 1 0; min-width: 116px; border: 1px solid var(--line); border-radius: 10px;
  padding: .55rem; background: var(--bg); }
.trace .stn h5 { margin: 0 0 .45rem; font-size: .8rem; color: var(--ink); }
.trace .cellrow { display: flex; gap: .3rem; align-items: center; flex-wrap: wrap; }
.trace .vc { min-width: 2.1rem; padding: .32rem .45rem; text-align: center; border-radius: 7px;
  background: var(--panel-2); border: 1px solid var(--line); font: 600 .76rem ui-monospace, monospace; white-space: nowrap; }
.trace .vc.hot  { background: var(--accent-soft); border-color: var(--accent); color: var(--accent-ink); }
.trace .vc.blue { background: var(--blue-soft); border-color: var(--blue); color: var(--blue); }
.trace .vc.dim  { opacity: .42; }
.trace .tlab { font-size: .68rem; color: var(--faint); margin-top: .35rem; }
.trace .op { align-self: center; color: var(--accent); font: 700 .72rem ui-monospace, monospace;
  padding: 0 .5rem; text-align: center; white-space: nowrap; }
.trace svg { max-width: 100%; height: auto; display: block; margin: .3rem auto; }
@media (max-width: 640px) { .trace .stations { flex-direction: column; } .trace .op { padding: .3rem 0; } }
/* --- hand-drawn figure (inline SVG illustrations) --- */
.fig { margin: 1.3rem 0; background: var(--panel); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 1rem 1rem .85rem; box-shadow: var(--shadow); text-align: center; }
.fig svg { max-width: 100%; height: auto; display: block; margin: 0 auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif; }
.fig svg text { fill: var(--ink); }
.fig .figcap { margin: .72rem auto 0; font-size: .8rem; color: var(--muted); line-height: 1.55; max-width: 46rem; }
.fig .figcap b { color: var(--accent-ink); font-weight: 700; }
"""

SEARCH_JS = """
(function(){
  var q=document.getElementById('q'); if(!q) return;
  var toc=document.querySelector('.toc');
  var empty=document.getElementById('tocempty');
  var count=document.getElementById('qcount');
  var links=[].slice.call(toc.querySelectorAll('a'));
  var heads=[].slice.call(toc.querySelectorAll('.toc-part'));
  links.forEach(function(a){ a.setAttribute('data-s',(a.textContent||'').toLowerCase()); });
  function run(){
    var t=(q.value||'').toLowerCase().trim(), n=0;
    links.forEach(function(a){
      var hit=!t||a.getAttribute('data-s').indexOf(t)>=0;
      a.classList.toggle('hide',!hit); if(hit)n++;
    });
    heads.forEach(function(h){
      var el=h.nextElementSibling, any=false;
      while(el && !el.classList.contains('toc-part')){
        if(el.tagName==='A' && !el.classList.contains('hide')){any=true;break;}
        el=el.nextElementSibling;
      }
      h.classList.toggle('hide',!any);
    });
    empty.classList.toggle('show', !!t && n===0);
    count.textContent = t ? String(n) : '';
  }
  q.addEventListener('input',run);
})();
"""

GLOSSARY_JS = """
(function(){
  function wire(inputId, countId, emptyId, scope){
    var q=document.getElementById(inputId); if(!q) return;
    var root=document.querySelector(scope); if(!root) return;
    var empty=document.getElementById(emptyId), count=document.getElementById(countId);
    var tables=[].slice.call(root.querySelectorAll('table.t'));
    var rows=[].slice.call(root.querySelectorAll('table.t tr')).filter(function(tr){return tr.querySelector('td');});
    rows.forEach(function(tr){ tr.setAttribute('data-s',(tr.textContent||'').toLowerCase()); });
    function run(){
      var t=(q.value||'').toLowerCase().trim(), n=0;
      rows.forEach(function(tr){
        var hit=!t||tr.getAttribute('data-s').indexOf(t)>=0;
        tr.classList.toggle('hide',!hit); if(hit)n++;
      });
      tables.forEach(function(tb){
        var any=[].slice.call(tb.querySelectorAll('tr')).some(function(tr){
          return tr.querySelector('td') && !tr.classList.contains('hide');
        });
        tb.classList.toggle('hide', !any);
        var h=tb.previousElementSibling;
        if(h && h.tagName==='H2') h.classList.toggle('hide', !any);
      });
      if(empty) empty.classList.toggle('show', !!t && n===0);
      if(count) count.textContent = t ? String(n) : '';
    }
    q.addEventListener('input',run);
  }
  wire('qglzh','qglzhc','qglzhe','.lang-zh');
  wire('qglen','qglenc','qglene','.lang-en');
})();
"""

LANG_JS = """
function lvgSetLang(l){
  l=(l==='en')?'en':'zh';
  var d=document.documentElement;
  d.dataset.lang=l; d.lang=(l==='en'?'en':'zh-CN');
  try{localStorage.setItem('lvg-lang',l);}catch(e){}
}
function lvgToggleLang(){
  lvgSetLang(document.documentElement.dataset.lang==='en'?'zh':'en');
}
"""

# Runs in <head> before first paint to avoid a flash of the wrong language.
LANG_BOOT = (
    "<script>try{var l=localStorage.getItem('lvg-lang');"
    "if(l==='en'){document.documentElement.dataset.lang='en';"
    "document.documentElement.lang='en';}}catch(e){}</script>"
)


def page(filename, content, home_href="../index.html"):
    """Wrap one lesson's bilingual content in the full HTML shell.

    ``content`` is a dict ``{"zh": html, "en": html}``. Both are emitted; CSS
    shows only the active language. Navigation uses plain relative ``href``
    links so the site works via file:// and any static server (lessons share
    one directory; home defaults to ``../index.html``).
    """
    idx = next(i for i, p in enumerate(PAGES) if p[0] == filename)
    fname, title_zh, title_en, part_zh, part_en = PAGES[idx]
    total = len(PAGES)
    pct = int((idx + 1) / total * 100)
    home = home_href

    if idx > 0:
        p = PAGES[idx - 1]
        prev_link = (
            f'<a class="prev" href="{p[0]}"><div class="dir">{bi("← 上一课", "← Prev")}</div>'
            f'<div class="ttl">{bi(esc(p[1]), esc(p[2]))}</div></a>'
        )
    else:
        prev_link = (
            f'<a class="prev" href="{home}"><div class="dir">{bi("← 返回", "← Back")}</div>'
            f'<div class="ttl">{bi("目录", "Contents")}</div></a>'
        )
    if idx + 1 < total:
        p = PAGES[idx + 1]
        next_link = (
            f'<a class="next" href="{p[0]}"><div class="dir">{bi("下一课 →", "Next →")}</div>'
            f'<div class="ttl">{bi(esc(p[1]), esc(p[2]))}</div></a>'
        )
    else:
        next_link = (
            f'<a class="next" href="{home}"><div class="dir">{bi("完成 →", "Done →")}</div>'
            f'<div class="ttl">{bi("返回目录", "Back to index")}</div></a>'
        )

    title_tag = f"{idx+1:02d} · {title_zh} / {title_en} - Langfuse 图解教程"
    desc = f"{part_zh}｜{title_zh} - Langfuse 图解教程（中英双语，配真实源码对应、折叠深挖与设计取舍）"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{LANG_BOOT}
<title>{esc(title_tag)}</title>
{head_meta(title_tag, desc, og_type="article")}
<style>{CSS}</style>
</head><body>
<div class="topbar">
  <div class="topbar-inner">
    <a class="home" href="{home}">🪢 <b class="lang-zh">Langfuse 图解教程</b><b class="lang-en">Langfuse Visual Guide</b></a>
    <span class="pill">{bi(esc(part_zh), esc(part_en))}</span>
    <span class="pill">{idx+1:02d} / {total:02d}</span>
    <button class="langtoggle" onclick="lvgToggleLang()" aria-label="switch language"><span class="lang-zh">EN</span><span class="lang-en">中</span></button>
  </div>
  <div class="progress"><span style="width:{pct}%"></span></div>
</div>
<div class="wrap">
  <div class="hero">
    <div class="part">{bi(esc(part_zh), esc(part_en))}</div>
    <h1><span class="lang-zh">{esc(title_zh)}</span><span class="lang-en">{esc(title_en)}</span></h1>
  </div>
  <div class="lang-zh">{content["zh"]}</div>
  <div class="lang-en">{content["en"]}</div>
  <div class="footnav">{prev_link}{next_link}</div>
</div>
<script>{LANG_JS}</script>
</body></html>"""
    return html


# Per-lesson TOC subtitle: filename -> (zh, en). Missing entries render blank.
# Grows one Part per milestone alongside PAGES.
SUBTITLES = {
    "01-what-is-langfuse.html": ("LLM 可观测性 · trace/observation/score · 为何要这样一套平台",
                                 "LLM observability; trace/observation/score; why a platform like this"),
    "02-observability-2-and-wide-events.html": ("可观测性 1.0 的困境 · 宽事件 · 十条原则 · unknown unknowns",
                                                "the 1.0 trouble; wide events; the principles; unknown unknowns"),
    "03-three-pillars-deep.html": ("trace 薄 · observation 厚（10 型·树）· score 两维 · 落到三张 CH 表",
                                   "thin trace; heavy observation (10 types, tree); score 2-D; three CH tables"),
    "04-project-map-monorepo.html": ("monorepo · 四工作区 · 窄腰依赖 · Turbo 编排 · 高频目录速查",
                                     "monorepo; four workspaces; narrow-waist deps; Turbo; hot-dir cheat-sheet"),
    "05-life-of-a-trace.html": ("写：SDK→API→队列→worker→CH · 读：UI→tRPC→仓储→CH · 异步·最终一致",
                                "write: SDK→API→queue→worker→CH; read: UI→tRPC→repo→CH; async; eventual consistency"),
    "06-instrumenting-an-llm-app.html": ("两个入口：SDK 原生事件 / OTel · 事件信封 · create+update 增量",
                                         "two entries: native SDK events / OTel; the event envelope; incremental create+update"),
    "07-dual-store-architecture.html": ("四存储分工：PG 配置 · CH 宽事件 · Redis 队列/缓存 · S3 真相之源 · OLTP vs OLAP",
                                        "four stores: PG config; CH wide events; Redis queue/cache; S3 source-of-truth; OLTP vs OLAP"),
    "08-clickhouse-wide-events.html": ("ReplacingMergeTree · 排序键 project_id 打头 · 月分区 · ZSTD/Map/bloom · 少扫才是关键",
                                       "ReplacingMergeTree; ordering key project_id-first; monthly partitions; ZSTD/Map/bloom; scan-less"),
    "09-postgres-metadata-schema.html": ("控制面 vs 数据面 · Project 枢纽 · 模型分组 · Legacy 残留 · API key 哈希",
                                         "control plane vs data plane; Project hub; model groups; Legacy remnants; hashed API keys"),
    "10-multi-tenancy.html": ("三层嵌套 org→project→env · project 硬隔离 · environment 软切片 · project_id 贯穿",
                              "three levels org→project→env; hard project isolation; soft environment slice; project_id threaded"),
    "11-deployment-topology.html": ("2 应用 + 4 基础设施 · docker-compose · web vs worker · MinIO 替身 · env 启动即校验",
                                    "2 apps + 4 infra; docker-compose; web vs worker; MinIO stand-in; env validated at startup"),
    "12-ingestion-api.html": ("鉴权+Zod+入队 · processEventBatch · 攒批上报 · 两道关 · 快返回",
                              "auth+Zod+enqueue; processEventBatch; batched reporting; two gates; fast return"),
    "13-event-types-merge.html": ("事件信封 · discriminatedUnion · body 继承链 · 两套 id · 合并最新者胜 · 18→3",
                                  "event envelope; discriminatedUnion; body inheritance; two ids; latest-wins merge; 18→3"),
    "14-ingestion-queue.html": ("Redis+BullMQ · 队列放指针 fileKey · S3 存本体 · 分片 · 主/次队列 · 重试退避",
                                "Redis+BullMQ; queue holds fileKey pointer; S3 stores body; sharding; primary/secondary; retry backoff"),
    "15-ingestion-service.html": ("mergeAndWrite 分派 · 双输入(S3 事件+CH 记录) · mergeRecords 左折叠 · 三条不覆盖规则 · event_ts 版本戳 · 只入队不直写",
                                  "mergeAndWrite dispatch; two inputs (S3 events + CH record); mergeRecords left-fold; three don't-overwrite rules; event_ts stamp; enqueue not direct-write"),
    "16-token-counting-cost.html": ("provided 压倒 computed · findModel 正则匹配 · tokenizer 分词 · matchPricingTier · price×units · 项目价覆盖全局",
                                    "provided beats computed; findModel regex match; tokenizer counting; matchPricingTier; price×units; project price overrides global"),
    "17-clickhouse-writer.html": ("单例批写器 · 每表内存队列 · batchSize/writeInterval 双触发 · 批量 INSERT · 优雅排空 · 内存换吞吐(S3 兜底)",
                                  "singleton writer; per-table memory queues; batchSize/writeInterval triggers; bulk INSERT; graceful drain; memory-for-throughput (S3 backstop)"),
    "18-opentelemetry-ingestion.html": ("OTLP 端点 · protobuf/JSON · 万能适配器 · 优先级属性键 gen_ai/ai/llm · 映射成原生事件 · 边缘适配核心归一",
                                        "OTLP endpoint; protobuf/JSON; universal adapter; priority keys gen_ai/ai/llm; maps to native events; adapt-at-edge unify-at-core"),
    "19-media-blob-storage.html": ("大二进制不进 ClickHouse · @@@langfuseMedia@@@ 引用 · presigned 直传 S3 · sha256 内容寻址去重 · blob_storage_file_log 台账",
                                   "big binaries stay out of ClickHouse; @@@langfuseMedia@@@ reference; presigned direct S3 upload; sha256 content-addressed dedup; blob_storage_file_log ledger"),
    "20-web-app-architecture.html": ("Next.js · Pages Router 为主 · 三种 API(tRPC/REST/App-Router) · features 纵向切片 · 对内类型安全对外契约稳定",
                                     "Next.js; mostly Pages Router; three APIs (tRPC/REST/App-Router); features vertical slices; internal type-safety vs external stable contract"),
    "21-trpc-backbone.html": ("appRouter 聚合 ~64 路由 · context 注入 session/prisma · procedure=可叠中间件栈 · RBAC 从输入取 projectId · 安全靠结构",
                              "appRouter aggregates ~64 routers; context injects session/prisma; procedure=stackable middleware; RBAC pulls projectId from input; security by structure"),
    "22-repository-layer.html": ("queryClickhouse 统一执行器 · OTel/log_comment 标签/退避重试/资源错误包装 · 回看时间窗 2天/1小时 · 流式变体",
                                "queryClickhouse unified executor; OTel/log_comment tags/backoff retry/resource-error wrap; look-back windows 2d/1h; streaming variants"),
    "23-filtering-search-bar.html": ("FilterState 中间契约 · 编译到 CH/PG 两套 SQL · 随机占位符防注入 · 强制 project_id · 搜索栏受控编辑器 · AI filter 往返丢幻觉",
                                     "FilterState intermediate contract; compiles to CH/PG SQL; random placeholders block injection; mandatory project_id; search bar controlled editor; AI filter round-trip drops hallucinations"),
    "24-lists-and-tables.html": ("getTracesTableGeneric 四形状 · 紧凑行 vs 指标并发 · joinTableCoreAndMetrics 按 id 合并 · 按需 JOIN/FINAL · 表态 URL 真源三层",
                                 "getTracesTableGeneric four shapes; compact rows vs metrics parallel; joinTableCoreAndMetrics merge by id; conditional JOIN/FINAL; table state URL-as-truth three layers"),
    "25-trace-detail-tree.html": ("byIdWithObservationsAndScores 全量取树 · 并行树+评分 · includeIO:false 懒加载 · partition CORRECTION · verbosity 封顶 · 列表/详情同纪律两尺度",
                                  "byIdWithObservationsAndScores full tree fetch; parallel tree+scores; includeIO:false lazy-load; partition CORRECTION; verbosity cap; list/detail one discipline two scales"),
    "26-sessions.html": ("session = traces 按 session_id 分组聚合 · 派生视图非新实体 · user_ids/duration/总成本 · 复用第24课表格机制 · 永远一致零额外写",
                         "session = traces grouped by session_id; derived view not new entity; user_ids/duration/total cost; reuses L24 table machinery; always consistent zero extra writes"),
    "27-public-rest-api.html": ("路由工厂统一鉴权/限流/校验 · Redis 缓存+负缓存扛量 · 文件夹版本 v1/v2/v3 · Fern 契约生成多语言 SDK · 对外求稳",
                                "route factory unifies auth/rate-limit/validation; Redis cache+negative caching scales; folder versions v1/v2/v3; Fern contract generates multi-language SDKs; external stability"),
    "28-scoring-model.html": ("score = 评估的原子单位 (name/value/dataType/source) · 三种刻度数值/分类/布尔 · 布尔是锁死的特殊分类 · config 是 name 的 schema 保可比 · 三来源 API/EVAL/ANNOTATION 同写 scores 表",
                              "score = evaluation's atomic unit (name/value/dataType/source); three scales numeric/categorical/boolean; boolean is a locked special category; config is a name's schema for comparability; three sources API/EVAL/ANNOTATION write one scores table"),
    "29-llm-as-a-judge.html": ("用一个 LLM 给另一个 LLM 打分 · 三件套模板/评估器/执行 · 变量映射把 trace 列填进 {{占位符}} · 结构化输出 {score,reasoning} · reasoning→comment · source=EVAL 经 SCORE_CREATE 回流第12课摄取链路",
                               "use one LLM to score another; three pieces template/evaluator/execution; variable mapping fills trace columns into {{placeholders}}; structured output {score,reasoning}; reasoning→comment; source=EVAL flows back via SCORE_CREATE through L12 ingestion"),
    "30-eval-execution-pipeline.html": ("事件驱动 createEvalJobs 扇出到 ACTIVE 评估器 · 两级队列创建/执行解耦 · 三道闸去重/采样/延迟 · JobExecution 状态机 PENDING→COMPLETED/ERROR/CANCELLED/DELAYED · langfuse- 前缀防无限循环",
                                        "event-driven createEvalJobs fans out to ACTIVE evaluators; two-stage queues decouple create/execute; three gates dedup/sampling/delay; JobExecution state machine PENDING→COMPLETED/ERROR/CANCELLED/DELAYED; langfuse- prefix guards against infinite loops"),
    "31-code-based-evaluation.html": ("确定性评估：写函数算分 vs LLM 概率判断 · dispatcher 策略模式 {name,dispatch} · Lambda 沙箱(按语言)/本地 vm(insecure-local) · 沙箱铁律禁网络+限大小256KB/5.5MB/256KB+超时 · 同回流 source=EVAL",
                                      "deterministic eval: a function computes the score vs LLM's probabilistic judgment; dispatcher strategy pattern {name,dispatch}; Lambda sandbox (per-language)/local vm (insecure-local); sandbox iron rules no-network+size caps 256KB/5.5MB/256KB+timeout; same flow-back source=EVAL"),
    "32-human-annotation.html": ("第三种 score 来源 source=ANNOTATION 闭合三来源 · 常作 ground truth 校准 AI 裁判 · 标注队列绑 scoreConfigIds · item 评 TRACE/OBSERVATION/SESSION · 5 分钟软锁防重复标注 · 同回流 scores 表",
                                 "third score source source=ANNOTATION closes the three sources; often ground truth to calibrate the AI judge; annotation queue binds scoreConfigIds; items review TRACE/OBSERVATION/SESSION; 5-minute soft lock prevents double-annotation; same flow-back into scores table"),
    "33-monitors-and-alerting.html": ("主动评估：把质量监测从拉(看仪表盘)变推(越线告警) · monitor 复用 DashboardWidget 的 view/filters/metric · window/cadence/阈值 · severity 状态机 OK/WARNING/ALERT · 只在变化时 emit 防刷屏 · 发布 WebhookQueue 解耦投递",
                                      "active evaluation: turn quality monitoring from pull (dashboard) to push (alert on crossing); a monitor reuses DashboardWidget's view/filters/metric; window/cadence/thresholds; severity state machine OK/WARNING/ALERT; emit only on change to avoid spam; publish to WebhookQueue for decoupled delivery"),
    "34-datasets-and-items.html": ("数据集=一组测试用例(item: input+expectedOutput+metadata) · 题可从真实 trace 提拔(sourceTraceId) · 数据项版本化主键(id,projectId,validFrom) · 改题=关旧版盖validTo+插新版(SCD Type2) · run 钉住 validFrom 保实验可复现",
                                   "a dataset = a set of test cases (item: input+expectedOutput+metadata); questions promotable from real traces (sourceTraceId); items versioned by key (id,projectId,validFrom); editing = close old (stamp validTo) + insert new (SCD Type 2); a run pins validFrom for reproducible experiments"),
    "35-dataset-runs.html": ("run=一场考试(某配置跑整套题) · run item 把 runId+itemId→traceId 三元钉一起 · run 的 trace 就是普通 trace 复用前5部分 · 镜像 CH dataset_run_items_rmt 反范式快照题面(ReplacingMergeTree) · dataset-run-item-upsert 自动触发评分 · 按 run 聚合 agg_scores_avg",
                             "a run = an exam sitting (a config runs the whole set); a run item pins runId+itemId→traceId three-way; a run's trace is an ordinary trace reusing the first five parts; mirrored to CH dataset_run_items_rmt with a denormalized question snapshot (ReplacingMergeTree); dataset-run-item-upsert auto-triggers scoring; aggregate by run via agg_scores_avg"),
    "36-experiments-and-comparison.html": ("实验=prompt×数据集×模型服务端自动跑(createExperimentJobClickhouse 逐题 replaceVariablesInPrompt→调LLM→产trace) · trace 标 PromptExperiments+链接prompt+钉item版本 · 评分自动接第30/35课 · 对比靠 baseline+增量(绝对分难判) · Part6 闭环把能打分升级为能决策",
                                            "experiment = prompt × dataset × model run server-side (createExperimentJobClickhouse per question replaceVariablesInPrompt→call LLM→produce trace); trace tagged PromptExperiments + links prompt + pins item version; scoring auto-connects via L30/35; comparison via baseline + deltas (absolute scores hard to judge); Part 6 closes the loop upgrading scoring into deciding"),
    "37-prompt-management.html": ("prompt = 专为 prompt 定制的 git：(name,version) 唯一、版本自增不可变+commitMessage · label(production/latest) 是唯一可移动指针，打新版自动从旧版摘除 · 按 label 取=配置与代码分离(发布/回滚秒级零部署)、按 version 取=绝对复现 · protected labels 防误操作 · PromptDependency 组合复用(childLabel浮动/childVersion钉死)",
                                  "a prompt = git tailored for prompts: (name,version) unique, version auto-increments immutably + commitMessage; a label (production/latest) is a unique movable pointer, tagging a new version auto-strips it from the old; fetch by label = config-code separation (second-scale release/rollback, zero-deploy), fetch by version = absolute reproducibility; protected labels guard against fat-fingering; PromptDependency composition reuse (childLabel floating / childVersion pinned)"),
    "38-prompt-serving-caching.html": ("生产每次 LLM 调用都取 prompt 故须快 · PromptService 用 Redis read-through(命中返回/未命中回库回填 SET EX ttl) · 服务时解析依赖内联成自包含成品(深度上限+seen 环检测) · epoch 失效：缓存 key 嵌项目级 epoch 令牌，改动只转令牌不删 key，旧 key 失联按 TTL 过期(O(1) 不漏)",
                                       "production fetches a prompt on every LLM call so it must be fast; PromptService uses a Redis read-through (hit returns / miss falls back and backfills SET EX ttl); resolves dependencies into a self-contained product at serving time (depth cap + seen cycle check); epoch invalidation: the cache key embeds a project-scoped epoch token, a change just rotates the token without deleting keys, old keys orphaned and expire by TTL (O(1), never misses)"),
    "39-playground-llm-connections.html": ("Playground=同一引擎的交互式前台，复用 fetchLLMCompletion(评估第29课/实验第36课同一核心) · LlmApiKeys.secretKey 用 AES-256-GCM 认证加密存密文+displaySecretKey 脱敏展示+adapter 抽象 provider · authTag 防篡改、随机 IV、即用即解 · LlmSchema/LlmTool 可复用积木 · Part7 收束开发者工作流闭环",
                                           "the Playground = the same engine's interactive front desk, reusing fetchLLMCompletion (same core as eval L29/experiment L36); LlmApiKeys.secretKey stores ciphertext via AES-256-GCM authenticated encryption + displaySecretKey masked display + adapter abstracts the provider; authTag anti-tamper, random IV, decrypt-on-use; LlmSchema/LlmTool reusable blocks; Part 7 seals the developer-workflow loop"),
    "40-dashboards-and-widgets.html": ("仪表盘看全局聚合 · Dashboard(definition 布局+板级 filters)装一排 DashboardWidget · widget=声明式查询(view+dimensions+metrics+filters)+图表(chartType 9种) · 查询与呈现解耦 · 一份查询形状三处复用(仪表盘画图/第33课监控比阈值/第41课引擎编SQL)，MonitorView=DashboardWidgetViews 去掉 TRACES",
                                       "dashboards see global aggregation; a Dashboard (definition layout + board-level filters) holds a row of DashboardWidgets; a widget = a declarative query (view+dimensions+metrics+filters) + a chart (chartType, 9 types); query/presentation decoupled; one query shape reused three ways (dashboard charts/L33 monitor thresholds/L41 engine SQL), MonitorView = DashboardWidgetViews minus TRACES"),
    "41-query-engine.html": ("查询引擎=声明式查询→ClickHouse SQL 编译器 · 语义层 dataModel 把逻辑名(name/totalCost)映射到真实 SQL 列/表达式 · QueryBuilder.build 对照字典译维度→GROUP BY/度量→聚合/时间分桶/过滤→参数化 WHERE/连表 · 值走 parameters 防注入(第23课) · view v1/v2 版本化护历史 · 一引擎多消费保口径一致",
                            "the query engine = a declarative-query → ClickHouse SQL compiler; the semantic-layer dataModel maps logical names (name/totalCost) to real SQL columns/expressions; QueryBuilder.build consults the dictionary to translate dimensions→GROUP BY/measures→aggregations/time-bucketing/filters→parameterized WHERE/joins; values go via parameters for injection safety (L23); view v1/v2 versioning protects history; one engine for many consumers keeps definitions consistent"),
    "42-models-and-pricing.html": ("定价数据模型喂第16课成本计算 · matchPattern 一条正则统一各家命名(provider前缀/区域前缀/版本后缀/@date) · pricingTiers 默认档+条件档分级定价(matchPricingTier 按 priority 评 AND 条件，否则回落默认) · prices 分项每token计费(输入/输出/缓存读) · 158条种子价 default-model-prices.json upsert，项目可自定义覆盖 · 规则即数据",
                                   "the pricing data model feeds Lesson 16's cost computation; matchPattern unifies naming with one regex (provider/region prefixes, version suffix, @date); pricingTiers tier pricing with a default + conditional tiers (matchPricingTier evaluates AND conditions by priority, else default); prices bills line-by-line per token (input/output/cache-read); 158 seed prices in default-model-prices.json are upserted, projects can override; rules as data"),
    "43-cloud-usage-metering.html": ("Cloud 专属平台计费(与你的LLM成本反向两笔账，自托管不收费) · 按观测数计量：每小时 cron 从CH数各org观测、对有Stripe customerId的org调 meterEvents.create 上报由Stripe出账(backOff重试) · 命门「恰好一次」：cronJobs表分布式锁+台账，整点对齐+Processing互斥+20分钟兜底接管 · 计费要exactly-once · 观测是对齐价值的计费单位 · cloudSpendAlert 管你的LLM花费",
                                     "Cloud-exclusive platform billing (an opposite ledger from your LLM cost, self-host charges nothing); meter by observation count: an hourly cron counts each org's observations from CH and for orgs with a Stripe customerId calls meterEvents.create to report, Stripe invoicing (backOff retry); the crux is 'exactly once': a cronJobs table as distributed lock + ledger, hour-aligned + Processing mutex + 20-min fallback takeover; billing must be exactly-once; the observation is a value-aligned billing unit; cloudSpendAlert manages your LLM spend"),
    "44-automations-webhooks.html": ("自动化=Trigger(eventSource/eventActions/filter 何时)→Action(WEBHOOK/SLACK/GITHUB_DISPATCH 做什么)，AutomationExecution 留执行记录(schema.prisma:1613/1635/1659/1690)，第33课告警经此投递 · 命门是 SSRF：让服务器请求用户填的URL，攻击者可借此打内网、偷169.254.169.254的云凭证 · 纵深防御：协议白名单(http/https)+端口白名单(80/443)+主机名黑名单(localhost/metadata)+IP CIDR黑名单(内网/loopback/link-local)+fail-closed(解析不了就拦) · 校验在请求时对真实IP做防DNS-rebinding · 投递硬化：HMAC签名(x-langfuse-signature)+超时+退避重试+2xx校验+反复失败自动停用",
                                     "Automation = Trigger (eventSource/eventActions/filter = when) → Action (WEBHOOK/SLACK/GITHUB_DISPATCH = what), AutomationExecution keeps run records (schema.prisma:1613/1635/1659/1690); Lesson 33 alerts are delivered through it; the Achilles heel is SSRF: making the server fetch a user-supplied URL lets attackers hit the internal net and steal 169.254.169.254's cloud credentials; defense in depth: protocol allowlist (http/https) + port allowlist (80/443) + hostname blocklist (localhost/metadata) + IP CIDR blocklist (private/loopback/link-local) + fail-closed (can't resolve → block); the check runs at request time on the real IP to defeat DNS-rebinding; delivery hardening: HMAC signing (x-langfuse-signature) + timeout + backoff retry + 2xx check + auto-disable on repeated failure"),
    "45-slack-and-notifications.html": ("Slack=一等公民投递通道(vs第44课裸webhook) · OAuth安装：InstallProvider(@slack/oauth)托管授权，storeInstallation 把 bot令牌 encrypt 入库 upsert SlackIntegration(projectId唯一·一项目一连接)，复用第39课 AES-256-GCM · 发消息：getWebClientForProject 经 fetchInstallation+decrypt 取令牌、构造带重试(3次)WebClient，sendMessage 调 chat.postMessage · Block Kit 富消息：buildMonitorAlertSlackMessage 按severity染色(ALERT红/WARNING黄/OK绿)，含标题正文时间戳+查看按钮 · notificationQueue 站内通知(COMMENT_MENTION) · 新功能=旧能力(加密/单例/分页/重试/队列)的新组合；信任模型决定保管强度；用时实时解密防凭据失效",
                                       "Slack = a first-class delivery channel (vs Lesson 44's naked webhook); OAuth install: InstallProvider (@slack/oauth) hosts auth, storeInstallation encrypts the bot token and upserts SlackIntegration (projectId unique, one connection per project), reusing Lesson 39 AES-256-GCM; sending: getWebClientForProject pulls the token via fetchInstallation+decrypt, builds a retrying (3×) WebClient, sendMessage calls chat.postMessage; Block Kit rich messages: buildMonitorAlertSlackMessage tints by severity (ALERT red/WARNING amber/OK green) with title, body, timestamp + view button; notificationQueue for in-app notifications (COMMENT_MENTION); new feature = new combination of old capabilities (encryption/singleton/pagination/retry/queue); the trust model sets safekeeping strength; decrypt at use time to guard stale credentials"),
    "46-analytics-integrations.html": ("你的数据你的去处(vs第43课平台收你钱)：把trace/observation/score导回你自己的PostHog/Mixpanel(产品分析)和S3/S3兼容/Azure(对象存储归档) · 三个同构集成(schema.prisma:1183/1196/1209)：projectId主键·加密凭据(复用第39课)·lastSyncAt水位·enabled·exportSource · 两级fan-out队列：调度队列(cron→查enabled→addBulk逐项目扇出，jobId=projectId-lastSyncAt去重+removeOnFail)+处理队列(每项目instrumentAsync各开新trace)，三集成各独立队列互不拖累 · 增量水位：min=lastSyncAt||createdAt，max=min(次日界,now−30min)，30分钟缓冲避在途数据·按日切块限单次工作量对齐CH分区，成功后挪lastSyncAt · blob流式导出：stream pipeline逐行转CSV/JSON/JSONL(±gzip)经StorageServiceFactory写S3/GCS/Azure不撑爆内存",
                                       "Your data, your destinations (vs Lesson 43's platform charging you): export trace/observation/score back to your own PostHog/Mixpanel (product analytics) and S3/S3-compatible/Azure (object-storage archival); three isomorphic integrations (schema.prisma:1183/1196/1209): projectId key, encrypted credentials (reuse Lesson 39), lastSyncAt watermark, enabled, exportSource; two-level fan-out queue: scheduling queue (cron→find enabled→addBulk fans out per project, jobId=projectId-lastSyncAt dedup + removeOnFail) + processing queue (each project instrumentAsync opens a fresh trace), each integration has its own queue pair with no mutual drag; incremental watermark: min=lastSyncAt||createdAt, max=min(next-day-boundary, now−30min), 30-min buffer avoids in-flight data, day-chunking bounds per-run work and aligns CH partitions, advance lastSyncAt on success; blob streaming export: stream pipeline transforms row by row into CSV/JSON/JSONL (±gzip) via StorageServiceFactory to S3/GCS/Azure without memory blowup"),
    "47-batch-exports-and-actions.html": ("一个查询两条路：批量导出(只读产文件)与批量操作(改数据：删/加标注队列/加数据集/重评)都基于第23课过滤、都走队列异步有状态机、都流式+分块防内存爆 · 批量导出=流式→文件→限时链接→邮件：BatchExportStatus(QUEUED→PROCESSING→COMPLETED)，getDatabaseReadStreamPaginated+pipeline转CSV/JSON，uploadFileBuffered传对象存储，getSignedUrl给限时下载链接，记expiresAt后sendBatchExportSuccessEmail · 批量操作=分块1000+幂等：cutoffCreatedAt快照边界固定目标集，CHUNK_SIZE=1000保护DB细化重试粒度，processActionChunk按actionId分发(trace-delete/add-to-annotation-queue/dataset-delete/eval-create) · 幂等是铁律：队列失败整体重试、已处理块会重跑，每个action必须重复执行不出错不翻倍副作用(同第43课恰好一次) · 限时签名URL：导出含敏感数据给带过期的临时授权而非永久公开",
                                          "One query two paths: batch export (read-only, produces a file) and batch action (mutate data: delete/add-to-annotation-queue/add-to-dataset/re-eval) both build on Lesson 23's filter, both go async via queue with a state machine, both use streaming + chunking to avoid memory blowup; batch export = stream → file → time-limited link → email: BatchExportStatus (QUEUED→PROCESSING→COMPLETED), getDatabaseReadStreamPaginated+pipeline transform to CSV/JSON, uploadFileBuffered to object storage, getSignedUrl gives a time-limited download link, record expiresAt then sendBatchExportSuccessEmail; batch action = chunks of 1000 + idempotency: cutoffCreatedAt snapshot boundary fixes the target set, CHUNK_SIZE=1000 protects the DB and refines retry granularity, processActionChunk dispatches by actionId (trace-delete/add-to-annotation-queue/dataset-delete/eval-create); idempotency is the iron rule: queue failure retries the whole job, processed chunks rerun, every action must not error on repeat nor double side effects (same as Lesson 43's exactly-once); time-limited signed URL: exports hold sensitive data so give a temporary-authorization link with an expiry rather than permanently-public"),
    "48-auth-and-sessions.html": ("运维视角第一问：谁能进来 · 鉴权=你是谁：NextAuth 托管，两条路——CredentialsProvider(邮箱密码,bcrypt)+十几种SSO(Google/Okta/AzureAD/Keycloak/WorkOS…外包给可信IdP)，provider 静态(env)+动态(DB)两源，扩展PrismaAdapter落库 · 密码登录安全护栏：SSO强制三闸(AUTH_DISABLE_USERNAME_PASSWORD实例级/域名黑名单/EE多租户)、时序攻击防护(用户不存在也跑一遍bcrypt防枚举)、SSO用户拦截(password=null引导走IdP)、bcrypt(12轮)比对 · 会话=JWT：strategy:jwt无状态自带签名身份、maxAge过期，比DB session更适合多实例水平扩展(本地验签免查库)，代价是即时吊销难 · session回调注入身份：查organizationMemberships→projects+ProjectMemberships塞进session=通往第49课RBAC的桥；回调被instrumentAsync包裹(连登录都自观测)",
                                  "The operator's first question: who gets in. Auth = who you are: NextAuth-hosted, two paths — CredentialsProvider (email-password, bcrypt) + a dozen-plus SSO (Google/Okta/AzureAD/Keycloak/WorkOS… outsourced to a trusted IdP); providers from two sources static(env)+dynamic(DB); extended PrismaAdapter persists. Password-login guardrails: three SSO-enforcement gates (AUTH_DISABLE_USERNAME_PASSWORD instance / domain blocklist / EE multi-tenant), timing-attack defense (run bcrypt even when the user is absent to block enumeration), SSO-user interception (password=null guides to the IdP), bcrypt(12-round) compare. Session = JWT: strategy:jwt stateless self-signed identity, maxAge expiry, better suited to multi-instance horizontal scaling than DB sessions (verify locally, no DB lookup), at the cost of harder instant revocation. Session callback injects identity: queries organizationMemberships→projects+ProjectMemberships into the session = the bridge to Lesson 49's RBAC; the callback is wrapped in instrumentAsync (even login self-observes)"),
    "49-rbac-apikeys-scim.html": ("授权=你能干什么，两类对象：人(UI)走RBAC、机器(SDK/API)走API key，加SCIM企业自动化 · RBAC角色→scope：projectRoleAccessRights Record<Role,Scope[]> 把OWNER/ADMIN/MEMBER/VIEWER/NONE映射到细粒度scope(traces:delete等，VIEWER仅read、NONE空)，判权限问角色含不含该scope · 纵深防御前后端双查：前端useHasProjectAccess隐藏按钮(体验)、后端throwIfNoProjectAccess抛FORBIDDEN(安全)，前端可绕过真正的闸是后端 · API key两层哈希：fastHashedSecretKey=sha256(确定性O(1)快查可缓存)+hashedSecretKey=bcrypt(加盐慢安全)+displaySecretKey(打码)，sk明文只创建时返回一次，验证算快哈希查Redis→PG，老key bcrypt验后升级，不存在缓存API_KEY_NON_EXISTENT防刷库 · SCIM让Okta/AzureAD自动开通注销用户(EE)",
                                  "Authorization = what you can do, two subjects: humans (UI) take RBAC, machines (SDK/API) take API keys, plus SCIM for enterprise automation. RBAC role→scope: projectRoleAccessRights Record<Role,Scope[]> maps OWNER/ADMIN/MEMBER/VIEWER/NONE to fine-grained scopes (traces:delete etc, VIEWER read-only, NONE empty), check whether the role contains the scope. Defense in depth dual check: front-end useHasProjectAccess hides buttons (UX), back-end throwIfNoProjectAccess throws FORBIDDEN (security); the front end is bypassable, the real gate is the back end. API key two-tier hash: fastHashedSecretKey=sha256 (deterministic O(1) fast lookup, cacheable) + hashedSecretKey=bcrypt (salted slow secure) + displaySecretKey (masked); the sk cleartext is returned only at creation; verification computes the fast hash and looks up Redis→PG, legacy keys verified by bcrypt then upgraded, nonexistent cached as API_KEY_NON_EXISTENT to stop DB hammering. SCIM lets Okta/AzureAD auto-provision/deprovision users (EE)"),
    "50-open-core-and-entitlements.html": ("开源核：全代码开放(含企业功能)，免费/付费的区别在运行时能否启用、不在有没有代码 · plan分层：组织挂plan，默认oss(免费自托管)，付费cloud:hobby/core/pro/enterprise+self-hosted:pro/enterprise，isCloudPlan/isSelfHostedPlan按前缀分 · 总表+一道闸：entitlementAccess Record<Plan,{entitlements二元功能, entitlementLimits数值额度number/false无限}>；hasEntitlement(admin→true、plan??oss兜底、includes)是所有功能共用的闸，收敛权威同第49课RBAC · EE许可证：isEnterpriseLicenseAvailable——Cloud任何区域有企业功能，自托管看LANGFUSE_EE_LICENSE_KEY是否langfuse_ee_开头(langfuse_pro_不算企业) · fail-safe默认：无plan兜底oss(最小权益、付费默认关)而非默认全开；EE代码在@langfuse/ee，依赖web→ee→shared",
                                          "Open core: all code is open (incl. enterprise features); free vs paid lies in runtime enablement, not whether the code exists. Plan tiering: an org carries a plan, defaulting to oss (free self-host), paid has cloud:hobby/core/pro/enterprise + self-hosted:pro/enterprise; isCloudPlan/isSelfHostedPlan split by prefix. Master table + one gate: entitlementAccess Record<Plan,{entitlements binary features, entitlementLimits numeric quotas number/false unlimited}>; hasEntitlement (admin→true, plan??oss fallback, includes) is the shared gate in front of every feature, converging authority like Lesson 49's RBAC. EE license: isEnterpriseLicenseAvailable — Cloud (any region) has enterprise features, self-hosting checks whether LANGFUSE_EE_LICENSE_KEY starts with langfuse_ee_ (langfuse_pro_ isn't enterprise). Fail-safe default: no plan falls back to oss (least entitlement, paid off by default) not all-on; EE code in @langfuse/ee, dependency web→ee→shared"),
    "51-self-observability-and-config.html": ("自我可观测(dogfooding)：Langfuse用它帮你观测LLM应用的同一套OTel观测自己 · instrumentAsync(instrumentation/index.ts:54)是span包装器——开span/跑逻辑/自动traceException/span.end，第30/33/46/48课都在用；同模块还有getCurrentSpan/getTracer/recordGauge/Increment/Histogram，还能反向摄取OTel(OtelIngestionProcessor) · 日志自动关联trace：winston的tracingFormat每行注入当前span的trace_id/span_id(含dd.*Datadog风格)，于是日志↔链路一键互跳，排查神器；格式text/json、级别由env定 · 配置即校验：所有env过Zod(共享EnvSchema=z.object、web createEnv分server/client)——fail-fast(启动即报错非半路崩)、类型安全(z.coerce/z.enum)、server/client边界(防密钥泄露进前端) · 可观测管运行时透明、配置校验管启动时堵错",
                                              "Self-observability (dogfooding): Langfuse observes itself with the same OTel it uses to observe your LLM apps. instrumentAsync (instrumentation/index.ts:54) is a span wrapper — open span/run logic/auto-traceException/span.end, used by Lessons 30/33/46/48; the same module has getCurrentSpan/getTracer/recordGauge/Increment/Histogram, and can ingest OTel in reverse (OtelIngestionProcessor). Logs auto-correlate with traces: winston's tracingFormat injects the current span's trace_id/span_id (incl. dd.* Datadog style) into every line, so logs↔traces jump in one click, a debugging gem; format text/json, level by env. Config as validation: all env through Zod (shared EnvSchema=z.object, web createEnv splitting server/client) — fail-fast (error at startup not crash mid-run), type-safe (z.coerce/z.enum), server/client boundary (prevent secrets leaking to the front end). Observability owns runtime transparency, config validation owns boot-time error-plugging"),
    "52-data-lifecycle-and-deletion.html": ("数据有一生：写入→分析→删除；一条trace散在三存储(Postgres元数据/ClickHouse海量事件/S3大块负载)，删除必须跨三处一处不漏，漏删=数据残留(合规隐患) · 删除有顺序：projectDelete先并行清CH+S3、最后才删Postgres——PG记录是「没删完」的重试锚点，先删PG会让CH/S3成无主孤儿 · 三种删除：①数据保留(EE，按retentionDays自动清旧，第46课同款两级fan-out，cutoffDate只删过期)②trace删除(按需，第47课批量操作走它)③项目删除(级联) · 后台迁移在线演进schema：给亿万行回填/重组不停机，BackgroundMigration的state记进度可断点续传(同第46课水位)、lockedAt/workerId锁保证单worker、心跳续约、结果落库 · 一脉相承：删除序=保留锚点、迁移state=可恢复、单worker锁",
                                            "Data has a lifetime: write→analyze→delete; one trace is scattered across three stores (Postgres metadata/ClickHouse massive events/S3 bulky payloads), so deletion must span all three missing none, a miss = data residue (compliance hazard). Deletion has an order: projectDelete cleans CH+S3 in parallel first, deletes Postgres last — the PG record is the retry anchor for 'not done yet', deleting PG first orphans CH/S3 data. Three deletions: ① data retention (EE, auto-cleans old by retentionDays, same two-level fan-out as Lesson 46, cutoffDate deletes only expired) ② trace deletion (on-demand, Lesson 47's batch action uses it) ③ project deletion (cascade). Background migrations evolve schema online: backfill/reorganize billions of rows without downtime, BackgroundMigration's state records progress for checkpoint resume (like Lesson 46's watermark), lockedAt/workerId lock ensures single-worker, heartbeat renewal, result persisted. One lineage: deletion order=keep anchor, migration state=resumable, single-worker lock"),
    "53-build-test-dev-workflow.html": ("平台自己怎么构建/测试/迭代 · pnpm monorepo：web/worker/packages/shared/ee 一个仓库，依赖只朝下(web/worker/ee→shared，shared不反向依赖)，pnpm强制(only-allow)+minimumReleaseAge防供应链投毒，共享代码一个commit原子改 · Turbo任务管道：dependsOn的^build顺依赖图自动排拓扑构建序(shared先web/worker后) · Turbo内容哈希缓存：把输入(源码+依赖+env)算哈希，没变就重放缓存outputs跳过构建，只重建真正改了的包，CI缓存全中几秒过 · 有副作用任务cache:false：dev(常驻)、db:generate(写node_modules)效果不在outputs里、重放日志恢复不了 · 一键开发流：dx一条命令从空环境到能跑(装依赖→docker基础设施→重置库→灌种子→dev)，--filter缩到单包，seed CLI按scenario生成逼真测试数据让bug可廉价复现",
                                        "How the platform itself is built/tested/iterated. pnpm monorepo: web/worker/packages/shared/ee in one repo, dependencies point only down (web/worker/ee→shared, shared doesn't reverse-depend), pnpm enforced (only-allow)+minimumReleaseAge against supply-chain poisoning, shared code atomic one-commit changes. Turbo task pipeline: dependsOn's ^build auto-orders builds topologically by the dependency graph (shared first, web/worker after). Turbo content-hash cache: hash the inputs (source+deps+env), if unchanged replay cached outputs skipping the build, rebuild only changed packages, all cache hits on CI may pass in seconds. Side-effecting tasks cache:false: dev (long-running), db:generate (writes node_modules) — effects not in outputs, unrestorable by log replay. One-command dev: dx goes from empty environment to running (install→docker infra→reset DBs→seed→dev), --filter scopes to one package, seed CLI generates realistic test data by scenario making bugs cheaply reproducible"),
    "54-design-themes-synthesis.html": ("退后一步：把53课反复出现的设计决策收拢成六个名字，都从ARCHITECTURE_PRINCIPLES.md那句「为宽的结构化事件数据做高吞吐探索式可观测」推导而来 · ①宽事件：observation为分析单位、trace为关联句柄，宽而富+高基数→调查unknown unknowns不必预建指标 · ②不可变：追加而非更新，改=追加新行+查时合并(L13 AggregatingMergeTree)，避读时去重隐藏成本 · ③异步：快接收、队列里慢处理，衍生fan-out/幂等/水位/锁(L30/43/46/52) · ④双(三)存储：PG(OLTP)+CH(OLAP列存)+S3(负载)各归各家、谨慎反范式 · ⑤多租户：处处projectId、鉴权→RBAC→entitlement层层隔离 · ⑥成本是约束：每个活动部件须挣回运维负担、契约scale-aware · 六主题非六技巧而是一套世界观的六切面；迁移关键是钉死目标+规模前提再用「部件配不配」做减法",
                                        "Step back: gather the design decisions recurring across 53 lessons into six names, all derived from ARCHITECTURE_PRINCIPLES.md's 'high-throughput exploratory observability on wide structured event data'. ① wide events: observation as analytical unit, trace as correlation handle, wide+rich+high cardinality → investigate unknown unknowns without pre-built metrics. ② immutability: append not update, modify = append new rows + merge at query (L13 AggregatingMergeTree), avoiding read-time-dedup hidden cost. ③ async: receive fast, process slowly in queues, deriving fan-out/idempotency/watermark/lock (L30/43/46/52). ④ dual (tri) storage: PG(OLTP)+CH(OLAP columnar)+S3(payloads) each goes home, careful denormalization. ⑤ multi-tenancy: projectId everywhere, auth→RBAC→entitlement layered isolation. ⑥ cost is a constraint: every moving part must earn its burden, contracts scale-aware. The six themes aren't six tricks but six facets of one worldview; the key to transferring is nailing goal+scale premises then subtracting via 'does this part deserve to exist'"),
    "55-capstone-trace-life.html": ("终章：跟着一条 trace 走完它的一生，把全部 55 课串成一条流水线 · 七个驿站：①出生(SDK创建攒批上报,L12)②摄取(API key认证→落S3→Redis队列→worker处理,L13-19/L49)③落库(散成三份:CH明细+S3负载+PG元数据,L13)④被读(列表查CH紧凑表示/详情取S3大字段/会话/REST,L20-27)⑤被评估(LLM裁判打分写回score、监控告警、数据集实验,L28-36)⑥被作用(自动化webhook/Slack、分析导出、批量导出,L44-47)⑦退场(保留期到跨三存储删除留重试锚点,L52) · 三条隐线贯穿全程：自观测(L51 dogfooding)、plan门控(L50)、projectId多租户隔离 · 一个闭环：trace产score、score驱动监控与实验反过来改进应用 · 大问题：把AI应用的不可观测变回可观测=记录→找到→评判→行动→负责任退场；真正带走的是用「目标+规模→取舍」的架构师眼光看任何系统",
                                      "Finale: follow one trace through its whole life, stringing all 55 lessons into one assembly line. Seven stations: ① born (SDK creates, batches, reports, L12) ② ingested (API-key auth→land S3→Redis queue→worker processes, L13-19/L49) ③ stored (split into three: CH detail+S3 payload+PG metadata, L13) ④ read (list queries CH compact representation/detail fetches S3 big fields/session/REST, L20-27) ⑤ evaluated (LLM judge scores write back, monitor alerts, datasets experiments, L28-36) ⑥ acted on (automation webhook/Slack, analytics export, batch export, L44-47) ⑦ retired (retention expires, cross-store deletion keeping retry anchor, L52). Three hidden threads throughout: self-observability (L51 dogfooding), plan gating (L50), projectId multi-tenant isolation. A closed loop: the trace produces a score, the score drives monitoring and experiments, in turn improving the app. The big question: turning an AI app's unobservability back into observability = record→find→judge→act→retire responsibly; what you truly carry away is seeing any system with an architect's 'goal+scale→trade-offs' eyes"),
}


def index_page(lesson_prefix="lessons/"):
    """Build the bilingual index (table of contents). Always relative links."""
    order = []   # ordered list of (part_zh, part_en)
    groups = {}  # part_zh -> [(num, fname, title_zh, title_en), ...]
    for i, (fname, tz, te, pz, pe) in enumerate(PAGES):
        if pz not in groups:
            groups[pz] = []
            order.append((pz, pe))
        groups[pz].append((i + 1, fname, tz, te))

    blocks = []
    for pz, pe in order:
        blocks.append(f'<div class="toc-part">{bi(esc(pz), esc(pe))}</div>')
        for num, fname, tz, te in groups[pz]:
            sz, se = SUBTITLES.get(fname, ("", ""))
            blocks.append(
                f'<a href="{lesson_prefix}{fname}"><span class="n">{num:02d}</span>'
                f'<span class="tt"><span class="lang-zh">{esc(tz)}</span>'
                f'<span class="lang-en">{esc(te)}</span></span>'
                f'<span class="ts"><span class="lang-zh">{esc(sz)}</span>'
                f'<span class="lang-en">{esc(se)}</span></span></a>'
            )
    toc = "\n".join(blocks)
    total = len(PAGES)
    nparts = len(order)

    title_tag = "Langfuse 图解教程 · 看懂 LLM 可观测性平台内部 / Langfuse Visual Guide"
    desc = ("从零理解整个 Langfuse LLM 工程平台的中英双语图解教程：宏观结构、数据模型、双存储、"
            "摄取链路、查询链路、评估、数据集、Prompt、仪表盘、平台与运维，每课配真实源码对应与设计取舍。")

    return f"""<!DOCTYPE html>
<html lang="zh-CN" data-lang="zh"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{LANG_BOOT}
<title>{esc(title_tag)}</title>
{head_meta(title_tag, desc, og_type="website")}
<style>{CSS}</style>
</head><body>
<div class="topbar">
  <div class="topbar-inner">
    <span class="home">🪢 <b class="lang-zh">Langfuse 图解教程</b><b class="lang-en">Langfuse Visual Guide</b></span>
    <span class="pill"><span class="lang-zh">共 {total} 课 · {nparts} 个部分</span><span class="lang-en">{total} lesson{'' if total == 1 else 's'} · {nparts} part{'' if nparts == 1 else 's'}</span></span>
    <button class="langtoggle" onclick="lvgToggleLang()" aria-label="switch language"><span class="lang-zh">EN</span><span class="lang-en">中</span></button>
  </div>
  <div class="progress"><span style="width:100%"></span></div>
</div>
<div class="wrap">
  <div class="hero index">
    <div class="part">{bi("面向工程师 · 从第一性原理到源码", "For engineers · first principles to source")}</div>
    <h1><span class="lang-zh">用图解读懂整个 Langfuse</span><span class="lang-en">Understand all of Langfuse, visually</span></h1>
    <p class="lead"><span class="lang-zh">这套教程带你<strong>层层深入</strong>：先建立<strong>宏观全景</strong>与<strong>可观测性 2.0 / 宽事件</strong>基础，看懂 <strong>trace/observation/score 数据模型</strong>与 <strong>Postgres+ClickHouse 双存储</strong>，
    然后顺着数据走一遍<strong>摄取（写）</strong>与<strong>查询（读）</strong>两条链路，再逐个拆解<strong>评估</strong>·<strong>数据集</strong>·<strong>Prompt</strong>·<strong>仪表盘</strong>等子系统，最后讲透<strong>鉴权与权限</strong>·<strong>运维</strong>与<strong>如何贡献</strong>。每课配真实源码对应、手绘图与设计取舍。</span>
    <span class="lang-en">A layered tour: build the <strong>big picture</strong> and the <strong>Observability 2.0 / wide-event</strong> foundation first, understand the <strong>trace/observation/score data model</strong> and the <strong>Postgres + ClickHouse dual store</strong>,
    then follow the data through the <strong>ingestion (write)</strong> and <strong>query (read)</strong> paths, take apart the <strong>evaluation</strong>, <strong>datasets</strong>, <strong>prompt</strong> and <strong>dashboard</strong> subsystems, and finally master <strong>auth &amp; RBAC</strong>, <strong>operations</strong> and <strong>how to contribute</strong>. Every lesson maps to real source, with hand-drawn diagrams and design tradeoffs.</span></p>
    <div class="legend">
      <span><i style="background:var(--blue)"></i>{bi("宏观理解", "Big picture")}</span>
      <span><i style="background:var(--purple)"></i>{bi("细节 / 源码", "Details / source")}</span>
      <span><i style="background:var(--amber)"></i>{bi("生活类比", "Analogy")}</span>
      <span><i style="background:var(--accent)"></i>{bi("关键要点", "Key points")}</span>
    </div>
    <p style="margin:.8rem 0 0;color:var(--faint);font-size:.8rem">{bi("📌 对照 langfuse/langfuse 仓库真实源码核实 · 源码引用以“文件 + 符号名/行号”标注（行号随上游更新而变）", "📌 Verified against the real langfuse/langfuse source; references cite file + symbol/line (line numbers drift upstream)")}</p>
  </div>
  <div class="toc-search">
    <input id="q" type="search" placeholder="🔎 搜索课程 / Search lessons" autocomplete="off" aria-label="search">
    <span class="qcount" id="qcount"></span>
  </div>
  <div class="toc">{toc}</div>
  <div class="toc-empty" id="tocempty">{bi("没有匹配的课程，换个关键词试试。", "No matching lessons, try another keyword.")}</div>
  <p style="margin:2.4rem 0 0;color:var(--faint);font-size:.78rem;text-align:center">{bi("本项目是第三方、非官方的学习材料，不含 Langfuse 源码（仅引用少量标注来源的片段）；Langfuse 由其作者以 MIT 许可发布（部分企业版功能除外）。", "Third-party, unofficial learning material; contains no Langfuse source code beyond small, cited snippets. Langfuse is MIT-licensed by its authors (except some enterprise features).")}</p>
</div>
<script>{LANG_JS}</script>
<script>{SEARCH_JS}</script>
</body></html>"""
