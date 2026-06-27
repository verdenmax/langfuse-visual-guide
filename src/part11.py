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

<p><strong>不可变（immutability）</strong>是宽事件的天然搭档。高吞吐遥测下，Langfuse <strong>偏好追加而非更新</strong>：事件写进去就基本不动。为什么？因为「<strong>更新</strong>」在海量数据上代价惊人——它逼着查询时做<strong>读时去重</strong>，凭空多出隐藏的查询成本。第13课你已见识过 ClickHouse 怎么用 <strong>ReplacingMergeTree(event_ts, is_deleted) + 读时 FINAL 去重</strong>来吞下「同一实体多次写入」：不真的去改老行，而是追加新行、查询时<strong>按 event_ts 保留最新版本</strong>。<strong>把「改」变成「追加 + 查时去重」，是高规模写入能扛住的关键。</strong></p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="宽事件vs碎片化：传统把数据拆成metrics/logs/traces三摊事后拼回；Langfuse以observation为单位把全部上下文(输入输出模型用量耗时属性)塞进一条又宽又富的事件，保住高基数可任意切片调查unknown unknowns；不可变=追加而非更新，避免读时去重的隐藏成本">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一条又宽又富的事件，胜过三摊事后拼图</text>
  <rect x="24" y="42" width="200" height="120" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">传统：拆成三摊</text>
  <rect x="38" y="72" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="87" text-anchor="middle" font-size="6.5" fill="var(--muted)">metrics（聚合数值，丢了细节）</text>
  <rect x="38" y="98" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="113" text-anchor="middle" font-size="6.5" fill="var(--muted)">logs（散乱文本）</text>
  <rect x="38" y="124" width="172" height="22" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="124" y="139" text-anchor="middle" font-size="6.5" fill="var(--muted)">traces（又一套）</text>
  <text x="124" y="156" text-anchor="middle" font-size="6.5" fill="var(--faint)">事后费劲拼回去</text>
  <rect x="260" y="42" width="230" height="120" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="375" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Langfuse：一条宽事件 observation</text><text x="375" y="80" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">输入 · 输出 · 模型 · 用量 · 耗时</text><text x="375" y="94" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">+ 任意自定义属性（高基数）</text><text x="375" y="112" text-anchor="middle" font-size="6.5" fill="var(--muted)">trace = 把相关 observation 串起来的句柄</text><text x="375" y="130" text-anchor="middle" font-size="6.5" fill="var(--faint)">可任意切片/分组/过滤</text><text x="375" y="146" text-anchor="middle" font-size="6.5" fill="var(--faint)">调查 unknown unknowns，不必预建指标</text>
  <rect x="520" y="56" width="176" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="608" y="74" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">不可变：追加</text><text x="608" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">写进去就不动，只追加新行</text>
  <rect x="520" y="110" width="176" height="52" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="608" y="128" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">为何不更新？</text><text x="608" y="143" text-anchor="middle" font-size="6.5" fill="var(--muted)">更新逼着读时去重</text><text x="608" y="154" text-anchor="middle" font-size="6.5" fill="var(--muted)">= 海量数据的隐藏查询成本</text>
  <line x1="224" y1="102" x2="258" y2="102" stroke="var(--accent)" stroke-width="1.4"/><polygon points="258,102 249,98 249,106" fill="var(--accent)"/>
  <line x1="490" y1="90" x2="518" y2="82" stroke="var(--teal)" stroke-width="1.3"/><polygon points="518,82 509,81 511,89" fill="var(--teal)"/>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">第13课：ClickHouse 用 ReplacingMergeTree(event_ts,is_deleted) + 读时 FINAL，把「同实体多次写入」变成「追加新行、查时保留最新」</text>
  <text x="360" y="206" text-anchor="middle" font-size="8" fill="var(--faint)">把「改」变成「追加 + 合并」——这是高规模写入扛得住的关键，也是不可变与宽事件的共谋</text>
</svg>
<div class="figcap"><b>宽事件 + 不可变</b>：<code>ARCHITECTURE_PRINCIPLES.md</code> 原则 1-4——「observation 为主要分析单位」「宽而富的事件优于碎片化的 metrics/logs/traces」「保住高基数上下文调查 unknown unknowns」「偏好不可变/追加，更新会造成读时去重的隐藏成本」。落地见第 5/6 课领域模型、第 13 课 ReplacingMergeTree、第 41 课查询引擎。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">主题一</span><span class="name">宽事件（observability 2.0）</span></div><div class="ld">一次操作 = 一条带全部上下文的宽事件。observation 是分析单位、trace 是关联句柄。保住高基数 → 能回答<strong>事前没想到的问题</strong>，而不必为每个未来问题预建指标。这是「探索式可观测」的根。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">主题二</span><span class="name">不可变（追加而非更新）</span></div><div class="ld">高吞吐下偏好追加。更新会逼出读时去重的隐藏成本，所以用 ReplacingMergeTree(event_ts, is_deleted)「追加新行 + 查时按 event_ts 保留最新」替代「原地改」。<strong>不可变让写入路径简单、可预测、能水平扩展。</strong></div></div>
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
  <rect x="24" y="40" width="150" height="50" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">请求路径（薄）</text><text x="99" y="76" text-anchor="middle" font-size="6.5" fill="var(--muted)">校验·落S3·塞队列→立刻返回</text>
  <rect x="200" y="40" width="150" height="50" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="275" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">BullMQ + worker</text><text x="275" y="76" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">重活后台慢慢消化</text>
  <rect x="200" y="100" width="320" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="115" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--accent-ink)">异步主题的反复变奏</text><text x="360" y="127" text-anchor="middle" font-size="6.5" fill="var(--muted)">两级 fan-out · 幂等 · 水位线 · 分布式锁（第30/43/46/52课）</text>
  <line x1="174" y1="65" x2="198" y2="65" stroke="var(--accent)" stroke-width="1.4"/><polygon points="198,65 189,61 189,69" fill="var(--accent)"/>
  <rect x="40" y="156" width="200" height="74" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="140" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">Postgres（OLTP）</text><text x="140" y="193" text-anchor="middle" font-size="6.5" fill="var(--muted)">配置/用户/权限·强一致低频改</text><text x="140" y="207" text-anchor="middle" font-size="6.5" fill="var(--faint)">结构化元数据</text><text x="140" y="220" text-anchor="middle" font-size="6.5" fill="var(--faint)">「源真相」</text>
  <rect x="260" y="156" width="200" height="74" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="360" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">ClickHouse（OLAP）</text><text x="360" y="193" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">海量事件·列存+分区+排序键</text><text x="360" y="207" text-anchor="middle" font-size="6.5" fill="var(--muted)">扫几十亿行做聚合可行</text><text x="360" y="220" text-anchor="middle" font-size="6.5" fill="var(--faint)">谨慎反范式去 join</text>
  <rect x="480" y="156" width="200" height="74" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="580" y="176" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">对象存储 S3</text><text x="580" y="193" text-anchor="middle" font-size="6.5" fill="var(--muted)">大块负载·完整输入输出/媒体</text><text x="580" y="207" text-anchor="middle" font-size="6.5" fill="var(--faint)">列表只取紧凑表示</text><text x="580" y="220" text-anchor="middle" font-size="6.5" fill="var(--faint)">详情才取大字段（第22/24课）</text>
  <line x1="275" y1="134" x2="160" y2="154" stroke="var(--faint)" stroke-width="1"/><line x1="320" y1="134" x2="360" y2="154" stroke="var(--accent)" stroke-width="1.2"/><line x1="360" y1="134" x2="560" y2="154" stroke="var(--faint)" stroke-width="1"/>
