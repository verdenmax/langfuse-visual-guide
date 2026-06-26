"""Part 1 — The Big Picture. L01 (What is Langfuse) ships as the visual baseline.

Authoring pattern: each lesson assembles its bilingual body from a list of
section strings (``_ZH`` / ``_EN``) so sections can be added one at a time and
the file stays diff-friendly. The exported value is the dict the registry
imports: ``LESSON_01 = {"zh": ..., "en": ...}``.

All technical claims are grounded in the real langfuse/langfuse source; figures
use CSS variables so they theme in light + dark mode.
"""

# ══════════════════════════════════════════════════════════════════════
# L01 · 什么是 Langfuse / What is Langfuse
# ══════════════════════════════════════════════════════════════════════
_ZH = []
_EN = []

# ── lead + life analogy ───────────────────────────────────────────────
_ZH.append(r"""
<p class="lead">
LLM 应用最让人头疼的地方是<strong>非确定性</strong>：同样的输入，今天和明天可能给出不一样的答案；
一次多步的 agent 调用里，到底是<strong>哪一步</strong>出了错、用了<strong>多少 token</strong>、花了
<strong>多少钱</strong>、慢在<strong>哪一环</strong>，光看几行日志几乎无从判断。
<a href="https://github.com/langfuse/langfuse">Langfuse</a> 是一个<strong>开源的 LLM 工程平台</strong>
（<code>langfuse/langfuse</code>，MIT 许可）。一句话：它把你 LLM 应用里那些<strong>看不见的每一步</strong>，
变成<strong>可观测、可评估、可复现</strong>的数据——围绕<strong>开发 → 监控 → 评估 → 调试</strong>这一个闭环转。
说白了，它要回答的是工程师每天都在问、却很难答的三个问题：<strong>这次到底发生了什么？好不好？怎么变得更好？</strong>
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把一个 LLM 应用想成<strong>一架飞机</strong>：平时能飞，可一旦出状况，你两眼一抹黑。Langfuse 给它装上两样东西——
  <strong>黑匣子（飞行记录仪）</strong>和<strong>实验记录本</strong>。黑匣子把每一次模型调用、每一步检索、用到的 prompt、
  消耗的 token、花掉的钱、各环节延迟，统统录下来；实验记录本则让你把“换个 prompt / 换个模型 / 改个参数”的每一次尝试
  并排摆开对比。<strong>出了事能回放，要改进有依据</strong>——这就是 Langfuse 想给 LLM 应用的东西。说到底，黑匣子负责「看见」，实验记录本负责「比较」，两者合起来才让「凭感觉调」变成「拿数据改」。
</div>
""")

_EN.append(r"""
<p class="lead">
The hardest thing about LLM apps is <strong>non-determinism</strong>: the same input can give different
answers today and tomorrow; and inside one multi-step agent run, figuring out <strong>which step</strong>
went wrong, how many <strong>tokens</strong> it burned, how much it <strong>cost</strong>, or where the
<strong>latency</strong> went is nearly impossible from a few log lines.
<a href="https://github.com/langfuse/langfuse">Langfuse</a> is an <strong>open-source LLM engineering
platform</strong> (<code>langfuse/langfuse</code>, MIT-licensed). In one line: it turns every
<strong>invisible step</strong> inside your LLM app into <strong>observable, evaluable, reproducible</strong>
data — around one loop: <strong>develop → monitor → evaluate → debug</strong>.
Put plainly, it answers the three questions engineers ask daily but struggle to answer: <strong>what actually happened this
time? was it any good? how do I make it better?</strong>
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Think of an LLM app as an <strong>airplane</strong>: it flies fine until something goes wrong — and then
  you're blind. Langfuse bolts on two things: a <strong>black box (flight recorder)</strong> and a
  <strong>lab notebook</strong>. The black box records every model call, every retrieval step, the prompt
  used, the tokens spent, the money burned and the latency of each leg; the lab notebook lets you line up
  every “try another prompt / model / parameter” experiment side by side. <strong>When things break you can
    replay; when you want to improve you have evidence</strong> — that's what Langfuse gives an LLM app. In short, the black box
    is for "seeing" and the lab notebook is for "comparing"; together they turn "tuning by vibes" into "improving with data".
  </div>
  """)

