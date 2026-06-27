"""Part 4 — 查询链路 / The read (query) path. Lessons L20–L27.

Same authoring pattern as part1/2/3: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L20 · web 应用架构 / The web app architecture
# ══════════════════════════════════════════════════════════════════════
_ZH20 = []
_EN20 = []

_ZH20.append(r"""
<p class="lead">
前三部分顺着<strong>写入</strong>走完了：数据怎么进来、存哪、怎么合并落盘。从这一部分起，我们反向追<strong>读取</strong>——UI 和 SDK 怎么把数据<strong>查出来</strong>。
第一站是 web 应用的<strong>骨架</strong>。Langfuse 的前端是个 <strong>Next.js</strong> 应用，绝大多数页面用<strong>老牌的 Pages Router</strong>，
并行跑着<strong>三种 API 风格</strong>：给自家 UI 用的 tRPC、给 SDK 用的公共 REST、以及给流式/Webhook 用的少量 App-Router 处理器。看懂这张「门牌图」，后面七课才不会迷路。
</p>

<div class="card analogy">
  <div class="tag">🏢 生活类比</div>
  把 web 应用想成一栋<strong>大楼</strong>（Next.js）。大楼开了<strong>三道门</strong>，迎接三类访客：<strong>员工通道</strong>（tRPC——只给自家 UI 走，类型安全、内部直达）、
  <strong>公共前台</strong>（REST <code>/api/public</code>——给外部 SDK 走，稳定、带版本号），还有一个<strong>特殊装卸口</strong>（App-Router / SSE 处理器——给需要流式推送、Webhook 回调的特殊货物走）。
  三道门通向同一栋楼、同一批数据，但<strong>各服务各的客</strong>：员工不用走前台登记，外部访客也进不了员工通道。分清这三道门，就分清了 Langfuse 所有对外接口的脉络。
</div>
""")

# (L20 sections appended below)

_ZH20.append(r"""
<h2>一栋楼、三道门</h2>
<p>先看整体。<code>web/</code> 是一个 Next.js 应用，<code>web/src</code> 下分几大块：<code>features/</code>（按功能切的纵向模块，数十个）、
<code>components/</code>（共享 UI，含表格系统）、<code>server/</code>（鉴权 + tRPC）、<code>pages/</code>（页面与 API 路由）、还有少量 <code>app/</code>（App Router）。
而对外的接口，正是开篇说的三道门：</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">features/</span><span class="name">纵向功能模块（数十个）</span></div><div class="ld">按业务功能切分的「竖切片」：traces、search-bar、public-api、batch-exports… 每个功能把自己的页面、组件、server 逻辑收在一处。Langfuse 绝大多数代码住在这里。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">components/</span><span class="name">共享 UI</span></div><div class="ld">跨功能复用的通用组件，最重要的是 <code>components/table/</code> 那套表格系统（第 24 课）——列表、过滤、分页、列控制、行选择全靠它，是整个后台界面的骨架。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">server/</span><span class="name">鉴权 + tRPC</span></div><div class="ld"><code>server/api/{root,trpc}.ts</code> 是 tRPC 的根与中间件、procedure 定义（第 21 课）；<code>server/auth.ts</code> 是 NextAuth 会话。这是「员工通道」的安检处。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">pages/ · app/</span><span class="name">路由</span></div><div class="ld"><code>pages/</code> 是主干（UI 页面 + API 路由），<code>app/</code> 仅 4 个文件兜特殊语义。还有 <code>hooks/</code>、<code>ee/</code>（企业版）等。</div></div>
</div>

<p>这里值得停一下看 <code>features/</code> 的组织哲学：它是<strong>按「功能」而非按「技术层」切分</strong>的。传统做法可能把所有页面塞 <code>pages/</code>、所有组件塞 <code>components/</code>、所有接口塞 <code>api/</code>——
找一个功能的代码得在三四个目录间来回跳。Langfuse 反过来，每个功能（比如 search-bar、batch-exports）是一个<strong>自包含的竖切片</strong>，把它的前端组件、状态 hook、server 端逻辑、甚至说明 README 都收在
<code>features/&lt;功能&gt;/</code> 一处。好处是：读懂或修改一个功能，<strong>主要只需看一个目录</strong>；功能之间边界清晰，不易互相牵连。这也是为什么后面每讲一课，我们几乎都能精准地指向一个 <code>features/</code> 子目录，而不必满仓库地翻找散落各处的代码。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Next.js web 应用：Pages Router 承载 UI 页面与多数 API；三种 API 风格 tRPC 给 UI、REST 给 SDK、特殊语义端点给流式与 webhook">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Langfuse web 应用：一栋楼，三道门</text>
  <rect x="30" y="40" width="660" height="62" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="60" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">Next.js 应用（web/）· 以 Pages Router 为主</text><text x="360" y="78" text-anchor="middle" font-size="8" fill="var(--muted)">UI 页面 pages/project/[projectId]/…（traces / sessions / dashboards / datasets …）</text><text x="360" y="92" text-anchor="middle" font-size="8" fill="var(--muted)">src 目录：features/ · components/ · server/ · hooks/ · ee/</text>
  <rect x="24" y="124" width="210" height="100" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="129" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">① 员工通道 · tRPC</text><text x="129" y="164" text-anchor="middle" font-size="8" fill="var(--accent-ink)">pages/api/trpc/[trpc].ts</text><text x="129" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">给自家 UI · 类型安全</text><text x="129" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">~64 个 feature 路由</text><text x="129" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">第 21 课</text>
  <rect x="255" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="360" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">② 公共前台 · REST</text><text x="360" y="164" text-anchor="middle" font-size="8" fill="var(--ink)">pages/api/public/**</text><text x="360" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">给外部 SDK · 稳定带版本</text><text x="360" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">v1 / v2 / v3 + Fern 契约</text><text x="360" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">第 27 课</text>
  <rect x="486" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="591" y="146" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">③ 装卸口 · 特殊语义</text><text x="591" y="164" text-anchor="middle" font-size="7.5" fill="var(--muted)">app/api/**（仅 4 个文件）</text><text x="591" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">+ dashboard/execute-query-stream</text><text x="591" y="196" text-anchor="middle" font-size="7.5" fill="var(--muted)">流式 SSE · webhook</text>
  <line x1="129" y1="102" x2="129" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="360" y1="102" x2="360" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="591" y1="102" x2="591" y2="122" stroke="var(--faint)" stroke-width="1.4"/>
</svg>
<div class="figcap"><b>三道门各服务各的客</b>：<b>tRPC</b>（<code>pages/api/trpc/[trpc].ts</code>）给自家 UI、类型安全；<b>REST</b>（<code>pages/api/public/**</code>）给外部 SDK、稳定带版本；<b>特殊语义</b>（App Router <code>app/api/**</code> 4 文件 + Pages Router 流式 SSE 端点）给 webhook 与流式。源码：<code>web/src/server/api/root.ts</code>、<code>web/src/features/public-api/</code>、<code>web/src/app/</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/ &amp; web/src/app/</span><span class="ln">三种 API 入口</span></div>
  <pre class="code"><span class="cm">// ① tRPC：UI 的类型安全后端，一个文件接住全部 ~64 个路由</span>
web/src/pages/api/trpc/[trpc].ts        <span class="cm">// → appRouter（第 21 课）</span>

<span class="cm">// ② 公共 REST：给 SDK 的稳定接口，按资源 + 版本分文件夹</span>
web/src/pages/api/public/traces/index.ts
web/src/pages/api/public/v2/scores/…    <span class="cm">// 文件夹即版本（第 27 课）</span>

<span class="cm">// ③ App Router：只有 4 个文件，专给需要原始 Request/流式/webhook 的端点</span>
web/src/app/api/billing/stripe-webhook/route.ts
web/src/app/api/chatCompletion/route.ts
web/src/app/api/in-app-agent/route.ts
web/src/pages/api/dashboard/execute-query-stream.ts  <span class="cm">// SSE 流式仪表盘</span></pre>
</div>
""")

# (pages vs app router section below)

_ZH20.append(r"""
<h2>为什么几乎全是 Pages Router</h2>
<p>你可能注意到一个反差：明明 Next.js 早就推出了 App Router，Langfuse 却<strong>几乎全用老的 Pages Router</strong>——App Router 下统共只有 <strong>4 个文件</strong>。
这不是落伍，而是<strong>务实</strong>的取舍。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="Pages Router 承载几乎全部 UI 与 API，App Router 仅 4 个文件用于原始 Request、流式与 webhook 语义">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Pages Router 主干 · App Router 仅作特例</text>
  <rect x="30" y="44" width="420" height="130" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="240" y="66" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">Pages Router（主干 · 99%）</text>
  <rect x="48" y="80" width="186" height="38" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="141" y="98" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">UI 页面</text><text x="141" y="111" text-anchor="middle" font-size="7" fill="var(--muted)">pages/project/[projectId]/…</text>
  <rect x="246" y="80" width="186" height="38" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="339" y="98" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">API 路由</text><text x="339" y="111" text-anchor="middle" font-size="7" fill="var(--muted)">pages/api/**（tRPC + REST）</text>
  <text x="240" y="140" text-anchor="middle" font-size="8" fill="var(--accent-ink)">UI 用 tRPC + React Query，类型从后端一路贯穿到组件</text>
  <text x="240" y="158" text-anchor="middle" font-size="8" fill="var(--muted)">长期沉淀的成熟路线，团队约定俗成</text>
  <rect x="466" y="44" width="224" height="130" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="578" y="66" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">App Router（仅 4 文件）</text><text x="578" y="88" text-anchor="middle" font-size="7.5" fill="var(--muted)">layout.tsx（根布局）</text><text x="578" y="104" text-anchor="middle" font-size="7.5" fill="var(--muted)">stripe-webhook/route.ts</text><text x="578" y="120" text-anchor="middle" font-size="7.5" fill="var(--muted)">chatCompletion/route.ts</text><text x="578" y="136" text-anchor="middle" font-size="7.5" fill="var(--muted)">in-app-agent/route.ts</text><text x="578" y="158" text-anchor="middle" font-size="8" fill="var(--blue)">只为「原始 Request / 流式 / webhook」</text>
</svg>
<div class="figcap"><b>务实而非落伍</b>：Pages Router 承载几乎全部 UI 与 API（tRPC + REST）；App Router 只保留 4 个文件，专给需要<strong>原始 <code>Request</code>、流式响应、webhook 回调</strong>这类 Pages Router 不擅长的语义。源码：<code>web/src/app/</code>（layout + 3 个 route.ts）。</div>
</div>

<table class="t">
  <tr><th>这道门</th><th>给谁用</th><th>在哪</th><th>为什么</th></tr>
  <tr><td><b>tRPC</b></td><td>自家 UI（React）</td><td><code>pages/api/trpc/[trpc].ts</code></td><td>类型从后端贯穿到前端，改一处全链路报错；内部接口无需对外稳定</td></tr>
  <tr><td><b>公共 REST</b></td><td>外部 SDK / 用户脚本</td><td><code>pages/api/public/**</code></td><td>对外契约要<strong>稳定、带版本</strong>，由 Fern 生成多语言 SDK（第 27 课）</td></tr>
  <tr><td><b>特殊语义（App Router + SSE）</b></td><td>webhook 源 · 流式仪表盘</td><td>App Router <code>app/api/**</code>（webhook 等）+ Pages Router 的流式 SSE 端点</td><td>需要原始 <code>Request</code>、<code>text/event-stream</code> 等普通 Pages Router 路由不顺手的语义</td></tr>
</table>

<p>这套划分背后是一条清晰的边界：<strong>对内求「类型安全、改得快」，对外求「契约稳定、版本可控」</strong>。UI 和后端是同一个团队、同一个仓库，用 tRPC 把类型一路打通，
重构时编译器即时报错；而 SDK 面向千千万万外部用户，接口一旦发布就不能随意改，于是用 REST + 版本号 + Fern 契约严格约束。<strong>同一批数据，两种对外姿态</strong>——
内部接口可以天天演进，外部契约必须长期稳定，把它们放进同一种 API 反而会互相掣肘。这正是 Part 4 要展开的读取链路的总纲。</p>

<p>预告一下整条读取链路：无论从哪道门进来，一次「查数据」的请求大致都要走这么几步。后面七课会逐站深入：</p>

<svg viewBox="0 0 720 200" role="img" aria-label="一次查数据请求要走的五站读取链路：① 入口 tRPC 或 REST 先鉴权(L21/27)、② 把 FilterState 编译成参数化 SQL(L23)、③ 仓储层 queryClickhouse 统一执行(L22)、④ 读模型塑形 列表双查询或详情观测树(L24/25)、⑤ 返回并用 URL 状态渲染(L24)">
  <rect x="0" y="0" width="720" height="200" fill="var(--bg)"></rect>
  <text x="24" y="28" font-size="12" font-weight="700" fill="var(--accent-ink)">一次「查数据」请求要走的 5 站（Part 4 路线图）</text>
  <rect x="16" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="78" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">① 入口</text>
  <text x="78" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">tRPC / REST</text>
  <text x="78" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">先鉴权</text>
  <text x="78" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L21 / L27</text>
  <rect x="156" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="218" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">② 过滤</text>
  <text x="218" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">FilterState</text>
  <text x="218" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">→ 参数化 SQL</text>
  <text x="218" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L23</text>
  <rect x="296" y="46" width="124" height="92" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="358" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">③ 仓储层</text>
  <text x="358" y="90" font-size="9" text-anchor="middle" fill="var(--ink)">queryClickhouse</text>
  <text x="358" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">重试 / 打 tag</text>
  <text x="358" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L22</text>
  <rect x="436" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="498" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">④ 读模型</text>
  <text x="498" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">列表双查询</text>
  <text x="498" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">/ 详情观测树</text>
  <text x="498" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L24 / L25</text>
  <rect x="576" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="638" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑤ 返回渲染</text>
  <text x="638" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">URL 状态</text>
  <text x="638" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">列预设 / 分享</text>
  <text x="638" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L24</text>
  <line x1="140" y1="92" x2="156" y2="92" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="280" y1="92" x2="296" y2="92" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="420" y1="92" x2="436" y2="92" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="560" y1="92" x2="576" y2="92" stroke="var(--blue)" stroke-width="2"></line>
  <text x="360" y="168" font-size="11" text-anchor="middle" fill="var(--muted)">无论从哪道门进来，读取链路殊途同归；sessions（L26）是在 trace 之上再加一层「对话」视角</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>入口（tRPC 或 REST）</h4><p>UI 发 tRPC 调用、SDK 发 REST 请求；各自的入口先做<strong>鉴权</strong>，确认你能读这个 project（第 21、27 课）。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>过滤与查询构建</h4><p>把 UI 的 <code>FilterState</code>（或 SDK 的查询参数）<strong>编译成参数化 SQL</strong>，并带上强制的 project_id 与时间窗（第 23 课）。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>仓储层执行</h4><p>经过统一的 ClickHouse 执行器：打 OTel span、贴查询 tag、失败退避重试、把资源错误翻成友好提示（第 22 课）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>读模型塑形</h4><p>列表走「紧凑行 + 懒加载指标」的双查询，详情走「整棵观测树」的全量取——按场景选不同读模型（第 24、25 课）。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>返回 + 前端渲染</h4><p>结果回到 UI，表格系统用 URL 状态、列预设、行选择把它<strong>快速且可分享地</strong>渲染出来（第 24 课）。</p></div></div>
</div>
""")

# (spark + key below)

_ZH20.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么不赶时髦全面迁到 App Router、或者干脆只用 REST 一种 API？</strong> 因为<strong>架构选择要服务于团队现实，而非追新</strong>。Langfuse 在 App Router 成熟之前
  就用 Pages Router + tRPC 立了稳固的根基——tRPC 让前后端<strong>共享同一套类型</strong>，是这个全栈团队迭代飞快的关键，贸然迁移收益小、风险大。至于 API：
  对内和对外是<strong>两类截然不同的需求</strong>。对内（UI）追求的是「改一处、全链路类型即时校验」，tRPC 完美契合；对外（SDK）追求的是「我两年前写的集成代码今天还能跑」，
  这就必须有稳定契约、显式版本。硬把两者统一成一种 API，要么牺牲内部的开发速度，要么牺牲外部的稳定性。Langfuse 的答案是<strong>不强求统一，按受众分而治之</strong>——
  再用 App Router 兜住少数特殊语义。<strong>合适，比统一更重要。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>Langfuse 前端是 <strong>Next.js 应用</strong>，<strong>绝大多数用 Pages Router</strong>；App Router 仅 4 个文件，专给原始 Request/流式/webhook。</li>
    <li><strong>三种 API 风格并存</strong>：tRPC（UI，类型安全）、公共 REST（SDK，稳定带版本）、特殊语义端点（App Router 处理器 + Pages Router 流式 SSE，供 webhook/流式）。</li>
    <li><code>web/src</code> 分层：<code>features/</code>（数十个纵向功能模块）、<code>components/</code>（共享 UI）、<code>server/</code>（鉴权+tRPC）、<code>pages/</code>、<code>app/</code>。</li>
    <li>核心边界：<strong>对内求类型安全与迭代速度（tRPC），对外求契约稳定与版本可控（REST + Fern）</strong>——同一批数据、两种对外姿态。</li>
    <li>这是 Part 4「读取链路」的总览图；接下来七课将分别钻进 tRPC 骨架、仓储层、过滤、表格、详情、sessions、公共 REST。</li>
  </ul>
</div>
""")

_EN20.append(r"""
<p class="lead">
The first three parts followed the <strong>write</strong> direction: how data comes in, where it's stored, how it's merged and persisted. From this part on
we trace <strong>reads</strong> in reverse — how the UI and SDKs <strong>query data back out</strong>. First stop: the web app's <strong>skeleton</strong>.
Langfuse's frontend is a <strong>Next.js</strong> app, with the vast majority of pages on the <strong>veteran Pages Router</strong>, running <strong>three API
styles</strong> in parallel: tRPC for its own UI, a public REST API for SDKs, and a handful of App-Router handlers for streaming/webhooks. Grasp this "door
map" and the next seven lessons won't get you lost.
</p>

<div class="card analogy">
  <div class="tag">🏢 Analogy</div>
  Think of the web app as a <strong>building</strong> (Next.js) with <strong>three doors</strong> for three kinds of visitors: a <strong>staff
  entrance</strong> (tRPC — only for its own UI, type-safe, direct internal access), a <strong>public reception</strong> (REST <code>/api/public</code> —
  for external SDKs, stable, versioned), and a <strong>special loading dock</strong> (App-Router / SSE handlers — for special cargo needing streaming
  pushes or webhook callbacks). All three doors lead into the same building, the same data, but <strong>each serves its own crowd</strong>: staff skip
  reception, external visitors can't use the staff entrance. Sort out these three doors and you've sorted out every Langfuse external interface.
</div>
""")

_EN20.append(r"""
<h2>One building, three doors</h2>
<p>The big picture first. <code>web/</code> is a Next.js app; under <code>web/src</code> sit a few big areas: <code>features/</code> (vertical, by-feature
modules, dozens of them), <code>components/</code> (shared UI, including the table system), <code>server/</code> (auth + tRPC), <code>pages/</code> (pages and API
routes), plus a small <code>app/</code> (App Router). And the external interfaces are exactly the three doors from the intro:</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">features/</span><span class="name">vertical feature modules (dozens)</span></div><div class="ld">"Vertical slices" cut by business feature: traces, search-bar, public-api, batch-exports… each gathers its own pages, components, and server logic in one place. Most Langfuse code lives here.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">components/</span><span class="name">shared UI</span></div><div class="ld">Cross-feature reusable components, most importantly <code>components/table/</code> (Lesson 24) — lists, filtering, pagination, column control, row selection, the skeleton of the whole back-office UI.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">server/</span><span class="name">auth + tRPC</span></div><div class="ld"><code>server/api/{root,trpc}.ts</code> is the tRPC root, middleware, and procedure definitions (Lesson 21); <code>server/auth.ts</code> is the NextAuth session. The "staff entrance" security check.</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">pages/ · app/</span><span class="name">routing</span></div><div class="ld"><code>pages/</code> is the trunk (UI pages + API routes), <code>app/</code> is just 4 files for special semantics. Plus <code>hooks/</code>, <code>ee/</code> (enterprise), etc.</div></div>
</div>

<p>Pause on <code>features/</code>'s organizing philosophy: it's cut <strong>by "feature", not by "technical layer"</strong>. A traditional layout might dump all
pages in <code>pages/</code>, all components in <code>components/</code>, all endpoints in <code>api/</code> — finding one feature's code means hopping across
three or four directories. Langfuse inverts this: each feature (say search-bar, batch-exports) is a <strong>self-contained vertical slice</strong> gathering its
frontend components, state hooks, server logic, even a README under one <code>features/&lt;feature&gt;/</code>. The payoff: to understand or change a feature you
<strong>mostly read just one directory</strong>; boundaries between features are clear, so they don't entangle. That's why nearly every later lesson can point
precisely at a <code>features/</code> subfolder.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Next.js web app: Pages Router carries UI pages and most APIs; three API styles tRPC for UI, REST for SDK, special-semantics endpoints for streaming and webhooks">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">The Langfuse web app: one building, three doors</text>
  <rect x="30" y="40" width="660" height="62" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="60" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">Next.js app (web/) · primarily Pages Router</text><text x="360" y="78" text-anchor="middle" font-size="8" fill="var(--muted)">UI pages pages/project/[projectId]/… (traces / sessions / dashboards / datasets …)</text><text x="360" y="92" text-anchor="middle" font-size="8" fill="var(--muted)">src dirs: features/ · components/ · server/ · hooks/ · ee/</text>
  <rect x="24" y="124" width="210" height="100" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="129" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">① staff entrance · tRPC</text><text x="129" y="164" text-anchor="middle" font-size="8" fill="var(--accent-ink)">pages/api/trpc/[trpc].ts</text><text x="129" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">own UI · type-safe</text><text x="129" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">~64 feature routers</text><text x="129" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">Lesson 21</text>
  <rect x="255" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="360" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">② public reception · REST</text><text x="360" y="164" text-anchor="middle" font-size="8" fill="var(--ink)">pages/api/public/**</text><text x="360" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">external SDK · stable, versioned</text><text x="360" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">v1 / v2 / v3 + Fern contract</text><text x="360" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">Lesson 27</text>
  <rect x="486" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="591" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">③ loading dock · special semantics</text><text x="591" y="164" text-anchor="middle" font-size="7.5" fill="var(--muted)">app/api/** (only 4 files)</text><text x="591" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">+ dashboard/execute-query-stream</text><text x="591" y="196" text-anchor="middle" font-size="7.5" fill="var(--muted)">streaming SSE · webhook</text>
  <line x1="129" y1="102" x2="129" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="360" y1="102" x2="360" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="591" y1="102" x2="591" y2="122" stroke="var(--faint)" stroke-width="1.4"/>
</svg>
<div class="figcap"><b>Three doors, each serving its own crowd</b>: <b>tRPC</b> (<code>pages/api/trpc/[trpc].ts</code>) for the UI, type-safe; <b>REST</b> (<code>pages/api/public/**</code>) for external SDKs, stable and versioned; <b>special semantics</b> (App Router <code>app/api/**</code> 4 files + a Pages-Router streaming SSE endpoint) for webhooks and streaming. Source: <code>web/src/server/api/root.ts</code>, <code>web/src/features/public-api/</code>, <code>web/src/app/</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/pages/api/ &amp; web/src/app/</span><span class="ln">three API entries</span></div>
  <pre class="code"><span class="cm">// ① tRPC: the UI's type-safe backend, one file catches all ~64 routers</span>
web/src/pages/api/trpc/[trpc].ts        <span class="cm">// → appRouter (Lesson 21)</span>

<span class="cm">// ② public REST: the stable interface for SDKs, by resource + version folder</span>
web/src/pages/api/public/traces/index.ts
web/src/pages/api/public/v2/scores/…    <span class="cm">// folder = version (Lesson 27)</span>

<span class="cm">// ③ App Router: only 4 files, for endpoints needing raw Request/streaming/webhook</span>
web/src/app/api/billing/stripe-webhook/route.ts
web/src/app/api/chatCompletion/route.ts
web/src/app/api/in-app-agent/route.ts
web/src/pages/api/dashboard/execute-query-stream.ts  <span class="cm">// SSE streaming dashboards</span></pre>
</div>
""")

_EN20.append(r"""
<h2>Why it's almost all Pages Router</h2>
<p>You may notice a contrast: even though Next.js shipped the App Router long ago, Langfuse <strong>uses the old Pages Router for almost everything</strong> —
the App Router has all of <strong>4 files</strong>. This isn't being behind the times; it's a <strong>pragmatic</strong> choice.</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="Pages Router carries nearly all UI and APIs; App Router is just 4 files for raw Request, streaming, and webhook semantics">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Pages Router trunk · App Router only for special cases</text>
  <rect x="30" y="44" width="420" height="130" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="240" y="66" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">Pages Router (trunk · 99%)</text>
  <rect x="48" y="80" width="186" height="38" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="141" y="98" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">UI pages</text><text x="141" y="111" text-anchor="middle" font-size="7" fill="var(--muted)">pages/project/[projectId]/…</text>
  <rect x="246" y="80" width="186" height="38" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="339" y="98" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">API routes</text><text x="339" y="111" text-anchor="middle" font-size="7" fill="var(--muted)">pages/api/** (tRPC + REST)</text>
  <text x="240" y="140" text-anchor="middle" font-size="8" fill="var(--accent-ink)">UI uses tRPC + React Query, types flow from backend to component</text>
  <text x="240" y="158" text-anchor="middle" font-size="8" fill="var(--muted)">a mature, long-settled path the team standardized on</text>
  <rect x="466" y="44" width="224" height="130" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="578" y="66" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--ink)">App Router (4 files only)</text><text x="578" y="88" text-anchor="middle" font-size="7.5" fill="var(--muted)">layout.tsx (root layout)</text><text x="578" y="104" text-anchor="middle" font-size="7.5" fill="var(--muted)">stripe-webhook/route.ts</text><text x="578" y="120" text-anchor="middle" font-size="7.5" fill="var(--muted)">chatCompletion/route.ts</text><text x="578" y="136" text-anchor="middle" font-size="7.5" fill="var(--muted)">in-app-agent/route.ts</text><text x="578" y="158" text-anchor="middle" font-size="8" fill="var(--blue)">only for "raw Request / streaming / webhook"</text>
</svg>
<div class="figcap"><b>Pragmatic, not behind</b>: Pages Router carries nearly all UI and APIs (tRPC + REST); App Router keeps just 4 files, for endpoints needing <strong>raw <code>Request</code>, streaming responses, webhook callbacks</strong> — semantics Pages Router handles awkwardly. Source: <code>web/src/app/</code> (layout + 3 route.ts).</div>
</div>

<table class="t">
  <tr><th>this door</th><th>for whom</th><th>where</th><th>why</th></tr>
  <tr><td><b>tRPC</b></td><td>own UI (React)</td><td><code>pages/api/trpc/[trpc].ts</code></td><td>types flow backend → frontend, change one spot and the whole chain errors; internal API needn't be externally stable</td></tr>
  <tr><td><b>public REST</b></td><td>external SDK / user scripts</td><td><code>pages/api/public/**</code></td><td>the external contract must be <strong>stable, versioned</strong>, with Fern generating multi-language SDKs (Lesson 27)</td></tr>
  <tr><td><b>special semantics (App Router + SSE)</b></td><td>webhook sources · streaming dashboards</td><td>App Router <code>app/api/**</code> (webhooks etc.) + a Pages-Router streaming SSE endpoint</td><td>needs raw <code>Request</code>, <code>text/event-stream</code>, etc. — semantics a plain Pages-Router route handles awkwardly</td></tr>
</table>

<p>Behind this split is a clear boundary: <strong>internally, seek "type-safe, fast to change"; externally, seek "stable contract, controlled versions"</strong>.
The UI and backend are one team, one repo, so tRPC threads types end to end — the compiler errors instantly on refactors; whereas the SDK faces countless external
users, where a published interface can't change freely, so REST + version numbers + the Fern contract enforce strict stability. <strong>Same data, two external
postures</strong> — the internal API can evolve daily, the external contract must stay stable for years; forcing them into one API style would only hobble each
other. This is the master plan of Part 4's read path.</p>

<p>A preview of the whole read path: whichever door you enter, a "query data" request roughly takes these steps. The next seven lessons dive into each stop:</p>

<svg viewBox="0 0 720 200" role="img" aria-label="the five stations of a query-data request: (1) entry tRPC or REST auths first (L21/27), (2) compile FilterState into parameterized SQL (L23), (3) the repository layer runs it via queryClickhouse (L22), (4) read-model shaping with the list two-query or detail observation tree (L24/25), (5) return and render with URL state (L24)">
  <rect x="0" y="0" width="720" height="200" fill="var(--bg)"></rect>
  <text x="24" y="28" font-size="12" font-weight="700" fill="var(--accent-ink)">The 5 stations of a "query data" request (Part 4 roadmap)</text>
  <rect x="16" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="78" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">1 entry</text>
  <text x="78" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">tRPC / REST</text>
  <text x="78" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">auth first</text>
  <text x="78" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L21 / L27</text>
  <rect x="156" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="218" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">2 filter</text>
  <text x="218" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">FilterState</text>
  <text x="218" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">→ param SQL</text>
  <text x="218" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L23</text>
  <rect x="296" y="46" width="124" height="92" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="358" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">3 repository</text>
  <text x="358" y="90" font-size="9" text-anchor="middle" fill="var(--ink)">queryClickhouse</text>
  <text x="358" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">retry / tag</text>
  <text x="358" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L22</text>
  <rect x="436" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="498" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">4 read model</text>
  <text x="498" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">list two-query</text>
  <text x="498" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">/ detail tree</text>
  <text x="498" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L24 / L25</text>
  <rect x="576" y="46" width="124" height="92" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="638" y="70" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">5 render</text>
  <text x="638" y="90" font-size="10" text-anchor="middle" fill="var(--ink)">URL state</text>
  <text x="638" y="108" font-size="10" text-anchor="middle" fill="var(--muted)">presets / share</text>
  <text x="638" y="128" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">L24</text>
  <line x1="140" y1="92" x2="156" y2="92" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="280" y1="92" x2="296" y2="92" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="420" y1="92" x2="436" y2="92" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="560" y1="92" x2="576" y2="92" stroke="var(--blue)" stroke-width="2"></line>
  <text x="360" y="168" font-size="11" text-anchor="middle" fill="var(--muted)">whichever door you enter, the read path converges; sessions (L26) add a "conversation" lens on top of traces</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>entry (tRPC or REST)</h4><p>The UI fires a tRPC call, the SDK a REST request; each entry first does <strong>auth</strong>, confirming you can read this project (Lessons 21, 27).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>filter &amp; query build</h4><p>The UI's <code>FilterState</code> (or SDK query params) is <strong>compiled into parameterized SQL</strong>, with the mandatory project_id and time window (Lesson 23).</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>repository executes</h4><p>Through a unified ClickHouse executor: OTel span, query tags, backoff retry on failure, resource errors turned into friendly messages (Lesson 22).</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>read-model shaping</h4><p>Lists use a "compact rows + lazy metrics" dual query; details fetch the "whole observation tree" — different read models per scenario (Lessons 24, 25).</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>return + frontend render</h4><p>Results return to the UI, where the table system renders them <strong>fast and shareably</strong> with URL state, column presets, row selection (Lesson 24).</p></div></div>
</div>
""")

_EN20.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why not chase the trend and migrate fully to App Router, or just use REST as the one API?</strong> Because <strong>architecture choices should serve
  team reality, not novelty</strong>. Langfuse laid a solid foundation on Pages Router + tRPC before the App Router matured — tRPC lets front and back
  <strong>share one type system</strong>, the key to this full-stack team iterating fast; a rash migration is low-reward, high-risk. As for the API: internal and
  external are <strong>two utterly different needs</strong>. Internal (UI) wants "change one spot, instant type-check across the chain" — tRPC fits perfectly;
  external (SDK) wants "the integration I wrote two years ago still runs today" — which demands a stable contract and explicit versions. Force the two into one
  API and you sacrifice either internal velocity or external stability. Langfuse's answer is <strong>don't force unity; divide and conquer by audience</strong> —
  with App Router catching the few special semantics. <strong>Fit matters more than uniformity.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>Langfuse's frontend is a <strong>Next.js app</strong>, <strong>mostly Pages Router</strong>; App Router is just 4 files for raw Request/streaming/webhook.</li>
    <li><strong>Three API styles coexist</strong>: tRPC (UI, type-safe), public REST (SDK, stable+versioned), special-semantics endpoints (App Router handlers + a Pages-Router streaming SSE, for webhook/streaming).</li>
    <li><code>web/src</code> layers: <code>features/</code> (dozens of vertical feature modules), <code>components/</code> (shared UI), <code>server/</code> (auth+tRPC), <code>pages/</code>, <code>app/</code>.</li>
    <li>Core boundary: <strong>internally seek type-safety and iteration speed (tRPC), externally seek contract stability and version control (REST + Fern)</strong> — same data, two external postures.</li>
    <li>This is Part 4's read-path overview; the next seven lessons drill into the tRPC backbone, repository layer, filtering, tables, detail, sessions, and the public REST API.</li>
  </ul>
</div>
""")
LESSON_20 = {"zh": "\n".join(_ZH20), "en": "\n".join(_EN20)}


# ══════════════════════════════════════════════════════════════════════
# L21 · tRPC 骨架 / The tRPC backbone
# ══════════════════════════════════════════════════════════════════════
_ZH21 = []
_EN21 = []

_ZH21.append(r"""
<p class="lead">
上一课点出了三道门，这一课推开「员工通道」——<strong>tRPC</strong>，看它的骨架。tRPC 是 UI 与后端之间<strong>类型安全的契约</strong>：后端定义的类型，前端调用时<strong>一路贯穿</strong>，
改一处、全链路即时报错。它的结构出奇地简洁：一个<strong>根路由</strong>聚合约 64 个功能路由，加一小撮<strong>「procedure 构建器」</strong>用<strong>分层中间件</strong>统一把守鉴权与 RBAC。
看懂这套中间件栈，你就看懂了 Langfuse 整个 UI 后端的安检与脉络。
</p>

<div class="card analogy">
  <div class="tag">🛂 生活类比</div>
  把每个 tRPC 请求想成走一条<strong>安检走廊</strong>。走廊里一道道关卡就是<strong>中间件</strong>：先有<strong>摄像头</strong>记录你来过（OTel 追踪），再有<strong>应急员</strong>守着随时接住异常（错误处理），
  然后是<strong>身份核验</strong>（你登录了吗），最后是<strong>门禁名单</strong>（你在<strong>这个房间</strong>的准入名单上吗——即「你是这个 project 的成员吗」）。
  不同的门（procedure）配不同数量的关卡：公开的门只过前两关，受保护的门要全程走完。<strong>关卡定义一次，每道门按需挑选</strong>——这就是 procedure 构建器的精髓。
</div>
""")

# (L21 sections appended below)

_ZH21.append(r"""
<h2>procedure = 可叠加的中间件栈</h2>
<p>tRPC 的精髓在于：<strong>procedure（过程）是一摞中间件叠出来的</strong>。每个中间件干一件事，按 <code>.use()</code> 顺序串起来；不同的 procedure 构建器叠不同的关卡。
Langfuse 在 <code>web/src/server/api/trpc.ts</code> 里定义了一组：从只过基础关卡的 <code>publicProcedure</code>，到层层加码的 <code>protectedProjectProcedure</code>。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="procedure 中间件栈：publicProcedure 含 OTel 追踪与错误处理，authenticatedProcedure 再加登录校验，protectedProjectProcedure 再加项目成员 RBAC">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">procedure 构建器：一层层叠中间件</text>
  <rect x="20" y="40" width="216" height="170" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="128" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">publicProcedure</text>
  <rect x="36" y="72" width="184" height="28" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="128" y="90" text-anchor="middle" font-size="8" fill="var(--ink)">① OTel 追踪</text>
  <rect x="36" y="106" width="184" height="28" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="128" y="124" text-anchor="middle" font-size="8" fill="var(--ink)">② 错误处理</text>
  <text x="128" y="160" text-anchor="middle" font-size="7.5" fill="var(--muted)">谁都能调</text><text x="128" y="174" text-anchor="middle" font-size="7.5" fill="var(--muted)">（如健康检查）</text>
  <rect x="252" y="40" width="216" height="170" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">authenticatedProcedure</text>
  <rect x="268" y="72" width="184" height="24" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="88" text-anchor="middle" font-size="7.5" fill="var(--ink)">① OTel ② 错误处理</text>
  <rect x="268" y="102" width="184" height="32" rx="5" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="118" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">③ 你登录了吗</text><text x="360" y="129" text-anchor="middle" font-size="7" fill="var(--accent-ink)">enforceUserIsAuthed</text>
  <text x="360" y="164" text-anchor="middle" font-size="7.5" fill="var(--muted)">需登录</text><text x="360" y="178" text-anchor="middle" font-size="7.5" fill="var(--muted)">（账号级操作）</text>
  <rect x="484" y="40" width="216" height="170" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="592" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">protectedProjectProcedure</text>
  <rect x="500" y="72" width="184" height="24" rx="5" fill="var(--bg)" stroke="var(--blue)"/><text x="592" y="88" text-anchor="middle" font-size="7.5" fill="var(--ink)">① OTel ② 错误处理</text>
  <rect x="500" y="102" width="184" height="44" rx="5" fill="var(--bg)" stroke="var(--accent)"/><text x="592" y="120" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">③ 你是这个 project 成员吗</text><text x="592" y="133" text-anchor="middle" font-size="7" fill="var(--accent-ink)">从输入取 projectId + 校验</text>
  <text x="592" y="166" text-anchor="middle" font-size="7.5" fill="var(--muted)">绝大多数业务路由</text><text x="592" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">（traces/scores/…）</text>
  <text x="360" y="222" text-anchor="middle" font-size="8.5" fill="var(--faint)">越往右关卡越多：定义一次中间件，每道门按需 .use() 挑选——RBAC 不必每个路由重写</text>
</svg>
<div class="figcap"><b>分层中间件，按需组合</b>：<code>publicProcedure</code>(OTel+错误处理) → <code>authenticatedProcedure</code>(+登录校验) → <code>protectedProjectProcedure</code>(+项目成员 RBAC)。还有 <code>protectedOrganizationProcedure</code>、<code>protectedGetTraceProcedure</code> 等变体。源码：<code>web/src/server/api/trpc.ts:238-583</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/api/trpc.ts</span><span class="ln">procedure 构建器</span></div>
  <pre class="code"><span class="kw">const</span> withOtelTracingProcedure = t.procedure.<span class="fn">use</span>(withOtelInstrumentation);

<span class="cm">// 公开：只过 OTel + 错误处理</span>
<span class="kw">export const</span> publicProcedure = withOtelTracingProcedure.<span class="fn">use</span>(withErrorHandling);

<span class="cm">// 需登录：再叠一层「你登录了吗」</span>
<span class="kw">export const</span> authenticatedProcedure = withOtelTracingProcedure
  .<span class="fn">use</span>(withErrorHandling).<span class="fn">use</span>(enforceUserIsAuthed);

<span class="cm">// 受保护（项目级）：再叠一层「你是这个 project 的成员吗」——最常用</span>
<span class="kw">export const</span> protectedProjectProcedure = withOtelTracingProcedure
  .<span class="fn">use</span>(withErrorHandling).<span class="fn">use</span>(enforceUserIsAuthedAndProjectMember);</pre>
</div>

<p>注意每道门最先叠的两层——<strong>OTel 追踪</strong>与<strong>错误处理</strong>——是<strong>所有</strong> procedure 的共同底座。错误处理这一层（<code>withErrorHandling</code>）尤其用心：
它把 resolver 抛出的异常<strong>统一翻译</strong>成对前端友好的形态——隐藏 5xx 的内部细节与堆栈（防泄露），还特别照顾 ClickHouse 的<strong>资源类错误</strong>（内存超限、查询超时），
把它们映射成 <code>UNPROCESSABLE_CONTENT</code> 并附上「换个更小的时间范围试试」之类的<strong>可操作建议</strong>。于是无论哪个路由、查崩了什么，用户看到的都是一致、可读、不暴露内幕的错误。</p>
""")

# (context + RBAC section below)

_ZH21.append(r"""
<h2>一次 UI 查询的旅程，与 RBAC 的关键一招</h2>
<p>把这套骨架放进真实数据流里看。UI 里一个 React Query 钩子（如 <code>api.traces.all.useQuery</code>）发起调用，经过统一入口 <code>pages/api/trpc/[trpc].ts</code>，
先由 <code>createTRPCContext</code> 注入<strong>上下文</strong>——把 <code>{ session, headers, prisma }</code> 挂上每个请求（session 来自 NextAuth）；再走中间件栈，最后到路由的 resolver，
调 <code>@langfuse/shared</code> 的仓储/服务读 ClickHouse/Postgres：</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="UI React Query 钩子经 trpc 入口、context 注入、中间件栈、路由 resolver、调用 shared 仓储读 ClickHouse/Postgres">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一次 tRPC 查询从前端到数据库</text>
  <rect x="14" y="48" width="116" height="50" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="72" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">UI 钩子</text><text x="72" y="83" text-anchor="middle" font-size="7" fill="var(--muted)">api.traces.all.useQuery</text>
  <rect x="148" y="48" width="116" height="50" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="206" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">tRPC 入口</text><text x="206" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">[trpc].ts + context</text><text x="206" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">注入 session/prisma</text>
  <rect x="282" y="48" width="116" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="340" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">中间件栈</text><text x="340" y="78" text-anchor="middle" font-size="7" fill="var(--accent-ink)">OTel→错误→鉴权</text><text x="340" y="90" text-anchor="middle" font-size="7" fill="var(--accent-ink)">RBAC 在此把守</text>
  <rect x="416" y="48" width="116" height="50" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="474" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">路由 resolver</text><text x="474" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">traceRouter.all</text><text x="474" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">(64 个路由之一)</text>
  <rect x="550" y="48" width="156" height="50" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="628" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">shared 仓储/服务</text><text x="628" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">@langfuse/shared</text><text x="628" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">→ ClickHouse / Postgres</text>
  <line x1="130" y1="73" x2="146" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="146,73 138,69 138,77" fill="var(--faint)"/>
  <line x1="264" y1="73" x2="280" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="280,73 272,69 272,77" fill="var(--faint)"/>
  <line x1="398" y1="73" x2="414" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="414,73 406,69 406,77" fill="var(--faint)"/>
  <line x1="532" y1="73" x2="548" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="548,73 540,69 540,77" fill="var(--faint)"/>
  <text x="360" y="130" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">类型贯穿全链路：resolver 的返回类型，前端 useQuery 拿到时即已知</text>
  <text x="360" y="150" text-anchor="middle" font-size="8" fill="var(--muted)">改后端字段 → 前端编译即报错，这是 tRPC 相对 REST 的最大不同</text>
  <rect x="150" y="166" width="420" height="26" rx="7" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="183" text-anchor="middle" font-size="8" fill="var(--faint)">仓储层、过滤、读模型的细节 → 第 22–25 课</text>
</svg>
<div class="figcap"><b>从钩子到数据库</b>：<code>createTRPCContext</code>（trpc.ts:57）把 <code>{session, headers, prisma}</code> 注入每个请求；中间件栈把守鉴权/RBAC；resolver 调 <code>@langfuse/shared</code> 仓储读库。返回<strong>类型一路贯穿到前端</strong>。源码：<code>root.ts:70</code>（appRouter 聚合 ~64 路由）。</div>
</div>

<p>那个被注入每个请求的 <strong>context</strong> 看似不起眼，却是整套机制的地基——它把「这次请求是谁、带了什么、能用哪些工具」一次性备齐：</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">session</span><span class="name">你是谁（NextAuth）</span></div><div class="ld">当前登录用户及其<strong>「组织 → 项目」成员树</strong>。RBAC 中间件正是查这棵树，判断你能否访问某个 project——身份信息<strong>随 session 一起到</strong>，不必每次查库。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">headers</span><span class="name">这次请求带了什么</span></div><div class="ld">原始请求头，供<strong>限流</strong>、<strong>追踪</strong>、<strong>特性标志</strong>等横切关注点使用——比如根据来源限速、或把请求关联到一条 OTel trace。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">prisma</span><span class="name">能用哪些工具</span></div><div class="ld">Postgres 客户端（第 9 课），让 resolver 与中间件能读控制面数据（如 admin 兜底查 project 的归属组织）。ClickHouse 则由仓储层按需取（第 22 课）。</div></div>
</div>

<p>RBAC 最关键的一招，藏在 <code>enforceUserIsAuthedAndProjectMember</code> 里：它不等 resolver 跑，而是<strong>在中间件阶段就从请求输入里把 <code>projectId</code> 抠出来</strong>，
再去 session 里查「你是不是这个 project 的成员」。这样一来，<strong>每个受保护路由都自动获得统一的租户校验</strong>，无需各写一遍，也不会因为某个路由作者一时疏忽而留下后门（呼应第 10 课「project_id 是隔离键」）：</p>

<svg viewBox="0 0 720 220" role="img" aria-label="RBAC 中间件在 resolver 之前把守：从请求原始输入抠出 projectId，再到 session 的组织到项目成员树里查你是不是该 project 成员，是成员或 admin 则放行去 resolver 读库，否则抛 403 FORBIDDEN，每个受保护路由因此自动获得统一租户校验">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="16" y="86" width="140" height="48" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="86" y="106" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">请求输入</text>
  <text x="86" y="123" font-size="10" text-anchor="middle" fill="var(--muted)">{ projectId, … }</text>
  <line x1="156" y1="110" x2="196" y2="110" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="196" y="36" width="250" height="150" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="321" y="58" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">RBAC 中间件（resolver 之前）</text>
  <text x="210" y="84" font-size="10" fill="var(--ink)">① 抠出 projectId（parse 原始输入）</text>
  <text x="210" y="108" font-size="10" fill="var(--ink)">② 查 session 的 组织→项目 成员树</text>
  <text x="210" y="140" font-size="10.5" font-weight="700" fill="var(--accent-ink)">③ 是成员 或 admin？</text>
  <text x="210" y="164" font-size="9" fill="var(--muted)">每个受保护路由自动统一校验</text>
  <rect x="476" y="36" width="228" height="52" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="590" y="58" font-size="10" text-anchor="middle" fill="var(--accent-ink)">session.user.organizations</text>
  <text x="590" y="76" font-size="9.5" text-anchor="middle" fill="var(--muted)">.flatMap(projects).find(id)</text>
  <line x1="446" y1="108" x2="476" y2="68" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <rect x="476" y="104" width="228" height="40" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="590" y="129" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">✓ 放行 → resolver 读库</text>
  <line x1="446" y1="138" x2="476" y2="124" stroke="var(--teal)" stroke-width="2"></line>
  <rect x="476" y="156" width="228" height="40" rx="8" fill="var(--bg)" stroke="var(--accent)"></rect>
  <text x="590" y="181" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">✗ throw 403 FORBIDDEN</text>
  <line x1="446" y1="152" x2="476" y2="176" stroke="var(--accent)" stroke-width="2"></line>
</svg>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/api/trpc.ts</span><span class="ln">enforceUserIsAuthedAndProjectMember :288</span></div>
  <pre class="code"><span class="kw">const</span> enforceUserIsAuthedAndProjectMember = t.<span class="fn">middleware</span>(<span class="kw">async</span> (opts) =&gt; {
  <span class="kw">if</span> (!ctx.session?.user) <span class="kw">throw new</span> TRPCError({ code: <span class="st">"UNAUTHORIZED"</span> });

  <span class="cm">// 关键：在 resolver 之前，就从原始输入里取出 projectId</span>
  <span class="kw">const</span> input = inputProjectSchema.<span class="fn">parse</span>(<span class="kw">await</span> opts.<span class="fn">getRawInput</span>());

  <span class="cm">// 在 session 的「组织 → 项目」树里找：你是这个 project 的成员吗？</span>
  <span class="kw">const</span> member = ctx.session.user.organizations
    .<span class="fn">flatMap</span>((org) =&gt; org.projects)
    .<span class="fn">find</span>((p) =&gt; p.id === input.projectId);
  <span class="kw">if</span> (!member &amp;&amp; !ctx.session.user.admin) <span class="kw">throw new</span> TRPCError({ code: <span class="st">"FORBIDDEN"</span> });
  <span class="kw">return</span> next({ <span class="cm">/* 把校验过的 scope 挂进 ctx */</span> });
});</pre>
</div>

