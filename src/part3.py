"""Part 3 — 摄取链路 / The ingestion (write) path. Lessons L12–L19.

Same authoring pattern as part1/part2: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L12 · 摄取 API / The ingestion API
# ══════════════════════════════════════════════════════════════════════
_ZH12 = []
_EN12 = []

_ZH12.append(r"""
<p class="lead">
第二部分把「数据长什么样、存在哪」讲完了。从这一课起，我们正式走<strong>摄取链路</strong>——也就是第 5 课那条「写入主干」的放大版。
第一站是<strong>公共摄取 API</strong>：你的应用发来一批事件，服务端这一头是怎么<strong>收下</strong>的。剧透一下它的性格——<strong>极快、极轻</strong>：
它只做「鉴权 + 校验 + 入队」三件事，然后立刻返回，<strong>绝不</strong>在这里合并、算成本、写库（那些是 worker 的活）。这就是第 5 课说的「快路」。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把摄取 API 想成快递的<strong>收件口</strong>：快递员（你的 SDK）抱来<strong>一批</strong>包裹（events），收件员（API）做三件事就放行——
  <strong>核对寄件人身份</strong>（鉴权：你这把 key 是哪个项目的？）、<strong>扫码登记面单</strong>（校验：每个包裹的格式对不对？）、<strong>丢上传送带</strong>（入队）。
  然后<strong>当场给你一张回执</strong>（HTTP 200），就让你走了——<strong>不会</strong>当着你的面去分拣、称重、送到目的地。那些慢活，传送带后面的人（worker）慢慢做。
  收件口的唯一目标，就是<strong>收得飞快、永不堵门</strong>。
</div>
""")

# (L12 sections appended below)
_ZH12.append(r"""
<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="摄取请求的生命周期：鉴权、Zod 校验、processEventBatch 入队、立即返回 200">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一个摄取请求的一生（毫秒级）</text>
  <rect x="20" y="70" width="120" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="92" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">SDK POST</text><text x="80" y="108" text-anchor="middle" font-size="8.5" fill="var(--muted)">一批 events</text>
  <rect x="160" y="70" width="110" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="215" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">① 鉴权</text><text x="215" y="108" text-anchor="middle" font-size="8" fill="var(--accent-ink)">key→project</text>
  <rect x="290" y="70" width="110" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="345" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">② Zod 校验</text><text x="345" y="108" text-anchor="middle" font-size="8" fill="var(--accent-ink)">格式对不对</text>
  <rect x="420" y="70" width="150" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="495" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">③ processEventBatch</text><text x="495" y="108" text-anchor="middle" font-size="8" fill="var(--accent-ink)">入队（+落 S3）</text>
  <rect x="590" y="70" width="110" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="645" y="92" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">200 OK</text><text x="645" y="108" text-anchor="middle" font-size="8.5" fill="var(--muted)">立即返回</text>
  <line x1="140" y1="95" x2="158" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="158,95 149,90 149,100" fill="var(--faint)"/>
  <line x1="270" y1="95" x2="288" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="288,95 279,90 279,100" fill="var(--faint)"/>
  <line x1="400" y1="95" x2="418" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="418,95 409,90 409,100" fill="var(--faint)"/>
  <line x1="570" y1="95" x2="588" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="588,95 579,90 579,100" fill="var(--faint)"/>
  <text x="360" y="160" text-anchor="middle" font-size="9.5" fill="var(--faint)">合并、算成本、写 ClickHouse 都不在这里——那是 worker 的活（第 15–17 课）</text>
  <text x="360" y="182" text-anchor="middle" font-size="9" fill="var(--accent-ink)">API 的全部职责：收下 → 校验 → 入队 → 回执</text>
</svg>
<div class="figcap"><b>极简的收件流程</b>：鉴权（API key 解析出 project，第 9·10 课）→ Zod 校验事件格式 → <code>processEventBatch</code> 把事件入队（同时把原件落 S3）→ 立即 200。整条链路上「重活」一件都不在这里做，所以 API 永远毫秒级返回。</div>
</div>

<h2>一个摄取请求的一生</h2>
<p>入口在 <code>web/src/pages/api/public/ingestion.ts</code> 的 <code>handler</code>。它收下请求体后，真正干活的是一个叫 <code>processEventBatch</code> 的共享函数：</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/public/ingestion.ts</span><span class="ln">handler</span></div>
  <pre class="code"><span class="kw">import</span> { processEventBatch } <span class="kw">from</span> <span class="st">"@langfuse/shared/src/server"</span>;

