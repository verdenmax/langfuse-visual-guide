"""Part 11 — 设计专题与终章 / Design Themes & Capstone. Lessons L54–L55.

Synthesis lessons: they weave together the recurring patterns (L54) and the
end-to-end trace lifecycle (L55) the reader has met across L01–L53. Anchored in
.agents/ARCHITECTURE_PRINCIPLES.md and prior lessons' already-verified facts.
"""

# ══════════════════════════════════════════════════════════════════════
# L54 · 设计专题综合 / Design themes synthesis
# ══════════════════════════════════════════════════════════════════════
_ZH54 = []
_EN54 = []

# (L54 sections below)

_ZH54.append(r"""
<p class="lead">
走到这里，你已经把 Langfuse 从一条 trace 的出生看到了它的落幕、从前端点按看到了后台队列。这一课往后退一步，做一件事：<strong>把 53 课里反复出现的设计决策，收拢成六个名字</strong>。你会发现，那些看似各管一摊的实现——ClickHouse 为什么用列存、为什么要用队列、为什么删除要跨三个库、为什么处处带着 projectId——<strong>背后其实是同一套世界观在反复落地</strong>。Langfuse 官方的 <code>ARCHITECTURE_PRINCIPLES.md</code> 把它一句话点明：「为<strong>宽的、结构化的事件数据</strong>上的<strong>高吞吐、探索式可观测</strong>而优化」。
六个主题——<strong>宽事件、不可变、异步、双存储、多租户、成本</strong>——不是六个孤立的技巧，而是这一句话的六个切面。看懂它们，你就不只是「读过 Langfuse 的代码」，而是真正理解了「一个高规模可观测平台该怎么想」。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  前面 53 课像是逐间参观一座大厦的每个房间——这一课，是带你登上对面的天台，<strong>看清这栋楼的整体设计语言</strong>。你会发现设计师其实只信奉<strong>几条原则</strong>，然后在每个房间里反复运用：承重墙都朝同一个方向、管线都走同一套规范、连灯开关的位置都遵循同一个习惯。
  一座好建筑的精妙，不在于某个房间多花哨，而在于<strong>整栋楼贯穿着一致的取舍</strong>——每一处局部选择，回头看都能归到那几条原则上。Langfuse 也是如此：宽事件决定了「数据长什么样」，不可变决定了「数据怎么写」，异步决定了「活儿在哪儿干」，双存储决定了「数据存哪儿」，多租户决定了「数据归谁」，成本决定了「什么该做什么不该做」。<strong>六根梁，撑起同一座楼。</strong>
</div>
""")

# (L54 sec1 below)

