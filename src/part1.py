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

<p><strong>那第三支柱 score 呢？</strong>它是<strong>评分</strong>，可挂在 trace 或某个 observation 上。取值<strong>主要</strong>有三类——
<code>NUMERIC</code> 数值（如 0.9）、<code>CATEGORICAL</code> 分类（如「正确 / 错误」）、<code>BOOLEAN</code> 布尔（领域模型里还有 <code>CORRECTION</code>、<code>TEXT</code>）；
来源有三种——<code>EVAL</code>（自动评审）、<code>ANNOTATION</code>（人工标注）、<code>API</code>（SDK 直接提交），见 <code>packages/shared/src/domain/scores.ts</code>。
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
<p>把三大支柱落到真实类型上——它们都是 Zod schema，定义在 <code>packages/shared/src/domain/</code>：</p>
<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/{traces,observations,scores}.ts</span><span class="ln">三大支柱</span></div>
  <pre class="code"><span class="cm">// ① trace = 一次完整调用的「根」（traces.ts）</span>
<span class="kw">export const</span> <span class="fn">TraceDomain</span> = z.object({
  id: z.string(),  name: z.string().nullable(),  timestamp: z.date(),
  input: jsonSchema.nullable(),   output: jsonSchema.nullable(),
  sessionId: z.string().nullable(),  userId: z.string().nullable(),
  projectId: z.string(),                 <span class="cm">// 每条都带 projectId：硬隔离键</span>
});

<span class="cm">// ② observation = trace 里的每一步，10 种类型（observations.ts）</span>
<span class="kw">export const</span> <span class="fn">ObservationType</span> = {
  SPAN, EVENT, GENERATION, AGENT, TOOL,
  CHAIN, RETRIEVER, EVALUATOR, EMBEDDING, GUARDRAIL,
} <span class="kw">as const</span>;

<span class="cm">// ③ score = 挂在 trace/observation 上的评分（scores.ts）</span>
<span class="cm">//   NUMERIC(value) · CATEGORICAL/BOOLEAN(stringValue) · CORRECTION</span></pre>
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

<p><strong>And the third pillar, score?</strong> It is a <strong>rating</strong> attached to a trace or an observation. Its value
is <strong>mainly</strong> one of three types — <code>NUMERIC</code> (e.g. 0.9), <code>CATEGORICAL</code> (e.g. "correct / wrong"),
<code>BOOLEAN</code> (the domain model also has <code>CORRECTION</code> and <code>TEXT</code>); from three sources —
<code>EVAL</code> (auto-judge), <code>ANNOTATION</code> (human), <code>API</code> (submitted via SDK), see
<code>packages/shared/src/domain/scores.ts</code>. Score is what upgrades "observable" into "evaluable": with comparable numbers
you can quantify "did this change actually make the app better" instead of guessing. A score's config (numeric range,
categories) lives in Postgres as <code>ScoreConfig</code>, while the scores themselves go into ClickHouse like
traces/observations.</p>

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
<p>Grounding the three pillars in real types — all are Zod schemas in <code>packages/shared/src/domain/</code>:</p>
<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/{traces,observations,scores}.ts</span><span class="ln">three pillars</span></div>
  <pre class="code"><span class="cm">// (1) trace = the "root" of one full call (traces.ts)</span>
<span class="kw">export const</span> <span class="fn">TraceDomain</span> = z.object({
  id: z.string(),  name: z.string().nullable(),  timestamp: z.date(),
  input: jsonSchema.nullable(),   output: jsonSchema.nullable(),
  sessionId: z.string().nullable(),  userId: z.string().nullable(),
  projectId: z.string(),                 <span class="cm">// every row carries projectId: the isolation key</span>
});

<span class="cm">// (2) observation = each step inside a trace, 10 types (observations.ts)</span>
<span class="kw">export const</span> <span class="fn">ObservationType</span> = {
  SPAN, EVENT, GENERATION, AGENT, TOOL,
  CHAIN, RETRIEVER, EVALUATOR, EMBEDDING, GUARDRAIL,
} <span class="kw">as const</span>;

<span class="cm">// (3) score = a grade attached to a trace/observation (scores.ts)</span>
<span class="cm">//   NUMERIC(value) · CATEGORICAL/BOOLEAN(stringValue) · CORRECTION</span></pre>
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


# ══════════════════════════════════════════════════════════════════════
# L02 · 可观测性 2.0 与宽事件 / Observability 2.0 & wide events
# ══════════════════════════════════════════════════════════════════════
_ZH2 = []
_EN2 = []

_ZH2.append(r"""
<p class="lead">
上一课说 Langfuse 的「设计灵魂」是<strong>宽事件 / 可观测性 2.0</strong>。这一课把这句口号讲透——它<strong>不是</strong>营销词，
而是写在 <code>.agents/ARCHITECTURE_PRINCIPLES.md</code> 里、约束着 Langfuse 每一处存储与查询设计的<strong>第一性原则</strong>。
理解了它，后面「为什么用 ClickHouse」「为什么事件不可变」「为什么列表只读窄字段」这些问题，答案都会自己浮现。
可以说，这一课是整份指南的<strong>地基课</strong>：它不讲某个具体模块，而讲一种<strong>看问题的方式</strong>，后面五十多课都建在它之上。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  传统「可观测性 1.0」像医院把你的体检拆成<strong>三个互不相通的科室</strong>：一个只记<strong>数字</strong>（血压、心率——指标 metrics），
  一个只写<strong>文字</strong>（医生手记——日志 logs），一个只画<strong>就诊路线</strong>（你今天先挂号再抽血——链路 traces）。
  想搞清「为什么这次不舒服」，你得自己<strong>跨三个科室对账</strong>。「可观测性 2.0」反过来：每看一次病，就写一份
  <strong>完整病历</strong>——数字、描述、过程<strong>全在一张纸上</strong>。这张「完整病历」，就是<strong>宽事件（wide event）</strong>。
  好处显而易见：换个医生、换个时间回看，都能从这<strong>一张纸</strong>上还原全部情况，而不必再去三个科室翻档案对时间线。
</div>
""")

_EN2.append(r"""
<p class="lead">
Last lesson called Langfuse's "design soul" <strong>wide events / Observability 2.0</strong>. This lesson makes the slogan
concrete — it is <strong>not</strong> marketing; it's a <strong>first principle</strong> written into
<code>.agents/ARCHITECTURE_PRINCIPLES.md</code> that constrains every storage and query decision in Langfuse. Grasp it and
the later questions — "why ClickHouse", "why immutable events", "why lists read only narrow fields" — answer themselves. This
lesson is the guide's <strong>foundation lesson</strong>: not about one module but about a <strong>way of seeing</strong> that the
fifty-odd later lessons build on.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Classic "Observability 1.0" is like a hospital splitting your check-up across <strong>three disconnected departments</strong>:
  one records only <strong>numbers</strong> (blood pressure, heart rate — metrics), one writes only <strong>text</strong> (the
  doctor's notes — logs), one draws only the <strong>route</strong> (register, then blood draw — traces). To understand "why I
  feel unwell" you must <strong>reconcile across all three yourself</strong>. "Observability 2.0" flips it: each visit writes one
  <strong>complete medical record</strong> — numbers, description and process <strong>on a single sheet</strong>. That single
  sheet is the <strong>wide event</strong>. The benefit is obvious: a different doctor, or you revisiting later, can reconstruct the
  whole picture from that <strong>one sheet</strong> — no re-digging three departments to line up the timeline.
</div>
""")

_ZH2.append(r"""
<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="左侧可观测性 1.0 把指标日志链路三件套分开存需要事后拼接，右侧 2.0 用一条宽事件可任意切片">
  <text x="170" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--red)">可观测性 1.0 · 三件套分离</text>
  <rect x="40" y="40" width="160" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="120" y="60" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">指标 metrics</text>
  <text x="120" y="76" text-anchor="middle" font-size="9.5" fill="var(--muted)">预聚合数字 · 丢细节</text>
  <rect x="40" y="92" width="160" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="120" y="112" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">日志 logs</text>
  <text x="120" y="128" text-anchor="middle" font-size="9.5" fill="var(--muted)">零散文本 · 难聚合</text>
  <rect x="40" y="144" width="160" height="44" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/>
  <text x="120" y="164" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">链路 traces</text>
  <text x="120" y="180" text-anchor="middle" font-size="9.5" fill="var(--muted)">有结构 · 缺业务属性</text>
  <text x="120" y="214" text-anchor="middle" font-size="11" fill="var(--red)">🧩 事后还要人肉拼接</text>
  <text x="120" y="232" text-anchor="middle" font-size="9.5" fill="var(--faint)">（reassemble later）</text>
  <text x="350" y="120" text-anchor="middle" font-size="18" font-weight="800" fill="var(--faint)">vs</text>
  <text x="545" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">可观测性 2.0 · 一条宽事件</text>
  <rect x="404" y="50" width="282" height="38" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="545" y="74" text-anchor="middle" font-size="10" fill="var(--accent-ink)">model · tokens · cost · latency · user · tag · env …</text>
  <text x="545" y="104" text-anchor="middle" font-size="9.5" fill="var(--muted)">一行里同时有「数字 + 结构 + 业务字段」</text>
  <line x1="460" y1="120" x2="430" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="430,158 432,147 439,153" fill="var(--accent)"/>
  <line x1="545" y1="120" x2="545" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="545,158 540,148 550,148" fill="var(--accent)"/>
  <line x1="630" y1="120" x2="660" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="660,158 651,153 658,147" fill="var(--accent)"/>
  <rect x="404" y="160" width="92" height="34" rx="8" fill="var(--panel)" stroke="var(--line)"/><text x="450" y="181" text-anchor="middle" font-size="9.5" fill="var(--ink)">按用户切片</text>
  <rect x="500" y="160" width="92" height="34" rx="8" fill="var(--panel)" stroke="var(--line)"/><text x="546" y="181" text-anchor="middle" font-size="9.5" fill="var(--ink)">按模型聚合</text>
  <rect x="596" y="160" width="92" height="34" rx="8" fill="var(--panel)" stroke="var(--line)"/><text x="642" y="181" text-anchor="middle" font-size="9.5" fill="var(--ink)">按时间下钻</text>
  <text x="545" y="226" text-anchor="middle" font-size="11" fill="var(--accent-ink)">✅ 同一张宽表，换个查询就是新视角</text>
</svg>
<div class="figcap"><b>1.0 vs 2.0</b>：传统三件套把信息<b>拆散</b>，回答跨维度问题前先得人肉拼接；宽事件把一步操作的数字、结构、业务字段<b>放进同一行</b>，「下钻」和「聚合」只是对同一张宽表的不同查询。这正是 <code>ARCHITECTURE_PRINCIPLES.md</code> 说的「<b>偏好宽而属性丰富的事件，而非需要事后重建的零散指标/日志/链路</b>」。</div>
</div>

<h2>可观测性 1.0 的困境</h2>
<p>「指标 + 日志 + 链路」这套经典组合（业内常称<strong>可观测性 1.0</strong>）每一件单看都没错，问题出在<strong>三者分离</strong>：</p>
<ul>
  <li><strong>指标（metrics）</strong>是<strong>预先聚合</strong>的数字，比如「平均延迟」「每分钟请求数」。省空间，但你<strong>上线前</strong>就得决定聚合哪些维度——
  事后想问「<strong>某个用户</strong>用<strong>某个模型</strong>在<strong>某段时间</strong>的延迟」，没预聚合就抓瞎。</li>
  <li><strong>日志（logs）</strong>是一行行文本，细节都在，但<strong>难以聚合与关联</strong>：你很难对一堆自由文本做「按模型分组求 token 中位数」。</li>
  <li><strong>链路（traces）</strong>能看清调用结构（谁调了谁、各花多久），却<strong>往往不带业务属性</strong>——它知道「调了 LLM」，但不知道「这次的 user 是谁、prompt 是哪版」。</li>
</ul>
<p>于是真要排查一个跨维度的问题，你得在三套系统之间<strong>来回对账</strong>。Langfuse 的架构原则第一条就是冲着这个来的——
<strong>把 observation 当作主分析单元</strong>，trace 只是<strong>关联句柄</strong>（原文：<em>"Model observations as the primary
analytical unit. A trace is a correlation handle that links related observations, not the only useful entry point."</em>）。</p>

<p>举个具体的对比。线上有人投诉「<strong>晚高峰回答变慢</strong>」，你想知道「<strong>是不是某个模型在某些用户上特别慢</strong>」。
在 1.0 里：指标只有「全局平均延迟」这一条曲线，看不出是哪个模型、哪批用户；日志里能翻到单条记录，但几万行文本没法快速按模型分组算分位数；
链路能看单次调用的耗时，却没记 user 和 model 这些业务字段。三套都「沾边」，但<strong>没有一套能直接回答</strong>，你只能导出数据自己写脚本拼。
在 2.0 里：每条 observation 都同时带着 <code>model</code>、<code>userId</code>、<code>latency</code>，于是这个问题退化成一句普通查询——
「按 model + userId 分组、看 latency 的 p95」。<strong>同一个问题，1.0 要跨三系统拼半天，2.0 改个查询就答了。</strong></p>
""")

_EN2.append(r"""
<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="Left: Observability 1.0 stores metrics, logs, traces separately needing later reassembly; right: 2.0 one wide event sliced any way">
  <text x="170" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--red)">Observability 1.0 · three split pillars</text>
  <rect x="40" y="40" width="160" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="120" y="60" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">metrics</text>
  <text x="120" y="76" text-anchor="middle" font-size="9.5" fill="var(--muted)">pre-aggregated · lose detail</text>
  <rect x="40" y="92" width="160" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="120" y="112" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">logs</text>
  <text x="120" y="128" text-anchor="middle" font-size="8.5" fill="var(--muted)">scattered text · hard to aggregate</text>
  <rect x="40" y="144" width="160" height="44" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/>
  <text x="120" y="164" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--ink)">traces</text>
  <text x="120" y="180" text-anchor="middle" font-size="9.5" fill="var(--muted)">structured · no business attrs</text>
  <text x="120" y="214" text-anchor="middle" font-size="11" fill="var(--red)">🧩 reassemble by hand later</text>
  <text x="350" y="120" text-anchor="middle" font-size="18" font-weight="800" fill="var(--faint)">vs</text>
  <text x="545" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Observability 2.0 · one wide event</text>
  <rect x="404" y="50" width="282" height="38" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="545" y="74" text-anchor="middle" font-size="10" fill="var(--accent-ink)">model · tokens · cost · latency · user · tag · env …</text>
  <text x="545" y="104" text-anchor="middle" font-size="9.5" fill="var(--muted)">numbers + structure + business fields, one row</text>
  <line x1="460" y1="120" x2="430" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="430,158 432,147 439,153" fill="var(--accent)"/>
  <line x1="545" y1="120" x2="545" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="545,158 540,148 550,148" fill="var(--accent)"/>
  <line x1="630" y1="120" x2="660" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="660,158 651,153 658,147" fill="var(--accent)"/>
  <rect x="404" y="160" width="92" height="34" rx="8" fill="var(--panel)" stroke="var(--line)"/><text x="450" y="181" text-anchor="middle" font-size="9" fill="var(--ink)">by user</text>
  <rect x="500" y="160" width="92" height="34" rx="8" fill="var(--panel)" stroke="var(--line)"/><text x="546" y="181" text-anchor="middle" font-size="9" fill="var(--ink)">by model</text>
  <rect x="596" y="160" width="92" height="34" rx="8" fill="var(--panel)" stroke="var(--line)"/><text x="642" y="181" text-anchor="middle" font-size="9" fill="var(--ink)">by time</text>
  <text x="545" y="226" text-anchor="middle" font-size="11" fill="var(--accent-ink)">✅ same wide table, new query = new view</text>
</svg>
<div class="figcap"><b>1.0 vs 2.0</b>: the classic three pillars <b>fragment</b> information, forcing manual reassembly before any cross-dimension question; a wide event puts the numbers, structure and business fields of one step <b>on a single row</b>, so "drill down" and "aggregate" are just different queries over one wide table. This is exactly what <code>ARCHITECTURE_PRINCIPLES.md</code> means by "<b>prefer wide, richly attributed events over fragmented metrics, logs, and trace records that require later reconstruction</b>".</div>
</div>

<h2>The trouble with Observability 1.0</h2>
<p>The classic "metrics + logs + traces" combo (often called <strong>Observability 1.0</strong>) is fine piece by piece; the
problem is that the <strong>three are separate</strong>:</p>
<ul>
  <li><strong>Metrics</strong> are <strong>pre-aggregated</strong> numbers — "average latency", "requests per minute". Cheap, but
  you must decide <strong>before shipping</strong> which dimensions to aggregate; ask later for "the latency of <strong>this
  user</strong> on <strong>this model</strong> in <strong>this window</strong>" and without that pre-aggregation you're stuck.</li>
  <li><strong>Logs</strong> are text lines — all the detail is there but they're <strong>hard to aggregate and correlate</strong>:
  computing "median tokens grouped by model" over free text is painful.</li>
  <li><strong>Traces</strong> show call structure (who called whom, how long) but <strong>usually carry no business
  attributes</strong> — they know "an LLM was called" but not "who the user was or which prompt version".</li>
</ul>
<p>So to triage a cross-dimension problem you end up <strong>reconciling across three systems</strong>. Langfuse's very first
architecture principle targets exactly this — <strong>treat the observation as the primary analytical unit</strong>, with the
trace as a <strong>correlation handle</strong> (verbatim: <em>"Model observations as the primary analytical unit. A trace is a
correlation handle that links related observations, not the only useful entry point."</em>).</p>

<p>A concrete contrast. Someone complains that "<strong>answers get slow at peak hours</strong>" and you want to know "<strong>is a
particular model slow for particular users</strong>". In 1.0: metrics give you one "global average latency" curve that can't tell
which model or which users; logs have the individual records but tens of thousands of text lines won't quickly group-by-model and
compute percentiles; traces show per-call duration but never recorded the <code>user</code> and <code>model</code> business fields.
All three are "related", yet <strong>none can answer directly</strong> — you end up exporting data and scripting the join yourself.
In 2.0: every observation already carries <code>model</code>, <code>userId</code> and <code>latency</code>, so the question
collapses to one ordinary query — "group by model + userId, look at p95 of latency". <strong>Same question: 1.0 stitches across
three systems for ages; 2.0 just changes the query.</strong></p>
""")