<span class="kw">export default async function</span> <span class="fn">handler</span>(req, res) {
  <span class="cm">// …鉴权、解析 body…</span>
  <span class="kw">const</span> result = <span class="kw">await</span> <span class="fn">processEventBatch</span>(batchForProcessing, authCheck);
  <span class="cm">// 立即把结果返回（成功/部分失败），不等 worker 处理</span>
}</pre>
</div>

<p>注意一个设计细节：<code>processEventBatch</code> 是<strong>共享的</strong>——除了 <code>/ingestion</code>，连「单独提交 score」的接口也复用它。
为什么？因为「收一批事件、校验、入队」这套逻辑<strong>到处都用得上</strong>，抽成一个函数就不必每个端点各写一遍、各错一遍（又是第 6 课「复杂度收敛到一处」的体现）。
它支持的事件类型涵盖了 <code>TRACE_CREATE</code> / <code>OBSERVATION_CREATE</code> / <code>SPAN_CREATE</code> / <code>GENERATION_CREATE</code> / <code>SCORE_CREATE</code> 等
（还包括 <code>SDK_LOG</code>、<code>DATASET_RUN_ITEM_CREATE</code>）——正是第 6 课说的那套事件信封。</p>

<h2>为什么是「一批」，不是「一条」</h2>
<p>SDK 不是每产生一个事件就发一次 HTTP，而是<strong>攒成一批</strong>再发。这个「批」的设计省了大事：</p>

<div class="cols">
  <div class="col"><h4>😖 一条一发</h4><p>每个 observation 都来一次 HTTP 往返，高频应用下网络开销巨大、连接数爆炸，对你的应用是实打实的拖累。</p></div>
  <div class="col"><h4>😀 攒批一发</h4><p>几十上百个事件打成一个请求，<strong>一次往返</strong>搞定。网络开销摊薄，API 也能一次性校验、一次性入队，吞吐高得多。</p></div>
</div>

<p>批处理还带来一个语义上的好处：同一批里可能既有某 observation 的 <code>CREATE</code> 又有它的 <code>UPDATE</code>，服务端可以<strong>整批一起</strong>处理，
减少来回。当然，批也不能无限大——请求体过大时 API 会拒绝（返回「请求体过大」），这也是一道保护：别让单个请求把服务端撑爆。</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SDK 攒批 → POST /ingestion</h4><p>应用侧把一段时间内的事件打成一批，一次发出。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>handler 鉴权</h4><p>从 API key 解析 project、校验写入权限（失败整批拒）。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Zod 校验每个事件</h4><p>结构不对的事件被拒；其余继续（可部分成功）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>processEventBatch 入队 + 落 S3</h4><p>合法事件进 Redis 队列、原件存 S3（第 14 课）。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>立即返回结果</h4><p>告诉调用方哪些收下、哪些被拒——全程毫秒级，不等 worker。</p></div></div>
</div>
""")

_ZH12.append(r"""
<h2>守门的两道关：鉴权 + 校验</h2>
<p>API 在「入队」之前，必须先过两道关。它们看似例行公事，却是整个系统<strong>安全与健壮</strong>的第一道防线：</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="两道关：鉴权解析出 project 并校验权限，Zod 校验事件格式，都通过才入队">
  <rect x="40" y="60" width="180" height="80" rx="11" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="130" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">① 鉴权关</text>
  <text x="130" y="106" text-anchor="middle" font-size="9" fill="var(--accent-ink)">API key → 哪个 project？</text>
  <text x="130" y="122" text-anchor="middle" font-size="9" fill="var(--accent-ink)">有没有写入权限？</text>
  <rect x="270" y="60" width="180" height="80" rx="11" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <text x="360" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="var(--blue)">② 校验关（Zod）</text>
  <text x="360" y="106" text-anchor="middle" font-size="9" fill="var(--ink)">每个事件结构对不对？</text>
  <text x="360" y="122" text-anchor="middle" font-size="9" fill="var(--ink)">坏事件早拒，别进系统</text>
  <rect x="510" y="70" width="170" height="60" rx="11" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="595" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">入队</text>
  <text x="595" y="113" text-anchor="middle" font-size="8.5" fill="var(--muted)">两关都过才放行</text>
  <line x1="220" y1="100" x2="268" y2="100" stroke="var(--faint)" stroke-width="1.8"/><polygon points="268,100 259,95 259,105" fill="var(--faint)"/>
  <line x1="450" y1="100" x2="508" y2="100" stroke="var(--faint)" stroke-width="1.8"/><polygon points="508,100 499,95 499,105" fill="var(--faint)"/>
  <text x="360" y="168" text-anchor="middle" font-size="9.5" fill="var(--faint)">鉴权决定「你是谁、能不能写」，校验决定「你发的东西干不干净」</text>
