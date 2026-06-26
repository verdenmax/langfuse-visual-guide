"""Part 5 — 评估与评分 / Evaluation & scoring. Lessons L28–L33.

Same authoring pattern as part1..part4: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L28 · 评分模型 / The scoring model
# ══════════════════════════════════════════════════════════════════════
_ZH28 = []
_EN28 = []

_ZH28.append(r"""
<p class="lead">
前四部分让你能<strong>看清</strong>每一次 LLM 调用发生了什么。但「发生了什么」不等于「<strong>做得好不好</strong>」。这一部分讲<strong>评估</strong>——怎么给 trace 打分。而一切的原子单位，是 <strong>score（评分）</strong>。
这一课先把 score 的<strong>数据模型</strong>讲透：一个 score 长什么样、有哪<strong>三种数据类型</strong>（数值/分类/布尔）、<strong>score config</strong> 这个「评分的 schema」管什么，以及一个 score 可能来自哪<strong>三种来源</strong>。
理解了这套模型，后面五课（LLM 评判、代码 eval、人工标注、监控）就都只是「<strong>用不同方式生产 score</strong>」而已。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  把 score 想成给一次回答贴的一张<strong>评价标签</strong>。标签上写着<strong>评什么</strong>（name，如「有用性」）、<strong>打多少</strong>（value）、以及这是<strong>哪种刻度</strong>（dataType：是 0–1 的分数？还是「好/中/差」的档位？还是「对/错」的勾叉？）。
  而 <strong>score config</strong> 就像这类标签的<strong>印制规范</strong>：它规定「有用性」这张标签必须是 0–1 的数值、「情感」那张必须从 {正/中/负} 里选一个——于是<strong>同名标签永远同一把尺</strong>，才能横向比较、求平均。
  至于标签是谁贴的（source）：可能是你<strong>亲手</strong>贴（API）、可能是 <strong>AI 评判员</strong>贴（EVAL）、也可能是<strong>人工审核</strong>贴（ANNOTATION）——但只要刻度一致，三方贴的标签就活在<strong>同一个可比的空间</strong>里。
</div>
""")

# (L28 sections appended below)

_ZH28.append(r"""
<h2>三种刻度：数值、分类、布尔</h2>
<p>一个 score 的灵魂是它的 <code>dataType</code>——它决定 value 怎么解读、怎么校验。Langfuse 用 Zod 把三种类型定义得清清楚楚（外加一个旧的 TEXT）：</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="score 三种数据类型：NUMERIC 带 min/max 的数值、CATEGORICAL 一组标签到值的映射、BOOLEAN 固定为 True=1/False=0 的特殊分类">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">score 的三种刻度（dataType）</text>
  <rect x="20" y="40" width="216" height="160" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="128" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">NUMERIC 数值</text><text x="128" y="84" text-anchor="middle" font-size="8" fill="var(--accent-ink)">value 是一个数</text><text x="128" y="102" text-anchor="middle" font-size="8" fill="var(--accent-ink)">可设 minValue / maxValue</text><text x="128" y="124" text-anchor="middle" font-size="7.5" fill="var(--muted)">例：有用性 0–1、延迟分 1–5</text><rect x="40" y="138" width="176" height="48" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="128" y="156" text-anchor="middle" font-size="7.5" fill="var(--ink)">"helpfulness": 0.82</text><text x="128" y="172" text-anchor="middle" font-size="7" fill="var(--muted)">可求平均、可排序</text>
  <rect x="252" y="40" width="216" height="160" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">CATEGORICAL 分类</text><text x="360" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">一组「标签 ↔ 值」</text><text x="360" y="102" text-anchor="middle" font-size="8" fill="var(--muted)">标签唯一、值唯一</text><text x="360" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">例：情感 {正/中/负}</text><rect x="272" y="138" width="176" height="48" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="156" text-anchor="middle" font-size="7.5" fill="var(--ink)">"sentiment": "positive"</text><text x="360" y="172" text-anchor="middle" font-size="7" fill="var(--muted)">可计数、可分组</text>
  <rect x="484" y="40" width="216" height="160" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="592" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--teal)">BOOLEAN 布尔</text><text x="592" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">特殊的分类</text><text x="592" y="102" text-anchor="middle" font-size="8" fill="var(--muted)">固定两档：True=1 / False=0</text><text x="592" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">例：是否含敏感词</text><rect x="504" y="138" width="176" height="48" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="592" y="156" text-anchor="middle" font-size="7.5" fill="var(--ink)">"is_toxic": False (0)</text><text x="592" y="172" text-anchor="middle" font-size="7" fill="var(--muted)">可算通过率</text>