<table class="t">
  <tr><th>procedure</th><th>叠了哪些关卡</th><th>用在哪</th></tr>
  <tr><td><code>publicProcedure</code></td><td>OTel + 错误处理</td><td>无需登录（健康检查、公开分享）</td></tr>
  <tr><td><code>authenticatedProcedure</code></td><td>+ 登录校验</td><td>账号级、跨项目操作</td></tr>
  <tr><td><code>protectedProjectProcedure</code></td><td>+ <strong>项目成员 RBAC</strong></td><td><strong>绝大多数业务路由</strong>（traces/scores/…）</td></tr>
  <tr><td><code>protectedOrganizationProcedure</code></td><td>+ 组织成员校验</td><td>组织级管理</td></tr>
  <tr><td><code>protectedGetTraceProcedure</code></td><td>+ trace 访问校验（含公开 trace）</td><td>单条 trace 读取（允许公开分享）</td></tr>
</table>

<div class="cols">
  <div class="col"><h4>😖 假如每个路由各写鉴权</h4><p>64 个路由各自手写「检查登录、检查项目成员」。只要有一个人忘了写、或写得不一致，那一处就成了<strong>租户隔离的破口</strong>——别的项目的数据可能被读走。安全代码最怕这种「一处疏漏」。</p></div>
  <div class="col"><h4>😀 收敛成中间件 + procedure</h4><p>校验写一次、测一次，路由作者只需<strong>选对那道门</strong>（<code>protectedProjectProcedure</code>），RBAC 就自动统一生效。新增路由几乎<strong>不可能漏掉</strong>租户校验——安全靠结构兜底。</p></div>
</div>
""")

# (spark + key below)

_ZH21.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么把鉴权做成「中间件 + procedure 构建器」，而不是在每个路由里各写一遍 if 判断？</strong> 因为<strong>安全代码最怕「漏写」和「写歪」</strong>。
  如果 64 个路由各自手写「检查登录、检查项目成员」，迟早有人会忘掉一处、或写得不一致——而那一处就是租户隔离的破口。把校验<strong>收敛成几个中间件</strong>、
  再用 procedure 构建器<strong>声明式地组合</strong>，路由作者只需选对「门」（<code>protectedProjectProcedure</code>），RBAC 就<strong>自动、统一</strong>地生效。
  更妙的是「<strong>从输入里取 projectId</strong>」这一招：它让校验<strong>先于业务逻辑</strong>发生，任何受保护路由都不可能在没核验租户的情况下碰到数据。
  这正是第 6 课「把复杂度收敛到一处能严格测试的地方」、第 10 课「project_id 是隔离键」在 API 层的落地——<strong>安全靠结构保证，而非靠每个人自觉。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>tRPC 是 UI↔后端的<strong>类型安全契约</strong>：一个根路由 <code>appRouter</code>（<code>root.ts:70</code>）聚合约 64 个功能路由，返回类型一路贯穿到前端。</li>
    <li><strong>context</strong>（<code>createTRPCContext</code>）给每个请求注入 <code>{ session, headers, prisma }</code>；session 来自 NextAuth。</li>
    <li><strong>procedure = 可叠加的中间件栈</strong>：<code>publicProcedure</code>(OTel+错误处理) → <code>authenticatedProcedure</code>(+登录) → <code>protectedProjectProcedure</code>(+项目 RBAC)。</li>
    <li><strong>RBAC 关键招</strong>：<code>enforceUserIsAuthedAndProjectMember</code> 在中间件阶段从输入取 <code>projectId</code>、校验 session 成员资格——统一、先于 resolver（呼应第 10 课）。</li>
    <li>取舍：把鉴权收敛成中间件 + 声明式 procedure，避免 64 个路由各写各错；<strong>安全靠结构保证、而非靠人人自觉</strong>（第 6 课）。错误处理还会把 ClickHouse 资源错误翻成友好提示。</li>
  </ul>
</div>
""")

_EN21.append(r"""
<p class="lead">
Last lesson named the three doors; this one pushes open the "staff entrance" — <strong>tRPC</strong> — and shows its skeleton. tRPC is the <strong>type-safe
contract</strong> between UI and server: types the backend defines flow <strong>end to end</strong> to the frontend caller, so a change in one place errors the
whole chain instantly. Its structure is surprisingly lean: one <strong>root router</strong> aggregates ~64 feature routers, plus a handful of <strong>"procedure
builders"</strong> that guard auth and RBAC uniformly via <strong>layered middleware</strong>. Grasp this middleware stack and you grasp the security and the flow
of Langfuse's entire UI backend.
</p>

<div class="card analogy">
  <div class="tag">🛂 Analogy</div>
  Think of each tRPC request as walking a <strong>security corridor</strong>. The checkpoints along it are the <strong>middleware</strong>: first a <strong>camera</strong>
  logs that you came (OTel tracing), then a <strong>responder</strong> stands ready to catch exceptions (error handling), then an <strong>ID check</strong> (are you
  logged in), and finally the <strong>guest list</strong> (are you on the access list for <strong>this room</strong> — i.e. "are you a member of this project").
  Different doors (procedures) carry different numbers of checkpoints: a public door passes only the first two, a protected door walks them all. <strong>Define a
  checkpoint once, each door picks what it needs</strong> — that's the essence of procedure builders.
</div>
""")

_EN21.append(r"""
<h2>A procedure = a stackable middleware chain</h2>
<p>The essence of tRPC: <strong>a procedure is built by stacking middleware</strong>. Each middleware does one thing, chained in <code>.use()</code> order; different
procedure builders stack different checkpoints. Langfuse defines a set in <code>web/src/server/api/trpc.ts</code>: from the bare-bones <code>publicProcedure</code> to
the layered <code>protectedProjectProcedure</code>.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="procedure middleware stack: publicProcedure has OTel tracing and error handling, authenticatedProcedure adds a login check, protectedProjectProcedure adds project-member RBAC">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Procedure builders: stacking middleware, layer by layer</text>
  <rect x="20" y="40" width="216" height="170" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="128" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">publicProcedure</text>
  <rect x="36" y="72" width="184" height="28" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="128" y="90" text-anchor="middle" font-size="8" fill="var(--ink)">① OTel tracing</text>
  <rect x="36" y="106" width="184" height="28" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="128" y="124" text-anchor="middle" font-size="8" fill="var(--ink)">② error handling</text>
  <text x="128" y="160" text-anchor="middle" font-size="7.5" fill="var(--muted)">anyone can call</text><text x="128" y="174" text-anchor="middle" font-size="7.5" fill="var(--muted)">(e.g. health check)</text>
  <rect x="252" y="40" width="216" height="170" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">authenticatedProcedure</text>
  <rect x="268" y="72" width="184" height="24" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="88" text-anchor="middle" font-size="7.5" fill="var(--ink)">① OTel ② error handling</text>
  <rect x="268" y="102" width="184" height="32" rx="5" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="118" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">③ are you logged in</text><text x="360" y="129" text-anchor="middle" font-size="7" fill="var(--accent-ink)">enforceUserIsAuthed</text>
  <text x="360" y="164" text-anchor="middle" font-size="7.5" fill="var(--muted)">login required</text><text x="360" y="178" text-anchor="middle" font-size="7.5" fill="var(--muted)">(account-level ops)</text>
  <rect x="484" y="40" width="216" height="170" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="592" y="60" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">protectedProjectProcedure</text>
  <rect x="500" y="72" width="184" height="24" rx="5" fill="var(--bg)" stroke="var(--blue)"/><text x="592" y="88" text-anchor="middle" font-size="7.5" fill="var(--ink)">① OTel ② error handling</text>
  <rect x="500" y="102" width="184" height="44" rx="5" fill="var(--bg)" stroke="var(--accent)"/><text x="592" y="120" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">③ member of this project?</text><text x="592" y="133" text-anchor="middle" font-size="7" fill="var(--accent-ink)">pull projectId from input + check</text>
  <text x="592" y="166" text-anchor="middle" font-size="7.5" fill="var(--muted)">most business routers</text><text x="592" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">(traces/scores/…)</text>
  <text x="360" y="222" text-anchor="middle" font-size="8.5" fill="var(--faint)">more checkpoints to the right: define middleware once, each door .use()s what it needs — no per-router RBAC rewrite</text>
</svg>
<div class="figcap"><b>Layered middleware, composed on demand</b>: <code>publicProcedure</code>(OTel+error) → <code>authenticatedProcedure</code>(+login) → <code>protectedProjectProcedure</code>(+project-member RBAC). Plus variants <code>protectedOrganizationProcedure</code>, <code>protectedGetTraceProcedure</code>. Source: <code>web/src/server/api/trpc.ts:238-583</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/api/trpc.ts</span><span class="ln">procedure builders</span></div>
  <pre class="code"><span class="kw">const</span> withOtelTracingProcedure = t.procedure.<span class="fn">use</span>(withOtelInstrumentation);

<span class="cm">// public: only OTel + error handling</span>
<span class="kw">export const</span> publicProcedure = withOtelTracingProcedure.<span class="fn">use</span>(withErrorHandling);

<span class="cm">// authenticated: add a "are you logged in" layer</span>
<span class="kw">export const</span> authenticatedProcedure = withOtelTracingProcedure
  .<span class="fn">use</span>(withErrorHandling).<span class="fn">use</span>(enforceUserIsAuthed);

<span class="cm">// protected (project-level): add "are you a member of this project" — the most used</span>
<span class="kw">export const</span> protectedProjectProcedure = withOtelTracingProcedure
  .<span class="fn">use</span>(withErrorHandling).<span class="fn">use</span>(enforceUserIsAuthedAndProjectMember);</pre>
</div>

<p>Note the first two layers every door stacks — <strong>OTel tracing</strong> and <strong>error handling</strong> — are the common base of <strong>all</strong>
procedures. The error-handling layer (<code>withErrorHandling</code>) is especially careful: it <strong>uniformly translates</strong> resolver exceptions into a
frontend-friendly form — hiding 5xx internal detail and stacks (no leaks), and specially caring for ClickHouse <strong>resource errors</strong> (out-of-memory,
query timeout), mapping them to <code>UNPROCESSABLE_CONTENT</code> with <strong>actionable advice</strong> like "try a smaller time range". So whatever router,
whatever blew up, the user sees a consistent, readable error that doesn't expose the internals.</p>
""")

_EN21.append(r"""
<h2>A UI query's journey, and RBAC's key move</h2>
<p>Put this skeleton into a real data flow. A React Query hook in the UI (e.g. <code>api.traces.all.useQuery</code>) fires a call, through the unified entry
<code>pages/api/trpc/[trpc].ts</code>; first <code>createTRPCContext</code> injects the <strong>context</strong> — attaching <code>{ session, headers, prisma }</code>
to every request (session from NextAuth); then the middleware stack runs, finally reaching the router's resolver, which calls a <code>@langfuse/shared</code>
repository/service to read ClickHouse/Postgres:</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="UI React Query hook through the trpc entry, context injection, middleware stack, router resolver, calling shared repositories to read ClickHouse/Postgres">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">One tRPC query from frontend to database</text>
  <rect x="14" y="48" width="116" height="50" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="72" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">UI hook</text><text x="72" y="83" text-anchor="middle" font-size="7" fill="var(--muted)">api.traces.all.useQuery</text>
  <rect x="148" y="48" width="116" height="50" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="206" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">tRPC entry</text><text x="206" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">[trpc].ts + context</text><text x="206" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">inject session/prisma</text>
  <rect x="282" y="48" width="116" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="340" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">middleware stack</text><text x="340" y="78" text-anchor="middle" font-size="7" fill="var(--accent-ink)">OTel→error→auth</text><text x="340" y="90" text-anchor="middle" font-size="7" fill="var(--accent-ink)">RBAC guards here</text>
  <rect x="416" y="48" width="116" height="50" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="474" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">router resolver</text><text x="474" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">traceRouter.all</text><text x="474" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">(one of ~64 routers)</text>
  <rect x="550" y="48" width="156" height="50" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="628" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">shared repo/service</text><text x="628" y="78" text-anchor="middle" font-size="7" fill="var(--muted)">@langfuse/shared</text><text x="628" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">→ ClickHouse / Postgres</text>
  <line x1="130" y1="73" x2="146" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="146,73 138,69 138,77" fill="var(--faint)"/>
  <line x1="264" y1="73" x2="280" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="280,73 272,69 272,77" fill="var(--faint)"/>
  <line x1="398" y1="73" x2="414" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="414,73 406,69 406,77" fill="var(--faint)"/>
  <line x1="532" y1="73" x2="548" y2="73" stroke="var(--faint)" stroke-width="1.5"/><polygon points="548,73 540,69 540,77" fill="var(--faint)"/>
  <text x="360" y="130" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">Types thread the whole chain: the resolver's return type is known when useQuery receives it</text>
  <text x="360" y="150" text-anchor="middle" font-size="8" fill="var(--muted)">change a backend field → the frontend errors at compile time — tRPC's biggest difference from REST</text>
  <rect x="150" y="166" width="420" height="26" rx="7" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="183" text-anchor="middle" font-size="8" fill="var(--faint)">repository, filtering, read-model details → Lessons 22–25</text>
</svg>
<div class="figcap"><b>From hook to database</b>: <code>createTRPCContext</code> (trpc.ts:57) injects <code>{session, headers, prisma}</code> into every request; the middleware stack guards auth/RBAC; the resolver calls a <code>@langfuse/shared</code> repository. The return <strong>type threads all the way to the frontend</strong>. Source: <code>root.ts:70</code> (appRouter aggregates ~64 routers).</div>
</div>

<p>That <strong>context</strong> injected into every request looks unremarkable but is the bedrock — it gathers, in one shot, "who is this request, what did it
carry, what tools may it use":</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">session</span><span class="name">who you are (NextAuth)</span></div><div class="ld">The current logged-in user and their <strong>"organization → project" membership tree</strong>. The RBAC middleware reads exactly this tree to decide whether you can access a project — identity <strong>arrives with the session</strong>, no per-request DB lookup.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">headers</span><span class="name">what the request carried</span></div><div class="ld">Raw request headers, used by cross-cutting concerns like <strong>rate limiting</strong>, <strong>tracing</strong>, <strong>feature flags</strong> — e.g. rate-limit by source, or tie the request to an OTel trace.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">prisma</span><span class="name">what tools you may use</span></div><div class="ld">The Postgres client (Lesson 9), letting resolvers and middleware read control-plane data (e.g. the admin fallback looking up a project's owning org). ClickHouse is fetched on demand by the repository layer (Lesson 22).</div></div>
</div>

<p>RBAC's key move hides in <code>enforceUserIsAuthedAndProjectMember</code>: rather than waiting for the resolver, it <strong>pulls <code>projectId</code> out of the
request input at the middleware stage</strong>, then checks the session for "are you a member of this project". This way <strong>every protected router gets uniform
tenant checking automatically</strong>, never re-written per router, and no backdoor left by one router author's lapse (echoing Lesson 10's "project_id is the
isolation key"):</p>

<svg viewBox="0 0 720 220" role="img" aria-label="the RBAC middleware guards before the resolver: it pulls projectId out of the request raw input, then looks it up in the session's organization-to-project membership tree; if you are a member or an admin it proceeds to the resolver to read the DB, otherwise it throws 403 FORBIDDEN, so every protected router gets uniform tenant checking automatically">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="16" y="86" width="140" height="48" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="86" y="106" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">request input</text>
  <text x="86" y="123" font-size="10" text-anchor="middle" fill="var(--muted)">{ projectId, … }</text>
  <line x1="156" y1="110" x2="196" y2="110" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="196" y="36" width="250" height="150" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="321" y="58" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">RBAC middleware (before resolver)</text>
  <text x="210" y="84" font-size="10" fill="var(--ink)">1 pull projectId (parse raw input)</text>
  <text x="210" y="108" font-size="10" fill="var(--ink)">2 look up in session org→project tree</text>
  <text x="210" y="140" font-size="10.5" font-weight="700" fill="var(--accent-ink)">3 member or admin?</text>
  <text x="210" y="164" font-size="9" fill="var(--muted)">every protected router, checked uniformly</text>
  <rect x="476" y="36" width="228" height="52" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="590" y="58" font-size="10" text-anchor="middle" fill="var(--accent-ink)">session.user.organizations</text>
  <text x="590" y="76" font-size="9.5" text-anchor="middle" fill="var(--muted)">.flatMap(projects).find(id)</text>
  <line x1="446" y1="108" x2="476" y2="68" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <rect x="476" y="104" width="228" height="40" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="590" y="129" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">✓ proceed → resolver reads DB</text>
  <line x1="446" y1="138" x2="476" y2="124" stroke="var(--teal)" stroke-width="2"></line>
  <rect x="476" y="156" width="228" height="40" rx="8" fill="var(--bg)" stroke="var(--accent)"></rect>
  <text x="590" y="181" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">✗ throw 403 FORBIDDEN</text>
  <line x1="446" y1="152" x2="476" y2="176" stroke="var(--accent)" stroke-width="2"></line>
</svg>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/api/trpc.ts</span><span class="ln">enforceUserIsAuthedAndProjectMember :288</span></div>
  <pre class="code"><span class="kw">const</span> enforceUserIsAuthedAndProjectMember = t.<span class="fn">middleware</span>(<span class="kw">async</span> (opts) =&gt; {
  <span class="kw">if</span> (!ctx.session?.user) <span class="kw">throw new</span> TRPCError({ code: <span class="st">"UNAUTHORIZED"</span> });

  <span class="cm">// key: pull projectId out of the raw input, before the resolver</span>
  <span class="kw">const</span> input = inputProjectSchema.<span class="fn">parse</span>(<span class="kw">await</span> opts.<span class="fn">getRawInput</span>());

  <span class="cm">// search the session's "org → project" tree: are you a member of this project?</span>
  <span class="kw">const</span> member = ctx.session.user.organizations
    .<span class="fn">flatMap</span>((org) =&gt; org.projects)
    .<span class="fn">find</span>((p) =&gt; p.id === input.projectId);
  <span class="kw">if</span> (!member &amp;&amp; !ctx.session.user.admin) <span class="kw">throw new</span> TRPCError({ code: <span class="st">"FORBIDDEN"</span> });
  <span class="kw">return</span> next({ <span class="cm">/* attach the verified scope to ctx */</span> });
});</pre>
</div>

<table class="t">
  <tr><th>procedure</th><th>checkpoints stacked</th><th>used where</th></tr>
  <tr><td><code>publicProcedure</code></td><td>OTel + error handling</td><td>no login (health check, public share)</td></tr>
  <tr><td><code>authenticatedProcedure</code></td><td>+ login check</td><td>account-level, cross-project ops</td></tr>
  <tr><td><code>protectedProjectProcedure</code></td><td>+ <strong>project-member RBAC</strong></td><td><strong>most business routers</strong> (traces/scores/…)</td></tr>
  <tr><td><code>protectedOrganizationProcedure</code></td><td>+ org-member check</td><td>org-level admin</td></tr>
  <tr><td><code>protectedGetTraceProcedure</code></td><td>+ trace-access check (incl. public traces)</td><td>single-trace reads (allows public share)</td></tr>
</table>

<div class="cols">
  <div class="col"><h4>😖 if each router wrote its own auth</h4><p>64 routers each hand-write "check login, check project membership". One person forgetting it, or writing it inconsistently, and that spot becomes a <strong>tenant-isolation breach</strong> — another project's data could be read. Security code dreads exactly this "single omission".</p></div>
  <div class="col"><h4>😀 converged into middleware + procedure</h4><p>The check is written once, tested once; a router author just <strong>picks the right door</strong> (<code>protectedProjectProcedure</code>) and RBAC applies automatically and uniformly. A new router can <strong>hardly miss</strong> tenant checking — security backstopped by structure.</p></div>
</div>
""")

