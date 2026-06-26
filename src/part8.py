"""Part 8 — 仪表盘·指标·成本 / Dashboards, metrics & cost. Lessons L40–L43.

Same authoring pattern as part1..part7: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L40 · 仪表盘 / widget 系统 / Dashboards & widgets
# ══════════════════════════════════════════════════════════════════════
_ZH40 = []
_EN40 = []

_ZH40.append(r"""
<p class="lead">
前七部分让你能<strong>看清单条</strong>——一条 trace、一个 score、一次实验。但运营一个 LLM 应用，你更常问的是<strong>全局</strong>的问题：这周成本涨了没？哪个模型最慢？平均有用性的走势如何？错误率有没有抬头？这些答案藏在成千上万条数据的<strong>聚合</strong>里——把它们汇成一张张图，就是<strong>仪表盘（dashboard）</strong>和它的积木 <strong>widget（图件）</strong>。
这一课讲它们的数据模型，重点是一个会反复回响的设计：一个 widget 把「<strong>要算什么</strong>」声明成 <code>view + dimensions + metrics + filters</code> 这样一套<strong>查询形状</strong>——而这套形状，正是第 33 课监控器复用的、也是下一课查询引擎要编译成 SQL 的。<strong>画一张图、盯一个指标、跑一个聚合，背后是同一种声明。</strong>
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  仪表盘就像汽车驾驶舱的那块<strong>仪表板</strong>：一块板上摆着一排<strong>表</strong>（widget）——油量表、转速表、时速表、水温灯。每块表只管一件事：<strong>读哪个量、画成什么样</strong>（指针？数字？柱状？），它<strong>不关心</strong>这个数到底是怎么从引擎、油箱里采集上来的。
  你能自由地往板上<strong>增删、挪动</strong>这些表，拼出最适合你的那套布局。而真正决定「这块表<strong>测什么、按什么分组</strong>」的，是一张<strong>声明</strong>（「测：平均时速；按：每分钟分组」），而不是焊死在表里的电路。于是同一份「测什么」的声明，既能驱动这块指针表，也能驱动旁边那盏「超速就亮」的警示灯（第 33 课监控）——<strong>测量与展示，是分开的两件事。</strong>
</div>
""")

# (L40 sections below)

_ZH40.append(r"""
<h2>仪表盘 = 一块布局 + 一排 widget</h2>
<p>数据模型分两层。<strong>Dashboard</strong> 是「一块板」：有名字、描述，一个 <code>definition</code>（JSON 布局，决定哪些 widget、各摆哪、多大），外加一组板级 <code>filters</code>（套在<strong>所有</strong> widget 上的全局过滤，比如「只看 production 环境」）。<strong>DashboardWidget</strong> 才是「一块表」：每个 widget 是一份保存好的<strong>查询 + 图表</strong>。一个 dashboard 装一排 widget，拼成你要的全景。</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="仪表盘布局：一个 Dashboard 含 definition 布局和全局 filters，板上摆着多个 DashboardWidget——折线图、柱状图、大数字、饼图，各自是一份查询+图表；全局 filter 同时套在所有 widget 上">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一块 Dashboard 板，摆一排 widget，全局 filter 套全板</text>
  <rect x="30" y="36" width="660" height="30" rx="7" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="56" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">Dashboard：definition（布局）+ 全局 filters（套在所有 widget 上，如「env=production」）</text>
  <rect x="40" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 成本走势</text><polyline points="60,138 90,128 120,132 150,118 180,122 210,110" fill="none" stroke="var(--accent)" stroke-width="1.6"/><text x="140" y="120" text-anchor="middle" font-size="6.4" fill="var(--muted)">折线时序</text>
  <rect x="260" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 各模型调用量</text><rect x="290" y="124" width="14" height="18" fill="var(--accent)"/><rect x="312" y="116" width="14" height="26" fill="var(--accent)"/><rect x="334" y="130" width="14" height="12" fill="var(--accent)"/><rect x="356" y="120" width="14" height="22" fill="var(--accent)"/><text x="410" y="135" text-anchor="middle" font-size="6.4" fill="var(--muted)">柱状</text>
  <rect x="480" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 总成本</text><text x="580" y="134" text-anchor="middle" font-size="15" font-weight="800" fill="var(--accent-ink)">$1,284</text>
  <rect x="40" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 平均有用性</text><polyline points="60,214 90,206 120,210 150,200 180,196 210,190" fill="none" stroke="var(--teal)" stroke-width="1.6"/><text x="140" y="198" text-anchor="middle" font-size="6.4" fill="var(--muted)">折线时序</text>
  <rect x="260" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · score 分布</text><circle cx="360" cy="200" r="16" fill="none" stroke="var(--accent)" stroke-width="6" stroke-dasharray="60 40"/><text x="410" y="203" text-anchor="middle" font-size="6.4" fill="var(--muted)">饼图</text>
  <rect x="480" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 延迟直方</text><rect x="510" y="206" width="10" height="12" fill="var(--teal)"/><rect x="524" y="198" width="10" height="20" fill="var(--teal)"/><rect x="538" y="202" width="10" height="16" fill="var(--teal)"/><rect x="552" y="210" width="10" height="8" fill="var(--teal)"/><text x="620" y="210" text-anchor="middle" font-size="6.4" fill="var(--muted)">直方图</text>