</svg>
<div class="figcap"><b>三种刻度，各有所长</b>：<b>NUMERIC</b>（数，带可选 min/max，能求平均/排序）、<b>CATEGORICAL</b>（标签↔值的固定集合，标签与值都唯一，能计数/分组）、<b>BOOLEAN</b>（固定为 <code>True=1 / False=0</code> 的特殊分类，能算通过率）。源码：<code>packages/shared/src/domain/score-configs.ts:18-80</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/score-configs.ts</span><span class="ln">三种 dataType</span></div>
  <pre class="code"><span class="cm">// 数值：可选区间，无 categories</span>
NumericConfigFields = { dataType: <span class="st">"NUMERIC"</span>, minValue?, maxValue? };

<span class="cm">// 分类：一组 {label, value}，标签唯一、值唯一（validateCategories）</span>
CategoricalConfigFields = { dataType: <span class="st">"CATEGORICAL"</span>, categories: [{label, value}, …] };

<span class="cm">// 布尔：其实是「恰好两档」的特殊分类，且锁死为 True=1 / False=0</span>
BooleanConfigFields = { dataType: <span class="st">"BOOLEAN"</span>,
  categories: [{label:<span class="st">"True"</span>, value:1}, {label:<span class="st">"False"</span>, value:0}] };  <span class="cm">// length===2 强校验</span></pre>
</div>

<p>注意一个优雅之处：<strong>布尔不是独立的第四种类型，而是被实现成「恰好两档、且锁死为 True=1/False=0」的分类</strong>。这样底层只需处理「数值」和「分类」两套逻辑，布尔顺势复用分类的存储与聚合——
少一套特例，多一分一致。这也呼应了第 8 课「宽事件」的思路：能用通用机制表达的，就别新造一个。</p>

<p>还有个贯穿始终的设计：<strong><code>value</code> 永远是一个数</strong>，而 <code>stringValue</code> 只用来存「标签」。NUMERIC 的 value 就是那个数、stringValue 为空；CATEGORICAL/BOOLEAN 则把标签放进 stringValue、把映射后的数放进 value（如 <code>"positive"</code>→某数、<code>"True"</code>→1）。
正因为<strong>任何 score 都有一个数值 value</strong>，求平均、画趋势、算通过率才对所有类型一视同仁——这是「可比」的物理基础。</p>

<table class="t">
  <thead><tr><th>dataType</th><th>value / stringValue</th><th>约束</th><th>能做的聚合</th><th>例子</th></tr></thead>
  <tbody>
    <tr><td><b>NUMERIC</b></td><td>value=那个数；stringValue 空</td><td>可选 minValue / maxValue</td><td>均值、分布、趋势</td><td>helpfulness 0.82</td></tr>
    <tr><td><b>CATEGORICAL</b></td><td>stringValue=标签；value=映射数</td><td>标签唯一、值唯一</td><td>计数、占比、分组</td><td>sentiment "positive"</td></tr>
    <tr><td><b>BOOLEAN</b></td><td>stringValue="True"/"False"；value∈{0,1}</td><td>锁死两档 True=1 / False=0</td><td>通过率</td><td>is_toxic False (0)</td></tr>
  </tbody>
