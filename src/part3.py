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


# ══════════════════════════════════════════════════════════════════════
# L13 · 事件类型与合并语义 / Event types & merge semantics
# ══════════════════════════════════════════════════════════════════════
_ZH13 = []
_EN13 = []

_ZH13.append(r"""
<p class="lead">
上一课，API 把<strong>一批事件</strong>收下并入队。这一课我们把镜头怼到<strong>单个事件</strong>上：它长什么样？为什么有 <code>create</code> 和 <code>update</code> 两副面孔？
最关键的是——你的 SDK 先后发来的<strong>好几个事件</strong>，最后怎么会变成数据库里<strong>同一行</strong>？这就是 Langfuse 摄取的灵魂：<strong>事件流 → 合并成记录</strong>。
看懂这一课，第 8 课那张 <code>ReplacingMergeTree(event_ts, is_deleted)</code> 的设计才算真正落地。
</p>

<div class="card analogy">
  <div class="tag">🩺 生活类比</div>
  把一个观测想成医院里的一份<strong>病历</strong>。病人挂号那一刻，医生写下第一条<strong>就诊记录</strong>（<code>generation-create</code>：开始时间、输入的主诉）；
  检查做完、开完药，医生<strong>补一条记录</strong>（<code>generation-update</code>：结束时间、诊断结论、用了多少药）。这两条记录都贴着<strong>同一个病人号</strong>（实体 id）——
  护士归档时，不会建两份病历，而是把它们<strong>合并进同一份</strong>，冲突字段<strong>以最新一条为准</strong>。而每条记录本身还有自己的<strong>流水号</strong>（事件 id），
  保证同一条记录<strong>归档两次也不会重复</strong>。「病人号合并、流水号去重」——正是这一课要拆解的两套 id。
</div>
""")

# (L13 sections appended below)

_ZH13.append(r"""
<h2>事件的信封：id · timestamp · type · body</h2>
<p>每个摄取事件，无论它描述的是 trace、observation 还是 score，都套着<strong>同一个信封</strong>。信封里有一个公共的「外壳」，再加一个随类型而变的「内容物」<code>body</code>。
Langfuse 用 Zod 把它定义得一清二楚：先有一个 <code>base</code>（外壳），各类型在它上面 <code>extend</code> 出自己的 <code>type</code> 与 <code>body</code>，
最后用 <strong>判别联合</strong>（<code>z.discriminatedUnion("type", […])</code>）把十几种事件拢成一个 schema。校验时，Zod 看 <code>type</code> 这个字段，
就知道该用哪一套 <code>body</code> 规则去验——这就是「<strong>一个字段定身份，一套规则配一种身</strong>」。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="事件信封结构：base 外壳 id/timestamp/metadata，type 字段作为判别器，路由到对应的 body schema">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一个事件的信封：外壳固定，body 随 type 而变</text>
  <rect x="30" y="44" width="230" height="180" rx="12" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="145" y="64" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">base（公共外壳）</text>
  <rect x="48" y="76" width="194" height="26" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="58" y="93" font-size="9.5" fill="var(--ink)"><tspan font-weight="700">id</tspan> · 事件 id（流水号）</text>
  <rect x="48" y="108" width="194" height="26" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="58" y="125" font-size="9.5" fill="var(--ink)"><tspan font-weight="700">timestamp</tspan> · 事件发生时刻</text>
  <rect x="48" y="140" width="194" height="26" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="58" y="157" font-size="9.5" fill="var(--ink)"><tspan font-weight="700">metadata</tspan> · 附带信息</text>
  <rect x="48" y="176" width="194" height="34" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="58" y="190" font-size="9.5" font-weight="700" fill="var(--accent-ink)">type · 判别器 🔑</text><text x="58" y="203" font-size="8" fill="var(--accent-ink)">决定下面 body 用哪套规则</text>
  <line x1="260" y1="193" x2="300" y2="193" stroke="var(--accent)" stroke-width="2"/><polygon points="300,193 290,188 290,198" fill="var(--accent)"/>
  <text x="280" y="184" text-anchor="middle" font-size="8" fill="var(--accent-ink)">按 type 路由</text>
  <rect x="310" y="50" width="380" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="500" y="68" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">type=generation-create → body: CreateGenerationBody</text><text x="500" y="82" text-anchor="middle" font-size="8" fill="var(--accent-ink)">startTime · model · usage · input/output…</text>
  <rect x="310" y="98" width="380" height="40" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="500" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">type=span-update → body: UpdateSpanBody</text><text x="500" y="130" text-anchor="middle" font-size="8" fill="var(--muted)">id · endTime · output…（补一条）</text>
  <rect x="310" y="146" width="380" height="40" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="500" y="164" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">type=score-create → body: ScoreBody</text><text x="500" y="178" text-anchor="middle" font-size="8" fill="var(--muted)">name · value · dataType…</text>
  <rect x="310" y="194" width="380" height="28" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="500" y="212" text-anchor="middle" font-size="8.5" fill="var(--faint)">…共 18 种 type（trace / 14 个 observation 事件 / score / sdk-log / dataset-run-item）</text>
</svg>
<div class="figcap"><b>信封 = 固定外壳 + 可变 body</b>：<code>base</code> 持有 <code>id</code>（事件 id）、<code>timestamp</code>、<code>metadata</code> 和判别字段 <code>type</code>；<code>type</code> 决定 <code>body</code> 套用哪一套 Zod 规则。这正是 <code>z.discriminatedUnion("type", […])</code> 的工作方式。源码：<code>packages/shared/src/server/ingestion/types.ts:597</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/types.ts</span><span class="ln">L597</span></div>
  <pre class="code"><span class="kw">const</span> base = z.<span class="fn">object</span>({
  id: idSchema,                        <span class="cm">// 事件 id（流水号）</span>
  timestamp: z.iso.<span class="fn">datetime</span>({ offset: <span class="kw">true</span> }),
  metadata: jsonSchema.<span class="fn">nullish</span>(),
});

<span class="kw">const</span> generationCreateEvent = base.<span class="fn">extend</span>({
  type: z.<span class="fn">literal</span>(eventTypes.GENERATION_CREATE),
  body: CreateGenerationBody,          <span class="cm">// 随 type 而变的内容物</span>
});
<span class="cm">// …span-create / span-update / score-create / 共 18 种…</span>

<span class="kw">const</span> ingestionEvent = z.<span class="fn">discriminatedUnion</span>(<span class="st">"type"</span>, [
  traceEvent, scoreEvent, spanCreateEvent, spanUpdateEvent,
  generationCreateEvent, generationUpdateEvent, <span class="cm">/* … */</span>
]);</pre>
</div>

<p>判别联合的妙处在于：它不是「把所有字段都设成可选、随便你填」，而是<strong>每种 type 配一套严格的 body 规则</strong>。
发 <code>generation-create</code> 就必须符合 <code>CreateGenerationBody</code>，发 <code>score-create</code> 就必须符合 <code>ScoreBody</code>——填错了类型、缺了字段，第 12 课那道 Zod 关当场就拦下。
而且这套 schema 还分<strong>公共版与内部版</strong>两个实例：像 <code>dataset-run-item-create</code> 这种就只允许内部使用，公共 API 发它会被拒。</p>
""")

# (more L13 sections below)

_ZH13.append(r"""
<h2>body 的「俄罗斯套娃」：Event ⊂ Span ⊂ Generation</h2>
<p>那些 <code>body</code> 不是各写各的，而是<strong>层层继承</strong>出来的。最里层是 <code>OptionalObservationBody</code>（traceId、name、startTime、input/output…），
往外 <code>extend</code> 一层加 <code>id</code> 成 <code>CreateEventEvent</code>，再加 <code>endTime</code> 成 <code>CreateSpanBody</code>，再加 <code>model / usage / modelParameters</code> 成 <code>CreateGenerationBody</code>。
这条链精确对应第 3 课的观测三型：<strong>EVENT 是时间点</strong>（无时长）、<strong>SPAN 有起止</strong>（多了 endTime）、<strong>GENERATION 是带 LLM 字段的 SPAN</strong>（多了 model/usage）。
有趣的是，第 8 课提到的那些新观测类型——AGENT / TOOL / CHAIN / RETRIEVER / EVALUATOR / EMBEDDING / GUARDRAIL——它们的 <code>body</code> <strong>全都复用 <code>CreateGenerationBody</code></strong>：
本质上都是「generation 那么丰富的一段观测」，只是语义标签不同。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="body 继承链：OptionalObservationBody 加 id 成 CreateEventEvent，加 endTime 成 CreateSpanBody，加 model/usage 成 CreateGenerationBody">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">body schema 的继承链（每往外一层，多几个字段）</text>
  <rect x="40" y="60" width="620" height="150" rx="12" fill="none" stroke="var(--teal)" stroke-dasharray="5 4"/>
  <text x="56" y="78" font-size="9" font-weight="700" fill="var(--teal)">CreateGenerationBody（+ model · usage · modelParameters · completionStartTime）</text>
  <rect x="70" y="88" width="560" height="112" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="86" y="106" font-size="9" font-weight="700" fill="var(--accent-ink)">CreateSpanBody（+ endTime）</text>
  <rect x="100" y="116" width="500" height="76" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="116" y="134" font-size="9" font-weight="700" fill="var(--ink)">CreateEventEvent（+ id）</text>
  <rect x="130" y="144" width="440" height="40" rx="8" fill="var(--bg)" stroke="var(--faint)"/>
  <text x="350" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">OptionalObservationBody</text>
  <text x="350" y="176" text-anchor="middle" font-size="8" fill="var(--muted)">traceId · name · startTime · input/output · level · parentObservationId…</text>
  <text x="685" y="120" text-anchor="end" font-size="8.5" fill="var(--accent-ink)">GENERATION</text>
  <text x="685" y="150" text-anchor="end" font-size="8.5" fill="var(--blue)">SPAN</text>
  <text x="685" y="178" text-anchor="end" font-size="8.5" fill="var(--faint)">EVENT</text>
</svg>
<div class="figcap"><b>越往外，能力越强</b>：EVENT 是无时长的时间点 → SPAN 加 <code>endTime</code> 有了起止 → GENERATION 再加 <code>model/usage</code> 成为可记 token 与成本的 LLM 调用。AGENT/TOOL/CHAIN 等 7 种新类型直接复用 <code>CreateGenerationBody</code>。源码：<code>types.ts:421-470</code>。</div>
</div>

<p>这套继承不仅省代码，更让<strong>类型语义层层递进</strong>：你不可能给一个 EVENT 填 endTime（它的 body 里压根没这字段），也不可能给一个 SPAN 填 usage。
schema 即文档——读完这条链，三型观测「能装什么、不能装什么」一目了然。</p>
""")

# (merge-semantics section below)

_ZH13.append(r"""
<h2>灵魂所在：好几个事件，怎么变成一行</h2>
<p>现在来回答开篇那个问题。一次 LLM 调用，SDK 通常发<strong>两个</strong>事件：开始时 <code>generation-create</code>（带 startTime、input），结束时 <code>generation-update</code>（带 endTime、output、usage）。
它们最终却落成 ClickHouse 里<strong>同一行 observation</strong>。秘密在于<strong>两套 id 各司其职</strong>：</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">实体 id</span><span class="name">body.id（合并键）</span></div><div class="ld">观测/trace 本身的 id。<strong>同一个 body.id 的所有事件，注定合并成一行</strong>。create 和 update 共享它，所以它们指向同一条记录。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">事件 id</span><span class="name">信封 base.id（去重键）</span></div><div class="ld">每个事件自己的流水号。它在 S3 里成为文件名 <code>&lt;eventId&gt;.json</code>——<strong>同一事件重发，覆盖同一个文件，天然幂等</strong>，不会算两次。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">版本</span><span class="name">timestamp（谁更新）</span></div><div class="ld">合并冲突字段时，<strong>以时间更晚的事件为准</strong>（last-write-wins）。这正是第 8 课 <code>ReplacingMergeTree(event_ts)</code> 在写入侧的镜像。</div></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="同一 body.id 的 create 与 update 两个事件，按 timestamp 合并成一行 observation，冲突字段以最新为准">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">事件流 → 合并成一条记录（同 body.id，最新者胜）</text>
  <rect x="30" y="50" width="250" height="78" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="155" y="68" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">事件① generation-create</text>
  <text x="46" y="86" font-size="8.5" fill="var(--muted)">eventId=e1 · body.id=<tspan font-weight="700" fill="var(--accent-ink)">obs-42</tspan> · t=10:00:00</text>
  <text x="46" y="102" font-size="8.5" fill="var(--ink)">startTime=10:00 · input="..." </text>
  <text x="46" y="118" font-size="8.5" fill="var(--ink)">model="gpt-4o"</text>
  <rect x="30" y="140" width="250" height="78" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="155" y="158" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">事件② generation-update</text>
  <text x="46" y="176" font-size="8.5" fill="var(--accent-ink)">eventId=e2 · body.id=<tspan font-weight="700">obs-42</tspan> · t=10:00:03</text>
  <text x="46" y="192" font-size="8.5" fill="var(--accent-ink)">endTime=10:00:03 · output="..."</text>
  <text x="46" y="208" font-size="8.5" fill="var(--accent-ink)">usage={in:120,out:80}</text>
  <line x1="280" y1="134" x2="430" y2="134" stroke="var(--faint)" stroke-width="1.8"/><polygon points="430,134 420,129 420,139" fill="var(--faint)"/>
  <text x="355" y="126" text-anchor="middle" font-size="8.5" fill="var(--faint)">按 body.id 分组合并</text>
  <rect x="440" y="74" width="250" height="120" rx="12" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/>
  <text x="565" y="94" text-anchor="middle" font-size="10" font-weight="700" fill="var(--teal)">合并后的 observation 行</text>
  <text x="456" y="114" font-size="8.5" fill="var(--ink)">id=<tspan font-weight="700" fill="var(--accent-ink)">obs-42</tspan> · type=GENERATION</text>
  <text x="456" y="132" font-size="8.5" fill="var(--ink)">startTime=10:00 · endTime=10:00:03</text>
  <text x="456" y="150" font-size="8.5" fill="var(--ink)">input + output（各取有值的一方）</text>
  <text x="456" y="168" font-size="8.5" fill="var(--ink)">model=gpt-4o · usage={120,80}</text>
  <text x="456" y="186" font-size="8" fill="var(--muted)">冲突字段：t 更大的②胜</text>
</svg>
<div class="figcap"><b>create + update → 一行</b>：两个事件共享 <code>body.id=obs-42</code>，被分到一组合并；各字段取有值的一方，冲突时以 <code>timestamp</code> 更晚者为准。worker 端的合并逻辑（第 15 课）正是第 8 课 ReplacingMergeTree 行为的「写入侧预演」。</div>
</div>

<p>把这条「事件流 → 一行」的路径拆成五步，合并的来龙去脉就完全清楚了——前两步在你的应用侧发生，后三步在 Langfuse 服务端发生：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>开始：发 create</h4><p>LLM 调用一开始，SDK 发 <code>generation-create</code>，带上 <code>body.id</code>、startTime、input。发完即忘，不在内存里攥着。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>结束：发 update</h4><p>调用结束，SDK 再发 <code>generation-update</code>，<strong>沿用同一个 body.id</strong>，补上 endTime、output、usage。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>按 body.id 分组</h4><p>服务端把 <code>dedupKey = 实体类型-body.id</code> 相同的事件归到一组——这两条就被认成「同一条记录的两次上报」。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>合并字段（最新者胜）</h4><p>逐字段取有值的一方；create 与 update 都给了的字段，以 <code>timestamp</code> 更晚的为准。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>落成一行</h4><p>合并结果写进 <code>observations</code> 表的<strong>同一行</strong>（id=body.id）；ReplacingMergeTree 在后台再做一次同样的去重兜底（第 8 课）。</p></div></div>
</div>
""")

# (taxonomy table + dedup code below)

