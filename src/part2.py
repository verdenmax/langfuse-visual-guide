"""Part 2 — 前置基础 / Foundations. Lessons L06–L11.

Same authoring pattern as part1: each lesson assembles its bilingual body from
``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh", "en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L06 · 给 LLM 应用埋点 / Instrumenting an LLM app
# ══════════════════════════════════════════════════════════════════════
_ZH6 = []
_EN6 = []

_ZH6.append(r"""
<p class="lead">
第 5 课的全链路里，第一段是「SDK 创建事件」。这一课就把镜头对准这第一段：在数据还没离开<strong>你的应用</strong>之前，它是怎么被「<strong>埋点</strong>」生成的。
你会看到 Langfuse 接收数据的<strong>两个入口</strong>——一种是用 Langfuse 自家的 <strong>SDK</strong> 发「原生事件」，另一种是走业界标准的
<strong>OpenTelemetry（OTLP）</strong>。理解了「应用这头发出的是什么」，后面第三部分「服务端怎么收、怎么处理」才有的放矢。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  埋点就像给一栋大楼<strong>装传感器</strong>：你<strong>不改变</strong>大楼本身的功能，只是在关键位置（大门、电梯、机房）装上记录器，把「谁什么时候经过、停留多久」记下来。
  Langfuse 的 <strong>SDK</strong> 是它<strong>自家定制的传感器</strong>，装起来最贴合、信息最全；而 <strong>OpenTelemetry</strong> 像一套<strong>通用接口的传感器标准</strong>——
  你楼里要是已经按这套标准装了线，Langfuse 直接<strong>接上现成的线</strong>就能收数据，不用重装。两条路，殊途同归：都是把应用运行的「踪迹」送出来。
  这一课的目标，就是让你看清「传感器这头到底发出了什么」——只有先看懂应用发出的<strong>原料</strong>，才能理解后面服务端是怎么把它加工成 trace 树和宽事件表的。
</div>
""")

# (L06 sections appended below)
_ZH6.append(r"""
<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="应用通过 Langfuse SDK 原生事件或 OpenTelemetry OTLP 两条入口把数据送进公共 API">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">两条入口，殊途同归</text>
  <rect x="40" y="98" width="150" height="56" rx="11" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="115" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">你的 LLM 应用</text><text x="115" y="140" text-anchor="middle" font-size="9" fill="var(--muted)">埋点发生在这里</text>
  <rect x="270" y="50" width="180" height="52" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="72" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">Langfuse SDK</text><text x="360" y="90" text-anchor="middle" font-size="9" fill="var(--accent-ink)">原生事件 trace/observation/score</text>
  <rect x="270" y="150" width="180" height="52" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="360" y="172" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">OpenTelemetry</text><text x="360" y="190" text-anchor="middle" font-size="9" fill="var(--muted)">OTLP 标准 span → 映射成 observation</text>
  <rect x="540" y="98" width="150" height="56" rx="11" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="615" y="122" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">公共摄取 API</text><text x="615" y="140" text-anchor="middle" font-size="9" fill="var(--accent-ink)">web · 收下入队</text>
  <line x1="190" y1="112" x2="268" y2="80" stroke="var(--faint)" stroke-width="1.8"/><polygon points="268,80 257,80 261,88" fill="var(--faint)"/>
  <line x1="190" y1="140" x2="268" y2="172" stroke="var(--faint)" stroke-width="1.8"/><polygon points="268,172 257,164 261,172" fill="var(--faint)"/>
  <line x1="450" y1="76" x2="538" y2="112" stroke="var(--faint)" stroke-width="1.8"/><polygon points="538,112 527,108 527,118" fill="var(--faint)"/>
  <line x1="450" y1="176" x2="538" y2="140" stroke="var(--faint)" stroke-width="1.8"/><polygon points="538,140 527,140 527,150" fill="var(--faint)"/>
  <text x="360" y="228" text-anchor="middle" font-size="9.5" fill="var(--faint)">SDK 路：ingestion.ts　·　OTel 路：otel/v1/traces（最终都进同一条摄取链路）</text>
</svg>
<div class="figcap"><b>两个入口</b>：用 <b>Langfuse SDK</b> 发原生事件（<code>web/src/pages/api/public/ingestion.ts</code>），或用 <b>OpenTelemetry OTLP</b> 发标准 span（<code>web/src/pages/api/public/otel/v1/traces</code>，span 会被映射成 observation）。两条路最后汇入同一条服务端摄取链路（第三部分）。</div>
</div>

<h2>事件信封：你的应用发出的是什么</h2>
<p>无论走哪条入口，应用发出的本质都是一批<strong>事件（event）</strong>。Langfuse 定义了一组事件类型（<code>packages/shared/src/server/ingestion/types.ts</code> 的 <code>eventTypes</code>），
每个事件描述「<strong>对哪个对象做了什么</strong>」：</p>

<table class="t">
  <tr><th>事件类型</th><th>含义</th></tr>
  <tr><td class="mono">TRACE_CREATE</td><td>创建/更新一个 trace（整次交互的外壳）</td></tr>
  <tr><td class="mono">SPAN_CREATE / SPAN_UPDATE</td><td>开始 / 结束一个 span 型 observation（有耗时的一段）</td></tr>
  <tr><td class="mono">GENERATION_CREATE</td><td>记录一次 LLM 调用（generation 型 observation）</td></tr>
  <tr><td class="mono">OBSERVATION_CREATE / OBSERVATION_UPDATE</td><td>通用的 observation 创建 / 更新</td></tr>
  <tr><td class="mono">EVENT_CREATE</td><td>记录一个瞬时事件</td></tr>
  <tr><td class="mono">SCORE_CREATE</td><td>提交一个 score（评分）</td></tr>
</table>

<p>注意这里有 <code>CREATE</code> 也有 <code>UPDATE</code>——这正是第 5 课「合并」的来源：一个 span 通常先 <code>SPAN_CREATE</code>（开始时），结束时再 <code>SPAN_UPDATE</code>（补上耗时、输出）。
应用把这些事件<strong>攒成一批</strong>，一次 HTTP 请求发给摄取 API，服务端再去合并。所以你在 SDK 里写的 <code>langfuse.trace(...)</code>、<code>span.end()</code>，
本质上就是在<strong>生成这些事件</strong>。</p>

<p>概念上，你在应用里写的埋点代码大致长这样（不同语言 SDK 形态略有差异，这里只示意「调用 → 事件」的对应关系）：</p>

<pre class="code"><span class="cm"># 创建一个 trace（发出 TRACE_CREATE）</span>
trace = langfuse.<span class="fn">trace</span>(name=<span class="st">"chat"</span>, user_id=<span class="st">"u_42"</span>)

<span class="cm"># 在 trace 下记录一次 LLM 调用（发出 GENERATION_CREATE）</span>
gen = trace.<span class="fn">generation</span>(name=<span class="st">"answer"</span>, model=<span class="st">"gpt-4o"</span>, input=prompt)
result = call_llm(prompt)
<span class="cm"># 调用结束，补上输出与用量（发出 OBSERVATION_UPDATE）</span>
gen.<span class="fn">end</span>(output=result, usage={<span class="st">"input"</span>: 800, <span class="st">"output"</span>: 440})

<span class="cm"># 给这次回答打个分（发出 SCORE_CREATE）</span>
trace.<span class="fn">score</span>(name=<span class="st">"helpfulness"</span>, value=0.9)</pre>

<p>关键观察：你只是<strong>在原有业务代码旁边「顺手记一笔」</strong>，并没有改变 <code>call_llm</code> 本身的逻辑。好的埋点应当<strong>尽量不侵入</strong>——
它不该决定你的应用怎么跑，只是<strong>旁观并记录</strong>。这也呼应了第 1 课的定位：Langfuse 站在你应用<strong>旁边</strong>，而不是<strong>里面</strong>。
正因为埋点是「旁路」的，它出问题（比如网络抖动发不出去）也<strong>不应拖垮你的主流程</strong>——SDK 通常会异步、批量、失败可丢地发送，把对应用的影响压到最低。把交互拆成「一串带类型的小事件」而不是「一个大对象」，正是为了让它们能分批、增量、乱序地发送。</p>

<p>那「一串带类型的小事件」到底长什么样？源码里每个事件都是同一个<strong>信封</strong>：一个 <code>base</code>（id + timestamp + metadata），再 <code>extend</code> 出 <code>type</code>（取值来自 <code>eventTypes</code> 映射）和 <code>body</code>（这种类型特有的字段）。一次 LLM 调用，SDK 可能发 <code>generation-create</code> 起头、<code>generation-update</code> 收尾——同一个信封、不同的 type，分批送达，worker 再按 id 合并（第 5 课已预演过）。</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/types.ts:259,597</span><span class="ln">事件信封 + 事件类型</span></div>
  <pre class="code"><span class="cm">// 每个上报事件都是「同一个信封」：base + type + body</span>
<span class="kw">const</span> base = z.<span class="fn">object</span>({
  id: idSchema,                              <span class="cm">// 这条事件的唯一 id</span>
  timestamp: z.iso.<span class="fn">datetime</span>({ offset: <span class="kw">true</span> }),  <span class="cm">// 何时发生（合并冲突以更晚者为准）</span>
  metadata: jsonSchema.<span class="fn">nullish</span>(),
});
<span class="kw">const</span> generationCreateEvent = base.<span class="fn">extend</span>({
  type: z.<span class="fn">literal</span>(eventTypes.GENERATION_CREATE),  <span class="cm">// 信封上的「类型」标签</span>
  body: CreateGenerationBody,                <span class="cm">// 这种类型特有的字段</span>
});

<span class="cm">// type 的合法取值（节选）——一次交互拆成这些小事件</span>
<span class="kw">export const</span> eventTypes = {
  TRACE_CREATE: <span class="st">"trace-create"</span>,        SCORE_CREATE: <span class="st">"score-create"</span>,
  GENERATION_CREATE: <span class="st">"generation-create"</span>, GENERATION_UPDATE: <span class="st">"generation-update"</span>,
  SPAN_CREATE: <span class="st">"span-create"</span>,  EVENT_CREATE: <span class="st">"event-create"</span>,  …
} <span class="kw">as const</span>;</pre>
</div>
""")

_ZH6.append(r"""
<h2>两种入口：原生 SDK vs OpenTelemetry</h2>
<p>为什么要同时支持两条入口？因为它们服务两类用户：</p>

<div class="cols">
  <div class="col"><h4>🎯 Langfuse SDK（原生）</h4><p>Langfuse 官方的 Python/JS SDK，直接发上面那套原生事件。<strong>信息最全、最贴合</strong>（prompt 关联、用量、成本字段都能精确上报），是大多数人的首选。入口：<code>ingestion.ts</code>。</p></div>
  <div class="col"><h4>🔌 OpenTelemetry（OTLP）</h4><p>如果你的系统<strong>已经用 OTel</strong> 做可观测，不想再引一套 SDK，就可以把 OTel 的 span 直接发到 Langfuse 的 OTLP 端点（<code>otel/v1/traces</code>）。Langfuse 把标准 span <strong>映射成 observation</strong>。代价是有些 Langfuse 专有语义要靠约定俗成的属性名传递。</p></div>
</div>

<p>这是一个典型的<strong>「拥抱标准 vs 发挥专长」</strong>的权衡。OTel 是云原生可观测的事实标准，支持它意味着 Langfuse 能<strong>无缝接入</strong>已有的 OTel 生态——
你不必为了用 Langfuse 就把埋点全部重写。但 OTel 的通用模型并不天然懂「prompt 版本」「token 用量」这些 LLM 专有概念，所以原生 SDK 在表达力上仍更强。
Langfuse 的选择是<strong>两者都要</strong>：用 OTLP 降低接入门槛，用原生 SDK 提供最佳体验。OTel 这条路的服务端处理，单独放在第 18 课讲。</p>

<h2>create 然后 update：事件是「增量」的</h2>
<p>再强调一遍这个对理解整条链路至关重要的点：<strong>一个 observation 的信息往往不是一次发齐的</strong>。看一次 LLM 调用的典型时间线：</p>

<div class="timeline">
  <div class="lane"><span class="lane-label">t0 开始</span><span class="tslot now">GENERATION_CREATE</span><span class="tslot">model=gpt-4o, input=…（这时还没有输出）</span></div>
  <div class="lane"><span class="lane-label">t1 结束</span><span class="tslot now">OBSERVATION_UPDATE</span><span class="tslot">output=…, usage=1240 tok, latency=1.8s</span></div>
  <div class="lane"><span class="lane-label">服务端</span><span class="tslot span">worker 把 create + update 合并成一条最终 observation（第 15 课）</span></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="一个 create 事件和一个 update 事件被 worker 合并成一条最终 observation">
  <rect x="30" y="40" width="200" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="130" y="60" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">GENERATION_CREATE</text><text x="130" y="78" text-anchor="middle" font-size="9" fill="var(--muted)">model, input（t0 开始时发）</text>
  <rect x="30" y="110" width="200" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="130" y="130" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">OBSERVATION_UPDATE</text><text x="130" y="148" text-anchor="middle" font-size="9" fill="var(--muted)">output, usage（t1 结束时发）</text>
  <rect x="320" y="75" width="120" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="380" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="var(--blue)">worker 合并</text><text x="380" y="114" text-anchor="middle" font-size="9" fill="var(--muted)">第 15 课</text>
  <rect x="520" y="70" width="170" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="605" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">一条最终 observation</text><text x="605" y="110" text-anchor="middle" font-size="9" fill="var(--muted)">model+input+output+usage</text>
  <line x1="230" y1="62" x2="318" y2="92" stroke="var(--faint)" stroke-width="1.8"/><polygon points="318,92 307,89 310,98" fill="var(--faint)"/>
  <line x1="230" y1="138" x2="318" y2="108" stroke="var(--faint)" stroke-width="1.8"/><polygon points="318,108 310,102 307,111" fill="var(--faint)"/>
  <line x1="440" y1="100" x2="518" y2="100" stroke="var(--faint)" stroke-width="1.8"/><polygon points="518,100 507,95 507,105" fill="var(--faint)"/>
</svg>
<div class="figcap"><b>两个事件，一条记录</b>：先后到达的 <code>CREATE</code> 与 <code>UPDATE</code> 被 worker 合并成同一条最终 observation。这就是为什么 SDK 那头可以「拆开发」、而你在 UI 里看到的却是完整的一条。</div>
</div>

<p>为什么要这样「增量」上报，而不是等全部结束再发一条完整的？因为这样应用能<strong>更早地把「开始了」这件事记下来</strong>——即使后面调用<strong>崩了、超时了</strong>，
你至少知道「它确实开始过、卡在了这一步」。如果非要等结束才发，那一旦中途挂掉，这一步就<strong>彻底消失</strong>，反而最该被观测的失败 case 被漏掉了。
增量上报 + 服务端合并，是「<strong>边发生边记录</strong>」的可观测理念在协议层的体现。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>把「事件增量上报 + 服务端合并」这套协议，复杂度放在哪一端？</strong> 放在<strong>服务端</strong>。SDK 那头被刻意做得很「笨」——只管把发生的事拆成小事件发出去，
  不负责拼装最终状态；真正麻烦的「把先后到达、可能乱序、可能重复的事件收敛成一致的一行」交给 worker（第 15 课）。这么分工的好处是：SDK 轻、对应用影响小、各语言都好实现；
  而最复杂、最需要小心的合并逻辑<strong>只在一处</strong>（服务端）维护，不必每个语言的 SDK 各写一遍、各错一遍。<strong>把复杂度收敛到一个能严格测试的地方。</strong>这条「客户端薄、服务端厚」的取舍，在很多大型系统里都能见到，Langfuse 只是把它用在了遥测协议上。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>埋点发生在<strong>你的应用</strong>里：把运行踪迹拆成一批<strong>事件</strong>发给 Langfuse，不改变业务逻辑。</li>
    <li><strong>两个入口</strong>：Langfuse <strong>原生 SDK</strong>（<code>ingestion.ts</code>，表达力最强）或 <strong>OpenTelemetry OTLP</strong>（<code>otel/v1/traces</code>，无缝接入已有 OTel）。</li>
    <li>事件类型（<code>eventTypes</code>）：<code>TRACE_CREATE / SPAN_CREATE / GENERATION_CREATE / OBSERVATION_UPDATE / SCORE_CREATE …</code>，描述「对哪个对象做了什么」。</li>
    <li>事件是<strong>增量</strong>的（create 开始、update 补全），所以「边发生边记录」，失败 case 也不丢——服务端负责合并（第 15 课）。</li>
    <li>协议把复杂度放在服务端：SDK 轻、好移植；合并逻辑只在一处维护。</li>
  </ul>
</div>
""")

_EN6.append(r"""
<p class="lead">
In Lesson 5's pipeline, the first leg was "SDK creates events". This lesson focuses on that first leg: how, before data ever leaves
<strong>your app</strong>, it gets <strong>instrumented</strong> into existence. You'll see Langfuse's <strong>two entry points</strong> —
sending "native events" via the Langfuse <strong>SDK</strong>, or sending standard <strong>OpenTelemetry (OTLP)</strong>. Understanding
"what the app side emits" makes Part 3 ("how the server receives and processes it") land.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Instrumentation is like fitting a building with <strong>sensors</strong>: you <strong>don't change</strong> the building's function,
  you just place recorders at key spots (door, elevator, server room) noting "who passed when, stayed how long". The Langfuse
  <strong>SDK</strong> is its <strong>own custom sensor</strong> — the best fit, richest signal; <strong>OpenTelemetry</strong> is like a
  <strong>standard sensor interface</strong> — if your building is already wired to that standard, Langfuse just <strong>plugs into the
  existing wiring</strong>. Two paths, same end: ship the app's "traces" out. This lesson's goal is to make clear "what the sensor end
  actually emits" — only by understanding the <strong>raw material</strong> the app sends can you grasp how the server later refines it
  into trace trees and wide-event tables.
</div>
""")

_EN6.append(r"""
<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="An app sends data to the public API via either Langfuse SDK native events or OpenTelemetry OTLP">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Two entries, same destination</text>
  <rect x="40" y="98" width="150" height="56" rx="11" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="115" y="122" text-anchor="middle" font-size="12" font-weight="700" fill="var(--ink)">your LLM app</text><text x="115" y="140" text-anchor="middle" font-size="9" fill="var(--muted)">instrumentation here</text>
  <rect x="270" y="50" width="180" height="52" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="72" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">Langfuse SDK</text><text x="360" y="90" text-anchor="middle" font-size="9" fill="var(--accent-ink)">native events trace/observation/score</text>
  <rect x="270" y="150" width="180" height="52" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="360" y="172" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">OpenTelemetry</text><text x="360" y="190" text-anchor="middle" font-size="9" fill="var(--muted)">OTLP span → mapped to observation</text>
  <rect x="540" y="98" width="150" height="56" rx="11" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="615" y="122" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">public ingest API</text><text x="615" y="140" text-anchor="middle" font-size="9" fill="var(--accent-ink)">web · accept+enqueue</text>
  <line x1="190" y1="112" x2="268" y2="80" stroke="var(--faint)" stroke-width="1.8"/><polygon points="268,80 257,80 261,88" fill="var(--faint)"/>
  <line x1="190" y1="140" x2="268" y2="172" stroke="var(--faint)" stroke-width="1.8"/><polygon points="268,172 257,164 261,172" fill="var(--faint)"/>
  <line x1="450" y1="76" x2="538" y2="112" stroke="var(--faint)" stroke-width="1.8"/><polygon points="538,112 527,108 527,118" fill="var(--faint)"/>
  <line x1="450" y1="176" x2="538" y2="140" stroke="var(--faint)" stroke-width="1.8"/><polygon points="538,140 527,140 527,150" fill="var(--faint)"/>
  <text x="360" y="228" text-anchor="middle" font-size="9.5" fill="var(--faint)">SDK path: ingestion.ts　·　OTel path: otel/v1/traces (both join one ingestion path)</text>
</svg>
<div class="figcap"><b>Two entries</b>: send native events with the <b>Langfuse SDK</b> (<code>web/src/pages/api/public/ingestion.ts</code>), or standard spans via <b>OpenTelemetry OTLP</b> (<code>web/src/pages/api/public/otel/v1/traces</code>, spans mapped to observations). Both converge on the same server-side ingestion path (Part 3).</div>
</div>

<h2>The event envelope: what your app emits</h2>
<p>Whichever entry, the app essentially emits a batch of <strong>events</strong>. Langfuse defines a set of event types
(<code>eventTypes</code> in <code>packages/shared/src/server/ingestion/types.ts</code>), each describing "<strong>what was done to which
object</strong>":</p>