_ZH2.append(r"""
<h2>宽事件：把一切放进一行</h2>
<p>「可观测性 2.0」的解法很直接：<strong>不要事后拼接，写的时候就别拆开</strong>。把一步操作的<strong>所有高基数上下文</strong>
（哪个模型、多少 token、多少钱、多久、哪个用户、哪些标签、什么环境……）<strong>原样塞进同一条记录</strong>——这条记录就是
Langfuse 里的 <strong>observation</strong>。它既是「链路节点」（有 <code>parentObservationId</code> 能拼出调用树），
又自带可聚合的数字（<code>usageDetails</code> / <code>costDetails</code> / <code>latency</code>），还携带任意业务字段
（<code>metadata</code> / <code>tags</code> / <code>userId</code>）。三件套想分开做的事，一条宽事件全包了。</p>

<p>你可能会问：那为什么不把这些字段<strong>拆成多张规整的表</strong>、用外键关联，岂不是更「干净」？答案是——<strong>查询时的 JOIN 是热路径上的隐藏成本</strong>。
可观测数据量极大（一个活跃项目一天可能上亿条 observation），如果每次「按模型看成本」都要把 observation 表和一张「模型表」「用量表」JOIN 起来，
扫描与连接的代价会随数据量爆炸。Langfuse 的原则是<strong>谨慎反范式化</strong>（denormalize carefully）：把常用来过滤、聚合的字段<strong>直接内联</strong>到
observation 行上，让「按模型 / 按用户 / 按时间」这些高频查询变成<strong>直接的列谓词</strong>，而不是 JOIN。这就是「宽」的另一层含义——
不只是字段多，更是<strong>有意把该放在一起的放在一起</strong>，用一点存储冗余换查询时不必连表。</p>

<div class="cols">
  <div class="col">
    <h4>😕 1.0：先拆再拼</h4>
    <p>指标、日志、链路各存一处；问一个跨维度问题，要在三套系统里查三次再人肉对账。<strong>能问什么，上线前就被字段设计锁死了。</strong></p>
  </div>
  <div class="col">
    <h4>😀 2.0：一行装下</h4>
    <p>一条 observation 同时有数字、结构、业务字段。<strong>切片、分组、过滤都是对同一张宽表的查询</strong>，事后想问什么都行。代价：行更宽、存得更多。</p>
  </div>
</div>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="一条宽 observation 行的解剖：同一行里塞进三类字段——关联字段(id/traceId/parentObservationId 拼调用树)、数字字段(latency/usageDetails/costDetails 可聚合)、业务字段(model/userId/metadata/tags 可过滤分组)，于是按模型/用户/时间提问都是同一张宽表的列查询，无需JOIN">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一条 observation = 三类字段塞进同一行</text>
  <rect x="24" y="38" width="672" height="30" rx="6" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="57" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">observations 宽表的一行（ObservationSchema）</text>
  <rect x="24" y="80" width="216" height="118" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="132" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① 关联字段（拼调用树）</text><text x="132" y="120" text-anchor="middle" font-size="7" fill="var(--muted)">id · traceId · projectId</text><text x="132" y="135" text-anchor="middle" font-size="7" fill="var(--muted)">parentObservationId</text><text x="132" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">type · startTime/endTime</text><text x="132" y="172" text-anchor="middle" font-size="6.5" fill="var(--faint)">让它既是「链路节点」</text><text x="132" y="185" text-anchor="middle" font-size="6.5" fill="var(--faint)">又能独立查询</text>
  <rect x="252" y="80" width="216" height="118" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="360" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">② 数字字段（可聚合）</text><text x="360" y="120" text-anchor="middle" font-size="7" fill="var(--muted)">latency · timeToFirstToken</text><text x="360" y="135" text-anchor="middle" font-size="7" fill="var(--muted)">usageDetails（token 用量）</text><text x="360" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">costDetails · totalCost</text><text x="360" y="172" text-anchor="middle" font-size="6.5" fill="var(--faint)">直接 sum/avg/p95，</text><text x="360" y="185" text-anchor="middle" font-size="6.5" fill="var(--faint)">不必从日志里 parse</text>
  <rect x="480" y="80" width="216" height="118" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="588" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">③ 业务字段（可过滤分组）</text><text x="588" y="120" text-anchor="middle" font-size="7" fill="var(--muted)">model · internalModelId</text><text x="588" y="135" text-anchor="middle" font-size="7" fill="var(--muted)">metadata · environment</text><text x="588" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">promptName/Version</text><text x="588" y="172" text-anchor="middle" font-size="6.5" fill="var(--faint)">「按模型 / 按环境」</text><text x="588" y="185" text-anchor="middle" font-size="6.5" fill="var(--faint)">退化成列谓词</text>
  <text x="360" y="214" text-anchor="middle" font-size="8" fill="var(--faint)">三类字段同处一行 → 「按模型看 p95 延迟」「按用户看花费」都是对这张宽表的普通列查询，无需 JOIN</text>
</svg>
<div class="figcap"><b>宽 observation 的解剖</b>：<code>packages/shared/src/domain/observations.ts:55 ObservationSchema</code> 把<b>关联</b>（id/traceId/parentObservationId）、<b>数字</b>（latency/usageDetails/costDetails）、<b>业务</b>（model/metadata/environment/promptName）三类字段塞进同一行。这就是「宽」的字面含义——也是「下钻=查这张表、聚合=也查这张表」的根。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/observations.ts:55</span><span class="ln">一条 observation 的真实结构</span></div>
  <pre class="code"><span class="kw">export const</span> ObservationSchema = z.<span class="fn">object</span>({
  <span class="cm">// ① 关联字段：拼出调用树，也让本行能独立查询</span>
  id: z.<span class="fn">string</span>(),  traceId: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  projectId: z.<span class="fn">string</span>(),
  parentObservationId: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  type: ObservationTypeDomain,
  <span class="cm">// ② 数字字段：可直接 sum/avg/p95，无需从日志 parse</span>
  latency: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),  timeToFirstToken: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),
  usageDetails: z.<span class="fn">record</span>(z.<span class="fn">string</span>(), z.<span class="fn">number</span>()),  costDetails: z.<span class="fn">record</span>(z.<span class="fn">string</span>(), z.<span class="fn">number</span>()),
  totalCost: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),  totalUsage: z.<span class="fn">number</span>(),
  <span class="cm">// ③ 业务字段：让「按模型 / 按环境 / 按 prompt」变成列谓词</span>
  model: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  environment: z.<span class="fn">string</span>(),  metadata: MetadataDomain,
  promptName: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  promptVersion: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),
  input: jsonSchema.<span class="fn">nullable</span>(),  output: jsonSchema.<span class="fn">nullable</span>(),  <span class="cm">// 大字段，详情页才读（第24课）</span>
});</pre>
</div>

<h2>这套原则如何贯穿 Langfuse</h2>
<p><code>ARCHITECTURE_PRINCIPLES.md</code> 里的每一条，都能在后面的课里找到对应的工程落点。下表是「原则 → 它换来什么 → 哪一课展开」：</p>

<table class="t">
  <tr><th>架构原则（原文要义）</th><th>它换来什么</th><th>对应</th></tr>
  <tr><td>observation 为主分析单元，trace 是关联句柄</td><td>任何一步都能独立查询，不必从 trace 进入</td><td>第 3 课</td></tr>
  <tr><td>偏好宽而属性丰富的事件，而非零散三件套</td><td>下钻与聚合统一成「查同一张宽表」</td><td>第 8 课</td></tr>
  <tr><td>保留高基数上下文，应对 unknown unknowns</td><td>事后能问上线时没想到的问题</td><td>本课</td></tr>
  <tr><td>偏好不可变 / 追加式事件记录</td><td>避免读时去重的隐藏开销；用 ReplacingMergeTree</td><td>第 8 课</td></tr>
  <tr><td>谨慎反范式化，消除热路径 JOIN</td><td>常用过滤变成直接的列谓词</td><td>第 8 · 22 课</td></tr>
  <tr><td>围绕列式访问设计（窄字段、时间窗口、排序键、剪枝）</td><td>大表上也能毫秒级扫描聚合</td><td>第 8 · 23 课</td></tr>
  <tr><td>列表/仪表盘用紧凑表示，详情页才读大字段</td><td>列表快、详情全，互不拖累</td><td>第 24 课</td></tr>
  <tr><td>API 契约要「规模感知」：强制时间窗口、token 分页</td><td>防止一不小心扫全表历史</td><td>第 27 课</td></tr>
  <tr><td>把成本与运维简单性当作架构约束</td><td>不轻易加库/队列/物化视图</td><td>第 53 课</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  宽事件不是免费的：行更宽、写入数据更多、还得有聪明的写入与压缩。Langfuse 的取舍是——<strong>用一点存储与写入复杂度，换「事后任意提问」的自由</strong>。
  它靠三招把代价压下来：<strong>列式存储</strong>（只读你查的列）、<strong>ZSTD 压缩</strong>（input/output 大字段压到很小）、
  <strong>延迟读取</strong>（列表只读窄字段，大字段只在详情页拉）。这三招正是后面第 8、24 课的主题。
</div>

<h2>为什么值得：unknown unknowns</h2>
<p>宽事件最大的价值，是回答你<strong>当初没想到要问</strong>的问题。预先聚合的指标只能回答<strong>已知问题</strong>（你建了哪张仪表盘就只能看哪个维度）；
而把高基数上下文整行留下，新问题来了，<strong>换个查询</strong>就能答，不必改埋点、不必等下次上线。</p>

<p>这一点对一个<strong>平台</strong>尤其关键。Langfuse 要给成千上万个项目用，它<strong>不可能</strong>预先知道每个团队会关心什么维度——
有人想看「按 prompt 版本对比成本」，有人想看「按 session 看用户多轮对话的总延迟」，有人想按自定义 <code>metadata</code> 标签切分。
如果走预聚合的老路，平台就得为每种需求预先建一张指标——这既做不完、也僵化。宽事件让 Langfuse 把「<strong>定义新视图</strong>」这件事，
从「<strong>改埋点 + 重新上线</strong>」降级成「<strong>写一条新查询</strong>」：仪表盘、自定义指标、过滤器（第 23、40 课）本质上都是在同一张宽表上换查询。
这就是为什么「保留高基数上下文」不是锦上添花，而是整个平台<strong>可扩展性的地基</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="预聚合指标只能回答已知问题，宽事件能回答事后才想到的新问题">
  <rect x="30" y="48" width="300" height="160" rx="12" fill="var(--red-soft)" stroke="var(--red)"/>
  <text x="180" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="var(--red)">预聚合指标：只能问「已知问题」</text>
  <rect x="54" y="70" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="180" y="90" text-anchor="middle" font-size="10.5" fill="var(--ink)">✅ 平均延迟是多少？（建过这张图）</text>
  <rect x="54" y="108" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="180" y="128" text-anchor="middle" font-size="10.5" fill="var(--ink)">✅ 每分钟请求数？（建过这张图）</text>
  <rect x="54" y="146" width="252" height="46" rx="7" fill="var(--panel)" stroke="var(--red)" stroke-dasharray="4 3"/><text x="180" y="166" text-anchor="middle" font-size="10.5" fill="var(--red)">❌ 用户 X 在模型 Y 上为何变慢？</text><text x="180" y="182" text-anchor="middle" font-size="9" fill="var(--faint)">没预聚合这个维度 → 答不了</text>
  <rect x="390" y="48" width="300" height="160" rx="12" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="540" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">宽事件：还能问「新问题」</text>
  <rect x="414" y="70" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="90" text-anchor="middle" font-size="10.5" fill="var(--ink)">✅ 平均延迟？聚合 latency 列</text>
  <rect x="414" y="108" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="128" text-anchor="middle" font-size="10.5" fill="var(--ink)">✅ 用户 X + 模型 Y 的慢？加两个过滤</text>
  <rect x="414" y="146" width="252" height="46" rx="7" fill="var(--panel)" stroke="var(--accent)"/><text x="540" y="166" text-anchor="middle" font-size="10.5" fill="var(--accent-ink)">✅ 任何事后才想到的切法</text><text x="540" y="182" text-anchor="middle" font-size="9" fill="var(--faint)">高基数整行还在 → 换个查询即可</text>
</svg>
<div class="figcap"><b>已知 vs 未知</b>：预聚合把「能问什么」在上线时就固定了；宽事件把高基数上下文整行留存，于是面对「<b>unknown unknowns</b>」——那些你当初根本没想到要问的问题——只需换一个查询。这就是 Langfuse 宁可让行更宽、也要保留上下文的根本理由。</div>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>可观测性 1.0</strong> = 指标 + 日志 + 链路<strong>三件套分离</strong>，跨维度问题要人肉拼接，能问什么被字段设计锁死。</li>
    <li><strong>可观测性 2.0 / 宽事件</strong> = 把一步操作的数字、结构、业务字段<strong>放进同一条 observation</strong>；下钻与聚合统一成「查同一张宽表」。</li>
    <li>这是写在 <code>.agents/ARCHITECTURE_PRINCIPLES.md</code> 的<strong>第一性原则</strong>，逐条对应后面的存储与查询设计。</li>
    <li>代价是行更宽、存得更多，靠<strong>列存 + ZSTD 压缩 + 延迟读取</strong>三招平衡（第 8 · 24 课）。</li>
    <li>核心收益：能回答 <strong>unknown unknowns</strong>——事后才想到、没预先聚合的问题。</li>
  </ul>
</div>
""")

_EN2.append(r"""
<h2>Wide events: put everything on one row</h2>
<p>The "Observability 2.0" fix is direct: <strong>don't reassemble later — don't split it when you write</strong>. Cram <strong>all
the high-cardinality context</strong> of one step (which model, how many tokens, how much money, how long, which user, which tags,
what environment…) <strong>into one record</strong> — that record is a Langfuse <strong>observation</strong>. It's both a "trace
node" (with <code>parentObservationId</code> to rebuild the call tree), a bag of aggregatable numbers
(<code>usageDetails</code> / <code>costDetails</code> / <code>latency</code>), and a carrier of arbitrary business fields
(<code>metadata</code> / <code>tags</code> / <code>userId</code>). Everything the three pillars do separately, one wide event does
together.</p>

<p>You might ask: why not split these fields into <strong>several normalized tables</strong> with foreign keys — isn't that
"cleaner"? Because <strong>JOINs at query time are a hidden hot-path cost</strong>. Observability data is enormous (an active project
can write hundreds of millions of observations a day); if every "cost by model" had to JOIN the observation table with a "models"
table and a "usage" table, the scan-and-join cost explodes with volume. Langfuse's principle is to <strong>denormalize
carefully</strong>: inline the fields commonly used to filter and aggregate <strong>directly onto the observation row</strong>, so
"by model / by user / by time" become <strong>plain column predicates</strong> instead of JOINs. That's the other meaning of
"wide" — not just many fields, but <strong>deliberately keeping together what belongs together</strong>, trading a little storage
redundancy for not joining at query time.</p>

<div class="cols">
  <div class="col">
    <h4>😕 1.0: split then stitch</h4>
    <p>Metrics, logs and traces live apart; a cross-dimension question means three queries plus manual reconciliation. <strong>What you can ask is locked by field design before you ship.</strong></p>
  </div>
  <div class="col">
    <h4>😀 2.0: one row holds it</h4>
    <p>One observation carries numbers, structure and business fields at once. <strong>Slice, group and filter are all queries over one wide table</strong>; ask anything later. Cost: wider rows, more storage.</p>
  </div>
</div>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="Anatomy of one wide observation row: three kinds of fields on the same row — link fields (id/traceId/parentObservationId building the call tree), numeric fields (latency/usageDetails/costDetails, aggregatable), business fields (model/userId/metadata/tags, filterable/groupable), so asking by model/user/time is a column query over one wide table, no JOIN">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">One observation = three kinds of fields on one row</text>
  <rect x="24" y="38" width="672" height="30" rx="6" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="57" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">one row of the observations wide table (ObservationSchema)</text>
  <rect x="24" y="80" width="216" height="118" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="132" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① link fields (build call tree)</text><text x="132" y="120" text-anchor="middle" font-size="7" fill="var(--muted)">id · traceId · projectId</text><text x="132" y="135" text-anchor="middle" font-size="7" fill="var(--muted)">parentObservationId</text><text x="132" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">type · startTime/endTime</text><text x="132" y="172" text-anchor="middle" font-size="6.4" fill="var(--faint)">makes it a "call-tree node"</text><text x="132" y="185" text-anchor="middle" font-size="6.4" fill="var(--faint)">AND independently queryable</text>
  <rect x="252" y="80" width="216" height="118" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="360" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">② numeric fields (aggregatable)</text><text x="360" y="120" text-anchor="middle" font-size="7" fill="var(--muted)">latency · timeToFirstToken</text><text x="360" y="135" text-anchor="middle" font-size="7" fill="var(--muted)">usageDetails (token usage)</text><text x="360" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">costDetails · totalCost</text><text x="360" y="172" text-anchor="middle" font-size="6.4" fill="var(--faint)">sum/avg/p95 directly,</text><text x="360" y="185" text-anchor="middle" font-size="6.4" fill="var(--faint)">no parsing from logs</text>
  <rect x="480" y="80" width="216" height="118" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="588" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">③ business fields (filter/group)</text><text x="588" y="120" text-anchor="middle" font-size="7" fill="var(--muted)">model · internalModelId</text><text x="588" y="135" text-anchor="middle" font-size="7" fill="var(--muted)">metadata · environment</text><text x="588" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">promptName/Version</text><text x="588" y="172" text-anchor="middle" font-size="6.4" fill="var(--faint)">"by model / by env"</text><text x="588" y="185" text-anchor="middle" font-size="6.4" fill="var(--faint)">collapses to a column predicate</text>
  <text x="360" y="214" text-anchor="middle" font-size="8" fill="var(--faint)">Three kinds of fields on one row → "p95 latency by model", "cost by user" are ordinary column queries over this wide table, no JOIN</text>
</svg>
<div class="figcap"><b>Anatomy of a wide observation</b>: <code>packages/shared/src/domain/observations.ts:55 ObservationSchema</code> packs <b>link</b> (id/traceId/parentObservationId), <b>numeric</b> (latency/usageDetails/costDetails), and <b>business</b> (model/metadata/environment/promptName) fields onto one row. That's the literal meaning of "wide" — and the root of "drill-down = query this table, aggregate = also query this table".</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/observations.ts:55</span><span class="ln">the real shape of one observation</span></div>
  <pre class="code"><span class="kw">export const</span> ObservationSchema = z.<span class="fn">object</span>({
  <span class="cm">// ① link fields: build the call tree, and let this row be queried alone</span>
  id: z.<span class="fn">string</span>(),  traceId: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  projectId: z.<span class="fn">string</span>(),
  parentObservationId: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  type: ObservationTypeDomain,
  <span class="cm">// ② numeric fields: sum/avg/p95 directly, no parsing from logs</span>
  latency: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),  timeToFirstToken: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),
  usageDetails: z.<span class="fn">record</span>(z.<span class="fn">string</span>(), z.<span class="fn">number</span>()),  costDetails: z.<span class="fn">record</span>(z.<span class="fn">string</span>(), z.<span class="fn">number</span>()),
  totalCost: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),  totalUsage: z.<span class="fn">number</span>(),
  <span class="cm">// ③ business fields: make "by model / by env / by prompt" a column predicate</span>
  model: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  environment: z.<span class="fn">string</span>(),  metadata: MetadataDomain,
  promptName: z.<span class="fn">string</span>().<span class="fn">nullable</span>(),  promptVersion: z.<span class="fn">number</span>().<span class="fn">nullable</span>(),
  input: jsonSchema.<span class="fn">nullable</span>(),  output: jsonSchema.<span class="fn">nullable</span>(),  <span class="cm">// big fields, read on the detail page (Lesson 24)</span>
});</pre>
</div>

<h2>How the principles thread through Langfuse</h2>
<p>Every line in <code>ARCHITECTURE_PRINCIPLES.md</code> has an engineering landing spot in a later lesson. Below: "principle → what it buys → where".</p>

<table class="t">
  <tr><th>Architecture principle (gist)</th><th>What it buys</th><th>Lesson</th></tr>
  <tr><td>observation = primary unit; trace = correlation handle</td><td>any step is independently queryable</td><td>L03</td></tr>
  <tr><td>prefer wide, richly-attributed events over fragmented pillars</td><td>drill-down & aggregation unify into one wide table</td><td>L08</td></tr>
  <tr><td>preserve high-cardinality context for unknown unknowns</td><td>ask questions you didn't foresee</td><td>this</td></tr>
  <tr><td>favor immutable / append-oriented records</td><td>no read-time dedup cost; ReplacingMergeTree</td><td>L08</td></tr>
  <tr><td>denormalize carefully to kill hot-path JOINs</td><td>common filters become column predicates</td><td>L08·22</td></tr>
  <tr><td>design around columnar access (narrow fields, time bounds, ordering, pruning)</td><td>ms scans/aggregations even on big tables</td><td>L08·23</td></tr>
  <tr><td>compact list/dashboard views; read big payloads only on detail</td><td>fast lists, full detail, no mutual drag</td><td>L24</td></tr>
  <tr><td>scale-aware API contracts: time windows, token pagination</td><td>avoid accidental full-history scans</td><td>L27</td></tr>
  <tr><td>treat cost & operational simplicity as constraints</td><td>don't casually add DBs/queues/MVs</td><td>L53</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  Wide events aren't free: wider rows, more data written, and you need smart writes + compression. Langfuse's trade is
  <strong>a little storage and write complexity for the freedom to ask anything later</strong>. It tames the cost three ways:
  <strong>columnar storage</strong> (read only the columns you query), <strong>ZSTD compression</strong> (big input/output fields
  shrink hard), <strong>deferred reads</strong> (lists read narrow fields; big fields only on the detail page). Those three are the
  subject of lessons 8 and 24.
</div>

<h2>Why it's worth it: unknown unknowns</h2>
<p>The biggest payoff of wide events is answering questions you <strong>didn't think to ask</strong> up front. Pre-aggregated
metrics answer only <strong>known questions</strong> (you see only the dimensions of dashboards you built); keep the
high-cardinality context on the row and a new question is just a <strong>new query</strong> — no re-instrumenting, no waiting for
the next deploy.</p>

<p>This matters especially for a <strong>platform</strong>. Langfuse serves thousands of projects and <strong>cannot</strong> know in
advance which dimensions each team cares about — one wants "cost by prompt version", another "total latency of a user's multi-turn
<code>session</code>", another to slice by custom <code>metadata</code> tags. The pre-aggregation route would force the platform to
predefine a metric per need — never-ending and rigid. Wide events let Langfuse demote "<strong>define a new view</strong>" from
"<strong>change instrumentation + redeploy</strong>" to "<strong>write a new query</strong>": dashboards, custom metrics and filters
(lessons 23, 40) are all just different queries over the same wide table. That's why "preserve high-cardinality context" isn't a
nicety — it's the <strong>foundation of the platform's extensibility</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Pre-aggregated metrics answer only known questions; wide events answer new questions thought of later">
  <rect x="30" y="48" width="300" height="160" rx="12" fill="var(--red-soft)" stroke="var(--red)"/>
  <text x="180" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="var(--red)">Pre-aggregated: only "known questions"</text>
  <rect x="54" y="70" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="180" y="90" text-anchor="middle" font-size="10" fill="var(--ink)">✅ average latency? (you built this chart)</text>
  <rect x="54" y="108" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="180" y="128" text-anchor="middle" font-size="10" fill="var(--ink)">✅ requests/min? (you built this chart)</text>
  <rect x="54" y="146" width="252" height="46" rx="7" fill="var(--panel)" stroke="var(--red)" stroke-dasharray="4 3"/><text x="180" y="166" text-anchor="middle" font-size="10" fill="var(--red)">❌ why is user X slow on model Y?</text><text x="180" y="182" text-anchor="middle" font-size="9" fill="var(--faint)">dimension not pre-aggregated → can't</text>
  <rect x="390" y="48" width="300" height="160" rx="12" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="540" y="40" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">Wide events: also "new questions"</text>
  <rect x="414" y="70" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="90" text-anchor="middle" font-size="10" fill="var(--ink)">✅ avg latency? aggregate the latency col</text>
  <rect x="414" y="108" width="252" height="30" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="128" text-anchor="middle" font-size="10" fill="var(--ink)">✅ user X + model Y slow? add two filters</text>
  <rect x="414" y="146" width="252" height="46" rx="7" fill="var(--panel)" stroke="var(--accent)"/><text x="540" y="166" text-anchor="middle" font-size="10" fill="var(--accent-ink)">✅ any slice thought of later</text><text x="540" y="182" text-anchor="middle" font-size="9" fill="var(--faint)">row still has the context → just re-query</text>
</svg>
<div class="figcap"><b>Known vs unknown</b>: pre-aggregation fixes "what you can ask" at ship time; wide events keep the high-cardinality context on the row, so facing <b>unknown unknowns</b> — the questions you never thought to ask — you just write a new query. That's the root reason Langfuse keeps rows wide.</div>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Observability 1.0</strong> = metrics + logs + traces, <strong>three split pillars</strong>; cross-dimension questions need manual reassembly, and what you can ask is locked by field design.</li>
    <li><strong>Observability 2.0 / wide events</strong> = put numbers, structure and business fields of one step <strong>on one observation</strong>; drill-down and aggregation unify into "query one wide table".</li>
    <li>This is a <strong>first principle</strong> in <code>.agents/ARCHITECTURE_PRINCIPLES.md</code>, mapping line-by-line to later storage/query design.</li>
    <li>The cost is wider rows and more storage, balanced by <strong>columnar storage + ZSTD compression + deferred reads</strong> (L08·24).</li>
    <li>Core payoff: answering <strong>unknown unknowns</strong> — questions thought of after the fact, never pre-aggregated.</li>
  </ul>
</div>
""")