</svg>
<div class="figcap"><b>异步 + 双(三)存储</b>：<code>ARCHITECTURE_PRINCIPLES.md</code> 原则 5-7、10——反范式去热路径 join、为列式访问设计（窄选列/时间界/排序键/裁剪）、列表用紧凑表示大字段延后、保住近实时调试。异步骨架见第 12-19 课摄取，反复变奏见第 30/43/46/52 课；三存储见第 2/22/24/52 课。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">主题三</span><span class="name">异步（队列 + worker）</span></div><div class="ld">请求路径只接收、不干重活；重活进 BullMQ 由 worker 后台处理。削峰、解耦、可重试。其衍生纪律——fan-out、幂等、水位、锁——在 eval/计量/集成/迁移里反复出现，是同一主题的不同变奏。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">主题四</span><span class="name">双(三)存储（各归各家）</span></div><div class="ld">Postgres 扛 OLTP 元数据、ClickHouse 扛 OLAP 海量事件（列存）、S3 放大块负载。配套谨慎反范式、列表紧凑/详情取大字段。<strong>让不同形状的数据落进最合适的引擎</strong>，是性能与成本的根。</div></div>
</div>
<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/redis/ingestionQueue.ts</span><span class="ln">异步·分片队列</span></div>
  <pre class="code"><span class="cm">// 异步主题落到代码：摄取队列按「分片」fan-out，由 worker 后台消费</span>
<span class="kw">export class</span> <span class="fn">IngestionQueue</span> {
  <span class="kw">public static</span> <span class="fn">getShardNames</span>() {
    <span class="kw">return</span> Array.from(
      { length: env.LANGFUSE_INGESTION_QUEUE_SHARD_COUNT },
      (_, i) =&gt; `${QueueName.IngestionQueue}${i &gt; 0 ? `-${i}` : ""}`,
    );   <span class="cm">// → IngestionQueue, IngestionQueue-1, IngestionQueue-2 …</span>
  }
}</pre>
</div>
""")

# (L54 sec3 below)

_ZH54.append(r"""
<h2>主题五·六：多租户 + 成本（数据归谁、什么值得做）</h2>
<p><strong>多租户（multi-tenancy）</strong>是贯穿全栈的一条隐线：<strong>几乎每张表、每个查询、每条队列消息都带着 projectId</strong>。从第48课的登录（session 注入组织/项目成员关系）、到第49课的 RBAC scope 与 API key scope、再到第50课按 plan 给的 entitlement，构成层层收窄的隔离；第46课的分析集成、第52课的删除都<strong>按项目 fan-out</strong>。多租户不是某一处的功能，而是一条「<strong>任何数据都明确归属、任何访问都明确授权</strong>」的纪律——它决定了一个平台能不能安全地让成千上万个互不信任的租户共用同一套基础设施。</p>

<p><strong>成本（cost）</strong>是把前五个主题「管住」的那条约束。架构原则里写得很直白：<strong>把成本与运维简单性当作架构约束</strong>——「额外的数据库、队列、物化视图、迁移，都必须挣回它们的长期运维负担」。这解释了很多克制的选择：API 契约要求时间窗口、暴露字段选择、用 token 分页、不给「能扫全部历史」的危险默认（第27课）；模型与用量成本被显式计量（第42/43课）。<strong>不是「能加就加」，而是「每一个新增的活动部件，都要先证明自己值这份维护成本」</strong>——这份克制，恰恰是系统能长期简单、可维护的根。</p>

<svg viewBox="0 0 720 240" role="img" aria-label="六个设计主题都从同一目标逼出：在宽的结构化事件上做高吞吐、探索式可观测且是平台；探索式前提逼出①宽事件保高基数，高吞吐与横向扩展前提逼出②不可变查时去重、③异步削峰解耦、④双存储按形状分引擎，平台与长期前提逼出⑤多租户处处带projectId、⑥成本每个部件须挣回运维负担">
  <rect x="0" y="0" width="720" height="240" fill="var(--bg)"></rect>
  <rect x="12" y="32" width="696" height="24" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="360" y="49" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">目标：在宽的结构化事件上做高吞吐、探索式可观测（且是平台）</text>
  <rect x="20" y="66" width="150" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="91" font-size="9.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">前提：探索式</text>
  <rect x="20" y="118" width="150" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="143" font-size="9.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">前提：高吞吐+扩展</text>
  <rect x="20" y="170" width="150" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="195" font-size="9.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">前提：平台+长期</text>
  <rect x="220" y="66" width="480" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="234" y="91" font-size="9.5" fill="var(--accent-ink)">① 宽事件：保住高基数，调查 unknown unknowns</text>
  <rect x="220" y="118" width="156" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="298" y="143" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">② 不可变（查时去重）</text>
  <rect x="384" y="118" width="140" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="454" y="143" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">③ 异步（削峰）</text>
  <rect x="532" y="118" width="168" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="616" y="143" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">④ 双存储（按形状）</text>
  <rect x="220" y="170" width="230" height="40" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="335" y="195" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">⑤ 多租户（处处 projectId）</text>
  <rect x="460" y="170" width="240" height="40" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="580" y="195" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">⑥ 成本（部件须挣回运维）</text>
  <line x1="170" y1="86" x2="220" y2="86" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="170" y1="138" x2="220" y2="138" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="170" y1="190" x2="220" y2="190" stroke="var(--accent)" stroke-width="2"></line>
  <text x="360" y="232" font-size="10" text-anchor="middle" fill="var(--muted)">拆开任一个，其余都显别扭——架构是一组彼此印证、共同服务于同一目标的取舍</text>
</svg>

<table class="t">
  <thead><tr><th>主题</th><th>一句话</th><th>在哪些课见过</th></tr></thead>
  <tbody>
    <tr><td><b>① 宽事件</b></td><td>一条又宽又富的事件，保住高基数调查 unknown unknowns</td><td>L05/L06 领域模型 · L41 查询引擎</td></tr>
    <tr><td><b>② 不可变</b></td><td>追加而非更新；改 = 追加新行 + 查时去重(保留最新)</td><td>L13 ReplacingMergeTree · L18</td></tr>
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

<p><strong>Immutability</strong> is wide events' natural partner. Under high-throughput telemetry, Langfuse <strong>favors append over update</strong>: an event written basically doesn't move. Why? Because "<strong>updates</strong>" are shockingly costly at massive scale — they force <strong>read-time deduplication</strong>, conjuring hidden query costs. In Lesson 13 you saw how ClickHouse uses <strong>ReplacingMergeTree(event_ts, is_deleted) + read-time FINAL deduplication</strong> to swallow "the same entity written multiple times": it doesn't really modify old rows but appends new ones and <strong>keeps the latest version by event_ts</strong> at query time. <strong>Turning "modify" into "append + dedup at query" is the key to write-side surviving at high scale.</strong></p>

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
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">L13: ReplacingMergeTree(event_ts, is_deleted) + read-time FINAL → "entity written N times" = "append rows, keep latest at query"</text>
  <text x="360" y="206" text-anchor="middle" font-size="8" fill="var(--faint)">Turning "modify" into "append + merge" — the key to high-scale write survival, and the conspiracy between immutability and wide events</text>
</svg>
<div class="figcap"><b>Wide events + immutability</b>: <code>ARCHITECTURE_PRINCIPLES.md</code> principles 1-4 — "observation as the primary analytical unit," "wide richly-attributed events over fragmented metrics/logs/traces," "preserve high-cardinality context to investigate unknown unknowns," "favor immutable/append; updates create read-time-dedup hidden cost." Landed in Lessons 5/6 domain models, Lesson 13 ReplacingMergeTree, Lesson 41 query engine.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">theme 1</span><span class="name">wide events (observability 2.0)</span></div><div class="ld">One operation = one wide event with full context. The observation is the analytical unit, the trace a correlation handle. Preserving high cardinality → answer <strong>questions you didn't anticipate</strong>, without pre-building a metric per future question. This is the root of "exploratory observability."</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">theme 2</span><span class="name">immutability (append not update)</span></div><div class="ld">High-throughput favors append. Updates force read-time-dedup hidden cost, so ReplacingMergeTree(event_ts, is_deleted)'s "append new rows + keep the latest by event_ts at query" replaces "modify in place." <strong>Immutability keeps the write path simple, predictable, and horizontally scalable.</strong></div></div>
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
<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/redis/ingestionQueue.ts</span><span class="ln">async · sharded queue</span></div>
  <pre class="code"><span class="cm">// The async theme in code: the ingestion queue fans out across "shards", consumed by the worker</span>
