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
<div class="fig">
<svg viewBox="0 0 720 232" role="img" aria-label="摄取 API 真实例子：POST /api/public/ingestion 带 Basic 认证，body 是 batch 数组含 trace-create 与 observation-create；返回 207 Multi-Status，body 为 successes 与 errors。状态码与 batch 形状对齐 api/public/ingestion.ts，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：一次摄取请求与 207 响应</text>
  <rect x="20" y="32" width="340" height="190" rx="9" fill="var(--code-bg)" stroke="var(--code-line)"/>
  <text x="32" y="50" font-size="8" font-family="monospace" fill="var(--blue)">POST /api/public/ingestion</text>
  <text x="32" y="64" font-size="7.5" font-family="monospace" fill="var(--code-ink)" opacity="0.7">Authorization: Basic &lt;pk:sk&gt;</text>
  <text x="32" y="82" font-size="8" font-family="monospace" fill="var(--code-ink)">{ &quot;batch&quot;: [</text>
  <text x="32" y="96" font-size="7.5" font-family="monospace" fill="var(--code-ink)">  { &quot;type&quot;:&quot;trace-create&quot;,</text>
  <text x="32" y="108" font-size="7.5" font-family="monospace" fill="var(--code-ink)">    &quot;body&quot;:{&quot;id&quot;:&quot;chat_a1b2&quot;,&quot;name&quot;:&quot;qa&quot;} },</text>
  <text x="32" y="124" font-size="7.5" font-family="monospace" fill="var(--code-ink)">  { &quot;type&quot;:&quot;observation-create&quot;,</text>
  <text x="32" y="136" font-size="7.5" font-family="monospace" fill="var(--code-ink)">    &quot;body&quot;:{&quot;id&quot;:&quot;obs_7f&quot;,&quot;type&quot;:&quot;GENERATION&quot;,</text>
  <text x="32" y="148" font-size="7.5" font-family="monospace" fill="var(--code-ink)">      &quot;traceId&quot;:&quot;chat_a1b2&quot;} }</text>
  <text x="32" y="162" font-size="8" font-family="monospace" fill="var(--code-ink)">] }</text>
  <text x="32" y="210" font-size="7.5" fill="var(--blue)">↑ 请求（攒批一次发）</text>
  <line x1="362" y1="120" x2="396" y2="120" stroke="var(--accent)" stroke-width="1.6"/><polygon points="396,120 387,115 387,125" fill="var(--accent)"/>
  <rect x="398" y="32" width="302" height="190" rx="9" fill="var(--bg)" stroke="var(--accent)"/>
  <text x="412" y="50" font-size="9" font-weight="700" fill="var(--accent-ink)">207 Multi-Status</text>
  <text x="412" y="68" font-size="8" font-family="monospace" fill="var(--code-ink)">{ &quot;successes&quot;: [</text>
  <text x="412" y="82" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">    {&quot;id&quot;:&quot;chat_a1b2&quot;,&quot;status&quot;:201},</text>
  <text x="412" y="94" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">    {&quot;id&quot;:&quot;obs_7f&quot;,&quot;status&quot;:201}</text>
  <text x="412" y="108" font-size="8" font-family="monospace" fill="var(--code-ink)">  ],</text>
  <text x="412" y="122" font-size="8" font-family="monospace" fill="var(--code-ink)">  &quot;errors&quot;: []</text>
  <text x="412" y="136" font-size="8" font-family="monospace" fill="var(--code-ink)">}</text>
  <text x="412" y="166" font-size="7.5" fill="var(--muted)">每事件各自成败，整批一次 207</text>
  <text x="412" y="210" font-size="7.5" fill="var(--accent-ink)">↑ 响应（早返回，不等落库）</text>
</svg>
<div class="figcap"><b>一来一回</b>（状态码与 batch 形状对齐 <code>web/src/pages/api/public/ingestion.ts</code>；<b>值为示例</b>）：客户端把多个事件<b>攒成一个 batch</b> POST 上来，服务端校验入队后回 <code>207 Multi-Status</code>——<code>successes</code>/<code>errors</code> 逐事件给结果。207 而非 200，是因为「一批里可能有的成有的败」。</div>
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

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="批量 partial-success：一批N个事件逐个校验，合法的进队列处理、非法的被逐条拒绝(rejectedErrors)，最终返回 207 Multi-Status 带 {successes, errors}，于是一个混合批次里的好事件照样被处理、坏事件不连累好事件">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一批里好坏混杂？逐条处理，207 告诉你哪条成哪条败</text>
  <rect x="24" y="44" width="150" height="120" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">一批 N 个事件</text>
  <rect x="38" y="74" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--teal)"/><text x="99" y="86" text-anchor="middle" font-size="6.5" fill="var(--teal)">event ✓ 合法</text>
  <rect x="38" y="96" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--accent)"/><text x="99" y="108" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">event ✗ 结构错</text>
  <rect x="38" y="118" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--teal)"/><text x="99" y="130" text-anchor="middle" font-size="6.5" fill="var(--teal)">event ✓ 合法</text>
  <rect x="38" y="140" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--teal)"/><text x="99" y="152" text-anchor="middle" font-size="6.5" fill="var(--teal)">event ✓ 合法</text>
  <rect x="232" y="68" width="170" height="72" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="317" y="88" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">逐条校验</text><text x="317" y="104" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">合法 → 进队列处理</text><text x="317" y="118" text-anchor="middle" font-size="6.5" fill="var(--muted)">非法 → 逐条记 rejectedErrors</text><text x="317" y="132" text-anchor="middle" font-size="6.5" fill="var(--faint)">坏事件不连累好事件</text>
  <rect x="450" y="50" width="246" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="573" y="68" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">successes：已收下</text><text x="573" y="84" text-anchor="middle" font-size="6.5" fill="var(--muted)">进 Redis 队列、原件落 S3</text>
  <rect x="450" y="104" width="246" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="573" y="122" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">errors：被拒（带原因）</text><text x="573" y="138" text-anchor="middle" font-size="6.5" fill="var(--muted)">调用方可只重发这几条</text>
  <line x1="174" y1="104" x2="230" y2="104" stroke="var(--accent)" stroke-width="1.3"/><polygon points="230,104 221,100 221,108" fill="var(--accent)"/>
  <line x1="402" y1="92" x2="448" y2="72" stroke="var(--teal)" stroke-width="1.2"/><polygon points="448,72 439,72 442,80" fill="var(--teal)"/>
  <line x1="402" y1="116" x2="448" y2="126" stroke="var(--accent)" stroke-width="1.2"/><polygon points="448,126 439,122 440,130" fill="var(--accent)"/>
  <text x="360" y="184" text-anchor="middle" font-size="8" fill="var(--faint)">最终 HTTP 207 Multi-Status，返回 {successes, errors}——这就是「批量但可部分成功」的具体含义</text>
</svg>
<div class="figcap"><b>批量 = 可部分成功</b>：<code>ingestion.ts:153</code> <code>filterBatchForEventsOnly</code> 逐条筛、非法事件记 <code>rejectedErrors</code>；<code>:158 processEventBatch</code> 处理合法的；<code>:162</code> 最终 <code>res.status(207).json(result)</code> 返回 <code>{successes, errors}</code>。一个混合批次里，坏事件不连累好事件，调用方可只重发被拒的几条。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/public/ingestion.ts:132-162</span><span class="ln">批量解析 + 逐条筛 + 207</span></div>
  <pre class="code"><span class="cm">// 请求体就是「一个 batch 数组」，先整体 Zod 校验外壳</span>
<span class="kw">const</span> batchType = z.<span class="fn">object</span>({ batch: z.<span class="fn">array</span>(z.<span class="fn">unknown</span>()) });
<span class="kw">const</span> parsedSchema = batchType.<span class="fn">safeParse</span>(req.body);

<span class="cm">// 逐条筛：非法事件被单独拒，好事件继续——混合批次仍能处理</span>
<span class="kw">const</span> { batchForProcessing, rejectedErrors } = <span class="fn">filterBatchForEventsOnly</span>(parsedSchema.data.batch);
<span class="kw">const</span> result = <span class="kw">await</span> <span class="fn">processEventBatch</span>(batchForProcessing, authCheck);  <span class="cm">// 入队 + 落 S3</span>
<span class="kw">if</span> (rejectedErrors.length &gt; 0) result.errors = [...result.errors, ...rejectedErrors];

<span class="kw">return</span> res.<span class="fn">status</span>(<span class="st">207</span>).<span class="fn">json</span>(result);  <span class="cm">// 207 Multi-Status：{ successes, errors } 各是哪些</span></pre>
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
<div class="fig">
<svg viewBox="0 0 720 232" role="img" aria-label="Ingestion API real example: POST /api/public/ingestion with Basic auth, body is a batch array with trace-create and observation-create; returns 207 Multi-Status with successes and errors. Status and batch shape per api/public/ingestion.ts, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: one ingestion request and the 207 response</text>
  <rect x="20" y="32" width="340" height="190" rx="9" fill="var(--code-bg)" stroke="var(--code-line)"/>
  <text x="32" y="50" font-size="8" font-family="monospace" fill="var(--blue)">POST /api/public/ingestion</text>
  <text x="32" y="64" font-size="7.5" font-family="monospace" fill="var(--code-ink)" opacity="0.7">Authorization: Basic &lt;pk:sk&gt;</text>
  <text x="32" y="82" font-size="8" font-family="monospace" fill="var(--code-ink)">{ &quot;batch&quot;: [</text>
  <text x="32" y="96" font-size="7.5" font-family="monospace" fill="var(--code-ink)">  { &quot;type&quot;:&quot;trace-create&quot;,</text>
  <text x="32" y="108" font-size="7.5" font-family="monospace" fill="var(--code-ink)">    &quot;body&quot;:{&quot;id&quot;:&quot;chat_a1b2&quot;,&quot;name&quot;:&quot;qa&quot;} },</text>
  <text x="32" y="124" font-size="7.5" font-family="monospace" fill="var(--code-ink)">  { &quot;type&quot;:&quot;observation-create&quot;,</text>
  <text x="32" y="136" font-size="7.5" font-family="monospace" fill="var(--code-ink)">    &quot;body&quot;:{&quot;id&quot;:&quot;obs_7f&quot;,&quot;type&quot;:&quot;GENERATION&quot;,</text>
  <text x="32" y="148" font-size="7.5" font-family="monospace" fill="var(--code-ink)">      &quot;traceId&quot;:&quot;chat_a1b2&quot;} }</text>
  <text x="32" y="162" font-size="8" font-family="monospace" fill="var(--code-ink)">] }</text>
  <text x="32" y="210" font-size="7.5" fill="var(--blue)">↑ request (batched, sent once)</text>
  <line x1="362" y1="120" x2="396" y2="120" stroke="var(--accent)" stroke-width="1.6"/><polygon points="396,120 387,115 387,125" fill="var(--accent)"/>
  <rect x="398" y="32" width="302" height="190" rx="9" fill="var(--bg)" stroke="var(--accent)"/>
  <text x="412" y="50" font-size="9" font-weight="700" fill="var(--accent-ink)">207 Multi-Status</text>
  <text x="412" y="68" font-size="8" font-family="monospace" fill="var(--code-ink)">{ &quot;successes&quot;: [</text>
  <text x="412" y="82" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">    {&quot;id&quot;:&quot;chat_a1b2&quot;,&quot;status&quot;:201},</text>
  <text x="412" y="94" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">    {&quot;id&quot;:&quot;obs_7f&quot;,&quot;status&quot;:201}</text>
  <text x="412" y="108" font-size="8" font-family="monospace" fill="var(--code-ink)">  ],</text>
  <text x="412" y="122" font-size="8" font-family="monospace" fill="var(--code-ink)">  &quot;errors&quot;: []</text>
  <text x="412" y="136" font-size="8" font-family="monospace" fill="var(--code-ink)">}</text>
  <text x="412" y="166" font-size="7.5" fill="var(--muted)">per-event success/failure, one 207 for the batch</text>
  <text x="412" y="210" font-size="7.5" fill="var(--accent-ink)">↑ response (returns early, before persistence)</text>
</svg>
<div class="figcap"><b>One round trip</b> (status and batch shape per <code>web/src/pages/api/public/ingestion.ts</code>; <b>values illustrative</b>): the client <b>batches several events</b> into one POST; the server validates, enqueues and returns <code>207 Multi-Status</code> — <code>successes</code>/<code>errors</code> give a per-event result. It's 207, not 200, because a batch can be partly OK and partly failed.</div>
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

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="Batch partial success: a batch of N events is validated one by one, valid ones enter the queue, invalid ones are rejected per-event (rejectedErrors), finally returning 207 Multi-Status with {successes, errors}, so good events in a mixed batch still get processed and bad events don't drag down good ones">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Good and bad mixed in a batch? Per-event, 207 tells you which won/failed</text>
  <rect x="24" y="44" width="150" height="120" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">a batch of N events</text>
  <rect x="38" y="74" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--teal)"/><text x="99" y="86" text-anchor="middle" font-size="6.2" fill="var(--teal)">event ✓ valid</text>
  <rect x="38" y="96" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--accent)"/><text x="99" y="108" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">event ✗ malformed</text>
  <rect x="38" y="118" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--teal)"/><text x="99" y="130" text-anchor="middle" font-size="6.2" fill="var(--teal)">event ✓ valid</text>
  <rect x="38" y="140" width="122" height="18" rx="4" fill="var(--bg)" stroke="var(--teal)"/><text x="99" y="152" text-anchor="middle" font-size="6.2" fill="var(--teal)">event ✓ valid</text>
  <rect x="232" y="68" width="170" height="72" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="317" y="88" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">validate per event</text><text x="317" y="104" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">valid → enter the queue</text><text x="317" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">invalid → record rejectedErrors</text><text x="317" y="132" text-anchor="middle" font-size="6.0" fill="var(--faint)">bad don't drag down good</text>
  <rect x="450" y="50" width="246" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="573" y="68" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">successes: accepted</text><text x="573" y="84" text-anchor="middle" font-size="6.2" fill="var(--muted)">into Redis queue, originals to S3</text>
  <rect x="450" y="104" width="246" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="573" y="122" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">errors: rejected (with reasons)</text><text x="573" y="138" text-anchor="middle" font-size="6.2" fill="var(--muted)">caller can resend just these</text>
  <line x1="174" y1="104" x2="230" y2="104" stroke="var(--accent)" stroke-width="1.3"/><polygon points="230,104 221,100 221,108" fill="var(--accent)"/>
  <line x1="402" y1="92" x2="448" y2="72" stroke="var(--teal)" stroke-width="1.2"/><polygon points="448,72 439,72 442,80" fill="var(--teal)"/>
  <line x1="402" y1="116" x2="448" y2="126" stroke="var(--accent)" stroke-width="1.2"/><polygon points="448,126 439,122 440,130" fill="var(--accent)"/>
  <text x="360" y="184" text-anchor="middle" font-size="8" fill="var(--faint)">Finally HTTP 207 Multi-Status, returning {successes, errors} — the concrete meaning of "batched but partially successful"</text>
</svg>
<div class="figcap"><b>Batch = partial success</b>: <code>ingestion.ts:153</code> <code>filterBatchForEventsOnly</code> filters per-event, recording invalid ones as <code>rejectedErrors</code>; <code>:158 processEventBatch</code> handles the valid ones; <code>:162</code> finally <code>res.status(207).json(result)</code> returns <code>{successes, errors}</code>. In a mixed batch, bad events don't drag down good ones, and the caller can resend just the rejected few.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/public/ingestion.ts:132-162</span><span class="ln">batch parse + per-event filter + 207</span></div>
  <pre class="code"><span class="cm">// the request body is "a batch array"; first Zod-validate the outer shell</span>
<span class="kw">const</span> batchType = z.<span class="fn">object</span>({ batch: z.<span class="fn">array</span>(z.<span class="fn">unknown</span>()) });
<span class="kw">const</span> parsedSchema = batchType.<span class="fn">safeParse</span>(req.body);

<span class="cm">// filter per-event: invalid ones rejected individually, good ones continue — mixed batch still processes</span>
<span class="kw">const</span> { batchForProcessing, rejectedErrors } = <span class="fn">filterBatchForEventsOnly</span>(parsedSchema.data.batch);
<span class="kw">const</span> result = <span class="kw">await</span> <span class="fn">processEventBatch</span>(batchForProcessing, authCheck);  <span class="cm">// enqueue + land S3</span>
<span class="kw">if</span> (rejectedErrors.length &gt; 0) result.errors = [...result.errors, ...rejectedErrors];

<span class="kw">return</span> res.<span class="fn">status</span>(<span class="st">207</span>).<span class="fn">json</span>(result);  <span class="cm">// 207 Multi-Status: which are { successes, errors }</span></pre>
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
  <div class="tag">🎯 Design trade-off</div>
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
<div class="fig">
<svg viewBox="0 0 720 204" role="img" aria-label="事件合并真实例子：同一 id 的 observation-create 带 name/input，observation-update 带 output/usage/endTime，按 id 合并成最终一行 observation，后到的非空字段补齐。语义对齐 IngestionService 合并，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：create + update 合并成一行</text>
  <rect x="20" y="34" width="210" height="160" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="32" y="52" font-size="8.5" font-weight="700" fill="var(--blue)">① create（开始时）</text>
  <text x="32" y="72" font-size="7.5" font-family="monospace" fill="var(--code-ink)">id: obs_7f</text>
  <text x="32" y="88" font-size="7.5" font-family="monospace" fill="var(--code-ink)">type: GENERATION</text>
  <text x="32" y="104" font-size="7.5" font-family="monospace" fill="var(--code-ink)">name: answer</text>
  <text x="32" y="120" font-size="7.5" font-family="monospace" fill="var(--code-ink)">input: {messages}</text>
  <text x="32" y="136" font-size="7.5" font-family="monospace" fill="var(--faint)">output: —</text>
  <text x="32" y="152" font-size="7.5" font-family="monospace" fill="var(--faint)">usage: —</text>
  <text x="32" y="180" font-size="7" fill="var(--muted)">先发：知道什么算什么</text>
  <text x="250" y="120" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">+</text>
  <rect x="266" y="34" width="210" height="160" rx="8" fill="var(--bg)" stroke="var(--purple)"/><text x="278" y="52" font-size="8.5" font-weight="700" fill="var(--purple)">② update（结束时）</text>
  <text x="278" y="72" font-size="7.5" font-family="monospace" fill="var(--code-ink)">id: obs_7f  ← 同一个</text>
  <text x="278" y="88" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">output: &quot;Here is…&quot;</text>
  <text x="278" y="104" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">usageDetails: {512,88}</text>
  <text x="278" y="120" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">endTime: …+1.8s</text>
  <text x="278" y="180" font-size="7" fill="var(--muted)">后发：补上结束才知的</text>
  <text x="496" y="120" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">=</text>
  <rect x="512" y="34" width="188" height="160" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="524" y="52" font-size="8.5" font-weight="700" fill="var(--accent-ink)">③ 合并后的一行</text>
  <text x="524" y="72" font-size="7.5" font-family="monospace" fill="var(--ink)">id: obs_7f</text>
  <text x="524" y="88" font-size="7.5" font-family="monospace" fill="var(--ink)">name: answer</text>
  <text x="524" y="104" font-size="7.5" font-family="monospace" fill="var(--ink)">input: {messages}</text>
  <text x="524" y="120" font-size="7.5" font-family="monospace" fill="var(--ink)">output: &quot;Here is…&quot;</text>
  <text x="524" y="136" font-size="7.5" font-family="monospace" fill="var(--ink)">usageDetails: {512,88}</text>
  <text x="524" y="152" font-size="7.5" font-family="monospace" fill="var(--ink)">endTime: …+1.8s</text>
  <text x="524" y="180" font-size="7" font-weight="700" fill="var(--accent-ink)">非空字段补齐</text>
</svg>
<div class="figcap"><b>同 id 即合并</b>（语义对齐 <code>IngestionService</code> 合并；<b>值为示例</b>）：一次 LLM 调用<b>开始</b>时发一个 <code>observation-create</code>（知道 name/input），<b>结束</b>时发一个 <code>observation-update</code>（补上 output/usage/endTime）。两者 <code>id</code> 相同，<b>按 id 合并</b>成最终一行，后到的非空字段补齐——所以 SDK 不必在内存里攥着整条记录直到结束。</div>
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
<h2>18 种事件，5 类实体，3 张核心表</h2>
<p>事件 <code>type</code> 五花八门，但 worker 写库时只关心一件事：<strong>这条该进哪张表</strong>。一个叫 <code>getClickhouseEntityType</code> 的小函数把 18 种 type
坍缩成 <strong>5 个实体类型</strong>（<code>trace / observation / score / sdk_log / dataset_run_item</code>）；其中<strong>三个核心类型——trace / observation / score——
正好对应第 8 课的三张 ReplacingMergeTree 宽表</strong>，另两个（SDK 诊断日志 <code>sdk_log</code>、数据集运行项 <code>dataset_run_item</code>）走各自的处理：</p>

<table class="t">
  <tr><th>实体类型</th><th>由哪些事件 type 映射而来</th><th>落到哪张表</th></tr>
  <tr><td><b>trace</b></td><td><code>trace-create</code></td><td><code>traces</code>（第 8 课）</td></tr>
  <tr><td><b>observation</b></td><td><code>event/span/generation-create·update</code> + <code>agent/tool/chain/retriever/evaluator/embedding/guardrail-create</code> + 旧 <code>observation-*</code></td><td><code>observations</code>（第 8 课）</td></tr>
  <tr><td><b>score</b></td><td><code>score-create</code></td><td><code>scores</code>（第 8 课）</td></tr>
  <tr><td><b>sdk_log</b></td><td><code>sdk-log</code></td><td>SDK 诊断日志，单独处理</td></tr>
  <tr><td><b>dataset_run_item</b></td><td><code>dataset-run-item-create</code></td><td>数据集运行项，单独处理</td></tr>
</table>

