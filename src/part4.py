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
<p>先看整体。<code>web/</code> 是一个 Next.js 应用，<code>web/src</code> 下分几大块：<code>features/</code>（按功能切的纵向模块，约 80 个）、
<code>components/</code>（共享 UI，含表格系统）、<code>server/</code>（鉴权 + tRPC）、<code>pages/</code>（页面与 API 路由）、还有少量 <code>app/</code>（App Router）。
而对外的接口，正是开篇说的三道门：</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">features/</span><span class="name">纵向功能模块（~80 个）</span></div><div class="ld">按业务功能切分的「竖切片」：traces、search-bar、public-api、batch-exports… 每个功能把自己的页面、组件、server 逻辑收在一处。Langfuse 绝大多数代码住在这里。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">components/</span><span class="name">共享 UI</span></div><div class="ld">跨功能复用的通用组件，最重要的是 <code>components/table/</code> 那套表格系统（第 24 课）——列表、过滤、分页、列控制、行选择全靠它，是整个后台界面的骨架。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">server/</span><span class="name">鉴权 + tRPC</span></div><div class="ld"><code>server/api/{root,trpc}.ts</code> 是 tRPC 的根与中间件、procedure 定义（第 21 课）；<code>server/auth.ts</code> 是 NextAuth 会话。这是「员工通道」的安检处。</div></div>
  <div class="layer l-app"><div class="lh"><span class="badge">pages/ · app/</span><span class="name">路由</span></div><div class="ld"><code>pages/</code> 是主干（UI 页面 + API 路由），<code>app/</code> 仅 4 个文件兜特殊语义。还有 <code>hooks/</code>、<code>ee/</code>（企业版）等。</div></div>
</div>

<p>这里值得停一下看 <code>features/</code> 的组织哲学：它是<strong>按「功能」而非按「技术层」切分</strong>的。传统做法可能把所有页面塞 <code>pages/</code>、所有组件塞 <code>components/</code>、所有接口塞 <code>api/</code>——
找一个功能的代码得在三四个目录间来回跳。Langfuse 反过来，每个功能（比如 search-bar、batch-exports）是一个<strong>自包含的竖切片</strong>，把它的前端组件、状态 hook、server 端逻辑、甚至说明 README 都收在
<code>features/&lt;功能&gt;/</code> 一处。好处是：读懂或修改一个功能，<strong>主要只需看一个目录</strong>；功能之间边界清晰，不易互相牵连。这也是为什么后面每讲一课，我们几乎都能精准地指向一个 <code>features/</code> 子目录，而不必满仓库地翻找散落各处的代码。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Next.js web 应用：Pages Router 承载 UI 页面与多数 API；三种 API 风格 tRPC 给 UI、REST 给 SDK、App-Router/SSE 给流式与 webhook">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Langfuse web 应用：一栋楼，三道门</text>
  <rect x="30" y="40" width="660" height="62" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="60" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">Next.js 应用（web/）· 以 Pages Router 为主</text><text x="360" y="78" text-anchor="middle" font-size="8" fill="var(--muted)">UI 页面 pages/project/[projectId]/…（traces / sessions / dashboards / datasets …）</text><text x="360" y="92" text-anchor="middle" font-size="8" fill="var(--muted)">src 目录：features/ · components/ · server/ · hooks/ · ee/</text>
  <rect x="24" y="124" width="210" height="100" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="129" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">① 员工通道 · tRPC</text><text x="129" y="164" text-anchor="middle" font-size="8" fill="var(--accent-ink)">pages/api/trpc/[trpc].ts</text><text x="129" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">给自家 UI · 类型安全</text><text x="129" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">~64 个 feature 路由</text><text x="129" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">第 21 课</text>
  <rect x="255" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="360" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">② 公共前台 · REST</text><text x="360" y="164" text-anchor="middle" font-size="8" fill="var(--ink)">pages/api/public/**</text><text x="360" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">给外部 SDK · 稳定带版本</text><text x="360" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">v1 / v2 / v3 + Fern 契约</text><text x="360" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">第 27 课</text>
  <rect x="486" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="591" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">③ 装卸口 · App-Router/SSE</text><text x="591" y="164" text-anchor="middle" font-size="7.5" fill="var(--muted)">app/api/**（仅 4 个文件）</text><text x="591" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">+ dashboard/execute-query-stream</text><text x="591" y="196" text-anchor="middle" font-size="7.5" fill="var(--muted)">流式 SSE · webhook</text>
  <line x1="129" y1="102" x2="129" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="360" y1="102" x2="360" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="591" y1="102" x2="591" y2="122" stroke="var(--faint)" stroke-width="1.4"/>