<table class="t">
  <tr><th>Event type</th><th>Meaning</th></tr>
  <tr><td class="mono">TRACE_CREATE</td><td>create/update a trace (the interaction's shell)</td></tr>
  <tr><td class="mono">SPAN_CREATE / SPAN_UPDATE</td><td>start / end a span-type observation (a timed unit)</td></tr>
  <tr><td class="mono">GENERATION_CREATE</td><td>record an LLM call (generation-type observation)</td></tr>
  <tr><td class="mono">OBSERVATION_CREATE / OBSERVATION_UPDATE</td><td>generic observation create / update</td></tr>
  <tr><td class="mono">EVENT_CREATE</td><td>record an instantaneous event</td></tr>
  <tr><td class="mono">SCORE_CREATE</td><td>submit a score</td></tr>
</table>

<p>Note there's both <code>CREATE</code> and <code>UPDATE</code> — this is the source of Lesson 5's "merge": a span usually starts with
<code>SPAN_CREATE</code> and ends with <code>SPAN_UPDATE</code> (adding duration, output). The app <strong>batches</strong> these events
into one HTTP request to the ingestion API, and the server merges them. So your <code>langfuse.trace(...)</code> and
<code>span.end()</code> calls are essentially <strong>generating these events</strong>.</p>

<p>Conceptually, your instrumentation code looks roughly like this (SDK shapes differ by language; this just shows the "call →
event" mapping):</p>

<pre class="code"><span class="cm"># create a trace (emits TRACE_CREATE)</span>
trace = langfuse.<span class="fn">trace</span>(name=<span class="st">"chat"</span>, user_id=<span class="st">"u_42"</span>)

<span class="cm"># record an LLM call under the trace (emits GENERATION_CREATE)</span>
gen = trace.<span class="fn">generation</span>(name=<span class="st">"answer"</span>, model=<span class="st">"gpt-4o"</span>, input=prompt)
result = call_llm(prompt)
<span class="cm"># call ends; add output and usage (emits OBSERVATION_UPDATE)</span>
gen.<span class="fn">end</span>(output=result, usage={<span class="st">"input"</span>: 800, <span class="st">"output"</span>: 440})

<span class="cm"># score this answer (emits SCORE_CREATE)</span>
trace.<span class="fn">score</span>(name=<span class="st">"helpfulness"</span>, value=0.9)</pre>

<p>Key observation: you merely "<strong>jot a note alongside</strong>" your existing business code — you didn't change
<code>call_llm</code>'s logic. Good instrumentation is <strong>as non-intrusive as possible</strong> — it shouldn't dictate how your app
runs, only <strong>observe and record</strong>. This echoes Lesson 1: Langfuse sits <strong>beside</strong> your app, not
<strong>inside</strong> it. Because instrumentation is "side-channel", its failure (e.g. a network hiccup) <strong>shouldn't take down your
main flow</strong> — SDKs typically send asynchronously, batched, drop-on-failure, minimizing impact on the app.</p>

<p>So what does "a stream of typed little events" actually look like? In the source, every event is the same <strong>envelope</strong>: a <code>base</code> (id + timestamp + metadata), then <code>extend</code>ed with a <code>type</code> (a value from the <code>eventTypes</code> map) and a <code>body</code> (the fields specific to that type). One LLM call may have the SDK send a <code>generation-create</code> to start and a <code>generation-update</code> to finish — same envelope, different type, sent in batches, merged by id by the worker (rehearsed in Lesson 5).</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/types.ts:259,597</span><span class="ln">event envelope + event types</span></div>
  <pre class="code"><span class="cm">// every reported event is "the same envelope": base + type + body</span>
<span class="kw">const</span> base = z.<span class="fn">object</span>({
  id: idSchema,                              <span class="cm">// unique id of this event</span>
  timestamp: z.iso.<span class="fn">datetime</span>({ offset: <span class="kw">true</span> }),  <span class="cm">// when it happened (later wins on merge)</span>
  metadata: jsonSchema.<span class="fn">nullish</span>(),
});
<span class="kw">const</span> generationCreateEvent = base.<span class="fn">extend</span>({
  type: z.<span class="fn">literal</span>(eventTypes.GENERATION_CREATE),  <span class="cm">// the "type" tag on the envelope</span>
  body: CreateGenerationBody,                <span class="cm">// fields specific to this type</span>
});

<span class="cm">// the valid values of type (excerpt) — one interaction split into these little events</span>
<span class="kw">export const</span> eventTypes = {
  TRACE_CREATE: <span class="st">"trace-create"</span>,        SCORE_CREATE: <span class="st">"score-create"</span>,
  GENERATION_CREATE: <span class="st">"generation-create"</span>, GENERATION_UPDATE: <span class="st">"generation-update"</span>,
  SPAN_CREATE: <span class="st">"span-create"</span>,  EVENT_CREATE: <span class="st">"event-create"</span>,  …
} <span class="kw">as const</span>;</pre>
</div>
""")

_EN6.append(r"""
<h2>Two entries: native SDK vs OpenTelemetry</h2>
<p>Why support both? Because they serve two kinds of users:</p>

<div class="cols">
  <div class="col"><h4>🎯 Langfuse SDK (native)</h4><p>The official Python/JS SDKs emit the native events above. <strong>Richest, best-fit signal</strong> (prompt linkage, usage, cost reported precisely), the default for most. Entry: <code>ingestion.ts</code>.</p></div>
  <div class="col"><h4>🔌 OpenTelemetry (OTLP)</h4><p>If your system <strong>already uses OTel</strong> for observability and you'd rather not add another SDK, send OTel spans to Langfuse's OTLP endpoint (<code>otel/v1/traces</code>). Langfuse <strong>maps standard spans to observations</strong>. The cost: some Langfuse-specific semantics ride on convention-based attribute names.</p></div>
</div>

<p>This is a classic <strong>"embrace the standard vs play to your strengths"</strong> tradeoff. OTel is the de-facto standard for
cloud-native observability, so supporting it lets Langfuse <strong>plug into existing OTel ecosystems</strong> — you needn't rewrite all
your instrumentation to adopt Langfuse. But OTel's generic model doesn't natively understand LLM-specific concepts like "prompt
version" or "token usage", so the native SDK is still more expressive. Langfuse chooses <strong>both</strong>: OTLP lowers the barrier,
the native SDK gives the best experience. The server-side handling of the OTel path is its own Lesson 18.</p>

<h2>create then update: events are "incremental"</h2>
<p>Once more, a point crucial to understanding the whole path: <strong>an observation's info often isn't sent all at once</strong>. Look
at a typical LLM call timeline:</p>

<div class="timeline">
  <div class="lane"><span class="lane-label">t0 start</span><span class="tslot now">GENERATION_CREATE</span><span class="tslot">model=gpt-4o, input=… (no output yet)</span></div>
  <div class="lane"><span class="lane-label">t1 end</span><span class="tslot now">OBSERVATION_UPDATE</span><span class="tslot">output=…, usage=1240 tok, latency=1.8s</span></div>
  <div class="lane"><span class="lane-label">server</span><span class="tslot span">worker merges create + update into one final observation (L15)</span></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="A create event and an update event are merged by the worker into one final observation">
  <rect x="30" y="40" width="200" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="130" y="60" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">GENERATION_CREATE</text><text x="130" y="78" text-anchor="middle" font-size="9" fill="var(--muted)">model, input (sent at t0)</text>
  <rect x="30" y="110" width="200" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="130" y="130" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">OBSERVATION_UPDATE</text><text x="130" y="148" text-anchor="middle" font-size="9" fill="var(--muted)">output, usage (sent at t1)</text>
  <rect x="320" y="75" width="120" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="380" y="98" text-anchor="middle" font-size="11" font-weight="700" fill="var(--blue)">worker merge</text><text x="380" y="114" text-anchor="middle" font-size="9" fill="var(--muted)">L15</text>
  <rect x="520" y="70" width="170" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="605" y="92" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">one final observation</text><text x="605" y="110" text-anchor="middle" font-size="9" fill="var(--muted)">model+input+output+usage</text>
  <line x1="230" y1="62" x2="318" y2="92" stroke="var(--faint)" stroke-width="1.8"/><polygon points="318,92 307,89 310,98" fill="var(--faint)"/>
  <line x1="230" y1="138" x2="318" y2="108" stroke="var(--faint)" stroke-width="1.8"/><polygon points="318,108 310,102 307,111" fill="var(--faint)"/>
  <line x1="440" y1="100" x2="518" y2="100" stroke="var(--faint)" stroke-width="1.8"/><polygon points="518,100 507,95 507,105" fill="var(--faint)"/>
</svg>
<div class="figcap"><b>Two events, one record</b>: the <code>CREATE</code> and <code>UPDATE</code> arriving at different times are merged by the worker into one final observation. That's why the SDK can "send in pieces" while you see one complete row in the UI.</div>
</div>

<p>Why report "incrementally" instead of waiting and sending one complete event at the end? So the app can <strong>record "it
started" earlier</strong> — even if the call later <strong>crashes or times out</strong>, you at least know "it did start and got stuck
here". Wait until the end and a mid-flight crash makes that step <strong>vanish entirely</strong>, losing exactly the failure cases most
worth observing. Incremental reporting + server merge is the protocol-level expression of "<strong>record as it happens</strong>"
observability.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Where does the "incremental events + server merge" protocol put the complexity?</strong> On the <strong>server</strong>. The
  SDK is deliberately "dumb" — it just splits what happens into small events and ships them, not assembling the final state; the truly
  tricky "converge possibly-out-of-order, possibly-duplicate events into one consistent row" goes to the worker (L15). The payoff: the
  SDK is light, low-impact, easy to implement in every language; and the most complex, careful merge logic lives in <strong>one
  place</strong> (the server), not re-implemented (and re-bugged) in each language SDK. <strong>Converge complexity to one strictly
  testable place.</strong> This "thin client, thick server" trade shows up in many large systems; Langfuse just applies it to a
  telemetry protocol.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>Instrumentation happens in <strong>your app</strong>: split the run-time trace into a batch of <strong>events</strong> sent to Langfuse, without changing business logic.</li>
    <li><strong>Two entries</strong>: Langfuse <strong>native SDK</strong> (<code>ingestion.ts</code>, most expressive) or <strong>OpenTelemetry OTLP</strong> (<code>otel/v1/traces</code>, plugs into existing OTel).</li>
    <li>Event types (<code>eventTypes</code>): <code>TRACE_CREATE / SPAN_CREATE / GENERATION_CREATE / OBSERVATION_UPDATE / SCORE_CREATE …</code>, describing "what was done to which object".</li>
    <li>Events are <strong>incremental</strong> (create starts, update completes), so "record as it happens" and failures aren't lost — the server merges (L15).</li>
    <li>The protocol puts complexity on the server: SDKs stay light and portable; merge logic lives in one place.</li>
  </ul>
</div>
""")

LESSON_06 = {"zh": "\n".join(_ZH6), "en": "\n".join(_EN6)}


# ══════════════════════════════════════════════════════════════════════
# L07 · 双存储架构 / The dual-store architecture
# ══════════════════════════════════════════════════════════════════════
_ZH7 = []
_EN7 = []

_ZH7.append(r"""
<p class="lead">
上一课，数据以「事件」的形式离开了你的应用。这一课讲它们最终<strong>落在哪</strong>。很多人以为一个数据库就够了，但 Langfuse 用了<strong>四种存储</strong>——
<strong>Postgres、ClickHouse、Redis、S3</strong>，各管一摊。这不是炫技，而是因为不同数据的<strong>访问模式</strong>天差地别：用错存储，热路径会被活活拖垮。
看懂这四者的分工，你就理解了 Langfuse 性能与可扩展性的<strong>地基</strong>。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把这四种存储想成一家公司的四种「存放方式」：<strong>Postgres</strong> 是<strong>文件柜</strong>——放重要档案（谁是员工、项目配置），要求<strong>准、可改、查得快</strong>，但量不大；
  <strong>ClickHouse</strong> 是<strong>巨型货仓</strong>——堆放海量货物（每天上亿条事件），要的是<strong>按品类批量盘点</strong>的能力；<strong>Redis</strong> 是<strong>传送带 + 暂存台</strong>——
  货物先上传送带排队（队列），常用的小东西放手边随手取（缓存）；<strong>S3</strong> 是<strong>外部仓储</strong>——存又大又不常翻的原件（事件底稿、上传的图片、导出的大文件）。
  四者各有所长，硬塞进一个，必然顾此失彼。看懂这四种存储分别擅长什么、为什么这么分，是理解后面摄取与查询两条链路的前提。
</div>
""")

_ZH7.append(r"""
<div class="fig">
<svg viewBox="0 0 720 280" role="img" aria-label="web 和 worker 两个容器分别读写 Postgres、ClickHouse、Redis、S3 四种存储">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">两个容器，四种存储，各司其职</text>
  <rect x="150" y="40" width="160" height="44" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="230" y="60" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">web</text><text x="230" y="76" text-anchor="middle" font-size="9" fill="var(--accent-ink)">UI · API</text>
  <rect x="410" y="40" width="160" height="44" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="490" y="60" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">worker</text><text x="490" y="76" text-anchor="middle" font-size="9" fill="var(--accent-ink)">后台处理</text>
  <rect x="20" y="160" width="150" height="80" rx="11" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--blue)">Postgres</text><text x="95" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">配置/元数据</text><text x="95" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">事务·强一致·量小</text>
  <rect x="190" y="160" width="150" height="80" rx="11" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="265" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="265" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">宽事件 trace/obs/score</text><text x="265" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">列存·海量·聚合快</text>
  <rect x="360" y="160" width="150" height="80" rx="11" fill="var(--red-soft)" stroke="var(--red)"/><text x="435" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--red)">Redis</text><text x="435" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">队列(BullMQ) + 缓存</text><text x="435" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">内存·极快·临时</text>
  <rect x="530" y="160" width="160" height="80" rx="11" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="610" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--amber)">S3 / blob</text><text x="610" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">事件底稿·媒体·导出</text><text x="610" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">对象存储·大·便宜</text>
  <line x1="210" y1="84" x2="120" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="225" y1="84" x2="255" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="245" y1="84" x2="425" y2="158" stroke="var(--faint)" stroke-width="1.4"/>
  <line x1="470" y1="84" x2="280" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="485" y1="84" x2="440" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="510" y1="84" x2="610" y2="158" stroke="var(--faint)" stroke-width="1.4"/>
  <text x="360" y="262" text-anchor="middle" font-size="9.5" fill="var(--faint)">web 主要读 PG(配置)+CH(分析)；worker 主要写 CH/S3、用 Redis 队列</text>
</svg>
<div class="figcap"><b>四种存储的分工</b>：<b>Postgres</b>=配置/元数据（事务、强一致、量小）；<b>ClickHouse</b>=宽事件（列存、海量、聚合快）；<b>Redis</b>=队列+缓存（内存、极快、临时）；<b>S3</b>=事件底稿/媒体/导出（对象存储、大、便宜）。web 偏读、worker 偏写，但都按数据性质选对应的库。</div>
</div>

<h2>为什么不能只用一个</h2>
<p>核心原因一句话：<strong>事务型负载（OLTP）和分析型负载（OLAP）是两种相反的优化目标</strong>，没有哪个库能同时把两头都做到极致。</p>
<ul>
  <li><strong>配置/元数据</strong>（项目、用户、API key、prompt 定义）是典型 <strong>OLTP</strong>：数据量小、要频繁<strong>精确读写单条</strong>、要<strong>强一致</strong>（创建了项目立刻就能用）、还有外键关系。这正是 <strong>Postgres</strong> 的主场。</li>
  <li><strong>遥测数据</strong>（trace/observation/score）是典型 <strong>OLAP</strong>：数据量巨大（一天上亿）、写多于改、查询多是<strong>按时间窗口 + 某些维度做聚合</strong>（如「过去 7 天按模型看成本」）。这正是列存的 <strong>ClickHouse</strong> 的主场。</li>
</ul>

<div class="cols">
  <div class="col"><h4>🗄️ Postgres 擅长（OLTP）</h4><p>精确读写单条、强一致、外键关系、事务。适合<strong>小而重要、要立刻可用</strong>的配置类数据。不适合：海量行的聚合扫描。</p></div>
  <div class="col"><h4>📊 ClickHouse 擅长（OLAP）</h4><p>对海量行的某几列做时间窗口扫描 + 聚合，列存 + 压缩。适合<strong>巨量、追加写、按维度统计</strong>的遥测数据。不适合：频繁改单条 + 强一致。</p></div>
</div>

<p>如果硬把遥测塞进 Postgres，海量行 + 频繁聚合会让它不堪重负；反过来把配置塞进 ClickHouse，它的<strong>弱事务、最终一致</strong>又满足不了「创建即可用」。
所以 Langfuse 的选择不是「贪多」，而是<strong>让每种数据待在最适合它的库里</strong>——这正是第 2 课「按列式访问设计」「谨慎反范式化」等原则在存储层的总落点。</p>
""")

_ZH7.append(r"""
<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="OLTP 按主键精确取单条，OLAP 按时间窗口扫描海量行再聚合，两种访问模式相反">
  <text x="180" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">OLTP（Postgres）：精确取单条</text>
  <text x="540" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--purple)">OLAP（ClickHouse）：扫一片再聚合</text>
  <g>
    <rect x="40" y="44" width="280" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)"/>
    <rect x="40" y="72" width="280" height="22" rx="4" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
    <rect x="40" y="100" width="280" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)"/>
    <rect x="40" y="128" width="280" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)"/>
    <text x="180" y="88" text-anchor="middle" font-size="9.5" fill="var(--blue)">WHERE id = 'x' → 命中这一行</text>
    <text x="180" y="172" text-anchor="middle" font-size="9.5" fill="var(--muted)">读一条 · 毫秒 · 强一致</text>
  </g>
  <g>
    <rect x="400" y="44" width="280" height="106" rx="6" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2"/>
    <line x1="420" y1="62" x2="660" y2="62" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="80" x2="660" y2="80" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="98" x2="660" y2="98" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="116" x2="660" y2="116" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="134" x2="660" y2="134" stroke="var(--purple)" stroke-width="1"/>
    <text x="540" y="172" text-anchor="middle" font-size="9.5" fill="var(--muted)">扫上亿行的某几列 · 按维度聚合 · 列存才扛得住</text>
  </g>
</svg>
<div class="figcap"><b>两种相反的访问模式</b>：OLTP 靠索引<b>精确命中一行</b>（读配置、改设置）；OLAP 要<b>扫一大片行的某几列再聚合</b>（按时间/模型统计成本）。行存数据库擅长前者，列存数据库擅长后者——这就是为什么配置归 Postgres、遥测归 ClickHouse。</div>
</div>

<h2>四个存储各管什么</h2>
<table class="t">
  <tr><th>存储</th><th>装什么</th><th>仓库里的客户端</th></tr>
  <tr><td class="mono">Postgres</td><td>org/project/user、API key、prompt、eval 配置、定价…（控制面）</td><td class="mono">packages/shared/src/db.ts（Prisma）</td></tr>
  <tr><td class="mono">ClickHouse</td><td>traces / observations / scores 三张宽事件表（数据面）</td><td class="mono">.../server/clickhouse/client.ts</td></tr>
  <tr><td class="mono">Redis</td><td>BullMQ 队列（解耦摄取）+ 缓存（如 prompt、eval 配置）</td><td class="mono">.../server/redis/redis.ts</td></tr>
  <tr><td class="mono">S3 / blob</td><td>事件原始底稿（支撑合并/重放）、多模态媒体、批量导出</td><td class="mono">.../server/s3/index.ts</td></tr>
</table>

<p>注意一个细节：S3 不只是「存大文件」。摄取链路里，每个进来的事件<strong>先落 S3</strong>，worker 合并时再回 S3 取历史（第 5、15 课）——S3 在这里扮演的是
<strong>「事件日志 / 真相之源」</strong>的角色。ClickHouse 里的宽事件，本质上是 S3 事件底稿<strong>合并后的「物化视图」</strong>：万一 ClickHouse 数据需要重建，
理论上可以从 S3 的原始事件<strong>重放</strong>出来。这种「原始日志 + 派生表」的分工，正是第 2 课「不可变 / 追加式事件」原则的体现。</p>

<div class="layers">
  <div class="layer l-main"><div class="lh"><span class="badge">控制面</span><span class="name">Postgres</span></div><div class="ld">谁能用、配置成什么样：org/project/user、API key、prompt、eval 配置、定价。改动少而关键，要强一致。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">数据面</span><span class="name">ClickHouse</span></div><div class="ld">实际的遥测洪流：trace/observation/score 三张宽事件表。海量、追加、按维度聚合。</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">传输</span><span class="name">Redis</span></div><div class="ld">把摄取异步化的队列，加上热点配置的缓存。内存级、临时、极快。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">对象存储</span><span class="name">S3 / blob</span></div><div class="ld">事件真相之源、上传媒体、批量导出。又大又不常翻的东西放这里，便宜耐放。</div></div>
</div>