<span class="kw">export class</span> <span class="fn">IngestionQueue</span> {
  <span class="kw">public static</span> <span class="fn">getShardNames</span>() {
    <span class="kw">return</span> Array.from(
      { length: env.LANGFUSE_INGESTION_QUEUE_SHARD_COUNT },
      (_, i) =&gt; `${QueueName.IngestionQueue}${i &gt; 0 ? `-${i}` : ""}`,
    );   <span class="cm">// → IngestionQueue, IngestionQueue-1, IngestionQueue-2 …</span>
  }
}</pre>
</div>
""")

_EN54.append(r"""
<h2>Themes 5 & 6: multi-tenancy + cost (who data belongs to, what's worth doing)</h2>
<p><strong>Multi-tenancy</strong> is a hidden thread running full-stack: <strong>nearly every table, every query, every queue message carries a projectId</strong>. From Lesson 48's login (session injecting org/project memberships), to Lesson 49's RBAC scopes and API-key scopes, to Lesson 50's plan-based entitlements, they form layer-upon-layer narrowing isolation; Lesson 46's analytics integrations and Lesson 52's deletion both <strong>fan out per project</strong>. Multi-tenancy isn't a feature in one place but a discipline of "<strong>every datum has a clear owner, every access has clear authorization</strong>" — it decides whether a platform can safely let thousands of mutually-untrusting tenants share one infrastructure.</p>

<p><strong>Cost</strong> is the constraint that "reins in" the first five themes. The architecture principles say it bluntly: <strong>treat cost and operational simplicity as architectural constraints</strong> — "extra databases, queues, materialized views, and migrations must earn their long-term operational burden." This explains many restrained choices: API contracts require time windows, expose field selection, use token pagination, give no dangerous "can scan all history" defaults (Lesson 27); model and usage cost are explicitly metered (Lessons 42/43). <strong>Not "add it because you can," but "every new moving part must first prove it's worth its maintenance cost"</strong> — this restraint is precisely the root of a system staying simple and maintainable long-term.</p>

<svg viewBox="0 0 720 240" role="img" aria-label="all six design themes derive from one goal: high-throughput, exploratory observability over wide structured events, on a platform; the exploratory premise forces 1 wide events to preserve high cardinality, the high-throughput and scale premise forces 2 immutability with read-time dedup, 3 async to absorb spikes, 4 dual storage by access shape, and the platform and long-term premise forces 5 multi-tenancy with projectId everywhere and 6 cost where every moving part must earn its maintenance">
  <rect x="0" y="0" width="720" height="240" fill="var(--bg)"></rect>
  <rect x="12" y="32" width="696" height="24" rx="6" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="360" y="49" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">goal: high-throughput, exploratory observability over wide structured events (a platform)</text>
  <rect x="20" y="66" width="150" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="91" font-size="9.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">premise: exploratory</text>
  <rect x="20" y="118" width="150" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="143" font-size="9.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">premise: throughput+scale</text>
  <rect x="20" y="170" width="150" height="40" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="95" y="195" font-size="9.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">premise: platform+long-term</text>
  <rect x="220" y="66" width="480" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="234" y="91" font-size="9.5" fill="var(--accent-ink)">1 wide events: keep high cardinality, investigate unknown unknowns</text>
  <rect x="220" y="118" width="156" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="298" y="143" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">2 immutable (dedup)</text>
  <rect x="384" y="118" width="140" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="454" y="143" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">3 async (absorb)</text>
  <rect x="532" y="118" width="168" height="40" rx="8" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="616" y="143" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">4 dual store (by shape)</text>
  <rect x="220" y="170" width="230" height="40" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="335" y="195" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">5 multi-tenancy (projectId)</text>
  <rect x="460" y="170" width="240" height="40" rx="8" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="580" y="195" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">6 cost (parts earn maintenance)</text>
  <line x1="170" y1="86" x2="220" y2="86" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="170" y1="138" x2="220" y2="138" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="170" y1="190" x2="220" y2="190" stroke="var(--accent)" stroke-width="2"></line>
  <text x="360" y="232" font-size="10" text-anchor="middle" fill="var(--muted)">remove any one and the rest feel off — architecture is a set of mutually-reinforcing trade-offs for one goal</text>
</svg>

<table class="t">
  <thead><tr><th>Theme</th><th>In a sentence</th><th>Seen in lessons</th></tr></thead>
  <tbody>
    <tr><td><b>① wide events</b></td><td>one wide rich event, preserving high cardinality to investigate unknown unknowns</td><td>L05/L06 domain models · L41 query engine</td></tr>
    <tr><td><b>② immutability</b></td><td>append not update; modify = append new rows + dedup at query (keep latest)</td><td>L13 ReplacingMergeTree · L18</td></tr>
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


# ══════════════════════════════════════════════════════════════════════
# L55 · 终章·一条 trace 的完整一生 / Capstone: the full life of a trace
# ══════════════════════════════════════════════════════════════════════
_ZH55 = []
_EN55 = []

# (L55 sections below)

_ZH55.append(r"""
<p class="lead">
最后一课，我们做一件浪漫的事：<strong>跟着一条 trace，走完它的一生</strong>。前面 54 课，每一课都像在解剖一个器官——这一课，让这条 trace <strong>活过来</strong>，从它在你应用里<strong>出生</strong>的那一毫秒，到被摄取、落库、被查看、被评分、触发自动化、最终在保留期到点时<strong>谢幕</strong>。沿途，我们会在每个驿站标出「这是第几课讲的」，让你亲眼看见：那些你逐课学过的零件，是怎么<strong>严丝合缝地咬合成一台完整机器</strong>的。
读完这一程，你对 Langfuse 的理解会从「知道每个部件」升级为「看见整个系统如何协作」。而你会发现，这整台机器，归根到底只是在<strong>从容地回答一个问题</strong>：你的 AI 应用，到底做了什么——而你怎么<strong>记录它、找到它、评判它、并据此行动</strong>？
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  把一条 trace 想象成一个<strong>「快递包裹」</strong>的一生。它在<strong>寄件人手里诞生</strong>（你的应用调用 LLM，SDK 把这次调用打包）；在<strong>分拣中心被高速处理</strong>（摄取链路：扫码登记、分拣、入库）；在<strong>仓库里被妥善存放</strong>（三个库各放一部分：单号信息、明细、大件）；被人<strong>在系统里查询追踪</strong>（列表、详情、按时间线看它的来龙去脉）；被<strong>质检员抽检评分</strong>（评估与监控）；触发<strong>下游联动</strong>（到货通知、转寄、归档）；最后在<strong>保管期满时被销毁</strong>，且三个库一处不漏地清干净。
  你前面 54 课，是分别参观了寄件台、分拣机、货架、查询台、质检站、通知中心、销毁间——这一课，是<strong>跟着同一个包裹，把这些站点一次性串成一条流水线</strong>，看它们如何首尾相接、共同完成「让每一次 AI 调用都<strong>有据可查、可评可控</strong>」这件事。
</div>
""")

# (L55 sec1 below)

_ZH55.append(r"""
<h2>第一程：出生 → 摄取 → 落库</h2>
<p><strong>① 出生（第12课）。</strong>你的应用调一次 LLM，<strong>SDK</strong> 就地创建一条 trace 和它下面的若干 observation，把输入、输出、模型、用量都记下来，<strong>攒成一批</strong>，异步 POST 到摄取 API——你的主流程<strong>几乎无感</strong>。<strong>② 摄取（第13-19课）。</strong>API 先用 API key 认证（<strong>第49课</strong>的两层哈希校验），把原始事件<strong>落进 S3</strong>、把任务<strong>塞进 Redis 队列</strong>就立刻 200 返回——这就是「<strong>快接收</strong>」。然后 <strong>worker</strong> 从队列取出，做校验、解析、可能的合并，<strong>upsert 进 ClickHouse</strong>。<strong>③ 落库（第13课）。</strong>这条 trace 最终<strong>散成三份</strong>安家：可分析的事件明细进 <strong>ClickHouse</strong>（不可变、ReplacingMergeTree 查时去重保留最新）、大块输入输出进 <strong>S3</strong>、相关元数据进 <strong>Postgres</strong>。出生到落库，第10课「双(三)存储」与第54课「异步、不可变」两大主题，在这里第一次合奏。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="一条trace的一生时间线：出生(SDK创建,L12)→摄取(API认证落S3塞Redis队列worker处理,L13-19/L49)→落库(散成三份:ClickHouse事件+S3负载+Postgres元数据)→被读(列表详情会话REST,L20-27)→被评估(eval评分监控告警数据集,L28-36)→被作用(自动化webhook/Slack分析导出批量,L44-47)→退场(保留期跨三存储删除,L52)，全程被OTel观测(L51)、按plan门控(L50)、按project隔离">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一条 trace 的一生：七个驿站，串成一条流水线</text>
  <line x1="40" y1="70" x2="690" y2="70" stroke="var(--faint)" stroke-width="2"/><polygon points="690,70 680,65 680,75" fill="var(--faint)"/>
  <circle cx="70" cy="70" r="6" fill="var(--teal)"/><text x="70" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--teal)">①出生</text><text x="70" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">SDK创建</text><text x="70" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L12</text>
  <circle cx="170" cy="70" r="6" fill="var(--blue)"/><text x="170" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--blue)">②摄取</text><text x="170" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">S3+队列+worker</text><text x="170" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L13-19/L49</text>
  <circle cx="280" cy="70" r="6" fill="var(--accent)"/><text x="280" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">③落库</text><text x="280" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">CH+S3+PG</text><text x="280" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L13</text>
  <circle cx="390" cy="70" r="6" fill="var(--blue)"/><text x="390" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--blue)">④被读</text><text x="390" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">列表/详情/REST</text><text x="390" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L20-27</text>
  <circle cx="500" cy="70" r="6" fill="var(--accent)"/><text x="500" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">⑤被评估</text><text x="500" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">eval/监控/数据集</text><text x="500" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L28-36</text>
  <circle cx="600" cy="70" r="6" fill="var(--blue)"/><text x="600" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--blue)">⑥被作用</text><text x="600" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">自动化/导出</text><text x="600" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L44-47</text>
  <circle cx="675" cy="70" r="6" fill="var(--muted)"/><text x="672" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--muted)">⑦退场</text><text x="672" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">跨存储删除</text><text x="672" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L52</text>
  <rect x="40" y="138" width="650" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-dasharray="5 3"/><text x="365" y="156" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">贯穿全程的三条隐线</text><text x="365" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">全程被平台自己的 OTel/日志观测(L51) · 按组织 plan 门控功能(L50) · 每一步都按 projectId 隔离(多租户)</text>
  <rect x="40" y="194" width="650" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="365" y="211" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">六大主题在这条流水线上各就各位</text><text x="365" y="226" text-anchor="middle" font-size="6.5" fill="var(--muted)">宽事件(数据形状)·不可变(怎么写)·异步(在哪干)·双存储(存哪)·多租户(归谁)·成本(什么值得做)</text>
</svg>
<div class="figcap"><b>一条 trace 的完整生命周期</b>：出生(L12 SDK) → 摄取(L13-19 摄取链路 + L49 API key 认证) → 落库(L13 ClickHouse/S3/Postgres) → 被读(L20-27) → 被评估(L28-36) → 被作用(L44-47) → 退场(L52)。三条隐线贯穿：自观测(L51)、plan 门控(L50)、projectId 多租户隔离。</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>出生：SDK 就地打包（L12）</h4><p>应用调 LLM，SDK 创建 trace + observation，记下输入/输出/模型/用量，攒批异步 POST——主流程几乎无感。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>摄取：快接收 + 异步处理（L13-19, L49）</h4><p>API 用 API key 两层哈希认证、原始事件落 S3、塞 Redis 队列即返回；worker 取出做校验解析、upsert 进 ClickHouse。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>落库：散成三份安家（L13）</h4><p>事件明细→ClickHouse(不可变,查时合并)、大块负载→S3、元数据→Postgres。「双(三)存储 + 异步 + 不可变」三主题首次合奏。</p></div></div>
</div>
<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/queues/ingestionQueue.ts</span><span class="ln">落库这一刻</span></div>
  <pre class="code"><span class="cm">// 「落库」的真相：worker 取出队列消息后，把这条实体的多条事件 merge 后写入</span>
<span class="kw">await new</span> <span class="fn">IngestionService</span>(redis, prisma, clickhouseWriter, clickhouseClient())
  .<span class="fn">mergeAndWrite</span>(
    getClickhouseEntityType(events[0].type),        <span class="cm">// trace / observation / score</span>
    job.data.payload.authCheck.scope.projectId,     <span class="cm">// 多租户隔离键</span>
    canonicalEntityId,
    firstS3WriteTime,
    events,                                          <span class="cm">// 同一 id 的多条事件</span>
    forwardToEventsTable,
  );</pre>
</div>
""")

# (L55 sec2 below)

_ZH55.append(r"""
<h2>第二程：被读 → 被评估</h2>
<p><strong>④ 被读（第20-27课）。</strong>数据进来了，人要看。trace 出现在<strong>列表页</strong>——这里只查 ClickHouse 的<strong>紧凑表示</strong>（窄选列、时间窗、token 分页，第24课），快而省；你点进<strong>详情页</strong>，才把完整的 observation 树和大块输入输出从 S3 取出来（第25课）；<strong>会话视图</strong>把同一用户的多条 trace 串起来看（第26课）；而程序想读，走<strong>公共 REST API</strong>（第27课，scale-aware 契约）。<strong>⑤ 被评估（第28-36课）。</strong>光看不够，还要<strong>判好坏</strong>：一条 <strong>LLM-as-judge</strong> 评估器读这条 trace 的输入输出、调一个裁判模型给它评分写回 score（第28-31课）；<strong>监控</strong>盯着分数的聚合，越过阈值就发告警（第33课）；这条 trace 还可能被<strong>加进数据集</strong>当测试用例、在<strong>实验</strong>里和别的 prompt/模型对比（第34-36课）。注意这里出现了一个优雅的<strong>闭环</strong>：trace 产生 score、score 又能驱动监控与实验，<strong>观测的产物反过来改进应用</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="被读与被评估：落库的trace一面被读(列表查CH紧凑表示L24/详情取S3大字段L25/会话L26/REST L27)，一面被评估(LLM裁判评分L28-31→score写回，监控盯聚合越阈值告警L33，加数据集做实验L34-36)；score又驱动监控与实验形成闭环——观测产物反哺应用">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">既被人看，也被评判——还形成改进闭环</text>
  <rect x="280" y="44" width="160" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">落库的 trace</text><text x="360" y="80" text-anchor="middle" font-size="6.5" fill="var(--muted)">CH 明细 + S3 负载 + PG 元数据</text>
  <rect x="24" y="110" width="200" height="96" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="124" y="128" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">④ 被读（L20-27）</text><text x="124" y="145" text-anchor="middle" font-size="6.5" fill="var(--muted)">列表：CH 紧凑表示(L24)</text><text x="124" y="158" text-anchor="middle" font-size="6.5" fill="var(--muted)">详情：取 S3 大字段(L25)</text><text x="124" y="171" text-anchor="middle" font-size="6.5" fill="var(--muted)">会话：串同用户(L26)</text><text x="124" y="184" text-anchor="middle" font-size="6.5" fill="var(--muted)">REST：scale-aware 契约(L27)</text><text x="124" y="198" text-anchor="middle" font-size="6.5" fill="var(--faint)">人/程序读它</text>
  <rect x="496" y="110" width="200" height="96" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="596" y="128" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">⑤ 被评估（L28-36）</text><text x="596" y="145" text-anchor="middle" font-size="6.5" fill="var(--muted)">LLM 裁判评分→score(L28-31)</text><text x="596" y="158" text-anchor="middle" font-size="6.5" fill="var(--muted)">监控盯聚合越阈值告警(L33)</text><text x="596" y="171" text-anchor="middle" font-size="6.5" fill="var(--muted)">加数据集/做实验(L34-36)</text><text x="596" y="186" text-anchor="middle" font-size="6.5" fill="var(--muted)">人工标注补 score(L32)</text>
  <line x1="280" y1="74" x2="224" y2="120" stroke="var(--blue)" stroke-width="1.3"/><polygon points="224,120 233,116 230,124" fill="var(--blue)"/>
  <line x1="440" y1="74" x2="496" y2="120" stroke="var(--teal)" stroke-width="1.3"/><polygon points="496,120 487,116 490,124" fill="var(--teal)"/>
  <path d="M 596 206 q 0 28 -236 6" fill="none" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 3"/><polygon points="360,213 369,210 367,218" fill="var(--accent)"/>
  <text x="360" y="224" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">闭环：score 驱动监控与实验 → 反过来改进 prompt/模型/应用</text>
</svg>
<div class="figcap"><b>被读 + 被评估 + 闭环</b>：读路径 L20-27（列表 CH 紧凑表示、详情取 S3、会话、公共 REST）；评估 L28-36（LLM-as-judge 写回 score、监控聚合告警、人工标注、数据集/实验）。score 既是观测产物，又反向驱动监控与实验——形成「观测→评估→改进」的闭环。</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">4</div><div class="sc"><h4>被读：列表快、详情全（L20-27）</h4><p>列表只查 CH 紧凑表示(窄列/时间窗/token 分页)，详情才从 S3 取完整树与大字段；会话串同用户；REST 给程序读。「双存储 + scale-aware 契约 + 成本」主题在此。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>被评估：判好坏、成闭环（L28-36）</h4><p>LLM 裁判/人工标注给 trace 评分写回 score；监控盯分数聚合越阈值告警；加数据集做实验。score 反向驱动改进——观测的产物反哺应用。</p></div></div>
</div>
""")

# (L55 sec3 below)

_ZH55.append(r"""
<h2>第三程：被作用 → 退场（与三条隐线）</h2>
<p><strong>⑥ 被作用（第44-47课）。</strong>这条 trace 不只是躺着被看——它能<strong>触发行动</strong>。它的某个变化（或它引发的告警）匹配上一个<strong>自动化</strong>的触发器，就投递一个 <strong>webhook</strong>（第44课，一路 SSRF 纵深防御）或发到 <strong>Slack</strong>（第45课）；它会被<strong>分析集成</strong>源源不断地导进你自己的 PostHog/S3（第46课，两级 fan-out + 增量水位）；你也可以把它连同一票筛出来的 trace 一起<strong>批量导出</strong>成 CSV（第47课）。<strong>⑦ 退场（第52课）。</strong>数据不是永生的：保留期一到，它会被<strong>跨三个存储一处不漏地删干净</strong>（先 ClickHouse + S3、最后 Postgres，留住重试锚点）。一条 trace 的一生，至此圆满落幕。</p>

<p>而这整段旅程，始终被<strong>三条隐线</strong>笼罩：① 它从生到死的每一步，都被平台<strong>自己的 OTel/日志观测着</strong>（第51课，dogfooding——观测工具观测自己）；② 它能用到的每个功能，都被这个组织的 <strong>plan/entitlement 默默门控</strong>（第50课）；③ 它的每一次读、写、删，都被严格<strong>按 projectId 隔离</strong>（多租户），别的租户碰不到。<strong>七个驿站串起骨架，三条隐线织成底色</strong>——这，就是 Langfuse 这台机器的全貌。</p>

<svg viewBox="0 0 720 220" role="img" aria-label="一条 trace 的第三程：⑥ 被作用，落库的活跃 trace 触发下游行动——webhook（L44）、Slack（L45）、分析集成导进 PostHog/S3（L46）、批量导出 CSV（L47）；⑦ 退场，保留期到后跨三存储一处不漏地删除，先 ClickHouse 加 S3 再 Postgres 并留重试锚点；全程被自观测 L51、plan 门控 L50、projectId 隔离三条隐线笼罩">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="20" font-size="11" font-weight="700" fill="var(--accent-ink)">被作用：触发下游行动；退场：跨三存储删干净</text>
  <rect x="16" y="84" width="140" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="86" y="108" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">落库的 trace</text>
  <text x="86" y="125" font-size="8.5" text-anchor="middle" fill="var(--muted)">活跃期</text>
  <text x="240" y="38" font-size="9.5" font-weight="700" fill="var(--accent-ink)">⑥ 被作用（触发下游）</text>
  <rect x="180" y="44" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="63" font-size="9" text-anchor="middle" fill="var(--ink)">webhook（L44，SSRF 纵深）</text>
  <rect x="180" y="80" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="99" font-size="9" text-anchor="middle" fill="var(--ink)">Slack 富消息（L45）</text>
  <rect x="180" y="116" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="135" font-size="9" text-anchor="middle" fill="var(--ink)">分析集成 → PostHog/S3（L46）</text>
  <rect x="180" y="152" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="171" font-size="9" text-anchor="middle" fill="var(--ink)">批量导出 CSV（L47）</text>
  <line x1="156" y1="106" x2="180" y2="59" stroke="var(--blue)" stroke-width="1.5"></line>
  <line x1="156" y1="110" x2="180" y2="95" stroke="var(--blue)" stroke-width="1.5"></line>
  <line x1="156" y1="118" x2="180" y2="131" stroke="var(--blue)" stroke-width="1.5"></line>
  <line x1="156" y1="124" x2="180" y2="167" stroke="var(--blue)" stroke-width="1.5"></line>
  <rect x="420" y="92" width="284" height="64" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="562" y="114" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑦ 退场（L52）保留期到</text>
  <text x="562" y="132" font-size="9" text-anchor="middle" fill="var(--ink)">跨三存储删除：CH + S3 → PG</text>
  <text x="562" y="148" font-size="8.5" text-anchor="middle" fill="var(--muted)">（PG 留到最后，留重试锚点）</text>
  <line x1="370" y1="124" x2="420" y2="124" stroke="var(--accent)" stroke-width="2" stroke-dasharray="4 3"></line>
  <text x="395" y="118" font-size="8" text-anchor="middle" fill="var(--muted)">活跃期结束</text>
  <text x="360" y="204" font-size="9.5" text-anchor="middle" fill="var(--muted)">三条隐线全程笼罩：自观测(L51) · plan 门控(L50) · projectId 隔离</text>
</svg>

<table class="t">
  <thead><tr><th>一生的驿站</th><th>发生了什么</th><th>课</th><th>主导主题</th></tr></thead>
  <tbody>
    <tr><td>① 出生</td><td>SDK 创建 trace+observation，攒批异步上报</td><td>L12</td><td>异步</td></tr>
    <tr><td>② 摄取</td><td>认证→落 S3→Redis 队列→worker 处理</td><td>L13-19, L49</td><td>异步·多租户</td></tr>
    <tr><td>③ 落库</td><td>散成三份：CH 明细 + S3 负载 + PG 元数据</td><td>L13</td><td>双存储·不可变</td></tr>
    <tr><td>④ 被读</td><td>列表紧凑/详情取大字段/会话/REST</td><td>L20-27</td><td>双存储·成本</td></tr>
    <tr><td>⑤ 被评估</td><td>LLM 裁判评分→score、监控告警、数据集/实验</td><td>L28-36</td><td>宽事件(高基数)</td></tr>
    <tr><td>⑥ 被作用</td><td>webhook/Slack、分析导出、批量导出</td><td>L44-47</td><td>异步·成本</td></tr>
    <tr><td>⑦ 退场</td><td>保留期到，跨三存储删除(留重试锚点)</td><td>L52</td><td>双存储</td></tr>
    <tr><td><b>贯穿</b></td><td>自观测 · plan 门控 · projectId 隔离</td><td>L51·L50·全栈</td><td>多租户·成本</td></tr>
  </tbody>
</table>
""")

_ZH55.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍 · 全书收尾</div>
  <strong>跟完这条 trace 的一生，你该带走的「那个大问题」是什么？</strong> 是这个：<strong>当你的应用把一部分判断交给了一个你无法直接读懂、还时常飘忽的 LLM，你怎么重新拿回「看得见、说得清、控得住」？</strong> Langfuse 这台看似庞大的机器，从头到尾只是在从容地回答它。把这条 trace 的七个驿站连起来读，答案的形状就浮现了——<strong>记录（出生+摄取+落库，把每次调用变成可查的宽事件）→ 找到（被读，在海量里快速定位）→ 评判（被评估，给「好不好」一个可量化的 score）→ 行动（被作用，让结论自动驱动下游）</strong>，最后还得<strong>负责任地退场（删除）</strong>、并且这一切要在<strong>高规模、多租户、可控成本</strong>下成立。你会发现，第54课那六个主题不是抽象口号：宽事件让「记录」保住细节、双存储让「找到」又快又省、异步让「记录与行动」在高吞吐下不塌、多租户让它能服务所有人、成本让它长期养得起。<strong>每一个工程取舍，最终都服务于「把 AI 应用的不可观测，变回可观测」这一件事。</strong><br><br>
  <strong>而你,读完这 55 课,真正应该带走的不是某段源码,是一种「看系统」的眼光。</strong>下次你面对任何一个陌生的复杂系统,别再只问「这个函数干嘛」,而要追问:它的<strong>目标和规模前提</strong>是什么?数据<strong>从哪来、长什么样、到哪去</strong>?哪些活儿<strong>必须同步、哪些可以异步</strong>?哪些状态<strong>必须强一致、哪些可以最终一致</strong>?它怎么<strong>隔离租户、怎么控制成本、怎么观测自己</strong>?——这些问题,正是这 55 课反复演练的。Langfuse 只是一个足够真实、足够完整的<strong>范本</strong>;真正的收获,是你从此能用<strong>架构师的眼睛</strong>,去看见任何系统表象之下那套<strong>彼此印证的取舍</strong>。这趟旅程到这里就结束了,但用这双眼睛去读代码的旅程,才刚刚开始。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>一条 trace 的七个驿站</strong>：出生(L12)→摄取(L13-19,L49)→落库(L13)→被读(L20-27)→被评估(L28-36)→被作用(L44-47)→退场(L52)。每课学的零件，在这条流水线上严丝合缝地咬合。</li>
    <li><strong>三条贯穿全程的隐线</strong>：自观测(L51 dogfooding)、plan/entitlement 门控(L50)、projectId 多租户隔离(全栈)——七驿站串骨架，三隐线织底色。</li>
    <li><strong>一个优雅的闭环</strong>：trace 产生 score，score 驱动监控与实验，反过来改进 prompt/模型/应用——观测的产物反哺应用，这是「LLM 工程平台」的灵魂。</li>
    <li><strong>六大主题各就各位</strong>：宽事件(记录保细节)、不可变+异步(高吞吐扛得住)、双存储(找得快又省)、多租户(服务所有人)、成本(长期养得起)——第54课的六个主题，在这条一生里各司其职。</li>
    <li><strong>带走一种眼光</strong>：Langfuse 回答的大问题是「把 AI 应用的不可观测变回可观测」——记录→找到→评判→行动→负责任退场。你真正该带走的不是某段源码，而是用「目标+规模→取舍」的架构师眼光去看任何系统的能力。<strong>55 课到此为止，但这双眼睛刚刚睁开。</strong></li>
  </ul>
</div>
""")

_EN55.append(r"""
<p class="lead">
For the last lesson, we do something romantic: <strong>follow one trace through its whole life</strong>. The previous 54 lessons each dissected an organ — this one brings the trace <strong>alive</strong>, from the millisecond it's <strong>born</strong> in your app, to being ingested, stored, viewed, scored, triggering automations, and finally <strong>taking its bow</strong> when the retention period expires. Along the way, we mark each station with "this is the lesson that covered it," so you see with your own eyes how the parts you learned lesson by lesson <strong>mesh seamlessly into one complete machine</strong>.
By the end of this journey, your understanding of Langfuse upgrades from "knowing each part" to "seeing the whole system collaborate." And you'll find this whole machine is, at bottom, calmly answering one question: what did your AI app actually do — and how do you <strong>record it, find it, judge it, and act on it</strong>?
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Picture a trace's life as a <strong>"parcel."</strong> It's <strong>born in the sender's hands</strong> (your app calls an LLM, the SDK packages that call); it's <strong>processed at high speed in a sorting center</strong> (the ingestion path: scan, register, sort, shelve); it's <strong>properly stored in a warehouse</strong> (three stores each hold a part: tracking info, details, oversized items); it's <strong>queried and tracked in the system</strong> (lists, details, viewing its story on a timeline); it's <strong>spot-checked and scored by QC</strong> (evaluation and monitoring); it triggers <strong>downstream linkage</strong> (arrival notice, forwarding, archival); and finally, <strong>destroyed when the storage period ends</strong>, with all three stores cleaned missing none.
  Your previous 54 lessons toured the sending desk, the sorter, the shelves, the query counter, the QC station, the notification center, the destruction room separately — this lesson <strong>follows the same parcel, stringing these stations into one assembly line</strong>, watching them connect end to end to jointly accomplish "making every AI call <strong>traceable, assessable, and controllable</strong>."
</div>
""")

_EN55.append(r"""
<h2>Leg one: born → ingested → stored</h2>
<p><strong>① Born (Lesson 12).</strong> Your app calls an LLM, the <strong>SDK</strong> creates a trace and its child observations on the spot, recording input, output, model, usage, <strong>batches them up</strong>, and async-POSTs to the ingestion API — your main flow <strong>barely notices</strong>. <strong>② Ingested (Lessons 13-19).</strong> The API first authenticates by API key (<strong>Lesson 49</strong>'s two-tier hash check), <strong>lands the raw event in S3</strong>, <strong>pushes the task to a Redis queue</strong>, and returns 200 immediately — that's "<strong>receive fast</strong>." Then the <strong>worker</strong> pulls from the queue, validates, parses, possibly merges, and <strong>upserts into ClickHouse</strong>. <strong>③ Stored (Lesson 13).</strong> The trace finally <strong>splits into three copies</strong> to settle: analyzable event detail into <strong>ClickHouse</strong> (immutable, ReplacingMergeTree dedup-at-query keeping the latest), bulky inputs/outputs into <strong>S3</strong>, related metadata into <strong>Postgres</strong>. From birth to storage, Lesson 10's "dual (tri) storage" and Lesson 54's "async, immutability" themes first play in concert here.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="A trace's life timeline: born (SDK creates, L12) → ingested (API auth, land S3, push Redis queue, worker processes, L13-19/L49) → stored (split into three: ClickHouse events + S3 payloads + Postgres metadata) → read (list/detail/session/REST, L20-27) → evaluated (eval scoring, monitor alerts, datasets, L28-36) → acted on (automation webhook/Slack, analytics export, batch, L44-47) → retired (retention cross-store deletion, L52), observed by OTel throughout (L51), gated by plan (L50), isolated by project">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">A trace's life: seven stations, one assembly line</text>
  <line x1="40" y1="70" x2="690" y2="70" stroke="var(--faint)" stroke-width="2"/><polygon points="690,70 680,65 680,75" fill="var(--faint)"/>
  <circle cx="70" cy="70" r="6" fill="var(--teal)"/><text x="70" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--teal)">①born</text><text x="70" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">SDK creates</text><text x="70" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L12</text>
  <circle cx="170" cy="70" r="6" fill="var(--blue)"/><text x="170" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--blue)">②ingest</text><text x="170" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">S3+queue+worker</text><text x="170" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L13-19/L49</text>
  <circle cx="280" cy="70" r="6" fill="var(--accent)"/><text x="280" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">③stored</text><text x="280" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">CH+S3+PG</text><text x="280" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L13</text>
  <circle cx="390" cy="70" r="6" fill="var(--blue)"/><text x="390" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--blue)">④read</text><text x="390" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">list/detail/REST</text><text x="390" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L20-27</text>
  <circle cx="500" cy="70" r="6" fill="var(--accent)"/><text x="500" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">⑤evaluate</text><text x="500" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">eval/monitor/dataset</text><text x="500" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L28-36</text>
  <circle cx="600" cy="70" r="6" fill="var(--blue)"/><text x="600" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--blue)">⑥act on</text><text x="600" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">automation/export</text><text x="600" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L44-47</text>
  <circle cx="675" cy="70" r="6" fill="var(--muted)"/><text x="672" y="52" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--muted)">⑦retire</text><text x="672" y="90" text-anchor="middle" font-size="5.8" fill="var(--muted)">cross-store delete</text><text x="672" y="100" text-anchor="middle" font-size="5.6" fill="var(--faint)">L52</text>
  <rect x="40" y="138" width="650" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-dasharray="5 3"/><text x="365" y="156" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">three hidden threads running throughout</text><text x="365" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">observed by the platform's own OTel/logs (L51) · features gated by org plan (L50) · every step isolated by projectId (multi-tenancy)</text>
  <rect x="40" y="194" width="650" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="365" y="211" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">the six themes take their places on this assembly line</text><text x="365" y="226" text-anchor="middle" font-size="6.4" fill="var(--muted)">wide events(shape)·immutability(how to write)·async(where work)·dual storage(where stored)·multi-tenancy(whose)·cost(what's worth doing)</text>