_ZH13.append(r"""
<h2>18 种事件，3 张表</h2>
<p>事件 <code>type</code> 五花八门，但 worker 写库时只关心一件事：<strong>这条该进哪张表</strong>。一个叫 <code>getClickhouseEntityType</code> 的小函数把 18 种 type
干净地坍缩成 <strong>3 个实体类型</strong>——正好对应第 8 课的三张 ReplacingMergeTree 宽表：</p>

<table class="t">
  <tr><th>实体类型</th><th>由哪些事件 type 映射而来</th><th>落到哪张表（第 8 课）</th></tr>
  <tr><td><b>trace</b></td><td><code>trace-create</code></td><td><code>traces</code></td></tr>
  <tr><td><b>observation</b></td><td><code>event/span/generation-create·update</code> + <code>agent/tool/chain/retriever/evaluator/embedding/guardrail-create</code> + 旧 <code>observation-*</code></td><td><code>observations</code></td></tr>
  <tr><td><b>score</b></td><td><code>score-create</code></td><td><code>scores</code></td></tr>
</table>

<p>所有「像观测」的类型——无论它叫 span、generation 还是 agent——统统归到 <code>observation</code>，进同一张表，靠 observation 行里的 <code>type</code> 列区分。
这就是第 8 课「宽事件」的威力：<strong>一张表容纳所有观测形态</strong>，新增一种观测类型不必加表、不必改 schema。</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/processEventBatch.ts</span><span class="ln">分组</span></div>
  <pre class="code"><span class="cm">// 按 eventBodyId 把事件分组，使「同一实体」的多个事件能一起存、一起处理</span>
<span class="kw">const</span> entityType = <span class="fn">getClickhouseEntityType</span>(event.type);  <span class="cm">// → trace / observation / score</span>
<span class="kw">const</span> dedupKey = <span class="st">`${entityType}-${event.body.id}`</span>;       <span class="cm">// 合并键 = 实体类型 + 实体 id</span>

<span class="cm">// 每个事件以「事件 id」为名落 S3：&lt;eventId&gt;.json（同事件重发→覆盖同文件，幂等）</span>
key: <span class="fn">safeBlobFilenameStem</span>(event.id, <span class="st">".json"</span>),</pre>
</div>

<p>看清这段就懂了全局：<strong>实体 id（body.id）决定「合并到哪一行」，事件 id（envelope id）决定「在 S3 里叫什么名」</strong>。
前者保证 create/update 汇成一条；后者保证同一个事件重传一百次也只算一次。两套 id，两个目的，配合得严丝合缝。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么不直接做一个 upsert，非要拆成 create / update 两个事件？</strong> 因为<strong>SDK 端不该背状态</strong>。一次 LLM 调用，开始和结束之间可能隔着几秒、几十秒，
  期间应用甚至可能崩、可能换机器。如果要求「等结束后一次性 upsert 全量」，SDK 就得在内存里<strong>攥着</strong>这条记录直到结束——既占内存又怕丢。
  拆成 create + update，SDK 可以<strong>开始就发一半、结束再补一半</strong>，发完即忘；合并的脏活交给服务端按 body.id 去拼。<strong>把状态从客户端推给服务端</strong>，
  正是分布式系统里「让边缘无状态、让中心兜底」的经典思路——也呼应第 5 课那条「快路 / 慢路」分工。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>每个事件 = <strong>信封</strong>（<code>base</code>: id · timestamp · metadata + 判别字段 <code>type</code>）+ 随 type 而变的 <code>body</code>，由 <code>z.discriminatedUnion("type")</code> 拢成一个 schema。</li>
    <li>body 是<strong>继承链</strong>：<code>OptionalObservationBody</code> → +id <code>CreateEventEvent</code> → +endTime <code>CreateSpanBody</code> → +model/usage <code>CreateGenerationBody</code>，对应 EVENT⊂SPAN⊂GENERATION。</li>
    <li><strong>两套 id</strong>：实体 id（<code>body.id</code>）是合并键——同 id 的 create/update 汇成一行；事件 id（信封 id）是去重键——成为 S3 文件名，保证幂等。</li>
    <li>冲突字段<strong>以 timestamp 更晚者为准</strong>（last-write-wins），是第 8 课 <code>ReplacingMergeTree(event_ts)</code> 在写入侧的镜像。</li>
    <li><code>getClickhouseEntityType</code> 把 18 种事件 type 坍缩成 <strong>3 个实体类型</strong>（trace / observation / score）→ 第 8 课的三张宽表。</li>
  </ul>
</div>
""")

_EN13.append(r"""
<p class="lead">
Last lesson the API accepted <strong>a batch of events</strong> and enqueued them. Now we zoom into a <strong>single event</strong>: what does it
look like? Why does it have two faces, <code>create</code> and <code>update</code>? And most crucially — how do the <strong>several events</strong> your
SDK sends end up as <strong>one row</strong> in the database? This is the soul of Langfuse ingestion: <strong>an event stream merges into a
record</strong>. Get this and Lesson 8's <code>ReplacingMergeTree(event_ts, is_deleted)</code> design finally clicks into place.
</p>

<div class="card analogy">
  <div class="tag">🩺 Analogy</div>
  Think of one observation as a hospital <strong>chart</strong>. When the patient checks in, the doctor writes the first <strong>visit note</strong>
  (<code>generation-create</code>: start time, the input complaint). After tests and a prescription, the doctor <strong>adds a note</strong>
  (<code>generation-update</code>: end time, diagnosis, dosage). Both notes carry the <strong>same patient number</strong> (entity id) — so when
  filing, the nurse doesn't create two charts, she <strong>merges them into one</strong>, latest note winning on conflicts. Each note also has its
  own <strong>serial number</strong> (event id), so filing the same note twice never duplicates it. "Merge by patient number, dedup by serial" —
  exactly the two ids this lesson dissects.
</div>
""")

_EN13.append(r"""
<h2>The envelope: id · timestamp · type · body</h2>
<p>Every ingestion event — whether it describes a trace, an observation or a score — rides in the <strong>same envelope</strong>: a shared "shell"
plus a type-dependent payload <code>body</code>. Langfuse pins this down with Zod: a <code>base</code> (the shell), each type <code>extend</code>s it
with its own <code>type</code> and <code>body</code>, and finally a <strong>discriminated union</strong> (<code>z.discriminatedUnion("type", […])</code>)
gathers the dozen-plus events into one schema. To validate, Zod reads the <code>type</code> field and knows which <code>body</code> rules to apply —
"<strong>one field sets the identity, one ruleset per identity</strong>".</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="event envelope: base shell id/timestamp/metadata, the type field as discriminator routing to the matching body schema">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">An event's envelope: fixed shell, body varies by type</text>
  <rect x="30" y="44" width="230" height="180" rx="12" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="145" y="64" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">base (shared shell)</text>
  <rect x="48" y="76" width="194" height="26" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="58" y="93" font-size="9.5" fill="var(--ink)"><tspan font-weight="700">id</tspan> · event id (serial)</text>
  <rect x="48" y="108" width="194" height="26" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="58" y="125" font-size="9.5" fill="var(--ink)"><tspan font-weight="700">timestamp</tspan> · when it happened</text>
  <rect x="48" y="140" width="194" height="26" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="58" y="157" font-size="9.5" fill="var(--ink)"><tspan font-weight="700">metadata</tspan> · side info</text>
  <rect x="48" y="176" width="194" height="34" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="58" y="190" font-size="9.5" font-weight="700" fill="var(--accent-ink)">type · discriminator 🔑</text><text x="58" y="203" font-size="8" fill="var(--accent-ink)">picks the body ruleset below</text>
  <line x1="260" y1="193" x2="300" y2="193" stroke="var(--accent)" stroke-width="2"/><polygon points="300,193 290,188 290,198" fill="var(--accent)"/>
  <text x="280" y="184" text-anchor="middle" font-size="8" fill="var(--accent-ink)">route by type</text>
  <rect x="310" y="50" width="380" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="500" y="68" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">type=generation-create → body: CreateGenerationBody</text><text x="500" y="82" text-anchor="middle" font-size="8" fill="var(--accent-ink)">startTime · model · usage · input/output…</text>
  <rect x="310" y="98" width="380" height="40" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="500" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">type=span-update → body: UpdateSpanBody</text><text x="500" y="130" text-anchor="middle" font-size="8" fill="var(--muted)">id · endTime · output… (a patch)</text>
  <rect x="310" y="146" width="380" height="40" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="500" y="164" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">type=score-create → body: ScoreBody</text><text x="500" y="178" text-anchor="middle" font-size="8" fill="var(--muted)">name · value · dataType…</text>
  <rect x="310" y="194" width="380" height="28" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="500" y="212" text-anchor="middle" font-size="8.5" fill="var(--faint)">…18 types total (trace / 14 observation events / score / sdk-log / dataset-run-item)</text>
</svg>
<div class="figcap"><b>Envelope = fixed shell + variable body</b>: <code>base</code> holds <code>id</code> (event id), <code>timestamp</code>, <code>metadata</code> and the discriminator <code>type</code>; <code>type</code> decides which Zod ruleset the <code>body</code> follows. That's exactly how <code>z.discriminatedUnion("type", […])</code> works. Source: <code>packages/shared/src/server/ingestion/types.ts:597</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/types.ts</span><span class="ln">L597</span></div>
  <pre class="code"><span class="kw">const</span> base = z.<span class="fn">object</span>({
  id: idSchema,                        <span class="cm">// event id (serial)</span>
  timestamp: z.iso.<span class="fn">datetime</span>({ offset: <span class="kw">true</span> }),
  metadata: jsonSchema.<span class="fn">nullish</span>(),
});

<span class="kw">const</span> generationCreateEvent = base.<span class="fn">extend</span>({
  type: z.<span class="fn">literal</span>(eventTypes.GENERATION_CREATE),
  body: CreateGenerationBody,          <span class="cm">// payload varies by type</span>
});
<span class="cm">// …span-create / span-update / score-create / 18 in total…</span>

<span class="kw">const</span> ingestionEvent = z.<span class="fn">discriminatedUnion</span>(<span class="st">"type"</span>, [
  traceEvent, scoreEvent, spanCreateEvent, spanUpdateEvent,
  generationCreateEvent, generationUpdateEvent, <span class="cm">/* … */</span>
]);</pre>
</div>

<p>The beauty of the discriminated union: it isn't "make every field optional, fill in whatever" — it's <strong>a strict body ruleset per
type</strong>. Send <code>generation-create</code> and you must match <code>CreateGenerationBody</code>; send <code>score-create</code> and you must
match <code>ScoreBody</code> — wrong type or missing field, and Lesson 12's Zod gate rejects it on the spot. The schema even ships as <strong>two
instances, public and internal</strong>: things like <code>dataset-run-item-create</code> are internal-only and rejected on the public API.</p>
""")

_EN13.append(r"""
<h2>The body "matryoshka": Event ⊂ Span ⊂ Generation</h2>
<p>Those <code>body</code> schemas aren't written separately — they <strong>inherit layer by layer</strong>. The innermost is
<code>OptionalObservationBody</code> (traceId, name, startTime, input/output…); <code>extend</code> it with <code>id</code> to get
<code>CreateEventEvent</code>, add <code>endTime</code> for <code>CreateSpanBody</code>, then add <code>model / usage / modelParameters</code> for
<code>CreateGenerationBody</code>. This chain maps precisely onto Lesson 3's three observation kinds: <strong>EVENT is a point in time</strong> (no
duration), <strong>SPAN has start &amp; end</strong> (adds endTime), <strong>GENERATION is a SPAN with LLM fields</strong> (adds model/usage). Tellingly,
the newer observation types from Lesson 8 — AGENT / TOOL / CHAIN / RETRIEVER / EVALUATOR / EMBEDDING / GUARDRAIL — <strong>all reuse
<code>CreateGenerationBody</code></strong>: at heart they're each "a generation-rich span", differing only in semantic label.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="body inheritance chain: OptionalObservationBody plus id makes CreateEventEvent, plus endTime makes CreateSpanBody, plus model/usage makes CreateGenerationBody">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">The body schema inheritance chain (each outer layer adds fields)</text>
  <rect x="40" y="60" width="620" height="150" rx="12" fill="none" stroke="var(--teal)" stroke-dasharray="5 4"/>
  <text x="56" y="78" font-size="9" font-weight="700" fill="var(--teal)">CreateGenerationBody (+ model · usage · modelParameters · completionStartTime)</text>
  <rect x="70" y="88" width="560" height="112" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="86" y="106" font-size="9" font-weight="700" fill="var(--accent-ink)">CreateSpanBody (+ endTime)</text>
  <rect x="100" y="116" width="500" height="76" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="116" y="134" font-size="9" font-weight="700" fill="var(--ink)">CreateEventEvent (+ id)</text>
  <rect x="130" y="144" width="440" height="40" rx="8" fill="var(--bg)" stroke="var(--faint)"/>
  <text x="350" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">OptionalObservationBody</text>
  <text x="350" y="176" text-anchor="middle" font-size="8" fill="var(--muted)">traceId · name · startTime · input/output · level · parentObservationId…</text>
  <text x="685" y="120" text-anchor="end" font-size="8.5" fill="var(--accent-ink)">GENERATION</text>
  <text x="685" y="150" text-anchor="end" font-size="8.5" fill="var(--blue)">SPAN</text>
  <text x="685" y="178" text-anchor="end" font-size="8.5" fill="var(--faint)">EVENT</text>
</svg>
<div class="figcap"><b>The further out, the more capable</b>: EVENT is a duration-less point → SPAN adds <code>endTime</code> and gains start/end → GENERATION adds <code>model/usage</code>, becoming an LLM call that records tokens and cost. The 7 newer types (AGENT/TOOL/CHAIN…) reuse <code>CreateGenerationBody</code> directly. Source: <code>types.ts:421-470</code>.</div>
</div>

<p>This inheritance doesn't just save code, it makes <strong>the type semantics escalate step by step</strong>: you can't put an endTime on an EVENT
(its body simply has no such field), nor a usage on a SPAN. The schema is the documentation — read the chain and you see at a glance what each of
the three observation kinds can and cannot carry.</p>
""")

_EN13.append(r"""
<h2>The heart of it: several events, one row</h2>
<p>Now to answer the opening question. For one LLM call, the SDK usually sends <strong>two</strong> events: <code>generation-create</code> at the start
(with startTime, input) and <code>generation-update</code> at the end (with endTime, output, usage). Yet they land as <strong>the same observation
row</strong> in ClickHouse. The secret is <strong>two ids, each with its own job</strong>:</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">entity id</span><span class="name">body.id (merge key)</span></div><div class="ld">The id of the observation/trace itself. <strong>All events with the same body.id are destined to merge into one row</strong>. create and update share it, so they point at the same record.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">event id</span><span class="name">envelope base.id (dedup key)</span></div><div class="ld">Each event's own serial. In S3 it becomes the filename <code>&lt;eventId&gt;.json</code> — <strong>resend the same event, overwrite the same file, naturally idempotent</strong>, never counted twice.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">version</span><span class="name">timestamp (who wins)</span></div><div class="ld">When merging conflicting fields, <strong>the later-timestamped event wins</strong> (last-write-wins). This is the write-side mirror of Lesson 8's <code>ReplacingMergeTree(event_ts)</code>.</div></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="create and update events sharing one body.id merge by timestamp into one observation row, conflicts resolved latest-wins">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Event stream → one record (same body.id, latest wins)</text>
  <rect x="30" y="50" width="250" height="78" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="155" y="68" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">event ① generation-create</text>
  <text x="46" y="86" font-size="8.5" fill="var(--muted)">eventId=e1 · body.id=<tspan font-weight="700" fill="var(--accent-ink)">obs-42</tspan> · t=10:00:00</text>
  <text x="46" y="102" font-size="8.5" fill="var(--ink)">startTime=10:00 · input="..." </text>
  <text x="46" y="118" font-size="8.5" fill="var(--ink)">model="gpt-4o"</text>
  <rect x="30" y="140" width="250" height="78" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="155" y="158" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">event ② generation-update</text>
  <text x="46" y="176" font-size="8.5" fill="var(--accent-ink)">eventId=e2 · body.id=<tspan font-weight="700">obs-42</tspan> · t=10:00:03</text>
  <text x="46" y="192" font-size="8.5" fill="var(--accent-ink)">endTime=10:00:03 · output="..."</text>
  <text x="46" y="208" font-size="8.5" fill="var(--accent-ink)">usage={in:120,out:80}</text>
  <line x1="280" y1="134" x2="430" y2="134" stroke="var(--faint)" stroke-width="1.8"/><polygon points="430,134 420,129 420,139" fill="var(--faint)"/>
  <text x="355" y="126" text-anchor="middle" font-size="8.5" fill="var(--faint)">group &amp; merge by body.id</text>
  <rect x="440" y="74" width="250" height="120" rx="12" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/>
  <text x="565" y="94" text-anchor="middle" font-size="10" font-weight="700" fill="var(--teal)">merged observation row</text>
  <text x="456" y="114" font-size="8.5" fill="var(--ink)">id=<tspan font-weight="700" fill="var(--accent-ink)">obs-42</tspan> · type=GENERATION</text>
  <text x="456" y="132" font-size="8.5" fill="var(--ink)">startTime=10:00 · endTime=10:00:03</text>
  <text x="456" y="150" font-size="8.5" fill="var(--ink)">input + output (each takes the set side)</text>
  <text x="456" y="168" font-size="8.5" fill="var(--ink)">model=gpt-4o · usage={120,80}</text>
  <text x="456" y="186" font-size="8" fill="var(--muted)">conflicts: later-t ② wins</text>
</svg>
<div class="figcap"><b>create + update → one row</b>: the two events share <code>body.id=obs-42</code>, get grouped and merged; each field takes the side that has a value, conflicts resolved by later <code>timestamp</code>. The worker's merge logic (Lesson 15) is a "write-side rehearsal" of Lesson 8's ReplacingMergeTree behavior.</div>
</div>

<p>Break this "event stream → one row" path into five steps and the whole merge story is clear — the first two happen on your app side, the last
three on the Langfuse server:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>Start: send create</h4><p>As the LLM call begins, the SDK sends <code>generation-create</code> with <code>body.id</code>, startTime, input. Fire-and-forget, nothing held in memory.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>End: send update</h4><p>When the call ends, the SDK sends <code>generation-update</code>, <strong>reusing the same body.id</strong>, adding endTime, output, usage.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Group by body.id</h4><p>The server groups events with the same <code>dedupKey = entityType-body.id</code> — these two are recognized as "two reports of one record".</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>Merge fields (latest wins)</h4><p>Take the set side of each field; where both create and update gave a value, the later <code>timestamp</code> wins.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>Land as one row</h4><p>The merged result writes into <strong>one row</strong> of <code>observations</code> (id=body.id); ReplacingMergeTree re-dedups in the background as a safety net (Lesson 8).</p></div></div>
</div>
""")