<p>这四层在运行时是<strong>协作</strong>的，不是各自孤立。回想第 5 课那条链路：摄取时，事件先进 <strong>Redis 队列</strong>、原件落 <strong>S3</strong>，worker 合并后写 <strong>ClickHouse</strong>；
而合并时要知道「这个 observation 关联哪版 prompt」「按什么模型定价」，又要回 <strong>Postgres</strong> 查配置。一次摄取，四种存储各出一份力。读取时也类似：UI 列表查 <strong>ClickHouse</strong>，
但「这个项目叫什么、谁有权限」来自 <strong>Postgres</strong>，热点配置走 <strong>Redis</strong> 缓存。所以理解 Langfuse，本质上就是理解<strong>数据如何在这四种存储之间流动</strong>——
这也是为什么本指南的第二部分要专门用一课讲存储分工：它是后面所有链路课的<strong>共同底座</strong>。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>四个存储 = 四份运维负担，为什么还要这么拆？</strong> 第 2 课有一条原则：「把成本与运维简单性当作架构约束」——多一个数据库就要多一份备份、监控、升级、容灾。
  Langfuse 之所以仍坚持四存储，是因为<strong>每一个都在解决一个单一存储解决不了的硬问题</strong>：没有 ClickHouse，海量聚合查询会慢到不可用；没有 Redis 队列，摄取就无法异步抗洪峰；
  没有 S3，大字段和媒体会把数据库撑爆、也无法重放。换句话说，这四个不是「想加就加」，而是<strong>各自挣到了自己的存在</strong>。这也是判断「该不该再加一个存储」的标准——
  它解决的问题，是否值得它带来的长期运维成本。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>四种存储各管一摊</strong>：Postgres（配置/元数据·OLTP）、ClickHouse（宽事件·OLAP）、Redis（队列+缓存）、S3（事件底稿+媒体+导出）。</li>
    <li>核心理由：<strong>OLTP 与 OLAP 是相反的优化目标</strong>，配置要精确单条+强一致，遥测要海量扫描+聚合，必须分库。</li>
    <li><strong>S3 是「真相之源」</strong>：事件先落 S3，ClickHouse 的宽事件是其合并后的派生表，可重放。</li>
    <li>控制面（Postgres）vs 数据面（ClickHouse）的划分，是第 3 课「领域形状 vs 物理存储」的宏观版。</li>
    <li>四存储不是堆技术，而是各自<strong>挣到了存在</strong>——这也是「该不该再加一个存储」的判断标准。</li>
  </ul>
</div>
""")

_EN7.append(r"""
<p class="lead">
Last lesson, data left your app as "events". This lesson is about <strong>where it lands</strong>. Many assume one database suffices,
but Langfuse uses <strong>four stores</strong> — <strong>Postgres, ClickHouse, Redis, S3</strong> — each for its own job. Not
showing off: different data has wildly different <strong>access patterns</strong>, and the wrong store will crush the hot path.
Understand the division of labor and you understand the <strong>foundation</strong> of Langfuse's performance and scalability.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Picture the four stores as a company's four "ways to keep things": <strong>Postgres</strong> is the <strong>filing cabinet</strong> —
  important records (who's an employee, project config), needing to be <strong>accurate, editable, quick to look up</strong> but not
  huge; <strong>ClickHouse</strong> is the <strong>giant warehouse</strong> — mountains of goods (hundreds of millions of events a day),
  needing <strong>bulk stock-taking by category</strong>; <strong>Redis</strong> is the <strong>conveyor belt + staging table</strong> —
  goods queue on the belt (queues), and frequently-used small items stay at hand (cache); <strong>S3</strong> is <strong>off-site
  storage</strong> — big, rarely-flipped originals (event manuscripts, uploaded images, large exports). Each excels at its own; cram
  them into one and you lose.
</div>
""")

_EN7.append(r"""
<div class="fig">
<svg viewBox="0 0 720 280" role="img" aria-label="web and worker containers read/write the four stores Postgres, ClickHouse, Redis, S3">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Two containers, four stores, each its own job</text>
  <rect x="150" y="40" width="160" height="44" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="230" y="60" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">web</text><text x="230" y="76" text-anchor="middle" font-size="9" fill="var(--accent-ink)">UI · API</text>
  <rect x="410" y="40" width="160" height="44" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="490" y="60" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--accent-ink)">worker</text><text x="490" y="76" text-anchor="middle" font-size="9" fill="var(--accent-ink)">background</text>
  <rect x="20" y="160" width="150" height="80" rx="11" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--blue)">Postgres</text><text x="95" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">config/metadata</text><text x="95" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">txn·consistent·small</text>
  <rect x="190" y="160" width="150" height="80" rx="11" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="265" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="265" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">wide events</text><text x="265" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">columnar·huge·fast agg</text>
  <rect x="360" y="160" width="150" height="80" rx="11" fill="var(--red-soft)" stroke="var(--red)"/><text x="435" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--red)">Redis</text><text x="435" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">queue(BullMQ)+cache</text><text x="435" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">in-memory·fast·temp</text>
  <rect x="530" y="160" width="160" height="80" rx="11" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="610" y="186" text-anchor="middle" font-size="11.5" font-weight="700" fill="var(--amber)">S3 / blob</text><text x="610" y="205" text-anchor="middle" font-size="9" fill="var(--muted)">event log·media·export</text><text x="610" y="221" text-anchor="middle" font-size="9" fill="var(--muted)">object store·big·cheap</text>
  <line x1="210" y1="84" x2="120" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="225" y1="84" x2="255" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="245" y1="84" x2="425" y2="158" stroke="var(--faint)" stroke-width="1.4"/>
  <line x1="470" y1="84" x2="280" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="485" y1="84" x2="440" y2="158" stroke="var(--faint)" stroke-width="1.4"/><line x1="510" y1="84" x2="610" y2="158" stroke="var(--faint)" stroke-width="1.4"/>
  <text x="360" y="262" text-anchor="middle" font-size="9.5" fill="var(--faint)">web mostly reads PG(config)+CH(analytics); worker mostly writes CH/S3, uses the Redis queue</text>
</svg>
<div class="figcap"><b>The four stores' division of labor</b>: <b>Postgres</b>=config/metadata (txn, consistent, small); <b>ClickHouse</b>=wide events (columnar, huge, fast aggregation); <b>Redis</b>=queue+cache (in-memory, fast, temporary); <b>S3</b>=event manuscript/media/exports (object store, big, cheap). web leans read, worker leans write, but both pick the store that fits the data.</div>
</div>

<h2>Why not just one</h2>
<p>The core reason in one line: <strong>transactional (OLTP) and analytical (OLAP) workloads are opposite optimization targets</strong>,
and no single store nails both extremes.</p>
<ul>
  <li><strong>Config/metadata</strong> (projects, users, API keys, prompt definitions) is classic <strong>OLTP</strong>: small, frequent <strong>precise single-row read/write</strong>, <strong>strong consistency</strong> (create a project, use it instantly), with foreign keys. Postgres's home turf.</li>
  <li><strong>Telemetry</strong> (trace/observation/score) is classic <strong>OLAP</strong>: enormous (hundreds of millions/day), write-mostly, queries are mostly <strong>time-window + dimensional aggregation</strong> ("cost by model over 7 days"). Columnar ClickHouse's home turf.</li>
</ul>

<div class="cols">
  <div class="col"><h4>🗄️ Postgres is good at (OLTP)</h4><p>precise single-row read/write, strong consistency, foreign keys, transactions. Fits <strong>small, important, must-be-instant</strong> config data. Bad at: aggregating scans over huge rows.</p></div>
  <div class="col"><h4>📊 ClickHouse is good at (OLAP)</h4><p>time-window scans + aggregation over a few columns of huge rows, columnar + compressed. Fits <strong>massive, append-write, dimensional</strong> telemetry. Bad at: frequent single-row edits + strong consistency.</p></div>
</div>

<p>Cram telemetry into Postgres and huge rows + frequent aggregation overwhelm it; cram config into ClickHouse and its <strong>weak
transactions, eventual consistency</strong> fail "instantly usable". So Langfuse isn't being greedy — it's <strong>letting each kind of
data live in the store that fits it best</strong>, the storage-layer landing point of Lesson 2's "design around columnar access" and
"denormalize carefully".</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="OLTP fetches one row by key; OLAP scans a slice of many rows and aggregates - opposite access patterns">
  <text x="180" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">OLTP (Postgres): fetch one row</text>
  <text x="540" y="22" text-anchor="middle" font-size="12" font-weight="700" fill="var(--purple)">OLAP (ClickHouse): scan a slice + aggregate</text>
  <g>
    <rect x="40" y="44" width="280" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)"/>
    <rect x="40" y="72" width="280" height="22" rx="4" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
    <rect x="40" y="100" width="280" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)"/>
    <rect x="40" y="128" width="280" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)"/>
    <text x="180" y="88" text-anchor="middle" font-size="9.5" fill="var(--blue)">WHERE id = 'x' → hits this row</text>
    <text x="180" y="172" text-anchor="middle" font-size="9.5" fill="var(--muted)">one row · ms · strongly consistent</text>
  </g>
  <g>
    <rect x="400" y="44" width="280" height="106" rx="6" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2"/>
    <line x1="420" y1="62" x2="660" y2="62" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="80" x2="660" y2="80" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="98" x2="660" y2="98" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="116" x2="660" y2="116" stroke="var(--purple)" stroke-width="1"/><line x1="420" y1="134" x2="660" y2="134" stroke="var(--purple)" stroke-width="1"/>
    <text x="540" y="172" text-anchor="middle" font-size="9.5" fill="var(--muted)">scan a few columns of millions of rows · aggregate · needs columnar</text>
  </g>
</svg>
<div class="figcap"><b>Two opposite access patterns</b>: OLTP uses an index to <b>hit exactly one row</b> (read config, change settings); OLAP must <b>scan a few columns of a big slice of rows and aggregate</b> (cost by time/model). Row stores excel at the former, columnar at the latter — which is why config goes to Postgres and telemetry to ClickHouse.</div>
</div>

<h2>What each store holds</h2>
<table class="t">
  <tr><th>Store</th><th>Holds</th><th>Client in the repo</th></tr>
  <tr><td class="mono">Postgres</td><td>org/project/user, API keys, prompts, eval config, pricing… (control plane)</td><td class="mono">packages/shared/src/db.ts (Prisma)</td></tr>
  <tr><td class="mono">ClickHouse</td><td>traces / observations / scores — three wide-event tables (data plane)</td><td class="mono">.../server/clickhouse/client.ts</td></tr>
  <tr><td class="mono">Redis</td><td>BullMQ queues (decouple ingestion) + cache (e.g. prompts, eval config)</td><td class="mono">.../server/redis/redis.ts</td></tr>
  <tr><td class="mono">S3 / blob</td><td>raw event manuscript (for merge/replay), multimodal media, bulk exports</td><td class="mono">.../server/s3/index.ts</td></tr>
</table>

<p>One detail: S3 isn't just "big-file storage". In the ingestion path, each incoming event <strong>lands in S3 first</strong>, and the
worker re-reads S3 when merging (L05, L15) — here S3 plays the <strong>"event log / source of truth"</strong> role. The wide events in
ClickHouse are essentially a <strong>"materialized view" of the merged S3 manuscripts</strong>: if ClickHouse data ever needs rebuilding,
it can in principle be <strong>replayed</strong> from the raw S3 events. This "raw log + derived table" split is Lesson 2's "immutable /
append-oriented events" in action.</p>

<div class="layers">
  <div class="layer l-main"><div class="lh"><span class="badge">control plane</span><span class="name">Postgres</span></div><div class="ld">who can use it, configured how: org/project/user, API keys, prompts, eval config, pricing. Few but critical changes, needs strong consistency.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">data plane</span><span class="name">ClickHouse</span></div><div class="ld">the actual telemetry flood: traces/observations/scores wide-event tables. Huge, append, dimensional aggregation.</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">transport</span><span class="name">Redis</span></div><div class="ld">the queue that makes ingestion async, plus a cache for hot config. In-memory, temporary, very fast.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">object store</span><span class="name">S3 / blob</span></div><div class="ld">the event source of truth, uploaded media, bulk exports. Big, rarely-flipped things live here — cheap and durable.</div></div>
</div>

<p>These four layers <strong>collaborate</strong> at runtime, not in isolation. Recall Lesson 5's path: on ingestion, events first enter the
<strong>Redis queue</strong> and originals land in <strong>S3</strong>; after merging the worker writes <strong>ClickHouse</strong>; and to
merge it must know "which prompt version this observation links to" and "what model pricing applies", so it reads config back from
<strong>Postgres</strong>. One ingestion, four stores each pulling their weight. Reads are similar: the UI list queries
<strong>ClickHouse</strong>, but "what's this project called, who has access" comes from <strong>Postgres</strong>, and hot config goes
through the <strong>Redis</strong> cache. So understanding Langfuse is essentially understanding <strong>how data flows among these four
stores</strong> — which is why Part 2 spends a whole lesson on the storage division of labor: it's the <strong>shared foundation</strong>
of every later path lesson.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Four stores = four operational burdens, so why split this much?</strong> Lesson 2 has a principle: "treat cost and
  operational simplicity as constraints" — each extra database means more backups, monitoring, upgrades, DR. Langfuse still keeps four
  because <strong>each solves a hard problem a single store can't</strong>: without ClickHouse, huge aggregation queries are unusably
  slow; without the Redis queue, ingestion can't go async to absorb spikes; without S3, big fields and media bloat the database and you
  can't replay. In other words, these four aren't "add because we can" — each <strong>earned its existence</strong>. That's also the
  test for "should we add another store": does the problem it solves justify its long-term operational cost?
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Four stores, each its own job</strong>: Postgres (config/metadata·OLTP), ClickHouse (wide events·OLAP), Redis (queue+cache), S3 (event manuscript+media+exports).</li>
    <li>Core reason: <strong>OLTP and OLAP are opposite targets</strong> — config needs precise single-row + strong consistency, telemetry needs massive scan + aggregation, so split stores.</li>
    <li><strong>S3 is the "source of truth"</strong>: events land in S3 first; ClickHouse wide events are the merged derived table, replayable.</li>
    <li>Control plane (Postgres) vs data plane (ClickHouse) is the macro version of Lesson 3's "domain shape vs physical storage".</li>
    <li>Four stores aren't tech-stacking — each <strong>earned its existence</strong>, which is also the test for "should we add another store".</li>
  </ul>
</div>
""")

LESSON_07 = {"zh": "\n".join(_ZH7), "en": "\n".join(_EN7)}


# ══════════════════════════════════════════════════════════════════════
# L08 · ClickHouse 与宽事件表 / ClickHouse & the wide-event tables
# ══════════════════════════════════════════════════════════════════════
_ZH8 = []
_EN8 = []

_ZH8.append(r"""
<p class="lead">
上一课说遥测数据都进 ClickHouse。这一课打开引擎盖，看这三张宽事件表（traces / observations / scores）<strong>到底是怎么建的、为什么这么建</strong>。
这是整个存储层<strong>最该看懂</strong>的一课——一旦理解了表引擎、排序键、分区这几样，后面「为什么列表快、为什么按项目按时间查特别高效、为什么数据能边写边查」
这些问题都会迎刃而解。我们以 <code>observations</code> 表为例（建表 SQL 在 <code>packages/shared/clickhouse/migrations/unclustered/0002_observations.up.sql</code>）。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把 ClickHouse 的表想成一座<strong>超大图书馆</strong>。<strong>分区（PARTITION）</strong>像按<strong>出版年月分大书架</strong>——找「2024 年 6 月的书」直接去那个架，别的架碰都不用碰；
  <strong>排序键（ORDER BY）</strong>像每个架内的<strong>摆放顺序</strong>（先按学科、再按日期），于是「某学科某段时间的书」只要在架上扫<strong>连续一小段</strong>；
  <strong>ReplacingMergeTree 引擎</strong>则像一条<strong>上架规则</strong>：同一个书号来了新版本，<strong>用新版盖掉旧版</strong>（按版本号判断谁新）。  三者配合，海量藏书也能秒级定位与盘点。这一课就把这三条「上架与摆放规则」逐一拆开，让你看清 Langfuse 是怎么在上亿行里做到「边写边查、查得还快」的。
</div>
""")

_ZH8.append(r"""
<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="observations 表一行的结构：标识列、富属性列、Map 列、大字段压缩列、版本控制列">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">observations 一行的解剖（宽事件）</text>
  <rect x="20" y="36" width="680" height="40" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="30" y="52" font-size="10" font-weight="700" fill="var(--blue)">标识 / 关联</text><text x="30" y="68" font-size="9" fill="var(--muted)">id · trace_id · project_id · parent_observation_id · type · name</text>
  <rect x="20" y="84" width="680" height="40" rx="7" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="30" y="100" font-size="10" font-weight="700" fill="var(--purple)">富属性（内联的宽列）</text><text x="30" y="116" font-size="9" fill="var(--muted)">provided_model_name · internal_model_id · total_cost · start_time · end_time · prompt_id/name/version</text>
  <rect x="20" y="132" width="680" height="40" rx="7" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="30" y="148" font-size="10" font-weight="700" fill="var(--amber)">Map 列（半结构化）</text><text x="30" y="164" font-size="9" fill="var(--muted)">metadata · usage_details · cost_details · provided_usage_details · provided_cost_details</text>
  <rect x="20" y="180" width="430" height="40" rx="7" fill="var(--panel-2)" stroke="var(--line)"/><text x="30" y="196" font-size="10" font-weight="700" fill="var(--ink)">大字段（ZSTD 压缩）</text><text x="30" y="212" font-size="9" fill="var(--muted)">input  CODEC(ZSTD(3)) · output  CODEC(ZSTD(3))</text>
  <rect x="462" y="180" width="238" height="40" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="472" y="196" font-size="10" font-weight="700" fill="var(--accent-ink)">版本控制</text><text x="472" y="212" font-size="9" fill="var(--accent-ink)">event_ts · is_deleted</text>
</svg>
<div class="figcap"><b>一行宽事件的五类列</b>：标识/关联列（拼树、定位）、内联的富属性宽列（model、cost、prompt…）、半结构化的 <b>Map</b> 列（metadata、usage/cost 明细）、用 <b>ZSTD</b> 压缩的大字段（input/output）、以及版本控制列（<code>event_ts</code>、<code>is_deleted</code>）。一行就装下了第 3 课说的全部富属性。</div>
</div>

<h2>ReplacingMergeTree：同 id 后写覆盖先写</h2>
<p>三张表用的引擎都是 <code>ReplacingMergeTree</code>。它的建表声明长这样：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">clickhouse/migrations/unclustered/0002_observations.up.sql</span><span class="ln">ENGINE</span></div>
  <pre class="code">ENGINE = <span class="fn">ReplacingMergeTree</span>(event_ts, is_deleted)
PARTITION BY <span class="fn">toYYYYMM</span>(start_time)
ORDER BY (project_id, <span class="kw">type</span>, <span class="fn">toDate</span>(start_time), id)</pre>
</div>

<p>关键就在 <code>ReplacingMergeTree(event_ts, is_deleted)</code> 这一句。它的语义是：<strong>排序键完全相同的多行，会被「替换」成最新的一行</strong>——
谁的 <code>event_ts</code>（版本时间戳）更大，就保留谁；<code>is_deleted=1</code> 则表示这行被软删除。这正好<strong>完美契合第 5、6 课的合并模型</strong>：
一个 observation 先 create、后 update，会产生<strong>两次写入</strong>（相同 id、不同 event_ts），ClickHouse 在后台合并时<strong>自动用 update 那条盖掉 create 那条</strong>。
你不需要先查出旧行、改完再写回——<strong>只管追加，覆盖交给引擎</strong>。这就是第 2 课「不可变 / 追加式事件」能成立的存储基础。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="同一个 id 的两次写入，ReplacingMergeTree 后台合并时保留 event_ts 更大的那条">
  <rect x="30" y="50" width="240" height="44" rx="8" fill="var(--panel-2)" stroke="var(--line)"/><text x="150" y="68" text-anchor="middle" font-size="10" fill="var(--muted)">id=o1 · event_ts=t0</text><text x="150" y="84" text-anchor="middle" font-size="9" fill="var(--faint)">create：model, input（旧版）</text>
  <rect x="30" y="106" width="240" height="44" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="150" y="124" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">id=o1 · event_ts=t1（更大）</text><text x="150" y="140" text-anchor="middle" font-size="9" fill="var(--accent-ink)">update：+output, +usage（新版）</text>
  <rect x="350" y="78" width="120" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="410" y="100" text-anchor="middle" font-size="10" font-weight="700" fill="var(--blue)">后台合并</text><text x="410" y="115" text-anchor="middle" font-size="8.5" fill="var(--muted)">Replacing</text>
  <rect x="520" y="78" width="180" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="610" y="96" text-anchor="middle" font-size="10" font-weight="700" fill="var(--purple)">保留 t1 这一条</text><text x="610" y="112" text-anchor="middle" font-size="8.5" fill="var(--muted)">model+input+output+usage</text>
  <line x1="270" y1="72" x2="348" y2="96" stroke="var(--faint)" stroke-width="1.6"/><line x1="270" y1="128" x2="348" y2="104" stroke="var(--faint)" stroke-width="1.6"/>
  <line x1="470" y1="100" x2="518" y2="100" stroke="var(--faint)" stroke-width="1.6"/><polygon points="518,100 507,95 507,105" fill="var(--faint)"/>
  <text x="360" y="180" text-anchor="middle" font-size="9" fill="var(--faint)">查询时如果还没合并，可用 FINAL 或聚合保证读到最终态（细节见查询链路）</text>