# ── macro figure + what it is ─────────────────────────────────────────
_ZH.append(r"""
<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="你的 LLM 应用通过 SDK 把数据送进 Langfuse 平台的四大能力，工程师据此持续改进">
  <text x="360" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Langfuse 站在你的应用「旁边」，而不是「里面」</text>
  <!-- app -->
  <rect x="24" y="104" width="150" height="92" rx="12" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="99" y="140" text-anchor="middle" font-size="13" font-weight="700" fill="var(--ink)">你的 LLM 应用</text>
  <text x="99" y="162" text-anchor="middle" font-size="11" fill="var(--muted)">+ SDK / OpenTelemetry</text>
  <!-- arrow app->langfuse -->
  <line x1="174" y1="150" x2="244" y2="150" stroke="var(--faint)" stroke-width="2"/>
  <polygon points="244,150 235,145 235,155" fill="var(--faint)"/>
  <text x="209" y="142" text-anchor="middle" font-size="10" fill="var(--faint)">事件</text>
  <!-- langfuse panel -->
  <rect x="250" y="44" width="300" height="216" rx="14" fill="var(--panel-2)" stroke="var(--accent)" stroke-width="2"/>
  <text x="400" y="68" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Langfuse 平台</text>
  <rect x="266" y="84" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="330" y="112" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">🔭 可观测</text>
  <text x="330" y="132" text-anchor="middle" font-size="10.5" fill="var(--muted)">trace · observation</text>
  <rect x="406" y="84" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="470" y="112" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">✅ 评估</text>
  <text x="470" y="132" text-anchor="middle" font-size="10.5" fill="var(--muted)">score · LLM 评审</text>
  <rect x="266" y="164" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="330" y="192" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">📝 Prompt 管理</text>
  <text x="330" y="212" text-anchor="middle" font-size="10.5" fill="var(--muted)">版本 · 线上拉取</text>
  <rect x="406" y="164" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="470" y="192" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">🧪 数据集/实验</text>
  <text x="470" y="212" text-anchor="middle" font-size="10.5" fill="var(--muted)">dataset · 对比</text>
  <!-- arrow langfuse->engineer -->
  <line x1="550" y1="150" x2="612" y2="150" stroke="var(--faint)" stroke-width="2"/>
  <polygon points="612,150 603,145 603,155" fill="var(--faint)"/>
  <!-- engineer -->
  <rect x="616" y="104" width="80" height="92" rx="12" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="656" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">工程师</text>
  <text x="656" y="160" text-anchor="middle" font-size="10.5" fill="var(--accent-ink)">看·查·改</text>
  <!-- feedback loop -->
  <path d="M656 196 L656 282 L99 282 L99 196" fill="none" stroke="var(--amber)" stroke-width="1.8" stroke-dasharray="5 4"/>
  <polygon points="99,196 94,205 104,205" fill="var(--amber)"/>
  <text x="377" y="276" text-anchor="middle" font-size="10.5" fill="var(--amber)">持续改进：换 prompt / 换模型 / 修链路</text>
</svg>
<div class="figcap"><b>一个闭环</b>：你的应用经 SDK 把运行事件送进 Langfuse；平台沉淀成 <b>可观测 / 评估 / Prompt / 数据集</b> 四类能力；工程师据此发现问题、改进应用，再把改进送回线上。Langfuse 始终在应用<b>旁边</b>观测，不侵入业务逻辑。</div>
</div>

<h2>它到底是什么</h2>
<p>一句话定义：<strong>一个把 LLM 应用的运行过程「数据化」的平台</strong>。它<strong>不</strong>替你训练模型，也<strong>不是</strong>又一个调用大模型的框架；
它做的事发生在你的应用<strong>之外</strong>——把每一次运行原原本本地<strong>记录、度量</strong>，并支撑你对它<strong>评估与改进</strong>。
官方把能力归为四块（在仓库里就是 <code>web/src/features/</code> 下一个个目录）：</p>

<table class="t">
  <tr><th>能力</th><th>解决什么问题</th><th>仓库里的实现</th></tr>
  <tr><td><b>🔭 可观测 Tracing</b></td><td>看清每一次调用：调用树、输入输出、token、成本、延迟</td><td class="mono">web/src/features/traces · tracing-tables</td></tr>
  <tr><td><b>✅ 评估 Evaluation</b></td><td>给输出打分：LLM-as-judge、人工标注、自定义代码评估</td><td class="mono">web/src/features/evals · scores · annotation-queues</td></tr>
  <tr><td><b>📝 Prompt 管理</b></td><td>把 prompt 版本化，线上动态拉取、回滚、对比</td><td class="mono">web/src/features/prompts</td></tr>
  <tr><td><b>🧪 数据集与实验</b></td><td>攒测试集、跑实验、并排对比不同版本</td><td class="mono">web/src/features/datasets · experiments</td></tr>
</table>

<p>要特别说清楚它<strong>不是</strong>什么：它<strong>不是</strong>一个像 LangChain 那样帮你「写」LLM 应用的框架——你用什么框架写应用都行，
Langfuse 只在<strong>运行时</strong>把发生的事记下来；它也<strong>不是</strong>一个模型服务或网关，不替你「调」模型（虽然 Playground 能帮你试）。
它的位置是<strong>旁路观测者</strong>：你的应用照常跑，只是顺手把每一步「报告」给 Langfuse。</p>

<div class="card macro">
  <div class="tag">🗺️ 宏观理解</div>
  Langfuse 既是 <strong>SaaS 云服务</strong>（cloud.langfuse.com），也能<strong>完全自托管</strong>（self-host）——因为它开源、且只依赖
  Postgres、ClickHouse、Redis、S3 这几样常见基础设施。本教程讲的就是<strong>自托管那一套代码</strong>：你在 <code>langfuse/langfuse</code>
  仓库里看到的，正是云上跑的同一套。理解了这套代码，你既能把它<strong>用好</strong>，也能<strong>改它、给它提 PR</strong>。
</div>
""")

_EN.append(r"""
<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="Your LLM app sends data via the SDK into Langfuse's four capabilities, and engineers improve the app from there">
  <text x="360" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Langfuse sits BESIDE your app, not INSIDE it</text>
  <rect x="24" y="104" width="150" height="92" rx="12" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="99" y="140" text-anchor="middle" font-size="13" font-weight="700" fill="var(--ink)">Your LLM app</text>
  <text x="99" y="162" text-anchor="middle" font-size="11" fill="var(--muted)">+ SDK / OpenTelemetry</text>
  <line x1="174" y1="150" x2="244" y2="150" stroke="var(--faint)" stroke-width="2"/>
  <polygon points="244,150 235,145 235,155" fill="var(--faint)"/>
  <text x="209" y="142" text-anchor="middle" font-size="10" fill="var(--faint)">events</text>
  <rect x="250" y="44" width="300" height="216" rx="14" fill="var(--panel-2)" stroke="var(--accent)" stroke-width="2"/>
  <text x="400" y="68" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Langfuse platform</text>
  <rect x="266" y="84" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="330" y="112" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">🔭 Observe</text>
  <text x="330" y="132" text-anchor="middle" font-size="10.5" fill="var(--muted)">trace · observation</text>
  <rect x="406" y="84" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="470" y="112" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">✅ Evaluate</text>
  <text x="470" y="132" text-anchor="middle" font-size="10.5" fill="var(--muted)">score · LLM judge</text>
  <rect x="266" y="164" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="330" y="192" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">📝 Prompts</text>
  <text x="330" y="212" text-anchor="middle" font-size="10.5" fill="var(--muted)">version · fetch live</text>
  <rect x="406" y="164" width="128" height="68" rx="9" fill="var(--panel)" stroke="var(--line)"/>
  <text x="470" y="192" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">🧪 Datasets</text>
  <text x="470" y="212" text-anchor="middle" font-size="10.5" fill="var(--muted)">dataset · compare</text>
  <line x1="550" y1="150" x2="612" y2="150" stroke="var(--faint)" stroke-width="2"/>
  <polygon points="612,150 603,145 603,155" fill="var(--faint)"/>
  <rect x="616" y="104" width="80" height="92" rx="12" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="656" y="140" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">Engineer</text>
  <text x="656" y="160" text-anchor="middle" font-size="10.5" fill="var(--accent-ink)">see·query·fix</text>
  <path d="M656 196 L656 282 L99 282 L99 196" fill="none" stroke="var(--amber)" stroke-width="1.8" stroke-dasharray="5 4"/>
  <polygon points="99,196 94,205 104,205" fill="var(--amber)"/>
  <text x="377" y="276" text-anchor="middle" font-size="10.5" fill="var(--amber)">improve: swap prompt / model / fix the chain</text>
</svg>
<div class="figcap"><b>One loop</b>: your app ships run-time events through the SDK into Langfuse; the platform distills them into four capabilities — <b>observe / evaluate / prompts / datasets</b>; engineers find problems, improve the app, and push improvements back to production. Langfuse always observes from <b>beside</b> the app, never intruding on business logic.</div>
</div>

<h2>What it actually is</h2>
<p>A one-line definition: <strong>a platform that turns an LLM app's run-time behavior into data</strong>.
It does <strong>not</strong> train models for you, and it is <strong>not</strong> yet another framework for
calling an LLM; its work happens <strong>outside</strong> your app — faithfully <strong>recording and
measuring</strong> every run, and supporting you to <strong>evaluate and improve</strong> it. The official
capabilities map to one folder each under <code>web/src/features/</code>:</p>

<table class="t">
  <tr><th>Capability</th><th>Problem it solves</th><th>Where it lives</th></tr>
  <tr><td><b>🔭 Tracing</b></td><td>See every call: the call tree, I/O, tokens, cost, latency</td><td class="mono">web/src/features/traces · tracing-tables</td></tr>
  <tr><td><b>✅ Evaluation</b></td><td>Score outputs: LLM-as-judge, human annotation, custom code</td><td class="mono">web/src/features/evals · scores · annotation-queues</td></tr>
  <tr><td><b>📝 Prompt mgmt</b></td><td>Version prompts; fetch live, roll back, compare</td><td class="mono">web/src/features/prompts</td></tr>
  <tr><td><b>🧪 Datasets & experiments</b></td><td>Build test sets, run experiments, compare versions</td><td class="mono">web/src/features/datasets · experiments</td></tr>
</table>

<p>It helps to say what it is <strong>not</strong>: it is <strong>not</strong> a framework like LangChain that helps you
<strong>write</strong> an LLM app — use whatever framework you like; Langfuse only records what happens at
<strong>run time</strong>. It is also <strong>not</strong> a model server or gateway that <strong>calls</strong> models for
you (though the Playground lets you experiment). Its place is the <strong>side-channel observer</strong>: your app runs
as usual and simply "reports" each step to Langfuse.</p>

<div class="card macro">
  <div class="tag">🗺️ Big picture</div>
  Langfuse is both a <strong>SaaS cloud</strong> (cloud.langfuse.com) and <strong>fully self-hostable</strong> — because it's
  open source and depends only on commodity infra: Postgres, ClickHouse, Redis, S3. This guide explains the
  <strong>self-host codebase</strong>: what you see in <code>langfuse/langfuse</code> is the same stack that runs in the
  cloud. Understand this code and you can both <strong>use it well</strong> and <strong>change it / send a PR</strong>.
</div>
""")