_EN13.append(r"""
<h2>18 event types, 3 tables</h2>
<p>Event <code>type</code> comes in many flavors, but when the worker writes, it cares about one thing: <strong>which table does this go to</strong>. A
small function <code>getClickhouseEntityType</code> collapses the 18 types cleanly into <strong>3 entity types</strong> — exactly Lesson 8's three
ReplacingMergeTree wide tables:</p>

<table class="t">
  <tr><th>entity type</th><th>mapped from which event types</th><th>which table (Lesson 8)</th></tr>
  <tr><td><b>trace</b></td><td><code>trace-create</code></td><td><code>traces</code></td></tr>
  <tr><td><b>observation</b></td><td><code>event/span/generation-create·update</code> + <code>agent/tool/chain/retriever/evaluator/embedding/guardrail-create</code> + legacy <code>observation-*</code></td><td><code>observations</code></td></tr>
  <tr><td><b>score</b></td><td><code>score-create</code></td><td><code>scores</code></td></tr>
</table>

<p>Everything "observation-like" — be it span, generation or agent — lands in <code>observation</code>, the same table, distinguished by the
<code>type</code> column on the observation row. That's the power of Lesson 8's "wide events": <strong>one table holds every observation shape</strong>,
and adding a new observation kind needs no new table, no schema change.</p>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/processEventBatch.ts</span><span class="ln">grouping</span></div>
  <pre class="code"><span class="cm">// Group events by eventBodyId so multiple events of "one entity" store &amp; process together</span>
<span class="kw">const</span> entityType = <span class="fn">getClickhouseEntityType</span>(event.type);  <span class="cm">// → trace / observation / score</span>
<span class="kw">const</span> dedupKey = <span class="st">`${entityType}-${event.body.id}`</span>;       <span class="cm">// merge key = entity type + entity id</span>

<span class="cm">// each event lands in S3 named by its "event id": &lt;eventId&gt;.json (resend → overwrite, idempotent)</span>
key: <span class="fn">safeBlobFilenameStem</span>(event.id, <span class="st">".json"</span>),</pre>
</div>

<p>Read this snippet and the whole picture lands: <strong>the entity id (body.id) decides "which row to merge into", the event id (envelope id)
decides "what it's named in S3"</strong>. The former lets create/update converge into one record; the latter ensures resending the same event a
hundred times still counts once. Two ids, two purposes, fitting together seamlessly.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why not just do an upsert — why split into two create / update events?</strong> Because <strong>the SDK shouldn't carry state</strong>. An
  LLM call can take seconds, even tens of seconds, between start and end; meanwhile the app might crash or move machines. Requiring "wait until the
  end, then upsert the whole thing" forces the SDK to <strong>hold</strong> that record in memory until completion — costing memory and risking loss.
  Splitting into create + update lets the SDK <strong>send half at the start, the rest at the end</strong>, forgetting each as it goes; the dirty work
  of merging by body.id falls to the server. <strong>Pushing state from the client to the center</strong> is the classic distributed-systems move —
  "keep the edge stateless, let the center backstop it" — echoing Lesson 5's fast-lane / slow-lane split.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>Each event = an <strong>envelope</strong> (<code>base</code>: id · timestamp · metadata + discriminator <code>type</code>) + a type-varying <code>body</code>, gathered by <code>z.discriminatedUnion("type")</code> into one schema.</li>
    <li>body is an <strong>inheritance chain</strong>: <code>OptionalObservationBody</code> → +id <code>CreateEventEvent</code> → +endTime <code>CreateSpanBody</code> → +model/usage <code>CreateGenerationBody</code>, mapping EVENT⊂SPAN⊂GENERATION.</li>
    <li><strong>Two ids</strong>: entity id (<code>body.id</code>) is the merge key — same-id create/update converge into one row; event id (envelope id) is the dedup key — becomes the S3 filename, guaranteeing idempotency.</li>
    <li>Conflicting fields resolve <strong>by later timestamp</strong> (last-write-wins), the write-side mirror of Lesson 8's <code>ReplacingMergeTree(event_ts)</code>.</li>
    <li><code>getClickhouseEntityType</code> collapses the 18 event types into <strong>3 entity types</strong> (trace / observation / score) → Lesson 8's three wide tables.</li>
  </ul>
</div>
""")
LESSON_13 = {"zh": "\n".join(_ZH13), "en": "\n".join(_EN13)}

# ══════════════════════════════════════════════════════════════════════
# L14 · 摄取队列 / The ingestion queue
# ══════════════════════════════════════════════════════════════════════
_ZH14 = []
_EN14 = []

_ZH14.append(r"""
<p class="lead">
第 12 课 API「入队」后就闪人了，第 13 课讲清了入的是什么「事件」。这一课的主角，就是那条<strong>队列</strong>本身——Langfuse 用 <strong>Redis + BullMQ</strong>
搭起来的传送带。它是第 5 课「快路 / 慢路」之间的<strong>交接点</strong>：web 把活儿往上一放就走人，worker 在另一头不紧不慢地取走慢慢做。
这一课要回答三个问题：队列里到底放了<strong>什么</strong>（剧透：不是事件本体，而是一张「取件票」）、为什么要分<strong>主队列 / 次队列</strong>、以及高并发下怎么<strong>分片</strong>扛住洪峰。
</p>

<div class="card analogy">
  <div class="tag">🛄 生活类比</div>
  把队列想成机场的<strong>行李传送带</strong>。值机柜台（API）不会把你的行李箱直接堆在柜台上——它把箱子送进<strong>后仓</strong>（S3），只在传送带上放一张<strong>行李条</strong>（指针：箱子在后仓的编号）。
  分拣员（worker）从传送带上取下行李条，<strong>照着编号去后仓取箱子</strong>，再处理。这样设计的妙处：传送带（Redis 内存）只跑轻飘飘的纸条，<strong>又快又省</strong>；
  真正笨重的箱子（事件本体，可能很大）安安静静躺在后仓。万一分拣员忙不过来，纸条就在带上排队等着，<strong>箱子一件都不会丢</strong>——因为后仓才是货物的「真账本」。
</div>
""")

# (L14 sections appended below)

_ZH14.append(r"""
<h2>队列里放的是「取件票」，不是事件本体</h2>
<p>这是整条摄取链路最容易误解的一点：Redis 队列里<strong>并不存事件的完整内容</strong>。第 12 课 <code>processEventBatch</code> 在入队前，先把每个事件按
<code>&lt;eventId&gt;.json</code> 的名字<strong>写进 S3</strong>（第 13 课的事件 id 在这里当文件名）；队列里只放一个<strong>轻量任务</strong>，载荷里关键的就一个 <code>fileKey</code>——
指向 S3 里那个文件。worker 取到任务，再<strong>照着 fileKey 去 S3 把事件读回来</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="web 把事件写入 S3 并把含 fileKey 的轻量任务放入 Redis 队列，worker 取任务后照 fileKey 从 S3 读回事件再交给 IngestionService">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">交接：S3 存本体，队列只递指针</text>
  <rect x="24" y="80" width="120" height="70" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="84" y="108" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">web</text><text x="84" y="124" text-anchor="middle" font-size="8" fill="var(--muted)">processEventBatch</text><text x="84" y="138" text-anchor="middle" font-size="8" fill="var(--muted)">（第 12 课）</text>
  <rect x="300" y="36" width="170" height="56" rx="10" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="385" y="58" text-anchor="middle" font-size="10" font-weight="700" fill="var(--amber)">S3 事件日志</text><text x="385" y="74" text-anchor="middle" font-size="8" fill="var(--muted)">&lt;eventId&gt;.json（本体，可能很大）</text>
  <rect x="300" y="140" width="170" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="385" y="162" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">Redis 队列（BullMQ）</text><text x="385" y="178" text-anchor="middle" font-size="8" fill="var(--accent-ink)">任务载荷：fileKey · eventBodyId · type</text>
  <rect x="576" y="80" width="120" height="70" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="636" y="104" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">worker</text><text x="636" y="120" text-anchor="middle" font-size="8" fill="var(--muted)">取任务 → 读 S3</text><text x="636" y="134" text-anchor="middle" font-size="8" fill="var(--muted)">→ IngestionService</text>
  <line x1="144" y1="100" x2="298" y2="70" stroke="var(--amber)" stroke-width="1.8"/><polygon points="298,70 288,70 293,79" fill="var(--amber)"/><text x="215" y="78" text-anchor="middle" font-size="8" fill="var(--amber)">① 写本体</text>
  <line x1="144" y1="128" x2="298" y2="162" stroke="var(--accent)" stroke-width="1.8"/><polygon points="298,162 288,158 290,168" fill="var(--accent)"/><text x="215" y="158" text-anchor="middle" font-size="8" fill="var(--accent-ink)">② 放指针</text>
  <line x1="470" y1="168" x2="574" y2="120" stroke="var(--accent)" stroke-width="1.8"/><polygon points="574,120 564,120 569,129" fill="var(--accent)"/><text x="528" y="158" text-anchor="middle" font-size="8" fill="var(--accent-ink)">③ 取指针</text>
  <line x1="574" y1="100" x2="472" y2="66" stroke="var(--amber)" stroke-width="1.8" stroke-dasharray="3 2"/><polygon points="472,66 482,66 477,75" fill="var(--amber)"/><text x="528" y="74" text-anchor="middle" font-size="8" fill="var(--amber)">④ 按 fileKey 读回</text>
  <text x="360" y="222" text-anchor="middle" font-size="9" fill="var(--faint)">队列轻 → Redis 内存省、入队快；本体重 → 落 S3 当「真账本」，任务丢了也能从 S3 重建</text>
</svg>
<div class="figcap"><b>指针与本体分离</b>：事件本体写入 S3（<code>&lt;eventId&gt;.json</code>），队列里只放含 <code>fileKey</code> 的轻量任务。worker 取任务后照 <code>fileKey</code> 回 S3 读本体。源码：<code>processEventBatch.ts:340-398</code>（<code>queue.add(IngestionJob, {payload:{data:{type, eventBodyId, fileKey,…}, authCheck}}})</code>）。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/processEventBatch.ts</span><span class="ln">入队</span></div>
  <pre class="code"><span class="kw">const</span> shardingKey = <span class="st">`${projectId}-${eventData.eventBodyId}`</span>;   <span class="cm">// 分片键（见下）</span>
<span class="kw">const</span> queue = IngestionQueue.<span class="fn">getInstance</span>({ shardingKey });

<span class="kw">await</span> queue.<span class="fn">add</span>(QueueJobs.IngestionJob, {
  id: <span class="fn">randomUUID</span>(), timestamp: <span class="kw">new</span> Date(),
  payload: {
    data: { type, eventBodyId, fileKey: eventData.key, <span class="cm">/* 指向 S3 */</span> },
    authCheck,                          <span class="cm">// 把租户身份也带上（第 10 课）</span>
  },
}, { delay });</pre>
</div>

<div class="cols">
  <div class="col"><h4>📨 队列只放指针</h4><p>载荷是 <code>{ type, eventBodyId, fileKey, authCheck }</code> 这种几十字节的小任务。Redis 内存金贵，任务越小，入队越快、积压时也撑得住。</p></div>
  <div class="col"><h4>📦 S3 存本体</h4><p>事件原文（input/output 可能很大）躺在 S3。它还是第 15 课「合并」要回读的<strong>历史事件源</strong>，更是任务万一丢失时的<strong>可重建依据</strong>。</p></div>
</div>

<p>入队时还藏着一个细节：<code>queue.add(…, { delay })</code> 给任务挂了一小段<strong>延迟</strong>（默认约 5 秒）。为什么要故意「慢一拍」？因为同一实体的 create 和 update
可能<strong>先后脚到达</strong>，若 worker 抢在 update 落 S3 之前就处理 create，容易产生重复或乱序写入。延迟让一批相关事件先「落定」，worker 再统一取走，<strong>天然减少重复处理</strong>。
更妙的是 <code>getDelay</code> 在每天 UTC 的 <code>23:45–00:15</code> 这段「日界线」会把延迟拉长——因为第 8 课的排序键里有 <code>toDate(start_time)</code>，跨午夜的事件若处理太急，
可能被分到相邻两天的分区里造成重复。这个不起眼的延迟，正是为第 8 课那套按天组织的存储「保驾护航」，是工程上「用一点延迟换一致性」的典型权衡。</p>
""")

# (sharding section below)

_ZH14.append(r"""
<h2>分片：把一条队列摊成 N 条，扛住洪峰</h2>
<p>单条 Redis 队列总有上限。当部署开启 Redis 集群（<code>REDIS_CLUSTER_ENABLED=true</code>）时，摄取队列会<strong>分片</strong>成多条：
<code>ingestion-queue</code>、<code>ingestion-queue-1</code>、<code>ingestion-queue-2</code>……数量由 <code>LANGFUSE_INGESTION_QUEUE_SHARD_COUNT</code> 决定。
分到哪条，取决于<strong>分片键</strong> <code>projectId-eventBodyId</code> 的哈希：用 SHA-256 算出一个数，对分片数取模，得到 shard 下标。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="分片键 projectId-eventBodyId 经 SHA-256 哈希取模映射到某条 shard 队列，同一实体的事件始终落同一 shard">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一致性哈希分片：同一实体永远落同一 shard</text>
  <rect x="24" y="92" width="180" height="54" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="113" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">分片键</text><text x="114" y="130" text-anchor="middle" font-size="8.5" fill="var(--muted)">projectId-eventBodyId</text>
  <rect x="244" y="92" width="150" height="54" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="319" y="113" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">SHA-256 % N</text><text x="319" y="130" text-anchor="middle" font-size="8" fill="var(--accent-ink)">getShardIndex()</text>
  <line x1="204" y1="119" x2="242" y2="119" stroke="var(--faint)" stroke-width="1.8"/><polygon points="242,119 233,114 233,124" fill="var(--faint)"/>
  <rect x="470" y="44" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="580" y="65" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ingestion-queue（shard 0）</text>
  <rect x="470" y="86" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="107" text-anchor="middle" font-size="9" fill="var(--ink)">ingestion-queue-1</text>
  <rect x="470" y="128" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="149" text-anchor="middle" font-size="9" fill="var(--ink)">ingestion-queue-2</text>
  <rect x="470" y="170" width="220" height="28" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="580" y="189" text-anchor="middle" font-size="8.5" fill="var(--faint)">…直到 SHARD_COUNT-1</text>
  <line x1="394" y1="116" x2="468" y2="61" stroke="var(--faint)" stroke-width="1.4"/><line x1="394" y1="119" x2="468" y2="103" stroke="var(--faint)" stroke-width="1.4"/><line x1="394" y1="122" x2="468" y2="145" stroke="var(--faint)" stroke-width="1.4"/>
  <text x="360" y="216" text-anchor="middle" font-size="9" fill="var(--faint)">同一 projectId-eventBodyId → 同一哈希 → 同一 shard：create 和 update 永远在一条队列里、有序处理</text>
</svg>
<div class="figcap"><b>分片但不打乱实体</b>：哈希的是 <code>projectId-eventBodyId</code>，所以同一实体的所有事件（create/update）<strong>必然落到同一条 shard</strong>，既把负载摊到多个 Redis 节点，又保证一条记录的多次上报被同一个 worker 有序处理。源码：<code>redis/ingestionQueue.ts:38-52</code>、<code>redis/sharding.ts:9</code>。</div>
</div>

<p>注意分片键选 <code>projectId-eventBodyId</code> 而不是随机数，是有讲究的：随机分会把同一条记录的 create 和 update <strong>打散到不同 shard</strong>，
合并时就得跨队列协调，既复杂又可能乱序。用实体 id 当分片键，<strong>「同一实体同一 shard」</strong>天然成立——这和第 8 课用 <code>project_id</code> 领头排序键、
第 13 课用 <code>body.id</code> 当合并键，是同一种「让相关数据物理上聚在一起」的思路。</p>
""")