_ZH2.append(r"""
<h2>十条原则，四个主题</h2>
<p>九到十条原则乍看零散，其实围着<strong>四个主题</strong>转——它们层层递进，正好对应这份指南后面四大块内容。把它们分组记，比逐条背更有用：</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">数据模型</span><span class="name">observation 为主 · 高基数</span></div>
    <div class="ld">先把「记什么」定对：以 observation 为主分析单元、保留高基数上下文。记错了，后面再快的存储也救不回来。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">存储</span><span class="name">宽 · 不可变 · 反范式 · 列式</span></div>
    <div class="ld">再把「怎么存」定对：宽事件、追加不可变（ReplacingMergeTree）、谨慎反范式化、围绕列式访问设计排序键与分区。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">查询</span><span class="name">紧凑列表 · 详情才读大字段</span></div>
    <div class="ld">然后把「怎么读」定对：列表/仪表盘用紧凑的查询优化表示，大块 input/output 只在单条详情页才拉取。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">契约与成本</span><span class="name">规模感知 API · 运维从简</span></div>
    <div class="ld">最后把「对外/对运维」定对：API 强制时间窗口与 token 分页，避免扫全表；把额外的库、队列、物化视图的运维负担当成真实成本来权衡。</div></div>
</div>

<p>这四组也正是本指南的主线：<strong>数据模型</strong>是第一部分（本部分），<strong>存储</strong>是第二部分，<strong>写入与查询</strong>两条链路是第三、四部分，
<strong>契约与成本</strong>则散落在公共 API（第 27 课）与运维（第 53 课）。换句话说，你现在读的这份「设计哲学」，就是后面五十多课的<strong>提纲</strong>。</p>

<p>还有一条容易被忽略但很关键的原则：<strong>保留近实时的调试体验</strong>（原文：<em>"Preserve real-time or near-real-time debugging
workflows. Batch processing can help, but it should not make fresh production behavior invisible."</em>）。这解释了为什么 Langfuse
的摄取虽是<strong>异步</strong>的，却要把处理延迟压到<strong>秒级</strong>——可观测性如果「看不到刚刚发生的事」，就失去了一半意义。这条会在第 14–17 课的摄取链路里反复出现。</p>
""")

_EN2.append(r"""
<h2>Ten principles, four themes</h2>
<p>The nine-to-ten principles look scattered but revolve around <strong>four themes</strong> — layered, and matching the four big
blocks of this guide. Grouping them beats memorizing them one by one:</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">data model</span><span class="name">observation-first · high cardinality</span></div>
    <div class="ld">Get "what to record" right first: observation as the primary unit, keep high-cardinality context. Get this wrong and no amount of fast storage saves you.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">storage</span><span class="name">wide · immutable · denormalized · columnar</span></div>
    <div class="ld">Then "how to store": wide events, append-only immutability (ReplacingMergeTree), careful denormalization, ordering keys & partitions designed for columnar access.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">query</span><span class="name">compact lists · big fields on detail only</span></div>
    <div class="ld">Then "how to read": lists/dashboards on compact query-optimized representations; big input/output fetched only on a single detail page.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">contract & cost</span><span class="name">scale-aware API · lean ops</span></div>
    <div class="ld">Finally "outward/ops": APIs force time windows and token pagination to avoid full scans; treat extra DBs, queues and materialized views as real operational cost.</div></div>
</div>

<p>These four groups are also the spine of this guide: <strong>data model</strong> is Part 1 (here), <strong>storage</strong> is Part 2,
the <strong>write and read paths</strong> are Parts 3–4, and <strong>contract & cost</strong> show up in the public API (L27) and
operations (L53). In other words, the "design philosophy" you're reading now is the <strong>outline</strong> of the fifty-odd
lessons ahead.</p>

<p>One easily-missed but crucial principle: <strong>preserve near-real-time debugging</strong> (verbatim: <em>"Preserve real-time or
near-real-time debugging workflows. Batch processing can help, but it should not make fresh production behavior invisible."</em>).
This is why Langfuse's ingestion, though <strong>async</strong>, keeps processing lag to <strong>seconds</strong> — observability that
"can't see what just happened" loses half its value. This recurs across the ingestion path in lessons 14–17.</p>
""")

LESSON_02 = {"zh": "\n".join(_ZH2), "en": "\n".join(_EN2)}


# ══════════════════════════════════════════════════════════════════════
# L03 · 三大支柱深入：trace / observation / score / The three pillars in depth
# ══════════════════════════════════════════════════════════════════════
_ZH3 = []
_EN3 = []

_ZH3.append(r"""
<p class="lead">
第 1 课认识了 trace / observation / score 三个名字，这一课把它们<strong>拆开看里子</strong>：每个到底有哪些字段、为什么这样设计、
又怎么落到 ClickHouse 的三张表上。它们的「真身」是 <code>packages/shared/src/domain/</code> 下的三个 Zod schema——
<strong>读懂这三个 schema，等于拿到了理解 Langfuse 后面所有功能的钥匙</strong>，因为评估、数据集、仪表盘……最终都在操作这三种对象。
打个比方，如果说第 1 课给了你一张「Langfuse 全景照」，这一课就是把照片里的三个主角拉到跟前，挨个看清他们的<strong>五官</strong>——
记住他们长什么样，后面无论他们出现在哪一课的剧情里，你都能一眼认出。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把一次完整的用户交互想成医院里<strong>一个病历夹</strong>（trace）：夹子封面只写几行身份信息（谁、什么时候、贴了哪些标签）。
  夹子里<strong>一页页具体记录</strong>才是重点（observation）：这页是「拍了 CT」、那页是「开了药」、再一页是「医生下了诊断」——
  每页都详细写明用了什么、花了多久、多少钱。最后，<strong>页边的红笔批注</strong>（score）给某一页或整个夹子打分：「这个诊断准确吗？9 分」。
  封面薄、内页厚、批注点睛——这正是三大支柱的分工。把这套「夹子—内页—批注」的画面记住，下面看字段时就不会迷路：凡是「整次交互级」的信息往封面（trace）放，凡是「某一步级」的信息往内页（observation）放，凡是「评判级」的信息就是批注（score）。
</div>
""")

_EN3.append(r"""
<p class="lead">
Lesson 1 introduced the names trace / observation / score; this lesson <strong>opens them up</strong>: exactly which fields each
has, why it's designed that way, and how each lands in one of three ClickHouse tables. Their "true form" is three Zod schemas under
<code>packages/shared/src/domain/</code> — <strong>read these three schemas and you hold the key to every later Langfuse
feature</strong>, because evaluation, datasets, dashboards… all ultimately operate on these three objects.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Picture one full user interaction as a hospital <strong>chart folder</strong> (trace): the cover has just a few identity lines
  (who, when, which tags). The <strong>pages inside</strong> are the point (observations): this page is "ran a CT scan", that one
  "prescribed a drug", another "the doctor reached a diagnosis" — each page detailing what was used, how long it took, how much it
  cost. Finally, <strong>red-pen margin notes</strong> (score) rate a page or the whole folder: "is this diagnosis accurate? 9/10".
  Thin cover, thick pages, pinpoint notes — exactly the division of the three pillars. Hold this "folder — pages — notes" image and
  you won't get lost in the fields below: whatever is "whole-interaction level" goes on the cover (trace), whatever is "single-step
  level" goes on a page (observation), and whatever is "judgment level" is a margin note (score).
</div>
""")

_ZH3.append(r"""
<div class="fig">
<svg viewBox="0 0 720 330" role="img" aria-label="observation 通过 parentObservationId 指向父节点，从而拼出一棵调用树">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">observation 靠 parentObservationId 拼成一棵树</text>
  <rect x="40" y="34" width="640" height="26" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="52" y="52" font-size="11" font-weight="700" fill="var(--accent-ink)">trace（关联句柄）· traceId 把下面这些 observation 串起来</text>
  <rect x="280" y="78" width="170" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="365" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="var(--blue)">A · span: agent-run</text>
  <text x="365" y="115" text-anchor="middle" font-size="9.5" fill="var(--muted)">parentObservationId = null（根）</text>
  <rect x="110" y="168" width="180" height="48" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="200" y="188" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">B · span: retrieve</text>
  <text x="200" y="205" text-anchor="middle" font-size="9.5" fill="var(--muted)">parent = A</text>
  <rect x="470" y="168" width="180" height="56" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/>
  <text x="560" y="187" text-anchor="middle" font-size="11" font-weight="700" fill="var(--amber)">C · generation: gpt-4o</text>
  <text x="560" y="203" text-anchor="middle" font-size="9" fill="var(--muted)">parent = A · 1,240 tok · $0.012</text>
  <text x="560" y="216" text-anchor="middle" font-size="9" fill="var(--muted)">latency 1.8s · prompt v3</text>
  <rect x="110" y="258" width="180" height="48" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="200" y="278" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">D · span: rerank</text>
  <text x="200" y="295" text-anchor="middle" font-size="9.5" fill="var(--muted)">parent = B</text>
  <line x1="200" y1="168" x2="320" y2="126" stroke="var(--faint)" stroke-width="1.6"/><polygon points="320,126 309,127 314,134" fill="var(--faint)"/>
  <line x1="560" y1="168" x2="410" y2="126" stroke="var(--faint)" stroke-width="1.6"/><polygon points="410,126 416,134 421,127" fill="var(--faint)"/>
  <line x1="200" y1="258" x2="200" y2="218" stroke="var(--faint)" stroke-width="1.6"/><polygon points="200,218 195,228 205,228" fill="var(--faint)"/>
  <text x="250" y="150" font-size="9" fill="var(--faint)">parentObservationId →</text>
</svg>
<div class="figcap"><b>树是「指」出来的</b>：observation 表里并没有「children」字段；每个 observation 只记一个 <code>parentObservationId</code> 指向父节点，UI 再据此<b>反向拼出</b>整棵调用树（第 25 课）。根节点的 parent 为 null。这种「只存父指针」的设计，让写入时各 observation <b>互相独立、可乱序到达</b>——非常契合异步摄取。</div>
</div>

<h2>trace：薄薄的关联句柄</h2>
<p>先看最简单的 trace。它的领域模型 <code>TraceDomain</code> 字段很少，几乎都是<strong>身份与标记</strong>，没有什么「重」数据：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/traces.ts</span><span class="ln">TraceDomain</span></div>
  <pre class="code"><span class="kw">export const</span> TraceDomain = z.<span class="fn">object</span>({
  id: z.<span class="fn">string</span>(),            <span class="cm">// trace 的唯一 id</span>
  name: z.<span class="fn">string</span>().nullable(),
  timestamp: z.<span class="fn">date</span>(),
  environment: z.<span class="fn">string</span>(),    <span class="cm">// 多租户隔离维度（第 10 课）</span>
  tags: z.<span class="fn">array</span>(z.string()),
  bookmarked: z.<span class="fn">boolean</span>(),
  public: z.<span class="fn">boolean</span>(),
  sessionId: z.<span class="fn">string</span>().nullable(), <span class="cm">// 串成会话（第 26 课）</span>
  userId: z.<span class="fn">string</span>().nullable(),
  input: jsonSchema.<span class="fn">nullable</span>(),   <span class="cm">// 整次交互的输入/输出</span>
  output: jsonSchema.<span class="fn">nullable</span>(),
  metadata: MetadataDomain,
  projectId: z.<span class="fn">string</span>(),
});</pre>
</div>

<p>注意 trace 上几乎没有「成本」「token」「模型」这类字段——<strong>那些都在 observation 上</strong>。trace 的职责就是<strong>把一次交互的所有 observation 关联起来</strong>，
外加几个方便检索的标记：<code>userId</code>（哪个用户）、<code>sessionId</code>（哪一轮会话）、<code>tags</code>（自定义标签）、<code>bookmarked</code>（人工收藏）、
<code>public</code>（是否可公开分享）。这印证了第 1 课那句话：<strong>trace 是关联句柄，不是主分析单元</strong>。</p>

<p>别小看这几个「标记」字段，它们各自对应一个真实的产品功能：<code>bookmarked</code> 让你在排查时把可疑 trace <strong>收藏</strong>起来稍后细看；
<code>public</code> 控制这条 trace 能否生成一个<strong>公开分享链接</strong>（第 27 课），方便你把一个坏 case 甩给同事而不用对方登录；
<code>environment</code> 把 prod / staging / dev 的数据<strong>隔离</strong>开（第 10 课），避免测试流量污染线上看板；<code>release</code> 和
<code>version</code> 记录「这条 trace 来自应用的哪个版本」，于是上线后回归时，你能直接<strong>按版本对比</strong>质量与成本。换句话说，trace 虽薄，
但每个字段都是为「事后好查、好分享、好归类」而精心挑选的。</p>

<h2>observation：真正的主角</h2>
<p>observation 才是「厚」的那一个。先看类型——很多人以为只有 3 种，其实当前领域模型 <code>ObservationType</code> 有 <strong>10 种</strong>：</p>

<p>在看字段之前，先理解上面那张树图背后的一个关键设计：observation 之间的父子关系，<strong>只靠子节点上的一个 <code>parentObservationId</code> 指针</strong>表达，
父节点完全不知道自己有哪些孩子。这看似简单，却是为<strong>异步摄取</strong>量身定做的——因为每个 observation 都<strong>自带</strong>「我爸是谁」，它们就能
<strong>各自独立、乱序到达</strong>服务端：子节点比父节点先到也没关系，反正等查询时 UI 再按指针把树拼出来（第 25 课）。如果反过来让父节点维护一个 children 列表，
那就得「等所有孩子到齐才能写父节点」，在高并发异步管线里这是灾难。<strong>一个小小的指针方向选择，背后是整条摄取链路的可行性。</strong></p>

<table class="t">
  <tr><th>类型</th><th>含义</th><th>典型场景</th></tr>
  <tr><td class="mono">GENERATION</td><td>一次 LLM 调用</td><td>带 model / token / cost 的那种</td></tr>
  <tr><td class="mono">SPAN</td><td>一段有耗时的逻辑</td><td>检索、预处理、整段流程</td></tr>
  <tr><td class="mono">EVENT</td><td>一个瞬时事件</td><td>打点、状态变化</td></tr>
  <tr><td class="mono">AGENT</td><td>一个 agent 步骤</td><td>agent 框架的一轮决策</td></tr>
  <tr><td class="mono">TOOL</td><td>一次工具调用</td><td>function/tool call</td></tr>
  <tr><td class="mono">CHAIN</td><td>一条链</td><td>LangChain 式的链路</td></tr>
  <tr><td class="mono">RETRIEVER</td><td>一次检索</td><td>向量/关键词召回</td></tr>
  <tr><td class="mono">EMBEDDING</td><td>一次向量化</td><td>embedding 调用</td></tr>
  <tr><td class="mono">EVALUATOR</td><td>一次评估</td><td>评审步骤</td></tr>
  <tr><td class="mono">GUARDRAIL</td><td>一次护栏检查</td><td>安全/合规拦截</td></tr>
</table>

<p>这 10 种里，<code>SPAN / EVENT / GENERATION</code> 是<strong>最基础的三型</strong>（最早的 <code>LegacyPrismaObservationType</code> 就只有这 3 个），
其余 7 种是后来为更精细地刻画 agent/RAG 流程而加的「更具体的 span」。除了类型，observation 还有 <code>level</code>（DEBUG/DEFAULT/WARNING/ERROR）
表示严重程度。真正让它「厚」的，是下面这一大堆<strong>富属性字段</strong>：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/observations.ts</span><span class="ln">ObservationSchema（节选）</span></div>
  <pre class="code">  parentObservationId: z.string().nullable(), <span class="cm">// 拼树用的父指针</span>
  model: z.string().nullable(),               <span class="cm">// 哪个模型</span>
  modelParameters: jsonSchema.nullable(),
  input: jsonSchema.nullable(),
  output: jsonSchema.nullable(),
  promptId / promptName / promptVersion,      <span class="cm">// 关联到哪版 prompt（第 37 课）</span>
  latency, timeToFirstToken,                  <span class="cm">// 延迟 / 首 token 时延</span>
  usageDetails, costDetails,                  <span class="cm">// 用量 / 成本明细（Map）</span>
  inputUsage / outputUsage / totalUsage,      <span class="cm">// 聚合后的 token 数</span>
  inputCost / outputCost / totalCost,         <span class="cm">// 聚合后的成本</span>
  toolDefinitions, toolCalls, toolCallNames,  <span class="cm">// 工具调用信息</span></pre>
</div>

<p>看到没——一条 observation 就把「这步用了哪个模型、吃了多少 token、花了多少钱、多久、关联哪版 prompt、调了哪些工具」<strong>全装下了</strong>。
这正是第 2 课说的「宽事件」：高基数上下文整行内联，于是「按模型看成本」「按 prompt 版本比延迟」都成了对这张宽表的普通查询。</p>

<p>这里有个容易混淆、但很能体现设计用心的细节：用量和成本各有<strong>两套字段</strong>——<code>providedUsageDetails</code> / <code>providedCostDetails</code>
是 <strong>SDK 上报时「自带」</strong>的（你的应用如果知道 token 数和价格，可以直接报上来），而 <code>usageDetails</code> / <code>costDetails</code>
是 <strong>Langfuse 自己「算出来」</strong>的（摄取时按模型定价表计算，第 16 课）。两套并存的好处是：<strong>你报的我尊重，你没报的我兜底</strong>——
既允许应用精确控制，又保证即使应用什么都不报，Langfuse 也能根据 model 名匹配定价、把成本补齐。这种「provided 优先、computed 兜底」的模式，
在后面成本计算一课会反复出现。</p>

<p>还有两个不起眼但排错时极有用的字段：<code>level</code>（DEBUG / DEFAULT / WARNING / ERROR）和 <code>statusMessage</code>。前者给每个 observation 标上
<strong>严重程度</strong>，后者记一句<strong>状态说明</strong>（比如报错信息）。有了它们，你就能在成千上万条 observation 里一键过滤出
<code>level = ERROR</code> 的那些——直接定位「哪一步挂了、报了什么」，而不必从头翻整棵树。这又一次体现了「把高基数上下文留在每一步上」的价值：
连「这步是不是出错了」都是可查询、可聚合的一列。</p>
""")

