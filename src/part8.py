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
  <rect x="40" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 成本走势</text><polyline points="60,138 90,128 120,132 150,118 180,122 210,110" fill="none" stroke="var(--accent)" stroke-width="1.6"/><text x="140" y="120" text-anchor="middle" font-size="6.5" fill="var(--muted)">折线时序</text>
  <rect x="260" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 各模型调用量</text><rect x="290" y="124" width="14" height="18" fill="var(--accent)"/><rect x="312" y="116" width="14" height="26" fill="var(--accent)"/><rect x="334" y="130" width="14" height="12" fill="var(--accent)"/><rect x="356" y="120" width="14" height="22" fill="var(--accent)"/><text x="410" y="135" text-anchor="middle" font-size="6.5" fill="var(--muted)">柱状</text>
  <rect x="480" y="84" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 总成本</text><text x="580" y="134" text-anchor="middle" font-size="15" font-weight="800" fill="var(--accent-ink)">$1,284</text>
  <rect x="40" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 平均有用性</text><polyline points="60,214 90,206 120,210 150,200 180,196 210,190" fill="none" stroke="var(--teal)" stroke-width="1.6"/><text x="140" y="198" text-anchor="middle" font-size="6.5" fill="var(--muted)">折线时序</text>
  <rect x="260" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · score 分布</text><circle cx="360" cy="200" r="16" fill="none" stroke="var(--accent)" stroke-width="6" stroke-dasharray="60 40"/><text x="410" y="203" text-anchor="middle" font-size="6.5" fill="var(--muted)">饼图</text>
  <rect x="480" y="160" width="200" height="64" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="580" y="180" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">widget · 延迟直方</text><rect x="510" y="206" width="10" height="12" fill="var(--teal)"/><rect x="524" y="198" width="10" height="20" fill="var(--teal)"/><rect x="538" y="202" width="10" height="16" fill="var(--teal)"/><rect x="552" y="210" width="10" height="8" fill="var(--teal)"/><text x="620" y="210" text-anchor="middle" font-size="6.5" fill="var(--muted)">直方图</text>
</svg>
<div class="figcap"><b>两层结构</b>：<code>schema.prisma:1494</code> Dashboard 有 <code>definition</code>（布局 JSON）与板级 <code>filters</code>；<code>:1536</code> DashboardWidget 是单块「查询+图表」。一个板上的多个 widget 各看一个角度，板级 filter 同时收敛全部——「先全局圈定范围，再各看各的指标」。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 368" role="img" aria-label="仪表盘真实例子：顶部是筛选条（时间范围、env=production、model 过滤），下面 2×2 四个 widget——折线 LINE_TIME_SERIES 每日 trace 数、纵向柱 VERTICAL_BAR 各模型成本、大数字 NUMBER 的 p95 延迟、透视表 PIVOT_TABLE 的高频用户；每个 widget 都是查询引擎上的一条保存查询。widget 类型取自 DashboardService 的 chartType，值为示例">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：一个仪表盘（4 个 widget）</text>
  <rect x="18" y="28" width="684" height="26" rx="7" fill="var(--panel-2)" stroke="var(--line)"/>
  <rect x="28" y="34" width="92" height="14" rx="7" fill="var(--accent)" opacity="0.16"/><text x="74" y="44" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent)">📅 last 30 days</text>
  <rect x="127.60000000000001" y="34" width="102" height="14" rx="7" fill="var(--blue)" opacity="0.16"/><text x="179" y="44" text-anchor="middle" font-size="7" font-weight="700" fill="var(--blue)">env = production</text>
  <rect x="238.0" y="34" width="65" height="14" rx="7" fill="var(--purple)" opacity="0.16"/><text x="270" y="44" text-anchor="middle" font-size="7" font-weight="700" fill="var(--purple)">model = *</text>
  <text x="694" y="44" text-anchor="end" font-size="7" fill="var(--muted)">＋ 添加 widget</text>
  <rect x="18" y="62" width="335" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="30" y="80" font-size="8.5" font-weight="700" fill="var(--ink)">traces / day</text>
  <rect x="249" y="69" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="297" y="79" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">LINE_TIME_SERIES</text>
  <line x1="38" y1="190" x2="340" y2="190" stroke="var(--line)"/>
  <polyline points="40,180 82,168 124,172 166,150 208,140 250,120 292,108 334,92" fill="none" stroke="var(--accent)" stroke-width="2"/>
  <circle cx="40" cy="180" r="2.2" fill="var(--accent)"/>
  <circle cx="82" cy="168" r="2.2" fill="var(--accent)"/>
  <circle cx="124" cy="172" r="2.2" fill="var(--accent)"/>
  <circle cx="166" cy="150" r="2.2" fill="var(--accent)"/>
  <circle cx="208" cy="140" r="2.2" fill="var(--accent)"/>
  <circle cx="250" cy="120" r="2.2" fill="var(--accent)"/>
  <circle cx="292" cy="108" r="2.2" fill="var(--accent)"/>
  <circle cx="334" cy="92" r="2.2" fill="var(--accent)"/>
  <text x="40" y="200" font-size="6.4" fill="var(--faint)">Jun 1</text><text x="318" y="200" font-size="6.4" fill="var(--faint)">Jun 30</text>
  <rect x="366" y="62" width="336" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="378" y="80" font-size="8.5" font-weight="700" fill="var(--ink)">各模型成本 (USD)</text>
  <rect x="598" y="69" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="646" y="79" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">VERTICAL_BAR</text>
  <rect x="392" y="120" width="44" height="70" rx="4" fill="var(--accent)" opacity="0.7"/><text x="414" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">gpt-4o</text><text x="414" y="116" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--accent)">$126</text>
  <rect x="460" y="166" width="44" height="24" rx="4" fill="var(--blue)" opacity="0.7"/><text x="482" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">4o-mini</text><text x="482" y="162" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--blue)">$43</text>
  <rect x="528" y="138" width="44" height="52" rx="4" fill="var(--purple)" opacity="0.7"/><text x="550" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">claude</text><text x="550" y="134" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--purple)">$94</text>
  <rect x="596" y="176" width="44" height="14" rx="4" fill="var(--amber)" opacity="0.7"/><text x="618" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">llama</text><text x="618" y="172" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--amber)">$25</text>
  <rect x="18" y="206" width="335" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="30" y="224" font-size="8.5" font-weight="700" fill="var(--ink)">p95 延迟</text>
  <rect x="249" y="213" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="297" y="223" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">NUMBER</text>
  <text x="60" y="290" font-size="46" font-weight="800" fill="var(--accent-ink)">1.8<tspan font-size="20"> s</tspan></text>
  <rect x="60" y="300" width="120" height="16" rx="8" fill="var(--accent-soft)"/><text x="120" y="312" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent)">▼ 12% 对比上周</text>
  <polyline points="210,318 232,312 254,316 276,300 298,304 320,290 340,286" fill="none" stroke="var(--blue)" stroke-width="1.6"/>
  <rect x="366" y="206" width="336" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="378" y="224" font-size="8.5" font-weight="700" fill="var(--ink)">高频用户</text>
  <rect x="598" y="213" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="646" y="223" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">PIVOT_TABLE</text>
  <rect x="380" y="232" width="308" height="16" fill="var(--panel-2)"/>
  <text x="388" y="244" font-size="6.8" font-weight="700" fill="var(--ink)">userId</text>
  <text x="560" y="244" font-size="6.8" font-weight="700" fill="var(--ink)">traces</text>
  <text x="636" y="244" font-size="6.8" font-weight="700" fill="var(--ink)">cost</text>
  <rect x="380" y="248" width="308" height="20" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/><text x="388" y="261" font-size="7" font-family="monospace" fill="var(--ink)">u_8f3a</text><text x="560" y="261" font-size="7" fill="var(--muted)">1820</text><text x="636" y="261" font-size="7" fill="var(--accent-ink)">$58</text>
  <rect x="380" y="268" width="308" height="20" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/><text x="388" y="281" font-size="7" font-family="monospace" fill="var(--ink)">u_2b71</text><text x="560" y="281" font-size="7" fill="var(--muted)">1340</text><text x="636" y="281" font-size="7" fill="var(--accent-ink)">$41</text>
  <rect x="380" y="288" width="308" height="20" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/><text x="388" y="301" font-size="7" font-family="monospace" fill="var(--ink)">u_55c9</text><text x="560" y="301" font-size="7" fill="var(--muted)">980</text><text x="636" y="301" font-size="7" fill="var(--accent-ink)">$33</text>
  <text x="360" y="358" text-anchor="middle" font-size="7.4" fill="var(--muted)">每个 widget = 查询引擎上的一条保存查询（view + metrics + dimensions），第 41 课细讲</text>
</svg>
<div class="figcap"><b>一个仪表盘 = 一组 widget，每个 widget = 一条保存的查询</b>（widget 类型取自 <code>DashboardService</code> 的 <code>chartType</code>；<b>数据为示例</b>）：顶部筛选条作用于<b>全盘</b>，下面四块分别是 <code>LINE_TIME_SERIES</code>（每日 trace）、<code>VERTICAL_BAR</code>（各模型成本）、<code>NUMBER</code>（p95 延迟大数字）、<code>PIVOT_TABLE</code>（高频用户）。同一份指标，<b>选不同图型就有不同读法</b>——趋势看折线、构成看柱状、单点 KPI 看大数字、明细看透视表。这些 widget 背后都是第 41 课的查询引擎。</div>
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
  <rect x="265" y="130" width="190" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">监控器（第33课）</text><text x="360" y="167" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">定时比阈值（push：它来喊）</text>
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
<div class="fig">
<svg viewBox="0 0 720 368" role="img" aria-label="Dashboard real example: a filter bar on top (time range, env=production, model filter), then a 2x2 of widgets — a LINE_TIME_SERIES of traces per day, a VERTICAL_BAR of cost by model, a NUMBER big-stat of p95 latency, and a PIVOT_TABLE of top users; each widget is one saved query on the query engine. Widget types from DashboardService chartType, values illustrative">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: one dashboard (4 widgets)</text>
  <rect x="18" y="28" width="684" height="26" rx="7" fill="var(--panel-2)" stroke="var(--line)"/>
  <rect x="28" y="34" width="92" height="14" rx="7" fill="var(--accent)" opacity="0.16"/><text x="74" y="44" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent)">📅 last 30 days</text>
  <rect x="127.60000000000001" y="34" width="102" height="14" rx="7" fill="var(--blue)" opacity="0.16"/><text x="179" y="44" text-anchor="middle" font-size="7" font-weight="700" fill="var(--blue)">env = production</text>
  <rect x="238.0" y="34" width="65" height="14" rx="7" fill="var(--purple)" opacity="0.16"/><text x="270" y="44" text-anchor="middle" font-size="7" font-weight="700" fill="var(--purple)">model = *</text>
  <text x="694" y="44" text-anchor="end" font-size="7" fill="var(--muted)">+ add widget</text>
  <rect x="18" y="62" width="335" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="30" y="80" font-size="8.5" font-weight="700" fill="var(--ink)">traces / day</text>
  <rect x="249" y="69" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="297" y="79" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">LINE_TIME_SERIES</text>
  <line x1="38" y1="190" x2="340" y2="190" stroke="var(--line)"/>
  <polyline points="40,180 82,168 124,172 166,150 208,140 250,120 292,108 334,92" fill="none" stroke="var(--accent)" stroke-width="2"/>
  <circle cx="40" cy="180" r="2.2" fill="var(--accent)"/>
  <circle cx="82" cy="168" r="2.2" fill="var(--accent)"/>
  <circle cx="124" cy="172" r="2.2" fill="var(--accent)"/>
  <circle cx="166" cy="150" r="2.2" fill="var(--accent)"/>
  <circle cx="208" cy="140" r="2.2" fill="var(--accent)"/>
  <circle cx="250" cy="120" r="2.2" fill="var(--accent)"/>
  <circle cx="292" cy="108" r="2.2" fill="var(--accent)"/>
  <circle cx="334" cy="92" r="2.2" fill="var(--accent)"/>
  <text x="40" y="200" font-size="6.4" fill="var(--faint)">Jun 1</text><text x="318" y="200" font-size="6.4" fill="var(--faint)">Jun 30</text>
  <rect x="366" y="62" width="336" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="378" y="80" font-size="8.5" font-weight="700" fill="var(--ink)">cost by model (USD)</text>
  <rect x="598" y="69" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="646" y="79" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">VERTICAL_BAR</text>
  <rect x="392" y="120" width="44" height="70" rx="4" fill="var(--accent)" opacity="0.7"/><text x="414" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">gpt-4o</text><text x="414" y="116" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--accent)">$126</text>
  <rect x="460" y="166" width="44" height="24" rx="4" fill="var(--blue)" opacity="0.7"/><text x="482" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">4o-mini</text><text x="482" y="162" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--blue)">$43</text>
  <rect x="528" y="138" width="44" height="52" rx="4" fill="var(--purple)" opacity="0.7"/><text x="550" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">claude</text><text x="550" y="134" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--purple)">$94</text>
  <rect x="596" y="176" width="44" height="14" rx="4" fill="var(--amber)" opacity="0.7"/><text x="618" y="200" text-anchor="middle" font-size="6.6" fill="var(--muted)">llama</text><text x="618" y="172" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--amber)">$25</text>
  <rect x="18" y="206" width="335" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="30" y="224" font-size="8.5" font-weight="700" fill="var(--ink)">p95 latency</text>
  <rect x="249" y="213" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="297" y="223" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">NUMBER</text>
  <text x="60" y="290" font-size="46" font-weight="800" fill="var(--accent-ink)">1.8<tspan font-size="20"> s</tspan></text>
  <rect x="60" y="300" width="120" height="16" rx="8" fill="var(--accent-soft)"/><text x="120" y="312" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent)">▼ 12% vs last wk</text>
  <polyline points="210,318 232,312 254,316 276,300 298,304 320,290 340,286" fill="none" stroke="var(--blue)" stroke-width="1.6"/>
  <rect x="366" y="206" width="336" height="138" rx="9" fill="var(--bg)" stroke="var(--line)"/>
  <text x="378" y="224" font-size="8.5" font-weight="700" fill="var(--ink)">top users</text>
  <rect x="598" y="213" width="96" height="14" rx="7" fill="var(--accent-soft)"/><text x="646" y="223" text-anchor="middle" font-size="6.4" font-weight="700" font-family="monospace" fill="var(--accent-ink)">PIVOT_TABLE</text>
  <rect x="380" y="232" width="308" height="16" fill="var(--panel-2)"/>
  <text x="388" y="244" font-size="6.8" font-weight="700" fill="var(--ink)">userId</text>
  <text x="560" y="244" font-size="6.8" font-weight="700" fill="var(--ink)">traces</text>
  <text x="636" y="244" font-size="6.8" font-weight="700" fill="var(--ink)">cost</text>
  <rect x="380" y="248" width="308" height="20" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/><text x="388" y="261" font-size="7" font-family="monospace" fill="var(--ink)">u_8f3a</text><text x="560" y="261" font-size="7" fill="var(--muted)">1820</text><text x="636" y="261" font-size="7" fill="var(--accent-ink)">$58</text>
  <rect x="380" y="268" width="308" height="20" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/><text x="388" y="281" font-size="7" font-family="monospace" fill="var(--ink)">u_2b71</text><text x="560" y="281" font-size="7" fill="var(--muted)">1340</text><text x="636" y="281" font-size="7" fill="var(--accent-ink)">$41</text>
  <rect x="380" y="288" width="308" height="20" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/><text x="388" y="301" font-size="7" font-family="monospace" fill="var(--ink)">u_55c9</text><text x="560" y="301" font-size="7" fill="var(--muted)">980</text><text x="636" y="301" font-size="7" fill="var(--accent-ink)">$33</text>
  <text x="360" y="358" text-anchor="middle" font-size="7.4" fill="var(--muted)">each widget = one saved query on the engine (view + metrics + dimensions), detailed in Lesson 41</text>