</svg>
<div class="figcap"><b>两道关</b>：<b>鉴权</b>从 API key 解析出 project（第 9 课 key 属于某 project）并确认有写入权限——这一步也<b>把租户钉死</b>（第 10 课 project_id 贯穿）；<b>Zod 校验</b>逐个事件检查结构，<b>坏数据在门口就被拒</b>，不会污染下游。两关都过，才允许入队。</div>
</div>

<p>第二道关「Zod 校验」尤其重要：摄取系统每天吞下海量来自<strong>各种 SDK、各种版本</strong>的数据，难免有格式不对、字段缺失的「脏事件」。
在<strong>入口</strong>就用 Zod schema 把它们挡下、给出清晰错误，比让它们流进队列、到 worker 处理时才崩要好得多——<strong>越早拒绝坏数据，整个系统越省心</strong>。
这一批里如果有几个坏事件，API 还能返回「部分成功」，告诉你哪几条没收下，而不是整批一刀切。</p>

<table class="t">
  <tr><th>这一关</th><th>把守什么</th><th>失败会怎样</th></tr>
  <tr><td><b>鉴权</b></td><td>API key 有效吗？属于哪个 project？能写吗？</td><td>401/403，整批拒绝</td></tr>
  <tr><td><b>Zod 校验</b></td><td>每个事件的结构/类型是否合法</td><td>坏事件被拒，可返回部分成功</td></tr>
  <tr><td><b>体积保护</b></td><td>请求体是否过大</td><td>返回「请求体过大」，防撑爆</td></tr>
</table>

<p>「部分成功」不是说说而已，它写进了<strong>响应契约</strong>：<code>ingestion.ts</code> 的 handler 最后一行是 <code>res.status(<strong>207</strong>).json(result)</code>，
而 <code>result</code> 形如 <code>{ successes, errors }</code>——两个数组，分别列出收下的事件与被拒的事件（每条带错误原因）。<strong>207 Multi-Status</strong> 这个 HTTP 状态码
天生就是为「一个请求里多个子操作、结果各异」设计的。于是即便你这批 100 个事件里混进 3 个脏的，服务端也会<strong>收下 97 个、退回 3 个并告诉你为什么</strong>，
而不是因为 3 颗老鼠屎把整锅粥倒掉。这对 SDK 极其友好：客户端可以只重传失败的那几条，无需整批重来。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么 API 只做「鉴权+校验+入队」，把一切重活都推给 worker？</strong> 因为摄取 API 是<strong>直面你应用的那一层</strong>，它的首要 KPI 是
  「<strong>永远快、永远不拖累调用方</strong>」。任何放在这里的额外工作——合并、查定价、写库——都会变成你每次埋点调用的延迟，还会因为下游抖动而失败。
  所以 Langfuse 把这条线<strong>切得极干净</strong>：API 端只保留「无论如何都必须当场做」的最小集合（鉴权防止越权写入、校验防止脏数据入库、入队完成交接），
  剩下能异步的<strong>一律异步</strong>。代价是「最终一致」（第 5 课），但收益是一个几乎不可能慢、不可能拖垮你业务的摄取入口。<strong>入口越薄，越扛得住洪峰。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>摄取 API 的全部职责：<strong>鉴权 + Zod 校验 + 入队</strong>，然后立即返回——合并/算成本/写库都不在这里（是 worker 的活）。</li>
    <li>入口 <code>ingestion.ts</code> 的 <code>handler</code> 调用共享的 <code>processEventBatch</code>（连单独提交 score 的接口也复用它）。</li>
    <li><strong>攒批上报</strong>：几十上百个事件一次 HTTP，摊薄网络开销、一次校验一次入队；批过大会被拒（体积保护）。</li>
    <li><strong>两道关</strong>：鉴权（key→project、权限，把租户钉死）+ Zod 校验（坏数据门口就拒，可部分成功）。</li>
    <li>取舍：入口只留「必须当场做」的最小集合，能异步的全异步——入口越薄越扛洪峰，代价是最终一致。</li>
  </ul>