_ZH54.append(r"""
<h2>主题一·二：宽事件 + 不可变（数据怎么长、怎么写）</h2>
<p><strong>宽事件（wide events）</strong>是整套架构的地基，也是「可观测性 2.0」的核心主张。传统做法把监控数据拆成三摊——指标(metrics)、日志(logs)、链路(traces)，事后再费劲拼回去。Langfuse 反其道：以 <strong>observation 为主要分析单位</strong>，把一次操作的<strong>全部上下文</strong>（输入、输出、模型、用量、耗时、自定义属性……）<strong>塞进一条又宽又富的事件</strong>里；trace 只是把相关 observation 串起来的「关联句柄」，不是唯一入口。这样保住了<strong>高基数上下文</strong>——你能任意切片、分组、过滤，去调查那些<strong>事前没预料到的问题（unknown unknowns）</strong>，而不必预先为每个未来的问题建好指标（第5/6课的领域模型、第41课的查询引擎都是这个主张的落地）。</p>

<p><strong>不可变（immutability）</strong>是宽事件的天然搭档。高吞吐遥测下，Langfuse <strong>偏好追加而非更新</strong>：事件写进去就基本不动。为什么？因为「<strong>更新</strong>」在海量数据上代价惊人——它逼着查询时做<strong>读时去重</strong>，凭空多出隐藏的查询成本。第13课你已见识过 ClickHouse 怎么用 <strong>AggregatingMergeTree + 读时 final 聚合</strong>来吞下「同一实体多次写入」：不真的去改老行，而是追加新行、查询时按规则合并。<strong>把「改」变成「追加 + 合并」，是高规模写入能扛住的关键。</strong></p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="宽事件vs碎片化：传统把数据拆成metrics/logs/traces三摊事后拼回；Langfuse以observation为单位把全部上下文(输入输出模型用量耗时属性)塞进一条又宽又富的事件，保住高基数可任意切片调查unknown unknowns；不可变=追加而非更新，避免读时去重的隐藏成本">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一条又宽又富的事件，胜过三摊事后拼图</text>
  <rect x="24" y="42" width="200" height="120" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">传统：拆成三摊</text>
  <rect x="38" y="72" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="87" text-anchor="middle" font-size="6.4" fill="var(--muted)">metrics（聚合数值，丢了细节）</text>
  <rect x="38" y="98" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="113" text-anchor="middle" font-size="6.4" fill="var(--muted)">logs（散乱文本）</text>
  <rect x="38" y="124" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="139" text-anchor="middle" font-size="6.4" fill="var(--muted)">traces（又一套）</text>
  <text x="124" y="156" text-anchor="middle" font-size="6" fill="var(--faint)">事后费劲拼回去</text>
  <rect x="260" y="42" width="230" height="120" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="375" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Langfuse：一条宽事件 observation</text><text x="375" y="80" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">输入 · 输出 · 模型 · 用量 · 耗时</text><text x="375" y="94" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">+ 任意自定义属性（高基数）</text><text x="375" y="112" text-anchor="middle" font-size="6.4" fill="var(--muted)">trace = 把相关 observation 串起来的句柄</text><text x="375" y="130" text-anchor="middle" font-size="6.2" fill="var(--faint)">可任意切片/分组/过滤</text><text x="375" y="146" text-anchor="middle" font-size="6.2" fill="var(--faint)">调查 unknown unknowns，不必预建指标</text>
  <rect x="520" y="56" width="176" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="608" y="74" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">不可变：追加</text><text x="608" y="90" text-anchor="middle" font-size="6.0" fill="var(--muted)">写进去就不动，只追加新行</text>
  <rect x="520" y="110" width="176" height="52" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="608" y="128" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">为何不更新？</text><text x="608" y="143" text-anchor="middle" font-size="6.0" fill="var(--muted)">更新逼着读时去重</text><text x="608" y="154" text-anchor="middle" font-size="6.0" fill="var(--muted)">= 海量数据的隐藏查询成本</text>
  <line x1="224" y1="102" x2="258" y2="102" stroke="var(--accent)" stroke-width="1.4"/><polygon points="258,102 249,98 249,106" fill="var(--accent)"/>
  <line x1="490" y1="90" x2="518" y2="82" stroke="var(--teal)" stroke-width="1.3"/><polygon points="518,82 509,81 511,89" fill="var(--teal)"/>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">第13课：ClickHouse 用 AggregatingMergeTree + 读时 final，把「同实体多次写入」变成「追加新行、查时合并」</text>
  <text x="360" y="206" text-anchor="middle" font-size="8" fill="var(--faint)">把「改」变成「追加 + 合并」——这是高规模写入扛得住的关键，也是不可变与宽事件的共谋</text>
</svg>
<div class="figcap"><b>宽事件 + 不可变</b>：<code>ARCHITECTURE_PRINCIPLES.md</code> 原则 1-4——「observation 为主要分析单位」「宽而富的事件优于碎片化的 metrics/logs/traces」「保住高基数上下文调查 unknown unknowns」「偏好不可变/追加，更新会造成读时去重的隐藏成本」。落地见第 5/6 课领域模型、第 13 课 AggregatingMergeTree、第 41 课查询引擎。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">主题一</span><span class="name">宽事件（observability 2.0）</span></div><div class="ld">一次操作 = 一条带全部上下文的宽事件。observation 是分析单位、trace 是关联句柄。保住高基数 → 能回答<strong>事前没想到的问题</strong>，而不必为每个未来问题预建指标。这是「探索式可观测」的根。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">主题二</span><span class="name">不可变（追加而非更新）</span></div><div class="ld">高吞吐下偏好追加。更新会逼出读时去重的隐藏成本，所以用 AggregatingMergeTree「追加新行 + 查时合并」替代「原地改」。<strong>不可变让写入路径简单、可预测、能水平扩展。</strong></div></div>
</div>
""")

# (L54 sec2 below)