</svg>
<div class="figcap"><b>A dashboard = a set of widgets, each widget = one saved query</b> (widget types from <code>DashboardService</code>'s <code>chartType</code>; <b>data illustrative</b>): the filter bar on top applies to <b>the whole board</b>, and the four panels are <code>LINE_TIME_SERIES</code> (traces/day), <code>VERTICAL_BAR</code> (cost by model), <code>NUMBER</code> (p95 latency big-stat) and <code>PIVOT_TABLE</code> (top users). Same metrics, <b>different chart types read differently</b> — a line for trend, bars for composition, a big number for a single KPI, a pivot for detail. Every widget is backed by Lesson 41's query engine.</div>
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


# ══════════════════════════════════════════════════════════════════════
# L41 · 查询引擎 / The query engine
# ══════════════════════════════════════════════════════════════════════
_ZH41 = []
_EN41 = []

_ZH41.append(r"""
<p class="lead">
上一课的 widget 声明了 <code>view + dimensions + metrics + filters</code>。但 ClickHouse 只懂 <strong>SQL</strong>，根本不认识这些声明。中间那座桥，就是<strong>查询引擎（query engine）</strong>——它把这套声明<strong>编译成 SQL</strong>，跑出数据。这一课拆开它，看清两个核心部件：一个<strong>语义层</strong>（data model，把「成本」「按模型」这样的友好逻辑名，映射到真实的 ClickHouse 列与表达式），和一个<strong>编译器</strong>（<code>QueryBuilder.build()</code>，把声明拼装成<strong>参数化</strong>的 SQL）。
理解了它，你就明白第 40 课仪表盘、第 33 课监控、第 35 课实验聚合<strong>为何能共用一份查询形状</strong>——因为它们背后都是这同一台编译器；也会再次见到第 23 课「参数化防注入」的纪律，在聚合查询里如何贯彻。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  查询引擎像餐厅里的<strong>「翻译官 + 一本菜单」</strong>。你（widget）用<strong>人话点菜</strong>：「按模型分组、统计总成本，只看 production 的」。翻译官（<code>QueryBuilder</code>）翻开一本<strong>菜单</strong>（data model）——菜单上每道「逻辑菜名」都标注着<strong>后厨用的真实食材和做法</strong>（「总成本」=后厨表里的 <code>sum(total_cost)</code> 列、「按模型」=按 <code>provided_model_name</code> 分组）。
  翻译官照着菜单，把你的人话<strong>精确翻译成后厨（ClickHouse）能执行的工单</strong>（SQL）。妙处有二：其一，你<strong>永远不用知道</strong>后厨的食材叫什么、放在哪个冷柜——菜单这层把你和后厨的<strong>物理细节</strong>隔开了，后厨改了食材摆放（换列名、改表结构），只要菜单跟着更新，你的点法<strong>一字不用改</strong>。其二，凡是你填的「具体值」（如 <code>production</code>），翻译官都<strong>另用一张小纸条夹着递进去</strong>（参数化），绝不直接写进工单正文——这样哪怕你写个奇怪的店名，也绝<strong>串改不了工单本身</strong>（防 SQL 注入，第 23 课）。
</div>
""")

# (L41 sections below)

_ZH41.append(r"""
<h2>语义层：把逻辑名翻译成真实 SQL</h2>
<p>引擎的第一个部件是 <strong>data model（数据模型 / 语义层）</strong>。它为每个 <code>view</code>（traces / observations / scores-numeric / scores-categorical）声明一份「字典」：这个视图有哪些 <strong>dimensions（维度，可分组的字段）</strong>、哪些 <strong>measures（度量，可聚合的量）</strong>，以及它们各自对应<strong>哪一段真实的 ClickHouse SQL</strong>。比如维度 <code>name</code> 对应 <code>traces.name</code>、时间维度对应一段 <code>formatDateTime(...)</code>。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="语义层：widget 用逻辑名 view/dimensions/metrics，data model 把每个逻辑名映射到真实 ClickHouse 列或表达式，比如维度 name 映射 traces.name、度量 count 映射 count() 聚合、时间映射 formatDateTime">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">data model：逻辑名 ↔ 真实 SQL 的字典</text>
  <rect x="30" y="44" width="180" height="140" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="120" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">你说的（逻辑名）</text><rect x="46" y="76" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="120" y="92" text-anchor="middle" font-size="7" fill="var(--ink)">view: traces</text><rect x="46" y="106" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="120" y="122" text-anchor="middle" font-size="7" fill="var(--ink)">dimension: name</text><rect x="46" y="136" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="120" y="152" text-anchor="middle" font-size="7" fill="var(--ink)">metric: count</text><text x="120" y="176" text-anchor="middle" font-size="6.5" fill="var(--muted)">友好、稳定、与物理解耦</text>
  <rect x="270" y="64" width="180" height="100" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="86" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">data model（字典）</text><text x="360" y="105" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">每个逻辑名 →</text><text x="360" y="119" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">{ sql, alias }</text><text x="360" y="138" text-anchor="middle" font-size="6.5" fill="var(--muted)">还声明可分组维度、可聚合度量</text><text x="360" y="152" text-anchor="middle" font-size="6.5" fill="var(--muted)">支持 v1/v2 版本</text>
  <rect x="510" y="44" width="180" height="140" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">后厨懂的（真实 SQL）</text><rect x="526" y="76" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="92" text-anchor="middle" font-size="6.6" fill="var(--ink)">FROM traces …</text><rect x="526" y="106" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="122" text-anchor="middle" font-size="6.6" fill="var(--ink)">traces.name</text><rect x="526" y="136" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="152" text-anchor="middle" font-size="6.6" fill="var(--ink)">count(*)</text><text x="600" y="176" text-anchor="middle" font-size="6.5" fill="var(--muted)">物理列名、可演化</text>
  <line x1="210" y1="114" x2="268" y2="114" stroke="var(--accent)" stroke-width="1.5"/><polygon points="268,114 259,110 259,118" fill="var(--accent)"/>
  <line x1="450" y1="114" x2="508" y2="114" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,114 499,110 499,118" fill="var(--teal)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">语义层把「你说的」和「后厨懂的」隔开：物理列改了名，只动字典，所有 widget/监控/API 的查询照常</text>
</svg>
<div class="figcap"><b>语义层 = 一本逻辑名↔SQL 的字典</b>：<code>dataModel.ts</code> 为每个 view 声明 <code>dimensions</code> 与 <code>measures</code>，每项形如 <code>{ sql: "traces.name", alias: "name" }</code>（维度），时间维度甚至是 <code>formatDateTime(traces.timestamp, …)</code> 这样的表达式。源码：<code>packages/shared/src/features/query/dataModel.ts:10-70</code>、<code>types.ts:9</code>（viewDeclaration）。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 288" role="img" aria-label="查询引擎真实例子：左边是仪表盘提交的查询规格 JSON（view=observations、metrics 是 measure+aggregation 对象、dimensions 是 field 对象、timeDimension 的 granularity=day、filters），右边是 queryBuilder 编译出的 ClickHouse SQL（select provided_model_name、count()、sum(total_cost)、toStartOfDay(start_time)，from observations FINAL，where 带 project_id 与时间范围占位符，group by 维度与天）。规格形状取自 features/query/types.ts，列名取自 observations 迁移，值为示例">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：查询规格 → 编译出的 ClickHouse SQL</text>
  <rect x="16" y="30" width="340" height="248" rx="9" fill="var(--code-bg)" stroke="var(--blue)"/>
  <text x="30" y="46" font-size="8" font-weight="700" fill="var(--blue)">query spec (JSON) · 仪表盘提交</text>
  <text x="30" y="62" font-size="6.7" font-family="monospace" fill="var(--code-ink)">{</text>
  <text x="30" y="77.4" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  view: &quot;observations&quot;,</text>
  <text x="30" y="92.80000000000001" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  metrics: [</text>
  <text x="30" y="108.20000000000002" font-size="6.7" font-family="monospace" fill="var(--code-ink)">    { measure:&quot;count&quot;, aggregation:&quot;count&quot; },</text>
  <text x="30" y="123.60000000000002" font-size="6.7" font-family="monospace" fill="var(--code-ink)">    { measure:&quot;totalCost&quot;, aggregation:&quot;sum&quot; }</text>
  <text x="30" y="139.00000000000003" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  ],</text>
  <text x="30" y="154.40000000000003" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  dimensions: [{ field:&quot;providedModelName&quot; }],</text>
  <text x="30" y="169.80000000000004" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  timeDimension: { granularity:&quot;day&quot; },</text>
  <text x="30" y="185.20000000000005" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  filters: [{ column:&quot;environment&quot;,</text>
  <text x="30" y="200.60000000000005" font-size="6.7" font-family="monospace" fill="var(--code-ink)">    operator:&quot;=&quot;, value:&quot;production&quot; }],</text>
  <text x="30" y="216.00000000000006" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  fromTimestamp:&quot;2026-06-01…&quot;,</text>
  <text x="30" y="231.40000000000006" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  toTimestamp:&quot;2026-06-30…&quot;</text>
  <text x="30" y="246.80000000000007" font-size="6.7" font-family="monospace" fill="var(--code-ink)">}</text>
  <text x="360" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">queryBuilder</text>
  <path d="M357 158 L363 158 L363 164 L357 164 L363 161 Z" fill="var(--accent)"/><line x1="357" y1="155" x2="357" y2="167" stroke="var(--accent)" stroke-width="2"/><polygon points="362,161 354,156 354,166" fill="var(--accent)"/>
  <rect x="372" y="30" width="332" height="248" rx="9" fill="var(--code-bg)" stroke="var(--accent)"/>
  <text x="386" y="46" font-size="8" font-weight="700" fill="var(--accent-ink)">compiled ClickHouse SQL</text>
  <text x="386" y="62" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">SELECT</text>
  <text x="386" y="77.4" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  provided_model_name,</text>
  <text x="386" y="92.80000000000001" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  count() AS count,</text>
  <text x="386" y="108.20000000000002" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  sum(total_cost) AS sum_totalCost,</text>
  <text x="386" y="123.60000000000002" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  toStartOfDay(start_time) AS day</text>
  <text x="386" y="139.00000000000003" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">FROM observations FINAL</text>
  <text x="386" y="154.40000000000003" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">WHERE project_id = {projectId}</text>
  <text x="386" y="169.80000000000004" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--code-ink)">  AND environment = 'production'</text>
  <text x="386" y="185.20000000000005" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--code-ink)">  AND start_time &gt;= {from}</text>
  <text x="386" y="200.60000000000005" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--code-ink)">  AND start_time &lt;  {to}</text>
  <text x="386" y="216.00000000000006" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">GROUP BY provided_model_name, day</text>
  <text x="386" y="231.40000000000006" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">ORDER BY day</text>
  <text x="360" y="276" text-anchor="middle" font-size="6.6" fill="var(--faint)">参数化占位符（{projectId}/{from}/{to}）杜绝 SQL 注入</text>
</svg>
<div class="figcap"><b>一份声明式规格，引擎替你写 SQL</b>（规格形状取自 <code>features/query/types.ts</code>，列名取自 <code>observations</code> 迁移；<b>值为示例</b>）：你只描述<b>要什么</b>——<code>view</code> 选表、<code>metrics</code> 是 <code>{measure, aggregation}</code>、<code>dimensions</code> 是 <code>{field}</code>、<code>timeDimension.granularity</code> 定时间桶；<code>queryBuilder</code> 把它编译成真正的 ClickHouse SQL：度量变 <code>count()</code>/<code>sum(total_cost)</code>、维度进 <code>GROUP BY</code>、时间桶变 <code>toStartOfDay(start_time)</code>。所有用户值都走<b>参数化占位符</b>，从根上挡住 SQL 注入。换个 <code>view</code> 就查另一张表——同一套规格语言覆盖全部图表。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/features/query/dataModel.ts</span><span class="ln">一个 view 的声明</span></div>
  <pre class="code"><span class="cm">// 每个 view 声明：有哪些维度/度量，各自对应哪段真实 SQL</span>
{
  name: <span class="st">"traces"</span>,
  dimensions: {
    name:        { sql: <span class="st">"traces.name"</span>,      alias: <span class="st">"name"</span> },        <span class="cm">// 逻辑名 → 物理列</span>
    environment: { sql: <span class="st">"traces.environment"</span>, alias: <span class="st">"environment"</span> },
    timestampMonth: { sql: <span class="st">"formatDateTime(traces.timestamp, '%Y-%m')"</span>, … },  <span class="cm">// 可是表达式</span>
  },
  measures: { count: { … }, totalCost: { sql: <span class="st">"sum(total_cost)"</span>, … }, … },   <span class="cm">// 可聚合的量</span>
}
<span class="cm">// widget 只引用 "name"/"totalCost" 这些逻辑名，永不直接碰物理列</span></pre>
</div>

<table class="t">
  <thead><tr><th>view（数据源）</th><th>聚合的对象</th><th>典型维度 / 度量</th></tr></thead>
  <tbody>
    <tr><td><code>traces</code></td><td>整条 trace</td><td>维度：name、environment、userId；度量：count、总成本</td></tr>
    <tr><td><code>observations</code></td><td>单步观测（含 generation）</td><td>维度：model、type；度量：count、token 数、成本、延迟</td></tr>
    <tr><td><code>scores-numeric</code></td><td>数值分</td><td>维度：name、source；度量：avg(value)、count</td></tr>
    <tr><td><code>scores-categorical</code></td><td>分类分</td><td>维度：name、stringValue；度量：count、各类占比</td></tr>
  </tbody>
</table>
<p>四个 view 各对应一类核心数据（呼应第 8、13、28 课的领域模型）。一个 widget 选定一个 view，再从它声明好的维度/度量里挑要分组、要算的——<strong>能问什么，由 view 的字典划定边界</strong>，既好用又防越界。</p>
""")

_ZH41.append(r"""
<h2>编译器：把声明拼成参数化 SQL</h2>
<p>第二个部件是 <code>QueryBuilder.build()</code>——真正的<strong>编译器</strong>。它拿到一个声明式的 <code>QueryType</code>，对照 data model，分几步把它拼成完整 SQL：<strong>维度</strong>翻译成 <code>SELECT … GROUP BY</code> 的列（<code>mapDimensions</code>）、<strong>度量</strong>翻译成 <code>count()/sum()/avg()</code> 等聚合（<code>mapMetrics</code> + <code>translateAggregation</code>）、<strong>时间</strong>按粒度分桶（<code>applyBucketingDimension</code>，做时序图）、<strong>过滤</strong>翻译成 <code>WHERE</code>，必要时<strong>连表</strong>（<code>buildJoins</code>）。</p>

<div class="fig">
<svg viewBox="0 0 720 225" role="img" aria-label="QueryBuilder.build 编译流程：声明式 QueryType 进入，依次经 mapDimensions 生成 GROUP BY 列、mapMetrics 生成聚合、applyBucketingDimension 做时间分桶、mapFilters 生成参数化 WHERE、buildJoins 连表，产出 SQL 加参数交给 queryExecutor 跑 ClickHouse">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">QueryBuilder.build()：声明 → 参数化 SQL</text>
  <rect x="20" y="50" width="120" height="120" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="70" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">QueryType（声明）</text><text x="80" y="88" text-anchor="middle" font-size="6.4" fill="var(--muted)">view</text><text x="80" y="102" text-anchor="middle" font-size="6.4" fill="var(--muted)">dimensions</text><text x="80" y="116" text-anchor="middle" font-size="6.4" fill="var(--muted)">metrics</text><text x="80" y="130" text-anchor="middle" font-size="6.4" fill="var(--muted)">filters</text><text x="80" y="144" text-anchor="middle" font-size="6.4" fill="var(--muted)">timeDimension</text>
  <rect x="180" y="44" width="160" height="132" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="260" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">QueryBuilder.build()</text><text x="260" y="82" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">mapDimensions → GROUP BY</text><text x="260" y="98" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">mapMetrics → count/sum/avg</text><text x="260" y="114" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">applyBucketing → 时间分桶</text><text x="260" y="130" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">mapFilters → 参数化 WHERE</text><text x="260" y="146" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">buildJoins → 必要时连表</text><text x="260" y="164" text-anchor="middle" font-size="6.5" fill="var(--muted)">对照 data model 翻译每一项</text>
  <rect x="380" y="56" width="150" height="58" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="455" y="76" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">SQL（带 {占位符}）</text><text x="455" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">SELECT … GROUP BY …</text><text x="455" y="104" text-anchor="middle" font-size="6.2" fill="var(--muted)">WHERE env = {p1}</text>
  <rect x="380" y="124" width="150" height="44" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="455" y="142" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">parameters</text><text x="455" y="157" text-anchor="middle" font-size="6.2" fill="var(--muted)">{ p1: "production" }</text>
  <rect x="565" y="80" width="135" height="62" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="632" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">queryExecutor</text><text x="632" y="121" text-anchor="middle" font-size="6.5" fill="var(--muted)">把 SQL+参数发给 ClickHouse</text>
  <line x1="140" y1="110" x2="178" y2="110" stroke="var(--accent)" stroke-width="1.5"/><polygon points="178,110 169,106 169,114" fill="var(--accent)"/>
  <line x1="340" y1="92" x2="378" y2="86" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,86 369,85 371,93" fill="var(--accent)"/><line x1="340" y1="130" x2="378" y2="142" stroke="var(--teal)" stroke-width="1.4"/><polygon points="378,142 369,138 369,146" fill="var(--teal)"/>
  <line x1="530" y1="100" x2="563" y2="108" stroke="var(--teal)" stroke-width="1.4"/><polygon points="563,108 554,105 555,113" fill="var(--teal)"/><line x1="530" y1="146" x2="563" y2="120" stroke="var(--teal)" stroke-width="1.4"/><polygon points="563,120 554,121 558,128" fill="var(--teal)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">关键：用户填的具体值（production）永远走 parameters，不拼进 SQL 正文——参数化防注入（第23课）</text>
  <text x="360" y="214" text-anchor="middle" font-size="8" fill="var(--faint)">SQL 与值分离：模板可缓存/可审计，值随调用绑定，恶意输入串改不了结构</text>
</svg>
<div class="figcap"><b>编译器对照字典逐项翻译</b>：<code>queryBuilder.ts</code> 的 <code>build()</code> 串起 <code>mapDimensions</code>(:270) / <code>mapMetrics</code>+<code>translateAggregation</code>(:290,137) / <code>applyBucketingDimension</code>(:182) / <code>mapFilters</code>+<code>buildWhereClause</code>(:490,858)。过滤用 FilterList 的 <code>apply()</code> 产出 <b>SQL+参数</b>——用户值绑成参数，绝不拼进正文（第 23 课同款防注入）。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/features/query/server/queryBuilder.ts · queryExecutor.ts</span><span class="ln">声明 → SQL → 执行</span></div>
  <pre class="code"><span class="cm">// 1) 声明式查询（来自 widget / monitor / 实验聚合，都是这个形状）</span>
<span class="kw">const</span> query = { view: <span class="st">"observations"</span>, dimensions: [{ field: <span class="st">"model"</span> }],
  metrics: [{ measure: <span class="st">"totalCost"</span>, aggregation: <span class="st">"sum"</span> }],
  filters: [{ column: <span class="st">"environment"</span>, operator: <span class="st">"="</span>, value: <span class="st">"production"</span> }] };

<span class="cm">// 2) 编译：对照 data model，拼成参数化 SQL（GROUP BY/聚合/WHERE/分桶/JOIN）</span>
<span class="kw">const</span> { sql, parameters } = <span class="kw">new</span> QueryBuilder(chartConfig, version).build(query, projectId);
<span class="cm">// sql:  SELECT model, sum(total_cost) … WHERE environment = {p_env} GROUP BY model</span>
<span class="cm">// parameters: { p_env: "production" }   ← 值走参数，不拼进 SQL</span>

<span class="cm">// 3) 执行：queryExecutor 把 sql+parameters 发给 ClickHouse</span></pre>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>取 view 字典</h4><p><code>getViewDeclaration(view, version)</code> 按版本拿到该 view 的维度/度量字典——后续每一步都对照它翻译。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>维度 → GROUP BY</h4><p><code>mapDimensions</code> 把每个逻辑维度译成 SELECT 列和 GROUP BY；时间维度交给 <code>applyBucketingDimension</code> 按粒度分桶。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>度量 → 聚合</h4><p><code>mapMetrics</code> + <code>translateAggregation</code> 把度量译成 count()/sum()/avg() 等聚合函数。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>过滤 → 参数化 WHERE</h4><p><code>mapFilters</code> + <code>buildWhereClause</code> 用 FilterList.apply 产出 WHERE，用户值绑成 parameters。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>连表 + 出 SQL</h4><p>需要跨表时 <code>buildJoins</code> 补 JOIN；最终拼出 <code>{ sql, parameters }</code>，交 <code>queryExecutor</code> 跑 ClickHouse。</p></div></div>
</div>
""")

_ZH41.append(r"""
<h2>为什么值得造这台引擎</h2>
<p>把声明编译成 SQL，本可以让每个 widget 自己拼字符串。但 Langfuse 偏要造一台统一引擎，因为它一次解决了四个问题：</p>

<svg viewBox="0 0 720 230" role="img" aria-label="查询引擎是一个小型指标语言的编译器：上层用 view、dimensions、metrics、filters 声明式描述要什么指标（与物理无关、注入安全），引擎内部四件事语义层逻辑名换 SQL、参数化防注入、视图版本化 v1/v2、一引擎多消费，向下编译成参数化 ClickHouse SQL，仪表盘 L40、监控 L33、实验聚合共用它所以同一指标永远算出同一个数">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="24" y="36" width="420" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="234" y="56" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">① 上层声明（声明式 · 与物理无关 · 注入安全）</text>
  <text x="234" y="72" font-size="9.5" text-anchor="middle" fill="var(--muted)">view + dimensions + metrics + filters</text>
  <line x1="234" y1="80" x2="234" y2="92" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="24" y="92" width="420" height="86" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="234" y="110" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">② 查询引擎 = 指标语言的编译器</text>
  <rect x="36" y="118" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="132" y="135" font-size="9" text-anchor="middle" fill="var(--ink)">语义层：逻辑名 ↔ SQL（解耦）</text>
  <rect x="240" y="118" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="336" y="135" font-size="9" text-anchor="middle" fill="var(--ink)">参数化：值走 parameters（防注入）</text>
  <rect x="36" y="148" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="132" y="165" font-size="9" text-anchor="middle" fill="var(--ink)">视图版本化：v1/v2（不破历史）</text>
  <rect x="240" y="148" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="336" y="165" font-size="9" text-anchor="middle" fill="var(--ink)">一引擎多消费（口径一致）</text>
  <line x1="234" y1="178" x2="234" y2="190" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="24" y="190" width="420" height="34" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="234" y="211" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">③ 参数化 SQL → ClickHouse 执行</text>
  <rect x="466" y="92" width="238" height="86" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="585" y="116" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">一引擎多消费</text>
  <text x="585" y="136" font-size="9.5" text-anchor="middle" fill="var(--muted)">仪表盘 L40 · 监控 L33</text>
  <text x="585" y="152" font-size="9.5" text-anchor="middle" fill="var(--muted)">· 实验聚合</text>
  <text x="585" y="170" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">→ 同一指标永远同一个数</text>
  <line x1="444" y1="135" x2="466" y2="135" stroke="var(--teal)" stroke-width="2"></line>
</svg>

<table class="t">
  <thead><tr><th>设计</th><th>解决什么</th><th>呼应</th></tr></thead>
  <tbody>
    <tr><td><b>语义层</b>（逻辑名↔SQL）</td><td>物理列改名/换表，只改字典，所有查询不动；用户也无需懂物理 schema</td><td>解耦「想要什么」与「怎么存」</td></tr>
    <tr><td><b>参数化</b>（值走 parameters）</td><td>用户值绝不拼进 SQL 正文，根除 SQL 注入</td><td>第 23 课 FilterState 同款</td></tr>
    <tr><td><b>视图版本化</b>（v1/v2）</td><td>物理 schema 演进时，老查询仍按老视图编译，不破坏历史</td><td>第 34/37 课「不可变 + 演进」</td></tr>
    <tr><td><b>一引擎多消费</b></td><td>仪表盘/监控/实验聚合共用，指标口径全局一致</td><td>第 40 课「一份查询形状三处复用」</td></tr>
  </tbody>
</table>

<p>把这四点连起来看，查询引擎其实是一个<strong>小型「指标语言 + 编译器」</strong>：上层用一种<strong>声明式、与物理无关、注入安全</strong>的小语言描述「我要什么指标」，引擎负责把它<strong>正确、一致、安全</strong>地落成 ClickHouse 能跑的 SQL。这和第 23 课把 FilterState 编译成过滤 SQL 是同一种思路，只是从「过滤」升级到了完整的「聚合查询」。<strong>声明在上、编译在下，物理细节被牢牢封在引擎里</strong>——这正是 Langfuse 能让仪表盘、监控、API 对同一指标永远算出同一个数的底层原因。</p>
""")

_ZH41.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么要造一个语义层，而不让 widget 直接写 SQL？</strong> 直接写 SQL 看似省事，实则埋三颗雷。其一是<strong>耦合</strong>：每个 widget 都硬编码物理列名，哪天 ClickHouse 改了表结构、换了列名，成百上千张 widget 一起崩，得逐个改。语义层把「逻辑名→物理 SQL」收进一本字典，物理一变只改字典，上层岿然不动。其二是<strong>安全</strong>：让每个 widget 自己拼 SQL，就等于把防注入的责任摊给每个写 widget 的人——总有人会忘、会拼错，一个口子就是一次数据泄露。统一引擎把参数化焊死在唯一出口，<strong>注入安全靠结构兜底</strong>，不靠自觉。其三是<strong>一致</strong>：散落各处的 SQL 迟早对同一指标算出不同数。把指标定义收进语义层，全公司一种算法。<strong>一台引擎，同时买下解耦、安全、一致三件大事</strong>——这就是为什么值得为它多写这几千行。<br><br>
  <strong>为什么 view 要带 v1/v2 版本？</strong> 因为<strong>物理 schema 会演进，但历史查询不该因此失效</strong>。ClickHouse 表会重构、列会拆分合并、为性能引入新的物化视图——这些都是底层的正常演化。如果查询直接绑死当前物理结构，那每次底层一动，所有保存好的 widget、monitor、API 查询都可能算错或报错。给 view 引入版本，等于让「语义」也有了不可变的快照：一个 v1 的查询永远按 v1 的字典编译，哪怕底层早已迁到 v2 的新表。这和第 34 课数据项版本、第 37 课 prompt 版本是<strong>同一种信念在查询层的回响</strong>——<strong>底层可以大胆演进，因为上层被一层稳定的版本化语义保护着</strong>。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>查询引擎 = 声明式查询 → SQL 的编译器</strong>：widget 的 <code>view+dimensions+metrics+filters</code> 声明，由它编译成 ClickHouse SQL 并执行，是第 40 课仪表盘背后的发动机。</li>
    <li><strong>语义层（data model）</strong>：为每个 view 声明 <code>dimensions</code>/<code>measures</code>，每项把逻辑名映射到真实 SQL（如 <code>name</code>→<code>traces.name</code>、时间→<code>formatDateTime(...)</code>）——上层永不直接碰物理列。</li>
    <li><strong>编译器（QueryBuilder.build）</strong>：对照字典把维度译成 GROUP BY、度量译成聚合、时间分桶、过滤译成 WHERE、必要时连表，产出 <strong>SQL + 参数</strong>。</li>
    <li><strong>参数化防注入</strong>：用户填的值绑成 parameters、绝不拼进 SQL 正文——第 23 课 FilterState 的纪律在聚合查询里同样贯彻，注入安全靠结构兜底。</li>
    <li><strong>一引擎四收益</strong>：语义层解耦物理、参数化保安全、视图 v1/v2 版本化护历史、一引擎多消费保口径一致——仪表盘/监控/实验对同一指标永远同一个数。</li>
  </ul>
</div>
""")

_EN41.append(r"""
<p class="lead">
The last lesson's widget declared <code>view + dimensions + metrics + filters</code>. But ClickHouse only understands <strong>SQL</strong>—it knows nothing of these declarations. The bridge between them is the <strong>query engine</strong>—it <strong>compiles</strong> that declaration <strong>into SQL</strong> and runs it. This lesson takes it apart, revealing two core parts: a <strong>semantic layer</strong> (the data model, mapping friendly logical names like "cost" and "by model" to real ClickHouse columns and expressions), and a <strong>compiler</strong> (<code>QueryBuilder.build()</code>, assembling the declaration into <strong>parameterized</strong> SQL).
Understanding it explains why Lesson 40's dashboards, Lesson 33's monitors, and Lesson 35's experiment aggregation <strong>can share one query shape</strong>—because they're all backed by this same compiler; you'll also see again how Lesson 23's "parameterized = injection-safe" discipline carries into aggregation queries.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  The query engine is like a restaurant's <strong>"interpreter + a menu"</strong>. You (the widget) <strong>order in plain words</strong>: "group by model, total the cost, only production". The interpreter (<code>QueryBuilder</code>) opens a <strong>menu</strong> (the data model)—where each "logical dish name" is annotated with <strong>the real ingredients and methods the kitchen uses</strong> ("total cost" = the kitchen table's <code>sum(total_cost)</code> column, "by model" = group by <code>provided_model_name</code>).
  Following the menu, the interpreter <strong>precisely translates your plain words into a work ticket the kitchen (ClickHouse) can execute</strong> (SQL). Two beauties: one, you <strong>never need to know</strong> what the kitchen's ingredients are called or which fridge they're in—this menu layer isolates you from the kitchen's <strong>physical details</strong>; if the kitchen rearranges ingredients (renames columns, restructures tables), as long as the menu updates, your ordering style <strong>doesn't change one word</strong>. Two, any "concrete value" you fill in (like <code>production</code>) the interpreter <strong>passes in on a separate slip</strong> (parameterized), never written into the ticket body—so even a weird store name <strong>can't alter the ticket itself</strong> (SQL injection prevention, Lesson 23).