_EN21.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why make auth a "middleware + procedure builder" rather than an if-check hand-written in each router?</strong> Because <strong>security code most fears
  "omission" and "drift"</strong>. If 64 routers each hand-write "check login, check project membership", sooner or later someone forgets one, or writes it
  inconsistently — and that one spot is a hole in tenant isolation. Converging the checks into a <strong>few middleware</strong>, then composing them
  <strong>declaratively</strong> via procedure builders, means a router author only picks the right "door" (<code>protectedProjectProcedure</code>) and RBAC takes
  effect <strong>automatically and uniformly</strong>. Even better is the "<strong>pull projectId from the input</strong>" move: it makes the check happen
  <strong>before</strong> business logic, so no protected router can ever touch data without verifying the tenant first. This is Lesson 6's "converge complexity
  into one strictly testable place" and Lesson 10's "project_id is the isolation key" landing at the API layer — <strong>security guaranteed by structure, not by
  everyone's diligence.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>tRPC is the <strong>type-safe contract</strong> between UI and backend: one root router <code>appRouter</code> (<code>root.ts:70</code>) aggregates ~64 feature routers, the return type threading to the frontend.</li>
    <li><strong>context</strong> (<code>createTRPCContext</code>) injects <code>{ session, headers, prisma }</code> into every request; session from NextAuth.</li>
    <li><strong>A procedure = a stackable middleware chain</strong>: <code>publicProcedure</code>(OTel+error) → <code>authenticatedProcedure</code>(+login) → <code>protectedProjectProcedure</code>(+project RBAC).</li>
    <li><strong>RBAC's key move</strong>: <code>enforceUserIsAuthedAndProjectMember</code> pulls <code>projectId</code> from the input at the middleware stage and checks session membership — uniform, before the resolver (echoing Lesson 10).</li>
    <li>Tradeoff: converging auth into middleware + declarative procedures avoids 64 routers each writing (and mis-writing) it; <strong>security guaranteed by structure</strong> (Lesson 6). The error layer also turns ClickHouse resource errors into friendly advice.</li>
  </ul>
</div>
""")
LESSON_21 = {"zh": "\n".join(_ZH21), "en": "\n".join(_EN21)}


# ══════════════════════════════════════════════════════════════════════
# L22 · 仓储层：从 ClickHouse 读 / The repository layer
# ══════════════════════════════════════════════════════════════════════
_ZH22 = []
_EN22 = []

_ZH22.append(r"""
<p class="lead">
上一课结束在「resolver 调 <code>@langfuse/shared</code> 的仓储读库」。这一课就推开<strong>仓储层</strong>那扇门，看它怎么从 ClickHouse 把数据捞出来。核心是一条纪律：
<strong>所有分析查询都汇到同一个执行器</strong>——<code>queryClickhouse()</code>。它给每条查询<strong>统一</strong>套上：OTel 追踪、查询<strong>标签</strong>、失败<strong>退避重试</strong>、
资源错误<strong>友好包装</strong>。再加上一个让跨表 JOIN 变得便宜的关键技巧——<strong>回看时间窗</strong>。看懂这一层，就看懂了 Langfuse 所有读取的「总闸门」。
</p>

<div class="card analogy">
  <div class="tag">🏬 生活类比</div>
  把 ClickHouse 想成一个巨大的<strong>仓库</strong>。如果让每个工人（每段查询代码）<strong>各自闯进仓库</strong>乱翻，既没人记录谁拿了什么，出了乱子也无从追查。
  Langfuse 的做法是开<strong>唯一一个领料窗口</strong>（<code>queryClickhouse</code>）：所有人都从这儿递单子。窗口管理员会<strong>登记是谁来领的</strong>（查询标签）、<strong>给你贴张追踪票</strong>（OTel span）、
  <strong>货架一时占用就稍等再试</strong>（退避重试）；要是你一张单子想搬走整个仓库（内存超限），他不会让仓库塌掉，而是礼貌地退回一句「<strong>把范围缩小点再来</strong>」（资源错误）。
  一个窗口，把观测、追责、容错全管住了。
</div>
""")

# (L22 sections appended below)

_ZH22.append(r"""
<h2>唯一的领料窗口：queryClickhouse</h2>
<p>每段读取代码都不直接连 ClickHouse，而是把查询和一组<strong>标签</strong>交给 <code>queryClickhouse()</code>。它在真正发查询的外面，<strong>统一</strong>裹了好几层横切关注：</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="众多服务与路由都经 queryClickhouse 这一个执行器读 ClickHouse，沿途套上 OTel span、查询标签、退避重试、资源错误包装">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">所有读取汇到一个执行器</text>
  <rect x="20" y="46" width="120" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="67" text-anchor="middle" font-size="8" fill="var(--ink)">traces 服务</text>
  <rect x="20" y="86" width="120" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="107" text-anchor="middle" font-size="8" fill="var(--ink)">dashboard 引擎</text>
  <rect x="20" y="126" width="120" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="147" text-anchor="middle" font-size="8" fill="var(--ink)">public API</text>
  <rect x="20" y="166" width="120" height="34" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="187" text-anchor="middle" font-size="8" fill="var(--muted)">…几十处调用</text>
  <rect x="200" y="58" width="230" height="130" rx="12" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="315" y="80" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">queryClickhouse()</text>
  <rect x="216" y="92" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="106" text-anchor="middle" font-size="7.5" fill="var(--ink)">① OTel span（每条查询可追踪）</text>
  <rect x="216" y="116" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">② log_comment 标签（谁/哪个面/路由）</text>
  <rect x="216" y="140" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="154" text-anchor="middle" font-size="7.5" fill="var(--ink)">③ backOff 退避重试（网络抖动）</text>
  <rect x="216" y="164" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--accent)"/><text x="315" y="178" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">④ 资源错误友好包装</text>
  <rect x="488" y="92" width="120" height="56" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="548" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">ClickHouse</text><text x="548" y="132" text-anchor="middle" font-size="7" fill="var(--muted)">JSONEachRow</text>
  <rect x="488" y="158" width="120" height="42" rx="9" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="548" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">流式变体</text><text x="548" y="190" text-anchor="middle" font-size="6.8" fill="var(--muted)">Stream / WithProgress(SSE)</text>
  <line x1="140" y1="63" x2="198" y2="100" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="103" x2="198" y2="118" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="143" x2="198" y2="136" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="183" x2="198" y2="155" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="430" y1="120" x2="486" y2="120" stroke="var(--accent)" stroke-width="1.6"/><polygon points="486,120 477,116 477,124" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>一个窗口，四样统一</b>：<code>queryClickhouse()</code> 给每条查询裹上 OTel span、<code>log_comment</code> 标签、退避重试、资源错误包装，再发往 ClickHouse（大读走 <code>queryClickhouseStream</code>/<code>WithProgress</code>）。源码：<code>packages/shared/src/server/repositories/clickhouse.ts:639</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/repositories/clickhouse.ts</span><span class="ln">queryClickhouse :639</span></div>
  <pre class="code"><span class="kw">export async function</span> <span class="fn">queryClickhouse</span>&lt;T&gt;(opts) {
  <span class="fn">assertNoLegacyEventsRead</span>(opts.query);          <span class="cm">// 守卫：别读旧 events 表</span>
  <span class="kw">return await</span> <span class="fn">instrumentAsync</span>({ name: <span class="st">"clickhouse-query"</span> }, <span class="kw">async</span> (span) =&gt; {
    <span class="fn">setSpanQueryAttributes</span>(span, opts.query);        <span class="cm">// ① 把 SQL 挂到 OTel span</span>
    <span class="kw">return await</span> <span class="fn">backOff</span>(                          <span class="cm">// ③ 网络错可重试，指数退避</span>
      () =&gt; <span class="fn">sendClickhouseQuery</span>({ ...opts, span }),     <span class="cm">// ② 内部设 log_comment=JSON(tags)</span>
      { numOfAttempts, retry: isRetryableError },
    ).<span class="fn">catch</span>((e) =&gt; { <span class="kw">throw</span> ClickHouseResourceError.<span class="fn">wrapIfResourceError</span>(e, tags); });
  });                                                <span class="cm">// ④ 内存/超时 → 友好错误（第 21 课接住）</span>
}</pre>
</div>

<p>这四样里，<strong>查询标签</strong>尤其值得一提。<code>sendClickhouseQuery</code> 会把标签塞进 ClickHouse 的 <code>log_comment</code> 设置（即查询日志的注释字段）：
于是<strong>每一条打到 ClickHouse 的 SQL，都自带「是哪个 project、哪个面（UI/公共 API/worker）、哪个路由发起的」</strong>。当某条慢查询拖垮集群时，运维能直接在 ClickHouse 的查询日志里
按标签定位元凶——这是把<strong>可观测性焊进数据访问层</strong>的一招，散落各处的裸查询永远做不到。</p>

<p>同一个领料窗口还备了<strong>几种取货方式</strong>，应对不同读取场景——但它们共享同一套追踪/标签/重试机制：</p>

<svg viewBox="0 0 720 220" role="img" aria-label="一个 queryClickhouse 窗口三种取货方式：queryClickhouse 一次取回全部用于列表详情聚合、queryClickhouseStream 边读边吐用于批量导出内存有界、queryClickhouseWithProgress 带进度的流用于 SSE 流式仪表盘，三者共享 OTel span、log_comment 标签与退避重试">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="26" font-size="11.5" font-weight="700" fill="var(--accent-ink)">一个窗口，三种取货方式 —— 共享 OTel span · log_comment 标签 · 退避重试</text>
  <rect x="20" y="42" width="300" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="34" y="62" font-size="11" font-weight="700" fill="var(--accent-ink)">queryClickhouse</text>
  <text x="34" y="79" font-size="9.5" fill="var(--muted)">一次取回全部（结果读成数组）</text>
  <rect x="20" y="98" width="300" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="34" y="118" font-size="11" font-weight="700" fill="var(--accent-ink)">queryClickhouseStream</text>
  <text x="34" y="135" font-size="9.5" fill="var(--muted)">边读边吐（流式 · 内存有界）</text>
  <rect x="20" y="154" width="300" height="44" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="34" y="174" font-size="11" font-weight="700" fill="var(--accent-ink)">queryClickhouseWithProgress</text>
  <text x="34" y="191" font-size="9.5" fill="var(--muted)">带进度的流</text>
  <rect x="392" y="42" width="308" height="44" rx="8" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="406" y="69" font-size="10.5" fill="var(--ink)">列表 / 详情 / 聚合（装得下内存）</text>
  <rect x="392" y="98" width="308" height="44" rx="8" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="406" y="125" font-size="10.5" fill="var(--ink)">批量导出（结果可能巨大）</text>
  <rect x="392" y="154" width="308" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="406" y="181" font-size="10.5" fill="var(--ink)">SSE 流式仪表盘（边查边推进度）</text>
  <line x1="320" y1="64" x2="392" y2="64" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="320" y1="120" x2="392" y2="120" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="320" y1="176" x2="392" y2="176" stroke="var(--accent)" stroke-width="2"></line>
</svg>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">queryClickhouse</span><span class="name">一次取回全部</span></div><div class="ld">最常用：跑查询、把结果一次性读成数组返回。绝大多数列表、详情、聚合都走它。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">queryClickhouseStream</span><span class="name">边读边吐</span></div><div class="ld">大读不必把整个结果攒在内存里，而是<strong>流式</strong>一行行吐出——批量导出（第 12 课提过的导出）这类「结果可能巨大」的场景靠它，内存有界。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">queryClickhouseWithProgress</span><span class="name">带进度的流</span></div><div class="ld">给 <strong>SSE 流式仪表盘</strong>用：一边查一边把进度推给前端，让大仪表盘查询「有反馈、不假死」。</div></div>
</div>
""")

# (look-back windows section below)

_ZH22.append(r"""
<h2>回看时间窗：让跨表 JOIN 不再扫全表</h2>
<p>还记得第 8 课吗——trace、observation、score 是<strong>三张独立的宽表</strong>，彼此没有外键，而是靠<strong>时间</strong>关联。问题来了：要把一条 trace 的观测和评分拼起来，
难道要在动辄几个月、上亿行的 observations 表里全表搜一遍？那会慢到无法接受。仓储层的答案是<strong>回看时间窗</strong>：利用「一条 trace 的观测，几乎都集中在它发生后的一小段时间内」这个事实，
只在一个<strong>有界的时间范围</strong>里找。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="按 trace 时间戳划出有界回看窗：观测在 2 天内、评分在 1 小时内，只扫这几个分区而非全表">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">以 trace 时间戳为锚，只看有界的回看窗</text>
  <line x1="40" y1="86" x2="700" y2="86" stroke="var(--faint)" stroke-width="1.5"/><text x="690" y="80" text-anchor="end" font-size="7.5" fill="var(--faint)">时间 →</text>
  <circle cx="360" cy="86" r="6" fill="var(--accent)"/><text x="360" y="72" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">trace.timestamp（锚点）</text>
  <rect x="300" y="100" width="180" height="26" rx="5" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="390" y="117" text-anchor="middle" font-size="8" fill="var(--accent-ink)">观测窗：start_time ≥ 锚 − 2 天</text>
  <rect x="336" y="132" width="96" height="24" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="384" y="148" text-anchor="middle" font-size="7.5" fill="var(--ink)">评分窗：1 小时</text>
  <rect x="40" y="100" width="250" height="56" rx="6" fill="none" stroke="var(--faint)" stroke-dasharray="5 4"/><text x="165" y="122" text-anchor="middle" font-size="8" fill="var(--muted)">窗外：不扫</text><text x="165" y="138" text-anchor="middle" font-size="7" fill="var(--faint)">（几个月的旧分区被跳过）</text>
  <rect x="490" y="100" width="210" height="56" rx="6" fill="none" stroke="var(--faint)" stroke-dasharray="5 4"/><text x="595" y="122" text-anchor="middle" font-size="8" fill="var(--muted)">窗外：不扫</text>
  <text x="360" y="184" text-anchor="middle" font-size="8.5" fill="var(--faint)">OBSERVATIONS_TO_TRACE_INTERVAL=2 天 · SCORE_TO_TRACE_OBSERVATIONS_INTERVAL=1 小时</text>
</svg>
<div class="figcap"><b>有界回看，跳过旧分区</b>：以 trace 的 <code>timestamp</code> 为锚，观测只在 <code>start_time ≥ 锚 − 2 天</code> 内找、评分在 1 小时内找。这些常量被注入 WHERE 子句，配合第 8 课「按月分区」让 JOIN <strong>只碰几个分区</strong>。源码：<code>repositories/constants.ts:4,9</code>。</div>
</div>

<div class="cols">
  <div class="col"><h4>😖 不设窗：全表 JOIN</h4><p>为一条 trace 找观测，要在整张 observations 表（几个月、上亿行）里搜。每次列表查询都这样，集群很快被拖垮——这正是把分析库当事务库用的典型翻车。</p></div>
  <div class="col"><h4>😀 设回看窗：有界扫描</h4><p>把 <code>start_time ≥ trace.timestamp − 2 天</code> 注入 WHERE，配合按月分区，JOIN <strong>只读那几个相关分区</strong>。扫描量从「几个月」骤降到「两天」，查询飞快。</p></div>
</div>

<p>当然，窗也有代价：极少数<strong>跨度异常长</strong>的 observation（晚于 2 天才结束）可能落在窗外、被漏掉。这是一个<strong>有意识的取舍</strong>——
用「放过极长尾的一点点正确性」换「JOIN 不再扫全表」的巨大成本节省。Langfuse 据实测（约 96% 的观测在 trace 之后 2 分钟内开始）把窗设成 2 天，留足极大的安全裕量，几乎不会真漏。
<strong>正确性与成本之间，工程师按真实数据分布画了一条务实的线。</strong></p>
""")

# (spark + key below)

_ZH22.append(r"""
<table class="t">
  <tr><th>这一层加了什么</th><th>解决什么</th></tr>
  <tr><td><b>OTel span</b></td><td>每条查询可追踪、可看耗时——观测性焊进数据层</td></tr>
  <tr><td><b>log_comment 标签</b></td><td>每条 SQL 自带 project/面/路由，慢查询能在 CH 查询日志里按标签追责</td></tr>
  <tr><td><b>退避重试</b></td><td>网络抖动等可重试错误自动重试，不打扰调用方</td></tr>
  <tr><td><b>资源错误包装</b></td><td>内存/超时翻成友好的 <code>ClickHouseResourceError</code>，交第 21 课给出「缩小范围」建议</td></tr>
  <tr><td><b>回看时间窗</b></td><td>跨表 JOIN 只扫有界分区，把全表扫描挡在门外</td></tr>
  <tr><td><b>legacy 守卫 + 流式变体</b></td><td>禁读旧 events 表；大读用 Stream、SSE 仪表盘用 WithProgress</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么把所有读取硬挤到一个执行器里，而不是哪儿要查哪儿写 SQL？</strong> 因为<strong>横切关注最忌散落</strong>。可观测性、追责、重试、资源保护——这些和「业务查什么」无关、
  却每条查询都需要的能力，如果让一百处裸查询各自实现，必然有的写、有的漏、写法还不一致。收敛成<strong>一个执行器</strong>，它们就<strong>一次实现、处处生效</strong>：
  加一项能力（比如新的查询标签维度），全平台的查询<strong>一起获得</strong>。回看时间窗则是另一种智慧：它承认第 8 课「三张独立宽表、靠时间关联」的设计代价（JOIN 没有外键可走），
  并用「数据的真实时间局部性」把这个代价摊薄到几乎为零。<strong>一个总闸门管住所有共性，一条务实的时间线管住所有 JOIN</strong>——这就是仓储层的全部精髓。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>所有 ClickHouse 读取都汇到一个执行器 <code>queryClickhouse()</code>，沿途统一套上 <strong>OTel span、查询标签、退避重试、资源错误包装</strong>。</li>
    <li><strong>查询标签</strong>经 <code>log_comment</code> 进 ClickHouse 查询日志，每条 SQL 自带 project/面/路由——慢查询可按标签追责。</li>
    <li><strong>资源错误</strong>（内存/超时）被包装成 <code>ClickHouseResourceError</code>，交第 21 课的错误中间件翻成「缩小时间范围」的可操作建议。</li>
    <li><strong>回看时间窗</strong>：trace/observation/score 是三张独立宽表、靠时间关联；JOIN 时以 trace 时间戳为锚、只在 2 天（观测）/1 小时（评分）内找，避免全表扫描。</li>
    <li>取舍：横切能力收敛到一处「一次实现处处生效」；时间窗用「真实时间局部性」摊薄第 8 课分表的 JOIN 成本，以极小长尾正确性换巨大成本节省。</li>
  </ul>
</div>
""")

_EN22.append(r"""
<p class="lead">
The last lesson ended at "the resolver calls a <code>@langfuse/shared</code> repository to read". This lesson opens that <strong>repository layer</strong> door and
shows how it pulls data out of ClickHouse. The core is a discipline: <strong>every analytical query funnels through one executor</strong> —
<code>queryClickhouse()</code>. It <strong>uniformly</strong> wraps each query with OTel tracing, query <strong>tags</strong>, backoff <strong>retry</strong>, and
friendly resource-error <strong>wrapping</strong>. Plus a key trick that makes cross-table JOINs cheap — the <strong>look-back window</strong>. Get this layer and
you get the "master valve" for all of Langfuse's reads.
</p>

<div class="card analogy">
  <div class="tag">🏬 Analogy</div>
  Think of ClickHouse as a vast <strong>warehouse</strong>. If every worker (each piece of query code) <strong>barges into the warehouse</strong> to rummage on their
  own, nobody records who took what, and when things go wrong there's no trail. Langfuse instead opens <strong>one single dispatch window</strong>
  (<code>queryClickhouse</code>): everyone hands in their slip here. The clerk <strong>logs who's collecting</strong> (query tags), <strong>stamps a tracking
  ticket</strong> (OTel span), and <strong>waits and retries if a shelf is briefly busy</strong> (backoff). If your slip tries to haul off the whole warehouse
  (out of memory), the clerk won't let the warehouse collapse — they politely hand back "<strong>narrow it down and come again</strong>" (resource error). One
  window handles observability, accountability, and fault tolerance all at once.
</div>
""")

_EN22.append(r"""
<h2>The one dispatch window: queryClickhouse</h2>
<p>No reading code connects to ClickHouse directly; it hands the query and a set of <strong>tags</strong> to <code>queryClickhouse()</code>. Around the actual
query, it <strong>uniformly</strong> wraps several cross-cutting concerns:</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="many services and routers read ClickHouse through the one queryClickhouse executor, wrapped with OTel span, query tags, backoff retry, resource-error wrapping">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">All reads funnel into one executor</text>
  <rect x="20" y="46" width="120" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="67" text-anchor="middle" font-size="8" fill="var(--ink)">traces service</text>
  <rect x="20" y="86" width="120" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="107" text-anchor="middle" font-size="8" fill="var(--ink)">dashboard engine</text>
  <rect x="20" y="126" width="120" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="147" text-anchor="middle" font-size="8" fill="var(--ink)">public API</text>
  <rect x="20" y="166" width="120" height="34" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="187" text-anchor="middle" font-size="8" fill="var(--muted)">…dozens of callers</text>
  <rect x="200" y="58" width="230" height="130" rx="12" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="315" y="80" text-anchor="middle" font-size="10.5" font-weight="700" fill="var(--accent-ink)">queryClickhouse()</text>
  <rect x="216" y="92" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="106" text-anchor="middle" font-size="7.5" fill="var(--ink)">① OTel span (every query traceable)</text>
  <rect x="216" y="116" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="130" text-anchor="middle" font-size="7" fill="var(--ink)">② log_comment tags (who/surface/route)</text>
  <rect x="216" y="140" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="154" text-anchor="middle" font-size="7.5" fill="var(--ink)">③ backOff retry (network blips)</text>
  <rect x="216" y="164" width="198" height="20" rx="4" fill="var(--bg)" stroke="var(--accent)"/><text x="315" y="178" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">④ friendly resource-error wrap</text>
  <rect x="488" y="92" width="120" height="56" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="548" y="116" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">ClickHouse</text><text x="548" y="132" text-anchor="middle" font-size="7" fill="var(--muted)">JSONEachRow</text>
  <rect x="488" y="158" width="120" height="42" rx="9" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="548" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">streaming variants</text><text x="548" y="190" text-anchor="middle" font-size="6.6" fill="var(--muted)">Stream / WithProgress(SSE)</text>
  <line x1="140" y1="63" x2="198" y2="100" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="103" x2="198" y2="118" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="143" x2="198" y2="136" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="183" x2="198" y2="155" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="430" y1="120" x2="486" y2="120" stroke="var(--accent)" stroke-width="1.6"/><polygon points="486,120 477,116 477,124" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>One window, four things unified</b>: <code>queryClickhouse()</code> wraps each query with an OTel span, <code>log_comment</code> tags, backoff retry, and resource-error wrapping, then sends it to ClickHouse (big reads via <code>queryClickhouseStream</code>/<code>WithProgress</code>). Source: <code>packages/shared/src/server/repositories/clickhouse.ts:639</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/repositories/clickhouse.ts</span><span class="ln">queryClickhouse :639</span></div>
  <pre class="code"><span class="kw">export async function</span> <span class="fn">queryClickhouse</span>&lt;T&gt;(opts) {
  <span class="fn">assertNoLegacyEventsRead</span>(opts.query);          <span class="cm">// guard: don't read legacy events tables</span>
  <span class="kw">return await</span> <span class="fn">instrumentAsync</span>({ name: <span class="st">"clickhouse-query"</span> }, <span class="kw">async</span> (span) =&gt; {
    <span class="fn">setSpanQueryAttributes</span>(span, opts.query);        <span class="cm">// ① attach SQL to the OTel span</span>
    <span class="kw">return await</span> <span class="fn">backOff</span>(                          <span class="cm">// ③ retry retryable (network) errors</span>
      () =&gt; <span class="fn">sendClickhouseQuery</span>({ ...opts, span }),     <span class="cm">// ② sets log_comment=JSON(tags) inside</span>
      { numOfAttempts, retry: isRetryableError },
    ).<span class="fn">catch</span>((e) =&gt; { <span class="kw">throw</span> ClickHouseResourceError.<span class="fn">wrapIfResourceError</span>(e, tags); });
  });                                                <span class="cm">// ④ memory/timeout → friendly error (caught by L21)</span>
}</pre>
</div>

<p>Of these four, the <strong>query tags</strong> deserve a special mention. <code>sendClickhouseQuery</code> stuffs the tags into ClickHouse's
<code>log_comment</code> setting (the query log's comment field): so <strong>every SQL hitting ClickHouse carries "which project, which surface (UI/public
API/worker), which route initiated it"</strong>. When one slow query drags down the cluster, operators can locate the culprit by tag directly in ClickHouse's own
query log — a way to <strong>weld observability into the data-access layer</strong> that scattered raw queries can never achieve.</p>

<p>The same dispatch window also offers <strong>several pickup modes</strong> for different read scenarios — but they share the same tracing/tags/retry machinery:</p>

<svg viewBox="0 0 720 220" role="img" aria-label="one queryClickhouse window with three pickup modes: queryClickhouse fetches all at once for lists, detail and aggregations; queryClickhouseStream streams row by row for batch exports with bounded memory; queryClickhouseWithProgress is a progress-pushing stream for SSE dashboards; all three share OTel span, log_comment tags and backoff retry">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="26" font-size="11.5" font-weight="700" fill="var(--accent-ink)">one window, three pickup modes — sharing OTel span · log_comment tags · backoff retry</text>
  <rect x="20" y="42" width="300" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="34" y="62" font-size="11" font-weight="700" fill="var(--accent-ink)">queryClickhouse</text>
  <text x="34" y="79" font-size="9.5" fill="var(--muted)">fetch all at once (into an array)</text>
  <rect x="20" y="98" width="300" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="34" y="118" font-size="11" font-weight="700" fill="var(--accent-ink)">queryClickhouseStream</text>
  <text x="34" y="135" font-size="9.5" fill="var(--muted)">stream as it reads (bounded memory)</text>
  <rect x="20" y="154" width="300" height="44" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="34" y="174" font-size="11" font-weight="700" fill="var(--accent-ink)">queryClickhouseWithProgress</text>
  <text x="34" y="191" font-size="9.5" fill="var(--muted)">a progress-pushing stream</text>
  <rect x="392" y="42" width="308" height="44" rx="8" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="406" y="69" font-size="10.5" fill="var(--ink)">lists / detail / aggregations (fits memory)</text>
  <rect x="392" y="98" width="308" height="44" rx="8" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="406" y="125" font-size="10.5" fill="var(--ink)">batch exports (result may be huge)</text>
  <rect x="392" y="154" width="308" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="406" y="181" font-size="10.5" fill="var(--ink)">SSE dashboards (push progress live)</text>
  <line x1="320" y1="64" x2="392" y2="64" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="320" y1="120" x2="392" y2="120" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="320" y1="176" x2="392" y2="176" stroke="var(--accent)" stroke-width="2"></line>
</svg>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">queryClickhouse</span><span class="name">fetch all at once</span></div><div class="ld">The common case: run the query, read the whole result into an array, return. Most lists, details, aggregations go through it.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">queryClickhouseStream</span><span class="name">stream as it reads</span></div><div class="ld">Big reads needn't buffer the whole result in memory; they <strong>stream</strong> row by row — batch exports (the exports mentioned in L12) and other "result might be huge" cases use it, with bounded memory.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">queryClickhouseWithProgress</span><span class="name">streaming with progress</span></div><div class="ld">For <strong>SSE streaming dashboards</strong>: pushes progress to the frontend as it queries, so big dashboard queries "give feedback, don't freeze".</div></div>
</div>
""")

_EN22.append(r"""
<h2>Look-back windows: cross-table JOINs without full scans</h2>
<p>Remember Lesson 8 — trace, observation, score are <strong>three independent wide tables</strong>, with no foreign keys, correlated by <strong>time</strong>. The
problem: to stitch a trace's observations and scores together, must we full-scan an observations table of months and billions of rows? Unacceptably slow. The
repository layer's answer is the <strong>look-back window</strong>: exploiting the fact that "a trace's observations almost all cluster in a short window after it
happened", it searches only within a <strong>bounded time range</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="a bounded look-back window anchored at the trace timestamp: observations within 2 days, scores within 1 hour, scanning only those partitions not the whole table">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Anchored at the trace timestamp, only a bounded look-back window</text>
  <line x1="40" y1="86" x2="700" y2="86" stroke="var(--faint)" stroke-width="1.5"/><text x="690" y="80" text-anchor="end" font-size="7.5" fill="var(--faint)">time →</text>
  <circle cx="360" cy="86" r="6" fill="var(--accent)"/><text x="360" y="72" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">trace.timestamp (anchor)</text>
  <rect x="300" y="100" width="180" height="26" rx="5" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="390" y="117" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">obs window: start_time ≥ anchor − 2 days</text>
  <rect x="336" y="132" width="96" height="24" rx="5" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="384" y="148" text-anchor="middle" font-size="7.5" fill="var(--ink)">score window: 1 hour</text>
  <rect x="40" y="100" width="250" height="56" rx="6" fill="none" stroke="var(--faint)" stroke-dasharray="5 4"/><text x="165" y="122" text-anchor="middle" font-size="8" fill="var(--muted)">outside: not scanned</text><text x="165" y="138" text-anchor="middle" font-size="7" fill="var(--faint)">(months of old partitions skipped)</text>
  <rect x="490" y="100" width="210" height="56" rx="6" fill="none" stroke="var(--faint)" stroke-dasharray="5 4"/><text x="595" y="122" text-anchor="middle" font-size="8" fill="var(--muted)">outside: not scanned</text>
  <text x="360" y="184" text-anchor="middle" font-size="8.5" fill="var(--faint)">OBSERVATIONS_TO_TRACE_INTERVAL=2 days · SCORE_TO_TRACE_OBSERVATIONS_INTERVAL=1 hour</text>
</svg>
<div class="figcap"><b>Bounded look-back, skip old partitions</b>: anchored at the trace's <code>timestamp</code>, observations are found within <code>start_time ≥ anchor − 2 days</code>, scores within 1 hour. These constants are injected into WHERE clauses, with Lesson 8's monthly partitioning letting JOINs <strong>touch only a few partitions</strong>. Source: <code>repositories/constants.ts:4,9</code>.</div>
</div>

<div class="cols">
  <div class="col"><h4>😖 no window: full-table JOIN</h4><p>To find a trace's observations, search the whole observations table (months, billions of rows). Every list query doing this would soon drag the cluster down — the classic crash of using an analytical store like a transactional one.</p></div>
  <div class="col"><h4>😀 look-back window: bounded scan</h4><p>Inject <code>start_time ≥ trace.timestamp − 2 days</code> into WHERE, and with monthly partitioning the JOIN <strong>reads only those few relevant partitions</strong>. The scan shrinks from "months" to "two days" — queries fly.</p></div>
</div>

<p>The window has a cost, of course: a rare <strong>unusually long</strong> observation (ending more than 2 days late) could fall outside the window and be missed. This
is a <strong>deliberate trade-off</strong> — trading "letting go of a tiny long tail of correctness" for "JOINs no longer scanning the whole table". Based on measurement
(~96% of observations start within 2 minutes of the trace), Langfuse sets the window to 2 days, leaving a huge safety margin, so it almost never truly misses.
<strong>Between correctness and cost, engineers drew a pragmatic line by the real data distribution.</strong></p>

<table class="t">
  <tr><th>what this layer adds</th><th>what it solves</th></tr>
  <tr><td><b>OTel span</b></td><td>every query traceable, its latency visible — observability welded into the data layer</td></tr>
  <tr><td><b>log_comment tags</b></td><td>every SQL carries project/surface/route, so slow queries can be traced by tag in CH's query log</td></tr>
  <tr><td><b>backoff retry</b></td><td>retryable errors (network blips) auto-retry without bothering the caller</td></tr>
  <tr><td><b>resource-error wrapping</b></td><td>memory/timeout become a friendly <code>ClickHouseResourceError</code>, handed to L21 for "narrow it" advice</td></tr>
  <tr><td><b>look-back window</b></td><td>cross-table JOINs scan only bounded partitions, keeping full scans out</td></tr>
  <tr><td><b>legacy guard + streaming variants</b></td><td>forbids reading legacy events; big reads use Stream, SSE dashboards use WithProgress</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why cram all reads into one executor, instead of writing SQL wherever you need it?</strong> Because <strong>cross-cutting concerns most dread being
  scattered</strong>. Observability, accountability, retry, resource protection — capabilities unrelated to "what business queries" yet needed by every query — if
  a hundred raw queries each implement them, some will write them, some omit them, and inconsistently. Converge into <strong>one executor</strong> and they're
  <strong>implemented once, in effect everywhere</strong>: add a capability (say a new query-tag dimension) and every query platform-wide <strong>gains it
  together</strong>. The look-back window is another kind of wisdom: it accepts the cost of Lesson 8's "three independent wide tables, correlated by time" design
  (JOINs have no foreign key to follow), and uses "the data's real temporal locality" to amortize that cost to near zero. <strong>One master valve for all
  commonalities, one pragmatic timeline for all JOINs</strong> — that's the whole essence of the repository layer.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>All ClickHouse reads funnel into one executor <code>queryClickhouse()</code>, uniformly wrapped with <strong>OTel span, query tags, backoff retry, resource-error wrapping</strong>.</li>
    <li><strong>Query tags</strong> go via <code>log_comment</code> into ClickHouse's query log, so every SQL carries project/surface/route — slow queries traceable by tag.</li>
    <li><strong>Resource errors</strong> (memory/timeout) are wrapped into <code>ClickHouseResourceError</code>, handed to L21's error middleware for "narrow the time range" advice.</li>
    <li><strong>Look-back windows</strong>: trace/observation/score are three independent wide tables correlated by time; JOINs anchor at the trace timestamp and search only within 2 days (obs) / 1 hour (scores), avoiding full scans.</li>
    <li>Tradeoff: cross-cutting capabilities converge to one place "implemented once, everywhere"; the time window uses "real temporal locality" to amortize Lesson 8's split-table JOIN cost, trading a tiny long-tail of correctness for huge cost savings.</li>
  </ul>