# ── three pillars: trace / observation / score ────────────────────────
_ZH.append(r"""
<h2>三大数据支柱：trace / observation / score</h2>
<p>Langfuse 里所有「可观测」数据，归根结底是三种东西。它们的<strong>领域模型</strong>定义在
<code>packages/shared/src/domain/</code> 下的 <code>traces.ts</code> / <code>observations.ts</code> /
<code>scores.ts</code>，<strong>分析存储</strong>则落在 ClickHouse 同名的三张表里
（<code>packages/shared/clickhouse/migrations/unclustered/0001_traces</code>、<code>0002_observations</code>、
<code>0003_scores</code>）：</p>

<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="一个 trace 包含多个 observation，observation 之间可嵌套，score 挂在 trace 或 observation 上">
  <text x="360" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">trace 是「外壳」，observation 是「主角」，score 是「评判」</text>
  <!-- trace outer -->
  <rect x="20" y="40" width="680" height="206" rx="13" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="36" y="62" font-size="12" font-weight="700" fill="var(--accent-ink)">trace · 一次用户问答 / session</text>
  <!-- root span -->
  <rect x="40" y="74" width="640" height="118" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="56" y="94" font-size="11.5" font-weight="700" fill="var(--blue)">observation · span：handle-request</text>
  <!-- child span retrieve -->
  <rect x="60" y="104" width="270" height="78" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="76" y="124" font-size="11" font-weight="700" fill="var(--purple)">span：retrieve-docs</text>
  <text x="76" y="144" font-size="10" fill="var(--muted)">input: 用户问题</text>
  <text x="76" y="160" font-size="10" fill="var(--muted)">output: 命中的 3 段文档</text>
  <!-- child generation -->
  <rect x="346" y="104" width="318" height="78" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/>
  <text x="362" y="124" font-size="11" font-weight="700" fill="var(--amber)">generation：llm-call · gpt-4o</text>
  <text x="362" y="144" font-size="10" fill="var(--muted)">model · 1,240 tok · $0.012 · 1.8s</text>
  <text x="362" y="160" font-size="10" fill="var(--muted)">input: prompt + 文档　output: 回答</text>
  <!-- score pill -->
  <rect x="470" y="206" width="210" height="30" rx="15" fill="var(--panel)" stroke="var(--accent)"/>
  <text x="575" y="225" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">score：helpfulness 0.9（LLM 评审）</text>
  <text x="36" y="226" font-size="10.5" fill="var(--muted)">↑ score 可挂在 trace 或某个 observation 上</text>
</svg>
<div class="figcap"><b>包含关系</b>：一个 <b>trace</b> 把一次完整交互的所有步骤装在一起；每一步是一个 <b>observation</b>（可嵌套）；<b>score</b> 则是对 trace 或某个 observation 的评分。注意架构取向——<b>observation 才是主分析单元</b>，trace 更像把它们串起来的「关联句柄」。</div>
</div>

<div class="cols">
  <div class="col">
    <h4>🧵 trace · 关联句柄</h4>
    <p>代表<strong>一次完整的请求/会话</strong>。它本身信息不多（名字、用户、会话、标签、时间），主要作用是把同一次交互里的所有
    observation <strong>关联</strong>起来，方便你顺藤摸瓜。定义见 <code>domain/traces.ts</code>。</p>
  </div>
  <div class="col">
    <h4>⭐ observation · 主角</h4>
    <p>一<strong>步</strong>具体操作。最核心是三型：<code>GENERATION</code>（一次 LLM 调用，带 model/token/cost）、
    <code>SPAN</code>（一段有耗时的逻辑，如检索）、<code>EVENT</code>（一个瞬时事件）；新版领域模型在此之上还细分出
    <code>AGENT / TOOL / CHAIN / RETRIEVER</code> 等更具体的类型。它带着 input/output、时间、用量、成本等<strong>丰富属性</strong>，是查询与聚合的主体。</p>
  </div>
</div>

<p><strong>那第三支柱 score 呢？</strong>它是<strong>评分</strong>，可挂在 trace 或某个 observation 上，取值有三类——<strong>数值</strong>（如 0.9）、
<strong>分类</strong>（如「正确 / 错误」）、<strong>布尔</strong>；来源也有三种——<strong>LLM 自动评审</strong>、<strong>人工标注</strong>、<strong>自定义代码</strong>。
正是 score 把「可观测」升级成「可评估」：有了可比较的分数，你才能量化「这次改动到底有没有让应用变好」，而不是凭感觉。score 的配置（数值范围、分类项）
存在 Postgres 的 <code>ScoreConfig</code> 里，分数本身则和 trace/observation 一样进 ClickHouse。</p>

<div class="card detail">
  <div class="tag">🔬 源码细节</div>
  observation 的类型在领域层是一个枚举：最初的 <code>LegacyPrismaObservationType</code> 只有
  <code>SPAN / EVENT / GENERATION</code> 三种（见 <code>packages/shared/prisma/schema.prisma</code>），
  而当前的领域模型 <code>packages/shared/src/domain/observations.ts</code> 的 <code>ObservationType</code> 已扩展到 <strong>10 种</strong>
  （新增 <code>AGENT / TOOL / CHAIN / RETRIEVER / EMBEDDING / EVALUATOR / GUARDRAIL</code>）。ClickHouse 的 <code>observations</code> 表把 model、
  <code>provided_usage_details</code>、<code>cost_details</code>、<code>prompt_id</code> 等都<strong>内联</strong>成一行的列与 Map——
  这正是「宽事件」的样子（下一节展开）。
</div>

<h2>看得见，才改得动：一个排错场景</h2>
<p>抽象的定义不如一个具体场景。假设你做了个<strong>客服问答机器人</strong>，用户反馈「<strong>它偶尔会答非所问</strong>」。
没有 Langfuse 时，你只有应用日志里几行 <code>prompt=... response=...</code>，既不知道是<strong>哪一步</strong>错了，
也复现不出来。接上 Langfuse 后，排查会变成这样：</p>
<p>① 在 <strong>trace 列表</strong>里按「用户点了踩」或「低分」过滤，几秒就翻出那几条出问题的 trace；
② 点开一条，<strong>observation 树</strong>一目了然——原来是 <code>retrieve-docs</code> 这一步<strong>召回了不相关的文档</strong>，
而不是模型本身的问题；③ 看这条 generation 的 <strong>input</strong>，确认被污染的上下文正是那几段错误文档；
④ 你把这条 trace <strong>加进一个数据集</strong>，改完检索逻辑后<strong>跑实验</strong>对比新旧版本，用<strong>评分</strong>确认真的修好了。
整个过程，靠的就是「每一步都被原样记下来」。</p>

<div class="card warn">
  <div class="tag">⚠️ 没有可观测时的常见坑</div>
  只盯着「模型输出不好」很容易<strong>错怪模型</strong>。真实世界里大量「LLM 答得差」其实是<strong>检索召回错了</strong>、
  <strong>prompt 拼错了</strong>、<strong>上游某步超时返回了空</strong>。这些只有把<strong>整条链路</strong>摊开才看得见——
  这就是为什么 Langfuse 把重点放在 <strong>observation 这一「步」</strong>，而不只是最终答案。
</div>
""")