</div>
""")

_EN41.append(r"""
<h2>The semantic layer: translate logical names into real SQL</h2>
<p>The engine's first part is the <strong>data model (semantic layer)</strong>. For each <code>view</code> (traces / observations / scores-numeric / scores-categorical) it declares a "dictionary": which <strong>dimensions (groupable fields)</strong> and <strong>measures (aggregatable quantities)</strong> this view has, and <strong>which real ClickHouse SQL</strong> each maps to. For example, the dimension <code>name</code> maps to <code>traces.name</code>, and the time dimension to a <code>formatDateTime(...)</code> expression.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="Semantic layer: the widget uses logical names view/dimensions/metrics, the data model maps each logical name to a real ClickHouse column or expression, e.g. dimension name maps to traces.name, measure count maps to a count() aggregation, time maps to formatDateTime">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">data model: a dictionary of logical name ↔ real SQL</text>
  <rect x="30" y="44" width="180" height="140" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="120" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">what you say (logical)</text><rect x="46" y="76" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="120" y="92" text-anchor="middle" font-size="7" fill="var(--ink)">view: traces</text><rect x="46" y="106" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="120" y="122" text-anchor="middle" font-size="7" fill="var(--ink)">dimension: name</text><rect x="46" y="136" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="120" y="152" text-anchor="middle" font-size="7" fill="var(--ink)">metric: count</text><text x="120" y="176" text-anchor="middle" font-size="6.2" fill="var(--muted)">friendly, stable, physical-decoupled</text>
  <rect x="270" y="64" width="180" height="100" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="86" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">data model (dictionary)</text><text x="360" y="105" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">each logical name →</text><text x="360" y="119" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">{ sql, alias }</text><text x="360" y="138" text-anchor="middle" font-size="6.2" fill="var(--muted)">declares groupable dims, aggregatable measures</text><text x="360" y="152" text-anchor="middle" font-size="6.4" fill="var(--muted)">supports v1/v2 versions</text>
  <rect x="510" y="44" width="180" height="140" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">what the kitchen knows (real SQL)</text><rect x="526" y="76" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="92" text-anchor="middle" font-size="6.6" fill="var(--ink)">FROM traces …</text><rect x="526" y="106" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="122" text-anchor="middle" font-size="6.6" fill="var(--ink)">traces.name</text><rect x="526" y="136" width="148" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="152" text-anchor="middle" font-size="6.6" fill="var(--ink)">count(*)</text><text x="600" y="176" text-anchor="middle" font-size="6.2" fill="var(--muted)">physical column names, evolvable</text>
  <line x1="210" y1="114" x2="268" y2="114" stroke="var(--accent)" stroke-width="1.5"/><polygon points="268,114 259,110 259,118" fill="var(--accent)"/>
  <line x1="450" y1="114" x2="508" y2="114" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,114 499,110 499,118" fill="var(--teal)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">the semantic layer isolates "what you say" from "what the kitchen knows": rename a physical column, only the dictionary changes, all widget/monitor/API queries go on</text>
</svg>
<div class="figcap"><b>semantic layer = a dictionary of logical name↔SQL</b>: <code>dataModel.ts</code> declares <code>dimensions</code> and <code>measures</code> per view, each shaped like <code>{ sql: "traces.name", alias: "name" }</code> (a dimension); a time dimension can even be an expression like <code>formatDateTime(traces.timestamp, …)</code>. Source: <code>packages/shared/src/features/query/dataModel.ts:10-70</code>, <code>types.ts:9</code> (viewDeclaration).</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 288" role="img" aria-label="Query-engine real example: left is the query spec JSON a dashboard submits (view=observations, metrics are measure+aggregation objects, dimensions are field objects, timeDimension granularity=day, filters); right is the ClickHouse SQL the queryBuilder compiles (select provided_model_name, count(), sum(total_cost), toStartOfDay(start_time), from observations FINAL, where with project_id and time-range placeholders, group by dimension and day). Spec shape from features/query/types.ts, column names from the observations migration, values illustrative">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: a query spec → compiled ClickHouse SQL</text>
  <rect x="16" y="30" width="340" height="248" rx="9" fill="var(--code-bg)" stroke="var(--blue)"/>
  <text x="30" y="46" font-size="8" font-weight="700" fill="var(--blue)">query spec (JSON) · dashboard submits</text>
  <text x="30" y="62" font-size="6.7" font-family="monospace" fill="var(--code-ink)">{</text>
  <text x="30" y="77.4" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  view: &quot;observations&quot;,</text>
  <text x="30" y="92.80000000000001" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  metrics: [</text>
  <text x="30" y="108.20000000000002" font-size="6.7" font-family="monospace" fill="var(--code-ink)">    { measure:&quot;count&quot;, aggregation:&quot;count&quot; },</text>
  <text x="30" y="123.60000000000002" font-size="6.7" font-family="monospace" fill="var(--code-ink)">    { measure:&quot;totalCost&quot;, aggregation:&quot;sum&quot; }</text>
  <text x="30" y="139.00000000000003" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  ],</text>
  <text x="30" y="154.40000000000003" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  dimensions: [{ field:&quot;providedModelName&quot; }],</text>
  <text x="30" y="169.80000000000004" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  timeDimension: { granularity:&quot;day&quot; },</text>
  <text x="30" y="185.20000000000005" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  filters: [{ column:&quot;environment&quot;,</text>
  <text x="30" y="200.60000000000005" font-size="6.7" font-family="monospace" fill="var(--code-ink)">    operator:&quot;=&quot;, value:&quot;production&quot; }],</text>
  <text x="30" y="216.00000000000006" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  fromTimestamp:&quot;2026-06-01…&quot;,</text>
  <text x="30" y="231.40000000000006" font-size="6.7" font-family="monospace" fill="var(--code-ink)">  toTimestamp:&quot;2026-06-30…&quot;</text>
  <text x="30" y="246.80000000000007" font-size="6.7" font-family="monospace" fill="var(--code-ink)">}</text>
  <text x="360" y="150" text-anchor="middle" font-size="7" fill="var(--muted)">queryBuilder</text>
  <path d="M357 158 L363 158 L363 164 L357 164 L363 161 Z" fill="var(--accent)"/><line x1="357" y1="155" x2="357" y2="167" stroke="var(--accent)" stroke-width="2"/><polygon points="362,161 354,156 354,166" fill="var(--accent)"/>
  <rect x="372" y="30" width="332" height="248" rx="9" fill="var(--code-bg)" stroke="var(--accent)"/>
  <text x="386" y="46" font-size="8" font-weight="700" fill="var(--accent-ink)">compiled ClickHouse SQL</text>
  <text x="386" y="62" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">SELECT</text>
  <text x="386" y="77.4" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  provided_model_name,</text>
  <text x="386" y="92.80000000000001" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  count() AS count,</text>
  <text x="386" y="108.20000000000002" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  sum(total_cost) AS sum_totalCost,</text>
  <text x="386" y="123.60000000000002" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--blue)">  toStartOfDay(start_time) AS day</text>
  <text x="386" y="139.00000000000003" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">FROM observations FINAL</text>
  <text x="386" y="154.40000000000003" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">WHERE project_id = {projectId}</text>
  <text x="386" y="169.80000000000004" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--code-ink)">  AND environment = 'production'</text>
  <text x="386" y="185.20000000000005" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--code-ink)">  AND start_time &gt;= {from}</text>
  <text x="386" y="200.60000000000005" font-size="6.9" font-family="monospace" font-weight="400" fill="var(--code-ink)">  AND start_time &lt;  {to}</text>
  <text x="386" y="216.00000000000006" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">GROUP BY provided_model_name, day</text>
  <text x="386" y="231.40000000000006" font-size="6.9" font-family="monospace" font-weight="700" fill="var(--accent-ink)">ORDER BY day</text>
  <text x="360" y="276" text-anchor="middle" font-size="6.6" fill="var(--faint)">parameterized placeholders ({projectId}/{from}/{to}) prevent SQL injection</text>
</svg>
<div class="figcap"><b>One declarative spec, the engine writes the SQL</b> (spec shape from <code>features/query/types.ts</code>, column names from the <code>observations</code> migration; <b>values illustrative</b>): you only describe <b>what you want</b> — <code>view</code> picks the table, <code>metrics</code> are <code>{measure, aggregation}</code>, <code>dimensions</code> are <code>{field}</code>, <code>timeDimension.granularity</code> sets the time bucket; <code>queryBuilder</code> compiles it into real ClickHouse SQL: measures become <code>count()</code>/<code>sum(total_cost)</code>, dimensions go into <code>GROUP BY</code>, the bucket becomes <code>toStartOfDay(start_time)</code>. Every user value flows through <b>parameterized placeholders</b>, blocking SQL injection at the root. Swap the <code>view</code> and you query a different table — one spec language covers every chart.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/features/query/dataModel.ts</span><span class="ln">one view's declaration</span></div>
  <pre class="code"><span class="cm">// each view declares: which dimensions/measures, each mapping to some real SQL</span>
{
  name: <span class="st">"traces"</span>,
  dimensions: {
    name:        { sql: <span class="st">"traces.name"</span>,      alias: <span class="st">"name"</span> },        <span class="cm">// logical name → physical column</span>
    environment: { sql: <span class="st">"traces.environment"</span>, alias: <span class="st">"environment"</span> },
    timestampMonth: { sql: <span class="st">"formatDateTime(traces.timestamp, '%Y-%m')"</span>, … },  <span class="cm">// can be an expression</span>
  },
  measures: { count: { … }, totalCost: { sql: <span class="st">"sum(total_cost)"</span>, … }, … },   <span class="cm">// aggregatable quantities</span>
}
<span class="cm">// a widget only references logical names like "name"/"totalCost", never touches physical columns</span></pre>
</div>

<table class="t">
  <thead><tr><th>view (data source)</th><th>what it aggregates</th><th>typical dimensions / measures</th></tr></thead>
  <tbody>
    <tr><td><code>traces</code></td><td>whole traces</td><td>dims: name, environment, userId; measures: count, total cost</td></tr>
    <tr><td><code>observations</code></td><td>single observations (incl. generations)</td><td>dims: model, type; measures: count, tokens, cost, latency</td></tr>
    <tr><td><code>scores-numeric</code></td><td>numeric scores</td><td>dims: name, source; measures: avg(value), count</td></tr>
    <tr><td><code>scores-categorical</code></td><td>categorical scores</td><td>dims: name, stringValue; measures: count, share per category</td></tr>
  </tbody>