<p>三个核心类型里，所有「像观测」的 type——无论它叫 span、generation 还是 agent——统统归到 <code>observation</code>，进同一张表，靠 observation 行里的 <code>type</code> 列区分。
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
    <li><code>getClickhouseEntityType</code> 把 18 种事件 type 坍缩成 <strong>5 个实体类型</strong>；其中三个核心的 <code>trace / observation / score</code> → 第 8 课的三张宽表（另两个 sdk_log、dataset_run_item 各自处理）。</li>
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
<div class="fig">
<svg viewBox="0 0 720 204" role="img" aria-label="Event merge real example: an observation-create with name/input and an observation-update with output/usage/endTime share an id and merge into one final observation row; later non-null fields fill in. Semantics per IngestionService merge, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: create + update merge into one row</text>
  <rect x="20" y="34" width="210" height="160" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="32" y="52" font-size="8.5" font-weight="700" fill="var(--blue)">① create (at start)</text>
  <text x="32" y="72" font-size="7.5" font-family="monospace" fill="var(--code-ink)">id: obs_7f</text>
  <text x="32" y="88" font-size="7.5" font-family="monospace" fill="var(--code-ink)">type: GENERATION</text>
  <text x="32" y="104" font-size="7.5" font-family="monospace" fill="var(--code-ink)">name: answer</text>
  <text x="32" y="120" font-size="7.5" font-family="monospace" fill="var(--code-ink)">input: {messages}</text>
  <text x="32" y="136" font-size="7.5" font-family="monospace" fill="var(--faint)">output: —</text>
  <text x="32" y="152" font-size="7.5" font-family="monospace" fill="var(--faint)">usage: —</text>
  <text x="32" y="180" font-size="7" fill="var(--muted)">sent first: what is known so far</text>
  <text x="250" y="120" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">+</text>
  <rect x="266" y="34" width="210" height="160" rx="8" fill="var(--bg)" stroke="var(--purple)"/><text x="278" y="52" font-size="8.5" font-weight="700" fill="var(--purple)">② update (at end)</text>
  <text x="278" y="72" font-size="7.5" font-family="monospace" fill="var(--code-ink)">id: obs_7f  ← same one</text>
  <text x="278" y="88" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">output: &quot;Here is…&quot;</text>
  <text x="278" y="104" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">usageDetails: {512,88}</text>
  <text x="278" y="120" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">endTime: …+1.8s</text>
  <text x="278" y="180" font-size="7" fill="var(--muted)">sent later: fills end-time facts</text>
  <text x="496" y="120" text-anchor="middle" font-size="14" font-weight="700" fill="var(--accent)">=</text>
  <rect x="512" y="34" width="188" height="160" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="524" y="52" font-size="8.5" font-weight="700" fill="var(--accent-ink)">③ merged row</text>
  <text x="524" y="72" font-size="7.5" font-family="monospace" fill="var(--ink)">id: obs_7f</text>
  <text x="524" y="88" font-size="7.5" font-family="monospace" fill="var(--ink)">name: answer</text>
  <text x="524" y="104" font-size="7.5" font-family="monospace" fill="var(--ink)">input: {messages}</text>
  <text x="524" y="120" font-size="7.5" font-family="monospace" fill="var(--ink)">output: &quot;Here is…&quot;</text>
  <text x="524" y="136" font-size="7.5" font-family="monospace" fill="var(--ink)">usageDetails: {512,88}</text>
  <text x="524" y="152" font-size="7.5" font-family="monospace" fill="var(--ink)">endTime: …+1.8s</text>
  <text x="524" y="180" font-size="7" font-weight="700" fill="var(--accent-ink)">non-null fields filled in</text>
</svg>
<div class="figcap"><b>Same id merges</b> (semantics per <code>IngestionService</code> merge; <b>values illustrative</b>): an LLM call sends an <code>observation-create</code> at the <b>start</b> (name/input known) and an <code>observation-update</code> at the <b>end</b> (output/usage/endTime). They share an <code>id</code>, so they <b>merge by id</b> into one final row with later non-null fields filled in — the SDK needn't hold the whole record in memory until the end.</div>
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
<h2>18 event types, 5 entities, 3 core tables</h2>
<p>Event <code>type</code> comes in many flavors, but when the worker writes, it cares about one thing: <strong>which table does this go to</strong>. A
small function <code>getClickhouseEntityType</code> collapses the 18 types into <strong>5 entity types</strong>
(<code>trace / observation / score / sdk_log / dataset_run_item</code>); of these, the <strong>three core ones — trace / observation / score — map
exactly onto Lesson 8's three ReplacingMergeTree wide tables</strong>, while the other two (SDK diagnostic <code>sdk_log</code>, dataset-run linkage
<code>dataset_run_item</code>) take their own handling:</p>

<table class="t">
  <tr><th>entity type</th><th>mapped from which event types</th><th>which table</th></tr>
  <tr><td><b>trace</b></td><td><code>trace-create</code></td><td><code>traces</code> (Lesson 8)</td></tr>
  <tr><td><b>observation</b></td><td><code>event/span/generation-create·update</code> + <code>agent/tool/chain/retriever/evaluator/embedding/guardrail-create</code> + legacy <code>observation-*</code></td><td><code>observations</code> (Lesson 8)</td></tr>
  <tr><td><b>score</b></td><td><code>score-create</code></td><td><code>scores</code> (Lesson 8)</td></tr>
  <tr><td><b>sdk_log</b></td><td><code>sdk-log</code></td><td>SDK diagnostics, handled separately</td></tr>
  <tr><td><b>dataset_run_item</b></td><td><code>dataset-run-item-create</code></td><td>dataset run linkage, handled separately</td></tr>
</table>

<p>Within the three core types, everything "observation-like" — be it span, generation or agent — lands in <code>observation</code>, the same table, distinguished by the
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
  <div class="tag">🎯 Design trade-off</div>
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
    <li><code>getClickhouseEntityType</code> collapses the 18 event types into <strong>5 entity types</strong>; the three core ones <code>trace / observation / score</code> → Lesson 8's three wide tables (the other two, sdk_log &amp; dataset_run_item, handled separately).</li>
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
<div class="fig">
<svg viewBox="0 0 720 206" role="img" aria-label="摄取队列可视化：web 把事件塞进 Redis 队列，worker 取出消费；队列深度条显示积压，水位线提示告警阈值；高吞吐项目走 secondary 队列与 primary 隔离。队列契约见 server/queues.ts，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：摄取队列的水位与消费滞后</text>
  <text x="40" y="52" font-size="8.5" font-weight="700" fill="var(--blue)">web 入队（快）</text>
  <line x1="150" y1="48" x2="196" y2="48" stroke="var(--blue)" stroke-width="1.6"/><polygon points="196,48 187,43 187,53" fill="var(--blue)"/>
  <rect x="200" y="38" width="320" height="22" rx="5" fill="var(--panel-2)" stroke="var(--line)"/>
  <rect x="200" y="38" width="220" height="22" rx="5" fill="var(--red)" opacity="0.45"/>
  <text x="270" y="53" font-size="7.5" font-weight="700" fill="var(--red)">pending events ≈ 18k</text>
  <line x1="470" y1="32" x2="470" y2="66" stroke="var(--amber)" stroke-width="1.4" stroke-dasharray="3 2"/><text x="474" y="32" font-size="7" fill="var(--amber)">水位线/watermark</text>
  <line x1="524" y1="48" x2="566" y2="48" stroke="var(--purple)" stroke-width="1.6"/><polygon points="566,48 557,43 557,53" fill="var(--purple)"/>
  <text x="576" y="52" font-size="8.5" font-weight="700" fill="var(--purple)">worker 消费</text>
  <rect x="120" y="92" width="240" height="100" rx="9" fill="var(--bg)" stroke="var(--red)"/><text x="240" y="110" text-anchor="middle" font-size="9" font-weight="700" fill="var(--red)">primary 队列</text>
  <text x="240" y="128" text-anchor="middle" font-size="7.5" fill="var(--muted)">大多数项目共用</text>
  <path d="M150 168 a52 52 0 0 1 104 0" fill="none" stroke="var(--line)" stroke-width="7"/><path d="M150 168 a52 52 0 0 1 78 -36" fill="none" stroke="var(--amber)" stroke-width="7"/><text x="202" y="166" text-anchor="middle" font-size="8" font-weight="700" fill="var(--amber)">lag 偏高</text><text x="202" y="180" text-anchor="middle" font-size="6.5" fill="var(--muted)">消费滞后(s)</text>
  <rect x="380" y="92" width="240" height="100" rx="9" fill="var(--bg)" stroke="var(--purple)" stroke-dasharray="4 3"/><text x="500" y="110" text-anchor="middle" font-size="9" font-weight="700" fill="var(--purple)">secondary 队列</text>
  <text x="500" y="128" text-anchor="middle" font-size="7.5" fill="var(--muted)">高吞吐项目隔离到此</text>
  <text x="500" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">大客户的洪峰不拖垮别人</text>
  <text x="500" y="170" text-anchor="middle" font-size="7" fill="var(--faint)">primary/secondary 物理隔离</text>
</svg>
<div class="figcap"><b>队列削峰，水位预警</b>（队列契约见 <code>packages/shared/src/server/queues.ts</code>；<b>值为示例</b>）：web 把事件飞快塞进 Redis 就返回，worker 在另一头慢慢取。<b>队列深度</b>就是积压，<b>水位线</b>越过就该加 worker；<b>消费滞后</b>是「现在查得到多旧的数据」。高吞吐项目走 <code>secondary</code> 队列，和 <code>primary</code> 物理隔离，互不拖累。</div>
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

<svg viewBox="0 0 720 250" role="img" aria-label="worker 处理每个任务前判断该 project 是否改道：命中 env 白名单或 S3 SlowDown 标志的高吞吐项目 C 被路由到独立分片、独立 worker 的次队列，普通项目 A、B 留在主队列正常处理，吵闹租户被物理隔离不堵塞他人">
  <rect x="0" y="0" width="720" height="250" fill="var(--bg)"></rect>
  <rect x="18" y="58" width="80" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="58" y="78" font-size="12" text-anchor="middle" fill="var(--ink)">项目 A</text>
  <rect x="18" y="104" width="80" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="58" y="124" font-size="12" text-anchor="middle" fill="var(--ink)">项目 B</text>
  <rect x="18" y="158" width="80" height="34" rx="6" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="58" y="174" font-size="12" text-anchor="middle" fill="var(--ink)">项目 C</text>
  <text x="58" y="188" font-size="10" text-anchor="middle" fill="var(--muted)">高吞吐</text>
  <rect x="138" y="66" width="128" height="120" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="202" y="92" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">改道判断</text>
  <text x="202" y="116" font-size="10.5" text-anchor="middle" fill="var(--muted)">① env 白名单（静态）</text>
  <text x="202" y="134" font-size="10.5" text-anchor="middle" fill="var(--muted)">② S3 SlowDown（动态）</text>
  <text x="202" y="160" font-size="10" text-anchor="middle" fill="var(--muted)">命中 → 次队列</text>
  <text x="202" y="174" font-size="10" text-anchor="middle" fill="var(--muted)">否则 → 主队列</text>
  <line x1="98" y1="73" x2="138" y2="100" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="98" y1="119" x2="138" y2="124" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="98" y1="175" x2="138" y2="150" stroke="var(--faint)" stroke-width="1.5"></line>
  <rect x="320" y="58" width="160" height="48" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="400" y="80" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">主队列</text>
  <text x="400" y="97" font-size="10" text-anchor="middle" fill="var(--muted)">常规分片 · 给 A、B</text>
  <rect x="540" y="58" width="150" height="48" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="615" y="86" font-size="12" text-anchor="middle" fill="var(--ink)">主 worker</text>
  <rect x="320" y="150" width="160" height="52" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="400" y="172" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">次队列</text>
  <text x="400" y="190" font-size="10" text-anchor="middle" fill="var(--muted)">独立分片 · 给 C</text>
  <rect x="540" y="150" width="150" height="52" rx="8" fill="var(--bg)" stroke="var(--accent)"></rect>
  <text x="615" y="180" font-size="12" text-anchor="middle" fill="var(--ink)">次 worker</text>
  <line x1="266" y1="100" x2="320" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="266" y1="150" x2="320" y2="176" stroke="var(--accent)" stroke-width="2" stroke-dasharray="4 3"></line>
  <line x1="480" y1="82" x2="540" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="480" y1="176" x2="540" y2="176" stroke="var(--accent)" stroke-width="2"></line>
  <text x="360" y="234" font-size="11" text-anchor="middle" fill="var(--muted)">物理隔离：C 改道后，主队列立刻腾手处理 A、B——吵闹租户堵不住别人</text>
</svg>

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
<div class="fig">
<svg viewBox="0 0 720 206" role="img" aria-label="Ingestion queue visualization: web pushes events into the Redis queue, workers consume; a depth bar shows backlog, a watermark marks the alert threshold; high-throughput projects use a secondary queue isolated from primary. Queue contract in server/queues.ts, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: ingestion queue depth and consumer lag</text>
  <text x="40" y="52" font-size="8.5" font-weight="700" fill="var(--blue)">web enqueue (fast)</text>
  <line x1="150" y1="48" x2="196" y2="48" stroke="var(--blue)" stroke-width="1.6"/><polygon points="196,48 187,43 187,53" fill="var(--blue)"/>
  <rect x="200" y="38" width="320" height="22" rx="5" fill="var(--panel-2)" stroke="var(--line)"/>
  <rect x="200" y="38" width="220" height="22" rx="5" fill="var(--red)" opacity="0.45"/>
  <text x="270" y="53" font-size="7.5" font-weight="700" fill="var(--red)">pending events ≈ 18k</text>
  <line x1="470" y1="32" x2="470" y2="66" stroke="var(--amber)" stroke-width="1.4" stroke-dasharray="3 2"/><text x="474" y="32" font-size="7" fill="var(--amber)">watermark</text>
  <line x1="524" y1="48" x2="566" y2="48" stroke="var(--purple)" stroke-width="1.6"/><polygon points="566,48 557,43 557,53" fill="var(--purple)"/>
  <text x="576" y="52" font-size="8.5" font-weight="700" fill="var(--purple)">worker consume</text>
  <rect x="120" y="92" width="240" height="100" rx="9" fill="var(--bg)" stroke="var(--red)"/><text x="240" y="110" text-anchor="middle" font-size="9" font-weight="700" fill="var(--red)">primary queue</text>
  <text x="240" y="128" text-anchor="middle" font-size="7.5" fill="var(--muted)">shared by most projects</text>
  <path d="M150 168 a52 52 0 0 1 104 0" fill="none" stroke="var(--line)" stroke-width="7"/><path d="M150 168 a52 52 0 0 1 78 -36" fill="none" stroke="var(--amber)" stroke-width="7"/><text x="202" y="166" text-anchor="middle" font-size="8" font-weight="700" fill="var(--amber)">lag high</text><text x="202" y="180" text-anchor="middle" font-size="6.5" fill="var(--muted)">consumer lag (s)</text>
  <rect x="380" y="92" width="240" height="100" rx="9" fill="var(--bg)" stroke="var(--purple)" stroke-dasharray="4 3"/><text x="500" y="110" text-anchor="middle" font-size="9" font-weight="700" fill="var(--purple)">secondary queue</text>
  <text x="500" y="128" text-anchor="middle" font-size="7.5" fill="var(--muted)">high-throughput projects isolated here</text>
  <text x="500" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">a big tenant's spike won't drag others down</text>
  <text x="500" y="170" text-anchor="middle" font-size="7" fill="var(--faint)">primary/secondary physical isolation</text>
</svg>
<div class="figcap"><b>The queue absorbs spikes, the watermark warns</b> (queue contract in <code>packages/shared/src/server/queues.ts</code>; <b>values illustrative</b>): web pushes events into Redis and returns fast; workers drain the other end. <b>Queue depth</b> is the backlog; crossing the <b>watermark</b> means add workers; <b>consumer lag</b> is “how stale the queryable data is”. High-throughput projects use a <code>secondary</code> queue physically isolated from <code>primary</code>, so one tenant's flood can't starve others.</div>
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

<svg viewBox="0 0 720 250" role="img" aria-label="before processing each job the worker decides whether to redirect the project: a high-throughput project C matching the env allowlist or the S3 SlowDown flag is routed to the secondary queue with its own shards and own worker, while normal projects A and B stay on the primary queue, physically isolating the noisy tenant so it cannot block others">
  <rect x="0" y="0" width="720" height="250" fill="var(--bg)"></rect>
  <rect x="18" y="58" width="80" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="58" y="78" font-size="12" text-anchor="middle" fill="var(--ink)">project A</text>
  <rect x="18" y="104" width="80" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="58" y="124" font-size="12" text-anchor="middle" fill="var(--ink)">project B</text>
  <rect x="18" y="158" width="80" height="34" rx="6" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="58" y="174" font-size="12" text-anchor="middle" fill="var(--ink)">project C</text>
  <text x="58" y="188" font-size="8" text-anchor="middle" fill="var(--muted)">high-throughput</text>
  <rect x="138" y="66" width="128" height="120" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="202" y="92" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">redirect check</text>
  <text x="202" y="116" font-size="9" text-anchor="middle" fill="var(--muted)">(1) env allowlist (static)</text>
  <text x="202" y="134" font-size="9" text-anchor="middle" fill="var(--muted)">(2) S3 SlowDown (dynamic)</text>
  <text x="202" y="160" font-size="10" text-anchor="middle" fill="var(--muted)">match → secondary</text>
  <text x="202" y="174" font-size="10" text-anchor="middle" fill="var(--muted)">else → primary</text>
  <line x1="98" y1="73" x2="138" y2="100" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="98" y1="119" x2="138" y2="124" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="98" y1="175" x2="138" y2="150" stroke="var(--faint)" stroke-width="1.5"></line>
  <rect x="320" y="58" width="160" height="48" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="400" y="80" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">primary queue</text>
  <text x="400" y="97" font-size="10" text-anchor="middle" fill="var(--muted)">normal shards · for A, B</text>
  <rect x="540" y="58" width="150" height="48" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="615" y="86" font-size="12" text-anchor="middle" fill="var(--ink)">primary worker</text>
  <rect x="320" y="150" width="160" height="52" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="400" y="172" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">secondary queue</text>
  <text x="400" y="190" font-size="10" text-anchor="middle" fill="var(--muted)">own shards · for C</text>
  <rect x="540" y="150" width="150" height="52" rx="8" fill="var(--bg)" stroke="var(--accent)"></rect>
  <text x="615" y="180" font-size="12" text-anchor="middle" fill="var(--ink)">secondary worker</text>
  <line x1="266" y1="100" x2="320" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="266" y1="150" x2="320" y2="176" stroke="var(--accent)" stroke-width="2" stroke-dasharray="4 3"></line>
  <line x1="480" y1="82" x2="540" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="480" y1="176" x2="540" y2="176" stroke="var(--accent)" stroke-width="2"></line>
  <text x="360" y="234" font-size="11" text-anchor="middle" fill="var(--muted)">physical isolation: once C is redirected, the primary instantly serves A, B — a noisy tenant can't block others</text>
</svg>

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
  <div class="tag">🎯 Design trade-off</div>
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
<div class="fig">
<svg viewBox="0 0 720 198" role="img" aria-label="合并的数据视角：当前存储的 observation 行 + 一个 update 补丁（高亮变更字段）= 结果行；ReplacingMergeTree 按 event_ts 保留最新。语义对齐 IngestionService，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：合并 = 旧行 + 补丁 → 新行</text>
  <rect x="20" y="36" width="216" height="150" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="32" y="54" font-size="8.5" font-weight="700" fill="var(--muted)">当前存储行</text>
  <text x="32" y="74" font-size="7.5" font-family="monospace" fill="var(--ink)">id: obs_7f</text>
  <text x="32" y="90" font-size="7.5" font-family="monospace" fill="var(--ink)">output: null</text>
  <text x="32" y="106" font-size="7.5" font-family="monospace" fill="var(--ink)">total_cost: null</text>
  <text x="32" y="122" font-size="7.5" font-family="monospace" fill="var(--ink)">event_ts: 12:00:00.1</text>
  <line x1="244" y1="110" x2="276" y2="110" stroke="var(--accent)" stroke-width="1.4"/><polygon points="276,110 267,105 267,115" fill="var(--accent)"/>
  <rect x="252" y="36" width="200" height="150" rx="8" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="264" y="54" font-size="8.5" font-weight="700" fill="var(--purple)">incoming update（补丁）</text>
  <text x="264" y="74" font-size="7.5" font-family="monospace" fill="var(--purple)">id: obs_7f</text>
  <text x="264" y="92" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">output: &quot;Here is…&quot;</text>
  <text x="264" y="108" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">total_cost: 0.0041</text>
  <text x="264" y="130" font-size="7" fill="var(--muted)">只带变更的字段</text>
  <line x1="460" y1="110" x2="492" y2="110" stroke="var(--accent)" stroke-width="1.4"/><polygon points="492,110 483,105 483,115" fill="var(--accent)"/>
  <rect x="484" y="36" width="216" height="150" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="496" y="54" font-size="8.5" font-weight="700" fill="var(--accent-ink)">结果行（写回 CH）</text>
  <text x="496" y="74" font-size="7.5" font-family="monospace" fill="var(--ink)">id: obs_7f</text>
  <text x="496" y="92" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">output: &quot;Here is…&quot;</text>
  <text x="496" y="108" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">total_cost: 0.0041</text>
  <text x="496" y="124" font-size="7.5" font-family="monospace" fill="var(--ink)">event_ts: 12:00:01.9</text>
  <text x="496" y="148" font-size="7" font-weight="700" fill="var(--accent-ink)">event_ts 更新 → 留这条</text>
</svg>
<div class="figcap"><b>合并是「叠补丁」，不是「改原行」</b>（语义对齐 <code>IngestionService</code>；<b>值为示例</b>）：update 只带<b>变更字段</b>，合并器把它叠到当前行上得到结果行，再以<b>更新的</b> <code>event_ts</code> 追加写入。ClickHouse 的 <code>ReplacingMergeTree</code> 查询时按 <code>event_ts</code> 留最新——于是「改」被实现成了「追加 + 查时取最新」。</div>
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

<svg viewBox="0 0 720 230" role="img" aria-label="processObservationEventList 七步流水线：1 幂等跳过、2 按时间排序、3 读 ClickHouse 底稿、4 事件转记录后 mergeRecords 合并、5 补 input/output、6 算 token 与成本、7 入 ClickhouseWriter 写库队列，IngestionService 自己从不直接写库">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="18" y="46" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="93" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">① 幂等跳过</text>
  <text x="93" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">查 Redis 去重</text>
  <rect x="193" y="46" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="268" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">② 按时间排序</text>
  <text x="268" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">create 先于 update</text>
  <rect x="368" y="46" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="443" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">③ 读 CH 底稿</text>
  <text x="443" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">已存在行当基线</text>
  <rect x="543" y="46" width="150" height="54" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="618" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">④ 合并</text>
  <text x="618" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">mergeRecords 左折叠</text>
  <rect x="18" y="140" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="93" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑤ 补 input/output</text>
  <text x="93" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">回找最新非空</text>
  <rect x="193" y="140" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="268" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑥ 算 token+成本</text>
  <text x="268" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">getGenerationUsage</text>
  <rect x="368" y="140" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="443" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑦ 入写库队列</text>
  <text x="443" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">addToQueue</text>
  <rect x="543" y="140" width="150" height="54" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="618" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">ClickhouseWriter</text>
  <text x="618" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">批写落盘（L17）</text>
  <line x1="168" y1="73" x2="193" y2="73" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="343" y1="73" x2="368" y2="73" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="518" y1="73" x2="543" y2="73" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="618" y1="100" x2="618" y2="122" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="618" y1="122" x2="93" y2="122" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="93" y1="122" x2="93" y2="140" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="168" y1="167" x2="193" y2="167" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="343" y1="167" x2="368" y2="167" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="518" y1="167" x2="543" y2="167" stroke="var(--teal)" stroke-width="2"></line>
  <text x="360" y="216" font-size="11" text-anchor="middle" fill="var(--muted)">IngestionService 只合并、从不直接写库——第 7 步只把最终记录塞进批写器队列</text>