</table>
<p>提醒：<code>scores.ts</code> 里 dataType 其实列了 <strong>5</strong> 种——上面 3 种是 score config 支持的「可比刻度」，另有 <strong>TEXT</strong>（自由文本，长度 ≤500，旧式）和 <strong>CORRECTION</strong>（人工标注纠正专用，name 固定为 <code>"output"</code>）。后两者不是可聚合的刻度，故本课聚焦前三。源码：<code>scores.ts:46-52</code>（5 种）、<code>score-configs.ts:117-138</code>（config 仅 4 种 discriminatedUnion）。</p>

""")

# (config + source section below)

_ZH28.append(r"""
<h2>score config：一张「评分的 schema」</h2>
<p>光有 dataType 还不够。如果同一个「有用性」分数，今天有人打 0–1、明天有人打 1–100，数据就乱成一锅。<strong>score config</strong> 就是解决这个的：它是某个 score <strong>name 的 schema</strong>——
声明这个名字下的分数是什么 dataType、什么区间/有哪些类别。于是无论分数从哪来，都按<strong>同一把尺</strong>校验，才谈得上比较与聚合。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="score config 作为某 name 的 schema，校验来自 API、EVAL、ANNOTATION 三种来源的分数，使它们落入同一可比空间">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一份 config 把守一个 name：三来源、同一把尺</text>
  <rect x="20" y="44" width="150" height="36" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="61" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">API（你亲手提交）</text><text x="95" y="74" text-anchor="middle" font-size="7" fill="var(--muted)">source=API</text>
  <rect x="20" y="86" width="150" height="36" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="95" y="103" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">EVAL（AI/代码评判）</text><text x="95" y="116" text-anchor="middle" font-size="7" fill="var(--accent-ink)">source=EVAL</text>
  <rect x="20" y="128" width="150" height="36" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="145" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">ANNOTATION（人工）</text><text x="95" y="158" text-anchor="middle" font-size="7" fill="var(--muted)">source=ANNOTATION</text>
  <rect x="270" y="74" width="180" height="62" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="96" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">score config（name 的 schema）</text><text x="360" y="114" text-anchor="middle" font-size="7.5" fill="var(--ink)">"有用性" = NUMERIC [0,1]</text><text x="360" y="128" text-anchor="middle" font-size="7" fill="var(--muted)">校验 value 是否合规</text>
  <rect x="500" y="80" width="200" height="50" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="600" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">scores 表（第 8 课宽表）</text><text x="600" y="116" text-anchor="middle" font-size="7.5" fill="var(--muted)">同名同尺 → 可比、可聚合</text>
  <line x1="170" y1="62" x2="268" y2="92" stroke="var(--faint)" stroke-width="1.3"/><line x1="170" y1="104" x2="268" y2="105" stroke="var(--accent)" stroke-width="1.3"/><line x1="170" y1="146" x2="268" y2="118" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="450" y1="105" x2="498" y2="105" stroke="var(--faint)" stroke-width="1.5"/><polygon points="498,105 489,101 489,109" fill="var(--faint)"/>
  <text x="360" y="186" text-anchor="middle" font-size="8.5" fill="var(--faint)">三种来源殊途同归：都按 config 校验、都写进同一张 scores 表——评判/人工/API 活在同一个可比空间</text>
</svg>
<div class="figcap"><b>一份 config 守一个 name</b>：score config 声明某 name 的 dataType 与约束（数值区间 / 类别集合），校验来自 <b>API / EVAL / ANNOTATION</b> 三种来源的分数，使它们落进同一张 scores 表、同一把尺。源码：<code>scores.ts:4</code>（<code>ScoreSourceArray=["API","EVAL","ANNOTATION"]</code>）。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">API</span><span class="name">你亲手提交</span></div><div class="ld">用 SDK 直接 <code>score.create</code>——比如你自己的离线评测脚本、或线上收集的用户点赞。这是第 6、12 课摄取链路里 <code>SCORE_CREATE</code> 事件的来路之一。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">EVAL</span><span class="name">AI 或代码评判</span></div><div class="ld">LLM-as-a-judge（第 29 课）或代码 eval（第 31 课）算出来的分。它们最终也<strong>走回同一条摄取链路</strong>写成 score——评估不是独立管道，而是 score 的生产者。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">ANNOTATION</span><span class="name">人工标注</span></div><div class="ld">人类审核员在标注队列里（第 32 课）按 config 给 trace 打分。同样落进 scores 表，只是 source 标成 ANNOTATION。</div></div>
</div>