</table>
<p>The four views each correspond to a core data type (echoing Lessons 8, 13, 28's domain model). A widget picks a view, then chooses dimensions/measures to group and compute from those it declares—<strong>what you can ask is bounded by the view's dictionary</strong>, both usable and guarded against over-reach.</p>
""")

# (en sec2/3/spark below)

_EN41.append(r"""
<h2>The compiler: assemble the declaration into parameterized SQL</h2>
<p>The second part is <code>QueryBuilder.build()</code>—the real <strong>compiler</strong>. It takes a declarative <code>QueryType</code>, consults the data model, and assembles full SQL in steps: <strong>dimensions</strong> become <code>SELECT … GROUP BY</code> columns (<code>mapDimensions</code>); <strong>measures</strong> become <code>count()/sum()/avg()</code> aggregations (<code>mapMetrics</code> + <code>translateAggregation</code>); <strong>time</strong> is bucketed by granularity (<code>applyBucketingDimension</code>, for time-series charts); <strong>filters</strong> become <code>WHERE</code>; and tables are <strong>joined</strong> when needed (<code>buildJoins</code>).</p>

<div class="fig">
<svg viewBox="0 0 720 225" role="img" aria-label="QueryBuilder.build compile flow: a declarative QueryType enters, passing mapDimensions to make GROUP BY columns, mapMetrics for aggregations, applyBucketingDimension for time bucketing, mapFilters for parameterized WHERE, buildJoins to join tables, producing SQL plus parameters handed to queryExecutor to run on ClickHouse">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">QueryBuilder.build(): declaration → parameterized SQL</text>
  <rect x="20" y="50" width="120" height="120" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="80" y="70" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">QueryType (declaration)</text><text x="80" y="88" text-anchor="middle" font-size="6.4" fill="var(--muted)">view</text><text x="80" y="102" text-anchor="middle" font-size="6.4" fill="var(--muted)">dimensions</text><text x="80" y="116" text-anchor="middle" font-size="6.4" fill="var(--muted)">metrics</text><text x="80" y="130" text-anchor="middle" font-size="6.4" fill="var(--muted)">filters</text><text x="80" y="144" text-anchor="middle" font-size="6.4" fill="var(--muted)">timeDimension</text>
  <rect x="180" y="44" width="160" height="132" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="260" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">QueryBuilder.build()</text><text x="260" y="82" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">mapDimensions → GROUP BY</text><text x="260" y="98" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">mapMetrics → count/sum/avg</text><text x="260" y="114" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">applyBucketing → time buckets</text><text x="260" y="130" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">mapFilters → parameterized WHERE</text><text x="260" y="146" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">buildJoins → join when needed</text><text x="260" y="164" text-anchor="middle" font-size="6.2" fill="var(--muted)">translate each item via the data model</text>
  <rect x="380" y="56" width="150" height="58" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="455" y="76" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">SQL (with {placeholders})</text><text x="455" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">SELECT … GROUP BY …</text><text x="455" y="104" text-anchor="middle" font-size="6.2" fill="var(--muted)">WHERE env = {p1}</text>
  <rect x="380" y="124" width="150" height="44" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="455" y="142" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">parameters</text><text x="455" y="157" text-anchor="middle" font-size="6.2" fill="var(--muted)">{ p1: "production" }</text>
  <rect x="565" y="80" width="135" height="62" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="632" y="104" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">queryExecutor</text><text x="632" y="121" text-anchor="middle" font-size="6.2" fill="var(--muted)">sends SQL+params to ClickHouse</text>
  <line x1="140" y1="110" x2="178" y2="110" stroke="var(--accent)" stroke-width="1.5"/><polygon points="178,110 169,106 169,114" fill="var(--accent)"/>
  <line x1="340" y1="92" x2="378" y2="86" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,86 369,85 371,93" fill="var(--accent)"/><line x1="340" y1="130" x2="378" y2="142" stroke="var(--teal)" stroke-width="1.4"/><polygon points="378,142 369,138 369,146" fill="var(--teal)"/>
  <line x1="530" y1="100" x2="563" y2="108" stroke="var(--teal)" stroke-width="1.4"/><polygon points="563,108 554,105 555,113" fill="var(--teal)"/><line x1="530" y1="146" x2="563" y2="120" stroke="var(--teal)" stroke-width="1.4"/><polygon points="563,120 554,121 558,128" fill="var(--teal)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">key: user-filled concrete values (production) always go via parameters, never into the SQL body—parameterized = injection-safe (Lesson 23)</text>
  <text x="360" y="214" text-anchor="middle" font-size="8" fill="var(--faint)">SQL separate from values: the template is cacheable/auditable, values bound per call, malicious input can't alter the structure</text>
</svg>
<div class="figcap"><b>the compiler translates item by item via the dictionary</b>: <code>queryBuilder.ts</code>'s <code>build()</code> chains <code>mapDimensions</code>(:270) / <code>mapMetrics</code>+<code>translateAggregation</code>(:290,137) / <code>applyBucketingDimension</code>(:182) / <code>mapFilters</code>+<code>buildWhereClause</code>(:490,858). Filters use FilterList's <code>apply()</code> to produce <b>SQL+parameters</b>—user values are bound as parameters, never spliced into the body (same injection prevention as Lesson 23).</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/features/query/server/queryBuilder.ts · queryExecutor.ts</span><span class="ln">declaration → SQL → execute</span></div>
  <pre class="code"><span class="cm">// 1) a declarative query (from widget / monitor / experiment aggregation, all this shape)</span>
<span class="kw">const</span> query = { view: <span class="st">"observations"</span>, dimensions: [{ field: <span class="st">"model"</span> }],
  metrics: [{ measure: <span class="st">"totalCost"</span>, aggregation: <span class="st">"sum"</span> }],
  filters: [{ column: <span class="st">"environment"</span>, operator: <span class="st">"="</span>, value: <span class="st">"production"</span> }] };

<span class="cm">// 2) compile: consult the data model, assemble parameterized SQL (GROUP BY/aggregate/WHERE/bucket/JOIN)</span>
<span class="kw">const</span> { sql, parameters } = <span class="kw">new</span> QueryBuilder(chartConfig, version).build(query, projectId);
<span class="cm">// sql:  SELECT model, sum(total_cost) … WHERE environment = {p_env} GROUP BY model</span>
<span class="cm">// parameters: { p_env: "production" }   ← values go via parameters, not spliced into SQL</span>

<span class="cm">// 3) execute: queryExecutor sends sql+parameters to ClickHouse</span></pre>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>fetch the view dictionary</h4><p><code>getViewDeclaration(view, version)</code> gets that view's dimension/measure dictionary by version—every later step translates against it.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>dimensions → GROUP BY</h4><p><code>mapDimensions</code> translates each logical dimension into SELECT columns and GROUP BY; the time dimension goes to <code>applyBucketingDimension</code> for granularity bucketing.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>measures → aggregations</h4><p><code>mapMetrics</code> + <code>translateAggregation</code> turn measures into count()/sum()/avg() aggregation functions.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>filters → parameterized WHERE</h4><p><code>mapFilters</code> + <code>buildWhereClause</code> use FilterList.apply to produce WHERE, binding user values as parameters.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>join + emit SQL</h4><p>When crossing tables, <code>buildJoins</code> adds JOINs; finally it assembles <code>{ sql, parameters }</code>, handed to <code>queryExecutor</code> to run on ClickHouse.</p></div></div>
</div>
""")

_EN41.append(r"""
<h2>Why it's worth building this engine</h2>
<p>Compiling a declaration to SQL could let each widget assemble strings itself. But Langfuse insists on one unified engine, because it solves four problems at once:</p>

<svg viewBox="0 0 720 230" role="img" aria-label="the query engine is a small metric-language compiler: the top declares what metric it wants with view, dimensions, metrics and filters (physical-agnostic, injection-safe); inside, the engine does four things — semantic layer mapping logical names to SQL, parameterization against injection, view versioning v1/v2, and one-engine-many-consumers; it compiles down to parameterized ClickHouse SQL, and because dashboards (L40), monitors (L33) and experiment aggregation all share it, the same metric always computes the same number">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="24" y="36" width="420" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="234" y="56" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">1 declaration (declarative · physical-agnostic · safe)</text>
  <text x="234" y="72" font-size="9.5" text-anchor="middle" fill="var(--muted)">view + dimensions + metrics + filters</text>
  <line x1="234" y1="80" x2="234" y2="92" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="24" y="92" width="420" height="86" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="234" y="110" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">2 query engine = a metric-language compiler</text>
  <rect x="36" y="118" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="132" y="135" font-size="9" text-anchor="middle" fill="var(--ink)">semantic layer: name ↔ SQL</text>
  <rect x="240" y="118" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="336" y="135" font-size="9" text-anchor="middle" fill="var(--ink)">parameterized (no injection)</text>
  <rect x="36" y="148" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="132" y="165" font-size="9" text-anchor="middle" fill="var(--ink)">view versioning: v1/v2</text>
  <rect x="240" y="148" width="192" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="336" y="165" font-size="9" text-anchor="middle" fill="var(--ink)">one engine, many consumers</text>
  <line x1="234" y1="178" x2="234" y2="190" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="24" y="190" width="420" height="34" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="234" y="211" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">3 parameterized SQL → ClickHouse</text>
  <rect x="466" y="92" width="238" height="86" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="585" y="116" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">one engine, many consumers</text>
  <text x="585" y="136" font-size="9.5" text-anchor="middle" fill="var(--muted)">dashboards L40 · monitors L33</text>
  <text x="585" y="152" font-size="9.5" text-anchor="middle" fill="var(--muted)">· experiment aggregation</text>
  <text x="585" y="170" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">→ same metric, same number</text>
  <line x1="444" y1="135" x2="466" y2="135" stroke="var(--teal)" stroke-width="2"></line>
</svg>

<table class="t">
  <thead><tr><th>design</th><th>what it solves</th><th>echoes</th></tr></thead>
  <tbody>
    <tr><td><b>semantic layer</b> (logical name↔SQL)</td><td>rename/restructure physical columns—only the dictionary changes, all queries untouched; users needn't know the physical schema</td><td>decouple "what you want" from "how it's stored"</td></tr>
    <tr><td><b>parameterization</b> (values via parameters)</td><td>user values never spliced into the SQL body, rooting out SQL injection</td><td>same as Lesson 23's FilterState</td></tr>
    <tr><td><b>view versioning</b> (v1/v2)</td><td>as the physical schema evolves, old queries still compile against the old view, not breaking history</td><td>Lessons 34/37 "immutable + evolving"</td></tr>
    <tr><td><b>one engine, many consumers</b></td><td>dashboards/monitors/experiment-aggregation share it, keeping metric definitions globally consistent</td><td>Lesson 40 "one query shape, three reuses"</td></tr>
  </tbody>
</table>

<p>Connect these four and the query engine is really a small <strong>"metrics language + compiler"</strong>: the upper layers describe "which metric I want" in a <strong>declarative, physical-agnostic, injection-safe</strong> little language, and the engine renders it <strong>correctly, consistently, safely</strong> into SQL ClickHouse can run. It's the same idea as Lesson 23 compiling FilterState into filter SQL, just upgraded from "filtering" to full "aggregation queries". <strong>Declaration on top, compilation below, physical details sealed firmly inside the engine</strong>—the underlying reason Langfuse can make dashboards, monitors, and the API always compute the same number for the same metric.</p>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why build a semantic layer instead of letting widgets write SQL directly?</strong> Direct SQL seems easier but plants three landmines. One is <strong>coupling</strong>: every widget hardcodes physical column names, so the day ClickHouse restructures a table or renames a column, hundreds of widgets break together and must be fixed one by one. The semantic layer collects "logical name → physical SQL" into one dictionary, so a physical change touches only the dictionary, the upper layer unmoved. Two is <strong>safety</strong>: letting each widget assemble SQL spreads injection-prevention responsibility to everyone who writes a widget—someone will forget or get it wrong, and one hole is one data leak. A unified engine welds parameterization into its single exit, so <strong>injection safety is backstopped by structure</strong>, not diligence. Three is <strong>consistency</strong>: SQL scattered everywhere eventually computes different numbers for the same metric. Collecting metric definitions into the semantic layer gives one algorithm company-wide. <strong>One engine buys decoupling, safety, and consistency all at once</strong>—that's why it's worth the extra few thousand lines.<br><br>
  <strong>Why do views carry v1/v2 versions?</strong> Because <strong>the physical schema evolves, but historical queries shouldn't break for it</strong>. ClickHouse tables get refactored, columns split and merge, new materialized views appear for performance—all normal evolution of the underlying. If a query binds tightly to the current physical structure, then every underlying move risks miscomputing or erroring every saved widget, monitor, and API query. Introducing versions to a view gives "semantics" an immutable snapshot too: a v1 query forever compiles against the v1 dictionary, even if the underlying has long migrated to v2's new tables. This is the <strong>same belief echoing at the query layer</strong> as Lesson 34's dataset-item versions and Lesson 37's prompt versions—<strong>the underlying can evolve boldly because the upper layer is protected by a stable layer of versioned semantics</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>The query engine = a declarative-query → SQL compiler</strong>: a widget's <code>view+dimensions+metrics+filters</code> declaration is compiled to ClickHouse SQL and executed by it—the engine behind Lesson 40's dashboards.</li>
    <li><strong>Semantic layer (data model)</strong>: declares <code>dimensions</code>/<code>measures</code> per view, each mapping a logical name to real SQL (e.g. <code>name</code>→<code>traces.name</code>, time→<code>formatDateTime(...)</code>)—the upper layer never touches physical columns.</li>
    <li><strong>Compiler (QueryBuilder.build)</strong>: consults the dictionary to translate dimensions into GROUP BY, measures into aggregations, time into buckets, filters into WHERE, joining tables when needed, producing <strong>SQL + parameters</strong>.</li>
    <li><strong>Parameterized = injection-safe</strong>: user-filled values are bound as parameters, never spliced into the SQL body—Lesson 23's FilterState discipline carried into aggregation queries, injection safety backstopped by structure.</li>
    <li><strong>One engine, four payoffs</strong>: the semantic layer decouples physical, parameterization ensures safety, view v1/v2 versioning protects history, one engine for many consumers keeps definitions consistent—dashboards/monitors/experiments always the same number for the same metric.</li>
  </ul>
</div>
""")

LESSON_41 = {"zh": "\n".join(_ZH41), "en": "\n".join(_EN41)}


# ══════════════════════════════════════════════════════════════════════
# L42 · 模型与定价 / Models & pricing
# ══════════════════════════════════════════════════════════════════════
_ZH42 = []
_EN42 = []

_ZH42.append(r"""
<p class="lead">
第 16 课说过「成本 = 用量 × 单价」，但留了个悬念：<strong>单价从哪来？一个叫法五花八门的模型名，又怎么对上它的价目？</strong> 这一课补上这块拼图——Langfuse 的<strong>定价数据模型</strong>。重点有三：<code>matchPattern</code> 用<strong>一条正则</strong>把同一个模型在各家平台千奇百怪的命名统一认出来；<code>pricingTiers</code> 用<strong>「默认档 + 条件档」</strong>支持按用量/上下文窗口<strong>分级定价</strong>；而 <code>prices</code> 是一张「<strong>每种用量、每个 token</strong>」的细价目（输入、输出、缓存读……各有各的价）。
它直接喂养第 16 课的成本计算：拿一条调用的模型名去<strong>匹配</strong>出价目、按用量<strong>选中</strong>合适的档、再用「单价 × 用量」<strong>算</strong>出这次花了多少钱。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  模型定价像一本<strong>「跨国出租车计价手册」</strong>。同一款车，在不同城市、不同叫车平台有<strong>一堆不同的名字</strong>——<code>gpt-4o</code>、<code>openai/gpt-4o</code>、<code>us.anthropic.claude-...-v1:0</code>。手册用一条<strong>「识别规则」</strong>（<code>matchPattern</code> 正则）把这些花名<strong>全认成同一辆车</strong>，对上同一份价目。
  而车费<strong>不是一口价</strong>：市区短途一个价，但要是你这趟特别长（比如上下文窗口超过 20 万 token），就跳到「长途档」按另一套价算（<code>pricingTiers</code> 的条件档）。最后结账时，手册按<strong>「跑了多少 × 每单位多少钱」</strong>逐项相加——而且<strong>分项计费</strong>：起步价、里程费、等待费各算各的（输入 token、输出 token、缓存命中各有单价）。一本手册，把「认车 + 分档 + 分项计费」三件事一次办妥。
</div>
""")

# (L42 sections below)

_ZH42.append(r"""
<h2>matchPattern：一条正则，认尽各家花名</h2>
<p>同一个模型，在 OpenAI、Anthropic、AWS Bedrock、Google Vertex、Azure 上的<strong>命名规则各不相同</strong>：有的带 <code>openai/</code> 前缀、有的带 <code>us.</code> 区域前缀、有的带 <code>-v1:0</code> 版本后缀、有的用 <code>@日期</code>。如果用「精确名」去匹配价目，就得为每种写法各存一条，维护噩梦。Langfuse 的解法是给每个模型配一条<strong>大小写不敏感、全串匹配</strong>的正则 <code>matchPattern</code>，一网打尽所有合法写法。</p>

<div class="fig">
<svg viewBox="0 0 720 205" role="img" aria-label="matchPattern 统一命名：gpt-4o、openai/gpt-4o、带区域前缀和版本后缀的 Bedrock/Vertex 写法，都被同一条 matchPattern 正则匹配，对应到同一个 Model 价目条目">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">各家花名 → 一条正则 → 同一份价目</text>
  <rect x="30" y="44" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="64" text-anchor="middle" font-size="7.5" fill="var(--ink)">gpt-4o（裸名）</text>
  <rect x="30" y="82" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="102" text-anchor="middle" font-size="7.5" fill="var(--ink)">openai/gpt-4o（带 provider 前缀）</text>
  <rect x="30" y="120" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="140" text-anchor="middle" font-size="7" fill="var(--ink)">us.anthropic.claude-...-v1:0（Bedrock）</text>
  <rect x="30" y="158" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="178" text-anchor="middle" font-size="7" fill="var(--ink)">claude-...@20240620（Vertex 日期）</text>
  <rect x="300" y="90" width="160" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="380" y="110" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">matchPattern</text><text x="380" y="126" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">(?i)^(provider/)?(...)$</text><text x="380" y="138" text-anchor="middle" font-size="6.5" fill="var(--muted)">大小写不敏感 · 全串匹配</text>
  <rect x="510" y="84" width="180" height="68" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="106" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">同一个 Model 条目</text><text x="600" y="124" text-anchor="middle" font-size="6.6" fill="var(--muted)">tokenizerId + pricingTiers</text><text x="600" y="138" text-anchor="middle" font-size="6.5" fill="var(--muted)">认成同一辆车 → 同一价目</text>
  <line x1="250" y1="60" x2="298" y2="105" stroke="var(--faint)" stroke-width="1.2"/><line x1="250" y1="98" x2="298" y2="112" stroke="var(--faint)" stroke-width="1.2"/><line x1="250" y1="136" x2="298" y2="124" stroke="var(--faint)" stroke-width="1.2"/><line x1="250" y1="174" x2="298" y2="132" stroke="var(--faint)" stroke-width="1.2"/>
  <line x1="460" y1="118" x2="508" y2="118" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,118 499,114 499,122" fill="var(--teal)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">正则组件：(?i) 不分大小写 · ^…$ 全串 · (provider/)? 可选前缀 · (us.|eu.|apac.)? 区域 · (:0)? / @date 版本</text>
</svg>
<div class="figcap"><b>一条正则，统一碎片化命名</b>：<code>default-model-prices.json</code> 的每个条目都带一条 <code>matchPattern</code>，如 gpt-4o 的 <code>(?i)^(openai/)?(gpt-4o)$</code>。它用 <code>(?i)</code> 不分大小写、<code>^…$</code> 全串匹配、可选的 provider/区域前缀与版本后缀，把同一模型在六大平台的所有写法<b>一网打尽</b>。源码：<code>worker/src/constants/default-model-prices.json</code>。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 260" role="img" aria-label="模型定价真实例子：表格列出 gpt-4o、gpt-4o-mini、claude-3-5-sonnet、claude-3-haiku、gpt-4-turbo 五个真实模型的每百万 token 输入价与输出价，右侧用条形对比输出价（gpt-4-turbo 最贵 30 美元，gpt-4o-mini 最便宜 0.6 美元）；下方展示一次模型名经 matchPattern 正则匹配到价格行。数据取自 default-model-prices.json">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：模型定价表（每 1M token）</text>
  <rect x="18" y="28" width="684" height="20" fill="var(--panel-2)"/>
  <text x="30" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">modelName</text>
  <text x="252" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">输入 $/1M</text>
  <text x="348" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">输出 $/1M</text>
  <text x="440" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">输出价对比</text>
  <rect x="18" y="50" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="67" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">gpt-4o</text>
  <text x="262" y="67" text-anchor="end" font-size="7.8" fill="var(--ink)">$2.50</text>
  <text x="372" y="67" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$10.00</text>
  <rect x="438" y="57" width="56" height="12" rx="3" fill="var(--accent)" opacity="0.7"/><text x="500" y="67" font-size="6.8" fill="var(--accent)">$10.00</text>
  <rect x="18" y="76" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="93" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">gpt-4o-mini</text>
  <text x="262" y="93" text-anchor="end" font-size="7.8" fill="var(--ink)">$0.15</text>
  <text x="372" y="93" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$0.60</text>
  <rect x="438" y="83" width="3" height="12" rx="3" fill="var(--blue)" opacity="0.7"/><text x="447" y="93" font-size="6.8" fill="var(--blue)">$0.60</text>
  <rect x="18" y="102" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="119" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">claude-3-5-sonnet-20240620</text>
  <text x="262" y="119" text-anchor="end" font-size="7.8" fill="var(--ink)">$3.00</text>
  <text x="372" y="119" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$15.00</text>
  <rect x="438" y="109" width="84" height="12" rx="3" fill="var(--purple)" opacity="0.7"/><text x="528" y="119" font-size="6.8" fill="var(--purple)">$15.00</text>
  <rect x="18" y="128" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="145" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">claude-3-haiku-20240307</text>
  <text x="262" y="145" text-anchor="end" font-size="7.8" fill="var(--ink)">$0.25</text>
  <text x="372" y="145" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$1.25</text>
  <rect x="438" y="135" width="7" height="12" rx="3" fill="var(--accent)" opacity="0.7"/><text x="451" y="145" font-size="6.8" fill="var(--accent)">$1.25</text>
  <rect x="18" y="154" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="171" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">gpt-4-turbo</text>
  <text x="262" y="171" text-anchor="end" font-size="7.8" fill="var(--ink)">$10.00</text>
  <text x="372" y="171" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$30.00</text>
  <rect x="438" y="161" width="168" height="12" rx="3" fill="var(--amber)" opacity="0.7"/><text x="612" y="171" font-size="6.8" fill="var(--amber)">$30.00</text>
  <rect x="18" y="188" width="684" height="58" rx="9" fill="var(--code-bg)" stroke="var(--blue)"/>
  <text x="30" y="204" font-size="7.6" font-weight="700" fill="var(--blue)">模型名怎么对上价格？matchPattern 正则</text>
  <text x="30" y="221" font-size="7.2" font-family="monospace" fill="var(--code-ink)">usage.model = &quot;openai/gpt-4o&quot;</text>
  <text x="250" y="221" font-size="7.2" font-family="monospace" fill="var(--muted)">──match──▶</text>
  <text x="330" y="221" font-size="7" font-family="monospace" fill="var(--accent-ink)">(?i)^(openai/)?(gpt-4o)$</text>
  <text x="560" y="221" font-size="7.2" font-family="monospace" fill="var(--accent)">✓ → gpt-4o</text>
  <text x="30" y="238" font-size="6.8" fill="var(--faint)">价格按 token 存在 pricingTiers[].prices.{input,output}（图中已 ×1e6 换成每百万）；摄取时用正则把模型名匹配到价格行</text>
</svg>
<div class="figcap"><b>定价是「正则 → 每 token 价」的查找表</b>（数据取自 <code>worker/src/constants/default-model-prices.json</code>，<b>真实价</b>）：每个模型在 <code>pricingTiers[].prices</code> 里按 <b>token</b> 存 <code>input</code>/<code>output</code> 价（表中已 ×1e6 换成「每百万 token」更好读）。同是输出价，<code>gpt-4-turbo</code>（$30）是 <code>gpt-4o-mini</code>（$0.60）的 <b>50 倍</b>——选型即成本。模型名怎么对上价格？靠 <code>matchPattern</code> 正则：<code>&quot;openai/gpt-4o&quot;</code> 命中 <code>(?i)^(openai/)?(gpt-4o)$</code> 就用这行价，于是带不带 <code>openai/</code> 前缀都能正确计费（第 12 课摄取算成本就用它）。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/constants/default-model-prices.json</span><span class="ln">一个模型条目（节选）</span></div>
  <pre class="code"><span class="cm">// 158 条种子价之一；matchPattern 认尽各家花名</span>
{
  "modelName": <span class="st">"gpt-4o"</span>,
  "matchPattern": <span class="st">"(?i)^(openai/)?(gpt-4o)$"</span>,   <span class="cm">// gpt-4o / openai/gpt-4o / GPT-4O 都匹配</span>
  "tokenizerId": <span class="st">"openai"</span>,                        <span class="cm">// SDK 没报用量时，用这个分词器数 token</span>
  "pricingTiers": [ { "name": <span class="st">"Standard"</span>, "isDefault": <span class="kw">true</span>, "conditions": [],
    "prices": { "input": 2.5e-6, "output": 1e-5,             <span class="cm">// 每 token 单价</span>
                "input_cached_tokens": 1.25e-6, … } } ]      <span class="cm">// 分项：输入/输出/缓存读各有价</span>
}
<span class="cm">// Anthropic 的 matchPattern 还会含 us./eu./apac. 区域前缀与 -v1:0、@date 版本写法</span></pre>
</div>

<table class="t">
  <thead><tr><th>正则组件</th><th>作用</th><th>能认出的写法</th></tr></thead>
  <tbody>
    <tr><td><code>(?i)</code></td><td>大小写不敏感</td><td>gpt-4o 和 GPT-4O 都认</td></tr>
    <tr><td><code>^…$</code></td><td>全串匹配</td><td>避免误伤（不会把 gpt-4o-mini 当成 gpt-4o）</td></tr>
    <tr><td><code>(provider/)?</code></td><td>可选 provider 前缀</td><td>openai/gpt-4o、anthropic/claude-…</td></tr>
    <tr><td><code>(us\.|eu\.|apac\.)?</code></td><td>可选 AWS 区域前缀</td><td>us.anthropic.claude-…（Bedrock）</td></tr>
    <tr><td><code>(:0)?</code> / <code>@date</code></td><td>可选版本后缀</td><td>…-v1:0（Bedrock）、…@20240620（Vertex）</td></tr>
  </tbody>
</table>
<p>这几个组件像一套「<strong>可拆装的乐高</strong>」：哪家平台多了种命名花样，往正则里加一段可选组就行，无需重排价目表。一条规则，把六大平台的命名差异<strong>吸收在了模式层</strong>。</p>
""")

_ZH42.append(r"""
<h2>pricingTiers：默认档 + 条件档</h2>
<p>定价往往不是一口价。同一个模型，<strong>上下文窗口越大、单价可能越高</strong>；有的还按用量阶梯计费。Langfuse 用 <code>pricingTiers</code>（价目档）支持这种分级：每个模型有<strong>恰好一个默认档</strong>（<code>isDefault=true</code>、<code>priority=0</code>、<code>conditions=[]</code>），外加任意个<strong>条件档</strong>（带 <code>conditions</code>，如「输入 token &gt; 20 万」）。选档时，<code>matchPricingTier</code> 把条件档<strong>按 priority 升序</strong>逐个试，<strong>第一个所有条件都满足</strong>的胜出；都不满足就<strong>回落到默认档</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 205" role="img" aria-label="选档流程：一次调用的用量进来，matchPricingTier 把非默认条件档按 priority 升序逐个评估，第一个所有条件都满足的胜出，否则回落默认档；选中的 tier 提供 prices 价目">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">按用量选档：条件档优先，都不中则回落默认</text>
  <rect x="30" y="80" width="130" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">这次调用的用量</text><text x="95" y="115" text-anchor="middle" font-size="6.4" fill="var(--muted)">input=250k, output=8k</text>
  <rect x="200" y="44" width="300" height="36" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="350" y="61" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">条件档（priority 1）：input &gt; 200000 ?</text><text x="350" y="73" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">满足 ✓ → 选它（长上下文价）</text>
  <rect x="200" y="88" width="300" height="32" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="350" y="105" text-anchor="middle" font-size="7.5" fill="var(--muted)">条件档（priority 2）：…（前一个已中，不再试）</text>
  <rect x="200" y="128" width="300" height="32" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="350" y="148" text-anchor="middle" font-size="7.5" fill="var(--muted)">默认档（priority 0, conditions=[]）：都不中时的兜底</text>
  <rect x="540" y="80" width="150" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="615" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">选中档的 prices</text><text x="615" y="115" text-anchor="middle" font-size="6.5" fill="var(--muted)">→ 第16课算成本</text>
  <line x1="160" y1="96" x2="198" y2="62" stroke="var(--accent)" stroke-width="1.4"/><polygon points="198,62 189,64 193,71" fill="var(--accent)"/>
  <line x1="500" y1="62" x2="538" y2="96" stroke="var(--teal)" stroke-width="1.5"/><polygon points="538,96 529,92 532,100" fill="var(--teal)"/>
  <text x="360" y="180" text-anchor="middle" font-size="8" fill="var(--faint)">conditions 用 AND 逻辑（全满足才算中）；operator 支持 gt/gte/lt/lte/eq/neq；按 priority 升序「先到先得」</text>
  <text x="360" y="195" text-anchor="middle" font-size="8" fill="var(--faint)">默认档永远存在、永远兜底——保证任何用量都能算出一个价，绝不漏算</text>
</svg>
<div class="figcap"><b>分级定价，默认兜底</b>：<code>matchPricingTier</code>（<code>pricing-tiers/matcher.ts:88</code>）滤掉默认档、按 <code>priority</code> 升序评估条件档，第一个<b>全条件满足</b>（AND 逻辑）的胜出，否则回落默认档。条件 = <code>usageDetailPattern</code>（正则选用量项）+ <code>operator</code>（gt/gte/lt/lte/eq/neq）+ <code>value</code>。</div>
</div>

<table class="t">
  <thead><tr><th>档类型</th><th>isDefault / priority / conditions</th><th>作用</th></tr></thead>
  <tbody>
    <tr><td><b>默认档</b>（每模型恰一个）</td><td>true / 0 / []</td><td>兜底价——任何用量都能算出，绝不漏</td></tr>
    <tr><td><b>条件档</b>（任意个）</td><td>false / ≥1 / 有条件</td><td>按上下文窗口/用量分级（如「&gt;20万 token 走长上下文价」）</td></tr>
    <tr><td colspan="3" style="background:var(--blue-soft)"><b>选档规则</b>：条件档按 priority 升序逐个评，第一个全条件满足者胜；都不中→默认档</td></tr>
  </tbody>
</table>
""")

# (L42 sec3 costcalc below)

_ZH42.append(r"""
<h2>合起来：一次调用的成本是怎么算出来的</h2>
<p>把 matchPattern 和 pricingTiers 串起来，就还原了第 16 课「成本 = 用量 × 单价」的完整链条。<code>default-model-prices.json</code> 这 158 条种子价会被 <code>upsertDefaultModelPrices</code> 灌进数据库的 Model/Price 表；之后每条调用都走这条计价线：</p>

<svg viewBox="0 0 720 220" role="img" aria-label="一次调用的计价线五步：① 拿 observation 报告的模型名，② 用 matchPattern 正则匹配到 Model 条目（含 tokenizerId 与 pricingTiers），③ SDK 没报用量时按 tokenizerId 分词数 token，④ matchPricingTier 按用量选中价目档拿到 prices，⑤ 对每种用量用 prices 乘用量逐项相加，得总成本，还原第16课成本等于用量乘单价">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="16" y="42" width="128" height="80" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="80" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">① 拿模型名</text>
  <text x="80" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">us.anthropic</text>
  <text x="80" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">.claude-…</text>
  <rect x="156" y="42" width="128" height="80" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="220" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">② 匹配 Model</text>
  <text x="220" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">matchPattern 正则</text>
  <text x="220" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">→ tiers + tokenizer</text>
  <rect x="296" y="42" width="128" height="80" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">③ 数 token</text>
  <text x="360" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">(SDK 没报时)</text>
  <text x="360" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">tokenizerId 分词</text>
  <rect x="436" y="42" width="128" height="80" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="500" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">④ 选档</text>
  <text x="500" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">matchPricingTier</text>
  <text x="500" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">→ prices 价目</text>
  <rect x="576" y="42" width="128" height="80" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="640" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑤ 分项算钱</text>
  <text x="640" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">prices[项] × 用量</text>
  <text x="640" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">逐项相加</text>
  <line x1="144" y1="82" x2="156" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="284" y1="82" x2="296" y2="82" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="424" y1="82" x2="436" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="564" y1="82" x2="576" y2="82" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="160" y="148" width="400" height="40" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="360" y="173" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">总成本 = Σ(各项单价 × 各项用量)</text>
  <line x1="640" y1="122" x2="440" y2="148" stroke="var(--teal)" stroke-width="1.5"></line>
  <text x="360" y="208" font-size="10" text-anchor="middle" fill="var(--muted)">还原第 16 课「成本 = 用量 × 单价」的完整链条</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>拿模型名</h4><p>从一条 observation（generation）取出它报告的模型名，如 <code>us.anthropic.claude-...-v1:0</code>。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>匹配 Model</h4><p>用模型名去试各条 <code>matchPattern</code> 正则，命中的就是这次该用的价目条目（含 tokenizerId 与 pricingTiers）。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>（必要时）数 token</h4><p>若 SDK 没报用量，用条目的 <code>tokenizerId</code>/<code>tokenizerConfig</code> 把文本分词、数出 token 数（第 16 课）。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>选档</h4><p><code>matchPricingTier</code> 按用量选中合适的 tier（默认或条件档），拿到这次该用的 <code>prices</code> 价目。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>分项算钱</h4><p>对每种用量（输入/输出/缓存读…）用 <code>prices[该项] × 用量</code> 逐项相加，得这次调用的总成本。</p></div></div>
</div>

<p>还有一层灵活：这 158 条只是 <strong>Langfuse 内置的默认价</strong>（<code>projectId</code> 为空的全局 Model）。如果你用的是自研模型、私有部署、或谈了特殊折扣，可以在自己项目里<strong>新增/覆盖</strong> Model 价目（带 <code>projectId</code> 的项目级条目优先）——于是平台既<strong>开箱即用</strong>（主流模型价已备好），又能<strong>精确贴合</strong>你的真实账单。<code>add-model-price</code> 这个仓库技能，管的就是怎么安全地往这份种子价里增改条目（生成 UUID、写对 matchPattern、校验 JSON）。</p>
""")

_ZH42.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么用正则匹配模型名，而不是精确字符串相等？</strong> 因为模型命名在生态里<strong>碎得令人发指</strong>。同一个 Claude，OpenAI 风格叫 <code>claude-3-5-sonnet</code>、Bedrock 上叫 <code>us.anthropic.claude-3-5-sonnet-v1:0</code>、Vertex 上叫 <code>claude-3-5-sonnet@20240620</code>，再加上大小写、<code>provider/</code> 前缀的排列组合，一个模型轻松有十几种合法写法。若用精确匹配，你得为每种写法各存一条价目，加个新区域、改个版本号就得全表翻新——维护成本爆炸，还极易漏。一条精心写的正则把这些<strong>同义写法收敛成一个意图</strong>：「无论你怎么称呼它，我都认得这是 gpt-4o」。<strong>正则在这里不是炫技，而是对抗命名碎片化的必需品</strong>——它把「世界的混乱」挡在了价目表之外。<br><br>
  <strong>为什么定价要分「默认档 + 条件档」，而不是一口价？</strong> 因为真实定价<strong>本就分级</strong>：长上下文更贵、缓存命中更便宜、某些用量超阈值跳档。如果只存一口价，这些差异要么算错、要么得在计费代码里写满 if-else——把定价策略<strong>硬编码进逻辑</strong>，每变一次价就得改代码、发版本。把分级表达成<strong>数据</strong>（一组带 conditions 的 tier），计费逻辑就只剩一件事：<strong>按用量选中合适的档</strong>，而「档怎么分、价怎么定」全在数据里、可随时调。这又是一次「<strong>把策略从代码挪进数据</strong>」的胜利——和第 28 课 score config、第 16 课定价 schema 一脉相承：<strong>能用数据表达的规则，就别写进代码</strong>。而那个永远存在的默认档，则是一道优雅的兜底：保证<strong>任何</strong>用量都落得进某个价，绝不会因为没匹配上条件就算不出钱。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>定价数据模型喂养第 16 课成本计算</strong>：<code>default-model-prices.json</code> 158 条种子价被 upsert 进 Model/Price 表，每条调用据此算「用量 × 单价」。</li>
    <li><strong>matchPattern 统一命名</strong>：每模型一条大小写不敏感、全串匹配的正则，认尽 OpenAI/Anthropic/Bedrock/Vertex/Azure/Gemini 的各种写法（provider 前缀、区域前缀、版本后缀、@日期）。</li>
    <li><strong>pricingTiers 分级定价</strong>：恰一个默认档（兜底）+ 任意条件档；<code>matchPricingTier</code> 按 priority 升序评条件（AND 逻辑、operator gt/gte/lt/lte/eq/neq），第一个全满足者胜，否则回落默认。</li>
    <li><strong>prices 分项计费</strong>：每种用量（输入/输出/缓存读…）各有每-token 单价；成本 = Σ(各项单价 × 各项用量)。</li>
    <li><strong>默认价 + 项目覆盖</strong>：158 条全局默认开箱即用，项目可新增带 <code>projectId</code> 的 Model 覆盖（自研/私有/折扣价）。把分级策略放进数据而非代码——呼应第 16/28 课「规则即数据」。</li>
  </ul>
</div>
""")

