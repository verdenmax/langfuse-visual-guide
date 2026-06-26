"""Per-lesson bilingual self-test (自测题): design-insight multiple-choice + open prompts.

Schema per lesson::

    "NN-file.html": {
        "mcq": [
            {
                "q":   {"zh": "...", "en": "..."},
                "opts": [{"zh": "...", "en": "..."}, ...],
                "answer": 1,                      # 0-based index into opts (as written)
                "why": {"zh": "...", "en": "..."},
            },
        ],
        "open": [{"zh": "...", "en": "..."}],
    }

``render(fname, lang)`` turns it into HTML that build.py appends to the bottom of
each language's lesson body. Options are deterministically shuffled per question
(same permutation for zh and en, so the correct letter matches across languages).

Quiz text (q/opts/why) is raw HTML in a text context (like the lesson body):
write literal ``<``/``&`` as ``&lt;``/``&amp;`` (or wrap code in ``<code>``).
"""
import hashlib

_HEAD = {"zh": "🧪 自测 · 想一想为什么这么设计", "en": "🧪 Self-test - think about the design"}
_SEE = {"zh": "看答案与解析", "en": "Show answer &amp; explanation"}
_CLICK = {"zh": "点击展开", "en": "click to expand"}
_ANS = {"zh": "答案：", "en": "Answer: "}
_SEP = {"zh": "。", "en": ". "}
_OPEN = {
    "zh": "💭 发散思考（没有标准答案，动手或动脑想想）",
    "en": "💭 Open questions (no single right answer - just think or try)",
}


def _shuffle(opts, answer, seed):
    """Deterministically permute opts (stable across builds); return
    (new_opts, new_answer_index) so the correct option lands in a varied slot."""
    order = sorted(
        range(len(opts)),
        key=lambda i: hashlib.md5(f"{seed}:{i}".encode("utf-8")).hexdigest(),
    )
    return [opts[i] for i in order], order.index(answer)