_EN.append(r"""
<h2>The three pillars: trace / observation / score</h2>
<p>Every piece of "observable" data in Langfuse boils down to three things. Their <strong>domain
models</strong> live under <code>packages/shared/src/domain/</code> (<code>traces.ts</code> /
<code>observations.ts</code> / <code>scores.ts</code>); their <strong>analytical storage</strong> is three
same-named ClickHouse tables (<code>packages/shared/clickhouse/migrations/unclustered/0001_traces</code>,
<code>0002_observations</code>, <code>0003_scores</code>):</p>

<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="A trace contains observations that can nest; a score attaches to a trace or an observation">
  <text x="360" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">trace is the shell, observation is the star, score is the verdict</text>
  <rect x="20" y="40" width="680" height="206" rx="13" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="36" y="62" font-size="12" font-weight="700" fill="var(--accent-ink)">trace · one user interaction / session</text>
  <rect x="40" y="74" width="640" height="118" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="56" y="94" font-size="11.5" font-weight="700" fill="var(--blue)">observation · span: handle-request</text>
  <rect x="60" y="104" width="270" height="78" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="76" y="124" font-size="11" font-weight="700" fill="var(--purple)">span: retrieve-docs</text>
  <text x="76" y="144" font-size="10" fill="var(--muted)">input: user question</text>
  <text x="76" y="160" font-size="10" fill="var(--muted)">output: 3 matched chunks</text>
  <rect x="346" y="104" width="318" height="78" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/>
  <text x="362" y="124" font-size="11" font-weight="700" fill="var(--amber)">generation: llm-call · gpt-4o</text>
  <text x="362" y="144" font-size="10" fill="var(--muted)">model · 1,240 tok · $0.012 · 1.8s</text>
  <text x="362" y="160" font-size="10" fill="var(--muted)">input: prompt + docs　output: answer</text>
  <rect x="470" y="206" width="210" height="30" rx="15" fill="var(--panel)" stroke="var(--accent)"/>
  <text x="575" y="225" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">score: helpfulness 0.9 (LLM judge)</text>
  <text x="36" y="226" font-size="10.5" fill="var(--muted)">↑ a score attaches to a trace or an observation</text>
</svg>
<div class="figcap"><b>Containment</b>: a <b>trace</b> wraps all steps of one interaction; each step is an <b>observation</b> (which can nest); a <b>score</b> rates the trace or one observation. Note the architectural stance — <b>the observation is the primary analytical unit</b>; the trace is more of a "correlation handle" stringing them together.</div>
</div>

<div class="cols">
  <div class="col">
    <h4>🧵 trace · correlation handle</h4>
    <p>Represents <strong>one complete request/session</strong>. It carries little itself (name, user,
    session, tags, time); its main job is to <strong>correlate</strong> all the observations of one
    interaction so you can follow the thread. See <code>domain/traces.ts</code>.</p>
  </div>
  <div class="col">
    <h4>⭐ observation · the star</h4>
    <p>One concrete <strong>step</strong>. The three core types are <code>GENERATION</code> (an LLM call, with
    model/token/cost), <code>SPAN</code> (a timed unit of logic, e.g. retrieval) and <code>EVENT</code> (an instantaneous
    event); the current domain model further specializes these into <code>AGENT / TOOL / CHAIN / RETRIEVER</code> and more. It
    carries <strong>rich attributes</strong> — input/output, timing, usage, cost — and is the subject of querying and
    aggregation.</p>
  </div>
</div>

<p><strong>And the third pillar, score?</strong> It is a <strong>rating</strong> attached to a trace or an observation, in three
value types — <strong>numeric</strong> (e.g. 0.9), <strong>categorical</strong> (e.g. "correct / wrong"), <strong>boolean</strong>;
from three sources — <strong>LLM auto-judge</strong>, <strong>human annotation</strong>, <strong>custom code</strong>. Score is what
upgrades "observable" into "evaluable": with comparable numbers you can quantify "did this change actually make the app
better" instead of guessing. A score's config (numeric range, categories) lives in Postgres as <code>ScoreConfig</code>, while
the scores themselves go into ClickHouse like traces/observations.</p>

<div class="card detail">
  <div class="tag">🔬 Source detail</div>
  The observation type is an enum in the domain layer: the original <code>LegacyPrismaObservationType</code> had only
  <code>SPAN / EVENT / GENERATION</code> (see <code>packages/shared/prisma/schema.prisma</code>), while the current domain model
  <code>packages/shared/src/domain/observations.ts</code> defines an <code>ObservationType</code> with <strong>10 values</strong>
  (adding <code>AGENT / TOOL / CHAIN / RETRIEVER / EMBEDDING / EVALUATOR / GUARDRAIL</code>). The ClickHouse
  <code>observations</code> table <strong>inlines</strong> model, <code>provided_usage_details</code>,
  <code>cost_details</code>, <code>prompt_id</code> and more as columns and Maps on a single row — exactly what a
  "wide event" looks like (next section).
</div>

<h2>You can only fix what you can see: a debugging scene</h2>
<p>An abstract definition is weaker than a concrete scene. Say you built a <strong>customer-support bot</strong> and
users report "<strong>it sometimes answers off-topic</strong>". Without Langfuse you only have a few app-log lines like
<code>prompt=... response=...</code> — you can't tell <strong>which step</strong> failed, and you can't reproduce it.
With Langfuse, triage looks like this:</p>
<p>① In the <strong>trace list</strong>, filter by "user thumbs-down" or "low score" and surface the offending traces in
seconds; ② open one, and the <strong>observation tree</strong> makes it obvious — it was the <code>retrieve-docs</code> step
that <strong>fetched irrelevant documents</strong>, not the model itself; ③ inspect that generation's <strong>input</strong>
and confirm the polluted context is exactly those wrong docs; ④ <strong>add this trace to a dataset</strong>, fix the
retrieval logic, <strong>run an experiment</strong> comparing old vs new, and use a <strong>score</strong> to confirm it's
truly fixed. The whole flow rests on "every step was recorded as-is".</p>

<div class="card warn">
  <div class="tag">⚠️ The trap without observability</div>
  Staring only at "the model output is bad" makes it easy to <strong>blame the model wrongly</strong>. In the real world a
  huge share of "the LLM answered poorly" is actually <strong>bad retrieval</strong>, a <strong>mis-assembled prompt</strong>,
  or an <strong>upstream step that timed out and returned empty</strong>. You only see these by laying out the
  <strong>whole chain</strong> — which is why Langfuse centers on the <strong>observation (the "step")</strong>, not just the
  final answer.
</div>
""")