</svg>
<div class="figcap"><b>A trace's complete lifecycle</b>: born (L12 SDK) → ingested (L13-19 ingestion path + L49 API-key auth) → stored (L13 ClickHouse/S3/Postgres) → read (L20-27) → evaluated (L28-36) → acted on (L44-47) → retired (L52). Three hidden threads throughout: self-observability (L51), plan gating (L50), projectId multi-tenant isolation.</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>Born: SDK packages on the spot (L12)</h4><p>The app calls an LLM, the SDK creates trace + observations, records input/output/model/usage, batches and async-POSTs — the main flow barely notices.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>Ingested: receive fast + process async (L13-19, L49)</h4><p>The API authenticates by API-key two-tier hash, lands the raw event in S3, pushes to a Redis queue and returns; the worker pulls, validates/parses, upserts into ClickHouse.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Stored: split into three to settle (L13)</h4><p>Event detail→ClickHouse (immutable, merge at query), bulky payloads→S3, metadata→Postgres. The "dual (tri) storage + async + immutability" themes first play in concert.</p></div></div>
</div>
<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/queues/ingestionQueue.ts</span><span class="ln">the moment it's stored</span></div>
  <pre class="code"><span class="cm">// What "stored" really is: the worker pops the job, then merges this entity's events and writes them</span>