</svg>
<div class="figcap"><b>后写覆盖先写</b>：相同排序键的两次写入，引擎按 <code>event_ts</code> 保留更新的那条，<code>is_deleted</code> 实现软删除。于是「改一条 observation」= 追加一条更大 event_ts 的记录，无需读-改-写。</div>
</div>
""")

_ZH8.append(r"""
<h2>排序键 + 分区：为什么按 project_id 和时间</h2>
<p>再看那两行：<code>PARTITION BY toYYYYMM(start_time)</code> 和 <code>ORDER BY (project_id, type, toDate(start_time), id)</code>。
这两句决定了数据在磁盘上<strong>怎么分块、怎么排列</strong>，也就决定了查询能不能<strong>少扫数据</strong>。在上亿行的规模下，能不能「少扫」往往比单点「扫得多快」更决定性能。</p>

<div class="cols">
  <div class="col"><h4>📅 分区 PARTITION BY 月</h4><p>按 <code>toYYYYMM(start_time)</code> 把数据切成<strong>一月一块</strong>。查「最近 7 天」时，引擎直接<strong>跳过</strong>不相关月份的整块数据（partition pruning），连读都不读。</p></div>
  <div class="col"><h4>🔑 排序键 project_id 打头</h4><p><code>ORDER BY</code> 第一列是 <code>project_id</code>，于是同一项目的数据在磁盘上<strong>物理相邻</strong>。多租户查询天生只看自己项目，扫一段连续区间即可，无需全表过滤。</p></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="查询某项目最近时间段时，分区裁掉无关月份，排序键让数据集中在连续区间，只扫一小片">
  <text x="360" y="20" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">查询「项目 P · 最近 7 天」→ 只扫绿色一小片</text>
  <text x="60" y="44" font-size="9.5" fill="var(--faint)">2024-04</text><rect x="120" y="34" width="560" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)" opacity="0.5"/><text x="690" y="49" font-size="8" fill="var(--faint)">裁掉</text>
  <text x="60" y="74" font-size="9.5" fill="var(--faint)">2024-05</text><rect x="120" y="64" width="560" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)" opacity="0.5"/><text x="690" y="79" font-size="8" fill="var(--faint)">裁掉</text>
  <text x="60" y="104" font-size="9.5" fill="var(--purple)">2024-06</text><rect x="120" y="94" width="560" height="26" rx="4" fill="var(--panel)" stroke="var(--purple)"/>
  <rect x="300" y="97" width="120" height="20" rx="3" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="111" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">项目 P 的连续区间</text>
  <text x="200" y="111" text-anchor="middle" font-size="8" fill="var(--muted)">项目 A…</text><text x="540" y="111" text-anchor="middle" font-size="8" fill="var(--muted)">项目 Z…</text>
  <text x="360" y="150" text-anchor="middle" font-size="9.5" fill="var(--purple)">① 分区裁掉 4、5 月 → ② 排序键定位到 6 月里项目 P 那一段 → ③ 只读这一小片的几列</text>
  <text x="360" y="178" text-anchor="middle" font-size="9.5" fill="var(--faint)">海量数据下，「少扫」比「扫得快」重要得多——这是列存 + 排序键 + 分区的合力</text>
  <text x="360" y="200" text-anchor="middle" font-size="9" fill="var(--faint)">这也是第 2 课「围绕列式访问设计：时间窗口 + 排序键 + 数据剪枝」的实现</text>
</svg>
<div class="figcap"><b>少扫才是关键</b>：分区先按月裁掉无关数据，排序键（project_id 打头）再把目标项目的数据收拢成连续一段，最后列存只读你要的那几列。三者合力，让「按项目按时间」这类最高频查询在上亿行里也只碰一小片。</div>
</div>

<h2>列存 + 压缩 + 索引：让「宽」也能快</h2>
<p>宽事件行很宽，怎么保证不慢？靠三招，都写在建表 SQL 里：</p>

<table class="t">
  <tr><th>手段</th><th>建表里怎么写</th><th>解决什么</th></tr>
  <tr><td><b>列式存储</b></td><td>MergeTree 家族天生列存</td><td>查询只读用到的列，不为不相关的大字段买单</td></tr>
  <tr><td><b>ZSTD 压缩</b></td><td><code>input/output … CODEC(ZSTD(3))</code></td><td>把又大又重复的 prompt/输出文本压到很小，省空间也省 IO</td></tr>
  <tr><td><b>Map 列</b></td><td><code>metadata/usage_details … Map(...)</code></td><td>半结构化字段不必预先建列，灵活又可查</td></tr>
  <tr><td><b>布隆过滤索引</b></td><td><code>INDEX idx_id id TYPE bloom_filter()</code></td><td>按 id / trace_id 精确查时，快速跳过不含目标的数据块</td></tr>
</table>

<p>三张表的排序键略有不同，但<strong>都以 project_id 打头</strong>，体现「多租户隔离 = 排序键前缀」这一贯思路：</p>

<table class="t">
  <tr><th>表</th><th>ORDER BY</th></tr>
  <tr><td class="mono">traces</td><td class="mono">(project_id, toDate(timestamp), id)</td></tr>
  <tr><td class="mono">observations</td><td class="mono">(project_id, type, toDate(start_time), id)</td></tr>
  <tr><td class="mono">scores</td><td class="mono">(project_id, ...)</td></tr>
</table>

<p>这种「三张表排序键高度一致」并非巧合，而是<strong>刻意为之</strong>：因为最常见的查询模式就是「某项目、某时间段」，把 <code>project_id</code> 和时间放在排序键最前，
等于把这类查询的成本压到最低。这也呼应第 3 课「三支柱 1:1 映射三张表」——三张表不仅结构对应，连<strong>物理排布的逻辑都一致</strong>，于是无论查 trace、查 observation 还是查 score，
引擎都能用同一套「裁分区 + 定区间」的本事。理解了 <code>observations</code> 这张，另外两张你就触类旁通了。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>ReplacingMergeTree 的覆盖是「最终」的，不是「立刻」的</strong>——后台合并需要时间，所以理论上你可能在两次写入<strong>都还在、还没合并</strong>的瞬间读到旧行。
  这是它换来「只管追加、写入飞快」的代价。怎么补？查询侧用 <code>FINAL</code> 关键字强制合并后再读，或用<strong>聚合</strong>（按 id 取 event_ts 最大的那条）来保证读到最终态——
  这就把「去重」的成本从<strong>每次写入</strong>挪到了<strong>查询时（且可控）</strong>。第 2 课说「避免读时去重的隐藏开销」，Langfuse 的做法是：尽量让常规查询走聚合/最终态视图，
  把代价显式化、可优化，而不是让每次写入都付出读-改-写的代价。<strong>追加换吞吐，去重挪到读侧并优化</strong>——这是高写入遥测系统的经典取舍。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>引擎 = ReplacingMergeTree(event_ts, is_deleted)</strong>：相同排序键，后写（event_ts 更大）覆盖先写，<code>is_deleted</code> 软删除——完美承接第 5、6 课 create+update 的合并模型。</li>
    <li><strong>分区 = 按月</strong>（<code>toYYYYMM</code>），查时间窗口可整块裁剪；<strong>排序键 = project_id 打头</strong>，多租户查询只扫连续一段。</li>
    <li>「<strong>少扫</strong>」靠分区裁剪 + 排序键定位 + 列存只读所需列这三者合力，是海量数据下保持高效的关键。</li>
    <li><strong>列存 + ZSTD 压缩 + Map 列 + bloom_filter 索引</strong>，让又宽又大的行也能查得快、存得省，不为不相关的大字段买单。</li>
    <li>取舍：覆盖是「最终」的，去重成本从写入挪到查询（FINAL/聚合），换来写入飞快——避免读时去重的隐藏开销。</li>
  </ul>
</div>
""")

_EN8.append(r"""
<p class="lead">
Last lesson said telemetry goes to ClickHouse. This lesson opens the hood on how the three wide-event tables (traces / observations /
scores) <strong>are actually built and why</strong>. It's the <strong>must-understand</strong> storage lesson — once you grasp the table
engine, ordering key and partitioning, later questions ("why are lists fast", "why is by-project + by-time so efficient", "why can data
be queried while being written") all fall into place. We use the <code>observations</code> table as the example (CREATE TABLE in
<code>packages/shared/clickhouse/migrations/unclustered/0002_observations.up.sql</code>).
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Picture a ClickHouse table as a <strong>giant library</strong>. <strong>Partitioning</strong> is like <strong>big shelves by publish
  month</strong> — for "books from June 2024" you go straight to that shelf and never touch the others; the <strong>ordering key</strong>
  is the <strong>arrangement within a shelf</strong> (by subject, then date), so "a subject over a time range" is just a <strong>short
  contiguous scan</strong>; the <strong>ReplacingMergeTree engine</strong> is a <strong>shelving rule</strong>: a new edition of the same
  call number <strong>replaces the old</strong> (decided by version number). Together, even a vast collection is located and counted in
  milliseconds.
</div>
""")

_EN8.append(r"""
<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="anatomy of one observations row: identity columns, rich columns, Map columns, compressed big fields, version columns">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">anatomy of one observations row (wide event)</text>
  <rect x="20" y="36" width="680" height="40" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="30" y="52" font-size="10" font-weight="700" fill="var(--blue)">identity / linkage</text><text x="30" y="68" font-size="9" fill="var(--muted)">id · trace_id · project_id · parent_observation_id · type · name</text>
  <rect x="20" y="84" width="680" height="40" rx="7" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="30" y="100" font-size="10" font-weight="700" fill="var(--purple)">rich attributes (inlined wide columns)</text><text x="30" y="116" font-size="9" fill="var(--muted)">provided_model_name · internal_model_id · total_cost · start_time · end_time · prompt_id/name/version</text>
  <rect x="20" y="132" width="680" height="40" rx="7" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="30" y="148" font-size="10" font-weight="700" fill="var(--amber)">Map columns (semi-structured)</text><text x="30" y="164" font-size="9" fill="var(--muted)">metadata · usage_details · cost_details · provided_usage_details · provided_cost_details</text>
  <rect x="20" y="180" width="430" height="40" rx="7" fill="var(--panel-2)" stroke="var(--line)"/><text x="30" y="196" font-size="10" font-weight="700" fill="var(--ink)">big fields (ZSTD compressed)</text><text x="30" y="212" font-size="9" fill="var(--muted)">input  CODEC(ZSTD(3)) · output  CODEC(ZSTD(3))</text>
  <rect x="462" y="180" width="238" height="40" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="472" y="196" font-size="10" font-weight="700" fill="var(--accent-ink)">versioning</text><text x="472" y="212" font-size="9" fill="var(--accent-ink)">event_ts · is_deleted</text>
</svg>
<div class="figcap"><b>Five kinds of columns in one wide-event row</b>: identity/linkage (tree, lookup), inlined rich wide columns (model, cost, prompt…), semi-structured <b>Map</b> columns (metadata, usage/cost details), <b>ZSTD</b>-compressed big fields (input/output), and version columns (<code>event_ts</code>, <code>is_deleted</code>). One row holds all of Lesson 3's rich attributes.</div>
</div>

<h2>ReplacingMergeTree: later write of the same id wins</h2>
<p>All three tables use the <code>ReplacingMergeTree</code> engine. The declaration looks like:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">clickhouse/migrations/unclustered/0002_observations.up.sql</span><span class="ln">ENGINE</span></div>
  <pre class="code">ENGINE = <span class="fn">ReplacingMergeTree</span>(event_ts, is_deleted)
PARTITION BY <span class="fn">toYYYYMM</span>(start_time)
ORDER BY (project_id, <span class="kw">type</span>, <span class="fn">toDate</span>(start_time), id)</pre>
</div>

<p>The key is <code>ReplacingMergeTree(event_ts, is_deleted)</code>. Its semantics: <strong>multiple rows with the identical ordering key
are "replaced" down to the latest one</strong> — whoever has the larger <code>event_ts</code> (version timestamp) wins;
<code>is_deleted=1</code> marks a soft delete. This <strong>perfectly fits Lessons 5 and 6's merge model</strong>: an observation that's
created then updated produces <strong>two writes</strong> (same id, different event_ts), and ClickHouse <strong>automatically lets the
update overwrite the create</strong> during background merge. You needn't read the old row, edit, and write back — <strong>just append;
overwrite is the engine's job</strong>. This is the storage basis that makes Lesson 2's "immutable / append-oriented events" viable.</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="two writes of the same id; ReplacingMergeTree keeps the one with the larger event_ts at background merge">
  <rect x="30" y="50" width="240" height="44" rx="8" fill="var(--panel-2)" stroke="var(--line)"/><text x="150" y="68" text-anchor="middle" font-size="10" fill="var(--muted)">id=o1 · event_ts=t0</text><text x="150" y="84" text-anchor="middle" font-size="9" fill="var(--faint)">create: model, input (old)</text>
  <rect x="30" y="106" width="240" height="44" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="150" y="124" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">id=o1 · event_ts=t1 (larger)</text><text x="150" y="140" text-anchor="middle" font-size="9" fill="var(--accent-ink)">update: +output, +usage (new)</text>
  <rect x="350" y="78" width="120" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="410" y="100" text-anchor="middle" font-size="10" font-weight="700" fill="var(--blue)">bg merge</text><text x="410" y="115" text-anchor="middle" font-size="8.5" fill="var(--muted)">Replacing</text>
  <rect x="520" y="78" width="180" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="610" y="96" text-anchor="middle" font-size="10" font-weight="700" fill="var(--purple)">keep the t1 row</text><text x="610" y="112" text-anchor="middle" font-size="8.5" fill="var(--muted)">model+input+output+usage</text>
  <line x1="270" y1="72" x2="348" y2="96" stroke="var(--faint)" stroke-width="1.6"/><line x1="270" y1="128" x2="348" y2="104" stroke="var(--faint)" stroke-width="1.6"/>
  <line x1="470" y1="100" x2="518" y2="100" stroke="var(--faint)" stroke-width="1.6"/><polygon points="518,100 507,95 507,105" fill="var(--faint)"/>
  <text x="360" y="180" text-anchor="middle" font-size="9" fill="var(--faint)">if not yet merged at query time, FINAL or aggregation guarantees the final state (see the read path)</text>
</svg>
<div class="figcap"><b>Later write wins</b>: for two writes with the same ordering key, the engine keeps the newer <code>event_ts</code>; <code>is_deleted</code> implements soft delete. So "edit an observation" = append a record with a larger event_ts, no read-modify-write.</div>
</div>
""")

_EN8.append(r"""
<h2>Ordering key + partition: why by project_id and time</h2>
<p>Now the other two lines: <code>PARTITION BY toYYYYMM(start_time)</code> and <code>ORDER BY (project_id, type, toDate(start_time),
id)</code>. They decide <strong>how data is chunked and arranged</strong> on disk — and therefore whether a query can <strong>scan
less</strong>.</p>

<div class="cols">
  <div class="col"><h4>📅 PARTITION BY month</h4><p><code>toYYYYMM(start_time)</code> cuts data into <strong>one chunk per month</strong>. For "last 7 days", the engine simply <strong>skips</strong> whole irrelevant months (partition pruning) — never even reads them.</p></div>
  <div class="col"><h4>🔑 ORDER BY project_id first</h4><p>The first <code>ORDER BY</code> column is <code>project_id</code>, so one project's data is <strong>physically adjacent</strong> on disk. Multi-tenant queries naturally see only their project — a contiguous range, no full-table filtering.</p></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="querying a project over a recent window: partition prunes irrelevant months; ordering key clusters the project into a contiguous range; only a small slice is scanned">
  <text x="360" y="20" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">query "project P · last 7 days" → scan only the green slice</text>
  <text x="60" y="44" font-size="9.5" fill="var(--faint)">2024-04</text><rect x="120" y="34" width="560" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)" opacity="0.5"/><text x="690" y="49" font-size="8" fill="var(--faint)">pruned</text>
  <text x="60" y="74" font-size="9.5" fill="var(--faint)">2024-05</text><rect x="120" y="64" width="560" height="22" rx="4" fill="var(--panel-2)" stroke="var(--line)" opacity="0.5"/><text x="690" y="79" font-size="8" fill="var(--faint)">pruned</text>
  <text x="60" y="104" font-size="9.5" fill="var(--purple)">2024-06</text><rect x="120" y="94" width="560" height="26" rx="4" fill="var(--panel)" stroke="var(--purple)"/>
  <rect x="300" y="97" width="120" height="20" rx="3" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="111" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">project P contiguous range</text>
  <text x="200" y="111" text-anchor="middle" font-size="8" fill="var(--muted)">project A…</text><text x="540" y="111" text-anchor="middle" font-size="8" fill="var(--muted)">project Z…</text>
  <text x="360" y="150" text-anchor="middle" font-size="9.5" fill="var(--purple)">(1) prune Apr/May → (2) ordering key locates project P in June → (3) read only a few columns of that slice</text>
  <text x="360" y="178" text-anchor="middle" font-size="9.5" fill="var(--faint)">at scale, "scan less" beats "scan fast" — the combined effect of columnar + ordering key + partition</text>
  <text x="360" y="200" text-anchor="middle" font-size="9" fill="var(--faint)">this realizes Lesson 2's "columnar access: time windows + ordering keys + data pruning"</text>
</svg>
<div class="figcap"><b>Scanning less is the point</b>: partitions prune irrelevant data by month, the ordering key (project_id first) clusters the target project into a contiguous range, and columnar storage reads only the columns you want. Together, "by project, by time" — the hottest query — touches only a small slice even across hundreds of millions of rows.</div>
</div>

<h2>Columnar + compression + indexes: making "wide" fast too</h2>
<p>Wide rows are wide — how stay fast? Three moves, all in the CREATE TABLE:</p>

<table class="t">
  <tr><th>Move</th><th>In the schema</th><th>Solves</th></tr>
  <tr><td><b>Columnar storage</b></td><td>the MergeTree family is columnar</td><td>queries read only the columns used, not paying for irrelevant big fields</td></tr>
  <tr><td><b>ZSTD compression</b></td><td><code>input/output … CODEC(ZSTD(3))</code></td><td>shrinks big, repetitive prompt/output text — saves space and IO</td></tr>
  <tr><td><b>Map columns</b></td><td><code>metadata/usage_details … Map(...)</code></td><td>semi-structured fields need no predefined columns — flexible yet queryable</td></tr>
  <tr><td><b>Bloom-filter index</b></td><td><code>INDEX idx_id id TYPE bloom_filter()</code></td><td>for exact id/trace_id lookups, quickly skip blocks not containing the target</td></tr>
</table>

<p>The three tables' ordering keys differ slightly but <strong>all start with project_id</strong>, expressing the consistent "multi-tenant
isolation = ordering-key prefix" idea:</p>

<table class="t">
  <tr><th>Table</th><th>ORDER BY</th></tr>
  <tr><td class="mono">traces</td><td class="mono">(project_id, toDate(timestamp), id)</td></tr>
  <tr><td class="mono">observations</td><td class="mono">(project_id, type, toDate(start_time), id)</td></tr>
  <tr><td class="mono">scores</td><td class="mono">(project_id, ...)</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>ReplacingMergeTree's overwrite is "eventual", not "immediate"</strong> — background merge takes time, so in principle you could
  read the old row in the instant both writes exist but aren't merged yet. That's the price of "just append, write fast". The fix: on the
  query side use the <code>FINAL</code> keyword to force-merge before reading, or use <strong>aggregation</strong> (take the max-event_ts
  row per id) to guarantee the final state — moving the "dedup" cost from <strong>every write</strong> to <strong>query time (and
  controllable)</strong>. Lesson 2 says "avoid read-time dedup's hidden cost"; Langfuse's approach is to route regular queries through
  aggregation/final-state views, making the cost explicit and optimizable rather than paying read-modify-write on every write.
  <strong>Append for throughput, move dedup to the read side and optimize it</strong> — a classic write-heavy-telemetry trade.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Engine = ReplacingMergeTree(event_ts, is_deleted)</strong>: same ordering key, later write (larger event_ts) overwrites earlier, <code>is_deleted</code> soft-deletes — perfectly absorbing the create+update merge model.</li>
    <li><strong>Partition = by month</strong> (<code>toYYYYMM</code>), so time-window queries prune whole chunks; <strong>ordering key = project_id first</strong>, so multi-tenant queries scan one contiguous range.</li>
    <li>"<strong>Scan less</strong>" via partition pruning + ordering-key locating + columnar column-selection is the key to scale efficiency.</li>
    <li><strong>Columnar + ZSTD + Map columns + bloom_filter indexes</strong> keep wide, big rows fast to query and cheap to store.</li>
    <li>Tradeoff: overwrite is "eventual"; dedup cost moves from writes to queries (FINAL/aggregation), buying fast writes — avoiding read-time dedup's hidden cost.</li>
  </ul>