</div>
""")
LESSON_22 = {"zh": "\n".join(_ZH22), "en": "\n".join(_EN22)}


# ══════════════════════════════════════════════════════════════════════
# L23 · 过滤·搜索栏·查询构建 / Filtering & the search bar
# ══════════════════════════════════════════════════════════════════════
_ZH23 = []
_EN23 = []

_ZH23.append(r"""
<p class="lead">
第 22 课的执行器负责「把查询发出去」，可<strong>那些查询的 WHERE 条件是谁拼的</strong>？这一课就讲过滤。关键洞察是：用户过滤的方式五花八门——点侧栏面板、敲搜索栏语法、甚至用 AI 自然语言描述——
但它们最终<strong>都汇成同一个 <code>FilterState</code></strong>（一组带类型的条件），再由它编译成<strong>参数化 SQL</strong>（ClickHouse 或 Postgres）。一个中间契约，
既挡住了 SQL 注入，又让搜索栏、AI filter 这些花样都<strong>构造即安全</strong>。
</p>

<div class="card analogy">
  <div class="tag">🌐 生活类比</div>
  把 <code>FilterState</code> 想成联合国的<strong>中间语</strong>。与会者说着不同的母语——有人<strong>点菜单</strong>（侧栏面板）、有人<strong>写电报</strong>（搜索栏 <code>key:value</code> 语法）、有人<strong>口述需求</strong>（AI 自然语言）——
  但所有发言都先被译成<strong>同一种标准中间语</strong>（FilterState），再由它译成数据库听得懂的话（ClickHouse SQL 或 Postgres SQL）。这个译员有两条铁律：
  一是<strong>绝不把原话直接塞进译文</strong>（用占位符传值，杜绝注入）；二是<strong>听不懂的、编不出的，当场打回，绝不胡乱转述</strong>（校验 + 往返丢弃幻觉）。<strong>所有输入收敛到一种中间表示，再分发到各种后端</strong>——这就是过滤系统的骨架。
</div>
""")

# (L23 sections appended below)

_ZH23.append(r"""
<h2>一个 FilterState，编译到两套 SQL</h2>
<p><code>FilterState</code> 是一组<strong>带类型的条件</strong>：每条说清「哪一列、什么运算符、什么值」（如 <code>{column:"level", operator:"any of", value:["ERROR"]}</code>）。
它要变成 SQL，得过一个工厂 <code>createFilterFromFilterState</code>——这一步<strong>既翻译、又把关</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="侧栏、搜索栏、AI 三种输入都汇成一个 FilterState，经工厂校验列/类型并注入强制 project_id，再编译成参数化的 ClickHouse 或 Postgres SQL">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">三种输入 → 一个 FilterState → 两套 SQL</text>
  <rect x="20" y="42" width="120" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="61" text-anchor="middle" font-size="8" fill="var(--ink)">侧栏面板</text>
  <rect x="20" y="80" width="120" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="99" text-anchor="middle" font-size="8" fill="var(--ink)">搜索栏语法</text>
  <rect x="20" y="118" width="120" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="137" text-anchor="middle" font-size="8" fill="var(--ink)">AI 自然语言</text>
  <rect x="180" y="62" width="150" height="66" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="255" y="86" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">FilterState</text><text x="255" y="104" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">一组带类型的条件</text><text x="255" y="117" text-anchor="middle" font-size="7" fill="var(--muted)">列·运算符·值</text>
  <rect x="368" y="48" width="160" height="94" rx="10" fill="var(--bg)" stroke="var(--accent)"/><text x="448" y="68" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">工厂：翻译 + 把关</text><text x="448" y="86" text-anchor="middle" font-size="7.5" fill="var(--ink)">① 校验列是否在 schema</text><text x="448" y="100" text-anchor="middle" font-size="7.5" fill="var(--ink)">② 校验类型是否兼容</text><text x="448" y="114" text-anchor="middle" font-size="7.5" fill="var(--ink)">③ 注入强制 project_id</text><text x="448" y="130" text-anchor="middle" font-size="7" fill="var(--muted)">createFilterFromFilterState</text>
  <rect x="566" y="50" width="140" height="40" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="636" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">ClickHouse SQL</text><text x="636" y="82" text-anchor="middle" font-size="7" fill="var(--muted)">参数化 · 看板/列表</text>
  <rect x="566" y="100" width="140" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="636" y="118" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">Postgres SQL</text><text x="636" y="132" text-anchor="middle" font-size="7" fill="var(--muted)">参数化 · 评估/审计</text>
  <line x1="140" y1="57" x2="178" y2="86" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="95" x2="178" y2="95" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="133" x2="178" y2="104" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="330" y1="95" x2="366" y2="95" stroke="var(--accent)" stroke-width="1.6"/><polygon points="366,95 357,91 357,99" fill="var(--accent)"/>
  <line x1="528" y1="80" x2="564" y2="70" stroke="var(--faint)" stroke-width="1.3"/><line x1="528" y1="110" x2="564" y2="120" stroke="var(--faint)" stroke-width="1.3"/>
  <text x="360" y="170" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">同一份 FilterState + 列定义，可编译到 ClickHouse 或 Postgres——两套后端共享一个抽象</text>
  <rect x="120" y="188" width="480" height="50" rx="9" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--muted)">ClickHouse 栈：clickhouse-filter.ts（StringFilter/DateTimeFilter…）+ factory.ts</text><text x="360" y="226" text-anchor="middle" font-size="8" fill="var(--muted)">Postgres 栈：filterToPrisma.ts → Prisma.Sql（评估、审计等 Prisma 表）</text>
</svg>
<div class="figcap"><b>一个抽象，两套后端</b>：<code>FilterState</code> + 列定义经工厂 <code>createFilterFromFilterState</code> 校验列/类型、注入强制 <code>project_id</code>，再编译成参数化 SQL。ClickHouse 栈在 <code>clickhouse-sql/</code>，Postgres 栈在 <code>filterToPrisma.ts</code>。源码：<code>queries/clickhouse-sql/factory.ts:37,217</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/queries/clickhouse-sql/{factory,clickhouse-filter}.ts</span><span class="ln">编译 + 把关</span></div>
  <pre class="code"><span class="cm">// 工厂：逐个把关再翻译</span>
<span class="kw">const</span> column = <span class="fn">matchAndVerifyTracesUiColumn</span>(filter, columnMapping); <span class="cm">// 列必须在 CH schema 里</span>
<span class="kw">const</span> compatible = COMPATIBLE_FILTER_TYPES[colDef.type];           <span class="cm">// 类型必须兼容</span>
<span class="fn">getProjectIdDefaultFilter</span>(projectId, …);                        <span class="cm">// 强制注入 project_id（第 10 课）</span>

<span class="cm">// 每个过滤器的 apply()：用随机参数名传值，绝不拼接字符串</span>
<span class="fn">apply</span>(): ClickhouseFilter {
  <span class="kw">const</span> varName = <span class="st">`stringFilter${</span><span class="fn">clickhouseCompliantRandomCharacters</span>()<span class="st">}`</span>;
  <span class="kw">return</span> { query: <span class="st">`col = {${varName}: String}`</span>, params: { [varName]: <span class="kw">this</span>.value } };
}</pre>
</div>

<p>看清这段就抓住了过滤系统的<strong>安全底座</strong>：用户输入的值，<strong>永远不会被拼进 SQL 字符串</strong>，而是绑定到一个<strong>随机命名的占位符</strong>（<code>stringFilter_xY9z</code>），
由数据库驱动安全地代入。哪怕你在过滤值里写 <code>'; DROP TABLE…</code>，它也只会被当成一个普通字符串去匹配，<strong>注入无从下手</strong>。加上工厂对「列是否存在、类型是否兼容」的前置校验，
脏输入在编译期就被挡下——这正是第 22 课资源保护之外的另一道防线。</p>

<svg viewBox="0 0 720 220" role="img" aria-label="一条 FilterState 条件经 apply 编译后一分为二：SQL 片段只留随机命名的占位符 level IN 大括号 pXY9z，用户的值则单独绑进 params，绝不拼进 SQL 字符串，哪怕值是分号 DROP TABLE 也只当普通字符串匹配，注入无从下手">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="16" y="52" width="214" height="100" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="123" y="74" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">FilterState 一条条件</text>
  <text x="30" y="98" font-size="10" fill="var(--ink)">column: level</text>
  <text x="30" y="118" font-size="10" fill="var(--ink)">operator: any of</text>
  <text x="30" y="138" font-size="10" fill="var(--ink)">value: [ERROR, WARNING]</text>
  <line x1="230" y1="102" x2="262" y2="102" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="262" y="74" width="120" height="56" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="322" y="98" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">apply()</text>
  <text x="322" y="116" font-size="9.5" text-anchor="middle" fill="var(--muted)">编译 + 把关</text>
  <line x1="382" y1="92" x2="430" y2="68" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="382" y1="114" x2="430" y2="128" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="430" y="44" width="274" height="50" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="444" y="64" font-size="9.5" fill="var(--muted)">SQL 片段（只留占位符）</text>
  <text x="444" y="84" font-size="10.5" fill="var(--ink)">level IN {pXY9z: Array(String)}</text>
  <rect x="430" y="104" width="274" height="50" rx="9" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="444" y="124" font-size="9.5" fill="var(--muted)">params（用户值绑这里）</text>
  <text x="444" y="144" font-size="10.5" fill="var(--ink)">{ pXY9z: [ERROR, WARNING] }</text>
  <text x="360" y="182" font-size="10.5" text-anchor="middle" fill="var(--muted)">用户值只进 params（随机命名占位符），绝不拼进 SQL 字符串</text>
  <text x="360" y="202" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">哪怕值写成 '; DROP TABLE…，也只当普通字符串匹配 → 注入无从下手</text>
</svg>

<div class="cols">
  <div class="col"><h4>😖 各输入直连各后端：N×M</h4><p>3 种输入 × 2 套后端 = 6 套翻译逻辑、6 处要各自防注入。新加一种输入（比如 AI），就得为<strong>每个后端</strong>重写对接、重写安全校验——组合爆炸，且总有一处会写漏。</p></div>
  <div class="col"><h4>😀 收敛到 FilterState：N+M</h4><p>每个输入只管「译成 FilterState」，每个后端只管「从 FilterState 译出 SQL」。校验与参数化<strong>只在中间做一次</strong>。新加输入只需 +1 个译入器，<strong>白嫖</strong>所有后端与全部安全。</p></div>
</div>
""")

# (search bar + AI filter section below)

_ZH23.append(r"""
<h2>搜索栏与 AI filter：同一个真源的两种皮肤</h2>
<p>侧栏面板之外，Langfuse 还提供一个键盘党喜欢的<strong>搜索栏</strong>——一套 <code>key:value</code> 语法（如 <code>level:(ERROR OR WARNING)</code>、<code>latency:&gt;2</code>、<code>metadata.region:eu</code>）。
但要记住一条铁律（写在它的 README 里）：<strong>侧栏的 <code>FilterState</code> 才是唯一真源，搜索栏只是它的一个「受控编辑器」</strong>——它从 FilterState 读、往 FilterState 写，自己<strong>不另存一份</strong>。</p>

<table class="t">
  <tr><th>搜索栏写法</th><th>含义</th></tr>
  <tr><td><code>level:(ERROR OR WARNING)</code></td><td>任选其一（any-of）</td></tr>
  <tr><td><code>-env:dev</code></td><td>排除（none-of）</td></tr>
  <tr><td><code>latency:&gt;2</code> · <code>startTime:&gt;2026-06-01</code></td><td>数值/时间比较</td></tr>
  <tr><td><code>statusMessage:*chat*</code></td><td>文本包含（<code>*</code> 通配）</td></tr>
  <tr><td><code>metadata.region:eu</code> · <code>scores.accuracy:&gt;0.8</code></td><td>嵌套/点路径字段</td></tr>
</table>

<p>这套语法<strong>有意只覆盖扁平 <code>FilterState</code> 能表达的范围</strong>：跨字段 OR、分组括号这些 FilterState 装不下的形态，搜索栏会给出<strong>阻止提交的诊断提示</strong>，而<strong>不是悄悄丢掉</strong>——
宁可当面说「这我编不出来」，也不给你一个似是而非的错误过滤。这正是「真源单一」带来的好处：搜索栏永远不会和侧栏不一致，因为它们本就是同一份 FilterState 的两种皮肤。</p>

<p>最妙的是 <strong>AI filter</strong>：你用自然语言说「给我看上周延迟超过 2 秒的报错」，<code>generateFilter</code> 调用大模型（Bedrock）把它变成过滤。可大模型会<strong>胡编</strong>不存在的列怎么办？
Langfuse 的解法堪称精巧——把模型输出<strong>往返一遍</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 180" role="img" aria-label="AI filter：自然语言经大模型生成候选过滤，再往返 filterStateToQueryText，只保留能还原成搜索栏语法的过滤，幻觉列被丢弃">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">AI filter：往返校验，幻觉列进不来</text>
  <rect x="16" y="44" width="124" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="78" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">自然语言</text><text x="78" y="80" text-anchor="middle" font-size="7" fill="var(--muted)">「上周超 2s 的报错」</text>
  <rect x="160" y="44" width="124" height="48" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="222" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">大模型生成</text><text x="222" y="80" text-anchor="middle" font-size="7" fill="var(--muted)">候选过滤（可能含幻觉列）</text>
  <rect x="304" y="44" width="150" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="379" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">往返：转回搜索栏语法</text><text x="379" y="78" text-anchor="middle" font-size="7" fill="var(--accent-ink)">filterStateToQueryText</text>
  <rect x="474" y="32" width="112" height="34" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="530" y="50" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">能还原 → 保留</text><text x="530" y="61" text-anchor="middle" font-size="6.8" fill="var(--muted)">应用到 FilterState</text>
  <rect x="474" y="74" width="112" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="3 2"/><text x="530" y="92" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--faint)">还原不了 → 丢弃</text><text x="530" y="103" text-anchor="middle" font-size="6.8" fill="var(--faint)">droppedCount++</text>
  <line x1="140" y1="68" x2="158" y2="68" stroke="var(--faint)" stroke-width="1.4"/><polygon points="158,68 150,64 150,72" fill="var(--faint)"/>
  <line x1="284" y1="68" x2="302" y2="68" stroke="var(--faint)" stroke-width="1.4"/><polygon points="302,68 294,64 294,72" fill="var(--faint)"/>
  <line x1="454" y1="60" x2="472" y2="50" stroke="var(--teal)" stroke-width="1.3"/><line x1="454" y1="76" x2="472" y2="90" stroke="var(--faint)" stroke-width="1.3"/>
  <text x="360" y="140" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">只有「能还原成合法搜索栏语法」的过滤才被采纳——幻觉/不存在的列天然进不来</text>
  <text x="360" y="160" text-anchor="middle" font-size="8" fill="var(--muted)">「构造即合法」：安全不靠事后检查，而靠「编不出就过不来」的结构</text>
</svg>
<div class="figcap"><b>往返即护栏</b>：模型输出被 <code>filterStateToQueryText</code> 往返一遍，只有能还原成合法搜索栏语法（即能降解成 FilterState 能表达的过滤）的才保留，幻觉列直接 <code>droppedCount++</code> 丢弃。源码：<code>web/src/features/search-bar/server/router.ts:45,178-183</code>。</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>自然语言进来</h4><p>用户在搜索栏旁说「上周延迟超 2 秒的报错」；<code>generateFilter</code>（受保护过程，企业版）接住。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>喂给大模型</h4><p>用 v4 字段注册表拼出提示词，调 Bedrock 生成<strong>候选过滤</strong>——此时可能夹带不存在的列。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>往返一遍</h4><p>把候选过滤通过 <code>filterStateToQueryText</code> 转回搜索栏语法，再尝试解析回 FilterState。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>留真去假</h4><p>能干净往返的保留、应用；还原不了的（幻觉/非法列）<strong>丢弃</strong>并计入 <code>droppedCount</code>。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>落到同一个真源</h4><p>最终结果写进侧栏那份 <code>FilterState</code>——和你手点、手敲的过滤<strong>完全同源同路</strong>。</p></div></div>
</div>
""")

# (spark + key below)

_ZH23.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么不让搜索栏、AI 各自直接生成 SQL，非要都先收敛成 FilterState？</strong> 因为<strong>「输入面」和「后端」都不止一个</strong>。输入有侧栏、搜索栏、AI、未来还会更多；
  后端有 ClickHouse、Postgres。如果让每个输入面各自直连每个后端，就是 N×M 套翻译逻辑、N×M 处注入风险——而且新加一种输入，就要把所有后端的对接、所有安全校验<strong>重写一遍</strong>。
  收敛成一个 <code>FilterState</code> 中间契约后，事情变成 N+M：每个输入面只管「译成 FilterState」，每个后端只管「从 FilterState 译出 SQL」，校验与参数化<strong>只在中间做一次</strong>。
  更深的一层是<strong>「构造即合法」</strong>：因为 AI 的输出必须<strong>能还原成 FilterState 能表达的形态</strong>才被采纳，幻觉列<strong>从结构上就不可能</strong>通过——安全不再依赖「记得加一道检查」，而是<strong>由表示本身的边界来保证</strong>。
  这是「单一真源 + 中间表示」最优雅的一面。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>用户过滤的多种入口（侧栏 / 搜索栏 / AI）都<strong>汇成一个 <code>FilterState</code></strong>（带类型的条件组），再编译成 SQL。</li>
    <li><strong>一个抽象、两套后端</strong>：同一份 FilterState 经工厂可编译到 <strong>ClickHouse</strong>（<code>clickhouse-sql/</code>）或 <strong>Postgres</strong>（<code>filterToPrisma.ts</code>）。</li>
    <li><strong>注入安全</strong>：每个过滤器 <code>apply()</code> 用<strong>随机命名的占位符</strong>传值，绝不拼接字符串；工厂还校验列存在性、类型兼容，并注入强制 <code>project_id</code>（第 10 课）。</li>
    <li><strong>搜索栏</strong>是 FilterState 的「受控编辑器」（README：侧栏 FilterState 是唯一真源）；语法只覆盖 FilterState 能表达的范围，编不出的<strong>阻止提交、不静默丢弃</strong>。</li>
    <li><strong>AI filter</strong>把模型输出<strong>往返</strong> <code>filterStateToQueryText</code>，只留能还原成合法语法的——幻觉列<strong>构造上进不来</strong>。安全靠结构，不靠事后检查。</li>
  </ul>
</div>
""")

_EN23.append(r"""
<p class="lead">
Lesson 22's executor "sends queries out", but <strong>who builds those queries' WHERE clauses</strong>? This lesson is about filtering. The key insight: users filter in
many ways — clicking the sidebar facets, typing search-bar grammar, even describing it in natural language to AI — yet they all <strong>converge into one
<code>FilterState</code></strong> (a set of typed conditions), which then compiles to <strong>parameterized SQL</strong> (ClickHouse or Postgres). One intermediate
contract that both blocks SQL injection and makes the search bar and AI filters <strong>safe by construction</strong>.
</p>

<div class="card analogy">
  <div class="tag">🌐 Analogy</div>
  Think of <code>FilterState</code> as the UN's <strong>interlingua</strong>. Attendees speak different mother tongues — some <strong>pick from a menu</strong> (sidebar
  facets), some <strong>write a telegram</strong> (search-bar <code>key:value</code> grammar), some <strong>dictate a request</strong> (AI natural language) — but every
  utterance is first translated into <strong>one standard interlingua</strong> (FilterState), then translated again into what the database speaks (ClickHouse SQL or
  Postgres SQL). This translator has two iron rules: never <strong>splice the original words straight into the translation</strong> (pass values via placeholders, no
  injection); and <strong>refuse on the spot what it can't understand or express</strong>, never paraphrasing nonsense (validation + round-trip dropping
  hallucinations). <strong>All inputs converge to one intermediate representation, then fan out to various backends</strong> — that's the filtering system's skeleton.
</div>
""")

_EN23.append(r"""
<h2>One FilterState, compiled to two SQL backends</h2>
<p><code>FilterState</code> is a set of <strong>typed conditions</strong>: each says "which column, what operator, what value" (e.g.
<code>{column:"level", operator:"any of", value:["ERROR"]}</code>). To become SQL it passes a factory, <code>createFilterFromFilterState</code> — a step that
<strong>both translates and gatekeeps</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="sidebar, search bar, AI inputs all converge to one FilterState; the factory verifies columns/types and injects the mandatory project_id, then compiles to parameterized ClickHouse or Postgres SQL">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Three inputs → one FilterState → two SQL backends</text>
  <rect x="20" y="42" width="120" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="61" text-anchor="middle" font-size="8" fill="var(--ink)">sidebar facets</text>
  <rect x="20" y="80" width="120" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="99" text-anchor="middle" font-size="8" fill="var(--ink)">search-bar grammar</text>
  <rect x="20" y="118" width="120" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="137" text-anchor="middle" font-size="8" fill="var(--ink)">AI natural language</text>
  <rect x="180" y="62" width="150" height="66" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="255" y="86" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">FilterState</text><text x="255" y="104" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">a set of typed conditions</text><text x="255" y="117" text-anchor="middle" font-size="7" fill="var(--muted)">column·operator·value</text>
  <rect x="368" y="48" width="160" height="94" rx="10" fill="var(--bg)" stroke="var(--accent)"/><text x="448" y="68" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">factory: translate + gatekeep</text><text x="448" y="86" text-anchor="middle" font-size="7.5" fill="var(--ink)">① verify column in schema</text><text x="448" y="100" text-anchor="middle" font-size="7.5" fill="var(--ink)">② verify type compatible</text><text x="448" y="114" text-anchor="middle" font-size="7.5" fill="var(--ink)">③ inject mandatory project_id</text><text x="448" y="130" text-anchor="middle" font-size="7" fill="var(--muted)">createFilterFromFilterState</text>
  <rect x="566" y="50" width="140" height="40" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="636" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">ClickHouse SQL</text><text x="636" y="82" text-anchor="middle" font-size="7" fill="var(--muted)">parameterized · dashboards/lists</text>
  <rect x="566" y="100" width="140" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="636" y="118" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">Postgres SQL</text><text x="636" y="132" text-anchor="middle" font-size="7" fill="var(--muted)">parameterized · evals/audit</text>
  <line x1="140" y1="57" x2="178" y2="86" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="95" x2="178" y2="95" stroke="var(--faint)" stroke-width="1.3"/><line x1="140" y1="133" x2="178" y2="104" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="330" y1="95" x2="366" y2="95" stroke="var(--accent)" stroke-width="1.6"/><polygon points="366,95 357,91 357,99" fill="var(--accent)"/>
  <line x1="528" y1="80" x2="564" y2="70" stroke="var(--faint)" stroke-width="1.3"/><line x1="528" y1="110" x2="564" y2="120" stroke="var(--faint)" stroke-width="1.3"/>
  <text x="360" y="170" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">One FilterState + column defs compiles to ClickHouse or Postgres — two backends, one abstraction</text>
  <rect x="120" y="188" width="480" height="50" rx="9" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--muted)">ClickHouse stack: clickhouse-filter.ts (StringFilter/DateTimeFilter…) + factory.ts</text><text x="360" y="226" text-anchor="middle" font-size="8" fill="var(--muted)">Postgres stack: filterToPrisma.ts → Prisma.Sql (Prisma tables: evals, audit…)</text>
</svg>
<div class="figcap"><b>One abstraction, two backends</b>: <code>FilterState</code> + column defs pass the factory <code>createFilterFromFilterState</code>, which verifies columns/types, injects the mandatory <code>project_id</code>, then compiles to parameterized SQL. ClickHouse stack in <code>clickhouse-sql/</code>, Postgres stack in <code>filterToPrisma.ts</code>. Source: <code>queries/clickhouse-sql/factory.ts:37,217</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/queries/clickhouse-sql/{factory,clickhouse-filter}.ts</span><span class="ln">compile + gatekeep</span></div>
  <pre class="code"><span class="cm">// factory: gatekeep each, then translate</span>
<span class="kw">const</span> column = <span class="fn">matchAndVerifyTracesUiColumn</span>(filter, columnMapping); <span class="cm">// column must be in CH schema</span>
<span class="kw">const</span> compatible = COMPATIBLE_FILTER_TYPES[colDef.type];           <span class="cm">// type must be compatible</span>
<span class="fn">getProjectIdDefaultFilter</span>(projectId, …);                        <span class="cm">// force-inject project_id (L10)</span>

<span class="cm">// each filter's apply(): pass values via random param names, never splice strings</span>
<span class="fn">apply</span>(): ClickhouseFilter {
  <span class="kw">const</span> varName = <span class="st">`stringFilter${</span><span class="fn">clickhouseCompliantRandomCharacters</span>()<span class="st">}`</span>;
  <span class="kw">return</span> { query: <span class="st">`col = {${varName}: String}`</span>, params: { [varName]: <span class="kw">this</span>.value } };
}</pre>
</div>

<p>Grasp this and you've got the filtering system's <strong>security bedrock</strong>: user-input values are <strong>never spliced into the SQL string</strong>, but bound
to a <strong>randomly-named placeholder</strong> (<code>stringFilter_xY9z</code>), safely substituted by the DB driver. Even if you write <code>'; DROP TABLE…</code> in a
filter value, it's matched as a plain string — <strong>injection has no foothold</strong>. Plus the factory's up-front checks for "does the column exist, is the type
compatible" stop dirty input at compile time — another line of defense beyond Lesson 22's resource protection.</p>

<svg viewBox="0 0 720 220" role="img" aria-label="one FilterState condition compiled by apply splits into two: the SQL fragment keeps only a randomly-named placeholder level IN brace pXY9z, while the user's value is bound separately into params, never concatenated into the SQL string, so even a value like semicolon DROP TABLE is matched as a plain string and injection has no foothold">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="16" y="52" width="214" height="100" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="123" y="74" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">one FilterState condition</text>
  <text x="30" y="98" font-size="10" fill="var(--ink)">column: level</text>
  <text x="30" y="118" font-size="10" fill="var(--ink)">operator: any of</text>
  <text x="30" y="138" font-size="10" fill="var(--ink)">value: [ERROR, WARNING]</text>
  <line x1="230" y1="102" x2="262" y2="102" stroke="var(--blue)" stroke-width="2"></line>
  <rect x="262" y="74" width="120" height="56" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="322" y="98" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">apply()</text>
  <text x="322" y="116" font-size="9.5" text-anchor="middle" fill="var(--muted)">compile + guard</text>
  <line x1="382" y1="92" x2="430" y2="68" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="382" y1="114" x2="430" y2="128" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="430" y="44" width="274" height="50" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="444" y="64" font-size="9.5" fill="var(--muted)">SQL fragment (placeholder only)</text>
  <text x="444" y="84" font-size="10.5" fill="var(--ink)">level IN {pXY9z: Array(String)}</text>
  <rect x="430" y="104" width="274" height="50" rx="9" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="444" y="124" font-size="9.5" fill="var(--muted)">params (user value bound here)</text>
  <text x="444" y="144" font-size="10.5" fill="var(--ink)">{ pXY9z: [ERROR, WARNING] }</text>
  <text x="360" y="182" font-size="10.5" text-anchor="middle" fill="var(--muted)">the user value goes only into params (a random placeholder), never into the SQL string</text>
  <text x="360" y="202" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">even a value like '; DROP TABLE… is matched as plain text → injection has no foothold</text>
</svg>

<div class="cols">
  <div class="col"><h4>😖 each input to each backend: N×M</h4><p>3 inputs × 2 backends = 6 translation logics, 6 places to each guard injection. Add a new input (say AI) and you must rewrite the wiring and security checks for <strong>every backend</strong> — a combinatorial explosion, and one spot always gets missed.</p></div>
  <div class="col"><h4>😀 converge to FilterState: N+M</h4><p>Each input only "translates to FilterState", each backend only "translates FilterState to SQL". Validation and parameterization happen <strong>once in the middle</strong>. A new input is just +1 translator-in, freeloading all backends and all the safety.</p></div>
</div>
""")

_EN23.append(r"""
<h2>The search bar &amp; AI filter: two skins of one source of truth</h2>
<p>Beyond the sidebar facets, Langfuse offers a keyboard-lover's <strong>search bar</strong> — a <code>key:value</code> grammar (e.g. <code>level:(ERROR OR
WARNING)</code>, <code>latency:&gt;2</code>, <code>metadata.region:eu</code>). But remember one iron rule (in its README): <strong>the sidebar's
<code>FilterState</code> is the single source of truth, and the bar is just a "controlled editor" over it</strong> — it reads from and writes to FilterState,
keeping <strong>no second copy</strong>.</p>

<table class="t">
  <tr><th>search-bar syntax</th><th>meaning</th></tr>
  <tr><td><code>level:(ERROR OR WARNING)</code></td><td>any-of</td></tr>
  <tr><td><code>-env:dev</code></td><td>exclude (none-of)</td></tr>
  <tr><td><code>latency:&gt;2</code> · <code>startTime:&gt;2026-06-01</code></td><td>numeric/time comparison</td></tr>
  <tr><td><code>statusMessage:*chat*</code></td><td>text contains (<code>*</code> glob)</td></tr>
  <tr><td><code>metadata.region:eu</code> · <code>scores.accuracy:&gt;0.8</code></td><td>nested / dot-path fields</td></tr>
</table>

<p>This grammar <strong>deliberately covers only what flat <code>FilterState</code> can express</strong>: shapes FilterState can't hold (cross-field OR, grouping
parens) get a <strong>commit-blocking diagnostic</strong>, <strong>not a silent drop</strong> — better to say to your face "I can't express that" than hand you a
plausible-but-wrong filter. That's the gift of "single source of truth": the bar can never disagree with the sidebar, because they're two skins of the same
FilterState.</p>

<p>Best of all is the <strong>AI filter</strong>: you say in natural language "show me last week's errors over 2 seconds latency", and <code>generateFilter</code>
calls an LLM (Bedrock) to turn it into filters. But what if the model <strong>hallucinates</strong> a nonexistent column? Langfuse's fix is elegant — it
<strong>round-trips</strong> the model output:</p>

<div class="fig">
<svg viewBox="0 0 720 180" role="img" aria-label="AI filter: natural language through the LLM produces candidate filters, then round-trips filterStateToQueryText, keeping only filters that restore to search-bar grammar; hallucinated columns are dropped">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">AI filter: round-trip validation, hallucinated columns can't enter</text>
  <rect x="16" y="44" width="124" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="78" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">natural language</text><text x="78" y="80" text-anchor="middle" font-size="6.6" fill="var(--muted)">"errors over 2s last week"</text>
  <rect x="160" y="44" width="124" height="48" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="222" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">LLM generates</text><text x="222" y="80" text-anchor="middle" font-size="6.6" fill="var(--muted)">candidates (maybe hallucinated)</text>
  <rect x="304" y="44" width="150" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="379" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">round-trip: back to grammar</text><text x="379" y="78" text-anchor="middle" font-size="7" fill="var(--accent-ink)">filterStateToQueryText</text>
  <rect x="474" y="32" width="112" height="34" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="530" y="50" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">restores → keep</text><text x="530" y="61" text-anchor="middle" font-size="6.6" fill="var(--muted)">apply to FilterState</text>
  <rect x="474" y="74" width="112" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="3 2"/><text x="530" y="92" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--faint)">can't → drop</text><text x="530" y="103" text-anchor="middle" font-size="6.6" fill="var(--faint)">droppedCount++</text>
  <line x1="140" y1="68" x2="158" y2="68" stroke="var(--faint)" stroke-width="1.4"/><polygon points="158,68 150,64 150,72" fill="var(--faint)"/>
  <line x1="284" y1="68" x2="302" y2="68" stroke="var(--faint)" stroke-width="1.4"/><polygon points="302,68 294,64 294,72" fill="var(--faint)"/>
  <line x1="454" y1="60" x2="472" y2="50" stroke="var(--teal)" stroke-width="1.3"/><line x1="454" y1="76" x2="472" y2="90" stroke="var(--faint)" stroke-width="1.3"/>
  <text x="360" y="140" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">only filters that "restore to valid grammar" are accepted — hallucinated/unknown columns can't get in</text>
  <text x="360" y="160" text-anchor="middle" font-size="8" fill="var(--muted)">"valid by construction": safety not from after-checks but from "can't express → can't pass"</text>
</svg>
<div class="figcap"><b>The round-trip is the guardrail</b>: the model output is round-tripped through <code>filterStateToQueryText</code>; only filters that restore to valid search-bar grammar (i.e. lower to what FilterState can express) are kept, hallucinated columns <code>droppedCount++</code>. Source: <code>web/src/features/search-bar/server/router.ts:45,178-183</code>.</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>natural language in</h4><p>The user says, next to the bar, "errors over 2s latency last week"; <code>generateFilter</code> (protected procedure, enterprise) catches it.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>feed the LLM</h4><p>Build a prompt from the v4 field registry, call Bedrock to generate <strong>candidate filters</strong> — possibly smuggling in nonexistent columns.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>round-trip</h4><p>Turn candidates back to search-bar grammar via <code>filterStateToQueryText</code>, then try to parse back to FilterState.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>keep real, drop fake</h4><p>Cleanly round-tripping ones are kept and applied; un-restorable ones (hallucinated/illegal columns) are <strong>dropped</strong> and counted in <code>droppedCount</code>.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>land in the same source</h4><p>The result is written into the sidebar's <code>FilterState</code> — exactly the same source and path as your clicked and typed filters.</p></div></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why not let the search bar and AI each generate SQL directly, instead of all converging to FilterState first?</strong> Because <strong>there are multiple
  "input surfaces" AND multiple "backends"</strong>. Inputs: sidebar, search bar, AI, more to come; backends: ClickHouse, Postgres. Wire each input straight to each
  backend and it's N×M translation logics, N×M injection risks — and adding one input means <strong>rewriting</strong> every backend's wiring and every safety check.
  Converge to one <code>FilterState</code> contract and it becomes N+M: each input only "translates to FilterState", each backend only "translates FilterState to SQL",
  validation and parameterization done <strong>once in the middle</strong>. The deeper layer is <strong>"valid by construction"</strong>: because the AI output must
  <strong>restore to what FilterState can express</strong> to be accepted, hallucinated columns are <strong>structurally impossible</strong> to pass — safety no longer
  depends on "remembering to add a check" but is <strong>guaranteed by the boundaries of the representation itself</strong>. This is the most elegant face of "single
  source of truth + intermediate representation".
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>The many filtering entries (sidebar / search bar / AI) all <strong>converge to one <code>FilterState</code></strong> (a set of typed conditions), then compile to SQL.</li>
    <li><strong>One abstraction, two backends</strong>: the same FilterState compiles via the factory to <strong>ClickHouse</strong> (<code>clickhouse-sql/</code>) or <strong>Postgres</strong> (<code>filterToPrisma.ts</code>).</li>
    <li><strong>Injection safety</strong>: each filter's <code>apply()</code> passes values via <strong>randomly-named placeholders</strong>, never splicing strings; the factory also verifies column existence, type compatibility, and injects the mandatory <code>project_id</code> (L10).</li>
    <li><strong>The search bar</strong> is FilterState's "controlled editor" (README: the sidebar FilterState is the single source of truth); its grammar covers only what FilterState can express, the rest <strong>blocking commit, not silently dropped</strong>.</li>
    <li><strong>AI filter</strong> round-trips the model output through <code>filterStateToQueryText</code>, keeping only what restores to valid grammar — hallucinated columns <strong>can't enter by construction</strong>. Security by structure, not after-checks.</li>
  </ul>
</div>
""")
LESSON_23 = {"zh": "\n".join(_ZH23), "en": "\n".join(_EN23)}