QUIZZES = {
    "01-what-is-langfuse.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 把 <code>observation</code>（而不是 trace）当作“主分析单元”。这个定位最主要带来什么不同？",
                    "en": "Langfuse treats the <code>observation</code> (not the trace) as the primary analytical unit. What is the main difference this brings?",
                },
                "opts": [
                    {
                        "zh": "每个 LLM 调用/检索步骤本身就是一条带丰富属性的宽事件，可独立切片聚合；trace 只是把它们关联起来的句柄",
                        "en": "Each LLM call/retrieval step is itself a richly-attributed wide event you can slice & aggregate; the trace is just a handle that correlates them",
                    },
                    {"zh": "它把所有数据压缩成一个 trace 大对象，查询时整体读出", "en": "It compresses everything into one big trace object read whole at query time"},
                    {"zh": "它取消了 trace 概念，只保留扁平日志", "en": "It removes the trace concept and keeps only flat logs"},
                    {"zh": "它要求每个 trace 只能有一个 observation", "en": "It requires each trace to have exactly one observation"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这是“可观测性 2.0 / 宽事件”的核心：把高基数上下文留在每条 observation 上，用户就能在不预设问题的前提下任意切片、分组、过滤。trace 仍在，但它是关联句柄，不是唯一入口（见 <code>.agents/ARCHITECTURE_PRINCIPLES.md</code>）。",
                    "en": "This is the heart of 'Observability 2.0 / wide events': keep high-cardinality context on each observation so users can slice, group and filter without predefining questions. The trace still exists, but as a correlation handle, not the only entry point (see <code>.agents/ARCHITECTURE_PRINCIPLES.md</code>).",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 为什么要同时用 Postgres 和 ClickHouse 两套数据库，而不是只用一套？",
                    "en": "Why does Langfuse use both Postgres and ClickHouse instead of just one database?",
                },
                "opts": [
                    {
                        "zh": "事务性配置/元数据（项目、用户、prompt、配置）适合 Postgres；海量、可追加的宽事件（trace/observation/score）适合列存的 ClickHouse 做时间窗口扫描与聚合",
                        "en": "Transactional config/metadata (projects, users, prompts, settings) fits Postgres; high-volume append-oriented wide events (trace/observation/score) fit columnar ClickHouse for time-bounded scans & aggregation",
                    },
                    {"zh": "因为 Postgres 不能存字符串", "en": "Because Postgres cannot store strings"},
                    {"zh": "纯粹为了用更多技术显得复杂", "en": "Purely to look more complex by using more tech"},
                    {"zh": "ClickHouse 用来做用户登录，Postgres 用来跑 ML", "en": "ClickHouse handles logins while Postgres runs ML"},
                ],
                "answer": 0,
                "why": {
                    "zh": "两类负载的访问模式根本不同：元数据是小数据量、强一致、频繁更新——交给 Postgres；遥测是大数据量、写多于改、按时间和项目聚合——交给 ClickHouse（宽事件、列存、ReplacingMergeTree）。用对存储，热路径才不会被拖垮。",
                    "en": "The two workloads have fundamentally different access patterns: metadata is small, strongly-consistent and frequently updated — Postgres; telemetry is huge, write-mostly and aggregated by time/project — ClickHouse (wide events, columnar, ReplacingMergeTree). Matching storage to pattern keeps the hot path fast.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 的摄取为什么走“SDK → 公共 API → 队列 → worker → ClickHouse”这条异步链路，而不是 API 直接写 ClickHouse？",
                    "en": "Why does ingestion go 'SDK → public API → queue → worker → ClickHouse' asynchronously instead of the API writing ClickHouse directly?",
                },
                "opts": [
                    {
                        "zh": "解耦与削峰：API 只需快速收下事件并入队，重活（合并、token/成本计算、批量写）交给 worker 异步处理，既抗流量尖峰又能批量高效写入",
                        "en": "Decoupling & smoothing: the API just accepts and enqueues fast, while the heavy work (merge, token/cost compute, batched writes) runs async in the worker — absorbing spikes and writing in efficient batches",
                    },
                    {"zh": "因为 ClickHouse 只接受来自 worker 的连接", "en": "Because ClickHouse only accepts connections from the worker"},
                    {"zh": "队列是用来加密数据的", "en": "The queue is there to encrypt the data"},
                    {"zh": "为了让写入更慢以节省成本", "en": "To make writes slower and save cost"},
                ],
                "answer": 0,
                "why": {
                    "zh": "把“接收”和“处理”分开，是高吞吐遥测系统的经典做法。API 端轻量、可水平扩展、对 SDK 低延迟；worker 端可重试、可批量、可分片（主/次队列隔离高吞吐项目）。代价是“最终一致”——数据有秒级处理延迟，这正是 §设计取舍要权衡的。",
                    "en": "Separating 'accept' from 'process' is the classic shape for high-throughput telemetry. The API stays lightweight, horizontally scalable and low-latency to the SDK; the worker can retry, batch and shard (primary/secondary queues isolate high-throughput projects). The cost is eventual consistency — a few seconds of processing lag, exactly the tradeoff to weigh.",
                },
            },
        ],
        "open": [
            {
                "zh": "如果让你给一个自研的 LLM 应用加“可观测性”，你会先记录哪三类信息到每条 observation 上？为什么这三类最能帮你事后 debug？",
                "en": "If you were adding 'observability' to your own LLM app, which three kinds of data would you record on each observation first, and why would those three help you debug later?",
            },
        ],
    },
    "02-observability-2-and-wide-events.html": {
        "mcq": [
            {
                "q": {
                    "zh": "“可观测性 1.0（指标+日志+链路）”和“2.0（宽事件）”最本质的区别是什么？",
                    "en": "What is the most essential difference between Observability 1.0 (metrics+logs+traces) and 2.0 (wide events)?",
                },
                "opts": [
                    {
                        "zh": "1.0 把信息拆进三套分离的系统、回答跨维度问题前要人肉拼接；2.0 把一步的数字/结构/业务字段放进同一行，下钻与聚合都成了对同一张宽表的查询",
                        "en": "1.0 splits info across three separate systems and needs manual reassembly for cross-dimension questions; 2.0 puts numbers/structure/business fields of one step on one row, so drill-down and aggregation are both queries over one wide table",
                    },
                    {"zh": "2.0 不再存储任何数字指标", "en": "2.0 stops storing any numeric metrics"},
                    {"zh": "1.0 更快，因为数据更宽", "en": "1.0 is faster because the data is wider"},
                    {"zh": "2.0 要求每个 trace 只能有一条 observation", "en": "2.0 requires exactly one observation per trace"},
                ],
                "answer": 0,
                "why": {
                    "zh": "关键不在“用不用指标”，而在“分不分离”。1.0 的三件套各存一处，跨维度问题要在三套系统间对账；2.0 把高基数上下文整行留存，新问题只是换个查询。这正是 ARCHITECTURE_PRINCIPLES.md 第一条与第二条。",
                    "en": "The point isn't whether you use metrics, but whether things are separated. 1.0's three pillars live apart, forcing reconciliation across systems; 2.0 keeps high-cardinality context on the row, so a new question is just a new query. That's principles one and two in ARCHITECTURE_PRINCIPLES.md.",
                },
            },
            {
                "q": {
                    "zh": "为什么说宽事件能回答“unknown unknowns”，而预聚合指标不能？",
                    "en": "Why can wide events answer 'unknown unknowns' while pre-aggregated metrics cannot?",
                },
                "opts": [
                    {
                        "zh": "预聚合在上线前就把维度固定了，只能回答已建好的图；宽事件保留高基数整行，事后想到的新切法换个查询即可，无需改埋点或重新上线",
                        "en": "Pre-aggregation fixes dimensions before shipping, answering only charts you built; wide events keep the full high-cardinality row, so any slice thought of later is just a new query — no re-instrumenting or redeploy",
                    },
                    {"zh": "因为宽事件用了更贵的数据库", "en": "Because wide events use a more expensive database"},
                    {"zh": "因为预聚合指标不支持时间维度", "en": "Because pre-aggregated metrics don't support a time dimension"},
                    {"zh": "因为宽事件会自动猜测你想问的问题", "en": "Because wide events automatically guess your questions"},
                ],
                "answer": 0,
                "why": {
                    "zh": "“unknown unknowns”是你当初没想到要问的问题。预聚合把“能问什么”锁死在上线时；宽事件把上下文整行留下，于是定义新视图从“改埋点+重新上线”降级成“写一条新查询”——这是平台可扩展性的地基。",
                    "en": "'Unknown unknowns' are questions you didn't foresee. Pre-aggregation locks 'what you can ask' at ship time; wide events keep the context on the row, demoting 'define a new view' from 're-instrument + redeploy' to 'write a new query' — the foundation of platform extensibility.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 为什么把 model、usageDetails、costDetails 等<strong>内联</strong>到 observation 行上，而不是拆成多张表用外键关联？",
                    "en": "Why does Langfuse <strong>inline</strong> model, usageDetails, costDetails onto the observation row instead of splitting into normalized tables with foreign keys?",
                },
                "opts": [
                    {
                        "zh": "为了消除热路径上的 JOIN：可观测数据量极大，常用过滤/聚合若每次都要连表代价会爆炸；内联后“按模型/用户/时间”变成直接的列谓词",
                        "en": "To kill hot-path JOINs: observability data is huge, so joining for common filters/aggregations would explode in cost; inlining turns 'by model/user/time' into plain column predicates",
                    },
                    {"zh": "因为 ClickHouse 不支持多张表", "en": "Because ClickHouse doesn't support multiple tables"},
                    {"zh": "因为外键在任何数据库里都非法", "en": "Because foreign keys are illegal in any database"},
                    {"zh": "纯粹为了占用更多磁盘", "en": "Purely to use more disk"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这就是“谨慎反范式化”原则：用一点存储冗余换查询时不必连表。在上亿行规模下，把常用来过滤聚合的字段内联到行上，让高频查询变成直接列谓词，是把宽事件做快的关键一招（第 8 课展开）。",
                    "en": "This is the 'denormalize carefully' principle: trade a little storage redundancy for not joining at query time. At hundreds-of-millions-of-rows scale, inlining the fields used to filter/aggregate so hot queries become column predicates is key to making wide events fast (expanded in L08).",
                },
            },
        ],
        "open": [
            {
                "zh": "想象你维护一个公司内部的 LLM 网关，老板突然问“上周哪个部门、用哪个模型、花了最多钱”。如果你只有传统的“平均成本”指标，会卡在哪？换成宽事件后这个问题怎么变简单？",
                "en": "Imagine you run an internal LLM gateway and your boss asks 'which department, on which model, spent the most last week'. If you only had a traditional 'average cost' metric, where would you get stuck? How does a wide event make this easy?",
            },
        ],
    },
    "03-three-pillars-deep.html": {
        "mcq": [
            {
                "q": {
                    "zh": "为什么 Langfuse 把 model/token/cost/prompt 等“重”字段都放在 observation 上，而让 trace 只有身份与少数标记？",
                    "en": "Why does Langfuse put the 'heavy' fields (model/token/cost/prompt) on the observation while the trace has only identity and a few markers?",
                },
                "opts": [
                    {
                        "zh": "因为绝大多数查询发生在“步”这个粒度（按模型、按 prompt 版本聚合过滤），把这些维度放在 observation 上，常用查询就成了对宽表的直接列谓词；trace 只需负责关联",
                        "en": "Because most queries happen at the 'step' granularity (aggregate/filter by model, by prompt version); putting those dimensions on the observation makes common queries direct column predicates over the wide table, while the trace just correlates",
                    },
                    {"zh": "因为 trace 不允许有任何字段", "en": "Because a trace may not have any fields"},
                    {"zh": "因为 observation 存在 Postgres，trace 存在 ClickHouse", "en": "Because observations live in Postgres and traces in ClickHouse"},
                    {"zh": "因为这样能减少 SVG 数量", "en": "Because it reduces the number of SVGs"},
                ],
                "answer": 0,
                "why": {
                    "zh": "查询的粒度决定了字段的归属。把高频过滤/聚合维度放在 observation 上，热查询变成列谓词、无需 JOIN；trace 保持薄、只做关联。代价是 userId 等可能在两边冗余，这正是“谨慎反范式化”。",
                    "en": "Query granularity decides where fields belong. Put the hot filter/aggregate dimensions on the observation so hot queries become column predicates without JOINs; keep the trace thin for correlation. The cost is some redundancy (e.g. userId) — exactly 'denormalize carefully'.",
                },
            },
            {
                "q": {
                    "zh": "observation 之间的父子关系只用子节点上的一个 parentObservationId 指针表达。这个设计对“异步摄取”有什么关键好处？",
                    "en": "Parent-child links among observations are expressed only by a parentObservationId pointer on the child. What's the key benefit for async ingestion?",
                },
                "opts": [
                    {
                        "zh": "每个 observation 自带“我爸是谁”，于是它们能各自独立、乱序到达服务端；子节点先于父节点到也没关系，查询时 UI 再按指针拼出整棵树",
                        "en": "Each observation carries 'who my parent is', so they can arrive independently and out of order; a child arriving before its parent is fine, and the UI rebuilds the tree from pointers at query time",
                    },
                    {"zh": "它让父节点能实时统计自己有几个孩子", "en": "It lets the parent count its children in real time"},
                    {"zh": "它要求所有 observation 必须按顺序写入", "en": "It requires all observations to be written in order"},
                    {"zh": "它把树结构存成了一张额外的关系表", "en": "It stores the tree as an extra relational table"},
                ],
                "answer": 0,
                "why": {
                    "zh": "若反过来让父节点维护 children 列表，就得“等所有孩子到齐才能写父节点”，在高并发异步管线里是灾难。只存子节点的父指针，写入彻底解耦、可乱序，是摄取链路可行的关键（第 25 课拼树）。",
                    "en": "If the parent maintained a children list, you'd have to 'wait for all children before writing the parent' — a disaster in a high-concurrency async pipeline. Storing only the child's parent pointer fully decouples writes and allows any order, key to the ingestion path (tree rebuilt in L25).",
                },
            },
            {
                "q": {
                    "zh": "observation 上为什么同时有 providedUsageDetails 和 usageDetails（成本同理）两套字段？",
                    "en": "Why does an observation carry both providedUsageDetails and usageDetails (and similarly for cost)?",
                },
                "opts": [
                    {
                        "zh": "provided 是 SDK 上报时自带的，usage 是 Langfuse 摄取时按模型定价自己算的；“你报的我尊重、你没报的我兜底”",
                        "en": "'provided' is what the SDK reported, 'usage' is what Langfuse computed at ingestion from model pricing; 'respect what you sent, backfill what you didn't'",
                    },
                    {"zh": "两者完全相同，纯属冗余", "en": "They are identical, pure redundancy"},
                    {"zh": "provided 给前端用，usage 给后端用", "en": "'provided' is for the frontend, 'usage' for the backend"},
                    {"zh": "一个存 token，一个存金额", "en": "One stores tokens, the other money"},
                ],
                "answer": 0,
                "why": {
                    "zh": "两套并存兼顾“应用精确控制”和“平台兜底”：应用知道精确用量就直接报（provided），不报时 Langfuse 按 model 名匹配定价表算出来（computed）。这套“provided 优先、computed 兜底”在成本计算课（第 16 课）会展开。",
                    "en": "Having both balances 'app precision' and 'platform backfill': if the app knows exact usage it reports it (provided); if not, Langfuse computes it from the model pricing table (computed). This 'provided wins, computed backfills' is expanded in the cost lesson (L16).",
                },
            },
        ],
        "open": [
            {
                "zh": "如果让你设计 score 的“来源”枚举，你会不会也像 Langfuse 一样禁止外部 API 提交 EVAL 来源的分数？说说这么做在“信任谁打的分”上的意义。",
                "en": "If you designed the score 'source' enum, would you also forbid external API callers from submitting EVAL-sourced scores like Langfuse does? Discuss what this means for trusting 'who scored'.",
            },
        ],
    },
    "04-project-map-monorepo.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 规定依赖只能 web/worker/ee → shared，而 shared 不依赖任何一方。这条“窄腰”规则最主要的好处是什么？",
                    "en": "Langfuse mandates that dependencies go only web/worker/ee → shared, and shared depends on none. What's the main benefit of this 'narrow waist' rule?",
                },
                "opts": [
                    {
                        "zh": "两个容器各自独立演进/部署，却共用同一套领域模型与队列契约，契约集中在一处定义、不会漂移",
                        "en": "The two containers evolve/deploy independently yet share one set of domain models and queue contracts, defined in one place so they can't drift",
                    },
                    {"zh": "让 shared 包能直接调用 web 的 React 组件", "en": "It lets shared call web's React components directly"},
                    {"zh": "让构建变慢以便缓存", "en": "It slows builds so caching kicks in"},
                    {"zh": "强制 web 和 worker 跑在同一个进程里", "en": "It forces web and worker into one process"},
                ],
                "answer": 0,
                "why": {
                    "zh": "web（低延迟、面向用户）和 worker（重活、可重试）是两种负载；让它们互相直接依赖会彼此牵连。把共享内容收进谁都不反向依赖的 shared，并只许向下依赖，就在两容器间立了契约墙——队列传什么、表长什么样都由 shared 一处定义。",
                    "en": "web (low-latency, user-facing) and worker (heavy, retryable) are different workloads; letting them depend on each other entangles them. Collecting shared content into a shared that nothing depends on backwards, with only-downward deps, erects a contract wall — what goes through queues and what tables look like are defined in one place.",
                },
            },
            {
                "q": {
                    "zh": "turbo.json 里 build 任务写着 \"dependsOn\": [\"db:generate\", \"^build\"]。这表示什么？",
                    "en": "In turbo.json the build task says \"dependsOn\": [\"db:generate\", \"^build\"]. What does that mean?",
                },
                "opts": [
                    {
                        "zh": "构建任何包之前，先生成 Prisma 客户端，并先构建它依赖的上游包（^ 表示上游）；Turbo 据此算出顺序、并行、并跳过缓存命中的部分",
                        "en": "Before building any package, generate the Prisma client and first build its upstream deps (^ = upstream); Turbo computes order, parallelizes, and skips cache hits",
                    },
                    {"zh": "build 任务永远不能被缓存", "en": "The build task can never be cached"},
                    {"zh": "db:generate 必须手动在 build 之后运行", "en": "db:generate must be run manually after build"},
                    {"zh": "^build 表示构建下游的包", "en": "^build means build the downstream packages"},
                ],
                "answer": 0,
                "why": {
                    "zh": "dependsOn 声明任务依赖图：db:generate 先于 build（要先有 Prisma 类型），^build 表示先构建上游依赖包。于是一条 pnpm build 就能让 Turbo 自动排序、并行、并对没变的包命中缓存——大仓也能增量构建。",
                    "en": "dependsOn declares the task graph: db:generate before build (need Prisma types first), ^build means build upstream dep packages first. So one pnpm build lets Turbo order, parallelize, and cache-hit unchanged packages — incremental builds even in a big repo.",
                },
            },
            {
                "q": {
                    "zh": "给 trace 加一个字段，在 Langfuse 的 monorepo 里大致怎么落地？",
                    "en": "Adding a field to the trace in Langfuse's monorepo roughly takes what steps?",
                },
                "opts": [
                    {
                        "zh": "改 prisma/schema.prisma 与 domain/traces.ts，db:generate 后 web 和 worker 都从同一个 @langfuse/shared 拿到新类型，一个 PR、CI 一起验",
                        "en": "Edit prisma/schema.prisma and domain/traces.ts; after db:generate both web and worker pick up the new type from the same @langfuse/shared, in one PR verified together by CI",
                    },
                    {"zh": "在三个独立仓库各发一次版，再手动对版本", "en": "Release three separate repos and manually align versions"},
                    {"zh": "只能改 web，worker 不受影响", "en": "Only web changes; worker is unaffected"},
                    {"zh": "必须先删掉旧的 ClickHouse 表", "en": "You must first drop the old ClickHouse table"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这正是 monorepo + 窄腰的价值：共享结构改一处，web/worker 都从 @langfuse/shared 取，原子地在一个 PR 完成、一起过 CI。分仓则要跨仓发版对版本、易漂移。",
                    "en": "This is exactly the monorepo + narrow-waist payoff: change the shared structure once, both web/worker pull from @langfuse/shared, done atomically in one PR through CI together. Polyrepo would need cross-repo releases and version alignment, inviting drift.",
                },
            },
        ],
        "open": [
            {
                "zh": "你自己的项目如果同时有“面向用户的服务”和“后台 worker”，你会把它们放一个仓还是分仓？参考 Langfuse 的窄腰，你会把哪些东西抽进一个共享层？",
                "en": "If your own project had both a 'user-facing service' and a 'background worker', would you keep them in one repo or split? Borrowing Langfuse's narrow waist, what would you pull into a shared layer?",
            },
        ],
    },
    "05-life-of-a-trace.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的摄取为什么是异步的（API 收下就入队返回，由 worker 后台处理），而不是 API 同步写完 ClickHouse 才返回？",
                    "en": "Why is Langfuse ingestion async (the API enqueues and returns, the worker processes in the background) rather than the API synchronously writing ClickHouse before returning?",
                },
                "opts": [
                    {
                        "zh": "为了让 API 永远毫秒级返回、几乎不拖累你的应用，并能用队列做缓冲：洪峰先排队、worker 批量可重试地消费、扛不住就横向扩容",
                        "en": "So the API always returns in ms and barely drags your app, and the queue buffers: spikes queue up, the worker consumes in batches retryably, and you scale out when overwhelmed",
                    },
                    {"zh": "因为 ClickHouse 不支持同步写入", "en": "Because ClickHouse doesn't support synchronous writes"},
                    {"zh": "为了故意增加延迟以省钱", "en": "To deliberately add latency to save money"},
                    {"zh": "因为 API 不能访问数据库", "en": "Because the API cannot access the database"},
                ],
                "answer": 0,
                "why": {
                    "zh": "若 API 同步合并/算成本/写库，你每次 LLM 调用都被拖慢，且下游一抖动 API 就超时甚至把错误反弹给业务。异步把“收件”和“处理”解耦：API 极轻、几乎不可能慢；worker 批量、可重试、可扩容地消化洪峰。代价是秒级延迟（最终一致）。",
                    "en": "If the API synchronously merged/costed/wrote, every LLM call is slowed and a downstream hiccup times out the API or bounces errors into your business. Async decouples accept from process: the API is featherweight and rarely slow; the worker digests spikes in batches, retryably, scalably. The cost is seconds of lag (eventual consistency).",
                },
            },
            {
                "q": {
                    "zh": "worker 处理时为什么要回 S3 取“这个 id 的历史事件”再合并？",
                    "en": "Why does the worker re-read 'this id's prior events' from S3 and merge during processing?",
                },
                "opts": [
                    {
                        "zh": "因为一个 observation 常被分多次、可能乱序地上报（先 create 再 update），worker 必须把这些碎片合并成一条一致的最终记录",
                        "en": "Because one observation is often reported in multiple, possibly out-of-order events (create then update), and the worker must merge these fragments into one consistent final record",
                    },
                    {"zh": "因为 ClickHouse 会丢数据，要从 S3 恢复", "en": "Because ClickHouse loses data and must restore from S3"},
                    {"zh": "因为 S3 比队列快", "en": "Because S3 is faster than the queue"},
                    {"zh": "因为合并必须在前端做", "en": "Because merging must happen in the frontend"},
                ],
                "answer": 0,
                "why": {
                    "zh": "SDK 上报往往不是一次性的：先发 create（我开始了），调用返回后再发 update（输出/用量）。两条分别到达，worker 回 S3 取历史把碎片拼成完整一行。这也支撑了“事件可乱序到达、worker 收敛成最终态”，正是第 3 课 parentObservationId 设计的运行时体现。",
                    "en": "SDK reporting often isn't one-shot: a create ('I started') then an update ('output/usage') after the call returns. They arrive separately; the worker re-reads S3 to stitch the fragments into one row. This supports 'events arrive out of order, worker converges to final state' — the runtime realization of L03's parentObservationId design.",
                },
            },
            {
                "q": {
                    "zh": "“最终一致”对使用 Langfuse 意味着什么实践注意点？",
                    "en": "What practical caveat does 'eventual consistency' imply when using Langfuse?",
                },
                "opts": [
                    {
                        "zh": "刚埋点的数据可能要等一两秒才在 UI 出现；别把它当强一致业务库，写自动化测试验证埋点时要给摄取留处理时间",
                        "en": "Just-instrumented data may take a second or two to appear in the UI; don't treat it as a strongly-consistent business DB, and when testing instrumentation, allow ingestion time to process",
                    },
                    {"zh": "数据永远不会出现", "en": "Data will never appear"},
                    {"zh": "必须手动刷新数据库连接", "en": "You must manually refresh the DB connection"},
                    {"zh": "trace 会随机丢失", "en": "Traces are randomly lost"},
                ],
                "answer": 0,
                "why": {
                    "zh": "异步摄取有秒级处理延迟，对“事后排查/看板/评估”完全够用，但意味着“写完不一定立刻可读”。所以别拿它当强一致库；自动化验证埋点时要等摄取处理完，否则会误判“数据没上来”。",
                    "en": "Async ingestion has seconds of processing lag — fine for after-the-fact triage/dashboards/eval, but it means 'written isn't instantly readable'. So don't treat it as a strongly-consistent store; when verifying instrumentation in tests, wait for ingestion or you'll falsely conclude 'no data arrived'.",
                },
            },
        ],
        "open": [
            {
                "zh": "回顾第一部分：用你自己的话，把“一条 trace 的一生”讲给一个没用过 Langfuse 的同事听（从 SDK 到 UI）。你觉得哪一段最容易被忽略、但其实最关键？",
                "en": "Recap Part 1: in your own words, tell a colleague who's never used Langfuse the 'life of a trace' from SDK to UI. Which leg do you think is most overlooked yet most crucial?",
            },
        ],
    },
    "06-instrumenting-an-llm-app.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 为什么既支持自家 SDK 的“原生事件”，又支持 OpenTelemetry（OTLP）？",
                    "en": "Why does Langfuse support both its own SDK 'native events' and OpenTelemetry (OTLP)?",
                },
                "opts": [
                    {
                        "zh": "原生 SDK 表达力最强（精确报 prompt/用量/成本），OTel 则让已经用 OTel 的系统无缝接入、无需重写埋点；两者各服务一类用户",
                        "en": "The native SDK is most expressive (precise prompt/usage/cost), while OTel lets systems already on OTel plug in without rewriting instrumentation; each serves a different user",
                    },
                    {"zh": "因为原生 SDK 已经废弃，OTel 是唯一入口", "en": "Because the native SDK is deprecated and OTel is the only entry"},
                    {"zh": "因为 OTel 比原生事件携带更多 LLM 专有语义", "en": "Because OTel carries more LLM-specific semantics than native events"},
                    {"zh": "为了让数据走两条完全独立的存储", "en": "To route data into two completely separate stores"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这是“拥抱标准 vs 发挥专长”的权衡：OTel 是云原生可观测的事实标准，支持它降低接入门槛；但其通用模型不天然懂 prompt 版本/token 用量，原生 SDK 更精确。Langfuse 两者都要——OTLP 降门槛，原生 SDK 给最佳体验。",
                    "en": "This is 'embrace the standard vs play to strengths': OTel is the de-facto cloud-native standard, so supporting it lowers the barrier; but its generic model doesn't natively grok prompt version/token usage, where the native SDK is more precise. Langfuse does both — OTLP for reach, native SDK for the best experience.",
                },
            },
            {
                "q": {
                    "zh": "一个 span 型 observation 常常先发 SPAN_CREATE、结束时再发 SPAN_UPDATE。这种“增量上报”的主要好处是什么？",
                    "en": "A span-type observation often sends SPAN_CREATE first, then SPAN_UPDATE at the end. What's the main benefit of this 'incremental reporting'?",
                },
                "opts": [
                    {
                        "zh": "能更早记下“它开始了”，即使后面崩溃/超时也知道卡在哪步——失败 case 不会因为“没等到结束”而彻底消失",
                        "en": "It records 'it started' earlier, so even if it later crashes/times out you know which step stalled — failure cases don't vanish just because 'the end never came'",
                    },
                    {"zh": "为了减少事件数量", "en": "To reduce the number of events"},
                    {"zh": "因为 ClickHouse 只接受两次写入", "en": "Because ClickHouse only accepts two writes"},
                    {"zh": "为了让 SDK 自己拼装最终状态", "en": "So the SDK assembles the final state itself"},
                ],
                "answer": 0,
                "why": {
                    "zh": "若等结束才发一条完整事件，一旦中途挂掉这一步就彻底消失，而失败恰恰最该被观测。增量上报 = “边发生边记录”，服务端再把 create+update 合并成一条（第 15 课）。",
                    "en": "Waiting to send one complete event means a mid-flight crash erases that step — yet failures are exactly what you most want to observe. Incremental reporting = 'record as it happens', and the server merges create+update into one row (L15).",
                },
            },
            {
                "q": {
                    "zh": "这套“事件增量上报 + 合并”的协议，把最复杂的合并逻辑放在哪一端？为什么？",
                    "en": "In this 'incremental events + merge' protocol, where does the most complex merge logic live, and why?",
                },
                "opts": [
                    {
                        "zh": "放在服务端（worker）：SDK 只管把小事件发出去，合并“可能乱序/重复的事件成一致一行”只在一处维护，避免每种语言 SDK 各写各错",
                        "en": "On the server (worker): SDKs just emit small events; merging 'possibly out-of-order/duplicate events into one consistent row' lives in one place, avoiding each language SDK re-implementing (and re-bugging) it",
                    },
                    {"zh": "放在 SDK：每个语言各自实现合并", "en": "In the SDK: each language implements merging itself"},
                    {"zh": "放在数据库触发器里", "en": "In database triggers"},
                    {"zh": "放在前端 UI 渲染时", "en": "In the frontend at render time"},
                ],
                "answer": 0,
                "why": {
                    "zh": "把复杂度收敛到一个能严格测试的地方（服务端）：SDK 因此轻、好移植、对应用影响小；合并这种最易错的逻辑只在 worker 维护一份，而不是散落在每个语言 SDK 里。",
                    "en": "Converge complexity to one strictly testable place (the server): SDKs stay light, portable and low-impact; the error-prone merge logic is maintained once in the worker rather than scattered across every language SDK.",
                },
            },
        ],
        "open": [
            {
                "zh": "如果你要给自己的应用加埋点，你会选 Langfuse 原生 SDK 还是 OpenTelemetry？你的系统现状（有没有已用 OTel、需不需要精确成本）会怎么影响这个选择？",
                "en": "If you were instrumenting your own app, would you pick the Langfuse native SDK or OpenTelemetry? How would your system's current state (already on OTel? need precise cost?) shape that choice?",
            },
        ],
    },
    "07-dual-store-architecture.html": {
        "mcq": [
            {
                "q": {
                    "zh": "为什么 Langfuse 把配置/元数据放 Postgres、把 trace/observation/score 放 ClickHouse，而不是统一用一个库？",
                    "en": "Why does Langfuse put config/metadata in Postgres and trace/observation/score in ClickHouse, rather than one database for all?",
                },
                "opts": [
                    {
                        "zh": "因为两者是相反的负载：配置是 OLTP（小、精确单条读写、强一致），遥测是 OLAP（海量、按时间窗口+维度聚合）；没有哪个库能把两头都做到极致",
                        "en": "Because they're opposite workloads: config is OLTP (small, precise single-row, strongly consistent), telemetry is OLAP (massive, time-window + dimensional aggregation); no single store nails both extremes",
                    },
                    {"zh": "因为 ClickHouse 不能存字符串", "en": "Because ClickHouse can't store strings"},
                    {"zh": "因为 Postgres 不支持索引", "en": "Because Postgres has no indexes"},
                    {"zh": "纯粹为了用更多技术", "en": "Purely to use more tech"},
                ],
                "answer": 0,
                "why": {
                    "zh": "配置要精确读写单条且强一致（创建即可用），是行存 Postgres 的主场；遥测海量、写多于改、按维度聚合，是列存 ClickHouse 的主场。硬塞进一个必然顾此失彼。这是“按访问模式选存储”。",
                    "en": "Config needs precise single-row read/write and strong consistency (instantly usable) — row-store Postgres's turf; telemetry is massive, write-mostly, dimensionally aggregated — columnar ClickHouse's turf. Forcing one store loses both ways. This is 'choose storage by access pattern'.",
                },
            },
            {
                "q": {
                    "zh": "在摄取链路里，S3 扮演的关键角色是什么？",
                    "en": "What key role does S3 play in the ingestion path?",
                },
                "opts": [
                    {
                        "zh": "事件的“真相之源/原始日志”：事件先落 S3，worker 合并时回 S3 取历史；ClickHouse 的宽事件相当于其合并后的派生表，理论上可从 S3 重放重建",
                        "en": "The events' 'source of truth / raw log': events land in S3 first, the worker re-reads S3 to merge; ClickHouse wide events are the merged derived table, in principle replayable from S3",
                    },
                    {"zh": "只是存上传的图片，和摄取无关", "en": "Just stores uploaded images, unrelated to ingestion"},
                    {"zh": "代替 Redis 做队列", "en": "Replaces Redis as the queue"},
                    {"zh": "存用户密码", "en": "Stores user passwords"},
                ],
                "answer": 0,
                "why": {
                    "zh": "S3 不只是大文件仓。事件先落 S3 作为不可变原始日志，worker 据此合并出 ClickHouse 宽事件（派生/物化）。这正是第 2 课“不可变/追加式事件”的体现，也让数据可重放重建。",
                    "en": "S3 isn't just a big-file store. Events land in S3 as an immutable raw log, from which the worker merges ClickHouse wide events (derived/materialized). This is L02's 'immutable/append-oriented events', and makes data replayable.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 用四种存储，但第 2 课又说“把运维简单性当约束”。怎么调和？判断“该不该再加一个存储”的标准是什么？",
                    "en": "Langfuse uses four stores, yet L02 says 'treat operational simplicity as a constraint'. How to reconcile? What's the test for 'should we add another store'?",
                },
                "opts": [
                    {
                        "zh": "每个存储都必须挣到自己的存在——它解决的硬问题是否值得它带来的长期运维成本（备份/监控/升级/容灾）",
                        "en": "Each store must earn its existence — does the hard problem it solves justify its long-term ops cost (backup/monitoring/upgrade/DR)",
                    },
                    {"zh": "存储越多越好，多多益善", "en": "More stores are always better"},
                    {"zh": "永远只能用一个数据库", "en": "You may only ever use one database"},
                    {"zh": "由前端框架决定", "en": "The frontend framework decides"},
                ],
                "answer": 0,
                "why": {
                    "zh": "四存储不是“想加就加”：ClickHouse 解决海量聚合、Redis 解决异步抗洪峰、S3 解决大字段+重放，各自解决单库做不到的硬问题，所以挣到了存在。这也正是判断要不要再加存储的标准。",
                    "en": "The four aren't 'add because we can': ClickHouse solves huge aggregation, Redis solves async spike absorption, S3 solves big fields + replay — each solving what one store can't, thus earning its place. That's exactly the test for adding another store.",
                },
            },
        ],
        "open": [
            {
                "zh": "想象你在设计一个新的日志/监控系统，预算有限。你会从一个 Postgres 起步，还是一开始就上 ClickHouse？在什么规模/查询模式下，引入列存才真正“挣到存在”？",
                "en": "Imagine designing a new logging/monitoring system on a tight budget. Would you start with one Postgres, or bring in ClickHouse from day one? At what scale/query pattern does a columnar store truly 'earn its existence'?",
            },
        ],
    },
}