# ── system architecture ───────────────────────────────────────────────
_ZH.append(r"""
<h2>它由什么组成</h2>
<p>把镜头拉到系统层面，Langfuse 是一个 <strong>pnpm + Turbo 的 monorepo</strong>，运行时主要分两个容器，外加四类存储
（见根目录 <code>docker-compose.yml</code> 与 <code>AGENTS.md</code> 的项目结构说明）：</p>

<div class="fig">
<svg viewBox="0 0 720 320" role="img" aria-label="SDK 经 web 入队 Redis，worker 消费后写入 ClickHouse 与 S3，web 读取 Postgres 与 ClickHouse 渲染 UI">
  <text x="360" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">两个容器（web · worker）+ 四类存储</text>
  <!-- top pipeline -->
  <rect x="20" y="44" width="116" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="78" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">SDK / OTel</text>
  <text x="78" y="83" text-anchor="middle" font-size="10" fill="var(--muted)">你的应用</text>
  <rect x="170" y="44" width="150" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="245" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">web · Next.js</text>
  <text x="245" y="83" text-anchor="middle" font-size="10" fill="var(--accent-ink)">UI · tRPC · REST</text>
  <rect x="354" y="44" width="120" height="50" rx="10" fill="var(--red-soft)" stroke="var(--red)"/>
  <text x="414" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">Redis 队列</text>
  <text x="414" y="83" text-anchor="middle" font-size="10" fill="var(--muted)">BullMQ</text>
  <rect x="508" y="44" width="150" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="583" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">worker</text>
  <text x="583" y="83" text-anchor="middle" font-size="10" fill="var(--accent-ink)">队列消费 · 后台处理</text>
  <!-- top arrows -->
  <line x1="136" y1="69" x2="168" y2="69" stroke="var(--faint)" stroke-width="2"/><polygon points="168,69 159,64 159,74" fill="var(--faint)"/>
  <line x1="320" y1="69" x2="352" y2="69" stroke="var(--faint)" stroke-width="2"/><polygon points="352,69 343,64 343,74" fill="var(--faint)"/>
  <line x1="474" y1="69" x2="506" y2="69" stroke="var(--faint)" stroke-width="2"/><polygon points="506,69 497,64 497,74" fill="var(--faint)"/>
  <!-- storage row -->
  <rect x="56" y="214" width="138" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="125" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">Postgres</text>
  <text x="125" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">配置 / 元数据</text>
  <rect x="232" y="214" width="150" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="307" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">ClickHouse</text>
  <text x="307" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">宽事件 · 列存</text>
  <rect x="420" y="214" width="130" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="485" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">S3 / blob</text>
  <text x="485" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">原始事件 · 媒体</text>
  <rect x="588" y="214" width="106" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="641" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">Redis</text>
  <text x="641" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">缓存</text>
  <!-- worker writes -->
  <line x1="560" y1="94" x2="320" y2="212" stroke="var(--accent)" stroke-width="1.8"/><polygon points="320,212 326,202 332,210" fill="var(--accent)"/>
  <line x1="600" y1="94" x2="490" y2="212" stroke="var(--accent)" stroke-width="1.8"/><polygon points="490,212 492,201 500,207" fill="var(--accent)"/>
  <text x="470" y="150" font-size="10" fill="var(--accent-ink)">worker 写入</text>
  <!-- web reads/writes -->
  <line x1="230" y1="94" x2="150" y2="212" stroke="var(--blue)" stroke-width="1.8"/><polygon points="150,212 150,201 159,206" fill="var(--blue)"/>
  <line x1="262" y1="94" x2="300" y2="212" stroke="var(--blue)" stroke-width="1.8" stroke-dasharray="5 3"/><polygon points="300,212 292,205 299,200" fill="var(--blue)"/>
  <text x="150" y="150" font-size="10" fill="var(--blue)">web 读写配置 / 读分析</text>
</svg>
<div class="figcap"><b>数据怎么流</b>：SDK 把事件发给 <b>web</b> 的公共 API，web 快速入队 <b>Redis</b>；<b>worker</b> 消费队列、做合并与成本计算，把结果写进 <b>ClickHouse</b>（宽事件）与 <b>S3</b>（原始事件/媒体）；UI 再由 web 从 <b>Postgres</b>（配置）和 <b>ClickHouse</b>（分析）读出来渲染。摄取走<b>异步</b>，所以 web 端永远轻快。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">packages/shared</span><span class="name">共享内核</span></div>
    <div class="ld">领域模型、Prisma/ClickHouse 访问、队列契约、仓储层。被 web 与 worker 共用；它<strong>不</strong>反向依赖任何一方。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">web</span><span class="name">Next.js 应用</span></div>
    <div class="ld">UI（Pages Router）+ 给 UI 用的 <strong>tRPC</strong> + 给 SDK 用的<strong>公共 REST API</strong>。依赖 <code>@langfuse/shared</code> 与 <code>@langfuse/ee</code>。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">worker</span><span class="name">后台处理</span></div>
    <div class="ld">BullMQ 队列消费者：摄取、评估、实验、导出、删除、集成……几十个队列。只依赖 <code>@langfuse/shared</code>。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">ee</span><span class="name">企业版</span></div>
    <div class="ld">企业功能与 license 校验，被 web 引用；其余皆 MIT。依赖方向严格单向：<code>web/worker/ee → shared</code>。</div></div>
</div>

<p>为什么把核心抽进 <code>packages/shared</code>、让 web 与 worker 都只<strong>单向依赖</strong>它？因为 web 与 worker 是<strong>两种完全不同的负载</strong>：
web 面向用户、追求低延迟、要能随时重启；worker 啃重活、要可重试、按队列伸缩。把<strong>共享的领域模型、存储访问、队列契约</strong>
收进一个「谁都不反向依赖」的<strong>窄腰</strong>，两边就能各自独立演进、独立部署、独立扩容，同时又共用同一套契约、不会各写一套导致漂移。
这条<strong>单向依赖</strong>纪律（<code>web/worker/ee → shared</code>，而 <code>shared</code> 谁都不依赖），是整个 monorepo 能长期维护的关键。</p>
""")

