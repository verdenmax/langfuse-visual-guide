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