<h2>一个 score 对象到底有哪些字段</h2>
<p>把 <code>ScoreSchema</code> 拆开看，一条 score 大致分三组字段——「评什么·打多少」「谁打的·带什么」「挂在哪」。最值得记的是最后一组：<strong>一条 score 必须挂在 trace / observation / session / 数据集运行 四者之一上</strong>（四个引用字段，恰好一个非空）。</p>

<div class="cols">
  <div class="col"><h4>评什么 · 打多少</h4><p><code>name</code> 评的是哪个维度（如「有用性」）；<code>value</code> 永远是一个数；<code>stringValue</code> 标签（分类/布尔/文本才有）；<code>dataType</code> 哪种刻度。</p></div>
  <div class="col"><h4>谁打的 · 带什么</h4><p><code>source</code> API / EVAL / ANNOTATION；<code>authorUserId</code> 人工标注者（可空）；<code>comment</code> 备注（可空）；<code>configId</code> 按哪份 config 校验；<code>queueId</code> 来自哪个标注队列。</p></div>
  <div class="col"><h4>挂在哪（四选一）</h4><p><code>traceId</code> 整条 trace；<code>observationId</code> trace 里某一步；<code>sessionId</code> 整个会话；<code>datasetRunId</code> 某次数据集运行——<strong>必须恰有一个非空</strong>。</p></div>
</div>
<p>这组「四选一的挂载点」很关键：它让评分既能贴在<strong>整条 trace</strong>（这次回答整体好不好）、也能贴在<strong>某一步 observation</strong>（这步检索准不准）、还能贴在<strong>整个 session</strong> 或<strong>一次数据集运行</strong>（第 34、35 课的实验场景）。同一个 score 模型，覆盖了从「单步」到「整批实验」的所有评估粒度。源码：<code>packages/shared/src/domain/scores.ts:89-133</code>。</p>
""")

# (spark + key below)

_ZH28.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么要专门搞一个 score config，而不是让大家随手打分？</strong> 因为<strong>「能比较」是评估的全部价值</strong>。如果「有用性」这个名字下，A 团队打 0–1、B 团队打百分制、C 又用「好/差」，
  那这些分数<strong>放在一起毫无意义</strong>——求平均是错的、画趋势是错的、做对比更是错的。score config 把「某个名字 = 某种刻度」<strong>固定下来、强制校验</strong>，于是同名分数永远可比，
  你才能放心地算「这周有用性均分涨了没」「哪个模型的毒性通过率更高」。这和第 8 课「provided vs computed」、第 16 课「定价 schema」是同一种工程信念：<strong>把「数据该长什么样」显式建模、前置校验，
  下游的一切分析才有坚实地基</strong>。而把三种来源统一到同一张 scores 表、同一套 config，则让「AI 评的」「人审的」「API 报的」分数活在一个空间里——<strong>这正是 Part 5 后续每一课的共同终点：生产可比的 score</strong>。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>score 是评估的原子单位</strong>：一个 (name, value, dataType, source) 挂在 trace 或其中某步 observation 上（也可挂 session / 数据集运行），把「发生了什么」变成「做得多好」。</li>
    <li><strong>三种 dataType</strong>：NUMERIC（数，带可选 min/max）、CATEGORICAL（标签↔值的固定集合，二者皆唯一）、BOOLEAN（锁死 True=1/False=0 的特殊分类）。</li>
    <li><strong>布尔复用分类</strong>：不是独立第四类，而是「恰好两档」的分类——少一套特例，呼应第 8 课「能用通用机制就别新造」。</li>
    <li><strong>score config = 某 name 的 schema</strong>：声明 dataType 与约束（区间/类别），强制校验，使<strong>同名分数永远同一把尺</strong>、可比可聚合。</li>
    <li><strong>三种 source</strong>：API（亲手提交）、EVAL（AI/代码评判）、ANNOTATION（人工）——殊途同归，都写进第 8 课的 scores 表。后续五课都只是「用不同方式生产 score」。</li>
  </ul>
</div>
""")