_ZH54.append(r"""
<h2>主题三·四：异步 + 双存储（活在哪儿干、数据存哪儿）</h2>
<p><strong>异步（async）</strong>是 Langfuse 扛住高吞吐的骨架。请求路径上只做最轻的事——校验、落 S3、塞进 Redis 队列就<strong>立刻返回</strong>；真正的重活全推给 <strong>BullMQ 队列 + worker</strong> 在后台慢慢消化（第12-19课的摄取链路）。这套「<strong>快速接收、异步处理</strong>」的分工，在后面反复变奏：第30课 eval、第43课计量、第46课分析集成、第52课后台迁移——你见过的<strong>两级 fan-out（调度→逐项目）、幂等、水位线、分布式锁</strong>，全是「异步」这个主题为应对「失败会重试、规模会很大」演化出的纪律。把活儿从请求里搬到队列里，是高规模系统「<strong>削峰、解耦、可重试</strong>」的通用答案。</p>

<p><strong>双存储（实为三存储）</strong>决定数据的归宿，让读写各得其所。<strong>Postgres</strong> 扛 OLTP——配置、用户、权限这类强一致、低频改的结构化元数据；<strong>ClickHouse</strong> 扛 OLAP——海量、可分析的事件，靠列存 + 时间分区 + 排序键 + 数据裁剪把「扫几十亿行做聚合」变得可行；<strong>对象存储 S3</strong> 放体积大的原始负载（完整输入输出、媒体）。配套的取舍是<strong>谨慎反范式化</strong>（去掉热路径上的 join，把常用过滤变成直接列谓词）、<strong>列表/仪表盘只读紧凑表示、详情才取大字段</strong>（第22/24课）。不同形状的数据放进最合适的引擎——这是「为列式访问设计」的直接结果。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="异步+双存储：请求路径只做轻活(校验/落S3/塞Redis队列)立刻返回，重活推给BullMQ+worker后台处理(两级fan-out/幂等/水位/锁)；数据按形状分三存储——Postgres扛OLTP元数据、ClickHouse扛OLAP海量事件(列存)、S3放大块负载">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">快接收→异步处理；数据按形状各归各家</text>
  <rect x="24" y="40" width="150" height="50" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">请求路径（薄）</text><text x="99" y="76" text-anchor="middle" font-size="6.2" fill="var(--muted)">校验·落S3·塞队列→立刻返回</text>
  <rect x="200" y="40" width="150" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="275" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">BullMQ + worker</text><text x="275" y="76" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">重活后台慢慢消化</text>
  <rect x="200" y="100" width="320" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="115" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--accent-ink)">异步主题的反复变奏</text><text x="360" y="127" text-anchor="middle" font-size="6.0" fill="var(--muted)">两级 fan-out · 幂等 · 水位线 · 分布式锁（第30/43/46/52课）</text>
  <line x1="174" y1="65" x2="198" y2="65" stroke="var(--accent)" stroke-width="1.4"/><polygon points="198,65 189,61 189,69" fill="var(--accent)"/>
  <rect x="40" y="156" width="200" height="74" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="140" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">Postgres（OLTP）</text><text x="140" y="193" text-anchor="middle" font-size="6.2" fill="var(--muted)">配置/用户/权限·强一致低频改</text><text x="140" y="207" text-anchor="middle" font-size="6.0" fill="var(--faint)">结构化元数据</text><text x="140" y="220" text-anchor="middle" font-size="6.0" fill="var(--faint)">「源真相」</text>
  <rect x="260" y="156" width="200" height="74" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">ClickHouse（OLAP）</text><text x="360" y="193" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">海量事件·列存+分区+排序键</text><text x="360" y="207" text-anchor="middle" font-size="6.0" fill="var(--muted)">扫几十亿行做聚合可行</text><text x="360" y="220" text-anchor="middle" font-size="6.0" fill="var(--faint)">谨慎反范式去 join</text>
  <rect x="480" y="156" width="200" height="74" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="580" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">对象存储 S3</text><text x="580" y="193" text-anchor="middle" font-size="6.2" fill="var(--muted)">大块负载·完整输入输出/媒体</text><text x="580" y="207" text-anchor="middle" font-size="6.0" fill="var(--faint)">列表只取紧凑表示</text><text x="580" y="220" text-anchor="middle" font-size="6.0" fill="var(--faint)">详情才取大字段（第22/24课）</text>
  <line x1="275" y1="134" x2="160" y2="154" stroke="var(--faint)" stroke-width="1"/><line x1="320" y1="134" x2="360" y2="154" stroke="var(--accent)" stroke-width="1.2"/><line x1="360" y1="134" x2="560" y2="154" stroke="var(--faint)" stroke-width="1"/>
</svg>
<div class="figcap"><b>异步 + 双(三)存储</b>：<code>ARCHITECTURE_PRINCIPLES.md</code> 原则 5-7、10——反范式去热路径 join、为列式访问设计（窄选列/时间界/排序键/裁剪）、列表用紧凑表示大字段延后、保住近实时调试。异步骨架见第 12-19 课摄取，反复变奏见第 30/43/46/52 课；三存储见第 2/22/24/52 课。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">主题三</span><span class="name">异步（队列 + worker）</span></div><div class="ld">请求路径只接收、不干重活；重活进 BullMQ 由 worker 后台处理。削峰、解耦、可重试。其衍生纪律——fan-out、幂等、水位、锁——在 eval/计量/集成/迁移里反复出现，是同一主题的不同变奏。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">主题四</span><span class="name">双(三)存储（各归各家）</span></div><div class="ld">Postgres 扛 OLTP 元数据、ClickHouse 扛 OLAP 海量事件（列存）、S3 放大块负载。配套谨慎反范式、列表紧凑/详情取大字段。<strong>让不同形状的数据落进最合适的引擎</strong>，是性能与成本的根。</div></div>
</div>
""")

# (L54 sec3 below)