</svg>

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
<div class="fig">
<svg viewBox="0 0 720 198" role="img" aria-label="The data view of merge: the currently stored observation row + an update patch (changed fields highlighted) = the result row; ReplacingMergeTree keeps the latest by event_ts. Semantics per IngestionService, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: merge = stored row + patch → new row</text>
  <rect x="20" y="36" width="216" height="150" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="32" y="54" font-size="8.5" font-weight="700" fill="var(--muted)">stored row</text>
  <text x="32" y="74" font-size="7.5" font-family="monospace" fill="var(--ink)">id: obs_7f</text>
  <text x="32" y="90" font-size="7.5" font-family="monospace" fill="var(--ink)">output: null</text>
  <text x="32" y="106" font-size="7.5" font-family="monospace" fill="var(--ink)">total_cost: null</text>
  <text x="32" y="122" font-size="7.5" font-family="monospace" fill="var(--ink)">event_ts: 12:00:00.1</text>
  <line x1="244" y1="110" x2="276" y2="110" stroke="var(--accent)" stroke-width="1.4"/><polygon points="276,110 267,105 267,115" fill="var(--accent)"/>
  <rect x="252" y="36" width="200" height="150" rx="8" fill="var(--purple-soft)" stroke="var(--purple)"/><text x="264" y="54" font-size="8.5" font-weight="700" fill="var(--purple)">incoming update (patch)</text>
  <text x="264" y="74" font-size="7.5" font-family="monospace" fill="var(--purple)">id: obs_7f</text>
  <text x="264" y="92" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">output: &quot;Here is…&quot;</text>
  <text x="264" y="108" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">total_cost: 0.0041</text>
  <text x="264" y="130" font-size="7" fill="var(--muted)">only the changed fields</text>
  <line x1="460" y1="110" x2="492" y2="110" stroke="var(--accent)" stroke-width="1.4"/><polygon points="492,110 483,105 483,115" fill="var(--accent)"/>
  <rect x="484" y="36" width="216" height="150" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="496" y="54" font-size="8.5" font-weight="700" fill="var(--accent-ink)">result row (written to CH)</text>
  <text x="496" y="74" font-size="7.5" font-family="monospace" fill="var(--ink)">id: obs_7f</text>
  <text x="496" y="92" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">output: &quot;Here is…&quot;</text>
  <text x="496" y="108" font-size="7.5" font-family="monospace" fill="var(--accent-ink)">total_cost: 0.0041</text>
  <text x="496" y="124" font-size="7.5" font-family="monospace" fill="var(--ink)">event_ts: 12:00:01.9</text>
  <text x="496" y="148" font-size="7" font-weight="700" fill="var(--accent-ink)">event_ts updated → keep this one</text>
</svg>
<div class="figcap"><b>Merge is “apply a patch”, not “edit the row in place”</b> (semantics per <code>IngestionService</code>; <b>values illustrative</b>): the update carries only <b>changed fields</b>; the merger overlays them onto the current row to get the result row, then appends it with an <b>updated</b> <code>event_ts</code>. ClickHouse's <code>ReplacingMergeTree</code> keeps the latest by <code>event_ts</code> at read time — so “update” is implemented as “append + keep-latest-at-query”.</div>
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

<svg viewBox="0 0 720 230" role="img" aria-label="processObservationEventList seven-step pipeline: 1 idempotency skip, 2 sort by time, 3 read the ClickHouse base row, 4 events to records then mergeRecords, 5 backfill input/output, 6 compute token and cost, 7 enqueue into the ClickhouseWriter; IngestionService never writes the DB directly">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="18" y="46" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="93" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">1 idempotency skip</text>
  <text x="93" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">dedup via Redis</text>
  <rect x="193" y="46" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="268" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">2 sort by time</text>
  <text x="268" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">create before update</text>
  <rect x="368" y="46" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="443" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">3 read CH base</text>
  <text x="443" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">existing row as baseline</text>
  <rect x="543" y="46" width="150" height="54" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="618" y="69" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">4 merge</text>
  <text x="618" y="86" font-size="9.5" text-anchor="middle" fill="var(--muted)">mergeRecords left-fold</text>
  <rect x="18" y="140" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="93" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">5 backfill in/out</text>
  <text x="93" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">latest non-empty</text>
  <rect x="193" y="140" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="268" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">6 token+cost</text>
  <text x="268" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">getGenerationUsage</text>
  <rect x="368" y="140" width="150" height="54" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="443" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">7 enqueue write</text>
  <text x="443" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">addToQueue</text>
  <rect x="543" y="140" width="150" height="54" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="618" y="163" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">ClickhouseWriter</text>
  <text x="618" y="180" font-size="9.5" text-anchor="middle" fill="var(--muted)">batched persist (L17)</text>
  <line x1="168" y1="73" x2="193" y2="73" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="343" y1="73" x2="368" y2="73" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="518" y1="73" x2="543" y2="73" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="618" y1="100" x2="618" y2="122" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="618" y1="122" x2="93" y2="122" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="93" y1="122" x2="93" y2="140" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="168" y1="167" x2="193" y2="167" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="343" y1="167" x2="368" y2="167" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="518" y1="167" x2="543" y2="167" stroke="var(--teal)" stroke-width="2"></line>
  <text x="360" y="216" font-size="11" text-anchor="middle" fill="var(--muted)">IngestionService only merges, never writes directly — step 7 just drops the final record into the writer's queue</text>
</svg>

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
  <div class="tag">🎯 Design trade-off</div>
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
<div class="fig">
<svg viewBox="0 0 720 232" role="img" aria-label="token 与成本拆解：上方堆叠条把 usageDetails 拆成 input 与 output token，下方成本条按各自单价折算成 costDetails；总额 total_cost。字段对齐 domain/observations.ts，单价结构对齐 default-model-prices.json，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：token 用量与成本的拆解</text>
  <text x="40" y="58" font-size="9" font-weight="700" fill="var(--blue)">usageDetails（token）</text>
  <rect x="40" y="64" width="380" height="30" rx="5" fill="var(--blue)" opacity="0.5"/><text x="230" y="83" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--blue)">input 512 tok</text>
  <rect x="420" y="64" width="120" height="30" rx="5" fill="var(--accent)" opacity="0.55"/><text x="480" y="83" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">output 88</text>
  <text x="556" y="84" font-size="8" fill="var(--muted)">= 600 tok</text>
  <text x="40" y="124" font-size="9" font-weight="700" fill="var(--amber)">costDetails（成本）</text>
  <rect x="40" y="130" width="150" height="30" rx="5" fill="var(--amber)" opacity="0.45"/><text x="115" y="149" text-anchor="middle" font-size="8" font-weight="700" fill="var(--amber)">input·单价</text>
  <rect x="190" y="130" width="230" height="30" rx="5" fill="var(--red)" opacity="0.4"/><text x="305" y="149" text-anchor="middle" font-size="8" font-weight="700" fill="var(--red)">output·单价（通常更贵）</text>
  <text x="436" y="150" font-size="8.5" font-weight="700" fill="var(--ink)">total_cost ≈ $0.0041</text>
  <rect x="40" y="178" width="640" height="44" rx="8" fill="var(--panel-2)" stroke="var(--line)"/>
  <text x="52" y="196" font-size="8" fill="var(--ink)">cost = input_tok × in_price + output_tok × out_price</text>
  <text x="52" y="212" font-size="7.5" fill="var(--muted)">单价按 model 从定价表查（match-pattern）；usage 没带就按 tokenizer 估，再算钱</text>
</svg>
<div class="figcap"><b>token 决定钱</b>（字段对齐 <code>domain/observations.ts</code> 的 <code>usageDetails/costDetails</code>，单价结构对齐 <code>worker/src/constants/default-model-prices.json</code>；<b>值为示例</b>）：先把用量拆成 <b>input/output token</b>，再按该 <code>model</code> 的<b>各自单价</b>折算成 <code>costDetails</code> 求和得 <code>total_cost</code>。注意 output 单价通常比 input 贵，所以「话多」比「读得多」更费钱。</div>
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

<svg viewBox="0 0 720 250" role="img" aria-label="findModel 把上报模型名 gpt-4o-2024-08-06 拿到 Postgres models 表上，用 Postgres 正则运算符逐行套 match_pattern，命中后按 project_id 优先、start_date 倒序取一条，得到价格 tiers 与 tokenizer_id">
  <rect x="0" y="0" width="720" height="250" fill="var(--bg)"></rect>
  <rect x="16" y="60" width="190" height="50" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="111" y="82" font-size="11" text-anchor="middle" fill="var(--muted)">上报模型名</text>
  <text x="111" y="100" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">gpt-4o-2024-08-06</text>
  <text x="111" y="130" font-size="10" text-anchor="middle" fill="var(--muted)">findModel(...)</text>
  <line x1="206" y1="85" x2="236" y2="85" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="236" y="30" width="300" height="178" rx="10" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="248" y="50" font-size="11" font-weight="700" fill="var(--accent-ink)">Postgres models 表 · 每行一条正则 match_pattern</text>
  <rect x="248" y="60" width="276" height="30" rx="5" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="256" y="79" font-size="10" fill="var(--ink)">(?i)^(openai/)?(gpt-4o-2024-08-06)$　✓命中</text>
  <rect x="248" y="96" width="276" height="28" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="256" y="114" font-size="10" fill="var(--muted)">(?i)^(openai/)?(gpt-4o)$</text>
  <rect x="248" y="130" width="276" height="28" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="256" y="148" font-size="10" fill="var(--muted)">(?i)^(claude-3-5-sonnet-.*)$</text>
  <text x="248" y="180" font-size="9" fill="var(--muted)">WHERE project_id=? OR NULL</text>
  <text x="248" y="196" font-size="9" fill="var(--muted)">ORDER BY project_id, start_date DESC · LIMIT 1</text>
  <line x1="536" y1="85" x2="566" y2="85" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="566" y="56" width="140" height="104" rx="10" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="636" y="78" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">命中行</text>
  <text x="636" y="102" font-size="10.5" text-anchor="middle" fill="var(--ink)">→ 价格 tiers</text>
  <text x="636" y="124" font-size="10.5" text-anchor="middle" fill="var(--ink)">→ tokenizer_id</text>
  <text x="636" y="142" font-size="9" text-anchor="middle" fill="var(--muted)">（定分词器）</text>
  <text x="360" y="234" font-size="11" text-anchor="middle" fill="var(--muted)">项目模型盖过全局、新价盖过旧价：正则给灵活、project_id 给覆盖权、start_date 给时间维度</text>
</svg>

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
<div class="fig">
<svg viewBox="0 0 720 232" role="img" aria-label="Token and cost breakdown: the top stacked bar splits usageDetails into input and output tokens, the bottom cost bar converts each at its unit price into costDetails; total is total_cost. Fields per domain/observations.ts, price structure per default-model-prices.json, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: token usage and cost breakdown</text>
  <text x="40" y="58" font-size="9" font-weight="700" fill="var(--blue)">usageDetails (tokens)</text>
  <rect x="40" y="64" width="380" height="30" rx="5" fill="var(--blue)" opacity="0.5"/><text x="230" y="83" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--blue)">input 512 tok</text>
  <rect x="420" y="64" width="120" height="30" rx="5" fill="var(--accent)" opacity="0.55"/><text x="480" y="83" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">output 88</text>
  <text x="556" y="84" font-size="8" fill="var(--muted)">= 600 tok</text>
  <text x="40" y="124" font-size="9" font-weight="700" fill="var(--amber)">costDetails (cost)</text>
  <rect x="40" y="130" width="150" height="30" rx="5" fill="var(--amber)" opacity="0.45"/><text x="115" y="149" text-anchor="middle" font-size="8" font-weight="700" fill="var(--amber)">input · unit price</text>
  <rect x="190" y="130" width="230" height="30" rx="5" fill="var(--red)" opacity="0.4"/><text x="305" y="149" text-anchor="middle" font-size="8" font-weight="700" fill="var(--red)">output · unit price (usually pricier)</text>
  <text x="436" y="150" font-size="8.5" font-weight="700" fill="var(--ink)">total_cost ≈ $0.0041</text>
  <rect x="40" y="178" width="640" height="44" rx="8" fill="var(--panel-2)" stroke="var(--line)"/>
  <text x="52" y="196" font-size="8" fill="var(--ink)">cost = input_tok × in_price + output_tok × out_price</text>
  <text x="52" y="212" font-size="7.5" fill="var(--muted)">unit price looked up by model (match-pattern); if usage absent, estimate via tokenizer, then cost it</text>
</svg>
<div class="figcap"><b>Tokens drive cost</b> (fields per <code>usageDetails/costDetails</code> in <code>domain/observations.ts</code>, price structure per <code>worker/src/constants/default-model-prices.json</code>; <b>values illustrative</b>): usage splits into <b>input/output tokens</b>, each converted at the <code>model</code>'s <b>own unit price</b> into <code>costDetails</code> and summed into <code>total_cost</code>. Output is usually pricier than input, so “talking a lot” costs more than “reading a lot”.</div>
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

<svg viewBox="0 0 720 250" role="img" aria-label="findModel takes the reported model name gpt-4o-2024-08-06 to the Postgres models table, tests each row's match_pattern with the regex operator, then picks one ordered by project_id priority and start_date desc, yielding price tiers and tokenizer_id">
  <rect x="0" y="0" width="720" height="250" fill="var(--bg)"></rect>
  <rect x="16" y="60" width="190" height="50" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="111" y="82" font-size="11" text-anchor="middle" fill="var(--muted)">reported model name</text>
  <text x="111" y="100" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">gpt-4o-2024-08-06</text>
  <text x="111" y="130" font-size="10" text-anchor="middle" fill="var(--muted)">findModel(...)</text>
  <line x1="206" y1="85" x2="236" y2="85" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="236" y="30" width="300" height="178" rx="10" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="248" y="50" font-size="11" font-weight="700" fill="var(--accent-ink)">Postgres models · each row a regex match_pattern</text>
  <rect x="248" y="60" width="276" height="30" rx="5" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="256" y="79" font-size="10" fill="var(--ink)">(?i)^(openai/)?(gpt-4o-2024-08-06)$　✓match</text>
  <rect x="248" y="96" width="276" height="28" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="256" y="114" font-size="10" fill="var(--muted)">(?i)^(openai/)?(gpt-4o)$</text>
  <rect x="248" y="130" width="276" height="28" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="256" y="148" font-size="10" fill="var(--muted)">(?i)^(claude-3-5-sonnet-.*)$</text>
  <text x="248" y="180" font-size="9" fill="var(--muted)">WHERE project_id=? OR NULL</text>
  <text x="248" y="196" font-size="9" fill="var(--muted)">ORDER BY project_id, start_date DESC · LIMIT 1</text>
  <line x1="536" y1="85" x2="566" y2="85" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="566" y="56" width="140" height="104" rx="10" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="636" y="78" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">matched row</text>
  <text x="636" y="102" font-size="10.5" text-anchor="middle" fill="var(--ink)">→ price tiers</text>
  <text x="636" y="124" font-size="10.5" text-anchor="middle" fill="var(--ink)">→ tokenizer_id</text>
  <text x="636" y="142" font-size="9" text-anchor="middle" fill="var(--muted)">(picks tokenizer)</text>
  <text x="360" y="234" font-size="11" text-anchor="middle" fill="var(--muted)">project model beats global, new price beats old: regex gives flex, project_id gives override, start_date gives time</text>
</svg>

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
  <div class="tag">🎯 Design trade-off</div>
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


# ══════════════════════════════════════════════════════════════════════
# L17 · ClickhouseWriter：批量落盘 / ClickhouseWriter: batched persistence
# ══════════════════════════════════════════════════════════════════════
_ZH17 = []
_EN17 = []

_ZH17.append(r"""
<p class="lead">
第 15 课合并完，最后一步是 <code>clickHouseWriter.addToQueue(...)</code>——记录被塞进一个队列，而不是马上写库。这一课就讲那个队列背后的
<code>ClickhouseWriter</code>：一个<strong>单例</strong>，把潮水般涌来的<strong>单条记录</strong>攒成<strong>少数几个大批次</strong>，再一次性 INSERT 进 ClickHouse。
为什么非要攒？因为第 8 课说过，ClickHouse <strong>极度偏爱大批量写入</strong>、最怕逐条插入。这一层，就是把「高频小写」翻译成「低频大写」的<strong>缓冲带</strong>。
</p>

<div class="card analogy">
  <div class="tag">🚌 生活类比</div>
  把 <code>ClickhouseWriter</code> 想成<strong>摆渡班车</strong>。乘客（记录）一个个到站，司机<strong>不会来一个就开一趟</strong>——那样油费（写入开销）高得离谱。
  他等到<strong>车坐满了</strong>（达到 batchSize），<strong>或者</strong>发车时刻到了（writeInterval 定时器响），就<strong>一趟把整车人送过去</strong>。
  两个条件<strong>谁先到就按谁发</strong>：高峰期车一会儿就满、靠「坐满」发车；低谷期人少，就靠「到点」发车，免得最后几个乘客干等太久。
  而且<strong>每条线路（每张表）都有自己的一辆车</strong>：traces 一辆、observations 一辆、scores 一辆，各坐各的、各发各的，互不耽误。
</div>
""")

# (L17 sections appended below)

_ZH17.append(r"""
<h2>缓冲带：每张表一个队列，两个发车条件</h2>
<p><code>ClickhouseWriter</code> 内部为<strong>每张表各开一个内存队列</strong>（traces / observations / scores / …）。
第 15 课的 <code>addToQueue</code> 把合并好的记录推进对应队列；记录在队列里<strong>排队等发车</strong>。发车（flush）由<strong>两个条件</strong>触发，谁先到算谁：</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="ClickhouseWriter 为每张表开内存队列，记录达 batchSize 或 writeInterval 定时器触发时批量 INSERT 进 ClickHouse">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">ClickhouseWriter：攒批 → 批量 INSERT</text>
  <rect x="14" y="60" width="120" height="130" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="74" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">IngestionService</text><text x="74" y="95" text-anchor="middle" font-size="7.5" fill="var(--muted)">第 15 课</text><text x="74" y="120" text-anchor="middle" font-size="8" fill="var(--muted)">addToQueue</text><text x="74" y="134" text-anchor="middle" font-size="8" fill="var(--muted)">一条条推进来</text>
  <rect x="170" y="48" width="190" height="50" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="265" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">queue[traces] ▢▢▢▢</text><text x="265" y="84" text-anchor="middle" font-size="7.5" fill="var(--muted)">攒到 batchSize…</text>
  <rect x="170" y="104" width="190" height="50" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="265" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">queue[observations] ▢▢▢</text><text x="265" y="140" text-anchor="middle" font-size="7.5" fill="var(--muted)">各表独立</text>
  <rect x="170" y="160" width="190" height="50" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="265" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">queue[scores] ▢▢</text><text x="265" y="196" text-anchor="middle" font-size="7.5" fill="var(--muted)">各发各的</text>
  <rect x="398" y="78" width="150" height="104" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="473" y="104" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">flush 触发</text><text x="473" y="126" text-anchor="middle" font-size="8" fill="var(--accent-ink)">① 队列 ≥ batchSize</text><text x="473" y="144" text-anchor="middle" font-size="8" fill="var(--accent-ink)">② writeInterval 到点</text><text x="473" y="166" text-anchor="middle" font-size="7.5" fill="var(--muted)">谁先到算谁</text>
  <rect x="584" y="88" width="122" height="84" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="645" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">ClickHouse</text><text x="645" y="136" text-anchor="middle" font-size="8" fill="var(--muted)">一次 INSERT</text><text x="645" y="150" text-anchor="middle" font-size="8" fill="var(--muted)">整批写入</text>
  <line x1="134" y1="120" x2="168" y2="80" stroke="var(--faint)" stroke-width="1.4"/><line x1="134" y1="125" x2="168" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="134" y1="130" x2="168" y2="180" stroke="var(--faint)" stroke-width="1.4"/>
  <line x1="360" y1="125" x2="396" y2="125" stroke="var(--accent)" stroke-width="1.6"/><polygon points="396,125 387,121 387,129" fill="var(--accent)"/>
  <line x1="548" y1="128" x2="582" y2="128" stroke="var(--teal)" stroke-width="1.8"/><polygon points="582,128 573,124 573,132" fill="var(--teal)"/>
</svg>
<div class="figcap"><b>攒批缓冲带</b>：每张表一个内存队列；<code>addToQueue</code> 喂入，达 <code>batchSize</code> 立刻 flush 该表，或定时器每 <code>writeInterval</code> 触发 <code>flushAll</code> 刷所有表。flush 把整批一次 <code>INSERT</code>（<code>JSONEachRow</code>）。源码：<code>worker/src/services/ClickhouseWriter/index.ts:34-135, 550-600</code>。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 226" role="img" aria-label="ClickhouseWriter 时间轴：事件按表攒进内存缓冲，达到 batchSize 触发按量 flush，或每 writeInterval 触发按时 flush，关机时 flushAll(true) 排空。常量名对齐 ClickhouseWriter，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：批写器的攒批与 flush 时刻</text>
  <line x1="40" y1="180" x2="690" y2="180" stroke="var(--line)" stroke-width="1.2"/><text x="690" y="196" text-anchor="end" font-size="8" fill="var(--muted)">时间 →</text>
  <text x="20" y="70" font-size="8" fill="var(--muted)">缓冲量</text>
  <path d="M40 175 L150 100 L152 175 L260 70 L262 175 L400 130 L500 175" fill="none" stroke="var(--accent)" stroke-width="1.8"/>
  <line x1="40" y1="100" x2="690" y2="100" stroke="var(--blue)" stroke-width="1" stroke-dasharray="4 3"/><text x="44" y="96" font-size="7.5" fill="var(--blue)">batchSize 阈值</text>
  <line x1="150" y1="60" x2="150" y2="180" stroke="var(--accent)" stroke-width="1" stroke-dasharray="3 2"/><rect x="108" y="44" width="86" height="16" rx="4" fill="var(--accent-soft)"/><text x="151" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">① 按量 flush</text>
  <line x1="260" y1="60" x2="260" y2="180" stroke="var(--accent)" stroke-width="1" stroke-dasharray="3 2"/><rect x="218" y="44" width="86" height="16" rx="4" fill="var(--accent-soft)"/><text x="261" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">① 按量 flush</text>
  <line x1="400" y1="120" x2="400" y2="180" stroke="var(--blue)" stroke-width="1" stroke-dasharray="3 2"/><rect x="356" y="104" width="92" height="16" rx="4" fill="var(--blue-soft)"/><text x="402" y="116" text-anchor="middle" font-size="7" font-weight="700" fill="var(--blue)">② 按时 flush</text>
  <text x="400" y="150" text-anchor="middle" font-size="6.6" fill="var(--blue)">writeInterval 到点</text>
  <line x1="600" y1="40" x2="600" y2="180" stroke="var(--red)" stroke-width="1.2"/><rect x="556" y="44" width="92" height="16" rx="4" fill="var(--red-soft)"/><text x="602" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="var(--red)">③ flushAll(true)</text><text x="600" y="76" text-anchor="middle" font-size="6.6" fill="var(--red)">关机排空·不丢</text>
  <text x="40" y="212" font-size="7.5" fill="var(--muted)">谁先到算谁：攒满 batchSize 或到 writeInterval 就批量 INSERT 一次；优雅停机一次写尽</text>
</svg>
<div class="figcap"><b>攒批落盘：按量 + 按时 双触发</b>（常量名对齐 <code>ClickhouseWriter</code>；<b>值为示例</b>）：事件先进<b>每表内存缓冲</b>，<code>batchSize</code> 攒满就<b>按量 flush</b>，否则每 <code>writeInterval</code> <b>按时 flush</b>，谁先到算谁；关机时 <code>flushAll(true)</code> 一次写尽不丢数据。用「批量 INSERT」换 ClickHouse 的高写入吞吐。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/services/ClickhouseWriter/index.ts</span><span class="ln">两个触发</span></div>
  <pre class="code"><span class="cm">// 触发①：入队时，本表攒够一批就立刻刷</span>
<span class="fn">addToQueue</span>(tableName, data) {
  <span class="kw">this</span>.queue[tableName].<span class="fn">push</span>({ createdAt: Date.now(), data });
  <span class="kw">if</span> (<span class="kw">this</span>.queue[tableName].length &gt;= <span class="kw">this</span>.batchSize)
    <span class="kw">this</span>.<span class="fn">flush</span>(tableName);          <span class="cm">// 坐满发车</span>
}
<span class="cm">// 触发②：定时器，每 writeInterval 毫秒刷所有表</span>
<span class="fn">setInterval</span>(() =&gt; <span class="kw">this</span>.<span class="fn">flushAll</span>(), <span class="kw">this</span>.writeInterval);   <span class="cm">// 到点发车</span>

<span class="cm">// flush：从队列取一批，批量 INSERT（带退避重试 maxAttempts）</span>
<span class="kw">const</span> items = entityQueue.<span class="fn">splice</span>(0, fullQueue ? all : <span class="kw">this</span>.batchSize);
<span class="kw">await</span> <span class="fn">backOff</span>(() =&gt; <span class="fn">writeToClickhouse</span>({ table, records }), { numOfAttempts });</pre>
</div>

<p>为什么 ClickHouse 这么怕「逐条写」？回到第 8 课的存储机制：MergeTree 每收一次 <code>INSERT</code> 就在磁盘上落一个新的<strong>数据分片（part）</strong>，
之后还要靠后台不断把小分片<strong>合并</strong>成大分片。如果你每条记录都单独 INSERT，瞬间会产生<strong>海量小分片</strong>——磁盘元数据爆炸、后台合并永远追不上、查询也被拖慢
（甚至触发 ClickHouse 的「too many parts」保护而拒写）。把一万条记录攒成一次 INSERT，就只生成<strong>一个</strong>大分片，写入、合并、查询全都轻松。
所以这一层不是可有可无的优化，而是让 ClickHouse 这种列式存储能扛住高频摄取的<strong>必要前提</strong>——没有这道缓冲带，再好的表设计也会被海量小写拖垮。</p>
""")