<span class="kw">await new</span> <span class="fn">IngestionService</span>(redis, prisma, clickhouseWriter, clickhouseClient())
  .<span class="fn">mergeAndWrite</span>(
    getClickhouseEntityType(events[0].type),        <span class="cm">// trace / observation / score</span>
    job.data.payload.authCheck.scope.projectId,     <span class="cm">// the multi-tenant isolation key</span>
    canonicalEntityId,
    firstS3WriteTime,
    events,                                          <span class="cm">// the multiple events for one id</span>
    forwardToEventsTable,
  );</pre>
</div>
""")

_EN55.append(r"""
<h2>Leg two: read → evaluated</h2>
<p><strong>④ Read (Lessons 20-27).</strong> The data's in; people want to see it. The trace appears in the <strong>list view</strong> — which queries only ClickHouse's <strong>compact representation</strong> (narrow field selection, time windows, token pagination, Lesson 24), fast and cheap; you click into the <strong>detail view</strong>, and only then are the full observation tree and bulky inputs/outputs fetched from S3 (Lesson 25); the <strong>session view</strong> strings together one user's multiple traces (Lesson 26); and a program reads it via the <strong>public REST API</strong> (Lesson 27, a scale-aware contract). <strong>⑤ Evaluated (Lessons 28-36).</strong> Seeing isn't enough; you must <strong>judge quality</strong>: an <strong>LLM-as-judge</strong> evaluator reads this trace's input/output, calls a judge model to score it, and writes back a score (Lessons 28-31); a <strong>monitor</strong> watches the aggregate of scores and alerts when crossing a threshold (Lesson 33); the trace may also be <strong>added to a dataset</strong> as a test case and compared against other prompts/models in <strong>experiments</strong> (Lessons 34-36). Notice an elegant <strong>closed loop</strong> here: the trace produces a score, and the score in turn drives monitoring and experiments — <strong>the products of observation feed back to improve the app</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="Read and evaluated: the stored trace is on one side read (list queries CH compact representation L24/detail fetches S3 big fields L25/session L26/REST L27), on the other evaluated (LLM judge scoring L28-31→score written back, monitor watches aggregate alerts on threshold L33, added to dataset for experiments L34-36); the score in turn drives monitoring and experiments forming a closed loop — observation products feed the app">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Both viewed and judged — and forms an improvement loop</text>
  <rect x="280" y="44" width="160" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">the stored trace</text><text x="360" y="80" text-anchor="middle" font-size="6.2" fill="var(--muted)">CH detail + S3 payload + PG metadata</text>
  <rect x="24" y="110" width="200" height="96" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="124" y="128" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">④ read (L20-27)</text><text x="124" y="145" text-anchor="middle" font-size="6.2" fill="var(--muted)">list: CH compact repr (L24)</text><text x="124" y="158" text-anchor="middle" font-size="6.2" fill="var(--muted)">detail: fetch S3 big fields (L25)</text><text x="124" y="171" text-anchor="middle" font-size="6.2" fill="var(--muted)">session: string one user (L26)</text><text x="124" y="184" text-anchor="middle" font-size="6.2" fill="var(--muted)">REST: scale-aware contract (L27)</text><text x="124" y="198" text-anchor="middle" font-size="5.8" fill="var(--faint)">humans/programs read it</text>
  <rect x="496" y="110" width="200" height="96" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="596" y="128" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">⑤ evaluated (L28-36)</text><text x="596" y="145" text-anchor="middle" font-size="6.2" fill="var(--muted)">LLM judge scores→score (L28-31)</text><text x="596" y="158" text-anchor="middle" font-size="6.2" fill="var(--muted)">monitor watches aggregate, alerts (L33)</text><text x="596" y="171" text-anchor="middle" font-size="6.2" fill="var(--muted)">add to dataset / experiment (L34-36)</text><text x="596" y="186" text-anchor="middle" font-size="6.2" fill="var(--muted)">human annotation adds score (L32)</text>
  <line x1="280" y1="74" x2="224" y2="120" stroke="var(--blue)" stroke-width="1.3"/><polygon points="224,120 233,116 230,124" fill="var(--blue)"/>
  <line x1="440" y1="74" x2="496" y2="120" stroke="var(--teal)" stroke-width="1.3"/><polygon points="496,120 487,116 490,124" fill="var(--teal)"/>
  <path d="M 596 206 q 0 28 -236 6" fill="none" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 3"/><polygon points="360,213 369,210 367,218" fill="var(--accent)"/>
  <text x="360" y="224" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">loop: score drives monitoring & experiments → in turn improves prompt/model/app</text>