_EN3.append(r"""
<div class="fig">
<svg viewBox="0 0 720 330" role="img" aria-label="observations point to their parent via parentObservationId, forming a call tree">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">observations form a tree via parentObservationId</text>
  <rect x="40" y="34" width="640" height="26" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="52" y="52" font-size="11" font-weight="700" fill="var(--accent-ink)">trace (correlation handle) · its traceId strings the observations below</text>
  <rect x="280" y="78" width="170" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="365" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="var(--blue)">A · span: agent-run</text>
  <text x="365" y="115" text-anchor="middle" font-size="9.5" fill="var(--muted)">parentObservationId = null (root)</text>
  <rect x="110" y="168" width="180" height="48" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="200" y="188" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">B · span: retrieve</text>
  <text x="200" y="205" text-anchor="middle" font-size="9.5" fill="var(--muted)">parent = A</text>
  <rect x="470" y="168" width="180" height="56" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/>
  <text x="560" y="187" text-anchor="middle" font-size="11" font-weight="700" fill="var(--amber)">C · generation: gpt-4o</text>
  <text x="560" y="203" text-anchor="middle" font-size="9" fill="var(--muted)">parent = A · 1,240 tok · $0.012</text>
  <text x="560" y="216" text-anchor="middle" font-size="9" fill="var(--muted)">latency 1.8s · prompt v3</text>
  <rect x="110" y="258" width="180" height="48" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="200" y="278" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">D · span: rerank</text>
  <text x="200" y="295" text-anchor="middle" font-size="9.5" fill="var(--muted)">parent = B</text>
  <line x1="200" y1="168" x2="320" y2="126" stroke="var(--faint)" stroke-width="1.6"/><polygon points="320,126 309,127 314,134" fill="var(--faint)"/>
  <line x1="560" y1="168" x2="410" y2="126" stroke="var(--faint)" stroke-width="1.6"/><polygon points="410,126 416,134 421,127" fill="var(--faint)"/>
  <line x1="200" y1="258" x2="200" y2="218" stroke="var(--faint)" stroke-width="1.6"/><polygon points="200,218 195,228 205,228" fill="var(--faint)"/>
  <text x="250" y="150" font-size="9" fill="var(--faint)">parentObservationId →</text>
</svg>
<div class="figcap"><b>The tree is "pointed" into existence</b>: the observations table has no "children" field; each observation stores one <code>parentObservationId</code> pointing at its parent, and the UI <b>reconstructs</b> the call tree from that (L25). The root's parent is null. Storing only a parent pointer lets observations be <b>independent and arrive out of order</b> at write time — ideal for async ingestion.</div>
</div>

<h2>trace: the thin correlation handle</h2>
<p>Start with the simplest, the trace. Its domain model <code>TraceDomain</code> has few fields, almost all <strong>identity and
markers</strong>, no "heavy" data:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/traces.ts</span><span class="ln">TraceDomain</span></div>
  <pre class="code"><span class="kw">export const</span> TraceDomain = z.<span class="fn">object</span>({
  id: z.<span class="fn">string</span>(),            <span class="cm">// the trace's unique id</span>
  name: z.<span class="fn">string</span>().nullable(),
  timestamp: z.<span class="fn">date</span>(),
  environment: z.<span class="fn">string</span>(),    <span class="cm">// tenancy isolation dimension (L10)</span>
  tags: z.<span class="fn">array</span>(z.string()),
  bookmarked: z.<span class="fn">boolean</span>(),
  public: z.<span class="fn">boolean</span>(),
  sessionId: z.<span class="fn">string</span>().nullable(), <span class="cm">// strung into a session (L26)</span>
  userId: z.<span class="fn">string</span>().nullable(),
  input: jsonSchema.<span class="fn">nullable</span>(),   <span class="cm">// the whole interaction's I/O</span>
  output: jsonSchema.<span class="fn">nullable</span>(),
  metadata: MetadataDomain,
  projectId: z.<span class="fn">string</span>(),
});</pre>
</div>

<p>Notice there's almost no "cost", "token" or "model" field on the trace — <strong>those all live on observations</strong>. The
trace's job is to <strong>correlate all observations of one interaction</strong>, plus a few searchable markers: <code>userId</code>
(which user), <code>sessionId</code> (which conversation), <code>tags</code> (custom labels), <code>bookmarked</code> (human
favorite), <code>public</code> (shareable). This confirms Lesson 1's line: <strong>the trace is a correlation handle, not the
primary analytical unit</strong>.</p>

<p>Don't underrate those "marker" fields — each maps to a real product feature: <code>bookmarked</code> lets you <strong>favorite</strong>
a suspicious trace during triage to revisit later; <code>public</code> controls whether the trace can produce a <strong>public share
link</strong> (L27), so you can hand a bad case to a colleague without making them log in; <code>environment</code>
<strong>isolates</strong> prod / staging / dev data (L10) so test traffic doesn't pollute production dashboards; <code>release</code>
and <code>version</code> record "which app version this trace came from", so after a deploy you can <strong>compare quality and cost
by version</strong>. In short, the trace is thin, but every field is hand-picked for "easy to find, share and categorize later".</p>

<h2>observation: the real star</h2>
<p>The observation is the "heavy" one. Types first — many assume there are only 3, but the current <code>ObservationType</code> has
<strong>10</strong>:</p>

<p>Before the fields, grasp one key design behind that tree figure: the parent-child relationship among observations is expressed
<strong>only by a <code>parentObservationId</code> pointer on the child</strong> — the parent has no idea which children it has. Simple
as it looks, this is tailor-made for <strong>async ingestion</strong>: because each observation <strong>carries</strong> "who my
parent is", they can <strong>arrive independently and out of order</strong> at the server — a child arriving before its parent is
fine, since the UI rebuilds the tree from the pointers at query time (L25). Flip it — make the parent maintain a children list — and
you'd have to "wait for all children before writing the parent", a disaster in a high-concurrency async pipeline. <strong>One small
choice of pointer direction underwrites the whole ingestion path's feasibility.</strong></p>

<table class="t">
  <tr><th>Type</th><th>Meaning</th><th>Typical use</th></tr>
  <tr><td class="mono">GENERATION</td><td>one LLM call</td><td>the kind with model / token / cost</td></tr>
  <tr><td class="mono">SPAN</td><td>a timed unit of logic</td><td>retrieval, preprocessing, a whole flow</td></tr>
  <tr><td class="mono">EVENT</td><td>an instantaneous event</td><td>a marker, a state change</td></tr>
  <tr><td class="mono">AGENT</td><td>an agent step</td><td>one decision round in an agent framework</td></tr>
  <tr><td class="mono">TOOL</td><td>a tool call</td><td>function/tool call</td></tr>
  <tr><td class="mono">CHAIN</td><td>a chain</td><td>a LangChain-style chain</td></tr>
  <tr><td class="mono">RETRIEVER</td><td>a retrieval</td><td>vector/keyword recall</td></tr>
  <tr><td class="mono">EMBEDDING</td><td>an embedding</td><td>embedding call</td></tr>
  <tr><td class="mono">EVALUATOR</td><td>an evaluation</td><td>a judging step</td></tr>
  <tr><td class="mono">GUARDRAIL</td><td>a guardrail check</td><td>safety/compliance gate</td></tr>
</table>

<p>Of the 10, <code>SPAN / EVENT / GENERATION</code> are the <strong>three foundational types</strong> (the original
<code>LegacyPrismaObservationType</code> had only these); the other 7 are "more specific spans" added to describe agent/RAG flows
more precisely. Besides type, an observation has a <code>level</code> (DEBUG/DEFAULT/WARNING/ERROR) for severity. What truly makes
it "heavy" is the pile of <strong>rich-attribute fields</strong> below:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/observations.ts</span><span class="ln">ObservationSchema (excerpt)</span></div>
  <pre class="code">  parentObservationId: z.string().nullable(), <span class="cm">// parent pointer for the tree</span>
  model: z.string().nullable(),               <span class="cm">// which model</span>
  modelParameters: jsonSchema.nullable(),
  input: jsonSchema.nullable(),
  output: jsonSchema.nullable(),
  promptId / promptName / promptVersion,      <span class="cm">// which prompt version (L37)</span>
  latency, timeToFirstToken,                  <span class="cm">// latency / time to first token</span>
  usageDetails, costDetails,                  <span class="cm">// usage / cost breakdown (Map)</span>
  inputUsage / outputUsage / totalUsage,      <span class="cm">// aggregated token counts</span>
  inputCost / outputCost / totalCost,         <span class="cm">// aggregated cost</span>
  toolDefinitions, toolCalls, toolCallNames,  <span class="cm">// tool-call info</span></pre>
</div>

<p>See it — one observation captures "which model this step used, how many tokens, how much money, how long, which prompt version,
which tools" <strong>all at once</strong>. This is exactly Lesson 2's "wide event": high-cardinality context inlined on the row, so
"cost by model" and "latency by prompt version" become ordinary queries over this wide table.</p>

<p>One easily-confused detail that shows real design care: usage and cost each have <strong>two sets of fields</strong> —
<code>providedUsageDetails</code> / <code>providedCostDetails</code> are <strong>what the SDK "brought" at report time</strong> (if your
app knows the token count and price, it can send them directly), while <code>usageDetails</code> / <code>costDetails</code> are
<strong>what Langfuse "computed" itself</strong> (at ingestion, from the model pricing table, L16). Keeping both has a clear payoff:
<strong>respect what you sent, backfill what you didn't</strong> — apps can control things precisely, yet even if an app sends
nothing, Langfuse can match the model name to pricing and fill in the cost. This "provided wins, computed backfills" pattern recurs
in the cost lesson.</p>

<p>Two more humble-but-invaluable fields for debugging: <code>level</code> (DEBUG / DEFAULT / WARNING / ERROR) and
<code>statusMessage</code>. The former tags each observation with a <strong>severity</strong>; the latter records a <strong>status
line</strong> (e.g. an error message). With them you can filter tens of thousands of observations down to those with
<code>level = ERROR</code> in one click — jumping straight to "which step failed and what it said" instead of scanning the whole
tree. Again the value of "keep high-cardinality context on each step": even "did this step error" is a queryable, aggregatable
column.</p>
""")

_ZH3.append(r"""
<h2>score：评判</h2>
<p>第三支柱 score 把「可观测」升级成「可评估」。它的两个核心维度是<strong>来源（source）</strong>和<strong>数据类型（dataType）</strong>，都定义在
<code>packages/shared/src/domain/scores.ts</code>：</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="score 来自 EVAL/ANNOTATION/API 三种来源，可挂到 trace 或 observation 上">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">score：从三种来源，打给 trace 或 observation</text>
  <rect x="30" y="50" width="150" height="40" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="105" y="68" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">EVAL</text><text x="105" y="83" text-anchor="middle" font-size="9" fill="var(--muted)">LLM/代码自动评审</text>
  <rect x="30" y="105" width="150" height="40" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="105" y="123" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">ANNOTATION</text><text x="105" y="138" text-anchor="middle" font-size="9" fill="var(--muted)">人工标注</text>
  <rect x="30" y="160" width="150" height="40" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="105" y="178" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">API</text><text x="105" y="193" text-anchor="middle" font-size="9" fill="var(--muted)">SDK 直接提交</text>
  <rect x="300" y="100" width="120" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">score</text><text x="360" y="138" text-anchor="middle" font-size="9" fill="var(--accent-ink)">value + dataType</text>
  <line x1="180" y1="70" x2="298" y2="112" stroke="var(--faint)" stroke-width="1.6"/><polygon points="298,112 287,110 291,118" fill="var(--faint)"/>
  <line x1="180" y1="125" x2="298" y2="125" stroke="var(--faint)" stroke-width="1.6"/><polygon points="298,125 288,120 288,130" fill="var(--faint)"/>
  <line x1="180" y1="180" x2="298" y2="138" stroke="var(--faint)" stroke-width="1.6"/><polygon points="298,138 287,138 291,131" fill="var(--faint)"/>
  <rect x="540" y="72" width="150" height="40" rx="9" fill="var(--panel)" stroke="var(--accent)"/><text x="615" y="90" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">trace</text><text x="615" y="105" text-anchor="middle" font-size="9" fill="var(--muted)">给整次交互打分</text>
  <rect x="540" y="138" width="150" height="40" rx="9" fill="var(--panel)" stroke="var(--accent)"/><text x="615" y="156" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">observation</text><text x="615" y="171" text-anchor="middle" font-size="9" fill="var(--muted)">给某一步打分</text>
  <line x1="420" y1="118" x2="538" y2="92" stroke="var(--accent)" stroke-width="1.6"/><polygon points="538,92 527,92 531,99" fill="var(--accent)"/>
  <line x1="420" y1="132" x2="538" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="538,158 527,151 531,160" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>score 的两端</b>：左边是「谁打的分」——<code>EVAL</code>（自动评审，第 29–31 课）、<code>ANNOTATION</code>（人工，第 32 课）、<code>API</code>（SDK 提交）；右边是「打给谁」——可挂在 <b>trace</b>（整次交互）或某个 <b>observation</b>（具体一步）上。中间的 score 本身带一个值和一个 dataType。</div>
</div>

<p>score 的<strong>数据类型</strong>有 5 种（<code>ScoreDataTypeArray</code>）：<code>NUMERIC</code> 数值、<code>CATEGORICAL</code> 分类、
<code>BOOLEAN</code> 布尔、<code>CORRECTION</code> 订正、<code>TEXT</code> 文本。来源（<code>ScoreSourceArray</code>）有 3 种：
<code>API</code> / <code>EVAL</code> / <code>ANNOTATION</code>。一条规则值得记住：<strong>ANNOTATION 来源的 score 必须带一个匹配的
<code>configId</code></strong>（唯一例外是 CORRECTION 类型），这样它才能在标注队列 UI 里正确渲染——见 <code>scores.ts</code> 的
<code>isAnnotationScoreMissingConfigId</code>。</p>

<table class="t">
  <tr><th>dataType</th><th>取值长什么样</th><th>典型用途</th></tr>
  <tr><td class="mono">NUMERIC</td><td>一个数，如 0.9</td><td>相关性、帮助度等连续评分</td></tr>
  <tr><td class="mono">CATEGORICAL</td><td>一个标签，如「正确」</td><td>把输出分到若干类别</td></tr>
  <tr><td class="mono">BOOLEAN</td><td>true / false</td><td>是否通过、是否安全</td></tr>
  <tr><td class="mono">CORRECTION</td><td>一段订正后的文本</td><td>人工把错误输出改对（不需要 configId）</td></tr>
  <tr><td class="mono">TEXT</td><td>一段自由文本（≤500 字）</td><td>评语、理由</td></tr>
</table>

<p>三种<strong>来源</strong>也不是随便分的，它们对应着不同的「打分主体」，权限也不同：<code>EVAL</code> 是 Langfuse <strong>内部评估器</strong>的产物
（LLM-as-judge、代码评估，第 29–31 课），<strong>保留给系统内部</strong>使用；<code>ANNOTATION</code> 是人在 UI 里手动标注；<code>API</code> 则是你的应用
通过 SDK 直接提交（比如把用户点的「👍/👎」上报成分数）。源码里有个细节能印证这点：公共建分接口允许的来源只有 <code>API</code> 和 <code>ANNOTATION</code>
两种（<code>PublicApiCreateScoreSourceDomain</code>），<code>EVAL</code> 被刻意排除在外——因为它是平台自己产生的，不该由外部冒充。这种「按来源划权限」的小设计，
保证了「谁打的分」这件事可信。</p>

<p>为什么三支柱要落到<strong>三张分开的 ClickHouse 表</strong>，而不是塞进一张大表？因为它们的<strong>访问模式不同</strong>：observation 量最大、查询最频繁、字段最宽；
score 数量少、常按 trace/observation 关联查；trace 居中、是列表页的主入口。分表能让每张表用<strong>最适合自己的排序键与分区</strong>（第 8 课），
互不拖累。这又是一次「按访问模式选存储」的体现——和「为什么 Postgres + ClickHouse 并存」（第 7 课）是同一种思路，只是粒度更细。</p>

<div class="fig">
<svg viewBox="0 0 720 190" role="img" aria-label="三支柱落到三张分开的ClickHouse表：trace(列表主入口,量居中)、observation(量最大字段最宽查询最频繁)、score(量少常按关联查)各一张表，因访问模式不同而分表，各用最适合的排序键与分区，互不拖累；score 通过 traceId/observationId 关联，observation 通过 traceId 关联">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">三支柱 → 三张表：访问模式不同，所以分开存</text>
  <rect x="40" y="44" width="190" height="120" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="135" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">traces 表</text><text x="135" y="84" text-anchor="middle" font-size="6.6" fill="var(--muted)">列表页主入口</text><text x="135" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">量居中</text><text x="135" y="118" text-anchor="middle" font-size="6.5" fill="var(--faint)">排序键/分区</text><text x="135" y="130" text-anchor="middle" font-size="6.5" fill="var(--faint)">为「按时间列表」优化</text>
  <rect x="265" y="44" width="190" height="120" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">observations 表</text><text x="360" y="84" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">量最大·字段最宽</text><text x="360" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">查询最频繁</text><text x="360" y="118" text-anchor="middle" font-size="6.5" fill="var(--faint)">宽事件主场</text><text x="360" y="130" text-anchor="middle" font-size="6.5" fill="var(--faint)">为聚合/过滤优化</text>
  <rect x="490" y="44" width="190" height="120" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="585" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">scores 表</text><text x="585" y="84" text-anchor="middle" font-size="6.6" fill="var(--muted)">量最少</text><text x="585" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">常按关联查</text><text x="585" y="118" text-anchor="middle" font-size="6.5" fill="var(--faint)">为「按 trace/obs 取分」优化</text>
  <line x1="265" y1="150" x2="230" y2="150" stroke="var(--faint)" stroke-width="1.2"/><text x="247" y="146" text-anchor="middle" font-size="5.6" fill="var(--faint)">traceId</text><polygon points="230,150 239,146 239,154" fill="var(--faint)"/>
  <line x1="490" y1="150" x2="455" y2="150" stroke="var(--faint)" stroke-width="1.2"/><text x="472" y="146" text-anchor="middle" font-size="5.4" fill="var(--faint)">traceId/obsId</text><polygon points="455,150 464,146 464,154" fill="var(--faint)"/>
  <text x="360" y="180" text-anchor="middle" font-size="8" fill="var(--faint)">同「Postgres+ClickHouse 并存」（第7课）一脉：按访问模式选存储，只是粒度更细到「一支柱一张表」</text>
</svg>
<div class="figcap"><b>三支柱 → 三张表</b>：observation（量最大、字段最宽、查询最频繁）、trace（列表主入口）、score（量少、常按关联查）访问模式各异，分三张表各用最适合的排序键/分区（第 8 课），互不拖累。score 经 traceId/observationId 关联回去。</div>
</div>

<h2>三者如何落到 ClickHouse 与 sessions</h2>
<p>这三个领域对象，在分析存储里<strong>一一对应三张 ClickHouse 表</strong>（第 8 课细讲）。要区分两个层次：<code>domain/*.ts</code> 里的 Zod schema 是
<strong>「形状契约」</strong>——前端、后端、SDK 都按它理解数据；而 ClickHouse 的建表 SQL 是<strong>「物理存储」</strong>——决定数据在磁盘上怎么排、怎么压、怎么扫。
同一个概念，一个管「长什么样」，一个管「怎么存」：</p>

<div class="cols">
  <div class="col"><h4>领域模型（TS）</h4><p><code>domain/traces.ts</code><br><code>domain/observations.ts</code><br><code>domain/scores.ts</code><br><span class="mono">前端后端共用的形状</span></p></div>
  <div class="col"><h4>ClickHouse 表（宽事件）</h4><p><code>0001_traces.up.sql</code><br><code>0002_observations.up.sql</code><br><code>0003_scores.up.sql</code><br><span class="mono">ReplacingMergeTree · 按月分区</span></p></div>
</div>

<p>还有一个常被忽略的「第四类」聚合：<strong>session（会话）</strong>。它不是一张宽事件表，而是靠 trace 上的 <code>sessionId</code>
把<strong>多次 trace 串成一段连续对话</strong>（比如用户和你的 bot 来回聊了十轮）。session 的元数据在 Postgres 的 <code>TraceSession</code> 模型里，
聚合视图则在查询时算出来（第 26 课）。所以严格说，Langfuse 的核心数据是「三支柱 + 会话聚合」。</p>

<p>举个会话的例子：用户在客服 bot 上连问了三轮——「我的订单到哪了？」→「那能改地址吗？」→「帮我改成公司地址」。这<strong>三轮</strong>各自是一个独立的 trace
（每轮一次完整问答），但它们带着<strong>同一个 <code>sessionId</code></strong>。于是在「会话」视图里，你能把这三个 trace 当成一段连续对话来看：整段聊了多久、
一共花了多少钱、用户在第几轮开始不耐烦。这种「单次看 trace、连续看 session」的双视角，正是因为 <code>sessionId</code> 这一个字段把关联关系<strong>提前埋在了写入里</strong>，
查询时不必再做复杂的会话切分。</p>

<p>把三支柱合起来看，你会发现一个漂亮的分工：<strong>trace 负责「关联」、observation 负责「记录」、score 负责「评判」、session 负责「串联」</strong>。
四者各司其职、字段不重复堆砌，又都能在一次查询里被关联起来。后面五十多课无论讲摄取、查询、评估还是仪表盘，操作的都是这四种对象——
现在把它们的形状刻进脑子里，后面会轻松很多。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么把「重」字段都堆在 observation，而让 trace 这么薄？</strong> 因为查询绝大多数发生在「步」这个粒度：你想按模型、按 prompt 版本、
  按工具调用去聚合和过滤，这些维度天然属于<strong>某一步</strong>，而不是整次交互。把它们放在 observation 上，常用查询就成了对 observations 宽表的直接列谓词；
  trace 只需保留关联和少数检索标记。代价是同一信息（如 userId）可能要在 trace 和 observation 间<strong>冗余</strong>一份——这正是第 2 课「谨慎反范式化」的体现。
  反过来理解这个取舍：Langfuse <strong>主动</strong>付出一点重复，换来用户每天高频运行的查询<strong>无需连表、足够快</strong>。在可观测的数据规模下，这笔账几乎总是划算的。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>trace</strong> 很薄：几乎只有身份与标记（<code>userId/sessionId/tags/bookmarked/public</code>），职责是<strong>关联</strong>。</li>
    <li><strong>observation</strong> 很厚：<code>ObservationType</code> 有 <strong>10 种</strong>（核心三型 SPAN/EVENT/GENERATION），靠 <code>parentObservationId</code> 拼树，内联 model/usage/cost/prompt/tool 等富属性。</li>
    <li><strong>score</strong> 两维度：来源（<code>API/EVAL/ANNOTATION</code>）× 数据类型（<code>NUMERIC/CATEGORICAL/BOOLEAN/CORRECTION/TEXT</code>），可挂 trace 或 observation。</li>
    <li>三者 1:1 落到 <strong>三张 ClickHouse 宽事件表</strong>；<strong>session</strong> 靠 <code>sessionId</code> 把多个 trace 串成会话。</li>
    <li>读懂这三个 <code>domain/*.ts</code> schema，就拿到了理解后面所有功能的钥匙，因为评估、数据集、仪表盘最终都在操作它们。</li>
  </ul>
</div>
""")