def render(fname, lang):
    """Return the self-test HTML block for ``fname`` in ``lang`` ('' if none)."""
    data = QUIZZES.get(fname)
    if not data or not (data.get("mcq") or data.get("open")):
        return ""
    out = ['<div class="selftest">', f'<h2>{_HEAD[lang]}</h2>']
    for i, item in enumerate(data.get("mcq", []), 1):
        shuffled, ans = _shuffle(item["opts"], item["answer"], f"{fname}:{i}")
        opts = "\n".join(f"    <li>{o[lang]}</li>" for o in shuffled)
        letter = chr(65 + ans)
        out.append(
            f'<div class="quiz">\n'
            f'  <div class="qn">{i}. {item["q"][lang]}</div>\n'
            f'  <ol class="opts">\n{opts}\n  </ol>\n'
            f'  <details class="accordion">\n'
            f'    <summary>{_SEE[lang]} <span class="hint">{_CLICK[lang]}</span></summary>\n'
            f'    <div class="acc-body"><div class="qa"><div class="a">'
            f'<strong>{_ANS[lang]}{letter}</strong>{_SEP[lang]}{item["why"][lang]}'
            f"</div></div></div>\n"
            f"  </details>\n"
            f"</div>"
        )
    opens = data.get("open", [])
    if opens:
        lis = "\n".join(f"    <li>{o[lang]}</li>" for o in opens)
        out.append(
            '<div class="card spark">\n'
            f'  <div class="tag">{_OPEN[lang]}</div>\n'
            f"  <ul>\n{lis}\n  </ul>\n"
            "</div>"
        )
    out.append("</div>")
    return "\n".join(out)


def _validate():
    """Fail fast on authoring mistakes in QUIZZES (clear message names the lesson)."""
    for fname, data in QUIZZES.items():
        for qi, item in enumerate(data.get("mcq", []), 1):
            opts = item["opts"]
            if not (0 <= item["answer"] < len(opts)):
                raise ValueError(
                    f"quizzes[{fname!r}] Q{qi}: answer {item['answer']} out of range 0..{len(opts) - 1}"
                )
            for o in opts:
                if not ({"zh", "en"} <= o.keys()):
                    raise ValueError(f"quizzes[{fname!r}] Q{qi}: an option is missing zh/en")
            if not ({"zh", "en"} <= item["q"].keys() and {"zh", "en"} <= item["why"].keys()):
                raise ValueError(f"quizzes[{fname!r}] Q{qi}: q/why missing zh/en")
        for oi, o in enumerate(data.get("open", []), 1):
            if not ({"zh", "en"} <= o.keys()):
                raise ValueError(f"quizzes[{fname!r}] open{oi}: missing zh/en")


_validate()