</svg>
<div class="figcap"><b>两层结构</b>：<code>schema.prisma:1494</code> Dashboard 有 <code>definition</code>（布局 JSON）与板级 <code>filters</code>；<code>:1536</code> DashboardWidget 是单块「查询+图表」。一个板上的多个 widget 各看一个角度，板级 filter 同时收敛全部——「先全局圈定范围，再各看各的指标」。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">板</span><span class="name">Dashboard</span></div><div class="ld">一块画布：<code>definition</code> 是 JSON 布局（哪些 widget、各占什么格子），<code>filters</code> 是板级全局过滤。projectId 可空——Langfuse 还内置了一批「托管仪表盘」开箱即用。你能像摆桌面小组件一样自由编排。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">表</span><span class="name">DashboardWidget</span></div><div class="ld">一块表 = 一份<strong>声明式查询</strong>（<code>view</code> 看什么数据 + <code>dimensions</code> 按什么分组 + <code>metrics</code> 算什么 + <code>filters</code>）<strong>加</strong>一种<strong>图表呈现</strong>（<code>chartType</code> + <code>chartConfig</code>）。查询定义「算什么」，图表定义「怎么画」——下一节细看。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">复用</span><span class="name">同一份指标，多处消费</span></div><div class="ld">widget 的查询形状不是仪表盘私有的：第 33 课的监控器直接<strong>复用</strong>它（注释原文「mirrors DashboardWidget」），下一课的查询引擎负责把它<strong>编译成 ClickHouse SQL</strong>。一份「算什么」，画图、告警、聚合三处共享。</div></div>
</div>
""")

# (L40 sec2 widget below)

_ZH40.append(r"""
<h2>widget = 声明式查询 + 图表呈现</h2>
<p>拆开一个 widget，它清清楚楚分成两半：<strong>查询</strong>（要算什么）和<strong>图表</strong>（怎么画）。查询那半是四件套：<code>view</code>（数据源：TRACES / OBSERVATIONS / SCORES_NUMERIC / SCORES_CATEGORICAL）、<code>dimensions</code>（分组轴，如「按模型」「按天」）、<code>metrics</code>（聚合量，如「计数」「成本求和」「分数求平均」）、<code>filters</code>（过滤）。图表那半是 <code>chartType</code>（折线/柱状/饼/大数字/直方/透视表…）+ <code>chartConfig</code>。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="widget 的两半：左边查询声明 view+dimensions+metrics+filters 决定算什么，右边 chartType+chartConfig 决定怎么画；同一份查询可换不同图表呈现">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一个 widget：左半「算什么」+ 右半「怎么画」</text>
  <rect x="30" y="40" width="320" height="140" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="190" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">查询（声明：算什么）</text><rect x="46" y="72" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="87" text-anchor="middle" font-size="7" fill="var(--ink)">view: OBSERVATIONS（看观测）</text><rect x="46" y="98" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="113" text-anchor="middle" font-size="7" fill="var(--ink)">dimensions: [model]（按模型分组）</text><rect x="46" y="124" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="139" text-anchor="middle" font-size="7" fill="var(--ink)">metrics: [sum(totalCost)]（成本求和）</text><rect x="46" y="150" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="165" text-anchor="middle" font-size="7" fill="var(--ink)">filters: [env=production]</text>
  <rect x="400" y="40" width="290" height="140" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="545" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">图表（呈现：怎么画）</text><text x="545" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">chartType: BAR / LINE / PIE / NUMBER …</text><rect x="430" y="120" width="20" height="40" fill="var(--accent)"/><rect x="460" y="100" width="20" height="60" fill="var(--accent)"/><rect x="490" y="132" width="20" height="28" fill="var(--accent)"/><rect x="520" y="112" width="20" height="48" fill="var(--accent)"/><text x="620" y="135" text-anchor="middle" font-size="6.6" fill="var(--muted)">同一查询</text><text x="620" y="147" text-anchor="middle" font-size="6.6" fill="var(--muted)">可换图表</text>
  <line x1="350" y1="110" x2="398" y2="110" stroke="var(--accent)" stroke-width="1.6"/><polygon points="398,110 389,106 389,114" fill="var(--accent)"/>
  <text x="360" y="194" text-anchor="middle" font-size="8" fill="var(--faint)">查询与图表解耦：换一种 chartType 不动查询，换一个 metric 不动画法——各自独立演化</text>