_EN3.append(r"""
<h2>score: the verdict</h2>
<p>The third pillar, score, upgrades "observable" into "evaluable". Its two core dimensions are <strong>source</strong> and
<strong>dataType</strong>, both defined in <code>packages/shared/src/domain/scores.ts</code>:</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="A score comes from EVAL/ANNOTATION/API and attaches to a trace or an observation">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">score: from three sources, onto a trace or observation</text>
  <rect x="30" y="50" width="150" height="40" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="105" y="68" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">EVAL</text><text x="105" y="83" text-anchor="middle" font-size="9" fill="var(--muted)">LLM/code auto-judge</text>
  <rect x="30" y="105" width="150" height="40" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="105" y="123" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">ANNOTATION</text><text x="105" y="138" text-anchor="middle" font-size="9" fill="var(--muted)">human annotation</text>
  <rect x="30" y="160" width="150" height="40" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="105" y="178" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">API</text><text x="105" y="193" text-anchor="middle" font-size="9" fill="var(--muted)">submitted via SDK</text>
  <rect x="300" y="100" width="120" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">score</text><text x="360" y="138" text-anchor="middle" font-size="9" fill="var(--accent-ink)">value + dataType</text>
  <line x1="180" y1="70" x2="298" y2="112" stroke="var(--faint)" stroke-width="1.6"/><polygon points="298,112 287,110 291,118" fill="var(--faint)"/>
  <line x1="180" y1="125" x2="298" y2="125" stroke="var(--faint)" stroke-width="1.6"/><polygon points="298,125 288,120 288,130" fill="var(--faint)"/>
  <line x1="180" y1="180" x2="298" y2="138" stroke="var(--faint)" stroke-width="1.6"/><polygon points="298,138 287,138 291,131" fill="var(--faint)"/>
  <rect x="540" y="72" width="150" height="40" rx="9" fill="var(--panel)" stroke="var(--accent)"/><text x="615" y="90" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">trace</text><text x="615" y="105" text-anchor="middle" font-size="9" fill="var(--muted)">rate the whole interaction</text>
  <rect x="540" y="138" width="150" height="40" rx="9" fill="var(--panel)" stroke="var(--accent)"/><text x="615" y="156" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">observation</text><text x="615" y="171" text-anchor="middle" font-size="9" fill="var(--muted)">rate one step</text>
  <line x1="420" y1="118" x2="538" y2="92" stroke="var(--accent)" stroke-width="1.6"/><polygon points="538,92 527,92 531,99" fill="var(--accent)"/>
  <line x1="420" y1="132" x2="538" y2="158" stroke="var(--accent)" stroke-width="1.6"/><polygon points="538,158 527,151 531,160" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>Score's two ends</b>: on the left, "who scored" — <code>EVAL</code> (auto-judge, L29–31), <code>ANNOTATION</code> (human, L32), <code>API</code> (SDK); on the right, "scored what" — attaches to a <b>trace</b> (whole interaction) or an <b>observation</b> (one step). The score itself carries a value and a dataType.</div>
</div>

<p>A score's <strong>dataType</strong> is one of 5 (<code>ScoreDataTypeArray</code>): <code>NUMERIC</code>, <code>CATEGORICAL</code>,
<code>BOOLEAN</code>, <code>CORRECTION</code>, <code>TEXT</code>. Its <strong>source</strong> (<code>ScoreSourceArray</code>) is one
of 3: <code>API</code> / <code>EVAL</code> / <code>ANNOTATION</code>. One rule worth remembering: <strong>an ANNOTATION-sourced score
must carry a matching <code>configId</code></strong> (the sole exception is the CORRECTION type), so it renders correctly in the
annotation-queue UI — see <code>isAnnotationScoreMissingConfigId</code> in <code>scores.ts</code>.</p>

<table class="t">
  <tr><th>dataType</th><th>What the value looks like</th><th>Typical use</th></tr>
  <tr><td class="mono">NUMERIC</td><td>a number, e.g. 0.9</td><td>relevance, helpfulness — continuous scores</td></tr>
  <tr><td class="mono">CATEGORICAL</td><td>a label, e.g. "correct"</td><td>bucket the output into classes</td></tr>
  <tr><td class="mono">BOOLEAN</td><td>true / false</td><td>passed?, safe?</td></tr>
  <tr><td class="mono">CORRECTION</td><td>a corrected text</td><td>a human fixes a wrong output (no configId needed)</td></tr>
  <tr><td class="mono">TEXT</td><td>free text (≤500 chars)</td><td>a comment, a rationale</td></tr>
</table>

<p>The three <strong>sources</strong> aren't arbitrary either — they correspond to different "scoring authors" with different
permissions: <code>EVAL</code> is the output of Langfuse's <strong>internal evaluators</strong> (LLM-as-judge, code evals, L29–31) and
is <strong>reserved for the system</strong>; <code>ANNOTATION</code> is a human labeling in the UI; <code>API</code> is your app
submitting directly via the SDK (e.g. reporting a user's "👍/👎" as a score). A source-code detail confirms this: the public
create-score endpoint allows only <code>API</code> and <code>ANNOTATION</code> sources
(<code>PublicApiCreateScoreSourceDomain</code>), deliberately excluding <code>EVAL</code> — because it's platform-generated and
shouldn't be impersonated from outside. This little "permission by source" design keeps "who scored" trustworthy.</p>

<p>Why do the three pillars land in <strong>three separate ClickHouse tables</strong> rather than one big table? Because their
<strong>access patterns differ</strong>: observations are the largest, most-queried, widest; scores are few and usually queried by
trace/observation association; traces sit in the middle as the list-page entry point. Separate tables let each use the
<strong>ordering key and partitioning best for itself</strong> (L08) without dragging on the others. This is again "choose storage by
access pattern" — the same idea as "why Postgres + ClickHouse coexist" (L07), just at finer granularity.</p>

<div class="fig">
<svg viewBox="0 0 720 190" role="img" aria-label="Three pillars land in three separate ClickHouse tables: trace (list main entry, medium volume), observation (largest volume, widest fields, most-queried), score (low volume, queried by relation), each a table because access patterns differ, each using its best ordering key and partitioning, no mutual drag; score relates via traceId/observationId, observation via traceId">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Three pillars → three tables: different access patterns, stored apart</text>
  <rect x="40" y="44" width="190" height="120" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="135" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">traces table</text><text x="135" y="84" text-anchor="middle" font-size="6.6" fill="var(--muted)">list-page main entry</text><text x="135" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">medium volume</text><text x="135" y="118" text-anchor="middle" font-size="6.2" fill="var(--faint)">ordering/partition</text><text x="135" y="130" text-anchor="middle" font-size="6.2" fill="var(--faint)">optimized for "list by time"</text>
  <rect x="265" y="44" width="190" height="120" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">observations table</text><text x="360" y="84" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">largest · widest fields</text><text x="360" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">most-queried</text><text x="360" y="118" text-anchor="middle" font-size="6.2" fill="var(--faint)">home of wide events</text><text x="360" y="130" text-anchor="middle" font-size="6.2" fill="var(--faint)">optimized for aggregate/filter</text>
  <rect x="490" y="44" width="190" height="120" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="585" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">scores table</text><text x="585" y="84" text-anchor="middle" font-size="6.6" fill="var(--muted)">lowest volume</text><text x="585" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">queried by relation</text><text x="585" y="118" text-anchor="middle" font-size="6.2" fill="var(--faint)">optimized for "fetch by trace/obs"</text>
  <line x1="265" y1="150" x2="230" y2="150" stroke="var(--faint)" stroke-width="1.2"/><text x="247" y="146" text-anchor="middle" font-size="5.6" fill="var(--faint)">traceId</text><polygon points="230,150 239,146 239,154" fill="var(--faint)"/>
  <line x1="490" y1="150" x2="455" y2="150" stroke="var(--faint)" stroke-width="1.2"/><text x="472" y="146" text-anchor="middle" font-size="5.4" fill="var(--faint)">traceId/obsId</text><polygon points="455,150 464,146 464,154" fill="var(--faint)"/>
  <text x="360" y="180" text-anchor="middle" font-size="8" fill="var(--faint)">Same lineage as "Postgres+ClickHouse coexist" (L07): choose storage by access pattern, just finer — "one pillar, one table"</text>
</svg>
<div class="figcap"><b>Three pillars → three tables</b>: observation (largest, widest, most-queried), trace (list main entry), score (low volume, queried by relation) have different access patterns, so three tables each with its best ordering key/partition (L08), no mutual drag. score relates back via traceId/observationId.</div>
</div>

<h2>How the three land in ClickHouse and sessions</h2>
<p>These three domain objects map <strong>one-to-one to three ClickHouse tables</strong> in analytical storage (detailed in L08). Keep
two layers distinct: the Zod schema in <code>domain/*.ts</code> is the <strong>"shape contract"</strong> — frontend, backend and SDK
all read data by it; the ClickHouse CREATE TABLE SQL is the <strong>"physical storage"</strong> — deciding how data is ordered,
compressed and scanned on disk. Same concept: one governs "what it looks like", the other "how it's stored":</p>

<div class="cols">
  <div class="col"><h4>Domain model (TS)</h4><p><code>domain/traces.ts</code><br><code>domain/observations.ts</code><br><code>domain/scores.ts</code><br><span class="mono">shape shared by frontend & backend</span></p></div>
  <div class="col"><h4>ClickHouse table (wide event)</h4><p><code>0001_traces.up.sql</code><br><code>0002_observations.up.sql</code><br><code>0003_scores.up.sql</code><br><span class="mono">ReplacingMergeTree · monthly partitions</span></p></div>
</div>

<p>There's an easily-missed "fourth" aggregation: the <strong>session</strong>. It isn't a wide-event table; it's the trace's
<code>sessionId</code> stringing <strong>multiple traces into one continuous conversation</strong> (e.g. ten back-and-forth turns
with your bot). Session metadata lives in Postgres' <code>TraceSession</code> model; the aggregate view is computed at query time
(L26). So strictly, Langfuse's core data is "three pillars + session aggregation".</p>

<p>A session example: a user asks a support bot three turns in a row — "where's my order?" → "can I change the address?" → "change it
to my office address". Those <strong>three turns</strong> are each an independent trace (one full Q&amp;A each), but they carry the
<strong>same <code>sessionId</code></strong>. So in the "session" view you can see the three traces as one continuous conversation:
how long the whole chat took, how much it cost in total, at which turn the user got impatient. This "single trace vs continuous
session" dual view works precisely because the one <code>sessionId</code> field <strong>plants the relationship at write time</strong>,
so queries need no complex session segmentation.</p>

<p>Put the pillars together and a clean division of labor appears: <strong>trace correlates, observation records, score judges,
session links</strong>. Each does its job, no field is piled up redundantly, yet all can be joined in one query. Whether later
lessons cover ingestion, querying, evaluation or dashboards, they all operate on these four objects — carve their shapes into your
mind now and the rest gets much easier.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why pile the "heavy" fields on the observation and keep the trace so thin?</strong> Because the vast majority of queries
  happen at the "step" granularity: you aggregate and filter by model, by prompt version, by tool call — dimensions that naturally
  belong to <strong>one step</strong>, not the whole interaction. Put them on the observation and common queries become direct column
  predicates over the observations wide table; the trace just keeps correlation and a few search markers. The cost is that some info
  (e.g. userId) may be <strong>redundant</strong> across trace and observation — exactly Lesson 2's "denormalize carefully".
  Read the trade the other way: Langfuse <strong>chooses</strong> to pay a little duplication so that the queries users run all day
  stay JOIN-free and fast. At observability scale, that trade almost always wins.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>trace</strong> is thin: mostly identity and markers (<code>userId/sessionId/tags/bookmarked/public</code>); its job is to <strong>correlate</strong>.</li>
    <li><strong>observation</strong> is heavy: <code>ObservationType</code> has <strong>10</strong> values (core three SPAN/EVENT/GENERATION), builds a tree via <code>parentObservationId</code>, inlines model/usage/cost/prompt/tool rich attributes.</li>
    <li><strong>score</strong> has two dimensions: source (<code>API/EVAL/ANNOTATION</code>) × dataType (<code>NUMERIC/CATEGORICAL/BOOLEAN/CORRECTION/TEXT</code>); attaches to a trace or observation.</li>
    <li>The three map 1:1 to <strong>three ClickHouse wide-event tables</strong>; a <strong>session</strong> strings traces via <code>sessionId</code>.</li>
    <li>Read these three <code>domain/*.ts</code> schemas and you hold the key to every later feature.</li>
  </ul>
</div>
""")

LESSON_03 = {"zh": "\n".join(_ZH3), "en": "\n".join(_EN3)}


# ══════════════════════════════════════════════════════════════════════
# L04 · 项目全景地图（monorepo 与窄腰）/ Project map (monorepo & narrow waist)
# ══════════════════════════════════════════════════════════════════════
_ZH4 = []
_EN4 = []

_ZH4.append(r"""
<p class="lead">
前三课讲的是「数据长什么样」，这一课换个维度：<strong>代码住在哪里</strong>。Langfuse 是一个 <strong>monorepo</strong>（单仓库多工程），
所有东西都在 <code>langfuse/langfuse</code> 一个仓库里，但内部分成几个各司其职的「工作区」。把这张地图记在心里，后面任何一课说「打开
<code>web/src/...</code>」或「这段逻辑在 <code>worker</code> 里」，你都能立刻知道它在哪、为什么在那。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把这个仓库想成<strong>一座大型购物中心</strong>：整座楼是<strong>一个 monorepo</strong>，里面有几家独立店铺——
  <strong>web</strong> 是面向顾客的<strong>门店</strong>（人来人往、要快、随时营业），<strong>worker</strong> 是后场的<strong>加工车间</strong>（埋头干重活、可以排队慢慢做）。
  而 <strong>packages/shared</strong> 是<strong>中央仓库</strong>：所有店铺的货（数据模型、数据库访问、队列契约）都从这里取，但中央仓库<strong>从不反过来依赖</strong>某家店铺。
  大家在<strong>同一栋楼</strong>里，共用水电（构建工具），却又边界清晰、各自营业。逛这座楼之前先拿到这张「楼层导览图」，后面无论去哪家店，你都不会迷路。
</div>
""")

_ZH4.append(r"""
<div class="fig">
<svg viewBox="0 0 720 320" role="img" aria-label="Langfuse 仓库顶层目录：web、worker、packages/shared、ee、fern、generated 各自的职责">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">langfuse/langfuse 顶层目录地图</text>
  <rect x="40" y="40" width="200" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="140" y="64" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">web/</text>
  <text x="140" y="83" text-anchor="middle" font-size="9.5" fill="var(--muted)">Next.js 应用</text>
  <text x="140" y="100" text-anchor="middle" font-size="9.5" fill="var(--muted)">UI · tRPC · 公共 REST API</text>
  <rect x="260" y="40" width="200" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="360" y="64" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">worker/</text>
  <text x="360" y="83" text-anchor="middle" font-size="9.5" fill="var(--muted)">BullMQ 队列消费</text>
  <text x="360" y="100" text-anchor="middle" font-size="9.5" fill="var(--muted)">摄取·评估·导出·删除…</text>
  <rect x="480" y="40" width="200" height="74" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="580" y="64" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">ee/</text>
  <text x="580" y="83" text-anchor="middle" font-size="9.5" fill="var(--muted)">企业版功能</text>
  <text x="580" y="100" text-anchor="middle" font-size="9.5" fill="var(--muted)">license 校验</text>
  <rect x="150" y="150" width="420" height="78" rx="11" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2"/>
  <text x="360" y="174" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--purple)">packages/shared/ · 共享内核（窄腰）</text>
  <text x="360" y="194" text-anchor="middle" font-size="9.5" fill="var(--muted)">domain 领域模型 · server 仓储/CH/队列 · prisma schema · clickhouse 迁移</text>
  <text x="360" y="212" text-anchor="middle" font-size="9.5" fill="var(--muted)">被 web 与 worker 共用，自己谁都不依赖</text>
  <line x1="140" y1="114" x2="300" y2="148" stroke="var(--purple)" stroke-width="1.6"/><polygon points="300,148 289,146 293,154" fill="var(--purple)"/>
  <line x1="360" y1="114" x2="360" y2="148" stroke="var(--purple)" stroke-width="1.6"/><polygon points="360,148 355,138 365,138" fill="var(--purple)"/>
  <line x1="580" y1="114" x2="420" y2="148" stroke="var(--purple)" stroke-width="1.6"/><polygon points="420,148 431,146 427,154" fill="var(--purple)"/>
  <rect x="40" y="252" width="320" height="50" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="200" y="272" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">fern/ · 公共 API 契约定义</text>
  <text x="200" y="290" text-anchor="middle" font-size="9.5" fill="var(--muted)">用 Fern 描述 REST API，生成 generated/ 客户端</text>
  <rect x="380" y="252" width="300" height="50" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="530" y="272" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">generated/ · 自动生成（勿手改）</text>
  <text x="530" y="290" text-anchor="middle" font-size="9.5" fill="var(--muted)">由 Fern 生成的 API 客户端</text>
</svg>
<div class="figcap"><b>顶层就这几块</b>：<b>web</b>（门店）和 <b>worker</b>（车间）是两个运行时容器，都向上依赖 <b>packages/shared</b>（中央仓库 / 窄腰）；<b>ee</b> 是企业功能、被 web 引用；<b>fern</b> 定义公共 API 契约并生成 <b>generated</b> 客户端。记住这张图，后面所有「文件在哪」的问题都有了坐标系。</div>
</div>

<p>稍微展开一下两个运行时各自在忙什么，你会更有体感。<strong>web</strong> 是那个你浏览器里打开的 Next.js 应用，它干三件事：渲染<strong>界面</strong>、
给界面提供类型安全的内部 API（<strong>tRPC</strong>，第 21 课）、以及给外部 SDK 提供<strong>公共 REST API</strong>（<code>web/src/pages/api/public</code>，第 27 课）——
摄取事件的入口就在这里。<strong>worker</strong> 则是个没有界面的后台进程，它订阅几十个 <strong>BullMQ 队列</strong>，把所有<strong>重活、慢活、可重试的活</strong>都揽下来：
把摄取的事件合并写进 ClickHouse、跑 LLM 评估、导出数据、删除项目……（第三部分起逐个讲）。一句话：<strong>web 负责「快进快出」，worker 负责「埋头苦干」</strong>，
两者通过中间的 Redis 队列解耦——这也正是下一课「双存储」和第三部分「摄取链路」要展开的主线。</p>

<h2>一个仓库，四个工作区</h2>
<p>Langfuse 用 <strong>pnpm workspaces</strong> 把一个仓库切成几个独立可构建的包。根目录的 <code>pnpm-workspace.yaml</code> 一行行列出了它们：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">pnpm-workspace.yaml</span><span class="ln">workspaces</span></div>
  <pre class="code">packages:
  - <span class="st">"web"</span>          <span class="cm"># Next.js 应用（UI + tRPC + 公共 REST API）</span>
  - <span class="st">"worker"</span>       <span class="cm"># 队列消费者，后台处理</span>
  - <span class="st">"packages/**"</span>  <span class="cm"># 共享包，主要是 packages/shared</span>
  - <span class="st">"ee"</span>           <span class="cm"># 企业版功能</span></pre>
</div>

<p><code>packages/**</code> 下其实不止 <code>shared</code> 一个，还有 <code>config-eslint</code>、<code>config-typescript</code>、
<code>eslint-plugin</code> 这些「工具配置包」；但真正承载业务的<strong>共享内核是 <code>packages/shared</code></strong>——它就是上图里的中央仓库。
为什么要拆成工作区而不是一个大文件夹？因为这样每个包能<strong>独立声明依赖、独立构建、独立测试</strong>，pnpm 还能在它们之间做<strong>符号链接</strong>，
让 web 直接 <code>import ... from "@langfuse/shared"</code> 用上最新代码，不必发版。
这点对开发体验影响很大：你在 <code>packages/shared</code> 里改一个类型，<code>web</code> 和 <code>worker</code> 的编辑器会<strong>立刻飘红</strong>提示哪里要跟着改——
等于把「契约变更」的影响在<strong>编码阶段</strong>就暴露出来，而不是等到运行时才报错。</p>
""")