_EN28.append(r"""
<p class="lead">
The first four parts let you <strong>see</strong> what happened on every LLM call. But "what happened" is not the same as "<strong>how good was it</strong>". This part is about <strong>evaluation</strong>—how to put a number on a trace. And the atomic unit of all of it is the <strong>score</strong>.
This lesson nails down the score's <strong>data model</strong>: what a score looks like, its <strong>three data types</strong> (numeric / categorical / boolean), what the <strong>score config</strong> ("the schema of a score") governs, and which <strong>three sources</strong> a score can come from.
Once you have this model, the next five lessons (LLM-as-a-judge, code eval, human annotation, monitors) are all just "<strong>different ways of producing a score</strong>".
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Think of a score as an <strong>evaluation sticker</strong> slapped on one answer. The sticker says <strong>what you're rating</strong> (name, e.g. "helpfulness"), <strong>the rating</strong> (value), and <strong>which kind of scale</strong> (dataType: a 0–1 number? a "good/ok/bad" tier? a "right/wrong" tick?).
  The <strong>score config</strong> is the <strong>printing standard</strong> for that kind of sticker: it mandates that "helpfulness" must be a 0–1 number, that "sentiment" must be one of {pos/neutral/neg}—so <strong>same-named stickers always use the same ruler</strong>, which is what makes them comparable and averageable.
  As for who applied the sticker (source): maybe <strong>you</strong> did (API), maybe an <strong>AI judge</strong> did (EVAL), maybe a <strong>human reviewer</strong> did (ANNOTATION)—but as long as the scale matches, all three live in the <strong>same comparable space</strong>.
</div>
""")