# (triggers + shutdown section below)

_ZH17.append(r"""
<h2>两个发车条件，外加一次优雅排空</h2>
<p>「坐满」和「到点」这两个条件，分别照顾了两种负载，缺一不可：</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="高峰期靠 batchSize 坐满即发，低谷期靠 writeInterval 到点即发，关机时 flushAll 排空所有队列">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">谁先到算谁：吞吐与延迟的平衡</text>
  <text x="20" y="58" font-size="9" font-weight="700" fill="var(--accent-ink)">高峰期</text>
  <rect x="20" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="44" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="68" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="92" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="116" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="150" y="81" font-size="8.5" fill="var(--ink)">▶ 瞬间坐满 batchSize</text>
  <rect x="300" y="64" width="120" height="26" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="81" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① 立刻 flush（按量）</text>
  <text x="448" y="81" font-size="8" fill="var(--muted)">延迟极低、批批都满，吞吐拉满</text>
  <text x="20" y="118" font-size="9" font-weight="700" fill="var(--blue)">低谷期</text>
  <rect x="20" y="126" width="20" height="22" rx="3" fill="var(--blue-soft)" stroke="var(--blue)"/><rect x="44" y="126" width="20" height="22" rx="3" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="80" y="141" font-size="8.5" fill="var(--ink)">▶ 半天才两条，凑不满</text>
  <rect x="300" y="124" width="120" height="26" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="141" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② 到点 flush（按时）</text>
  <text x="448" y="141" font-size="8" fill="var(--muted)">每 writeInterval 一刷，不让数据干等</text>
  <text x="20" y="178" font-size="9" font-weight="700" fill="var(--amber)">关机时</text>
  <rect x="300" y="166" width="120" height="26" rx="6" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="360" y="183" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">flushAll(true) 排空</text>
  <text x="448" y="183" font-size="8" fill="var(--muted)">清定时器 + 把所有队列一次写尽，不丢数据</text>
</svg>
<div class="figcap"><b>两条件互补 + 优雅关机</b>：高峰靠 <code>batchSize</code> 保吞吐，低谷靠 <code>writeInterval</code> 保延迟上限；<code>shutdown</code> 先 <code>clearInterval</code> 再 <code>flushAll(true)</code> 把内存里剩的全部写尽。<code>flushAll</code> 用 <code>Promise.all</code> 并行刷各表。</div>
</div>

<table class="t">
  <tr><th>触发</th><th>条件</th><th>解决什么</th></tr>
  <tr><td><b>① 按量（batchSize）</b></td><td>某表队列长度 ≥ <code>batchSize</code></td><td>高吞吐时批批写满，把 ClickHouse 的写入效率拉满</td></tr>
  <tr><td><b>② 按时（writeInterval）</b></td><td>定时器每 <code>writeInterval</code> 毫秒触发 <code>flushAll</code></td><td>低吞吐时给延迟封顶，数据不会无限期滞留内存</td></tr>
  <tr><td><b>③ 关机排空</b></td><td><code>shutdown()</code> 调 <code>flushAll(true)</code></td><td>进程退出前把缓冲全部落盘，避免丢数据</td></tr>
</table>

<p>这两个参数 <code>batchSize</code> 与 <code>writeInterval</code> 其实是一对<strong>吞吐 / 延迟旋钮</strong>：调大 batchSize、拉长 interval，批更大、写库更省，但单条记录从「算完」到「能被查到」的延迟变长；
反之延迟低但写得更碎。Langfuse 把它们做成<strong>环境变量</strong>，让你按自己的流量与时效要求自由去拧，无需改代码。</p>

<p>把一条合并好的记录在写入器里的旅程拆开，正好五步：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>入队</h4><p><code>addToQueue(table, record)</code> 把记录连同 <code>createdAt</code> 时间戳推进该表队列尾部。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>等发车</h4><p>记录在内存队列里排队。期间系统还会记录它<strong>等了多久</strong>（wait_time 指标），用来观测积压。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>触发 flush</h4><p>本表攒到 <code>batchSize</code>（按量）或定时器到点（按时），<code>splice</code> 取出最多一批。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>批量写入</h4><p><code>writeToClickhouse</code> 把整批以 <code>JSONEachRow</code> 一次 <code>INSERT</code>；带 <code>backOff</code> 退避重试。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>成功 / 重试</h4><p>成功则这批出队完成；可重试错误退避再试，超长批拆小重排队——尽量不连累整批。</p></div></div>
</div>
""")

# (singleton + resilience + spark + key below)

_ZH17.append(r"""
<h2>为什么是单例，为什么敢用内存缓冲</h2>
<p><code>ClickhouseWriter</code> 是<strong>单例</strong>（私有构造 + <code>getInstance</code>）：整个 worker 进程<strong>只有一个</strong>写入器、一组队列。这很关键——
只有汇到一处，才能把来自无数任务的零散记录<strong>真正攒成大批</strong>；如果每个任务各写各的，批就永远攒不大。写入时还带<strong>退避重试</strong>（<code>maxAttempts</code>），
遇到可重试错误就指数退避再试，遇到「字符串过长」这类错误则<strong>把批拆小</strong>重试——既追求大批量，又不被个别异常记录拖垮整批。这种「<strong>整批共进退、坏的单独拎出来</strong>」的策略，和第 12 课摄取 API 的「部分成功」一脉相承：系统在每一层都尽量做到<strong>容错而不牵连</strong>，让一两条问题数据不至于阻塞整条管道。</p>

<svg viewBox="0 0 720 250" role="img" aria-label="ClickhouseWriter 的内存缓冲是易失的，崩溃会丢这批；但 S3 事件账本绝不丢、队列任务在写库成功前不 ack，于是 worker 半路崩溃时任务会重投、从 S3 重读重合并重写，数据一条不少，持久性由上游兜底所以这层敢用易失缓冲换吞吐">
  <rect x="0" y="0" width="720" height="250" fill="var(--bg)"></rect>
  <rect x="18" y="44" width="210" height="52" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="123" y="68" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">S3 · 事件账本</text>
  <text x="123" y="86" font-size="10" text-anchor="middle" fill="var(--muted)">绝不丢 · 持久层</text>
  <rect x="18" y="120" width="210" height="52" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="123" y="144" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">队列任务</text>
  <text x="123" y="162" font-size="10" text-anchor="middle" fill="var(--muted)">写库成功前不 ack</text>
  <line x1="228" y1="70" x2="268" y2="100" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="228" y1="146" x2="268" y2="130" stroke="var(--faint)" stroke-width="1.5"></line>
  <rect x="268" y="72" width="190" height="92" rx="10" fill="var(--amber-soft)" stroke="var(--accent)" stroke-dasharray="5 3"></rect>
  <text x="363" y="96" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">ClickhouseWriter</text>
  <text x="363" y="114" font-size="10.5" text-anchor="middle" fill="var(--muted)">内存缓冲（易失·攒大批）</text>
  <text x="363" y="140" font-size="10.5" text-anchor="middle" fill="var(--ink)">⚡ 崩溃 → 这批丢失</text>
  <line x1="458" y1="118" x2="500" y2="118" stroke="var(--teal)" stroke-width="2"></line>
  <rect x="500" y="84" width="200" height="68" rx="10" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="600" y="112" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">ClickHouse 最终行</text>
  <text x="600" y="132" font-size="10.5" text-anchor="middle" fill="var(--ink)">数据一条不少</text>
  <line x1="363" y1="164" x2="363" y2="196" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="363" y1="196" x2="123" y2="196" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="123" y1="196" x2="123" y2="172" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="243" y="214" font-size="10" text-anchor="middle" fill="var(--muted)">崩了就重投：从 S3 重读 → 重合并 → 重写</text>
  <text x="360" y="236" font-size="11" text-anchor="middle" fill="var(--muted)">持久性由 S3 + 队列兜底，这一层才敢用易失内存缓冲去换写入吞吐</text>
</svg>

<div class="cols">
  <div class="col"><h4>🧩 单例 + 按表队列</h4><p>一个进程一个 writer，把所有任务的记录汇聚成大批；按表分队列，让 traces/observations/scores 各自满批、并行刷，互不阻塞。</p></div>
  <div class="col"><h4>🛡️ 批量写 + 退避重试</h4><p>一次 INSERT 写整批（<code>JSONEachRow</code>），失败按 <code>maxAttempts</code> 退避重试；超长批自动拆分。把「写得快」和「写得稳」一起拿下。</p></div>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>记录攒在内存队列里，万一 worker 突然崩了，这批不就丢了吗？</strong> 会丢——但这<strong>不要紧</strong>，因为真正的「账本」不在这里。回想第 14 课：
  每个事件都<strong>原原本本躺在 S3</strong>，而队列任务在写库成功前<strong>不会被确认</strong>。于是 worker 半路崩溃，最多是这批合并结果没落盘，
  对应的队列任务会<strong>重新投递</strong>、从 S3 重新读事件、重新合并重新写——<strong>数据一条不少</strong>。正因为<strong>持久性已经由上游的 S3 + 队列兜底</strong>，
  这一层才敢<strong>放心地用易失的内存缓冲去换写入吞吐</strong>。这是一个典型的分层设计智慧：<strong>把持久和高效分给不同层，各自做到极致</strong>——
  S3 负责「绝不丢」，ClickhouseWriter 负责「写得快」，谁也不必为对方的目标妥协。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><code>ClickhouseWriter</code> 是<strong>单例</strong>，把高频单条记录攒成<strong>大批</strong>再一次 <code>INSERT</code>——因为第 8 课 ClickHouse 偏爱大批量、最怕逐条。</li>
    <li><strong>每张表一个内存队列</strong>（traces/observations/scores…），<code>addToQueue</code> 喂入，<code>flushAll</code> 用 <code>Promise.all</code> 并行刷各表。</li>
    <li><strong>两个 flush 触发</strong>：① 队列 ≥ <code>batchSize</code>（按量，保吞吐）② 每 <code>writeInterval</code> 定时器（按时，封顶延迟）；谁先到算谁。</li>
    <li><code>shutdown</code> 先清定时器、再 <code>flushAll(true)</code> <strong>排空</strong>所有队列，进程退出不丢数据；写入带退避重试、超长批自动拆分。</li>
    <li>敢用<strong>易失内存缓冲换吞吐</strong>，是因为<strong>持久性由上游 S3 + 队列兜底</strong>（第 14 课）：崩了就重投重算，一条不丢——分层各司其职。</li>
  </ul>
</div>
""")

_EN17.append(r"""
<p class="lead">
Lesson 15's merge ended with <code>clickHouseWriter.addToQueue(...)</code> — the record goes into a queue, not straight to the DB. This lesson covers
what's behind that queue, the <code>ClickhouseWriter</code>: a <strong>singleton</strong> that gathers the flood of <strong>single records</strong> into a
handful of <strong>big batches</strong>, then INSERTs them into ClickHouse in one shot. Why batch at all? Because, as Lesson 8 said, ClickHouse
<strong>strongly prefers large batched writes</strong> and dreads row-by-row inserts. This layer is the <strong>buffer</strong> that translates
"high-frequency small writes" into "low-frequency large writes".
</p>

<div class="card analogy">
  <div class="tag">🚌 Analogy</div>
  Think of <code>ClickhouseWriter</code> as a <strong>shuttle bus</strong>. Passengers (records) arrive one by one, but the driver <strong>doesn't depart
  for each one</strong> — the fuel cost (write overhead) would be absurd. He waits until the <strong>bus is full</strong> (hits batchSize), <strong>or</strong>
  the departure time arrives (the writeInterval timer fires), then <strong>takes the whole busload across in one trip</strong>. Whichever condition comes
  first wins: at rush hour the bus fills fast and leaves on "full"; in a lull, few passengers, so it leaves on "time" so the last few don't wait forever.
  And <strong>each route (each table) has its own bus</strong>: one for traces, one for observations, one for scores, each loading and departing
  independently, never holding up the others.
</div>
""")

_EN17.append(r"""
<h2>The buffer: one queue per table, two departure conditions</h2>
<p>Inside, <code>ClickhouseWriter</code> keeps <strong>an in-memory queue per table</strong> (traces / observations / scores / …). Lesson 15's
<code>addToQueue</code> pushes the merged record into the matching queue; records <strong>wait in line to depart</strong>. Departure (flush) is triggered by
<strong>two conditions</strong>, whichever comes first:</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="ClickhouseWriter keeps a per-table in-memory queue; records batch-INSERT into ClickHouse when hitting batchSize or when the writeInterval timer fires">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">ClickhouseWriter: batch up → bulk INSERT</text>
  <rect x="14" y="60" width="120" height="130" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="74" y="80" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">IngestionService</text><text x="74" y="95" text-anchor="middle" font-size="7.5" fill="var(--muted)">Lesson 15</text><text x="74" y="120" text-anchor="middle" font-size="8" fill="var(--muted)">addToQueue</text><text x="74" y="134" text-anchor="middle" font-size="8" fill="var(--muted)">pushed one by one</text>
  <rect x="170" y="48" width="190" height="50" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="265" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">queue[traces] ▢▢▢▢</text><text x="265" y="84" text-anchor="middle" font-size="7.5" fill="var(--muted)">fills to batchSize…</text>
  <rect x="170" y="104" width="190" height="50" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="265" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">queue[observations] ▢▢▢</text><text x="265" y="140" text-anchor="middle" font-size="7.5" fill="var(--muted)">per-table independent</text>
  <rect x="170" y="160" width="190" height="50" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="265" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">queue[scores] ▢▢</text><text x="265" y="196" text-anchor="middle" font-size="7.5" fill="var(--muted)">each departs on its own</text>
  <rect x="398" y="78" width="150" height="104" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="473" y="104" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">flush trigger</text><text x="473" y="126" text-anchor="middle" font-size="8" fill="var(--accent-ink)">① queue ≥ batchSize</text><text x="473" y="144" text-anchor="middle" font-size="8" fill="var(--accent-ink)">② writeInterval elapsed</text><text x="473" y="166" text-anchor="middle" font-size="7.5" fill="var(--muted)">whichever first</text>
  <rect x="584" y="88" width="122" height="84" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="645" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">ClickHouse</text><text x="645" y="136" text-anchor="middle" font-size="8" fill="var(--muted)">one INSERT</text><text x="645" y="150" text-anchor="middle" font-size="8" fill="var(--muted)">whole batch</text>
  <line x1="134" y1="120" x2="168" y2="80" stroke="var(--faint)" stroke-width="1.4"/><line x1="134" y1="125" x2="168" y2="128" stroke="var(--faint)" stroke-width="1.4"/><line x1="134" y1="130" x2="168" y2="180" stroke="var(--faint)" stroke-width="1.4"/>
  <line x1="360" y1="125" x2="396" y2="125" stroke="var(--accent)" stroke-width="1.6"/><polygon points="396,125 387,121 387,129" fill="var(--accent)"/>
  <line x1="548" y1="128" x2="582" y2="128" stroke="var(--teal)" stroke-width="1.8"/><polygon points="582,128 573,124 573,132" fill="var(--teal)"/>
</svg>
<div class="figcap"><b>A batching buffer</b>: one in-memory queue per table; <code>addToQueue</code> feeds it, hitting <code>batchSize</code> flushes that table immediately, or the timer fires <code>flushAll</code> every <code>writeInterval</code>. flush sends the whole batch in one <code>INSERT</code> (<code>JSONEachRow</code>). Source: <code>worker/src/services/ClickhouseWriter/index.ts:34-135, 550-600</code>.</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 226" role="img" aria-label="ClickhouseWriter timeline: events accumulate into per-table memory buffers, a flush fires at batchSize (by size) or every writeInterval (by time), and flushAll(true) drains at shutdown. Constant names per ClickhouseWriter, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: the batch writer accumulating then flushing</text>
  <line x1="40" y1="180" x2="690" y2="180" stroke="var(--line)" stroke-width="1.2"/><text x="690" y="196" text-anchor="end" font-size="8" fill="var(--muted)">time →</text>
  <text x="20" y="70" font-size="8" fill="var(--muted)">buffered</text>
  <path d="M40 175 L150 100 L152 175 L260 70 L262 175 L400 130 L500 175" fill="none" stroke="var(--accent)" stroke-width="1.8"/>
  <line x1="40" y1="100" x2="690" y2="100" stroke="var(--blue)" stroke-width="1" stroke-dasharray="4 3"/><text x="44" y="96" font-size="7.5" fill="var(--blue)">batchSize threshold</text>
  <line x1="150" y1="60" x2="150" y2="180" stroke="var(--accent)" stroke-width="1" stroke-dasharray="3 2"/><rect x="108" y="44" width="86" height="16" rx="4" fill="var(--accent-soft)"/><text x="151" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">① flush by size</text>
  <line x1="260" y1="60" x2="260" y2="180" stroke="var(--accent)" stroke-width="1" stroke-dasharray="3 2"/><rect x="218" y="44" width="86" height="16" rx="4" fill="var(--accent-soft)"/><text x="261" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">① flush by size</text>
  <line x1="400" y1="120" x2="400" y2="180" stroke="var(--blue)" stroke-width="1" stroke-dasharray="3 2"/><rect x="356" y="104" width="92" height="16" rx="4" fill="var(--blue-soft)"/><text x="402" y="116" text-anchor="middle" font-size="7" font-weight="700" fill="var(--blue)">② flush by time</text>
  <text x="400" y="150" text-anchor="middle" font-size="6.6" fill="var(--blue)">writeInterval elapsed</text>
  <line x1="600" y1="40" x2="600" y2="180" stroke="var(--red)" stroke-width="1.2"/><rect x="556" y="44" width="92" height="16" rx="4" fill="var(--red-soft)"/><text x="602" y="56" text-anchor="middle" font-size="7" font-weight="700" fill="var(--red)">③ flushAll(true)</text><text x="600" y="76" text-anchor="middle" font-size="6.6" fill="var(--red)">drain on shutdown · no loss</text>
  <text x="40" y="212" font-size="7.5" fill="var(--muted)">whichever comes first: when batchSize fills or writeInterval elapses, batch-INSERT once; graceful shutdown flushes all</text>
</svg>
<div class="figcap"><b>Batched persistence: flush by size and by time</b> (constant names per <code>ClickhouseWriter</code>; <b>values illustrative</b>): events enter a <b>per-table memory buffer</b>; a full <code>batchSize</code> triggers a <b>flush by size</b>, otherwise every <code>writeInterval</code> triggers a <b>flush by time</b>, whichever comes first; at shutdown <code>flushAll(true)</code> drains everything losslessly. Batched INSERTs buy ClickHouse's high write throughput.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/services/ClickhouseWriter/index.ts</span><span class="ln">two triggers</span></div>
  <pre class="code"><span class="cm">// Trigger ①: on enqueue, flush this table once it has a full batch</span>
<span class="fn">addToQueue</span>(tableName, data) {
  <span class="kw">this</span>.queue[tableName].<span class="fn">push</span>({ createdAt: Date.now(), data });
  <span class="kw">if</span> (<span class="kw">this</span>.queue[tableName].length &gt;= <span class="kw">this</span>.batchSize)
    <span class="kw">this</span>.<span class="fn">flush</span>(tableName);          <span class="cm">// depart when full</span>
}
<span class="cm">// Trigger ②: a timer, flush all tables every writeInterval ms</span>
<span class="fn">setInterval</span>(() =&gt; <span class="kw">this</span>.<span class="fn">flushAll</span>(), <span class="kw">this</span>.writeInterval);   <span class="cm">// depart on time</span>

<span class="cm">// flush: take a batch from the queue, bulk INSERT (with backoff retry maxAttempts)</span>
<span class="kw">const</span> items = entityQueue.<span class="fn">splice</span>(0, fullQueue ? all : <span class="kw">this</span>.batchSize);
<span class="kw">await</span> <span class="fn">backOff</span>(() =&gt; <span class="fn">writeToClickhouse</span>({ table, records }), { numOfAttempts });</pre>
</div>

<p>Why does ClickHouse so dread "row-by-row writes"? Back to Lesson 8's storage mechanics: a MergeTree drops a new <strong>data part</strong> on disk for
every <code>INSERT</code>, then relies on background <strong>merges</strong> to combine small parts into large ones. INSERT each record separately and you
instantly spawn <strong>a flood of tiny parts</strong> — exploding disk metadata, background merges that never catch up, slowed queries (and even ClickHouse's
"too many parts" guard rejecting writes). Batch ten thousand records into one INSERT and you create just <strong>one</strong> big part — easy to write,
merge, and query. So this layer isn't an optional optimization; it's a <strong>precondition</strong> for a columnar store like ClickHouse to withstand
high-frequency ingestion — without this buffer, even the best table design gets crushed by a deluge of small writes.</p>
""")