_ZH4.append(r"""
<h2>依赖方向：为什么是「窄腰」</h2>
<p>四个工作区之间不是随便互相引用的，而是有一条<strong>严格单向</strong>的依赖规则（写在 <code>.agents/AGENTS.md</code> 里）：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">.agents/AGENTS.md</span><span class="ln">Dependency direction</span></div>
  <pre class="code">- <span class="nb">web</span>    -> @langfuse/shared, @langfuse/ee
- <span class="nb">worker</span> -> @langfuse/shared
- <span class="nb">ee</span>     -> @langfuse/shared
- <span class="nb">@langfuse/shared</span> -> <span class="kw">no imports from</span> web, worker, or ee</pre>
</div>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="web、worker、ee 都单向依赖 shared，shared 不依赖任何一方，形成窄腰">
  <text x="360" y="24" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">窄腰：所有依赖箭头都指向 shared，没有回头箭头</text>
  <rect x="60" y="50" width="150" height="48" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="135" y="79" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">web</text>
  <rect x="285" y="50" width="150" height="48" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="79" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">worker</text>
  <rect x="510" y="50" width="150" height="48" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="585" y="79" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">ee</text>
  <rect x="210" y="168" width="300" height="56" rx="12" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2.5"/>
  <text x="360" y="192" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--purple)">packages/shared</text>
  <text x="360" y="210" text-anchor="middle" font-size="9.5" fill="var(--muted)">领域模型 · 仓储 · 队列契约 · DB 访问</text>
  <line x1="135" y1="98" x2="285" y2="166" stroke="var(--faint)" stroke-width="1.8"/><polygon points="285,166 273,162 277,172" fill="var(--faint)"/>
  <line x1="360" y1="98" x2="360" y2="166" stroke="var(--faint)" stroke-width="1.8"/><polygon points="360,166 355,156 365,156" fill="var(--faint)"/>
  <line x1="585" y1="98" x2="435" y2="166" stroke="var(--faint)" stroke-width="1.8"/><polygon points="435,166 447,162 443,172" fill="var(--faint)"/>
  <text x="360" y="244" text-anchor="middle" font-size="10" fill="var(--purple)">shared 不依赖上面任何一个 → 它是地基，不是消费者</text>
</svg>
<div class="figcap"><b>「窄腰」（narrow waist）</b>：把所有人都要用的东西收进一个<b>谁都不反向依赖</b>的薄层。web/worker/ee 像沙漏的上半，shared 是中间最细的「腰」，再往下是数据库。好处是：两个容器各自独立演进、独立部署，却共用同一套领域模型与队列契约，<b>契约不会漂移</b>。</div>
</div>

<p>这条纪律为什么重要？因为 web 和 worker 是<strong>两种完全不同的负载</strong>：web 要面向用户、低延迟、可随时重启；worker 要啃重活、可重试、按队列伸缩。
如果让它们<strong>互相直接引用</strong>，改一个就可能牵连另一个，部署也会绑死。把共享的东西收进 shared、并规定<strong>只能向下依赖</strong>，
就等于在两个容器之间立了一道清晰的<strong>契约墙</strong>：队列里传什么、数据库表长什么样，都由 shared 这一处定义（比如队列负载就归
<code>packages/shared/src/server/queues.ts</code> 管）。两边照着同一份契约各干各的，互不踩脚。</p>

<p>举个这条规则<strong>挡住的真实 bug</strong>：假设没有窄腰，worker 里图省事直接 <code>import</code> 了 web 的某个工具函数。某天 web 为了改界面重构了那个函数、
顺手改了它的参数——结果 <strong>worker 在毫不知情的情况下被改坏了</strong>，可能要到线上摄取出错才发现。而在窄腰规则下，worker 根本<strong>不允许</strong>依赖 web；
两边唯一的「共同语言」是 shared 里那份明确的契约。想共享逻辑？那就把它<strong>下沉</strong>到 shared，让它成为受契约约束的一等公民，而不是从隔壁悄悄借用。
<strong>「依赖只能向下」这一条，本质是在用编译器帮你挡住跨容器的隐式耦合。</strong></p>

<h2>Turbo 怎么把它们编排起来</h2>
<p>多个工作区的构建、测试、lint 由 <strong>Turbo</strong> 统一编排（根目录 <code>turbo.json</code>）。它最有用的两件事是<strong>任务依赖图</strong>和<strong>缓存</strong>：</p>

<div class="flow">
  <div class="node"><div class="nt">db:generate</div><div class="nd">先生成 Prisma 客户端</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">^build</div><div class="nd">先构建被依赖的包</div></div>
  <div class="arrow">→</div>
  <div class="node hl"><div class="nt">build</div><div class="nd">再构建本包</div></div>
  <div class="arrow">⚡</div>
  <div class="node"><div class="nt">cache</div><div class="nd">没变就直接命中缓存</div></div>
</div>

<p>看 <code>turbo.json</code> 里 <code>build</code> 任务的定义：<code>"dependsOn": ["db:generate", "^build"]</code>——意思是「构建任何一个包之前，
先生成数据库客户端、并先把它依赖的包（<code>^</code> 表示上游依赖）构建好」。于是你只要 <code>pnpm build</code>，Turbo 就会自动算出正确顺序、
把能并行的并行、能缓存的<strong>跳过</strong>（<code>"cache": true</code>）。这就是为什么在一个有几十个包的大仓库里，改一行代码也不必全量重建。</p>

<p>把窄腰和 Turbo 合起来，看一个<strong>具体的连锁反应</strong>：假设你要给 trace 加一个字段。你只需在
<code>packages/shared/prisma/schema.prisma</code> 改一处、再在 <code>domain/traces.ts</code> 改一处——一次 <code>db:generate</code> 重新生成
Prisma 客户端，<strong>web 和 worker 立刻都看到新字段</strong>，因为它们都从同一个 <code>@langfuse/shared</code> 取类型。整件事在<strong>一个 PR</strong> 里完成，
CI 一起跑通。要是分成三个仓库，这同一个改动得发三次版、改三处依赖、还要祈祷三边版本对得上——这就是「原子地一起改」的实际意义。</p>

<div class="cols">
  <div class="col"><h4>🧩 polyrepo（分仓）</h4><p>web/worker/shared 各一个仓。改一个共享结构 → 跨仓发版、对版本、易漂移。好处是各仓更小、更独立。</p></div>
  <div class="col"><h4>📦 monorepo（Langfuse 的选择）</h4><p>一个仓装下全部。共享改动一个 PR 原子完成、CI 一起验。代价：仓更大、要靠 Turbo 管构建缓存。</p></div>
</div>

<p>缓存这件事对<strong>持续集成（CI）</strong>尤其值钱。一个几十包的大仓，如果每次 PR 都把所有包从头 build + lint + test 一遍，CI 会慢到没法用。
Turbo 会给每个任务的<strong>输入算一个指纹</strong>（源码 + 依赖 + 配置），只要指纹没变，就直接<strong>复用上次的输出</strong>、整段跳过。于是改了 <code>worker</code> 的一个文件，
<code>web</code> 那些没被波及的构建/测试就<strong>命中缓存、秒过</strong>。配上远端缓存，团队成员之间还能共享构建结果。这就是大仓也能保持 CI 快的秘诀——
也是「用 monorepo」这个选择能成立的<strong>工程前提</strong>：没有好的缓存，monorepo 的构建成本会劝退所有人。</p>

<svg viewBox="0 0 720 230" role="img" aria-label="Turbo 缓存按指纹工作：改了 worker 的一个文件，Turbo 给每个包的任务算指纹（源码加依赖加配置）逐包比对，worker 指纹变了要重建，web 指纹没变直接命中缓存秒过，shared 没变也命中；远端缓存还能在团队成员间共享构建结果">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">Turbo 缓存：给每个任务的输入算指纹，没变就整段跳过</text>
  <rect x="16" y="72" width="150" height="46" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="91" y="92" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">改 worker</text>
  <text x="91" y="108" font-size="9.5" text-anchor="middle" fill="var(--muted)">一个文件</text>
  <line x1="166" y1="95" x2="200" y2="95" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="200" y="52" width="160" height="120" rx="10" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="280" y="78" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Turbo 算指纹</text>
  <text x="280" y="102" font-size="9.5" text-anchor="middle" fill="var(--ink)">= 源码 + 依赖</text>
  <text x="280" y="118" font-size="9.5" text-anchor="middle" fill="var(--ink)">+ 配置</text>
  <text x="280" y="146" font-size="9.5" text-anchor="middle" fill="var(--muted)">逐包比对</text>
  <line x1="360" y1="90" x2="400" y2="67" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="360" y1="118" x2="400" y2="119" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="360" y1="150" x2="400" y2="171" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="400" y="46" width="304" height="42" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="414" y="72" font-size="10.5" fill="var(--ink)">worker · 指纹变 → 重建</text>
  <rect x="400" y="98" width="304" height="42" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="414" y="124" font-size="10.5" fill="var(--ink)">web · 指纹没变 → 缓存命中（秒过）</text>
  <rect x="400" y="150" width="304" height="42" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="414" y="176" font-size="10.5" fill="var(--ink)">shared · 没变 → 命中</text>
  <text x="360" y="216" font-size="10.5" text-anchor="middle" fill="var(--muted)">远端缓存：团队成员间共享构建结果 —— 几十包的大仓 CI 也能快</text>
</svg>

<h2>每个工作区里有什么</h2>
<p>最后给你一张「高频目录速查表」，后面的课会反复回到这些位置：</p>

<table class="t">
  <tr><th>位置</th><th>放什么</th></tr>
  <tr><td class="mono">web/src/pages</td><td>Next.js 页面 + API 路由（含 <code>api/public</code> 公共 REST、<code>api/trpc</code>）</td></tr>
  <tr><td class="mono">web/src/server/api</td><td>tRPC 的 root 路由、context、中间件（第 21 课）</td></tr>
  <tr><td class="mono">web/src/features</td><td>按功能切分的「纵切片」目录（traces、evals、prompts…约几十个）</td></tr>
  <tr><td class="mono">worker/src/queues</td><td>各个 BullMQ 队列的消费者（ingestion、eval、export…）</td></tr>
  <tr><td class="mono">worker/src/services</td><td>核心服务（IngestionService、ClickhouseWriter）</td></tr>
  <tr><td class="mono">packages/shared/src/domain</td><td>领域模型（traces/observations/scores…）</td></tr>
  <tr><td class="mono">packages/shared/src/server</td><td>仓储层、ClickHouse/Redis/S3 客户端、队列契约</td></tr>
  <tr><td class="mono">packages/shared/prisma</td><td>Postgres schema 与迁移</td></tr>
  <tr><td class="mono">packages/shared/clickhouse</td><td>ClickHouse 迁移（宽事件表）</td></tr>
</table>

<p>表里没列、但值得单独一提的是 <code>fern/</code> 和 <code>generated/</code>。Langfuse 的公共 REST API 不是手写的，而是先在 <code>fern/</code> 里用
<strong>Fern</strong> 把「有哪些端点、收什么参数、返回什么」<strong>声明</strong>出来，再自动<strong>生成</strong> <code>generated/</code> 下的 API 客户端代码。
所以 <code>generated/</code> 是<strong>构建产物，绝不能手改</strong>——改了下次生成就被覆盖。这也是为什么改公共 API 时要同步更新 <code>fern/</code> 源（第 27 课）。
这种「契约先行、代码生成」的做法，保证了 API 文档、服务端、各语言 SDK 三者始终对得上。带着这张全景地图，下一课我们就深入支撑这一切的<strong>双存储</strong>：为什么偏要 Postgres 加 ClickHouse 一起上。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么用 monorepo + 窄腰，而不是把 web/worker/shared 拆成三个独立仓库（polyrepo）？</strong> 因为 web 和 worker 高度共享领域模型与队列契约，
  如果分仓，每次改一个数据结构就要<strong>跨仓发版、对版本</strong>，极易出现「web 以为字段叫 A、worker 还在用 B」的漂移。monorepo 让三者<strong>原子地一起改</strong>——
  一个 PR 同时改 shared 的契约和两边的用法，CI 一起验。代价是仓库更大、构建工具（Turbo）更复杂，  但对一个契约高度耦合的系统，这笔账划算。换个角度说：分仓省的是「单仓的复杂度」，monorepo 省的是「跨仓协调的复杂度」——而后者往往才是真正拖慢团队的那个。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>Langfuse 是 <strong>pnpm + Turbo 的 monorepo</strong>：<code>web</code>（门店）、<code>worker</code>（后场车间）两个运行时 + <code>packages/shared</code>（中央仓库）+ <code>ee</code>。</li>
    <li><strong>窄腰</strong>：依赖严格单向 <code>web/worker/ee → shared</code>，而 <code>shared</code> 谁都不依赖；契约（领域模型、队列）集中在 shared。</li>
    <li><strong>Turbo</strong> 用任务依赖图（<code>build</code> 依赖 <code>db:generate</code> + <code>^build</code>）+ 缓存，让大仓也能快速、增量构建。</li>
    <li>记住高频目录：<code>web/src/{pages,server,features}</code>、<code>worker/src/{queues,services}</code>、<code>packages/shared/src/{domain,server}</code>——这是后面查代码的速查表。</li>
    <li>选 monorepo 是为了让契约高度耦合的 web/worker/shared 能<strong>原子地一起改</strong>，避免跨仓版本漂移与协调成本。</li>
  </ul>
</div>
""")

_EN4.append(r"""
<p class="lead">
The first three lessons covered "what the data looks like"; this one switches axes: <strong>where the code lives</strong>. Langfuse
is a <strong>monorepo</strong> (one repo, many projects) — everything sits in the single <code>langfuse/langfuse</code> repo, split
internally into a few purpose-built "workspaces". Hold this map in mind and whenever a later lesson says "open
<code>web/src/...</code>" or "this logic is in <code>worker</code>", you'll instantly know where it is and why.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Think of the repo as <strong>one big shopping mall</strong>: the whole building is <strong>one monorepo</strong> housing a few
  independent shops — <strong>web</strong> is the customer-facing <strong>storefront</strong> (busy, fast, always open),
  <strong>worker</strong> is the back-of-house <strong>workshop</strong> (heads-down heavy lifting, can queue and take its time). And
  <strong>packages/shared</strong> is the <strong>central warehouse</strong>: every shop draws its goods (domain models, DB access,
  queue contracts) from here, but the warehouse <strong>never depends back</strong> on any shop. All under <strong>one roof</strong>,
  sharing utilities (build tools), yet cleanly bounded and independently run. Grab this "floor directory" before you wander the mall
  and you won't get lost no matter which shop you visit.
</div>
""")

_EN4.append(r"""
<div class="fig">
<svg viewBox="0 0 720 320" role="img" aria-label="Top-level dirs of the Langfuse repo: web, worker, packages/shared, ee, fern, generated and their roles">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">langfuse/langfuse top-level map</text>
  <rect x="40" y="40" width="200" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="140" y="64" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">web/</text>
  <text x="140" y="83" text-anchor="middle" font-size="9.5" fill="var(--muted)">Next.js app</text>
  <text x="140" y="100" text-anchor="middle" font-size="9.5" fill="var(--muted)">UI · tRPC · public REST API</text>
  <rect x="260" y="40" width="200" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="360" y="64" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">worker/</text>
  <text x="360" y="83" text-anchor="middle" font-size="9.5" fill="var(--muted)">BullMQ queue consumer</text>
  <text x="360" y="100" text-anchor="middle" font-size="9.5" fill="var(--muted)">ingest·eval·export·delete…</text>
  <rect x="480" y="40" width="200" height="74" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="580" y="64" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">ee/</text>
  <text x="580" y="83" text-anchor="middle" font-size="9.5" fill="var(--muted)">enterprise features</text>
  <text x="580" y="100" text-anchor="middle" font-size="9.5" fill="var(--muted)">license check</text>
  <rect x="150" y="150" width="420" height="78" rx="11" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2"/>
  <text x="360" y="174" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--purple)">packages/shared/ · shared core (narrow waist)</text>
  <text x="360" y="194" text-anchor="middle" font-size="9.5" fill="var(--muted)">domain models · server repos/CH/queues · prisma schema · clickhouse migrations</text>
  <text x="360" y="212" text-anchor="middle" font-size="9.5" fill="var(--muted)">used by web & worker; depends on neither</text>
  <line x1="140" y1="114" x2="300" y2="148" stroke="var(--purple)" stroke-width="1.6"/><polygon points="300,148 289,146 293,154" fill="var(--purple)"/>
  <line x1="360" y1="114" x2="360" y2="148" stroke="var(--purple)" stroke-width="1.6"/><polygon points="360,148 355,138 365,138" fill="var(--purple)"/>
  <line x1="580" y1="114" x2="420" y2="148" stroke="var(--purple)" stroke-width="1.6"/><polygon points="420,148 431,146 427,154" fill="var(--purple)"/>
  <rect x="40" y="252" width="320" height="50" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="200" y="272" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">fern/ · public API contract</text>
  <text x="200" y="290" text-anchor="middle" font-size="9.5" fill="var(--muted)">describes the REST API; generates generated/ clients</text>
  <rect x="380" y="252" width="300" height="50" rx="10" fill="var(--panel)" stroke="var(--line)"/>
  <text x="530" y="272" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">generated/ · auto-generated (don't edit)</text>
  <text x="530" y="290" text-anchor="middle" font-size="9.5" fill="var(--muted)">API clients produced by Fern</text>
</svg>
<div class="figcap"><b>Just a few top-level blocks</b>: <b>web</b> (storefront) and <b>worker</b> (workshop) are two runtime containers, both depending up on <b>packages/shared</b> (central warehouse / narrow waist); <b>ee</b> holds enterprise features used by web; <b>fern</b> defines the public API contract and generates the <b>generated</b> clients. Remember this and every "where is file X" question has a coordinate system.</div>
</div>

<p>Unpacking what each runtime actually does makes it tangible. <strong>web</strong> is the Next.js app you open in your browser; it does
three things: render the <strong>UI</strong>, serve that UI a type-safe internal API (<strong>tRPC</strong>, L21), and serve external
SDKs a <strong>public REST API</strong> (<code>web/src/pages/api/public</code>, L27) — the ingestion entry point lives here.
<strong>worker</strong> is a headless background process that subscribes to dozens of <strong>BullMQ queues</strong> and takes on all
the <strong>heavy, slow, retryable</strong> work: merge ingested events into ClickHouse, run LLM evals, export data, delete projects…
(covered from Part 3 on). In a line: <strong>web does "fast in, fast out", worker does "heads-down grind"</strong>, decoupled by a
Redis queue in the middle — exactly the through-line of the next lesson ("dual store") and Part 3 ("the ingestion path").</p>

<h2>One repo, four workspaces</h2>
<p>Langfuse uses <strong>pnpm workspaces</strong> to slice one repo into independently buildable packages. The root
<code>pnpm-workspace.yaml</code> lists them line by line:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">pnpm-workspace.yaml</span><span class="ln">workspaces</span></div>
  <pre class="code">packages:
  - <span class="st">"web"</span>          <span class="cm"># Next.js app (UI + tRPC + public REST API)</span>
  - <span class="st">"worker"</span>       <span class="cm"># queue consumer, background processing</span>
  - <span class="st">"packages/**"</span>  <span class="cm"># shared packages, mainly packages/shared</span>
  - <span class="st">"ee"</span>           <span class="cm"># enterprise features</span></pre>
</div>

<p>Under <code>packages/**</code> there's more than just <code>shared</code> — also "tooling config" packages like
<code>config-eslint</code>, <code>config-typescript</code>, <code>eslint-plugin</code>; but the real business <strong>shared core is
<code>packages/shared</code></strong> — the central warehouse in the figure. Why split into workspaces instead of one big folder?
Because each package can then <strong>declare deps, build and test independently</strong>, and pnpm <strong>symlinks</strong> them so
web can simply
<code>import ... from "@langfuse/shared"</code> against the latest code with no publishing step. This hugely helps the dev experience:
change a type in <code>packages/shared</code> and the editors in <code>web</code> and <code>worker</code> <strong>light up red
immediately</strong> showing what must follow — surfacing the impact of a "contract change" at <strong>coding time</strong> rather than
at runtime.</p>
""")

_EN4.append(r"""
<h2>Dependency direction: why a "narrow waist"</h2>
<p>The four workspaces don't reference each other freely — there's a <strong>strictly one-way</strong> dependency rule (written in
<code>.agents/AGENTS.md</code>):</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">.agents/AGENTS.md</span><span class="ln">Dependency direction</span></div>
  <pre class="code">- <span class="nb">web</span>    -> @langfuse/shared, @langfuse/ee
- <span class="nb">worker</span> -> @langfuse/shared
- <span class="nb">ee</span>     -> @langfuse/shared
- <span class="nb">@langfuse/shared</span> -> <span class="kw">no imports from</span> web, worker, or ee</pre>
</div>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="web, worker and ee all depend one-way on shared; shared depends on none, forming a narrow waist">
  <text x="360" y="24" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">narrow waist: every arrow points to shared, none come back</text>
  <rect x="60" y="50" width="150" height="48" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="135" y="79" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">web</text>
  <rect x="285" y="50" width="150" height="48" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="79" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">worker</text>
  <rect x="510" y="50" width="150" height="48" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="585" y="79" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">ee</text>
  <rect x="210" y="168" width="300" height="56" rx="12" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2.5"/>
  <text x="360" y="192" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--purple)">packages/shared</text>
  <text x="360" y="210" text-anchor="middle" font-size="9.5" fill="var(--muted)">domain · repositories · queue contracts · DB access</text>
  <line x1="135" y1="98" x2="285" y2="166" stroke="var(--faint)" stroke-width="1.8"/><polygon points="285,166 273,162 277,172" fill="var(--faint)"/>
  <line x1="360" y1="98" x2="360" y2="166" stroke="var(--faint)" stroke-width="1.8"/><polygon points="360,166 355,156 365,156" fill="var(--faint)"/>
  <line x1="585" y1="98" x2="435" y2="166" stroke="var(--faint)" stroke-width="1.8"/><polygon points="435,166 447,162 443,172" fill="var(--faint)"/>
  <text x="360" y="244" text-anchor="middle" font-size="10" fill="var(--purple)">shared depends on none above → it's the foundation, not a consumer</text>
</svg>
<div class="figcap"><b>The "narrow waist"</b>: collect what everyone needs into a thin layer that <b>nothing depends on backwards</b>. web/worker/ee are the top of an hourglass, shared is the thin "waist", and below is the database. The payoff: the two containers evolve and deploy independently while sharing one set of domain models and queue contracts, so <b>the contract can't drift</b>.</div>
</div>

<p>Why does this discipline matter? Because web and worker are <strong>two very different workloads</strong>: web faces users, wants
low latency, must restart anytime; worker chews heavy jobs, must be retryable, scales by queue. Let them <strong>import each other
directly</strong> and changing one can entangle the other, binding their deployments. Collecting shared things into shared and
allowing <strong>only downward dependencies</strong> erects a clean <strong>contract wall</strong> between the two containers: what
goes through queues, what the DB tables look like — all defined in one place (queue payloads, for instance, belong to
<code>packages/shared/src/server/queues.ts</code>). Both sides work to the same contract without stepping on each other.</p>

<p>A concrete bug this rule <strong>blocks</strong>: imagine no narrow waist, and worker lazily <code>import</code>s a utility function
from web. One day web refactors that function to change the UI and tweaks its parameters — and <strong>worker breaks without anyone
knowing</strong>, maybe surfacing only as a production ingestion error. Under the narrow-waist rule, worker simply <strong>cannot</strong>
depend on web; their only "shared language" is the explicit contract in shared. Want to share logic? <strong>Sink it down</strong> into
shared so it becomes a contract-bound first-class citizen, not something borrowed quietly from next door. <strong>"Dependencies only go
down" is really using the compiler to block implicit cross-container coupling.</strong></p>

<h2>How Turbo orchestrates them</h2>
<p>Build, test and lint across workspaces are orchestrated by <strong>Turbo</strong> (root <code>turbo.json</code>). Its two most
useful tricks are the <strong>task dependency graph</strong> and <strong>caching</strong>:</p>

<div class="flow">
  <div class="node"><div class="nt">db:generate</div><div class="nd">generate Prisma client first</div></div>
  <div class="arrow">→</div>
  <div class="node"><div class="nt">^build</div><div class="nd">build upstream deps first</div></div>
  <div class="arrow">→</div>
  <div class="node hl"><div class="nt">build</div><div class="nd">then build this package</div></div>
  <div class="arrow">⚡</div>
  <div class="node"><div class="nt">cache</div><div class="nd">unchanged → cache hit</div></div>
</div>

<p>Look at the <code>build</code> task in <code>turbo.json</code>: <code>"dependsOn": ["db:generate", "^build"]</code> — meaning "before
building any package, generate the DB client and first build the packages it depends on (<code>^</code> = upstream deps)". So a single
<code>pnpm build</code> lets Turbo compute the right order, parallelize what it can, and <strong>skip</strong> what's cached
(<code>"cache": true</code>). That's why, in a big repo of dozens of packages, changing one line doesn't force a full rebuild.</p>

<p>Put the narrow waist and Turbo together and watch a <strong>concrete chain reaction</strong>: say you add a field to the trace. You
edit one spot in <code>packages/shared/prisma/schema.prisma</code> and one in <code>domain/traces.ts</code> — one
<code>db:generate</code> regenerates the Prisma client and <strong>both web and worker immediately see the new field</strong>, because
both pull types from the same <code>@langfuse/shared</code>. The whole thing lands in <strong>one PR</strong>, verified together by CI.
Split into three repos and this same change needs three releases, three dependency bumps, and a prayer that versions line up — that's
the practical meaning of "change atomically".</p>

<div class="cols">
  <div class="col"><h4>🧩 polyrepo (split)</h4><p>web/worker/shared each a repo. Change a shared structure → cross-repo releases, version juggling, easy drift. Upside: smaller, more independent repos.</p></div>
  <div class="col"><h4>📦 monorepo (Langfuse's choice)</h4><p>one repo holds it all. A shared change is one atomic PR, verified together by CI. Cost: bigger repo, Turbo to manage build caching.</p></div>
</div>

<p>Caching is especially valuable for <strong>CI</strong>. In a dozens-of-packages repo, rebuilding + linting + testing everything on
every PR would make CI unusably slow. Turbo computes a <strong>fingerprint of each task's inputs</strong> (source + deps + config) and,
if the fingerprint is unchanged, <strong>reuses last time's output</strong> and skips the whole step. So editing one file in
<code>worker</code> lets the unaffected <code>web</code> builds/tests <strong>hit cache and pass instantly</strong>. With a remote
cache, teammates even share build results. That's the secret to keeping CI fast in a big repo — and the <strong>engineering
precondition</strong> that makes "use a monorepo" viable: without good caching, monorepo build cost scares everyone off.</p>

<svg viewBox="0 0 720 230" role="img" aria-label="Turbo caching works by fingerprint: change one file in worker and Turbo computes a fingerprint per package task (source plus dependencies plus config) and compares per package; worker's fingerprint changed so it rebuilds, web's is unchanged so it hits the cache and skips instantly, shared unchanged also hits; a remote cache even shares build results across teammates">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">Turbo cache: fingerprint each task's inputs, skip the whole thing if unchanged</text>
  <rect x="16" y="72" width="150" height="46" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="91" y="92" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">change worker</text>
  <text x="91" y="108" font-size="9.5" text-anchor="middle" fill="var(--muted)">one file</text>
  <line x1="166" y1="95" x2="200" y2="95" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="200" y="52" width="160" height="120" rx="10" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="280" y="78" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Turbo fingerprints</text>
  <text x="280" y="102" font-size="9.5" text-anchor="middle" fill="var(--ink)">= source + deps</text>
  <text x="280" y="118" font-size="9.5" text-anchor="middle" fill="var(--ink)">+ config</text>
  <text x="280" y="146" font-size="9.5" text-anchor="middle" fill="var(--muted)">compared per package</text>
  <line x1="360" y1="90" x2="400" y2="67" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="360" y1="118" x2="400" y2="119" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="360" y1="150" x2="400" y2="171" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="400" y="46" width="304" height="42" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="414" y="72" font-size="10.5" fill="var(--ink)">worker · fingerprint changed → rebuild</text>
  <rect x="400" y="98" width="304" height="42" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="414" y="124" font-size="10.5" fill="var(--ink)">web · unchanged → cache hit (instant)</text>
  <rect x="400" y="150" width="304" height="42" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="414" y="176" font-size="10.5" fill="var(--ink)">shared · unchanged → hit</text>
  <text x="360" y="216" font-size="10.5" text-anchor="middle" fill="var(--muted)">remote cache: share build results across teammates — even a dozens-of-packages repo keeps CI fast</text>
</svg>

<h2>What's inside each workspace</h2>
<p>Finally, a "hot directory cheat-sheet" — later lessons return to these spots again and again:</p>

<table class="t">
  <tr><th>Location</th><th>What's there</th></tr>
  <tr><td class="mono">web/src/pages</td><td>Next.js pages + API routes (incl. <code>api/public</code> REST, <code>api/trpc</code>)</td></tr>
  <tr><td class="mono">web/src/server/api</td><td>tRPC root router, context, middleware (L21)</td></tr>
  <tr><td class="mono">web/src/features</td><td>feature "vertical slices" (traces, evals, prompts… dozens)</td></tr>
  <tr><td class="mono">worker/src/queues</td><td>BullMQ queue consumers (ingestion, eval, export…)</td></tr>
  <tr><td class="mono">worker/src/services</td><td>core services (IngestionService, ClickhouseWriter)</td></tr>
  <tr><td class="mono">packages/shared/src/domain</td><td>domain models (traces/observations/scores…)</td></tr>
  <tr><td class="mono">packages/shared/src/server</td><td>repositories, ClickHouse/Redis/S3 clients, queue contracts</td></tr>
  <tr><td class="mono">packages/shared/prisma</td><td>Postgres schema & migrations</td></tr>
  <tr><td class="mono">packages/shared/clickhouse</td><td>ClickHouse migrations (wide-event tables)</td></tr>
</table>

<p>Not in the table but worth a separate mention: <code>fern/</code> and <code>generated/</code>. Langfuse's public REST API isn't
hand-written — it's first <strong>declared</strong> in <code>fern/</code> with <strong>Fern</strong> ("which endpoints, what params,
what responses"), then API client code is <strong>generated</strong> into <code>generated/</code>. So <code>generated/</code> is a
<strong>build artifact you must never hand-edit</strong> — edits get overwritten on the next generation. That's why changing the
public API means updating the <code>fern/</code> sources too (L27). This "contract-first, code-generated" approach keeps the API docs,
the server, and the per-language SDKs always in sync.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why a monorepo + narrow waist instead of three separate repos (polyrepo) for web/worker/shared?</strong> Because web and
  worker share domain models and queue contracts heavily; split into repos and every data-structure change means
  <strong>cross-repo releases and version juggling</strong>, inviting drift ("web thinks the field is A, worker still uses B"). A
  monorepo lets all three <strong>change atomically</strong> — one PR edits the shared contract and both usages, and CI verifies them
  together. The cost is a bigger repo and a more complex build tool (Turbo), but for a tightly contract-coupled system, the trade
  wins. Put differently: polyrepo saves "single-repo complexity", monorepo saves "cross-repo coordination complexity" — and the latter
  is usually what actually slows a team down.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>Langfuse is a <strong>pnpm + Turbo monorepo</strong>: <code>web</code> (storefront), <code>worker</code> (workshop) two runtimes + <code>packages/shared</code> (central warehouse) + <code>ee</code>.</li>
    <li><strong>Narrow waist</strong>: dependencies are strictly one-way <code>web/worker/ee → shared</code>, and <code>shared</code> depends on none; contracts (domain models, queues) live in shared.</li>
    <li><strong>Turbo</strong> uses a task graph (<code>build</code> depends on <code>db:generate</code> + <code>^build</code>) + caching, so even a big repo builds fast and incrementally.</li>
    <li>Memorize the hot dirs: <code>web/src/{pages,server,features}</code>, <code>worker/src/{queues,services}</code>, <code>packages/shared/src/{domain,server}</code>.</li>
    <li>Monorepo is chosen so the contract-coupled web/worker/shared can <strong>change atomically</strong>, avoiding cross-repo version drift.</li>
  </ul>
</div>
""")