# (primary-secondary + worker flow below)

_ZH14.append(r"""
<h2>主队列 vs 次队列：别让吵闹的租户堵住所有人</h2>
<p>所有项目共用一条主队列，会有个隐患：某个超高吞吐的项目<strong>瞬间灌进百万事件</strong>，把队列塞满，其他项目的事件只能干等。Langfuse 的解法是<strong>次队列隔离</strong>：
worker 在处理每个任务前先判断——这个 project 该不该<strong>改道</strong>去次队列？判断有两条：</p>

<table class="t">
  <tr><th>判断</th><th>触发条件</th><th>含义</th></tr>
  <tr><td><b>env 白名单</b></td><td>project 在 <code>LANGFUSE_SECONDARY_INGESTION_QUEUE_ENABLED_PROJECT_IDS</code> 里</td><td>已知的高吞吐大户，<strong>静态</strong>隔离到次队列</td></tr>
  <tr><td><b>S3 限流标志</b></td><td><code>hasS3SlowdownFlag(projectId)</code> 为真</td><td>该项目刚把 S3 写出 SlowDown，<strong>动态</strong>临时改道，给主队列减压</td></tr>
  <tr><td><b>都不满足</b></td><td>—</td><td>留在主队列正常处理</td></tr>
</table>

<p>命中任一条，worker 就把这条任务原样 <code>add</code> 进 <code>SecondaryIngestionQueue</code> 然后 <code>return</code>，主队列立刻腾出手处理别人的。
次队列有自己独立的分片数（<code>LANGFUSE_INGESTION_SECONDARY_QUEUE_SHARD_COUNT</code>）和独立的 worker，<strong>洪峰与日常彻底物理隔离</strong>，互不拖累。OTel 摄取也有同样的主 / 次一对（第 18 课）。</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>worker 取下一个任务</h4><p>从某条 shard 队列拿到 <code>{ fileKey, eventBodyId, type, authCheck }</code>。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>判断是否改道次队列</h4><p>命中 env 白名单或 S3 限流标志 → 重新入次队列并结束；否则继续。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>照 fileKey 读 S3</h4><p>取回事件本体（以及该实体此前的历史事件，供第 15 课合并）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>交给 IngestionService</h4><p><code>mergeAndWrite</code> 合并成一条记录（第 15 课），再交 <code>ClickhouseWriter</code> 攒批写库（第 17 课）。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>失败则重试</h4><p>任务配 <code>attempts: 6</code> + 指数退避（5s 起）；成功即 <code>removeOnComplete</code>，失败保留便于排查。</p></div></div>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么非要队列 + S3 这一套，不能 API 直接写库？</strong> 因为这套组合同时买到了<strong>解耦</strong>和<strong>持久</strong>两样东西。解耦：web 和 worker 各按自己的节奏跑，
  worker 挂了、ClickHouse 抖了，事件就在队列里排队、在 S3 里躺着，<strong>一条不丢</strong>，等下游恢复再慢慢消化（第 5 课最终一致）。持久：S3 是事件的「真账本」，
  即便某个队列任务彻底失败，数据也能从 S3 重放重建。代价是多了一跳（写 S3 + 入队 + 读 S3）和最终一致的延迟，但换来的是一个<strong>削峰、容错、可重放</strong>的摄取管道——
  对一个每天吞百亿事件的系统，这笔买卖太划算了。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>队列用 <strong>Redis + BullMQ</strong>，是 web（快路）与 worker（慢路）的交接点；任务载荷只放<strong>指针</strong>（<code>fileKey</code> 等），事件本体在 <strong>S3</strong>。</li>
    <li><strong>S3 是真账本</strong>：本体落 <code>&lt;eventId&gt;.json</code>，既供第 15 课合并回读，也让任务丢失时能重建——队列轻、内存省、可重放。</li>
    <li><strong>分片</strong>：集群下队列拆成 <code>ingestion-queue-N</code>，按 <code>projectId-eventBodyId</code> 的 SHA-256 取模定 shard——同一实体永远同一 shard，有序又均衡。</li>
    <li><strong>主 / 次队列</strong>：按 env 白名单（静态）或 S3 限流标志（动态）把高吞吐项目改道次队列，物理隔离，避免一个吵闹租户堵住所有人。</li>
    <li><strong>韧性</strong>：任务 <code>attempts: 6</code> + 指数退避；成功即删、失败保留。队列 + S3 = 削峰 + 容错 + 可重放。</li>
  </ul>
</div>
""")

_EN14.append(r"""
<p class="lead">
Lesson 12 had the API "enqueue" and vanish; Lesson 13 explained what "event" it enqueues. The star of this lesson is the <strong>queue</strong>
itself — a conveyor belt built on <strong>Redis + BullMQ</strong>. It's the <strong>handoff point</strong> between Lesson 5's fast lane and slow lane:
web drops the work and leaves, while the worker pulls it off the other end and processes at its own pace. Three questions to answer: what's actually
<strong>in</strong> the queue (spoiler: not the event itself, but a "claim ticket"), why split into a <strong>primary / secondary</strong> queue, and how
<strong>sharding</strong> survives spikes under high concurrency.
</p>

<div class="card analogy">
  <div class="tag">🛄 Analogy</div>
  Think of the queue as an airport <strong>baggage belt</strong>. The check-in desk (API) doesn't pile your suitcase on the counter — it sends the case
  to the <strong>back room</strong> (S3) and puts only a <strong>baggage tag</strong> (a pointer: the case's id in the back room) on the belt. A handler
  (worker) takes the tag off the belt, <strong>fetches the case by its id</strong>, then processes it. The beauty: the belt (Redis memory) only carries
  featherweight tags, <strong>fast and cheap</strong>; the bulky cases (event bodies, possibly large) rest quietly in the back. If handlers fall behind,
  tags simply queue on the belt and <strong>not a single case is lost</strong> — because the back room is the goods' "real ledger".
</div>
""")

# (L14 EN more sections)

_EN14.append(r"""
<h2>The queue holds a "claim ticket", not the event body</h2>
<p>Here's the most-misunderstood point of the whole ingestion path: the Redis queue <strong>does not store the event's full content</strong>. Before
enqueuing, Lesson 12's <code>processEventBatch</code> first <strong>writes each event to S3</strong> named <code>&lt;eventId&gt;.json</code> (Lesson 13's
event id becomes the filename); the queue holds only a <strong>lightweight job</strong> whose key field is a <code>fileKey</code> — a pointer to that S3
file. The worker takes the job, then <strong>reads the event back from S3 by fileKey</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="web writes the event to S3 and puts a lightweight job carrying fileKey on the Redis queue; the worker takes the job and reads the event from S3 by fileKey then hands to IngestionService">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Handoff: S3 stores the body, the queue passes a pointer</text>
  <rect x="24" y="80" width="120" height="70" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="84" y="108" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">web</text><text x="84" y="124" text-anchor="middle" font-size="8" fill="var(--muted)">processEventBatch</text><text x="84" y="138" text-anchor="middle" font-size="8" fill="var(--muted)">(Lesson 12)</text>
  <rect x="300" y="36" width="170" height="56" rx="10" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="385" y="58" text-anchor="middle" font-size="10" font-weight="700" fill="var(--amber)">S3 event log</text><text x="385" y="74" text-anchor="middle" font-size="8" fill="var(--muted)">&lt;eventId&gt;.json (body, may be large)</text>
  <rect x="300" y="140" width="170" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="385" y="162" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">Redis queue (BullMQ)</text><text x="385" y="178" text-anchor="middle" font-size="8" fill="var(--accent-ink)">job: fileKey · eventBodyId · type</text>
  <rect x="576" y="80" width="120" height="70" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="636" y="104" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">worker</text><text x="636" y="120" text-anchor="middle" font-size="8" fill="var(--muted)">take job → read S3</text><text x="636" y="134" text-anchor="middle" font-size="8" fill="var(--muted)">→ IngestionService</text>
  <line x1="144" y1="100" x2="298" y2="70" stroke="var(--amber)" stroke-width="1.8"/><polygon points="298,70 288,70 293,79" fill="var(--amber)"/><text x="215" y="78" text-anchor="middle" font-size="8" fill="var(--amber)">① write body</text>
  <line x1="144" y1="128" x2="298" y2="162" stroke="var(--accent)" stroke-width="1.8"/><polygon points="298,162 288,158 290,168" fill="var(--accent)"/><text x="215" y="158" text-anchor="middle" font-size="8" fill="var(--accent-ink)">② put pointer</text>
  <line x1="470" y1="168" x2="574" y2="120" stroke="var(--accent)" stroke-width="1.8"/><polygon points="574,120 564,120 569,129" fill="var(--accent)"/><text x="528" y="158" text-anchor="middle" font-size="8" fill="var(--accent-ink)">③ take pointer</text>
  <line x1="574" y1="100" x2="472" y2="66" stroke="var(--amber)" stroke-width="1.8" stroke-dasharray="3 2"/><polygon points="472,66 482,66 477,75" fill="var(--amber)"/><text x="528" y="74" text-anchor="middle" font-size="8" fill="var(--amber)">④ read back by fileKey</text>
  <text x="360" y="222" text-anchor="middle" font-size="9" fill="var(--faint)">light queue → Redis memory saved, fast enqueue; heavy body → S3 as "real ledger", rebuildable if a job is lost</text>
</svg>
<div class="figcap"><b>Pointer and body, separated</b>: the event body is written to S3 (<code>&lt;eventId&gt;.json</code>); the queue holds only a lightweight job carrying <code>fileKey</code>. The worker reads the body back from S3 by <code>fileKey</code>. Source: <code>processEventBatch.ts:340-398</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/ingestion/processEventBatch.ts</span><span class="ln">enqueue</span></div>
  <pre class="code"><span class="kw">const</span> shardingKey = <span class="st">`${projectId}-${eventData.eventBodyId}`</span>;   <span class="cm">// shard key (below)</span>
<span class="kw">const</span> queue = IngestionQueue.<span class="fn">getInstance</span>({ shardingKey });

<span class="kw">await</span> queue.<span class="fn">add</span>(QueueJobs.IngestionJob, {
  id: <span class="fn">randomUUID</span>(), timestamp: <span class="kw">new</span> Date(),
  payload: {
    data: { type, eventBodyId, fileKey: eventData.key, <span class="cm">/* points to S3 */</span> },
    authCheck,                          <span class="cm">// carry the tenant identity too (Lesson 10)</span>
  },
}, { delay });</pre>
</div>

<div class="cols">
  <div class="col"><h4>📨 the queue holds a pointer</h4><p>The payload is a tiny <code>{ type, eventBodyId, fileKey, authCheck }</code> job of a few dozen bytes. Redis memory is precious; the smaller the job, the faster the enqueue and the better it holds up under backlog.</p></div>
  <div class="col"><h4>📦 S3 holds the body</h4><p>The raw event (input/output can be large) sits in S3. It's also the <strong>historical event source</strong> Lesson 15's merge reads back, and the <strong>basis for rebuilding</strong> should a job ever be lost.</p></div>
</div>

<p>One more detail hides in the enqueue: <code>queue.add(…, { delay })</code> attaches a small <strong>delay</strong> (about 5s by default). Why be
deliberately "a beat slow"? Because the create and update for one entity may arrive <strong>back to back</strong>; if a worker processes the create
before the update lands in S3, duplicates or out-of-order writes can result. The delay lets a batch of related events "settle" first, so the worker
takes them together, <strong>naturally reducing duplicate processing</strong>. Better still, <code>getDelay</code> lengthens the delay around the UTC
<code>23:45–00:15</code> "date boundary" — because Lesson 8's ordering key contains <code>toDate(start_time)</code>, events straddling midnight, if
processed too eagerly, could split across two date partitions and duplicate. This unassuming delay is exactly what safeguards Lesson 8's
day-organized storage — a classic "trade a little latency for consistency".</p>
""")

_EN14.append(r"""
<h2>Sharding: split one queue into N, survive the spike</h2>
<p>A single Redis queue always has a ceiling. When a deployment enables Redis cluster (<code>REDIS_CLUSTER_ENABLED=true</code>), the ingestion queue is
<strong>sharded</strong> into several: <code>ingestion-queue</code>, <code>ingestion-queue-1</code>, <code>ingestion-queue-2</code>… the count set by
<code>LANGFUSE_INGESTION_QUEUE_SHARD_COUNT</code>. Which shard depends on the hash of the <strong>shard key</strong> <code>projectId-eventBodyId</code>:
SHA-256 produces a number, taken modulo the shard count to yield a shard index.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="shard key projectId-eventBodyId hashed by SHA-256 modulo maps to one shard queue; events of one entity always land on the same shard">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Consistent-hash sharding: one entity always lands on one shard</text>
  <rect x="24" y="92" width="180" height="54" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="113" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">shard key</text><text x="114" y="130" text-anchor="middle" font-size="8.5" fill="var(--muted)">projectId-eventBodyId</text>
  <rect x="244" y="92" width="150" height="54" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="319" y="113" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">SHA-256 % N</text><text x="319" y="130" text-anchor="middle" font-size="8" fill="var(--accent-ink)">getShardIndex()</text>
  <line x1="204" y1="119" x2="242" y2="119" stroke="var(--faint)" stroke-width="1.8"/><polygon points="242,119 233,114 233,124" fill="var(--faint)"/>
  <rect x="470" y="44" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="580" y="65" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ingestion-queue (shard 0)</text>
  <rect x="470" y="86" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="107" text-anchor="middle" font-size="9" fill="var(--ink)">ingestion-queue-1</text>
  <rect x="470" y="128" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="149" text-anchor="middle" font-size="9" fill="var(--ink)">ingestion-queue-2</text>
  <rect x="470" y="170" width="220" height="28" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="580" y="189" text-anchor="middle" font-size="8.5" fill="var(--faint)">…up to SHARD_COUNT-1</text>
  <line x1="394" y1="116" x2="468" y2="61" stroke="var(--faint)" stroke-width="1.4"/><line x1="394" y1="119" x2="468" y2="103" stroke="var(--faint)" stroke-width="1.4"/><line x1="394" y1="122" x2="468" y2="145" stroke="var(--faint)" stroke-width="1.4"/>
  <text x="360" y="216" text-anchor="middle" font-size="9" fill="var(--faint)">same projectId-eventBodyId → same hash → same shard: create &amp; update always in one queue, processed in order</text>
</svg>
<div class="figcap"><b>Shard without scattering an entity</b>: the hash is over <code>projectId-eventBodyId</code>, so all events of one entity (create/update) <strong>necessarily land on the same shard</strong> — spreading load across Redis nodes while keeping a record's multiple reports ordered on one worker. Source: <code>redis/ingestionQueue.ts:38-52</code>, <code>redis/sharding.ts:9</code>.</div>
</div>

<p>Choosing <code>projectId-eventBodyId</code> as the shard key — rather than a random number — is deliberate: random sharding would <strong>scatter</strong>
one record's create and update across different shards, forcing cross-queue coordination at merge time, complex and prone to disorder. Using the entity
id as the shard key makes <strong>"same entity, same shard"</strong> hold naturally — the same idea as Lesson 8 leading the ordering key with
<code>project_id</code> and Lesson 13 using <code>body.id</code> as the merge key: <strong>keep related data physically together</strong>.</p>
""")

