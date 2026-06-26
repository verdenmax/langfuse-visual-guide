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
    "08-clickhouse-wide-events.html": {
        "mcq": [
            {
                "q": {
                    "zh": "ReplacingMergeTree(event_ts, is_deleted) 的核心语义是什么？它怎么承接“一个 observation 先 create 后 update”？",
                    "en": "What's the core semantic of ReplacingMergeTree(event_ts, is_deleted)? How does it absorb 'an observation created then updated'?",
                },
                "opts": [
                    {
                        "zh": "排序键相同的多行会被替换成 event_ts 最大的那条（is_deleted 软删除）；create 与 update 是两次同 id 写入，后台合并时自动用 update 覆盖 create——只管追加，覆盖交给引擎",
                        "en": "Rows with the same ordering key collapse to the largest event_ts (is_deleted soft-deletes); create and update are two writes of the same id, and background merge auto-overwrites create with update — just append, the engine overwrites",
                    },
                    {"zh": "它会拒绝重复 id 的写入", "en": "It rejects writes with duplicate ids"},
                    {"zh": "它把两次写入都永久保留且都返回", "en": "It keeps both writes forever and returns both"},
                    {"zh": "它要求先删除旧行再写新行", "en": "It requires deleting the old row before writing the new one"},
                ],
                "answer": 0,
                "why": {
                    "zh": "ReplacingMergeTree 让“改一条”退化成“追加一条更大 event_ts 的记录”，无需读-改-写。这正好承接 create+update 的合并模型，也是第 2 课“不可变/追加式事件”能落地的存储基础。",
                    "en": "ReplacingMergeTree turns 'edit one' into 'append one with a larger event_ts', no read-modify-write. It absorbs the create+update merge model and is the storage basis for L02's 'immutable/append-oriented events'.",
                },
            },
            {
                "q": {
                    "zh": "为什么 observations 的 ORDER BY 以 project_id 打头、PARTITION BY 按月？这对“某项目最近 7 天”这类查询有什么用？",
                    "en": "Why does observations' ORDER BY start with project_id and PARTITION BY by month? What does that do for a 'project, last 7 days' query?",
                },
                "opts": [
                    {
                        "zh": "月分区让查询直接裁掉无关月份，project_id 打头让目标项目数据物理相邻成一段；于是只扫一小片、再列存只读所需列——“少扫”是海量下高效的关键",
                        "en": "Monthly partitions prune irrelevant months; project_id-first clusters the target project into a contiguous range; so only a small slice is scanned and columnar reads only needed columns — 'scan less' is the key at scale",
                    },
                    {"zh": "为了让写入更慢", "en": "To make writes slower"},
                    {"zh": "为了让所有项目的数据混在一起", "en": "To mix all projects' data together"},
                    {"zh": "因为 ClickHouse 不支持索引", "en": "Because ClickHouse has no indexes"},
                ],
                "answer": 0,
                "why": {
                    "zh": "分区裁剪 + 排序键定位 + 列存选列三者合力，让最高频的“按项目按时间”查询在上亿行里只碰一小片。这正是第 2 课“围绕列式访问设计：时间窗口+排序键+剪枝”。",
                    "en": "Partition pruning + ordering-key locating + columnar column-selection make the hottest 'by project, by time' query touch only a small slice across hundreds of millions of rows. This is L02's 'columnar access: time windows + ordering keys + pruning'.",
                },
            },
            {
                "q": {
                    "zh": "ReplacingMergeTree 的覆盖是“最终”的（后台合并需要时间）。这带来什么取舍，Langfuse 怎么应对？",
                    "en": "ReplacingMergeTree's overwrite is 'eventual' (background merge takes time). What tradeoff does this bring, and how does Langfuse handle it?",
                },
                "opts": [
                    {
                        "zh": "未合并瞬间可能读到旧行；用 FINAL 或按 id 取最大 event_ts 的聚合保证最终态——把去重成本从“每次写入”挪到“查询时且可控”，换来写入飞快",
                        "en": "Before merge you might read an old row; use FINAL or aggregate (max event_ts per id) for the final state — moving dedup cost from 'every write' to 'query time, controllable', buying fast writes",
                    },
                    {"zh": "没有任何取舍，永远强一致", "en": "No tradeoff at all, always strongly consistent"},
                    {"zh": "必须停机合并", "en": "You must take downtime to merge"},
                    {"zh": "只能每天查询一次", "en": "You may only query once a day"},
                ],
                "answer": 0,
                "why": {
                    "zh": "追加换吞吐的代价是“最终一致”。查询侧用 FINAL/聚合读到最终态，把去重从每次写入挪到查询时并显式优化——正是第 2 课“避免读时去重的隐藏开销”的实际做法。",
                    "en": "Append-for-throughput costs 'eventual consistency'. The read side uses FINAL/aggregation for the final state, moving dedup from every write to query time and optimizing it explicitly — exactly L02's 'avoid read-time dedup's hidden cost'.",
                },
            },
        ],
        "open": [
            {
                "zh": "ReplacingMergeTree 把“改”变成“追加 + 后台覆盖”。如果你自己的系统也常常“同一条记录被多次更新”，这种“只追加、读时取最新”的思路能怎么帮你？它的代价你能接受吗？",
                "en": "ReplacingMergeTree turns 'edit' into 'append + background overwrite'. If your own system also 'updates the same record many times', how could this 'append-only, read-the-latest' idea help you? Can you accept its cost?",
            },
        ],
    },
    "09-postgres-metadata-schema.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 为什么把配置/元数据（org/project/user、API key、prompt、定价…）放 Postgres，而不是和遥测一起放 ClickHouse？",
                    "en": "Why does Langfuse keep config/metadata (org/project/user, API keys, prompts, pricing…) in Postgres rather than in ClickHouse with telemetry?",
                },
                "opts": [
                    {
                        "zh": "配置要外键关系、事务、强一致（创建即可用），是关系型 Postgres 的强项；ClickHouse 弱事务、最终一致、不擅长频繁改单条，放配置是错配",
                        "en": "Config needs foreign keys, transactions and strong consistency (instantly usable) — relational Postgres's strength; ClickHouse has weak transactions, eventual consistency and dislikes frequent single-row edits, so config there is a mismatch",
                    },
                    {"zh": "因为 ClickHouse 容量太小", "en": "Because ClickHouse is too small"},
                    {"zh": "因为 Postgres 查询更慢，适合不常用的数据", "en": "Because Postgres is slower, fit for rarely-used data"},
                    {"zh": "纯粹历史原因，没有道理", "en": "Pure history, no reason"},
                ],
                "answer": 0,
                "why": {
                    "zh": "配置是 OLTP：量小、要精确单条读写、要强一致、有外键关系。这正是 Postgres 的主场；ClickHouse 适合海量追加+聚合（OLAP）。按职责分库，各做擅长的事——这是第 7 课的延续。",
                    "en": "Config is OLTP: small, precise single-row, strongly consistent, with foreign keys — Postgres's turf; ClickHouse fits massive append + aggregation (OLAP). Split by responsibility, each at its best — a continuation of L07.",
                },
            },
            {
                "q": {
                    "zh": "为什么说 Project 是控制面的“枢纽”，以及它为什么是多租户的“数据边界”？",
                    "en": "Why is Project the 'hub' of the control plane, and why is it the multi-tenant 'data boundary'?",
                },
                "opts": [
                    {
                        "zh": "Project 字段不多但挂着几十条 1:N 关系，几乎一切（key/成员/prompt/数据集/仪表盘/集成…）都属于某个 project；一把 API key 属于某 project，查询也被限定在该 project 内",
                        "en": "Project has few fields but dozens of 1:N relations; almost everything (keys/members/prompts/datasets/dashboards/integrations…) belongs to a project; an API key belongs to a project and queries are scoped to it",
                    },
                    {"zh": "因为 Project 表行数最多", "en": "Because the Project table has the most rows"},
                    {"zh": "因为 Project 存了所有 trace", "en": "Because Project stores all traces"},
                    {"zh": "因为它没有任何关系", "en": "Because it has no relations"},
                ],
                "answer": 0,
                "why": {
                    "zh": "几乎所有控制面对象都 1:N 挂在 project 下，所以它是中心；又因为 key、数据都按 project 划分，project 成了天然的隔离边界（也对应 ClickHouse 排序键以 project_id 打头）。多租户下一课展开。",
                    "en": "Almost all control-plane objects hang 1:N off a project, making it the center; and since keys and data are scoped by project, project is the natural isolation boundary (matching ClickHouse's project_id-first ordering key). Multi-tenancy next lesson.",
                },
            },
            {
                "q": {
                    "zh": "schema.prisma 里为什么还有 LegacyPrismaTrace/Observation/Score？API key 又是怎么存的？",
                    "en": "Why are there still LegacyPrismaTrace/Observation/Score in schema.prisma? And how are API keys stored?",
                },
                "opts": [
                    {
                        "zh": "Legacy 是早期把遥测存在 Postgres 的历史残留，分析数据已迁到 ClickHouse，仅为兼容/迁移保留；API key 的密钥只存哈希、不存明文",
                        "en": "Legacy models are historical remnants of storing telemetry in Postgres; analytical data moved to ClickHouse, kept only for compat/migration; API key secrets are stored hashed, never plaintext",
                    },
                    {"zh": "Legacy 是主力表；API key 明文存储", "en": "Legacy are the primary tables; API keys are stored in plaintext"},
                    {"zh": "Legacy 用于备份 ClickHouse；API key 不存储", "en": "Legacy back up ClickHouse; API keys aren't stored"},
                    {"zh": "两者都已从代码删除", "en": "Both have been removed from the code"},
                ],
                "answer": 0,
                "why": {
                    "zh": "带 Legacy 前缀=老路：遥测早已迁 ClickHouse（第 7、8 课的存在理由），这些只为兼容/迁移留着。API key 只存 hashedSecretKey 等哈希，即使库泄露也拿不到可用 key——安全细节，第 49/53 课展开。",
                    "en": "Legacy prefix = old way: telemetry long moved to ClickHouse (the reason for L07/L08); these remain for compat/migration. API keys store only hashedSecretKey etc., so a DB leak yields no usable key — a security detail expanded in L49/L53.",
                },
            },
        ],
        "open": [
            {
                "zh": "Langfuse 把“配置”和“数据”分到两个库。如果你自己的系统也有“少而关键的配置”+“海量的事件”，你会怎么划分？跨库读配置的代价你打算怎么压（提示：缓存）？",
                "en": "Langfuse splits 'config' and 'data' into two databases. If your system also had 'small critical config' + 'massive events', how would you divide them? How would you tame the cross-store config-read cost (hint: caching)?",
            },
        ],
    },
    "10-multi-tenancy.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的多租户隔离，project 和 environment 的本质区别是什么？",
                    "en": "In Langfuse multi-tenancy, what's the essential difference between project and environment?",
                },
                "opts": [
                    {
                        "zh": "project 是硬隔离（跨项目数据绝不可见，安全红线），environment 是软切片（同一项目内给 prod/staging/dev 贴标签，可分可合）",
                        "en": "project is hard isolation (data never visible across projects, a security red line); environment is a soft slice (tagging prod/staging/dev within one project, separable or combinable)",
                    },
                    {"zh": "两者完全一样，只是名字不同", "en": "They're identical, just different names"},
                    {"zh": "environment 比 project 隔离更强", "en": "environment isolates more strongly than project"},
                    {"zh": "project 是软的，environment 是硬的", "en": "project is soft, environment is hard"},
                ],
                "answer": 0,
                "why": {
                    "zh": "“不同团队数据绝不能串”是安全红线 → project 硬隔离；“线上 vs 测试”只是同团队的视图偏好 → environment 软切片。强度不同，待遇不同。",
                    "en": "'Different teams' data must never mix' is a security red line → project hard isolation; 'live vs test' is one team's view preference → environment soft slice. Different strengths, different treatment.",
                },
            },
            {
                "q": {
                    "zh": "为什么说 Langfuse 的租户隔离“不是事后加一个 WHERE project_id 过滤”？",
                    "en": "Why is Langfuse's tenant isolation 'not an afterthought WHERE project_id filter'?",
                },
                "opts": [
                    {
                        "zh": "因为 project_id 被焊进 ClickHouse 排序键最前面：同项目数据物理相邻，“只看我的项目”退化成扫一段连续区间——隔离与高效合一，且结构性地不可能看到别人",
                        "en": "Because project_id is welded into the front of the ClickHouse ordering key: one project's data is physically adjacent, so 'see only my project' becomes scanning a contiguous range — isolation and efficiency in one, and structurally impossible to see others",
                    },
                    {"zh": "因为 Langfuse 不支持过滤", "en": "Because Langfuse doesn't support filtering"},
                    {"zh": "因为每个项目用独立的数据库实例", "en": "Because each project uses a separate database instance"},
                    {"zh": "因为 project_id 是随机的", "en": "Because project_id is random"},
                ],
                "answer": 0,
                "why": {
                    "zh": "若 project_id 只是普通过滤列，海量下既慢又危险（写漏过滤就串租户）。放进排序键最前，隔离变成“定位连续区间”，又快又结构性安全。代价：排序键难改、查询须带 project_id。",
                    "en": "If project_id were an ordinary filter column, it'd be slow at scale and dangerous (miss the filter and you leak across tenants). Put it first in the ordering key and isolation becomes 'locate a contiguous range' — fast and structurally safe. Cost: hard-to-change ordering key, project_id required on queries.",
                },
            },
            {
                "q": {
                    "zh": "ClickHouse 里 environment 列定义为 LowCardinality(String) DEFAULT 'default' AFTER project_id。这三点各有什么用意？",
                    "en": "The ClickHouse environment column is LowCardinality(String) DEFAULT 'default' AFTER project_id. What's the intent of each?",
                },
                "opts": [
                    {
                        "zh": "低基数：环境名就那么几个，省空间快查询；默认 default：不指定时自动归类、向后兼容老数据；紧跟 project_id：与之构成“项目+环境”定位前缀",
                        "en": "Low-cardinality: few env names, saving space and speeding queries; default 'default': auto-classify when unspecified, backward-compatible with old data; right after project_id: forms a 'project+environment' locating prefix with it",
                    },
                    {"zh": "纯粹为了占位，没有用意", "en": "Pure placeholder, no intent"},
                    {"zh": "为了让环境名可以无限多", "en": "To allow infinitely many env names"},
                    {"zh": "为了删除 project_id", "en": "To remove project_id"},
                ],
                "answer": 0,
                "why": {
                    "zh": "LowCardinality 适合取值少的列（编码省空间、查得快）；DEFAULT 'default' 让老数据/未指定环境的数据天然归到 default（向后兼容）；AFTER project_id 让二者构成定位前缀，按“项目+环境”查同样高效。",
                    "en": "LowCardinality suits low-distinct columns (compact encoding, fast queries); DEFAULT 'default' makes old/unspecified-env data fall into default (backward compatible); AFTER project_id forms a locating prefix so 'project+environment' queries stay efficient.",
                },
            },
        ],
        "open": [
            {
                "zh": "“把多租户隔离做进存储结构，而不是一道可能写漏的过滤”——这条思路你能用到自己的系统吗？把租户键放进主键/排序键最前，会给你带来什么好处和什么约束？",
                "en": "'Bake multi-tenant isolation into the storage structure, not a filter you might forget' — can you apply this to your own system? What benefits and constraints come from putting the tenant key first in the primary/ordering key?",
            },
        ],
    },
    "11-deployment-topology.html": {
        "mcq": [
            {
                "q": {
                    "zh": "自托管一套 Langfuse，最小栈包含哪些容器？",
                    "en": "What containers make up the minimal stack to self-host Langfuse?",
                },
                "opts": [
                    {
                        "zh": "2 个应用（langfuse-web、langfuse-worker）+ 4 个基础设施（postgres、clickhouse、redis、minio/S3），全在 docker-compose.yml",
                        "en": "2 apps (langfuse-web, langfuse-worker) + 4 infra (postgres, clickhouse, redis, minio/S3), all in docker-compose.yml",
                    },
                    {"zh": "只要一个 langfuse 容器", "en": "Just one langfuse container"},
                    {"zh": "web + worker + 一个 SQLite 文件", "en": "web + worker + one SQLite file"},
                    {"zh": "只需要 ClickHouse", "en": "Only ClickHouse"},
                ],
                "answer": 0,
                "why": {
                    "zh": "docker-compose.yml 列出两个应用容器（web/worker）加四个基础设施（postgres:17、clickhouse-server、redis:7、minio）。这正是第 5、7 课架构图的实体版。",
                    "en": "docker-compose.yml lists two app containers (web/worker) plus four infra (postgres:17, clickhouse-server, redis:7, minio). It's the physical version of the architecture in L05/L07.",
                },
            },
            {
                "q": {
                    "zh": "web 和 worker 都连同一套存储，为什么还要拆成两个容器、还能分别扩容？",
                    "en": "web and worker connect the same storage — why split into two containers, and why scale them separately?",
                },
                "opts": [
                    {
                        "zh": "职责相反：web 面向用户、要低延迟、按 QPS 扩；worker 啃重活、可重试、按队列积压扩。靠 Redis 队列解耦，所以能各自独立扩容、互不阻塞",
                        "en": "Opposite duties: web is user-facing, low-latency, scales by QPS; worker chews heavy jobs, retryable, scales by queue backlog. Decoupled by the Redis queue, so each scales independently without blocking the other",
                    },
                    {"zh": "因为一个容器装不下代码", "en": "Because one container can't hold the code"},
                    {"zh": "因为它们用不同的数据库", "en": "Because they use different databases"},
                    {"zh": "纯粹为了多开机器", "en": "Just to run more machines"},
                ],
                "answer": 0,
                "why": {
                    "zh": "用户压力（QPS）和后台压力（队列积压）是两条独立的扩容信号。拆成两个容器、用队列解耦，就能“用户多了加 web、队列堵了加 worker”，互不牵连。这是第 4 课窄腰让两容器独立演进的部署体现。",
                    "en": "User pressure (QPS) and background pressure (queue backlog) are independent scaling signals. Splitting into two containers decoupled by a queue lets you 'add web for more users, add worker for a backed-up queue', without entanglement. It's the deployment-side expression of L04's narrow waist.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 用 Zod 在“启动时”校验环境变量。这条纪律的好处是什么？",
                    "en": "Langfuse validates env vars with Zod 'at startup'. What's the benefit of this discipline?",
                },
                "opts": [
                    {
                        "zh": "配错/漏填会让进程直接启动失败并指出哪个变量有问题——把“配置错误”从难查的运行时 bug 变成一眼可见的启动错误，而不是带病运行到半路才崩",
                        "en": "A misconfig/missing var makes the process fail to start and names the bad variable — turning 'config errors' from hard-to-find runtime bugs into obvious startup errors, instead of running sick and crashing midway",
                    },
                    {"zh": "让启动更慢以便检查", "en": "To make startup slower for checking"},
                    {"zh": "把环境变量加密", "en": "To encrypt env vars"},
                    {"zh": "自动修正错误的配置", "en": "To auto-fix wrong config"},
                ],
                "answer": 0,
                "why": {
                    "zh": "fail-fast：env.ts 用 Zod 在启动时校验类型与必填项，错了立刻报清楚。这比“带着错误配置跑半天、在某个边角功能才崩”可调试得多（第 51 课展开）。",
                    "en": "Fail-fast: env.ts uses Zod to validate types and required fields at startup, reporting clearly on error. Far more debuggable than 'running with bad config and crashing in some corner feature later' (expanded in L51).",
                },
            },
        ],
        "open": [
            {
                "zh": "Langfuse 的自托管需要 4 个基础设施，门槛比“一个二进制”高。如果你做一个开源工具，会怎么在“能扛规模”和“易自托管”之间取舍？docker-compose 一键编排算不算一个好答案？",
                "en": "Langfuse self-host needs 4 infra engines, a higher bar than 'one binary'. If you built an open-source tool, how would you trade off 'handles scale' vs 'easy to self-host'? Is one-command docker-compose orchestration a good answer?",
            },
        ],
    },
    "12-ingestion-api.html": {
        "mcq": [
            {
                "q": {
                    "zh": "摄取 API 收到一批事件后只做三件事就立即返回。是哪三件？为什么不在这里合并/算成本/写库？",
                    "en": "The ingestion API does only three things on a batch, then returns immediately. Which three, and why not merge/cost/write-DB here?",
                },
                "opts": [
                    {
                        "zh": "鉴权 + Zod 校验 + 入队；因为 API 直面你的应用，首要目标是“永远快、不拖累调用方”，重活放这里会增加每次埋点的延迟、还会因下游抖动而失败",
                        "en": "auth + Zod validation + enqueue; because the API faces your app directly, its top goal is 'always fast, never drag the caller'; heavy work here would add latency to every call and fail on downstream hiccups",
                    },
                    {"zh": "鉴权 + 合并 + 写库；因为这样最快", "en": "auth + merge + write-DB; because it's fastest"},
                    {"zh": "压缩 + 加密 + 入队", "en": "compress + encrypt + enqueue"},
                    {"zh": "只做入队，不鉴权也不校验", "en": "only enqueue, no auth or validation"},
                ],
                "answer": 0,
                "why": {
                    "zh": "入口只保留“必须当场做”的最小集合（鉴权防越权、校验拦脏数据、入队完成交接），能异步的全交给 worker。入口越薄越扛洪峰、越不可能拖垮你的业务，代价是最终一致（第 5 课）。",
                    "en": "The entry keeps only the must-do-now minimum (auth prevents unauthorized writes, validation blocks dirty data, enqueue hands off), deferring everything async to the worker. The thinner the entry, the better it survives spikes and the less it drags your business — at the cost of eventual consistency (L05).",
                },
            },
            {
                "q": {
                    "zh": "ingestion.ts 的 handler 把真正的活交给一个叫 processEventBatch 的共享函数，连单独提交 score 的接口也复用它。这么做的好处是？",
                    "en": "The ingestion.ts handler delegates the real work to a shared processEventBatch, reused even by the standalone score endpoint. The benefit?",
                },
                "opts": [
                    {
                        "zh": "“收一批、校验、入队”到处都用得上，抽成一处就不必每个端点各写一遍、各错一遍（复杂度收敛到一处，第 6 课）",
                        "en": "'accept a batch, validate, enqueue' is needed everywhere; factoring it into one place avoids re-implementing (and re-bugging) it per endpoint (converge complexity, L06)",
                    },
                    {"zh": "为了让 score 接口更慢", "en": "to make the score endpoint slower"},
                    {"zh": "因为 score 不能走队列", "en": "because scores can't use the queue"},
                    {"zh": "纯粹为了多写代码", "en": "just to write more code"},
                ],
                "answer": 0,
                "why": {
                    "zh": "多个端点共享同一套摄取逻辑，维护在一处、测试在一处，避免分散实现导致的不一致。这与第 6 课“把复杂度收敛到一个能严格测试的地方”一脉相承。",
                    "en": "Multiple endpoints share one ingestion routine, maintained and tested in one place, avoiding inconsistency from scattered implementations — in line with L06's 'converge complexity to one strictly testable place'.",
                },
            },
            {
                "q": {
                    "zh": "为什么说“在入口用 Zod 校验、越早拒绝坏数据越好”，而且 API 还能返回“部分成功”？",
                    "en": "Why 'validate with Zod at the entry, reject bad data as early as possible', and why can the API return 'partial success'?",
                },
                "opts": [
                    {
                        "zh": "摄取每天吞下各种 SDK/版本的数据，难免有脏事件；入口拦下并给清晰错误，比让它流进队列、到 worker 才崩好得多；一批里坏几条只拒那几条、其余照收",
                        "en": "Ingestion swallows data from many SDKs/versions daily, inevitably with dirty events; rejecting at the entry with a clear error beats letting them crash the worker; a few bad events in a batch get rejected while the rest are accepted",
                    },
                    {"zh": "因为 Zod 能加密数据", "en": "because Zod encrypts data"},
                    {"zh": "因为坏数据更快", "en": "because bad data is faster"},
                    {"zh": "因为部分成功能省钱", "en": "because partial success saves money"},
                ],
                "answer": 0,
                "why": {
                    "zh": "fail-fast + 容错：在门口用 schema 拦下脏数据，避免污染下游、避免 worker 崩；同时按事件粒度返回部分成功，不因个别坏事件牵连整批。这让海量异构来源的摄取既健壮又友好。",
                    "en": "Fail-fast + fault tolerance: a schema blocks dirty data at the door, sparing downstream and the worker; per-event partial success avoids letting a few bad events doom the whole batch. This keeps ingestion from massive heterogeneous sources both robust and friendly.",
                },
            },
        ],
        "open": [
            {
                "zh": "把“接收”和“处理”切开、入口只做最小集合——这条思路你能用到自己写的 API 上吗？哪些工作“必须当场做”，哪些可以丢给后台异步？切错了会怎样？",
                "en": "Splitting 'accept' from 'process' so the entry does the minimum — can you apply this to your own APIs? Which work 'must happen now', and which can be deferred to async background? What if you split it wrong?",
            },
        ],
    },
    "13-event-types-merge.html": {
        "mcq": [
            {
                "q": {
                    "zh": "一次 LLM 调用，SDK 先发 generation-create、后发 generation-update，最后却落成 ClickHouse 里同一行。靠的是什么？",
                    "en": "For one LLM call the SDK sends generation-create then generation-update, yet they land as the same row in ClickHouse. How?",
                },
                "opts": [
                    {
                        "zh": "两个事件共享同一个实体 id（body.id），服务端按 body.id 分组合并成一行；冲突字段以 timestamp 更晚者为准（last-write-wins）",
                        "en": "Both events share one entity id (body.id); the server groups by body.id and merges into one row, conflicts resolved by later timestamp (last-write-wins)",
                    },
                    {"zh": "靠事件 id 相同来合并", "en": "they merge because their event ids are equal"},
                    {"zh": "靠 SDK 在本地先合并好再发一条", "en": "the SDK merges locally and sends just one"},
                    {"zh": "靠 ClickHouse 随机挑一条保留", "en": "ClickHouse randomly keeps one of them"},
                ],
                "answer": 0,
                "why": {
                    "zh": "实体 id（body.id）是合并键：同 id 的 create/update 注定汇成一行；事件 id（信封 id）是去重键，成为 S3 文件名 <eventId>.json 保证幂等。合并冲突时按 timestamp 最新者胜，正是第 8 课 ReplacingMergeTree(event_ts) 在写入侧的镜像。",
                    "en": "The entity id (body.id) is the merge key: same-id create/update converge into one row; the event id (envelope id) is the dedup key, becoming the S3 filename <eventId>.json for idempotency. Conflicts resolve latest-timestamp-wins — the write-side mirror of L08's ReplacingMergeTree(event_ts).",
                },
            },
            {
                "q": {
                    "zh": "事件用 z.discriminatedUnion(\"type\", […]) 定义，而不是“一个所有字段都可选的大 schema”。这样做的核心好处是？",
                    "en": "Events are defined with z.discriminatedUnion(\"type\", […]) rather than 'one big schema with all fields optional'. The core benefit?",
                },
                "opts": [
                    {
                        "zh": "每种 type 配一套严格的 body 规则：发 generation-create 必须符合 CreateGenerationBody，缺字段/填错类型当场被 Zod 拦下，校验既精确又能给出清晰错误",
                        "en": "A strict body ruleset per type: generation-create must match CreateGenerationBody; missing/wrong fields are rejected by Zod on the spot — precise validation with clear errors",
                    },
                    {"zh": "让所有事件都能随便填字段", "en": "lets every event fill any field freely"},
                    {"zh": "让事件体积更小", "en": "makes events smaller on the wire"},
                    {"zh": "可以省掉 type 字段", "en": "lets you drop the type field"},
                ],
                "answer": 0,
                "why": {
                    "zh": "判别联合用 type 这一个字段决定该套哪套 body 规则，是“一个字段定身份、一套规则配一种身”。比“全字段可选”精确得多——后者无法在入口拦下结构性错误，脏数据会一路流到 worker 才崩。",
                    "en": "The discriminated union uses the single type field to pick the body ruleset — 'one field sets identity, one ruleset per identity'. Far more precise than 'all-optional', which can't catch structural errors at the entry and lets dirty data crash the worker downstream.",
                },
            },
            {
                "q": {
                    "zh": "getClickhouseEntityType 把 18 种事件 type 坍缩成 5 个实体类型，其中 span / generation / agent / tool 等都归到哪个，意味着什么？",
                    "en": "getClickhouseEntityType collapses 18 event types into 5 entity types; where do span/generation/agent/tool land among them, and what does that imply?",
                },
                "opts": [
                    {
                        "zh": "全归到 observation，进同一张 observations 表，靠行内 type 列区分；新增一种观测类型不必加表、不必改 schema——这正是第 8 课“宽事件”的威力",
                        "en": "all into observation, the same observations table, distinguished by the row's type column; adding a new observation kind needs no new table or schema change — the power of L08's 'wide events'",
                    },
                    {"zh": "各自进一张独立的表", "en": "each into its own separate table"},
                    {"zh": "归到 trace 表", "en": "into the trace table"},
                    {"zh": "归到 score 表", "en": "into the score table"},
                ],
                "answer": 0,
                "why": {
                    "zh": "5 个实体类型里，三个核心的 trace / observation / score 正好对应第 8 课的三张 ReplacingMergeTree 宽表（另两个 sdk_log、dataset_run_item 各自处理）。所有“像观测”的形态共用 observations 一张表、用 type 列区分，所以 Langfuse 能不断新增观测类型（AGENT/TOOL/CHAIN…）而无需迁移表结构。",
                    "en": "Among the 5 entity types, the three core ones trace / observation / score map onto L08's three ReplacingMergeTree wide tables (the other two, sdk_log & dataset_run_item, are handled separately). Every 'observation-like' shape shares the one observations table, distinguished by the type column, so Langfuse can keep adding observation kinds (AGENT/TOOL/CHAIN…) without schema migrations.",
                },
            },
        ],
        "open": [
            {
                "zh": "create/update 拆成两个事件，把“攒着整条记录”的状态从客户端推给了服务端。你自己的系统里，有没有类似“让边缘无状态、让中心兜底”的地方？这样做的代价和收益各是什么？",
                "en": "Splitting create/update into two events pushes the 'hold the whole record' state from client to server. In your own systems, is there a similar 'keep the edge stateless, let the center backstop' spot? What are its costs and benefits?",
            },
        ],
    },
    "14-ingestion-queue.html": {
        "mcq": [
            {
                "q": {
                    "zh": "摄取队列里到底放了什么？为什么不直接把事件本体塞进 Redis？",
                    "en": "What's actually in the ingestion queue, and why not stuff the event body straight into Redis?",
                },
                "opts": [
                    {
                        "zh": "只放含 fileKey 的轻量任务（指针）；事件本体先写进 S3 的 <eventId>.json，worker 再照 fileKey 回 S3 读回——队列轻则 Redis 内存省、入队快，本体留在 S3 当“真账本”，任务丢了也能重建",
                        "en": "only a lightweight job carrying fileKey (a pointer); the body is first written to S3 as <eventId>.json, the worker reads it back by fileKey — a light queue saves Redis memory and speeds enqueue, while the body stays in S3 as the 'real ledger', rebuildable if a job is lost",
                    },
                    {"zh": "放事件的完整内容，包括可能很大的 input/output", "en": "the full event content, including possibly huge input/output"},
                    {"zh": "什么都不放，worker 自己去数据库查", "en": "nothing; the worker queries the DB itself"},
                    {"zh": "放一份加密后的事件副本", "en": "an encrypted copy of the event"},
                ],
                "answer": 0,
                "why": {
                    "zh": "S3 存本体、队列递指针是这条链路最易误解的点。Redis 内存金贵，任务越小越快越扛积压；S3 既是合并要回读的历史事件源（第 15 课），也是任务失败时的可重放依据。这就买到了“轻队列 + 持久存储”两样好处。",
                    "en": "S3 holds the body, the queue passes a pointer — the most-misunderstood point of the path. Redis memory is precious, so smaller jobs are faster and survive backlog; S3 is both the historical event source the merge reads back (L15) and the replay basis on job failure. You get 'light queue + durable storage' at once.",
                },
            },
            {
                "q": {
                    "zh": "分片键为什么选 projectId-eventBodyId，而不是随机分配？",
                    "en": "Why is the shard key projectId-eventBodyId rather than a random assignment?",
                },
                "opts": [
                    {
                        "zh": "对实体 id 哈希取模能保证“同一实体永远落同一 shard”：一条记录的 create/update 始终在同一队列、被同一 worker 有序处理，合并无需跨队列协调；随机分会把它们打散、合并时复杂又可能乱序",
                        "en": "hashing the entity id guarantees 'same entity always on the same shard': a record's create/update stay in one queue, processed in order by one worker, no cross-queue coordination at merge; random scatter would split them, making merge complex and prone to disorder",
                    },
                    {"zh": "因为随机分配根本无法实现", "en": "because random assignment is impossible to implement"},
                    {"zh": "因为 projectId-eventBodyId 最短", "en": "because projectId-eventBodyId is the shortest string"},
                    {"zh": "为了让每个 shard 负载完全相等", "en": "to make every shard's load exactly equal"},
                ],
                "answer": 0,
                "why": {
                    "zh": "用一致性哈希（SHA-256 取模）把负载摊到多个 Redis 节点，同时用实体 id 当键，让“同一实体同一 shard”天然成立——这与第 8 课用 project_id 领头排序键、第 13 课用 body.id 当合并键，是同一种“让相关数据物理聚在一起”的思路。",
                    "en": "Consistent hashing (SHA-256 modulo) spreads load across Redis nodes, while using the entity id as key makes 'same entity, same shard' hold naturally — the same 'keep related data physically together' idea as L08 leading the ordering key with project_id and L13 using body.id as the merge key.",
                },
            },
            {
                "q": {
                    "zh": "主队列 vs 次队列的隔离机制解决了什么问题？worker 何时把任务改道次队列？",
                    "en": "What problem does primary-vs-secondary isolation solve, and when does the worker redirect a job to the secondary?",
                },
                "opts": [
                    {
                        "zh": "防止某个超高吞吐项目塞满主队列、饿死其他项目；命中 env 白名单（静态隔离已知大户）或 S3 限流标志（动态临时改道）就把该任务原样入次队列并 return，主队列立刻服务别人",
                        "en": "it prevents one ultra-high-throughput project from packing the primary and starving others; on hitting the env allowlist (statically isolating known heavy hitters) or the S3 slowdown flag (dynamic temporary redirect), the worker re-enqueues the job to the secondary and returns, freeing the primary to serve others",
                    },
                    {"zh": "让次队列处理得更慢以省钱", "en": "to make the secondary slower to save money"},
                    {"zh": "次队列只处理失败的任务", "en": "the secondary only handles failed jobs"},
                    {"zh": "主队列只处理 trace，次队列只处理 score", "en": "primary handles only traces, secondary only scores"},
                ],
                "answer": 0,
                "why": {
                    "zh": "次队列有独立的分片数和独立的 worker，把洪峰与日常物理隔离。两条判断：env 白名单（LANGFUSE_SECONDARY_INGESTION_QUEUE_ENABLED_PROJECT_IDS）做静态隔离，S3 SlowDown 标志做动态减压。这是典型的“吵闹邻居”隔离，保障多租户公平。",
                    "en": "The secondary has its own shard count and workers, physically isolating spike from steady-state. Two checks: the env allowlist (LANGFUSE_SECONDARY_INGESTION_QUEUE_ENABLED_PROJECT_IDS) for static isolation, the S3 SlowDown flag for dynamic relief. A classic 'noisy neighbor' isolation safeguarding multi-tenant fairness.",
                },
            },
        ],
        "open": [
            {
                "zh": "“队列 + S3 当真账本”换来了削峰、容错、可重放，代价是多一跳和最终一致的延迟。如果让你给一个高并发写入系统做选型，你会在“直接写库”和“队列缓冲 + 对象存储”之间怎么权衡？哪些信号会让你倒向后者？",
                "en": "'Queue + S3 as real ledger' buys spike absorption, fault tolerance and replayability, at the cost of an extra hop and eventual-consistency latency. Designing a high-concurrency write system, how would you weigh 'write the DB directly' against 'queue buffer + object storage'? What signals would tip you toward the latter?",
            },
        ],
    },
    "15-ingestion-service.html": {
        "mcq": [
            {
                "q": {
                    "zh": "一个 observation 先收到 create（带 startTime、input、model），后收到 update（带 endTime、output、usage）。mergeRecords 合并后，startTime 和 model 还在吗？为什么？",
                    "en": "An observation gets create (startTime, input, model) then update (endTime, output, usage). After mergeRecords, do startTime and model survive? Why?",
                },
                "opts": [
                    {
                        "zh": "都还在：update 没带这些字段（值为 undefined），overwriteObject 的“不覆盖”规则会保留旧值；startTime 还是 immutable 键，本就锁死",
                        "en": "both survive: update doesn't carry them (undefined), so overwriteObject's 'don't overwrite' rule keeps the old values; startTime is also an immutable key, locked anyway",
                    },
                    {"zh": "都被清空：后到的 update 整体覆盖了 create", "en": "both wiped: the later update wholly overwrites create"},
                    {"zh": "随机保留其一", "en": "one of them is randomly kept"},
                    {"zh": "只有 model 还在，startTime 被清空", "en": "only model survives, startTime is wiped"},
                ],
                "answer": 0,
                "why": {
                    "zh": "overwriteObject 用 lodash mergeWith，命中三条之一就保留旧值：① immutable 键（id/project_id/trace_id/start_time/created_at/environment）② 值为 undefined ③ 空对象。update 只带变化字段，没带的 input/model 是 undefined 故不被抹；start_time 更是 immutable。这正是 create/update 能正确合并的根本。",
                    "en": "overwriteObject uses lodash mergeWith and keeps the old value on any of three: ① immutable keys (id/project_id/trace_id/start_time/created_at/environment) ② undefined value ③ empty object. update carries only changed fields, so absent input/model are undefined and not wiped; start_time is immutable anyway. This is exactly why create/update merge correctly.",
                },
            },
            {
                "q": {
                    "zh": "合并时，mergeRecords 的输入数组里第一个元素总是 ClickHouse 已存在的那条记录。把它放第一位有什么用？",
                    "en": "In mergeRecords, the first element of the input array is always the existing ClickHouse record. What's the point of putting it first?",
                },
                "opts": [
                    {
                        "zh": "它当 immutable 字段的基线：左折叠从它开始，后续事件只能覆盖 mutable 字段；created_at、start_time 等锁死字段以它为准，保证身份/锚点稳定",
                        "en": "it's the baseline for immutable fields: the left-fold starts from it, later events can only overwrite mutable fields; locked fields like created_at, start_time take its value, keeping identity/anchors stable",
                    },
                    {"zh": "纯粹是数组顺序习惯，没有语义", "en": "purely an array-order habit, no semantics"},
                    {"zh": "为了让 ClickHouse 记录覆盖所有新事件", "en": "so the ClickHouse record overwrites all new events"},
                    {"zh": "为了先把它删掉", "en": "to delete it first"},
                ],
                "answer": 0,
                "why": {
                    "zh": "折叠从最左（CH 底稿）往右叠事件，后者覆盖前者。但 immutable 键不被覆盖，于是 created_at/start_time 等永远保留 CH 底稿（即第一次写定）的值。这让“读旧底稿 + 叠新修订”既纳新又不改旧，是合并正确性的关键。",
                    "en": "The fold goes left (CH base) to right (events), later overwriting earlier. But immutable keys aren't overwritten, so created_at/start_time keep the CH base's (first-written) value. This lets 'read old base + apply new revisions' absorb new while preserving old — key to merge correctness.",
                },
            },
            {
                "q": {
                    "zh": "既然第 8 课的 ReplacingMergeTree 会按 event_ts 自动去重，为什么 IngestionService 在写入侧还要预合并一遍？",
                    "en": "Since Lesson 8's ReplacingMergeTree auto-dedups by event_ts, why does IngestionService still pre-merge on the write side?",
                },
                "opts": [
                    {
                        "zh": "两层解决不同时刻的问题：写入侧预合并保证“写出的那一行当下就完整正确”，查询立即可读；ReplacingMergeTree 的后台去重是最终发生的，收拾并发竞态的尾巴。event_ts=now 让新行总能胜出，两层咬合成纵深防御",
                        "en": "the two layers solve problems at different moments: write-side pre-merge ensures 'the written row is complete and correct now', readable immediately; ReplacingMergeTree's background dedup is eventual, cleaning up concurrency races. event_ts=now lets the new row always win, meshing the layers into defense in depth",
                    },
                    {"zh": "因为 ReplacingMergeTree 其实不工作", "en": "because ReplacingMergeTree doesn't actually work"},
                    {"zh": "为了把数据写两遍更安全", "en": "to write the data twice for safety"},
                    {"zh": "纯粹是历史遗留代码", "en": "purely legacy code"},
                ],
                "answer": 0,
                "why": {
                    "zh": "写入侧求“即时正确”——不预合并的话，查询会读到半成品（只有 create 没有 update）；存储侧求“最终唯一”——收拾“同一记录被并发处理产生多行”的竞态。event_ts=now 这个版本戳把两层咬合：预合并产出的新行 event_ts 更大，必在 ReplacingMergeTree 去重里胜出。这是典型的纵深防御。",
                    "en": "The write side seeks 'immediate correctness' — without pre-merge, queries would read a half-baked row (create but no update); the storage side seeks 'eventual uniqueness', cleaning races that produce multiple rows for one record. The event_ts=now stamp meshes them: a pre-merged new row has a larger event_ts and always wins ReplacingMergeTree's dedup. Classic defense in depth.",
                },
            },
        ],
        "open": [
            {
                "zh": "IngestionService 把“合并”和“落盘”切成两层，又把“即时正确”和“最终唯一”分给写入侧与存储侧。这种“同一目标、两层各管一段、用一个版本戳咬合”的纵深防御，你在自己接触过的系统里见过类似设计吗？它的好处和复杂度代价你怎么看？",
                "en": "IngestionService splits 'merge' from 'persist', and assigns 'immediate correctness' to the write side and 'eventual uniqueness' to the storage side. Have you seen this 'one goal, two layers each owning a stretch, meshed by a version stamp' defense-in-depth elsewhere? How do you weigh its benefits against the added complexity?",
            },
        ],
    },
    "16-token-counting-cost.html": {
        "mcq": [
            {
                "q": {
                    "zh": "你的 SDK 上报了 usage={input:1000, output:500}，也报了 cost={total: 0.01}。Langfuse 会怎么处理 token 数和成本？",
                    "en": "Your SDK reported usage={input:1000, output:500} and cost={total: 0.01}. How does Langfuse handle the token counts and cost?",
                },
                "opts": [
                    {
                        "zh": "都直接采用你报的：token 跳过分词、用你的 1000/500；成本因为你给了至少一项，全用你的 0.01，连价目表都不查——provided 压倒 computed",
                        "en": "uses yours directly: tokens skip tokenization and use your 1000/500; since you gave at least one cost point, it uses your 0.01 wholesale and doesn't even consult the rate card — provided beats computed",
                    },
                    {"zh": "重新分词验证你的 token 数，再按价目表重算成本", "en": "re-tokenizes to verify your counts, then recomputes cost from the rate card"},
                    {"zh": "把你报的和系统估算的取平均", "en": "averages your reported values with the system's estimate"},
                    {"zh": "忽略你报的，一律自己算", "en": "ignores your values and computes everything itself"},
                ],
                "answer": 0,
                "why": {
                    "zh": "provided 压倒 computed 是贯穿 Langfuse 的原则。getUsageUnits 见有 provided_usage 就直接用；calculateUsageCosts 见“给了任一 cost 点”就全用 provided、不再算别的。系统从不把估算和你报的真实值混用，因为半真半估的账更危险。",
                    "en": "Provided beats computed runs through all of Langfuse. getUsageUnits uses provided_usage directly when present; calculateUsageCosts, seeing 'any cost point given', uses provided wholesale and computes nothing else. The system never mixes estimates with your real reported values, since a half-real, half-estimated bill is more dangerous.",
                },
            },
            {
                "q": {
                    "zh": "你用裸 HTTP 调了一个模型，埋点里没有任何 usage。什么情况下 Langfuse 会替你分词数 token？",
                    "en": "You called a model over raw HTTP with no usage in the event. When will Langfuse tokenize-count for you?",
                },
                "opts": [
                    {
                        "zh": "三条同时满足：模型名能正则匹配到一条 model 记录、observation 不是 ERROR、且你没提供 usage——这时用该模型的 tokenizerId 对 input/output 分词计数",
                        "en": "all three hold: the model name regex-matches a model row, the observation isn't ERROR, and you provided no usage — then it counts input/output tokens using that model's tokenizerId",
                    },
                    {"zh": "任何时候都会无条件分词", "en": "always, unconditionally"},
                    {"zh": "只有付费版才会分词", "en": "only on the paid plan"},
                    {"zh": "只有当 level=ERROR 时才分词", "en": "only when level=ERROR"},
                ],
                "answer": 0,
                "why": {
                    "zh": "computed 是有前提的兜底：匹配到模型（才知道用哪种 tokenizer、什么价）、非 ERROR（错误生成没必要算）、且无 provided。三者缺一就不分词。分词用 model.tokenizerId，在 worker/src/features/tokenisation 里、可走独立线程以免阻塞。",
                    "en": "Computed is a precondition-gated backstop: a matched model (so it knows which tokenizer and price), non-ERROR (no point counting a failed generation), and no provided usage. Missing any one, no tokenization. It counts via model.tokenizerId, in worker/src/features/tokenisation, optionally on a separate thread to avoid blocking.",
                },
            },
            {
                "q": {
                    "zh": "findModel 把模型名匹配到价目时，如果一个项目自定义了 gpt-4o 的价格，同时内置也有 gpt-4o，会用哪条？",
                    "en": "When findModel matches a model name to a price, if a project customized gpt-4o's price while a built-in gpt-4o also exists, which is used?",
                },
                "opts": [
                    {
                        "zh": "用项目自定义的：SQL 是 project_id = ? OR project_id IS NULL，再 ORDER BY project_id，项目模型排在全局(NULL)前面；同名下还按 start_date 最新取一条",
                        "en": "the project's custom one: the SQL is project_id = ? OR project_id IS NULL, then ORDER BY project_id so project rows rank before global (NULL); among those it also takes the latest start_date",
                    },
                    {"zh": "用内置的，自定义会被忽略", "en": "the built-in; the customization is ignored"},
                    {"zh": "随机选一条", "en": "picks one at random"},
                    {"zh": "两条价格相加", "en": "adds the two prices together"},
                ],
                "answer": 0,
                "why": {
                    "zh": "findModel 用 Postgres 正则 ~ match_pattern 匹配，WHERE 同时取项目模型与全局(project_id IS NULL)，ORDER BY project_id 让自定义优先、start_date DESC 取最新生效价、LIMIT 1。于是项目能覆盖默认定价或加自有模型，历史数据按当时价、新数据按新价。",
                    "en": "findModel matches via Postgres regex ~ match_pattern, the WHERE takes both project and global (project_id IS NULL) models, ORDER BY project_id prioritizes custom, start_date DESC takes the latest effective price, LIMIT 1. So projects can override defaults or add own models; history is priced at its time, new data at the new price.",
                },
            },
        ],
        "open": [
            {
                "zh": "“可信来源优先、估算只做兜底、两者严格隔离”——这条原则不止用于 token/成本。想想你自己的系统里，有没有“用户/上游给的权威数据”和“本地推断/估算”并存的场景？你会怎么设计它们的优先级与隔离，避免半真半估造成的误判？",
                "en": "'Trusted source first, estimation only as backup, the two strictly isolated' — this principle isn't only for tokens/cost. In your own systems, where do 'authoritative data from users/upstream' and 'local inference/estimates' coexist? How would you design their precedence and isolation to avoid the misjudgment of half-real, half-estimated data?",
            },
        ],
    },
    "17-clickhouse-writer.html": {
        "mcq": [
            {
                "q": {
                    "zh": "ClickhouseWriter 为什么要把单条记录攒成大批再写，而不是 IngestionService 算完一条就直接 INSERT 一条？",
                    "en": "Why does ClickhouseWriter batch single records before writing, instead of IngestionService INSERTing each record as soon as it's computed?",
                },
                "opts": [
                    {
                        "zh": "因为 ClickHouse 的 MergeTree 每次 INSERT 都落一个磁盘分片(part)，逐条写会产生海量小分片、后台合并追不上、查询变慢甚至触发 too-many-parts 拒写；攒成一批只生成一个大分片",
                        "en": "because ClickHouse's MergeTree drops a disk part per INSERT; row-by-row spawns a flood of tiny parts, background merges can't keep up, queries slow, even hitting the too-many-parts guard; one batch makes just one big part",
                    },
                    {"zh": "因为攒批能加密数据", "en": "because batching encrypts the data"},
                    {"zh": "因为 IngestionService 不能访问数据库", "en": "because IngestionService can't access the database"},
                    {"zh": "因为单条写会丢数据", "en": "because single writes lose data"},
                ],
                "answer": 0,
                "why": {
                    "zh": "第 8 课讲过 ClickHouse 偏爱大批量。MergeTree 每个 INSERT 生成一个数据分片，小分片越多、磁盘元数据和后台合并压力越大。把高频小写翻译成低频大写，是列式存储扛住高频摄取的必要前提，而非可有可无的优化。",
                    "en": "Lesson 8 noted ClickHouse prefers large batches. Each INSERT creates a MergeTree part; more tiny parts means heavier disk metadata and background merges. Translating high-frequency small writes into low-frequency large ones is a precondition for a columnar store to withstand high-frequency ingestion, not an optional optimization.",
                },
            },
            {
                "q": {
                    "zh": "ClickhouseWriter 的两个 flush 触发条件是什么？为什么需要两个而不是一个？",
                    "en": "What are ClickhouseWriter's two flush triggers, and why two rather than one?",
                },
                "opts": [
                    {
                        "zh": "① 某表队列 ≥ batchSize（按量）② 定时器每 writeInterval 触发 flushAll（按时）；谁先到算谁——高峰靠“坐满”保吞吐，低谷靠“到点”保延迟上限，缺一就会要么延迟失控、要么批永远凑不满",
                        "en": "① a table's queue ≥ batchSize (by size) ② a timer fires flushAll every writeInterval (by time); whichever first — rush hour uses 'full' for throughput, lulls use 'on time' to cap latency; with only one, either latency runs away or batches never fill",
                    },
                    {"zh": "① 内存满 ② 磁盘满", "en": "① memory full ② disk full"},
                    {"zh": "① 白天 ② 夜间", "en": "① daytime ② nighttime"},
                    {"zh": "只有一个：队列满才写", "en": "only one: write when the queue is full"},
                ],
                "answer": 0,
                "why": {
                    "zh": "只靠 batchSize：低谷期凑不满一批，记录会无限期滞留内存、延迟失控。只靠定时器：高峰期一个 interval 内涌入远超一批，仍可能积压。两者“谁先到算谁”互补：高吞吐批批写满拉高效率，低吞吐到点即发封顶延迟。关机时再 flushAll(true) 排空，不丢数据。",
                    "en": "batchSize alone: in a lull a batch never fills, so records linger in memory indefinitely with runaway latency. Timer alone: at peak far more than a batch floods in per interval, risking backlog. The two complement 'whichever first': high throughput writes full batches for efficiency, low throughput flushes on time to cap latency. On shutdown, flushAll(true) drains everything, losing nothing.",
                },
            },
            {
                "q": {
                    "zh": "记录攒在内存队列里，worker 崩溃这批就没了。Langfuse 为什么敢用这种“易失”的内存缓冲？",
                    "en": "Records sit in an in-memory queue, so a worker crash loses that batch. Why does Langfuse dare to use such 'volatile' in-memory buffering?",
                },
                "opts": [
                    {
                        "zh": "因为持久性由上游兜底：每个事件原原本本在 S3，队列任务写库成功前不会被确认；崩了任务会重投、从 S3 重读重合并重写，一条不丢——所以这层可放心用内存换吞吐",
                        "en": "because durability is backstopped upstream: every event sits verbatim in S3, and the queue job isn't acked until the DB write succeeds; on crash the job is redelivered, re-reads from S3, re-merges and re-writes, losing nothing — so this layer can trade memory for throughput",
                    },
                    {"zh": "因为 worker 永远不会崩", "en": "because the worker never crashes"},
                    {"zh": "因为内存比磁盘更可靠", "en": "because memory is more reliable than disk"},
                    {"zh": "因为丢一点数据无所谓", "en": "because losing some data is fine"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这是典型的分层智慧：S3（第 14 课）负责“绝不丢”，ClickhouseWriter 负责“写得快”，谁也不为对方妥协。因为队列 + S3 已经保证了持久性与可重放，写入器才敢用易失内存缓冲去换吞吐——崩溃只是触发一次重投重算。",
                    "en": "Classic layered wisdom: S3 (Lesson 14) owns 'never lose', ClickhouseWriter owns 'write fast', neither compromising for the other. Because the queue + S3 already guarantee durability and replayability, the writer can trade volatile memory buffering for throughput — a crash merely triggers a redeliver-and-recompute.",
                },
            },
        ],
        "open": [
            {
                "zh": "ClickhouseWriter 把“持久”交给上游 S3、自己专注“高效”，于是敢用易失内存缓冲换吞吐。这种“把不同的质量目标分给不同层、各自做到极致”的思路，你在自己设计系统时会怎么运用？如果某一层既要快又要绝不丢，会带来哪些额外复杂度？",
                "en": "ClickhouseWriter delegates durability to upstream S3 and focuses on efficiency, so it dares to trade volatile memory buffering for throughput. How would you apply this 'assign different quality goals to different layers, each taken to the extreme' approach in your own designs? If one layer must be both fast and never-lose, what extra complexity does that bring?",
            },
        ],
    },
    "18-opentelemetry-ingestion.html": {
        "mcq": [
            {
                "q": {
                    "zh": "OTLP 数据从 /otel/v1/traces 进来后，OtelIngestionProcessor 把 span 翻译成什么？之后又如何处理？",
                    "en": "After OTLP data enters at /otel/v1/traces, what does OtelIngestionProcessor translate spans into, and what happens next?",
                },
                "opts": [
                    {
                        "zh": "翻译成原生的 IngestionEventType[]（第 13 课事件格式）：observation 交 IngestionService.mergeAndWrite，trace 走 processEventBatch——从此与原生 SDK 数据完全同路（合并/算钱/落盘共用一套）",
                        "en": "into native IngestionEventType[] (Lesson 13's format): observations go to IngestionService.mergeAndWrite, traces to processEventBatch — thereafter identical to native-SDK data (one shared merge/cost/write)",
                    },
                    {"zh": "直接写进一张专门的 otel 表，不经过合并", "en": "straight into a dedicated otel table, skipping merge"},
                    {"zh": "转成 SQL 语句执行", "en": "into SQL statements to execute"},
                    {"zh": "原样存进 S3 就结束了", "en": "just stored verbatim in S3 and done"},
                ],
                "answer": 0,
                "why": {
                    "zh": "OTel 摄取本质是“边缘适配、核心归一”。OtelIngestionProcessor.processToIngestionEvents 把 span 映射成原生事件格式，按实体类型分流后汇入第 15–17 课同一条管道。OTel 特异的只有最前端的映射，后端与原生完全共享。",
                    "en": "OTel ingestion is essentially 'adapt at the edge, unify at the core'. OtelIngestionProcessor.processToIngestionEvents maps spans into the native event format, splits by entity type, and converges into the same Lesson 15–17 pipeline. Only the front-end mapping is OTel-specific; the backend is fully shared with native.",
                },
            },
            {
                "q": {
                    "zh": "同一个“模型名”，OpenTelemetry 写在 gen_ai.response.model、Vercel AI SDK 写在 ai.model.id、OpenLLMetry 写在 llm.model_name。适配器怎么应对这种混乱？",
                    "en": "The same 'model name' is written to gen_ai.response.model by OpenTelemetry, ai.model.id by Vercel AI SDK, llm.model_name by OpenLLMetry. How does the adapter cope with this mess?",
                },
                "opts": [
                    {
                        "zh": "为每个字段准备一份优先级属性键列表，从上往下试，第一个有值的就采用；新约定出现只需往列表里加几个键，老数据不受影响、新数据立刻被认得",
                        "en": "it keeps a priority list of attribute keys per field, tries top to bottom, takes the first present; a new convention just needs a few keys added to the list — old data unaffected, new data instantly recognized",
                    },
                    {"zh": "要求所有用户统一改用一种约定", "en": "requires all users to standardize on one convention"},
                    {"zh": "随机选一个键", "en": "picks a key at random"},
                    {"zh": "只认 OpenTelemetry 官方约定，其他一律丢弃", "en": "only recognizes the official OpenTelemetry convention, discarding others"},
                ],
                "answer": 0,
                "why": {
                    "zh": "extractModelName 依次尝试 langfuse 原生 → gen_ai.response.model → ai.model.id → gen_ai.request.model → llm.* → 通用 model，第一个命中即用。usage、input/output 同理。这种“加键即兼容”的优先级回退，让 Langfuse 不必强迫用户改约定，也能跟着生态演进。",
                    "en": "extractModelName tries in turn langfuse-native → gen_ai.response.model → ai.model.id → gen_ai.request.model → llm.* → generic model, using the first hit. usage and input/output likewise. This 'add a key, gain compatibility' priority fallback lets Langfuse avoid forcing users to change conventions while evolving with the ecosystem.",
                },
            },
            {
                "q": {
                    "zh": "原生摄取比 OTel 更精确，为什么 Langfuse 还要支持 OpenTelemetry？这个取舍的本质是什么？",
                    "en": "Native ingestion is more precise than OTel — so why does Langfuse still support OpenTelemetry, and what's the essence of the tradeoff?",
                },
                "opts": [
                    {
                        "zh": "为了“去用户所在的地方接住他们”：OTel 是事实标准，无数应用早已埋好点；支持 OTLP 意味着用户不用改一行埋点就能接入。代价是一个满是回退的适配器+推断的语义损耗，但适配器只在最前端，翻完即汇入共享核心",
                        "en": "to 'meet users where they are': OTel is the de facto standard and countless apps are already instrumented; supporting OTLP means users onboard without changing a line of instrumentation. The cost is a fallback-laden adapter + inference's semantic loss, but the adapter is only at the front, converging into the shared core after translation",
                    },
                    {"zh": "因为 OTel 比原生更快", "en": "because OTel is faster than native"},
                    {"zh": "因为原生 SDK 即将废弃", "en": "because the native SDK is being deprecated"},
                    {"zh": "纯粹为了营销噱头", "en": "purely a marketing gimmick"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这是经典的适配器模式：把脏活、特例（追各家约定、处理语义落差）收敛到边缘的一层适配器，让核心（合并/算钱/落盘）保持纯净统一。降低接入门槛换来更广的用户覆盖，而复杂度被限制在最前端一层，不污染后端。",
                    "en": "A classic adapter pattern: confine the grunt work and special cases (chasing conventions, handling the semantic gap) to one edge adapter, keeping the core (merge/cost/write) pure and unified. Lowering the onboarding barrier buys broader user coverage, while complexity is confined to the front layer without polluting the backend.",
                },
            },
        ],
        "open": [
            {
                "zh": "“把适配各种外部格式的脏活收敛到边缘一层适配器，核心只认一种统一格式”——这条原则你在自己的系统里能用上吗？如果要同时支持多种输入协议/数据源，你会在哪里画那条“适配器 vs 核心”的边界？画错了会怎样？",
                "en": "'Confine the grunt work of adapting various external formats to one edge adapter, and let the core know only one unified format' — can you apply this in your own systems? If you must support multiple input protocols/data sources, where would you draw the 'adapter vs core' boundary? What goes wrong if you draw it wrong?",
            },
        ],
    },
    "19-media-blob-storage.html": {
        "mcq": [
            {
                "q": {
                    "zh": "一次多模态调用的 input 里有一张 3MB 的图。Langfuse 是怎么处理它的，ClickHouse 里最终存了什么？",
                    "en": "A multimodal call's input has a 3MB image. How does Langfuse handle it, and what ends up in ClickHouse?",
                },
                "opts": [
                    {
                        "zh": "图片本体存进 S3 媒体桶，事件里那张图被替换成一个小引用串 @@@langfuseMedia:…@@@；ClickHouse 只存这个几十字节的引用，绝不存 3MB 二进制",
                        "en": "the image body goes into the S3 media bucket, and in the event the image is replaced by a small reference @@@langfuseMedia:…@@@; ClickHouse stores only that few-dozen-byte reference, never the 3MB binary",
                    },
                    {"zh": "把 3MB base64 直接存进 ClickHouse 的 input 列", "en": "stores the 3MB base64 straight into ClickHouse's input column"},
                    {"zh": "把图片丢弃，只留文字", "en": "discards the image, keeping only text"},
                    {"zh": "把图片压缩后存进 Postgres", "en": "compresses the image into Postgres"},
                ],
                "answer": 0,
                "why": {
                    "zh": "大块二进制绝不能进 ClickHouse 宽表，否则 input/output 列暴涨、拖慢所有查询。Langfuse 把 blob 与引用分离：本体进 S3 媒体桶，事件里只留 MEDIA_REFERENCE_PATTERN 匹配的小引用串，ClickHouse 始终精瘦。",
                    "en": "Large binaries must never enter ClickHouse wide tables, or input/output columns balloon and slow every query. Langfuse splits blob from reference: the body to the S3 media bucket, the event keeping only a small reference matched by MEDIA_REFERENCE_PATTERN, keeping ClickHouse lean.",
                },
            },
            {
                "q": {
                    "zh": "媒体上传时，SDK 先把 sha256 报给服务端、而不是直接把文件 POST 过去。这个“先报指纹”的设计带来哪两个好处？",
                    "en": "On media upload, the SDK first reports the sha256 to the server instead of POSTing the file directly. What two benefits does this 'fingerprint first' design bring?",
                },
                "opts": [
                    {
                        "zh": "① 去重：按 (projectId, sha256) 查 prisma.media，已传过就回 uploadUrl=null 跳过，同一文件只存一份；② 直传：未命中则返回 presigned URL，SDK 把本体直接 PUT 进 S3，绕开应用服务器省带宽",
                        "en": "① dedup: look up prisma.media by (projectId, sha256), if already uploaded return uploadUrl=null to skip, storing the same file once; ② direct upload: on miss return a presigned URL so the SDK PUTs the body straight to S3, bypassing app servers and saving bandwidth",
                    },
                    {"zh": "① 加密文件 ② 压缩文件", "en": "① encrypt the file ② compress the file"},
                    {"zh": "① 给文件改名 ② 给文件分类", "en": "① rename the file ② categorize it"},
                    {"zh": "① 让上传更慢 ② 让 API 更忙", "en": "① slow the upload ② busy the API"},
                ],
                "answer": 0,
                "why": {
                    "zh": "先报指纹让服务端能在传输前就判断“是否已有同一文件”，实现内容寻址去重；命中则秒过，未命中才发 presigned URL 让 SDK 直传 S3。本体全程不经 Langfuse 应用层，既省带宽又不堵 API——这是把大文件挡在热路径之外的关键一招。",
                    "en": "Reporting the fingerprint first lets the server decide 'do we already have this file' before any transfer, achieving content-addressed dedup; on hit it passes instantly, on miss it issues a presigned URL for the SDK to upload directly to S3. The body never passes through Langfuse's app layer, saving bandwidth and not clogging the API — key to keeping big files off the hot path.",
                },
            },
            {
                "q": {
                    "zh": "为什么 Langfuse 要把遥测数据放 ClickHouse、媒体 blob 放 S3，而不是图省事都放一处？背后的核心原则是什么？",
                    "en": "Why does Langfuse put telemetry in ClickHouse and media blobs in S3, rather than everything in one place? What's the core principle?",
                },
                "opts": [
                    {
                        "zh": "因为两者“体质”不同：遥测小、结构化、要高频查询聚合（适合 ClickHouse 宽表）；媒体大、是不透明二进制、几乎只按 id 整取（适合对象存储）。让每种数据待在最适合它的存储里，互不拖累",
                        "en": "because their 'constitutions' differ: telemetry is small, structured, frequently queried/aggregated (fits ClickHouse wide tables); media is large, opaque binary, almost only fetched whole by id (fits object storage). Let each kind of data live in the storage that fits it best, neither dragging the other",
                    },
                    {"zh": "因为 S3 比 ClickHouse 更快查询", "en": "because S3 queries faster than ClickHouse"},
                    {"zh": "因为 ClickHouse 不能存文本", "en": "because ClickHouse can't store text"},
                    {"zh": "纯粹是历史原因", "en": "purely historical reasons"},
                ],
                "answer": 0,
                "why": {
                    "zh": "把几 MB 图片塞进 ClickHouse 会同时毁两件事：宽表撑爆、连不碰图的查询也被拖慢，又用昂贵分析库干对象存储的活。各按本性安置——结构化进 ClickHouse、二进制进 S3、引用串牵线、sha256 去重——这条“让每种数据待在最适合的存储里”正是第 7 课双存储分工的延续，也为第三部分收尾。",
                    "en": "Stuffing a multi-MB image into ClickHouse ruins two things: the wide table bloats and even image-free queries slow, and you waste a pricey analytical store on object storage's job. Placing each by its nature — structured to ClickHouse, binary to S3, linked by a reference, deduped by sha256 — extends Lesson 7's dual-store division of labor and closes out Part 3.",
                },
            },
        ],
        "open": [
            {
                "zh": "“让每种数据待在最适合它的存储里，用一个小引用把它们牵起来”——这条原则在你做过的系统里有没有类似场景（比如大文件、日志、缩略图）？你会怎么决定“什么放主库、什么放对象存储/外部存储”，那条边界怎么画？内容寻址去重又能帮你省下什么？",
                "en": "'Let each kind of data live in the storage that fits it best, linked by a small reference' — is there a similar scenario in systems you've built (large files, logs, thumbnails)? How would you decide 'what goes in the main DB vs object/external storage', and where to draw that line? What could content-addressed dedup save you?",
            },
        ],
    },
    "20-web-app-architecture.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的 web 应用为什么并存三种 API 风格（tRPC、公共 REST、App-Router/SSE），而不是统一成一种？",
                    "en": "Why does Langfuse's web app run three API styles (tRPC, public REST, App-Router/SSE) rather than unifying into one?",
                },
                "opts": [
                    {
                        "zh": "因为对内和对外是两类需求：UI 要类型安全、改得快（tRPC，前后端共享类型）；SDK 要契约稳定、带版本（REST + Fern）；少数流式/webhook 要原始 Request 语义（App-Router）。硬统一会牺牲其一",
                        "en": "because internal and external are two needs: the UI wants type-safety and fast change (tRPC, shared types front-to-back); SDKs want a stable, versioned contract (REST + Fern); a few streaming/webhook cases need raw Request semantics (App-Router). Forcing unity sacrifices one of them",
                    },
                    {"zh": "因为开发者忘了删旧代码", "en": "because developers forgot to delete old code"},
                    {"zh": "因为三种 API 各自更快", "en": "because each API is individually faster"},
                    {"zh": "因为 Next.js 强制要求三种都用", "en": "because Next.js mandates all three"},
                ],
                "answer": 0,
                "why": {
                    "zh": "核心边界是“对内求类型安全与迭代速度、对外求契约稳定与版本可控”。UI 和后端同仓同队，tRPC 把类型贯穿、重构即时报错；SDK 面向外部用户，接口发布后不能随意改，需 REST+版本+Fern。同一批数据、两种对外姿态——按受众分而治之，比强求统一更合适。",
                    "en": "The core boundary: internally seek type-safety and iteration speed, externally seek a stable, versioned contract. UI and backend share one repo/team, so tRPC threads types and errors instantly on refactor; the SDK faces external users where published interfaces can't change freely, needing REST+versions+Fern. Same data, two external postures — dividing by audience fits better than forced uniformity.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 几乎全用老的 Pages Router，App Router 下只有 4 个文件。这说明了什么？",
                    "en": "Langfuse uses the old Pages Router for almost everything, with only 4 files under App Router. What does this show?",
                },
                "opts": [
                    {
                        "zh": "务实的取舍：Pages Router + tRPC 是 App Router 成熟前就立的稳固根基，贸然迁移收益小风险大；App Router 只保留给需要原始 Request/流式/webhook 这类 Pages Router 不擅长的语义",
                        "en": "a pragmatic choice: Pages Router + tRPC is a solid foundation laid before App Router matured, so a rash migration is low-reward/high-risk; App Router is kept only for raw Request/streaming/webhook semantics Pages Router handles awkwardly",
                    },
                    {"zh": "代码库已经过时、无人维护", "en": "the codebase is outdated and unmaintained"},
                    {"zh": "App Router 完全不能用", "en": "App Router is completely unusable"},
                    {"zh": "团队不知道 App Router 存在", "en": "the team doesn't know App Router exists"},
                ],
                "answer": 0,
                "why": {
                    "zh": "架构选择服务于团队现实而非追新。tRPC 让前后端共享类型，是全栈团队快速迭代的关键；迁移成本高、收益小。App Router 的 4 个文件（layout + stripe-webhook/chatCompletion/in-app-agent）正是那些需要原始 Request、流式或 webhook 语义的特例——合适比统一更重要。",
                    "en": "Architecture serves team reality, not novelty. tRPC's shared types are key to fast full-stack iteration; migration is costly and low-reward. App Router's 4 files (layout + stripe-webhook/chatCompletion/in-app-agent) are exactly the cases needing raw Request, streaming, or webhook semantics — fit matters more than uniformity.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 的 web/src 用 features/ 按“功能”切分（约 80 个纵向模块），而不是按“技术层”（全部页面/全部组件/全部接口各一目录）。这样组织的主要好处是？",
                    "en": "Langfuse's web/src cuts by 'feature' under features/ (~80 vertical modules) rather than by 'technical layer' (all pages/all components/all APIs each in one dir). The main benefit?",
                },
                "opts": [
                    {
                        "zh": "每个功能是自包含的竖切片，把它的组件、状态、server 逻辑收在一处；读懂或改一个功能主要只看一个目录，功能之间边界清晰、不易牵连",
                        "en": "each feature is a self-contained vertical slice gathering its components, state, and server logic in one place; to understand or change a feature you mostly read one directory, with clear boundaries that don't entangle",
                    },
                    {"zh": "让目录数量更少", "en": "to have fewer directories"},
                    {"zh": "强制所有功能共享代码", "en": "to force all features to share code"},
                    {"zh": "让构建更快", "en": "to make builds faster"},
                ],
                "answer": 0,
                "why": {
                    "zh": "按功能切分（vertical slice）让一个功能的全部代码聚在 features/<功能>/ 一处，避免在 pages/components/api 三四个目录间来回跳。修改局部化、边界清晰，是大型前端可维护性的关键——这也是为什么后面每课几乎都能指向一个 features/ 子目录。",
                    "en": "By-feature (vertical-slice) organization gathers a feature's whole code under features/<feature>/, avoiding hops across pages/components/api. Localized changes and clear boundaries are key to large-frontend maintainability — which is why nearly every later lesson points at a features/ subfolder.",
                },
            },
        ],
        "open": [
            {
                "zh": "“对内类型安全、对外契约稳定”——同一批数据用两种 API 姿态对待。你做过的系统里，内部调用和对外接口是混在一起还是分开的？如果分开，你会怎么划界？tRPC 这种“前后端共享类型”的收益，在什么规模/团队结构下最划算？",
                "en": "'Internal type-safety, external stable contract' — the same data treated with two API postures. In systems you've built, are internal calls and external interfaces mixed or separated? If separated, how would you draw the line? At what scale/team structure does tRPC's 'shared types front-to-back' pay off most?",
            },
        ],
    },
    "21-trpc-backbone.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 用 procedure 构建器（publicProcedure / authenticatedProcedure / protectedProjectProcedure）来定义 tRPC 接口。这种「分层中间件栈」的本质是什么？",
                    "en": "Langfuse defines tRPC endpoints with procedure builders (publicProcedure / authenticatedProcedure / protectedProjectProcedure). What's the essence of this 'layered middleware stack'?",
                },
                "opts": [
                    {
                        "zh": "procedure 是一摞中间件按 .use() 叠出来的；公开门只过 OTel+错误处理，受保护门再叠登录、项目成员校验。中间件定义一次，每个路由按需挑选——RBAC 不必各写一遍",
                        "en": "a procedure is a stack of middleware chained by .use(); a public door passes only OTel+error handling, a protected door adds login and project-member checks. Middleware is defined once and each router picks what it needs — RBAC isn't rewritten per router",
                    },
                    {"zh": "每个路由都必须手写完整的鉴权逻辑", "en": "every router must hand-write full auth logic"},
                    {"zh": "procedure 只是给接口起个名字，无实际作用", "en": "procedures just name endpoints, with no real effect"},
                    {"zh": "中间件只能用一个，不能叠加", "en": "only one middleware is allowed, no stacking"},
                ],
                "answer": 0,
                "why": {
                    "zh": "tRPC 的精髓是 procedure = 可叠加的中间件栈。withOtelTracingProcedure 叠 OTel，再 .use(withErrorHandling) 得 publicProcedure，再 .use(enforceUserIsAuthed) 得 authenticatedProcedure，再换成 enforceUserIsAuthedAndProjectMember 得 protectedProjectProcedure。声明式组合让安全检查写一次、处处复用。",
                    "en": "tRPC's essence is procedure = stackable middleware. withOtelTracingProcedure adds OTel, then .use(withErrorHandling) gives publicProcedure, then .use(enforceUserIsAuthed) gives authenticatedProcedure, then swapping in enforceUserIsAuthedAndProjectMember gives protectedProjectProcedure. Declarative composition lets a security check be written once and reused everywhere.",
                },
            },
            {
                "q": {
                    "zh": "protectedProjectProcedure 的 RBAC 中间件做了一件关键的事：它在 resolver 跑之前就从请求输入里取出 projectId。为什么这一招重要？",
                    "en": "protectedProjectProcedure's RBAC middleware does one key thing: it pulls projectId from the request input before the resolver runs. Why does this matter?",
                },
                "opts": [
                    {
                        "zh": "校验先于业务逻辑发生：任何受保护路由都不可能在没核验「你是这个 project 成员」之前碰到数据，租户隔离由结构保证，而非靠每个路由作者自觉",
                        "en": "the check happens before business logic: no protected router can ever touch data before verifying 'you're a member of this project', so tenant isolation is guaranteed by structure, not by each router author's diligence",
                    },
                    {"zh": "为了让请求更快返回", "en": "to make requests return faster"},
                    {"zh": "为了节省数据库连接", "en": "to save database connections"},
                    {"zh": "projectId 只是用来打日志", "en": "projectId is only used for logging"},
                ],
                "answer": 0,
                "why": {
                    "zh": "enforceUserIsAuthedAndProjectMember 用 getRawInput() 取出 projectId，再去 session 的「组织→项目」树里查成员资格，不通过就抛 FORBIDDEN。这让每个受保护路由自动获得统一、前置的租户校验——正是第 10 课「project_id 是隔离键」在 API 层的落地，安全靠结构而非靠人。",
                    "en": "enforceUserIsAuthedAndProjectMember pulls projectId via getRawInput(), then checks membership in the session's 'org→project' tree, throwing FORBIDDEN otherwise. This gives every protected router uniform, up-front tenant checking — Lesson 10's 'project_id is the isolation key' landing at the API layer, security by structure not by people.",
                },
            },
            {
                "q": {
                    "zh": "所有 procedure 最底层都叠了 withErrorHandling 这一中间件。它对 ClickHouse 的资源类错误（内存超限、超时）做了什么特殊处理？",
                    "en": "All procedures stack withErrorHandling at the base. What special handling does it give ClickHouse resource errors (out-of-memory, timeout)?",
                },
                "opts": [
                    {
                        "zh": "把它们映射成 UNPROCESSABLE_CONTENT 并附上「换个更小的时间范围」之类可操作建议；同时隐藏 5xx 内部细节与堆栈，防止泄露",
                        "en": "maps them to UNPROCESSABLE_CONTENT with actionable advice like 'try a smaller time range'; and hides 5xx internal detail and stacks to prevent leaks",
                    },
                    {"zh": "直接把原始堆栈和 SQL 返回给前端", "en": "returns the raw stack and SQL straight to the frontend"},
                    {"zh": "忽略错误，返回空结果", "en": "ignores the error and returns empty results"},
                    {"zh": "自动重试一百次", "en": "automatically retries a hundred times"},
                ],
                "answer": 0,
                "why": {
                    "zh": "withErrorHandling 统一翻译异常：5xx 隐藏内部细节防泄露；ClickHouse 资源错误（如内存/超时）被特判为 UNPROCESSABLE_CONTENT，并给出「缩小时间范围」等用户能照做的建议。于是无论哪个路由查崩了什么，用户看到的都是一致、可读、不暴露内幕的错误。",
                    "en": "withErrorHandling uniformly translates exceptions: 5xx hides internal detail to prevent leaks; ClickHouse resource errors (memory/timeout) are special-cased to UNPROCESSABLE_CONTENT with actionable advice like 'narrow the time range'. So whatever router blew up, the user sees a consistent, readable error that doesn't expose internals.",
                },
            },
        ],
        "open": [
            {
                "zh": "「把安全检查收敛成中间件、用声明式 procedure 组合，而不是每个接口各写一遍」——这条原则你能用到自己的系统吗？如果你的 API 有几十个端点都要做同一种权限校验，你会怎么设计，才能让「新增端点几乎不可能漏掉校验」？",
                "en": "'Converge security checks into middleware and compose via declarative procedures, rather than hand-writing per endpoint' — can you apply this to your systems? If your API has dozens of endpoints all needing the same permission check, how would you design it so 'a new endpoint can hardly miss the check'?",
            },
        ],
    },
    "22-repository-layer.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 让所有 ClickHouse 读取都经过一个 queryClickhouse() 执行器，而不是各处直接写查询。这样做最核心的收益是？",
                    "en": "Langfuse routes all ClickHouse reads through one queryClickhouse() executor rather than writing queries everywhere. The core benefit?",
                },
                "opts": [
                    {
                        "zh": "横切关注（OTel 追踪、查询标签、退避重试、资源错误包装）一次实现、处处生效；加一项能力全平台查询一起获得，不会有的写有的漏、写法不一",
                        "en": "cross-cutting concerns (OTel tracing, query tags, backoff retry, resource-error wrapping) are implemented once and apply everywhere; add a capability and every query gains it, with no some-write-some-omit inconsistency",
                    },
                    {"zh": "让查询语法更简单", "en": "to make query syntax simpler"},
                    {"zh": "因为 ClickHouse 只接受一个连接", "en": "because ClickHouse accepts only one connection"},
                    {"zh": "为了隐藏 SQL 不让人看", "en": "to hide the SQL from view"},
                ],
                "answer": 0,
                "why": {
                    "zh": "可观测性、追责、重试、资源保护都和「业务查什么」无关却每条查询都需要。收敛到一个执行器，它们一次实现、处处复用；散落各处的裸查询必然写法不一、漏东漏西。这与第 6 课「把复杂度收敛到一处」一脉相承。",
                    "en": "Observability, accountability, retry, resource protection are unrelated to 'what business queries' yet needed by every query. Converged into one executor they're implemented once and reused; scattered raw queries inevitably drift and omit. In line with L06's 'converge complexity to one place'.",
                },
            },
            {
                "q": {
                    "zh": "queryClickhouse 通过 log_comment 给每条 SQL 打上 project/面/路由标签。这个标签的实际用处是？",
                    "en": "queryClickhouse tags every SQL via log_comment with project/surface/route. What's the practical use?",
                },
                "opts": [
                    {
                        "zh": "标签随查询进入 ClickHouse 的查询日志；当某条慢查询拖垮集群时，运维能直接在日志里按标签定位是哪个 project/面/路由的元凶——把可观测性焊进数据访问层",
                        "en": "the tags enter ClickHouse's query log with the query; when a slow query drags the cluster down, operators can locate the culprit project/surface/route by tag right in the log — observability welded into the data-access layer",
                    },
                    {"zh": "标签用来加密查询", "en": "the tags encrypt the query"},
                    {"zh": "标签让查询更快", "en": "the tags speed up the query"},
                    {"zh": "标签替代了 WHERE 条件", "en": "the tags replace the WHERE clause"},
                ],
                "answer": 0,
                "why": {
                    "zh": "sendClickhouseQuery 把标签塞进 clickhouse_settings.log_comment，于是每条打到 CH 的 SQL 都自带「谁/哪个面/哪个路由发起」。出现慢查询或资源耗尽时，可在 CH 自己的查询日志里按标签追责——这是散落各处的裸查询永远做不到的。",
                    "en": "sendClickhouseQuery stuffs tags into clickhouse_settings.log_comment, so every SQL hitting CH carries 'who/which surface/which route initiated it'. On a slow query or resource exhaustion, you can trace the culprit by tag in CH's own query log — impossible for scattered raw queries.",
                },
            },
            {
                "q": {
                    "zh": "把一条 trace 的观测拼起来时，Langfuse 不全表扫 observations，而是只在 trace 时间戳前后一个有界窗口（如 2 天）内找。为什么能、且为什么要这样？",
                    "en": "To stitch a trace's observations, Langfuse doesn't full-scan observations but searches only a bounded window (e.g. 2 days) around the trace timestamp. Why can it, and why must it?",
                },
                "opts": [
                    {
                        "zh": "能：trace/observation/score 是三张独立宽表、靠时间关联，且一条 trace 的观测几乎都集中在它发生后很短时间内；要：否则跨表 JOIN 要扫几个月上亿行，把分析库当事务库用必然拖垮集群",
                        "en": "can: trace/observation/score are three independent wide tables correlated by time, and a trace's observations almost all cluster shortly after it; must: otherwise the cross-table JOIN scans months and billions of rows, crashing the cluster by using an analytical store like a transactional one",
                    },
                    {"zh": "因为 2 天前的数据会被自动删除", "en": "because data older than 2 days is auto-deleted"},
                    {"zh": "因为 ClickHouse 不支持大于 2 天的查询", "en": "because ClickHouse can't query beyond 2 days"},
                    {"zh": "纯粹是随便定的限制", "en": "an arbitrary limit"},
                ],
                "answer": 0,
                "why": {
                    "zh": "第 8 课让三表独立、靠时间关联，JOIN 没有外键可走。回看时间窗（OBSERVATIONS_TO_TRACE_INTERVAL=2 天、SCORE=1 小时）注入 WHERE，配合按月分区只扫几个相关分区。代价是极长尾观测可能漏（约 98% 在 5 分钟内，2 天留足裕量）——用极小正确性换巨大成本节省。",
                    "en": "L08 made the three tables independent and time-correlated, so JOINs have no FK to follow. Look-back windows (OBSERVATIONS_TO_TRACE_INTERVAL=2 days, SCORE=1 hour) injected into WHERE, with monthly partitioning, scan only a few relevant partitions. The cost is missing extreme-long-tail observations (~98% finish within 5 min; 2 days leaves margin) — a tiny correctness trade for huge cost savings.",
                },
            },
        ],
        "open": [
            {
                "zh": "「把所有数据访问收敛到一个执行器，统一加上追踪、标签、重试、资源保护」——这条原则你能用到自己的系统吗？如果你的代码里到处是裸 SQL/裸 HTTP 调用，把它们收敛到一个执行器，你最想先统一加上哪三样能力？为什么？",
                "en": "'Converge all data access into one executor, uniformly adding tracing, tags, retry, resource protection' — can you apply this to your systems? If your code is full of raw SQL/raw HTTP calls, converging them into one executor, which three capabilities would you add first, and why?",
            },
        ],
    },
    "23-filtering-search-bar.html": {
        "mcq": [
            {
                "q": {
                    "zh": "用户的过滤来自侧栏、搜索栏、AI 三种入口，后端又有 ClickHouse 和 Postgres 两套。Langfuse 让它们都先汇成一个 FilterState 再编译成 SQL，最大的好处是？",
                    "en": "Filters come from three entries (sidebar, search bar, AI), and there are two backends (ClickHouse, Postgres). Langfuse converges them into one FilterState before compiling to SQL. The biggest benefit?",
                },
                "opts": [
                    {
                        "zh": "把 N×M 的直连组合降成 N+M：每个输入只管译成 FilterState、每个后端只管从 FilterState 译出 SQL；校验与参数化只在中间做一次，新增输入白嫖所有后端与全部安全",
                        "en": "it cuts the N×M direct-wiring combinatorics to N+M: each input only translates to FilterState, each backend only translates FilterState to SQL; validation and parameterization happen once in the middle, and a new input freeloads all backends and all the safety",
                    },
                    {"zh": "让查询变快", "en": "it makes queries faster"},
                    {"zh": "可以不用 WHERE 条件", "en": "it removes the need for WHERE clauses"},
                    {"zh": "让前端不用写代码", "en": "the frontend needs no code"},
                ],
                "answer": 0,
                "why": {
                    "zh": "若每个输入直连每个后端，是 N×M 套翻译 + N×M 处注入风险，新增输入要为每个后端重写。收敛到一个 FilterState 中间契约后变 N+M：输入只译入、后端只译出，校验/参数化集中一次。这是「单一中间表示」的核心收益。",
                    "en": "Wiring each input to each backend is N×M translations + N×M injection risks, and a new input means rewriting for every backend. Converging to one FilterState contract makes it N+M: inputs only translate in, backends only translate out, validation/parameterization centralized once. The core gain of a single intermediate representation.",
                },
            },
            {
                "q": {
                    "zh": "FilterState 编译成 ClickHouse SQL 时，每个过滤器的 apply() 用随机命名的占位符（如 stringFilter_xY9z）传值，而不是把值拼进 SQL 字符串。这防住了什么？",
                    "en": "When FilterState compiles to ClickHouse SQL, each filter's apply() passes values via randomly-named placeholders (e.g. stringFilter_xY9z) rather than splicing values into the SQL string. What does this prevent?",
                },
                "opts": [
                    {
                        "zh": "SQL 注入：用户输入的值永远是被绑定的参数、不进 SQL 文本，哪怕写 '; DROP TABLE… 也只当普通字符串匹配；加上工厂校验列存在/类型兼容，脏输入编译期就被挡下",
                        "en": "SQL injection: user values are always bound parameters, never in the SQL text, so even '; DROP TABLE… is matched as a plain string; plus the factory's column-existence/type checks stop dirty input at compile time",
                    },
                    {"zh": "防止查询太慢", "en": "prevents slow queries"},
                    {"zh": "防止结果太多", "en": "prevents too many results"},
                    {"zh": "防止用户看到数据", "en": "prevents users from seeing data"},
                ],
                "answer": 0,
                "why": {
                    "zh": "参数化查询是防注入的根本：值绑定到占位符、由驱动安全代入，绝不与 SQL 文本拼接。随机参数名进一步避免命名冲突。工厂还前置校验列是否在 schema、类型是否兼容，并注入强制 project_id（第 10 课）——多道防线叠加。",
                    "en": "Parameterized queries are the root of injection defense: values bind to placeholders and are safely substituted by the driver, never spliced into SQL text. Random param names avoid collisions. The factory also pre-checks column existence, type compatibility, and injects the mandatory project_id (L10) — layered defenses.",
                },
            },
            {
                "q": {
                    "zh": "AI filter 用大模型从自然语言生成过滤，可大模型可能编造不存在的列。Langfuse 怎么保证幻觉列绝不被应用？",
                    "en": "The AI filter uses an LLM to generate filters from natural language, but the model may hallucinate nonexistent columns. How does Langfuse ensure hallucinated columns are never applied?",
                },
                "opts": [
                    {
                        "zh": "把模型输出往返一遍：用 filterStateToQueryText 转回搜索栏语法、再解析回 FilterState，只保留能干净往返的；还原不了的（幻觉/非法列）直接丢弃。能表达才能进——构造即合法",
                        "en": "it round-trips the model output: convert back to search-bar grammar via filterStateToQueryText and re-parse to FilterState, keeping only what cleanly round-trips; un-restorable ones (hallucinated/illegal columns) are dropped. Only the expressible passes — valid by construction",
                    },
                    {"zh": "人工逐条审核模型输出", "en": "a human reviews each model output"},
                    {"zh": "信任模型，直接应用", "en": "trusts the model and applies directly"},
                    {"zh": "让模型自己检查", "en": "asks the model to check itself"},
                ],
                "answer": 0,
                "why": {
                    "zh": "generateFilter 调 Bedrock 生成候选，再通过 filterStateToQueryText 往返：只有能还原成合法搜索栏语法（即能降解成 FilterState 能表达的过滤）的才被采纳，其余 droppedCount++ 丢弃。因为输出必须能被 FilterState 表达，幻觉列从结构上就进不来——安全靠表示边界而非事后检查。",
                    "en": "generateFilter calls Bedrock for candidates, then round-trips via filterStateToQueryText: only filters that restore to valid search-bar grammar (i.e. lower to what FilterState expresses) are accepted, the rest droppedCount++. Because the output must be expressible by FilterState, hallucinated columns can't enter structurally — safety from the representation's boundaries, not after-checks.",
                },
            },
        ],
        "open": [
            {
                "zh": "「让 AI 的输出必须能还原成一个受限中间表示，不能表达的就进不来」——这种『构造即合法』的护栏，比『生成后再用规则检查』强在哪？你能想到把它用到自己系统里哪个『让 LLM 生成结构化指令』的场景吗？",
                "en": "'Make the AI output have to restore to a constrained intermediate representation, and the inexpressible can't enter' — how is this 'valid by construction' guardrail stronger than 'generate then check with rules'? Can you think of a 'let an LLM generate structured commands' scenario in your own systems where you'd apply it?",
            },
        ],
    },
    "24-lists-and-tables.html": {
        "mcq": [
            {
                "q": {
                    "zh": "打开 trace 列表时，Langfuse 并行发 traces.all（行）和 traces.metrics（指标）两路，而不是一次查全。这样设计为了什么？",
                    "en": "Opening the trace list, Langfuse fires traces.all (rows) and traces.metrics (metrics) in parallel rather than one combined query. Why?",
                },
                "opts": [
                    {
                        "zh": "紧凑行便宜、立刻就到，先把表画出来；成本/延迟/评分等指标要 JOIN 两张表、较慢，作为附加信息后到再按 id 合并。感知延迟从「最慢一路」降到「最快一路」",
                        "en": "compact rows are cheap and arrive instantly so the table paints first; cost/latency/score metrics need 2 JOINs and are slower, merged in by id later as extra info. Perceived latency drops from 'slowest call' to 'fastest call'",
                    },
                    {"zh": "为了多发请求把服务器压垮", "en": "to flood the server with more requests"},
                    {"zh": "因为 ClickHouse 不能一次查两类数据", "en": "because ClickHouse can't query two kinds at once"},
                    {"zh": "为了让指标更准确", "en": "to make metrics more accurate"},
                ],
                "answer": 0,
                "why": {
                    "zh": "列表的体验目标是秒开，而指标天生昂贵（2 JOIN）。把便宜的行和昂贵的指标拆开，joinTableCoreAndMetrics 按 id 合并、指标缺席也返回 success，于是表格先用行渲染、指标后到补入。这是「紧凑列表模型」——能立刻给的先给，要算的边算边补。",
                    "en": "The list's goal is instant open, but metrics are inherently expensive (2 JOINs). Splitting cheap rows from costly metrics, joinTableCoreAndMetrics merges by id and returns success even without metrics, so the table renders from rows first and fills metrics later. The 'compact list model' — give what you can instantly, fill in what you compute as it comes.",
                },
            },
            {
                "q": {
                    "zh": "traces 是 ReplacingMergeTree（同 id 可能多行）。默认按时间排序时，Langfuse 不用 FINAL，而是 ORDER BY toDate(timestamp),event_ts DESC + LIMIT 1 BY id。为什么这样更好？",
                    "en": "traces is a ReplacingMergeTree (one id may have multiple rows). For default time ordering, Langfuse skips FINAL and uses ORDER BY toDate(timestamp),event_ts DESC + LIMIT 1 BY id. Why is this better?",
                },
                "opts": [
                    {
                        "zh": "FINAL 会当场读全部分区去重、很慢；而按时间排序 + LIMIT 1 BY id 让 CH 只从磁盘读最新那天的分区、在内存里取每个 id 的最新行——既对又快，不必为去重捞一个月的数据",
                        "en": "FINAL reads all partitions and dedups on the spot, slow; time ordering + LIMIT 1 BY id lets CH read only the latest day's partition from disk and take each id's latest row in memory — correct and fast, no pulling a month of data just to dedup",
                    },
                    {"zh": "因为 FINAL 会返回错误结果", "en": "because FINAL returns wrong results"},
                    {"zh": "因为 LIMIT 1 BY id 更省内存", "en": "because LIMIT 1 BY id saves memory"},
                    {"zh": "因为默认排序不需要去重", "en": "because default ordering needs no dedup"},
                ],
                "answer": 0,
                "why": {
                    "zh": "FINAL 正确但慢（读全量去重）。默认按时间排序时，用 event_ts DESC + LIMIT 1 BY id 在内存里取每个 id 最新行，CH 只读最新分区。只有按非时间列（如成本）排序时才退回 FROM traces FINAL 全量去重——按需付费，常见路径不被拖累。",
                    "en": "FINAL is correct but slow (reads all to dedup). For default time ordering, event_ts DESC + LIMIT 1 BY id takes each id's latest row in memory, CH reading only the latest partition. Only sorting by a non-time column (e.g. cost) falls back to FROM traces FINAL full dedup — pay on demand, the common path unburdened.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 的表格状态（过滤、排序、列设置、视图预设）分三层存储，以 URL 为真源。这样分层最直接的好处是？",
                    "en": "Langfuse stores table state (filters, sort, column settings, view presets) in three layers, with the URL as the source of truth. The most direct benefit?",
                },
                "opts": [
                    {
                        "zh": "URL 编码当前视图 → 把链接发给同事，他看到的和你一模一样（可分享/可深链）；session 记导航间状态不丢；DB 存永久预设、可跨设备共享，失效列优雅降级",
                        "en": "the URL encodes the current view → send a colleague the link and they see exactly what you do (shareable/deep-linkable); session preserves state across navigation; DB stores permanent presets, cross-device shareable, with graceful degradation for invalid columns",
                    },
                    {"zh": "让表格渲染更快", "en": "to render the table faster"},
                    {"zh": "为了减少数据库查询", "en": "to reduce database queries"},
                    {"zh": "为了隐藏过滤条件", "en": "to hide filter conditions"},
                ],
                "answer": 0,
                "why": {
                    "zh": "三层各管一段时效：URL「此刻可分享」（深链、一个链接复现全貌，呼应第 23 课 FilterState）、session「这次导航」（跳转间不丢列宽/可见列）、DB「永久」（saved view 跨设备团队共享，失效部分丢弃+提示不白屏）。这让大表格既快又稳又可分享。",
                    "en": "Three layers each own a timescale: URL 'shareable now' (deep links, one link reproduces the whole view, echoing L23's FilterState), session 'this navigation' (column widths/visible columns survive hops), DB 'permanent' (saved views shared cross-device/team, invalid parts dropped+warned, no blank screen). This makes big tables fast, stable, and shareable.",
                },
            },
        ],
        "open": [
            {
                "zh": "「为最常见路径极致优化，把复杂度/代价推迟到真的要了才引入」——紧凑行 vs 指标、按需 JOIN、按需 FINAL 都是这条原则。你做过的列表/详情界面里，有没有「为了 1% 的高级需求，拖慢了 99% 的日常浏览」的地方？你会怎么拆？",
                "en": "'Optimize for the most common path, defer complexity/cost until actually asked' — compact rows vs metrics, conditional JOIN, conditional FINAL all follow it. In your own list/detail UIs, is there a place where 'the 1% advanced need slows the 99% daily browse'? How would you split it?",
            },
        ],
    },
    "25-trace-detail-tree.html": {
        "mcq": [
            {
                "q": {
                    "zh": "详情页要看一条 trace 的整棵观测树，可 byIdWithObservationsAndScores 取观测时却传 includeIO:false（不带 input/output）。为什么？",
                    "en": "The detail page shows a trace's whole observation tree, yet byIdWithObservationsAndScores fetches observations with includeIO:false (no input/output). Why?",
                },
                "opts": [
                    {
                        "zh": "树查询只带结构与时序（轻、快），整棵树立刻可见；某个观测的 IO 可能是几 MB JSON、几百个叠起来会爆，所以点开哪个节点才懒加载那一个的 IO——按需付费，不为没看的节点买单",
                        "en": "the tree query carries only structure and timing (light, fast) so the whole tree shows instantly; one observation's IO can be a multi-MB JSON and hundreds explode, so only opening a node lazy-loads that one's IO — pay on demand, never for nodes you didn't look at",
                    },
                    {"zh": "因为观测没有 IO 字段", "en": "because observations have no IO fields"},
                    {"zh": "为了隐藏 IO 不让用户看", "en": "to hide IO from users"},
                    {"zh": "因为 IO 存在另一个数据库", "en": "because IO lives in another database"},
                ],
                "answer": 0,
                "why": {
                    "zh": "一条 agent trace 可能有几百个观测，每个 IO 是不短的 JSON。开树就拉全部 IO 会是几十 MB、好几秒，而你大多数节点根本不展开——白拉。Langfuse 让树先到（结构+时序）、IO 点开懒加载，于是超大 trace 详情也能秒开。",
                    "en": "An agent trace may have hundreds of observations, each IO a sizeable JSON. Loading all IO when opening the tree would be tens of MB and seconds, yet you won't expand most nodes — wasted. Langfuse sends the tree first (structure+timing) and lazy-loads IO on click, so even a huge trace's detail opens instantly.",
                },
            },
            {
                "q": {
                    "zh": "第 24 课列表「极力推迟」、第 25 课详情「一次取全树」，看似相反。它们其实遵循同一条原则，是哪条？",
                    "en": "Lesson 24's list 'defers aggressively' while Lesson 25's detail 'fetches the whole tree' — seemingly opposite. What single principle do they share?",
                },
                "opts": [
                    {
                        "zh": "先取有界的维度、推迟无界的维度：列表面对无界行数→连稍贵的列都推迟；详情面对一条 trace（观测数有界）→结构取全，但树内单个观测 IO 仍是无界维度→懒加载。只急着取你扛得住的那部分",
                        "en": "fetch the bounded dimension first, defer the unbounded one: the list faces unbounded rows → defer even slightly pricey columns; the detail faces one trace (bounded observation count) → fetch structure in full, but a single observation's IO is still an unbounded dimension within → lazy-load. Only rush to fetch the part you can bear",
                    },
                    {"zh": "都尽量多取数据", "en": "both fetch as much data as possible"},
                    {"zh": "都尽量少取数据", "en": "both fetch as little data as possible"},
                    {"zh": "列表用 ClickHouse、详情用 Postgres", "en": "list uses ClickHouse, detail uses Postgres"},
                ],
                "answer": 0,
                "why": {
                    "zh": "关键是有界性。列表的行数无界（几千几万），故连一行里稍贵的指标都推迟；详情面对一条 trace，观测数虽多但有界，且看全这一条正是详情价值，故结构与时序一次取全。但有界实体内仍藏无界维度（单观测 IO），于是同一纪律下沉到树内：树取全、IO 缓取、verbosity 封顶。",
                    "en": "The key is boundedness. The list's row count is unbounded (thousands+), so even per-row metrics are deferred; the detail faces one trace whose observation count, though large, is bounded, and seeing this one in full is the detail's value, so structure and timing are fetched at once. But a bounded entity hides an unbounded dimension (per-observation IO), so the same discipline descends into the tree: fetch the tree, defer IO, cap with verbosity.",
                },
            },
            {
                "q": {
                    "zh": "byId 接口带一个 verbosity 参数（compact/truncated/full），在服务端决定 trace 自身 IO 是否解析/截断。为什么要在服务端而不是前端做这个截断？",
                    "en": "byId carries a verbosity param (compact/truncated/full) deciding server-side whether the trace's own IO is parsed/truncated. Why truncate server-side rather than on the frontend?",
                },
                "opts": [
                    {
                        "zh": "等数据传到前端再裁已经晚了——那几 MB 已从 ClickHouse 读出、序列化、走完网络。verbosity 让裁剪发生在最靠近数据源处：compact 压根不取、truncated 序列化前截短、full 才完整返回",
                        "en": "trimming after data reaches the frontend is too late — those MB already got read from ClickHouse, serialized, crossed the network. verbosity puts trimming closest to the source: compact doesn't fetch, truncated cuts before serialization, only full returns it whole",
                    },
                    {"zh": "前端不能截断字符串", "en": "the frontend can't truncate strings"},
                    {"zh": "为了让前端代码更简单", "en": "to simplify frontend code"},
                    {"zh": "因为服务端更安全", "en": "because the server is more secure"},
                ],
                "answer": 0,
                "why": {
                    "zh": "截断的目的是省「读取+序列化+传输」的成本；这些成本在数据离开 ClickHouse 时就已发生，到前端再裁只是徒劳。verbosity 在服务端、最靠近数据源处定档：compact 不取 IO、truncated 序列化前截短、full 完整。于是同一个 byId 既能给列表轻量预览、又能给详情看全文。",
                    "en": "Truncation aims to save 'read+serialize+transfer' cost; those costs already happen as data leaves ClickHouse, so trimming at the frontend is futile. verbosity tiers server-side, closest to the source: compact fetches no IO, truncated cuts before serialization, full returns whole. So one byId serves both a list's lightweight preview and a detail's full text.",
                },
            },
        ],
        "open": [
            {
                "zh": "「圈定有界维度先取、推迟无界维度」——这条原则你能用到自己做的「列表 + 详情」界面吗？想想你的实体里哪些维度是有界的（适合一次取）、哪些是无界的（该懒加载或封顶）？你会在哪一层、用什么手段给无界维度封顶？",
                "en": "'Fence the bounded dimension and fetch it first, defer the unbounded one' — can you apply this to your own 'list + detail' UIs? Which dimensions of your entities are bounded (fetch at once) and which unbounded (lazy-load or cap)? At which layer and by what means would you cap the unbounded ones?",
            },
        ],
    },
    "26-sessions.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的 session（会话，比如一段多轮对话）的「指标与列表」在存储上是怎么回事？",
                    "en": "How do a Langfuse session's metrics and listing (e.g. a multi-turn conversation) exist in storage?",
                },
                "opts": [
                    {
                        "zh": "它们不单独存，而是 traces 按 session_id 的 GROUP BY 现算出来——session_id 只是第 8 课宽表上的一列，分组即得各项聚合指标（仅有一个轻量元数据存根 trace_sessions 在摄取时落 Postgres）",
                        "en": "they aren't stored separately but computed on the fly by GROUP BY of traces on session_id — session_id is just a column on Lesson 8's wide table, grouping yields all the aggregate metrics (only a lightweight metadata stub, trace_sessions, is persisted to Postgres on ingestion)",
                    },
                    {"zh": "每个会话的全部指标（计数/成本/时长）都预先算好、存进一张表，每条 trace 进来都更新它", "en": "every session's full metrics (count/cost/duration) are pre-computed and stored in a table, updated by each incoming trace"},
                    {"zh": "session 的指标全存在 Redis 里", "en": "session metrics all live in Redis"},
                    {"zh": "session 是前端临时拼出来的，后端完全不参与", "en": "sessions are assembled ad-hoc on the frontend, with no backend involvement"},
                ],
                "answer": 0,
                "why": {
                    "zh": "session_id 本就是 traces 宽表的一列，按它 GROUP BY 就能现算出会话的全部指标：user_ids（去重）、trace_count（计数）、duration（最晚−最早）、session_total_cost（求和）。这些聚合不预存——避免每条 trace 都要同步更新。摄取时只往 Postgres trace_sessions 落一个极轻的存根（id/project/environment + 元数据如收藏/公开），登记会话存在，但不存指标。",
                    "en": "session_id is already a column on the traces wide table, so GROUP BY on it computes all the session's metrics on the fly: user_ids (distinct), trace_count (count), duration (latest−earliest), session_total_cost (sum). These aggregates aren't pre-stored — avoiding a sync update per trace. On ingestion only a tiny stub goes into Postgres trace_sessions (id/project/environment + metadata like bookmarked/public), registering the session's existence but storing no metrics.",
                },
            },
            {
                "q": {
                    "zh": "把 session 的「指标」靠 GROUP BY 现算、而不是预先算好存进一张表，最大的好处是？",
                    "en": "Computing a session's metrics on the fly by GROUP BY rather than pre-computing them into a table — the biggest benefit?",
                },
                "opts": [
                    {
                        "zh": "指标永远和底层 traces 一致 + 零额外聚合写入：新来一条带某 session_id 的 trace 自动被算进那个会话的统计，不需要「更新会话聚合」的同步，也就不会出现「trace 写了、会话计数忘了加」的不一致",
                        "en": "metrics always consistent with the underlying traces + zero extra aggregate writes: a new trace with some session_id is automatically counted into that session's stats, no 'update the session aggregates' sync, so no 'trace written but session count forgotten' inconsistency",
                    },
                    {"zh": "让 session 查询更快", "en": "makes session queries faster"},
                    {"zh": "节省 trace 的存储空间", "en": "saves trace storage space"},
                    {"zh": "让 session 能被单独删除", "en": "lets sessions be deleted independently"},
                ],
                "answer": 0,
                "why": {
                    "zh": "现算的聚合天然和底层一致：会话指标从 traces 现场 GROUP BY 得出，新 trace 自动算入，无需同步聚合值，杜绝了「双写不一致」bug。若反过来把每个会话的计数/成本/时长预存进表，每条 trace 都要更新它——多一条写入链路、多一份要操心同步的状态。会话仍会落一个轻量元数据存根（trace_sessions），但昂贵的聚合一律现算、不预存。",
                    "en": "On-the-fly aggregates are inherently consistent with the underlying data: session metrics come from a live GROUP BY over traces, a new trace is auto-counted, no aggregate to sync, eliminating 'dual-write inconsistency' bugs. Conversely pre-storing each session's count/cost/duration makes every trace update it — an extra write path and state to sync. A lightweight metadata stub (trace_sessions) is still persisted, but the expensive aggregates are always computed, never pre-stored.",
                },
            },
            {
                "q": {
                    "zh": "sessions-ui-table-service 的 getSessionsTableGeneric 和第 24 课 traces 的 getTracesTableGeneric「几乎一个模子」（同样四形状、同样紧凑行 vs 指标拆分）。这说明了什么设计价值？",
                    "en": "getSessionsTableGeneric mirrors Lesson 24's getTracesTableGeneric (same four shapes, same compact-rows-vs-metrics split). What design value does this show?",
                },
                "opts": [
                    {
                        "zh": "把表格系统做成「实体无关的通用件」：会话表白白继承第 24 课的分页、回看窗、按需聚合、URL 状态等全部能力，一行新代码不用写；再来一个「按某维度聚合的列表」也能套同一模子",
                        "en": "making the table system an 'entity-agnostic generic part': the sessions table inherits all of Lesson 24's pagination, look-back windows, on-demand aggregation, URL state etc. without a line of new code; any new 'list aggregated by some dimension' fits the same mold",
                    },
                    {"zh": "说明代码重复、应该合并", "en": "it shows duplicated code that should be merged"},
                    {"zh": "说明 session 和 trace 是同一种东西", "en": "it shows sessions and traces are the same thing"},
                    {"zh": "纯属巧合", "en": "pure coincidence"},
                ],
                "answer": 0,
                "why": {
                    "zh": "把通用表格机制（四形状、紧凑行 vs 指标、按需聚合、URL 状态、列预设）抽象成实体无关的通用件后，会话表只需提供「按 session_id 分组」的查询，就免费获得全部性能与体验。这就是正交设计的红利：一个看似实在的新功能，本质是一句 GROUP BY + 复用已有机制。",
                    "en": "Abstracting the generic table machinery (four shapes, compact-vs-metrics, on-demand aggregation, URL state, column presets) into an entity-agnostic part means the sessions table only supplies a 'GROUP BY session_id' query to get all the performance and UX free. The dividend of orthogonal design: a seemingly substantial feature is essentially one GROUP BY plus reusing existing machinery.",
                },
            },
        ],
        "open": [
            {
                "zh": "「能从已有数据现算的，就别再单独存一份」——session 用 GROUP BY 从 traces 派生，省掉了一套写入与同步。你做过的系统里，有没有「为了方便而冗余存了一份、结果要操心同步一致性」的地方？哪些适合改成派生视图？派生的代价（每次查都要现算）你怎么权衡？",
                "en": "'What you can compute from existing data, don't store again' — sessions derive from traces by GROUP BY, sparing a write-and-sync path. In your systems, is there a place where 'you stored a redundant copy for convenience and then had to worry about sync consistency'? Which would suit a derived view? How do you weigh the cost of deriving (computing on every query)?",
            },
        ],
    },
    "27-public-rest-api.html": {
        "mcq": [
            {
                "q": {
                    "zh": "公共 REST API 用一个路由工厂 createAuthedProjectAPIRoute 统一所有端点。和第 21 课 tRPC 的 procedure 构建器相比，它额外多了哪些「面向公众」的关卡？",
                    "en": "The public REST API unifies all endpoints with one route factory createAuthedProjectAPIRoute. Compared to Lesson 21's tRPC procedure builders, what 'public-facing' gates does it add?",
                },
                "opts": [
                    {
                        "zh": "限流（防外部滥用）、响应校验（防对外契约漂移）、访问级别（如 Bearer 只读 score）——都是对内 tRPC 不需要、对外才必须的关卡",
                        "en": "rate limiting (against external abuse), response validation (against external contract drift), access levels (e.g. Bearer read-only scores) — gates the internal tRPC doesn't need but the external API must have",
                    },
                    {"zh": "更复杂的类型检查", "en": "more complex type checking"},
                    {"zh": "更快的数据库连接", "en": "faster database connections"},
                    {"zh": "去掉了鉴权", "en": "it removes auth"},
                ],
                "answer": 0,
                "why": {
                    "zh": "两套都用「工厂/构建器把横切关注收敛到一处」的同一模式，但优先级不同：tRPC 对内求速度，REST 对外求稳定与扛量，故多了限流、响应校验、访问级别。鉴权、Zod 校验则是两者共有——都不靠端点作者自觉，由工厂强制跑。",
                    "en": "Both use the same 'factory/builder converges cross-cutting concerns' pattern, but with different priorities: tRPC seeks internal speed, REST external stability and scale, hence the added rate-limit, response validation, access levels. Auth and Zod validation are common to both — neither relies on endpoint-author diligence; the factory forces them.",
                },
            },
            {
                "q": {
                    "zh": "对外 API 每个请求都要验 key，SDK 可能每秒上万条。Langfuse 的鉴权除了用 Redis 缓存命中的 key，还特意「负缓存」不存在的 key。负缓存防的是什么？",
                    "en": "An external API verifies a key per request, and SDKs may send tens of thousands per second. Besides caching valid keys in Redis, Langfuse deliberately 'negatively caches' nonexistent keys. What does negative caching prevent?",
                },
                "opts": [
                    {
                        "zh": "暴力打库：攻击者拿大量假 key 来刷，若不缓存「不存在」，每个假 key 都会回 Postgres 查一遍；负缓存（API_KEY_NON_EXISTENT）让第二次起就被 Redis 挡回，保护数据库",
                        "en": "brute-forcing the DB: attackers flood with many fake keys; without caching 'nonexistent', each fake key would hit Postgres; negative caching (API_KEY_NON_EXISTENT) blocks them at Redis from the 2nd hit, shielding the database",
                    },
                    {"zh": "防止 key 泄露", "en": "prevents key leakage"},
                    {"zh": "防止响应太大", "en": "prevents oversized responses"},
                    {"zh": "防止版本不一致", "en": "prevents version mismatch"},
                ],
                "answer": 0,
                "why": {
                    "zh": "只缓存有效 key 时，攻击者用海量不存在的 key 仍能让每次都穿透到 Postgres。负缓存把「这个 key 不存在」也记进 Redis，于是无论正常流量还是恶意刷量，数据库都被保护在缓存后面，只在真正缓存未命中时才被惊动。这是「缓存正例也缓存反例」的安全考量。",
                    "en": "Caching only valid keys still lets attackers with floods of nonexistent keys punch through to Postgres each time. Negative caching records 'this key doesn't exist' in Redis too, so whether normal traffic or malicious flooding, the DB stays shielded behind the cache, disturbed only on a true miss. A 'cache the positives and the negatives' security consideration.",
                },
            },
            {
                "q": {
                    "zh": "Langfuse 用「文件夹做版本」（v1 在根、v2/、v3/）+「Fern 契约生成 SDK」来管理对外 API。这套组合解决的核心矛盾是？",
                    "en": "Langfuse manages the external API with 'versioning by folder' (v1 at root, v2/, v3/) + 'Fern contract generates SDKs'. What core tension does this combo resolve?",
                },
                "opts": [
                    {
                        "zh": "「需求要演进」与「发布后不能破坏老用户」的矛盾：文件夹版本让老路径永不改（旧集成照跑）、新版可显式切换甚至做减法；Fern 一份契约生成多语言 SDK、保证一致，开发期响应校验防实现与契约漂移",
                        "en": "the tension between 'needs evolve' and 'can't break existing users after release': folder versions keep old paths unchanged (old integrations run) while new versions opt-in and can even subtract; Fern's one contract generates multi-language SDKs ensuring consistency, with dev-time response validation against drift",
                    },
                    {"zh": "让 API 响应更快", "en": "makes API responses faster"},
                    {"zh": "减少端点数量", "en": "reduces the number of endpoints"},
                    {"zh": "让前端不用写代码", "en": "lets the frontend skip code"},
                ],
                "answer": 0,
                "why": {
                    "zh": "对外契约一旦发布就不能随意改，但需求总在变。文件夹版本让 v1 永不破、新能力进 v2/v3（甚至砍掉昂贵旧设计，如 v3 scores 去掉需 JOIN 的过滤、改游标分页）；Fern 用一份手写 YAML 生成 Python/TS SDK + OpenAPI，一处定义处处一致。这正是第 20 课「对外求契约稳定」的落地。",
                    "en": "An external contract can't change freely once published, yet needs keep evolving. Folder versions keep v1 unbroken and put new capability in v2/v3 (even cutting costly old designs, e.g. v3 scores dropping JOIN-needing filters for cursor pagination); Fern generates Python/TS SDKs + OpenAPI from one hand-written YAML, define-once consistent everywhere. This realizes Lesson 20's 'externally seek contract stability'.",
                },
            },
        ],
        "open": [
            {
                "zh": "「对内优化『改得快』、对外优化『不破坏』」——同一份数据，UI 用 tRPC、SDK 用版本化 REST。你做过或用过的系统里，内部接口和对外 API 是怎么处理这对矛盾的？如果让你给一个对外 API 设计「演进而不破坏」的机制，你会怎么做版本、怎么防契约漂移？",
                "en": "'Internally optimize fast-to-change, externally optimize don't-break' — same data, UI via tRPC, SDK via versioned REST. In systems you've built or used, how were internal interfaces and external APIs handled against this tension? Designing an 'evolve without breaking' mechanism for an external API, how would you do versioning and prevent contract drift?",
            },
        ],
    },
    "28-scoring-model.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的 score 有三种 dataType：NUMERIC、CATEGORICAL、BOOLEAN。但源码里 BOOLEAN 并不是「独立的第四套逻辑」，而是被实现成什么？",
                    "en": "A Langfuse score has three dataTypes: NUMERIC, CATEGORICAL, BOOLEAN. But in the source, BOOLEAN is not an 'independent fourth logic' — what is it implemented as?",
                },
                "opts": [
                    {
                        "zh": "一个「恰好两档、且锁死为 True=1 / False=0」的特殊 CATEGORICAL——底层只需处理数值与分类两套逻辑，布尔复用分类的存储与聚合",
                        "en": "a special CATEGORICAL with 'exactly two categories, locked to True=1 / False=0' — the core only handles numeric and categorical, and boolean reuses categorical storage and aggregation",
                    },
                    {"zh": "一个独立的布尔表", "en": "a separate boolean table"},
                    {"zh": "一个 NUMERIC 的别名", "en": "an alias of NUMERIC"},
                    {"zh": "一段前端专用的校验", "en": "a frontend-only validation"},
                ],
                "answer": 0,
                "why": {
                    "zh": "BooleanConfigFields 强制 categories 长度为 2、且锁死 {True:1, False:0}（score-configs.ts）。这样就不必为布尔新造一套存储/聚合，它顺着分类的路走——少一套特例、多一分一致。这正呼应第 8 课「能用通用机制表达的，就别新造一个」。",
                    "en": "BooleanConfigFields forces categories length 2, locked to {True:1, False:0} (score-configs.ts). So boolean needs no new storage/aggregation; it rides the categorical path — one fewer special case, more consistency. This echoes Lesson 8's 'if a general mechanism expresses it, don't invent a new one'.",
                },
            },
            {
                "q": {
                    "zh": "「有用性」这个分数，A 团队打 0–1、B 团队用百分制、C 用「好/差」。score config 要解决的核心问题是？",
                    "en": "For the score 'helpfulness', team A rates 0–1, team B uses a percentage, C uses 'good/bad'. What core problem does a score config solve?",
                },
                "opts": [
                    {
                        "zh": "可比性：config 是某个 name 的 schema，把「这个名字=这种刻度」固定并强制校验，于是同名分数永远同一把尺——求平均、画趋势、做对比才有意义",
                        "en": "comparability: a config is the schema of a name, fixing and enforcing 'this name = this scale', so same-named scores always use one ruler — only then are averaging, trending, and comparison meaningful",
                    },
                    {"zh": "让打分速度更快", "en": "makes scoring faster"},
                    {"zh": "减少数据库存储", "en": "reduces database storage"},
                    {"zh": "自动生成分数", "en": "auto-generates scores"},
                ],
                "answer": 0,
                "why": {
                    "zh": "「能比较」是评估的全部价值。若同名分数刻度各异，放一起求平均/画趋势/对比全是错的。score config 显式声明 dataType 与约束（区间/类别）并前置校验，使同名分数恒可比。这和第 8 课 provided/computed、第 16 课定价 schema 是同一种「把数据该长什么样显式建模」的工程信念。",
                    "en": "'Being comparable' is the whole value of evaluation. If same-named scores use different scales, averaging/trending/comparing them is all wrong. A score config explicitly declares dataType and constraints (bounds/categories) and validates up front, keeping same-named scores forever comparable. Same belief as Lesson 8's provided/computed and Lesson 16's pricing schema: model 'what the data should look like' explicitly.",
                },
            },
            {
                "q": {
                    "zh": "score 有三种 source：API、EVAL、ANNOTATION（scores.ts 的 ScoreSourceArray）。关于这三者的关系，下列哪句最准确？",
                    "en": "A score has three sources: API, EVAL, ANNOTATION (ScoreSourceArray in scores.ts). Which statement about them is most accurate?",
                },
                "opts": [
                    {
                        "zh": "三者殊途同归：AI 评判(EVAL)、人工标注(ANNOTATION)、亲手提交(API)最终都按同一 config 校验、写进同一张 scores 表——评估不是独立管道，而是 score 的生产者",
                        "en": "all three converge: AI judging (EVAL), human annotation (ANNOTATION), and direct submission (API) are all validated by the same config and written to the same scores table — evaluation isn't a separate pipeline but a producer of scores",
                    },
                    {"zh": "三种 source 各有独立的表和聚合逻辑", "en": "each source has its own table and aggregation logic"},
                    {"zh": "只有 API 来源会被存储", "en": "only the API source gets stored"},
                    {"zh": "EVAL 分数不经过摄取链路", "en": "EVAL scores bypass the ingestion path"},
                ],
                "answer": 0,
                "why": {
                    "zh": "ScoreSourceArray=[\"API\",\"EVAL\",\"ANNOTATION\"] 只是给同一张 scores 表的一行标注「这分谁打的」。LLM-as-a-judge、代码 eval、人工标注算出的分都走回同一条摄取链路、按同一 config 校验。这就是 Part 5 后续每课的共同终点：用不同方式生产可比的 score。",
                    "en": "ScoreSourceArray=[\"API\",\"EVAL\",\"ANNOTATION\"] merely labels a row in the same scores table with 'who scored this'. Scores from LLM-as-a-judge, code eval, and human annotation all flow back through the same ingestion path, validated by the same config. This is the shared destination of every remaining Part 5 lesson: producing comparable scores in different ways.",
                },
            },
        ],
        "open": [
            {
                "zh": "Langfuse 把「AI 评的、人审的、API 报的」分数统一成一种 score、一张表、一套 config，只用 source 字段区分来源。在你做过或设想的系统里，如果要把「多种来源的质量信号」统一成一个可比的指标，你会怎么设计它的数据模型？需要一个像 score config 那样的「schema 守门人」吗，为什么？",
                "en": "Langfuse unifies 'AI-judged, human-reviewed, API-reported' scores into one score type, one table, one config, distinguishing origin only by a source field. In a system you've built or imagined, if you had to unify 'quality signals from many sources' into one comparable metric, how would you design its data model? Would you want a 'schema gatekeeper' like a score config — and why?",
            },
        ],
    },
    "29-llm-as-a-judge.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的 LLM-as-a-judge 强制裁判 LLM 用「结构化输出」返回 {score, reasoning}，而不是让它自由写一段评语。这么做的核心原因是？",
                    "en": "Langfuse's LLM-as-a-judge forces the judge LLM to return {score, reasoning} via 'structured output' rather than free prose. The core reason is?",
                },
                "opts": [
                    {
                        "zh": "评估的产物要能录入、聚合、比较：分必须能进 scores 表跨千条 trace 求平均，理由留在 comment 里可追溯——散文两样都做不到",
                        "en": "the product of evaluation must be recordable, aggregatable, comparable: the score must enter the scores table to average across thousands of traces, with the reasoning kept in comment for traceability — prose does neither",
                    },
                    {"zh": "结构化输出让 LLM 调用更便宜", "en": "structured output makes the LLM call cheaper"},
                    {"zh": "可以不调用 LLM", "en": "it avoids calling the LLM"},
                    {"zh": "让裁判模型必须用 GPT-4", "en": "it forces the judge to use GPT-4"},
                ],
                "answer": 0,
                "why": {
                    "zh": "若裁判回一段散文，既没法可靠抽出一个数值分、也没法跨大量 trace 聚合。强制 {score, reasoning} 的 schema 让 value 进 scores 表（可聚合）、reasoning 进 comment（可追溯），两全。toNormalizedScores 正是据此把输出归一成 score（value=分，comment=理由）。",
                    "en": "If the judge returns prose, you can't reliably extract a numeric score nor aggregate across many traces. Forcing a {score, reasoning} schema puts value into the scores table (aggregatable) and reasoning into comment (traceable) — both at once. toNormalizedScores normalizes the output into a score exactly this way (value=score, comment=reasoning).",
                },
            },
            {
                "q": {
                    "zh": "裁判 LLM 评出的分，最终是怎么变成数据库里一条可查询的 score 的？",
                    "en": "How does the judge LLM's verdict ultimately become a queryable score in the database?",
                },
                "opts": [
                    {
                        "zh": "包成 source=EVAL 的 SCORE_CREATE 事件，走第 12 课那条和手写 score 完全相同的摄取链路——评估是摄取管道的又一个生产者，不是独立系统",
                        "en": "wrapped as a source=EVAL SCORE_CREATE event through the exact same Lesson-12 ingestion path as a hand-written score — evaluation is another producer for the ingestion pipeline, not a separate system",
                    },
                    {"zh": "直接 INSERT 进 ClickHouse，绕过摄取链路", "en": "directly INSERTed into ClickHouse, bypassing ingestion"},
                    {"zh": "存进一张专门的 eval 结果表", "en": "stored in a dedicated eval-results table"},
                    {"zh": "只存在内存里供仪表盘读取", "en": "kept in memory only for dashboards"},
                ],
                "answer": 0,
                "why": {
                    "zh": "evalScoreEvent.ts 把归一后的结果包成 eventTypes.SCORE_CREATE、标 source=ScoreSourceEnum.EVAL，再走摄取链路。于是去重、合并、落 ClickHouse 的逻辑只写一遍、对 API/EVAL/ANNOTATION 三来源一致。这正是「一个入口，多个生产者」的体现，也让裁判分天然与其它来源同表可比。",
                    "en": "evalScoreEvent.ts wraps the normalized result as eventTypes.SCORE_CREATE tagged source=ScoreSourceEnum.EVAL, then runs the ingestion path. So dedup/merge/ClickHouse-persist are written once and consistent across API/EVAL/ANNOTATION. This is 'one entry, many producers', and makes judge scores inherently comparable in the same table.",
                },
            },
            {
                "q": {
                    "zh": "模板里写的是 {{question}}、{{answer}} 这样的占位符。执行时它们怎么变成真实内容？",
                    "en": "The template holds placeholders like {{question}}, {{answer}}. How do they become real content at execution?",
                },
                "opts": [
                    {
                        "zh": "靠变量映射：每个模板变量声明来自 trace/observation/dataset_item 的哪一列，extractVariablesFromTracingData 去真实数据取值，compileEvalPrompt 再填进占位符",
                        "en": "via variable mapping: each template variable declares which column of trace/observation/dataset_item it comes from; extractVariablesFromTracingData fetches real values, then compileEvalPrompt fills the placeholders",
                    },
                    {"zh": "裁判 LLM 自己去数据库查", "en": "the judge LLM queries the database itself"},
                    {"zh": "用固定的示例数据", "en": "with fixed sample data"},
                    {"zh": "前端把内容硬编码进模板", "en": "the frontend hardcodes content into the template"},
                ],
                "answer": 0,
                "why": {
                    "zh": "每条映射是 {templateVariable, langfuseObject, selectedColumnId}。执行时按映射从真实 trace/observation/dataset_item 取那一列的值，得到 {var, value}；compileEvalPrompt 在「喂给 LLM」的边界用 parseUnknownToString 拍平成字符串再填进 {{占位符}}。提取阶段保留原始形状（给代码 eval 用），只在边界处转换。",
                    "en": "Each mapping is {templateVariable, langfuseObject, selectedColumnId}. At run it pulls that column's value from the real trace/observation/dataset_item into {var, value}; compileEvalPrompt flattens to a string via parseUnknownToString at the 'feed-to-LLM' boundary before filling {{placeholders}}. Extraction keeps original shapes (for code eval), converting only at the boundary.",
                },
            },
        ],
        "open": [
            {
                "zh": "LLM-as-a-judge 用一个 LLM 评判另一个 LLM——但裁判自己也会犯错、也有偏好。你会怎么验证「裁判本身是否可靠」？（提示：Langfuse 把裁判的每次调用也记成一条 trace，且评出的分能和人工标注的分同表比较。）这对「用 AI 评 AI」的可信度建设意味着什么？",
                "en": "LLM-as-a-judge uses one LLM to judge another — but the judge itself errs and has biases. How would you validate 'whether the judge itself is reliable'? (Hint: Langfuse records each judge call as a trace, and judge scores sit in the same table as human-annotation scores for comparison.) What does this imply for building trust in 'AI judging AI'?",
            },
        ],
    },
    "30-eval-execution-pipeline.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的评估调度把工作拆成「创建」和「执行」两级队列。这种分离最核心的好处是？",
                    "en": "Langfuse's eval scheduling splits work into 'creation' and 'execution' two-stage queues. The core benefit of this separation is?",
                },
                "opts": [
                    {
                        "zh": "两件事性质不同：创建是轻快的纯数据库匹配，执行是慢、花钱、会限流的 LLM 调用——分开后各自独立扩容、采样、重试，慢的不拖死快的",
                        "en": "the two differ in nature: creation is light pure-DB matching, execution is slow, costly, rate-limited LLM calls — split apart they scale/sample/retry independently, and the slow doesn't drag down the fast",
                    },
                    {"zh": "让评估结果更准确", "en": "makes eval results more accurate"},
                    {"zh": "减少数据库表的数量", "en": "reduces the number of DB tables"},
                    {"zh": "省掉 LLM 调用", "en": "avoids the LLM call"},
                ],
                "answer": 0,
                "why": {
                    "zh": "创建（匹配、去重、采样）轻快、失败重跑代价小；执行（调 LLM）慢、贵、会被限流、可能超时。混在一起则慢拖快、贵的没法单独采样、失败没法独立重试。两级队列让第一级高吞吐决定「该评谁」，第二级带延迟/采样/重试/分流地慢慢消化——正是第 14 课「队列解耦」在评估域的复刻。",
                    "en": "Creation (match, dedup, sample) is light and cheap to re-run; execution (LLM call) is slow, costly, rate-limited, may time out. Mixed, the slow drags the fast, the costly can't be sampled alone, failures can't retry independently. Two-stage queues let stage one decide 'whom' at high throughput and stage two digest slowly with delay/sampling/retry/offload — Lesson 14's queue decoupling in the eval domain.",
                },
            },
            {
                "q": {
                    "zh": "评估本身要调 LLM，而 Langfuse 会把每次 LLM 调用记成一条 trace。createEvalJobs 里有一段「如果 trace 环境以 langfuse 开头就直接 return」的代码。它防的是什么？",
                    "en": "Evaluation calls the LLM, and Langfuse records each LLM call as a trace. createEvalJobs has code that 'returns immediately if the trace environment starts with langfuse'. What does it prevent?",
                },
                "opts": [
                    {
                        "zh": "无限循环：用户 trace 触发评估 → 评估的 LLM 调用又成一条 trace → 又触发评估 → 无限套娃；给内部 trace 打 langfuse- 前缀并在入口挡掉即可斩断",
                        "en": "an infinite loop: a user trace triggers eval → the eval's LLM call becomes a trace → triggers eval again → nesting forever; tagging internal traces with a langfuse- prefix and blocking them at the entry breaks the cycle",
                    },
                    {"zh": "防止内部 trace 被用户看到", "en": "hides internal traces from users"},
                    {"zh": "加快内部 trace 的写入", "en": "speeds up writing internal traces"},
                    {"zh": "防止重复计费", "en": "prevents double billing"},
                ],
                "answer": 0,
                "why": {
                    "zh": "这是自指系统的经典陷阱：一个能观测一切的系统，会把自己的评估调用也观测成 trace，从而触发对自己的评估。Langfuse 让内部 trace 用 LangfuseInternalTraceEnvironment（langfuse- 前缀），并在 createEvalJobs 入口对 trace-upsert 来源的这类 trace 直接 return，斩断递归。fetchLLMCompletion 还强制内部 trace 必须带该前缀，形成双重保险。",
                    "en": "A classic self-reference trap: a system that observes everything observes its own eval call as a trace, triggering eval on itself. Langfuse marks internal traces with LangfuseInternalTraceEnvironment (langfuse- prefix) and returns early at createEvalJobs for such trace-upsert-sourced traces, cutting the recursion. fetchLLMCompletion also enforces that internal traces carry the prefix — a dual safeguard.",
                },
            },
            {
                "q": {
                    "zh": "一行 JobExecution 落在 Postgres 里，而不只是一条「阅后即焚」的队列消息。为什么评估系统需要这样一个有状态、可更新的工单？",
                    "en": "A JobExecution row lives in Postgres, not just a 'read-once' queue message. Why does the eval system need such a stateful, updatable ticket?",
                },
                "opts": [
                    {
                        "zh": "它要支持去重、取消、追溯：能回答「这条 trace 被哪些评估器评过、成功没、产出哪条分」，并通过 jobOutputScoreId/executionTraceId 双向链到产出的分与裁判自己的 trace",
                        "en": "it must support dedup, cancellation, and audit: answering 'which evaluators evaluated this trace, did it succeed, which score did it produce', and via jobOutputScoreId/executionTraceId bidirectionally linking to the produced score and the judge's own trace",
                    },
                    {"zh": "Postgres 比队列快", "en": "Postgres is faster than a queue"},
                    {"zh": "为了不用 Redis", "en": "to avoid using Redis"},
                    {"zh": "队列不能存 JSON", "en": "queues can't store JSON"},
                ],
                "answer": 0,
                "why": {
                    "zh": "队列消息消费即逝，无法回答「评过没、结果如何」。JobExecution 是落库的状态机（PENDING→COMPLETED/ERROR/CANCELLED/DELAYED），支持：去重（已有工单就不重复建）、取消（trace 被后续事件踢出目标集合则标 CANCELLED）、追溯（jobOutputScoreId 链到评出的分、executionTraceId 链到裁判的 trace），全链路可审计。",
                    "en": "A queue message is gone on consume, unable to answer 'evaluated yet, what outcome'. JobExecution is a persisted state machine (PENDING→COMPLETED/ERROR/CANCELLED/DELAYED) supporting: dedup (don't recreate an existing ticket), cancel (mark CANCELLED if a later event kicks the trace out of the target set), and audit (jobOutputScoreId links to the score, executionTraceId links to the judge's trace) — auditable end to end.",
                },
            },
        ],
        "open": [
            {
                "zh": "评估系统给了三道闸：去重、采样、延迟。假设你的生产流量每天一百万条 trace，每条评估要调一次 GPT-4 花约 ¥0.05。你会怎么配置这三道闸（采样率、延迟）来平衡「成本」与「质量信号的及时性/代表性」？延迟设太短、采样设太低分别会带来什么问题？",
                "en": "The eval system offers three gates: dedup, sampling, delay. Suppose your production handles a million traces/day, each eval calling GPT-4 at ~$0.007. How would you configure these gates (sample rate, delay) to balance 'cost' against 'timeliness/representativeness of the quality signal'? What problems arise from setting delay too short or sampling too low?",
            },
        ],
    },
    "31-code-based-evaluation.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 同时有 LLM-as-judge（第 29 课）和代码 eval（本课）两种评估。下面哪种说法最准确地刻画了它们的关系？",
                    "en": "Langfuse has both LLM-as-judge (Lesson 29) and code eval (this lesson). Which statement most accurately characterizes their relationship?",
                },
                "opts": [
                    {
                        "zh": "互补：代码 eval 确定、适合客观/规则信号（合法 JSON、含 PII、长度）；LLM-as-judge 概率、适合主观/语义信号（有用性、语气）。两者都接同一条调度流水线，只是「执行」步不同",
                        "en": "complementary: code eval is deterministic, for objective/rule signals (valid JSON, has PII, length); LLM-as-judge is probabilistic, for subjective/semantic signals (helpfulness, tone). Both attach to the same scheduling pipeline, differing only at the 'execution' step",
                    },
                    {"zh": "代码 eval 是 LLM-as-judge 的升级替代品", "en": "code eval is an upgraded replacement for LLM-as-judge"},
                    {"zh": "两者用完全独立的调度与存储", "en": "they use entirely separate scheduling and storage"},
                    {"zh": "代码 eval 只能产出布尔分", "en": "code eval can only produce boolean scores"},
                ],
                "answer": 0,
                "why": {
                    "zh": "两者是同一个 score 的两种生产方式，都挂在第 30 课调度流水线后，区别只在「执行」那一步：LLM-as-judge 调模型、代码 eval 跑函数。结果都归一成 source=EVAL 的 score 回流同一张表、走同一个 JobExecution 状态机。能用规则说清的交给代码 eval（确定、免费），要语义理解的交给 LLM-as-judge。",
                    "en": "Both are two ways of producing the same score, hanging off Lesson 30's pipeline, differing only at the 'execution' step: LLM-as-judge calls a model, code eval runs a function. Both normalize into source=EVAL scores flowing into the same table via the same JobExecution state machine. Rule-expressible goes to code eval (deterministic, free); semantic goes to LLM-as-judge.",
                },
            },
            {
                "q": {
                    "zh": "代码 eval 要执行用户写的代码。Langfuse 的本地派发器在源码里直接命名为 \"insecure-local\"。这个命名透露了什么？",
                    "en": "Code eval executes user-written code. Langfuse's local dispatcher is named \"insecure-local\" right in the source. What does this naming reveal?",
                },
                "opts": [
                    {
                        "zh": "诚实的警告：它用 node 的 vm 模块，而 vm 不是真正的安全沙箱（可被逃逸）；命名即文档，明示这条路只配本地开发，生产要用 Lambda 那种真隔离",
                        "en": "an honest warning: it uses node's vm module, and vm is not a real security sandbox (escapable); naming as documentation, signaling this path is for local dev only, with production needing real isolation like Lambda",
                    },
                    {"zh": "本地运行速度慢", "en": "local execution is slow"},
                    {"zh": "本地只支持 Python", "en": "local only supports Python"},
                    {"zh": "它会泄露环境变量", "en": "it leaks environment variables"},
                ],
                "answer": 0,
                "why": {
                    "zh": "node 的 vm 模块能创建隔离 context 跑代码，但业界共识是它不足以安全运行不可信代码（有已知逃逸手法）。Langfuse 不粉饰，把 insecure 写进 dispatcher 的 name，相当于在源码里贴警告条：本地开发可用，生产请切到 AwsLambdaCodeEvalDispatcher（ephemeral、强隔离、按语言调 python/node 函数）。",
                    "en": "Node's vm can create an isolated context to run code, but the consensus is it's insufficient for safely running untrusted code (known escapes exist). Langfuse doesn't gloss over it—writing insecure into the dispatcher's name is a source-level warning: fine for local dev, switch to AwsLambdaCodeEvalDispatcher (ephemeral, strong isolation, per-language python/node functions) in production.",
                },
            },
            {
                "q": {
                    "zh": "代码 eval 的沙箱有一条铁律：评估器代码不准发任何网络请求。为什么这条「禁网络」被认为一箭双雕？",
                    "en": "The code-eval sandbox has an iron rule: evaluator code may make no network requests. Why is this 'no network' considered to kill two birds?",
                },
                "opts": [
                    {
                        "zh": "既保安全（用户代码联网就能外泄你递进去的 trace 数据、或拿沙箱打内网 SSRF），又保确定性（网络天生不确定、会抖会超时甚至可能永不返回，破坏「同输入恒同分」）",
                        "en": "it preserves security (networked user code could exfiltrate the trace data you fed it, or use the sandbox for SSRF into your internal network) and determinism (network is inherently nondeterministic—flaky, timing out, even may-never-return, breaking 'same input, same score')",
                    },
                    {"zh": "只是为了省带宽", "en": "just to save bandwidth"},
                    {"zh": "让评估跑得更快", "en": "to make eval run faster"},
                    {"zh": "防止评估器调用 LLM", "en": "to stop the evaluator from calling an LLM"},
                ],
                "answer": 0,
                "why": {
                    "zh": "安全上：一旦能联网，用户代码可把含敏感信息的 trace 数据偷传出去，或以沙箱为跳板访问内网服务（SSRF）。确定性上：评估的灵魂是「同输入恒同分」，而网络请求会抖、超时、返回不同结果，源码原话甚至说「可能永不返回」。掐断网络同时焊死了安全口子和不确定性源头——一条约束，两重收益。",
                    "en": "Security: once networked, user code can smuggle out sensitive trace data or use the sandbox as a springboard to internal services (SSRF). Determinism: the soul of eval is 'same input, same score', yet network requests flake, time out, return different results—the source even says 'may never return'. Cutting the network welds shut both the security hole and the nondeterminism source — one constraint, two payoffs.",
                },
            },
        ],
        "open": [
            {
                "zh": "想象你要给一个客服机器人写 5 个评估器。哪些你会用代码 eval（确定/规则），哪些用 LLM-as-judge（概率/语义）？请各举几个，并说说为什么——以及如果某个信号「看起来客观但其实有灰区」（比如「回答是否礼貌」），你会怎么权衡？",
                "en": "Imagine writing 5 evaluators for a customer-service bot. Which would you do with code eval (deterministic/rule) and which with LLM-as-judge (probabilistic/semantic)? Give a few of each and say why—and if a signal 'looks objective but has a gray zone' (e.g. 'is the reply polite'), how would you weigh it?",
            },
        ],
    },
    "32-human-annotation.html": {
        "mcq": [
            {
                "q": {
                    "zh": "人工标注是第 28 课三种 score 来源里的 ANNOTATION。除了「人比机器更准」，它在评估体系里还扮演一个独特角色，是什么？",
                    "en": "Human annotation is the ANNOTATION of Lesson 28's three score sources. Beyond 'humans are more accurate than machines', it plays a unique role in the evaluation system. What is it?",
                },
                "opts": [
                    {
                        "zh": "充当 ground truth / 校准 AI 裁判：把人评的「金标准」和 AI 裁判分放在同一批 trace 上对照，量出裁判哪里偏了——这正是第 29 课「怎么信任 AI 裁判」的答案",
                        "en": "serving as ground truth / calibrating the AI judge: laying the human 'gold standard' against AI-judge scores on the same traces measures where the judge is biased — the answer to Lesson 29's 'how to trust the AI judge'",
                    },
                    {"zh": "让评估跑得更快", "en": "makes evaluation run faster"},
                    {"zh": "替代 LLM-as-judge", "en": "replaces LLM-as-judge"},
                    {"zh": "降低标注成本", "en": "lowers annotation cost"},
                ],
                "answer": 0,
                "why": {
                    "zh": "人工分又慢又贵，通常只评一小撮关键样本，但这一小撮是衡量 AI 裁判的金标准。因为三来源同表同 config（ScoreSourceArray=[API,EVAL,ANNOTATION]），人评分和 AI 裁判分可在同一批对象上直接对照；不一致处正是裁判要改 prompt/换模型的地方。这把「人工标注当裁判的标尺」，正是评估可信度的基石。",
                    "en": "Human scores are slow and costly, usually only on a small key sample—but that sample is the gold standard for the AI judge. Because the three sources share one table and config (ScoreSourceArray=[API,EVAL,ANNOTATION]), human and AI-judge scores compare directly on the same objects; disagreements are where the judge must fix its prompt/model. Using human annotation as the judge's yardstick is the bedrock of evaluation trust.",
                },
            },
            {
                "q": {
                    "zh": "多个评审员同时盯着一个标注队列。Langfuse 用一个「5 分钟时间软锁」防止两人评到同一份。相比数据库事务锁或永久占用标记，软锁的关键好处是？",
                    "en": "Several reviewers eye one annotation queue at once. Langfuse uses a '5-minute time-based soft lock' to stop two from annotating the same item. Versus a DB transaction lock or a permanent-hold marker, the soft lock's key benefit is?",
                },
                "opts": [
                    {
                        "zh": "匹配人的节奏且永不死锁：5 分钟够看完一份、避免撞车；又因自动过期，关浏览器/断网都只会让锁自愈，绝不会把 item 永久占死",
                        "en": "fits the human rhythm and never deadlocks: 5 minutes suffices to finish one item and avoid collisions; and because it auto-expires, closing the browser/losing network just lets the lock self-heal, never holding an item forever",
                    },
                    {"zh": "比事务锁查询更快", "en": "queries faster than a transaction lock"},
                    {"zh": "能锁住整个队列", "en": "can lock the whole queue"},
                    {"zh": "不需要数据库字段", "en": "needs no database fields"},
                ],
                "answer": 0,
                "why": {
                    "zh": "isItemLocked 只认 lockedAt 在最近 5 分钟内的锁。数据库事务锁是毫秒级、占连接，扛不住人看几分钟；永久标记一旦评审员关页面就把 item 占死。时间软锁两头讨好：5 分钟避免并发撞车，又因自动过期而自愈、永不死锁。这是「乐观并发 + 租约」用在人类工作流上——锁的粒度匹配被锁者的节奏。",
                    "en": "isItemLocked only counts a lock whose lockedAt is within the last 5 minutes. A DB transaction lock is millisecond-scale and ties up a connection, unfit for minutes of human reading; a permanent marker holds the item forever once a reviewer closes the tab. The time-based soft lock pleases both: 5 minutes avoids collisions, and auto-expiry self-heals, never deadlocking. It's 'optimistic concurrency + a lease' applied to a human workflow — lock granularity matching the locked party's rhythm.",
                },
            },
            {
                "q": {
                    "zh": "一个 AnnotationQueue 上绑了一组 scoreConfigIds。这个绑定起什么作用？",
                    "en": "An AnnotationQueue binds a set of scoreConfigIds. What does this binding do?",
                },
                "opts": [
                    {
                        "zh": "它是这个队列的「统一评分表」：规定所有评审员要按同一组 score config 打分（同名同刻度），分数才可比、才能聚合——直接复用第 28 课的 config",
                        "en": "it's the queue's 'uniform scoring sheet': all reviewers must score by the same set of score configs (same name, same scale) so scores are comparable and aggregatable — directly reusing Lesson 28's configs",
                    },
                    {"zh": "决定队列指派给哪些评审员", "en": "decides which reviewers the queue is assigned to"},
                    {"zh": "决定评哪些 trace", "en": "decides which traces to review"},
                    {"zh": "控制 5 分钟锁的时长", "en": "controls the 5-minute lock duration"},
                ],
                "answer": 0,
                "why": {
                    "zh": "scoreConfigIds 绑定第 28 课的 score config，规定这个队列里每位评审员要填哪几项分、每项什么刻度（NUMERIC/CATEGORICAL/BOOLEAN）。统一了尺，不同评审员、不同 item 的分才可比可聚合。指派给谁是另一个模型 AnnotationQueueAssignment 的事，评哪些对象是 AnnotationQueueItem 的事——三者各司其职。",
                    "en": "scoreConfigIds bind Lesson 28's score configs, dictating which scores each reviewer in this queue fills and on what scale (NUMERIC/CATEGORICAL/BOOLEAN). With a unified ruler, scores across reviewers and items are comparable and aggregatable. Who it's assigned to is the separate AnnotationQueueAssignment model; which objects to review is AnnotationQueueItem — each with its own job.",
                },
            },
        ],
        "open": [
            {
                "zh": "Part 5 走到这里，三种 score 来源（API/EVAL/ANNOTATION）全部汇入同一张 scores 表、同一套 config。回头看这条主线：为什么 Langfuse 不为「AI 评的分」和「人评的分」分别建表，而是执意让它们同表同尺？这种「统一数据模型」的设计，在可信度、可维护性、未来扩展上分别带来了什么？你能想到它的代价或局限吗？",
                "en": "By this point in Part 5, all three score sources (API/EVAL/ANNOTATION) flow into one scores table, one set of configs. Looking back at this through-line: why does Langfuse refuse to build separate tables for 'AI-judged' and 'human-judged' scores, insisting on one table and one ruler? What does this 'unified data model' buy in trust, maintainability, and future extension? Can you think of its costs or limits?",
            },
        ],
    },
    "33-monitors-and-alerting.html": {
        "mcq": [
            {
                "q": {
                    "zh": "Langfuse 的 monitor（监控器）和 dashboard（仪表盘）有什么本质关系？",
                    "en": "What is the essential relationship between a Langfuse monitor and a dashboard?",
                },
                "opts": [
                    {
                        "zh": "monitor 复用仪表盘组件的查询形状（view/filters/metric，源码注释 mirrors DashboardWidget），区别在于它由调度器定时算、并拿去比阈值——pull（你看）变 push（它喊）",
                        "en": "a monitor reuses the dashboard widget's query shape (view/filters/metric, the source comment says mirrors DashboardWidget), differing in that a scheduler computes it on a cadence and compares against thresholds — pull (you look) becomes push (it calls you)",
                    },
                    {"zh": "monitor 是 dashboard 的只读快照", "en": "a monitor is a read-only snapshot of a dashboard"},
                    {"zh": "两者用完全不同的查询引擎", "en": "they use entirely different query engines"},
                    {"zh": "dashboard 是 monitor 的告警历史", "en": "a dashboard is a monitor's alert history"},
                ],
                "answer": 0,
                "why": {
                    "zh": "Monitor 的 view/filters/metric 直接 mirror DashboardWidget——能在仪表盘画出的曲线，都能一键变成会自己盯着的告警，底层 ClickHouse 查询机制只写一遍。区别只在 monitor 多了①调度（按 cadenceMs 定时）+③④阈值与状态机。pull 与 push 共享同一个指标定义，既省代码又顺直觉。",
                    "en": "Monitor's view/filters/metric directly mirror DashboardWidget—any curve you can draw on a dashboard becomes a self-watching alert in one click, with the ClickHouse query machinery written once. The difference is only that a monitor adds ① scheduling (per cadenceMs) + ③④ thresholds and a state machine. Pull and push share one metric definition: saves code and matches intuition.",
                },
            },
            {
                "q": {
                    "zh": "一个 monitor 持续处于 ALERT 状态。它每 5 分钟算一次，但并不会每 5 分钟都发一条告警。这种克制由什么实现，解决什么问题？",
                    "en": "A monitor stays in ALERT. It computes every 5 minutes but does not send an alert every 5 minutes. What implements this restraint, and what problem does it solve?",
                },
                "opts": [
                    {
                        "zh": "applyStateMachine：原则上只在严重度「变化」时 emit（OK→ALERT 发、ALERT→ALERT 不发），持续异常按 renotify 周期补发——根治告警疲劳",
                        "en": "applyStateMachine: as a rule emit only on a severity 'change' (OK→ALERT sends, ALERT→ALERT doesn't), topping up persistent anomalies per the renotify period — curing alert fatigue",
                    },
                    {"zh": "每次都发，靠 Slack 自己去重", "en": "it sends every time, relying on Slack to dedupe"},
                    {"zh": "随机丢弃一部分告警", "en": "it randomly drops some alerts"},
                    {"zh": "只在工作时间发", "en": "it only sends during work hours"},
                ],
                "answer": 0,
                "why": {
                    "zh": "告警疲劳是监控系统头号杀手：持续 ALERT 每 5 分钟一条，工程师会把频道静音，真问题也被淹没。applyStateMachine 对比 prev/next 严重度，severityChanged 才考虑 emit，并按 renotify 决定是否补发；PAUSED 直接跳过不覆盖用户意图。把 severity 做成状态机而非瞬时值，正是为了能问「和上次比变了吗」。",
                    "en": "Alert fatigue is a monitoring system's top killer: a persistent ALERT pinging every 5 minutes makes engineers mute the channel and bury real issues. applyStateMachine compares prev/next severity, considering emit only when severityChanged, and tops up per renotify; PAUSED is skipped to not overwrite user intent. Making severity a state machine rather than an instantaneous value is exactly to ask 'did it change from last time'.",
                },
            },
            {
                "q": {
                    "zh": "monitor 判定要告警后，并不直接调 Slack API，而是把告警发布到 WebhookQueue，再由自动化系统转投递。为什么这样设计？",
                    "en": "After deciding to alert, a monitor doesn't call the Slack API directly but publishes the alert to the WebhookQueue, with the automation system forwarding it. Why this design?",
                },
                "opts": [
                    {
                        "zh": "判断与投递分离（解耦）：monitor 只管「要不要告警」，不必认识每种投递渠道；投递方式可独立演进/重试/接新渠道，monitor 一行不改——呼应第30课创建/执行分离",
                        "en": "decision separate from delivery (decoupling): the monitor only decides 'whether to alert' and needn't know each delivery channel; delivery can evolve/retry/add channels independently with the monitor unchanged — echoing Lesson 30's create/execute split",
                    },
                    {"zh": "WebhookQueue 比直接调 Slack 快", "en": "the WebhookQueue is faster than calling Slack directly"},
                    {"zh": "为了把告警存档", "en": "to archive the alerts"},
                    {"zh": "Slack 不支持直接调用", "en": "Slack can't be called directly"},
                ],
                "answer": 0,
                "why": {
                    "zh": "monitor 的职责是判断是否越线告警，不该耦合「告警怎么送到人手里」（Slack/webhook/邮件/值班）。发布到统一 WebhookQueue，由自动化（第44课 Trigger→Action）决定渠道，于是投递可独立演进、可重试、可接任意新渠道，monitor 不变。这与第30课创建/执行分离、第12课一个入口多生产者，是同一种「解耦」品味。",
                    "en": "A monitor's job is deciding whether a line is crossed, not coupling to 'how the alert reaches a human' (Slack/webhook/email/on-call). Publishing to one WebhookQueue, with automation (Lesson 44's Trigger→Action) choosing the channel, lets delivery evolve/retry/add channels independently while the monitor stays put. Same decoupling taste as Lesson 30's create/execute split and Lesson 12's one-entry-many-producers.",
                },
            },
        ],
        "open": [
            {
                "zh": "Part 5 到此完整：score 模型（28）→ 四种生产 score 的方式（29–32）→ 主动监控告警（33）。回顾整个第五部分，Langfuse 让「评估」从一个静态的「能打分、能查」系统，变成一个动态的「能自动评、能主动告警、还能用人工分校准 AI」的闭环。如果让你为自己的 LLM 应用设计一套评估体系，你会怎么组合这五种能力（人工/LLM裁判/代码/监控）？哪些质量信号你会持续监控并告警，为什么？",
                "en": "Part 5 is now complete: the score model (28) → four ways to produce scores (29–32) → active monitoring and alerting (33). Reviewing the whole part, Langfuse turns 'evaluation' from a static 'can score, can query' system into a dynamic closed loop that 'auto-evaluates, alerts actively, and calibrates AI with human scores'. If you designed an evaluation system for your own LLM app, how would you combine these five capabilities (human/LLM-judge/code/monitoring)? Which quality signals would you continuously monitor and alert on, and why?",
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