# ══════════════════════════════════════════════════════════════════════
# L24 · 列表与表格 / Lists & tables
# ══════════════════════════════════════════════════════════════════════
_ZH24 = []
_EN24 = []

_ZH24.append(r"""
<p class="lead">
前两课讲了查询怎么拼、怎么跑。这一课看 Langfuse 的<strong>旗舰列表</strong>——trace 表，它凭什么能<strong>秒开</strong>。秘诀有二：一是<strong>一个通用函数服务四种「形状」</strong>
（计数 / 行 / 指标 / 标识），二是把<strong>「便宜的行」和「昂贵的指标」拆开</strong>——表格先把行画出来，成本/延迟/评分这些要 JOIN 的指标<strong>稍后流入、客户端再拼</strong>。
再加上一招<strong>按需 FINAL</strong>的查询纪律，让默认视图只读最新分区。看懂这一课，你就懂了大数据表「既要全、又要快」的全部门道。
</p>

<div class="card analogy">
  <div class="tag">🍽️ 生活类比</div>
  把列表加载想成餐厅<strong>分批上菜</strong>。如果非要等整桌大餐（行 + 所有指标）一次端上，你得干坐很久。聪明的厨房先上<strong>面包</strong>（紧凑行——便宜、人人都要），让你<strong>立刻开吃</strong>；
  那些<strong>费工夫的硬菜</strong>（指标：成本、延迟、评分，每样都要现做现拼）<strong>做好一道端一道</strong>，悄悄添到你桌上。你的体验是「<strong>一坐下就有得吃</strong>」，而不是「盯着空桌等二十分钟」。
  Langfuse 的表格正是这么干的：<strong>能立刻给的先给，要算的边算边补</strong>——这就是「紧凑列表模型」。
</div>
""")

# (L24 sections appended below)

_ZH24.append(r"""
<h2>紧凑行 vs 指标：两路并发、客户端再拼</h2>
<p>打开 trace 列表时，UI <strong>同时</strong>发两路 tRPC 调用：<code>traces.all</code> 取<strong>紧凑行</strong>（约 12 个永远要看的列），<code>traces.metrics</code> 取<strong>指标</strong>（成本、延迟、评分聚合——要 JOIN 两张表）。
谁先回谁先用：行一回来表格立刻渲染，指标回来后<strong>按 id 拼进去</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="UI 并行发 traces.all 取紧凑行与 traces.metrics 取指标；行先到先渲染，指标后到按 id 合并，joinTableCoreAndMetrics 即使指标缺席也返回成功">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">紧凑行先画，指标后补——表格秒开</text>
  <rect x="20" y="42" width="130" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="85" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">traces.all（行）</text><text x="85" y="78" text-anchor="middle" font-size="7" fill="var(--accent-ink)">~12 列 · 便宜 · 快</text>
  <rect x="20" y="104" width="130" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="85" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">traces.metrics（指标）</text><text x="85" y="140" text-anchor="middle" font-size="7" fill="var(--muted)">成本/延迟/评分 · 要 2 JOIN · 慢</text>
  <text x="85" y="170" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">↑ 两路并发发出 ↑</text>
  <rect x="280" y="60" width="170" height="74" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/><text x="365" y="82" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">joinTableCoreAndMetrics</text><text x="365" y="100" text-anchor="middle" font-size="7.5" fill="var(--ink)">按 id 把行与指标拼起来</text><text x="365" y="116" text-anchor="middle" font-size="7.5" fill="var(--ink)">指标缺席也返回 success</text><text x="365" y="128" text-anchor="middle" font-size="7" fill="var(--muted)">→ 行先渲染，不空等</text>
  <rect x="500" y="48" width="200" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="600" y="66" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">① 表格立刻画出行</text><text x="600" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">指标列先留空/转圈</text>
  <rect x="500" y="100" width="200" height="40" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="600" y="118" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② 指标到，按 id 填进对应行</text><text x="600" y="132" text-anchor="middle" font-size="7" fill="var(--muted)">无闪烁、无整表重渲</text>
  <line x1="150" y1="66" x2="278" y2="84" stroke="var(--faint)" stroke-width="1.3"/><line x1="150" y1="128" x2="278" y2="108" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="450" y1="80" x2="498" y2="68" stroke="var(--accent)" stroke-width="1.4"/><line x1="450" y1="112" x2="498" y2="120" stroke="var(--faint)" stroke-width="1.3"/>
  <text x="360" y="206" text-anchor="middle" font-size="8.5" fill="var(--faint)">关键：紧凑行不依赖指标，所以表格在指标算完之前就能用——感知延迟从「最慢一路」变成「最快一路」</text>
</svg>
<div class="figcap"><b>拆开「行」与「指标」</b>：UI 并行发 <code>traces.all</code>（行）+ <code>traces.metrics</code>（指标）；<code>joinTableCoreAndMetrics</code> 按 id 合并、即使指标缺席也返回 <code>success</code>，所以表格先用行渲染、指标后到再填。源码：<code>web/src/components/table/utils/joinTableCoreAndMetrics.ts:1</code>、<code>services/traces-ui-table-service.ts:206</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/traces-ui-table-service.ts</span><span class="ln">getTracesTableGeneric :206</span></div>
  <pre class="code"><span class="cm">// 一个函数，四种「形状」——靠 select 区分（类型安全重载）</span>
<span class="kw">function</span> <span class="fn">getTracesTableGeneric</span>(props: { select: <span class="st">"count"</span> | <span class="st">"rows"</span> | <span class="st">"metrics"</span> | <span class="st">"identifiers"</span> })

<span class="cm">// 只在「真的需要」时才 LEFT JOIN——默认浏览行时省掉两次 JOIN</span>
<span class="kw">const</span> requiresScoresJoin = <span class="cm">/* 有评分过滤/排序，或 select==="metrics" */</span>;
<span class="kw">const</span> requiresObservationsJoin = <span class="cm">/* 同理 */</span>;
...
FROM traces t ${defaultOrder ? <span class="st">""</span> : <span class="st">"FINAL"</span>}        <span class="cm">// 默认排序不用 FINAL（见下）</span>
${requiresObservationsJoin ? <span class="st">"LEFT JOIN observations_stats o ..."</span> : <span class="st">""</span>}
${requiresScoresJoin ? <span class="st">"LEFT JOIN scores_avg s ..."</span> : <span class="st">""</span>}</pre>
</div>
""")

# (conditional FINAL section below)

_ZH24.append(r"""
<h2>按需 FINAL：默认视图只读最新分区</h2>
<p>这里藏着一个 ClickHouse 老手才懂的优化。回想第 8 课：traces 是 <code>ReplacingMergeTree</code>，同一 id 可能有多行（create/update 各一行），靠后台合并去重。
查询时若加 <code>FINAL</code>，ClickHouse 会<strong>当场把所有分区读出来、去重</strong>，结果正确但<strong>慢</strong>。Langfuse 的取舍是——<strong>能不用 FINAL 就不用</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="默认排序按 toDate(timestamp)+event_ts desc 加 LIMIT 1 BY id 不用 FINAL 只读最新分区内存去重；非默认排序才 FROM traces FINAL 全量去重">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">按需 FINAL：默认路径快，非默认路径才付全量代价</text>
  <rect x="20" y="40" width="330" height="140" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="185" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">默认排序（按时间）· 不用 FINAL</text>
  <rect x="38" y="76" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--blue)"/><text x="185" y="93" text-anchor="middle" font-size="8" fill="var(--ink)">ORDER BY toDate(timestamp), event_ts DESC</text>
  <rect x="38" y="108" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--blue)"/><text x="185" y="125" text-anchor="middle" font-size="8" fill="var(--ink)">LIMIT 1 BY id（内存里取每个 id 最新一行）</text>
  <text x="185" y="152" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">✅ CH 只从磁盘读「最新那天」的分区</text>
  <text x="185" y="168" text-anchor="middle" font-size="7.5" fill="var(--muted)">不必为去重把一个月的数据全捞出来——又对又快</text>
  <rect x="370" y="40" width="330" height="140" rx="10" fill="var(--bg)" stroke="var(--faint)"/><text x="535" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">非默认排序 · 用 FINAL</text>
  <rect x="388" y="76" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="535" y="93" text-anchor="middle" font-size="8" fill="var(--muted)">如按成本/延迟排序时</text>
  <rect x="388" y="108" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="535" y="125" text-anchor="middle" font-size="8" fill="var(--muted)">FROM traces t FINAL（全量去重）</text>
  <text x="535" y="152" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">⚠️ 必须读全、去重才能保证正确</text>
  <text x="535" y="168" text-anchor="middle" font-size="7.5" fill="var(--muted)">慢一些，但只在你主动换排序时才付这代价</text>
</svg>
<div class="figcap"><b>对与快兼得</b>：默认按时间排序时用 <code>toDate(timestamp), event_ts DESC</code> + <code>LIMIT 1 BY id</code> 代替 <code>FINAL</code>，CH 只读最新分区、在内存里取每个 id 的最新行；只有当你<strong>按非时间列排序</strong>时才退回 <code>FROM traces FINAL</code> 全量去重。源码注释见 <code>traces-ui-table-service.ts:443-455</code>。</div>
</div>

<div class="cols">
  <div class="col"><h4>🟢 默认路径（最常走）</h4><p>按时间排序 + 不需指标 → 不 FINAL、不 JOIN，只读最新分区。这是 80% 的「打开列表扫一眼」场景，做到了又对又飞快。</p></div>
  <div class="col"><h4>🟡 重路径（按需付费）</h4><p>按成本排序、或要看指标 → 才加 FINAL、才 LEFT JOIN observations/scores。复杂度只在你<strong>主动要</strong>时才被引入，不拖累常见路径。</p></div>
</div>

<table class="t">
  <tr><th>select 形状</th><th>取什么</th><th>给谁用</th></tr>
  <tr><td><code>rows</code></td><td>~12 个紧凑列</td><td>表格主体，立刻渲染</td></tr>
  <tr><td><code>metrics</code></td><td>成本/延迟/评分聚合（要 2 JOIN）</td><td>指标列，后到补入</td></tr>
  <tr><td><code>count</code></td><td><code>uniqExact(id)</code></td><td>分页总数（去重计数）</td></tr>
  <tr><td><code>identifiers</code></td><td>只要 id 列表</td><td>批量操作、跨页选择</td></tr>
</table>

<h2>表格状态：URL 是真源，三层持久化</h2>
<p>列表不只是「画一堆行」。你调了列顺序、设了过滤、排了序、存成一个「视图预设」——这些<strong>表格状态</strong>该存哪？Langfuse 的答案是<strong>分三层、以 URL 为真源</strong>：</p>

<svg viewBox="0 0 720 230" role="img" aria-label="表格状态分三层按时效递增：URL 是真源与分享层(过滤排序搜索视图id编码进链接,发链接即复现)、session 存储是本次导航记忆(列宽可见列滚动,关标签即清)、数据库是永久预设saved view(跨设备团队共享,失效则优雅降级)">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="24" y="44" width="204" height="122" rx="10" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="126" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">URL · 真源</text>
  <text x="126" y="90" font-size="10.5" text-anchor="middle" fill="var(--muted)">分享 + 深度链接</text>
  <text x="126" y="114" font-size="10" text-anchor="middle" fill="var(--ink)">过滤/排序/搜索/视图id</text>
  <text x="126" y="138" font-size="10" text-anchor="middle" fill="var(--ink)">→ 发链接即原样复现</text>
  <text x="126" y="158" font-size="9.5" text-anchor="middle" fill="var(--muted)">时效：此刻可分享</text>
  <rect x="258" y="44" width="204" height="122" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">session 存储</text>
  <text x="360" y="90" font-size="10.5" text-anchor="middle" fill="var(--muted)">导航记忆</text>
  <text x="360" y="114" font-size="10" text-anchor="middle" fill="var(--ink)">列宽/可见列/滚动位置</text>
  <text x="360" y="138" font-size="10" text-anchor="middle" fill="var(--ink)">→ 跳转间不丢</text>
  <text x="360" y="158" font-size="9.5" text-anchor="middle" fill="var(--muted)">时效：关标签即清</text>
  <rect x="492" y="44" width="204" height="122" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="594" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">数据库</text>
  <text x="594" y="90" font-size="10.5" text-anchor="middle" fill="var(--muted)">永久预设 saved view</text>
  <text x="594" y="114" font-size="10" text-anchor="middle" fill="var(--ink)">跨设备 · 团队共享</text>
  <text x="594" y="138" font-size="10" text-anchor="middle" fill="var(--ink)">→ 失效则优雅降级</text>
  <text x="594" y="158" font-size="9.5" text-anchor="middle" fill="var(--muted)">时效：永久沉淀</text>
  <line x1="24" y1="194" x2="696" y2="194" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="360" y="216" font-size="11" text-anchor="middle" fill="var(--muted)">时效递增 →：URL（此刻可分享）· session（这次导航）· DB（永久沉淀）</text>
</svg>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">URL</span><span class="name">分享与真源</span></div><div class="ld">过滤、排序、搜索、当前视图 id 都编码进 <strong>URL</strong>。于是你把链接发给同事，他打开看到的<strong>和你一模一样</strong>——URL 是「此刻这张表长什么样」的单一真源（呼应第 23 课 FilterState）。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">session 存储</span><span class="name">导航记忆</span></div><div class="ld">在表之间来回跳时，用<strong>会话存储</strong>记住你刚才的列宽、可见列、滚动位置等，免得每次回来都被重置——只在本次浏览会话内有效，关掉标签页即清。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">数据库</span><span class="name">永久预设</span></div><div class="ld">「视图预设」（saved view）存进 <strong>DB</strong>，永久保留、可跨设备、可团队共享。删了某个预设、或它引用的列已不存在？<strong>优雅降级</strong>：丢掉失效部分 + 提示，绝不白屏。</div></div>
</div>

<p>这三层各管一段时效——URL 管「此刻可分享」、session 管「这次导航」、DB 管「永久保存」——共同让大表格<strong>既可深度链接、又在跳转间不丢状态、还能长期沉淀团队的常用视图</strong>。
配合一个全局时间范围（Zustand 默认 ⊕ URL 显式），它会变成那条强制的 <code>timestamp</code> 过滤，正好喂给第 22 课的回看窗、把扫描范围钉死。<strong>状态分层，是大型列表「快」之外的另一半功夫——「稳」（跳转间不丢）与「可分享」（一个链接复现全貌）。</strong></p>
""")

# (spark + key below)

_ZH24.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么不一次查全（行 + 所有指标），非要拆成两路、还搞一堆「按需」开关？</strong> 因为<strong>列表的体验目标是「秒开」，而指标天生昂贵</strong>。
  成本、延迟、评分这些要 JOIN 两张大表才能算，若和行绑在一起，整张表就得<strong>等最慢的那路</strong>才能显示——用户盯着空白干等。把它们拆开后，
  紧凑行（便宜、人人要）<strong>立刻就到</strong>，指标作为「附加信息」边算边补；感知延迟从「最慢一路」降到「最快一路」。同理，<strong>按需 FINAL、按需 JOIN</strong> 都是同一种智慧：
  <strong>为最常见、最简单的路径极致优化，把复杂度与代价推迟到「你真的要了」才引入</strong>。这是高频列表界面性能的黄金法则——别让 1% 的高级需求（按成本排序、看全指标）拖慢 99% 的日常浏览。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>一个 <code>getTracesTableGeneric</code> 服务<strong>四种形状</strong>（<code>rows / metrics / count / identifiers</code>），靠 <code>select</code> 区分、类型安全重载。</li>
    <li><strong>紧凑行 vs 指标拆开</strong>：UI 并行发 <code>traces.all</code>（行）+ <code>traces.metrics</code>（指标）；<code>joinTableCoreAndMetrics</code> 按 id 合并、指标缺席也返回 success，表格<strong>先用行渲染</strong>。</li>
    <li><strong>按需 JOIN</strong>：只在过滤/排序需要或 <code>select==="metrics"</code> 时才 LEFT JOIN observations/scores，默认浏览省掉两次 JOIN。</li>
    <li><strong>按需 FINAL</strong>：默认按时间排序用 <code>toDate(timestamp),event_ts DESC</code> + <code>LIMIT 1 BY id</code> 只读最新分区；非默认排序才退回 <code>FROM traces FINAL</code> 全量去重。</li>
    <li>黄金法则：为最常见路径极致优化，把复杂度/代价推迟到「真的要了」才引入——别让 1% 的高级需求拖慢 99% 的日常浏览。</li>
    <li><strong>表格状态分三层、以 URL 为真源</strong>：URL（可分享/真源）⊕ session（导航记忆）⊕ DB（永久视图预设，失效部分优雅降级）；全局时间范围变成喂给第 22 课回看窗的强制 timestamp 过滤。</li>
  </ul>
</div>
""")

_EN24.append(r"""
<p class="lead">
The last two lessons covered how queries are built and run. This one looks at Langfuse's <strong>flagship list</strong> — the trace table — and how it
<strong>opens instantly</strong>. Two secrets: one, <strong>a single generic function serves four "shapes"</strong> (count / rows / metrics / identifiers); two, it
<strong>splits the cheap rows from the expensive metrics</strong> — the table paints rows first, while cost/latency/score metrics needing JOINs <strong>stream in
later and merge client-side</strong>. Plus a <strong>conditional-FINAL</strong> query discipline that keeps the default view reading only the latest partition. Get this
lesson and you've got the whole art of a big-data table being "complete yet fast".
</p>

<div class="card analogy">
  <div class="tag">🍽️ Analogy</div>
  Think of list loading as a restaurant <strong>serving in courses</strong>. Insisting the whole elaborate meal (rows + all metrics) arrive at once means you sit
  waiting a long time. A smart kitchen brings the <strong>bread</strong> first (compact rows — cheap, everyone wants them) so you <strong>start eating
  immediately</strong>; the <strong>labor-intensive mains</strong> (metrics: cost, latency, scores, each made and assembled to order) <strong>arrive dish by dish</strong>,
  quietly added to your table. Your experience is "<strong>something to eat the moment you sit down</strong>", not "staring at an empty table for twenty minutes".
  Langfuse's table does exactly this: <strong>give what you can instantly, fill in what you must compute as it comes</strong> — that's the "compact list model".
</div>
""")

_EN24.append(r"""
<h2>Compact rows vs metrics: two parallel calls, merged client-side</h2>
<p>Opening the trace list, the UI fires <strong>two</strong> tRPC calls <strong>at once</strong>: <code>traces.all</code> for the <strong>compact rows</strong> (~12
always-wanted columns), and <code>traces.metrics</code> for the <strong>metrics</strong> (cost, latency, score aggregates — needing 2 JOINs). Whoever returns first is
used: rows back, the table renders immediately; metrics back, they're <strong>merged in by id</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="UI fires traces.all for compact rows and traces.metrics for metrics in parallel; rows render first, metrics merge by id when ready, joinTableCoreAndMetrics returns success even without metrics">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Compact rows paint first, metrics fill in — instant table</text>
  <rect x="20" y="42" width="130" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="85" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">traces.all (rows)</text><text x="85" y="78" text-anchor="middle" font-size="7" fill="var(--accent-ink)">~12 cols · cheap · fast</text>
  <rect x="20" y="104" width="130" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="85" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">traces.metrics</text><text x="85" y="140" text-anchor="middle" font-size="6.6" fill="var(--muted)">cost/latency/scores · 2 JOINs · slow</text>
  <text x="85" y="170" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">↑ fired in parallel ↑</text>
  <rect x="280" y="60" width="170" height="74" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/><text x="365" y="82" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">joinTableCoreAndMetrics</text><text x="365" y="100" text-anchor="middle" font-size="7.5" fill="var(--ink)">merge rows + metrics by id</text><text x="365" y="116" text-anchor="middle" font-size="7.5" fill="var(--ink)">returns success even without metrics</text><text x="365" y="128" text-anchor="middle" font-size="7" fill="var(--muted)">→ rows render, no idle wait</text>
  <rect x="500" y="48" width="200" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="600" y="66" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">① table paints rows now</text><text x="600" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">metric cols blank/spinner first</text>
  <rect x="500" y="100" width="200" height="40" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="600" y="118" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② metrics arrive, fill rows by id</text><text x="600" y="132" text-anchor="middle" font-size="7" fill="var(--muted)">no flicker, no full re-render</text>
  <line x1="150" y1="66" x2="278" y2="84" stroke="var(--faint)" stroke-width="1.3"/><line x1="150" y1="128" x2="278" y2="108" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="450" y1="80" x2="498" y2="68" stroke="var(--accent)" stroke-width="1.4"/><line x1="450" y1="112" x2="498" y2="120" stroke="var(--faint)" stroke-width="1.3"/>
  <text x="360" y="206" text-anchor="middle" font-size="8.5" fill="var(--faint)">key: compact rows don't depend on metrics, so the table is usable before metrics finish — perceived latency goes from "slowest call" to "fastest call"</text>
</svg>
<div class="figcap"><b>Splitting "rows" from "metrics"</b>: the UI fires <code>traces.all</code> (rows) + <code>traces.metrics</code> (metrics) in parallel; <code>joinTableCoreAndMetrics</code> merges by id and returns <code>success</code> even when metrics are absent, so the table renders from rows and fills metrics later. Source: <code>web/src/components/table/utils/joinTableCoreAndMetrics.ts:1</code>, <code>services/traces-ui-table-service.ts:206</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/traces-ui-table-service.ts</span><span class="ln">getTracesTableGeneric :206</span></div>
  <pre class="code"><span class="cm">// one function, four "shapes" — distinguished by select (type-safe overloads)</span>
<span class="kw">function</span> <span class="fn">getTracesTableGeneric</span>(props: { select: <span class="st">"count"</span> | <span class="st">"rows"</span> | <span class="st">"metrics"</span> | <span class="st">"identifiers"</span> })

<span class="cm">// LEFT JOIN only when really needed — default row browsing skips two JOINs</span>
<span class="kw">const</span> requiresScoresJoin = <span class="cm">/* score filter/sort, or select==="metrics" */</span>;
<span class="kw">const</span> requiresObservationsJoin = <span class="cm">/* likewise */</span>;
...
FROM traces t ${defaultOrder ? <span class="st">""</span> : <span class="st">"FINAL"</span>}        <span class="cm">// default ordering skips FINAL (below)</span>
${requiresObservationsJoin ? <span class="st">"LEFT JOIN observations_stats o ..."</span> : <span class="st">""</span>}
${requiresScoresJoin ? <span class="st">"LEFT JOIN scores_avg s ..."</span> : <span class="st">""</span>}</pre>
</div>
""")

_EN24.append(r"""
<h2>Conditional FINAL: the default view reads only the latest partition</h2>
<p>Here hides an optimization only ClickHouse veterans appreciate. Recall Lesson 8: traces is a <code>ReplacingMergeTree</code>, where one id may have multiple rows
(create/update each a row), deduped by background merges. Add <code>FINAL</code> to a query and ClickHouse <strong>reads all partitions and dedups on the spot</strong> —
correct but <strong>slow</strong>. Langfuse's trade-off: <strong>avoid FINAL whenever possible</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="default ordering by toDate(timestamp)+event_ts desc with LIMIT 1 BY id skips FINAL and reads only the latest partition deduping in memory; non-default ordering falls back to FROM traces FINAL full dedup">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Conditional FINAL: fast default path, full cost only on the non-default path</text>
  <rect x="20" y="40" width="330" height="140" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="185" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">default ordering (by time) · no FINAL</text>
  <rect x="38" y="76" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--blue)"/><text x="185" y="93" text-anchor="middle" font-size="8" fill="var(--ink)">ORDER BY toDate(timestamp), event_ts DESC</text>
  <rect x="38" y="108" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--blue)"/><text x="185" y="125" text-anchor="middle" font-size="7.5" fill="var(--ink)">LIMIT 1 BY id (latest row per id, in memory)</text>
  <text x="185" y="152" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">✅ CH reads only the "latest day" partition from disk</text>
  <text x="185" y="168" text-anchor="middle" font-size="7.5" fill="var(--muted)">no need to pull a month of data just to dedup — correct AND fast</text>
  <rect x="370" y="40" width="330" height="140" rx="10" fill="var(--bg)" stroke="var(--faint)"/><text x="535" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">non-default ordering · use FINAL</text>
  <rect x="388" y="76" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="535" y="93" text-anchor="middle" font-size="8" fill="var(--muted)">e.g. ordering by cost/latency</text>
  <rect x="388" y="108" width="294" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="535" y="125" text-anchor="middle" font-size="8" fill="var(--muted)">FROM traces t FINAL (full dedup)</text>
  <text x="535" y="152" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">⚠️ must read all &amp; dedup to be correct</text>
  <text x="535" y="168" text-anchor="middle" font-size="7.5" fill="var(--muted)">slower, but paid only when you actively change the sort</text>
</svg>
<div class="figcap"><b>Correct AND fast</b>: default time-ordering uses <code>toDate(timestamp), event_ts DESC</code> + <code>LIMIT 1 BY id</code> instead of <code>FINAL</code>, so CH reads only the latest partition and takes each id's latest row in memory; only when you <strong>sort by a non-time column</strong> does it fall back to <code>FROM traces FINAL</code> full dedup. Source comment: <code>traces-ui-table-service.ts:443-455</code>.</div>
</div>

<div class="cols">
  <div class="col"><h4>🟢 default path (most common)</h4><p>time-ordered + no metrics needed → no FINAL, no JOINs, read only the latest partition. This is the 80% "open the list and glance" case — correct and blazing fast.</p></div>
  <div class="col"><h4>🟡 heavy path (pay on demand)</h4><p>sort by cost, or want metrics → only then add FINAL and LEFT JOIN observations/scores. Complexity is introduced only when you <strong>actively ask</strong>, never burdening the common path.</p></div>
</div>

<table class="t">
  <tr><th>select shape</th><th>what it fetches</th><th>used for</th></tr>
  <tr><td><code>rows</code></td><td>~12 compact columns</td><td>the table body, rendered immediately</td></tr>
  <tr><td><code>metrics</code></td><td>cost/latency/score aggregates (2 JOINs)</td><td>metric columns, filled in later</td></tr>
  <tr><td><code>count</code></td><td><code>uniqExact(id)</code></td><td>pagination total (deduped count)</td></tr>
  <tr><td><code>identifiers</code></td><td>just the id list</td><td>batch actions, cross-page selection</td></tr>
</table>

<h2>Table state: URL is the source of truth, three layers of persistence</h2>
<p>A list isn't just "draw some rows". You tweaked column order, set filters, sorted, saved a "view preset" — where should this <strong>table state</strong> live?
Langfuse's answer is <strong>three layers, with the URL as the source of truth</strong>:</p>

<svg viewBox="0 0 720 230" role="img" aria-label="table state has three layers by increasing lifetime: the URL is source-of-truth and sharing (filters/sort/search/view id encoded into the link, send it to reproduce), session storage is this-navigation memory (column widths/visible columns/scroll, cleared when the tab closes), and the database holds permanent saved views (cross-device, team-shared, gracefully degrading when stale)">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="24" y="44" width="204" height="122" rx="10" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="126" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">URL · source of truth</text>
  <text x="126" y="90" font-size="10.5" text-anchor="middle" fill="var(--muted)">sharing + deep link</text>
  <text x="126" y="114" font-size="10" text-anchor="middle" fill="var(--ink)">filter/sort/search/view id</text>
  <text x="126" y="138" font-size="10" text-anchor="middle" fill="var(--ink)">→ send link, reproduce</text>
  <text x="126" y="158" font-size="9.5" text-anchor="middle" fill="var(--muted)">scope: shareable now</text>
  <rect x="258" y="44" width="204" height="122" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">session storage</text>
  <text x="360" y="90" font-size="10.5" text-anchor="middle" fill="var(--muted)">navigation memory</text>
  <text x="360" y="114" font-size="10" text-anchor="middle" fill="var(--ink)">widths/columns/scroll</text>
  <text x="360" y="138" font-size="10" text-anchor="middle" fill="var(--ink)">→ kept across jumps</text>
  <text x="360" y="158" font-size="9.5" text-anchor="middle" fill="var(--muted)">scope: cleared on close</text>
  <rect x="492" y="44" width="204" height="122" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="594" y="70" font-size="13" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">database</text>
  <text x="594" y="90" font-size="10.5" text-anchor="middle" fill="var(--muted)">permanent saved view</text>
  <text x="594" y="114" font-size="10" text-anchor="middle" fill="var(--ink)">cross-device · team-shared</text>
  <text x="594" y="138" font-size="10" text-anchor="middle" fill="var(--ink)">→ graceful degrade</text>
  <text x="594" y="158" font-size="9.5" text-anchor="middle" fill="var(--muted)">scope: kept forever</text>
  <line x1="24" y1="194" x2="696" y2="194" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="360" y="216" font-size="11" text-anchor="middle" fill="var(--muted)">increasing lifetime →: URL (shareable now) · session (this navigation) · DB (permanent)</text>
</svg>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">URL</span><span class="name">sharing &amp; source of truth</span></div><div class="ld">Filters, sort, search, current view id are all encoded into the <strong>URL</strong>. So you send a colleague the link and they see <strong>exactly the same thing</strong> — the URL is the single source of truth for "what this table looks like right now" (echoing Lesson 23's FilterState).</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">session storage</span><span class="name">navigation memory</span></div><div class="ld">Hopping between tables, <strong>session storage</strong> remembers your recent column widths, visible columns, scroll position so you aren't reset each time you return — valid only within this browsing session.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">database</span><span class="name">permanent presets</span></div><div class="ld">"View presets" (saved views) go into the <strong>DB</strong>, permanent, cross-device, team-shareable. Deleted a preset, or a column it referenced no longer exists? <strong>Graceful degradation</strong>: drop the invalid part + warn, never a blank screen.</div></div>
</div>

<p>The three layers each own a timescale — URL "shareable right now", session "this navigation", DB "permanent" — together letting a big table be
<strong>deep-linkable, state-preserving across navigation, and a long-term home for the team's go-to views</strong>. Paired with a global time range (Zustand default
⊕ URL explicit), it becomes the mandatory <code>timestamp</code> filter feeding Lesson 22's look-back windows, nailing down the scan range. <strong>State layering is
the other half of a big list's craft beyond "fast" — "stable" (no loss across navigation) and "shareable" (one link reproduces the whole view).</strong></p>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why not fetch it all at once (rows + all metrics), instead of two calls and a pile of "on-demand" switches?</strong> Because <strong>the list's experience
  goal is "instant", while metrics are inherently expensive</strong>. Cost, latency, scores need 2 big-table JOINs to compute; bound to the rows, the whole table must
  <strong>wait for the slowest call</strong> to show — the user stares at blank space. Split them and the compact rows (cheap, everyone wants) <strong>arrive
  instantly</strong>, metrics fill in as "extra info" as computed; perceived latency drops from "slowest call" to "fastest call". Likewise, <strong>conditional FINAL
  and conditional JOIN</strong> are the same wisdom: <strong>optimize ruthlessly for the most common, simplest path, deferring complexity and cost until "you actually
  ask"</strong>. This is the golden rule of high-frequency list performance — don't let the 1% advanced need (sort by cost, see all metrics) slow the 99% daily browse.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>One <code>getTracesTableGeneric</code> serves <strong>four shapes</strong> (<code>rows / metrics / count / identifiers</code>), distinguished by <code>select</code> with type-safe overloads.</li>
    <li><strong>Compact rows vs metrics, split</strong>: the UI fires <code>traces.all</code> (rows) + <code>traces.metrics</code> (metrics) in parallel; <code>joinTableCoreAndMetrics</code> merges by id and returns success even without metrics, so the table <strong>renders from rows first</strong>.</li>
    <li><strong>Conditional JOIN</strong>: LEFT JOIN observations/scores only when filter/sort needs it or <code>select==="metrics"</code>, saving two JOINs on default browsing.</li>
    <li><strong>Conditional FINAL</strong>: default time-ordering uses <code>toDate(timestamp),event_ts DESC</code> + <code>LIMIT 1 BY id</code> to read only the latest partition; non-default ordering falls back to <code>FROM traces FINAL</code> full dedup.</li>
    <li>Golden rule: optimize for the most common path, defer complexity/cost until "actually asked". Table state lives in <strong>three layers, URL as source of truth</strong> (URL ⊕ session ⊕ DB presets with graceful degradation); the global time range becomes the mandatory timestamp filter feeding Lesson 22's look-back windows.</li>
  </ul>