</div>
""")

LESSON_08 = {"zh": "\n".join(_ZH8), "en": "\n".join(_EN8)}


# ══════════════════════════════════════════════════════════════════════
# L09 · 元数据 schema（Postgres/Prisma）/ The metadata schema (Postgres)
# ══════════════════════════════════════════════════════════════════════
_ZH9 = []
_EN9 = []

_ZH9.append(r"""
<p class="lead">
前两课的主角是 ClickHouse（海量遥测）。这一课换到另一半：<strong>Postgres</strong>。如果说 ClickHouse 存的是「<strong>发生了什么</strong>」（trace/observation/score），
那 Postgres 存的就是「<strong>这套平台是怎么配置的</strong>」——谁是你的组织和项目、谁有权限、有哪些 API key、定义了哪些 prompt、配了哪些评估规则、各模型怎么定价。
这一面叫<strong>控制面（control plane）</strong>，数据量不大却<strong>事关全局</strong>。它的形状全写在 <code>packages/shared/prisma/schema.prisma</code> 里。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把两套存储想成一家公司的两类系统：<strong>Postgres</strong> 是<strong>行政/人事系统</strong>——记录谁是员工、分在哪个部门、有什么权限、签了哪些规章。
  数据不多，但要求<strong>准确、可改、立刻生效</strong>（新员工入职，权限马上得能用）。<strong>ClickHouse</strong> 则是<strong>业务流水账</strong>——海量交易记录，
  平时只往里追加，事后拿来按月按品类统计。  <strong>你不会把规章制度记到流水账里，也不会把每笔交易塞进人事档案</strong>——两类数据，两套系统，各得其所。这一课就专门看「人事系统」这一半：它存了什么、为什么这么存。
</div>
""")

# (L09 sections appended below)
_ZH9.append(r"""
<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Postgres 存控制面（配置/元数据），ClickHouse 存数据面（遥测洪流），两者分工">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">控制面（Postgres）vs 数据面（ClickHouse）</text>
  <rect x="30" y="40" width="320" height="190" rx="12" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <text x="190" y="62" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">Postgres · 控制面</text>
  <text x="190" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">少而关键 · 强一致 · 频繁精确读写</text>
  <rect x="48" y="92" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="115" y="111" text-anchor="middle" font-size="9.5" fill="var(--ink)">org / project / user</text>
  <rect x="197" y="92" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="264" y="111" text-anchor="middle" font-size="9.5" fill="var(--ink)">API key · 权限</text>
  <rect x="48" y="130" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="115" y="149" text-anchor="middle" font-size="9.5" fill="var(--ink)">prompt 定义</text>
  <rect x="197" y="130" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="264" y="149" text-anchor="middle" font-size="9.5" fill="var(--ink)">eval / 数据集 配置</text>
  <rect x="48" y="168" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="115" y="187" text-anchor="middle" font-size="9.5" fill="var(--ink)">模型定价</text>
  <rect x="197" y="168" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="264" y="187" text-anchor="middle" font-size="9.5" fill="var(--ink)">集成 · 审计日志</text>
  <text x="190" y="218" text-anchor="middle" font-size="9" fill="var(--blue)">「这套平台怎么配置」</text>
  <rect x="390" y="40" width="300" height="190" rx="12" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2"/>
  <text x="540" y="62" text-anchor="middle" font-size="12" font-weight="700" fill="var(--purple)">ClickHouse · 数据面</text>
  <text x="540" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">海量 · 追加 · 按维度聚合</text>
  <rect x="410" y="100" width="260" height="34" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="121" text-anchor="middle" font-size="10" fill="var(--ink)">traces（宽事件）</text>
  <rect x="410" y="140" width="260" height="34" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="161" text-anchor="middle" font-size="10" fill="var(--ink)">observations（宽事件）</text>
  <rect x="410" y="180" width="260" height="34" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="201" text-anchor="middle" font-size="10" fill="var(--ink)">scores（宽事件）</text>
</svg>
<div class="figcap"><b>两面分工</b>：<b>Postgres</b> 存「平台怎么配置」——组织/项目/用户、API key、prompt、eval/数据集配置、定价、集成、审计；<b>ClickHouse</b> 存「实际发生了什么」——三张宽事件表。这正是第 3 课「领域形状 vs 物理存储」的宏观版：一个管控制、一个管数据。</div>
</div>

<h2>Postgres 里装的是「控制面」</h2>
<p>打开 <code>schema.prisma</code>，你会看到几十个模型。它们可以按用途归成几组（都用 <code>@@map</code> 映射成 snake_case 表名、用 cuid 做主键）：</p>

<table class="t">
  <tr><th>分组</th><th>主要模型</th><th>管什么</th></tr>
  <tr><td><b>身份与租户</b></td><td class="mono">Organization · Project · User · *Membership · Role · ApiKey</td><td>谁是组织/项目、谁有什么权限、用哪把 key</td></tr>
  <tr><td><b>Prompt</b></td><td class="mono">Prompt · PromptDependency · PromptProtectedLabels</td><td>prompt 的版本化定义与依赖</td></tr>
  <tr><td><b>数据集 / 评估</b></td><td class="mono">Dataset · DatasetItem · DatasetRuns · DatasetRunItems · ScoreConfig · EvalTemplate · JobConfiguration · JobExecution</td><td>测试集、评分配置、评估任务的<strong>定义与编排</strong></td></tr>
  <tr><td><b>模型与计费</b></td><td class="mono">Model · Price · PricingTier</td><td>模型定价表（成本计算的依据，第 16 课）</td></tr>
  <tr><td><b>集成与运维</b></td><td class="mono">*Integration · BatchExport · BatchAction · Media · AuditLog · BackgroundMigration</td><td>对外集成、导出、媒体、审计、后台迁移</td></tr>
</table>

<p>看出规律了吗？这些全是<strong>「配置」和「定义」</strong>，而不是「海量发生的事」。它们数量级在<strong>千到百万</strong>之间，要被<strong>频繁精确地读写单条</strong>
（创建一个项目、改一个 prompt、查一把 key 是否有效），还要<strong>强一致</strong>——这正是关系型数据库 Postgres 的拿手好戏。</p>

<div class="cols">
  <div class="col"><h4>✅ 配置放 Postgres</h4><p>要外键关系（project → 它的 prompt/key/配置）、要事务（一次改多张表要么全成要么全败）、要「改完立刻可读」。这些都是关系型数据库的强项。</p></div>
  <div class="col"><h4>❌ 配置不放 ClickHouse</h4><p>ClickHouse 弱事务、最终一致，且不擅长频繁改单条。把「创建项目立刻可用」交给它，会出现刚建好却查不到的尴尬。配置类数据放它纯属错配。</p></div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">第一层</span><span class="name">身份与租户</span></div><div class="ld">Organization / Project / User / Membership / Role / ApiKey——决定「谁、在哪个项目、有什么权限」。是其它一切的前提。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">第二层</span><span class="name">功能配置</span></div><div class="ld">Prompt、Dataset、ScoreConfig、EvalTemplate/JobConfiguration、Model/Price——各功能的「定义与编排」，都挂在 project 下。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">第三层</span><span class="name">集成与运维</span></div><div class="ld">各种 *Integration、BatchExport/Action、Media、AuditLog、BackgroundMigration——对外连接与平台自身的运维记录。</div></div>
</div>
""")

_ZH9.append(r"""
<h2>Project 是枢纽</h2>
<p>在这几十个模型里，<code>Project</code> 是当之无愧的<strong>中心</strong>。打开它的定义你会发现，它字段不多（id、orgId、name、deletedAt 软删、retentionDays…），
但<strong>挂着几十条关系</strong>——几乎所有其它东西都从属于某个 project：</p>

<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="Organization 包含 Project，Project 作为枢纽连接 API key、成员、数据集、prompt、配置、仪表盘、自动化、集成等">
  <rect x="285" y="20" width="150" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">Organization</text><text x="360" y="52" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">计费 · 成员</text>
  <rect x="290" y="125" width="140" height="48" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2.5"/><text x="360" y="146" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">Project</text><text x="360" y="162" text-anchor="middle" font-size="8.5" fill="var(--muted)">数据边界 · 枢纽</text>
  <line x1="360" y1="60" x2="360" y2="123" stroke="var(--faint)" stroke-width="1.8"/><polygon points="360,123 355,113 365,113" fill="var(--faint)"/>
  <text x="375" y="95" font-size="8.5" fill="var(--faint)">1 : N</text>
  <g font-size="9" fill="var(--ink)" text-anchor="middle">
    <rect x="20" y="100" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="75" y="118">API key</text>
    <rect x="20" y="148" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="75" y="166">成员/权限</text>
    <rect x="20" y="196" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="75" y="214">prompt</text>
    <rect x="160" y="232" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="215" y="250">数据集/eval</text>
    <rect x="300" y="248" width="120" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="360" y="266">模型/定价</text>
    <rect x="450" y="232" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="505" y="250">仪表盘</text>
    <rect x="590" y="196" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="645" y="214">自动化/监控</text>
    <rect x="590" y="148" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="645" y="166">集成</text>
    <rect x="590" y="100" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="645" y="118">媒体/导出</text>
  </g>
  <g stroke="var(--line)" stroke-width="1.3">
    <line x1="290" y1="150" x2="130" y2="114"/><line x1="290" y1="152" x2="130" y2="162"/><line x1="295" y1="165" x2="130" y2="206"/>
    <line x1="320" y1="173" x2="240" y2="232"/><line x1="360" y1="173" x2="360" y2="246"/><line x1="400" y1="173" x2="490" y2="232"/>
    <line x1="430" y1="165" x2="590" y2="206"/><line x1="430" y1="152" x2="590" y2="162"/><line x1="430" y1="150" x2="590" y2="114"/>
  </g>
</svg>
<div class="figcap"><b>Project 是控制面的中心</b>：Organization 之下，几乎一切（API key、成员、prompt、数据集/eval、模型/定价、仪表盘、自动化/监控、集成、媒体/导出）都<b>1:N 地挂在某个 project 上</b>。所以 <b>project 是天然的「数据边界」</b>——一把 API key 属于某个 project，你查的所有数据也都被限定在它所属的 project 里（多租户，下一课展开）。</div>
</div>

<p>「project 是枢纽」还带来两个很实在的后果。其一是<strong>级联</strong>：删掉一个 project，它名下的 key、prompt、数据集、配置会跟着被清理（schema 里很多关系标了 <code>onDelete: Cascade</code>），
这让「删一个项目」变成一个干净的操作，而不是到处留下孤儿数据。其二是<strong>边界即权限</strong>：因为一切都挂在 project 下，鉴权只要回答「你属不属于这个 project」就够了——
这也是下一课多租户、以及第 21 课 tRPC 中间件 <code>protectedProjectProcedure</code> 的工作基础。记住这张「以 project 为中心」的图，后面很多看似分散的功能，其实都挂在它上面。</p>

<h2>为什么 Postgres 里还有 trace 表？</h2>
<p>翻 <code>schema.prisma</code> 时你可能会困惑：怎么还有 <code>LegacyPrismaTrace</code>、<code>LegacyPrismaObservation</code>、<code>LegacyPrismaScore</code>？
不是说遥测都在 ClickHouse 吗？答案在名字里——<strong>Legacy（遗留）</strong>。这是 Langfuse 早期把 trace/observation/score 存在 Postgres 的<strong>历史残留</strong>；
后来为了应对规模，分析数据整体<strong>迁到了 ClickHouse</strong>（这正是第 7、8 课的存在理由）。这些 legacy 模型留着主要是<strong>兼容与迁移</strong>用，不再是热路径。
看到带 <code>Legacy</code> 前缀的，就知道「这是老路，别照着学」。</p>

<h2>API key 与权限（预览）</h2>
<p>身份这组里，<code>ApiKey</code> 有个值得现在就记住的安全细节：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma</span><span class="ln">model ApiKey</span></div>
  <pre class="code">publicKey            <span class="cm">// 公钥，明文</span>
hashedSecretKey      <span class="cm">// 密钥的哈希（不存明文！）</span>
fastHashedSecretKey  <span class="cm">// 快速校验用的哈希</span>
displaySecretKey     <span class="cm">// 只用于 UI 展示的脱敏片段</span>
scope                <span class="cm">// ApiKeyScope，默认 PROJECT</span></pre>
</div>

<p>注意：<strong>密钥本身从不以明文存库</strong>，只存哈希——这样即使数据库泄露，攻击者也拿不到可用的 key。权限则用 <code>Role</code> 枚举表达：
<code>OWNER / ADMIN / MEMBER / VIEWER / NONE</code>，配合组织级与项目级的 membership 决定「谁能在哪个项目做什么」。这套鉴权与权限会在第 49、53 课展开，
这里你只需建立印象：<strong>控制面不仅存「配置」，也存「谁能碰这些配置」。</strong></p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>把「控制面」和「数据面」分到两个数据库，最大的好处是什么？</strong> 是让两者能<strong>各自按自己的规律演进与伸缩</strong>。控制面数据量小、改动要强一致，
  适合一台（或主从）Postgres 稳稳扛住；数据面是洪流，要水平扩展的 ClickHouse 集群。如果硬塞进一个库，要么委屈了配置的强一致，要么拖垮了遥测的吞吐。
  代价是：一次操作有时要<strong>跨两个库</strong>（比如摄取时要回 Postgres 查模型定价、查 prompt 关联）——但这种「读配置、写数据」的跨库协作是<strong>可控且高频缓存</strong>的，
  远比「让一个库同时做好 OLTP 和 OLAP」现实。<strong>按职责分库，让每个库只做自己最擅长的事。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>Postgres = 控制面</strong>：存「平台怎么配置」——org/project/user、API key、prompt、eval/数据集配置、模型定价、集成、审计。定义在 <code>schema.prisma</code>。</li>
    <li><strong>Project 是枢纽</strong>：字段不多但挂着几十条关系，几乎一切都 1:N 属于某个 project——它是天然的<strong>数据边界</strong>（多租户基础）。</li>
    <li><strong>LegacyPrismaTrace/Observation/Score 是历史残留</strong>：分析数据早已迁到 ClickHouse，这些只为兼容/迁移而留。</li>
    <li><strong>API key 存哈希、不存明文</strong>；权限用 <code>Role</code>（OWNER/ADMIN/MEMBER/VIEWER/NONE）+ 组织/项目 membership（第 49、53 课）。</li>
    <li>控制面 vs 数据面，是第 3 课「领域形状 vs 物理存储」的宏观版：<strong>按职责分库</strong>，各做擅长的事。</li>
  </ul>
</div>
""")

_EN9.append(r"""
<p class="lead">
The last two lessons starred ClickHouse (massive telemetry). This one switches to the other half: <strong>Postgres</strong>. If ClickHouse
stores "<strong>what happened</strong>" (trace/observation/score), Postgres stores "<strong>how the platform is configured</strong>" — who
your orgs and projects are, who has access, which API keys exist, which prompts are defined, which eval rules are set, how each model is
priced. This side is the <strong>control plane</strong> — small in volume yet <strong>global in importance</strong>. Its shape is all in
<code>packages/shared/prisma/schema.prisma</code>.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Think of the two stores as a company's two systems: <strong>Postgres</strong> is the <strong>HR/admin system</strong> — who's an
  employee, in which department, with what permissions, under which policies. Not much data, but it must be <strong>accurate, editable,
  instantly effective</strong> (a new hire's permissions must work right away). <strong>ClickHouse</strong> is the <strong>transaction
  ledger</strong> — mountains of records, append-only, used later for monthly/category stats. <strong>You wouldn't write policies into the
  ledger, nor stuff every transaction into HR files</strong> — two kinds of data, two systems, each in its place.
</div>
""")

_EN9.append(r"""
<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Postgres holds the control plane (config/metadata), ClickHouse holds the data plane (telemetry flood)">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">control plane (Postgres) vs data plane (ClickHouse)</text>
  <rect x="30" y="40" width="320" height="190" rx="12" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <text x="190" y="62" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">Postgres · control plane</text>
  <text x="190" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">small but critical · consistent · precise read/write</text>
  <rect x="48" y="92" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="115" y="111" text-anchor="middle" font-size="9.5" fill="var(--ink)">org / project / user</text>
  <rect x="197" y="92" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="264" y="111" text-anchor="middle" font-size="9.5" fill="var(--ink)">API key · permissions</text>
  <rect x="48" y="130" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="115" y="149" text-anchor="middle" font-size="9.5" fill="var(--ink)">prompt definitions</text>
  <rect x="197" y="130" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="264" y="149" text-anchor="middle" font-size="9.5" fill="var(--ink)">eval / dataset config</text>
  <rect x="48" y="168" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="115" y="187" text-anchor="middle" font-size="9.5" fill="var(--ink)">model pricing</text>
  <rect x="197" y="168" width="135" height="30" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="264" y="187" text-anchor="middle" font-size="9.5" fill="var(--ink)">integrations · audit</text>
  <text x="190" y="218" text-anchor="middle" font-size="9" fill="var(--blue)">"how the platform is configured"</text>
  <rect x="390" y="40" width="300" height="190" rx="12" fill="var(--purple-soft)" stroke="var(--purple)" stroke-width="2"/>
  <text x="540" y="62" text-anchor="middle" font-size="12" font-weight="700" fill="var(--purple)">ClickHouse · data plane</text>
  <text x="540" y="80" text-anchor="middle" font-size="9" fill="var(--muted)">huge · append · dimensional aggregation</text>
  <rect x="410" y="100" width="260" height="34" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="121" text-anchor="middle" font-size="10" fill="var(--ink)">traces (wide events)</text>
  <rect x="410" y="140" width="260" height="34" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="161" text-anchor="middle" font-size="10" fill="var(--ink)">observations (wide events)</text>
  <rect x="410" y="180" width="260" height="34" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="540" y="201" text-anchor="middle" font-size="10" fill="var(--ink)">scores (wide events)</text>
</svg>
<div class="figcap"><b>Two halves</b>: <b>Postgres</b> stores "how the platform is configured" — org/project/user, API keys, prompts, eval/dataset config, pricing, integrations, audit; <b>ClickHouse</b> stores "what actually happened" — three wide-event tables. This is the macro version of Lesson 3's "domain shape vs physical storage": one governs control, one governs data.</div>
</div>

<h2>Postgres holds the "control plane"</h2>
<p>Open <code>schema.prisma</code> and you'll see dozens of models. They group by purpose (all map to snake_case tables via
<code>@@map</code>, with cuid primary keys):</p>

<table class="t">
  <tr><th>Group</th><th>Main models</th><th>Governs</th></tr>
  <tr><td><b>Identity & tenancy</b></td><td class="mono">Organization · Project · User · *Membership · Role · ApiKey</td><td>who the org/project is, who has what permission, which key</td></tr>
  <tr><td><b>Prompt</b></td><td class="mono">Prompt · PromptDependency · PromptProtectedLabels</td><td>versioned prompt definitions and dependencies</td></tr>
  <tr><td><b>Datasets / eval</b></td><td class="mono">Dataset · DatasetItem · DatasetRuns · DatasetRunItems · ScoreConfig · EvalTemplate · JobConfiguration · JobExecution</td><td>the <strong>definition & orchestration</strong> of test sets, score configs, eval jobs</td></tr>
  <tr><td><b>Models & billing</b></td><td class="mono">Model · Price · PricingTier</td><td>model pricing tables (basis for cost computation, L16)</td></tr>
  <tr><td><b>Integrations & ops</b></td><td class="mono">*Integration · BatchExport · BatchAction · Media · AuditLog · BackgroundMigration</td><td>outbound integrations, exports, media, audit, background migrations</td></tr>
</table>