_EN17.append(r"""
<h2>Two departure conditions, plus a graceful drain</h2>
<p>"Full" and "on time" each serve a different load, and both are needed:</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="at rush hour flush on batchSize when full, in a lull flush on writeInterval when due, on shutdown flushAll drains all queues">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Whichever first: balancing throughput and latency</text>
  <text x="20" y="58" font-size="9" font-weight="700" fill="var(--accent-ink)">rush hour</text>
  <rect x="20" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="44" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="68" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="92" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/><rect x="116" y="66" width="20" height="22" rx="3" fill="var(--accent-soft)" stroke="var(--accent)"/>
  <text x="150" y="81" font-size="8.5" fill="var(--ink)">▶ fills batchSize instantly</text>
  <rect x="300" y="64" width="120" height="26" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="81" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① flush now (by size)</text>
  <text x="448" y="81" font-size="8" fill="var(--muted)">low latency, full batches, max throughput</text>
  <text x="20" y="118" font-size="9" font-weight="700" fill="var(--blue)">lull</text>
  <rect x="20" y="126" width="20" height="22" rx="3" fill="var(--blue-soft)" stroke="var(--blue)"/><rect x="44" y="126" width="20" height="22" rx="3" fill="var(--blue-soft)" stroke="var(--blue)"/>
  <text x="80" y="141" font-size="8.5" fill="var(--ink)">▶ only two in ages, never fills</text>
  <rect x="300" y="124" width="120" height="26" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="141" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② flush on time</text>
  <text x="448" y="141" font-size="8" fill="var(--muted)">flush every writeInterval, no waiting forever</text>
  <text x="20" y="178" font-size="9" font-weight="700" fill="var(--amber)">on shutdown</text>
  <rect x="300" y="166" width="120" height="26" rx="6" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="360" y="183" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">flushAll(true) drain</text>
  <text x="448" y="183" font-size="8" fill="var(--muted)">clear timer + write out every queue, no loss</text>
</svg>
<div class="figcap"><b>Complementary conditions + graceful shutdown</b>: rush hour leans on <code>batchSize</code> for throughput, lulls on <code>writeInterval</code> to cap latency; <code>shutdown</code> first <code>clearInterval</code> then <code>flushAll(true)</code> writes out everything left in memory. <code>flushAll</code> fans out across tables with <code>Promise.all</code>.</div>
</div>

<table class="t">
  <tr><th>trigger</th><th>condition</th><th>what it solves</th></tr>
  <tr><td><b>① by size (batchSize)</b></td><td>a table's queue length ≥ <code>batchSize</code></td><td>at high throughput, write full batches, maxing ClickHouse write efficiency</td></tr>
  <tr><td><b>② by time (writeInterval)</b></td><td>the timer fires <code>flushAll</code> every <code>writeInterval</code> ms</td><td>at low throughput, caps latency so data doesn't linger in memory indefinitely</td></tr>
  <tr><td><b>③ shutdown drain</b></td><td><code>shutdown()</code> calls <code>flushAll(true)</code></td><td>persist all buffers before the process exits, avoiding data loss</td></tr>
</table>

<p>The two parameters <code>batchSize</code> and <code>writeInterval</code> are really a pair of <strong>throughput / latency knobs</strong>: a bigger
batchSize and longer interval mean larger batches and cheaper writes, but a longer delay from "computed" to "queryable" for each record; the reverse means
lower latency but more fragmented writes. Langfuse makes them <strong>environment variables</strong> so you can tune them to your traffic and freshness
needs without touching code.</p>

<p>Unpack a merged record's journey through the writer, and it's exactly five steps:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>enqueue</h4><p><code>addToQueue(table, record)</code> pushes the record, with a <code>createdAt</code> timestamp, onto that table's queue tail.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>wait to depart</h4><p>The record waits in the in-memory queue. Meanwhile the system records <strong>how long it waited</strong> (a wait_time metric) to observe backlog.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>trigger flush</h4><p>This table hits <code>batchSize</code> (by size) or the timer fires (by time); <code>splice</code> takes up to a batch.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>bulk write</h4><p><code>writeToClickhouse</code> INSERTs the whole batch as <code>JSONEachRow</code> in one go; with <code>backOff</code> retry.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>success / retry</h4><p>On success the batch is done; retryable errors back off and retry, oversized batches split and requeue — sparing the rest of the batch.</p></div></div>
</div>
""")

_EN17.append(r"""
<h2>Why a singleton, and why dare to buffer in memory</h2>
<p><code>ClickhouseWriter</code> is a <strong>singleton</strong> (private constructor + <code>getInstance</code>): one writer, one set of queues per worker
process. That's crucial — only by converging to one place can scattered records from countless jobs <strong>actually batch up large</strong>; if each job
wrote on its own, batches would never grow. Writes carry <strong>backoff retry</strong> (<code>maxAttempts</code>): retryable errors back off and retry,
"string too long" errors <strong>split the batch</strong> and retry — chasing big batches without letting one bad record drag down the whole batch. This
"<strong>the batch rises and falls together, the bad ones get pulled out alone</strong>" strategy echoes Lesson 12's ingestion-API "partial success": at
every layer the system tries to be <strong>fault-tolerant without collateral damage</strong>, so a problem record or two won't block the whole pipeline.</p>

<svg viewBox="0 0 720 250" role="img" aria-label="The ClickhouseWriter in-memory buffer is volatile and a crash drops that batch; but the S3 event ledger never loses data and the queue job is not acked until the write succeeds, so when the worker crashes mid-way the job is redelivered, re-read from S3, re-merged and re-written, losing nothing; durability is handled upstream so this layer dares to trade a volatile buffer for write throughput">
  <rect x="0" y="0" width="720" height="250" fill="var(--bg)"></rect>
  <rect x="18" y="44" width="210" height="52" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="123" y="68" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">S3 · event ledger</text>
  <text x="123" y="86" font-size="10" text-anchor="middle" fill="var(--muted)">never loses · durable</text>
  <rect x="18" y="120" width="210" height="52" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="123" y="144" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">queue job</text>
  <text x="123" y="162" font-size="10" text-anchor="middle" fill="var(--muted)">not acked until write ok</text>
  <line x1="228" y1="70" x2="268" y2="100" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="228" y1="146" x2="268" y2="130" stroke="var(--faint)" stroke-width="1.5"></line>
  <rect x="268" y="72" width="190" height="92" rx="10" fill="var(--amber-soft)" stroke="var(--accent)" stroke-dasharray="5 3"></rect>
  <text x="363" y="96" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">ClickhouseWriter</text>
  <text x="363" y="114" font-size="10.5" text-anchor="middle" fill="var(--muted)">memory buffer (volatile · batches)</text>
  <text x="363" y="140" font-size="10.5" text-anchor="middle" fill="var(--ink)">⚡ crash → batch lost</text>
  <line x1="458" y1="118" x2="500" y2="118" stroke="var(--teal)" stroke-width="2"></line>
  <rect x="500" y="84" width="200" height="68" rx="10" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="600" y="112" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">ClickHouse final row</text>
  <text x="600" y="132" font-size="10.5" text-anchor="middle" fill="var(--ink)">nothing lost</text>
  <line x1="363" y1="164" x2="363" y2="196" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="363" y1="196" x2="123" y2="196" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <line x1="123" y1="196" x2="123" y2="172" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="243" y="214" font-size="10" text-anchor="middle" fill="var(--muted)">crash ⇒ redeliver: re-read S3 → re-merge → re-write</text>
  <text x="360" y="236" font-size="11" text-anchor="middle" fill="var(--muted)">durability handled by S3 + queue, so this layer dares to trade a volatile buffer for write throughput</text>
</svg>

<div class="cols">
  <div class="col"><h4>🧩 singleton + per-table queues</h4><p>One writer per process gathers all jobs' records into big batches; per-table queues let traces/observations/scores each fill and flush in parallel, never blocking each other.</p></div>
  <div class="col"><h4>🛡️ bulk write + backoff retry</h4><p>One INSERT per whole batch (<code>JSONEachRow</code>); failures retry with <code>maxAttempts</code> backoff; oversized batches auto-split. "Fast" and "stable" together.</p></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Records sit in an in-memory queue — if the worker suddenly crashes, isn't the batch lost?</strong> It is — but that <strong>doesn't matter</strong>,
  because the real "ledger" isn't here. Recall Lesson 14: every event <strong>rests verbatim in S3</strong>, and the queue job <strong>isn't acked</strong>
  until the DB write succeeds. So a mid-flight worker crash, at worst, means this batch of merged results didn't land; the corresponding queue job is
  <strong>redelivered</strong>, re-reads events from S3, re-merges and re-writes — <strong>not a single record lost</strong>. Precisely because
  <strong>durability is already backstopped by upstream S3 + the queue</strong>, this layer can <strong>safely trade volatile in-memory buffering for write
  throughput</strong>. A classic layered-design insight: <strong>assign durability and efficiency to different layers, each taken to the extreme</strong> —
  S3 owns "never lose", ClickhouseWriter owns "write fast", neither compromising for the other's goal.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><code>ClickhouseWriter</code> is a <strong>singleton</strong> that gathers high-frequency single records into <strong>big batches</strong> for one <code>INSERT</code> — because Lesson 8's ClickHouse prefers large batches and dreads row-by-row.</li>
    <li><strong>One in-memory queue per table</strong> (traces/observations/scores…); <code>addToQueue</code> feeds it, <code>flushAll</code> fans out across tables with <code>Promise.all</code>.</li>
    <li><strong>Two flush triggers</strong>: ① queue ≥ <code>batchSize</code> (by size, for throughput) ② every <code>writeInterval</code> timer (by time, capping latency); whichever first.</li>
    <li><code>shutdown</code> clears the timer then <code>flushAll(true)</code> <strong>drains</strong> all queues so nothing is lost on exit; writes carry backoff retry, oversized batches auto-split.</li>
    <li>It <strong>dares to trade volatile memory buffering for throughput</strong> because <strong>durability is backstopped by upstream S3 + the queue</strong> (Lesson 14): crash → redeliver and recompute, nothing lost — layers each doing their job.</li>
  </ul>
</div>
""")
LESSON_17 = {"zh": "\n".join(_ZH17), "en": "\n".join(_EN17)}


# ══════════════════════════════════════════════════════════════════════
# L18 · OpenTelemetry 摄取 / OpenTelemetry ingestion
# ══════════════════════════════════════════════════════════════════════
_ZH18 = []
_EN18 = []

_ZH18.append(r"""
<p class="lead">
前面六课讲的都是 Langfuse 的<strong>原生摄取</strong>——你用它自己的 SDK、按它自己的事件 schema 上报。可现实里，很多团队早已用
<strong>OpenTelemetry</strong>（业界可观测性标准）埋好了点。这一课讲 Langfuse 怎么<strong>张开双臂接住 OTLP</strong>：把五花八门的 OpenTelemetry span
<strong>映射</strong>成自己的 observation 模型。关键洞察是——OTel 摄取本质是一个<strong>万能适配器</strong>：前端把各种约定翻译过来，翻译完<strong>汇入和原生完全相同</strong>的合并/算钱/落盘管道。
</p>

<div class="card analogy">
  <div class="tag">🔌 生活类比</div>
  把 OTel 端点想成一个<strong>万能转换插头</strong>。你的设备（应用）来自世界各地，插头标准各不相同——有的是 OpenTelemetry 的 <code>gen_ai.*</code> 约定、
  有的是 Vercel AI SDK 的 <code>ai.*</code>、有的是 OpenLLMetry 的 <code>llm.*</code>。万能适配器<strong>每个标准都认</strong>：它挨个去试「这个字段在你那套约定里叫什么」，
  一旦认出来，就把电流接进<strong>同一个插座</strong>（Langfuse 的 observation 模型）。插座后面的电路（合并、算成本、写库）<strong>只有一套</strong>——
  适配器只负责「把各种插头转成统一接口」，转完之后，谁来的都一样走。
</div>
""")

# (L18 sections appended below)

_ZH18.append(r"""
<h2>OTLP 的一条路：解析 → 落 S3 → 专用队列 → 适配器</h2>
<p>OTLP 数据从 <code>POST /api/public/otel/v1/traces</code> 进来。这个端点和第 12 课的原生入口<strong>性格一致</strong>——也是「鉴权 + 解析 + 入队，立即返回」，
只是解析的是 OpenTelemetry 的 span 格式（支持 protobuf 和 JSON 两种编码、支持 gzip）。解析出 <code>resourceSpans</code> 后，走的还是第 14 课那套<strong>S3 存本体 + 队列递指针</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="OTLP span 从 otel/v1/traces 进入，解析后上传 S3、入 OtelIngestionQueue，worker 用 OtelIngestionProcessor 映射成 observation，汇入与原生相同的合并写库管道">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">OTLP 摄取：前端适配，后端归一</text>
  <rect x="12" y="44" width="116" height="52" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="70" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">应用 + OTel SDK</text><text x="70" y="80" text-anchor="middle" font-size="7.5" fill="var(--muted)">POST otel/v1/traces</text>
  <rect x="158" y="44" width="120" height="52" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="218" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">端点解析</text><text x="218" y="77" text-anchor="middle" font-size="7" fill="var(--accent-ink)">protobuf/JSON·gzip</text><text x="218" y="89" text-anchor="middle" font-size="7" fill="var(--accent-ink)">→ resourceSpans</text>
  <rect x="308" y="20" width="120" height="38" rx="8" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="368" y="38" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--amber)">S3：span 本体</text><text x="368" y="51" text-anchor="middle" font-size="7" fill="var(--muted)">otel/&lt;proj&gt;/…json</text>
  <rect x="308" y="78" width="120" height="38" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="368" y="96" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">OtelIngestionQueue</text><text x="368" y="109" text-anchor="middle" font-size="7" fill="var(--accent-ink)">指针 fileKey（+ 次队列）</text>
  <rect x="458" y="44" width="130" height="52" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="523" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">OtelIngestion</text><text x="523" y="74" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">Processor</text><text x="523" y="88" text-anchor="middle" font-size="7" fill="var(--muted)">span→ingestion 事件</text>
  <rect x="610" y="44" width="100" height="52" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="660" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">同一管道</text><text x="660" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">第 15–17 课</text><text x="660" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">合并·算钱·写库</text>
  <line x1="128" y1="70" x2="156" y2="70" stroke="var(--faint)" stroke-width="1.5"/><polygon points="156,70 148,66 148,74" fill="var(--faint)"/>
  <line x1="278" y1="62" x2="306" y2="42" stroke="var(--amber)" stroke-width="1.4"/><line x1="278" y1="78" x2="306" y2="94" stroke="var(--accent)" stroke-width="1.4"/>
  <line x1="428" y1="96" x2="456" y2="78" stroke="var(--faint)" stroke-width="1.4"/><polygon points="456,78 447,77 450,86" fill="var(--faint)"/>
  <line x1="588" y1="70" x2="608" y2="70" stroke="var(--faint)" stroke-width="1.5"/><polygon points="608,70 600,66 600,74" fill="var(--faint)"/>
  <text x="360" y="135" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">OTel 特异的只有「映射」这一段 ▲；其后与原生摄取共用一套后端</text>
  <rect x="150" y="156" width="420" height="54" rx="9" fill="none" stroke="var(--teal)" stroke-dasharray="5 4"/><text x="360" y="176" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">processToIngestionEvents → IngestionEventType[]（第 13 课的事件格式）</text><text x="360" y="195" text-anchor="middle" font-size="8" fill="var(--muted)">observation → IngestionService.mergeAndWrite；trace → processEventBatch</text>
</svg>
<div class="figcap"><b>边缘适配、核心归一</b>：端点解析 OTLP（protobuf/JSON）→ span 本体落 S3、指针入 <code>OtelIngestionQueue</code>（+次队列）→ worker 用 <code>OtelIngestionProcessor</code> 把 span 翻译成<strong>原生 ingestion 事件</strong>，再走第 15–17 课同一条合并/算钱/落盘管道。源码：<code>web/.../otel/v1/traces/index.ts</code>、<code>OtelIngestionProcessor.ts</code>、<code>worker/.../otelIngestionQueue.ts</code>。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="OpenTelemetry 摄取真实例子：一个 OTLP span 的语义属性 gen_ai.request.model、gen_ai.usage.*、name、operation.name 逐行映射到 observation 的 model、usageDetails、name、type。属性名对齐 server/otel/ObservationTypeMapper.ts，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：一个 OTLP span 映射成 observation</text>
  <rect x="20" y="34" width="300" height="186" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="32" y="52" font-size="9" font-weight="700" fill="var(--blue)">OTLP span（标准遥测）</text>
  <text x="32" y="72" font-size="7.5" font-family="monospace" fill="var(--ink)">name: &quot;chat completion&quot;</text>
  <text x="32" y="88" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.operation.name: &quot;chat&quot;</text>
  <text x="32" y="104" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.request.model: &quot;gpt-4o&quot;</text>
  <text x="32" y="120" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.usage.input_tokens: 512</text>
  <text x="32" y="136" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.usage.output_tokens: 88</text>
  <text x="32" y="152" font-size="7.5" font-family="monospace" fill="var(--ink)">startTimeUnixNano: …</text>
  <text x="32" y="168" font-size="7.5" font-family="monospace" fill="var(--ink)">endTimeUnixNano: …</text>
  <text x="32" y="200" font-size="7" fill="var(--muted)">任意 OTel SDK 都能发</text>
  <g font-size="7" fill="var(--accent)"><line x1="324" y1="94" x2="392" y2="74" stroke="var(--accent)" stroke-width="1.2"/><polygon points="392,74 383,73 385,81" fill="var(--accent)"/><line x1="324" y1="104" x2="392" y2="106" stroke="var(--accent)" stroke-width="1.2"/><polygon points="392,106 383,102 384,110" fill="var(--accent)"/><line x1="324" y1="128" x2="392" y2="138" stroke="var(--accent)" stroke-width="1.2"/><polygon points="392,138 383,134 384,142" fill="var(--accent)"/></g>
  <rect x="396" y="34" width="304" height="186" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="408" y="52" font-size="9" font-weight="700" fill="var(--accent-ink)">Langfuse observation</text>
  <text x="408" y="74" font-size="7.5" font-family="monospace" fill="var(--ink)">type: GENERATION  ← operation.name</text>
  <text x="408" y="92" font-size="7.5" font-family="monospace" fill="var(--ink)">name: &quot;chat completion&quot;</text>
  <text x="408" y="110" font-size="7.5" font-family="monospace" fill="var(--ink)">model: &quot;gpt-4o&quot;  ← request.model</text>
  <text x="408" y="128" font-size="7.5" font-family="monospace" fill="var(--ink)">usageDetails:</text>
  <text x="408" y="142" font-size="7.5" font-family="monospace" fill="var(--ink)">  {input:512, output:88}</text>
  <text x="408" y="160" font-size="7.5" font-family="monospace" fill="var(--ink)">startTime/endTime ← UnixNano</text>
  <text x="408" y="200" font-size="7" font-weight="700" fill="var(--accent-ink)">无需改 SDK，OTel 直接进来</text>
</svg>
<div class="figcap"><b>OTel 是第二条入口</b>（属性名对齐 <code>packages/shared/src/server/otel/ObservationTypeMapper.ts</code>；<b>值为示例</b>）：你用任意 OpenTelemetry SDK 发出的 span，其 <code>gen_ai.*</code> 语义属性被<b>逐字段映射</b>成 observation——<code>gen_ai.request.model</code>→<code>model</code>、<code>gen_ai.usage.*</code>→<code>usageDetails</code>、<code>operation.name</code>→<code>type</code>。于是不改埋点也能接入 Langfuse。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/public/otel/v1/traces/index.ts &amp; OtelIngestionProcessor.ts</span><span class="ln">端点+发布</span></div>
  <pre class="code"><span class="cm">// 端点：按 content-type 解析 OTLP（protobuf 或 JSON），取出 resourceSpans</span>
<span class="kw">const</span> resourceSpans = contentType.<span class="fn">includes</span>(<span class="st">"x-protobuf"</span>)
  ? ExportTraceServiceRequest.<span class="fn">decode</span>(body).resourceSpans
  : JSON.<span class="fn">parse</span>(body).resourceSpans;
<span class="kw">return</span> <span class="kw">await</span> processor.<span class="fn">publishToOtelIngestionQueue</span>(resourceSpans);

<span class="cm">// publishToOtelIngestionQueue：本体落 S3，指针入专用队列（同第 14 课模式）</span>
<span class="kw">const</span> fileKey = <span class="st">`…otel/${projectId}/…/${randomUUID()}.json`</span>;
<span class="kw">await</span> <span class="fn">getS3EventStorageClient</span>(bucket).<span class="fn">uploadJson</span>(fileKey, resourceSpans);
OtelIngestionQueue.<span class="fn">getInstance</span>({ shardingKey: <span class="st">`${projectId}-${fileKey}`</span> })
  .<span class="fn">add</span>(QueueJobs.OtelIngestionJob, { payload: { data: { fileKey } } });</pre>
</div>
""")

# (mapping section below)

_ZH18.append(r"""
<h2>万能适配器：一个字段，试遍各种约定</h2>
<p>映射的核心难点在于：同一个语义（比如「这次调用用了哪个模型」），不同的埋点库会写进<strong>不同的 span 属性键</strong>。<code>OtelIngestionProcessor</code> 的办法是
为每个字段准备一份<strong>优先级列表</strong>，<strong>从上往下试</strong>，第一个有值的就采用。以提取模型名为例：</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="extractModelName 按优先级依次尝试多套约定的 span 属性键，第一个有值的即作为模型名映射到 observation">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">extractModelName：按优先级试遍各家约定</text>
  <rect x="20" y="40" width="250" height="22" rx="5" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="32" y="55" font-size="8.5" fill="var(--accent-ink)">① langfuse.observation.model（原生）</text>
  <rect x="20" y="66" width="250" height="22" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="32" y="81" font-size="8.5" fill="var(--ink)">② gen_ai.response.model（OTel 标准）</text>
  <rect x="20" y="92" width="250" height="22" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="32" y="107" font-size="8.5" fill="var(--ink)">③ ai.model.id（Vercel AI SDK）</text>
  <rect x="20" y="118" width="250" height="22" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="32" y="133" font-size="8.5" fill="var(--ink)">④ gen_ai.request.model</text>
  <rect x="20" y="144" width="250" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="32" y="159" font-size="8.5" fill="var(--muted)">⑤ llm.response.model / llm.model_name</text>
  <rect x="20" y="170" width="250" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="32" y="185" font-size="8.5" fill="var(--muted)">⑥ model（兜底通用键）</text>
  <text x="290" y="112" font-size="13" fill="var(--faint)">▶</text>
  <rect x="330" y="80" width="180" height="64" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="420" y="104" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">第一个有值的</text><text x="420" y="122" text-anchor="middle" font-size="8" fill="var(--accent-ink)">→ observation.model</text>
  <text x="540" y="116" font-size="13" fill="var(--faint)">▶</text>
  <rect x="566" y="80" width="140" height="64" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="636" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">进 provided_*</text><text x="636" y="116" text-anchor="middle" font-size="7.5" fill="var(--muted)">交第 16 课</text><text x="636" y="128" text-anchor="middle" font-size="7.5" fill="var(--muted)">匹配价格/算钱</text>
  <text x="360" y="210" text-anchor="middle" font-size="8.5" fill="var(--faint)">usage、input/output、observation 类型……每个字段都有这样一份「试遍各家」的优先级列表</text>
</svg>
<div class="figcap"><b>优先级回退，认遍各家约定</b>：<code>extractModelName</code> 依次尝试 Langfuse 原生 → OTel <code>gen_ai.*</code> → Vercel <code>ai.*</code> → OpenLLMetry <code>llm.*</code> → 通用 <code>model</code>，第一个命中的即为模型名。usage/input/output 同理。提取出的 usage 进 <code>provided_usage_details</code>，再走第 16 课。源码：<code>OtelIngestionProcessor.ts:2232-2257</code>。</div>
</div>

<table class="t">
  <tr><th>Langfuse 字段</th><th>依次尝试的 span 属性键（节选）</th><th>来自哪套约定</th></tr>
  <tr><td><b>模型名</b></td><td><code>gen_ai.response.model</code> · <code>ai.model.id</code> · <code>gen_ai.request.model</code> · <code>llm.model_name</code> · <code>model</code></td><td>OTel GenAI · Vercel · OpenLLMetry · 通用</td></tr>
  <tr><td><b>usage（token）</b></td><td>Langfuse <code>observation.usage_details</code> · gen_ai 的 token 计数 · Genkit 输出…</td><td>原生 · OTel · Genkit</td></tr>
  <tr><td><b>input / output</b></td><td>span 属性 + span <strong>事件</strong>（<code>gen_ai.user.message</code>、<code>gen_ai.choice</code>）</td><td>OTel GenAI 语义约定</td></tr>
  <tr><td><b>observation 类型</b></td><td><code>observationTypeMapper</code> 据属性判定 GENERATION / SPAN / …</td><td>映射器规则</td></tr>
</table>

<p>举个具体的：一段用 OpenLLMetry 埋点的 OpenAI 调用，会产生一个带这些属性的 span——<code>gen_ai.request.model="gpt-4o"</code>、
若干 token 计数属性，外加两条 span <strong>事件</strong> <code>gen_ai.user.message</code>（用户输入）和 <code>gen_ai.choice</code>（模型输出）。适配器一一对上：
模型名从 <code>gen_ai.request.model</code> 取到、usage 从 token 属性取到、input/output 从那两条事件取到、类型被判成 <strong>GENERATION</strong>。
于是这个原本「OTel 味」的 span，就变成了一条结构完整、和你用 Langfuse SDK 上报<strong>别无二致</strong>的 generation observation。
特别值得一提的是 input/output：它们常常不在 span 的属性里，而藏在 span 的<strong>事件</strong>流中——适配器必须连 span events 也一并翻译，才能把整段对话完整还原出来。</p>
""")