</div>
""")
LESSON_24 = {"zh": "\n".join(_ZH24), "en": "\n".join(_EN24)}


# ══════════════════════════════════════════════════════════════════════
# L25 · trace 详情与观测树 / Trace detail & the observation tree
# ══════════════════════════════════════════════════════════════════════
_ZH25 = []
_EN25 = []

_ZH25.append(r"""
<p class="lead">
第 24 课是<strong>列表</strong>——给几千条 trace 各取一行紧凑数据、把昂贵的都推迟。这一课是它的<strong>反面</strong>：<strong>详情页</strong>。点开一条 trace，你要看的是<strong>整棵观测树 + 所有评分</strong>——
一次<strong>全量取</strong>。为什么敢全取？因为「一条 trace」本身是<strong>有界</strong>的（不是几千条的列表）。但树里每个观测的 input/output 可能<strong>巨大</strong>，所以详情依然有纪律：
树查询<strong>不带 IO</strong>（点开某节点才懒加载），再用一个 <code>verbosity</code> 旋钮给 trace 自身的 IO 封顶。<strong>同一套「限制无界维度」的功夫，换了个尺度施展。</strong>
</p>

<div class="card analogy">
  <div class="tag">📖 生活类比</div>
  把列表和详情想成<strong>图书馆目录</strong>与<strong>一本书</strong>。目录（列表）给你几千本书的<strong>小卡片</strong>，谁也不会把整本书抄上去。可当你<strong>抽出某一本</strong>（详情），
  你要的是<strong>整本书的结构</strong>——目录、章节、页码一览无余。但你<strong>不会一上来就把每一页的长篇脚注全复印下来</strong>；只有翻到某页、想细看时，才去读那条脚注（某个观测的 IO 懒加载）。
  「<strong>整本书的骨架一次给全，单页的长内容用到才取</strong>」——这就是详情页在「全量」与「克制」之间的平衡。
</div>
""")

# (L25 sections appended below)

_ZH25.append(r"""
<h2>一次取全树，但树上不挂 IO</h2>
<p>详情页的主查询是 <code>byIdWithObservationsAndScores</code>。它跑在 <code>protectedGetTraceProcedure</code> 上——这道门（第 21 课）已经<strong>预取了 trace 本体并校验过访问权</strong>（还允许公开分享的 trace）。
然后它<strong>并行</strong>取两样：整棵<strong>观测树</strong>和这条 trace 的<strong>全部评分</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="byIdWithObservationsAndScores 并行取观测树（不含 IO）与评分，partition 出 CORRECTION，从观测起止派生 latency，返回不带 IO 的树，点开节点再懒加载 IO">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">详情：一次取全树（结构+时序），IO 留到点开再取</text>
  <rect x="20" y="42" width="150" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="95" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">门已预取 trace</text><text x="95" y="76" text-anchor="middle" font-size="7" fill="var(--accent-ink)">protectedGetTraceProcedure</text><text x="95" y="87" text-anchor="middle" font-size="6.8" fill="var(--muted)">校验访问权（含公开）</text>
  <rect x="200" y="34" width="180" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="290" y="53" text-anchor="middle" font-size="8" fill="var(--ink)">getObservationsForTrace（树）</text>
  <rect x="200" y="70" width="180" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="290" y="89" text-anchor="middle" font-size="8" fill="var(--ink)">getScoresAndCorrections（评分）</text>
  <text x="290" y="118" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">↑ Promise.all 并行 ↑</text>
  <rect x="410" y="40" width="140" height="92" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="480" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">组装</text><text x="480" y="78" text-anchor="middle" font-size="7.5" fill="var(--ink)">partition 出 CORRECTION</text><text x="480" y="93" text-anchor="middle" font-size="7.5" fill="var(--ink)">从起止派生 latency</text><text x="480" y="108" text-anchor="middle" font-size="7.5" fill="var(--ink)">观测 IO 置空</text><text x="480" y="122" text-anchor="middle" font-size="7" fill="var(--muted)">includeIO:false</text>
  <rect x="578" y="40" width="128" height="44" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="642" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">返回：树 + 评分</text><text x="642" y="73" text-anchor="middle" font-size="7" fill="var(--muted)">结构、时序，无 IO</text>
  <rect x="578" y="94" width="128" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="642" y="111" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">点开某节点 →</text><text x="642" y="125" text-anchor="middle" font-size="7" fill="var(--accent-ink)">懒加载该观测 IO</text>
  <line x1="170" y1="60" x2="198" y2="50" stroke="var(--faint)" stroke-width="1.3"/><line x1="170" y1="72" x2="198" y2="84" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="380" y1="84" x2="408" y2="84" stroke="var(--faint)" stroke-width="1.4"/><polygon points="408,84 400,80 400,88" fill="var(--faint)"/>
  <line x1="550" y1="70" x2="576" y2="62" stroke="var(--faint)" stroke-width="1.3"/><line x1="550" y1="100" x2="576" y2="110" stroke="var(--accent)" stroke-width="1.3"/>
  <rect x="40" y="150" width="660" height="76" rx="9" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="170" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">一棵观测树（结构与时序）：</text>
  <text x="80" y="190" font-size="9" fill="var(--ink)">▸ trace</text><text x="120" y="206" font-size="9" fill="var(--ink)">▸ span: 检索</text><text x="180" y="222" font-size="9" fill="var(--muted)">• generation: LLM 调用（IO 点开才取）</text><text x="470" y="206" font-size="8" fill="var(--muted)">右侧：getAgentGraphData → agent 图视图</text>
</svg>
<div class="figcap"><b>取全骨架、缓取血肉</b>：<code>byIdWithObservationsAndScores</code> 并行取观测树（<code>includeIO:false</code>）与评分，partition 出 CORRECTION 类分数、从观测起止派生 latency，返回<strong>不含 IO</strong> 的树；点开某节点才懒加载它的 IO。另有 <code>getAgentGraphData</code> 供 agent 图。源码：<code>web/src/server/api/routers/traces.ts:368,610</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/api/routers/traces.ts</span><span class="ln">byIdWithObservationsAndScores :368</span></div>
  <pre class="code"><span class="cm">// ctx.trace 已由门预取（含权限校验）；并行取树与评分</span>
<span class="kw">const</span> [observations, traceScores] = <span class="kw">await</span> Promise.<span class="fn">all</span>([
  <span class="fn">getObservationsForTrace</span>({ traceId, projectId, includeIO: <span class="kw">false</span> }), <span class="cm">// 树不带 IO</span>
  <span class="fn">getScoresAndCorrectionsForTraces</span>({ projectId, traceIds: [traceId] }),
]);
<span class="cm">// CORRECTION 类分数单独分出来</span>
<span class="kw">const</span> [corrections, scores] = <span class="fn">partition</span>(scores, (s) =&gt; s.dataType === <span class="st">"CORRECTION"</span>);
<span class="cm">// 从观测的最早起、最晚止派生整条 trace 的延迟</span>
<span class="kw">const</span> latencyMs = maxEnd - minStart;
<span class="kw">return</span> { ...trace, observations: obs.<span class="fn">map</span>((o) =&gt; ({ ...o, input: undefined, output: undefined })) };</pre>
</div>

<p>注意 <code>includeIO: false</code> 这个不起眼的参数——它是详情页性能的关键。设想一条 agent trace 有<strong>三百个观测</strong>，每个观测的 input/output 又是一段不短的 JSON：
如果开树时就把全部 IO 一并拉回，光这一个请求就可能是几十 MB、几秒钟。Langfuse 的选择是<strong>树先到、IO 后取</strong>：</p>

<svg viewBox="0 0 720 200" role="img" aria-label="整条 trace 的延迟不是单独存的，而是从观测的最早起 minStart 与最晚止 maxEnd 派生：多条观测在时间轴上错落分布，latencyMs 等于 maxEnd 减 minStart">
  <rect x="0" y="0" width="720" height="200" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">整条 trace 的延迟：从观测的最早起、最晚止派生（不单独存）</text>
  <line x1="60" y1="150" x2="688" y2="150" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="684" y="144" font-size="9.5" text-anchor="end" fill="var(--muted)">时间 →</text>
  <rect x="80" y="44" width="200" height="16" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="86" y="56" font-size="9" fill="var(--ink)">span: 检索</text>
  <rect x="150" y="68" width="330" height="16" rx="4" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="156" y="80" font-size="9" fill="var(--ink)">generation: LLM 调用</text>
  <rect x="300" y="92" width="180" height="16" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="306" y="104" font-size="9" fill="var(--ink)">tool: 调外部 API</text>
  <rect x="420" y="116" width="200" height="16" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="426" y="128" font-size="9" fill="var(--ink)">span: 汇总</text>
  <line x1="80" y1="40" x2="80" y2="162" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="80" y="38" font-size="9" text-anchor="middle" fill="var(--accent-ink)">minStart</text>
  <line x1="620" y1="40" x2="620" y2="162" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="620" y="38" font-size="9" text-anchor="middle" fill="var(--accent-ink)">maxEnd</text>
  <line x1="80" y1="174" x2="620" y2="174" stroke="var(--accent)" stroke-width="2"></line>
  <text x="350" y="192" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">latencyMs = maxEnd − minStart（派生口径，永远和观测一致）</text>
</svg>

<div class="cols">
  <div class="col"><h4>😖 树带全 IO</h4><p>一次拉回三百个观测 + 它们的全部 IO，请求几十 MB、慢且占内存。可你打开详情时，<strong>大多数节点你压根不会展开</strong>——绝大部分 IO 是白拉的。</p></div>
  <div class="col"><h4>😀 树先到，IO 懒加载</h4><p>树查询只带<strong>结构与时序</strong>（轻、快），整棵树<strong>立刻可见</strong>；你点开哪个观测，才去取<strong>那一个</strong>的 IO。按需付费，绝不为没看的节点买单——这也让超大 trace 的详情页依然能秒开。</p></div>
</div>
""")

# (verbosity + contrast section below)

_ZH25.append(r"""
<h2>verbosity 旋钮：给「巨型 trace」的 IO 封顶</h2>
<p>就算是一条 trace，它<strong>自身</strong>的 input/output 也可能是个几 MB 的大 JSON（比如塞了整段长上下文）。为此，单条 trace 的查询 <code>byId</code> 带一个 <code>verbosity</code> 参数（<code>compact / truncated / full</code>），
在<strong>服务端</strong>就决定 IO 要不要解析、要不要截断——别让一个超大 trace 把响应撑爆：</p>

<p>为什么要在<strong>服务端</strong>而不是前端截断？因为<strong>等数据传到前端再裁，已经晚了</strong>——那几 MB 已经从 ClickHouse 读出、序列化、走完网络。<code>verbosity</code> 让裁剪发生在<strong>最靠近数据源的地方</strong>：
该不带 IO 的（compact）压根不取，该截断的（truncated）在序列化前就截短，只有明确要看全（full）才完整返回。同一个 <code>byId</code> 接口，因此能既服务「列表里要个轻量预览」又服务「详情页要看全文」，靠一个参数切换姿态。</p>

<div class="fig">
<svg viewBox="0 0 720 170" role="img" aria-label="verbosity 三档：compact 不取 IO、truncated 截断 IO、full 完整 IO，在服务端决定，给巨型 trace 的 IO 封顶">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">verbosity：在服务端就给 IO 定档</text>
  <rect x="30" y="40" width="200" height="106" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="130" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">compact</text><text x="130" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">不带 IO，最轻</text><text x="130" y="104" text-anchor="middle" font-size="7.5" fill="var(--faint)">列表/概览场景</text><text x="130" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">载荷最小</text>
  <rect x="260" y="40" width="200" height="106" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">truncated</text><text x="360" y="84" text-anchor="middle" font-size="8" fill="var(--accent-ink)">IO 截断到上限</text><text x="360" y="104" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">巨型 trace 也不撑爆</text><text x="360" y="124" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">够看个大概</text>
  <rect x="490" y="40" width="200" height="106" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="590" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">full（默认）</text><text x="590" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">完整 IO</text><text x="590" y="104" text-anchor="middle" font-size="7.5" fill="var(--faint)">单条详情、要看全</text><text x="590" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">载荷最大</text>
</svg>
<div class="figcap"><b>三档封顶</b>：<code>byId</code> 的 <code>verbosity</code>（<code>compact / truncated / full</code>，默认 full）在服务端决定 trace 自身 IO 是否解析/截断，给超大 trace 的响应封顶。源码：<code>web/src/server/api/trpc.ts:480,524-525</code>（<code>parseIO(input, verbosity)</code>）。</div>
</div>

<p>从用户视角看，打开一条 trace 详情的完整体验是这样五步——树几乎瞬间出现，细节随你的点击逐步充实：</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>进门预取 + 校验</h4><p><code>protectedGetTraceProcedure</code> 已把 trace 本体取好、并确认你有权访问（公开分享的 trace 也放行）。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>并行取树与评分</h4><p><code>Promise.all</code> 同时拉观测树（不带 IO）与全部评分，两者谁慢等谁、但一起发出。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>组装并渲染骨架</h4><p>partition 出 CORRECTION、派生 latency，整棵<strong>观测树的结构与时序立刻画出</strong>——你马上能看清这次调用的全貌。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>点开节点，懒加载 IO</h4><p>你点某个 generation 想看它的 prompt/completion，前端才去取<strong>那一个</strong>观测的 IO，按 verbosity 决定完整还是截断。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>（可选）切到 agent 图</h4><p>想看 agent 的步骤拓扑？<code>getAgentGraphData</code> 另起一路，把这棵树渲染成一张有向图（trace-graph-view），让多步 agent 的调用关系一眼看清。</p></div></div>
</div>

<p>把第 24、25 两课摆在一起，「同一套纪律、两个尺度」就一目了然了——<strong>无论列表还是详情，都先圈定有界的维度、把无界的维度往后推</strong>：</p>

<table class="t">
  <tr><th></th><th>列表（第 24 课）</th><th>详情（本课）</th></tr>
  <tr><td><b>有界的，先取</b></td><td>几千条 trace 的<strong>紧凑行</strong>（每条 ~12 列）</td><td>一条 trace 的<strong>整棵观测树</strong>（结构+时序）</td></tr>
  <tr><td><b>无界的，缓取</b></td><td>成本/延迟/评分<strong>指标</strong>（要 JOIN）→ 并行后到</td><td>每个观测的 <strong>IO</strong>（可能巨大）→ 点开懒加载</td></tr>
  <tr><td><b>封顶手段</b></td><td>分页、回看时间窗、按需 FINAL/JOIN</td><td>树查询不带 IO、<code>verbosity</code> 截断 trace 自身 IO</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么详情敢「一次取全树」，列表却要「极力推迟」？</strong> 关键在<strong>有界性</strong>。列表面对的是<strong>无界的行数</strong>（几千、几万条 trace），所以连一行里稍贵的列都得推迟；
  详情面对的是<strong>一条 trace</strong>——它的观测数量再多也是<strong>有界</strong>的，而且「看清这一条的全貌」正是详情页的价值，所以结构与时序值得一次取全。
  但<strong>有界的实体里仍藏着无界的维度</strong>：单个观测的 IO 可以是 2MB 的 JSON，几百个观测叠起来又会爆。于是同一套「圈定有界、推迟无界」的纪律<strong>下沉到树内部</strong>——
  树取全（有界的结构），IO 缓取（无界的内容），再用 verbosity 给 trace 自身 IO 封顶。<strong>不是「列表克制、详情放纵」，而是两者都在各自的尺度上做同一件事：只急着取你扛得住的那部分。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li>详情页主查询 <code>byIdWithObservationsAndScores</code> 跑在 <code>protectedGetTraceProcedure</code> 上（门已<strong>预取 trace 并校验访问权</strong>，含公开分享）。</li>
    <li><strong>并行</strong>取观测树 + 评分；<code>partition</code> 出 CORRECTION 类分数；从观测起止<strong>派生 latency</strong>。</li>
    <li><strong>树不带 IO</strong>（<code>includeIO:false</code>，观测 input/output 置空）——点开某节点才<strong>懒加载</strong>它的 IO，避免一次拉几百个观测的巨型内容、让超大 trace 详情也能秒开。</li>
    <li><code>verbosity</code>（<code>compact / truncated / full</code>）在<strong>服务端</strong>给 trace 自身 IO 定档/截断，防超大 trace 撑爆响应。另有 <code>getAgentGraphData</code> 供 agent 图视图。</li>
    <li>与第 24 课「同一纪律、两个尺度」：<strong>先取有界维度（列表=紧凑行 / 详情=树结构），推迟无界维度（列表=指标 / 详情=观测 IO）</strong>——只急着取你扛得住的那部分。</li>
  </ul>
</div>
""")

_EN25.append(r"""
<p class="lead">
Lesson 24 was the <strong>list</strong> — fetch one compact row each for thousands of traces, defer everything expensive. This lesson is its <strong>opposite</strong>:
the <strong>detail page</strong>. Open one trace and you want the <strong>whole observation tree + all scores</strong> — one <strong>full fetch</strong>. Why dare to fetch
it all? Because "one trace" is <strong>bounded</strong> (not a list of thousands). But each observation's input/output in the tree could be <strong>huge</strong>, so the
detail still has discipline: the tree query carries <strong>no IO</strong> (lazy-loaded per node when you expand it), with a <code>verbosity</code> knob capping the
trace's own IO. <strong>The same "bound the unbounded dimension" craft, applied at a different scale.</strong>
</p>