</svg>
<div class="figcap"><b>声明式查询 + 呈现，干净分家</b>：<code>schema.prisma:1536</code> DashboardWidget 把 <code>view</code>/<code>dimensions</code>/<code>metrics</code>/<code>filters</code>（算什么）与 <code>chartType</code>/<code>chartConfig</code>（怎么画）分别建模。<code>view</code> 取自 <code>DashboardWidgetViews</code>（4 值），<code>chartType</code> 取自 <code>DashboardWidgetChartType</code>（9 种图）。</div>
</div>

<table class="t">
  <thead><tr><th>四件套（查询）</th><th>含义</th><th>例子</th></tr></thead>
  <tbody>
    <tr><td><code>view</code></td><td>数据源</td><td>TRACES / OBSERVATIONS / SCORES_NUMERIC / SCORES_CATEGORICAL</td></tr>
    <tr><td><code>dimensions</code></td><td>分组轴（GROUP BY）</td><td>按 model、按 day、按 name……</td></tr>
    <tr><td><code>metrics</code></td><td>聚合量</td><td>count、sum(totalCost)、avg(value)、p95(latency)</td></tr>
    <tr><td><code>filters</code></td><td>过滤条件</td><td>env=production、name=chat、时间窗</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma:1516-1560</span><span class="ln">widget 模型 + 两个枚举</span></div>
  <pre class="code"><span class="kw">enum</span> DashboardWidgetViews { TRACES  OBSERVATIONS  SCORES_NUMERIC  SCORES_CATEGORICAL }
<span class="kw">enum</span> DashboardWidgetChartType { LINE_TIME_SERIES  BAR_TIME_SERIES  HORIZONTAL_BAR
  VERTICAL_BAR  PIE  NUMBER  HISTOGRAM  PIVOT_TABLE  … }   <span class="cm">// 9 种图表</span>
<span class="kw">model</span> DashboardWidget {
  view       DashboardWidgetViews   <span class="cm">// 看什么数据</span>
  dimensions Json   <span class="cm">// 按什么分组（GROUP BY 轴）</span>
  metrics    Json   <span class="cm">// 算什么（聚合）</span>
  filters    Json   <span class="cm">// 过滤</span>
  chartType   DashboardWidgetChartType   <span class="cm">// 怎么画</span>
  chartConfig Json                       <span class="cm">// 图表细节</span>
}</pre>
</div>

<table class="t">
  <thead><tr><th>图表类型（节选）</th><th>适合表达</th><th>典型用途</th></tr></thead>
  <tbody>
    <tr><td>LINE / AREA / BAR_TIME_SERIES</td><td>随时间的<b>趋势</b></td><td>成本走势、每日调用量、分数变化</td></tr>
    <tr><td>HORIZONTAL / VERTICAL_BAR</td><td>类别间<b>对比</b></td><td>各模型调用量、各用户花费排名</td></tr>
    <tr><td>NUMBER</td><td>单个<b>关键值</b></td><td>本月总成本、总 trace 数（KPI 大数字）</td></tr>
    <tr><td>PIE</td><td>整体的<b>构成</b></td><td>各模型成本占比、score 分类分布</td></tr>
    <tr><td>HISTOGRAM</td><td>数值的<b>分布</b></td><td>延迟分布、token 数分布</td></tr>
    <tr><td>PIVOT_TABLE</td><td>多维<b>交叉</b></td><td>模型 × 环境 的成本矩阵</td></tr>
  </tbody>