_EN14.append(r"""
<h2>Primary vs secondary: don't let a noisy tenant block everyone</h2>
<p>All projects sharing one primary queue has a hazard: one ultra-high-throughput project <strong>floods in a million events</strong>, packs the queue,
and everyone else's events just wait. Langfuse's answer is <strong>secondary-queue isolation</strong>: before processing each job, the worker decides —
should this project be <strong>redirected</strong> to the secondary queue? Two checks:</p>

<table class="t">
  <tr><th>check</th><th>trigger</th><th>meaning</th></tr>
  <tr><td><b>env allowlist</b></td><td>project is in <code>LANGFUSE_SECONDARY_INGESTION_QUEUE_ENABLED_PROJECT_IDS</code></td><td>a known high-throughput heavy hitter, <strong>statically</strong> isolated to the secondary</td></tr>
  <tr><td><b>S3 slowdown flag</b></td><td><code>hasS3SlowdownFlag(projectId)</code> is true</td><td>this project just got an S3 SlowDown, <strong>dynamically</strong> redirected to relieve the primary</td></tr>
  <tr><td><b>neither</b></td><td>—</td><td>stays on the primary, processed normally</td></tr>
</table>

<p>On either hit, the worker <code>add</code>s the job as-is to <code>SecondaryIngestionQueue</code> and <code>return</code>s, freeing the primary to serve
others immediately. The secondary has its own shard count (<code>LANGFUSE_INGESTION_SECONDARY_QUEUE_SHARD_COUNT</code>) and its own workers, so spike and
steady-state are <strong>physically isolated</strong>, neither dragging the other. OTel ingestion has the same primary/secondary pair (Lesson 18).</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>worker takes the next job</h4><p>Pulls <code>{ fileKey, eventBodyId, type, authCheck }</code> off one shard queue.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>decide secondary redirect</h4><p>Hit the env allowlist or the S3 slowdown flag → re-enqueue to the secondary and finish; else continue.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>read S3 by fileKey</h4><p>Fetch the event body (plus this entity's prior events, for Lesson 15's merge).</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>hand to IngestionService</h4><p><code>mergeAndWrite</code> merges into one record (Lesson 15), then <code>ClickhouseWriter</code> batches the write (Lesson 17).</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>retry on failure</h4><p>Jobs carry <code>attempts: 6</code> + exponential backoff (from 5s); <code>removeOnComplete</code> on success, kept on failure for debugging.</p></div></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why insist on queue + S3 — why not have the API write the DB directly?</strong> Because the combo buys both <strong>decoupling</strong> and
  <strong>durability</strong>. Decoupling: web and worker each run at their own pace; if the worker dies or ClickHouse hiccups, events queue in Redis and
  rest in S3, <strong>not one lost</strong>, digested once downstream recovers (Lesson 5's eventual consistency). Durability: S3 is the events' "real
  ledger" — even if a queue job fails outright, the data can be replayed and rebuilt from S3. The cost is an extra hop (write S3 + enqueue + read S3)
  and eventual-consistency latency, but in return you get a <strong>spike-absorbing, fault-tolerant, replayable</strong> ingestion pipeline — for a
  system swallowing tens of billions of events a day, a bargain.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>The queue is <strong>Redis + BullMQ</strong>, the handoff between web (fast lane) and worker (slow lane); the job carries only a <strong>pointer</strong> (<code>fileKey</code> etc.), the event body lives in <strong>S3</strong>.</li>
    <li><strong>S3 is the real ledger</strong>: bodies land in <code>&lt;eventId&gt;.json</code>, read back for Lesson 15's merge and able to rebuild a lost job — light queue, saved memory, replayable.</li>
    <li><strong>Sharding</strong>: under cluster the queue splits into <code>ingestion-queue-N</code>, shard chosen by SHA-256 modulo of <code>projectId-eventBodyId</code> — same entity always same shard, ordered and balanced.</li>
    <li><strong>Primary / secondary</strong>: redirect high-throughput projects to the secondary by env allowlist (static) or S3 slowdown flag (dynamic), physically isolating them so one noisy tenant can't block everyone.</li>
    <li><strong>Resilience</strong>: jobs use <code>attempts: 6</code> + exponential backoff; removed on success, kept on failure. Queue + S3 = spike absorption + fault tolerance + replayability.</li>
  </ul>
</div>
""")
LESSON_14 = {"zh": "\n".join(_ZH14), "en": "\n".join(_EN14)}


# ══════════════════════════════════════════════════════════════════════
# L15 · IngestionService：合并的心脏 / IngestionService: the merge heart
# ══════════════════════════════════════════════════════════════════════
_ZH15 = []
_EN15 = []

_ZH15.append(r"""
<p class="lead">
第 14 课 worker 取走任务、照 fileKey 把事件从 S3 读了回来。这一课是整条写入链路的<strong>心脏</strong>：那一堆事件，外加数据库里这条记录的<strong>当前状态</strong>，
究竟怎么被揉成<strong>一条最终记录</strong>？答案藏在 <code>IngestionService</code> 里——<code>mergeAndWrite</code> 按实体类型分流，
<code>mergeRecords</code> 用一招「左折叠 + 后者覆盖」把多份输入合一，再盖上 <code>event_ts=now</code> 的版本戳。读懂它，第 8 课 ReplacingMergeTree 的「写入侧另一半」就补齐了。
</p>

<div class="card analogy">
  <div class="tag">📝 生活类比</div>
  把合并想成<strong>协作编辑一篇维基词条</strong>。数据库里<strong>当前发布的版本</strong>是底稿；这次收到的每个事件，就像一条按时间排好的<strong>修订</strong>，
  依次盖在底稿上。后改的覆盖先改的（同一字段，新值赢）；但<strong>某条修订没碰的字段，保持原样</strong>（你只改了「结论」，「正文」不会被清空）。
  还有几样东西被<strong>锁死</strong>，谁都不能改：词条的<strong>创建时间、唯一 id</strong>。所有修订叠完，得到一份<strong>合并稿</strong>，标上「本次合并时刻」当版本号——
  这正是 <code>IngestionService</code> 干的事：底稿来自 ClickHouse，修订来自 S3，叠出来的合并稿写回库。
</div>
""")

# (L15 sections appended below)

_ZH15.append(r"""
<h2>mergeAndWrite：先按实体类型分流</h2>
<p><code>mergeAndWrite</code> 本身只是个<strong>调度员</strong>。它拿到第 13 课算出的实体类型（trace / observation / score / dataset_run_item），
用一个 <code>switch</code> 把活儿分给对应的 <code>process{Type}EventList</code>。每条线路的骨架一样——<strong>读旧、转换、合并、写回</strong>——只是字段细节随类型而异。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="mergeAndWrite 按实体类型 switch 分派到 processTrace/Observation/Score/DatasetRunItem EventList 四条处理线">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">mergeAndWrite：一个 switch，四条处理线</text>
  <rect x="280" y="40" width="160" height="46" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="60" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">mergeAndWrite</text><text x="360" y="76" text-anchor="middle" font-size="8" fill="var(--accent-ink)">switch (entityType)</text>
  <rect x="24" y="130" width="158" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="103" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">processTrace</text><text x="103" y="165" text-anchor="middle" font-size="8" fill="var(--muted)">EventList</text><text x="103" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">→ traces 表</text>
  <rect x="194" y="130" width="158" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="273" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">processObservation</text><text x="273" y="165" text-anchor="middle" font-size="8" fill="var(--accent-ink)">EventList</text><text x="273" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">→ observations 表（最复杂）</text>
  <rect x="364" y="130" width="158" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="443" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">processScore</text><text x="443" y="165" text-anchor="middle" font-size="8" fill="var(--muted)">EventList</text><text x="443" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">→ scores 表</text>
  <rect x="534" y="130" width="162" height="56" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="615" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">processDatasetRunItem</text><text x="615" y="165" text-anchor="middle" font-size="8" fill="var(--muted)">EventList</text><text x="615" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">仅 create，不合并</text>
  <line x1="320" y1="86" x2="120" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="345" y1="86" x2="280" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="375" y1="86" x2="430" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="400" y1="86" x2="595" y2="128" stroke="var(--faint)" stroke-width="1.4"/>
</svg>
<div class="figcap"><b>分流而非合流</b>：<code>mergeAndWrite</code> 按实体类型把任务交给四条专用处理线，各自写回第 8 课的对应表。observation 那条最复杂（要算 token/成本、补包装 trace）。源码：<code>worker/src/services/IngestionService/index.ts:149-195</code>。</div>
</div>

<p>每条处理线，合并的输入其实有<strong>两个来源</strong>，缺一不可：</p>

<div class="cols">
  <div class="col"><h4>📜 S3：本实体的全部事件</h4><p>worker 用 <code>listFiles</code> 把这个实体在 S3 里的<strong>所有事件</strong>都读回来（create、update……一个不漏），再按 <code>timestamp</code> 排好序。这是「修订流」。</p></div>
  <div class="col"><h4>🗄️ ClickHouse：当前这条记录</h4><p>同时去 observations 表 <code>getClickhouseRecord</code> 把<strong>已存在的那一行</strong>读出来当<strong>底稿</strong>。它排在合并数组的最前面，作为 immutable 字段的基线。</p></div>
</div>

<p>为什么两个来源都要？看似冗余，其实各有不可替代的作用。S3 那份是<strong>事件的真账本</strong>（第 14 课），重读全部事件能保证合并出的记录<strong>完整无遗漏</strong>，
即便这次任务是个迟到的补传；ClickHouse 那份则提供 <strong>immutable 字段的权威基线</strong>（created_at、start_time 这些「第一次写定就锁死」的值），
还兜住那些可能已经从 S3 滚动清理掉的早期事件。两者叠在一起，<strong>既不丢新、又不改旧</strong>——这就是「读旧底稿 + 叠新修订」的精髓。</p>
""")

# (merge fold section below)

_ZH15.append(r"""
<h2>mergeRecords：左折叠，后者覆盖</h2>
<p>核心算法只有几行：把「ClickHouse 底稿 + 按时间排序的事件记录」拼成一个数组，从左往右一个个 <code>overwriteObject</code> 叠上去，最后盖一个 <code>event_ts = now</code>。
关键全在 <code>overwriteObject</code> 的<strong>三条「不覆盖」规则</strong>里。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="合并左折叠：ClickHouse 底稿加按时间排序的事件依次 overwriteObject 叠加，得到最终记录并打上 event_ts=now">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">左折叠：底稿 → 叠事件 → 最终记录</text>
  <rect x="20" y="64" width="120" height="62" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="80" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">CH 底稿</text><text x="80" y="99" text-anchor="middle" font-size="7.5" fill="var(--muted)">已存在的行</text><text x="80" y="113" text-anchor="middle" font-size="7.5" fill="var(--faint)">（可能为空）</text>
  <rect x="170" y="64" width="120" height="62" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="230" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">事件① create</text><text x="230" y="99" text-anchor="middle" font-size="7.5" fill="var(--muted)">startTime·input</text><text x="230" y="113" text-anchor="middle" font-size="7.5" fill="var(--muted)">model</text>
  <rect x="320" y="64" width="120" height="62" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="380" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">事件② update</text><text x="380" y="99" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">endTime·output</text><text x="380" y="113" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">usage</text>
  <rect x="560" y="58" width="140" height="74" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="630" y="80" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">最终记录</text><text x="630" y="96" text-anchor="middle" font-size="7.5" fill="var(--ink)">各字段最新有值者</text><text x="630" y="112" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">event_ts = now</text>
  <line x1="140" y1="95" x2="168" y2="95" stroke="var(--faint)" stroke-width="1.6"/><polygon points="168,95 160,91 160,99" fill="var(--faint)"/>
  <line x1="290" y1="95" x2="318" y2="95" stroke="var(--faint)" stroke-width="1.6"/><polygon points="318,95 310,91 310,99" fill="var(--faint)"/>
  <line x1="440" y1="95" x2="558" y2="95" stroke="var(--faint)" stroke-width="1.6"/><polygon points="558,95 550,91 550,99" fill="var(--faint)"/>
  <text x="500" y="88" text-anchor="middle" font-size="7.5" fill="var(--faint)">overwriteObject ×N</text>
  <text x="360" y="158" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">overwriteObject 的三条「不覆盖」规则（后者的值被忽略，保留前者）：</text>
  <rect x="40" y="170" width="200" height="42" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="187" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① immutable 键</text><text x="140" y="201" text-anchor="middle" font-size="7.5" fill="var(--muted)">id·start_time·created_at…</text>
  <rect x="260" y="170" width="200" height="42" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="187" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② 值为 undefined</text><text x="360" y="201" text-anchor="middle" font-size="7.5" fill="var(--muted)">没带的字段不抹旧值</text>
  <rect x="480" y="170" width="200" height="42" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="580" y="187" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">③ 空对象 {}</text><text x="580" y="201" text-anchor="middle" font-size="7.5" fill="var(--muted)">空 usage/cost 不覆盖</text>
</svg>
<div class="figcap"><b>叠的是「有值的新字段」</b>：后到的事件覆盖先到的，但<strong>三种情况例外</strong>——immutable 键、值为 <code>undefined</code>、空对象。所以 update 只带 endTime/output/usage，create 的 startTime/input/model 安然无恙。源码：<code>IngestionService/index.ts:984-1005</code>、<code>utils.ts:56-81</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/services/IngestionService/index.ts &amp; utils.ts</span><span class="ln">合并核心</span></div>
  <pre class="code"><span class="cm">// 左折叠：底稿在前，事件按时间在后，逐个叠加</span>
<span class="kw">let</span> result = { id: records[0].id, project_id: records[0].project_id };
<span class="kw">for</span> (<span class="kw">const</span> record <span class="kw">of</span> records)
  result = <span class="fn">overwriteObject</span>(result, record, immutableEntityKeys);
result.event_ts = <span class="kw">new</span> Date().<span class="fn">getTime</span>();   <span class="cm">// 版本戳 → 交给第 8 课 ReplacingMergeTree</span>

<span class="cm">// overwriteObject：用 lodash mergeWith，命中任一条就保留旧值 objValue</span>
<span class="kw">if</span> (nonOverwritableKeys.<span class="fn">includes</span>(key)        <span class="cm">// ① immutable</span>
    || srcValue === <span class="kw">undefined</span>             <span class="cm">// ② 没带这个字段</span>
    || (isObject(srcValue) &amp;&amp; isEmpty(srcValue)))  <span class="cm">// ③ 空 usage/cost</span>
  <span class="kw">return</span> objValue;
<span class="kw">return</span> srcValue;                            <span class="cm">// 否则后者覆盖前者</span></pre>
</div>

<p>哪些字段被锁成 immutable？看 observations 这张表：<code>[id, project_id, trace_id, start_time, created_at, environment]</code>。
它们是记录的<strong>身份与锚点</strong>——一旦第一条事件写定，后续 update 再怎么改都动不了；其余 payload 字段（output、usage、end_time、level、metadata……）才走 last-write-wins。</p>

<p>合并过程中还藏着一个体贴的<strong>向后兼容</strong>细节：如果一个 observation 合并完发现<strong>没有 trace_id</strong>（很老的 SDK，&lt; 2.0 时代埋点不带 trace），
<code>IngestionService</code> 会顺手<strong>造一条「包装 trace」</strong>——用 observation 自己的 id 当 trace id，补写进 traces 表，再把它挂上去。这样无论数据多老，
每个 observation 都不会变成「孤儿」，第 5 课那棵 trace 树永远完整。一个小小的补偿逻辑，体现的是这套系统对<strong>历史数据与多版本 SDK</strong> 的尊重与照顾。</p>

<table class="t">
  <tr><th>字段类别</th><th>例子</th><th>合并规则</th></tr>
  <tr><td><b>身份 / 锚点（immutable）</b></td><td>id · project_id · trace_id · start_time · created_at · environment</td><td><strong>first-wins</strong>：第一次写定，永不被覆盖</td></tr>
  <tr><td><b>载荷（mutable）</b></td><td>end_time · output · usage · level · metadata · model…</td><td><strong>last-write-wins</strong>：后到事件覆盖，但 undefined / 空对象不抹旧值</td></tr>
</table>
""")

# (full flow + idempotency + spark + key below)