<div class="card analogy">
  <div class="tag">📖 Analogy</div>
  Think of list vs detail as a <strong>library catalog</strong> vs <strong>one book</strong>. The catalog (list) gives you <strong>tiny cards</strong> for thousands of
  books — nobody transcribes a whole book onto a card. But when you <strong>pull one book</strong> (detail), you want the <strong>whole book's structure</strong> — table
  of contents, chapters, page numbers at a glance. Yet you <strong>don't photocopy every page's long footnotes upfront</strong>; only when you flip to a page and want
  the detail do you read that footnote (an observation's IO, lazy-loaded). "<strong>The whole book's skeleton at once, a page's long content fetched on demand</strong>"
  — that's the detail page's balance between "complete" and "restraint".
</div>
""")

_EN25.append(r"""
<h2>Fetch the whole tree at once, but hang no IO on it</h2>
<p>The detail page's main query is <code>byIdWithObservationsAndScores</code>. It runs on <code>protectedGetTraceProcedure</code> — that door (Lesson 21) has already
<strong>prefetched the trace itself and verified access</strong> (allowing publicly shared traces too). It then fetches two things <strong>in parallel</strong>: the
whole <strong>observation tree</strong> and all of this trace's <strong>scores</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="byIdWithObservationsAndScores fetches the observation tree (no IO) and scores in parallel, partitions out CORRECTION, derives latency from observation start/end, returns the IO-less tree, and lazy-loads IO when a node is opened">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Detail: fetch the whole tree (structure+timing), IO on click</text>
  <rect x="20" y="42" width="150" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="95" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">door prefetched trace</text><text x="95" y="76" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">protectedGetTraceProcedure</text><text x="95" y="87" text-anchor="middle" font-size="6.8" fill="var(--muted)">access verified (incl. public)</text>
  <rect x="200" y="34" width="180" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="290" y="53" text-anchor="middle" font-size="8" fill="var(--ink)">getObservationsForTrace (tree)</text>
  <rect x="200" y="70" width="180" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="290" y="89" text-anchor="middle" font-size="7.5" fill="var(--ink)">getScoresAndCorrections (scores)</text>
  <text x="290" y="118" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">↑ Promise.all parallel ↑</text>
  <rect x="410" y="40" width="140" height="92" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="480" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">assemble</text><text x="480" y="78" text-anchor="middle" font-size="7.5" fill="var(--ink)">partition out CORRECTION</text><text x="480" y="93" text-anchor="middle" font-size="7.5" fill="var(--ink)">derive latency from spans</text><text x="480" y="108" text-anchor="middle" font-size="7.5" fill="var(--ink)">strip observation IO</text><text x="480" y="122" text-anchor="middle" font-size="7" fill="var(--muted)">includeIO:false</text>
  <rect x="578" y="40" width="128" height="44" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="642" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">return: tree + scores</text><text x="642" y="73" text-anchor="middle" font-size="7" fill="var(--muted)">structure, timing, no IO</text>
  <rect x="578" y="94" width="128" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="642" y="111" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">open a node →</text><text x="642" y="125" text-anchor="middle" font-size="7" fill="var(--accent-ink)">lazy-load that IO</text>
  <line x1="170" y1="60" x2="198" y2="50" stroke="var(--faint)" stroke-width="1.3"/><line x1="170" y1="72" x2="198" y2="84" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="380" y1="84" x2="408" y2="84" stroke="var(--faint)" stroke-width="1.4"/><polygon points="408,84 400,80 400,88" fill="var(--faint)"/>
  <line x1="550" y1="70" x2="576" y2="62" stroke="var(--faint)" stroke-width="1.3"/><line x1="550" y1="100" x2="576" y2="110" stroke="var(--accent)" stroke-width="1.3"/>
  <rect x="40" y="150" width="660" height="76" rx="9" fill="none" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="360" y="170" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">one observation tree (structure &amp; timing):</text>
  <text x="80" y="190" font-size="9" fill="var(--ink)">▸ trace</text><text x="120" y="206" font-size="9" fill="var(--ink)">▸ span: retrieval</text><text x="200" y="222" font-size="9" fill="var(--muted)">• generation: LLM call (IO fetched on click)</text><text x="480" y="206" font-size="8" fill="var(--muted)">right: getAgentGraphData → agent graph view</text>
</svg>
<div class="figcap"><b>Fetch the skeleton, defer the flesh</b>: <code>byIdWithObservationsAndScores</code> fetches the observation tree (<code>includeIO:false</code>) and scores in parallel, partitions out CORRECTION-type scores, derives latency from observation start/end, returns the <strong>IO-less</strong> tree; opening a node lazy-loads its IO. Plus <code>getAgentGraphData</code> for the agent graph. Source: <code>web/src/server/api/routers/traces.ts:368,610</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/api/routers/traces.ts</span><span class="ln">byIdWithObservationsAndScores :368</span></div>
  <pre class="code"><span class="cm">// ctx.trace prefetched by the door (with access check); fetch tree &amp; scores in parallel</span>
<span class="kw">const</span> [observations, traceScores] = <span class="kw">await</span> Promise.<span class="fn">all</span>([
  <span class="fn">getObservationsForTrace</span>({ traceId, projectId, includeIO: <span class="kw">false</span> }), <span class="cm">// tree without IO</span>
  <span class="fn">getScoresAndCorrectionsForTraces</span>({ projectId, traceIds: [traceId] }),
]);
<span class="cm">// split out CORRECTION-type scores</span>
<span class="kw">const</span> [corrections, scores] = <span class="fn">partition</span>(scores, (s) =&gt; s.dataType === <span class="st">"CORRECTION"</span>);
<span class="cm">// derive the whole trace's latency from earliest start, latest end of observations</span>
<span class="kw">const</span> latencyMs = maxEnd - minStart;
<span class="kw">return</span> { ...trace, observations: obs.<span class="fn">map</span>((o) =&gt; ({ ...o, input: undefined, output: undefined })) };</pre>
</div>

<p>Note the unremarkable <code>includeIO: false</code> — it's the key to the detail page's performance. Imagine an agent trace with <strong>three hundred
observations</strong>, each observation's input/output a sizeable JSON: load all the IO when opening the tree and that one request could be tens of MB and several
seconds. Langfuse's choice is <strong>tree first, IO later</strong>:</p>

<svg viewBox="0 0 720 200" role="img" aria-label="the whole trace's latency is not stored separately but derived from the observations' earliest start minStart and latest end maxEnd: several observations are scattered across the time axis and latencyMs equals maxEnd minus minStart">
  <rect x="0" y="0" width="720" height="200" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">the trace's latency is derived from the observations' earliest start and latest end (not stored)</text>
  <line x1="60" y1="150" x2="688" y2="150" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="684" y="144" font-size="9.5" text-anchor="end" fill="var(--muted)">time →</text>
  <rect x="80" y="44" width="200" height="16" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="86" y="56" font-size="9" fill="var(--ink)">span: retrieve</text>
  <rect x="150" y="68" width="330" height="16" rx="4" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="156" y="80" font-size="9" fill="var(--ink)">generation: LLM call</text>
  <rect x="300" y="92" width="180" height="16" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="306" y="104" font-size="9" fill="var(--ink)">tool: external API</text>
  <rect x="420" y="116" width="200" height="16" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="426" y="128" font-size="9" fill="var(--ink)">span: summarize</text>
  <line x1="80" y1="40" x2="80" y2="162" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="80" y="38" font-size="9" text-anchor="middle" fill="var(--accent-ink)">minStart</text>
  <line x1="620" y1="40" x2="620" y2="162" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <text x="620" y="38" font-size="9" text-anchor="middle" fill="var(--accent-ink)">maxEnd</text>
  <line x1="80" y1="174" x2="620" y2="174" stroke="var(--accent)" stroke-width="2"></line>
  <text x="350" y="192" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">latencyMs = maxEnd − minStart (derived, always consistent with the observations)</text>
</svg>

<div class="cols">
  <div class="col"><h4>😖 tree with all IO</h4><p>Fetch three hundred observations + all their IO at once: a tens-of-MB request, slow and memory-heavy. But when you open the detail, <strong>you won't expand most nodes</strong> — most of that IO was fetched for nothing.</p></div>
  <div class="col"><h4>😀 tree first, IO lazy</h4><p>The tree query carries only <strong>structure and timing</strong> (light, fast), so the whole tree is <strong>visible immediately</strong>; expand an observation and only <strong>that one's</strong> IO is fetched. Pay on demand, never for nodes you didn't look at — so even a huge trace's detail page opens instantly.</p></div>
</div>
""")

_EN25.append(r"""
<h2>The verbosity knob: capping IO for "giant traces"</h2>
<p>Even one trace's <strong>own</strong> input/output could be a multi-MB JSON (say, stuffed with a long context). For this, the single-trace query <code>byId</code>
carries a <code>verbosity</code> param (<code>compact / truncated / full</code>) that decides <strong>server-side</strong> whether IO is parsed or truncated — don't let a
giant trace blow up the response:</p>

<p>Why truncate <strong>server-side</strong>, not on the frontend? Because <strong>trimming after the data reaches the frontend is too late</strong> — those few MB
already got read from ClickHouse, serialized, and crossed the network. <code>verbosity</code> puts the trimming <strong>closest to the data source</strong>: what should
carry no IO (compact) isn't fetched at all, what should be truncated (truncated) is cut before serialization, and only an explicit "show all" (full) returns the
whole thing. So one <code>byId</code> endpoint serves both "a lightweight preview in a list" and "see the full text on a detail page", switching posture by a single
parameter.</p>

<div class="fig">
<svg viewBox="0 0 720 170" role="img" aria-label="verbosity three levels: compact no IO, truncated cut IO, full complete IO, decided server-side to cap giant-trace IO">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">verbosity: tier the IO server-side</text>
  <rect x="30" y="40" width="200" height="106" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="130" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">compact</text><text x="130" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">no IO, lightest</text><text x="130" y="104" text-anchor="middle" font-size="7.5" fill="var(--faint)">list/overview cases</text><text x="130" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">smallest payload</text>
  <rect x="260" y="40" width="200" height="106" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">truncated</text><text x="360" y="84" text-anchor="middle" font-size="8" fill="var(--accent-ink)">IO cut to a cap</text><text x="360" y="104" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">giant traces don't blow up</text><text x="360" y="124" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">enough for the gist</text>
  <rect x="490" y="40" width="200" height="106" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="590" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">full (default)</text><text x="590" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">complete IO</text><text x="590" y="104" text-anchor="middle" font-size="7.5" fill="var(--faint)">single detail, see it all</text><text x="590" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">largest payload</text>
</svg>
<div class="figcap"><b>Three-tier cap</b>: <code>byId</code>'s <code>verbosity</code> (<code>compact / truncated / full</code>, default full) decides server-side whether the trace's own IO is parsed/truncated, capping the response for huge traces. Source: <code>web/src/server/api/trpc.ts:480,524-525</code> (<code>parseIO(input, verbosity)</code>).</div>
</div>

<p>From the user's view, opening a trace detail is five steps — the tree appears almost instantly, details fill in as you click:</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>door prefetch + verify</h4><p><code>protectedGetTraceProcedure</code> has already fetched the trace and confirmed your access (publicly shared traces pass too).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>parallel fetch tree &amp; scores</h4><p><code>Promise.all</code> pulls the observation tree (no IO) and all scores at once — both fired together, wait for the slower.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>assemble &amp; render skeleton</h4><p>Partition out CORRECTION, derive latency, and the tree's <strong>structure and timing paint immediately</strong> — you see the whole call at once.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>open a node, lazy-load IO</h4><p>Click a generation to see its prompt/completion and the frontend fetches <strong>that one</strong> observation's IO, full or truncated per verbosity.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>(optional) switch to the agent graph</h4><p>Want the agent's step topology? <code>getAgentGraphData</code> takes another path, rendering the tree as a directed graph (trace-graph-view).</p></div></div>
</div>

<p>Place Lessons 24 and 25 side by side and "one discipline, two scales" is plain — <strong>whether list or detail, fence the bounded dimension first and defer the
unbounded one</strong>:</p>

<table class="t">
  <tr><th></th><th>list (Lesson 24)</th><th>detail (this lesson)</th></tr>
  <tr><td><b>bounded — fetch first</b></td><td>thousands of traces' <strong>compact rows</strong> (~12 cols each)</td><td>one trace's <strong>whole observation tree</strong> (structure+timing)</td></tr>
  <tr><td><b>unbounded — defer</b></td><td>cost/latency/score <strong>metrics</strong> (need JOINs) → parallel, later</td><td>each observation's <strong>IO</strong> (possibly huge) → lazy-load on click</td></tr>
  <tr><td><b>capping means</b></td><td>pagination, look-back windows, conditional FINAL/JOIN</td><td>tree query without IO, <code>verbosity</code> truncating the trace's own IO</td></tr>
</table>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why does detail dare to "fetch the whole tree", while the list "defers aggressively"?</strong> The key is <strong>boundedness</strong>. The list faces an
  <strong>unbounded number of rows</strong> (thousands, tens of thousands of traces), so even a slightly pricey column per row must be deferred; the detail faces
  <strong>one trace</strong> — however many observations it has, that count is <strong>bounded</strong>, and "seeing this one in full" is precisely the detail page's value, so
  the structure and timing are worth fetching all at once. But <strong>a bounded entity still hides an unbounded dimension inside</strong>: a single observation's IO can be
  a 2MB JSON, and hundreds stacked up explode again. So the same "fence the bounded, defer the unbounded" discipline <strong>descends into the tree</strong> — fetch the tree
  in full (the bounded structure), defer the IO (the unbounded content), and cap the trace's own IO with verbosity. <strong>It's not "list restrained, detail
  indulgent"; both do the same thing at their own scale: only rush to fetch the part you can bear.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li>The detail page's main query <code>byIdWithObservationsAndScores</code> runs on <code>protectedGetTraceProcedure</code> (the door <strong>prefetched the trace and verified access</strong>, including public shares).</li>
    <li><strong>Parallel</strong> fetch of the observation tree + scores; <code>partition</code> out CORRECTION-type scores; <strong>derive latency</strong> from observation start/end.</li>
    <li><strong>Tree without IO</strong> (<code>includeIO:false</code>, observation input/output stripped) — opening a node <strong>lazy-loads</strong> its IO, avoiding pulling hundreds of observations' huge content at once.</li>
    <li><code>verbosity</code> (<code>compact / truncated / full</code>) tiers/truncates the trace's own IO <strong>server-side</strong>, preventing huge traces from blowing up the response. Plus <code>getAgentGraphData</code> for the agent graph view.</li>
    <li>With Lesson 24, "one discipline, two scales": <strong>fetch the bounded dimension first (list=compact rows / detail=tree structure), defer the unbounded one (list=metrics / detail=observation IO)</strong> — only rush to fetch the part you can bear.</li>
  </ul>
</div>
""")
LESSON_25 = {"zh": "\n".join(_ZH25), "en": "\n".join(_EN25)}


# ══════════════════════════════════════════════════════════════════════
# L26 · sessions / Sessions
# ══════════════════════════════════════════════════════════════════════
_ZH26 = []
_EN26 = []

_ZH26.append(r"""
<p class="lead">
第 24、25 课讲的是单条 trace 的列表与详情。可真实的对话往往是<strong>多轮</strong>的——用户问一句、AI 答一句，来回十几轮，每一轮是一条 trace。把它们<strong>串成一段完整对话</strong>的，就是
<strong>session（会话）</strong>。这一课的关键洞察出奇地简洁：<strong>会话的全部「指标与列表」都不单独存储，而是 traces 按 <code>session_id</code> 的一次「分组聚合」现算出来</strong>
（仅有一个极轻的元数据存根落库，下面会讲）。更妙的是，会话表<strong>几乎原样复用了第 24 课那套表格机制</strong>——说白了，<strong>它就是 trace 表，分了个组</strong>。
</p>

<div class="card analogy">
  <div class="tag">💬 生活类比</div>
  把 session 想成聊天软件里的<strong>一个对话框</strong>，把 trace 想成里面的<strong>一条条消息</strong>。每条消息都<strong>单独存着</strong>，但你是把它们当成<strong>一整段对话</strong>来读的。
  这个「对话框」<strong>并不是另外存在某处的一个东西</strong>——它只是「<strong>所有带同一个会话号的消息，凑到一起显示，再配一行摘要</strong>」：谁参与了、聊了几轮、持续多久、总共花了多少钱。
  你不需要为「对话框」单独建一张表、单独维护——它<strong>从消息里自然长出来</strong>。Langfuse 的 session 正是这么来的。
</div>
""")

# (L26 sections appended below)

_ZH26.append(r"""
<h2>session = traces 按 session_id 分组</h2>
<p>回想第 8 课：<code>session_id</code> 只是 traces 宽表上的<strong>一个普通列</strong>。所以会话的<strong>指标与列表不必单独存</strong>——只要把同一个 <code>session_id</code> 的 traces <strong>GROUP BY 聚到一起</strong>，
就得到一行「会话」，它的各项指标都是<strong>对组内 traces 的聚合</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="多条带相同 session_id 的 trace 经 GROUP BY session_id 聚成一行会话，聚合出 user_ids、trace_count、duration（最早到最晚）、session_total_cost">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">GROUP BY session_id：多条 trace → 一行会话</text>
  <rect x="20" y="44" width="250" height="150" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="145" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">traces 表（第 8 课宽表）</text>
  <rect x="36" y="74" width="218" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="46" y="91" font-size="7.5" fill="var(--ink)">trace#1 · session_id=<tspan font-weight="700" fill="var(--accent-ink)">S1</tspan> · user=A · $0.01</text>
  <rect x="36" y="104" width="218" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="46" y="121" font-size="7.5" fill="var(--ink)">trace#2 · session_id=<tspan font-weight="700" fill="var(--accent-ink)">S1</tspan> · user=A · $0.02</text>
  <rect x="36" y="134" width="218" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="46" y="151" font-size="7.5" fill="var(--ink)">trace#3 · session_id=<tspan font-weight="700" fill="var(--accent-ink)">S1</tspan> · user=B · $0.03</text>
  <rect x="36" y="164" width="218" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="3 2"/><text x="46" y="179" font-size="7" fill="var(--faint)">trace#4 · session_id=S2 · …（另一会话）</text>
  <rect x="306" y="84" width="120" height="60" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="366" y="108" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">GROUP BY</text><text x="366" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">session_id</text>
  <rect x="462" y="58" width="240" height="120" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="582" y="78" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">一行会话 S1</text>
  <text x="478" y="98" font-size="8" fill="var(--ink)">user_ids = [A, B]（谁参与）</text>
  <text x="478" y="116" font-size="8" fill="var(--ink)">trace_count = 3（聊了几轮）</text>
  <text x="478" y="134" font-size="8" fill="var(--ink)">duration = 最晚 − 最早（持续多久）</text>
  <text x="478" y="152" font-size="8" fill="var(--ink)">session_total_cost = $0.06（求和）</text>
  <text x="478" y="170" font-size="7.5" fill="var(--muted)">trace_ids = [#1, #2, #3]</text>
  <line x1="270" y1="114" x2="304" y2="114" stroke="var(--accent)" stroke-width="1.6"/><polygon points="304,114 295,110 295,118" fill="var(--accent)"/>
  <line x1="426" y1="114" x2="460" y2="114" stroke="var(--accent)" stroke-width="1.6"/><polygon points="460,114 451,110 451,118" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>会话是分组出来的</b>：同一 <code>session_id</code> 的 traces 经 <code>GROUP BY session_id</code> 聚成一行会话；各指标是对组内 traces 的聚合——<code>user_ids</code>（去重谁参与）、<code>trace_count</code>（计数）、<code>duration</code>（最晚 − 最早）、<code>session_total_cost</code>（求和）。源码：<code>packages/shared/src/server/services/sessions-ui-table-service.ts:86,123</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/sessions-ui-table-service.ts</span><span class="ln">getSessionsTableGeneric :123</span></div>
  <pre class="code"><span class="cm">// 和第 24 课的 getTracesTableGeneric 同一个套路：一个函数，几种「形状」（会话用 count/rows/metrics 三种）</span>
<span class="kw">const</span> getSessionsTableGeneric = <span class="kw">async</span> &lt;T&gt;(props: { select: <span class="st">"count"</span> | <span class="st">"rows"</span> | <span class="st">"metrics"</span> }) =&gt; {
  <span class="kw">switch</span> (select) {
    <span class="kw">case</span> <span class="st">"rows"</span>:    sqlSelect = <span class="st">"session_id, min/max_timestamp, trace_ids, user_ids, trace_count …"</span>; <span class="cm">// 便宜</span>
    <span class="kw">case</span> <span class="st">"metrics"</span>: sqlSelect = <span class="st">"… + duration, total_observations, session_total_cost …"</span>;      <span class="cm">// 要算</span>
  }
  <span class="cm">// 底层就是对 traces（及其 observations 求成本）GROUP BY session_id</span>
}</pre>
</div>

<p>这里有个值得留意的细节：会话的「总成本」并不直接长在 trace 上，而是要<strong>下钻到每条 trace 的 observations</strong>去求和（成本是第 16 课在 observation 上算出来的）。
所以一个会话的总成本，本质是「这个会话里所有 trace 的所有 observation 的成本」之和——一个<strong>两层的聚合</strong>。这也是为什么 <code>session_total_cost</code> 属于「贵」的 metrics 形状、要后补：
它和第 24 课列表里的成本指标一样，得跨表算。而便宜的 rows 形状只取会话身份（谁、几轮、哪些 trace_id），<strong>不碰成本</strong>，于是会话列表能<strong>先秒开、再补指标</strong>。</p>
""")

# (reuse + spark + key section below)

_ZH26.append(r"""
<h2>原样复用：会话表就是「分了组的 trace 表」</h2>
<p>看出来了吗——<code>getSessionsTableGeneric</code> 和第 24 课的 <code>getTracesTableGeneric</code> <strong>简直是一个模子</strong>：同样的<strong>「按 select 取不同形状」</strong>（会话有 count / rows / metrics 三种，比 traces 少一个 identifiers），
同样的<strong>「紧凑行 vs 指标」拆分</strong>。会话列表也是：先把便宜的会话身份行画出来，昂贵的聚合指标（duration、总成本）<strong>后到补入</strong>。第 24 课的所有性能技巧，会话<strong>白白继承</strong>：
分页、回看时间窗、按需聚合、URL 状态、列预设、行选择——这些在第 24 课里费心打磨的能力，会话表<strong>一行新代码都不用写</strong>就全有了，因为它走的是同一套通用机制。
这就是把表格系统做成<strong>「实体无关的通用件」</strong>的回报：再来一个「按某个维度聚合的列表」（会话、用户、模型……），都能套同一个模子。</p>

<div class="fig">
<svg viewBox="0 0 720 180" role="img" aria-label="会话表沿用第24课的紧凑行vs指标拆分：rows 取会话身份与 trace 列表（便宜先到），metrics 取 duration/总成本等聚合（贵后补）">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">沿用第 24 课：紧凑行先画，聚合指标后补</text>
  <rect x="30" y="42" width="300" height="118" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="180" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">rows（紧凑会话行 · 便宜 · 先到）</text>
  <text x="50" y="84" font-size="8" fill="var(--accent-ink)">session_id · min/max 时间</text>
  <text x="50" y="102" font-size="8" fill="var(--accent-ink)">trace_ids · user_ids · trace_count</text>
  <text x="50" y="120" font-size="8" fill="var(--accent-ink)">trace_tags · environment</text>
  <text x="50" y="142" font-size="7.5" fill="var(--muted)">→ 会话列表立刻可见</text>
  <rect x="390" y="42" width="300" height="118" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="540" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">metrics（聚合 · 贵 · 后补）</text>
  <text x="410" y="84" font-size="8" fill="var(--ink)">duration（持续时长）</text>
  <text x="410" y="102" font-size="8" fill="var(--ink)">total_observations（总观测数）</text>
  <text x="410" y="120" font-size="8" fill="var(--ink)">session_total_cost / usage（总成本/用量）</text>
  <text x="410" y="142" font-size="7.5" fill="var(--muted)">→ 算好再按 session_id 填进对应行</text>
</svg>
<div class="figcap"><b>同一套表格机制</b>：会话表沿用第 24 课的「四形状 + 紧凑行/指标拆分」。<code>rows</code> 取会话身份与它含的 <code>trace_ids</code>（便宜、先渲染），<code>metrics</code> 取 <code>duration</code>、<code>session_total_cost</code> 等聚合（贵、后补）。源码：<code>sessions-ui-table-service.ts:132-160</code>。</div>
</div>

<table class="t">
  <tr><th>会话指标</th><th>怎么从组内 traces 算出来</th></tr>
  <tr><td><code>user_ids</code></td><td>去重收集组内所有 trace 的 user_id（谁参与了对话）</td></tr>
  <tr><td><code>trace_count</code></td><td>计数：这个会话里有几条 trace（聊了几轮）</td></tr>
  <tr><td><code>duration</code></td><td>最晚时间戳 − 最早时间戳（整段对话持续多久）</td></tr>
  <tr><td><code>session_total_cost</code></td><td>对组内所有 trace 的成本<strong>求和</strong>（这段对话总共花了多少）</td></tr>
  <tr><td><code>trace_ids</code></td><td>收集组内所有 trace 的 id（点开会话即按序展开它们）</td></tr>
</table>

<div class="cols">
  <div class="col"><h4>🟢 指标靠现算（Langfuse 的选择）</h4><p>会话的<strong>各项指标不预先存</strong>，靠 GROUP BY 从 traces 现算。新来一条带 <code>session_id=S1</code> 的 trace，它<strong>自动</strong>就被算进会话 S1 的统计——指标永远和底层 traces 一致，无需同步聚合值。</p></div>
  <div class="col"><h4>🔴 预存聚合（没这么做）</h4><p>若把每个会话的计数、成本、时长<strong>预先算好存进一张表</strong>，每条 trace 进来都得去<strong>更新对应会话</strong>的这些聚合值——多一套写入、多一处可能与底层 traces 不一致的状态。能现算就别预存。</p></div>
</div>

<p>需要厘清一个细节：会话<strong>并非完全不落库</strong>。摄取时，如果一条 trace 带了 <code>session_id</code>，worker 会往 Postgres 的 <code>trace_sessions</code> 表
<strong>upsert 一个极轻的「存根」行</strong>（只有 id、project_id、environment、时间戳，且 <code>ON CONFLICT DO NOTHING</code>——同一会话只登记一次）。这行的作用是「<strong>登记这个会话存在</strong>」、
以及挂一些<strong>会话级元数据</strong>（如收藏、公开标记）。但请注意：真正昂贵的那些——<strong>user_ids、轮数、时长、总成本、trace 列表——全都不在这张表里</strong>，它们一律由 ClickHouse 对 traces 现场 GROUP BY 算出。
所以准确的说法是：<strong>会话有一个轻量元数据实体被持久化，但它的全部指标与列表是派生的</strong>。这正是关键取舍——<strong>该存的（身份、元数据）才存，能算的（聚合指标）就别存</strong>。</p>

<h2>会话详情：把对话按时序铺开</h2>
<p>点开一个会话，看到的是它含的那些 trace<strong>按时间排成一条对话时间线</strong>——第一轮、第二轮……每一轮点进去又是第 25 课那棵观测树。从列表到详情，会话只是在 trace 之上加了一层「对话」的视角，
让你不再孤立地看单条调用，而是看清「一整段交互」的来龙去脉。这对调试多轮 agent 尤其重要：很多问题不在某一轮，而在<strong>轮与轮之间</strong>——上一轮的输出怎样影响了下一轮、对话从哪里开始跑偏。</p>

<svg viewBox="0 0 720 230" role="img" aria-label="会话详情把一个 session 含的多条 trace 按时间排成对话时间线：第1轮、第2轮、第3轮依次排开，点进任一轮就是第25课的观测树（trace 根挂 span 与 generation，IO 懒加载），让你看清一整段多轮交互怎么演进、在哪轮变贵或出错">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="24" y="30" width="672" height="38" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="54" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">会话 = 多条 trace 按 session_id 分组 · 按时间排成一条对话时间线</text>
  <line x1="40" y1="104" x2="680" y2="104" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="668" y="96" font-size="10" text-anchor="end" fill="var(--muted)">时间 →</text>
  <rect x="64" y="84" width="120" height="40" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="124" y="108" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">第 1 轮 trace</text>
  <rect x="300" y="84" width="120" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="360" y="108" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">第 2 轮 trace</text>
  <rect x="536" y="84" width="120" height="40" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="596" y="108" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">第 3 轮 trace</text>
  <line x1="184" y1="104" x2="300" y2="104" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="420" y1="104" x2="536" y2="104" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="360" y1="124" x2="360" y2="150" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <rect x="300" y="150" width="120" height="26" rx="6" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="360" y="167" font-size="10.5" text-anchor="middle" fill="var(--accent-ink)">trace 根（第 25 课）</text>
  <rect x="270" y="186" width="96" height="24" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="318" y="202" font-size="10" text-anchor="middle" fill="var(--ink)">span</text>
  <rect x="378" y="186" width="96" height="24" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="426" y="202" font-size="10" text-anchor="middle" fill="var(--ink)">generation</text>
  <line x1="330" y1="176" x2="318" y2="186" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="390" y1="176" x2="426" y2="186" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="540" y="200" font-size="10.5" fill="var(--muted)">点进任一轮 → 观测树（IO 懒加载）</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>会话列表</h4><p>每行一个会话：谁参与、几轮、多久、花了多少（聚合指标后补，同第 24 课）。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>点开某会话</h4><p>用该会话的 <code>trace_ids</code> 把它含的 traces 取回，<strong>按时间排序</strong>成一条时间线。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>逐轮浏览</h4><p>时间线上每一项是一轮 trace（一问一答）；想细看哪轮，点进去就是第 25 课的观测树（IO 懒加载）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>看整段的全貌</h4><p>会话视角让你一眼看出「这段对话怎么演进、在哪轮变贵、哪轮出错」——这是单看一条 trace 给不了的。</p></div></div>
</div>
""")

# (spark + key below)

_ZH26.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么会话的指标都靠现算，而不是预先算好、单独存一份聚合？</strong> 因为<strong>能从已有数据现算的聚合，就别再冗余存一份</strong>。
  <code>session_id</code> 本就是第 8 课宽表上的一列，按它分组是<strong>免费</strong>的；而且这种「现算」天然<strong>永远和底层一致</strong>——新来一条 trace 带着某 session_id，它<strong>自动</strong>就被算进那个会话的统计，
  不需要任何「更新会话聚合」的同步步骤，也就不存在「trace 写进去了、会话计数却忘了加」这种不一致 bug。Langfuse 只在 Postgres 落一个<strong>极轻的会话存根</strong>（登记存在 + 挂元数据），
  把所有<strong>昂贵的聚合留给查询时现算</strong>——既避免了预存聚合的同步负担，又保留了一个挂收藏/公开等元数据的落点。更划算的是：因为会话表<strong>原样复用了第 24 课的表格机制</strong>，
  它<strong>白嫖</strong>了那套「紧凑行 vs 指标、按需聚合、URL 状态」的全部性能与体验。<strong>一个看起来很实在的新功能，列表与指标本质上只是一句 GROUP BY + 复用已有机制</strong>——这是「正交设计」最省力的红利。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>session = 多条 trace 按 <code>session_id</code> 分组</strong>（一段多轮对话 = 一个会话 = 多条 trace）；其<strong>指标与列表是派生的</strong>，仅一个轻量元数据存根（<code>trace_sessions</code>）在摄取时落 Postgres。</li>
    <li><code>session_id</code> 只是第 8 课宽表的一列，<code>GROUP BY session_id</code> 即得会话；各指标是对组内 traces 的聚合（不预存）。</li>
    <li><strong>聚合口径</strong>：<code>user_ids</code>（去重谁参与）、<code>trace_count</code>（计数）、<code>duration</code>（最晚−最早）、<code>session_total_cost</code>（求和）、<code>trace_ids</code>（收集）。</li>
    <li><strong>原样复用第 24 课</strong>：<code>getSessionsTableGeneric</code> 同样的紧凑行 vs 指标拆分（会话有 count/rows/metrics 三种形状，比 traces 少一个 identifiers）——性能技巧白白继承。</li>
    <li>取舍：派生指标<strong>永远和底层一致</strong>（新 trace 自动算入、无需同步聚合）、<strong>零额外聚合写入</strong>；该存的（身份/元数据存根）才存，能算的（聚合指标）就别预存——正交设计的省力红利。</li>
  </ul>
</div>
""")

_EN26.append(r"""
<p class="lead">
Lessons 24 and 25 covered the list and detail of a single trace. But a real conversation is often <strong>multi-turn</strong> — the user asks, the AI answers,
back and forth a dozen rounds, each round a trace. What threads them into <strong>one whole conversation</strong> is the <strong>session</strong>. This lesson's key
insight is strikingly lean: <strong>a session's metrics and listing aren't stored separately; they're computed on the fly by grouping traces on <code>session_id</code></strong> (only a tiny metadata stub is persisted, more below). Better still,
the sessions table <strong>reuses Lesson 24's table machinery nearly verbatim</strong> — bluntly, <strong>it's the trace table, grouped</strong>.
</p>

<div class="card analogy">
  <div class="tag">💬 Analogy</div>
  Think of a session as a <strong>chat thread</strong> and a trace as a <strong>message</strong> in it. Each message is <strong>stored individually</strong>, but you
  read them as <strong>one whole conversation</strong>. That "thread" <strong>isn't a separate thing stored somewhere</strong> — it's just "<strong>all messages with the
  same thread-id, shown together, with a summary line</strong>": who took part, how many rounds, how long, total cost. You needn't build a separate table or maintain
  a "thread" — it <strong>grows naturally out of the messages</strong>. That's exactly where Langfuse's sessions come from.
</div>
""")

_EN26.append(r"""
<h2>session = traces grouped by session_id</h2>
<p>Recall Lesson 8: <code>session_id</code> is just <strong>an ordinary column</strong> on the traces wide table. So a session's metrics and listing <strong>needn't be stored separately</strong> — just
<strong>GROUP BY session_id</strong> over traces sharing the same id and you get one "session" row, whose metrics are all <strong>aggregates over the grouped
traces</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="multiple traces with the same session_id grouped by session_id into one session row, aggregating user_ids, trace_count, duration (earliest to latest), session_total_cost">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">GROUP BY session_id: many traces → one session row</text>
  <rect x="20" y="44" width="250" height="150" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="145" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">traces table (Lesson 8 wide table)</text>
  <rect x="36" y="74" width="218" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="46" y="91" font-size="7.5" fill="var(--ink)">trace#1 · session_id=<tspan font-weight="700" fill="var(--accent-ink)">S1</tspan> · user=A · $0.01</text>
  <rect x="36" y="104" width="218" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="46" y="121" font-size="7.5" fill="var(--ink)">trace#2 · session_id=<tspan font-weight="700" fill="var(--accent-ink)">S1</tspan> · user=A · $0.02</text>
  <rect x="36" y="134" width="218" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="46" y="151" font-size="7.5" fill="var(--ink)">trace#3 · session_id=<tspan font-weight="700" fill="var(--accent-ink)">S1</tspan> · user=B · $0.03</text>
  <rect x="36" y="164" width="218" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="3 2"/><text x="46" y="179" font-size="7" fill="var(--faint)">trace#4 · session_id=S2 · …(another session)</text>
  <rect x="306" y="84" width="120" height="60" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="366" y="108" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">GROUP BY</text><text x="366" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">session_id</text>
  <rect x="462" y="58" width="240" height="120" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="582" y="78" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">one session row S1</text>
  <text x="478" y="98" font-size="8" fill="var(--ink)">user_ids = [A, B] (who took part)</text>
  <text x="478" y="116" font-size="8" fill="var(--ink)">trace_count = 3 (how many rounds)</text>
  <text x="478" y="134" font-size="8" fill="var(--ink)">duration = latest − earliest (how long)</text>
  <text x="478" y="152" font-size="8" fill="var(--ink)">session_total_cost = $0.06 (sum)</text>
  <text x="478" y="170" font-size="7.5" fill="var(--muted)">trace_ids = [#1, #2, #3]</text>
  <line x1="270" y1="114" x2="304" y2="114" stroke="var(--accent)" stroke-width="1.6"/><polygon points="304,114 295,110 295,118" fill="var(--accent)"/>
  <line x1="426" y1="114" x2="460" y2="114" stroke="var(--accent)" stroke-width="1.6"/><polygon points="460,114 451,110 451,118" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>A session is grouped out</b>: traces with the same <code>session_id</code> grouped by <code>GROUP BY session_id</code> into one session row; each metric is an aggregate over the grouped traces — <code>user_ids</code> (distinct who), <code>trace_count</code> (count), <code>duration</code> (latest − earliest), <code>session_total_cost</code> (sum). Source: <code>packages/shared/src/server/services/sessions-ui-table-service.ts:86,123</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/sessions-ui-table-service.ts</span><span class="ln">getSessionsTableGeneric :123</span></div>
  <pre class="code"><span class="cm">// the same pattern as Lesson 24's getTracesTableGeneric: one function, several "shapes" (sessions: count/rows/metrics)</span>
<span class="kw">const</span> getSessionsTableGeneric = <span class="kw">async</span> &lt;T&gt;(props: { select: <span class="st">"count"</span> | <span class="st">"rows"</span> | <span class="st">"metrics"</span> }) =&gt; {
  <span class="kw">switch</span> (select) {
    <span class="kw">case</span> <span class="st">"rows"</span>:    sqlSelect = <span class="st">"session_id, min/max_timestamp, trace_ids, user_ids, trace_count …"</span>; <span class="cm">// cheap</span>
    <span class="kw">case</span> <span class="st">"metrics"</span>: sqlSelect = <span class="st">"… + duration, total_observations, session_total_cost …"</span>;      <span class="cm">// computed</span>
  }
  <span class="cm">// under the hood: GROUP BY session_id over traces (and their observations for cost)</span>
}</pre>
</div>

<p>A detail worth noting: a session's "total cost" doesn't sit directly on the trace; it must <strong>drill into each trace's observations</strong> to sum (cost is
computed on the observation in Lesson 16). So a session's total cost is essentially "the sum of all observations' costs across all traces in the session" — a
<strong>two-level aggregation</strong>. That's why <code>session_total_cost</code> belongs to the "expensive" metrics shape, filled in later: like the cost metric in
Lesson 24's list, it must be computed across tables. The cheap rows shape takes only the session identity (who, how many rounds, which trace_ids), <strong>never
touching cost</strong>, so the session list can <strong>open instantly, then fill metrics</strong>.</p>
""")

_EN26.append(r"""
<h2>Reuse verbatim: the sessions table is "the trace table, grouped"</h2>
<p>See it? <code>getSessionsTableGeneric</code> and Lesson 24's <code>getTracesTableGeneric</code> are <strong>cut from the same mold</strong>: the same <strong>four
shapes</strong> (count / rows / metrics), the same <strong>"compact rows vs metrics" split</strong>. The session list too: paint the cheap session-identity rows first,
the expensive aggregates (duration, total cost) <strong>filled in later</strong>. All of Lesson 24's performance tricks the session <strong>inherits free</strong>:
pagination, look-back windows, on-demand aggregation, URL state, column presets, row selection — all the capabilities polished in Lesson 24, the sessions table gets
<strong>without writing a line</strong>, because it rides the same generic machinery. This is the payoff of making the table system <strong>"an entity-agnostic generic
part"</strong>: any new "list aggregated by some dimension" (sessions, users, models…) fits the same mold.</p>

<div class="fig">
<svg viewBox="0 0 720 180" role="img" aria-label="the sessions table reuses Lesson 24's compact-rows-vs-metrics split: rows takes session identity and trace list (cheap, first), metrics takes duration/total-cost aggregates (expensive, later)">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Reusing Lesson 24: compact rows paint first, aggregate metrics fill later</text>
  <rect x="30" y="42" width="300" height="118" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="180" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">rows (compact session rows · cheap · first)</text>
  <text x="50" y="84" font-size="8" fill="var(--accent-ink)">session_id · min/max timestamp</text>
  <text x="50" y="102" font-size="8" fill="var(--accent-ink)">trace_ids · user_ids · trace_count</text>
  <text x="50" y="120" font-size="8" fill="var(--accent-ink)">trace_tags · environment</text>
  <text x="50" y="142" font-size="7.5" fill="var(--muted)">→ session list visible immediately</text>
  <rect x="390" y="42" width="300" height="118" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="540" y="62" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">metrics (aggregates · expensive · later)</text>
  <text x="410" y="84" font-size="8" fill="var(--ink)">duration (how long)</text>
  <text x="410" y="102" font-size="8" fill="var(--ink)">total_observations (total observations)</text>
  <text x="410" y="120" font-size="8" fill="var(--ink)">session_total_cost / usage (total cost/usage)</text>
  <text x="410" y="142" font-size="7.5" fill="var(--muted)">→ computed, filled by session_id into rows</text>
</svg>
<div class="figcap"><b>The same table machinery</b>: the sessions table reuses Lesson 24's "select-driven shapes + compact-rows/metrics split" (sessions has count/rows/metrics). <code>rows</code> takes session identity and its <code>trace_ids</code> (cheap, rendered first), <code>metrics</code> takes <code>duration</code>, <code>session_total_cost</code> etc. (expensive, later). Source: <code>sessions-ui-table-service.ts:132-160</code>.</div>
</div>

<table class="t">
  <tr><th>session metric</th><th>how it's computed from grouped traces</th></tr>
  <tr><td><code>user_ids</code></td><td>distinctly collect every grouped trace's user_id (who took part in the conversation)</td></tr>
  <tr><td><code>trace_count</code></td><td>count: how many traces in this session (how many rounds)</td></tr>
  <tr><td><code>duration</code></td><td>latest timestamp − earliest timestamp (how long the whole conversation lasted)</td></tr>
  <tr><td><code>session_total_cost</code></td><td><strong>sum</strong> of all grouped traces' costs (total spent in this conversation)</td></tr>
  <tr><td><code>trace_ids</code></td><td>collect every grouped trace's id (open the session to expand them in order)</td></tr>
</table>

<div class="cols">
  <div class="col"><h4>🟢 metrics computed on the fly (Langfuse's choice)</h4><p>A session's metrics <strong>aren't pre-stored</strong>; they're computed from traces by GROUP BY. A new trace with <code>session_id=S1</code> is <strong>automatically</strong> counted into session S1's stats — metrics always consistent with the underlying traces, no aggregate to sync.</p></div>
  <div class="col"><h4>🔴 pre-stored aggregates (not done)</h4><p>Pre-compute each session's count, cost, duration into a table and every incoming trace must <strong>update its session's</strong> aggregates — an extra write path, an extra piece of state that could drift from the underlying traces. Compute rather than pre-store.</p></div>
</div>

<p>One detail to set straight: a session <strong>isn't entirely absent from storage</strong>. On ingestion, if a trace carries a <code>session_id</code>, the worker
<strong>upserts a tiny "stub" row</strong> into Postgres's <code>trace_sessions</code> table (just id, project_id, environment, timestamps, with <code>ON CONFLICT DO
NOTHING</code> — registered once per session). Its job is to "<strong>register that this session exists</strong>" and to hang some <strong>session-level metadata</strong>
(like bookmarked, public). But note: the truly expensive parts — <strong>user_ids, round count, duration, total cost, the trace list — are none of them in this
table</strong>; they're all computed by ClickHouse grouping traces on the fly. So the precise statement is: <strong>a lightweight session metadata entity is persisted,
but all of its metrics and listing are derived</strong>. That's exactly the trade-off — <strong>store what should be stored (identity, metadata), don't store what can be
computed (aggregate metrics)</strong>.</p>

<h2>Session detail: the conversation laid out over time</h2>
<p>Open a session and you see its traces <strong>laid out as a conversation timeline by time</strong> — round one, round two… click into a round and it's Lesson 25's
observation tree. From list to detail, a session just adds a "conversation" lens on top of traces, so you no longer see a call in isolation but the whole arc of an
interaction. This matters especially for debugging multi-turn agents: many problems aren't in one round but <strong>between rounds</strong> — how the previous output
shaped the next, where the conversation started to go off the rails.</p>

<svg viewBox="0 0 720 230" role="img" aria-label="session detail lays a session's traces into a conversation timeline: round 1, round 2, round 3 in time order, and clicking any round opens Lesson 25's observation tree (a trace root with span and generation children, IO lazy-loaded), so you can see how a multi-round interaction evolves and where it gets expensive or fails">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="24" y="30" width="672" height="38" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="54" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">session = traces grouped by session_id · laid out as one conversation timeline</text>
  <line x1="40" y1="104" x2="680" y2="104" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="668" y="96" font-size="10" text-anchor="end" fill="var(--muted)">time →</text>
  <rect x="64" y="84" width="120" height="40" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="124" y="108" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">round 1 trace</text>
  <rect x="300" y="84" width="120" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="360" y="108" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">round 2 trace</text>
  <rect x="536" y="84" width="120" height="40" rx="8" fill="var(--bg)" stroke="var(--blue)"></rect>
  <text x="596" y="108" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">round 3 trace</text>
  <line x1="184" y1="104" x2="300" y2="104" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="420" y1="104" x2="536" y2="104" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="360" y1="124" x2="360" y2="150" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="4 3"></line>
  <rect x="300" y="150" width="120" height="26" rx="6" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="360" y="167" font-size="10" text-anchor="middle" fill="var(--accent-ink)">trace root (L25)</text>
  <rect x="270" y="186" width="96" height="24" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="318" y="202" font-size="10" text-anchor="middle" fill="var(--ink)">span</text>
  <rect x="378" y="186" width="96" height="24" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="426" y="202" font-size="10" text-anchor="middle" fill="var(--ink)">generation</text>
  <line x1="330" y1="176" x2="318" y2="186" stroke="var(--faint)" stroke-width="1.5"></line>
  <line x1="390" y1="176" x2="426" y2="186" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="700" y="200" font-size="10.5" text-anchor="end" fill="var(--muted)">click any round → observation tree (lazy IO)</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>session list</h4><p>One session per row: who took part, how many rounds, how long, how much spent (aggregates filled later, same as Lesson 24).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>open a session</h4><p>Use the session's <code>trace_ids</code> to fetch its traces, <strong>ordered by time</strong> into a timeline.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>browse round by round</h4><p>Each timeline item is a trace (one Q&amp;A); to inspect a round, click in to Lesson 25's observation tree (IO lazy-loaded).</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>see the whole arc</h4><p>The session lens shows at a glance "how this conversation evolved, which round got costly, which round errored" — something one trace alone can't give.</p></div></div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why compute a session's metrics on the fly rather than pre-compute and store the aggregates?</strong> Because <strong>aggregates you can compute from existing data,
  don't store again</strong>. <code>session_id</code> is already a column on Lesson 8's wide table, so grouping by it is <strong>free</strong>; and this on-the-fly form is
  naturally <strong>always consistent with the underlying traces</strong> — a new trace bearing some session_id is <strong>automatically</strong> counted into that
  session's stats, no "update the session aggregates" sync step, hence no "the trace got written but the session count was forgotten" inconsistency bug. Langfuse
  persists only a <strong>tiny session stub</strong> in Postgres (registering existence + holding metadata), leaving all the <strong>expensive aggregates to query-time
  computation</strong> — avoiding the sync burden of pre-stored aggregates while keeping a place to hang metadata like bookmarked/public. Better still: because the
  sessions table <strong>reuses Lesson 24's machinery verbatim</strong>, it <strong>freeloads</strong> all of that "compact rows vs metrics, on-demand aggregation, URL
  state". <strong>A seemingly substantial new feature's listing and metrics are essentially one GROUP BY plus reusing existing machinery</strong> — the most effortless
  dividend of orthogonal design.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A session = many traces grouped by <code>session_id</code></strong> (one multi-turn conversation = one session = many traces); its <strong>metrics and listing are derived</strong>, with only a lightweight metadata stub (<code>trace_sessions</code>) persisted to Postgres on ingestion.</li>
    <li><code>session_id</code> is just a column on Lesson 8's wide table; <code>GROUP BY session_id</code> yields the session; each metric is an aggregate over the grouped traces (not pre-stored).</li>
    <li><strong>Aggregation rules</strong>: <code>user_ids</code> (distinct who), <code>trace_count</code> (count), <code>duration</code> (latest − earliest), <code>session_total_cost</code> (sum, a two-level aggregation into observations), <code>trace_ids</code> (collect).</li>
    <li><strong>Reuses Lesson 24 verbatim</strong>: <code>getSessionsTableGeneric</code> has the same select-driven shapes (count/rows/metrics — one fewer than traces, no identifiers) and the same compact-rows-vs-metrics split — all the performance tricks inherited free.</li>
    <li>Tradeoff: derived metrics are <strong>always consistent with the underlying traces</strong> (new traces auto-counted, no aggregate to sync) with <strong>zero extra aggregate writes</strong>; persist what's identity/metadata, compute the aggregates rather than pre-store — the effortless dividend of orthogonal design.</li>
  </ul>
</div>
""")
LESSON_26 = {"zh": "\n".join(_ZH26), "en": "\n".join(_EN26)}


# ══════════════════════════════════════════════════════════════════════
# L27 · 公共 REST API / The public REST API
# ══════════════════════════════════════════════════════════════════════
_ZH27 = []
_EN27 = []

_ZH27.append(r"""
<p class="lead">
第 21 课开的是给自家 UI 的「员工通道」（tRPC）。这一课开<strong>第三道门也是最后一道</strong>——给外部 SDK 的<strong>公共 REST API</strong>。它的优先级和 tRPC 截然不同：对内求<strong>类型安全、改得快</strong>，
对外求<strong>契约稳定、扛得住量</strong>。这一课看四件事：一个<strong>路由工厂</strong>怎么统一所有端点的鉴权/限流/校验，鉴权怎么<strong>用 Redis 缓存</strong>扛住海量请求，
版本怎么<strong>靠文件夹</strong>管理，以及一份 <strong>Fern 契约</strong>怎么生成多语言 SDK。看完这一课，第 20 课「三道门」就全开齐了。
</p>

<div class="card analogy">
  <div class="tag">🏛️ 生活类比</div>
  把公共 REST API 想成一座政府大楼的<strong>对外服务大厅</strong>。不管你来办哪种业务（查 trace、提交 score、拉 dataset），都先走<strong>同一道安检与叫号流程</strong>（路由工厂：验证件、限流、查表格填得对不对）——
  没人能绕开。常来的人，证件信息被<strong>前台缓存</strong>下来，下次不必每回都回档案室核查（Redis 缓存鉴权）。大厅的<strong>办事规程印成了手册</strong>，还翻译成各种语言发给你（Fern 生成多语言 SDK）；
  规程更新时，<strong>旧版手册仍然有效</strong>，新规程发布成「v2」，老用户不受影响（按文件夹版本化）。<strong>统一、稳定、可缓存、带版本</strong>——这就是一个对外 API 该有的样子。
</div>
""")

# (L27 sections appended below)

_ZH27.append(r"""
<h2>一个路由工厂，统一所有端点</h2>
<p>就像 tRPC 用 procedure 构建器把鉴权收敛到一处（第 21 课），公共 REST 用一个<strong>路由工厂</strong> <code>createAuthedProjectAPIRoute</code> 把所有端点的「规定动作」收敛到一处。
每个端点只需声明自己的 query/body/response schema 和限流资源，工厂就<strong>统一</strong>把这几关跑完：</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="createAuthedProjectAPIRoute 路由工厂依次跑鉴权、访问级别检查、限流、Zod 校验 query/body、在 OTel 上下文里跑 handler、校验响应、超大请求体拒绝">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">createAuthedProjectAPIRoute：每个端点的统一流水线</text>
  <rect x="16" y="44" width="100" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="66" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">SDK 请求</text><text x="66" y="76" text-anchor="middle" font-size="7" fill="var(--muted)">Basic/Bearer</text>
  <rect x="130" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="182" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">① 鉴权</text><text x="182" y="74" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">key→project (缓存)</text>
  <rect x="248" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="300" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">② 访问级别</text><text x="300" y="74" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">project / scores</text>
  <rect x="366" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="418" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">③ 限流</text><text x="418" y="74" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">按资源/计划</text>
  <rect x="484" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="536" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">④ Zod 校验</text><text x="536" y="74" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">query/body</text>
  <rect x="602" y="44" width="104" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="654" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">⑤ 你的 handler</text><text x="654" y="74" text-anchor="middle" font-size="6.6" fill="var(--muted)">OTel surface=publicapi</text>
  <line x1="116" y1="64" x2="128" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="128,64 121,61 121,67" fill="var(--faint)"/>
  <line x1="234" y1="64" x2="246" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="246,64 239,61 239,67" fill="var(--faint)"/>
  <line x1="352" y1="64" x2="364" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="364,64 357,61 357,67" fill="var(--faint)"/>
  <line x1="470" y1="64" x2="482" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="482,64 475,61 475,67" fill="var(--faint)"/>
  <line x1="588" y1="64" x2="600" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="600,64 593,61 593,67" fill="var(--faint)"/>
  <rect x="120" y="104" width="468" height="34" rx="8" fill="none" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="354" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">这五关由工厂统一跑——端点只声明 schema，不重复写鉴权/限流/校验</text>
  <rect x="160" y="156" width="180" height="50" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="250" y="176" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">超大请求体</text><text x="250" y="192" text-anchor="middle" font-size="7" fill="var(--muted)">→ PayloadTooLargeError</text>
  <rect x="380" y="156" width="180" height="50" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="470" y="176" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">响应也校验（开发期）</text><text x="470" y="192" text-anchor="middle" font-size="7" fill="var(--muted)">防契约漂移</text>
</svg>
<div class="figcap"><b>对外端点的统一流水线</b>：<code>createAuthedProjectAPIRoute</code> 依次跑鉴权（key→project，含访问级别）→ 限流 → Zod 校验 query/body → 在 OTel 上下文（<code>surface=publicapi</code>）里跑你的 handler → 校验响应（开发期防契约漂移）；请求体过大 → <code>PayloadTooLargeError</code>。源码：<code>web/src/features/public-api/server/createAuthedProjectAPIRoute.ts</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/public-api/server/createAuthedProjectAPIRoute.ts</span><span class="ln">路由工厂</span></div>
  <pre class="code"><span class="cm">// 每个端点只声明 schema 与限流资源，工厂统一跑鉴权/限流/校验/OTel</span>
<span class="kw">export const</span> handler = <span class="fn">createAuthedProjectAPIRoute</span>({
  name: <span class="st">"Get Traces"</span>,
  querySchema: GetTracesV1Query,   bodySchema: z.<span class="fn">never</span>(),
  responseSchema: GetTracesV1Response,
  rateLimitResource: <span class="st">"public-api"</span>,
  allowedAccessLevels: [<span class="st">"project"</span>],  <span class="cm">// 这个端点要 project 级 key</span>
  fn: <span class="kw">async</span> ({ query, auth }) =&gt; { <span class="cm">/* 只写业务：此时已鉴权+校验完毕 */</span> },
});</pre>
</div>

<p>这正是第 21 课「安全靠结构」在 REST 侧的翻版：鉴权、限流、Zod 校验<strong>不靠每个端点作者自觉</strong>，而是工厂强制跑完。
区别在优先级——tRPC 那套是给内部的，REST 这套多了<strong>限流</strong>（防外部滥用）、<strong>响应校验</strong>（防对外契约漂移）、<strong>访问级别</strong>（如 Bearer 只读 score）这些<strong>面向公众</strong>才需要的关卡。</p>

<table class="t">
  <tr><th></th><th>tRPC（第 21 课 · 对内）</th><th>公共 REST（本课 · 对外）</th></tr>
  <tr><td><b>给谁</b></td><td>自家 UI（同仓库、同团队）</td><td>外部 SDK / 用户脚本（海量、长期）</td></tr>
  <tr><td><b>首要价值</b></td><td>类型安全、<strong>改得快</strong></td><td>契约稳定、<strong>扛得住量</strong></td></tr>
  <tr><td><b>收敛方式</b></td><td>procedure 构建器（叠中间件）</td><td>路由工厂 <code>createAuthedProjectAPIRoute</code></td></tr>
  <tr><td><b>额外关卡</b></td><td>—</td><td>限流、响应校验、访问级别</td></tr>
  <tr><td><b>稳定手段</b></td><td>编译期类型检查（改了即报错）</td><td>文件夹版本 + Fern 契约 + 多语言 SDK</td></tr>
</table>
""")

# (auth cache + versioning + fern section below)

_ZH27.append(r"""
<h2>鉴权要扛量：Redis 缓存 + 负缓存</h2>
<p>对外 API 每一个请求都要先验 key——而 SDK 可能每秒打来成千上万条。要是每条都回 Postgres 查 key，数据库会被<strong>鉴权本身</strong>压垮。
于是 <code>ApiAuthService</code> 给 key 验证套了一层 <strong>Redis 缓存</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="鉴权先查 Redis 缓存命中即返回，未命中回 Postgres 按 fastHashedSecretKey 查再回填；不存在的 key 用负缓存 API_KEY_NON_EXISTENT 记下防暴力打库">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">缓存鉴权：让数据库别为「验 key」累垮</text>
  <rect x="20" y="44" width="120" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">收到 API key</text><text x="80" y="79" text-anchor="middle" font-size="7" fill="var(--muted)">先查 Redis</text>
  <rect x="180" y="34" width="180" height="30" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="270" y="53" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">✅ 命中 → 直接返回 scope</text>
  <rect x="180" y="72" width="180" height="30" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="270" y="91" text-anchor="middle" font-size="8" fill="var(--ink)">❌ 未命中 → 回 Postgres 查</text>
  <rect x="400" y="72" width="170" height="30" rx="7" fill="var(--bg)" stroke="var(--blue)"/><text x="485" y="91" text-anchor="middle" font-size="7.5" fill="var(--ink)">按 fastHashedSecretKey 查 + 回填 Redis</text>
  <rect x="180" y="112" width="390" height="34" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="375" y="126" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">负缓存：key 不存在也记一笔（API_KEY_NON_EXISTENT）</text><text x="375" y="139" text-anchor="middle" font-size="7" fill="var(--accent-ink)">→ 用假 key 暴力打库时，第二次起直接被 Redis 挡回，不碰 Postgres</text>
  <line x1="140" y1="58" x2="178" y2="49" stroke="var(--accent)" stroke-width="1.3"/><line x1="140" y1="70" x2="178" y2="86" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="360" y1="87" x2="398" y2="87" stroke="var(--faint)" stroke-width="1.3"/><polygon points="398,87 390,83 390,91" fill="var(--faint)"/>
  <text x="360" y="170" text-anchor="middle" font-size="8.5" fill="var(--faint)">缓存命中 → 验 key 几乎零成本；负缓存 → 攻击者用不存在的 key 刷不动数据库</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--muted)">删除 key 时主动失效缓存——没有「更新」路径，只有「失效」</text>
</svg>
<div class="figcap"><b>缓存正例、也缓存反例</b>：鉴权先查 Redis，命中即返回；未命中回 Postgres 按 <code>fastHashedSecretKey</code> 查再回填。关键是<strong>负缓存</strong>：连「这个 key 不存在」也记下（<code>API_KEY_NON_EXISTENT</code>），让攻击者拿假 key 暴力打库时打不动数据库。源码：<code>web/src/features/public-api/server/apiAuth.ts:75</code>。</div>
</div>

<div class="cols">
  <div class="col"><h4>😖 不缓存：每请求都查库</h4><p>SDK 每秒上万条请求，每条都回 Postgres 验一次 key——数据库的负载里很大一块是<strong>鉴权本身</strong>，业务还没开始就先被拖慢；攻击者拿一堆假 key 来刷，更是直接打在库上。</p></div>
  <div class="col"><h4>😀 缓存 + 负缓存：库几乎不碰</h4><p>常用 key 命中 Redis，验 key 几乎零成本；连「不存在的 key」也被负缓存挡在 Redis 这一层。<strong>无论正常流量还是恶意刷量，Postgres 都被保护在后面</strong>，只在缓存未命中时才被惊动。</p></div>
</div>

<h2>版本靠文件夹，契约靠 Fern</h2>
<p>对外 API 一旦发布就不能随意改——可需求总在变，怎么办？Langfuse 的两招：<strong>用文件夹做版本</strong>、<strong>用 Fern 生成 SDK</strong>。</p>

<svg viewBox="0 0 720 240" role="img" aria-label="两招：① 版本是文件夹，v1 在 public 根、新版进 v2/ v3/ 子文件夹，老路径永不改，v3 还能做减法改用游标分页；② 契约是 Fern，一份手写 YAML 生成 Python SDK、TypeScript SDK 并导出 OpenAPI，一处定义处处一致">
  <rect x="0" y="0" width="720" height="240" fill="var(--bg)"></rect>
  <text x="24" y="26" font-size="12" font-weight="700" fill="var(--accent-ink)">① 版本 = 文件夹（老路径永不改）</text>
  <rect x="24" y="38" width="232" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="140" y="62" font-size="11" text-anchor="middle" fill="var(--ink)">public/ (v1) · 默认在根</text>
  <rect x="48" y="90" width="232" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="164" y="114" font-size="11" text-anchor="middle" fill="var(--ink)">public/v2/</text>
  <rect x="72" y="142" width="244" height="44" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="194" y="162" font-size="11" text-anchor="middle" fill="var(--ink)">public/v3/ · 可做减法</text>
  <text x="194" y="178" font-size="9.5" text-anchor="middle" fill="var(--muted)">如 v3/scores 改用游标分页</text>
  <line x1="350" y1="34" x2="350" y2="192" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 4"></line>
  <text x="392" y="26" font-size="12" font-weight="700" fill="var(--accent-ink)">② 契约 = Fern（一处定义）</text>
  <rect x="392" y="68" width="150" height="72" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="467" y="98" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Fern YAML</text>
  <text x="467" y="118" font-size="9" text-anchor="middle" fill="var(--muted)">fern/apis/{server,client}</text>
  <rect x="576" y="44" width="128" height="36" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="640" y="66" font-size="10.5" text-anchor="middle" fill="var(--ink)">Python SDK</text>
  <rect x="576" y="92" width="128" height="36" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="640" y="114" font-size="10.5" text-anchor="middle" fill="var(--ink)">TypeScript SDK</text>
  <rect x="576" y="140" width="128" height="36" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="640" y="162" font-size="10.5" text-anchor="middle" fill="var(--ink)">OpenAPI 导出</text>
  <line x1="542" y1="96" x2="576" y2="62" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="542" y1="104" x2="576" y2="110" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="542" y1="112" x2="576" y2="158" stroke="var(--accent)" stroke-width="2"></line>
  <text x="360" y="220" font-size="11" text-anchor="middle" fill="var(--muted)">版本化保证「旧的不破」，Fern 生成保证「多语言一致、契约即文档」</text>
</svg>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">版本=文件夹</span><span class="name">v1 在根，v2/、v3/…</span></div><div class="ld">默认 v1 在 <code>public/</code> 根，新版放进 <code>v2/</code>、<code>v3/</code> 子文件夹。<strong>老路径永不改</strong>，你两年前的集成今天照跑；想要新能力就显式切到新版本。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">新版可做减法</span><span class="name">去掉昂贵特性</span></div><div class="ld">新版本不只是加功能，也能<strong>砍掉代价大的旧设计</strong>：比如 <code>v3/scores</code> 去掉了需要 JOIN trace 的 userId/traceTags 过滤、改用<strong>游标分页</strong>——把「该用 v2」的话直接写进文档。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">Fern 契约</span><span class="name">一份 YAML → 多语言 SDK</span></div><div class="ld">API 契约是手写的 Fern YAML（<code>fern/apis/{server,client}/…</code>），由它<strong>生成 Python 与 TypeScript SDK</strong>（<code>generated/</code>），还导出 OpenAPI。一处定义、处处一致。</div></div>
</div>

<p>这两招合起来，正是第 20 课说的「对外求契约稳定」的落地：<strong>版本化</strong>保证「旧的不破」，<strong>Fern 生成</strong>保证「多语言一致、契约即文档」。
配合开发期的响应 schema 校验（防手写实现和 Fern 契约悄悄漂移），整条对外通道既稳又不会偷偷变样。</p>
""")

# (spark + key below)

_ZH27.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>同样是「把数据查出来」，为什么 UI 走 tRPC、SDK 却要这一整套 REST 工厂 + 缓存 + 版本 + Fern？</strong> 因为<strong>受众不同，约束就不同</strong>（呼应第 20 课）。
  UI 是自家的、同仓库的，所以 tRPC 用<strong>类型贯穿</strong>换迭代速度，接口天天改也无妨。而 SDK 面向<strong>外部、海量、长期</strong>的用户：海量，所以鉴权必须<strong>能缓存</strong>（Redis + 负缓存），否则数据库被验 key 拖垮；
  长期，所以接口必须<strong>带版本</strong>（文件夹 + Fern），否则一改就破坏别人两年前写的集成。同一个「把横切关注收敛到一处」的工厂模式（第 21、22 课），
  在这里被赋予了<strong>面向公众</strong>的新内涵：限流防滥用、响应校验防契约漂移、缓存扛流量、版本保稳定。<strong>对内优化「改得快」，对外优化「不破坏」——这是同一套数据，两种工程价值观的分野。</strong>
  至此，第 20 课的「三道门」全部走完：tRPC 给 UI、REST 给 SDK、App-Router 给流式/webhook，各按受众分而治之。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>一个路由工厂</strong> <code>createAuthedProjectAPIRoute</code> 统一所有公共端点的鉴权 → 访问级别 → 限流 → Zod 校验 query/body → OTel(surface=publicapi) → 响应校验 → 超大体拒绝。</li>
    <li><strong>鉴权用 Redis 缓存</strong>扛海量请求：命中即返回、未命中回 Postgres 按 <code>fastHashedSecretKey</code> 查再回填；<strong>负缓存</strong>（<code>API_KEY_NON_EXISTENT</code>）挡住假 key 暴力打库。</li>
    <li><strong>版本靠文件夹</strong>：v1 在根、v2/v3 子文件夹；老路径永不改，新版可做减法（如 v3 scores 去掉需 JOIN 的过滤、改游标分页）。</li>
    <li><strong>契约靠 Fern</strong>：手写 Fern YAML → 生成 Python/TS SDK + OpenAPI；开发期响应校验防手写实现与契约漂移。</li>
    <li>取舍：对内（tRPC）优化类型安全与速度，对外（REST）优化稳定与扛量——同一份数据、两种价值观。至此第 20 课「三道门」全开齐。</li>
  </ul>
</div>
""")

_EN27.append(r"""
<p class="lead">
Lesson 21 opened the "staff entrance" for the in-house UI (tRPC). This lesson opens <strong>the third and last door</strong> — the <strong>public REST API</strong> for
external SDKs. Its priorities differ sharply from tRPC's: internally seek <strong>type-safety, fast to change</strong>; externally seek <strong>contract stability,
holding up at scale</strong>. Four things to see: how a <strong>route factory</strong> unifies auth/rate-limit/validation across all endpoints, how auth <strong>uses a
Redis cache</strong> to withstand massive traffic, how versions are managed <strong>by folder</strong>, and how a <strong>Fern contract</strong> generates multi-language
SDKs. Finish this and Lesson 20's "three doors" are all open.
</p>

<div class="card analogy">
  <div class="tag">🏛️ Analogy</div>
  Think of the public REST API as a government building's <strong>public service hall</strong>. Whatever business you come for (query a trace, submit a score, pull a
  dataset), you first go through <strong>the same security and queue process</strong> (the route factory: check ID, rate-limit, verify your form is filled right) — no
  one skips it. Frequent visitors get their ID info <strong>cached at the front desk</strong>, no trip to the archives each time (Redis-cached auth). The hall's
  <strong>procedures are printed into a manual</strong> and translated into your language (Fern generates multi-language SDKs); when procedures update, the <strong>old
  manual still works</strong>, the new procedure ships as "v2", existing users unaffected (versioning by folder). <strong>Unified, stable, cacheable, versioned</strong> —
  that's what an external API should look like.