</svg>
<div class="figcap"><b>Read + evaluated + closed loop</b>: read path L20-27 (list CH compact representation, detail fetch S3, session, public REST); evaluation L28-36 (LLM-as-judge writes back score, monitor aggregate alerts, human annotation, datasets/experiments). The score is both an observation product and a driver of monitoring and experiments — forming an "observe→evaluate→improve" loop.</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">4</div><div class="sc"><h4>Read: list fast, detail full (L20-27)</h4><p>The list queries only CH compact representation (narrow columns/time windows/token pagination), detail fetches the full tree and big fields from S3; session strings one user; REST serves programs. The "dual storage + scale-aware contract + cost" themes are here.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>Evaluated: judge quality, close the loop (L28-36)</h4><p>LLM-judge/human annotation scores the trace, writes back; the monitor watches score aggregates and alerts on threshold; add to a dataset for experiments. The score drives improvement in turn — observation products feed the app.</p></div></div>
</div>
""")

_EN55.append(r"""
<h2>Leg three: acted on → retired (with the three hidden threads)</h2>
<p><strong>⑥ Acted on (Lessons 44-47).</strong> The trace doesn't just lie there being viewed — it can <strong>trigger action</strong>. Some change in it (or an alert it raised) matches an <strong>automation</strong>'s trigger, delivering a <strong>webhook</strong> (Lesson 44, with full SSRF defense in depth) or posting to <strong>Slack</strong> (Lesson 45); it's continuously exported into your own PostHog/S3 by <strong>analytics integrations</strong> (Lesson 46, two-level fan-out + incremental watermark); you can also <strong>batch-export</strong> it together with a filtered set of traces to CSV (Lesson 47). <strong>⑦ Retired (Lesson 52).</strong> Data isn't immortal: when the retention period expires, it's <strong>deleted across all three stores missing none</strong> (ClickHouse + S3 first, Postgres last, keeping the retry anchor). A trace's life thus comes to a complete close.</p>