# (convergence + spark + key below)

_ZH18.append(r"""
<h2>映射完，殊途同归</h2>
<p>worker 端的 <code>OtelIngestionProcessor.processToIngestionEvents</code> 把一批 span 翻译成 <code>IngestionEventType[]</code>——
<strong>正是第 13 课那套原生事件格式</strong>。接着它把结果一分为二：<strong>observation</strong> 类直接交给 <code>IngestionService.mergeAndWrite</code>（第 15 课），
<strong>trace</strong> 等非 observation 再走一遍 <code>processEventBatch</code>（第 12 课）。从这里开始，OTel 来的数据和原生 SDK 来的数据<strong>再无分别</strong>：
同样的合并、同样的算 token/成本、同样的批量落盘。</p>

<svg viewBox="0 0 720 240" role="img" aria-label="原生 SDK 摄取走精确通道、OTel span 经适配器翻译走兼容通道，两条路都产出第 13 课的原生 IngestionEventType 数组，从此汇入同一后端：mergeAndWrite 合并、算 token 与成本、ClickhouseWriter 批量落盘，OTel 与原生再无分别">
  <rect x="0" y="0" width="720" height="240" fill="var(--bg)"></rect>
  <rect x="16" y="44" width="180" height="52" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="106" y="68" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">原生 SDK 摄取</text>
  <text x="106" y="86" font-size="10" text-anchor="middle" fill="var(--muted)">精确通道（L12–13）</text>
  <rect x="16" y="152" width="150" height="52" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="91" y="176" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">OTel span</text>
  <text x="91" y="194" font-size="10" text-anchor="middle" fill="var(--muted)">兼容通道（本课）</text>
  <rect x="186" y="152" width="170" height="52" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="271" y="176" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">适配器翻译</text>
  <text x="271" y="194" font-size="9.5" text-anchor="middle" fill="var(--muted)">processToIngestionEvents</text>
  <rect x="300" y="84" width="180" height="72" rx="10" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="390" y="114" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">IngestionEventType[]</text>
  <text x="390" y="134" font-size="10" text-anchor="middle" fill="var(--muted)">L13 原生事件格式</text>
  <line x1="196" y1="70" x2="300" y2="104" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="356" y1="178" x2="390" y2="156" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="512" y="84" width="192" height="84" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="608" y="108" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">殊途同归 · 同一后端</text>
  <text x="608" y="128" font-size="9.5" text-anchor="middle" fill="var(--muted)">mergeAndWrite · 算 token/成本</text>
  <text x="608" y="146" font-size="9.5" text-anchor="middle" fill="var(--muted)">ClickhouseWriter 批写（L15–17）</text>
  <line x1="480" y1="120" x2="512" y2="126" stroke="var(--teal)" stroke-width="2"></line>
  <text x="360" y="224" font-size="11" text-anchor="middle" fill="var(--muted)">从这一步起，OTel 与原生 SDK 再无分别——同样合并、同样算成本、同样批量落盘</text>
</svg>

<div class="cols">
  <div class="col"><h4>🟦 原生摄取（第 12–13 课）</h4><p>你用 Langfuse SDK，<strong>直接说它的母语</strong>——事件就是它定义的 schema，字段精确、无需猜测。这是「精确通道」。</p></div>
  <div class="col"><h4>🔌 OTel 摄取（本课）</h4><p>你用 OpenTelemetry，<strong>需要翻译</strong>——适配器从异构约定里<strong>尽力推断</strong>字段。灵活但有语义损耗，是「兼容通道」。两者最终汇入同一后端。</p></div>
</div>

<p>把 worker 端 OTel 任务的处理拆开，就能看清「翻译完汇入主管道」这件事是怎么发生的：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>取下 OTel 任务</h4><p>worker 从 <code>OtelIngestionQueue</code> 拿到任务，照 <code>fileKey</code> 去 S3 下载这批 span 本体。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>解析 span</h4><p>把 S3 里的 resourceSpans 解析成结构化的 span 列表，准备喂给适配器。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>适配器翻译</h4><p><code>processToIngestionEvents(spans)</code> 用优先级属性键把每个 span 映射成<strong>原生 ingestion 事件</strong>（第 13 课格式）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>分流</h4><p>按实体类型一分为二：<strong>observation</strong> 直接交 <code>IngestionService</code>，<strong>trace</strong> 走 <code>processEventBatch</code>。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>汇入主管道</h4><p>从这步起，OTel 与原生<strong>共用</strong>第 15–17 课：合并、算 token/成本、<code>ClickhouseWriter</code> 批量落盘。</p></div></div>
</div>

<p>正因为映射是「尽力推断」，OTel 通道天然存在<strong>语义落差</strong>：某些埋点库没写、或用了适配器还不认的属性键，对应字段就可能缺失。
这也是为什么模型名要试六七个键、usage 还要去翻 span 事件——<strong>适配器认得越多，落差越小</strong>。但无论怎么补，OTel 的「推断」终究不如原生的「明说」精确——
这是拥抱开放标准必然付出的代价。好在这套适配器是<strong>持续演进</strong>的：每当社区冒出一种新的埋点约定，只要往优先级列表里<strong>再加几个属性键</strong>，
老数据不受影响、新数据立刻被认得。这种「<strong>加键即兼容</strong>」的扩展方式，让 Langfuse 能跟着 OpenTelemetry GenAI 生态一起成长，而不必每次都大改一遍映射逻辑。</p>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>既然原生通道更精确，为什么还要费力支持 OpenTelemetry？</strong> 因为<strong>要去用户所在的地方接住他们</strong>。OpenTelemetry 是可观测性的事实标准，
  无数团队的应用早已用它埋好了点。如果 Langfuse 只认自己的 SDK，就等于要求用户<strong>为了它重新埋一遍点</strong>——这个门槛会劝退一大批人。
  支持 OTLP，意味着「你<strong>不用改一行埋点</strong>，把 OTel 数据指过来就能用」。代价确实存在：一个要不断追各家约定、满是优先级回退的<strong>适配器</strong>，
  以及推断带来的语义损耗。但这笔账算得过来——因为适配器只在<strong>最前端</strong>，翻译完就汇入和原生<strong>共享的核心</strong>（合并、算钱、落盘只有一套）。
  <strong>把脏活、特例都收敛到边缘的一层适配器，让核心保持纯净统一</strong>——这正是「适配器模式」最经典的用法。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>Langfuse 提供 <strong>OTLP 端点</strong>（<code>/api/public/otel/v1/traces</code>），接收 OpenTelemetry span（protobuf/JSON、支持 gzip），让你<strong>无需改埋点</strong>即可接入。</li>
    <li>OTLP 走和第 14 课<strong>相同的 S3 + 队列</strong>模式：span 本体落 S3，指针入<strong>专用</strong> <code>OtelIngestionQueue</code>（含主/次）。</li>
    <li><code>OtelIngestionProcessor</code> 是<strong>万能适配器</strong>：每个字段备一份<strong>优先级属性键列表</strong>，试遍 OTel <code>gen_ai.*</code>、Vercel <code>ai.*</code>、OpenLLMetry <code>llm.*</code> 等约定，第一个有值的即采用。</li>
    <li>映射产出<strong>原生 ingestion 事件</strong>（第 13 课格式），observation 入 <code>IngestionService</code>、trace 入 <code>processEventBatch</code>——之后与原生<strong>完全同路</strong>。</li>
    <li>取舍：OTel 是「兼容通道」，靠推断、有语义落差；原生是「精确通道」。<strong>把适配特例收敛到边缘，核心保持统一</strong>——经典适配器模式。</li>
  </ul>
</div>
""")

_EN18.append(r"""
<p class="lead">
The last six lessons covered Langfuse's <strong>native ingestion</strong> — you use its own SDK, report in its own event schema. But in reality, many teams
already instrument with <strong>OpenTelemetry</strong> (the industry observability standard). This lesson covers how Langfuse <strong>opens its arms to
OTLP</strong>: mapping the motley assortment of OpenTelemetry spans onto its own observation model. The key insight — OTel ingestion is essentially a
<strong>universal adapter</strong>: the front end translates the various conventions, and once translated, it <strong>flows into the exact same</strong>
merge / cost / persist pipeline as native.
</p>

<div class="card analogy">
  <div class="tag">🔌 Analogy</div>
  Think of the OTel endpoint as a <strong>universal travel adapter</strong>. Your devices (apps) come from all over, with different plug standards — some
  OpenTelemetry's <code>gen_ai.*</code> convention, some Vercel AI SDK's <code>ai.*</code>, some OpenLLMetry's <code>llm.*</code>. The universal adapter
  <strong>recognizes them all</strong>: it tries, one by one, "what's this field called in your convention", and once it recognizes it, routes the current
  into the <strong>same socket</strong> (Langfuse's observation model). The circuitry behind the socket (merge, cost, write) is <strong>just one</strong> —
  the adapter only "turns various plugs into one interface"; after that, everyone flows the same way.
</div>
""")

_EN18.append(r"""
<h2>OTLP's path: parse → land in S3 → dedicated queue → adapter</h2>
<p>OTLP data arrives at <code>POST /api/public/otel/v1/traces</code>. This endpoint shares Lesson 12's native-entry <strong>character</strong> — also "auth +
parse + enqueue, return immediately" — only it parses the OpenTelemetry span format (both protobuf and JSON encodings, plus gzip). After parsing out
<code>resourceSpans</code>, it follows the same <strong>S3-stores-body + queue-passes-pointer</strong> pattern as Lesson 14:</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="OTLP spans arrive at otel/v1/traces, get parsed, uploaded to S3 and enqueued to OtelIngestionQueue; the worker maps spans to observations via OtelIngestionProcessor, converging into the same merge/write pipeline as native">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">OTLP ingestion: adapt at the edge, unify at the core</text>
  <rect x="12" y="44" width="116" height="52" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="70" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">app + OTel SDK</text><text x="70" y="80" text-anchor="middle" font-size="7.5" fill="var(--muted)">POST otel/v1/traces</text>
  <rect x="158" y="44" width="120" height="52" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="218" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">endpoint parse</text><text x="218" y="77" text-anchor="middle" font-size="7" fill="var(--accent-ink)">protobuf/JSON·gzip</text><text x="218" y="89" text-anchor="middle" font-size="7" fill="var(--accent-ink)">→ resourceSpans</text>
  <rect x="308" y="20" width="120" height="38" rx="8" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="368" y="38" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--amber)">S3: span body</text><text x="368" y="51" text-anchor="middle" font-size="7" fill="var(--muted)">otel/&lt;proj&gt;/…json</text>
  <rect x="308" y="78" width="120" height="38" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="368" y="96" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">OtelIngestionQueue</text><text x="368" y="109" text-anchor="middle" font-size="7" fill="var(--accent-ink)">pointer fileKey (+ secondary)</text>
  <rect x="458" y="44" width="130" height="52" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="523" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">OtelIngestion</text><text x="523" y="74" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">Processor</text><text x="523" y="88" text-anchor="middle" font-size="7" fill="var(--muted)">span→ingestion event</text>
  <rect x="610" y="44" width="100" height="52" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="660" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">same pipeline</text><text x="660" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">Lessons 15–17</text><text x="660" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">merge·cost·write</text>
  <line x1="128" y1="70" x2="156" y2="70" stroke="var(--faint)" stroke-width="1.5"/><polygon points="156,70 148,66 148,74" fill="var(--faint)"/>
  <line x1="278" y1="62" x2="306" y2="42" stroke="var(--amber)" stroke-width="1.4"/><line x1="278" y1="78" x2="306" y2="94" stroke="var(--accent)" stroke-width="1.4"/>
  <line x1="428" y1="96" x2="456" y2="78" stroke="var(--faint)" stroke-width="1.4"/><polygon points="456,78 447,77 450,86" fill="var(--faint)"/>
  <line x1="588" y1="70" x2="608" y2="70" stroke="var(--faint)" stroke-width="1.5"/><polygon points="608,70 600,66 600,74" fill="var(--faint)"/>
  <text x="360" y="135" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">Only the "mapping" stretch ▲ is OTel-specific; everything after is shared with native</text>
  <rect x="150" y="156" width="420" height="54" rx="9" fill="none" stroke="var(--teal)" stroke-dasharray="5 4"/><text x="360" y="176" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">processToIngestionEvents → IngestionEventType[] (Lesson 13's event format)</text><text x="360" y="195" text-anchor="middle" font-size="8" fill="var(--muted)">observation → IngestionService.mergeAndWrite; trace → processEventBatch</text>
</svg>
<div class="figcap"><b>Adapt at the edge, unify at the core</b>: the endpoint parses OTLP (protobuf/JSON) → span body to S3, pointer to <code>OtelIngestionQueue</code> (+ secondary) → the worker uses <code>OtelIngestionProcessor</code> to translate spans into <strong>native ingestion events</strong>, then runs the same Lesson 15–17 merge/cost/persist pipeline. Source: <code>web/.../otel/v1/traces/index.ts</code>, <code>OtelIngestionProcessor.ts</code>, <code>worker/.../otelIngestionQueue.ts</code>.</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="OpenTelemetry ingestion real example: an OTLP span's semantic attributes gen_ai.request.model, gen_ai.usage.*, name, operation.name map row-by-row to an observation's model, usageDetails, name, type. Attribute names per server/otel/ObservationTypeMapper.ts, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: an OTLP span mapped to an observation</text>
  <rect x="20" y="34" width="300" height="186" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="32" y="52" font-size="9" font-weight="700" fill="var(--blue)">OTLP span (standard telemetry)</text>
  <text x="32" y="72" font-size="7.5" font-family="monospace" fill="var(--ink)">name: &quot;chat completion&quot;</text>
  <text x="32" y="88" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.operation.name: &quot;chat&quot;</text>
  <text x="32" y="104" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.request.model: &quot;gpt-4o&quot;</text>
  <text x="32" y="120" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.usage.input_tokens: 512</text>
  <text x="32" y="136" font-size="7.5" font-family="monospace" fill="var(--ink)">gen_ai.usage.output_tokens: 88</text>
  <text x="32" y="152" font-size="7.5" font-family="monospace" fill="var(--ink)">startTimeUnixNano: …</text>
  <text x="32" y="168" font-size="7.5" font-family="monospace" fill="var(--ink)">endTimeUnixNano: …</text>
  <text x="32" y="200" font-size="7" fill="var(--muted)">any OTel SDK can send</text>
  <g font-size="7" fill="var(--accent)"><line x1="324" y1="94" x2="392" y2="74" stroke="var(--accent)" stroke-width="1.2"/><polygon points="392,74 383,73 385,81" fill="var(--accent)"/><line x1="324" y1="104" x2="392" y2="106" stroke="var(--accent)" stroke-width="1.2"/><polygon points="392,106 383,102 384,110" fill="var(--accent)"/><line x1="324" y1="128" x2="392" y2="138" stroke="var(--accent)" stroke-width="1.2"/><polygon points="392,138 383,134 384,142" fill="var(--accent)"/></g>
  <rect x="396" y="34" width="304" height="186" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="408" y="52" font-size="9" font-weight="700" fill="var(--accent-ink)">Langfuse observation</text>
  <text x="408" y="74" font-size="7.5" font-family="monospace" fill="var(--ink)">type: GENERATION  ← operation.name</text>
  <text x="408" y="92" font-size="7.5" font-family="monospace" fill="var(--ink)">name: &quot;chat completion&quot;</text>
  <text x="408" y="110" font-size="7.5" font-family="monospace" fill="var(--ink)">model: &quot;gpt-4o&quot;  ← request.model</text>
  <text x="408" y="128" font-size="7.5" font-family="monospace" fill="var(--ink)">usageDetails:</text>
  <text x="408" y="142" font-size="7.5" font-family="monospace" fill="var(--ink)">  {input:512, output:88}</text>
  <text x="408" y="160" font-size="7.5" font-family="monospace" fill="var(--ink)">startTime/endTime ← UnixNano</text>
  <text x="408" y="200" font-size="7" font-weight="700" fill="var(--accent-ink)">no SDK change; OTel comes straight in</text>
</svg>
<div class="figcap"><b>OTel is a second entry point</b> (attribute names per <code>packages/shared/src/server/otel/ObservationTypeMapper.ts</code>; <b>values illustrative</b>): a span from any OpenTelemetry SDK has its <code>gen_ai.*</code> semantic attributes <b>mapped field-by-field</b> into an observation — <code>gen_ai.request.model</code>→<code>model</code>, <code>gen_ai.usage.*</code>→<code>usageDetails</code>, <code>operation.name</code>→<code>type</code>. So you can feed Langfuse without changing your instrumentation.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/public/otel/v1/traces/index.ts &amp; OtelIngestionProcessor.ts</span><span class="ln">endpoint+publish</span></div>
  <pre class="code"><span class="cm">// endpoint: parse OTLP by content-type (protobuf or JSON), extract resourceSpans</span>
<span class="kw">const</span> resourceSpans = contentType.<span class="fn">includes</span>(<span class="st">"x-protobuf"</span>)
  ? ExportTraceServiceRequest.<span class="fn">decode</span>(body).resourceSpans
  : JSON.<span class="fn">parse</span>(body).resourceSpans;
<span class="kw">return</span> <span class="kw">await</span> processor.<span class="fn">publishToOtelIngestionQueue</span>(resourceSpans);

<span class="cm">// publishToOtelIngestionQueue: body to S3, pointer to the dedicated queue (Lesson 14 pattern)</span>
<span class="kw">const</span> fileKey = <span class="st">`…otel/${projectId}/…/${randomUUID()}.json`</span>;
<span class="kw">await</span> <span class="fn">getS3EventStorageClient</span>(bucket).<span class="fn">uploadJson</span>(fileKey, resourceSpans);
OtelIngestionQueue.<span class="fn">getInstance</span>({ shardingKey: <span class="st">`${projectId}-${fileKey}`</span> })
  .<span class="fn">add</span>(QueueJobs.OtelIngestionJob, { payload: { data: { fileKey } } });</pre>
</div>
""")

_EN18.append(r"""
<h2>The universal adapter: one field, try every convention</h2>
<p>The core difficulty of mapping: the same semantic (say "which model did this call use") gets written into <strong>different span attribute keys</strong>
by different instrumentation libraries. <code>OtelIngestionProcessor</code>'s approach is to keep a <strong>priority list</strong> per field and <strong>try top
to bottom</strong>, taking the first one with a value. Take extracting the model name:</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="extractModelName tries span attribute keys from multiple conventions in priority order, taking the first present one as the model name mapped to the observation">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">extractModelName: try each convention in priority order</text>
  <rect x="20" y="40" width="250" height="22" rx="5" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="32" y="55" font-size="8.5" fill="var(--accent-ink)">① langfuse.observation.model (native)</text>
  <rect x="20" y="66" width="250" height="22" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="32" y="81" font-size="8.5" fill="var(--ink)">② gen_ai.response.model (OTel standard)</text>
  <rect x="20" y="92" width="250" height="22" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="32" y="107" font-size="8.5" fill="var(--ink)">③ ai.model.id (Vercel AI SDK)</text>
  <rect x="20" y="118" width="250" height="22" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="32" y="133" font-size="8.5" fill="var(--ink)">④ gen_ai.request.model</text>
  <rect x="20" y="144" width="250" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="32" y="159" font-size="8.5" fill="var(--muted)">⑤ llm.response.model / llm.model_name</text>
  <rect x="20" y="170" width="250" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="32" y="185" font-size="8.5" fill="var(--muted)">⑥ model (generic fallback)</text>
  <text x="290" y="112" font-size="13" fill="var(--faint)">▶</text>
  <rect x="330" y="80" width="180" height="64" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="420" y="104" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">first one present</text><text x="420" y="122" text-anchor="middle" font-size="8" fill="var(--accent-ink)">→ observation.model</text>
  <text x="540" y="116" font-size="13" fill="var(--faint)">▶</text>
  <rect x="566" y="80" width="140" height="64" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="636" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">into provided_*</text><text x="636" y="116" text-anchor="middle" font-size="7.5" fill="var(--muted)">handed to Lesson 16</text><text x="636" y="128" text-anchor="middle" font-size="7.5" fill="var(--muted)">price/cost</text>
  <text x="360" y="210" text-anchor="middle" font-size="8.5" fill="var(--faint)">usage, input/output, observation type… each field has such a "try everyone" priority list</text>
</svg>
<div class="figcap"><b>Priority fallback, recognizing every convention</b>: <code>extractModelName</code> tries in turn Langfuse-native → OTel <code>gen_ai.*</code> → Vercel <code>ai.*</code> → OpenLLMetry <code>llm.*</code> → generic <code>model</code>, taking the first hit as the model name. usage/input/output likewise. The extracted usage goes into <code>provided_usage_details</code>, then Lesson 16. Source: <code>OtelIngestionProcessor.ts:2232-2257</code>.</div>
</div>

<table class="t">
  <tr><th>Langfuse field</th><th>span attribute keys tried in order (excerpt)</th><th>from which convention</th></tr>
  <tr><td><b>model name</b></td><td><code>gen_ai.response.model</code> · <code>ai.model.id</code> · <code>gen_ai.request.model</code> · <code>llm.model_name</code> · <code>model</code></td><td>OTel GenAI · Vercel · OpenLLMetry · generic</td></tr>
  <tr><td><b>usage (tokens)</b></td><td>Langfuse <code>observation.usage_details</code> · gen_ai token counts · Genkit output…</td><td>native · OTel · Genkit</td></tr>
  <tr><td><b>input / output</b></td><td>span attributes + span <strong>events</strong> (<code>gen_ai.user.message</code>, <code>gen_ai.choice</code>)</td><td>OTel GenAI semantic conventions</td></tr>
  <tr><td><b>observation type</b></td><td><code>observationTypeMapper</code> decides GENERATION / SPAN / … by attributes</td><td>mapper rules</td></tr>
</table>

<p>Concretely: an OpenAI call instrumented with OpenLLMetry produces a span with attributes like <code>gen_ai.request.model="gpt-4o"</code>, several token
counts, plus two span <strong>events</strong> <code>gen_ai.user.message</code> (the user input) and <code>gen_ai.choice</code> (the model output). The adapter
matches them one by one: model name from <code>gen_ai.request.model</code>, usage from the token attributes, input/output from those two events, type judged
as <strong>GENERATION</strong>. So that originally "OTel-flavored" span becomes a fully-structured generation observation, <strong>indistinguishable</strong>
from one reported via the Langfuse SDK. Note input/output especially: they often aren't in the span's attributes but hide in the span's <strong>event</strong>
stream — the adapter must translate span events too to fully reconstruct the conversation.</p>
""")