_EN.append(r"""
<h2>What it's made of</h2>
<p>Zoom out to the system level: Langfuse is a <strong>pnpm + Turbo monorepo</strong>, running as two main
containers plus four kinds of storage (see the root <code>docker-compose.yml</code> and the project structure in
<code>AGENTS.md</code>):</p>

<div class="fig">
<svg viewBox="0 0 720 320" role="img" aria-label="SDK enqueues via web into Redis; worker consumes and writes ClickHouse and S3; web reads Postgres and ClickHouse to render the UI">
  <text x="360" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Two containers (web · worker) + four stores</text>
  <rect x="20" y="44" width="116" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="78" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">SDK / OTel</text>
  <text x="78" y="83" text-anchor="middle" font-size="10" fill="var(--muted)">your app</text>
  <rect x="170" y="44" width="150" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="245" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">web · Next.js</text>
  <text x="245" y="83" text-anchor="middle" font-size="10" fill="var(--accent-ink)">UI · tRPC · REST</text>
  <rect x="354" y="44" width="120" height="50" rx="10" fill="var(--red-soft)" stroke="var(--red)"/>
  <text x="414" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">Redis queue</text>
  <text x="414" y="83" text-anchor="middle" font-size="10" fill="var(--muted)">BullMQ</text>
  <rect x="508" y="44" width="150" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="583" y="66" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">worker</text>
  <text x="583" y="83" text-anchor="middle" font-size="10" fill="var(--accent-ink)">queue consumer · jobs</text>
  <line x1="136" y1="69" x2="168" y2="69" stroke="var(--faint)" stroke-width="2"/><polygon points="168,69 159,64 159,74" fill="var(--faint)"/>
  <line x1="320" y1="69" x2="352" y2="69" stroke="var(--faint)" stroke-width="2"/><polygon points="352,69 343,64 343,74" fill="var(--faint)"/>
  <line x1="474" y1="69" x2="506" y2="69" stroke="var(--faint)" stroke-width="2"/><polygon points="506,69 497,64 497,74" fill="var(--faint)"/>
  <rect x="56" y="214" width="138" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="125" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">Postgres</text>
  <text x="125" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">config / metadata</text>
  <rect x="232" y="214" width="150" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="307" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">ClickHouse</text>
  <text x="307" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">wide events · columnar</text>
  <rect x="420" y="214" width="130" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="485" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">S3 / blob</text>
  <text x="485" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">raw events · media</text>
  <rect x="588" y="214" width="106" height="64" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="641" y="240" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">Redis</text>
  <text x="641" y="258" text-anchor="middle" font-size="10" fill="var(--muted)">cache</text>
  <line x1="560" y1="94" x2="320" y2="212" stroke="var(--accent)" stroke-width="1.8"/><polygon points="320,212 326,202 332,210" fill="var(--accent)"/>
  <line x1="600" y1="94" x2="490" y2="212" stroke="var(--accent)" stroke-width="1.8"/><polygon points="490,212 492,201 500,207" fill="var(--accent)"/>
  <text x="470" y="150" font-size="10" fill="var(--accent-ink)">worker writes</text>
  <line x1="230" y1="94" x2="150" y2="212" stroke="var(--blue)" stroke-width="1.8"/><polygon points="150,212 150,201 159,206" fill="var(--blue)"/>
  <line x1="262" y1="94" x2="300" y2="212" stroke="var(--blue)" stroke-width="1.8" stroke-dasharray="5 3"/><polygon points="300,212 292,205 299,200" fill="var(--blue)"/>
  <text x="150" y="150" font-size="10" fill="var(--blue)">web reads/writes config / reads analytics</text>
</svg>
<div class="figcap"><b>How data flows</b>: the SDK posts events to <b>web</b>'s public API, which quickly enqueues into <b>Redis</b>; the <b>worker</b> consumes the queue, merges and computes cost, and writes <b>ClickHouse</b> (wide events) and <b>S3</b> (raw events/media); the UI is then rendered by web reading from <b>Postgres</b> (config) and <b>ClickHouse</b> (analytics). Ingestion is <b>async</b>, so the web tier stays light.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">packages/shared</span><span class="name">shared core</span></div>
    <div class="ld">Domain models, Prisma/ClickHouse access, queue contracts, repositories. Used by both web and worker; it depends on <strong>neither</strong>.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">web</span><span class="name">Next.js app</span></div>
    <div class="ld">UI (Pages Router) + <strong>tRPC</strong> for the UI + a <strong>public REST API</strong> for SDKs. Depends on <code>@langfuse/shared</code> and <code>@langfuse/ee</code>.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">worker</span><span class="name">background jobs</span></div>
    <div class="ld">BullMQ queue consumers: ingestion, evaluation, experiments, exports, deletion, integrations… dozens of queues. Depends only on <code>@langfuse/shared</code>.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">ee</span><span class="name">enterprise</span></div>
    <div class="ld">Enterprise features + license check, used by web; everything else is MIT. Dependency direction is strictly one-way: <code>web/worker/ee → shared</code>.</div></div>
</div>

<p>Why pull the core into <code>packages/shared</code> and have both web and worker depend on it <strong>one-way only</strong>?
Because web and worker are <strong>two very different workloads</strong>: web faces users, wants low latency and must restart
anytime; the worker chews through heavy jobs, must be retryable and scales by queue. Putting the <strong>shared domain models,
storage access and queue contracts</strong> into a <strong>narrow waist</strong> that nothing depends on backwards lets the two
sides evolve, deploy and scale independently while sharing one contract that can't drift. That <strong>one-way dependency</strong>
discipline (<code>web/worker/ee → shared</code>, and <code>shared</code> depends on none) is key to keeping the whole monorepo
maintainable.</p>
""")