</table>
<p>同一份查询，选不同 chartType 就是不同的看法：想看趋势用时序、想比大小用柱状、想看构成用饼、想看分布用直方。<strong>数据不变，视角随需而换</strong>——这正是查询/呈现分离给探索带来的自由。</p>
""")

# (L40 sec3 reuse below)

_ZH40.append(r"""
<h2>一份查询形状，三处复用</h2>
<p>widget 这套 <code>view + dimensions + metrics + filters</code> 的声明，最妙的不是它能画图，而是它<strong>不只用来画图</strong>。同一套声明被三个地方共享：仪表盘拿它<strong>画成图表</strong>、第 33 课的监控器拿它<strong>定时算并比阈值</strong>、下一课的查询引擎拿它<strong>编译成 ClickHouse SQL</strong>。一个例证就藏在枚举里：监控器的 <code>MonitorView</code> 恰好是 <code>DashboardWidgetViews</code> <strong>去掉 TRACES</strong>（源码注释原文「mirrors DashboardWidget, minus TRACES」）。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="一份查询形状三处复用：同一套 view+dimensions+metrics+filters 声明，被仪表盘用来画图表、被第33课监控器用来定时比阈值、被第41课查询引擎用来编译成 ClickHouse SQL">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">同一份「算什么」声明，喂给三个消费者</text>
  <rect x="250" y="40" width="220" height="50" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">查询形状（声明）</text><text x="360" y="78" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">view + dimensions + metrics + filters</text>
  <rect x="40" y="130" width="190" height="50" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="135" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">仪表盘（本课）</text><text x="135" y="167" text-anchor="middle" font-size="6.6" fill="var(--muted)">画成图表（pull：你来看）</text>
  <rect x="265" y="130" width="190" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">监控器（第33课）</text><text x="360" y="167" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">定时比阈值（push：它来喊）</text>
  <rect x="490" y="130" width="190" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="585" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">查询引擎（第41课）</text><text x="585" y="167" text-anchor="middle" font-size="6.6" fill="var(--muted)">编译成 ClickHouse SQL</text>
  <line x1="320" y1="90" x2="160" y2="128" stroke="var(--blue)" stroke-width="1.4"/><polygon points="160,128 169,124 165,120" fill="var(--blue)"/>
  <line x1="360" y1="90" x2="360" y2="128" stroke="var(--accent)" stroke-width="1.4"/><polygon points="360,128 356,119 364,119" fill="var(--accent)"/>
  <line x1="400" y1="90" x2="560" y2="128" stroke="var(--teal)" stroke-width="1.4"/><polygon points="560,128 551,120 555,124" fill="var(--teal)"/>
  <text x="360" y="116" text-anchor="middle" font-size="7" fill="var(--faint)">MonitorView = DashboardWidgetViews 去掉 TRACES（源码注释 mirrors DashboardWidget, minus TRACES）</text>
</svg>
<div class="figcap"><b>声明一次，处处复用</b>：能在仪表盘上画出的任何曲线，都能一键变成一个监控告警（第 33 课），也都由同一个查询引擎（第 41 课）落成 SQL。<b>pull</b>（仪表盘你来看）与 <b>push</b>（监控它来喊）共享同一个指标定义——这正是第 33 课能「复用 DashboardWidget」的根因。</div>
</div>

<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么 widget 要把「算什么」和「怎么画」分开声明，而不是直接写死一段「画某张图」的代码？</strong> 因为这是两个<strong>正交</strong>的维度，强行耦合只会两头受限。把它们分开，你立刻得到三重自由：同一份查询<strong>换个 chartType</strong> 就从折线变柱状（探索数据时极有用）；同一种图表<strong>换个 metric</strong> 就从看成本变看延迟；更关键的是，那份纯粹的「算什么」声明，因为<strong>不掺任何展示逻辑</strong>，才能被监控器、查询引擎原样借走。<strong>声明式的威力，正在于它描述「意图」而非「步骤」</strong>——意图可以被任意多个执行者以不同方式实现。这和第 23 课 FilterState、第 21 课 tRPC 契约是同一种信念：把「想要什么」从「怎么做到」里剥离，复用与演进的空间就此打开。<br><br>
  <strong>为什么这套查询形状值得被三处共用，而不是各写各的？</strong> 因为「指标」这个概念在产品里本就该<strong>统一</strong>。如果仪表盘上的「平均有用性」和监控器里的「平均有用性」是两段独立实现，它们迟早会<strong>算出不同的数</strong>——口径漂移是数据产品的慢性毒药。让三处共享同一份声明、同一个查询引擎，等于钉死了「这个指标全公司只有一种算法」。你在图上看到的、和告警依据的、和 API 取到的，<strong>永远是同一个数</strong>。一致性不是靠纪律维持，而是靠架构<strong>从根上保证</strong>。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>仪表盘看全局</strong>：把成千上万条数据聚合成图，回答「成本涨没」「哪个模型慢」「分数走势」这类全局问题——补上前七部分「看单条」之外的「看整体」。</li>
    <li><strong>两层模型</strong>：<code>Dashboard</code>（<code>definition</code> 布局 + 板级 <code>filters</code>）装一排 <code>DashboardWidget</code>；每个 widget 是一份保存好的「查询 + 图表」。</li>
    <li><strong>widget = 声明式查询 + 图表</strong>：查询四件套 <code>view</code>（数据源）+ <code>dimensions</code>（分组）+ <code>metrics</code>（聚合）+ <code>filters</code>；呈现是 <code>chartType</code>（9 种图）+ <code>chartConfig</code>。算什么与怎么画，干净分家。</li>
    <li><strong>查询/呈现解耦</strong>：换图不动查询、换指标不动画法；纯粹的「算什么」声明才能被原样复用——声明式描述意图而非步骤。</li>
    <li><strong>一份查询形状三处复用</strong>：仪表盘画图、第 33 课监控比阈值、第 41 课引擎编译 SQL，共享同一声明（<code>MonitorView</code> = <code>DashboardWidgetViews</code> 去掉 TRACES）。指标全公司一种算法，pull 与 push 永远同一个数。</li>
  </ul>