</div>
""")

_EN27.append(r"""
<h2>One route factory, unifying every endpoint</h2>
<p>Just as tRPC converges auth into procedure builders (Lesson 21), the public REST converges every endpoint's "mandatory moves" into one <strong>route factory</strong>
<code>createAuthedProjectAPIRoute</code>. Each endpoint just declares its query/body/response schema and rate-limit resource, and the factory <strong>uniformly</strong>
runs these gates:</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="createAuthedProjectAPIRoute runs auth, access-level check, rate limit, Zod validation of query/body, the handler in an OTel context, response validation, and rejects oversized bodies">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">createAuthedProjectAPIRoute: every endpoint's unified pipeline</text>
  <rect x="16" y="44" width="100" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="66" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">SDK request</text><text x="66" y="76" text-anchor="middle" font-size="7" fill="var(--muted)">Basic/Bearer</text>
  <rect x="130" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="182" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">① auth</text><text x="182" y="74" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">key→project (cached)</text>
  <rect x="248" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="300" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">② access level</text><text x="300" y="74" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">project / scores</text>
  <rect x="366" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="418" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">③ rate limit</text><text x="418" y="74" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">by resource/plan</text>
  <rect x="484" y="44" width="104" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="536" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">④ Zod validate</text><text x="536" y="74" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">query/body</text>
  <rect x="602" y="44" width="104" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="654" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">⑤ your handler</text><text x="654" y="74" text-anchor="middle" font-size="6.4" fill="var(--muted)">OTel surface=publicapi</text>
  <line x1="116" y1="64" x2="128" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="128,64 121,61 121,67" fill="var(--faint)"/>
  <line x1="234" y1="64" x2="246" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="246,64 239,61 239,67" fill="var(--faint)"/>
  <line x1="352" y1="64" x2="364" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="364,64 357,61 357,67" fill="var(--faint)"/>
  <line x1="470" y1="64" x2="482" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="482,64 475,61 475,67" fill="var(--faint)"/>
  <line x1="588" y1="64" x2="600" y2="64" stroke="var(--faint)" stroke-width="1.4"/><polygon points="600,64 593,61 593,67" fill="var(--faint)"/>
  <rect x="120" y="104" width="468" height="34" rx="8" fill="none" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="354" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">the factory runs these five — endpoints just declare schema, never re-write auth/rate-limit/validation</text>
  <rect x="160" y="156" width="180" height="50" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="250" y="176" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">oversized body</text><text x="250" y="192" text-anchor="middle" font-size="7" fill="var(--muted)">→ PayloadTooLargeError</text>
  <rect x="380" y="156" width="180" height="50" rx="8" fill="var(--bg)" stroke="var(--teal)"/><text x="470" y="176" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">response validated (dev)</text><text x="470" y="192" text-anchor="middle" font-size="7" fill="var(--muted)">prevents contract drift</text>
</svg>
<div class="figcap"><b>The unified pipeline for external endpoints</b>: <code>createAuthedProjectAPIRoute</code> runs auth (key→project, incl. access level) → rate limit → Zod-validate query/body → the handler in an OTel context (<code>surface=publicapi</code>) → validate the response (dev, anti contract-drift); oversized body → <code>PayloadTooLargeError</code>. Source: <code>web/src/features/public-api/server/createAuthedProjectAPIRoute.ts</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/public-api/server/createAuthedProjectAPIRoute.ts</span><span class="ln">route factory</span></div>
  <pre class="code"><span class="cm">// each endpoint only declares schema &amp; rate-limit resource; the factory runs auth/limit/validate/OTel</span>
<span class="kw">export const</span> handler = <span class="fn">createAuthedProjectAPIRoute</span>({
  name: <span class="st">"Get Traces"</span>,
  querySchema: GetTracesV1Query,   bodySchema: z.<span class="fn">never</span>(),
  responseSchema: GetTracesV1Response,
  rateLimitResource: <span class="st">"public-api"</span>,
  allowedAccessLevels: [<span class="st">"project"</span>],  <span class="cm">// this endpoint needs a project-level key</span>
  fn: <span class="kw">async</span> ({ query, auth }) =&gt; { <span class="cm">/* business only: already authed + validated */</span> },
});</pre>
</div>

<p>This is Lesson 21's "security by structure" on the REST side: auth, rate-limit, Zod validation <strong>don't rely on each endpoint author's diligence</strong> — the
factory forces them all. The difference is priority — tRPC's set is internal; REST's adds <strong>rate limiting</strong> (against external abuse), <strong>response
validation</strong> (against external contract drift), <strong>access levels</strong> (e.g. Bearer read-only scores) — gates only the <strong>public-facing</strong> side
needs.</p>

<table class="t">
  <tr><th></th><th>tRPC (Lesson 21 · internal)</th><th>public REST (this lesson · external)</th></tr>
  <tr><td><b>for whom</b></td><td>own UI (same repo, same team)</td><td>external SDK / user scripts (massive, long-lived)</td></tr>
  <tr><td><b>top value</b></td><td>type-safety, <strong>fast to change</strong></td><td>contract stability, <strong>holds up at scale</strong></td></tr>
  <tr><td><b>convergence</b></td><td>procedure builders (stacked middleware)</td><td>route factory <code>createAuthedProjectAPIRoute</code></td></tr>
  <tr><td><b>extra gates</b></td><td>—</td><td>rate limit, response validation, access level</td></tr>
  <tr><td><b>stability means</b></td><td>compile-time type checks (change → error)</td><td>folder versions + Fern contract + multi-language SDKs</td></tr>
</table>
""")

_EN27.append(r"""
<h2>Auth must scale: Redis cache + negative caching</h2>
<p>An external API verifies a key on every request — and an SDK may send thousands per second. Hit Postgres for every key check and the database gets crushed by
<strong>auth itself</strong>. So <code>ApiAuthService</code> wraps key verification in a <strong>Redis cache</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="auth checks Redis cache first and returns on hit, falls back to Postgres by fastHashedSecretKey and re-caches on miss; nonexistent keys are negatively cached with API_KEY_NON_EXISTENT to stop brute-force DB hits">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Cached auth: keep the DB from being crushed by "verify key"</text>
  <rect x="20" y="44" width="120" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">API key arrives</text><text x="80" y="79" text-anchor="middle" font-size="7" fill="var(--muted)">check Redis first</text>
  <rect x="180" y="34" width="180" height="30" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="270" y="53" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">✅ hit → return scope directly</text>
  <rect x="180" y="72" width="180" height="30" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="270" y="91" text-anchor="middle" font-size="8" fill="var(--ink)">❌ miss → fall back to Postgres</text>
  <rect x="400" y="72" width="170" height="30" rx="7" fill="var(--bg)" stroke="var(--blue)"/><text x="485" y="91" text-anchor="middle" font-size="7" fill="var(--ink)">look up by fastHashedSecretKey + re-cache</text>
  <rect x="180" y="112" width="390" height="34" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="375" y="126" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">negative caching: even "key doesn't exist" is recorded (API_KEY_NON_EXISTENT)</text><text x="375" y="139" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">→ brute-forcing with fake keys is blocked by Redis from the 2nd hit, never touching Postgres</text>
  <line x1="140" y1="58" x2="178" y2="49" stroke="var(--accent)" stroke-width="1.3"/><line x1="140" y1="70" x2="178" y2="86" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="360" y1="87" x2="398" y2="87" stroke="var(--faint)" stroke-width="1.3"/><polygon points="398,87 390,83 390,91" fill="var(--faint)"/>
  <text x="360" y="170" text-anchor="middle" font-size="8.5" fill="var(--faint)">cache hit → near-zero-cost key check; negative cache → attackers with fake keys can't pound the DB</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--muted)">on key deletion the cache is actively invalidated — no "update" path, only "invalidate"</text>
</svg>
<div class="figcap"><b>Cache the positives, and the negatives too</b>: auth checks Redis first, returns on hit; on miss falls back to Postgres by <code>fastHashedSecretKey</code> and re-caches. The key is <strong>negative caching</strong>: even "this key doesn't exist" is recorded (<code>API_KEY_NON_EXISTENT</code>), so attackers brute-forcing with fake keys can't pound the database. Source: <code>web/src/features/public-api/server/apiAuth.ts:75</code>.</div>
</div>

<div class="cols">
  <div class="col"><h4>😖 no cache: every request hits the DB</h4><p>The SDK sends tens of thousands of requests a second, each verifying a key against Postgres — a big chunk of the DB's load is <strong>auth itself</strong>, slowing things before business even starts; attackers flooding with fake keys hit the DB directly.</p></div>
  <div class="col"><h4>😀 cache + negative cache: the DB is barely touched</h4><p>Common keys hit Redis, key checks near-zero-cost; even "nonexistent keys" are stopped at the Redis layer by negative caching. <strong>Whether normal traffic or malicious flooding, Postgres is shielded behind</strong>, disturbed only on a cache miss.</p></div>
</div>

<h2>Versions by folder, contracts by Fern</h2>
<p>An external API, once published, can't change freely — but needs keep evolving, so what? Langfuse's two moves: <strong>version by folder</strong>, <strong>generate SDKs
with Fern</strong>.</p>

<svg viewBox="0 0 720 240" role="img" aria-label="two moves: (1) version is a folder, v1 at the public root and new versions in v2/ v3/ subfolders, old paths never change and v3 can even drop features like switching to cursor pagination; (2) the contract is Fern, one hand-written YAML generates the Python SDK and TypeScript SDK and exports OpenAPI, defined once and consistent everywhere">
  <rect x="0" y="0" width="720" height="240" fill="var(--bg)"></rect>
  <text x="24" y="26" font-size="12" font-weight="700" fill="var(--accent-ink)">(1) version = folder (old paths never change)</text>
  <rect x="24" y="38" width="232" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="140" y="62" font-size="11" text-anchor="middle" fill="var(--ink)">public/ (v1) · default at root</text>
  <rect x="48" y="90" width="232" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="164" y="114" font-size="11" text-anchor="middle" fill="var(--ink)">public/v2/</text>
  <rect x="72" y="142" width="244" height="44" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="194" y="162" font-size="11" text-anchor="middle" fill="var(--ink)">public/v3/ · can subtract</text>
  <text x="194" y="178" font-size="9.5" text-anchor="middle" fill="var(--muted)">e.g. v3/scores uses cursor paging</text>
  <line x1="350" y1="34" x2="350" y2="192" stroke="var(--faint)" stroke-width="1.5" stroke-dasharray="4 4"></line>
  <text x="392" y="26" font-size="12" font-weight="700" fill="var(--accent-ink)">(2) contract = Fern (define once)</text>
  <rect x="392" y="68" width="150" height="72" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="467" y="98" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Fern YAML</text>
  <text x="467" y="118" font-size="9" text-anchor="middle" fill="var(--muted)">fern/apis/{server,client}</text>
  <rect x="576" y="44" width="128" height="36" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="640" y="66" font-size="10.5" text-anchor="middle" fill="var(--ink)">Python SDK</text>
  <rect x="576" y="92" width="128" height="36" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="640" y="114" font-size="10.5" text-anchor="middle" fill="var(--ink)">TypeScript SDK</text>
  <rect x="576" y="140" width="128" height="36" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="640" y="162" font-size="10.5" text-anchor="middle" fill="var(--ink)">OpenAPI export</text>
  <line x1="542" y1="96" x2="576" y2="62" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="542" y1="104" x2="576" y2="110" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="542" y1="112" x2="576" y2="158" stroke="var(--accent)" stroke-width="2"></line>
  <text x="360" y="220" font-size="11" text-anchor="middle" fill="var(--muted)">versioning keeps "the old unbroken"; Fern generation keeps "multi-language consistent, contract is the doc"</text>
</svg>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">version = folder</span><span class="name">v1 at root, v2/, v3/…</span></div><div class="ld">v1 sits at the <code>public/</code> root by default, new versions in <code>v2/</code>, <code>v3/</code> subfolders. <strong>Old paths never change</strong>, so your two-year-old integration still runs today; opt into new capability by explicitly switching version.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">new versions can subtract</span><span class="name">drop expensive features</span></div><div class="ld">A new version isn't only additive; it can <strong>cut costly old designs</strong>: e.g. <code>v3/scores</code> drops the userId/traceTags filters that need a trace JOIN and uses <strong>cursor pagination</strong> — writing "use v2 for that" straight into the docs.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">Fern contract</span><span class="name">one YAML → multi-language SDKs</span></div><div class="ld">The API contract is hand-written Fern YAML (<code>fern/apis/{server,client}/…</code>), which <strong>generates the Python and TypeScript SDKs</strong> (<code>generated/</code>) and exports OpenAPI. Define once, consistent everywhere.</div></div>
</div>

<p>Together these are Lesson 20's "externally seek contract stability" made real: <strong>versioning</strong> ensures "the old doesn't break", <strong>Fern
generation</strong> ensures "multi-language consistency, contract-as-docs". Paired with dev-time response-schema validation (against the hand-written implementation
silently drifting from the Fern contract), the whole external channel stays stable and never quietly changes shape.</p>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>It's all "query the data out", so why does the UI use tRPC while the SDK needs this whole REST factory + cache + versions + Fern?</strong> Because
  <strong>different audiences, different constraints</strong> (echoing Lesson 20). The UI is in-house, same repo, so tRPC trades <strong>type threading</strong> for iteration
  speed, where daily changes are fine. The SDK faces <strong>external, massive, long-lived</strong> users: massive, so auth must be <strong>cacheable</strong> (Redis +
  negative cache), or the DB gets crushed by key checks; long-lived, so the API must be <strong>versioned</strong> (folders + Fern), or one change breaks someone's
  two-year-old integration. The same "converge cross-cutting concerns into one factory" pattern (Lessons 21, 22) takes on a <strong>public-facing</strong> new meaning
  here: rate-limit against abuse, response-validate against drift, cache to take traffic, version to stay stable. <strong>Internally optimize "fast to change",
  externally optimize "don't break" — the same data, two engineering value systems parting ways.</strong> With that, Lesson 20's "three doors" are all walked through:
  tRPC for the UI, REST for the SDK, App-Router for streaming/webhooks — each divided and conquered by audience.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>One route factory</strong> <code>createAuthedProjectAPIRoute</code> unifies every public endpoint's auth → access level → rate limit → Zod-validate query/body → OTel(surface=publicapi) → response validation → oversized-body rejection.</li>
    <li><strong>Auth uses a Redis cache</strong> to scale: hit returns directly, miss falls back to Postgres by <code>fastHashedSecretKey</code> and re-caches; <strong>negative caching</strong> (<code>API_KEY_NON_EXISTENT</code>) blocks fake-key brute force.</li>
    <li><strong>Versioning by folder</strong>: v1 at root, v2/v3 subfolders; old paths never change, new versions can subtract (e.g. v3 scores drops JOIN-needing filters, uses cursor pagination).</li>
    <li><strong>Contract by Fern</strong>: hand-written Fern YAML → generated Python/TS SDKs + OpenAPI; dev-time response validation guards against the implementation drifting from the contract.</li>
    <li>Tradeoff: internal (tRPC) optimizes type-safety and speed, external (REST) optimizes stability and scale — same data, two value systems. With this, Lesson 20's "three doors" are all open.</li>
  </ul>
</div>
""")
LESSON_27 = {"zh": "\n".join(_ZH27), "en": "\n".join(_EN27)}