<p>See the pattern? These are all <strong>"config" and "definition"</strong>, not "mountains of events". They number in the
<strong>thousands to millions</strong>, are <strong>read/written precisely and often one at a time</strong> (create a project, edit a
prompt, check a key's validity), and need <strong>strong consistency</strong> — exactly the relational database Postgres's forte.</p>

<div class="cols">
  <div class="col"><h4>✅ Config in Postgres</h4><p>You want foreign keys (project → its prompts/keys/config), transactions (a multi-table change all-or-nothing), and "readable right after writing". All relational-DB strengths.</p></div>
  <div class="col"><h4>❌ Config not in ClickHouse</h4><p>ClickHouse has weak transactions, eventual consistency, and dislikes frequent single-row edits. Put "create-project-instantly-usable" there and you'd get the awkward "just created but can't find it". Config there is a mismatch.</p></div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">tier 1</span><span class="name">identity & tenancy</span></div><div class="ld">Organization / Project / User / Membership / Role / ApiKey — decide "who, in which project, with what permission". The prerequisite for everything else.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">tier 2</span><span class="name">feature config</span></div><div class="ld">Prompt, Dataset, ScoreConfig, EvalTemplate/JobConfiguration, Model/Price — each feature's "definition & orchestration", all hung under a project.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">tier 3</span><span class="name">integrations & ops</span></div><div class="ld">the *Integration models, BatchExport/Action, Media, AuditLog, BackgroundMigration — outbound connections and the platform's own ops records.</div></div>
</div>
""")

_EN9.append(r"""
<h2>Project is the hub</h2>
<p>Among these dozens of models, <code>Project</code> is the undeniable <strong>center</strong>. Open its definition and you'll find few
fields (id, orgId, name, deletedAt soft-delete, retentionDays…) but <strong>dozens of relations</strong> — almost everything else belongs
to some project:</p>

<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="Organization contains Project; Project is the hub linking API keys, members, datasets, prompts, configs, dashboards, automations, integrations">
  <rect x="285" y="20" width="150" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="38" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">Organization</text><text x="360" y="52" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">billing · members</text>
  <rect x="290" y="125" width="140" height="48" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2.5"/><text x="360" y="146" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">Project</text><text x="360" y="162" text-anchor="middle" font-size="8.5" fill="var(--muted)">data boundary · hub</text>
  <line x1="360" y1="60" x2="360" y2="123" stroke="var(--faint)" stroke-width="1.8"/><polygon points="360,123 355,113 365,113" fill="var(--faint)"/>
  <text x="377" y="95" font-size="8.5" fill="var(--faint)">1 : N</text>
  <g font-size="9" fill="var(--ink)" text-anchor="middle">
    <rect x="20" y="100" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="75" y="118">API key</text>
    <rect x="20" y="148" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="75" y="166">members/roles</text>
    <rect x="20" y="196" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="75" y="214">prompts</text>
    <rect x="160" y="232" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="215" y="250">datasets/eval</text>
    <rect x="300" y="248" width="120" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="360" y="266">models/pricing</text>
    <rect x="450" y="232" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="505" y="250">dashboards</text>
    <rect x="590" y="196" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="645" y="214">automation</text>
    <rect x="590" y="148" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="645" y="166">integrations</text>
    <rect x="590" y="100" width="110" height="28" rx="6" fill="var(--panel)" stroke="var(--line)"/><text x="645" y="118">media/export</text>
  </g>
  <g stroke="var(--line)" stroke-width="1.3">
    <line x1="290" y1="150" x2="130" y2="114"/><line x1="290" y1="152" x2="130" y2="162"/><line x1="295" y1="165" x2="130" y2="206"/>
    <line x1="320" y1="173" x2="240" y2="232"/><line x1="360" y1="173" x2="360" y2="246"/><line x1="400" y1="173" x2="490" y2="232"/>
    <line x1="430" y1="165" x2="590" y2="206"/><line x1="430" y1="152" x2="590" y2="162"/><line x1="430" y1="150" x2="590" y2="114"/>
  </g>
</svg>
<div class="figcap"><b>Project is the center of the control plane</b>: under Organization, almost everything (API keys, members, prompts, datasets/eval, models/pricing, dashboards, automation, integrations, media/export) hangs off some project <b>1:N</b>. So <b>project is the natural "data boundary"</b> — an API key belongs to a project, and all the data you query is scoped to its project (multi-tenancy, next lesson).</div>
</div>

<p>"Project is the hub" has two very real consequences. One is <strong>cascade</strong>: delete a project and its keys, prompts, datasets and
config are cleaned up with it (many relations are marked <code>onDelete: Cascade</code>), making "delete a project" a clean operation rather
than leaving orphan data everywhere. The other is <strong>boundary equals permission</strong>: because everything hangs under a project,
authorization only needs to answer "do you belong to this project" — the basis for the next lesson's multi-tenancy and for L21's tRPC
middleware <code>protectedProjectProcedure</code>. Remember this "project-centric" picture and many seemingly-scattered features later turn
out to hang off it.</p>

<h2>Why are there trace tables in Postgres?</h2>
<p>Browsing <code>schema.prisma</code> you may be puzzled: why are there <code>LegacyPrismaTrace</code>, <code>LegacyPrismaObservation</code>,
<code>LegacyPrismaScore</code>? Isn't telemetry all in ClickHouse? The answer is in the name — <strong>Legacy</strong>. This is a
<strong>historical remnant</strong> of Langfuse's early days storing trace/observation/score in Postgres; later, to handle scale, the
analytical data <strong>moved to ClickHouse</strong> (the very reason for Lessons 7 and 8). These legacy models remain mainly for
<strong>compatibility and migration</strong> — no longer the hot path. See a <code>Legacy</code> prefix and you know "that's the old way,
don't copy it".</p>

<h2>API keys & permissions (preview)</h2>
<p>In the identity group, <code>ApiKey</code> has a security detail worth remembering now:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma</span><span class="ln">model ApiKey</span></div>
  <pre class="code">publicKey            <span class="cm">// public key, plaintext</span>
hashedSecretKey      <span class="cm">// hash of the secret (no plaintext!)</span>
fastHashedSecretKey  <span class="cm">// a hash for fast verification</span>
displaySecretKey     <span class="cm">// a masked fragment, UI display only</span>
scope                <span class="cm">// ApiKeyScope, default PROJECT</span></pre>
</div>

<p>Note: <strong>the secret is never stored in plaintext</strong>, only hashed — so even a DB leak yields no usable key. Permissions use the
<code>Role</code> enum: <code>OWNER / ADMIN / MEMBER / VIEWER / NONE</code>, combined with org-level and project-level memberships to decide
"who can do what in which project". Auth and permissions get their own lessons (L49, L53); for now just register the impression:
<strong>the control plane stores not only "config" but "who may touch that config".</strong></p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>What's the biggest payoff of splitting "control plane" and "data plane" into two databases?</strong> Letting each
  <strong>evolve and scale by its own rules</strong>. The control plane is small and needs strong consistency — fine for a single (or
  primary/replica) Postgres; the data plane is a flood needing a horizontally-scalable ClickHouse cluster. Force them into one store and
  you either shortchange config consistency or crush telemetry throughput. The cost: some operations span <strong>two stores</strong> (e.g.
  ingestion reads model pricing and prompt links back from Postgres) — but this "read config, write data" cross-store collaboration is
  <strong>controllable and heavily cached</strong>, far more realistic than "making one store great at both OLTP and OLAP". <strong>Split
  by responsibility; let each store do only what it's best at.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Postgres = control plane</strong>: stores "how the platform is configured" — org/project/user, API keys, prompts, eval/dataset config, model pricing, integrations, audit. Defined in <code>schema.prisma</code>.</li>
    <li><strong>Project is the hub</strong>: few fields but dozens of relations; almost everything belongs 1:N to a project — the natural <strong>data boundary</strong> (multi-tenancy basis).</li>
    <li><strong>LegacyPrismaTrace/Observation/Score are historical remnants</strong>: analytical data long moved to ClickHouse; these remain only for compatibility/migration.</li>
    <li><strong>API keys are stored hashed, never plaintext</strong>; permissions use <code>Role</code> (OWNER/ADMIN/MEMBER/VIEWER/NONE) + org/project memberships (L49, L53).</li>
    <li>Control plane vs data plane is the macro version of Lesson 3's "domain shape vs physical storage": <strong>split by responsibility</strong>, each doing what it's best at.</li>
  </ul>
</div>
""")

LESSON_09 = {"zh": "\n".join(_ZH9), "en": "\n".join(_EN9)}


# ══════════════════════════════════════════════════════════════════════
# L10 · 多租户：org → project → environment / Multi-tenancy
# ══════════════════════════════════════════════════════════════════════
_ZH10 = []
_EN10 = []

_ZH10.append(r"""
<p class="lead">
上一课说 <code>project</code> 是枢纽、是「数据边界」。这一课把这件事讲透：Langfuse 是个<strong>多租户</strong>平台——同一套部署要同时服务成千上万个互不相干的团队，
它靠<strong>三层嵌套</strong>把大家的数据干净地隔开：<strong>organization（组织）→ project（项目）→ environment（环境）</strong>。
理解这三层，你就明白了「为什么你只看得到自己的数据」「为什么 ClickHouse 排序键非要以 project_id 打头」。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把多租户想成<strong>一栋写字楼</strong>：<strong>organization</strong> 是<strong>租下楼层的公司</strong>——签合同、付账单、管自己的员工（成员与计费在这一层）；
  <strong>project</strong> 是公司里的<strong>一个部门</strong>，有独立的办公区和门禁，部门的东西不会跑到别的部门去；<strong>environment</strong> 则是部门内部再隔出的
  「<strong>正式区 / 测试区</strong>」——同一个部门的人，把线上数据和测试数据分开摆，互不干扰。大家可能<strong>同在一栋楼</strong>（同一套部署、同一个数据库），
  但靠层层<strong>门禁</strong>谁也串不了门。
</div>
""")

_ZH10.append(r"""
<div class="fig">
<svg viewBox="0 0 720 270" role="img" aria-label="organization 包含多个 project，每个 project 内再分 production/staging/development 环境">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">三层嵌套：组织 → 项目 → 环境</text>
  <rect x="30" y="36" width="660" height="220" rx="13" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="48" y="58" font-size="11.5" font-weight="700" fill="var(--accent-ink)">Organization · 计费 + 成员（合同主体）</text>
  <rect x="48" y="70" width="300" height="172" rx="11" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="64" y="92" font-size="11" font-weight="700" fill="var(--blue)">Project A · 数据边界</text>
  <rect x="64" y="104" width="268" height="40" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="198" y="128" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: production</text>
  <rect x="64" y="150" width="130" height="36" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="129" y="172" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: staging</text>
  <rect x="202" y="150" width="130" height="36" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="267" y="172" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: development</text>
  <text x="198" y="212" text-anchor="middle" font-size="9" fill="var(--muted)">一个 project 内可有多个 environment</text>
  <rect x="372" y="70" width="300" height="172" rx="11" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="388" y="92" font-size="11" font-weight="700" fill="var(--purple)">Project B · 另一个数据边界</text>
  <rect x="388" y="104" width="268" height="40" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="522" y="128" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: production</text>
  <rect x="388" y="150" width="268" height="36" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="522" y="172" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: default</text>
  <text x="522" y="212" text-anchor="middle" font-size="9" fill="var(--muted)">Project B 看不到 Project A 的任何数据</text>
</svg>
<div class="figcap"><b>三层嵌套</b>：一个 <b>organization</b> 下有多个 <b>project</b>，每个 project 内可再分多个 <b>environment</b>（如 production / staging / development，默认 <code>default</code>）。组织管计费与成员，<b>project 是硬数据边界</b>，environment 是项目内的软切片。</div>
</div>

<h2>三层各管什么</h2>
<table class="t">
  <tr><th>层级</th><th>管什么</th><th>隔离强度</th></tr>
  <tr><td><b>Organization 组织</b></td><td>计费、成员、SSO、组织级 API key</td><td>最外层的「账户」边界</td></tr>
  <tr><td><b>Project 项目</b></td><td>实际数据归属：trace/observation/score、prompt、配置全挂在某 project 下</td><td><strong>硬隔离</strong>：跨 project 互不可见</td></tr>
  <tr><td><b>Environment 环境</b></td><td>同一 project 内区分 production / staging / development 等</td><td><strong>软切片</strong>：同 project 内可一起查、也可按环境过滤</td></tr>
</table>

<p>关键区别在最后两层：<strong>project 是「硬边界」</strong>——你拿着某 project 的 key，<strong>根本看不到</strong>别的 project 的数据；
而 <strong>environment 是「软切片」</strong>——它在同一个 project 内部，把线上和测试的数据<strong>贴上标签</strong>分开，你既能只看 production，也能把几个环境放一起比。
为什么这么设计？因为「不同团队的数据绝不能串」是<strong>安全红线</strong>（硬隔离），而「线上 vs 测试」只是同一团队<strong>自己的视图偏好</strong>（软切片），强度不同，待遇也不同。</p>

<p>举个具体场景体会这三层。一家公司（<strong>organization</strong>）在 Langfuse 上签约、付费、邀请了 5 名工程师做成员。他们开了两个项目（<strong>project</strong>）：
「客服机器人」和「文档问答」。这两个项目的数据<strong>互不可见</strong>——查客服机器人时绝不会混进文档问答的 trace。在「客服机器人」项目内，他们又用
<strong>environment</strong> 把<strong>线上流量</strong>（production）和<strong>压测/调试流量</strong>（staging）分开，于是看线上成本时不会被压测数据污染，
但需要时也能把两个环境放一起对比。最外层的「公司」只关心<strong>账单和谁是成员</strong>，不直接持有数据；数据全都落在某个 project + environment 上。
这套「组织管钱和人、项目管数据、环境管视图」的分工，就是多租户的全部骨架。</p>
""")

_ZH10.append(r"""
<h2>project_id 是硬隔离键，贯穿始终</h2>
<p>多租户隔离<strong>不是事后加一个 <code>WHERE project_id = ?</code> 过滤这么简单</strong>。在 Langfuse 里，<code>project_id</code> 是一条<strong>贯穿全链路</strong>的主线：</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="project_id 从 API key 解析出来，写入时落到每行，ClickHouse 排序键以它打头，查询时据它定位">
  <rect x="20" y="80" width="150" height="54" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">API key</text><text x="95" y="120" text-anchor="middle" font-size="8.5" fill="var(--muted)">解析出 project_id</text>
  <rect x="200" y="80" width="150" height="54" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="275" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">写入</text><text x="275" y="120" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">每行都带 project_id</text>
  <rect x="380" y="80" width="160" height="54" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="460" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="460" y="120" text-anchor="middle" font-size="8.5" fill="var(--muted)">ORDER BY project_id 打头</text>
  <rect x="570" y="80" width="130" height="54" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="635" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">查询</text><text x="635" y="120" text-anchor="middle" font-size="8.5" fill="var(--muted)">只扫该 project 区间</text>
  <line x1="170" y1="107" x2="198" y2="107" stroke="var(--faint)" stroke-width="2"/><polygon points="198,107 189,102 189,112" fill="var(--faint)"/>
  <line x1="350" y1="107" x2="378" y2="107" stroke="var(--faint)" stroke-width="2"/><polygon points="378,107 369,102 369,112" fill="var(--faint)"/>
  <line x1="540" y1="107" x2="568" y2="107" stroke="var(--faint)" stroke-width="2"/><polygon points="568,107 559,102 559,112" fill="var(--faint)"/>
  <text x="360" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">project_id：一把钥匙，串起鉴权·写入·存储·查询</text>
  <text x="360" y="170" text-anchor="middle" font-size="9.5" fill="var(--faint)">隔离不是“查时过滤”，而是把 project_id 焊进了排序键——隔离即定位，定位即高效</text>
</svg>
<div class="figcap"><b>project_id 贯穿全链路</b>：鉴权时从 API key 解析出 project_id（第 9 课 key 属于某 project）；写入时每行都带上它；ClickHouse 的排序键<b>以 project_id 打头</b>（第 8 课）；查询时据它定位到连续区间。所以隔离<b>不是</b>事后过滤，而是写进了物理排布——隔离和「查得快」是同一件事。</div>
</div>

<p>这条「project_id 贯穿全链路」的设计，最大的价值是<strong>把安全从「靠程序员记得写过滤」变成「靠结构保证」</strong>。想想看：如果隔离只靠每个查询都记得加 <code>WHERE project_id = ?</code>，
那只要有一处查询忘了写、或写错了，就可能让 A 公司看到 B 公司的数据——这种 bug 在多租户系统里是<strong>灾难级</strong>的。Langfuse 的做法是把 project_id 焊进存储与鉴权的底层：
仓储层的读取 API <strong>统一要求</strong>传入 project_id，tRPC 的 <code>protectedProjectProcedure</code> 在中间件里<strong>先</strong>校验你属不属于这个 project（第 21 课）。
于是「越权看别人数据」不是「容易写错」，而是<strong>压根没有那条路</strong>。这就是「安全做进结构」与「安全靠自觉」的本质区别。</p>

<h2>environment：项目内的软切片</h2>
<p>environment 是后来加上的一层。看它在 ClickHouse 里的样子——三张宽事件表都加了一个 <code>environment</code> 列：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">clickhouse/migrations/unclustered/0008_add_environments_column.up.sql</span><span class="ln">ALTER</span></div>
  <pre class="code">ALTER TABLE traces       ADD COLUMN environment LowCardinality(String) DEFAULT <span class="st">'default'</span> AFTER project_id;
ALTER TABLE observations ADD COLUMN environment LowCardinality(String) DEFAULT <span class="st">'default'</span> AFTER project_id;
ALTER TABLE scores       ADD COLUMN environment LowCardinality(String) DEFAULT <span class="st">'default'</span> AFTER project_id;</pre>
</div>

<p>三个细节值得注意：① 类型是 <code>LowCardinality(String)</code>——环境名翻来覆去就那么几个（prod/staging/dev），低基数编码又省空间又查得快；
② 默认值 <code>'default'</code>——你不显式指定环境时，数据自动落到 <code>default</code>，向后兼容（老数据天然属于 default）；③ 位置 <code>AFTER project_id</code>——
这只是让它在表结构里<strong>紧挨 project_id 排列（纯粹是列的书写顺序，便于阅读）</strong>，<strong>注意它并没有进入排序键</strong>。所以和 project_id 不同，environment 本质是行上的一个
<strong>普通过滤列</strong>，也就是软切片：想按环境过滤就在查询里加个条件，不想分就忽略它。</p>

<p>这正好对照出 project 与 environment 隔离机制的不同：<strong>project_id 焊进了排序键</strong>（隔离即定位，结构性安全），而 <strong>environment 只是一个普通列</strong>（查询时过滤）。
这也合理——硬隔离要靠结构保证，软切片只是个方便的视图维度，不必、也不该动用排序键这种重武器。</p>

<div class="cols">
  <div class="col"><h4>🔒 project = 硬隔离</h4><p>安全红线：不同 project 的数据<strong>绝不可见</strong>。焊进排序键前缀 + API key 归属，从存储到鉴权层层保证。</p></div>
  <div class="col"><h4>🏷️ environment = 软切片</h4><p>视图偏好：同一 project 内给数据贴 prod/staging/dev 标签，<strong>可分可合</strong>，只是查询时的一个过滤维度。</p></div>
</div>

<h2>一次请求怎么定位租户</h2>
<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>带上凭证</h4><p>SDK 用 API key（写入），或用户登录后带 session（读取）发起请求。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>解析出 project</h4><p>服务端从 key/session 解析出「这是哪个 project」，并校验是否有权限（第 9 课 ApiKey、第 21 课 <code>protectedProjectProcedure</code>）。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>所有读写都锁定该 project</h4><p>写入时 project_id 落到每行；查询时 project_id 进排序键前缀。你<strong>没有办法</strong>越过它看到别的 project。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>可选：按 environment 再切</h4><p>在该 project 内，按需用 environment 过滤出 prod / staging。</p></div></div>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么把 project_id 焊进排序键，而不是当成一个普通的过滤列？</strong> 因为这样<strong>「隔离」和「高效」就成了同一件事</strong>。如果 project_id 只是个普通列，
  那「只看我的项目」就是一次全表过滤，海量数据下既慢又危险（万一过滤写漏了，就串了租户）。把它放进排序键<strong>最前面</strong>，同一 project 的数据物理相邻，
  「只看我的项目」退化成「扫一段连续区间」——又快又<strong>结构性地</strong>不可能看到别人。代价是排序键一旦定了就难改、且要求几乎所有查询都带上 project_id（这正是仓储层 API 的统一约定）。
  <strong>把多租户隔离做成存储结构的一部分，而不是一道可能写漏的过滤。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>三层嵌套</strong>：organization（计费/成员）⊃ project（数据边界）⊃ environment（项目内 prod/staging/dev）。</li>
    <li><strong>project = 硬隔离</strong>（跨项目绝不可见），<strong>environment = 软切片</strong>（同项目内可分可合的标签）。</li>
    <li><strong>project_id 贯穿全链路</strong>：从 API key 解析 → 写入每行 → ClickHouse 排序键打头 → 查询定位。隔离<strong>不是事后过滤，而是焊进排序键</strong>。</li>
    <li><code>environment</code> 列：<code>LowCardinality(String) DEFAULT 'default' AFTER project_id</code>（第 8 课迁移 0008），低基数、向后兼容、紧贴 project_id。</li>
    <li>取舍：把隔离做进存储结构 → 隔离与高效合一、且结构性安全；代价是排序键难改、查询须带 project_id。</li>
  </ul>
</div>
""")

_EN10.append(r"""
<p class="lead">
Last lesson called <code>project</code> the hub and the "data boundary". This lesson makes that concrete: Langfuse is a
<strong>multi-tenant</strong> platform — one deployment serves thousands of unrelated teams at once, isolating their data cleanly via
<strong>three nesting levels</strong>: <strong>organization → project → environment</strong>. Grasp these three and you understand
"why you only see your own data" and "why the ClickHouse ordering key must start with project_id".
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Picture multi-tenancy as an <strong>office building</strong>: the <strong>organization</strong> is the <strong>company renting a
  floor</strong> — signs the lease, pays the bills, manages its staff (members and billing live here); the <strong>project</strong> is a
  <strong>department</strong> with its own area and access control, whose stuff never wanders into another department; the
  <strong>environment</strong> is a further "<strong>production / test area</strong>" split inside the department — the same people keep
  live and test data apart. Everyone may be <strong>in one building</strong> (one deployment, one database), but layered <strong>access
  controls</strong> keep them from crossing over.
</div>
""")

_EN10.append(r"""
<div class="fig">
<svg viewBox="0 0 720 270" role="img" aria-label="an organization contains multiple projects, each project splitting into production/staging/development environments">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">three nesting levels: org → project → environment</text>
  <rect x="30" y="36" width="660" height="220" rx="13" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="48" y="58" font-size="11.5" font-weight="700" fill="var(--accent-ink)">Organization · billing + members (the lease holder)</text>
  <rect x="48" y="70" width="300" height="172" rx="11" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="64" y="92" font-size="11" font-weight="700" fill="var(--blue)">Project A · data boundary</text>
  <rect x="64" y="104" width="268" height="40" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="198" y="128" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: production</text>
  <rect x="64" y="150" width="130" height="36" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="129" y="172" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: staging</text>
  <rect x="202" y="150" width="130" height="36" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="267" y="172" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: development</text>
  <text x="198" y="212" text-anchor="middle" font-size="9" fill="var(--muted)">a project may have multiple environments</text>
  <rect x="372" y="70" width="300" height="172" rx="11" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="388" y="92" font-size="11" font-weight="700" fill="var(--purple)">Project B · another data boundary</text>
  <rect x="388" y="104" width="268" height="40" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="522" y="128" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: production</text>
  <rect x="388" y="150" width="268" height="36" rx="7" fill="var(--panel)" stroke="var(--line)"/><text x="522" y="172" text-anchor="middle" font-size="9.5" fill="var(--ink)">env: default</text>
  <text x="522" y="212" text-anchor="middle" font-size="9" fill="var(--muted)">Project B sees none of Project A's data</text>
</svg>
<div class="figcap"><b>Three nesting levels</b>: one <b>organization</b> holds multiple <b>projects</b>, each project may split into multiple <b>environments</b> (e.g. production / staging / development, default <code>default</code>). The org manages billing and members, the <b>project is the hard data boundary</b>, and the environment is a soft slice within a project.</div>
</div>

<h2>What each level governs</h2>
<table class="t">
  <tr><th>Level</th><th>Governs</th><th>Isolation strength</th></tr>
  <tr><td><b>Organization</b></td><td>billing, members, SSO, org-level API keys</td><td>the outer "account" boundary</td></tr>
  <tr><td><b>Project</b></td><td>where data actually belongs: trace/observation/score, prompts, config all hang under a project</td><td><strong>hard isolation</strong>: invisible across projects</td></tr>
  <tr><td><b>Environment</b></td><td>distinguishes production / staging / development within one project</td><td><strong>soft slice</strong>: queryable together or filtered by env</td></tr>
</table>

<p>The key distinction is the last two: <strong>project is a "hard boundary"</strong> — hold one project's key and you simply
<strong>cannot see</strong> another project's data; <strong>environment is a "soft slice"</strong> — within one project it <strong>tags</strong>
live vs test data apart, so you can view only production, or compare several environments together. Why? Because "different teams' data must
never mix" is a <strong>security red line</strong> (hard isolation), while "live vs test" is just one team's <strong>own view preference</strong>
(soft slice) — different strengths, different treatment.</p>

<p>A concrete scenario for all three levels. A company (<strong>organization</strong>) signs up and pays on Langfuse, inviting 5 engineers as
members. They open two projects (<strong>project</strong>): "support bot" and "doc Q&amp;A". The two projects' data is <strong>mutually
invisible</strong> — querying the support bot never mixes in doc-Q&amp;A traces. Within "support bot" they use <strong>environment</strong> to
separate <strong>live traffic</strong> (production) from <strong>load-test/debug traffic</strong> (staging), so live cost isn't polluted by
load-test data — yet they can compare the two environments together when needed. The outer "company" cares only about <strong>the bill and
who's a member</strong>, holding no data directly; all data lands on some project + environment. This "org manages money and people, project
manages data, environment manages views" division is the entire skeleton of multi-tenancy.</p>
""")

_EN10.append(r"""
<h2>project_id is the hard isolation key, threaded throughout</h2>
<p>Multi-tenant isolation is <strong>not as simple as adding a <code>WHERE project_id = ?</code> filter afterward</strong>. In Langfuse,
<code>project_id</code> is a thread running <strong>through the whole pipeline</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="project_id is parsed from the API key, stamped on every row at write, leads the ClickHouse ordering key, and locates data at query time">
  <rect x="20" y="80" width="150" height="54" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">API key</text><text x="95" y="120" text-anchor="middle" font-size="8.5" fill="var(--muted)">resolves project_id</text>
  <rect x="200" y="80" width="150" height="54" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="275" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">write</text><text x="275" y="120" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">every row carries project_id</text>
  <rect x="380" y="80" width="160" height="54" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="460" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--purple)">ClickHouse</text><text x="460" y="120" text-anchor="middle" font-size="8.5" fill="var(--muted)">ORDER BY project_id first</text>
  <rect x="570" y="80" width="130" height="54" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="635" y="103" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">query</text><text x="635" y="120" text-anchor="middle" font-size="8.5" fill="var(--muted)">scan only that project's range</text>
  <line x1="170" y1="107" x2="198" y2="107" stroke="var(--faint)" stroke-width="2"/><polygon points="198,107 189,102 189,112" fill="var(--faint)"/>
  <line x1="350" y1="107" x2="378" y2="107" stroke="var(--faint)" stroke-width="2"/><polygon points="378,107 369,102 369,112" fill="var(--faint)"/>
  <line x1="540" y1="107" x2="568" y2="107" stroke="var(--faint)" stroke-width="2"/><polygon points="568,107 559,102 559,112" fill="var(--faint)"/>
  <text x="360" y="40" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">project_id: one key threading auth · write · storage · query</text>
  <text x="360" y="170" text-anchor="middle" font-size="9.5" fill="var(--faint)">isolation isn't "filter at query time" — project_id is welded into the ordering key: isolate = locate = fast</text>