</div>
""")

_EN40.append(r"""
<p class="lead">
The first seven parts let you <strong>see one thing clearly</strong>—one trace, one score, one experiment. But operating an LLM app, you more often ask <strong>global</strong> questions: did cost rise this week? which model is slowest? how is average helpfulness trending? is the error rate creeping up? These answers hide in the <strong>aggregation</strong> of thousands of records—rolling them into charts is the <strong>dashboard</strong> and its building block, the <strong>widget</strong>.
This lesson covers their data model, focusing on a design that will echo repeatedly: a widget declares "<strong>what to compute</strong>" as a <code>view + dimensions + metrics + filters</code> <strong>query shape</strong>—and this shape is the very one Lesson 33's monitor reuses, and the one the next lesson's query engine compiles to SQL. <strong>Drawing a chart, watching a metric, running an aggregation—behind them is the same declaration.</strong>
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  A dashboard is like a car's cockpit <strong>instrument panel</strong>: a board with a row of <strong>gauges</strong> (widgets)—fuel gauge, tachometer, speedometer, temperature light. Each gauge cares about one thing: <strong>which quantity to read, and how to draw it</strong> (needle? number? bar?); it <strong>doesn't care</strong> how that number was actually gathered from the engine or tank.
  You can freely <strong>add, remove, rearrange</strong> these gauges into the layout that suits you. And what truly decides "what this gauge <strong>measures, grouped by what</strong>" is a <strong>declaration</strong> ("measure: average speed; group by: per minute"), not circuitry welded into the gauge. So the same "what to measure" declaration can drive both this needle gauge and the "blinks when over-speeding" warning light next to it (Lesson 33's monitor)—<strong>measurement and display are two separate things.</strong>
</div>
""")

_EN40.append(r"""
<h2>A dashboard = a layout + a row of widgets</h2>
<p>The data model has two layers. <strong>Dashboard</strong> is "the board": a name, a description, a <code>definition</code> (JSON layout deciding which widgets go where and how big), plus a set of board-level <code>filters</code> (global filters applied to <strong>all</strong> widgets, e.g. "only production"). <strong>DashboardWidget</strong> is "a gauge": each widget is a saved <strong>query + chart</strong>. A dashboard holds a row of widgets, composing the panorama you want.</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="Dashboard layout: a Dashboard has a definition layout and global filters, with multiple DashboardWidgets on the board—a line chart, bar chart, big number, pie—each a query+chart; the global filter applies to all widgets at once">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">one Dashboard board, a row of widgets, global filter over the whole board</text>
  <rect x="30" y="36" width="660" height="30" rx="7" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="56" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">Dashboard: definition (layout) + global filters (on all widgets, e.g. "env=production")</text>
  <rect x="40" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · cost trend</text><polyline points="60,138 90,128 120,132 150,118 180,122 210,110" fill="none" stroke="var(--accent)" stroke-width="1.6"/><text x="140" y="120" text-anchor="middle" font-size="6.4" fill="var(--muted)">line time-series</text>
  <rect x="260" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · calls per model</text><rect x="290" y="124" width="14" height="18" fill="var(--accent)"/><rect x="312" y="116" width="14" height="26" fill="var(--accent)"/><rect x="334" y="130" width="14" height="12" fill="var(--accent)"/><rect x="356" y="120" width="14" height="22" fill="var(--accent)"/><text x="410" y="135" text-anchor="middle" font-size="6.4" fill="var(--muted)">bar</text>
  <rect x="480" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · total cost</text><text x="580" y="134" text-anchor="middle" font-size="15" font-weight="800" fill="var(--accent-ink)">$1,284</text>
  <rect x="40" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · avg helpfulness</text><polyline points="60,214 90,206 120,210 150,200 180,196 210,190" fill="none" stroke="var(--teal)" stroke-width="1.6"/><text x="140" y="198" text-anchor="middle" font-size="6.4" fill="var(--muted)">line time-series</text>
  <rect x="260" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · score distribution</text><circle cx="360" cy="200" r="16" fill="none" stroke="var(--accent)" stroke-width="6" stroke-dasharray="60 40"/><text x="410" y="203" text-anchor="middle" font-size="6.4" fill="var(--muted)">pie</text>
  <rect x="480" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · latency histogram</text><rect x="510" y="206" width="10" height="12" fill="var(--teal)"/><rect x="524" y="198" width="10" height="20" fill="var(--teal)"/><rect x="538" y="202" width="10" height="16" fill="var(--teal)"/><rect x="552" y="210" width="10" height="8" fill="var(--teal)"/><text x="620" y="210" text-anchor="middle" font-size="6.4" fill="var(--muted)">histogram</text>
</svg>
<div class="figcap"><b>Two-layer structure</b>: <code>schema.prisma:1494</code> Dashboard has a <code>definition</code> (layout JSON) and board-level <code>filters</code>; <code>:1536</code> DashboardWidget is one "query+chart". Multiple widgets on a board each show one angle, the board filter converging all at once—"globally scope first, then each shows its own metric".</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">board</span><span class="name">Dashboard</span></div><div class="ld">A canvas: <code>definition</code> is a JSON layout (which widgets, what grid cells), <code>filters</code> are board-level global filters. projectId is optional—Langfuse ships a set of "managed dashboards" ready out of the box. You arrange it freely like desktop widgets.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">gauge</span><span class="name">DashboardWidget</span></div><div class="ld">A gauge = a <strong>declarative query</strong> (<code>view</code> what data + <code>dimensions</code> group by what + <code>metrics</code> compute what + <code>filters</code>) <strong>plus</strong> a <strong>chart presentation</strong> (<code>chartType</code> + <code>chartConfig</code>). The query defines "what to compute", the chart defines "how to draw"—detailed next.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">reuse</span><span class="name">one metric, many consumers</span></div><div class="ld">The widget's query shape isn't dashboard-private: Lesson 33's monitor directly <strong>reuses</strong> it (the source comment "mirrors DashboardWidget"), and the next lesson's query engine <strong>compiles it to ClickHouse SQL</strong>. One "what to compute" is shared by charting, alerting, and aggregation.</div></div>
</div>
""")

# (en sec2/3/spark below)

_EN40.append(r"""
<h2>A widget = a declarative query + a chart presentation</h2>
<p>Unpack a widget and it clearly splits in two: the <strong>query</strong> (what to compute) and the <strong>chart</strong> (how to draw). The query half is a quartet: <code>view</code> (data source: TRACES / OBSERVATIONS / SCORES_NUMERIC / SCORES_CATEGORICAL), <code>dimensions</code> (group-by axes, e.g. "by model", "by day"), <code>metrics</code> (aggregations, e.g. "count", "sum cost", "average score"), <code>filters</code>. The chart half is <code>chartType</code> (line/bar/pie/number/histogram/pivot…) + <code>chartConfig</code>.</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="A widget's two halves: the left query declaration view+dimensions+metrics+filters decides what to compute, the right chartType+chartConfig decides how to draw; the same query can switch chart presentations">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">one widget: left "what to compute" + right "how to draw"</text>
  <rect x="30" y="40" width="320" height="140" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="190" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">query (declare: what to compute)</text><rect x="46" y="72" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="87" text-anchor="middle" font-size="7" fill="var(--ink)">view: OBSERVATIONS</text><rect x="46" y="98" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="113" text-anchor="middle" font-size="7" fill="var(--ink)">dimensions: [model] (group by model)</text><rect x="46" y="124" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="139" text-anchor="middle" font-size="7" fill="var(--ink)">metrics: [sum(totalCost)]</text><rect x="46" y="150" width="288" height="22" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="190" y="165" text-anchor="middle" font-size="7" fill="var(--ink)">filters: [env=production]</text>
  <rect x="400" y="40" width="290" height="140" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="545" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">chart (present: how to draw)</text><text x="545" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">chartType: BAR / LINE / PIE / NUMBER …</text><rect x="430" y="120" width="20" height="40" fill="var(--accent)"/><rect x="460" y="100" width="20" height="60" fill="var(--accent)"/><rect x="490" y="132" width="20" height="28" fill="var(--accent)"/><rect x="520" y="112" width="20" height="48" fill="var(--accent)"/><text x="620" y="135" text-anchor="middle" font-size="6.6" fill="var(--muted)">same query</text><text x="620" y="147" text-anchor="middle" font-size="6.6" fill="var(--muted)">swap the chart</text>
  <line x1="350" y1="110" x2="398" y2="110" stroke="var(--accent)" stroke-width="1.6"/><polygon points="398,110 389,106 389,114" fill="var(--accent)"/>
  <text x="360" y="194" text-anchor="middle" font-size="8" fill="var(--faint)">query and chart decoupled: swap a chartType without touching the query, swap a metric without touching the drawing—each evolves independently</text>
</svg>
<div class="figcap"><b>declarative query + presentation, cleanly split</b>: <code>schema.prisma:1536</code> DashboardWidget models <code>view</code>/<code>dimensions</code>/<code>metrics</code>/<code>filters</code> (what to compute) separately from <code>chartType</code>/<code>chartConfig</code> (how to draw). <code>view</code> from <code>DashboardWidgetViews</code> (4 values), <code>chartType</code> from <code>DashboardWidgetChartType</code> (9 charts).</div>
</div>

<table class="t">
  <thead><tr><th>quartet (query)</th><th>meaning</th><th>example</th></tr></thead>
  <tbody>
    <tr><td><code>view</code></td><td>data source</td><td>TRACES / OBSERVATIONS / SCORES_NUMERIC / SCORES_CATEGORICAL</td></tr>
    <tr><td><code>dimensions</code></td><td>group-by axes (GROUP BY)</td><td>by model, by day, by name…</td></tr>
    <tr><td><code>metrics</code></td><td>aggregations</td><td>count, sum(totalCost), avg(value), p95(latency)</td></tr>
    <tr><td><code>filters</code></td><td>filter conditions</td><td>env=production, name=chat, time window</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma:1516-1560</span><span class="ln">widget model + two enums</span></div>
  <pre class="code"><span class="kw">enum</span> DashboardWidgetViews { TRACES  OBSERVATIONS  SCORES_NUMERIC  SCORES_CATEGORICAL }
<span class="kw">enum</span> DashboardWidgetChartType { LINE_TIME_SERIES  BAR_TIME_SERIES  HORIZONTAL_BAR
  VERTICAL_BAR  PIE  NUMBER  HISTOGRAM  PIVOT_TABLE  … }   <span class="cm">// 9 chart types</span>
<span class="kw">model</span> DashboardWidget {
  view       DashboardWidgetViews   <span class="cm">// what data</span>
  dimensions Json   <span class="cm">// group by what (GROUP BY axes)</span>
  metrics    Json   <span class="cm">// compute what (aggregations)</span>
  filters    Json   <span class="cm">// filter</span>
  chartType   DashboardWidgetChartType   <span class="cm">// how to draw</span>
  chartConfig Json                       <span class="cm">// chart details</span>
}</pre>
</div>

<table class="t">
  <thead><tr><th>chart type (selection)</th><th>good at expressing</th><th>typical use</th></tr></thead>
  <tbody>
    <tr><td>LINE / AREA / BAR_TIME_SERIES</td><td><b>trend</b> over time</td><td>cost trend, daily call volume, score changes</td></tr>
    <tr><td>HORIZONTAL / VERTICAL_BAR</td><td><b>comparison</b> across categories</td><td>calls per model, spend ranking by user</td></tr>
    <tr><td>NUMBER</td><td>a single <b>key value</b></td><td>this month's total cost, total trace count (KPI number)</td></tr>
    <tr><td>PIE</td><td><b>composition</b> of a whole</td><td>cost share per model, score categorical distribution</td></tr>
    <tr><td>HISTOGRAM</td><td><b>distribution</b> of a value</td><td>latency distribution, token-count distribution</td></tr>
    <tr><td>PIVOT_TABLE</td><td>multi-dimensional <b>cross-tab</b></td><td>model × environment cost matrix</td></tr>
  </tbody>
</table>
<p>The same query, with a different chartType, is a different view: trend → time-series, magnitude → bar, composition → pie, distribution → histogram. <strong>Data stays, the angle changes on demand</strong>—exactly the exploratory freedom query/presentation separation brings.</p>
""")

_EN40.append(r"""
<h2>One query shape, three reuses</h2>
<p>The widget's <code>view + dimensions + metrics + filters</code> declaration—the neat part isn't that it can draw charts, it's that it's <strong>not only for drawing charts</strong>. The same declaration is shared by three places: the dashboard <strong>draws it as a chart</strong>, Lesson 33's monitor <strong>periodically computes it and compares to thresholds</strong>, and the next lesson's query engine <strong>compiles it to ClickHouse SQL</strong>. One proof hides in the enums: the monitor's <code>MonitorView</code> is exactly <code>DashboardWidgetViews</code> <strong>minus TRACES</strong> (the source comment literally says "mirrors DashboardWidget, minus TRACES").</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="One query shape, three reuses: the same view+dimensions+metrics+filters declaration is used by the dashboard to draw charts, by Lesson 33's monitor to periodically compare thresholds, and by Lesson 41's query engine to compile ClickHouse SQL">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">one "what to compute" declaration, fed to three consumers</text>
  <rect x="250" y="40" width="220" height="50" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">query shape (declaration)</text><text x="360" y="78" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">view + dimensions + metrics + filters</text>
  <rect x="40" y="130" width="190" height="50" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="135" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">dashboard (this lesson)</text><text x="135" y="167" text-anchor="middle" font-size="6.6" fill="var(--muted)">draw as a chart (pull: you look)</text>
  <rect x="265" y="130" width="190" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">monitor (Lesson 33)</text><text x="360" y="167" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">periodic threshold (push: it calls)</text>
  <rect x="490" y="130" width="190" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="585" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">query engine (Lesson 41)</text><text x="585" y="167" text-anchor="middle" font-size="6.6" fill="var(--muted)">compile to ClickHouse SQL</text>
  <line x1="320" y1="90" x2="160" y2="128" stroke="var(--blue)" stroke-width="1.4"/><polygon points="160,128 169,124 165,120" fill="var(--blue)"/>
  <line x1="360" y1="90" x2="360" y2="128" stroke="var(--accent)" stroke-width="1.4"/><polygon points="360,128 356,119 364,119" fill="var(--accent)"/>
  <line x1="400" y1="90" x2="560" y2="128" stroke="var(--teal)" stroke-width="1.4"/><polygon points="560,128 551,120 555,124" fill="var(--teal)"/>
  <text x="360" y="116" text-anchor="middle" font-size="7" fill="var(--faint)">MonitorView = DashboardWidgetViews minus TRACES (source comment: mirrors DashboardWidget, minus TRACES)</text>
</svg>
<div class="figcap"><b>declare once, reuse everywhere</b>: any curve you can draw on a dashboard can become a monitor alert in one click (Lesson 33), and is compiled to SQL by the same query engine (Lesson 41). <b>Pull</b> (you look at a dashboard) and <b>push</b> (a monitor calls you) share one metric definition—the very reason Lesson 33 can "reuse DashboardWidget".</div>
</div>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why does a widget declare "what to compute" and "how to draw" separately rather than just write code that "draws some chart"?</strong> Because these are two <strong>orthogonal</strong> dimensions, and forcing them together limits both. Splitting them, you instantly get triple freedom: the same query <strong>swaps a chartType</strong> to go from line to bar (great for exploring data); the same chart <strong>swaps a metric</strong> to go from cost to latency; and crucially, that pure "what to compute" declaration, <strong>untainted by any presentation logic</strong>, can be borrowed verbatim by the monitor and the query engine. <strong>The power of declarative is that it describes "intent" not "steps"</strong>—intent can be realized by arbitrarily many executors in different ways. Same belief as Lesson 23's FilterState and Lesson 21's tRPC contract: lift "what you want" out of "how to do it", and the room for reuse and evolution opens up.<br><br>
  <strong>Why is this query shape worth sharing across three places rather than each writing its own?</strong> Because "a metric" as a product concept should be <strong>unified</strong>. If the dashboard's "average helpfulness" and the monitor's "average helpfulness" are two separate implementations, they will eventually <strong>compute different numbers</strong>—definition drift is a slow poison for data products. Having three places share one declaration and one query engine nails down "this metric has exactly one algorithm company-wide". What you see on the chart, what alerts are based on, and what the API returns are <strong>always the same number</strong>. Consistency isn't maintained by discipline but <strong>guaranteed at the root by architecture</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Dashboards see the global</strong>: aggregate thousands of records into charts, answering "did cost rise", "which model is slow", "score trends"—adding the "see the whole" the first seven parts' "see one" lacked.</li>
    <li><strong>Two-layer model</strong>: <code>Dashboard</code> (<code>definition</code> layout + board-level <code>filters</code>) holds a row of <code>DashboardWidget</code>s; each widget is a saved "query + chart".</li>
    <li><strong>A widget = declarative query + chart</strong>: the query quartet <code>view</code> (source) + <code>dimensions</code> (group) + <code>metrics</code> (aggregate) + <code>filters</code>; presentation is <code>chartType</code> (9 charts) + <code>chartConfig</code>. What to compute and how to draw, cleanly split.</li>
    <li><strong>Query/presentation decoupled</strong>: swap the chart without the query, swap the metric without the drawing; a pure "what to compute" declaration can be reused verbatim—declarative describes intent not steps.</li>
    <li><strong>One query shape, three reuses</strong>: dashboard charts, Lesson 33 monitor thresholds, Lesson 41 engine SQL share one declaration (<code>MonitorView</code> = <code>DashboardWidgetViews</code> minus TRACES). One algorithm per metric company-wide; pull and push always the same number.</li>
  </ul>
</div>
""")

LESSON_40 = {"zh": "\n".join(_ZH40), "en": "\n".join(_EN40)}