</svg>
<div class="figcap"><b>三道门各服务各的客</b>：<b>tRPC</b>（<code>pages/api/trpc/[trpc].ts</code>）给自家 UI、类型安全；<b>REST</b>（<code>pages/api/public/**</code>）给外部 SDK、稳定带版本；<b>App-Router/SSE</b>（<code>app/api/**</code> 仅 4 文件 + 流式端点）给 webhook 与流式。源码：<code>web/src/server/api/root.ts</code>、<code>web/src/features/public-api/</code>、<code>web/src/app/</code>。</div>
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
  <tr><td><b>App-Router / SSE</b></td><td>webhook 源 · 流式仪表盘</td><td><code>app/api/**</code> + 流式端点</td><td>需要原始 <code>Request</code>、<code>text/event-stream</code> 等 Pages Router 不顺手的语义</td></tr>
</table>

<p>这套划分背后是一条清晰的边界：<strong>对内求「类型安全、改得快」，对外求「契约稳定、版本可控」</strong>。UI 和后端是同一个团队、同一个仓库，用 tRPC 把类型一路打通，
重构时编译器即时报错；而 SDK 面向千千万万外部用户，接口一旦发布就不能随意改，于是用 REST + 版本号 + Fern 契约严格约束。<strong>同一批数据，两种对外姿态</strong>——
内部接口可以天天演进，外部契约必须长期稳定，把它们放进同一种 API 反而会互相掣肘。这正是 Part 4 要展开的读取链路的总纲。</p>

<p>预告一下整条读取链路：无论从哪道门进来，一次「查数据」的请求大致都要走这么几步。后面七课会逐站深入：</p>

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
    <li><strong>三种 API 风格并存</strong>：tRPC（UI，类型安全）、公共 REST（SDK，稳定带版本）、App-Router/SSE（流式/webhook）。</li>
    <li><code>web/src</code> 分层：<code>features/</code>（~80 个纵向功能模块）、<code>components/</code>（共享 UI）、<code>server/</code>（鉴权+tRPC）、<code>pages/</code>、<code>app/</code>。</li>
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
modules, ~80 of them), <code>components/</code> (shared UI, including the table system), <code>server/</code> (auth + tRPC), <code>pages/</code> (pages and API
routes), plus a small <code>app/</code> (App Router). And the external interfaces are exactly the three doors from the intro:</p>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">features/</span><span class="name">vertical feature modules (~80)</span></div><div class="ld">"Vertical slices" cut by business feature: traces, search-bar, public-api, batch-exports… each gathers its own pages, components, and server logic in one place. Most Langfuse code lives here.</div></div>
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
<svg viewBox="0 0 720 250" role="img" aria-label="Next.js web app: Pages Router carries UI pages and most APIs; three API styles tRPC for UI, REST for SDK, App-Router/SSE for streaming and webhooks">
  <text x="360" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">The Langfuse web app: one building, three doors</text>
  <rect x="30" y="40" width="660" height="62" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="60" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">Next.js app (web/) · primarily Pages Router</text><text x="360" y="78" text-anchor="middle" font-size="8" fill="var(--muted)">UI pages pages/project/[projectId]/… (traces / sessions / dashboards / datasets …)</text><text x="360" y="92" text-anchor="middle" font-size="8" fill="var(--muted)">src dirs: features/ · components/ · server/ · hooks/ · ee/</text>
  <rect x="24" y="124" width="210" height="100" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="129" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">① staff entrance · tRPC</text><text x="129" y="164" text-anchor="middle" font-size="8" fill="var(--accent-ink)">pages/api/trpc/[trpc].ts</text><text x="129" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">own UI · type-safe</text><text x="129" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">~64 feature routers</text><text x="129" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">Lesson 21</text>
  <rect x="255" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="360" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--teal)">② public reception · REST</text><text x="360" y="164" text-anchor="middle" font-size="8" fill="var(--ink)">pages/api/public/**</text><text x="360" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">external SDK · stable, versioned</text><text x="360" y="194" text-anchor="middle" font-size="7.5" fill="var(--muted)">v1 / v2 / v3 + Fern contract</text><text x="360" y="210" text-anchor="middle" font-size="7.5" fill="var(--faint)">Lesson 27</text>
  <rect x="486" y="124" width="210" height="100" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="591" y="146" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">③ loading dock · App-Router/SSE</text><text x="591" y="164" text-anchor="middle" font-size="7.5" fill="var(--muted)">app/api/** (only 4 files)</text><text x="591" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">+ dashboard/execute-query-stream</text><text x="591" y="196" text-anchor="middle" font-size="7.5" fill="var(--muted)">streaming SSE · webhook</text>
  <line x1="129" y1="102" x2="129" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="360" y1="102" x2="360" y2="122" stroke="var(--faint)" stroke-width="1.4"/><line x1="591" y1="102" x2="591" y2="122" stroke="var(--faint)" stroke-width="1.4"/>
</svg>
<div class="figcap"><b>Three doors, each serving its own crowd</b>: <b>tRPC</b> (<code>pages/api/trpc/[trpc].ts</code>) for the UI, type-safe; <b>REST</b> (<code>pages/api/public/**</code>) for external SDKs, stable and versioned; <b>App-Router/SSE</b> (<code>app/api/**</code>, 4 files + the streaming endpoint) for webhooks and streaming. Source: <code>web/src/server/api/root.ts</code>, <code>web/src/features/public-api/</code>, <code>web/src/app/</code>.</div>
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
  <tr><td><b>App-Router / SSE</b></td><td>webhook sources · streaming dashboards</td><td><code>app/api/**</code> + streaming endpoint</td><td>needs raw <code>Request</code>, <code>text/event-stream</code>, etc. — semantics Pages Router handles awkwardly</td></tr>
</table>

<p>Behind this split is a clear boundary: <strong>internally, seek "type-safe, fast to change"; externally, seek "stable contract, controlled versions"</strong>.
The UI and backend are one team, one repo, so tRPC threads types end to end — the compiler errors instantly on refactors; whereas the SDK faces countless external
users, where a published interface can't change freely, so REST + version numbers + the Fern contract enforce strict stability. <strong>Same data, two external
postures</strong> — the internal API can evolve daily, the external contract must stay stable for years; forcing them into one API style would only hobble each
other. This is the master plan of Part 4's read path.</p>

<p>A preview of the whole read path: whichever door you enter, a "query data" request roughly takes these steps. The next seven lessons dive into each stop:</p>

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
  <div class="tag">🎯 Design tradeoff</div>
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
    <li><strong>Three API styles coexist</strong>: tRPC (UI, type-safe), public REST (SDK, stable+versioned), App-Router/SSE (streaming/webhook).</li>
    <li><code>web/src</code> layers: <code>features/</code> (~80 vertical feature modules), <code>components/</code> (shared UI), <code>server/</code> (auth+tRPC), <code>pages/</code>, <code>app/</code>.</li>
    <li>Core boundary: <strong>internally seek type-safety and iteration speed (tRPC), externally seek contract stability and version control (REST + Fern)</strong> — same data, two external postures.</li>
    <li>This is Part 4's read-path overview; the next seven lessons drill into the tRPC backbone, repository layer, filtering, tables, detail, sessions, and the public REST API.</li>
  </ul>
</div>
""")
LESSON_20 = {"zh": "\n".join(_ZH20), "en": "\n".join(_EN20)}