_EN28.append(r"""
<h2>Three scales: numeric, categorical, boolean</h2>
<p>The soul of a score is its <code>dataType</code>—it decides how the value is read and validated. Langfuse pins down three types with Zod (plus a legacy TEXT):</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="The three score data types: NUMERIC a number with optional min/max, CATEGORICAL a fixed set of label-to-value pairs, BOOLEAN a special category locked to True=1/False=0">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">A score's three scales (dataType)</text>
  <rect x="20" y="40" width="216" height="160" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="128" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--accent-ink)">NUMERIC</text><text x="128" y="84" text-anchor="middle" font-size="8" fill="var(--accent-ink)">value is a number</text><text x="128" y="102" text-anchor="middle" font-size="8" fill="var(--accent-ink)">optional minValue / maxValue</text><text x="128" y="124" text-anchor="middle" font-size="7.5" fill="var(--muted)">e.g. helpfulness 0–1, latency 1–5</text><rect x="40" y="138" width="176" height="48" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="128" y="156" text-anchor="middle" font-size="7.5" fill="var(--ink)">"helpfulness": 0.82</text><text x="128" y="172" text-anchor="middle" font-size="7" fill="var(--muted)">averageable, sortable</text>
  <rect x="252" y="40" width="216" height="160" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="360" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--ink)">CATEGORICAL</text><text x="360" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">a set of label ↔ value</text><text x="360" y="102" text-anchor="middle" font-size="8" fill="var(--muted)">labels unique, values unique</text><text x="360" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">e.g. sentiment {pos/neu/neg}</text><rect x="272" y="138" width="176" height="48" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="360" y="156" text-anchor="middle" font-size="7.5" fill="var(--ink)">"sentiment": "positive"</text><text x="360" y="172" text-anchor="middle" font-size="7" fill="var(--muted)">countable, groupable</text>
  <rect x="484" y="40" width="216" height="160" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="592" y="62" text-anchor="middle" font-size="10" font-weight="700" fill="var(--teal)">BOOLEAN</text><text x="592" y="84" text-anchor="middle" font-size="8" fill="var(--muted)">a special category</text><text x="592" y="102" text-anchor="middle" font-size="8" fill="var(--muted)">locked: True=1 / False=0</text><text x="592" y="124" text-anchor="middle" font-size="7.5" fill="var(--faint)">e.g. contains toxic words?</text><rect x="504" y="138" width="176" height="48" rx="6" fill="var(--bg)" stroke="var(--faint)"/><text x="592" y="156" text-anchor="middle" font-size="7.5" fill="var(--ink)">"is_toxic": False (0)</text><text x="592" y="172" text-anchor="middle" font-size="7" fill="var(--muted)">pass-rate computable</text>
</svg>
<div class="figcap"><b>Three scales, each with a strength</b>: <b>NUMERIC</b> (a number with optional min/max, averageable/sortable), <b>CATEGORICAL</b> (a fixed set of label↔value, both unique, countable/groupable), <b>BOOLEAN</b> (a special category locked to <code>True=1 / False=0</code>, pass-rate computable). Source: <code>packages/shared/src/domain/score-configs.ts:18-80</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/domain/score-configs.ts</span><span class="ln">the three dataTypes</span></div>
  <pre class="code"><span class="cm">// numeric: optional bounds, no categories</span>
NumericConfigFields = { dataType: <span class="st">"NUMERIC"</span>, minValue?, maxValue? };

<span class="cm">// categorical: a set of {label, value}; labels unique, values unique (validateCategories)</span>
CategoricalConfigFields = { dataType: <span class="st">"CATEGORICAL"</span>, categories: [{label, value}, …] };

<span class="cm">// boolean: really a "exactly two" special category, locked to True=1 / False=0</span>
BooleanConfigFields = { dataType: <span class="st">"BOOLEAN"</span>,
  categories: [{label:<span class="st">"True"</span>, value:1}, {label:<span class="st">"False"</span>, value:0}] };  <span class="cm">// length===2 enforced</span></pre>
</div>

<p>Note one elegant move: <strong>boolean is not a separate fourth type—it is implemented as a "exactly two categories, locked to True=1/False=0" category</strong>. So the core only handles two logics, "numeric" and "categorical", and boolean reuses categorical storage and aggregation—
one fewer special case, one more bit of consistency. This echoes Lesson 8's "wide event" idea: if a general mechanism can express it, don't invent a new one.</p>

<p>One more design that runs throughout: <strong>the <code>value</code> is always a number</strong>, while <code>stringValue</code> only holds the "label". A NUMERIC value is just that number with an empty stringValue; CATEGORICAL/BOOLEAN put the label in stringValue and the mapped number in value (e.g. <code>"positive"</code>→a number, <code>"True"</code>→1).
Precisely because <strong>every score has a numeric value</strong>, averaging, trending, and pass-rate work uniformly across all types—the physical basis of "comparable".</p>

<table class="t">
  <thead><tr><th>dataType</th><th>value / stringValue</th><th>constraints</th><th>aggregations</th><th>example</th></tr></thead>
  <tbody>
    <tr><td><b>NUMERIC</b></td><td>value=the number; stringValue empty</td><td>optional minValue / maxValue</td><td>mean, distribution, trend</td><td>helpfulness 0.82</td></tr>
    <tr><td><b>CATEGORICAL</b></td><td>stringValue=label; value=mapped number</td><td>labels unique, values unique</td><td>count, share, group-by</td><td>sentiment "positive"</td></tr>
    <tr><td><b>BOOLEAN</b></td><td>stringValue="True"/"False"; value∈{0,1}</td><td>locked: True=1 / False=0</td><td>pass-rate</td><td>is_toxic False (0)</td></tr>
  </tbody>
</table>
<p>Reminder: <code>scores.ts</code> actually lists <strong>5</strong> dataTypes—the three above are the "comparable scales" a score config supports, plus <strong>TEXT</strong> (free text, length ≤500, legacy) and <strong>CORRECTION</strong> (for human-annotation corrections, name fixed to <code>"output"</code>). The latter two aren't aggregatable scales, so this lesson focuses on the first three. Source: <code>scores.ts:46-52</code> (5 types), <code>score-configs.ts:117-138</code> (config is a 4-way discriminatedUnion).</p>

""")