# ── why this design + how to read + key points ────────────────────────
_ZH.append(r"""
<h2>为什么这么设计：宽事件 / 可观测性 2.0</h2>
<p>Langfuse 的存储与查询路径，都被一条设计原则贯穿——<strong>把 observation 当作主分析单元，用「宽事件」记录一切</strong>
（明确写在 <code>.agents/ARCHITECTURE_PRINCIPLES.md</code> 里）。所谓宽事件，就是<strong>不</strong>把信息拆成零散的
指标（metrics）、日志（logs）、链路（traces）再事后拼接，而是把一步操作的<strong>所有高基数上下文</strong>
（模型、用量、成本、prompt、用户、标签、环境……）<strong>原样塞进同一行</strong>。</p>

<p>对比一下传统的「可观测性三件套」：<strong>指标（metrics）</strong>是预先聚合好的数字（如 QPS、平均延迟），省空间但<strong>丢了细节</strong>，
事后想按「某个用户 + 某个模型 + 某段时间」下钻就抓瞎；<strong>日志（logs）</strong>是零散的文本行，细节有了却<strong>难以聚合与关联</strong>；
<strong>链路（traces）</strong>能看调用结构，却往往<strong>不带业务属性</strong>。宽事件的思路是把这三者<strong>合一</strong>：每条 observation 既是一条
带结构的「链路节点」，又自带可聚合的数值（token/cost/latency），还携带任意业务字段（user/tag/metadata）。于是「下钻」和「聚合」
不再是两套系统，而是<strong>对同一张宽表的不同查询</strong>。这也是 Langfuse 选择 <strong>ClickHouse</strong> 的根本原因——列存天生擅长
「在一张宽表上做时间窗口扫描 + 任意维度聚合」。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么宁可让每行很「宽」，也不拆成规整的多张表？</strong> 因为可观测的本质是<strong>事后回答你当时没想到的问题</strong>
  （unknown unknowns）。如果上线前就把字段拆进固定指标，那你<strong>只能</strong>查预设好的维度；而把高基数上下文整行留下，
  你就能在事后<strong>任意切片、分组、过滤</strong>。代价是单行更大、存储更多、写入要更聪明——Langfuse 用<strong>列存 +
  ZSTD 压缩 + 仅在详情页才读大字段</strong>来平衡（后续课展开）。<strong>用一点存储，换无限的提问自由。</strong>
</div>

<div class="flow">
  <div class="node hl"><div class="nt">开发 Develop</div><div class="nd">接 SDK·埋点</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">监控 Monitor</div><div class="nd">看 trace·成本·延迟</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">评估 Evaluate</div><div class="nd">打分·标注·实验</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">调试 Debug</div><div class="nd">定位坏 case·改</div></div>
  <div class="arrow">↺</div>
  <div class="node hl"><div class="nt">再开发</div><div class="nd">闭环</div></div>
</div>

<h2>这套教程怎么读</h2>
<p>本指南<strong>沿着数据走</strong>：先打地基，再顺着「写入 → 读取」两条主链路，然后逐个拆功能子系统，最后讲平台与运维。
每一课都配<strong>真实源码对应（文件:行号）</strong>、手绘图与设计取舍框，并以一段自测题收尾。
本指南有一条<strong>硬承诺</strong>：每一处技术论断都对应 <code>langfuse/langfuse</code> 仓库里<strong>真实存在</strong>的源码，<strong>绝不臆造</strong>；
引用以「文件:行号」标注，方便你打开仓库逐一核对。看不懂的地方，顺着引用去读源码，往往比读十段解释都管用。</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>宏观与基础（第 1–11 课）</h4><p>数据模型、双存储、ClickHouse 宽事件表、多租户、部署拓扑。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>摄取链路 · 写（第 12–19 课）</h4><p>从 SDK 到 ClickHouse：API、队列、合并、token/成本、OTel、媒体。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>查询链路 · 读（第 20–27 课）</h4><p>tRPC、仓储层、过滤/搜索、列表、trace 详情、公共 API。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>功能子系统（第 28–47 课）</h4><p>评估/评分、数据集/实验、Prompt/Playground、仪表盘/成本、自动化/集成。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>平台·运维·设计专题（第 48–55 课）</h4><p>鉴权/RBAC、EE、运维、删除、构建测试，最后是设计专题与终章。</p></div></div>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>Langfuse 是开源 LLM 工程平台</strong>（MIT）：围绕<strong>开发→监控→评估→调试</strong>闭环，把 LLM 应用的每一步变成数据。</li>
    <li><strong>三大支柱</strong>：<strong>trace</strong>（关联句柄）⊃ <strong>observation</strong>（主分析单元，分 GENERATION/SPAN/EVENT）+ <strong>score</strong>（评分）。</li>
    <li><strong>两容器四存储</strong>：<strong>web</strong> + <strong>worker</strong>；<strong>Postgres</strong>(配置) + <strong>ClickHouse</strong>(宽事件) + <strong>Redis</strong>(队列/缓存) + <strong>S3</strong>(原始/媒体)。</li>
    <li><strong>摄取是异步的</strong>：SDK→web 入队→worker 处理→写存储，所以 web 端轻快、能抗尖峰。</li>
    <li><strong>设计灵魂是「宽事件 / 可观测性 2.0」</strong>：用高基数整行换取事后任意提问的自由。</li>
  </ul>
</div>
""")