_ZH15.append(r"""
<h2>observation 那条线的完整一生</h2>
<p>把最复杂的 <code>processObservationEventList</code> 拆开看，从一堆事件到写回库，正好七步：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>幂等跳过</h4><p>先查 Redis：这个 fileKey 最近几分钟处理过吗？处理过就<strong>直接跳过</strong>（配合第 13 课「事件 id 当文件名」，重复投递不重复算）。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>按时间排序</h4><p><code>toTimeSortedEventList</code> 把事件按 <code>timestamp</code> 排好；同一时刻 create 排在 update 前。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>读 ClickHouse 底稿</h4><p><code>getClickhouseRecord</code> 取出该 observation 已存在的行（带类型与 start_time 过滤），当合并基线。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>事件 → 记录 → 合并</h4><p>把事件映射成记录，<code>mergeRecords</code> 左折叠出 <code>mergedObservationRecord</code>。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>补 input/output</h4><p>从最新往回找第一条非空的 input / output（事件里没有就退回 ClickHouse 的值），并归一化 tool 数据。</p></div></div>
  <div class="step"><div class="num">6</div><div class="sc"><h4>算 token 与成本</h4><p><code>getGenerationUsage</code> 做模型匹配、token 计数、成本计算（第 16 课详解），并进最终记录。</p></div></div>
  <div class="step"><div class="num">7</div><div class="sc"><h4>入写库队列</h4><p><code>clickHouseWriter.addToQueue(Observations, finalRecord)</code>——<strong>不直接写库</strong>，交给第 17 课的批写器攒批落盘。</p></div></div>
</div>

<p>第 7 步要特别留意：<code>IngestionService</code> 自己<strong>从不直接写 ClickHouse</strong>，它只把合并好的记录塞进 <code>ClickhouseWriter</code> 的队列。
为什么？因为<strong>逐条写 ClickHouse 是性能灾难</strong>（第 8 课说过它爱大批量）。把「合并」和「落盘」再切开，正是第 6 课「每层只干一件事」的又一次体现——合并归 IngestionService，攒批归 ClickhouseWriter。这种「先在内存里把记录算到位、再交给专门的批写器统一落盘」的两段式，让高频写入既保持正确，又不至于把列式存储压垮；第 17 课会看到批写器如何按表攒批、定时刷新。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>既然第 8 课的 ReplacingMergeTree 自己就会按 event_ts 去重，为什么写入侧还要再合并一遍？</strong> 因为两者解决的是<strong>不同时刻</strong>的问题。
  写入侧的预合并保证：<strong>每次写出的那一行，当下就是正确的完整状态</strong>——查询立刻就能读到对的数据，不必等后台合并。而 ReplacingMergeTree 的后台去重是<strong>最终</strong>发生的，
  用来收拾「同一条记录被并发处理、产生多行」这类竞态的尾巴。两层各管一段：<strong>写入侧求「即时正确」，存储侧求「最终唯一」</strong>。
  再加上 <code>event_ts=now</code> 这个版本戳把两层咬合起来——预合并产出的新行永远有更大的 event_ts，于是它一定能在存储层的去重里胜出。这是典型的<strong>纵深防御</strong>。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><code>mergeAndWrite</code> 是调度员：按实体类型 <code>switch</code> 到 <code>process{Trace,Observation,Score,DatasetRunItem}EventList</code>，骨架都是「读旧→转换→合并→写回」。</li>
    <li>合并有<strong>两个输入</strong>：S3 里本实体的<strong>全部事件</strong>（listFiles，按时间排序）+ ClickHouse 里<strong>当前那一行</strong>（当 immutable 基线）。</li>
    <li><code>mergeRecords</code> 把它们<strong>左折叠</strong>（<code>overwriteObject</code> 后者覆盖前者），并打 <code>event_ts=now</code> 版本戳。</li>
    <li><strong>三条不覆盖规则</strong>：immutable 键（id/start_time/created_at…first-wins）、<code>undefined</code>、空对象——所以 update 只带变化字段、不抹掉 create 的值。</li>
    <li>合并完只 <code>addToQueue</code>，<strong>不直接写库</strong>（落盘归第 17 课）。写入侧预合并求「即时正确」，存储侧 ReplacingMergeTree 求「最终唯一」，靠 event_ts 咬合——纵深防御。</li>
  </ul>
</div>
""")

_EN15.append(r"""
<p class="lead">
Lesson 14's worker took the job and read the events back from S3 by fileKey. This lesson is the <strong>heart</strong> of the whole write path: how
does that pile of events, plus the record's <strong>current state</strong> in the database, get kneaded into <strong>one final record</strong>? The answer
lives in <code>IngestionService</code> — <code>mergeAndWrite</code> dispatches by entity type, <code>mergeRecords</code> folds many inputs into one with a
single "left-fold + later-overwrites" move, then stamps a <code>event_ts=now</code> version. Get it, and Lesson 8's ReplacingMergeTree gains its
"other (write-side) half".
</p>

<div class="card analogy">
  <div class="tag">📝 Analogy</div>
  Think of merging as <strong>collaboratively editing a wiki article</strong>. The database's <strong>currently published version</strong> is the base;
  each event received this time is like a chronologically ordered <strong>revision</strong>, applied onto the base in turn. Later edits override earlier
  ones (same field, newer value wins); but <strong>a field a revision didn't touch stays as is</strong> (you only changed the "conclusion", the "body"
  isn't wiped). A few things are <strong>locked</strong>, untouchable by anyone: the article's <strong>creation time, its unique id</strong>. Stack all
  revisions and you get a <strong>merged draft</strong>, tagged with "this merge's moment" as the version — exactly what <code>IngestionService</code> does:
  the base from ClickHouse, the revisions from S3, the merged draft written back.
</div>
""")

_EN15.append(r"""
<h2>mergeAndWrite: split by entity type first</h2>
<p><code>mergeAndWrite</code> itself is just a <strong>dispatcher</strong>. It takes Lesson 13's computed entity type (trace / observation / score /
dataset_run_item) and a <code>switch</code> hands the work to the matching <code>process{Type}EventList</code>. Every line has the same skeleton —
<strong>read old, transform, merge, write back</strong> — only the field details differ by type.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="mergeAndWrite switches by entity type to processTrace/Observation/Score/DatasetRunItem EventList, four processing lines">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">mergeAndWrite: one switch, four lines</text>
  <rect x="280" y="40" width="160" height="46" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="60" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">mergeAndWrite</text><text x="360" y="76" text-anchor="middle" font-size="8" fill="var(--accent-ink)">switch (entityType)</text>
  <rect x="24" y="130" width="158" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="103" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">processTrace</text><text x="103" y="165" text-anchor="middle" font-size="8" fill="var(--muted)">EventList</text><text x="103" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">→ traces table</text>
  <rect x="194" y="130" width="158" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="273" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">processObservation</text><text x="273" y="165" text-anchor="middle" font-size="8" fill="var(--accent-ink)">EventList</text><text x="273" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">→ observations (richest)</text>
  <rect x="364" y="130" width="158" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="443" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">processScore</text><text x="443" y="165" text-anchor="middle" font-size="8" fill="var(--muted)">EventList</text><text x="443" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">→ scores table</text>
  <rect x="534" y="130" width="162" height="56" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="615" y="151" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">processDatasetRunItem</text><text x="615" y="165" text-anchor="middle" font-size="8" fill="var(--muted)">EventList</text><text x="615" y="178" text-anchor="middle" font-size="7.5" fill="var(--faint)">create only, no merge</text>
  <line x1="320" y1="86" x2="120" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="345" y1="86" x2="280" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="375" y1="86" x2="430" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="400" y1="86" x2="595" y2="128" stroke="var(--faint)" stroke-width="1.4"/>
</svg>
<div class="figcap"><b>Split, not converge</b>: <code>mergeAndWrite</code> hands the job by entity type to four dedicated lines, each writing back to Lesson 8's matching table. The observation line is the richest (token/cost, wrapper-trace backfill). Source: <code>worker/src/services/IngestionService/index.ts:149-195</code>.</div>
</div>

<p>On each line, the merge actually has <strong>two sources</strong>, both indispensable:</p>

<div class="cols">
  <div class="col"><h4>📜 S3: all events of this entity</h4><p>The worker uses <code>listFiles</code> to read back <strong>all events</strong> of this entity in S3 (create, update… none missed), then sorts them by <code>timestamp</code>. This is the "revision stream".</p></div>
  <div class="col"><h4>🗄️ ClickHouse: the current record</h4><p>Meanwhile it <code>getClickhouseRecord</code>s the <strong>existing row</strong> from observations as the <strong>base draft</strong>. It goes first in the merge array, the baseline for immutable fields.</p></div>
</div>

<p>Why need both? Seemingly redundant, but each is irreplaceable. The S3 one is the events' <strong>real ledger</strong> (Lesson 14); re-reading all
events guarantees the merged record is <strong>complete</strong>, even if this job is a late backfill. The ClickHouse one provides the <strong>authoritative
baseline for immutable fields</strong> (created_at, start_time — those "locked once first written" values) and backstops early events that may have aged out
of S3. Stacked together, they <strong>lose nothing new while changing nothing old</strong> — the essence of "read the old base + apply new revisions".</p>
""")

_EN15.append(r"""
<h2>mergeRecords: left-fold, later overwrites</h2>
<p>The core algorithm is just a few lines: assemble "ClickHouse base + time-sorted event records" into an array, fold them left-to-right with
<code>overwriteObject</code>, then stamp <code>event_ts = now</code>. The crux is entirely in <code>overwriteObject</code>'s <strong>three "don't
overwrite" rules</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="merge left-fold: ClickHouse base plus time-sorted events overwriteObject in turn, yielding the final record stamped event_ts=now">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Left-fold: base → stack events → final record</text>
  <rect x="20" y="64" width="120" height="62" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="80" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">CH base</text><text x="80" y="99" text-anchor="middle" font-size="7.5" fill="var(--muted)">existing row</text><text x="80" y="113" text-anchor="middle" font-size="7.5" fill="var(--faint)">(may be empty)</text>
  <rect x="170" y="64" width="120" height="62" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="230" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">event ① create</text><text x="230" y="99" text-anchor="middle" font-size="7.5" fill="var(--muted)">startTime·input</text><text x="230" y="113" text-anchor="middle" font-size="7.5" fill="var(--muted)">model</text>
  <rect x="320" y="64" width="120" height="62" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="380" y="84" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">event ② update</text><text x="380" y="99" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">endTime·output</text><text x="380" y="113" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">usage</text>
  <rect x="560" y="58" width="140" height="74" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="630" y="80" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">final record</text><text x="630" y="96" text-anchor="middle" font-size="7.5" fill="var(--ink)">each field: latest set value</text><text x="630" y="112" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">event_ts = now</text>
  <line x1="140" y1="95" x2="168" y2="95" stroke="var(--faint)" stroke-width="1.6"/><polygon points="168,95 160,91 160,99" fill="var(--faint)"/>
  <line x1="290" y1="95" x2="318" y2="95" stroke="var(--faint)" stroke-width="1.6"/><polygon points="318,95 310,91 310,99" fill="var(--faint)"/>
  <line x1="440" y1="95" x2="558" y2="95" stroke="var(--faint)" stroke-width="1.6"/><polygon points="558,95 550,91 550,99" fill="var(--faint)"/>
  <text x="500" y="88" text-anchor="middle" font-size="7.5" fill="var(--faint)">overwriteObject ×N</text>
  <text x="360" y="158" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">overwriteObject's three "don't overwrite" rules (later value ignored, earlier kept):</text>
  <rect x="40" y="170" width="200" height="42" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="187" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① immutable key</text><text x="140" y="201" text-anchor="middle" font-size="7.5" fill="var(--muted)">id·start_time·created_at…</text>
  <rect x="260" y="170" width="200" height="42" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="187" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② value is undefined</text><text x="360" y="201" text-anchor="middle" font-size="7.5" fill="var(--muted)">absent field won't wipe old</text>
  <rect x="480" y="170" width="200" height="42" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="580" y="187" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">③ empty object {}</text><text x="580" y="201" text-anchor="middle" font-size="7.5" fill="var(--muted)">empty usage/cost no-op</text>
</svg>
<div class="figcap"><b>It stacks "new fields that have a value"</b>: a later event overwrites an earlier one, with <strong>three exceptions</strong> — immutable keys, <code>undefined</code> values, empty objects. So update carrying only endTime/output/usage leaves create's startTime/input/model untouched. Source: <code>IngestionService/index.ts:984-1005</code>, <code>utils.ts:56-81</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/services/IngestionService/index.ts &amp; utils.ts</span><span class="ln">merge core</span></div>
  <pre class="code"><span class="cm">// Left-fold: base first, events (time-sorted) after, stacked one by one</span>
<span class="kw">let</span> result = { id: records[0].id, project_id: records[0].project_id };
<span class="kw">for</span> (<span class="kw">const</span> record <span class="kw">of</span> records)
  result = <span class="fn">overwriteObject</span>(result, record, immutableEntityKeys);
result.event_ts = <span class="kw">new</span> Date().<span class="fn">getTime</span>();   <span class="cm">// version stamp → Lesson 8's ReplacingMergeTree</span>

<span class="cm">// overwriteObject: lodash mergeWith; hit any rule → keep old objValue</span>
<span class="kw">if</span> (nonOverwritableKeys.<span class="fn">includes</span>(key)        <span class="cm">// ① immutable</span>
    || srcValue === <span class="kw">undefined</span>             <span class="cm">// ② field not provided</span>
    || (isObject(srcValue) &amp;&amp; isEmpty(srcValue)))  <span class="cm">// ③ empty usage/cost</span>
  <span class="kw">return</span> objValue;
<span class="kw">return</span> srcValue;                            <span class="cm">// else later overwrites earlier</span></pre>
</div>

<p>Which fields are locked immutable? For the observations table: <code>[id, project_id, trace_id, start_time, created_at, environment]</code>. These are
the record's <strong>identity and anchors</strong> — set once by the first event, untouchable by any later update; everything else (output, usage, end_time,
level, metadata…) follows last-write-wins.</p>

<table class="t">
  <tr><th>field class</th><th>examples</th><th>merge rule</th></tr>
  <tr><td><b>identity / anchor (immutable)</b></td><td>id · project_id · trace_id · start_time · created_at · environment</td><td><strong>first-wins</strong>: set once, never overwritten</td></tr>
  <tr><td><b>payload (mutable)</b></td><td>end_time · output · usage · level · metadata · model…</td><td><strong>last-write-wins</strong>: later event overwrites, but undefined / empty object won't wipe old</td></tr>
</table>

<p>The merge also hides a thoughtful <strong>backward-compat</strong> detail: if a merged observation turns out to have <strong>no trace_id</strong> (a very
old SDK from the pre-2.0 era that instrumented without a trace), <code>IngestionService</code> quietly <strong>creates a "wrapper trace"</strong> — using
the observation's own id as the trace id, writing it into the traces table and attaching the observation to it. So no matter how old the data, no
observation becomes an <strong>orphan</strong>, and Lesson 5's trace tree stays whole. A tiny compensating bit of logic that respects <strong>historical
data and multi-version SDKs</strong>.</p>
""")

_EN15.append(r"""
<h2>The full life of the observation line</h2>
<p>Unpack the most complex <code>processObservationEventList</code> and the path from a pile of events to a DB write is exactly seven steps:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>idempotency skip</h4><p>Check Redis first: was this fileKey processed in the last few minutes? If so, <strong>skip outright</strong> (with Lesson 13's "event id as filename", redelivery never double-counts).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>sort by time</h4><p><code>toTimeSortedEventList</code> orders events by <code>timestamp</code>; at the same instant, create comes before update.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>read ClickHouse base</h4><p><code>getClickhouseRecord</code> fetches the observation's existing row (filtered by type and start_time) as the merge baseline.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>events → records → merge</h4><p>Map events to records, <code>mergeRecords</code> left-folds into <code>mergedObservationRecord</code>.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>fill input/output</h4><p>Find the first non-null input/output scanning from newest back (fallback to ClickHouse's), and normalize tool data.</p></div></div>
  <div class="step"><div class="num">6</div><div class="sc"><h4>compute tokens &amp; cost</h4><p><code>getGenerationUsage</code> does model matching, token counting, cost calculation (detailed in Lesson 16), folded into the final record.</p></div></div>
  <div class="step"><div class="num">7</div><div class="sc"><h4>enqueue the write</h4><p><code>clickHouseWriter.addToQueue(Observations, finalRecord)</code> — <strong>not a direct DB write</strong>, handed to Lesson 17's batch writer.</p></div></div>
</div>

<p>Note step 7: <code>IngestionService</code> <strong>never writes ClickHouse directly</strong> — it only pushes the merged record into
<code>ClickhouseWriter</code>'s queue. Why? Because <strong>row-by-row ClickHouse writes are a performance disaster</strong> (Lesson 8 noted it loves big
batches). Splitting "merge" from "persist" is again Lesson 6's "each layer does one thing" — merging to IngestionService, batching to ClickhouseWriter.
This two-stage "compute the record fully in memory, then hand it to a dedicated batch writer" keeps high-frequency writes correct without crushing the
columnar store; Lesson 17 shows how the writer batches per table and flushes on a timer.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>If Lesson 8's ReplacingMergeTree already dedups by event_ts, why merge again on the write side?</strong> Because they solve problems at
  <strong>different moments</strong>. The write-side pre-merge guarantees: <strong>the very row written out is the correct, complete state right now</strong>
  — queries read correct data immediately, no waiting for background merges. ReplacingMergeTree's background dedup happens <strong>eventually</strong>,
  cleaning up the tail of races like "one record processed concurrently, producing multiple rows". Each layer owns a stretch: <strong>the write side seeks
  "immediate correctness", the storage side "eventual uniqueness"</strong>. And <code>event_ts=now</code> meshes the two — a pre-merged new row always has
  a larger event_ts, so it always wins the storage layer's dedup. Classic <strong>defense in depth</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><code>mergeAndWrite</code> is a dispatcher: <code>switch</code> by entity type to <code>process{Trace,Observation,Score,DatasetRunItem}EventList</code>, all sharing "read old → transform → merge → write back".</li>
    <li>Merge has <strong>two inputs</strong>: <strong>all events</strong> of this entity from S3 (listFiles, time-sorted) + the <strong>current row</strong> from ClickHouse (the immutable baseline).</li>
    <li><code>mergeRecords</code> <strong>left-folds</strong> them (<code>overwriteObject</code>, later overwrites earlier) and stamps the <code>event_ts=now</code> version.</li>
    <li><strong>Three don't-overwrite rules</strong>: immutable keys (id/start_time/created_at… first-wins), <code>undefined</code>, empty objects — so update carries only changed fields without wiping create's values.</li>
    <li>After merging it only <code>addToQueue</code>s, <strong>not a direct write</strong> (persist is Lesson 17). Write-side pre-merge for "immediate correctness", storage-side ReplacingMergeTree for "eventual uniqueness", meshed by event_ts — defense in depth.</li>
  </ul>
</div>
""")
LESSON_15 = {"zh": "\n".join(_ZH15), "en": "\n".join(_EN15)}