_EN18.append(r"""
<h2>Once mapped, all roads converge</h2>
<p>On the worker, <code>OtelIngestionProcessor.processToIngestionEvents</code> translates a batch of spans into <code>IngestionEventType[]</code> —
<strong>exactly Lesson 13's native event format</strong>. It then splits the result in two: <strong>observation</strong> kinds go straight to
<code>IngestionService.mergeAndWrite</code> (Lesson 15), <strong>trace</strong> and other non-observations run through <code>processEventBatch</code> (Lesson
12). From here on, OTel-sourced data and native-SDK data are <strong>indistinguishable</strong>: the same merge, the same token/cost calculation, the same
batched persistence.</p>

<svg viewBox="0 0 720 240" role="img" aria-label="native SDK ingestion takes the precise channel, OTel spans go through the adapter on the compatibility channel, both produce Lesson 13's native IngestionEventType array and from there converge into one backend: mergeAndWrite, token and cost calculation, ClickhouseWriter batched persistence, OTel and native become indistinguishable">
  <rect x="0" y="0" width="720" height="240" fill="var(--bg)"></rect>
  <rect x="16" y="44" width="180" height="52" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="106" y="68" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">native SDK ingestion</text>
  <text x="106" y="86" font-size="10" text-anchor="middle" fill="var(--muted)">precise channel (L12–13)</text>
  <rect x="16" y="152" width="150" height="52" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="91" y="176" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">OTel span</text>
  <text x="91" y="194" font-size="10" text-anchor="middle" fill="var(--muted)">compat channel (here)</text>
  <rect x="186" y="152" width="170" height="52" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="271" y="176" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">adapter translates</text>
  <text x="271" y="194" font-size="9.5" text-anchor="middle" fill="var(--muted)">processToIngestionEvents</text>
  <rect x="300" y="84" width="180" height="72" rx="10" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="390" y="114" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">IngestionEventType[]</text>
  <text x="390" y="134" font-size="10" text-anchor="middle" fill="var(--muted)">L13 native event format</text>
  <line x1="196" y1="70" x2="300" y2="104" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="356" y1="178" x2="390" y2="156" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="512" y="84" width="192" height="84" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="608" y="108" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">converge · one backend</text>
  <text x="608" y="128" font-size="9.5" text-anchor="middle" fill="var(--muted)">mergeAndWrite · token/cost</text>
  <text x="608" y="146" font-size="9.5" text-anchor="middle" fill="var(--muted)">ClickhouseWriter batch (L15–17)</text>
  <line x1="480" y1="120" x2="512" y2="126" stroke="var(--teal)" stroke-width="2"></line>
  <text x="360" y="224" font-size="11" text-anchor="middle" fill="var(--muted)">from here on, OTel and native SDK are indistinguishable — same merge, same cost, same batched persistence</text>
</svg>

<div class="cols">
  <div class="col"><h4>🟦 native ingestion (L12–13)</h4><p>You use the Langfuse SDK and <strong>speak its mother tongue</strong> directly — events are exactly its schema, fields precise, no guessing. The "precise channel".</p></div>
  <div class="col"><h4>🔌 OTel ingestion (this lesson)</h4><p>You use OpenTelemetry and <strong>need translation</strong> — the adapter <strong>infers</strong> fields from heterogeneous conventions. Flexible but with semantic loss, the "compatibility channel". Both converge into one backend.</p></div>
</div>

<p>Unpack the worker's OTel job and you see exactly how "translate then converge into the main pipeline" happens:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>take the OTel job</h4><p>The worker pulls a job from <code>OtelIngestionQueue</code> and downloads this batch of span bodies from S3 by <code>fileKey</code>.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>parse spans</h4><p>Parse the S3 resourceSpans into a structured span list, ready to feed the adapter.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>adapter translates</h4><p><code>processToIngestionEvents(spans)</code> maps each span into a <strong>native ingestion event</strong> (Lesson 13's format) via priority attribute keys.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>split</h4><p>By entity type: <strong>observation</strong> straight to <code>IngestionService</code>, <strong>trace</strong> via <code>processEventBatch</code>.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>converge into the main pipeline</h4><p>From here OTel <strong>shares</strong> Lessons 15–17 with native: merge, token/cost, <code>ClickhouseWriter</code> batched persistence.</p></div></div>
</div>

<p>Precisely because the mapping is "best-effort inference", the OTel channel inherently has a <strong>semantic gap</strong>: if a library didn't write a key,
or used one the adapter doesn't yet recognize, that field may be missing. That's why the model name tries six or seven keys and usage even digs into span
events — <strong>the more the adapter recognizes, the smaller the gap</strong>. But however much it backfills, OTel's "inference" is never as precise as
native's "explicit statement" — the price of embracing an open standard. Happily the adapter <strong>keeps evolving</strong>: whenever the community spawns
a new convention, just <strong>add a few attribute keys</strong> to the priority list — old data unaffected, new data instantly recognized. This
"<strong>add a key, gain compatibility</strong>" extensibility lets Langfuse grow with the OpenTelemetry GenAI ecosystem without rewriting the mapping each
time.</p>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>If the native channel is more precise, why bother supporting OpenTelemetry?</strong> Because you <strong>meet users where they are</strong>.
  OpenTelemetry is the de facto observability standard; countless teams' apps are already instrumented with it. If Langfuse only spoke its own SDK, it would
  demand users <strong>re-instrument just for it</strong> — a barrier that turns many away. Supporting OTLP means "you <strong>change not one line of
  instrumentation</strong>, just point your OTel data over and it works". The cost is real: an <strong>adapter</strong> that must keep chasing each
  convention, full of priority fallbacks, plus the semantic loss of inference. But the math works out — because the adapter lives only at the
  <strong>very front</strong>, and after translating it converges into the <strong>shared core</strong> (merge, cost, write is just one). <strong>Confine the
  grunt work and special cases to one adapter layer at the edge, keep the core pure and unified</strong> — the most classic use of the "adapter pattern".
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>Langfuse offers an <strong>OTLP endpoint</strong> (<code>/api/public/otel/v1/traces</code>) accepting OpenTelemetry spans (protobuf/JSON, gzip), letting you onboard <strong>without changing instrumentation</strong>.</li>
    <li>OTLP uses the <strong>same S3 + queue</strong> pattern as Lesson 14: span body to S3, pointer to the <strong>dedicated</strong> <code>OtelIngestionQueue</code> (with primary/secondary).</li>
    <li><code>OtelIngestionProcessor</code> is a <strong>universal adapter</strong>: a <strong>priority attribute-key list</strong> per field, trying OTel <code>gen_ai.*</code>, Vercel <code>ai.*</code>, OpenLLMetry <code>llm.*</code> and more, taking the first present.</li>
    <li>Mapping yields <strong>native ingestion events</strong> (Lesson 13 format); observations to <code>IngestionService</code>, traces to <code>processEventBatch</code> — thereafter <strong>identical to native</strong>.</li>
    <li>Tradeoff: OTel is the "compatibility channel", inferred and with a semantic gap; native is the "precise channel". <strong>Confine adapter special-cases to the edge, keep the core unified</strong> — the classic adapter pattern.</li>
  </ul>
</div>
""")
LESSON_18 = {"zh": "\n".join(_ZH18), "en": "\n".join(_EN18)}


# ══════════════════════════════════════════════════════════════════════
# L19 · 媒体与 blob 存储 / Media & blob storage
# ══════════════════════════════════════════════════════════════════════
_ZH19 = []
_EN19 = []

_ZH19.append(r"""
<p class="lead">
多模态时代，一次 LLM 调用的 input/output 里可能塞着<strong>一张图、一段音频、一个 PDF</strong>——动辄几 MB 的二进制。如果把这些原样写进第 8 课的 ClickHouse 宽表，
input/output 列会<strong>瞬间膨胀</strong>，查询变慢、存储浪费。Langfuse 的解法干净利落：<strong>大块二进制根本不进 ClickHouse</strong>，
而是单独存进 S3 媒体桶，事件里只留一个<strong>小小的引用串</strong>。这一课，就讲这套「把笨重的 blob 挡在热路径之外」的媒体存储设计。
</p>

<div class="card analogy">
  <div class="tag">📚 生活类比</div>
  把它想成<strong>图书馆</strong>。目录卡片（ClickHouse 里的事件）上<strong>不会抄整本书</strong>，只写一个<strong>索书号</strong>（引用串 <code>@@@langfuseMedia:…@@@</code>）；
  真正厚重的书（媒体二进制）摆在<strong>书库的架子上</strong>（S3 媒体桶）。两个人上传同一本书，图书馆<strong>不会摆两本</strong>——靠书的「指纹」（sha256 哈希）认出是同一本，只存一份。
  你需要看书时，凭索书号去<strong>把书取出来</strong>。卡片轻、检索快；书库便宜、容量大——<strong>各得其所</strong>。
</div>
""")

# (L19 sections appended below)

_ZH19.append(r"""
<h2>blob 与引用分离：事件里只留索书号</h2>
<p>核心思想一句话：<strong>把 blob 从事件里拆出去</strong>。媒体二进制存进 S3 媒体桶；事件的 input/output 里，原本那张图的位置被替换成一个引用串
<code>@@@langfuseMedia:…@@@</code>。于是 ClickHouse 存的是几十字节的索书号，而不是几 MB 的图片。</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="原始多模态消息里的图片被替换成 langfuseMedia 引用串，图片本体存入 S3 媒体桶，ClickHouse 只存引用">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">blob 与引用分离：重的进 S3，轻的进 ClickHouse</text>
  <rect x="20" y="46" width="220" height="150" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="130" y="66" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">原始消息（多模态）</text>
  <rect x="36" y="78" width="188" height="30" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="130" y="97" text-anchor="middle" font-size="8" fill="var(--ink)">"text": "这张图里是什么？"</text>
  <rect x="36" y="114" width="188" height="66" rx="5" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="130" y="134" text-anchor="middle" font-size="8" font-weight="700" fill="var(--amber)">"image": &lt;3.4 MB base64&gt;</text><text x="130" y="152" text-anchor="middle" font-size="7.5" fill="var(--muted)">🖼️ 笨重的二进制</text><text x="130" y="167" text-anchor="middle" font-size="7.5" fill="var(--muted)">绝不能进 ClickHouse</text>
  <text x="260" y="120" font-size="14" fill="var(--faint)">▶</text><text x="278" y="112" font-size="7.5" fill="var(--faint)">拆分</text>
  <rect x="300" y="40" width="190" height="70" rx="10" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="395" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--amber)">S3 媒体桶</text><text x="395" y="78" text-anchor="middle" font-size="7.5" fill="var(--muted)">存图片本体（一份）</text><text x="395" y="93" text-anchor="middle" font-size="7.5" fill="var(--muted)">按 sha256 命名/去重</text>
  <rect x="300" y="126" width="190" height="70" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="395" y="146" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ClickHouse 事件</text><text x="395" y="164" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">"text": "这张图里是什么？"</text><text x="395" y="180" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">"image": @@@langfuseMedia:…@@@</text>
  <rect x="540" y="84" width="166" height="68" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="623" y="106" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">blob_storage_file_log</text><text x="623" y="124" text-anchor="middle" font-size="7.5" fill="var(--muted)">台账：哪个 blob</text><text x="623" y="138" text-anchor="middle" font-size="7.5" fill="var(--muted)">属于哪个 entity</text>
  <line x1="490" y1="75" x2="538" y2="105" stroke="var(--faint)" stroke-width="1.3"/><line x1="490" y1="160" x2="538" y2="130" stroke="var(--faint)" stroke-width="1.3"/>
</svg>
<div class="figcap"><b>重的进 S3、轻的进 ClickHouse</b>：多模态消息里的图片被替换成 <code>@@@langfuseMedia:…@@@</code> 引用串，本体存入 S3 媒体桶（按 sha256 去重），<code>blob_storage_file_log</code> 记录每个 blob 归属哪个 entity。源码：<code>packages/shared/src/utils/mediaReferences.ts:6</code>（<code>MEDIA_REFERENCE_PATTERN</code>）。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 212" role="img" aria-label="媒体与 blob 真实例子：observation 的 input 里不直接塞图片，而是一个 @@@langfuseMedia:...@@@ 引用 token，指向 S3 上的对象（key 形如 projectId/mediaId）。token 形如 MEDIA_REFERENCE_PATTERN，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：媒体存指针，本体落 S3</text>
  <rect x="20" y="38" width="320" height="160" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="32" y="56" font-size="9" font-weight="700" fill="var(--blue)">observation.input（小）</text>
  <text x="32" y="78" font-size="7.5" font-family="monospace" fill="var(--ink)">{ &quot;role&quot;: &quot;user&quot;,</text>
  <text x="32" y="94" font-size="7.5" font-family="monospace" fill="var(--ink)">  &quot;content&quot;: [</text>
  <text x="32" y="110" font-size="7.5" font-family="monospace" fill="var(--ink)">    {&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;这张图…&quot;},</text>
  <rect x="44" y="118" width="284" height="20" rx="4" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="50" y="132" font-size="7" font-family="monospace" fill="var(--amber)">@@@langfuseMedia:…id=med_9@@@</text>
  <text x="32" y="156" font-size="7.5" font-family="monospace" fill="var(--ink)">  ] }</text>
  <text x="32" y="184" font-size="7" fill="var(--muted)">只存「指针」，行很小、可聚合</text>
  <line x1="330" y1="128" x2="392" y2="128" stroke="var(--amber)" stroke-width="1.6"/><polygon points="392,128 383,123 383,133" fill="var(--amber)"/><text x="361" y="120" text-anchor="middle" font-size="7" font-weight="700" fill="var(--amber)">解引用</text>
  <rect x="396" y="38" width="304" height="160" rx="8" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.6"/><text x="408" y="56" font-size="9" font-weight="700" fill="var(--amber)">S3 对象（大）</text>
  <text x="408" y="78" font-size="7.5" font-family="monospace" fill="var(--ink)">key: {projectId}/{mediaId}</text>
  <text x="408" y="94" font-size="7.5" font-family="monospace" fill="var(--ink)">     proj_ab/med_9.png</text>
  <text x="408" y="112" font-size="7.5" font-family="monospace" fill="var(--ink)">content-type: image/png</text>
  <text x="408" y="128" font-size="7.5" font-family="monospace" fill="var(--ink)">size: 1.8 MB</text>
  <rect x="600" y="120" width="84" height="56" rx="6" fill="var(--bg)" stroke="var(--amber)"/><text x="642" y="152" text-anchor="middle" font-size="18" fill="var(--amber)">🖼</text>
  <text x="408" y="160" font-size="7.5" fill="var(--ink)">本体（可能很大）安静躺这</text>
  <text x="408" y="186" font-size="7" fill="var(--muted)">既不撑大宽表，又能按需取</text>
</svg>
<div class="figcap"><b>指针进表，本体落 S3</b>（token 形如 <code>MEDIA_REFERENCE_PATTERN</code>；<b>值为示例</b>）：图片/音频不直接塞进 observation，而是替换成一个 <code>@@@langfuseMedia:…@@@</code> 引用 token，真正的字节按 <code>{{projectId}}/{{mediaId}}</code> 存到 S3。于是宽表的行<b>保持小而可聚合</b>，UI 要看时再按指针去 S3 取——「队列轻、本体重」在媒体场景的延续。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/utils/mediaReferences.ts &amp; clickhouse/migrations/.../0011_*.sql</span><span class="ln">引用 + 台账</span></div>
  <pre class="code"><span class="cm">// 事件里媒体被替换成这种小引用串，ClickHouse 只存它（几十字节）</span>
<span class="kw">export const</span> MEDIA_REFERENCE_PATTERN = /@@@langfuseMedia:.+?@@@/g;
<span class="cm">// 例：@@@langfuseMedia:type=image/png|id=abc123|source=base64@@@</span>

<span class="cm">// blob_storage_file_log：所有 blob 的台账（又是第 8 课的 ReplacingMergeTree 宽表）</span>
CREATE TABLE blob_storage_file_log (
  project_id String, entity_type String, entity_id String, event_id String,
  bucket_name String, bucket_path String,        <span class="cm">-- 这个 blob 在哪</span>
  event_ts DateTime64(3), is_deleted UInt8,
) ENGINE = ReplacingMergeTree(event_ts, is_deleted)
  ORDER BY (project_id, entity_type, entity_id, event_id);</pre>
</div>

<p>为什么非得这么分？因为遥测数据和媒体 blob 的「体质」根本不同，硬放在一起会两头受罪——一个被撑大、一个被低效访问。对比一下就一目了然：</p>

<table class="t">
  <tr><th>维度</th><th>遥测数据（trace/observation）</th><th>媒体 blob（图/音/文件）</th></tr>
  <tr><td><b>大小</b></td><td>小，几 KB 的结构化 JSON/文本</td><td>大，动辄几 MB 的二进制</td></tr>
  <tr><td><b>访问方式</b></td><td>高频<strong>查询、过滤、聚合</strong></td><td>几乎只按 id <strong>整取</strong>，不查内部</td></tr>
  <tr><td><b>该放哪</b></td><td>ClickHouse 宽表（第 8 课）——为分析而生</td><td>S3 对象存储——为大文件而生、便宜</td></tr>
  <tr><td><b>事件里留什么</b></td><td>—</td><td>只留 <code>@@@langfuseMedia:…@@@</code> 引用串</td></tr>
</table>
""")

# (upload flow section below)

_ZH19.append(r"""
<h2>上传：直传 S3、按指纹去重</h2>
<p>媒体怎么进到 S3？关键是<strong>SDK 直接传给 S3</strong>，本体<strong>不经过 Langfuse 的应用服务器</strong>。流程是：SDK 先把媒体的<strong>指纹</strong>（sha256 哈希）、
类型、大小报给 <code>POST /api/public/media</code>；服务端据此决定——这媒体<strong>之前传过吗</strong>？</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="SDK 报 sha256 给 media 端点，已存在则返回 uploadUrl=null 跳过上传，否则返回 presigned URL 让 SDK 直传 S3">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">presigned 直传 + 内容寻址去重</text>
  <rect x="20" y="44" width="120" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">SDK</text><text x="80" y="80" text-anchor="middle" font-size="7.5" fill="var(--muted)">报 sha256+类型+大小</text>
  <rect x="180" y="44" width="140" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="250" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">media 端点</text><text x="250" y="78" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">查 prisma.media 去重</text>
  <line x1="140" y1="68" x2="178" y2="68" stroke="var(--faint)" stroke-width="1.5"/><polygon points="178,68 170,64 170,72" fill="var(--faint)"/>
  <rect x="360" y="20" width="180" height="40" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="450" y="38" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">命中：已传过同指纹</text><text x="450" y="52" text-anchor="middle" font-size="7.5" fill="var(--muted)">→ uploadUrl=null，跳过上传</text>
  <rect x="360" y="74" width="180" height="44" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="450" y="92" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">未命中：返回 presigned URL</text><text x="450" y="107" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">一个有时效的 S3 直传地址</text>
  <line x1="320" y1="60" x2="358" y2="42" stroke="var(--faint)" stroke-width="1.3"/><line x1="320" y1="76" x2="358" y2="94" stroke="var(--accent)" stroke-width="1.3"/>
  <rect x="566" y="74" width="140" height="44" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="636" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="var(--amber)">S3 媒体桶</text><text x="636" y="107" text-anchor="middle" font-size="7.5" fill="var(--muted)">SDK 凭 URL 直传本体</text>
  <line x1="540" y1="96" x2="564" y2="96" stroke="var(--amber)" stroke-width="1.6"/><polygon points="564,96 555,92 555,100" fill="var(--amber)"/>
  <text x="360" y="150" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">关键：媒体本体走 SDK→S3 直连，绝不经过 Langfuse 应用服务器</text>
  <rect x="120" y="166" width="480" height="36" rx="8" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="183" text-anchor="middle" font-size="8" fill="var(--muted)">内容寻址：媒体按 (project, sha256) 唯一；同一文件传一百次也只占一份存储</text><text x="360" y="196" text-anchor="middle" font-size="7.5" fill="var(--faint)">大小受 LANGFUSE_S3_MEDIA_MAX_CONTENT_LENGTH 限制</text>
</svg>
<div class="figcap"><b>presigned 直传 + 去重</b>：SDK 报指纹 → 服务端查 <code>prisma.media</code>（按 projectId+sha256 唯一）；已传过则回 <code>uploadUrl: null</code> 跳过，否则回 presigned URL 让 SDK <strong>直传 S3</strong>。本体不过应用层。源码：<code>web/src/features/media/server/mediaService.ts:66-122</code>。</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SDK 报指纹</h4><p>计算媒体的 sha256、contentType、contentLength，<code>POST /api/public/media</code>（先不传本体）。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>服务端去重判断</h4><p>按 <code>(projectId, sha256Hash)</code> 查 <code>prisma.media</code>；已成功上传过同类型 → 返回 <code>uploadUrl: null</code>，<strong>秒过</strong>。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>否则发 presigned URL</h4><p>新媒体则算出 <code>mediaId</code>、bucketPath，返回一个<strong>有时效的 S3 直传地址</strong>。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>SDK 直传 S3</h4><p>SDK 凭 URL 把本体<strong>直接 PUT 进 S3 媒体桶</strong>，不经 Langfuse 应用服务器——省带宽、不堵 API。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>关联 + 记台账</h4><p>媒体与 trace/observation 关联；<code>blob_storage_file_log</code> 记下这个 blob 归属哪个 entity，供生命周期管理与导出。</p></div></div>
</div>

<p>内容寻址去重在真实场景里收益惊人。设想你做了个「图片问答」应用，<strong>每条对话都带同一张企业 logo 当水印</strong>，或者一个 few-shot 提示里固定塞着<strong>同几张示例图</strong>——
一天下来可能有<strong>上万条 trace 引用同一张图</strong>。靠 sha256 指纹，这张图在 S3 里<strong>只存一份</strong>，后续每次「上传」都会在第 2 步被识破、<code>uploadUrl: null</code> 秒过，
既省存储、又省带宽、还省了 SDK 反复上传的时间。这就是把「同一性」交给内容哈希、而非文件名或时间戳来判断的妙处——<strong>相同的字节，永远只有一份</strong>，无论它被多少条 trace、多少个项目内的对话引用。</p>
""")

# (spark + key below)