_EN42.append(r"""
<p class="lead">
Lesson 16 said "cost = usage × price", but left a cliffhanger: <strong>where does the price come from, and how does a wildly-named model name match its price list?</strong> This lesson fills that piece—Langfuse's <strong>pricing data model</strong>. Three focuses: <code>matchPattern</code> uses <strong>one regex</strong> to recognize the same model under every platform's quirky naming; <code>pricingTiers</code> uses <strong>"a default tier + conditional tiers"</strong> to support <strong>tiered pricing</strong> by usage / context window; and <code>prices</code> is a fine price list "<strong>per usage type, per token</strong>" (input, output, cache reads… each with its own price).
It directly feeds Lesson 16's cost computation: take a call's model name, <strong>match</strong> its price list, <strong>select</strong> the right tier by usage, and compute "price × usage" to get how much this call cost.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Model pricing is like a <strong>"cross-country taxi fare manual"</strong>. The same car has <strong>a pile of different names</strong> across cities and ride apps—<code>gpt-4o</code>, <code>openai/gpt-4o</code>, <code>us.anthropic.claude-...-v1:0</code>. The manual uses one <strong>"recognition rule"</strong> (the <code>matchPattern</code> regex) to recognize all these aliases as <strong>the same car</strong>, matching one fare table.
  And the fare <strong>isn't flat</strong>: a short city trip at one rate, but if your trip is especially long (say a context window over 200K tokens), it jumps to a "long-haul tier" at another rate (<code>pricingTiers</code>' conditional tiers). At checkout, the manual sums "how much × rate per unit" item by item—and bills <strong>line-by-line</strong>: base fare, mileage, waiting each separately (input tokens, output tokens, cache hits each have their own rate). One manual handles "identify the car + pick the tier + itemized billing" in one go.
</div>
""")

_EN42.append(r"""
<h2>matchPattern: one regex to recognize every alias</h2>
<p>The same model is <strong>named differently</strong> on OpenAI, Anthropic, AWS Bedrock, Google Vertex, and Azure: some carry an <code>openai/</code> prefix, some a <code>us.</code> region prefix, some a <code>-v1:0</code> version suffix, some an <code>@date</code>. Matching the price list by "exact name" would mean storing one entry per spelling—a maintenance nightmare. Langfuse's solution gives each model a <strong>case-insensitive, full-string</strong> regex <code>matchPattern</code> that catches every valid spelling.</p>

<div class="fig">
<svg viewBox="0 0 720 205" role="img" aria-label="matchPattern unifies naming: gpt-4o, openai/gpt-4o, and the region-prefixed and version-suffixed Bedrock/Vertex spellings are all matched by the same matchPattern regex, mapping to the same Model price entry">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">every alias → one regex → one price list</text>
  <rect x="30" y="44" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="64" text-anchor="middle" font-size="7.5" fill="var(--ink)">gpt-4o (bare name)</text>
  <rect x="30" y="82" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="102" text-anchor="middle" font-size="7.5" fill="var(--ink)">openai/gpt-4o (provider prefix)</text>
  <rect x="30" y="120" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="140" text-anchor="middle" font-size="7" fill="var(--ink)">us.anthropic.claude-...-v1:0 (Bedrock)</text>
  <rect x="30" y="158" width="220" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="140" y="178" text-anchor="middle" font-size="7" fill="var(--ink)">claude-...@20240620 (Vertex date)</text>
  <rect x="300" y="90" width="160" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="380" y="110" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">matchPattern</text><text x="380" y="126" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">(?i)^(provider/)?(...)$</text><text x="380" y="138" text-anchor="middle" font-size="6.2" fill="var(--muted)">case-insensitive · full-string</text>
  <rect x="510" y="84" width="180" height="68" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="106" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">one Model entry</text><text x="600" y="124" text-anchor="middle" font-size="6.6" fill="var(--muted)">tokenizerId + pricingTiers</text><text x="600" y="138" text-anchor="middle" font-size="6.4" fill="var(--muted)">same car → same price list</text>
  <line x1="250" y1="60" x2="298" y2="105" stroke="var(--faint)" stroke-width="1.2"/><line x1="250" y1="98" x2="298" y2="112" stroke="var(--faint)" stroke-width="1.2"/><line x1="250" y1="136" x2="298" y2="124" stroke="var(--faint)" stroke-width="1.2"/><line x1="250" y1="174" x2="298" y2="132" stroke="var(--faint)" stroke-width="1.2"/>
  <line x1="460" y1="118" x2="508" y2="118" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,118 499,114 499,122" fill="var(--teal)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">regex parts: (?i) case-insensitive · ^…$ full-string · (provider/)? optional prefix · (us.|eu.|apac.)? region · (:0)? / @date version</text>
</svg>
<div class="figcap"><b>one regex unifies fragmented naming</b>: each <code>default-model-prices.json</code> entry carries a <code>matchPattern</code>, e.g. gpt-4o's <code>(?i)^(openai/)?(gpt-4o)$</code>. With <code>(?i)</code> case-insensitive, <code>^…$</code> full-string, optional provider/region prefixes and version suffixes, it <b>catches all</b> spellings of one model across six platforms. Source: <code>worker/src/constants/default-model-prices.json</code>.</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 260" role="img" aria-label="Model pricing real example: the table lists five real models — gpt-4o, gpt-4o-mini, claude-3-5-sonnet, claude-3-haiku, gpt-4-turbo — with input and output price per million tokens, and bars on the right compare output price (gpt-4-turbo most expensive at $30, gpt-4o-mini cheapest at $0.60); below, a model name is matched to a price row via its matchPattern regex. Data from default-model-prices.json">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: model pricing (per 1M tokens)</text>
  <rect x="18" y="28" width="684" height="20" fill="var(--panel-2)"/>
  <text x="30" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">modelName</text>
  <text x="252" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">input $/1M</text>
  <text x="348" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">output $/1M</text>
  <text x="440" y="42" font-size="7.4" font-weight="700" fill="var(--ink)">output price</text>
  <rect x="18" y="50" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="67" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">gpt-4o</text>
  <text x="262" y="67" text-anchor="end" font-size="7.8" fill="var(--ink)">$2.50</text>
  <text x="372" y="67" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$10.00</text>
  <rect x="438" y="57" width="56" height="12" rx="3" fill="var(--accent)" opacity="0.7"/><text x="500" y="67" font-size="6.8" fill="var(--accent)">$10.00</text>
  <rect x="18" y="76" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="93" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">gpt-4o-mini</text>
  <text x="262" y="93" text-anchor="end" font-size="7.8" fill="var(--ink)">$0.15</text>
  <text x="372" y="93" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$0.60</text>
  <rect x="438" y="83" width="3" height="12" rx="3" fill="var(--blue)" opacity="0.7"/><text x="447" y="93" font-size="6.8" fill="var(--blue)">$0.60</text>
  <rect x="18" y="102" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="119" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">claude-3-5-sonnet-20240620</text>
  <text x="262" y="119" text-anchor="end" font-size="7.8" fill="var(--ink)">$3.00</text>
  <text x="372" y="119" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$15.00</text>
  <rect x="438" y="109" width="84" height="12" rx="3" fill="var(--purple)" opacity="0.7"/><text x="528" y="119" font-size="6.8" fill="var(--purple)">$15.00</text>
  <rect x="18" y="128" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="145" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">claude-3-haiku-20240307</text>
  <text x="262" y="145" text-anchor="end" font-size="7.8" fill="var(--ink)">$0.25</text>
  <text x="372" y="145" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$1.25</text>
  <rect x="438" y="135" width="7" height="12" rx="3" fill="var(--accent)" opacity="0.7"/><text x="451" y="145" font-size="6.8" fill="var(--accent)">$1.25</text>
  <rect x="18" y="154" width="684" height="26" fill="var(--bg)" stroke="var(--line)" stroke-width="0.4"/>
  <text x="30" y="171" font-size="8" font-weight="700" font-family="monospace" fill="var(--accent-ink)">gpt-4-turbo</text>
  <text x="262" y="171" text-anchor="end" font-size="7.8" fill="var(--ink)">$10.00</text>
  <text x="372" y="171" text-anchor="end" font-size="7.8" font-weight="700" fill="var(--ink)">$30.00</text>
  <rect x="438" y="161" width="168" height="12" rx="3" fill="var(--amber)" opacity="0.7"/><text x="612" y="171" font-size="6.8" fill="var(--amber)">$30.00</text>
  <rect x="18" y="188" width="684" height="58" rx="9" fill="var(--code-bg)" stroke="var(--blue)"/>
  <text x="30" y="204" font-size="7.6" font-weight="700" fill="var(--blue)">how a model maps to a price? the matchPattern regex</text>
  <text x="30" y="221" font-size="7.2" font-family="monospace" fill="var(--code-ink)">usage.model = &quot;openai/gpt-4o&quot;</text>
  <text x="250" y="221" font-size="7.2" font-family="monospace" fill="var(--muted)">──match──▶</text>
  <text x="330" y="221" font-size="7" font-family="monospace" fill="var(--accent-ink)">(?i)^(openai/)?(gpt-4o)$</text>
  <text x="560" y="221" font-size="7.2" font-family="monospace" fill="var(--accent)">✓ → gpt-4o</text>
  <text x="30" y="238" font-size="6.8" fill="var(--faint)">prices stored per-token in pricingTiers[].prices.{input,output} (shown x1e6 as per-million); at ingestion the regex maps the model name to a price row</text>
</svg>
<div class="figcap"><b>Pricing is a "regex → per-token price" lookup table</b> (data from <code>worker/src/constants/default-model-prices.json</code>, <b>real prices</b>): each model stores <code>input</code>/<code>output</code> price <b>per token</b> under <code>pricingTiers[].prices</code> (shown x1e6 as "per million" for readability). On output price alone, <code>gpt-4-turbo</code> ($30) is <b>50x</b> <code>gpt-4o-mini</code> ($0.60) — model choice is a cost choice. How does a model name map to a price? Via the <code>matchPattern</code> regex: <code>&quot;openai/gpt-4o&quot;</code> matches <code>(?i)^(openai/)?(gpt-4o)$</code> and uses that row, so it bills correctly with or without the <code>openai/</code> prefix (used by Lesson 12's ingestion cost step).</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/constants/default-model-prices.json</span><span class="ln">one model entry (excerpt)</span></div>
  <pre class="code"><span class="cm">// one of 158 seed prices; matchPattern catches every alias</span>
{
  "modelName": <span class="st">"gpt-4o"</span>,
  "matchPattern": <span class="st">"(?i)^(openai/)?(gpt-4o)$"</span>,   <span class="cm">// matches gpt-4o / openai/gpt-4o / GPT-4O</span>
  "tokenizerId": <span class="st">"openai"</span>,                        <span class="cm">// if the SDK didn't report usage, count tokens with this tokenizer</span>
  "pricingTiers": [ { "name": <span class="st">"Standard"</span>, "isDefault": <span class="kw">true</span>, "conditions": [],
    "prices": { "input": 2.5e-6, "output": 1e-5,             <span class="cm">// per-token prices</span>
                "input_cached_tokens": 1.25e-6, … } } ]      <span class="cm">// line items: input/output/cache-read each priced</span>
}
<span class="cm">// an Anthropic matchPattern also includes us./eu./apac. region prefixes and -v1:0, @date version forms</span></pre>
</div>

<table class="t">
  <thead><tr><th>regex part</th><th>purpose</th><th>spellings it recognizes</th></tr></thead>
  <tbody>
    <tr><td><code>(?i)</code></td><td>case-insensitive</td><td>recognizes both gpt-4o and GPT-4O</td></tr>
    <tr><td><code>^…$</code></td><td>full-string match</td><td>avoids false hits (won't treat gpt-4o-mini as gpt-4o)</td></tr>
    <tr><td><code>(provider/)?</code></td><td>optional provider prefix</td><td>openai/gpt-4o, anthropic/claude-…</td></tr>
    <tr><td><code>(us\.|eu\.|apac\.)?</code></td><td>optional AWS region prefix</td><td>us.anthropic.claude-… (Bedrock)</td></tr>
    <tr><td><code>(:0)?</code> / <code>@date</code></td><td>optional version suffix</td><td>…-v1:0 (Bedrock), …@20240620 (Vertex)</td></tr>
  </tbody>
</table>
<p>These parts are like <strong>detachable Lego</strong>: when a platform adds a new naming quirk, just add an optional group to the regex—no need to rearrange the price table. One rule <strong>absorbs the naming differences of six platforms at the pattern layer</strong>.</p>
""")