LESSON_04 = {"zh": "\n".join(_ZH4), "en": "\n".join(_EN4)}


# ══════════════════════════════════════════════════════════════════════
# L05 · 一条 trace 的一生·鸟瞰 / Life of a trace (bird's-eye)
# ══════════════════════════════════════════════════════════════════════
_ZH5 = []
_EN5 = []

_ZH5.append(r"""
<p class="lead">
第一部分快收尾了。你已经知道<strong>数据长什么样</strong>（trace/observation/score）、<strong>代码住在哪</strong>（monorepo 与窄腰）、
背后的<strong>设计哲学</strong>（宽事件）。这一课把它们<strong>串成一条线</strong>：跟着<strong>一条具体的 trace</strong>，从你应用里 <code>langfuse.trace(...)</code> 那一刻起，
一路走到它出现在 UI 列表里、被你点开、甚至被自动评分。这是一支「<strong>预告片</strong>」——每一段路都标好了由后面哪一课详细展开，看完你就有了整张地图的<strong>行车路线</strong>。
换句话说，前四课是把零件一个个拆给你看，这一课是把它们装回去、发动一次，让你看见数据<strong>真正流动起来</strong>的样子——有了这个动态全景，再去逐课深挖每个零件，就不会只见树木不见森林。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把一条 trace 的一生想成<strong>寄一件快递</strong>：你在家<strong>下单封箱</strong>（SDK 里创建 trace/observation）；快递员<strong>上门收件</strong>，扫码入袋
  （公共 API 收下事件、快速入队）；包裹进了<strong>分拣中心</strong>排队，由后台<strong>分拣处理</strong>（worker 从队列取出、合并、算运费=成本）；
  然后<strong>上架入库</strong>（写进 ClickHouse）；最后你打开手机<strong>查物流</strong>（在 UI 里看到这条 trace）。关键是——<strong>下单那一刻并不等于已入库</strong>，
  中间隔着收件、分拣、上架几步，所以会有<strong>短暂的处理延迟</strong>。这正是 Langfuse 摄取「异步」的本质。
</div>
""")

_ZH5.append(r"""
<div class="fig">
<svg viewBox="0 0 720 360" role="img" aria-label="一条 trace 从 SDK 经 API、Redis 队列、worker 写入 ClickHouse，再由 repository、tRPC 回到 UI">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">写入：SDK → … → ClickHouse（上行）　读取：ClickHouse → … → UI（下行）</text>
  <rect x="20" y="44" width="116" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="78" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">SDK / OTel</text><text x="78" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">你的应用</text>
  <rect x="164" y="44" width="116" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="222" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">公共 API</text><text x="222" y="80" text-anchor="middle" font-size="9" fill="var(--accent-ink)">web · 校验入队</text>
  <rect x="308" y="44" width="104" height="46" rx="9" fill="var(--red-soft)" stroke="var(--red)"/><text x="360" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">Redis 队列</text><text x="360" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">BullMQ</text>
  <rect x="440" y="44" width="116" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="498" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">worker</text><text x="498" y="80" text-anchor="middle" font-size="9" fill="var(--accent-ink)">合并·算成本</text>
  <rect x="584" y="44" width="116" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="642" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="642" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">宽事件表</text>
  <line x1="136" y1="67" x2="162" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="162,67 153,62 153,72" fill="var(--faint)"/><text x="149" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L12</text>
  <line x1="280" y1="67" x2="306" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="306,67 297,62 297,72" fill="var(--faint)"/><text x="293" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L14</text>
  <line x1="412" y1="67" x2="438" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="438,67 429,62 429,72" fill="var(--faint)"/><text x="425" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L15</text>
  <line x1="556" y1="67" x2="582" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="582,67 573,62 573,72" fill="var(--faint)"/><text x="569" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L17</text>
  <rect x="440" y="128" width="116" height="40" rx="9" fill="var(--panel)" stroke="var(--line)"/><text x="498" y="146" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">S3 / blob</text><text x="498" y="160" text-anchor="middle" font-size="8.5" fill="var(--muted)">事件日志·媒体 L19</text>
  <line x1="498" y1="90" x2="498" y2="126" stroke="var(--faint)" stroke-width="1.6" stroke-dasharray="4 3"/><polygon points="498,126 493,117 503,117" fill="var(--faint)"/>
  <line x1="642" y1="90" x2="642" y2="214" stroke="var(--purple)" stroke-width="1.8"/><polygon points="642,214 637,205 647,205" fill="var(--purple)"/>
  <text x="360" y="200" text-anchor="middle" font-size="11" font-weight="700" fill="var(--muted)">— — — — — 数据已落库，下面是读取 — — — — —</text>
  <rect x="584" y="218" width="116" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="642" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="642" y="254" text-anchor="middle" font-size="9" fill="var(--muted)">同一张宽表</text>
  <rect x="430" y="218" width="130" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="495" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">repository</text><text x="495" y="254" text-anchor="middle" font-size="9" fill="var(--accent-ink)">拼 SQL 查询 L22</text>
  <rect x="270" y="218" width="130" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="335" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">tRPC</text><text x="335" y="254" text-anchor="middle" font-size="9" fill="var(--accent-ink)">类型安全 API L21</text>
  <rect x="110" y="218" width="130" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="175" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">UI</text><text x="175" y="254" text-anchor="middle" font-size="9" fill="var(--muted)">列表·详情 L20·25</text>
  <line x1="584" y1="241" x2="562" y2="241" stroke="var(--faint)" stroke-width="2"/><polygon points="562,241 571,236 571,246" fill="var(--faint)"/>
  <line x1="430" y1="241" x2="402" y2="241" stroke="var(--faint)" stroke-width="2"/><polygon points="402,241 411,236 411,246" fill="var(--faint)"/>
  <line x1="270" y1="241" x2="242" y2="241" stroke="var(--faint)" stroke-width="2"/><polygon points="242,241 251,236 251,246" fill="var(--faint)"/>
  <text x="360" y="312" text-anchor="middle" font-size="10" fill="var(--faint)">上行写入异步（秒级延迟）· 下行读取实时（用户点一下就查）</text>
</svg>
<div class="figcap"><b>一条 trace 的完整旅程</b>：上半是<b>写入链路</b>（SDK→API→Redis→worker→ClickHouse，旁挂 S3），每段标了对应课号（第 12–19 课）；下半是<b>读取链路</b>（ClickHouse→repository→tRPC→UI，第 20–27 课）。两条链路在 ClickHouse 这张宽表上「碰头」：写入把数据放进去，读取把它取出来。</div>
</div>

<h2>上行 · 写：从 SDK 到 ClickHouse</h2>
<p>先看包裹「寄出到入库」的全过程。它被刻意设计成<strong>异步</strong>的——API 只负责飞快地收下并入队，真正的重活交给 worker 慢慢做：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SDK 创建事件（第 6 课）</h4><p>你的应用调用 SDK 或发 OTel span，生成 trace-create / observation-create / score-create 等<strong>事件</strong>。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>公共 API 收件入队（第 12·14 课）</h4><p><code>web/src/pages/api/public/ingestion.ts</code> 鉴权、用 Zod 校验一批事件，然后<strong>快速塞进 Redis 队列</strong>就返回——不等处理完。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>worker 合并聚合（第 15 课）</h4><p><code>IngestionService</code> 从队列取出事件，<strong>从 S3 取这条记录的历史事件</strong>合并（同一个 observation 的多次 update 会合成一条），再决定最终长什么样。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>算 token 与成本（第 16 课）</h4><p>按模型名匹配定价表，把没上报的 usage/cost <strong>兜底算出来</strong>（还记得第 3 课的 provided vs computed 吗）。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>ClickhouseWriter 批量写（第 17 课）</h4><p>把处理好的记录<strong>攒成批</strong>，一次性写进 ClickHouse 的 traces/observations/scores 表（ReplacingMergeTree 负责「同 id 后写覆盖先写」）。</p></div></div>
</div>

<p>这条链路里，<strong>S3 扮演了「事件原始底稿」的角色</strong>：每个进来的事件先落 S3，worker 合并时再回 S3 取历史。这样即使处理出错也能<strong>重放</strong>，
而且让「同一条 observation 的多次更新」能被正确合并——这些细节在第 15–17 课会逐一拆开。现在你只需记住这条主干：<strong>收件 → 入队 → 合并 → 算钱 → 入库</strong>。</p>

<p>这里要特别点出第 3 步「<strong>合并</strong>」为什么不可省。原因是：SDK 上报一个 observation 往往<strong>不是一次性</strong>的。比如一次 LLM 调用，SDK 可能先发一个
「observation-create」说「我开始了，模型是 gpt-4o」，等调用返回后再发一个「observation-update」补上「输出是 X、用了 1240 token」。这两条事件<strong>分别到达</strong>，
worker 必须把它们<strong>合并成同一条最终记录</strong>。这就是为什么要回 S3 取「这个 id 的历史事件」——把先后到达的碎片拼成完整的一行。理解了这一点，你就明白第 3 课说的
「observation 靠 parentObservationId 乱序到达也没关系」是怎么在摄取里真正实现的：<strong>事件可以分多次、乱序到，worker 负责把它们收敛成一致的最终态。</strong></p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="同一个 observation 的多次事件乱序到达：observation-create(开始,模型gpt-4o)与observation-update(输出X,1240token)分别到达，worker 回S3取这个id的历史事件，按id分组合并、冲突以更晚timestamp为准，收敛成一条最终ClickHouse行">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">分多次、乱序到达 → worker 收敛成一行最终态</text>
  <rect x="24" y="44" width="180" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="60" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--ink)">事件1 observation-create</text><text x="114" y="74" text-anchor="middle" font-size="6.5" fill="var(--muted)">{id:obs-42, 开始, model:gpt-4o}</text>
  <rect x="24" y="96" width="180" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="112" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--ink)">事件2 observation-update</text><text x="114" y="126" text-anchor="middle" font-size="6.2" fill="var(--muted)">{id:obs-42, output:X, 1240 token}</text>
  <text x="114" y="156" text-anchor="middle" font-size="6.5" fill="var(--faint)">两条分别到达、可能乱序</text>
  <rect x="266" y="62" width="180" height="74" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="356" y="82" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">worker 合并</text><text x="356" y="99" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">回 S3 取 id=obs-42 历史</text><text x="356" y="113" text-anchor="middle" font-size="6.5" fill="var(--muted)">按 id 分组、字段取有值方</text><text x="356" y="127" text-anchor="middle" font-size="6.5" fill="var(--muted)">冲突以更晚 timestamp 为准</text>
  <rect x="508" y="68" width="188" height="62" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="602" y="88" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">一条最终行</text><text x="602" y="105" text-anchor="middle" font-size="6.5" fill="var(--muted)">obs-42：gpt-4o + output:X</text><text x="602" y="119" text-anchor="middle" font-size="6.5" fill="var(--muted)">+ 1240 token，写进 ClickHouse</text>
  <line x1="204" y1="64" x2="264" y2="88" stroke="var(--blue)" stroke-width="1.3"/><polygon points="264,88 255,85 256,93" fill="var(--blue)"/><line x1="204" y1="116" x2="264" y2="100" stroke="var(--blue)" stroke-width="1.3"/><polygon points="264,100 255,100 258,108" fill="var(--blue)"/>
  <line x1="446" y1="99" x2="506" y2="99" stroke="var(--accent)" stroke-width="1.4"/><polygon points="506,99 497,95 497,103" fill="var(--accent)"/>
  <text x="360" y="184" text-anchor="middle" font-size="8" fill="var(--faint)">这正是第3课「乱序到达也没关系」在摄取里的实现，也是第13/15课要细讲的合并逻辑</text>
</svg>
<div class="figcap"><b>乱序事件 → 一条最终态</b>：同一 observation 的 create/update 分多次、可能乱序到达；worker 回 S3 取该 id 的历史事件，按 id 分组合并（冲突以更晚 <code>timestamp</code> 为准），收敛成一条最终行写入 ClickHouse。细节见第 13·15 课。</div>
</div>
""")

_ZH5.append(r"""
<h2>下行 · 读：从 UI 回到 ClickHouse</h2>
<p>数据落库后，你在浏览器里看到它，走的是另一条更<strong>实时</strong>的链路——你点一下，它就去查：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>UI 发起查询（第 20 课）</h4><p>你打开 trace 列表页，前端通过 <strong>tRPC</strong> 的 hook（如 <code>api.traces.all.useQuery</code>）发起一次类型安全的请求。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>tRPC 鉴权分派（第 21 课）</h4><p>请求进 <code>web/src/server/api</code>，中间件先校验「你属于这个项目吗」（RBAC），再分派到对应的路由处理函数。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>仓储层拼查询（第 22·23 课）</h4><p>路由调用 <code>packages/shared/src/server/repositories</code> 里的函数，把你的过滤条件翻译成 <strong>ClickHouse SQL</strong>（带时间窗口、只选需要的列）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>ClickHouse 返回，UI 渲染（第 24·25 课）</h4><p>列表页只取<strong>紧凑的窄字段</strong>（快）；你点开某条 trace 时，才去拉完整的 input/output 大字段并拼出观测树。</p></div></div>
</div>

<p>注意写入和读取在 ClickHouse 这张表上<strong>会师</strong>：写入链路负责把宽事件放进去，读取链路负责用各种姿势把它查出来。第 2 课说的「列表只读窄字段、详情才读大字段」，
正是在这条读取链路上落地的。</p>

<h2>为什么要把「收件」和「处理」分开</h2>
<p>这条链路最妙的一步，是 API「<strong>收下就返回</strong>」。它把整件事掰成了「快路」和「慢路」两半：</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="API 收下事件后毫秒级返回给应用（快路），同时把事件入队由 worker 在后台批量处理（慢路）">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">快路：API 毫秒级返回　慢路：worker 后台慢慢处理</text>
  <rect x="30" y="80" width="120" height="56" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="90" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">你的应用</text><text x="90" y="122" text-anchor="middle" font-size="9" fill="var(--muted)">等不起</text>
  <rect x="220" y="80" width="120" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="280" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">公共 API</text><text x="280" y="122" text-anchor="middle" font-size="9" fill="var(--accent-ink)">只校验+入队</text>
  <line x1="150" y1="96" x2="218" y2="96" stroke="var(--faint)" stroke-width="1.8"/><polygon points="218,96 209,91 209,101" fill="var(--faint)"/><text x="184" y="88" text-anchor="middle" font-size="8.5" fill="var(--faint)">事件</text>
  <line x1="218" y1="120" x2="152" y2="120" stroke="var(--accent)" stroke-width="2"/><polygon points="152,120 161,115 161,125" fill="var(--accent)"/><text x="185" y="138" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">毫秒级 200 OK（快路）</text>
  <rect x="410" y="80" width="110" height="56" rx="10" fill="var(--red-soft)" stroke="var(--red)"/><text x="465" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">Redis 队列</text><text x="465" y="122" text-anchor="middle" font-size="9" fill="var(--muted)">蓄水池</text>
  <rect x="580" y="80" width="110" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="635" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">worker ×N</text><text x="635" y="122" text-anchor="middle" font-size="9" fill="var(--accent-ink)">批量·可重试</text>
  <line x1="340" y1="108" x2="408" y2="108" stroke="var(--faint)" stroke-width="1.8"/><polygon points="408,108 399,103 399,113" fill="var(--faint)"/>
  <line x1="520" y1="108" x2="578" y2="108" stroke="var(--faint)" stroke-width="1.8"/><polygon points="578,108 569,103 569,113" fill="var(--faint)"/>
  <text x="465" y="170" text-anchor="middle" font-size="9.5" fill="var(--faint)">慢路：洪峰先在队列排队，worker 按自己节奏消费、扛不住就加机器</text>
</svg>
<div class="figcap"><b>一刀切开</b>：应用和 API 之间是<b>快路</b>（毫秒级返回，几乎不可能慢）；API 之后是<b>慢路</b>（入队 → worker 后台批量处理）。队列像蓄水池，洪峰来了先排队，worker 扛不住就横向加机器。</div>
</div>

<p>想想看：一个高流量的 LLM 应用，每秒可能产生成千上万条 observation。如果 API 必须<strong>同步地</strong>合并、算成本、写 ClickHouse 才返回，那么两件坏事会发生：
其一，你的应用每次调用都要<strong>多等</strong>这几百毫秒，平白被监控工具拖慢；其二，一旦 ClickHouse 抖动或洪峰打满，API 就会<strong>超时、甚至把错误反弹给你的业务</strong>。
把「收件」和「处理」一刀切开，API 就退化成一个极轻的「<strong>只管校验 + 入队</strong>」端点——它几乎不可能慢，也几乎不可能因为下游问题而连累你的应用。</p>

<p>队列则像一个<strong>蓄水池</strong>：洪峰来了先在队列里排队，worker 按自己的节奏<strong>批量</strong>消费，扛不住就<strong>加 worker</strong>（横向扩容）。
Langfuse 甚至把摄取队列分成<strong>主/次两条</strong>（第 14 课），把高吞吐的大项目和普通项目隔开，避免一个项目的洪峰拖垮所有人。
代价就是后面要说的那点延迟——但只要把 Δ 压到秒级，用户几乎无感。这也是为什么几乎所有高吞吐遥测系统（不只是 Langfuse）都长成这个样子：
<strong>轻量接收 + 异步处理 + 批量落库</strong>。看懂了这条主干，你就能预判后面第三部分每一课在解决什么问题。</p>

<h2>异步的代价：最终一致</h2>
<p>把上下行拼起来，有一个你必须心里有数的事实：<strong>从 SDK 发出，到 UI 能查到，中间隔着队列处理，有秒级延迟</strong>。这叫<strong>最终一致</strong>。</p>

<p>「最终一致」在实践中意味着什么？意味着你刚在应用里跑完一次调用、马上切到 Langfuse 界面刷新，<strong>可能还看不到它</strong>——再等一两秒、刷新一下，它就出现了。
这对绝大多数可观测场景完全够用：你是<strong>事后</strong>来排查、来看板、来评估的，差几秒无所谓。但它也提醒你两件事：第一，<strong>别拿 Langfuse 当强一致的业务数据库</strong>——
它是遥测系统，不保证「写完立刻可读」；第二，如果你写自动化测试去验证「埋点对不对」，要记得<strong>给摄取留出处理时间</strong>，否则会误判成「数据没上来」。
理解这条边界，你就不会对那点延迟感到意外，反而会欣赏它背后「<strong>永不拖累业务</strong>」的取舍。</p>

<div class="timeline">
  <div class="lane"><span class="lane-label">t0</span><span class="tslot now">SDK 发出事件</span><span class="tslot">API 入队（毫秒级返回）</span></div>
  <div class="lane"><span class="lane-label">t0 + Δ</span><span class="tslot span">worker 排队 → 合并 → 算成本 → 写 ClickHouse</span></div>
  <div class="lane"><span class="lane-label">t0 + Δ′</span><span class="tslot now">UI 才能查到这条 trace</span></div>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么宁可有这点延迟，也要异步？</strong> 因为摄取要扛<strong>极高的写入吞吐</strong>，而你的应用<strong>等不起</strong>。如果 API 同步地做完合并、算成本、写库才返回，
  你的每次 LLM 调用都会被 Langfuse 拖慢、还可能因为下游抖动而失败。异步把「收件」和「处理」解耦：API 永远<strong>毫秒级返回</strong>、几乎不可能拖累你的应用；
  worker 则能<strong>批量、可重试、按队列扩容</strong>地消化洪峰。代价就是那点处理延迟——而第 2 课提到的「保留近实时调试」原则，要求把这个 Δ 压到秒级，
  让可观测性依然「几乎实时」。<strong>用一点延迟，换一个永不拖累业务、又扛得住洪峰的摄取层。</strong>
这套「轻接收 + 异步处理」的取舍，会在第三部分被你反复看到——它不是某个模块的小聪明，而是贯穿整条摄取链路的指导思想。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点 · 也是第一部分小结</div>
  <ul>
    <li>一条 trace 的一生：<strong>SDK → 公共 API（入队）→ Redis → worker（合并·算成本）→ ClickHouse</strong>（写），再 <strong>UI → tRPC → repository → ClickHouse</strong>（读）。</li>
    <li><strong>写入异步</strong>（秒级延迟、最终一致，刚埋点要稍等才可见），<strong>读取实时</strong>；两条链路在 ClickHouse 宽表上会师。</li>
    <li><strong>S3</strong> 存事件原始底稿，支撑合并与重放（出错可重来）；<strong>Redis</strong> 队列解耦收件与处理、并能分主次隔离大项目。</li>
    <li>每一段路都对应后面一课：写入是第三部分（第 12–19 课），读取是第四部分（第 20–27 课）。</li>
    <li>第一部分到此结束：你已经有了<strong>数据模型 + 仓库地图 + 设计哲学 + 端到端链路</strong>这张总图，接下来就从第二部分的「前置基础」开始逐段深入。</li>
  </ul>
</div>
""")