_ZH19.append(r"""
<p>取用时反过来：<code>GET /api/public/media/[mediaId]</code> 返回一个<strong>有时效的下载地址</strong>，UI 或你的程序凭它去 S3 取回本体。
这个「有时效」也顺带管住了<strong>访问控制</strong>：下载链接由服务端在鉴权之后才签发、且很快过期，媒体既不会被公开裸奔在互联网上、也不会绕过项目边界（第 10 课）被别的租户读到。
整个生命周期里，几 MB 的二进制<strong>只在 SDK 和 S3 之间流动</strong>，Langfuse 的应用层和 ClickHouse 全程只碰那个轻飘飘的引用串——这正是把笨重负载挡在热路径之外的关键。</p>

<svg viewBox="0 0 720 220" role="img" aria-label="取用媒体的反向路径：程序用 mediaId 请求 GET /api/public/media，Langfuse 应用层鉴权后签发一个有时效的 S3 下载 URL，程序凭它直接从 S3 媒体桶取回 blob 本体；应用层与 ClickHouse 全程只碰引用串，URL 很快过期且不跨项目边界">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="20" y="78" width="150" height="60" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="104" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">UI / 你的程序</text>
  <text x="95" y="122" font-size="10" text-anchor="middle" fill="var(--muted)">只拿到引用串</text>
  <rect x="250" y="32" width="200" height="62" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="350" y="58" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Langfuse 应用层</text>
  <text x="350" y="78" font-size="10" text-anchor="middle" fill="var(--muted)">鉴权 → 签 presigned GET</text>
  <rect x="520" y="120" width="180" height="62" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="610" y="146" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">S3 媒体桶</text>
  <text x="610" y="166" font-size="10" text-anchor="middle" fill="var(--muted)">blob 本体（几 MB）</text>
  <line x1="170" y1="95" x2="250" y2="66" stroke="var(--blue)" stroke-width="2"></line>
  <text x="184" y="74" font-size="11" font-weight="700" fill="var(--accent-ink)">①</text>
  <line x1="250" y1="84" x2="170" y2="110" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="196" y="104" font-size="11" font-weight="700" fill="var(--accent-ink)">②</text>
  <line x1="170" y1="124" x2="520" y2="150" stroke="var(--teal)" stroke-width="2"></line>
  <text x="330" y="132" font-size="11" font-weight="700" fill="var(--accent-ink)">③</text>
  <text x="360" y="200" font-size="10.5" text-anchor="middle" fill="var(--muted)">① 请求 mediaId → ② 应用层鉴权后签有时效 URL → ③ 凭 URL 直接取 S3 本体</text>
  <text x="360" y="216" font-size="10" text-anchor="middle" fill="var(--muted)">应用层与 ClickHouse 全程只碰引用串；URL 很快过期、不跨项目边界（L10）</text>
</svg>

<div class="cols">
  <div class="col"><h4>😖 假如塞进 ClickHouse</h4><p>input 列里躺着几 MB base64，宽表体积暴涨；连「查最近 100 条 trace」这种<strong>压根不碰图</strong>的查询，也要扫过这些大字段，全表跟着变慢——一颗老鼠屎坏一锅汤。</p></div>
  <div class="col"><h4>😀 分离到 S3</h4><p>ClickHouse 只存几十字节引用，宽表<strong>始终精瘦</strong>、扫描飞快；图片躺在便宜的对象存储里，要用才按 id 取。各自待在最适合的地方，<strong>互不拖累</strong>，这也是第 7 课「双存储分工」在媒体场景的延续。</p></div>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么大费周章地把媒体单拎出来，而不是图省事直接塞进事件？</strong> 因为<strong>blob 和遥测数据的「体质」完全不同</strong>，硬塞在一起会两败俱伤。
  遥测数据（trace/observation）<strong>小、结构化、要被高频查询和聚合</strong>，所以放进 ClickHouse 宽表（第 8 课）；而媒体<strong>大、是不透明二进制、几乎只按 id 整取</strong>，
  天生属于对象存储。如果把几 MB 的图片塞进 ClickHouse 的 input 列，会<strong>同时毁掉两件事</strong>：宽表被撑爆、扫描变慢（连不带图的查询都被拖累），又用昂贵的分析库去干对象存储的活。
  Langfuse 的做法是<strong>各按本性安置</strong>：结构化的进 ClickHouse、二进制的进 S3，中间用一个 <code>@@@langfuseMedia@@@</code> 引用串牵线；再用 sha256 内容寻址<strong>天然去重</strong>、
  用 presigned URL 让本体<strong>绕开应用层直传</strong>。这套组合拳背后是一条朴素的工程智慧：<strong>让每种数据待在最适合它的存储里</strong>——这也为第三部分「摄取链路」画上句点。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>多模态媒体（图/音/文件）是<strong>大块二进制</strong>，绝不能塞进第 8 课的 ClickHouse 宽表——会撑爆 input/output 列、拖慢所有查询。</li>
    <li><strong>blob 与引用分离</strong>：本体存进 S3 媒体桶，事件里只留一个小引用串 <code>@@@langfuseMedia:…@@@</code>（<code>MEDIA_REFERENCE_PATTERN</code>）。</li>
    <li><strong>presigned 直传</strong>：SDK 凭服务端发的有时效 URL 把媒体<strong>直接 PUT 进 S3</strong>，本体不经 Langfuse 应用层，省带宽、不堵 API。</li>
    <li><strong>内容寻址去重</strong>：媒体按 <code>(projectId, sha256)</code> 唯一；已传过则回 <code>uploadUrl: null</code> 跳过——同一文件只占一份存储。</li>
    <li><code>blob_storage_file_log</code>（第 8 课同款 ReplacingMergeTree 宽表）记录每个 blob 归属哪个 entity，供生命周期管理与导出。核心智慧：<strong>让每种数据待在最适合它的存储里</strong>。</li>
  </ul>
</div>
""")

_EN19.append(r"""
<p class="lead">
In the multimodal era, an LLM call's input/output may carry <strong>an image, an audio clip, a PDF</strong> — binaries of several MB. Write those verbatim
into Lesson 8's ClickHouse wide tables and the input/output columns <strong>balloon instantly</strong>, queries slow, storage is wasted. Langfuse's answer is
clean: <strong>large binaries never enter ClickHouse</strong> at all; they're stored separately in an S3 media bucket, and the event keeps only a <strong>tiny
reference string</strong>. This lesson covers that media-storage design — keeping bulky blobs off the hot path.
</p>

<div class="card analogy">
  <div class="tag">📚 Analogy</div>
  Think of a <strong>library</strong>. The catalog card (the ClickHouse event) <strong>never transcribes the whole book</strong>, just a <strong>call
  number</strong> (the reference string <code>@@@langfuseMedia:…@@@</code>); the heavy books themselves (the media binaries) sit on the <strong>stacks</strong>
  (the S3 media bucket). Two people upload the same book and the library <strong>doesn't shelve two copies</strong> — it recognizes them as one by the book's
  "fingerprint" (the sha256 hash), storing just one. When you want to read, you fetch the book by its call number. Cards are light and searchable; stacks
  are cheap and roomy — <strong>each in its right place</strong>.
</div>
""")

_EN19.append(r"""
<h2>Blob and reference, split: the event keeps only a call number</h2>
<p>The core idea in one line: <strong>pull the blob out of the event</strong>. Media binaries go to the S3 media bucket; in the event's input/output, where
that image used to sit, a reference string <code>@@@langfuseMedia:…@@@</code> takes its place. So ClickHouse stores a few-dozen-byte call number, not a
multi-MB image.</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="the image in a raw multimodal message is replaced by a langfuseMedia reference string; the image body goes into the S3 media bucket; ClickHouse stores only the reference">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Blob/reference split: heavy to S3, light to ClickHouse</text>
  <rect x="20" y="46" width="220" height="150" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="130" y="66" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">raw message (multimodal)</text>
  <rect x="36" y="78" width="188" height="30" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="130" y="97" text-anchor="middle" font-size="8" fill="var(--ink)">"text": "what's in this image?"</text>
  <rect x="36" y="114" width="188" height="66" rx="5" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="130" y="134" text-anchor="middle" font-size="8" font-weight="700" fill="var(--amber)">"image": &lt;3.4 MB base64&gt;</text><text x="130" y="152" text-anchor="middle" font-size="7.5" fill="var(--muted)">🖼️ bulky binary</text><text x="130" y="167" text-anchor="middle" font-size="7.5" fill="var(--muted)">must NOT enter ClickHouse</text>
  <text x="260" y="120" font-size="14" fill="var(--faint)">▶</text><text x="278" y="112" font-size="7.5" fill="var(--faint)">split</text>
  <rect x="300" y="40" width="190" height="70" rx="10" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="395" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--amber)">S3 media bucket</text><text x="395" y="78" text-anchor="middle" font-size="7.5" fill="var(--muted)">stores the image (once)</text><text x="395" y="93" text-anchor="middle" font-size="7.5" fill="var(--muted)">named/deduped by sha256</text>
  <rect x="300" y="126" width="190" height="70" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="395" y="146" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ClickHouse event</text><text x="395" y="164" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">"text": "what's in this image?"</text><text x="395" y="180" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">"image": @@@langfuseMedia:…@@@</text>
  <rect x="540" y="84" width="166" height="68" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="623" y="106" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">blob_storage_file_log</text><text x="623" y="124" text-anchor="middle" font-size="7.5" fill="var(--muted)">ledger: which blob</text><text x="623" y="138" text-anchor="middle" font-size="7.5" fill="var(--muted)">belongs to which entity</text>
  <line x1="490" y1="75" x2="538" y2="105" stroke="var(--faint)" stroke-width="1.3"/><line x1="490" y1="160" x2="538" y2="130" stroke="var(--faint)" stroke-width="1.3"/>
</svg>
<div class="figcap"><b>Heavy to S3, light to ClickHouse</b>: the image in a multimodal message is replaced by a <code>@@@langfuseMedia:…@@@</code> reference; the body goes to the S3 media bucket (deduped by sha256), and <code>blob_storage_file_log</code> records which entity each blob belongs to. Source: <code>packages/shared/src/utils/mediaReferences.ts:6</code> (<code>MEDIA_REFERENCE_PATTERN</code>).</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 212" role="img" aria-label="Media and blob real example: an observation's input does not embed the image; instead an @@@langfuseMedia:...@@@ reference token points to an S3 object (key like projectId/mediaId). Token shape per MEDIA_REFERENCE_PATTERN, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: store a media pointer, body to S3</text>
  <rect x="20" y="38" width="320" height="160" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="32" y="56" font-size="9" font-weight="700" fill="var(--blue)">observation.input (small)</text>
  <text x="32" y="78" font-size="7.5" font-family="monospace" fill="var(--ink)">{ &quot;role&quot;: &quot;user&quot;,</text>
  <text x="32" y="94" font-size="7.5" font-family="monospace" fill="var(--ink)">  &quot;content&quot;: [</text>
  <text x="32" y="110" font-size="7.5" font-family="monospace" fill="var(--ink)">    {&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;this image…&quot;},</text>
  <rect x="44" y="118" width="284" height="20" rx="4" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="50" y="132" font-size="7" font-family="monospace" fill="var(--amber)">@@@langfuseMedia:…id=med_9@@@</text>
  <text x="32" y="156" font-size="7.5" font-family="monospace" fill="var(--ink)">  ] }</text>
  <text x="32" y="184" font-size="7" fill="var(--muted)">stores only a pointer; the row stays small and aggregatable</text>
  <line x1="330" y1="128" x2="392" y2="128" stroke="var(--amber)" stroke-width="1.6"/><polygon points="392,128 383,123 383,133" fill="var(--amber)"/><text x="361" y="120" text-anchor="middle" font-size="7" font-weight="700" fill="var(--amber)">dereference</text>
  <rect x="396" y="38" width="304" height="160" rx="8" fill="var(--amber-soft)" stroke="var(--amber)" stroke-width="1.6"/><text x="408" y="56" font-size="9" font-weight="700" fill="var(--amber)">S3 object (big)</text>
  <text x="408" y="78" font-size="7.5" font-family="monospace" fill="var(--ink)">key: {projectId}/{mediaId}</text>
  <text x="408" y="94" font-size="7.5" font-family="monospace" fill="var(--ink)">     proj_ab/med_9.png</text>
  <text x="408" y="112" font-size="7.5" font-family="monospace" fill="var(--ink)">content-type: image/png</text>
  <text x="408" y="128" font-size="7.5" font-family="monospace" fill="var(--ink)">size: 1.8 MB</text>
  <rect x="600" y="120" width="84" height="56" rx="6" fill="var(--bg)" stroke="var(--amber)"/><text x="642" y="152" text-anchor="middle" font-size="18" fill="var(--amber)">🖼</text>
  <text x="408" y="160" font-size="7.5" fill="var(--ink)">the blob (possibly large) sits quietly here</text>
  <text x="408" y="186" font-size="7" fill="var(--muted)">neither bloats the wide table nor blocks on-demand fetch</text>
</svg>
<div class="figcap"><b>Pointer in the table, body in S3</b> (token shape per <code>MEDIA_REFERENCE_PATTERN</code>; <b>values illustrative</b>): images/audio aren't embedded in the observation; they're replaced by a <code>@@@langfuseMedia:…@@@</code> reference token, while the real bytes go to S3 at <code>{{projectId}}/{{mediaId}}</code>. The wide-table row <b>stays small and aggregatable</b>, and the UI dereferences to S3 on demand — the “light queue, heavy body” idea applied to media.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/utils/mediaReferences.ts &amp; clickhouse/migrations/.../0011_*.sql</span><span class="ln">reference + ledger</span></div>
  <pre class="code"><span class="cm">// media in events is replaced by this small reference string; ClickHouse stores only it (~bytes)</span>
<span class="kw">export const</span> MEDIA_REFERENCE_PATTERN = /@@@langfuseMedia:.+?@@@/g;
<span class="cm">// e.g. @@@langfuseMedia:type=image/png|id=abc123|source=base64@@@</span>

<span class="cm">// blob_storage_file_log: a ledger of all blobs (again Lesson 8's ReplacingMergeTree wide table)</span>
CREATE TABLE blob_storage_file_log (
  project_id String, entity_type String, entity_id String, event_id String,
  bucket_name String, bucket_path String,        <span class="cm">-- where this blob lives</span>
  event_ts DateTime64(3), is_deleted UInt8,
) ENGINE = ReplacingMergeTree(event_ts, is_deleted)
  ORDER BY (project_id, entity_type, entity_id, event_id);</pre>
</div>

<p>Why split this way? Because telemetry data and media blobs have fundamentally different "constitutions", and forcing them together hurts both. A quick
comparison makes it obvious:</p>

<table class="t">
  <tr><th>dimension</th><th>telemetry (trace/observation)</th><th>media blob (image/audio/file)</th></tr>
  <tr><td><b>size</b></td><td>small, a few KB of structured JSON/text</td><td>large, often several MB of binary</td></tr>
  <tr><td><b>access</b></td><td>frequent <strong>query, filter, aggregate</strong></td><td>almost only fetched whole by id, never queried inside</td></tr>
  <tr><td><b>where it belongs</b></td><td>ClickHouse wide tables (Lesson 8) — built for analytics</td><td>S3 object storage — built for big files, cheap</td></tr>
  <tr><td><b>what stays in the event</b></td><td>—</td><td>only the <code>@@@langfuseMedia:…@@@</code> reference</td></tr>
</table>
""")

_EN19.append(r"""
<h2>Upload: direct to S3, deduped by fingerprint</h2>
<p>How does media get into S3? The key: the <strong>SDK uploads directly to S3</strong>, the body <strong>never passing through Langfuse's app
servers</strong>. The flow: the SDK first reports the media's <strong>fingerprint</strong> (sha256 hash), type and size to <code>POST /api/public/media</code>;
the server decides — has this media <strong>been uploaded before</strong>?</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="the SDK reports sha256 to the media endpoint; if it exists, returns uploadUrl=null to skip upload, otherwise returns a presigned URL for the SDK to upload directly to S3">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Presigned direct upload + content-addressed dedup</text>
  <rect x="20" y="44" width="120" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">SDK</text><text x="80" y="80" text-anchor="middle" font-size="7.5" fill="var(--muted)">reports sha256+type+size</text>
  <rect x="180" y="44" width="140" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="250" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">media endpoint</text><text x="250" y="78" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">checks prisma.media</text>
  <line x1="140" y1="68" x2="178" y2="68" stroke="var(--faint)" stroke-width="1.5"/><polygon points="178,68 170,64 170,72" fill="var(--faint)"/>
  <rect x="360" y="20" width="180" height="40" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="450" y="38" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">hit: same fingerprint exists</text><text x="450" y="52" text-anchor="middle" font-size="7.5" fill="var(--muted)">→ uploadUrl=null, skip upload</text>
  <rect x="360" y="74" width="180" height="44" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="450" y="92" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">miss: return presigned URL</text><text x="450" y="107" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">a time-limited direct-to-S3 address</text>
  <line x1="320" y1="60" x2="358" y2="42" stroke="var(--faint)" stroke-width="1.3"/><line x1="320" y1="76" x2="358" y2="94" stroke="var(--accent)" stroke-width="1.3"/>
  <rect x="566" y="74" width="140" height="44" rx="9" fill="var(--amber-soft)" stroke="var(--amber)"/><text x="636" y="92" text-anchor="middle" font-size="9" font-weight="700" fill="var(--amber)">S3 media bucket</text><text x="636" y="107" text-anchor="middle" font-size="7.5" fill="var(--muted)">SDK uploads body via URL</text>
  <line x1="540" y1="96" x2="564" y2="96" stroke="var(--amber)" stroke-width="1.6"/><polygon points="564,96 555,92 555,100" fill="var(--amber)"/>
  <text x="360" y="150" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">Key: media body goes SDK→S3 directly, never through Langfuse app servers</text>
  <rect x="120" y="166" width="480" height="36" rx="8" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="183" text-anchor="middle" font-size="8" fill="var(--muted)">content-addressed: media unique by (project, sha256); upload the same file 100x, store one copy</text><text x="360" y="196" text-anchor="middle" font-size="7.5" fill="var(--faint)">size capped by LANGFUSE_S3_MEDIA_MAX_CONTENT_LENGTH</text>
</svg>
<div class="figcap"><b>Presigned direct upload + dedup</b>: the SDK reports the fingerprint → the server checks <code>prisma.media</code> (unique by projectId+sha256); already uploaded → returns <code>uploadUrl: null</code> to skip, else a presigned URL for the SDK to <strong>upload directly to S3</strong>. The body never touches the app layer. Source: <code>web/src/features/media/server/mediaService.ts:66-122</code>.</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SDK reports the fingerprint</h4><p>Computes the media's sha256, contentType, contentLength, <code>POST /api/public/media</code> (no body yet).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>server dedup check</h4><p>Looks up <code>prisma.media</code> by <code>(projectId, sha256Hash)</code>; already uploaded with same type → returns <code>uploadUrl: null</code>, <strong>instant pass</strong>.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>else issue a presigned URL</h4><p>For new media, compute <code>mediaId</code>, bucketPath, and return a <strong>time-limited direct-to-S3 address</strong>.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>SDK uploads directly to S3</h4><p>The SDK PUTs the body <strong>straight into the S3 media bucket</strong> via the URL, bypassing Langfuse app servers — saves bandwidth, doesn't clog the API.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>link + log</h4><p>The media is linked to the trace/observation; <code>blob_storage_file_log</code> records which entity this blob belongs to, for lifecycle and export.</p></div></div>
</div>

<p>Content-addressed dedup pays off dramatically in practice. Imagine an "image Q&amp;A" app where <strong>every conversation carries the same company logo</strong>
as a watermark, or a few-shot prompt fixed with <strong>the same example images</strong> — over a day that could be <strong>tens of thousands of traces
referencing one image</strong>. By sha256 fingerprint, that image is <strong>stored once</strong> in S3; every subsequent "upload" is caught at step 2 with an
instant <code>uploadUrl: null</code> — saving storage, bandwidth, and the SDK's repeated upload time. That's the beauty of deciding "sameness" by content hash
rather than filename or timestamp — <strong>identical bytes, only ever one copy</strong>, however many traces or conversations within a project reference it.</p>
""")

_EN19.append(r"""
<p>Retrieval is the reverse: <code>GET /api/public/media/[mediaId]</code> returns a <strong>time-limited download address</strong>, and the UI or your code
fetches the body from S3 with it. That "time-limited" also handles <strong>access control</strong>: the download link is signed by the server only after auth
and expires quickly, so media is neither left publicly exposed nor readable across the project boundary (Lesson 10) by another tenant. Across the whole
lifecycle, the multi-MB binary <strong>only flows between the SDK and S3</strong>; Langfuse's app layer and ClickHouse only ever touch the featherweight
reference string — exactly what keeps bulky payloads off the hot path.</p>

<svg viewBox="0 0 720 220" role="img" aria-label="The reverse retrieval path: your code requests GET /api/public/media with a mediaId, Langfuse's app layer signs a time-limited S3 download URL after auth, and the code fetches the blob body directly from the S3 media bucket; the app layer and ClickHouse only ever touch the reference string, and the URL expires fast and never crosses the project boundary">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="20" y="78" width="150" height="60" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="104" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">UI / your code</text>
  <text x="95" y="122" font-size="10" text-anchor="middle" fill="var(--muted)">has only the reference</text>
  <rect x="250" y="32" width="200" height="62" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="350" y="58" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Langfuse app layer</text>
  <text x="350" y="78" font-size="10" text-anchor="middle" fill="var(--muted)">auth → sign presigned GET</text>
  <rect x="520" y="120" width="180" height="62" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="610" y="146" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">S3 media bucket</text>
  <text x="610" y="166" font-size="10" text-anchor="middle" fill="var(--muted)">blob body (several MB)</text>
  <line x1="170" y1="95" x2="250" y2="66" stroke="var(--blue)" stroke-width="2"></line>
  <text x="184" y="74" font-size="11" font-weight="700" fill="var(--accent-ink)">1</text>
  <line x1="250" y1="84" x2="170" y2="110" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="196" y="104" font-size="11" font-weight="700" fill="var(--accent-ink)">2</text>
  <line x1="170" y1="124" x2="520" y2="150" stroke="var(--teal)" stroke-width="2"></line>
  <text x="330" y="132" font-size="11" font-weight="700" fill="var(--accent-ink)">3</text>
  <text x="360" y="200" font-size="10.5" text-anchor="middle" fill="var(--muted)">1 request mediaId → 2 app signs a time-limited URL after auth → 3 fetch the body straight from S3</text>
  <text x="360" y="216" font-size="10" text-anchor="middle" fill="var(--muted)">app layer and ClickHouse only touch the reference; the URL expires fast and never crosses the project boundary (L10)</text>
</svg>

<div class="cols">
  <div class="col"><h4>😖 if stuffed into ClickHouse</h4><p>Several MB of base64 sit in the input column, the wide table bloats; even a query like "fetch the latest 100 traces" that <strong>never touches the image</strong> must scan past these huge fields, slowing the whole table — one bad apple spoils the barrel.</p></div>
  <div class="col"><h4>😀 split out to S3</h4><p>ClickHouse stores a few-dozen-byte reference, the wide table <strong>stays lean</strong> and scans fast; images rest in cheap object storage, fetched by id only when needed. Each in its best-fit place, <strong>neither dragging the other</strong>.</p></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why go to all this trouble to pull media out, rather than just stuffing it into the event?</strong> Because <strong>blobs and telemetry have utterly
  different constitutions</strong>, and cramming them together hurts both. Telemetry (trace/observation) is <strong>small, structured, queried and aggregated
  frequently</strong>, so it lives in ClickHouse wide tables (Lesson 8); media is <strong>large, opaque binary, almost only fetched whole by id</strong>,
  inherently belonging in object storage. Stuff a multi-MB image into a ClickHouse input column and you <strong>ruin two things at once</strong>: the wide table
  bloats and scans slow (dragging down even image-free queries), and you waste a pricey analytical store doing object storage's job. Langfuse instead
  <strong>places each by its nature</strong>: structured into ClickHouse, binary into S3, linked by a <code>@@@langfuseMedia@@@</code> reference; plus sha256
  content addressing for <strong>natural dedup</strong> and presigned URLs to let bodies <strong>bypass the app layer</strong>. Behind this combo is a plain
  engineering wisdom: <strong>let each kind of data live in the storage that fits it best</strong> — fittingly closing out Part 3, "the ingestion path".
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>Multimodal media (image/audio/file) are <strong>large binaries</strong> that must never enter Lesson 8's ClickHouse wide tables — they'd bloat input/output columns and slow every query.</li>
    <li><strong>Blob/reference split</strong>: the body goes to the S3 media bucket, the event keeps only a small reference <code>@@@langfuseMedia:…@@@</code> (<code>MEDIA_REFERENCE_PATTERN</code>).</li>
    <li><strong>Presigned direct upload</strong>: the SDK PUTs media <strong>straight to S3</strong> via a server-issued time-limited URL, the body bypassing Langfuse's app layer — saving bandwidth, not clogging the API.</li>
    <li><strong>Content-addressed dedup</strong>: media unique by <code>(projectId, sha256)</code>; already uploaded → <code>uploadUrl: null</code> skip — the same file stored only once.</li>
    <li><code>blob_storage_file_log</code> (Lesson 8's ReplacingMergeTree wide table) records which entity each blob belongs to, for lifecycle and export. The core wisdom: <strong>let each kind of data live in the storage that fits it best</strong>.</li>
  </ul>
</div>
""")
LESSON_19 = {"zh": "\n".join(_ZH19), "en": "\n".join(_EN19)}