# (en config + source + spark + key below)

_EN28.append(r"""
<h2>score config: a "schema for scoring"</h2>
<p>A dataType alone isn't enough. If the same "helpfulness" score is rated 0–1 by one person today and 1–100 by another tomorrow, the data turns to mush. <strong>score config</strong> fixes exactly this: it is the <strong>schema of a score name</strong>—
declaring what dataType that name uses, and what bounds / which categories. So no matter where a score comes from, it is validated against the <strong>same ruler</strong>, which is the precondition for comparison and aggregation.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="A score config as the schema of a name, validating scores from API, EVAL, and ANNOTATION sources so they land in one comparable space">
  <text x="360" y="20" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">One config guards one name: three sources, one ruler</text>
  <rect x="20" y="44" width="150" height="36" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="61" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">API (you submit it)</text><text x="95" y="74" text-anchor="middle" font-size="7" fill="var(--muted)">source=API</text>
  <rect x="20" y="86" width="150" height="36" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="95" y="103" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">EVAL (AI/code judge)</text><text x="95" y="116" text-anchor="middle" font-size="7" fill="var(--accent-ink)">source=EVAL</text>
  <rect x="20" y="128" width="150" height="36" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="145" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">ANNOTATION (human)</text><text x="95" y="158" text-anchor="middle" font-size="7" fill="var(--muted)">source=ANNOTATION</text>
  <rect x="270" y="74" width="180" height="62" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="96" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">score config (name's schema)</text><text x="360" y="114" text-anchor="middle" font-size="7.5" fill="var(--ink)">"helpfulness" = NUMERIC [0,1]</text><text x="360" y="128" text-anchor="middle" font-size="7" fill="var(--muted)">validates the value</text>
  <rect x="500" y="80" width="200" height="50" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="600" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">scores table (L8 wide table)</text><text x="600" y="116" text-anchor="middle" font-size="7.5" fill="var(--muted)">same name+ruler → comparable</text>
  <line x1="170" y1="62" x2="268" y2="92" stroke="var(--faint)" stroke-width="1.3"/><line x1="170" y1="104" x2="268" y2="105" stroke="var(--accent)" stroke-width="1.3"/><line x1="170" y1="146" x2="268" y2="118" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="450" y1="105" x2="498" y2="105" stroke="var(--faint)" stroke-width="1.5"/><polygon points="498,105 489,101 489,109" fill="var(--faint)"/>
  <text x="360" y="186" text-anchor="middle" font-size="8.5" fill="var(--faint)">three sources converge: all validated by config, all written to one scores table—judge/human/API in one comparable space</text>
</svg>
<div class="figcap"><b>One config guards one name</b>: a score config declares a name's dataType and constraints (numeric bounds / category set), validating scores from <b>API / EVAL / ANNOTATION</b> into one scores table, one ruler. Source: <code>scores.ts:4</code> (<code>ScoreSourceArray=["API","EVAL","ANNOTATION"]</code>).</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">API</span><span class="name">you submit it</span></div><div class="ld">Use the SDK's <code>score.create</code> directly—e.g. your own offline eval script, or thumbs-up collected in production. This is one origin of the <code>SCORE_CREATE</code> event on the ingestion path of Lessons 6 & 12.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">EVAL</span><span class="name">AI or code judge</span></div><div class="ld">Scores computed by LLM-as-a-judge (Lesson 29) or code eval (Lesson 31). They too <strong>flow back through the same ingestion path</strong> to become scores—evaluation isn't a separate pipeline, it's a producer of scores.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">ANNOTATION</span><span class="name">human annotation</span></div><div class="ld">Human reviewers score traces against the config in an annotation queue (Lesson 32). They land in the same scores table, just with source set to ANNOTATION.</div></div>
</div>

<h2>What fields a score object actually has</h2>
<p>Unpack <code>ScoreSchema</code> and a score splits into three groups of fields—"what & how much", "who & with what", and "attached to what". The most worth remembering is the last: <strong>a score must attach to exactly one of trace / observation / session / dataset-run</strong> (four reference fields, exactly one non-null).</p>

<div class="cols">
  <div class="col"><h4>what · how much</h4><p><code>name</code> which dimension (e.g. "helpfulness"); <code>value</code> always a number; <code>stringValue</code> the label (categorical/boolean/text only); <code>dataType</code> which scale.</p></div>
  <div class="col"><h4>who · with what</h4><p><code>source</code> API / EVAL / ANNOTATION; <code>authorUserId</code> the human annotator (nullable); <code>comment</code> a note (nullable); <code>configId</code> which config validates it; <code>queueId</code> which annotation queue it came from.</p></div>
  <div class="col"><h4>attached to (one of)</h4><p><code>traceId</code> the whole trace; <code>observationId</code> one step within; <code>sessionId</code> the whole session; <code>datasetRunId</code> one dataset run—<strong>exactly one must be non-null</strong>.</p></div>
</div>
<p>This "one-of-four attachment point" matters: it lets a score sit on the <strong>whole trace</strong> (was this answer good overall), on <strong>one observation</strong> (was this retrieval step accurate), or on a <strong>whole session</strong> or a <strong>dataset run</strong> (the experiment scenarios of Lessons 34–35). One score model covers every evaluation granularity, from a single step to a whole batch experiment. Source: <code>packages/shared/src/domain/scores.ts:89-133</code>.</p>
""")