# ══════════════════════════════════════════════════════════════════════
# L16 · Token 计数与成本 / Token counting & cost
# ══════════════════════════════════════════════════════════════════════
_ZH16 = []
_EN16 = []

_ZH16.append(r"""
<p class="lead">
第 15 课合并到第 6 步时一句带过：「算 token 与成本」。这一课就把那一步摊开。核心是一条贯穿 Langfuse 的原则——<strong>provided 压倒 computed</strong>：
你（或 LLM 提供商）报上来的 usage / cost <strong>一律优先采信</strong>；只有你<strong>什么都没报</strong>时，Langfuse 才亲自动手：用<strong>分词器数 token</strong>、
按<strong>价目表算钱</strong>。这正是第 3 课 <code>provided_*</code> 与 <code>usage_details</code> 两套字段的来历，也是第 8 课那些 <code>provided_*</code> Map 列存在的理由。
</p>

<div class="card analogy">
  <div class="tag">📞 生活类比</div>
  把它想成<strong>话费账单</strong>。如果运营商已经把账单<strong>逐项列好</strong>（你这月打了多少分钟、各花多少钱），系统直接<strong>照单归档</strong>——这就是 provided。
  可如果你手里只有一堆<strong>通话记录</strong>、没有金额，系统就得自己来：先<strong>数通话时长</strong>（分词、数 token），再翻出这个套餐的<strong>资费表</strong>（模型价格）
  <strong>算出应付多少</strong>——这就是 computed。注意：只要运营商给了哪怕一项金额，系统就<strong>全盘采信它的账单</strong>，绝不把「自己估的」和「运营商给的」掺着用——
  两套数字混在一起，账就乱了。
</div>
""")

# (L16 sections appended below)

_ZH16.append(r"""
<h2>getGenerationUsage：四步流水线</h2>
<p>合并出 observation 后，<code>getGenerationUsage</code> 接手，把「模型 → token → 价格 → 成本」串成一条流水线。每一步的输入都可能来自你上报的 <code>provided_*</code>，
也可能由系统补算：</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="getGenerationUsage 四步：findModel 正则匹配模型、getUsageUnits 取或算 token、matchPricingTier 选价目、calculateUsageCosts 算成本">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">getGenerationUsage：模型 → token → 价格 → 成本</text>
  <rect x="16" y="62" width="160" height="64" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="96" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">① findModel</text><text x="96" y="100" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">provided_model_name</text><text x="96" y="113" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">~ match_pattern 正则</text>
  <rect x="192" y="62" width="160" height="64" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="272" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">② getUsageUnits</text><text x="272" y="100" text-anchor="middle" font-size="7.5" fill="var(--muted)">有 provided 就用</text><text x="272" y="113" text-anchor="middle" font-size="7.5" fill="var(--muted)">否则分词数 token</text>
  <rect x="368" y="62" width="160" height="64" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="448" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">③ matchPricingTier</text><text x="448" y="100" text-anchor="middle" font-size="7.5" fill="var(--muted)">按 usage 选价目层</text><text x="448" y="113" text-anchor="middle" font-size="7.5" fill="var(--muted)">每种用量一个单价</text>
  <rect x="544" y="62" width="162" height="64" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="625" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">④ calculateUsageCosts</text><text x="625" y="100" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">有 provided cost 就用</text><text x="625" y="113" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">否则 price×units</text>
  <line x1="176" y1="94" x2="190" y2="94" stroke="var(--faint)" stroke-width="1.6"/><polygon points="190,94 182,90 182,98" fill="var(--faint)"/>
  <line x1="352" y1="94" x2="366" y2="94" stroke="var(--faint)" stroke-width="1.6"/><polygon points="366,94 358,90 358,98" fill="var(--faint)"/>
  <line x1="528" y1="94" x2="542" y2="94" stroke="var(--faint)" stroke-width="1.6"/><polygon points="542,94 534,90 534,98" fill="var(--faint)"/>
  <rect x="160" y="160" width="400" height="40" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="1.5"/><text x="360" y="178" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">产物：usage_details · cost_details · total_cost</text><text x="360" y="192" text-anchor="middle" font-size="7.5" fill="var(--muted)">+ internal_model_id · 价目层 id/名</text>
  <line x1="360" y1="126" x2="360" y2="158" stroke="var(--faint)" stroke-width="1.4" stroke-dasharray="3 2"/><polygon points="360,158 356,150 364,150" fill="var(--faint)"/>
</svg>
<div class="figcap"><b>一条四步流水线</b>：<code>findModel</code> 用正则把模型名匹配到价目 → <code>getUsageUnits</code> 取/算 token → <code>matchPricingTier</code> 选价目层 → <code>calculateUsageCosts</code> 算钱。产物写进 observation 的 <code>usage_details</code>/<code>cost_details</code>。源码：<code>IngestionService/index.ts:1057-1143</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/services/IngestionService/index.ts</span><span class="ln">getGenerationUsage</span></div>
  <pre class="code"><span class="cm">// ① 模型匹配：拿 provided_model_name 去 models 表正则匹配</span>
<span class="kw">const</span> { model, pricingTiers } = provided_model_name
  ? <span class="kw">await</span> <span class="fn">findModel</span>({ projectId, model: provided_model_name })
  : { model: <span class="kw">null</span>, pricingTiers: [] };

<span class="cm">// ② 取/算 token；③ 选价目层；④ 算成本</span>
<span class="kw">const</span> usage = <span class="kw">await</span> <span class="fn">getUsageUnits</span>(observationRecord, model);
<span class="kw">const</span> tier  = <span class="fn">matchPricingTier</span>(pricingTiers, usage.usage_details);
<span class="kw">const</span> cost  = IngestionService.<span class="fn">calculateUsageCosts</span>(tier.prices, obs, usage.usage_details);

<span class="kw">return</span> { ...usage, ...cost, internal_model_id: model?.id, /* 价目层 */ };</pre>
</div>
""")

# (provided vs computed section below)

_ZH16.append(r"""
<h2>provided 压倒 computed：两条岔路</h2>
<p>token 和成本各有一条「provided 还是 computed」的岔路，规则一模一样：<strong>你给了，就用你的；你没给，系统才算</strong>。但「系统才算」是有<strong>前提</strong>的。</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="provided 与 computed 两条岔路：用户提供 usage/cost 则直接采用，否则在满足条件时分词计数并按价目计算">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">token / 成本：provided 优先，computed 兜底</text>
  <rect x="280" y="40" width="160" height="42" rx="10" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">你上报了吗？</text><text x="360" y="74" text-anchor="middle" font-size="7.5" fill="var(--muted)">provided_usage / provided_cost</text>
  <rect x="40" y="118" width="290" height="96" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="185" y="138" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">✅ 给了 → 直接采用（provided）</text><text x="185" y="158" text-anchor="middle" font-size="8" fill="var(--accent-ink)">usage：原样收下你的 token 数</text><text x="185" y="174" text-anchor="middle" font-size="8" fill="var(--accent-ink)">cost：只要给了任一项，全用你的</text><text x="185" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">绝不和系统估算掺用</text>
  <rect x="390" y="118" width="290" height="96" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="535" y="138" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">🤖 没给 → 系统补算（computed）</text><text x="535" y="156" text-anchor="middle" font-size="8" fill="var(--muted)">前提：匹配到模型 且 level≠ERROR</text><text x="535" y="172" text-anchor="middle" font-size="8" fill="var(--muted)">token：用 model.tokenizerId 分词计数</text><text x="535" y="188" text-anchor="middle" font-size="8" fill="var(--muted)">cost：Σ 价格[用量类型] × 数量</text>
  <line x1="320" y1="78" x2="200" y2="116" stroke="var(--accent)" stroke-width="1.6"/><polygon points="200,116 205,107 210,116" fill="var(--accent)"/><text x="238" y="104" text-anchor="middle" font-size="8" fill="var(--accent-ink)">是</text>
  <line x1="400" y1="78" x2="520" y2="116" stroke="var(--blue)" stroke-width="1.6"/><polygon points="520,116 510,116 515,107" fill="var(--blue)"/><text x="482" y="104" text-anchor="middle" font-size="8" fill="var(--ink)">否</text>
  <text x="360" y="232" text-anchor="middle" font-size="8.5" fill="var(--faint)">估算只是兜底，永远不会覆盖你上报的真实值——可信来源优先</text>
</svg>
<div class="figcap"><b>估算是兜底，不是覆盖</b>：provided 永远优先；computed 只在「匹配到模型 + 非 ERROR + 你没提供」三条同时满足时才发生。源码：<code>getUsageUnits</code>（index.ts:1145+，分词条件）与 <code>calculateUsageCosts</code>（「给了任一 cost 点就不再算」）。</div>
</div>

<table class="t">
  <tr><th>维度</th><th>provided（你上报）</th><th>computed（系统补算，仅当你没给）</th></tr>
  <tr><td><b>token 用量</b></td><td>原样采用 <code>provided_usage_details</code></td><td>匹配到模型 + level≠ERROR 时，用 <code>tokenizerId</code> 对 input/output 分词计数</td></tr>
  <tr><td><b>成本</b></td><td>给了任一 cost 点 → 全用 <code>provided_cost_details</code>，不再算别的</td><td>对每种用量：<code>价格 × 数量</code>，加总为 <code>total_cost</code></td></tr>
  <tr><td><b>为什么这样</b></td><td>来源更可信（LLM API 常返回精确 token 数）</td><td>无来源时的合理估计，不能与 provided 混用</td></tr>
</table>

<p>落到真实埋点里，这两条岔路对应两种很常见的接入方式：</p>

<div class="cols">
  <div class="col"><h4>🅰️ 官方 SDK：走 provided</h4><p>你用 OpenAI / Anthropic 官方 SDK，响应体里自带 <code>usage</code>（精确的 prompt/completion token 数）。SDK 把它原样上报，Langfuse <strong>照单全收</strong>——既准确又省去分词开销。这是最理想的情况。</p></div>
  <div class="col"><h4>🅱️ 裸 HTTP / 自建：走 computed</h4><p>你直接拼 HTTP 调一个模型、或用了不返回 usage 的网关，埋点里没有 token 数。只要模型名能匹配上、且不是 ERROR，Langfuse 就<strong>替你分词数 token、按价目算钱</strong>，让你照样有用量和成本可看。</p></div>
</div>

<p>举个具体的数：一次 <code>gpt-4o</code> 调用，computed 路径数出 input 1,000 token、output 500 token；价目表里这个模型 input 单价 $2.5/百万、output $10/百万，
于是 <code>cost_details = { input: 0.0025, output: 0.005, total: 0.0075 }</code>。如果你的 SDK 本就报了 <code>usage = {input:1000, output:500}</code>，
第②步就跳过分词、直接用这两个数；如果你连 <code>cost</code> 也报了，第④步连乘法都省了，整条成本直接采信你的。<strong>能少算就少算，能信你就信你</strong>。</p>

<p>第③步 <code>matchPricingTier</code> 是较新的精细化能力：一个模型可以有多个<strong>价目层</strong>，每层带一组<strong>条件</strong>——把 usage 里匹配某模式的用量<strong>求和</strong>、
和阈值比较（<code>&gt;</code>、<code>&gt;=</code>、<code>&lt;</code> 等，多条件 AND）。于是「超过 128k token 走长上下文高价」「缓存 token 走折扣价」这类<strong>按量分层定价</strong>就能精确表达。
选中的层提供每种用量类型的单价，第④步再据此算钱。没有命中任何层，就退回模型的基础价格——分层只是在「一价到底」之上多了一层灵活度。</p>
""")

# (model matching + spark + key below)

_ZH16.append(r"""
<h2>模型匹配：一条正则找到价目</h2>
<p>computed 这条路的起点，是把你上报的<strong>模型名字符串</strong>（如 <code>gpt-4o-2024-08-06</code>）对应到一条<strong>价目记录</strong>。这事由 <code>findModel</code> 在
Postgres 的 <code>models</code> 表上完成，靠的是一句正则匹配：</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">怎么匹配</span><span class="name">model ~ match_pattern</span></div><div class="ld">每条 model 记录带一个<strong>正则</strong> <code>match_pattern</code>；用 Postgres 的 <code>~</code> 运算符拿你的模型名去套。正则允许大小写不敏感、可选的提供商前缀等灵活写法。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">谁优先</span><span class="name">项目模型 &gt; 全局模型</span></div><div class="ld"><code>WHERE project_id = ? OR project_id IS NULL</code>，再 <code>ORDER BY project_id</code>——你<strong>自定义的模型价格盖过内置的</strong>，方便覆盖默认定价或加自有模型。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">取哪条</span><span class="name">start_date 最新</span></div><div class="ld"><code>ORDER BY start_date DESC</code> + <code>LIMIT 1</code>：价格会随时间调整，匹配时取<strong>生效日期最近</strong>的那一条，于是历史数据按当时价、新数据按新价。</div></div>
</div>

<p>匹配上的 model 记录里，除了价格，还有一个关键字段 <code>tokenizer_id</code>——它决定了 computed 时<strong>用哪种分词器</strong>数 token（不同模型家族分词规则不同）。
分词本身在 <code>worker/src/features/tokenisation</code> 里，甚至放进<strong>独立 worker 线程</strong>跑（<code>tokenCountAsync</code>），免得大文本分词阻塞主流程；失败再退回同步 <code>tokenCount</code>。
这又是第 8 课 <code>provided_*</code> 与计算列分离的写入侧来源：provided 进 <code>provided_usage_details</code>，算出来的进 <code>usage_details</code>，互不污染。</p>

<p>看一条真实的内置规则（Langfuse 自带约 150+ 个模型价格）：<code>gpt-4o</code> 的 <code>match_pattern</code> 是 <code>(?i)^(openai/)?(gpt-4o)$</code>——
大小写不敏感、可带可不带 <code>openai/</code> 前缀，精确匹配 <code>gpt-4o</code>。而带日期的版本（如 <code>gpt-4o-2024-05-13</code>）有<strong>各自独立的价格行</strong>，
因为不同发布日的定价可能不同。这套「正则 + 内置价目表」让 Langfuse 开箱即认得主流模型，你也能在 <code>models</code> 表里加自己的行覆盖或扩展——
正则给了灵活度，<code>project_id</code> 优先级给了覆盖权，<code>start_date</code> 给了时间维度。三者合起来，就是一套能跟着模型市场演进的<strong>活的定价系统</strong>。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么铁了心「provided 压倒 computed」，而不是两者求平均、或谁更大用谁？</strong> 因为这是一个关于<strong>数据可信度</strong>的立场。LLM 提供商在响应里返回的 token 数，
  是<strong>计费的权威依据</strong>——它知道自己怎么切的 token，比 Langfuse 在外面用通用分词器估的准得多。系统的本分是<strong>如实记录</strong>，而不是用自己的估算去「纠正」权威来源。
  于是规则被设计得毫不含糊：<strong>有 provided 就一字不改地用，连成本都「给了一项就全用你的」</strong>，绝不把估算掺进去——因为半真半估的账，比纯估算更危险（你会误以为它精确）。
  computed 只在<strong>信息真空</strong>（你啥也没给）时登场，当一个<strong>合理的兜底</strong>。可信优先、估算兜底、两者隔离——这条原则贯穿 usage 与 cost 的每一个角落。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><code>getGenerationUsage</code> 四步：<code>findModel</code>（匹配模型/价格）→ <code>getUsageUnits</code>（取/算 token）→ <code>matchPricingTier</code>（选价目层）→ <code>calculateUsageCosts</code>（算钱）。</li>
    <li><strong>provided 压倒 computed</strong>：你上报了 usage/cost 就原样用；<strong>成本只要给了任一项就全用你的</strong>，绝不与估算混用。</li>
    <li>computed 有前提：<strong>匹配到模型 + level≠ERROR + 你没提供</strong>，才用 <code>tokenizerId</code> 对 input/output 分词计数。</li>
    <li><code>findModel</code>：Postgres <code>~ match_pattern</code> 正则匹配；<strong>项目模型盖过全局</strong>，<code>start_date</code> 最新者胜——历史按旧价、新数据按新价。</li>
    <li>分词在 <code>worker/src/features/tokenisation</code>，可走独立线程（<code>tokenCountAsync</code>）；结果分别落第 8 课的 <code>provided_*</code> 与 <code>usage_details</code> 列，互不污染。</li>
  </ul>
</div>
""")