</svg>
<div class="figcap"><b>project_id threads the whole pipeline</b>: auth resolves project_id from the API key (L09: a key belongs to a project); writes stamp it on every row; ClickHouse's ordering key <b>starts with project_id</b> (L08); queries locate the contiguous range by it. So isolation is <b>not</b> an afterthought filter — it's baked into the physical layout; isolation and "fast" are the same thing.</div>
</div>

<p>This "project_id threads the whole pipeline" design's biggest value is turning <strong>security from "the programmer remembers to filter"
into "the structure guarantees it"</strong>. Consider: if isolation relied on every query remembering to add <code>WHERE project_id = ?</code>,
then one forgotten or wrong filter could let company A see company B's data — a <strong>catastrophic</strong> bug in a multi-tenant system.
Langfuse instead welds project_id into the storage and auth foundations: the repository read APIs <strong>uniformly require</strong> a
project_id, and tRPC's <code>protectedProjectProcedure</code> middleware checks <strong>first</strong> whether you belong to this project
(L21). So "see another tenant's data by accident" isn't "easy to get wrong" — <strong>there simply is no such path</strong>. That's the
essential difference between "security in the structure" and "security by discipline".</p>

<h2>environment: a soft slice within a project</h2>
<p>environment was added later. Here's how it looks in ClickHouse — all three wide-event tables gained an <code>environment</code> column:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">clickhouse/migrations/unclustered/0008_add_environments_column.up.sql</span><span class="ln">ALTER</span></div>
  <pre class="code">ALTER TABLE traces       ADD COLUMN environment LowCardinality(String) DEFAULT <span class="st">'default'</span> AFTER project_id;
ALTER TABLE observations ADD COLUMN environment LowCardinality(String) DEFAULT <span class="st">'default'</span> AFTER project_id;
ALTER TABLE scores       ADD COLUMN environment LowCardinality(String) DEFAULT <span class="st">'default'</span> AFTER project_id;</pre>
</div>

<p>Three details: (1) the type is <code>LowCardinality(String)</code> — env names are a small fixed set (prod/staging/dev), and
low-cardinality encoding saves space and speeds queries; (2) the default <code>'default'</code> — without an explicit environment, data lands
in <code>default</code>, backward-compatible (old data naturally belongs to default); (3) the position <code>AFTER project_id</code> — this only
places it <strong>right after project_id in the table's column layout (purely a cosmetic column order for readability)</strong>; <strong>note it
is NOT added to the ordering key</strong>. So unlike project_id, environment is essentially a <strong>plain filter column</strong> on the row — a
soft slice: add a condition to filter by env, or ignore it to see them together.</p>

<p>This neatly contrasts the two isolation mechanisms: <strong>project_id is welded into the ordering key</strong> (isolate = locate,
structurally safe), while <strong>environment is just an ordinary column</strong> (filtered at query time). Reasonably so — hard isolation must
be guaranteed by structure, while a soft slice is just a convenient view dimension that needn't (and shouldn't) wield the heavy weapon of the
ordering key.</p>

<div class="cols">
  <div class="col"><h4>🔒 project = hard isolation</h4><p>A security red line: different projects' data is <strong>never visible</strong> to each other. Welded into the ordering-key prefix + API-key ownership, guaranteed from storage to auth.</p></div>
  <div class="col"><h4>🏷️ environment = soft slice</h4><p>A view preference: within one project, tag data prod/staging/dev — <strong>separable or combinable</strong>, just one filter dimension at query time.</p></div>
</div>

<h2>How one request resolves the tenant</h2>
<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>carry a credential</h4><p>the SDK uses an API key (writes), or a logged-in user carries a session (reads), to make a request.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>resolve the project</h4><p>the server resolves "which project" from the key/session and checks access (L09 ApiKey, L21 <code>protectedProjectProcedure</code>).</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>all reads/writes lock to that project</h4><p>writes stamp project_id on every row; queries put project_id in the ordering-key prefix. You <strong>cannot</strong> bypass it to see another project.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>optional: slice by environment</h4><p>within that project, filter prod / staging by environment as needed.</p></div></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why weld project_id into the ordering key instead of treating it as an ordinary filter column?</strong> Because that makes
  <strong>"isolation" and "efficiency" the same thing</strong>. If project_id were just a column, "see only my project" would be a full-table
  filter — slow at scale and dangerous (miss the filter once and you leak across tenants). Put it <strong>first</strong> in the ordering key
  and one project's data is physically adjacent, so "see only my project" degrades to "scan a contiguous range" — fast and
  <strong>structurally</strong> unable to see others. The cost: the ordering key is hard to change once set, and nearly every query must carry
  project_id (the repository layer's uniform contract). <strong>Make multi-tenant isolation part of the storage structure, not a filter you
  might forget.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Three nesting levels</strong>: organization (billing/members) ⊃ project (data boundary) ⊃ environment (prod/staging/dev within a project).</li>
    <li><strong>project = hard isolation</strong> (never visible across projects), <strong>environment = soft slice</strong> (a tag separable/combinable within a project).</li>
    <li><strong>project_id threads the whole pipeline</strong>: resolved from the API key → stamped on every row → leads the ClickHouse ordering key → locates queries. Isolation is <strong>welded into the ordering key, not an afterthought filter</strong>.</li>
    <li>the <code>environment</code> column: <code>LowCardinality(String) DEFAULT 'default' AFTER project_id</code> (migration 0008, L08) — low-cardinality, backward-compatible, right after project_id.</li>
    <li>Tradeoff: baking isolation into storage → isolation and efficiency become one, and it's structurally safe; the cost is a hard-to-change ordering key and project_id required on queries.</li>
  </ul>
</div>
""")

LESSON_10 = {"zh": "\n".join(_ZH10), "en": "\n".join(_EN10)}


# ══════════════════════════════════════════════════════════════════════
# L11 · 部署拓扑与依赖 / Deployment topology
# ══════════════════════════════════════════════════════════════════════
_ZH11 = []
_EN11 = []

_ZH11.append(r"""
<p class="lead">
第二部分讲了数据模型与存储「<strong>是什么</strong>」。这一课收尾，讲「<strong>跑起来要什么</strong>」——自托管一套 Langfuse，你实际要启动哪些容器、它们怎么连。
答案很干净：<strong>2 个应用容器 + 4 个基础设施</strong>，全写在根目录的 <code>docker-compose.yml</code> 里。把前面几课抽象的架构图，落到这张具体的「装箱清单」上，
你对 Langfuse 的「形」就完整了。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把一套 Langfuse 部署想成开一家餐厅需要的几个「房间」：<strong>前厅</strong>（web）接待客人、上菜单、端菜；<strong>后厨</strong>（worker）在后面默默备菜、洗碗、处理大单；
  <strong>冷库</strong>（ClickHouse）存海量食材（遥测）；<strong>文件柜</strong>（Postgres）放菜单和员工档案（配置）；<strong>传菜口</strong>（Redis）排订单（队列）；
  <strong>大仓库</strong>（S3/MinIO）堆又大又不常用的存货（原件、媒体）。  少了哪个房间，餐厅都开不利索——但凑齐这 6 个，店就能营业了。这一课就带你认全这六个「房间」，看清它们各自是谁、为什么少不了、又怎么连成一家能营业的店。
</div>
""")

_ZH11.append(r"""
<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="docker-compose 拓扑：langfuse-web 与 langfuse-worker 两个应用，连接 postgres、clickhouse、redis、minio 四个基础设施">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">docker-compose 拓扑：2 应用 + 4 基础设施</text>
  <rect x="120" y="40" width="200" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="220" y="60" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">langfuse-web</text><text x="220" y="78" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">langfuse/langfuse:3 · UI+API</text>
  <rect x="400" y="40" width="200" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="500" y="60" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">langfuse-worker</text><text x="500" y="78" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">langfuse-worker:3 · 后台</text>
  <rect x="30" y="170" width="150" height="64" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="105" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--blue)">postgres:17</text><text x="105" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">配置/元数据</text>
  <rect x="195" y="170" width="150" height="64" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="270" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--purple)">clickhouse-server</text><text x="270" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">宽事件</text>
  <rect x="360" y="170" width="150" height="64" rx="10" fill="var(--red-soft)" stroke="var(--red)"/><text x="435" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--red)">redis:7</text><text x="435" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">队列 + 缓存</text>
  <rect x="525" y="170" width="165" height="64" rx="10" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="607" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--amber)">minio（S3 兼容）</text><text x="607" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">事件底稿·媒体</text>
  <g stroke="var(--line)" stroke-width="1.3">
    <line x1="190" y1="90" x2="110" y2="168"/><line x1="210" y1="90" x2="265" y2="168"/><line x1="240" y1="90" x2="430" y2="168"/>
    <line x1="470" y1="90" x2="280" y2="168"/><line x1="490" y1="90" x2="440" y2="168"/><line x1="520" y1="90" x2="600" y2="168"/><line x1="450" y1="90" x2="120" y2="168"/>
  </g>
  <text x="360" y="262" text-anchor="middle" font-size="9" fill="var(--faint)">每个基础设施都有自己的 named volume 做持久化（pg / clickhouse data+logs / redis / minio）</text>
  <text x="360" y="282" text-anchor="middle" font-size="9" fill="var(--faint)">web 偏读 PG+CH；worker 偏写 CH/S3、消费 Redis 队列（连线为示意）</text>
</svg>
<div class="figcap"><b>自托管装箱清单</b>：两个应用容器 <b>langfuse-web</b>（langfuse/langfuse:3）与 <b>langfuse-worker</b>（langfuse/langfuse-worker:3），加四个基础设施 <b>postgres:17 · clickhouse-server · redis:7 · minio</b>（S3 兼容）。每个基础设施配一个 named volume 持久化。这正是第 5、7 课架构图的「实体版」。</div>
</div>

<h2>最小自托管栈：2 应用 + 4 基础设施</h2>
<table class="t">
  <tr><th>服务</th><th>镜像</th><th>角色</th></tr>
  <tr><td class="mono">langfuse-web</td><td class="mono">langfuse/langfuse:3</td><td>面向用户：UI + tRPC + 公共 REST API（摄取入口）</td></tr>
  <tr><td class="mono">langfuse-worker</td><td class="mono">langfuse/langfuse-worker:3</td><td>后台：消费队列、合并写入、评估、导出…</td></tr>
  <tr><td class="mono">postgres</td><td class="mono">postgres:17</td><td>控制面：配置/元数据（第 9 课）</td></tr>
  <tr><td class="mono">clickhouse</td><td class="mono">clickhouse/clickhouse-server</td><td>数据面：宽事件表（第 8 课）</td></tr>
  <tr><td class="mono">redis</td><td class="mono">redis:7</td><td>BullMQ 队列 + 缓存</td></tr>
  <tr><td class="mono">minio</td><td class="mono">chainguard/minio</td><td>S3 兼容对象存储（本地替身）：事件底稿·媒体·导出</td></tr>
</table>

<p>注意 <strong>minio</strong>：它是一个<strong>兼容 S3 协议</strong>的开源对象存储，在本地/自托管时充当 AWS S3 的<strong>替身</strong>。这意味着同一套代码，
在云上用真 S3、在自托管用 MinIO，<strong>应用层完全无感</strong>——这正是「面向接口（S3 协议）而非实现」带来的可移植性。<strong>四个基础设施容器各自挂 named volume</strong> 做持久化
（postgres / clickhouse data+logs / redis / minio），而 <strong>web 与 worker 无状态、不挂卷</strong>；所以你 <code>docker compose down</code> 再 <code>up</code>，数据还在。</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">应用层</span><span class="name">web · worker</span></div><div class="ld">无状态的业务容器，可随时重启、按需扩容。它们启动后连上下面的存储干活。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">数据层</span><span class="name">postgres · clickhouse</span></div><div class="ld">两类数据库：控制面（配置）与数据面（遥测）。有状态，靠 named volume 持久化，是整套系统的根基。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">支撑层</span><span class="name">redis · minio</span></div><div class="ld">队列/缓存与对象存储。让摄取异步、让大字段/媒体有处可放。同样有状态、需持久化。</div></div>
</div>

<p>这三层有个朴素的启动次序：<strong>先把数据层与支撑层拉起、等它们健康，再启动应用层</strong>——所以 compose 里应用容器会 <code>depends_on</code> 这些基础设施并等待其 healthcheck。
理解这个分层，你 debug 部署问题时就有了方向：连不上库先看数据层、摄取不动先看 Redis、媒体存不进先看 MinIO。</p>
""")

_ZH11.append(r"""
<h2>web 与 worker：分工与协作</h2>
<p>两个应用容器是 Langfuse 的「左右手」。它们形态相似（都连同一套存储），但<strong>职责相反</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="web 容器面向用户、低延迟、可随时重启；worker 容器啃重活、可重试、按队列伸缩；二者通过 Redis 队列解耦">
  <rect x="40" y="50" width="260" height="120" rx="12" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="170" y="74" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">web</text>
  <text x="170" y="96" text-anchor="middle" font-size="9.5" fill="var(--accent-ink)">面向用户 · 要低延迟</text>
  <text x="170" y="114" text-anchor="middle" font-size="9.5" fill="var(--accent-ink)">无状态 · 可随时重启/扩容</text>
  <text x="170" y="132" text-anchor="middle" font-size="9.5" fill="var(--muted)">收请求、入队、读数据渲染</text>
  <text x="170" y="152" text-anchor="middle" font-size="9" fill="var(--faint)">扩容看：并发用户/QPS</text>
  <rect x="420" y="50" width="260" height="120" rx="12" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <text x="550" y="74" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">worker</text>
  <text x="550" y="96" text-anchor="middle" font-size="9.5" fill="var(--ink)">啃重活 · 可慢</text>
  <text x="550" y="114" text-anchor="middle" font-size="9.5" fill="var(--ink)">可重试 · 按队列伸缩</text>
  <text x="550" y="132" text-anchor="middle" font-size="9.5" fill="var(--muted)">消费队列、合并写库、评估</text>
  <text x="550" y="152" text-anchor="middle" font-size="9" fill="var(--faint)">扩容看：队列积压</text>
  <rect x="320" y="92" width="80" height="36" rx="9" fill="var(--red-soft)" stroke="var(--red)"/><text x="360" y="114" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--red)">Redis 队列</text>
  <line x1="300" y1="110" x2="318" y2="110" stroke="var(--faint)" stroke-width="1.8"/><polygon points="318,110 309,105 309,115" fill="var(--faint)"/>
  <line x1="400" y1="110" x2="418" y2="110" stroke="var(--faint)" stroke-width="1.8"/><polygon points="418,110 409,105 409,115" fill="var(--faint)"/>
  <text x="360" y="200" text-anchor="middle" font-size="9.5" fill="var(--faint)">通过队列解耦：两者可各自独立部署、独立扩容、互不阻塞</text>