<p>And this whole journey is always wrapped in <strong>three hidden threads</strong>: ① every step from birth to death is <strong>observed by the platform's own OTel/logs</strong> (Lesson 51, dogfooding — the observability tool observing itself); ② every feature it can use is <strong>silently gated by the org's plan/entitlement</strong> (Lesson 50); ③ its every read, write, delete is strictly <strong>isolated by projectId</strong> (multi-tenancy), untouchable by other tenants. <strong>Seven stations string the skeleton, three hidden threads weave the background</strong> — this is the full picture of the Langfuse machine.</p>

<svg viewBox="0 0 720 220" role="img" aria-label="a trace's third leg: 6 acted on, the active stored trace triggers downstream actions — webhook (L44), Slack (L45), analytics integration into PostHog/S3 (L46), batch export to CSV (L47); 7 retired, when retention expires it is deleted across all three stores missing none, ClickHouse plus S3 first then Postgres, keeping the retry anchor; the whole journey is wrapped by three hidden threads: self-observability L51, plan gating L50, projectId isolation">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="20" font-size="11" font-weight="700" fill="var(--accent-ink)">acted on: trigger downstream actions; retired: deleted across all three stores</text>
  <rect x="16" y="84" width="140" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="86" y="108" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">stored trace</text>
  <text x="86" y="125" font-size="8.5" text-anchor="middle" fill="var(--muted)">active life</text>
  <text x="240" y="38" font-size="9.5" font-weight="700" fill="var(--accent-ink)">6 acted on (trigger downstream)</text>
  <rect x="180" y="44" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="63" font-size="9" text-anchor="middle" fill="var(--ink)">webhook (L44, SSRF depth)</text>
  <rect x="180" y="80" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="99" font-size="9" text-anchor="middle" fill="var(--ink)">Slack rich message (L45)</text>
  <rect x="180" y="116" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="135" font-size="9" text-anchor="middle" fill="var(--ink)">analytics → PostHog/S3 (L46)</text>
  <rect x="180" y="152" width="190" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="275" y="171" font-size="9" text-anchor="middle" fill="var(--ink)">batch export to CSV (L47)</text>
  <line x1="156" y1="106" x2="180" y2="59" stroke="var(--blue)" stroke-width="1.5"></line>
  <line x1="156" y1="110" x2="180" y2="95" stroke="var(--blue)" stroke-width="1.5"></line>
  <line x1="156" y1="118" x2="180" y2="131" stroke="var(--blue)" stroke-width="1.5"></line>
  <line x1="156" y1="124" x2="180" y2="167" stroke="var(--blue)" stroke-width="1.5"></line>
  <rect x="420" y="92" width="284" height="64" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="562" y="114" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">7 retired (L52) on retention expiry</text>
  <text x="562" y="132" font-size="9" text-anchor="middle" fill="var(--ink)">delete across stores: CH + S3 → PG</text>
  <text x="562" y="148" font-size="8.5" text-anchor="middle" fill="var(--muted)">(PG last, keep the retry anchor)</text>
  <line x1="370" y1="124" x2="420" y2="124" stroke="var(--accent)" stroke-width="2" stroke-dasharray="4 3"></line>
  <text x="395" y="118" font-size="8" text-anchor="middle" fill="var(--muted)">life ends</text>
  <text x="360" y="204" font-size="9.5" text-anchor="middle" fill="var(--muted)">three hidden threads throughout: self-observability (L51) · plan gating (L50) · projectId isolation</text>