_EN.append(r"""
<h2>Why this design: wide events / Observability 2.0</h2>
<p>Langfuse's storage and query paths are all threaded by one design principle — <strong>treat the observation
as the primary analytical unit and record everything as "wide events"</strong> (stated explicitly in
<code>.agents/ARCHITECTURE_PRINCIPLES.md</code>). A wide event means you do <strong>not</strong> shatter
information into separate metrics, logs and traces to be reassembled later; instead you cram <strong>all the
high-cardinality context</strong> of one step (model, usage, cost, prompt, user, tags, environment…)
<strong>onto a single row</strong>.</p>

<p>Contrast the classic "three pillars of observability": <strong>metrics</strong> are pre-aggregated numbers (QPS, average
latency) — cheap but they <strong>lose detail</strong>, so drilling into "this user + this model + this time window" later is
hopeless; <strong>logs</strong> are scattered text lines — detail is there but they're <strong>hard to aggregate and
correlate</strong>; <strong>traces</strong> show call structure but usually <strong>carry no business attributes</strong>. The
wide-event idea <strong>fuses</strong> all three: each observation is at once a structured "trace node", a bag of aggregatable
numbers (token/cost/latency), and a carrier of arbitrary business fields (user/tag/metadata). So "drill down" and "aggregate"
stop being two systems and become <strong>different queries over one wide table</strong>. That's also the root reason Langfuse
picked <strong>ClickHouse</strong> — columnar storage is built for "time-bounded scans + arbitrary-dimension aggregation over a
wide table".</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why keep each row "wide" instead of splitting it into tidy normalized tables?</strong> Because the
  essence of observability is <strong>answering questions you didn't think of at the time</strong> (unknown
  unknowns). If you split fields into fixed metrics before shipping, you can <strong>only</strong> query the
  dimensions you predefined; keep the high-cardinality context on the row and you can <strong>slice, group and
  filter arbitrarily after the fact</strong>. The cost is bigger rows, more storage and smarter writes — Langfuse
  balances it with <strong>columnar storage + ZSTD compression + reading big fields only on the detail
  page</strong> (later lessons). <strong>Trade a little storage for unlimited freedom to ask questions.</strong>
</div>

<div class="flow">
  <div class="node hl"><div class="nt">Develop</div><div class="nd">wire SDK · instrument</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">Monitor</div><div class="nd">traces · cost · latency</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">Evaluate</div><div class="nd">score · annotate · experiment</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">Debug</div><div class="nd">find bad cases · fix</div></div>
  <div class="arrow">↺</div>
  <div class="node hl"><div class="nt">Develop again</div><div class="nd">loop</div></div>
</div>

<h2>How to read this guide</h2>
<p>This guide <strong>follows the data</strong>: lay the foundations first, then walk the two main paths
"write → read", then take apart the feature subsystems one by one, and finally cover platform & operations.
Every lesson ships <strong>real source citations (file:line)</strong>, hand-drawn diagrams and a design-tradeoff
box, and closes with a short self-test. This guide makes one <strong>hard promise</strong>: every technical claim corresponds to
source that <strong>really exists</strong> in <code>langfuse/langfuse</code>, <strong>never invented</strong>; citations carry
"file:line" so you can open the repo and check. Where something is unclear, following the citation into the source often beats
ten paragraphs of explanation.</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>Big picture & foundations (L01–11)</h4><p>Data model, dual store, ClickHouse wide-event tables, multi-tenancy, deployment topology.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>Ingestion · write (L12–19)</h4><p>SDK to ClickHouse: API, queue, merge, token/cost, OTel, media.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Query · read (L20–27)</h4><p>tRPC, repositories, filtering/search, lists, trace detail, public API.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>Feature subsystems (L28–47)</h4><p>Eval/scoring, datasets/experiments, prompts/playground, dashboards/cost, automation/integrations.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>Platform · ops · design themes (L48–55)</h4><p>Auth/RBAC, EE, operations, deletion, build & test, then design themes and the capstone.</p></div></div>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Langfuse is an open-source LLM engineering platform</strong> (MIT): a <strong>develop → monitor → evaluate → debug</strong> loop that turns every step of an LLM app into data.</li>
    <li><strong>Three pillars</strong>: <strong>trace</strong> (correlation handle) ⊃ <strong>observation</strong> (primary unit; GENERATION/SPAN/EVENT) + <strong>score</strong> (rating).</li>
    <li><strong>Two containers, four stores</strong>: <strong>web</strong> + <strong>worker</strong>; <strong>Postgres</strong> (config) + <strong>ClickHouse</strong> (wide events) + <strong>Redis</strong> (queue/cache) + <strong>S3</strong> (raw/media).</li>
    <li><strong>Ingestion is async</strong>: SDK → web enqueues → worker processes → writes storage, so web stays light and absorbs spikes.</li>
    <li><strong>The soul of the design is "wide events / Observability 2.0"</strong>: trade high-cardinality rows for the freedom to ask any question later.</li>
  </ul>
</div>
""")

# (more sections appended below, before the LESSON_01 assembly)

LESSON_01 = {"zh": "\n".join(_ZH), "en": "\n".join(_EN)}
