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