# (en sec2/3/spark below)

_EN42.append(r"""
<h2>pricingTiers: a default tier + conditional tiers</h2>
<p>Pricing is often not flat. For the same model, a <strong>larger context window may cost more</strong>; some bill by usage steps. Langfuse uses <code>pricingTiers</code> for this tiering: each model has <strong>exactly one default tier</strong> (<code>isDefault=true</code>, <code>priority=0</code>, <code>conditions=[]</code>), plus any number of <strong>conditional tiers</strong> (with <code>conditions</code>, e.g. "input tokens &gt; 200K"). To pick, <code>matchPricingTier</code> evaluates conditional tiers <strong>in ascending priority</strong>, the <strong>first whose conditions all hold</strong> wins; if none, it <strong>falls back to the default tier</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 205" role="img" aria-label="Tier selection: a call's usage enters, matchPricingTier evaluates non-default conditional tiers in ascending priority, the first whose conditions all hold wins, else fall back to the default tier; the selected tier provides the prices list">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">pick a tier by usage: conditional first, fall back to default if none</text>
  <rect x="30" y="80" width="130" height="44" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">this call's usage</text><text x="95" y="115" text-anchor="middle" font-size="6.4" fill="var(--muted)">input=250k, output=8k</text>
  <rect x="200" y="44" width="300" height="36" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="350" y="61" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">conditional (priority 1): input &gt; 200000 ?</text><text x="350" y="73" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">holds ✓ → pick it (long-context price)</text>
  <rect x="200" y="88" width="300" height="32" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="350" y="105" text-anchor="middle" font-size="7.5" fill="var(--muted)">conditional (priority 2): … (prior one won, not tried)</text>
  <rect x="200" y="128" width="300" height="32" rx="8" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="350" y="148" text-anchor="middle" font-size="7.5" fill="var(--muted)">default (priority 0, conditions=[]): fallback when none hold</text>
  <rect x="540" y="80" width="150" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="615" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">the tier's prices</text><text x="615" y="115" text-anchor="middle" font-size="6.4" fill="var(--muted)">→ Lesson 16 cost</text>
  <line x1="160" y1="96" x2="198" y2="62" stroke="var(--accent)" stroke-width="1.4"/><polygon points="198,62 189,64 193,71" fill="var(--accent)"/>
  <line x1="500" y1="62" x2="538" y2="96" stroke="var(--teal)" stroke-width="1.5"/><polygon points="538,96 529,92 532,100" fill="var(--teal)"/>
  <text x="360" y="180" text-anchor="middle" font-size="8" fill="var(--faint)">conditions use AND logic (all must hold); operator supports gt/gte/lt/lte/eq/neq; first-come-first-served by ascending priority</text>
  <text x="360" y="195" text-anchor="middle" font-size="8" fill="var(--faint)">the default tier always exists and always backstops—guaranteeing any usage gets a price, never uncomputed</text>
</svg>
<div class="figcap"><b>tiered pricing, default backstop</b>: <code>matchPricingTier</code> (<code>pricing-tiers/matcher.ts:88</code>) filters out the default tier, evaluates conditional tiers in ascending <code>priority</code>, the first with <b>all conditions holding</b> (AND logic) wins, else falls back to default. A condition = <code>usageDetailPattern</code> (regex selecting a usage item) + <code>operator</code> (gt/gte/lt/lte/eq/neq) + <code>value</code>.</div>
</div>

<table class="t">
  <thead><tr><th>tier type</th><th>isDefault / priority / conditions</th><th>role</th></tr></thead>
  <tbody>
    <tr><td><b>default</b> (exactly one per model)</td><td>true / 0 / []</td><td>backstop price—any usage gets computed, never missed</td></tr>
    <tr><td><b>conditional</b> (any number)</td><td>false / ≥1 / has conditions</td><td>tier by context window/usage (e.g. "&gt;200K tokens → long-context price")</td></tr>
    <tr><td colspan="3" style="background:var(--blue-soft)"><b>selection rule</b>: evaluate conditional tiers in ascending priority, first with all conditions holding wins; none → default</td></tr>
  </tbody>
</table>
""")

_EN42.append(r"""
<h2>Put together: how a call's cost is computed</h2>
<p>Chaining matchPattern and pricingTiers restores Lesson 16's full "cost = usage × price" chain. The 158 seed prices in <code>default-model-prices.json</code> are loaded into the DB's Model/Price tables by <code>upsertDefaultModelPrices</code>; thereafter every call follows this pricing line:</p>

<svg viewBox="0 0 720 220" role="img" aria-label="a call's pricing line in five steps: 1 take the model name the observation reported, 2 match it with a matchPattern regex to a Model entry (with tokenizerId and pricingTiers), 3 if the SDK reported no usage, tokenize by tokenizerId to count tokens, 4 matchPricingTier picks the tier by usage to get prices, 5 multiply prices by usage per item and sum, giving total cost, restoring Lesson 16's cost equals usage times price">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="16" y="42" width="128" height="80" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="80" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">1 model name</text>
  <text x="80" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">us.anthropic</text>
  <text x="80" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">.claude-…</text>
  <rect x="156" y="42" width="128" height="80" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="220" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">2 match Model</text>
  <text x="220" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">matchPattern regex</text>
  <text x="220" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">→ tiers + tokenizer</text>
  <rect x="296" y="42" width="128" height="80" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">3 count tokens</text>
  <text x="360" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">(if SDK omitted)</text>
  <text x="360" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">tokenizerId</text>
  <rect x="436" y="42" width="128" height="80" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="500" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">4 pick tier</text>
  <text x="500" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">matchPricingTier</text>
  <text x="500" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">→ prices</text>
  <rect x="576" y="42" width="128" height="80" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="640" y="64" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">5 sum per item</text>
  <text x="640" y="84" font-size="8" text-anchor="middle" fill="var(--muted)">prices[i] × usage</text>
  <text x="640" y="98" font-size="8" text-anchor="middle" fill="var(--muted)">added up</text>
  <line x1="144" y1="82" x2="156" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="284" y1="82" x2="296" y2="82" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="424" y1="82" x2="436" y2="82" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="564" y1="82" x2="576" y2="82" stroke="var(--accent)" stroke-width="2"></line>
  <rect x="160" y="148" width="400" height="40" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="360" y="173" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">total cost = Σ(price per item × usage per item)</text>
  <line x1="640" y1="122" x2="440" y2="148" stroke="var(--teal)" stroke-width="1.5"></line>
  <text x="360" y="208" font-size="10" text-anchor="middle" fill="var(--muted)">restoring Lesson 16's full "cost = usage × price" chain</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>get the model name</h4><p>From an observation (generation), take its reported model name, e.g. <code>us.anthropic.claude-...-v1:0</code>.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>match the Model</h4><p>Test the name against each <code>matchPattern</code> regex; the hit is the price entry to use (with tokenizerId and pricingTiers).</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>(if needed) count tokens</h4><p>If the SDK didn't report usage, use the entry's <code>tokenizerId</code>/<code>tokenizerConfig</code> to tokenize the text and count tokens (Lesson 16).</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>select the tier</h4><p><code>matchPricingTier</code> picks the right tier by usage (default or conditional), yielding the <code>prices</code> list to use this time.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>itemized cost</h4><p>For each usage type (input/output/cache-read…) sum <code>prices[item] × usage</code>, giving the call's total cost.</p></div></div>
</div>

<p>One more layer of flexibility: these 158 are just <strong>Langfuse's built-in defaults</strong> (global Models with empty <code>projectId</code>). If you use a self-built model, a private deployment, or negotiated special discounts, you can <strong>add/override</strong> Model prices in your own project (project-scoped entries with a <code>projectId</code> take priority)—so the platform is both <strong>ready out of the box</strong> (mainstream model prices preloaded) and <strong>precisely fitted</strong> to your real bill. The repo skill <code>add-model-price</code> governs exactly how to safely add/edit entries in this seed file (generate a UUID, write the right matchPattern, validate the JSON).</p>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why match model names with regex rather than exact string equality?</strong> Because model naming in the ecosystem is <strong>maddeningly fragmented</strong>. The same Claude is <code>claude-3-5-sonnet</code> in OpenAI style, <code>us.anthropic.claude-3-5-sonnet-v1:0</code> on Bedrock, <code>claude-3-5-sonnet@20240620</code> on Vertex, plus permutations of casing and <code>provider/</code> prefixes—a model easily has a dozen valid spellings. With exact matching, you'd store one price entry per spelling, and adding a region or bumping a version means overhauling the whole table—maintenance explodes and misses abound. One carefully written regex <strong>converges these synonymous spellings into one intent</strong>: "however you call it, I know this is gpt-4o". <strong>Regex here isn't showing off but a necessity against naming fragmentation</strong>—it keeps "the world's chaos" outside the price table.<br><br>
  <strong>Why split pricing into "default + conditional tiers" rather than a flat price?</strong> Because real pricing <strong>is tiered</strong>: long context costs more, cache hits cost less, some usage jumps tiers above a threshold. Storing only a flat price would either miscompute or fill the billing code with if-else—<strong>hardcoding pricing policy into logic</strong>, so every price change means a code change and a release. Expressing tiering as <strong>data</strong> (a set of tiers with conditions) leaves the billing logic just one job: <strong>pick the right tier by usage</strong>, while "how tiers split, how prices are set" lives in data, adjustable anytime. Another win for "<strong>move policy from code into data</strong>"—the same lineage as Lesson 28's score config and Lesson 16's pricing schema: <strong>a rule expressible as data shouldn't be written into code</strong>. And the ever-present default tier is an elegant backstop: it guarantees <strong>any</strong> usage lands in some price, never failing to compute just because no condition matched.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>The pricing data model feeds Lesson 16's cost computation</strong>: <code>default-model-prices.json</code>'s 158 seed prices are upserted into the Model/Price tables, and every call computes "usage × price" from them.</li>
    <li><strong>matchPattern unifies naming</strong>: one case-insensitive, full-string regex per model catches all the spellings of OpenAI/Anthropic/Bedrock/Vertex/Azure/Gemini (provider prefix, region prefix, version suffix, @date).</li>
    <li><strong>pricingTiers tier pricing</strong>: exactly one default tier (backstop) + any conditional tiers; <code>matchPricingTier</code> evaluates conditions in ascending priority (AND logic, operators gt/gte/lt/lte/eq/neq), first all-holding wins, else default.</li>
    <li><strong>prices bills line-by-line</strong>: each usage type (input/output/cache-read…) has its own per-token price; cost = Σ(per-item price × per-item usage).</li>
    <li><strong>defaults + project override</strong>: 158 global defaults ready out of the box, projects can add <code>projectId</code>-scoped Models to override (self-built/private/discount prices). Policy in data not code—echoing Lessons 16/28's "rules as data".</li>
  </ul>
</div>
""")

LESSON_42 = {"zh": "\n".join(_ZH42), "en": "\n".join(_EN42)}


# ══════════════════════════════════════════════════════════════════════
# L43 · 云用量计量与花费 / Cloud usage metering & spend
# ══════════════════════════════════════════════════════════════════════
_ZH43 = []
_EN43 = []

_ZH43.append(r"""
<p class="lead">
前面讲的「成本」（第 16、42 课）是<strong>你的 LLM 花了多少</strong>。这一课讲<strong>另一笔账</strong>：你用 Langfuse 这个<strong>平台</strong>本身，平台怎么向你<strong>计量、收费</strong>。这是 <strong>Langfuse Cloud 特有</strong>的一环——自托管（self-host）版本<strong>不向你收费</strong>，所以这一课你可以当作「看看托管服务背后的计费是怎么搭的」。
重点有三：Langfuse Cloud 按<strong>观测数</strong>计量、用<strong>每小时一次的定时任务</strong>把用量上报给 <strong>Stripe</strong> 开账单，以及一个关乎钱的命门——<strong>「计量必须恰好一次」</strong>的幂等设计。钱算多了惹客户、算少了亏自己，所以这套计量对「不重不漏」的要求，比前面任何一条链路都严苛。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  云计量像小区里的<strong>「水表 + 抄表员」</strong>。你用平台就像用水，平台给你装了一块<strong>表</strong>，按用量（用量事件）默默地计。<strong>抄表员</strong>（每小时一次的定时任务）准点来抄一次<strong>这一小时</strong>的读数，把数字报给<strong>收费公司</strong>（Stripe），由它汇总成月度账单。
  最要命的是：抄表<strong>绝不能重复、也绝不能漏</strong>。抄两遍，你这个月水费翻倍、客户暴怒；漏一次，平台白送了一小时算力。所以抄表员手里攥着一本<strong>「上次抄到几点」的台账</strong>（一张带锁的 cron 记录），死死卡住「<strong>每个整点小时的用量，不多不少、恰好上报一次</strong>」——哪怕他中途打了个盹、网断了重来、或者不小心来了两个抄表员，这本台账都能保证账目分毫不乱。
</div>
""")

# (L43 sections below)

_ZH43.append(r"""
<h2>计量模型：每小时数一次观测，报给 Stripe</h2>
<p>Langfuse Cloud 按<strong>用量事件</strong>计费。计量任务（<code>handleCloudUsageMeteringJob</code>）由一个<strong>每小时触发</strong>的定时队列驱动：对刚过去的<strong>那个整点小时</strong>，从 ClickHouse 数出每个项目的 observation/trace/score 数，再按组织（organization）汇总，最后推给 <strong>Stripe 的计量 API</strong>——它上报<strong>两个 meter</strong>：<code>tracing_observations</code>（仅观测数，<strong>legacy</strong>）和 <code>tracing_events</code>（= trace + score + observation 之和，<strong>当前计费口径</strong>），由 Stripe 出账单。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="云计量流程：每小时定时任务对过去一小时区间，从 ClickHouse 数各项目的观测/trace/score 数，按组织汇总，对有 Stripe customerId 的组织调用 stripe.billing.meterEvents.create 上报 tracing_observations(legacy) 与 tracing_events 用量，由 Stripe 出账单">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">每小时计量：数观测 → 按组织汇总 → 报 Stripe</text>
  <rect x="20" y="80" width="120" height="48" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="80" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">每小时 cron</text><text x="80" y="116" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">CloudUsageMeteringJob</text>
  <rect x="170" y="68" width="150" height="72" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="245" y="88" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">数这一小时的用量</text><text x="245" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">getObservationCounts…</text><text x="245" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">getTrace / getScore Counts</text><text x="245" y="131" text-anchor="middle" font-size="6.5" fill="var(--faint)">按项目，来自 ClickHouse</text>
  <rect x="350" y="74" width="150" height="60" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="425" y="94" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">按 organization 汇总</text><text x="425" y="110" text-anchor="middle" font-size="6.5" fill="var(--muted)">仅有 Stripe customerId 的</text><text x="425" y="123" text-anchor="middle" font-size="6.5" fill="var(--faint)">∑ 各项目观测数</text>
  <rect x="530" y="74" width="170" height="60" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="615" y="94" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Stripe 计量 API</text><text x="615" y="110" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">meterEvents.create</text><text x="615" y="123" text-anchor="middle" font-size="6.2" fill="var(--muted)">tracing_events + obs(legacy)</text>
  <line x1="140" y1="104" x2="168" y2="104" stroke="var(--accent)" stroke-width="1.4"/><polygon points="168,104 159,100 159,108" fill="var(--accent)"/>
  <line x1="320" y1="104" x2="348" y2="104" stroke="var(--teal)" stroke-width="1.4"/><polygon points="348,104 339,100 339,108" fill="var(--teal)"/>
  <line x1="500" y1="104" x2="528" y2="104" stroke="var(--blue)" stroke-width="1.4"/><polygon points="528,104 519,100 519,108" fill="var(--blue)"/>
  <text x="360" y="170" text-anchor="middle" font-size="8" fill="var(--faint)">Stripe 拿到「某客户这一小时用了 N 个观测」的计量事件，月底汇总成发票——平台只管报数，开票交给专业的</text>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">上报包在 backOff 重试里：网络抖动也要保证这笔用量最终送达</text>
</svg>
<div class="figcap"><b>用量计量 → Stripe 出账</b>：<code>handleCloudUsageMeteringJob</code> 每小时对过去整点区间，用 <code>getObservation/Trace/ScoreCountsByProjectInCreationInterval</code> 从 ClickHouse 数量，按 org 汇总，对有 <code>cloudConfig.stripe.customerId</code> 的组织调 <code>meterEvents.create</code> 上报两个 meter——<code>tracing_observations</code>(legacy) 与 <code>tracing_events</code>(=trace+score+obs)（<code>backOff</code> 重试）。源码：<code>worker/src/ee/cloudUsageMetering/handleCloudUsageMeteringJob.ts</code>。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 268" role="img" aria-label="云用量计量真实例子：左边是按小时累计的计量（每个项目记 observations 数，按组织汇总），整月累计成一个总用量；右边是月末 Stripe 账单，分订阅(套餐)、用量(observations 计费)、税三类行项目，合计总额。结构取自 billing 的 getInvoices（subscription/usage/tax 分解），observations 为计费单位，金额为示例">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：用量计量 → 月末 Stripe 账单</text>
  <rect x="16" y="30" width="316" height="210" rx="9" fill="var(--bg)" stroke="var(--blue)"/>
  <text x="30" y="48" font-size="8.5" font-weight="700" fill="var(--blue)">用量计量 · per project → per org</text>
  <rect x="30" y="66" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="80" font-size="7" font-family="monospace" fill="var(--ink)">Jun 1 10:00</text><text x="308" y="80" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+1,240 obs</text>
  <rect x="30" y="92" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="106" font-size="7" font-family="monospace" fill="var(--ink)">Jun 1 11:00</text><text x="308" y="106" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+980 obs</text>
  <rect x="30" y="118" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="132" font-size="7" font-family="monospace" fill="var(--ink)">Jun 1 12:00</text><text x="308" y="132" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+1,510 obs</text>
  <rect x="30" y="144" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="158" font-size="7" font-family="monospace" fill="var(--ink)">…</text><text x="308" y="158" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">… obs</text>
  <rect x="30" y="170" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="184" font-size="7" font-family="monospace" fill="var(--ink)">Jun 30 23:00</text><text x="308" y="184" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+1,090 obs</text>
  <line x1="30" y1="198" x2="318" y2="198" stroke="var(--line)"/>
  <text x="40" y="216" font-size="8" font-weight="700" fill="var(--accent-ink)">Σ 6 月</text><text x="308" y="216" text-anchor="end" font-size="9" font-weight="800" fill="var(--accent-ink)">1,240,000 obs</text>
  <text x="352" y="120" text-anchor="middle" font-size="6.6" fill="var(--muted)">月末</text>
  <line x1="336" y1="130" x2="372" y2="130" stroke="var(--accent)" stroke-width="2"/><polygon points="372,130 364,125 364,135" fill="var(--accent)"/>
  <rect x="388" y="30" width="316" height="210" rx="9" fill="var(--bg)" stroke="var(--accent)"/>
  <text x="402" y="48" font-size="9" font-weight="700" fill="var(--accent-ink)">Stripe Invoice · 2026 年 6 月</text>
  <line x1="402" y1="54" x2="690" y2="54" stroke="var(--line)"/>
  <text x="402" y="72" font-size="7.8" fill="var(--ink)">订阅 · Team 套餐</text><text x="690" y="72" text-anchor="end" font-size="8" font-weight="700" fill="var(--ink)">$199.00</text>
  <text x="402" y="96" font-size="7.8" fill="var(--ink)">用量 · 1.24M events</text><text x="690" y="96" text-anchor="end" font-size="8" font-weight="700" fill="var(--ink)">$124.00</text>
  <text x="402" y="120" font-size="7.8" fill="var(--muted)">税 (tax)</text><text x="690" y="120" text-anchor="end" font-size="8" font-weight="700" fill="var(--muted)">$25.84</text>
  <text x="402" y="142" font-size="6.6" fill="var(--faint)">用量 = Σobs × 单价（按套餐阶梯，金额为示例）</text>
  <line x1="402" y1="154" x2="690" y2="154" stroke="var(--accent)"/>
  <rect x="396" y="160" width="300" height="30" rx="7" fill="var(--accent-soft)"/><text x="408" y="180" font-size="9.5" font-weight="700" fill="var(--accent-ink)">合计 Total</text><text x="688" y="180" text-anchor="end" font-size="12" font-weight="800" fill="var(--accent-ink)">$348.84</text>
  <text x="360" y="256" text-anchor="middle" font-size="7.2" fill="var(--muted)">平台只负责「数数」（每项目记 observations、按组织汇总）；真正开票、收税、扣款交给 Stripe</text>
</svg>
<div class="figcap"><b>平台数数，Stripe 开票</b>（结构取自 billing 的 <code>getInvoices</code>：subscription / usage / tax 分解；<b>金额为示例</b>）：用量按 <code>tracing_events</code>（trace+score+observation 之和）计费——每个<b>项目</b>按小时累计、再按<b>组织</b>汇总（图左以 obs 累计示意，整月 1.24M）。月末 Stripe 出一张账单，拆成<b>订阅</b>（固定套餐费）、<b>用量</b>（Σevents × 阶梯单价）、<b>税</b>三类行项目，合计扣款。这条「<b>计量与计费分离</b>」的边界很关键：平台专心准确地数数，发票、税务、支付这些又重又合规的事全甩给 Stripe。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/ee/cloudUsageMetering/handleCloudUsageMeteringJob.ts</span><span class="ln">数量 + 上报 Stripe</span></div>
  <pre class="code"><span class="cm">// 1) 对刚过去的整点小时，从 ClickHouse 数各项目用量</span>
<span class="kw">const</span> observationCounts = <span class="kw">await</span> getObservationCountsByProjectInCreationInterval({ start, end });

<span class="kw">for</span> (<span class="kw">const</span> org <span class="kw">of</span> organizations) {                  <span class="cm">// 仅含有 stripe.customerId 的组织</span>
  <span class="kw">const</span> countObservations = observationCounts<span class="cm">/* …该 org 各项目 */</span>.reduce((s, p) =&gt; s + p.count, 0);
  <span class="kw">if</span> (countObservations &gt; 0) {
    <span class="kw">await</span> backOff(() =&gt;                              <span class="cm">// 重试：保证最终送达</span>
      stripe.billing.meterEvents.create({
        event_name: <span class="st">"tracing_observations"</span>,
        timestamp: meterIntervalEnd.getTime() / 1000,
        payload: { stripe_customer_id, value: countObservations.toString() } }));  <span class="cm">// legacy meter</span>
  }
  <span class="cm">// 当前计费口径：events = traces + scores + observations</span>
  <span class="kw">const</span> countEvents = countScores + countTraces + countObservations;
  <span class="kw">if</span> (countEvents &gt; 0) <span class="kw">await</span> backOff(() =&gt;
    stripe.billing.meterEvents.create({ event_name: <span class="st">"tracing_events"</span>,
      timestamp: meterIntervalEnd.getTime() / 1000,
      payload: { stripe_customer_id, value: countEvents.toString() } }));
}</pre>
</div>

<table class="t">
  <thead><tr><th>这一小时数了什么</th><th>来源</th><th>是否用于计费</th></tr></thead>
  <tbody>
    <tr><td>观测数（observations）</td><td><code>getObservationCountsByProjectInCreationInterval</code></td><td><b>是</b>——单独上报 <code>tracing_observations</code>(legacy)，并计入 <code>tracing_events</code></td></tr>
    <tr><td>trace 数</td><td><code>getTraceCounts…</code></td><td><b>是</b>——计入 <code>tracing_events</code></td></tr>
    <tr><td>score 数</td><td><code>getScoreCounts…</code></td><td><b>是</b>——计入 <code>tracing_events</code></td></tr>
  </tbody>
</table>
<p>三种量都数，且都进账：计量上报<strong>两个 meter</strong>——<code>tracing_observations</code>（仅观测数，<strong>legacy</strong>、向后兼容）与 <code>tracing_events</code>（trace + score + observation 之和，<strong>当前计费口径</strong>）。也就是说 <strong>trace、score 同样计入计费</strong>（汇入 <code>tracing_events</code>），并非只是内部统计。计费单位从「纯观测数」演进为「用量事件之和」，仍保持<strong>按可观测操作的细颗粒度</strong>。</p>
""")