_ZH54.append(r"""
<h2>主题五·六：多租户 + 成本（数据归谁、什么值得做）</h2>
<p><strong>多租户（multi-tenancy）</strong>是贯穿全栈的一条隐线：<strong>几乎每张表、每个查询、每条队列消息都带着 projectId</strong>。从第48课的登录（session 注入组织/项目成员关系）、到第49课的 RBAC scope 与 API key scope、再到第50课按 plan 给的 entitlement，构成层层收窄的隔离；第46课的分析集成、第52课的删除都<strong>按项目 fan-out</strong>。多租户不是某一处的功能，而是一条「<strong>任何数据都明确归属、任何访问都明确授权</strong>」的纪律——它决定了一个平台能不能安全地让成千上万个互不信任的租户共用同一套基础设施。</p>

<p><strong>成本（cost）</strong>是把前五个主题「管住」的那条约束。架构原则里写得很直白：<strong>把成本与运维简单性当作架构约束</strong>——「额外的数据库、队列、物化视图、迁移，都必须挣回它们的长期运维负担」。这解释了很多克制的选择：API 契约要求时间窗口、暴露字段选择、用 token 分页、不给「能扫全部历史」的危险默认（第27课）；模型与用量成本被显式计量（第42/43课）。<strong>不是「能加就加」，而是「每一个新增的活动部件，都要先证明自己值这份维护成本」</strong>——这份克制，恰恰是系统能长期简单、可维护的根。</p>

<table class="t">
  <thead><tr><th>主题</th><th>一句话</th><th>在哪些课见过</th></tr></thead>
  <tbody>
    <tr><td><b>① 宽事件</b></td><td>一条又宽又富的事件，保住高基数调查 unknown unknowns</td><td>L05/L06 领域模型 · L41 查询引擎</td></tr>
    <tr><td><b>② 不可变</b></td><td>追加而非更新；改 = 追加新行 + 查时合并</td><td>L13 AggregatingMergeTree · L18</td></tr>
    <tr><td><b>③ 异步</b></td><td>快接收、队列里慢处理；fan-out/幂等/水位/锁</td><td>L12–19 摄取 · L30/L43/L46/L52</td></tr>
    <tr><td><b>④ 双(三)存储</b></td><td>PG(OLTP)+CH(OLAP)+S3(负载)，各归各家</td><td>L02/L22/L24 · L52 删除</td></tr>
    <tr><td><b>⑤ 多租户</b></td><td>处处带 projectId；鉴权→RBAC→entitlement 层层隔离</td><td>L48/L49/L50 · L46/L52 按项目</td></tr>
    <tr><td><b>⑥ 成本</b></td><td>每个活动部件须挣回运维负担；契约要 scale-aware</td><td>L27 公共API · L42/L43 成本</td></tr>
  </tbody>
</table>
""")

_ZH54.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>这六个主题，为什么说是「一套世界观的六个切面」，而不是六个互不相干的技巧？</strong> 因为它们全都从同一个目标推导而来：<strong>在宽的、结构化的事件数据上，做高吞吐、探索式的可观测</strong>。把这句话拆开看——「<strong>探索式</strong>」要求你能回答事前没想到的问题，于是必须保住高基数（<strong>宽事件</strong>），而不能预先把数据揉成几个固定指标；「<strong>高吞吐</strong>」要求写入便宜、查询能横向扩展，于是写要<strong>不可变</strong>（避免读时去重）、活要<strong>异步</strong>（削峰解耦）、存要按访问形状分到<strong>列式引擎</strong>（双存储）；而「<strong>平台</strong>」二字意味着它要服务很多租户、要长期能维护，于是必须<strong>多租户</strong>隔离、必须把<strong>成本</strong>当硬约束。你看，每一个主题都不是凭空的偏好，而是从「目标 + 规模」这两个前提一步步逼出来的<strong>必然</strong>。这正是「架构」和「一堆技术选型」的区别：<strong>架构是一组彼此印证、共同服务于同一目标的取舍</strong>，拆开任何一个，其余的都会显得别扭。<br><br>
  <strong>这套思维方式，怎么迁移到你自己的系统？</strong> 别照搬 Langfuse 的具体选型（你未必需要 ClickHouse、未必要 fan-out 队列），而要学它<strong>推导的方式</strong>：先把你系统的「目标 + 规模前提」想清楚——你要回答的是<strong>已知</strong>问题还是<strong>探索式</strong>问题？写多还是读多？一个租户还是很多租户？能容忍多大延迟？把这几个前提钉死，很多「该不该上消息队列」「该不该分库」「要不要反范式」的争论会自动有答案。而架构原则文档里那句最朴素的<strong>「每个额外的活动部件都要挣回它的长期运维负担」</strong>，则是一把万能的减法尺子——<strong>在加任何东西之前，先问它配不配。</strong>能用更少的部件达成目标，几乎永远是更好的架构。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>六个主题 = 一套世界观的六个切面</strong>：都从「为宽的结构化事件数据做高吞吐、探索式可观测」推导而来（<code>ARCHITECTURE_PRINCIPLES.md</code>）。</li>
    <li><strong>① 宽事件</strong>：observation 为分析单位、trace 为关联句柄；宽而富 + 高基数 → 调查 unknown unknowns，不必预建指标。</li>
    <li><strong>② 不可变 + ③ 异步</strong>：写不可变（追加+合并，避读时去重）、活异步（队列削峰解耦，衍生 fan-out/幂等/水位/锁）——高吞吐扛得住的两根支柱。</li>
    <li><strong>④ 双(三)存储 + ⑤ 多租户</strong>：PG/CH/S3 按形状各归各家（反范式、列式、紧凑列表）；处处 projectId、鉴权→RBAC→entitlement 层层隔离。</li>
    <li><strong>⑥ 成本是约束</strong>：每个额外的库/队列/视图/迁移都要挣回运维负担；契约 scale-aware（时间窗/字段选择/token 分页）。<strong>迁移这套思维的关键不是照搬选型，而是先钉死「目标+规模」前提、再用「部件配不配」做减法。</strong></li>
  </ul>