_EN5.append(r"""
<p class="lead">
Part 1 is nearly done. You now know <strong>what the data looks like</strong> (trace/observation/score), <strong>where the code
lives</strong> (monorepo & narrow waist), and the <strong>design philosophy</strong> behind it (wide events). This lesson
<strong>strings them into one line</strong>: follow <strong>one concrete trace</strong> from the moment your app calls
<code>langfuse.trace(...)</code> all the way to it appearing in the UI list, being opened, even being auto-scored. It's a
<strong>trailer</strong> — each leg is tagged with the later lesson that covers it, so by the end you have the whole map's
<strong>route plan</strong>. Put differently, the first four lessons took the parts out one by one; this one puts them back and
fires the engine once, so you see the data <strong>actually flowing</strong> — with that dynamic panorama, digging into each part
lesson by lesson won't lose the forest for the trees.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Think of a trace's life as <strong>shipping a parcel</strong>: at home you <strong>place the order and seal the box</strong> (create
  trace/observation in the SDK); a courier <strong>picks it up</strong>, scans it into a bag (the public API accepts the events and
  quickly enqueues); the parcel queues in a <strong>sorting center</strong> and is <strong>processed in the back</strong> (the worker
  pulls from the queue, merges, computes "shipping cost" = cost); then it's <strong>shelved into the warehouse</strong> (written to
  ClickHouse); finally you open your phone to <strong>track it</strong> (see the trace in the UI). The key: <strong>placing the order
  is not the same as being shelved</strong> — pickup, sorting and shelving sit in between, so there's a <strong>brief processing
  delay</strong>. That's the essence of Langfuse's "async" ingestion.
</div>
""")

_EN5.append(r"""
<div class="fig">
<svg viewBox="0 0 720 360" role="img" aria-label="A trace flows from SDK through API, Redis queue, worker into ClickHouse, then back to the UI via repository and tRPC">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Write: SDK → … → ClickHouse (top)　Read: ClickHouse → … → UI (bottom)</text>
  <rect x="20" y="44" width="116" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="78" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">SDK / OTel</text><text x="78" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">your app</text>
  <rect x="164" y="44" width="116" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="222" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">public API</text><text x="222" y="80" text-anchor="middle" font-size="9" fill="var(--accent-ink)">web · validate+enqueue</text>
  <rect x="308" y="44" width="104" height="46" rx="9" fill="var(--red-soft)" stroke="var(--red)"/><text x="360" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">Redis queue</text><text x="360" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">BullMQ</text>
  <rect x="440" y="44" width="116" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="498" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">worker</text><text x="498" y="80" text-anchor="middle" font-size="9" fill="var(--accent-ink)">merge·cost</text>
  <rect x="584" y="44" width="116" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="642" y="64" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="642" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">wide-event tables</text>
  <line x1="136" y1="67" x2="162" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="162,67 153,62 153,72" fill="var(--faint)"/><text x="149" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L12</text>
  <line x1="280" y1="67" x2="306" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="306,67 297,62 297,72" fill="var(--faint)"/><text x="293" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L14</text>
  <line x1="412" y1="67" x2="438" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="438,67 429,62 429,72" fill="var(--faint)"/><text x="425" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L15</text>
  <line x1="556" y1="67" x2="582" y2="67" stroke="var(--faint)" stroke-width="2"/><polygon points="582,67 573,62 573,72" fill="var(--faint)"/><text x="569" y="38" text-anchor="middle" font-size="8.5" fill="var(--blue)">L17</text>
  <rect x="440" y="128" width="116" height="40" rx="9" fill="var(--panel)" stroke="var(--line)"/><text x="498" y="146" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">S3 / blob</text><text x="498" y="160" text-anchor="middle" font-size="8.5" fill="var(--muted)">event log·media L19</text>
  <line x1="498" y1="90" x2="498" y2="126" stroke="var(--faint)" stroke-width="1.6" stroke-dasharray="4 3"/><polygon points="498,126 493,117 503,117" fill="var(--faint)"/>
  <line x1="642" y1="90" x2="642" y2="214" stroke="var(--purple)" stroke-width="1.8"/><polygon points="642,214 637,205 647,205" fill="var(--purple)"/>
  <text x="360" y="200" text-anchor="middle" font-size="11" font-weight="700" fill="var(--muted)">— — — — — data is stored; below is reading — — — — —</text>
  <rect x="584" y="218" width="116" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="642" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="642" y="254" text-anchor="middle" font-size="9" fill="var(--muted)">same wide table</text>
  <rect x="430" y="218" width="130" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="495" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">repository</text><text x="495" y="254" text-anchor="middle" font-size="9" fill="var(--accent-ink)">build SQL L22</text>
  <rect x="270" y="218" width="130" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="335" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">tRPC</text><text x="335" y="254" text-anchor="middle" font-size="9" fill="var(--accent-ink)">type-safe API L21</text>
  <rect x="110" y="218" width="130" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="175" y="238" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">UI</text><text x="175" y="254" text-anchor="middle" font-size="9" fill="var(--muted)">list·detail L20·25</text>
  <line x1="584" y1="241" x2="562" y2="241" stroke="var(--faint)" stroke-width="2"/><polygon points="562,241 571,236 571,246" fill="var(--faint)"/>
  <line x1="430" y1="241" x2="402" y2="241" stroke="var(--faint)" stroke-width="2"/><polygon points="402,241 411,236 411,246" fill="var(--faint)"/>
  <line x1="270" y1="241" x2="242" y2="241" stroke="var(--faint)" stroke-width="2"/><polygon points="242,241 251,236 251,246" fill="var(--faint)"/>
  <text x="360" y="312" text-anchor="middle" font-size="10" fill="var(--faint)">writes are async (seconds of lag) · reads are real-time (one click queries)</text>
</svg>
<div class="figcap"><b>A trace's full journey</b>: the top half is the <b>write path</b> (SDK→API→Redis→worker→ClickHouse, with S3 alongside), each leg tagged with its lesson (L12–19); the bottom half is the <b>read path</b> (ClickHouse→repository→tRPC→UI, L20–27). The two paths "meet" at the ClickHouse wide table: writes put data in, reads take it out.</div>
</div>

<h2>Top half · write: SDK to ClickHouse</h2>
<p>First the parcel's "shipped to shelved" journey. It's deliberately <strong>async</strong> — the API only accepts and enqueues
fast, leaving the heavy lifting to the worker:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SDK creates events (L06)</h4><p>Your app calls the SDK or emits an OTel span, producing <strong>events</strong> like trace-create / observation-create / score-create.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>Public API accepts & enqueues (L12·14)</h4><p><code>web/src/pages/api/public/ingestion.ts</code> authenticates, Zod-validates a batch, then <strong>quickly drops it into the Redis queue</strong> and returns — without waiting for processing.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>worker merges & aggregates (L15)</h4><p><code>IngestionService</code> pulls events from the queue, <strong>fetches this record's prior events from S3</strong> and merges (multiple updates to one observation fold into one), deciding the final shape.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>compute token & cost (L16)</h4><p>Match the model name to the pricing table and <strong>backfill</strong> any unreported usage/cost (remember provided vs computed from L03?).</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>ClickhouseWriter batches the write (L17)</h4><p><strong>Batch</strong> processed records and write them to ClickHouse traces/observations/scores in one go (ReplacingMergeTree handles "later write of same id wins").</p></div></div>
</div>

<p>In this path, <strong>S3 plays "the raw event manuscript"</strong>: each incoming event lands in S3 first, and the worker re-reads S3
when merging. That allows <strong>replay</strong> on failure and lets "multiple updates to one observation" merge correctly — details
unpacked in L15–17. For now, remember the spine: <strong>accept → enqueue → merge → cost → store</strong>.</p>

<p>It's worth calling out why step 3, "<strong>merge</strong>", can't be skipped. The reason: an SDK often reports one observation
<strong>not all at once</strong>. For an LLM call, the SDK might first send an "observation-create" saying "I started, model is gpt-4o",
then after the call returns send an "observation-update" adding "output is X, used 1240 tokens". Those two events <strong>arrive
separately</strong>, and the worker must <strong>merge them into one final record</strong>. That's why it re-reads S3 for "this id's
prior events" — stitching the fragments that arrived at different times into one complete row. Grasp this and you see how Lesson 3's
"observations can arrive out of order via parentObservationId" is actually realized in ingestion: <strong>events may come in multiple
pieces, out of order, and the worker converges them into a consistent final state.</strong></p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="Multiple events for the same observation arrive out of order: observation-create (started, model gpt-4o) and observation-update (output X, 1240 tokens) arrive separately, the worker fetches this id's history from S3, groups and merges by id with the later timestamp winning conflicts, converging into one final ClickHouse row">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Arrive in pieces, out of order → worker converges to one final row</text>
  <rect x="24" y="44" width="180" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="60" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--ink)">event1 observation-create</text><text x="114" y="74" text-anchor="middle" font-size="6.2" fill="var(--muted)">{id:obs-42, started, model:gpt-4o}</text>
  <rect x="24" y="96" width="180" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="112" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--ink)">event2 observation-update</text><text x="114" y="126" text-anchor="middle" font-size="6.2" fill="var(--muted)">{id:obs-42, output:X, 1240 tokens}</text>
  <text x="114" y="156" text-anchor="middle" font-size="6.4" fill="var(--faint)">arrive separately, possibly out of order</text>
  <rect x="266" y="62" width="180" height="74" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="356" y="82" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">worker merges</text><text x="356" y="99" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">fetch id=obs-42 history from S3</text><text x="356" y="113" text-anchor="middle" font-size="6.4" fill="var(--muted)">group by id, each field takes the value side</text><text x="356" y="127" text-anchor="middle" font-size="6.4" fill="var(--muted)">conflicts: later timestamp wins</text>
  <rect x="508" y="68" width="188" height="62" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="602" y="88" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">one final row</text><text x="602" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">obs-42: gpt-4o + output:X</text><text x="602" y="119" text-anchor="middle" font-size="6.4" fill="var(--muted)">+ 1240 tokens, written to ClickHouse</text>
  <line x1="204" y1="64" x2="264" y2="88" stroke="var(--blue)" stroke-width="1.3"/><polygon points="264,88 255,85 256,93" fill="var(--blue)"/><line x1="204" y1="116" x2="264" y2="100" stroke="var(--blue)" stroke-width="1.3"/><polygon points="264,100 255,100 258,108" fill="var(--blue)"/>
  <line x1="446" y1="99" x2="506" y2="99" stroke="var(--accent)" stroke-width="1.4"/><polygon points="506,99 497,95 497,103" fill="var(--accent)"/>
  <text x="360" y="184" text-anchor="middle" font-size="8" fill="var(--faint)">This is exactly how Lesson 3's "out-of-order arrival is fine" is realized in ingestion, and the merge logic Lessons 13/15 detail</text>
</svg>
<div class="figcap"><b>Out-of-order events → one final state</b>: the same observation's create/update arrive in multiple pieces, possibly out of order; the worker fetches that id's history from S3, groups and merges by id (conflicts resolved by the later <code>timestamp</code>), converging into one final row written to ClickHouse. Details in Lessons 13·15.</div>
</div>
""")

_EN5.append(r"""
<h2>Bottom half · read: from UI back to ClickHouse</h2>
<p>Once stored, seeing it in your browser takes a different, more <strong>real-time</strong> path — you click, it queries:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>UI issues a query (L20)</h4><p>You open the trace list; the frontend issues a type-safe request via a <strong>tRPC</strong> hook (e.g. <code>api.traces.all.useQuery</code>).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>tRPC auth & dispatch (L21)</h4><p>The request hits <code>web/src/server/api</code>; middleware first checks "do you belong to this project" (RBAC), then dispatches to the right router handler.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>repository builds the query (L22·23)</h4><p>The handler calls functions in <code>packages/shared/src/server/repositories</code>, translating your filters into <strong>ClickHouse SQL</strong> (with time windows, selecting only the needed columns).</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>ClickHouse returns; UI renders (L24·25)</h4><p>The list reads only <strong>compact narrow fields</strong> (fast); only when you open a trace does it fetch the full input/output and build the observation tree.</p></div></div>
</div>

<p>Note that write and read <strong>converge</strong> on this one ClickHouse table: writes put the wide event in, reads pull it out
every which way. Lesson 2's "lists read narrow fields, detail reads big fields" is realized on exactly this read path.</p>

<h2>Why separate "accept" from "process"</h2>
<p>The cleverest step in this path is the API "<strong>accept and return</strong>". It splits the whole thing into a "fast lane" and a
"slow lane":</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="The API returns to the app in milliseconds (fast lane) while enqueuing events for the worker to process in the background (slow lane)">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Fast lane: API returns in ms　Slow lane: worker processes in background</text>
  <rect x="30" y="80" width="120" height="56" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="90" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">your app</text><text x="90" y="122" text-anchor="middle" font-size="9" fill="var(--muted)">can't wait</text>
  <rect x="220" y="80" width="120" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="280" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">public API</text><text x="280" y="122" text-anchor="middle" font-size="9" fill="var(--accent-ink)">validate+enqueue only</text>
  <line x1="150" y1="96" x2="218" y2="96" stroke="var(--faint)" stroke-width="1.8"/><polygon points="218,96 209,91 209,101" fill="var(--faint)"/><text x="184" y="88" text-anchor="middle" font-size="8.5" fill="var(--faint)">events</text>
  <line x1="218" y1="120" x2="152" y2="120" stroke="var(--accent)" stroke-width="2"/><polygon points="152,120 161,115 161,125" fill="var(--accent)"/><text x="185" y="138" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">200 OK in ms (fast lane)</text>
  <rect x="410" y="80" width="110" height="56" rx="10" fill="var(--red-soft)" stroke="var(--red)"/><text x="465" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">Redis queue</text><text x="465" y="122" text-anchor="middle" font-size="9" fill="var(--muted)">reservoir</text>
  <rect x="580" y="80" width="110" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="635" y="104" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">worker ×N</text><text x="635" y="122" text-anchor="middle" font-size="9" fill="var(--accent-ink)">batch·retryable</text>
  <line x1="340" y1="108" x2="408" y2="108" stroke="var(--faint)" stroke-width="1.8"/><polygon points="408,108 399,103 399,113" fill="var(--faint)"/>
  <line x1="520" y1="108" x2="578" y2="108" stroke="var(--faint)" stroke-width="1.8"/><polygon points="578,108 569,103 569,113" fill="var(--faint)"/>
  <text x="465" y="170" text-anchor="middle" font-size="9.5" fill="var(--faint)">slow lane: spikes queue up; the worker consumes at its own pace, scale out if overwhelmed</text>
</svg>
<div class="figcap"><b>One clean cut</b>: between app and API is the <b>fast lane</b> (returns in ms, almost never slow); after the API is the <b>slow lane</b> (enqueue → worker batches in the background). The queue is a reservoir: spikes queue up, and you add workers when overwhelmed.</div>
</div>

<p>Consider: a high-traffic LLM app may produce thousands of observations per second. If the API had to <strong>synchronously</strong>
merge, compute cost and write ClickHouse before returning, two bad things happen: one, every app call <strong>waits</strong> those
extra hundreds of ms, needlessly slowed by your monitoring tool; two, if ClickHouse hiccups or a spike maxes it out, the API
<strong>times out and even bounces errors back into your business</strong>. Cutting "accept" from "process" reduces the API to a
featherweight "<strong>validate + enqueue</strong>" endpoint — almost impossible to slow, almost impossible to drag your app down via
a downstream issue.</p>

<p>The queue is a <strong>reservoir</strong>: spikes queue up, the worker consumes in <strong>batches</strong> at its own pace, and you
<strong>add workers</strong> (scale out) when it can't keep up. Langfuse even splits the ingestion queue into <strong>primary/secondary
lanes</strong> (L14), isolating high-throughput big projects from ordinary ones so one project's spike can't drown everyone. The cost
is the bit of lag mentioned next — but keep Δ to seconds and users barely notice. This is why nearly every high-throughput telemetry
system (not just Langfuse) looks like this: <strong>lightweight accept + async process + batched store</strong>. Grasp this spine and
you can predict what each Part 3 lesson is solving.</p>

<h2>The cost of async: eventual consistency</h2>
<p>Stitch the halves together and one fact must be clear in your mind: <strong>from SDK send to UI visibility there's queue processing
in between, a few seconds of lag</strong>. This is <strong>eventual consistency</strong>.</p>

<p>What does "eventual consistency" mean in practice? It means that right after a call runs in your app, if you immediately switch to
the Langfuse UI and refresh, you <strong>might not see it yet</strong> — wait a second or two, refresh, and it appears. For almost all
observability use this is perfectly fine: you come <strong>after the fact</strong> to triage, view dashboards, evaluate — a few seconds
don't matter. But it flags two things: first, <strong>don't treat Langfuse as a strongly-consistent business database</strong> — it's a
telemetry system, not a "write-then-read-immediately" store; second, if you write automated tests to verify "is instrumentation
correct", remember to <strong>allow ingestion time to process</strong>, or you'll falsely conclude "the data never arrived". Understand
this boundary and the lag won't surprise you — you'll appreciate the "<strong>never drag the business</strong>" trade behind it.</p>

<div class="timeline">
  <div class="lane"><span class="lane-label">t0</span><span class="tslot now">SDK sends events</span><span class="tslot">API enqueues (returns in ms)</span></div>
  <div class="lane"><span class="lane-label">t0 + Δ</span><span class="tslot span">worker queues → merge → cost → write ClickHouse</span></div>
  <div class="lane"><span class="lane-label">t0 + Δ′</span><span class="tslot now">only now can the UI query this trace</span></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why tolerate that lag and go async?</strong> Because ingestion must absorb <strong>very high write throughput</strong> while
  your app <strong>can't afford to wait</strong>. If the API synchronously merged, computed cost and wrote before returning, every LLM
  call would be slowed by Langfuse and could fail on downstream hiccups. Async decouples "accept" from "process": the API always
  <strong>returns in milliseconds</strong> and almost never drags your app; the worker can digest spikes <strong>in batches,
  retryably, scaling by queue</strong>. The cost is that bit of processing lag — and Lesson 2's "preserve near-real-time debugging"
  principle demands keeping Δ to seconds so observability stays "almost live". <strong>Trade a little lag for an ingestion layer that
  never drags the business and survives spikes.</strong> This "lightweight accept + async process" trade recurs throughout Part 3 — it's
  not one module's trick but the guiding idea across the whole ingestion path.
</div>

<div class="card key">
  <div class="tag">🎯 Key points · and the Part 1 recap</div>
  <ul>
    <li>A trace's life: <strong>SDK → public API (enqueue) → Redis → worker (merge·cost) → ClickHouse</strong> (write), then <strong>UI → tRPC → repository → ClickHouse</strong> (read).</li>
    <li><strong>Writes are async</strong> (seconds of lag, eventual consistency), <strong>reads are real-time</strong>; the two paths converge on the ClickHouse wide table.</li>
    <li><strong>S3</strong> stores the raw event manuscript for merge and replay; the <strong>Redis</strong> queue decouples accept from process.</li>
    <li>Every leg maps to a later lesson: writing is Part 3 (L12–19), reading is Part 4 (L20–27).</li>
    <li>Part 1 ends here: you now hold the master map — <strong>data model + repo map + design philosophy + end-to-end path</strong> — and we dive in leg by leg next.</li>
  </ul>
</div>
""")

LESSON_05 = {"zh": "\n".join(_ZH5), "en": "\n".join(_EN5)}