</div>
""")

_EN12.append(r"""
<p class="lead">
Part 2 finished "what the data looks like and where it lives". From here we walk the <strong>ingestion path</strong> — the close-up of
Lesson 5's "write trunk". First stop: the <strong>public ingestion API</strong> — how the server <strong>receives</strong> a batch of events
your app sends. Spoiler on its character: <strong>extremely fast and light</strong>. It does just three things — <strong>auth + validate +
enqueue</strong> — then returns immediately, <strong>never</strong> merging, computing cost, or writing the DB here (those are the worker's
job). This is Lesson 5's "fast lane".
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Picture the ingestion API as a courier's <strong>drop-off counter</strong>: the courier (your SDK) brings <strong>a batch</strong> of parcels
  (events), and the clerk (the API) does three things before waving you through — <strong>check the sender's identity</strong> (auth: which
  project is this key?), <strong>scan and log the labels</strong> (validate: is each parcel well-formed?), <strong>drop them on the
  belt</strong> (enqueue). Then it <strong>hands you a receipt on the spot</strong> (HTTP 200) and lets you go — it <strong>won't</strong> sort,
  weigh and deliver in front of you. The slow work is done by people down the belt (the worker). The counter's only goal: <strong>accept fast,
  never block the door</strong>.
</div>
""")

_EN12.append(r"""
<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="ingestion request lifecycle: auth, Zod validation, processEventBatch enqueue, immediate 200">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">the life of one ingestion request (milliseconds)</text>
  <rect x="20" y="70" width="120" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="92" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">SDK POST</text><text x="80" y="108" text-anchor="middle" font-size="8.5" fill="var(--muted)">a batch of events</text>
  <rect x="160" y="70" width="110" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="215" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">1 auth</text><text x="215" y="108" text-anchor="middle" font-size="8" fill="var(--accent-ink)">key→project</text>
  <rect x="290" y="70" width="110" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="345" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">2 Zod validate</text><text x="345" y="108" text-anchor="middle" font-size="8" fill="var(--accent-ink)">well-formed?</text>
  <rect x="420" y="70" width="150" height="50" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="495" y="92" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">3 processEventBatch</text><text x="495" y="108" text-anchor="middle" font-size="8" fill="var(--accent-ink)">enqueue (+ S3)</text>
  <rect x="590" y="70" width="110" height="50" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="645" y="92" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">200 OK</text><text x="645" y="108" text-anchor="middle" font-size="8.5" fill="var(--muted)">return now</text>
  <line x1="140" y1="95" x2="158" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="158,95 149,90 149,100" fill="var(--faint)"/>
  <line x1="270" y1="95" x2="288" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="288,95 279,90 279,100" fill="var(--faint)"/>
  <line x1="400" y1="95" x2="418" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="418,95 409,90 409,100" fill="var(--faint)"/>
  <line x1="570" y1="95" x2="588" y2="95" stroke="var(--faint)" stroke-width="1.8"/><polygon points="588,95 579,90 579,100" fill="var(--faint)"/>
  <text x="360" y="160" text-anchor="middle" font-size="9.5" fill="var(--faint)">merge, cost, ClickHouse writes are not here — that's the worker (L15–17)</text>
  <text x="360" y="182" text-anchor="middle" font-size="9" fill="var(--accent-ink)">the API's entire duty: accept → validate → enqueue → receipt</text>
</svg>
<div class="figcap"><b>A minimal accept flow</b>: auth (API key resolves a project, L09·10) → Zod-validate event shapes → <code>processEventBatch</code> enqueues (and lands originals in S3) → immediate 200. No "heavy work" happens here, so the API always returns in milliseconds.</div>
</div>

<h2>The life of one ingestion request</h2>
<p>The entry is the <code>handler</code> in <code>web/src/pages/api/public/ingestion.ts</code>. After taking the body, the real work is a
shared function called <code>processEventBatch</code>:</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/public/ingestion.ts</span><span class="ln">handler</span></div>
  <pre class="code"><span class="kw">import</span> { processEventBatch } <span class="kw">from</span> <span class="st">"@langfuse/shared/src/server"</span>;