</div>
""")

_EN54.append(r"""
<p class="lead">
By now you've followed a trace from birth to curtain call, from front-end clicks to background queues. This lesson takes a step back to do one thing: <strong>gather the design decisions that kept recurring across 53 lessons into six names</strong>. You'll find that the seemingly-separate implementations — why ClickHouse uses columnar storage, why queues, why deletion spans three stores, why projectId is everywhere — are <strong>actually one worldview landing over and over</strong>. Langfuse's official <code>ARCHITECTURE_PRINCIPLES.md</code> states it in a sentence: optimize for <strong>high-scale, exploratory observability on wide, structured event data</strong>.
The six themes — <strong>wide events, immutability, async, dual storage, multi-tenancy, cost</strong> — aren't six isolated tricks but six facets of that one sentence. Grasp them and you've not just "read Langfuse's code" but truly understood "how a high-scale observability platform should think."
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  The previous 53 lessons were like touring each room of a great building one by one — this lesson takes you up to the rooftop across the street to <strong>see the building's overall design language</strong>. You'll find the architect actually believes in just <strong>a few principles</strong>, then applies them repeatedly in every room: load-bearing walls all face the same way, conduits all follow one standard, even the light-switch positions follow one habit.
  A good building's elegance isn't in any one room being fancy, but in <strong>consistent trade-offs running through the whole building</strong> — every local choice, in hindsight, traces back to those few principles. Langfuse is the same: wide events decide "what the data looks like," immutability decides "how it's written," async decides "where the work happens," dual storage decides "where it's stored," multi-tenancy decides "who it belongs to," cost decides "what should and shouldn't be done." <strong>Six beams, holding up one building.</strong>
