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