_EN28.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why bother with a dedicated score config instead of letting everyone score freely?</strong> Because <strong>"being comparable" is the entire value of evaluation</strong>. If under the name "helpfulness" team A rates 0–1, team B uses a percentage, and C uses "good/bad",
  then those scores are <strong>meaningless together</strong>—averaging is wrong, trending is wrong, comparing is more wrong still. A score config <strong>fixes and enforces</strong> "a given name = a given scale", so same-named scores are forever comparable,
  and you can confidently ask "did average helpfulness rise this week" or "which model has the higher toxicity pass-rate". This is the same engineering belief as Lesson 8's "provided vs computed" and Lesson 16's "pricing schema": <strong>model "what the data should look like" explicitly and validate up front,
  and every downstream analysis stands on solid ground</strong>. Unifying three sources into one scores table and one config set lets "AI-judged", "human-reviewed", and "API-reported" scores live in one space—<strong>which is the shared destination of every remaining lesson in Part 5: producing comparable scores</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A score is evaluation's atomic unit</strong>: one (name, value, dataType, source) attached to a trace or one observation within it (or a session / dataset run), turning "what happened" into "how well".</li>
    <li><strong>Three dataTypes</strong>: NUMERIC (a number with optional min/max), CATEGORICAL (a fixed set of label↔value, both unique), BOOLEAN (a special category locked to True=1/False=0).</li>
    <li><strong>Boolean reuses categorical</strong>: not a separate fourth type but an "exactly two" category—one fewer special case, echoing Lesson 8's "don't invent when a general mechanism works".</li>
    <li><strong>score config = a name's schema</strong>: declares dataType and constraints (bounds/categories), enforces validation, so <strong>same-named scores always share one ruler</strong>—comparable and aggregatable.</li>
    <li><strong>Three sources</strong>: API (you submit), EVAL (AI/code judge), ANNOTATION (human)—all converge, all written to Lesson 8's scores table. The next five lessons are just "producing scores in different ways".</li>
  </ul>
</div>
""")

LESSON_28 = {"zh": "\n".join(_ZH28), "en": "\n".join(_EN28)}