</div>
""")

_EN54.append(r"""
<h2>Themes 1 & 2: wide events + immutability (how data looks and is written)</h2>
<p><strong>Wide events</strong> are the foundation of the whole architecture and the core claim of "observability 2.0." The traditional approach splits monitoring data into three piles — metrics, logs, traces — then laboriously stitches them back later. Langfuse does the reverse: with the <strong>observation as the primary analytical unit</strong>, it packs an operation's <strong>full context</strong> (input, output, model, usage, latency, custom attributes…) <strong>into one wide, rich event</strong>; a trace is just the "correlation handle" linking related observations, not the only entry point. This preserves <strong>high-cardinality context</strong> — you can slice, group, filter at will to investigate problems <strong>you didn't anticipate (unknown unknowns)</strong>, without pre-building a metric for every future question (Lessons 5/6 domain models and Lesson 41's query engine are this claim landing).</p>

<p><strong>Immutability</strong> is wide events' natural partner. Under high-throughput telemetry, Langfuse <strong>favors append over update</strong>: an event written basically doesn't move. Why? Because "<strong>updates</strong>" are shockingly costly at massive scale — they force <strong>read-time deduplication</strong>, conjuring hidden query costs. In Lesson 13 you saw how ClickHouse uses <strong>AggregatingMergeTree + read-time final aggregation</strong> to swallow "the same entity written multiple times": it doesn't really modify old rows but appends new ones and merges by rule at query time. <strong>Turning "modify" into "append + merge" is the key to write-side surviving at high scale.</strong></p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Wide events vs fragmented: tradition splits data into metrics/logs/traces piles stitched later; Langfuse packs full context (input output model usage latency attributes) into one wide rich event per observation, preserving high cardinality to investigate unknown unknowns; immutability = append not update, avoiding read-time dedup hidden cost">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">One wide rich event beats three piles stitched later</text>
  <rect x="24" y="42" width="200" height="120" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">tradition: three piles</text>
  <rect x="38" y="72" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="87" text-anchor="middle" font-size="6.4" fill="var(--muted)">metrics (aggregated, detail lost)</text>
  <rect x="38" y="98" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="113" text-anchor="middle" font-size="6.4" fill="var(--muted)">logs (scattered text)</text>
  <rect x="38" y="124" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="139" text-anchor="middle" font-size="6.4" fill="var(--muted)">traces (yet another set)</text>
  <text x="124" y="156" text-anchor="middle" font-size="6" fill="var(--faint)">laboriously stitched back later</text>
  <rect x="260" y="42" width="230" height="120" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="375" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Langfuse: one wide event = observation</text><text x="375" y="80" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">input · output · model · usage · latency</text><text x="375" y="94" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">+ any custom attributes (high cardinality)</text><text x="375" y="112" text-anchor="middle" font-size="6.4" fill="var(--muted)">trace = handle linking related observations</text><text x="375" y="130" text-anchor="middle" font-size="6.2" fill="var(--faint)">slice/group/filter at will</text><text x="375" y="146" text-anchor="middle" font-size="6.2" fill="var(--faint)">investigate unknown unknowns, no pre-built metrics</text>
  <rect x="520" y="56" width="176" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="608" y="74" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">immutable: append</text><text x="608" y="90" text-anchor="middle" font-size="6.0" fill="var(--muted)">written stays put, only append new rows</text>
  <rect x="520" y="110" width="176" height="52" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="608" y="128" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">why not update?</text><text x="608" y="143" text-anchor="middle" font-size="6.0" fill="var(--muted)">updates force read-time dedup</text><text x="608" y="154" text-anchor="middle" font-size="6.0" fill="var(--muted)">= hidden query cost at scale</text>
  <line x1="224" y1="102" x2="258" y2="102" stroke="var(--accent)" stroke-width="1.4"/><polygon points="258,102 249,98 249,106" fill="var(--accent)"/>
  <line x1="490" y1="90" x2="518" y2="82" stroke="var(--teal)" stroke-width="1.3"/><polygon points="518,82 509,81 511,89" fill="var(--teal)"/>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">Lesson 13: ClickHouse uses AggregatingMergeTree + read-time final, turning "same entity written multiple times" into "append new rows, merge at query"</text>
  <text x="360" y="206" text-anchor="middle" font-size="8" fill="var(--faint)">Turning "modify" into "append + merge" — the key to high-scale write survival, and the conspiracy between immutability and wide events</text>
</svg>
<div class="figcap"><b>Wide events + immutability</b>: <code>ARCHITECTURE_PRINCIPLES.md</code> principles 1-4 — "observation as the primary analytical unit," "wide richly-attributed events over fragmented metrics/logs/traces," "preserve high-cardinality context to investigate unknown unknowns," "favor immutable/append; updates create read-time-dedup hidden cost." Landed in Lessons 5/6 domain models, Lesson 13 AggregatingMergeTree, Lesson 41 query engine.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">theme 1</span><span class="name">wide events (observability 2.0)</span></div><div class="ld">One operation = one wide event with full context. The observation is the analytical unit, the trace a correlation handle. Preserving high cardinality → answer <strong>questions you didn't anticipate</strong>, without pre-building a metric per future question. This is the root of "exploratory observability."</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">theme 2</span><span class="name">immutability (append not update)</span></div><div class="ld">High-throughput favors append. Updates force read-time-dedup hidden cost, so AggregatingMergeTree's "append new rows + merge at query" replaces "modify in place." <strong>Immutability keeps the write path simple, predictable, and horizontally scalable.</strong></div></div>
</div>
""")

_EN54.append(r"""
<h2>Themes 3 & 4: async + dual storage (where work happens, where data lives)</h2>
<p><strong>Async</strong> is the skeleton that lets Langfuse survive high throughput. The request path does only the lightest things — validate, land in S3, push to a Redis queue and <strong>return immediately</strong>; the real heavy lifting goes to <strong>BullMQ queues + workers</strong> to digest slowly in the background (Lessons 12-19's ingestion path). This "<strong>receive fast, process async</strong>" division recurs in variations later: Lesson 30 eval, Lesson 43 metering, Lesson 46 analytics integrations, Lesson 52 background migrations — the <strong>two-level fan-out (schedule→per-object), idempotency, watermarks, distributed locks</strong> you've seen are all disciplines the "async" theme evolved to handle "failures retry, scale gets big." Moving work from the request into the queue is the universal answer to high-scale "<strong>peak-shaving, decoupling, retryability</strong>."</p>

<p><strong>Dual storage</strong> (really tri-store) decides data's home, letting reads and writes each fit. <strong>Postgres</strong> handles OLTP — strongly-consistent, rarely-changed structured metadata like config, users, permissions; <strong>ClickHouse</strong> handles OLAP — massive analyzable events, using columnar storage + time partitions + ordering keys + data pruning to make "scan billions of rows to aggregate" feasible; <strong>object storage S3</strong> holds bulky raw payloads (full inputs/outputs, media). The accompanying trade-offs are <strong>careful denormalization</strong> (kill hot-path joins, turn common filters into direct column predicates) and <strong>lists/dashboards read only compact representations, detail views fetch big fields</strong> (Lessons 22/24). Putting differently-shaped data into the most-fitting engine — a direct result of "designing for columnar access."</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Async + dual storage: the request path does only light work (validate/land S3/push Redis queue) and returns immediately, heavy work goes to BullMQ+worker background processing (two-level fan-out/idempotency/watermark/lock); data split by shape into three stores — Postgres for OLTP metadata, ClickHouse for OLAP massive events (columnar), S3 for bulky payloads">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Receive fast→process async; data goes home by shape</text>
  <rect x="24" y="40" width="150" height="50" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">request path (thin)</text><text x="99" y="76" text-anchor="middle" font-size="6.2" fill="var(--muted)">validate·land S3·queue→return now</text>
  <rect x="200" y="40" width="150" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="275" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">BullMQ + worker</text><text x="275" y="76" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">heavy work digested in background</text>
  <rect x="200" y="100" width="320" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="115" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--accent-ink)">recurring variations of the async theme</text><text x="360" y="127" text-anchor="middle" font-size="6.0" fill="var(--muted)">two-level fan-out · idempotency · watermark · distributed lock (L30/43/46/52)</text>
  <line x1="174" y1="65" x2="198" y2="65" stroke="var(--accent)" stroke-width="1.4"/><polygon points="198,65 189,61 189,69" fill="var(--accent)"/>
  <rect x="40" y="156" width="200" height="74" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="140" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">Postgres (OLTP)</text><text x="140" y="193" text-anchor="middle" font-size="6.2" fill="var(--muted)">config/users/perms·consistent rarely-changed</text><text x="140" y="207" text-anchor="middle" font-size="6.0" fill="var(--faint)">structured metadata</text><text x="140" y="220" text-anchor="middle" font-size="6.0" fill="var(--faint)">"source of truth"</text>
  <rect x="260" y="156" width="200" height="74" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">ClickHouse (OLAP)</text><text x="360" y="193" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">massive events·columnar+partition+order key</text><text x="360" y="207" text-anchor="middle" font-size="6.0" fill="var(--muted)">scan billions to aggregate, feasible</text><text x="360" y="220" text-anchor="middle" font-size="6.0" fill="var(--faint)">careful denorm to kill joins</text>
  <rect x="480" y="156" width="200" height="74" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="580" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">object storage S3</text><text x="580" y="193" text-anchor="middle" font-size="6.2" fill="var(--muted)">bulky payloads·full I/O / media</text><text x="580" y="207" text-anchor="middle" font-size="6.0" fill="var(--faint)">lists fetch only compact representations</text><text x="580" y="220" text-anchor="middle" font-size="6.0" fill="var(--faint)">detail fetches big fields (L22/24)</text>
  <line x1="275" y1="134" x2="160" y2="154" stroke="var(--faint)" stroke-width="1"/><line x1="320" y1="134" x2="360" y2="154" stroke="var(--accent)" stroke-width="1.2"/><line x1="360" y1="134" x2="560" y2="154" stroke="var(--faint)" stroke-width="1"/>
</svg>
<div class="figcap"><b>Async + dual (tri) storage</b>: <code>ARCHITECTURE_PRINCIPLES.md</code> principles 5-7, 10 — denormalize to kill hot-path joins, design for columnar access (narrow field selection/time bounds/ordering keys/pruning), lists use compact representations deferring big fields, preserve near-real-time debugging. The async skeleton is Lessons 12-19 ingestion, variations in Lessons 30/43/46/52; tri-store in Lessons 2/22/24/52.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">theme 3</span><span class="name">async (queue + worker)</span></div><div class="ld">The request path only receives, no heavy work; heavy work enters BullMQ for the worker to process in the background. Peak-shaving, decoupling, retryability. Its derived disciplines — fan-out, idempotency, watermark, lock — recur in eval/metering/integration/migration, variations of one theme.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">theme 4</span><span class="name">dual (tri) storage (each goes home)</span></div><div class="ld">Postgres handles OLTP metadata, ClickHouse OLAP massive events (columnar), S3 bulky payloads. With careful denormalization, compact lists / big-field detail. <strong>Letting differently-shaped data land in the most-fitting engine</strong> is the root of performance and cost.</div></div>
</div>
""")

_EN54.append(r"""
<h2>Themes 5 & 6: multi-tenancy + cost (who data belongs to, what's worth doing)</h2>
<p><strong>Multi-tenancy</strong> is a hidden thread running full-stack: <strong>nearly every table, every query, every queue message carries a projectId</strong>. From Lesson 48's login (session injecting org/project memberships), to Lesson 49's RBAC scopes and API-key scopes, to Lesson 50's plan-based entitlements, they form layer-upon-layer narrowing isolation; Lesson 46's analytics integrations and Lesson 52's deletion both <strong>fan out per project</strong>. Multi-tenancy isn't a feature in one place but a discipline of "<strong>every datum has a clear owner, every access has clear authorization</strong>" — it decides whether a platform can safely let thousands of mutually-untrusting tenants share one infrastructure.</p>

<p><strong>Cost</strong> is the constraint that "reins in" the first five themes. The architecture principles say it bluntly: <strong>treat cost and operational simplicity as architectural constraints</strong> — "extra databases, queues, materialized views, and migrations must earn their long-term operational burden." This explains many restrained choices: API contracts require time windows, expose field selection, use token pagination, give no dangerous "can scan all history" defaults (Lesson 27); model and usage cost are explicitly metered (Lessons 42/43). <strong>Not "add it because you can," but "every new moving part must first prove it's worth its maintenance cost"</strong> — this restraint is precisely the root of a system staying simple and maintainable long-term.</p>

<table class="t">
  <thead><tr><th>Theme</th><th>In a sentence</th><th>Seen in lessons</th></tr></thead>
  <tbody>
    <tr><td><b>① wide events</b></td><td>one wide rich event, preserving high cardinality to investigate unknown unknowns</td><td>L05/L06 domain models · L41 query engine</td></tr>
    <tr><td><b>② immutability</b></td><td>append not update; modify = append new rows + merge at query</td><td>L13 AggregatingMergeTree · L18</td></tr>
    <tr><td><b>③ async</b></td><td>receive fast, process slowly in queues; fan-out/idempotency/watermark/lock</td><td>L12–19 ingestion · L30/L43/L46/L52</td></tr>
    <tr><td><b>④ dual (tri) storage</b></td><td>PG(OLTP)+CH(OLAP)+S3(payloads), each goes home</td><td>L02/L22/L24 · L52 deletion</td></tr>
    <tr><td><b>⑤ multi-tenancy</b></td><td>projectId everywhere; auth→RBAC→entitlement layered isolation</td><td>L48/L49/L50 · L46/L52 per-project</td></tr>
    <tr><td><b>⑥ cost</b></td><td>every moving part must earn its burden; contracts must be scale-aware</td><td>L27 public API · L42/L43 cost</td></tr>
  </tbody>
</table>
""")

_EN54.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why are these six themes "six facets of one worldview" rather than six unrelated tricks?</strong> Because they all derive from one goal: <strong>high-throughput, exploratory observability on wide, structured event data</strong>. Unpack that sentence — "<strong>exploratory</strong>" requires answering questions you didn't anticipate, so you must preserve high cardinality (<strong>wide events</strong>), not pre-mash data into a few fixed metrics; "<strong>high-throughput</strong>" requires cheap writes and horizontally-scalable queries, so writes are <strong>immutable</strong> (avoid read-time dedup), work is <strong>async</strong> (peak-shave, decouple), storage is split by access shape into <strong>columnar engines</strong> (dual storage); and the word "<strong>platform</strong>" means it serves many tenants and must be maintainable long-term, so it must isolate by <strong>multi-tenancy</strong> and treat <strong>cost</strong> as a hard constraint. See — each theme isn't an arbitrary preference but a <strong>necessity</strong> forced step by step from the two premises "goal + scale." This is exactly the difference between "architecture" and "a pile of tech choices": <strong>architecture is a set of trade-offs that mutually corroborate and jointly serve one goal</strong>; pull out any one and the rest look awkward.<br><br>
  <strong>How does this way of thinking transfer to your own system?</strong> Don't copy Langfuse's specific choices (you may not need ClickHouse, may not need fan-out queues), but learn its <strong>way of deriving</strong>: first get clear on your system's "goal + scale premises" — are you answering <strong>known</strong> questions or <strong>exploratory</strong> ones? Write-heavy or read-heavy? One tenant or many? How much latency can you tolerate? Nail these premises and many debates over "should we add a message queue," "should we shard," "should we denormalize" answer themselves. And the principles doc's plainest line — "<strong>every extra moving part must earn its long-term operational burden</strong>" — is a universal subtraction ruler: <strong>before adding anything, ask whether it deserves to be there.</strong> Achieving the goal with fewer parts is almost always the better architecture.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Six themes = six facets of one worldview</strong>: all derived from "high-throughput, exploratory observability on wide structured event data" (<code>ARCHITECTURE_PRINCIPLES.md</code>).</li>
    <li><strong>① wide events</strong>: observation as the analytical unit, trace as the correlation handle; wide + rich + high cardinality → investigate unknown unknowns, no pre-built metrics.</li>
    <li><strong>② immutability + ③ async</strong>: immutable writes (append+merge, avoid read-time dedup), async work (queues peak-shave/decouple, deriving fan-out/idempotency/watermark/lock) — the two pillars of surviving high throughput.</li>
    <li><strong>④ dual (tri) storage + ⑤ multi-tenancy</strong>: PG/CH/S3 each go home by shape (denorm, columnar, compact lists); projectId everywhere, auth→RBAC→entitlement layered isolation.</li>
    <li><strong>⑥ cost is a constraint</strong>: every extra DB/queue/view/migration must earn its burden; contracts scale-aware (time windows/field selection/token pagination). <strong>The key to transferring this thinking isn't copying choices but nailing "goal+scale" premises first, then subtracting via "does this part deserve to exist."</strong></li>
  </ul>
</div>
""")

LESSON_54 = {"zh": "\n".join(_ZH54), "en": "\n".join(_EN54)}