# (L43 sec2 idempotency below)

_ZH43.append(r"""
<h2>命门：计量必须「恰好一次」</h2>
<p>定时任务最怕<strong>重复执行</strong>和<strong>中途崩溃</strong>——但对计费来说，这两样都是灾难：重复上报，客户被双倍收费；漏报，平台白送算力。所以计量任务用一张 <code>cronJobs</code> 表当<strong>分布式锁 + 进度台账</strong>，把「恰好一次」焊死。它做三件事：<strong>对齐整点</strong>（区间严格按小时切，<code>lastRun</code> 记到哪个整点）、<strong>互斥锁</strong>（<code>state=Processing</code> 期间别的实例不许进）、<strong>兜底解锁</strong>（锁超过 20 分钟没释放，判定上个任务崩了、强制接管）。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="幂等三道闸：cronJobs 表记录 lastRun 对齐整点小时、state=Processing 互斥锁防并发重复、jobStartedAt 超过20分钟判定崩溃强制接管；三者保证每个小时区间恰好计量一次">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">cronJobs 表：把「恰好一次」焊死的三道闸</text>
  <rect x="40" y="44" width="640" height="34" rx="7" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="65" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">cronJobs 表：lastRun（已计到哪个整点）· state（Processing?）· jobStartedAt（何时开工）</text>
  <rect x="40" y="96" width="200" height="96" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="140" y="116" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">闸1 · 对齐整点</text><text x="140" y="134" text-anchor="middle" font-size="6.6" fill="var(--muted)">区间 = [lastRun, +1h)</text><text x="140" y="148" text-anchor="middle" font-size="6.6" fill="var(--muted)">严格小时边界对齐</text><text x="140" y="168" text-anchor="middle" font-size="6.5" fill="var(--faint)">同一小时不会算两遍</text>
  <rect x="260" y="96" width="200" height="96" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="116" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">闸2 · 互斥锁</text><text x="360" y="134" text-anchor="middle" font-size="6.6" fill="var(--muted)">state=Processing 期间</text><text x="360" y="148" text-anchor="middle" font-size="6.6" fill="var(--muted)">别的实例不许进</text><text x="360" y="168" text-anchor="middle" font-size="6.5" fill="var(--faint)">防并发重复上报</text>
  <rect x="480" y="96" width="200" height="96" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="580" y="116" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">闸3 · 兜底解锁</text><text x="580" y="134" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">锁 &gt; 20 分钟未释放</text><text x="580" y="148" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">判定上个任务崩了</text><text x="580" y="168" text-anchor="middle" font-size="6.5" fill="var(--muted)">强制接管，不会永久卡死</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">重复执行被锁挡、崩溃被兜底接管、区间按整点对齐——三道闸合力，让每个小时的用量「不重不漏，恰好一次」</text>
</svg>
<div class="figcap"><b>「恰好一次」靠数据库锁兜底</b>：<code>handleCloudUsageMeteringJob</code> 用 <code>prisma.cronJobs.upsert</code> 维护 <code>lastRun</code>/<code>state</code>/<code>jobStartedAt</code>：区间严格对齐整点（<code>lastRun % 3600000 === 0</code>）、<code>state=Processing</code> 互斥、<code>jobStartedAt</code> 超 <code>1200000</code>ms（20 分钟）判定崩溃强制接管。重复或崩溃都不会让某小时多算或漏算。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/ee/cloudUsageMetering/handleCloudUsageMeteringJob.ts</span><span class="ln">cronJobs 幂等锁</span></div>
  <pre class="code"><span class="cm">// 取/建 cron 记录（分布式锁 + 进度台账）</span>
<span class="kw">const</span> cron = <span class="kw">await</span> prisma.cronJobs.upsert({ … });

<span class="cm">// 闸1：区间严格对齐整点小时（避免错位重叠/漏算）</span>
<span class="kw">if</span> (cron.lastRun.getTime() % <span class="st">3600000</span> !== 0) { <span class="cm">/* 异常，不处理 */</span> }
<span class="kw">const</span> meterIntervalStart = cron.lastRun;
<span class="kw">const</span> meterIntervalEnd = <span class="kw">new</span> Date(cron.lastRun.getTime() + <span class="st">3600000</span>);  <span class="cm">// 正好 1 小时</span>

<span class="cm">// 闸2+3：Processing 互斥；但 jobStartedAt 超 20 分钟视为上个任务崩了，强制接管</span>
<span class="kw">if</span> (cron.state === <span class="st">Processing</span> &amp;&amp;
    cron.jobStartedAt &gt;= <span class="kw">new</span> Date(Date.now() - <span class="st">1200000</span>)) { <span class="cm">/* 别人在跑，退出 */</span> }</pre>
</div>

<table class="t">
  <thead><tr><th>威胁</th><th>会造成</th><th>这道闸怎么挡</th></tr></thead>
  <tbody>
    <tr><td>同一区间被算两遍</td><td>客户被双倍收费</td><td>区间严格对齐整点（<code>lastRun%3600000===0</code>），同一小时只处理一次</td></tr>
    <tr><td>两个实例并发跑</td><td>重复上报</td><td><code>state=Processing</code> 互斥锁，后来者直接退出</td></tr>
    <tr><td>任务中途崩溃</td><td>锁永久卡死、之后全漏算</td><td><code>jobStartedAt</code> 超 20 分钟视为崩溃，强制接管续算</td></tr>
  </tbody>
</table>
<p>三道闸各防一种现实威胁，合起来把抽象的「精确一次」落成了<strong>三个具体、可测的不变量</strong>。这比空谈「我们保证 exactly-once」靠谱得多——<strong>把保证拆成能写进测试的具体条件</strong>，正是计费这种零容错系统该有的工程姿态。</p>
""")

# (L43 sec3 spend below)

_ZH43.append(r"""
<h2>两本不同的账：平台计费 vs 你的花费告警</h2>
<p>容易混淆的是：Part 8 里出现了<strong>两种「钱」</strong>，方向正好相反。一种是<strong>平台向你收费</strong>（本课的计量，按用量事件报 Stripe）；另一种是<strong>你自己的 LLM 花费</strong>（第 16、42 课算出的成本）。后者还配了一个 <strong>花费告警（cloudSpendAlert）</strong>队列：盯着你这个月在各家 provider 上的 LLM 开销，越过你设的阈值就提醒你——这是帮<strong>你</strong>管好<strong>你的</strong>钱，和平台怎么收你的费是两码事。</p>

<svg viewBox="0 0 720 220" role="img" aria-label="Part 8 里两种方向相反的钱：① 平台计费，方向是平台向你收费，按用量事件每小时报 Stripe，走 cloudUsageMeteringQueue 讲究恰好一次；② 花费告警，方向是帮你管你的 LLM 花费，盯你在各 provider 的成本，走 cloudSpendAlertQueue，越过阈值就告警；自托管没有①不收平台费，但②那样的成本观测照用">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="24" y="42" width="322" height="132" rx="10" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="185" y="64" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">① 平台计费（平台 → 收你的费）</text>
  <text x="40" y="90" font-size="9.5" fill="var(--ink)">方向：平台 → 收你的费</text>
  <text x="40" y="110" font-size="9.5" fill="var(--ink)">按用量事件 / 每小时报 Stripe</text>
  <text x="40" y="130" font-size="9.5" fill="var(--muted)">cloudUsageMeteringQueue</text>
  <text x="40" y="150" font-size="9.5" fill="var(--muted)">讲究「恰好一次」</text>
  <text x="360" y="108" font-size="14" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">↔</text>
  <text x="360" y="126" font-size="9" text-anchor="middle" fill="var(--muted)">方向相反</text>
  <rect x="374" y="42" width="322" height="132" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="535" y="64" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">② 花费告警（帮你 → 管你的钱）</text>
  <text x="390" y="90" font-size="9.5" fill="var(--ink)">方向：帮你 → 管你的 LLM 花费</text>
  <text x="390" y="110" font-size="9.5" fill="var(--ink)">盯你在 OpenAI/Anthropic 的成本</text>
  <text x="390" y="130" font-size="9.5" fill="var(--muted)">cloudSpendAlertQueue</text>
  <text x="390" y="150" font-size="9.5" fill="var(--muted)">越过阈值就告警（L16/42 成本）</text>
  <text x="360" y="200" font-size="10" text-anchor="middle" fill="var(--muted)">自托管：没有 ①（不收平台费），但 ② 那样的成本观测照用</text>
</svg>

<div class="cols">
  <div class="col"><h4>① 平台计量（本课主线）</h4><p>方向：平台 → 收你的费。按<strong>用量事件</strong>每小时报 Stripe，Cloud 专属。<code>cloudUsageMeteringQueue</code>。讲究「恰好一次」。</p></div>
  <div class="col"><h4>② 花费告警（cloudSpendAlert）</h4><p>方向：帮你 → 管你的 LLM 花费。盯你在 OpenAI/Anthropic 等的成本，越阈值就告警。<code>cloudSpendAlertQueue</code>（CloudSpendAlertJob）。</p></div>
  <div class="col"><h4>③ 自托管（self-host）</h4><p>没有①——自己部署 Langfuse <strong>不向你收平台费</strong>。但②那样的成本观测、第 16/42 课的成本计算照样能用，你的 LLM 花了多少一样看得清。</p></div>
</div>

<p>把这条线收个尾：Part 8 从第 40 课「把数据聚合成图」一路走到这里，本质是回答<strong>「看清并管住数字」</strong>这件事——仪表盘看趋势、查询引擎统一口径、定价模型算清成本，而这一课，是把其中一类数字（用量）<strong>变成真金白银的账单</strong>。它也顺势揭开了 Langfuse 作为一门<strong>云生意</strong>的内里：开源可自托管（不收费），云托管按用量计费（这套 Stripe 计量）——技术与商业，在这台 worker 上严丝合缝地咬合。</p>
""")

_ZH43.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么计量任务要为「恰好一次」下这么大功夫——对齐整点、加锁、还要兜底解锁？</strong> 因为<strong>这是钱</strong>，而钱对错误的容忍度是零。前面所有链路，偶尔多算一条 trace、漏掉一个 score，大多无伤大雅、下次自愈。但计费不一样：<strong>多上报一小时用量，客户的信用卡就被多刷一次</strong>，是会上投诉、上推特的事故；少报，则是平台实打实的亏损。普通后台任务追求「最终一致」就够了，计量任务却必须做到<strong>「精确一次」（exactly-once）</strong>——这是分布式系统里出了名难啃的保证。Langfuse 的解法很务实：不去追求理论上完美的精确一次，而是用一张<strong>数据库行当锁</strong>，把三种现实威胁逐一堵死——重复执行（互斥锁挡）、任务崩溃（20 分钟兜底接管）、区间错位（严格对齐整点）。<strong>把「精确一次」拆解成几个可落地的具体防护，而非空谈理论保证</strong>，这是工程的智慧。<br><br>
  <strong>为什么按「用量事件」而不是 token 数计费？</strong> 这是个有意思的产品取舍。按 <strong>token</strong> 计费会和你用的模型强绑定（贵模型 token 多），且和 Langfuse 提供的价值不直接相关——Langfuse 的价值是<strong>记录和分析</strong>，不是替你跑模型。按 <strong>trace</strong> 又太粗：一个 trace 可能含一步、也可能含上百步观测。所以 Langfuse 选了<strong>细颗粒度的「可观测操作」</strong>作单位：早期只数 observation（<code>tracing_observations</code>，至今保留为 legacy），现已演进为 <code>tracing_events</code>＝trace + score + observation 之和。无论哪种，复杂应用产生的事件多、付得也多，简单的少付，<strong>计费颗粒度与平台提供的价值对齐</strong>。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>这是 Cloud 专属的平台计费</strong>：和你的 LLM 成本（第 16/42 课）是两笔反向的账；自托管不收平台费，可只看作「托管计费如何搭建」。</li>
    <li><strong>按用量事件计量</strong>：每小时定时任务从 ClickHouse 数各 org 的 obs/trace/score 数，对有 Stripe customerId 的组织调 <code>meterEvents.create</code> 上报两个 meter（<code>tracing_observations</code> legacy + <code>tracing_events</code>＝三者之和，<code>backOff</code> 重试），由 Stripe 出账。</li>
    <li><strong>「恰好一次」是命门</strong>：用 <code>cronJobs</code> 表当分布式锁+台账——区间严格对齐整点、<code>Processing</code> 互斥、20 分钟兜底接管，让每小时用量不重不漏。</li>
    <li><strong>计费要精确一次</strong>：钱对错误零容忍，普通任务的「最终一致」不够；把 exactly-once 拆成「防重复+防崩溃+防错位」三道可落地的具体防护。</li>
    <li><strong>用量事件是对齐价值的计费单位</strong>（<code>tracing_events</code>=trace+score+observation，<code>tracing_observations</code> 为 legacy）：比 token（绑模型）更贴合「Langfuse 帮你记录分析了多少」——客户付的钱正比于得到的价值。另有 <code>cloudSpendAlert</code> 帮你管自己的 LLM 花费。</li>
  </ul>
</div>
""")

_EN43.append(r"""
<p class="lead">
The "cost" discussed earlier (Lessons 16, 42) is <strong>how much your LLM spent</strong>. This lesson is about <strong>a different ledger</strong>: how the Langfuse <strong>platform itself</strong> <strong>meters and charges</strong> you for using it. This is <strong>Langfuse Cloud-specific</strong>—the self-hosted version <strong>does not charge you</strong>, so you can read this lesson as "a look at how a managed service's billing is built".
Three focuses: Langfuse Cloud meters by <strong>observation count</strong>, uses an <strong>hourly scheduled job</strong> to report usage to <strong>Stripe</strong> for invoicing, and a money-critical concern—the <strong>"meter exactly once"</strong> idempotency design. Over-count and you anger customers, under-count and you lose money, so this metering's demand for "no duplicates, no misses" is stricter than any chain before it.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Cloud metering is like a residential <strong>"water meter + meter reader"</strong>. Using the platform is like using water; the platform installs a <strong>meter</strong> that quietly counts by usage (usage events). The <strong>meter reader</strong> (an hourly scheduled job) shows up on time to read <strong>that hour's</strong> figure, reporting it to the <strong>billing company</strong> (Stripe), which rolls it into a monthly invoice.
  The critical part: a reading <strong>must never duplicate, never miss</strong>. Read twice and your water bill doubles this month—an enraged customer; miss one and the platform gives away an hour of compute for free. So the reader clutches a <strong>"where did I read up to" ledger</strong> (a locked cron record), rigidly enforcing "<strong>each whole hour's usage is reported exactly once, no more, no less</strong>"—even if he dozes off mid-read, the network drops and he restarts, or two readers accidentally show up, this ledger keeps the books flawless.
</div>
""")

_EN43.append(r"""
<h2>The metering model: count observations hourly, report to Stripe</h2>
<p>Langfuse Cloud bills by <strong>usage events</strong>. The metering job (<code>handleCloudUsageMeteringJob</code>) is driven by an <strong>hourly-triggered</strong> scheduled queue: for the <strong>just-passed whole hour</strong>, it counts each project's observation/trace/score counts from ClickHouse, aggregates by organization, and pushes them to <strong>Stripe's metering API</strong> — reporting <strong>two meters</strong>: <code>tracing_observations</code> (observation count only, <strong>legacy</strong>) and <code>tracing_events</code> (= trace + score + observation, the <strong>current billing unit</strong>), leaving Stripe to invoice.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="Cloud metering flow: an hourly scheduled job, for the past hour interval, counts each project's observation/trace/score counts from ClickHouse, aggregates by organization, and for orgs with a Stripe customerId calls stripe.billing.meterEvents.create to report tracing_observations(legacy) and tracing_events usage, with Stripe invoicing">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">hourly metering: count observations → aggregate by org → report to Stripe</text>
  <rect x="20" y="80" width="120" height="48" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="80" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">hourly cron</text><text x="80" y="116" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">CloudUsageMeteringJob</text>
  <rect x="170" y="68" width="150" height="72" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="245" y="88" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">count this hour's usage</text><text x="245" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">getObservationCounts…</text><text x="245" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">getTrace / getScore Counts</text><text x="245" y="131" text-anchor="middle" font-size="6.2" fill="var(--faint)">per project, from ClickHouse</text>
  <rect x="350" y="74" width="150" height="60" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="425" y="94" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">aggregate by organization</text><text x="425" y="110" text-anchor="middle" font-size="6.2" fill="var(--muted)">only those with a Stripe customerId</text><text x="425" y="123" text-anchor="middle" font-size="6.2" fill="var(--faint)">∑ each project's observations</text>
  <rect x="530" y="74" width="170" height="60" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="615" y="94" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Stripe metering API</text><text x="615" y="110" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">meterEvents.create</text><text x="615" y="123" text-anchor="middle" font-size="6.0" fill="var(--muted)">tracing_events + obs(legacy)</text>
  <line x1="140" y1="104" x2="168" y2="104" stroke="var(--accent)" stroke-width="1.4"/><polygon points="168,104 159,100 159,108" fill="var(--accent)"/>
  <line x1="320" y1="104" x2="348" y2="104" stroke="var(--teal)" stroke-width="1.4"/><polygon points="348,104 339,100 339,108" fill="var(--teal)"/>
  <line x1="500" y1="104" x2="528" y2="104" stroke="var(--blue)" stroke-width="1.4"/><polygon points="528,104 519,100 519,108" fill="var(--blue)"/>
  <text x="360" y="170" text-anchor="middle" font-size="8" fill="var(--faint)">Stripe receives "N observations this hour" metering events → invoice at month end; the platform reports counts, invoicing left to the specialist</text>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">the report is wrapped in backOff retry: even network blips must let this usage eventually arrive</text>