_EN16.append(r"""
<p class="lead">
At step 6 of Lesson 15's merge we said in passing: "compute tokens & cost". This lesson unfolds that step. The core is a principle running through all
of Langfuse — <strong>provided beats computed</strong>: the usage / cost you (or the LLM provider) report are <strong>always trusted first</strong>; only
when you report <strong>nothing</strong> does Langfuse roll up its sleeves: <strong>count tokens with a tokenizer</strong>, <strong>price it from a rate
card</strong>. This is the origin of Lesson 3's two field sets <code>provided_*</code> and <code>usage_details</code>, and the reason Lesson 8's
<code>provided_*</code> Map columns exist.
</p>

<div class="card analogy">
  <div class="tag">📞 Analogy</div>
  Think of a <strong>phone bill</strong>. If the carrier already <strong>itemized</strong> it (how many minutes you used, the charge for each), the system
  just <strong>files it as is</strong> — that's provided. But if all you have is a pile of <strong>call logs</strong> with no amounts, the system must do it
  itself: first <strong>count the call durations</strong> (tokenize, count tokens), then pull up this plan's <strong>rate card</strong> (model prices) and
  <strong>compute what's owed</strong> — that's computed. Note: the moment the carrier gives even one amount, the system <strong>trusts its bill
  wholesale</strong>, never mixing "its own estimate" with "the carrier's figure" — mixing the two scrambles the books.
</div>
""")

_EN16.append(r"""
<h2>getGenerationUsage: a four-step pipeline</h2>
<p>Once the observation is merged, <code>getGenerationUsage</code> takes over, threading "model → tokens → price → cost" into one pipeline. Each step's
input may come from your reported <code>provided_*</code>, or be backfilled by the system:</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="getGenerationUsage four steps: findModel regex-matches the model, getUsageUnits takes or counts tokens, matchPricingTier picks the tier, calculateUsageCosts computes cost">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">getGenerationUsage: model → tokens → price → cost</text>
  <rect x="16" y="62" width="160" height="64" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="96" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">① findModel</text><text x="96" y="100" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">provided_model_name</text><text x="96" y="113" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">~ match_pattern regex</text>
  <rect x="192" y="62" width="160" height="64" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="272" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">② getUsageUnits</text><text x="272" y="100" text-anchor="middle" font-size="7.5" fill="var(--muted)">use provided if any</text><text x="272" y="113" text-anchor="middle" font-size="7.5" fill="var(--muted)">else tokenize-count</text>
  <rect x="368" y="62" width="160" height="64" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="448" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">③ matchPricingTier</text><text x="448" y="100" text-anchor="middle" font-size="7.5" fill="var(--muted)">pick tier by usage</text><text x="448" y="113" text-anchor="middle" font-size="7.5" fill="var(--muted)">unit price per usage type</text>
  <rect x="544" y="62" width="162" height="64" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="625" y="84" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">④ calculateUsageCosts</text><text x="625" y="100" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">use provided cost if any</text><text x="625" y="113" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">else price×units</text>
  <line x1="176" y1="94" x2="190" y2="94" stroke="var(--faint)" stroke-width="1.6"/><polygon points="190,94 182,90 182,98" fill="var(--faint)"/>
  <line x1="352" y1="94" x2="366" y2="94" stroke="var(--faint)" stroke-width="1.6"/><polygon points="366,94 358,90 358,98" fill="var(--faint)"/>
  <line x1="528" y1="94" x2="542" y2="94" stroke="var(--faint)" stroke-width="1.6"/><polygon points="542,94 534,90 534,98" fill="var(--faint)"/>
  <rect x="160" y="160" width="400" height="40" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="1.5"/><text x="360" y="178" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">outputs: usage_details · cost_details · total_cost</text><text x="360" y="192" text-anchor="middle" font-size="7.5" fill="var(--muted)">+ internal_model_id · pricing tier id/name</text>
  <line x1="360" y1="126" x2="360" y2="158" stroke="var(--faint)" stroke-width="1.4" stroke-dasharray="3 2"/><polygon points="360,158 356,150 364,150" fill="var(--faint)"/>
</svg>
<div class="figcap"><b>A four-step pipeline</b>: <code>findModel</code> regex-matches the model name to a price → <code>getUsageUnits</code> takes/counts tokens → <code>matchPricingTier</code> picks the tier → <code>calculateUsageCosts</code> computes the cost. The outputs land in the observation's <code>usage_details</code>/<code>cost_details</code>. Source: <code>IngestionService/index.ts:1057-1143</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/services/IngestionService/index.ts</span><span class="ln">getGenerationUsage</span></div>
  <pre class="code"><span class="cm">// ① model match: regex-match provided_model_name against the models table</span>
<span class="kw">const</span> { model, pricingTiers } = provided_model_name
  ? <span class="kw">await</span> <span class="fn">findModel</span>({ projectId, model: provided_model_name })
  : { model: <span class="kw">null</span>, pricingTiers: [] };

<span class="cm">// ② take/count tokens; ③ pick tier; ④ compute cost</span>
<span class="kw">const</span> usage = <span class="kw">await</span> <span class="fn">getUsageUnits</span>(observationRecord, model);
<span class="kw">const</span> tier  = <span class="fn">matchPricingTier</span>(pricingTiers, usage.usage_details);
<span class="kw">const</span> cost  = IngestionService.<span class="fn">calculateUsageCosts</span>(tier.prices, obs, usage.usage_details);

<span class="kw">return</span> { ...usage, ...cost, internal_model_id: model?.id, /* tier */ };</pre>
</div>
""")

_EN16.append(r"""
<h2>provided beats computed: two forks</h2>
<p>Tokens and cost each have a "provided or computed" fork, with identical rules: <strong>if you gave it, use yours; only if you didn't does the system
compute</strong>. But "the system computes" has <strong>preconditions</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="provided and computed forks: if the user provided usage/cost use it directly, otherwise tokenize-count and price when conditions are met">
<text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">tokens / cost: provided first, computed as backup</text>
<rect x="280" y="40" width="160" height="42" rx="10" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">Did you report it?</text><text x="360" y="74" text-anchor="middle" font-size="7.5" fill="var(--muted)">provided_usage / provided_cost</text>
<rect x="40" y="118" width="290" height="96" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="185" y="138" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">✅ given → use directly (provided)</text><text x="185" y="158" text-anchor="middle" font-size="8" fill="var(--accent-ink)">usage: take your token counts as-is</text><text x="185" y="174" text-anchor="middle" font-size="8" fill="var(--accent-ink)">cost: any one point given → all yours</text><text x="185" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">never mixed with system estimate</text>
<rect x="390" y="118" width="290" height="96" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="535" y="138" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">🤖 not given → system computes</text><text x="535" y="156" text-anchor="middle" font-size="8" fill="var(--muted)">precond: model matched AND level≠ERROR</text><text x="535" y="172" text-anchor="middle" font-size="8" fill="var(--muted)">tokens: count via model.tokenizerId</text><text x="535" y="188" text-anchor="middle" font-size="8" fill="var(--muted)">cost: Σ price[usageType] × units</text>
<line x1="320" y1="78" x2="200" y2="116" stroke="var(--accent)" stroke-width="1.6"/><polygon points="200,116 205,107 210,116" fill="var(--accent)"/><text x="238" y="104" text-anchor="middle" font-size="8" fill="var(--accent-ink)">yes</text>
<line x1="400" y1="78" x2="520" y2="116" stroke="var(--blue)" stroke-width="1.6"/><polygon points="520,116 510,116 515,107" fill="var(--blue)"/><text x="482" y="104" text-anchor="middle" font-size="8" fill="var(--ink)">no</text>
<text x="360" y="232" text-anchor="middle" font-size="8.5" fill="var(--faint)">estimation is a backup, never overrides your reported real values — trusted source first</text>
</svg>
<div class="figcap"><b>Estimation backstops, never overrides</b>: provided always wins; computed happens only when all three hold — model matched + non-ERROR + you provided nothing. Source: <code>getUsageUnits</code> (index.ts:1145+, tokenization condition) and <code>calculateUsageCosts</code> ("any provided cost point disables computation").</div>
</div>

<table class="t">
<tr><th>dimension</th><th>provided (you reported)</th><th>computed (system, only if you didn't)</th></tr>
<tr><td><b>token usage</b></td><td>take <code>provided_usage_details</code> as-is</td><td>if model matched + level≠ERROR, tokenize-count input/output via <code>tokenizerId</code></td></tr>
<tr><td><b>cost</b></td><td>any cost point given → use <code>provided_cost_details</code> wholesale, compute nothing else</td><td>per usage type: <code>price × units</code>, summed to <code>total_cost</code></td></tr>
<tr><td><b>why</b></td><td>more trustworthy source (LLM APIs often return exact token counts)</td><td>a reasonable estimate absent a source; never mixed with provided</td></tr>
</table>

<p>In real instrumentation, the two forks map to two very common integration styles:</p>

<div class="cols">
<div class="col"><h4>🅰️ Official SDK: provided</h4><p>You use the official OpenAI / Anthropic SDK; the response body carries <code>usage</code> (exact prompt/completion token counts). The SDK reports it as-is and Langfuse <strong>takes it whole</strong> — accurate, and no tokenization cost. The ideal case.</p></div>
<div class="col"><h4>🅱️ Raw HTTP / homegrown: computed</h4><p>You hit a model over raw HTTP, or via a gateway that doesn't return usage, so there's no token count. As long as the model name matches and it isn't ERROR, Langfuse <strong>tokenizes and prices it for you</strong>, so you still get usage and cost.</p></div>
</div>

<p>A concrete number: a <code>gpt-4o</code> call, the computed path counts input 1,000 tokens, output 500; the rate card prices this model at $2.5/1M input,
$10/1M output, giving <code>cost_details = { input: 0.0025, output: 0.005, total: 0.0075 }</code>. If your SDK already reported
<code>usage = {input:1000, output:500}</code>, step ② skips tokenization and uses those directly; if you also reported <code>cost</code>, step ④ skips
even the multiplication and trusts your cost entirely. <strong>Compute as little as possible, trust you whenever possible.</strong></p>

<p>Step ③ <code>matchPricingTier</code> is a newer fine-grained capability: a model can have several <strong>pricing tiers</strong>, each with a set of
<strong>conditions</strong> — sum the usage matching some pattern and compare to a threshold (<code>&gt;</code>, <code>&gt;=</code>, <code>&lt;</code>…, multiple
conditions AND-ed). So "over 128k tokens → long-context higher price" or "cached tokens → discounted price" — <strong>usage-volume tiered pricing</strong> —
can be expressed precisely. The matched tier provides per-usage-type unit prices for step ④. Match no tier, and it falls back to the model's base price —
tiers just add flexibility on top of "one flat price".</p>
""")

_EN16.append(r"""
<h2>Model matching: one regex to the price</h2>
<p>The computed path begins by mapping your reported <strong>model-name string</strong> (e.g. <code>gpt-4o-2024-08-06</code>) to a <strong>price
record</strong>. <code>findModel</code> does this on Postgres's <code>models</code> table, via a single regex match:</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">how it matches</span><span class="name">model ~ match_pattern</span></div><div class="ld">Each model row carries a <strong>regex</strong> <code>match_pattern</code>; Postgres's <code>~</code> operator tests your model name against it. The regex allows case-insensitivity, an optional provider prefix, and other flexible forms.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">who wins</span><span class="name">project model &gt; global</span></div><div class="ld"><code>WHERE project_id = ? OR project_id IS NULL</code>, then <code>ORDER BY project_id</code> — your <strong>custom model prices override the built-in ones</strong>, handy for overriding default pricing or adding your own models.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">which one</span><span class="name">latest start_date</span></div><div class="ld"><code>ORDER BY start_date DESC</code> + <code>LIMIT 1</code>: prices change over time, so matching takes the one with the <strong>most recent effective date</strong> — historical data priced at its time, new data at the new price.</div></div>
</div>

<p>Beyond price, a matched model row has a key field <code>tokenizer_id</code> — it decides <strong>which tokenizer</strong> counts tokens when computing
(different model families tokenize differently). Tokenization itself lives in <code>worker/src/features/tokenisation</code>, even running in a
<strong>separate worker thread</strong> (<code>tokenCountAsync</code>) so large-text tokenization doesn't block the main flow; on failure it falls back to
synchronous <code>tokenCount</code>. This too is the write-side origin of Lesson 8's split between <code>provided_*</code> and computed columns: provided
goes into <code>provided_usage_details</code>, the computed into <code>usage_details</code>, never polluting each other.</p>

<p>Look at one real built-in rule (Langfuse ships ~150+ model prices): <code>gpt-4o</code>'s <code>match_pattern</code> is
<code>(?i)^(openai/)?(gpt-4o)$</code> — case-insensitive, with or without the <code>openai/</code> prefix, matching <code>gpt-4o</code> exactly. Dated
versions (like <code>gpt-4o-2024-05-13</code>) have their <strong>own separate price rows</strong>, since pricing can differ by release date. This "regex +
built-in rate card" lets Langfuse recognize mainstream models out of the box, and you can add your own rows in <code>models</code> to override or extend —
the regex gives flexibility, <code>project_id</code> precedence gives override rights, <code>start_date</code> gives a time dimension. Together they make a
<strong>living pricing system</strong> that evolves with the model market.</p>

<div class="card spark">
  <div class="tag">🎯 Design tradeoff</div>
  <strong>Why so adamant that "provided beats computed" — rather than averaging the two, or taking the larger?</strong> Because it's a stance on
  <strong>data trustworthiness</strong>. The token count an LLM provider returns in its response is the <strong>authoritative basis for billing</strong> — it
  knows how it tokenized, far more accurately than Langfuse estimating from outside with a generic tokenizer. The system's job is to <strong>record
  faithfully</strong>, not to "correct" an authoritative source with its own estimate. So the rule is unambiguous: <strong>if provided, use it verbatim;
  even for cost, "give one point and all of it is yours"</strong>, never mixing in estimates — because a half-real, half-estimated bill is more dangerous
  than a pure estimate (you'd mistake it for exact). Computed appears only in an <strong>information vacuum</strong> (you gave nothing), as a
  <strong>reasonable backstop</strong>. Trust first, estimate as backup, keep the two isolated — this principle pervades every corner of usage and cost.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><code>getGenerationUsage</code> in four steps: <code>findModel</code> (match model/price) → <code>getUsageUnits</code> (take/count tokens) → <code>matchPricingTier</code> (pick tier) → <code>calculateUsageCosts</code> (compute cost).</li>
    <li><strong>Provided beats computed</strong>: report usage/cost and it's used as-is; for <strong>cost, any one provided point means all yours</strong>, never mixed with estimates.</li>
    <li>Computed has preconditions: <strong>model matched + level≠ERROR + you provided nothing</strong>, then tokenize-count input/output via <code>tokenizerId</code>.</li>
    <li><code>findModel</code>: Postgres <code>~ match_pattern</code> regex; <strong>project models override global</strong>, latest <code>start_date</code> wins — history at old price, new data at new.</li>
    <li>Tokenization in <code>worker/src/features/tokenisation</code>, optionally on a separate thread (<code>tokenCountAsync</code>); results land in Lesson 8's <code>provided_*</code> vs <code>usage_details</code> columns, never polluting each other.</li>
  </ul>
</div>
""")
LESSON_16 = {"zh": "\n".join(_ZH16), "en": "\n".join(_EN16)}