</svg>
<div class="figcap"><b>左右手分工</b>：<b>web</b> 面向用户、追求低延迟、可随时重启；<b>worker</b> 啃重活、可重试、按队列积压伸缩。二者通过 <b>Redis 队列</b>解耦（第 5 课），所以你能<b>分别</b>给它们扩容——用户多了加 web，队列堵了加 worker。这正是第 4 课「窄腰」让两个容器独立演进的部署体现。</div>
</div>

<div class="cols">
  <div class="col"><h4>web 怎么扩</h4><p>无状态、面向请求 → 看<strong>并发用户 / QPS</strong>，水平多开几份、前面挂负载均衡即可。</p></div>
  <div class="col"><h4>worker 怎么扩</h4><p>面向队列 → 看<strong>队列积压</strong>，积压上来就多开 worker 实例消费（还能按队列分片，第 14 课）。</p></div>
</div>

<h2>配置全靠环境变量</h2>
<p>这六个容器怎么知道彼此地址、密钥、各种开关？答案是<strong>环境变量</strong>。仓库里有一组 <code>.env.*.example</code> 模板（如 <code>.env.dev.example</code>、<code>.env.prod.example</code>），
列出了所有需要配置的变量（数据库连接、S3 端点、加密密钥…）。更重要的是，这些 env <strong>不是随便读的</strong>——它们经过 <strong>Zod 校验</strong>
（<code>packages/shared/src/env.ts</code>、<code>worker/src/env.ts</code> 等），<strong>启动时</strong>就检查类型与必填项。配错了、漏填了，进程会<strong>直接启动失败并报清楚哪个变量有问题</strong>，
而不是带病运行到半路才崩。这条「<strong>启动即校验配置</strong>」的纪律，是把「配置错误」从难查的运行时 bug 变成一眼可见的启动错误（第 51 课展开）。</p>

<p>把这些拼起来，第一次自托管的体验其实很简单：<strong>克隆仓库 → 复制一份 <code>.env.dev.example</code> 填好关键变量 → <code>docker compose up</code></strong>，
六个容器就按依赖次序拉起、连通，几分钟后你就能打开浏览器看到 Langfuse 界面。仓库里还备了<strong>多套 compose 文件</strong>应对不同场景——
<code>docker-compose.dev.yml</code>（本地开发，常只拉基础设施、应用跑在本机便于热重载）、<code>docker-compose.yml</code>（完整一套）、
以及针对特定云的变体（如 Azure）。这种「<strong>一份编排管全栈、按场景给变体</strong>」的安排，正是把前面说的「四依赖的复杂度」收进了几个 yml 文件里——
你不需要手动一个个装数据库、配网络，compose 替你把这些都串好了。理解了这张拓扑，你不仅会「跑起来」，遇到问题也知道该去哪个容器看日志。</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">.env.dev.example（节选，按「4 基础设施 + 认证」分组）</span><span class="ln">配置即接线</span></div>
  <pre class="code"><span class="cm"># ① Postgres —— 配置/用户/权限等元数据（第7课 OLTP）</span>
DATABASE_URL=<span class="st">"postgresql://postgres:postgres@localhost:5432/postgres"</span>
<span class="cm"># ② ClickHouse —— 海量 trace/observation/score 事件（第8课列存）</span>
CLICKHOUSE_URL=<span class="st">"http://localhost:8123"</span>
CLICKHOUSE_USER=<span class="st">"clickhouse"</span>   CLICKHOUSE_PASSWORD=<span class="st">"clickhouse"</span>
<span class="cm"># ③ Redis —— 摄取队列 + 缓存（第12课快接收的落点）</span>
REDIS_HOST=localhost   REDIS_PORT=6379
<span class="cm"># ④ S3 / MinIO —— 大块负载与媒体（第18课）；MinIO 是本地 S3 替身</span>
LANGFUSE_S3_MEDIA_UPLOAD_BUCKET=langfuse
LANGFUSE_S3_..._ENDPOINT=<span class="st">"http://localhost:9090"</span>   ..._FORCE_PATH_STYLE=<span class="kw">true</span>
<span class="cm"># 认证与密钥 —— 启动时由 Zod 校验，缺一即启动失败（第51课）</span>
NEXTAUTH_URL=<span class="st">"http://localhost:3000"</span>   NEXTAUTH_SECRET=<span class="st">"secret"</span>
SALT=<span class="st">"salt"</span>   <span class="cm"># API key 哈希用盐（第49课 createShaHash）</span></pre>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>四个基础设施依赖，对自托管者是不是负担？</strong> 坦白说，是——相比「一个二进制 + 一个 SQLite」，Langfuse 的自托管门槛确实更高。但这正是第 7 课那条取舍的<strong>部署侧后果</strong>：
  为了能扛生产级规模（海量遥测、异步摄取、对象存储），这四个组件每一个都不可省。Langfuse 的缓解办法是用 <strong>docker-compose 一键拉起</strong>全部六个容器、用 <strong>MinIO 替身</strong>免去对云 S3 的依赖，
  让「在自己机器上跑起完整一套」变得简单。<strong>复杂度无法消除，但可以被打包好、一键交付。</strong>这也是为什么官方强调「self-host in minutes」——不是没有依赖，而是把依赖编排好了。对自托管者来说，真正要权衡的不是「依赖多不多」，而是「这套规模化能力你用不用得上」。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>最小自托管栈 = 2 应用 + 4 基础设施</strong>：<code>langfuse-web</code> + <code>langfuse-worker</code>，加 <code>postgres</code> · <code>clickhouse</code> · <code>redis</code> · <code>minio(S3)</code>，全在 <code>docker-compose.yml</code>。</li>
    <li><strong>web vs worker</strong>：同连一套存储但职责相反——web 面向用户低延迟、按 QPS 扩；worker 啃重活、按队列积压扩；靠 Redis 队列解耦。</li>
    <li><strong>MinIO</strong> 是 S3 协议替身：同一套代码云上用真 S3、本地用 MinIO，应用无感。</li>
    <li><strong>配置全靠环境变量</strong>，并经 Zod <strong>启动即校验</strong>（<code>env.ts</code>）——配错就启动失败、报清楚，而非带病运行。</li>
    <li>四依赖是规模化的必要代价（第 7 课），用 docker-compose 一键编排来缓解——「依赖不少，但都打包好了」。</li>
  </ul>
</div>
""")

_EN11.append(r"""
<p class="lead">
Part 2 covered <strong>what</strong> the data model and storage are. This lesson closes it with <strong>what it takes to run</strong> — to
self-host Langfuse, which containers you actually start and how they connect. The answer is clean: <strong>2 app containers + 4
infrastructure engines</strong>, all in the root <code>docker-compose.yml</code>. Land the abstract architecture of earlier lessons onto this
concrete "packing list" and your mental model of Langfuse's "shape" is complete.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Picture a Langfuse deployment as the rooms a restaurant needs: the <strong>front of house</strong> (web) greets guests, shows the menu,
  serves dishes; the <strong>kitchen</strong> (worker) quietly preps, washes up, handles big orders; the <strong>cold storage</strong>
  (ClickHouse) holds mountains of ingredients (telemetry); the <strong>filing cabinet</strong> (Postgres) keeps the menu and staff records
  (config); the <strong>order pass</strong> (Redis) queues tickets; the <strong>warehouse</strong> (S3/MinIO) stacks big, rarely-used stock
  (manuscripts, media). Miss a room and the restaurant limps — but assemble these 6 and you can open for business.
</div>
""")

_EN11.append(r"""
<div class="fig">
<svg viewBox="0 0 720 300" role="img" aria-label="docker-compose topology: langfuse-web and langfuse-worker apps connect to postgres, clickhouse, redis, minio infrastructure">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">docker-compose topology: 2 apps + 4 infra</text>
  <rect x="120" y="40" width="200" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="220" y="60" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">langfuse-web</text><text x="220" y="78" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">langfuse/langfuse:3 · UI+API</text>
  <rect x="400" y="40" width="200" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="500" y="60" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">langfuse-worker</text><text x="500" y="78" text-anchor="middle" font-size="8.5" fill="var(--accent-ink)">langfuse-worker:3 · jobs</text>
  <rect x="30" y="170" width="150" height="64" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="105" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--blue)">postgres:17</text><text x="105" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">config/metadata</text>
  <rect x="195" y="170" width="150" height="64" rx="10" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="270" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--purple)">clickhouse-server</text><text x="270" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">wide events</text>
  <rect x="360" y="170" width="150" height="64" rx="10" fill="var(--red-soft)" stroke="var(--red)"/><text x="435" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--red)">redis:7</text><text x="435" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">queue + cache</text>
  <rect x="525" y="170" width="165" height="64" rx="10" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="607" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--amber)">minio (S3-compatible)</text><text x="607" y="212" text-anchor="middle" font-size="8.5" fill="var(--muted)">event log · media</text>
  <g stroke="var(--line)" stroke-width="1.3">
    <line x1="190" y1="90" x2="110" y2="168"/><line x1="210" y1="90" x2="265" y2="168"/><line x1="240" y1="90" x2="430" y2="168"/>
    <line x1="470" y1="90" x2="280" y2="168"/><line x1="490" y1="90" x2="440" y2="168"/><line x1="520" y1="90" x2="600" y2="168"/><line x1="450" y1="90" x2="120" y2="168"/>
  </g>
  <text x="360" y="262" text-anchor="middle" font-size="9" fill="var(--faint)">each infra has its own named volume for persistence (pg / clickhouse data+logs / redis / minio)</text>
  <text x="360" y="282" text-anchor="middle" font-size="9" fill="var(--faint)">web leans read PG+CH; worker leans write CH/S3, consumes the Redis queue (lines are illustrative)</text>
</svg>
<div class="figcap"><b>The self-host packing list</b>: two app containers <b>langfuse-web</b> (langfuse/langfuse:3) and <b>langfuse-worker</b> (langfuse/langfuse-worker:3), plus four infra <b>postgres:17 · clickhouse-server · redis:7 · minio</b> (S3-compatible). Each infra gets a named volume for persistence. This is the "physical version" of the architecture in Lessons 5 and 7.</div>
</div>

<h2>The minimal self-host stack: 2 apps + 4 infra</h2>
<table class="t">
  <tr><th>Service</th><th>Image</th><th>Role</th></tr>
  <tr><td class="mono">langfuse-web</td><td class="mono">langfuse/langfuse:3</td><td>user-facing: UI + tRPC + public REST API (ingestion entry)</td></tr>
  <tr><td class="mono">langfuse-worker</td><td class="mono">langfuse/langfuse-worker:3</td><td>background: consume queues, merge-write, eval, export…</td></tr>
  <tr><td class="mono">postgres</td><td class="mono">postgres:17</td><td>control plane: config/metadata (L09)</td></tr>
  <tr><td class="mono">clickhouse</td><td class="mono">clickhouse/clickhouse-server</td><td>data plane: wide-event tables (L08)</td></tr>
  <tr><td class="mono">redis</td><td class="mono">redis:7</td><td>BullMQ queues + cache</td></tr>
  <tr><td class="mono">minio</td><td class="mono">chainguard/minio</td><td>S3-compatible object store (local stand-in): event log · media · exports</td></tr>
</table>

<p>Note <strong>minio</strong>: an open-source object store that <strong>speaks the S3 protocol</strong>, standing in for AWS S3 locally / when
self-hosting. So the same code uses real S3 in the cloud and MinIO when self-hosted, <strong>entirely transparent to the app layer</strong> —
the portability of "program to an interface (the S3 protocol), not an implementation". The <strong>four infra containers each mount a named
volume</strong> for persistence (postgres / clickhouse data+logs / redis / minio), while <strong>web and worker are stateless — no volumes</strong>;
so <code>docker compose down</code> then <code>up</code> keeps your data.</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">app tier</span><span class="name">web · worker</span></div><div class="ld">stateless business containers, restartable and scalable on demand. They start, connect to the storage below, and work.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">data tier</span><span class="name">postgres · clickhouse</span></div><div class="ld">two databases: control plane (config) and data plane (telemetry). Stateful, persisted via named volumes — the bedrock.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">support tier</span><span class="name">redis · minio</span></div><div class="ld">queue/cache and object store. Make ingestion async and give big fields/media a home. Also stateful, also persisted.</div></div>
</div>

<p>These tiers have a plain startup order: <strong>bring up the data and support tiers and wait for them to be healthy, then start the app
tier</strong> — so in compose the app containers <code>depends_on</code> the infra and wait for healthchecks. Grasp this layering and you have
direction when debugging deployments: can't reach the DB → check the data tier; ingestion stalled → check Redis; media won't save → check
MinIO.</p>
""")

_EN11.append(r"""
<h2>web and worker: division and collaboration</h2>
<p>The two app containers are Langfuse's "two hands". Similar in form (both connect the same storage) but <strong>opposite in
duty</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="the web container is user-facing, low-latency, restartable; the worker chews heavy jobs, retryable, scales by queue; the two are decoupled by a Redis queue">
  <rect x="40" y="50" width="260" height="120" rx="12" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="170" y="74" text-anchor="middle" font-size="12" font-weight="700" fill="var(--accent-ink)">web</text>
  <text x="170" y="96" text-anchor="middle" font-size="9.5" fill="var(--accent-ink)">user-facing · low latency</text>
  <text x="170" y="114" text-anchor="middle" font-size="9.5" fill="var(--accent-ink)">stateless · restart/scale anytime</text>
  <text x="170" y="132" text-anchor="middle" font-size="9.5" fill="var(--muted)">accept requests, enqueue, read &amp; render</text>
  <text x="170" y="152" text-anchor="middle" font-size="9" fill="var(--faint)">scale by: concurrent users / QPS</text>
  <rect x="420" y="50" width="260" height="120" rx="12" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <text x="550" y="74" text-anchor="middle" font-size="12" font-weight="700" fill="var(--blue)">worker</text>
  <text x="550" y="96" text-anchor="middle" font-size="9.5" fill="var(--ink)">heavy jobs · may be slow</text>
  <text x="550" y="114" text-anchor="middle" font-size="9.5" fill="var(--ink)">retryable · scales by queue</text>
  <text x="550" y="132" text-anchor="middle" font-size="9.5" fill="var(--muted)">consume queue, merge-write, eval</text>
  <text x="550" y="152" text-anchor="middle" font-size="9" fill="var(--faint)">scale by: queue backlog</text>
  <rect x="320" y="92" width="80" height="36" rx="9" fill="var(--red-soft)" stroke="var(--red)"/><text x="360" y="114" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--red)">Redis queue</text>
  <line x1="300" y1="110" x2="318" y2="110" stroke="var(--faint)" stroke-width="1.8"/><polygon points="318,110 309,105 309,115" fill="var(--faint)"/>
  <line x1="400" y1="110" x2="418" y2="110" stroke="var(--faint)" stroke-width="1.8"/><polygon points="418,110 409,105 409,115" fill="var(--faint)"/>
  <text x="360" y="200" text-anchor="middle" font-size="9.5" fill="var(--faint)">decoupled by the queue: deploy and scale each independently, without blocking the other</text>
</svg>
<div class="figcap"><b>Two hands</b>: <b>web</b> is user-facing, low-latency, restartable; <b>worker</b> chews heavy jobs, retryable, scales by queue backlog. The two are decoupled by the <b>Redis queue</b> (L05), so you scale them <b>separately</b> — more users, add web; backed-up queue, add worker. This is the deployment-side expression of Lesson 4's "narrow waist" letting the two containers evolve independently.</div>
</div>

<div class="cols">
  <div class="col"><h4>scaling web</h4><p>stateless, request-facing → watch <strong>concurrent users / QPS</strong>, run a few replicas behind a load balancer.</p></div>
  <div class="col"><h4>scaling worker</h4><p>queue-facing → watch <strong>queue backlog</strong>, spin up more worker instances to consume (and shard by queue, L14).</p></div>
</div>

<h2>Configuration is all environment variables</h2>
<p>How do the six containers know each other's addresses, secrets and toggles? <strong>Environment variables</strong>. The repo has a set of
<code>.env.*.example</code> templates (e.g. <code>.env.dev.example</code>, <code>.env.prod.example</code>) listing every variable to set (DB
connections, S3 endpoint, encryption keys…). More importantly, these envs <strong>aren't read loosely</strong> — they pass through <strong>Zod
validation</strong> (<code>packages/shared/src/env.ts</code>, <code>worker/src/env.ts</code>, etc.), checking types and required fields <strong>at
startup</strong>. Misconfigure or miss one and the process <strong>fails to start and tells you exactly which variable is wrong</strong>, rather
than running sick and crashing midway. This "<strong>validate config at startup</strong>" discipline turns "config errors" from hard-to-find
runtime bugs into obvious startup errors (expanded in L51).</p>

<p>Put it together and the first self-host experience is actually simple: <strong>clone the repo → copy an <code>.env.dev.example</code> and fill
the key variables → <code>docker compose up</code></strong>, and the six containers come up in dependency order, connect, and within minutes you
open a browser to the Langfuse UI. The repo also ships <strong>several compose files</strong> for different scenarios —
<code>docker-compose.dev.yml</code> (local dev, often just the infra while the apps run on your machine for hot reload),
<code>docker-compose.yml</code> (the full stack), and cloud-specific variants (e.g. Azure). This "<strong>one orchestration for the whole
stack, variants per scenario</strong>" is exactly how the earlier "four-dependency complexity" gets folded into a few yml files — you needn't
hand-install each database or wire the network; compose strings it all together. Grasp this topology and you'll not only "get it running" but
also know which container's logs to check when something breaks.</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">.env.dev.example (excerpt, grouped by "4 infra + auth")</span><span class="ln">config = wiring</span></div>
  <pre class="code"><span class="cm"># ① Postgres — metadata: config/users/permissions (L07 OLTP)</span>
DATABASE_URL=<span class="st">"postgresql://postgres:postgres@localhost:5432/postgres"</span>
<span class="cm"># ② ClickHouse — massive trace/observation/score events (L08 columnar)</span>
CLICKHOUSE_URL=<span class="st">"http://localhost:8123"</span>
CLICKHOUSE_USER=<span class="st">"clickhouse"</span>   CLICKHOUSE_PASSWORD=<span class="st">"clickhouse"</span>
<span class="cm"># ③ Redis — ingestion queue + cache (where L12's "receive fast" lands)</span>
REDIS_HOST=localhost   REDIS_PORT=6379
<span class="cm"># ④ S3 / MinIO — bulky payloads & media (L18); MinIO is a local S3 stand-in</span>
LANGFUSE_S3_MEDIA_UPLOAD_BUCKET=langfuse
LANGFUSE_S3_..._ENDPOINT=<span class="st">"http://localhost:9090"</span>   ..._FORCE_PATH_STYLE=<span class="kw">true</span>
<span class="cm"># auth & secrets — Zod-validated at startup, miss one = fail to start (L51)</span>
NEXTAUTH_URL=<span class="st">"http://localhost:3000"</span>   NEXTAUTH_SECRET=<span class="st">"secret"</span>
SALT=<span class="st">"salt"</span>   <span class="cm">// salt for API-key hashing (L49 createShaHash)</span></pre>
</div>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Are four infra dependencies a burden for self-hosters?</strong> Honestly, yes — versus "one binary + one SQLite", Langfuse's
  self-host bar is genuinely higher. But that's the <strong>deployment-side consequence</strong> of Lesson 7's tradeoff: to handle
  production scale (massive telemetry, async ingestion, object storage), none of the four is droppable. Langfuse's mitigation is bringing up
  all six containers with <strong>one docker-compose command</strong> and using a <strong>MinIO stand-in</strong> to remove the dependency on
  cloud S3, making "run the whole thing on your own machine" easy. <strong>Complexity can't be erased, but it can be packaged and delivered in
  one command.</strong> That's why the docs say "self-host in minutes" — not no dependencies, but dependencies orchestrated for you.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Minimal self-host stack = 2 apps + 4 infra</strong>: <code>langfuse-web</code> + <code>langfuse-worker</code>, plus <code>postgres</code> · <code>clickhouse</code> · <code>redis</code> · <code>minio(S3)</code>, all in <code>docker-compose.yml</code>.</li>
    <li><strong>web vs worker</strong>: same storage, opposite duties — web user-facing/low-latency, scales by QPS; worker heavy/retryable, scales by queue backlog; decoupled by the Redis queue.</li>
    <li><strong>MinIO</strong> is an S3-protocol stand-in: same code uses real S3 in the cloud, MinIO locally — transparent to the app.</li>
    <li><strong>Config is all env vars</strong>, Zod-<strong>validated at startup</strong> (<code>env.ts</code>) — misconfigure and it fails to start with a clear message, no sick running.</li>
    <li>Four deps are the necessary cost of scale (L07), mitigated by one-command docker-compose orchestration — "plenty of deps, but packaged".</li>
  </ul>
</div>
""")

LESSON_11 = {"zh": "\n".join(_ZH11), "en": "\n".join(_EN11)}