</svg>
<div class="figcap"><b>usage metering → Stripe invoicing</b>: <code>handleCloudUsageMeteringJob</code> hourly counts the past whole-hour interval via <code>getObservation/Trace/ScoreCountsByProjectInCreationInterval</code> from ClickHouse, aggregates by org, and for orgs with a <code>cloudConfig.stripe.customerId</code> calls <code>meterEvents.create</code> reporting two meters — <code>tracing_observations</code>(legacy) and <code>tracing_events</code>(=trace+score+obs) (<code>backOff</code> retry). Source: <code>worker/src/ee/cloudUsageMetering/handleCloudUsageMeteringJob.ts</code>.</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 268" role="img" aria-label="Cloud usage-metering real example: left is hourly metering accumulating (each project counts observations, aggregated per organization) into a monthly total; right is the month-end Stripe invoice broken into subscription (plan), usage (observations billing) and tax line items, summing to a total. Structure from billing getInvoices (subscription/usage/tax breakdown), observations as the billing unit, amounts illustrative">
  <text x="360" y="18" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: usage metering → month-end Stripe invoice</text>
  <rect x="16" y="30" width="316" height="210" rx="9" fill="var(--bg)" stroke="var(--blue)"/>
  <text x="30" y="48" font-size="8.5" font-weight="700" fill="var(--blue)">usage metering · per project → per org</text>
  <rect x="30" y="66" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="80" font-size="7" font-family="monospace" fill="var(--ink)">Jun 1 10:00</text><text x="308" y="80" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+1,240 obs</text>
  <rect x="30" y="92" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="106" font-size="7" font-family="monospace" fill="var(--ink)">Jun 1 11:00</text><text x="308" y="106" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+980 obs</text>
  <rect x="30" y="118" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="132" font-size="7" font-family="monospace" fill="var(--ink)">Jun 1 12:00</text><text x="308" y="132" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+1,510 obs</text>
  <rect x="30" y="144" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="158" font-size="7" font-family="monospace" fill="var(--ink)">…</text><text x="308" y="158" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">… obs</text>
  <rect x="30" y="170" width="288" height="20" rx="5" fill="var(--panel-2)"/><text x="40" y="184" font-size="7" font-family="monospace" fill="var(--ink)">Jun 30 23:00</text><text x="308" y="184" text-anchor="end" font-size="7" font-weight="700" fill="var(--blue)">+1,090 obs</text>
  <line x1="30" y1="198" x2="318" y2="198" stroke="var(--line)"/>
  <text x="40" y="216" font-size="8" font-weight="700" fill="var(--accent-ink)">Σ June</text><text x="308" y="216" text-anchor="end" font-size="9" font-weight="800" fill="var(--accent-ink)">1,240,000 obs</text>
  <text x="352" y="120" text-anchor="middle" font-size="6.6" fill="var(--muted)">month end</text>
  <line x1="336" y1="130" x2="372" y2="130" stroke="var(--accent)" stroke-width="2"/><polygon points="372,130 364,125 364,135" fill="var(--accent)"/>
  <rect x="388" y="30" width="316" height="210" rx="9" fill="var(--bg)" stroke="var(--accent)"/>
  <text x="402" y="48" font-size="9" font-weight="700" fill="var(--accent-ink)">Stripe Invoice · June 2026</text>
  <line x1="402" y1="54" x2="690" y2="54" stroke="var(--line)"/>
  <text x="402" y="72" font-size="7.8" fill="var(--ink)">subscription · Team plan</text><text x="690" y="72" text-anchor="end" font-size="8" font-weight="700" fill="var(--ink)">$199.00</text>
  <text x="402" y="96" font-size="7.8" fill="var(--ink)">usage · 1.24M events</text><text x="690" y="96" text-anchor="end" font-size="8" font-weight="700" fill="var(--ink)">$124.00</text>
  <text x="402" y="120" font-size="7.8" fill="var(--muted)">tax</text><text x="690" y="120" text-anchor="end" font-size="8" font-weight="700" fill="var(--muted)">$25.84</text>
  <text x="402" y="142" font-size="6.6" fill="var(--faint)">usage = Σevents × unit price (per plan tier; illustrative)</text>
  <line x1="402" y1="154" x2="690" y2="154" stroke="var(--accent)"/>
  <rect x="396" y="160" width="300" height="30" rx="7" fill="var(--accent-soft)"/><text x="408" y="180" font-size="9.5" font-weight="700" fill="var(--accent-ink)">Total due</text><text x="688" y="180" text-anchor="end" font-size="12" font-weight="800" fill="var(--accent-ink)">$348.84</text>
  <text x="360" y="256" text-anchor="middle" font-size="7.2" fill="var(--muted)">the platform only counts (observations per project, aggregated per org); Stripe does the actual invoicing, tax and charging</text>
</svg>
<div class="figcap"><b>The platform counts, Stripe invoices</b> (structure from billing's <code>getInvoices</code>: subscription / usage / tax breakdown; <b>amounts illustrative</b>): usage is billed via <code>tracing_events</code> (trace+score+observation) — each <b>project</b> accumulates them hourly, then they aggregate per <b>organization</b> into a monthly total (1.24M obs illustrative on the left). At month end Stripe issues one invoice split into <b>subscription</b> (fixed plan fee), <b>usage</b> (Σevents × tiered unit price) and <b>tax</b> line items, charged as a total. This "<b>metering separate from billing</b>" boundary matters: the platform focuses on counting accurately, and hands the heavy, compliance-laden invoicing, tax and payments entirely to Stripe.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/ee/cloudUsageMetering/handleCloudUsageMeteringJob.ts</span><span class="ln">count + report to Stripe</span></div>
  <pre class="code"><span class="cm">// 1) for the just-passed whole hour, count each project's usage from ClickHouse</span>
<span class="kw">const</span> observationCounts = <span class="kw">await</span> getObservationCountsByProjectInCreationInterval({ start, end });

<span class="kw">for</span> (<span class="kw">const</span> org <span class="kw">of</span> organizations) {                  <span class="cm">// only orgs with a stripe.customerId</span>
  <span class="kw">const</span> countObservations = observationCounts<span class="cm">/* …this org's projects */</span>.reduce((s, p) =&gt; s + p.count, 0);
  <span class="kw">if</span> (countObservations &gt; 0) {
    <span class="kw">await</span> backOff(() =&gt;                              <span class="cm">// retry: guarantee eventual delivery</span>
      stripe.billing.meterEvents.create({
        event_name: <span class="st">"tracing_observations"</span>,
        timestamp: meterIntervalEnd.getTime() / 1000,
        payload: { stripe_customer_id, value: countObservations.toString() } }));  <span class="cm">// legacy meter</span>
  }
  <span class="cm">// current billing unit: events = traces + scores + observations</span>
  <span class="kw">const</span> countEvents = countScores + countTraces + countObservations;
  <span class="kw">if</span> (countEvents &gt; 0) <span class="kw">await</span> backOff(() =&gt;
    stripe.billing.meterEvents.create({ event_name: <span class="st">"tracing_events"</span>,
      timestamp: meterIntervalEnd.getTime() / 1000,
      payload: { stripe_customer_id, value: countEvents.toString() } }));
}</pre>
</div>

<table class="t">
  <thead><tr><th>what's counted this hour</th><th>source</th><th>used for billing?</th></tr></thead>
  <tbody>
    <tr><td>observation count</td><td><code>getObservationCountsByProjectInCreationInterval</code></td><td><b>yes</b> — reported alone as <code>tracing_observations</code>(legacy), and summed into <code>tracing_events</code></td></tr>
    <tr><td>trace count</td><td><code>getTraceCounts…</code></td><td><b>yes</b> — summed into <code>tracing_events</code></td></tr>
    <tr><td>score count</td><td><code>getScoreCounts…</code></td><td><b>yes</b> — summed into <code>tracing_events</code></td></tr>
  </tbody>
</table>
<p>All three are counted, and all three are billed: metering reports <strong>two meters</strong> — <code>tracing_observations</code> (observation count only, <strong>legacy</strong>, kept for backward compat) and <code>tracing_events</code> (trace + score + observation, the <strong>current billing unit</strong>). So <strong>trace and score counts do count toward billing</strong> (folded into <code>tracing_events</code>), not just internal stats. The billing unit evolved from "observations only" to "the sum of usage events," still at the <strong>fine granularity of one observable operation</strong>.</p>
""")

# (en sec2/3/spark below)

_EN43.append(r"""
<h2>The crux: metering must be "exactly once"</h2>
<p>A scheduled job most fears <strong>duplicate execution</strong> and <strong>crashing mid-way</strong>—but for billing, both are disasters: a duplicate report double-charges the customer; a miss gives away compute. So the metering job uses a <code>cronJobs</code> table as a <strong>distributed lock + progress ledger</strong>, welding "exactly once" shut. It does three things: <strong>align to the hour</strong> (intervals strictly cut by hour, <code>lastRun</code> records which hour), <strong>mutual exclusion</strong> (during <code>state=Processing</code>, another instance may not enter), and <strong>fallback unlock</strong> (if the lock is held over 20 minutes, deem the prior job crashed and forcibly take over).</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="Three idempotency gates: the cronJobs table records lastRun aligned to whole hours, state=Processing as a mutex preventing concurrent duplicates, and jobStartedAt over 20 minutes deemed a crash forcing takeover; together they ensure each hour interval is metered exactly once">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">cronJobs table: three gates welding "exactly once" shut</text>
  <rect x="40" y="44" width="640" height="34" rx="7" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="65" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">cronJobs table: lastRun (metered up to which hour) · state (Processing?) · jobStartedAt (when started)</text>
  <rect x="40" y="96" width="200" height="96" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="140" y="116" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">gate1 · align to hour</text><text x="140" y="134" text-anchor="middle" font-size="6.6" fill="var(--muted)">interval = [lastRun, +1h)</text><text x="140" y="148" text-anchor="middle" font-size="6.6" fill="var(--muted)">strict hour-boundary aligned</text><text x="140" y="168" text-anchor="middle" font-size="6.4" fill="var(--faint)">no hour counted twice</text>
  <rect x="260" y="96" width="200" height="96" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="116" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">gate2 · mutex</text><text x="360" y="134" text-anchor="middle" font-size="6.6" fill="var(--muted)">while state=Processing</text><text x="360" y="148" text-anchor="middle" font-size="6.6" fill="var(--muted)">other instances may not enter</text><text x="360" y="168" text-anchor="middle" font-size="6.4" fill="var(--faint)">prevents concurrent duplicate reports</text>
  <rect x="480" y="96" width="200" height="96" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="580" y="116" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">gate3 · fallback unlock</text><text x="580" y="134" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">lock held &gt; 20 minutes</text><text x="580" y="148" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">deem prior job crashed</text><text x="580" y="168" text-anchor="middle" font-size="6.4" fill="var(--muted)">forcibly take over, never stuck forever</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">duplicates blocked by the lock, crashes recovered by fallback, intervals aligned to the hour—three gates together make each hour's usage "no dup, no miss, exactly once"</text>
</svg>
<div class="figcap"><b>"exactly once" backstopped by a DB lock</b>: <code>handleCloudUsageMeteringJob</code> maintains <code>lastRun</code>/<code>state</code>/<code>jobStartedAt</code> via <code>prisma.cronJobs.upsert</code>: intervals strictly hour-aligned (<code>lastRun % 3600000 === 0</code>), <code>state=Processing</code> mutex, <code>jobStartedAt</code> over <code>1200000</code>ms (20 min) deemed crashed and forcibly taken over. Neither a duplicate nor a crash makes an hour over- or under-counted.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/ee/cloudUsageMetering/handleCloudUsageMeteringJob.ts</span><span class="ln">cronJobs idempotency lock</span></div>
  <pre class="code"><span class="cm">// get/create the cron record (distributed lock + progress ledger)</span>
<span class="kw">const</span> cron = <span class="kw">await</span> prisma.cronJobs.upsert({ … });

<span class="cm">// gate1: interval strictly aligned to a whole hour (avoid misaligned overlap/gaps)</span>
<span class="kw">if</span> (cron.lastRun.getTime() % <span class="st">3600000</span> !== 0) { <span class="cm">/* anomaly, don't process */</span> }
<span class="kw">const</span> meterIntervalStart = cron.lastRun;
<span class="kw">const</span> meterIntervalEnd = <span class="kw">new</span> Date(cron.lastRun.getTime() + <span class="st">3600000</span>);  <span class="cm">// exactly 1 hour</span>

<span class="cm">// gate2+3: Processing mutex; but jobStartedAt over 20 min = prior job crashed, take over</span>
<span class="kw">if</span> (cron.state === <span class="st">Processing</span> &amp;&amp;
    cron.jobStartedAt &gt;= <span class="kw">new</span> Date(Date.now() - <span class="st">1200000</span>)) { <span class="cm">/* someone's running, exit */</span> }</pre>
</div>

<table class="t">
  <thead><tr><th>threat</th><th>would cause</th><th>how this gate blocks it</th></tr></thead>
  <tbody>
    <tr><td>the same interval counted twice</td><td>customer double-charged</td><td>intervals strictly hour-aligned (<code>lastRun%3600000===0</code>), each hour processed once</td></tr>
    <tr><td>two instances running concurrently</td><td>duplicate reports</td><td><code>state=Processing</code> mutex, the latecomer exits</td></tr>
    <tr><td>the job crashing mid-way</td><td>lock stuck forever, all later misses</td><td><code>jobStartedAt</code> over 20 min deemed a crash, forcibly taken over to resume</td></tr>
  </tbody>
</table>
<p>Each gate guards one real threat; together they ground abstract "exactly once" into <strong>three concrete, testable invariants</strong>. That's far more reliable than vaguely claiming "we guarantee exactly-once"—<strong>decomposing the guarantee into conditions you can write tests for</strong> is exactly the engineering posture a zero-tolerance billing system deserves.</p>
""")

_EN43.append(r"""
<h2>Two different ledgers: platform billing vs your spend alerts</h2>
<p>Easily confused: Part 8 features <strong>two kinds of "money"</strong>, in opposite directions. One is <strong>the platform charging you</strong> (this lesson's metering, reporting usage events to Stripe); the other is <strong>your own LLM spend</strong> (the cost computed in Lessons 16, 42). The latter has a <strong>spend-alert (cloudSpendAlert)</strong> queue: it watches your monthly LLM spend across providers and pings you when it crosses a threshold you set—helping <strong>you</strong> manage <strong>your</strong> money, a separate matter from how the platform bills you.</p>

<svg viewBox="0 0 720 220" role="img" aria-label="two kinds of money in opposite directions: 1 platform billing, the platform charges you, reporting observation counts hourly to Stripe via cloudUsageMeteringQueue with exactly-once care; 2 spend alerts, helping you manage your LLM spend, watching your provider costs via cloudSpendAlertQueue and pinging you over a threshold; self-host has no 1 (no platform fee) but still uses 2-style cost observation">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <rect x="24" y="42" width="322" height="132" rx="10" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="185" y="64" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">1 platform billing (platform → charges you)</text>
  <text x="40" y="90" font-size="9.5" fill="var(--ink)">direction: platform → charges you</text>
  <text x="40" y="110" font-size="9.5" fill="var(--ink)">by usage events / hourly → Stripe</text>
  <text x="40" y="130" font-size="9.5" fill="var(--muted)">cloudUsageMeteringQueue</text>
  <text x="40" y="150" font-size="9.5" fill="var(--muted)">cares about "exactly once"</text>
  <text x="360" y="108" font-size="14" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">↔</text>
  <text x="360" y="126" font-size="9" text-anchor="middle" fill="var(--muted)">opposite</text>
  <rect x="374" y="42" width="322" height="132" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="535" y="64" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">2 spend alerts (helps you → manage)</text>
  <text x="390" y="90" font-size="9.5" fill="var(--ink)">direction: helps you → your LLM spend</text>
  <text x="390" y="110" font-size="9.5" fill="var(--ink)">watches your OpenAI/Anthropic cost</text>
  <text x="390" y="130" font-size="9.5" fill="var(--muted)">cloudSpendAlertQueue</text>
  <text x="390" y="150" font-size="9.5" fill="var(--muted)">alerts over a threshold (L16/42 cost)</text>
  <text x="360" y="200" font-size="10" text-anchor="middle" fill="var(--muted)">self-host: no 1 (no platform fee), but still uses 2-style cost observation</text>
</svg>

<div class="cols">
  <div class="col"><h4>① platform metering (this lesson)</h4><p>direction: platform → charges you. Reports <strong>usage events</strong> to Stripe hourly, Cloud-exclusive. <code>cloudUsageMeteringQueue</code>. Insists on "exactly once".</p></div>
  <div class="col"><h4>② spend alerts (cloudSpendAlert)</h4><p>direction: helps you → manage your LLM spend. Watches your cost on OpenAI/Anthropic etc., alerts on threshold crossing. <code>cloudSpendAlertQueue</code> (CloudSpendAlertJob).</p></div>
  <div class="col"><h4>③ self-host</h4><p>no ①—self-deploying Langfuse <strong>charges you no platform fee</strong>. But cost observation like ② and the cost computation of Lessons 16/42 still work—you see your LLM spend just the same.</p></div>
</div>

<p>To wrap this thread: Part 8 ran from Lesson 40's "aggregate data into charts" all the way here, essentially answering <strong>"see clearly and govern the numbers"</strong>—dashboards show trends, the query engine unifies definitions, the pricing model computes cost clearly, and this lesson turns one kind of number (usage) <strong>into a real-money invoice</strong>. It also pulls back the curtain on Langfuse as a <strong>cloud business</strong>: open source and self-hostable (no charge), cloud-managed and usage-billed (this Stripe metering)—technology and commerce meshing tightly on this one worker.</p>

<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why does the metering job go to such lengths for "exactly once"—hour alignment, locking, plus fallback unlock?</strong> Because <strong>this is money</strong>, and money's tolerance for error is zero. All earlier chains can occasionally over-count a trace or miss a score with little harm, self-healing next time. Billing is different: <strong>over-report one hour and a customer's credit card gets charged once more</strong>—a complaint-and-Twitter incident; under-report and the platform takes a real loss. A normal background job seeking "eventual consistency" is enough, but the metering job must achieve <strong>"exactly once"</strong>—a notoriously hard guarantee in distributed systems. Langfuse's solution is pragmatic: rather than chase theoretically perfect exactly-once, it uses a <strong>database row as a lock</strong> to plug three real threats one by one—duplicate execution (mutex blocks), task crash (20-minute fallback takeover), interval misalignment (strict hour alignment). <strong>Decomposing "exactly once" into a few implementable concrete defenses, rather than theorizing about guarantees</strong>—that's engineering wisdom.<br><br>
  <strong>Why bill by "usage events" rather than token count?</strong> An interesting product trade-off. Billing by <strong>token</strong> would tightly couple to the model you use (pricey models burn more tokens) and isn't directly tied to Langfuse's value—Langfuse's value is <strong>recording and analysis</strong>, not running the model for you. Billing by <strong>trace</strong> is too coarse: one trace may hold one step or hundreds of observations. So Langfuse picked a <strong>fine-grained "observable operation" unit</strong>: early on it counted only observations (<code>tracing_observations</code>, kept to this day as legacy), and has since evolved to <code>tracing_events</code> = trace + score + observation. Either way, complex apps produce more events and pay more, simple ones pay less, <strong>billing granularity aligned with the value the platform provides</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>This is Cloud-exclusive platform billing</strong>: a separate, opposite ledger from your LLM cost (Lessons 16/42); self-host charges no platform fee, so read it as "how managed billing is built".</li>
    <li><strong>Meter by usage events</strong>: an hourly job counts each org's obs/trace/score from ClickHouse, and for orgs with a Stripe customerId calls <code>meterEvents.create</code> to report two meters (<code>tracing_observations</code> legacy + <code>tracing_events</code> = the sum; <code>backOff</code> retry), Stripe invoicing.</li>
    <li><strong>"Exactly once" is the crux</strong>: a <code>cronJobs</code> table as distributed lock + ledger—strict hour-aligned intervals, <code>Processing</code> mutex, 20-minute fallback takeover—so each hour's usage is no-dup, no-miss.</li>
    <li><strong>Billing must be exactly-once</strong>: money tolerates no error, normal jobs' "eventual consistency" isn't enough; decompose exactly-once into "anti-duplicate + anti-crash + anti-misalignment" implementable defenses.</li>
    <li><strong>Usage events = a value-aligned billing unit</strong> (<code>tracing_events</code>=trace+score+observation; <code>tracing_observations</code> legacy): better than token (model-bound) at matching "how much Langfuse recorded/analyzed for you"—what the customer pays is proportional to value received. A separate <code>cloudSpendAlert</code> helps you manage your own LLM spend.</li>
  </ul>
</div>
""")

LESSON_43 = {"zh": "\n".join(_ZH43), "en": "\n".join(_EN43)}