<span class="kw">export default async function</span> <span class="fn">handler</span>(req, res) {
  <span class="cm">// …auth, parse body…</span>
  <span class="kw">const</span> result = <span class="kw">await</span> <span class="fn">processEventBatch</span>(batchForProcessing, authCheck);
  <span class="cm">// return the result immediately (success / partial failure), not waiting for the worker</span>
}</pre>
</div>

<p>One design detail: <code>processEventBatch</code> is <strong>shared</strong> — besides <code>/ingestion</code>, even the standalone "submit a
score" endpoint reuses it. Why? Because "accept a batch, validate, enqueue" is <strong>needed everywhere</strong>; factoring it into one
function avoids re-implementing (and re-bugging) it per endpoint (again Lesson 6's "converge complexity to one place"). The event types it
supports cover <code>TRACE_CREATE</code> / <code>OBSERVATION_CREATE</code> / <code>SPAN_CREATE</code> / <code>GENERATION_CREATE</code> /
<code>SCORE_CREATE</code> and more (including <code>SDK_LOG</code>, <code>DATASET_RUN_ITEM_CREATE</code>) — exactly Lesson 6's event
envelope.</p>

<h2>Why a "batch", not "one"</h2>
<p>The SDK doesn't fire one HTTP per event — it <strong>collects a batch</strong> and sends it. This "batch" design saves a lot:</p>

<div class="cols">
  <div class="col"><h4>😖 one-by-one</h4><p>Every observation a full HTTP round trip; at high frequency the network overhead is huge and connections explode — a real drag on your app.</p></div>
  <div class="col"><h4>😀 batched</h4><p>Dozens or hundreds of events in one request, <strong>one round trip</strong>. Network overhead amortizes, and the API validates and enqueues in one go — far higher throughput.</p></div>
</div>

<p>Batching also gives a semantic benefit: a batch may hold both a <code>CREATE</code> and an <code>UPDATE</code> for one observation, and the
server can process them <strong>together</strong>, cutting round trips. Of course a batch can't be infinite — when the body is too large the API
rejects it ("payload too large"), another guard: don't let one request blow up the server.</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SDK batches → POST /ingestion</h4><p>the app packs a window of events into one batch and sends it.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>handler authenticates</h4><p>resolve the project from the API key and check write permission (fail → reject the whole batch).</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Zod-validate each event</h4><p>ill-formed events are rejected; the rest continue (partial success possible).</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>processEventBatch enqueues + lands S3</h4><p>valid events enter the Redis queue; originals are stored in S3 (L14).</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>return the result immediately</h4><p>tell the caller which were accepted, which rejected — all in milliseconds, not waiting for the worker.</p></div></div>
</div>
""")

_EN12.append(r"""
<h2>Two gates: auth + validation</h2>
<p>Before "enqueue", the API must pass two gates. They look routine but are the system's first line of <strong>security and
robustness</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="two gates: auth resolves the project and checks permission, Zod validates event shape, both must pass to enqueue">
  <rect x="40" y="60" width="180" height="80" rx="11" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/>
  <text x="130" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="var(--accent-ink)">1 auth gate</text>
  <text x="130" y="106" text-anchor="middle" font-size="9" fill="var(--accent-ink)">API key → which project?</text>
  <text x="130" y="122" text-anchor="middle" font-size="9" fill="var(--accent-ink)">may it write?</text>
  <rect x="270" y="60" width="180" height="80" rx="11" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/>
  <text x="360" y="86" text-anchor="middle" font-size="11" font-weight="700" fill="var(--blue)">2 validate gate (Zod)</text>
  <text x="360" y="106" text-anchor="middle" font-size="9" fill="var(--ink)">is each event well-formed?</text>
  <text x="360" y="122" text-anchor="middle" font-size="9" fill="var(--ink)">reject bad events early</text>
  <rect x="510" y="70" width="170" height="60" rx="11" fill="var(--purple-soft)" stroke="var(--purple)"/>
  <text x="595" y="95" text-anchor="middle" font-size="11" font-weight="700" fill="var(--purple)">enqueue</text>
  <text x="595" y="113" text-anchor="middle" font-size="8.5" fill="var(--muted)">only if both pass</text>
  <line x1="220" y1="100" x2="268" y2="100" stroke="var(--faint)" stroke-width="1.8"/><polygon points="268,100 259,95 259,105" fill="var(--faint)"/>
  <line x1="450" y1="100" x2="508" y2="100" stroke="var(--faint)" stroke-width="1.8"/><polygon points="508,100 499,95 499,105" fill="var(--faint)"/>
  <text x="360" y="168" text-anchor="middle" font-size="9.5" fill="var(--faint)">auth decides "who you are and may you write", validation decides "is what you sent clean"</text>
</svg>
<div class="figcap"><b>Two gates</b>: <b>auth</b> resolves the project from the API key (L09: a key belongs to a project) and confirms write permission — this also <b>pins the tenant</b> (L10's project_id threading); <b>Zod validation</b> checks each event's shape, so <b>bad data is rejected at the door</b> and never pollutes downstream. Pass both, then enqueue.</div>
</div>

<p>The second gate, Zod validation, especially matters: the ingestion system swallows a flood of data from <strong>many SDKs and
versions</strong> daily, inevitably with malformed or missing-field "dirty events". Rejecting them at the <strong>entry</strong> with a Zod
schema and a clear error beats letting them flow into the queue and crash the worker — <strong>the earlier you reject bad data, the calmer the
whole system</strong>. If a few events in a batch are bad, the API can still return "partial success", telling you which weren't accepted,
rather than failing the whole batch.</p>

<table class="t">
  <tr><th>This gate</th><th>Guards</th><th>On failure</th></tr>
  <tr><td><b>auth</b></td><td>Is the API key valid? Which project? May it write?</td><td>401/403, whole batch rejected</td></tr>
  <tr><td><b>Zod validation</b></td><td>Is each event's shape/type legal</td><td>bad events rejected; partial success possible</td></tr>
  <tr><td><b>size guard</b></td><td>Is the body too large</td><td>"payload too large", prevents blow-up</td></tr>
</table>

<p>"Partial success" isn't just talk — it's baked into the <strong>response contract</strong>: the last line of <code>ingestion.ts</code>'s handler
is <code>res.status(<strong>207</strong>).json(result)</code>, where <code>result</code> looks like <code>{ successes, errors }</code> — two arrays
listing the accepted events and the rejected ones (each with its error reason). The <strong>207 Multi-Status</strong> HTTP code is purpose-built for
"one request, many sub-operations, mixed outcomes". So even if 3 of your 100 events are dirty, the server <strong>accepts 97, returns the 3 with
reasons</strong>, instead of throwing out the whole pot for a few bad apples. Hugely SDK-friendly: the client can retransmit just the failed ones,
no full-batch retry.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why does the API only "auth + validate + enqueue", pushing all heavy work to the worker?</strong> Because the ingestion API is the
  layer <strong>facing your app directly</strong>, and its top KPI is "<strong>always fast, never drag the caller</strong>". Any extra work
  here — merging, looking up pricing, writing the DB — becomes latency on every instrumentation call and can fail on downstream hiccups. So
  Langfuse <strong>cuts this line very cleanly</strong>: the API keeps only the minimum that <strong>must happen on the spot</strong> (auth to
  prevent unauthorized writes, validation to keep dirty data out, enqueue to hand off), and everything else that can be async <strong>is
  async</strong>. The cost is "eventual consistency" (L05), but the gain is an ingestion entry that's almost impossible to slow or to drag
  your business down. <strong>The thinner the entry, the better it survives spikes.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>The ingestion API's entire job: <strong>auth + Zod validation + enqueue</strong>, then return immediately — merge/cost/DB-write are not here (the worker's job).</li>
    <li>The <code>handler</code> in <code>ingestion.ts</code> calls the shared <code>processEventBatch</code> (even the standalone score endpoint reuses it).</li>
    <li><strong>Batched reporting</strong>: dozens/hundreds of events per HTTP, amortizing network cost, validated and enqueued in one go; oversized batches are rejected (size guard).</li>
    <li><strong>Two gates</strong>: auth (key→project, permission, pins the tenant) + Zod validation (reject bad data at the door, partial success possible).</li>
    <li>Tradeoff: the entry keeps only "must happen now", everything async-able is async — the thinner the entry the better it survives spikes, at the cost of eventual consistency.</li>
  </ul>
</div>
""")

LESSON_12 = {"zh": "\n".join(_ZH12), "en": "\n".join(_EN12)}