</svg>

<table class="t">
  <thead><tr><th>Life station</th><th>What happened</th><th>Lesson</th><th>Lead theme</th></tr></thead>
  <tbody>
    <tr><td>① born</td><td>SDK creates trace+observation, batches async report</td><td>L12</td><td>async</td></tr>
    <tr><td>② ingested</td><td>auth→land S3→Redis queue→worker processes</td><td>L13-19, L49</td><td>async·multi-tenancy</td></tr>
    <tr><td>③ stored</td><td>split into three: CH detail + S3 payload + PG metadata</td><td>L13</td><td>dual storage·immutability</td></tr>
    <tr><td>④ read</td><td>list compact/detail fetches big fields/session/REST</td><td>L20-27</td><td>dual storage·cost</td></tr>
    <tr><td>⑤ evaluated</td><td>LLM judge scores→score, monitor alerts, datasets/experiments</td><td>L28-36</td><td>wide events(high cardinality)</td></tr>
    <tr><td>⑥ acted on</td><td>webhook/Slack, analytics export, batch export</td><td>L44-47</td><td>async·cost</td></tr>
    <tr><td>⑦ retired</td><td>retention expires, cross-store deletion (keep retry anchor)</td><td>L52</td><td>dual storage</td></tr>
    <tr><td><b>throughout</b></td><td>self-observability · plan gating · projectId isolation</td><td>L51·L50·full-stack</td><td>multi-tenancy·cost</td></tr>
  </tbody>
</table>
""")

_EN55.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off · Send-off</div>
  <strong>Having followed this trace's life, what's "the big question" you should carry away?</strong> It's this: <strong>when your app hands part of its judgment to an LLM you can't directly read and that often drifts, how do you reclaim "visible, articulable, controllable"?</strong> This seemingly-vast Langfuse machine is, from start to finish, calmly answering it. String the trace's seven stations together and the shape of the answer emerges — <strong>record (born+ingested+stored, turning each call into a queryable wide event) → find (read, locating fast among the masses) → judge (evaluated, giving "good or not" a quantifiable score) → act (acted on, letting conclusions auto-drive downstream)</strong>, and finally <strong>retire responsibly (deletion)</strong> — and all of this must hold under <strong>high scale, multi-tenancy, and controlled cost</strong>. You'll find Lesson 54's six themes aren't abstract slogans: wide events let "record" keep detail, dual storage lets "find" be fast and cheap, async keeps "record and act" from collapsing under high throughput, multi-tenancy lets it serve everyone, cost lets it stay affordable long-term. <strong>Every engineering trade-off ultimately serves one thing: turning an AI app's unobservability back into observability.</strong><br><br>
  <strong>And what you should truly carry away from these 55 lessons isn't a snippet of source — it's a way of "seeing systems."</strong> Next time you face any unfamiliar complex system, don't just ask "what does this function do," but probe: what are its <strong>goal and scale premises</strong>? Where does data <strong>come from, what shape is it, where does it go</strong>? Which work <strong>must be sync, which can be async</strong>? Which state <strong>must be strongly consistent, which can be eventually consistent</strong>? How does it <strong>isolate tenants, control cost, observe itself</strong>? — these are exactly the questions these 55 lessons rehearsed over and over. Langfuse is merely a real-enough, complete-enough <strong>specimen</strong>; the real gain is that you can now use an <strong>architect's eyes</strong> to see, beneath any system's surface, the set of <strong>mutually-corroborating trade-offs</strong>. This journey ends here, but the journey of reading code with these eyes has only just begun.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A trace's seven stations</strong>: born (L12)→ingested (L13-19,L49)→stored (L13)→read (L20-27)→evaluated (L28-36)→acted on (L44-47)→retired (L52). The parts learned per lesson mesh seamlessly on this assembly line.</li>
    <li><strong>Three hidden threads throughout</strong>: self-observability (L51 dogfooding), plan/entitlement gating (L50), projectId multi-tenant isolation (full-stack) — seven stations string the skeleton, three threads weave the background.</li>
    <li><strong>An elegant closed loop</strong>: the trace produces a score, the score drives monitoring and experiments, in turn improving prompt/model/app — observation products feed the app, the soul of an "LLM engineering platform."</li>
    <li><strong>The six themes take their places</strong>: wide events (record keeps detail), immutability+async (survives high throughput), dual storage (find fast and cheap), multi-tenancy (serve everyone), cost (affordable long-term) — Lesson 54's six themes each do their job across this life.</li>
    <li><strong>Carry away a way of seeing</strong>: the big question Langfuse answers is "turn an AI app's unobservability back into observability" — record→find→judge→act→retire responsibly. What you should truly carry away isn't a snippet of source but the ability to see any system with an architect's "goal+scale→trade-offs" eyes. <strong>The 55 lessons end here, but these eyes have only just opened.</strong></li>
  </ul>
</div>
""")

LESSON_55 = {"zh": "\n".join(_ZH55), "en": "\n".join(_EN55)}
