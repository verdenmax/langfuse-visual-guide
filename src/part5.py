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


# ══════════════════════════════════════════════════════════════════════
# L29 · LLM 当裁判 / LLM-as-a-judge
# ══════════════════════════════════════════════════════════════════════
_ZH29 = []
_EN29 = []

_ZH29.append(r"""
<p class="lead">
上一课说 score 是评估的原子单位，也说了它有三种来源。这一课讲最有意思的那种来源：<strong>EVAL——用一个 LLM 去给另一个 LLM 的输出打分</strong>，业界叫 <strong>LLM-as-a-judge（LLM 当裁判）</strong>。
人工标注准但慢且贵，规则匹配快但只能查表面。让一个「裁判 LLM」读你的 trace、按你给的标准打分，就能<strong>自动、可扩展地</strong>评估「这次回答到底好不好」。这一课拆开 Langfuse 的裁判流水线：
<strong>模板</strong>（评分标准）、<strong>变量映射</strong>（把 trace 的哪些部分递给裁判看）、<strong>结构化输出</strong>（裁判必须返回规整的分数 + 理由），以及最关键的——评出来的分<strong>怎么变回一个 score</strong>。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  想象一场作文比赛的<strong>评委</strong>。<strong>评分细则</strong>（模板 prompt）写着「请就『有用性』给 0–1 分，并说明理由」；但评委不会读整个学生档案，工作人员只把<strong>作文正文和题目</strong>递过去（变量映射：把 trace 的 input/output 填进模板的 <code>{{question}}</code>/<code>{{answer}}</code>）。
  评委看完，必须在<strong>规定表格</strong>里填「分数 + 评语」（结构化输出，不能写成一段散文让人没法录入）。最后这张评分表被<strong>归档进成绩册</strong>（评出的分作为一个 source=EVAL 的 score，走回第 12 课那条摄取链路，落进 scores 表）。
  整套流程的妙处：评委本身也是一次 LLM 调用，<strong>所以它自己也被 Langfuse 记成一条 trace</strong>——裁判也在被观测。
</div>
""")

_ZH29.append(r"""
<h2>裁判流水线：从一条 trace 到一个分数</h2>
<p>Langfuse 把 LLM-as-a-judge 拆成三件可复用的东西：<strong>模板</strong>（评什么、怎么评、用哪个模型）、<strong>评估器</strong>（把模板绑到哪些 trace、变量怎么取、分数叫什么名）、以及一次次的<strong>执行</strong>（真正去取数据、调裁判、产出分数）。下图是一条 trace 走完整条流水线的样子：</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="LLM-as-a-judge 流水线：模板与评估器配置，对一条 trace 提取变量、编译提示、调用裁判 LLM 得到结构化的分数+理由，再作为 source=EVAL 的 score 走回摄取链路写入 scores 表">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">裁判流水线：trace → 变量 → 裁判 LLM → score(EVAL)</text>
  <rect x="20" y="36" width="150" height="58" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="95" y="56" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">① 模板 Template</text><text x="95" y="72" text-anchor="middle" font-size="7" fill="var(--accent-ink)">prompt + 输出定义</text><text x="95" y="84" text-anchor="middle" font-size="7" fill="var(--accent-ink)">+ 模型/provider</text>
  <rect x="20" y="104" width="150" height="58" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="124" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">② 评估器 Evaluator</text><text x="95" y="140" text-anchor="middle" font-size="7" fill="var(--muted)">目标过滤 + 变量映射</text><text x="95" y="152" text-anchor="middle" font-size="7" fill="var(--muted)">+ scoreName</text>
  <rect x="210" y="70" width="120" height="58" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="270" y="90" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">③ 提取变量</text><text x="270" y="106" text-anchor="middle" font-size="6.8" fill="var(--muted)">从 trace/observation</text><text x="270" y="117" text-anchor="middle" font-size="6.8" fill="var(--muted)">/dataset 取列值</text>
  <rect x="210" y="140" width="120" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="270" y="158" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">编译提示</text><text x="270" y="173" text-anchor="middle" font-size="6.8" fill="var(--muted)">{{var}} 填实值</text>
  <rect x="370" y="86" width="140" height="80" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="440" y="108" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">④ 裁判 LLM</text><text x="440" y="126" text-anchor="middle" font-size="7" fill="var(--accent-ink)">结构化输出</text><text x="440" y="140" text-anchor="middle" font-size="7" fill="var(--accent-ink)">{ score, reasoning }</text><text x="440" y="156" text-anchor="middle" font-size="6.5" fill="var(--muted)">自身也被记成 trace</text>
  <rect x="548" y="70" width="152" height="50" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="624" y="89" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">⑤ score(source=EVAL)</text><text x="624" y="105" text-anchor="middle" font-size="6.8" fill="var(--muted)">value + comment=理由</text>
  <rect x="548" y="132" width="152" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="624" y="151" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">⑥ 摄取链路(第12课)</text><text x="624" y="167" text-anchor="middle" font-size="6.8" fill="var(--muted)">SCORE_CREATE → scores 表</text>
  <line x1="170" y1="65" x2="208" y2="92" stroke="var(--faint)" stroke-width="1.3"/><line x1="170" y1="133" x2="208" y2="150" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="270" y1="128" x2="270" y2="138" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="330" y1="120" x2="368" y2="120" stroke="var(--accent)" stroke-width="1.5"/><polygon points="368,120 359,116 359,124" fill="var(--accent)"/>
  <line x1="510" y1="110" x2="546" y2="98" stroke="var(--accent)" stroke-width="1.5"/><polygon points="546,98 537,97 540,105" fill="var(--accent)"/>
  <line x1="624" y1="120" x2="624" y2="130" stroke="var(--faint)" stroke-width="1.3"/><polygon points="624,132 620,123 628,123" fill="var(--teal)"/>
  <text x="360" y="240" text-anchor="middle" font-size="8" fill="var(--faint)">配置一次（①②），就对每条命中的 trace 自动跑③④⑤⑥——评估是「持续的」，不是「一次性的」</text>
</svg>
<div class="figcap"><b>三件套 + 六步</b>：模板与评估器是<b>配置</b>（一次），提取变量/编译提示/调裁判/产出分数/回流摄取是<b>执行</b>（每条 trace 一次）。源码：<code>worker/src/features/evaluation/evalService.ts</code> 的 <code>runLLMAsJudgeEvaluation</code>（:735）串起④⑤，<code>createEvalJobs</code>（:180，下一课）负责①②③ 的调度。</div>
</div>

<div class="layers">
  <div class="layer l-part"><div class="lh"><span class="badge">①</span><span class="name">模板 Eval Template</span></div><div class="ld">可复用的「评分标准」：一段带 <code>{{变量}}</code> 的 prompt（如「就有用性给 0–1 分并说明理由」）、一个<strong>输出定义</strong>（产出 NUMERIC/CATEGORICAL/BOOLEAN 哪种分、范围多少），外加用哪个 provider/model 当裁判。模板只描述「怎么评」，不绑定具体数据。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">②</span><span class="name">评估器 Evaluator（JobConfiguration）</span></div><div class="ld">把模板「落地」：用一个<strong>过滤条件</strong>圈定要评哪些 trace（如「只评 production 环境、name=chat 的」）、一份<strong>变量映射</strong>（模板里的 <code>{{answer}}</code> 该取 trace 的哪一列），以及最终分数叫什么名（<code>scoreName</code>）。</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">③–⑥</span><span class="name">执行 Execution（JobExecution）</span></div><div class="ld">每条命中的 trace 触发一次执行：提取变量 → 编译提示 → 调裁判 LLM 拿结构化结果 → 归一成 score → 经摄取链路写回。这条「执行」本身有状态生命周期（第 30 课细讲）。</div></div>
</div>
""")

# (L29 sec2 mapping below)

_ZH29.append(r"""
<h2>变量映射：把 trace 的哪一部分递给裁判</h2>
<p>模板里写的是 <code>{{question}}</code> <code>{{answer}}</code> 这样的占位符——它们怎么变成真实内容？靠<strong>变量映射</strong>：每个模板变量声明它来自哪个 <code>langfuseObject</code>（trace / observation / dataset_item）的哪一列（<code>selectedColumnId</code>，如 input/output/metadata）。执行时，<code>extractVariablesFromTracingData</code> 按映射去真实的 trace 里把值一个个取出来。</p>

<div class="cols">
  <div class="col"><h4>模板变量（你写的占位符）</h4><p><code>{{question}}</code> → 用户的问题<br><code>{{answer}}</code> → 模型的回答<br><code>{{context}}</code> → 检索到的资料<br>模板只认名字，不关心数据从哪来。</p></div>
  <div class="col"><h4>映射（你配的对应关系）</h4><p><code>question</code> ← trace.input<br><code>answer</code> ← trace.output<br><code>context</code> ← observation[retriever].output<br>每条映射 = {templateVariable, langfuseObject, selectedColumnId}。</p></div>
  <div class="col"><h4>提取（执行时自动做）</h4><p>对每个变量找到映射，去真实 trace/observation/dataset_item 取那一列的值，得到 <code>{var, value}</code>。取不到就退化为空串并告警，不让整次评估崩。</p></div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalRuntime.ts · evalService.ts</span><span class="ln">提取 + 编译</span></div>
  <pre class="code"><span class="cm">// 1) 按映射从真实 trace 取每个变量的值（evalService.ts:1152）</span>
<span class="kw">for</span> (<span class="kw">const</span> variable <span class="kw">of</span> variables) {
  <span class="kw">const</span> mapping = variableMapping.find(m =&gt; m.templateVariable === variable);
  <span class="kw">if</span> (mapping.langfuseObject === <span class="st">"trace"</span>) {        <span class="cm">// 也可能是 observation / dataset_item</span>
    <span class="kw">const</span> trace = <span class="kw">await</span> getTraceById({ traceId, projectId, timestamp });
    results.push({ var: variable, value: parseDatabaseRowValue(trace, mapping) });
  }
}

<span class="cm">// 2) 把取到的值填进模板的 {{占位符}}（evalRuntime.ts:14）</span>
<span class="kw">export function</span> <span class="fn">compileEvalPrompt</span>(params) {
  <span class="kw">const</span> variableMap = Object.fromEntries(
    params.variables.map(({ var: key, value }) =&gt; [key, parseUnknownToString(value)]));
  <span class="kw">return</span> compileTemplateString(params.templatePrompt, variableMap);  <span class="cm">// {{answer}} → 实际回答</span>
}</pre>
</div>

<p>注意一个细节：提取阶段<strong>保留原始数据形状</strong>（给代码 eval 用，第 31 课），只有在 <code>compileEvalPrompt</code> 这个「喂给裁判 LLM」的边界上才用 <code>parseUnknownToString</code> 拍平成字符串——因为 LLM 的 prompt 终究是文本。这种「在边界处才转换、内部保留原样」的克制，是干净数据流的标志。</p>
""")

# (L29 sec3 output below)

_ZH29.append(r"""
<h2>结构化输出与回流：分数怎么变回一个 score</h2>
<p>裁判 LLM 不能只回一段散文——那样没法录入。Langfuse 用<strong>结构化输出</strong>（structured output）强制它返回规整的 JSON：按模板的输出定义，要么 <code>{score: 数, reasoning}</code>（NUMERIC/BOOLEAN），要么 <code>{matches: [...], reasoning}</code>（CATEGORICAL）。拿到后 <code>toNormalizedScores</code> 把它归一成 score：<strong>value 是分、comment 是裁判的理由</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="裁判 LLM 返回结构化的分数与理由，toNormalizedScores 归一成 score，作为 source=EVAL 的 SCORE_CREATE 事件走回第 12 课的摄取链路，最终落进 scores 宽表，与 API、人工来源的分数同表可比">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">结构化输出 → 归一 → 回流摄取链路</text>
  <rect x="20" y="42" width="170" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="105" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">裁判 LLM 的结构化输出</text><text x="105" y="80" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">{ score: 0.82,</text><text x="105" y="94" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">  reasoning: "回答完整…" }</text><text x="105" y="109" text-anchor="middle" font-size="6.8" fill="var(--muted)">schema 强校验，非自由散文</text>
  <rect x="232" y="48" width="150" height="62" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="307" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">toNormalizedScores</text><text x="307" y="85" text-anchor="middle" font-size="7" fill="var(--muted)">value ← score</text><text x="307" y="98" text-anchor="middle" font-size="7" fill="var(--muted)">comment ← reasoning</text>
  <rect x="424" y="42" width="150" height="74" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/><text x="499" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">SCORE_CREATE 事件</text><text x="499" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">source = EVAL</text><text x="499" y="93" text-anchor="middle" font-size="7" fill="var(--accent-ink)">name/value/dataType/comment</text><text x="499" y="107" text-anchor="middle" font-size="6.8" fill="var(--muted)">和你手写 score 同一种事件</text>
  <rect x="600" y="54" width="104" height="50" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="652" y="74" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">scores 宽表</text><text x="652" y="90" text-anchor="middle" font-size="6.6" fill="var(--muted)">三来源同表可比</text>
  <line x1="190" y1="79" x2="230" y2="79" stroke="var(--blue)" stroke-width="1.5"/><polygon points="230,79 221,75 221,83" fill="var(--blue)"/>
  <line x1="382" y1="79" x2="422" y2="79" stroke="var(--accent)" stroke-width="1.5"/><polygon points="422,79 413,75 413,83" fill="var(--accent)"/>
  <line x1="574" y1="79" x2="598" y2="79" stroke="var(--teal)" stroke-width="1.5"/><polygon points="598,79 589,75 589,83" fill="var(--teal)"/>
  <rect x="120" y="142" width="480" height="50" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="360" y="162" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">关键：评估不是另开一条管道，而是「第 12 课摄取链路」的又一个生产者</text><text x="360" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">EVAL 分数和 API、ANNOTATION 分数走同一条 SCORE_CREATE 入口，享受同样的去重/合并/落库</text>
</svg>
<div class="figcap"><b>评出来的分，和你亲手提交的分，是同一种事件</b>。<code>evalScoreEvent.ts:52</code> 把结果包成 <code>SCORE_CREATE</code> 且 <code>source: ScoreSourceEnum.EVAL</code>，再走第 12 课的摄取链路。所以裁判产出的分天然与其它来源<strong>同表、同尺、可比</strong>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalService.ts:953 · evalScoreEvent.ts:52</span><span class="ln">归一 + 回流</span></div>
  <pre class="code"><span class="cm">// 归一：value=分，comment=裁判的理由（evalService.ts: toNormalizedScores）</span>
<span class="kw">const</span> baseFields = { name: scoreName, comment: outputResult.reasoning };
<span class="kw">if</span> (outputResult.dataType === <span class="st">"NUMERIC"</span>) <span class="kw">return</span> [{ ...baseFields, dataType: <span class="st">"NUMERIC"</span>, value: outputResult.score }];
<span class="kw">if</span> (outputResult.dataType === <span class="st">"BOOLEAN"</span>) <span class="kw">return</span> [{ ...baseFields, dataType: <span class="st">"BOOLEAN"</span>, value: outputResult.score ? 1 : 0 }];

<span class="cm">// 回流：包成与手写 score 完全相同的 SCORE_CREATE 事件（evalScoreEvent.ts）</span>
{ type: eventTypes.SCORE_CREATE,
  body: { name: score.name, value: score.value, dataType: score.dataType,
          comment: score.comment, configId: score.configId,
          source: <span class="st">ScoreSourceEnum.EVAL</span>,        <span class="cm">// ← 唯一的「来源」标记</span>
          executionTraceId: params.executionTraceId } }</pre>
</div>

<table class="t">
  <thead><tr><th>输出定义</th><th>裁判返回</th><th>归一成 score</th><th>产几条分</th></tr></thead>
  <tbody>
    <tr><td><b>NUMERIC</b></td><td>{ score: 数, reasoning }</td><td>value = score</td><td>1 条</td></tr>
    <tr><td><b>BOOLEAN</b></td><td>{ score: 真/假, reasoning }</td><td>value = score ? 1 : 0</td><td>1 条</td></tr>
    <tr><td><b>CATEGORICAL</b></td><td>{ matches: [标签…], reasoning }</td><td>每个 match 一条，value = 该标签</td><td>可多条</td></tr>
  </tbody>
</table>
<p>三种输出定义对应模板里你选的分数类型；注意 CATEGORICAL 的 <code>matches</code> 是<strong>数组</strong>——一次评判可以打出<strong>多条</strong>分类分（如同时命中「事实正确」与「语气友好」两个标签）。无论哪种，<code>reasoning</code> 都被原样塞进每条 score 的 <code>comment</code>。源码：<code>evalService.ts:953-997</code> 的 <code>toNormalizedScores</code>。</p>
""")

_ZH29.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么裁判必须用「结构化输出」，而不是让它自由发挥？</strong> 因为评估的产物要能<strong>录入、聚合、比较</strong>。若裁判回一段「我觉得这个回答还不错，但开头有点啰嗦……」的散文，你既没法可靠地抽出一个分、也没法跨千条 trace 求平均。
  强制 <code>{score, reasoning}</code> 的 schema，让分数能进 scores 表（可聚合），又把「为什么给这个分」留在 <code>comment</code> 里（可追溯）——<strong>两全</strong>。<br><br>
  <strong>更深一层：为什么评估结果要走回摄取链路，而不是直接写库？</strong> 这是 Langfuse 反复出现的信念——<strong>「一个入口，多个生产者」</strong>。无论分数来自 API、人工、还是裁判 LLM，都包成同一种 <code>SCORE_CREATE</code> 事件、走第 12 课那条链路，
  于是去重、合并、落 ClickHouse 的逻辑只写一遍、对所有来源一致。评估因此不是「另一个系统」，而是<strong>摄取管道的又一个上游</strong>。还有个优雅的递归：裁判自己的那次 LLM 调用，也被记成一条 Langfuse trace（环境标为 LLMJudge）——<strong>观测平台连自己的裁判都一并观测了</strong>。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>LLM-as-a-judge = 用一个 LLM 给另一个 LLM 的输出打分</strong>：在人工（准但慢）与规则（快但浅）之间，提供自动、可扩展的质量评估。</li>
    <li><strong>三件套</strong>：模板（prompt+输出定义+模型，描述「怎么评」）、评估器（过滤目标+变量映射+scoreName，描述「评谁」）、执行（每条 trace 实际跑一次）。</li>
    <li><strong>变量映射</strong>：模板的 <code>{{占位符}}</code> 各自声明来自 trace/observation/dataset_item 的哪一列；<code>extractVariablesFromTracingData</code> 执行时去真实数据里取值，<code>compileEvalPrompt</code> 在「喂给 LLM」的边界才拍平成字符串。</li>
    <li><strong>结构化输出</strong>：裁判被强制返回 <code>{score, reasoning}</code>（或分类的 <code>{matches, reasoning}</code>）；<code>toNormalizedScores</code> 归一为 value=分、comment=理由——可聚合又可追溯。</li>
    <li><strong>回流摄取（source=EVAL）</strong>：结果包成与手写 score 相同的 <code>SCORE_CREATE</code> 事件走第 12 课链路。评估是摄取管道的又一个生产者，不是独立系统；裁判自身的调用也被记成 trace。</li>
  </ul>
</div>
""")

_EN29.append(r"""
<p class="lead">
Last lesson said a score is evaluation's atomic unit, and that it has three sources. This lesson covers the most interesting source: <strong>EVAL—using one LLM to score another LLM's output</strong>, known industry-wide as <strong>LLM-as-a-judge</strong>.
Human labeling is accurate but slow and costly; rule matching is fast but only checks the surface. Letting a "judge LLM" read your trace and score it against your criteria gives you <strong>automatic, scalable</strong> assessment of "was this answer actually good". This lesson takes apart Langfuse's judge pipeline:
the <strong>template</strong> (the rubric), the <strong>variable mapping</strong> (which parts of the trace to hand the judge), the <strong>structured output</strong> (the judge must return a tidy score + reasoning), and most crucially—<strong>how the verdict turns back into a score</strong>.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Picture a <strong>judge</strong> at an essay contest. The <strong>scoring rubric</strong> (template prompt) says "rate 'helpfulness' 0–1 and explain why"; but the judge doesn't read the whole student file—staff hand over only the <strong>essay body and the prompt</strong> (variable mapping: fill the trace's input/output into the template's <code>{{question}}</code>/<code>{{answer}}</code>).
  After reading, the judge must fill in a <strong>fixed form</strong> with "score + comment" (structured output—not a prose blob no one can record). Finally that scoring sheet is <strong>filed into the gradebook</strong> (the verdict becomes a source=EVAL score, flowing back through Lesson 12's ingestion path into the scores table).
  The neat part: the judge is itself an LLM call, <strong>so it too is recorded as a Langfuse trace</strong>—the judge is also observed.
</div>
""")

_EN29.append(r"""
<h2>The judge pipeline: from one trace to one score</h2>
<p>Langfuse splits LLM-as-a-judge into three reusable things: a <strong>template</strong> (what to rate, how, with which model), an <strong>evaluator</strong> (which traces to bind the template to, how variables are fetched, what the score is named), and repeated <strong>executions</strong> (actually fetching data, calling the judge, producing scores). Below is one trace's journey through the whole pipeline:</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="The LLM-as-a-judge pipeline: a template and evaluator configure it; for a trace it extracts variables, compiles the prompt, calls the judge LLM to get a structured score+reasoning, then as a source=EVAL score flows back through the ingestion path into the scores table">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">judge pipeline: trace → variables → judge LLM → score(EVAL)</text>
  <rect x="20" y="36" width="150" height="58" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="95" y="56" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">① Template</text><text x="95" y="72" text-anchor="middle" font-size="7" fill="var(--accent-ink)">prompt + output def</text><text x="95" y="84" text-anchor="middle" font-size="7" fill="var(--accent-ink)">+ model/provider</text>
  <rect x="20" y="104" width="150" height="58" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="124" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">② Evaluator</text><text x="95" y="140" text-anchor="middle" font-size="7" fill="var(--muted)">target filter + var mapping</text><text x="95" y="152" text-anchor="middle" font-size="7" fill="var(--muted)">+ scoreName</text>
  <rect x="210" y="70" width="120" height="58" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="270" y="90" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">③ extract vars</text><text x="270" y="106" text-anchor="middle" font-size="6.8" fill="var(--muted)">from trace/observation</text><text x="270" y="117" text-anchor="middle" font-size="6.8" fill="var(--muted)">/dataset columns</text>
  <rect x="210" y="140" width="120" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="270" y="158" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">compile prompt</text><text x="270" y="173" text-anchor="middle" font-size="6.8" fill="var(--muted)">{{var}} → real value</text>
  <rect x="370" y="86" width="140" height="80" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="440" y="108" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">④ judge LLM</text><text x="440" y="126" text-anchor="middle" font-size="7" fill="var(--accent-ink)">structured output</text><text x="440" y="140" text-anchor="middle" font-size="7" fill="var(--accent-ink)">{ score, reasoning }</text><text x="440" y="156" text-anchor="middle" font-size="6.5" fill="var(--muted)">itself recorded as a trace</text>
  <rect x="548" y="70" width="152" height="50" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="624" y="89" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">⑤ score(source=EVAL)</text><text x="624" y="105" text-anchor="middle" font-size="6.8" fill="var(--muted)">value + comment=reasoning</text>
  <rect x="548" y="132" width="152" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="624" y="151" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">⑥ ingestion path (L12)</text><text x="624" y="167" text-anchor="middle" font-size="6.8" fill="var(--muted)">SCORE_CREATE → scores table</text>
  <line x1="170" y1="65" x2="208" y2="92" stroke="var(--faint)" stroke-width="1.3"/><line x1="170" y1="133" x2="208" y2="150" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="270" y1="128" x2="270" y2="138" stroke="var(--faint)" stroke-width="1.3"/>
  <line x1="330" y1="120" x2="368" y2="120" stroke="var(--accent)" stroke-width="1.5"/><polygon points="368,120 359,116 359,124" fill="var(--accent)"/>
  <line x1="510" y1="110" x2="546" y2="98" stroke="var(--accent)" stroke-width="1.5"/><polygon points="546,98 537,97 540,105" fill="var(--accent)"/>
  <line x1="624" y1="120" x2="624" y2="130" stroke="var(--faint)" stroke-width="1.3"/><polygon points="624,132 620,123 628,123" fill="var(--teal)"/>
  <text x="360" y="240" text-anchor="middle" font-size="8" fill="var(--faint)">configure once (①②) and ③④⑤⑥ run automatically per matching trace—evaluation is "continuous", not "one-off"</text>
</svg>
<div class="figcap"><b>Three pieces + six steps</b>: template and evaluator are <b>config</b> (once); extract/compile/judge/produce/flow-back are <b>execution</b> (once per trace). Source: <code>worker/src/features/evaluation/evalService.ts</code>'s <code>runLLMAsJudgeEvaluation</code> (:735) wires ④⑤; <code>createEvalJobs</code> (:180, next lesson) schedules ①②③.</div>
</div>

<div class="layers">
  <div class="layer l-part"><div class="lh"><span class="badge">①</span><span class="name">Eval Template</span></div><div class="ld">A reusable "rubric": a prompt with <code>{{variables}}</code> (e.g. "rate helpfulness 0–1 with reasoning"), an <strong>output definition</strong> (which score it produces—NUMERIC/CATEGORICAL/BOOLEAN, what range), plus which provider/model judges. A template only describes "how to rate", binding no specific data.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">②</span><span class="name">Evaluator (JobConfiguration)</span></div><div class="ld">"Grounds" the template: a <strong>filter</strong> picking which traces to evaluate (e.g. "only production, name=chat"), a <strong>variable mapping</strong> (which column the template's <code>{{answer}}</code> reads), and what the final score is named (<code>scoreName</code>).</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">③–⑥</span><span class="name">Execution (JobExecution)</span></div><div class="ld">Each matching trace triggers one execution: extract variables → compile prompt → call judge LLM for a structured result → normalize into a score → write back via the ingestion path. This "execution" has its own status lifecycle (detailed in Lesson 30).</div></div>
</div>
""")

# (en sec2/3/spark below)

_EN29.append(r"""
<h2>Variable mapping: which part of the trace to hand the judge</h2>
<p>The template holds placeholders like <code>{{question}}</code> <code>{{answer}}</code>—how do they become real content? Via the <strong>variable mapping</strong>: each template variable declares which <code>langfuseObject</code> (trace / observation / dataset_item) and which column (<code>selectedColumnId</code>, e.g. input/output/metadata) it comes from. At execution, <code>extractVariablesFromTracingData</code> pulls each value from the real trace per the mapping.</p>

<div class="cols">
  <div class="col"><h4>Template variables (your placeholders)</h4><p><code>{{question}}</code> → the user's question<br><code>{{answer}}</code> → the model's answer<br><code>{{context}}</code> → retrieved material<br>The template only knows names, not where data comes from.</p></div>
  <div class="col"><h4>Mapping (the correspondence you configure)</h4><p><code>question</code> ← trace.input<br><code>answer</code> ← trace.output<br><code>context</code> ← observation[retriever].output<br>Each mapping = {templateVariable, langfuseObject, selectedColumnId}.</p></div>
  <div class="col"><h4>Extraction (done automatically at run)</h4><p>For each variable find its mapping, fetch that column's value from the real trace/observation/dataset_item, yielding <code>{var, value}</code>. If missing, degrade to an empty string with a warning—never crash the whole eval.</p></div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalRuntime.ts · evalService.ts</span><span class="ln">extract + compile</span></div>
  <pre class="code"><span class="cm">// 1) Pull each variable's value from the real trace per its mapping (evalService.ts:1152)</span>
<span class="kw">for</span> (<span class="kw">const</span> variable <span class="kw">of</span> variables) {
  <span class="kw">const</span> mapping = variableMapping.find(m =&gt; m.templateVariable === variable);
  <span class="kw">if</span> (mapping.langfuseObject === <span class="st">"trace"</span>) {        <span class="cm">// could also be observation / dataset_item</span>
    <span class="kw">const</span> trace = <span class="kw">await</span> getTraceById({ traceId, projectId, timestamp });
    results.push({ var: variable, value: parseDatabaseRowValue(trace, mapping) });
  }
}

<span class="cm">// 2) Fill the values into the template's {{placeholders}} (evalRuntime.ts:14)</span>
<span class="kw">export function</span> <span class="fn">compileEvalPrompt</span>(params) {
  <span class="kw">const</span> variableMap = Object.fromEntries(
    params.variables.map(({ var: key, value }) =&gt; [key, parseUnknownToString(value)]));
  <span class="kw">return</span> compileTemplateString(params.templatePrompt, variableMap);  <span class="cm">// {{answer}} → actual answer</span>
}</pre>
</div>

<p>Note a detail: extraction <strong>preserves the original data shape</strong> (for code eval, Lesson 31), and only at the <code>compileEvalPrompt</code> boundary—the "feed to the judge LLM" boundary—is it flattened to a string via <code>parseUnknownToString</code>, because a prompt is ultimately text. This restraint—"convert at the boundary, keep raw internally"—is a hallmark of clean data flow.</p>
""")

_EN29.append(r"""
<h2>Structured output and flow-back: how a verdict becomes a score</h2>
<p>The judge LLM can't just return prose—that can't be recorded. Langfuse uses <strong>structured output</strong> to force tidy JSON: per the template's output definition, either <code>{score: number, reasoning}</code> (NUMERIC/BOOLEAN) or <code>{matches: [...], reasoning}</code> (CATEGORICAL). Then <code>toNormalizedScores</code> normalizes it into a score: <strong>value is the score, comment is the judge's reasoning</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="The judge LLM returns a structured score and reasoning; toNormalizedScores normalizes it into a score, which as a source=EVAL SCORE_CREATE event flows back through Lesson 12's ingestion path into the scores wide table, comparable with API and human-sourced scores in the same table">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">structured output → normalize → flow back to ingestion</text>
  <rect x="20" y="42" width="170" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="105" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">judge LLM structured output</text><text x="105" y="80" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">{ score: 0.82,</text><text x="105" y="94" text-anchor="middle" font-size="7.5" fill="var(--accent-ink)">  reasoning: "complete…" }</text><text x="105" y="109" text-anchor="middle" font-size="6.8" fill="var(--muted)">schema-enforced, not free prose</text>
  <rect x="232" y="48" width="150" height="62" rx="10" fill="var(--bg)" stroke="var(--blue)"/><text x="307" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">toNormalizedScores</text><text x="307" y="85" text-anchor="middle" font-size="7" fill="var(--muted)">value ← score</text><text x="307" y="98" text-anchor="middle" font-size="7" fill="var(--muted)">comment ← reasoning</text>
  <rect x="424" y="42" width="150" height="74" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/><text x="499" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">SCORE_CREATE event</text><text x="499" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">source = EVAL</text><text x="499" y="93" text-anchor="middle" font-size="7" fill="var(--accent-ink)">name/value/dataType/comment</text><text x="499" y="107" text-anchor="middle" font-size="6.8" fill="var(--muted)">same event as a hand-written score</text>
  <rect x="600" y="54" width="104" height="50" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="652" y="74" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">scores table</text><text x="652" y="90" text-anchor="middle" font-size="6.4" fill="var(--muted)">3 sources, comparable</text>
  <line x1="190" y1="79" x2="230" y2="79" stroke="var(--blue)" stroke-width="1.5"/><polygon points="230,79 221,75 221,83" fill="var(--blue)"/>
  <line x1="382" y1="79" x2="422" y2="79" stroke="var(--accent)" stroke-width="1.5"/><polygon points="422,79 413,75 413,83" fill="var(--accent)"/>
  <line x1="574" y1="79" x2="598" y2="79" stroke="var(--teal)" stroke-width="1.5"/><polygon points="598,79 589,75 589,83" fill="var(--teal)"/>
  <rect x="120" y="142" width="480" height="50" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="360" y="162" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Key: evaluation isn't a separate pipeline—it's another producer for Lesson 12's ingestion path</text><text x="360" y="180" text-anchor="middle" font-size="7.5" fill="var(--muted)">EVAL scores share the SCORE_CREATE entry with API & ANNOTATION—same dedup/merge/persist</text>
</svg>
<div class="figcap"><b>A judged score and a hand-submitted score are the same event</b>. <code>evalScoreEvent.ts:52</code> wraps the result as a <code>SCORE_CREATE</code> with <code>source: ScoreSourceEnum.EVAL</code>, then runs Lesson 12's ingestion path. So judge-produced scores are inherently <strong>same-table, same-ruler, comparable</strong> with other sources.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalService.ts:953 · evalScoreEvent.ts:52</span><span class="ln">normalize + flow back</span></div>
  <pre class="code"><span class="cm">// normalize: value=score, comment=judge's reasoning (evalService.ts: toNormalizedScores)</span>
<span class="kw">const</span> baseFields = { name: scoreName, comment: outputResult.reasoning };
<span class="kw">if</span> (outputResult.dataType === <span class="st">"NUMERIC"</span>) <span class="kw">return</span> [{ ...baseFields, dataType: <span class="st">"NUMERIC"</span>, value: outputResult.score }];
<span class="kw">if</span> (outputResult.dataType === <span class="st">"BOOLEAN"</span>) <span class="kw">return</span> [{ ...baseFields, dataType: <span class="st">"BOOLEAN"</span>, value: outputResult.score ? 1 : 0 }];

<span class="cm">// flow back: wrap as the exact same SCORE_CREATE event as a hand-written score (evalScoreEvent.ts)</span>
{ type: eventTypes.SCORE_CREATE,
  body: { name: score.name, value: score.value, dataType: score.dataType,
          comment: score.comment, configId: score.configId,
          source: <span class="st">ScoreSourceEnum.EVAL</span>,        <span class="cm">// ← the one "source" marker</span>
          executionTraceId: params.executionTraceId } }</pre>
</div>

<table class="t">
  <thead><tr><th>output definition</th><th>judge returns</th><th>normalized to score</th><th>scores produced</th></tr></thead>
  <tbody>
    <tr><td><b>NUMERIC</b></td><td>{ score: number, reasoning }</td><td>value = score</td><td>1</td></tr>
    <tr><td><b>BOOLEAN</b></td><td>{ score: true/false, reasoning }</td><td>value = score ? 1 : 0</td><td>1</td></tr>
    <tr><td><b>CATEGORICAL</b></td><td>{ matches: [labels…], reasoning }</td><td>one per match, value = that label</td><td>may be many</td></tr>
  </tbody>
</table>
<p>The three output definitions match the score type you pick in the template; note CATEGORICAL's <code>matches</code> is an <strong>array</strong>—one verdict can emit <strong>several</strong> categorical scores (e.g. hitting both "factually correct" and "friendly tone"). Either way, <code>reasoning</code> is dropped verbatim into each score's <code>comment</code>. Source: <code>evalService.ts:953-997</code> <code>toNormalizedScores</code>.</p>
""")

_EN29.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why must the judge use "structured output" instead of free-forming?</strong> Because the product of evaluation must be <strong>recordable, aggregatable, comparable</strong>. If the judge returns prose like "I think this answer is decent but the opening is wordy…", you can neither reliably extract a score nor average across a thousand traces.
  Forcing a <code>{score, reasoning}</code> schema lets the score enter the scores table (aggregatable) while keeping "why this score" in <code>comment</code> (traceable)—<strong>both at once</strong>.<br><br>
  <strong>Deeper: why do eval results flow back through the ingestion path rather than write the DB directly?</strong> This is a recurring Langfuse belief—<strong>"one entry, many producers"</strong>. Whether a score comes from API, human, or a judge LLM, it's wrapped as the same <code>SCORE_CREATE</code> event through Lesson 12's path,
  so dedup, merge, and ClickHouse persistence are written once and consistent for every source. Evaluation is therefore not "another system" but <strong>another upstream of the ingestion pipeline</strong>. And an elegant recursion: the judge's own LLM call is recorded as a Langfuse trace (environment tagged LLMJudge)—<strong>the observability platform observes even its own judge</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>LLM-as-a-judge = use one LLM to score another's output</strong>: between human (accurate but slow) and rules (fast but shallow), it offers automatic, scalable quality assessment.</li>
    <li><strong>Three pieces</strong>: template (prompt+output def+model, "how to rate"), evaluator (target filter+variable mapping+scoreName, "whom to rate"), execution (actually runs once per trace).</li>
    <li><strong>Variable mapping</strong>: each template <code>{{placeholder}}</code> declares which column of trace/observation/dataset_item it comes from; <code>extractVariablesFromTracingData</code> fetches real values at run, and <code>compileEvalPrompt</code> flattens to a string only at the "feed-to-LLM" boundary.</li>
    <li><strong>Structured output</strong>: the judge is forced to return <code>{score, reasoning}</code> (or <code>{matches, reasoning}</code> for categorical); <code>toNormalizedScores</code> normalizes to value=score, comment=reasoning—aggregatable and traceable.</li>
    <li><strong>Flow back (source=EVAL)</strong>: the result is wrapped as the same <code>SCORE_CREATE</code> event through Lesson 12's path. Evaluation is another producer for the ingestion pipeline, not a separate system; the judge's own call is also recorded as a trace.</li>
  </ul>
</div>
""")
LESSON_29 = {"zh": "\n".join(_ZH29), "en": "\n".join(_EN29)}


# ══════════════════════════════════════════════════════════════════════
# L30 · eval 执行流水线 / The eval execution pipeline
# ══════════════════════════════════════════════════════════════════════
_ZH30 = []
_EN30 = []

_ZH30.append(r"""
<p class="lead">
上一课讲了「一次评判怎么跑」，但留了个大问题：<strong>谁来触发它？什么时候？评哪些 trace？</strong> 你不可能给每条 trace 手动点「评估」。这一课讲<strong>调度流水线</strong>——一个 trace 事件进来，系统怎么自动算出「该用哪些评估器评它」、给每个开一张<strong>待办工单</strong>（JobExecution），排进执行队列，最后跑出分。
我们会看到 <code>createEvalJobs</code> 的扇出与匹配、<strong>去重 / 抽样 / 延迟</strong>三个闸门、JobExecution 的<strong>状态生命周期</strong>（PENDING→COMPLETED/ERROR/CANCELLED/DELAYED），以及一个微妙但关键的<strong>无限循环防护</strong>——因为评估本身也产生 trace。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  想象一条工厂流水线的<strong>质检调度</strong>。每当一件产品下线（一个 trace 事件到达），<strong>调度员</strong>（<code>createEvalJobs</code>）翻出所有<strong>启用中的质检规程</strong>（ACTIVE 评估器），逐条问「这件产品符合这条规程的适用范围吗？」（按 filter 匹配 trace）。
  符合的，就开一张<strong>质检工单</strong>（JobExecution，初始 PENDING）放进<strong>排队筐</strong>（执行队列）——但有三道闸：这张工单<strong>已经开过就不重复开</strong>（去重）、按<strong>抽检比例</strong>决定抽不抽（采样）、还能让工单<strong>等一会儿再做</strong>（延迟，等产品彻底定型）。
  若产品在后续工序里<strong>被撤下生产线</strong>（第二个事件让 trace 不再匹配），还没做的工单就<strong>作废</strong>（CANCELLED）。最妙的一道防呆：质检过程本身也会产出一件「产品」（评估也生成 trace），<strong>必须拦住它，否则质检又触发质检，无限套娃</strong>。
</div>
""")

_ZH30.append(r"""
<h2>从一个事件到一队工单：两级队列</h2>
<p>评估是<strong>事件驱动</strong>的。当一条 trace 写入（<code>TraceUpsert</code> 事件，第 14 课那条摄取队列的下游），worker 的「创建器」就跑 <code>createEvalJobs</code>。它不直接评，而是把工作<strong>拆成两级队列</strong>：第一级负责「该评谁」（创建工单），第二级负责「真正评」（执行）。这种分离是这套系统能扛量、能重试、能采样的关键。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="两级队列：trace-upsert 事件触发 createEvalJobs，扇出到项目内所有 ACTIVE 评估器，逐个按 filter 匹配并经去重/采样/延迟闸门，创建 PENDING 的 JobExecution 入执行队列；执行队列消费端跑 LLM-as-a-judge 并在完成时写分、标 COMPLETED">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">两级队列：创建工单 → 执行评估</text>
  <rect x="16" y="40" width="120" height="48" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="76" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">trace 写入</text><text x="76" y="76" text-anchor="middle" font-size="6.8" fill="var(--muted)">TraceUpsert 事件</text>
  <rect x="160" y="34" width="150" height="60" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="235" y="54" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">① 创建器</text><text x="235" y="70" text-anchor="middle" font-size="7" fill="var(--accent-ink)">createEvalJobs</text><text x="235" y="84" text-anchor="middle" font-size="6.6" fill="var(--muted)">扇出到所有 ACTIVE 评估器</text>
  <rect x="160" y="104" width="150" height="92" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="235" y="122" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">逐个评估器</text><text x="235" y="138" text-anchor="middle" font-size="6.8" fill="var(--muted)">filter 匹配 trace？</text><text x="235" y="154" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">闸1 去重</text><text x="235" y="168" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">闸2 采样</text><text x="235" y="182" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">闸3 延迟</text>
  <rect x="356" y="104" width="150" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="431" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② JobExecution</text><text x="431" y="140" text-anchor="middle" font-size="7" fill="var(--muted)">status = PENDING</text><text x="431" y="152" text-anchor="middle" font-size="6.6" fill="var(--muted)">落 Postgres + 入执行队列</text>
  <rect x="356" y="40" width="150" height="50" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-dasharray="4 3"/><text x="431" y="59" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">执行队列</text><text x="431" y="75" text-anchor="middle" font-size="6.6" fill="var(--muted)">EvaluationExecution（可延迟）</text>
  <rect x="552" y="92" width="152" height="80" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="628" y="112" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">③ 执行消费端</text><text x="628" y="128" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">跑 L29 裁判流水线</text><text x="628" y="142" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">写分 → ingestion 队列</text><text x="628" y="158" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">标 COMPLETED + 记 scoreId</text>
  <line x1="136" y1="64" x2="158" y2="64" stroke="var(--teal)" stroke-width="1.5"/><polygon points="158,64 149,60 149,68" fill="var(--teal)"/>
  <line x1="235" y1="94" x2="235" y2="102" stroke="var(--faint)" stroke-width="1.3"/><polygon points="235,104 231,95 239,95" fill="var(--faint)"/>
  <line x1="310" y1="135" x2="354" y2="135" stroke="var(--blue)" stroke-width="1.5"/><polygon points="354,135 345,131 345,139" fill="var(--blue)"/>
  <line x1="431" y1="104" x2="431" y2="92" stroke="var(--faint)" stroke-width="1.3"/><polygon points="431,90 427,99 435,99" fill="var(--teal)"/>
  <line x1="506" y1="80" x2="550" y2="110" stroke="var(--accent)" stroke-width="1.5"/><polygon points="550,110 541,106 544,114" fill="var(--accent)"/>
  <text x="360" y="226" text-anchor="middle" font-size="8" fill="var(--faint)">第一级只决定「该评谁、开不开工单」（轻、快、纯 Postgres）；第二级才真正调 LLM（慢、可能失败、要重试）</text>
  <text x="360" y="242" text-anchor="middle" font-size="8" fill="var(--faint)">两级分离 = 把「调度」与「干活」解耦，各自独立扩容、重试、限流</text>
</svg>
<div class="figcap"><b>创建与执行分离</b>：<code>worker/src/queues/evalQueue.ts</code> 里，<code>TraceUpsert</code>（:25）/<code>CreateEvalQueue</code>（:98）触发 <code>createEvalJobs</code>；它产出 PENDING 工单并入 <code>EvaluationExecution</code> 队列（:126 消费）。大项目还可分流到 <code>EvaluationExecutionSecondaryQueue</code>（:151）隔离。</div>
</div>

<div class="layers">
  <div class="layer l-part"><div class="lh"><span class="badge">扇出</span><span class="name">取出所有启用的评估器</span></div><div class="ld"><code>createEvalJobs</code> 先查这个项目下所有 <code>jobType=EVAL</code>、<code>status=ACTIVE</code>、未被 <code>blockedAt</code> 的 JobConfiguration。一条 trace 可能同时命中多个评估器（如「有用性」+「毒性」），所以是一对多的扇出。若一个都没有，还会<strong>缓存「本项目无评估器」</strong>，省掉后续每条 trace 的空查。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">匹配</span><span class="name">这条 trace 符合评估器的目标吗</span></div><div class="ld">每个评估器都带一个 <strong>filter</strong>（如「环境=production 且 name=chat」）。系统优先<strong>在内存里</strong>用已缓存的 trace 判断（<code>InMemoryFilterService.evaluateFilter</code>，:422）；只有当 filter 需要查库才回 ClickHouse。匹配上才继续，否则跳过。</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">建单</span><span class="name">开一张 PENDING 工单并入队</span></div><div class="ld">过了三道闸（下一节）后，创建一行 <code>JobExecution(status=PENDING)</code> 落 Postgres，并把它的 id 推进执行队列，带上 <code>config.delay</code> 毫秒延迟。工单落库的意义：它是<strong>有状态、可追溯</strong>的——日后能查「这条 trace 被哪些评估器评过、结果如何」。</div></div>
</div>

<p>谁会触发这套创建器？不止「线上来了条新 trace」一种。<code>createEvalJobs</code> 有三个入口（<code>evalQueue.ts</code>），<code>sourceEventType</code> 字段记下它从哪来：</p>
<div class="cols">
  <div class="col"><h4>线上 trace（trace-upsert）</h4><p>最常见：用户的真实调用写入 trace，<code>evalJobTraceCreatorQueueProcessor</code> 接住。这也是那条需要 <code>langfuse-</code> 防循环的入口。</p></div>
  <div class="col"><h4>数据集运行（dataset-run-item-upsert）</h4><p>跑实验时，数据集里每个条目过一遍模型也会触发评估（第 35 课）。<code>evalJobDatasetCreatorQueueProcessor</code> 接住，带 <code>datasetItemId</code>——这就是为什么变量映射能取 dataset_item 的列。</p></div>
  <div class="col"><h4>回填（CreateEvalQueue）</h4><p>新建/改了评估器后，想对<strong>历史</strong> trace 也补评，由这条队列驱动；<code>timeScope</code> 控制一个评估器是只评新数据还是也评历史。</p></div>
</div>
""")

# (L30 sec2 gates below)

_ZH30.append(r"""
<h2>三道闸：去重、采样、延迟</h2>
<p>匹配上了，也不一定立刻开工单。<code>createEvalJobs</code> 在创建前串了三道闸——每一道都解决一个真实的生产问题：</p>

<table class="t">
  <thead><tr><th>闸门</th><th>它问什么</th><th>不通过会怎样</th><th>解决的问题</th></tr></thead>
  <tbody>
    <tr><td><b>① 去重</b></td><td>这条 (评估器, trace) 已经有工单了吗？</td><td>跳过，不再建</td><td>同一 trace 的多个事件（创建、更新）重复触发，不该评好几遍</td></tr>
    <tr><td><b>② 采样</b></td><td><code>Math.random() &gt; config.sampling</code>？</td><td>本次抽不中，跳过</td><td>评估要花 LLM 钱；只抽 10% 的流量评，成本可控</td></tr>
    <tr><td><b>③ 延迟</b></td><td>（不拦截，而是推迟）</td><td>工单带 <code>config.delay</code> 毫秒入队</td><td>等整条 trace 的所有 observation 都到齐了再评，避免评到半截数据</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalService.ts</span><span class="ln">三道闸 + 建单 + 入队</span></div>
  <pre class="code"><span class="cm">// 闸1 去重：批量查过的已有工单里，已存在就不再建</span>
<span class="kw">if</span> (existingJob.length &gt; 0) { logger.debug(<span class="st">"already exists"</span>); <span class="kw">continue</span>; }

<span class="cm">// 闸2 采样：sampling∈[0,1] 是抽中概率，抽不中就跳过</span>
<span class="kw">if</span> (Number(config.sampling) !== 1) {
  <span class="kw">if</span> (Math.random() &gt; Number(config.sampling)) { <span class="kw">continue</span>; }   <span class="cm">// sampled out</span>
}

<span class="cm">// 建单：一行 PENDING 的 JobExecution 落 Postgres</span>
<span class="kw">await</span> prisma.jobExecution.create({ data: {
  id: jobExecutionId, projectId, jobConfigurationId: config.id,
  jobInputTraceId: event.traceId, jobTemplateId: config.evalTemplateId,
  status: <span class="st">"PENDING"</span>, startTime: <span class="kw">new</span> Date() } });

<span class="cm">// 闸3 延迟：推进执行队列时带上 config.delay 毫秒</span>
<span class="kw">await</span> EvalExecutionQueue.getInstance({ shardingKey })?.add(
  QueueName.EvaluationExecution,
  { payload: { projectId, jobExecutionId, delay: config.delay } },
  { delay: config.delay });   <span class="cm">// 毫秒</span></pre>
</div>

<p>还有一道「反向闸」：如果某条 trace 后来<strong>不再匹配</strong>评估器的 filter（第二个 trace 事件改了它的属性，把它「踢出」目标集合），而它之前已有工单，系统会把那张<strong>还没跑完的工单标成 CANCELLED</strong>（用 <code>updateMany</code> 且排除 COMPLETED，避免误改已完成的）。评估的目标集合是<strong>动态</strong>的——选中了能取消，这让调度对「数据后到、属性后改」很有韧性。</p>
""")

# (L30 sec3 lifecycle below)

_ZH30.append(r"""
<h2>工单的一生：状态机与无限循环防护</h2>
<p>JobExecution 是一台<strong>状态机</strong>。它出生于 PENDING，命运有四种终局；中间还可能因限流而 DELAYED 后重试。下图是它的完整生命周期：</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="JobExecution 状态机：PENDING 创建后进入执行；成功则 COMPLETED 并记录产出的 scoreId；非可重试错误或重试预算耗尽则 ERROR；被后续事件取消选中则 CANCELLED；遇限流则 DELAYED 约 120 分钟后重试回到执行">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">JobExecution 状态生命周期</text>
  <rect x="40" y="100" width="110" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="95" y="120" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">PENDING</text><text x="95" y="135" text-anchor="middle" font-size="6.6" fill="var(--muted)">建单时</text>
  <rect x="220" y="100" width="120" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="280" y="120" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">执行中</text><text x="280" y="135" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">跑 L29 裁判</text>
  <rect x="420" y="34" width="130" height="44" rx="9" fill="var(--teal)" opacity="0.18" stroke="var(--teal)" stroke-width="2"/><text x="485" y="53" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">COMPLETED ✓</text><text x="485" y="68" text-anchor="middle" font-size="6.4" fill="var(--muted)">记 jobOutputScoreId</text>
  <rect x="420" y="92" width="130" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="485" y="110" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">DELAYED</text><text x="485" y="124" text-anchor="middle" font-size="6.2" fill="var(--muted)">限流，~120min 后重试</text>
  <rect x="420" y="146" width="130" height="40" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="485" y="164" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ERROR ✗</text><text x="485" y="178" text-anchor="middle" font-size="6.2" fill="var(--muted)">不可重试/预算耗尽</text>
  <rect x="220" y="170" width="120" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="280" y="188" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">CANCELLED</text><text x="280" y="201" text-anchor="middle" font-size="6.2" fill="var(--muted)">被后续事件取消选中</text>
  <line x1="150" y1="123" x2="218" y2="123" stroke="var(--accent)" stroke-width="1.6"/><polygon points="218,123 209,119 209,127" fill="var(--accent)"/>
  <line x1="340" y1="110" x2="418" y2="62" stroke="var(--teal)" stroke-width="1.6"/><polygon points="418,62 408,62 412,70" fill="var(--teal)"/>
  <line x1="340" y1="118" x2="418" y2="112" stroke="var(--faint)" stroke-width="1.4"/><polygon points="418,112 409,108 409,116" fill="var(--faint)"/>
  <line x1="340" y1="130" x2="418" y2="162" stroke="var(--accent)" stroke-width="1.4"/><polygon points="418,162 409,158 408,166" fill="var(--accent)"/>
  <path d="M 485 92 Q 380 70 300 100" fill="none" stroke="var(--teal)" stroke-width="1.3" stroke-dasharray="3 2"/><polygon points="300,100 309,97 305,92" fill="var(--teal)"/><text x="392" y="80" text-anchor="middle" font-size="6.2" fill="var(--teal)">重试回执行</text>
  <line x1="120" y1="146" x2="250" y2="168" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="4 3"/><polygon points="250,168 240,166 243,174" fill="var(--faint)"/>
  <text x="360" y="230" text-anchor="middle" font-size="8" fill="var(--faint)">四种终局 + 一个可重试中间态；DELAYED→执行的环让限流不致命，而是「稍后再试」</text>
</svg>
<div class="figcap"><b>状态枚举来自真实 schema</b>：<code>JobExecutionStatus = { COMPLETED, ERROR, PENDING, CANCELLED, DELAYED }</code>（<code>schema.prisma:1080-1086</code>）。完成时 <code>evalCompletion.ts:82-92</code> 把分写进 ingestion 队列、再把工单标 COMPLETED 并填 <code>jobOutputScoreId</code> 与 <code>executionTraceId</code>——工单从此<strong>双向链接</strong>到「它产出的分」和「裁判自己的 trace」。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalService.ts:240 · evalCompletion.ts:82</span><span class="ln">防循环 + 收尾</span></div>
  <pre class="code"><span class="cm">// 无限循环防护：来自 trace-upsert 且环境以 "langfuse" 开头的内部 trace，直接不建评估工单</span>
<span class="cm">// 否则：用户 trace → 评估 → 评估自己的 trace → 又触发评估 → 无限套娃</span>
<span class="kw">if</span> (sourceEventType === <span class="st">"trace-upsert"</span> &amp;&amp;
    event.traceEnvironment?.startsWith(<span class="st">"langfuse"</span>)) {
  <span class="kw">return</span>;   <span class="cm">// 跳过：这是评估自身产生的 trace</span>
}

<span class="cm">// 收尾：分写进 ingestion 队列，工单标 COMPLETED 并双向链接产出物</span>
<span class="kw">await</span> deps.enqueueScoreIngestion({ projectId, scoreId, eventId });
<span class="kw">await</span> deps.updateJobExecution({ id: jobExecutionId, projectId, data: {
  status: <span class="st">"COMPLETED"</span>, endTime: <span class="kw">new</span> Date(),
  jobOutputScoreId,                       <span class="cm">// ← 链到「评出的那条分」</span>
  executionTraceId: result.executionTraceId } });  <span class="cm">// ← 链到「裁判自己的 trace」</span></pre>
</div>
""")

# (L30 spark+key below)

_ZH30.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么要拆成「创建」和「执行」两级队列，而不是一步评完？</strong> 因为这两件事的<strong>性质截然不同</strong>。创建（匹配、去重、采样）是<strong>轻、快、纯数据库</strong>的活，失败了重跑代价小；执行（调 LLM）是<strong>慢、花钱、会被限流、可能超时</strong>的活。
  混在一起，慢的会拖死快的、贵的没法单独采样、失败的没法独立重试。拆开后：第一级可以高吞吐地决定「该评谁」，第二级可以带<strong>延迟、采样、独立重试、甚至分流到二级队列</strong>地慢慢消化。这正是第 14 课「队列解耦」思想在评估域的复刻。<br><br>
  <strong>为什么 JobExecution 必须落 Postgres，而不只是一条队列消息？</strong> 因为它要<strong>有状态、可追溯、可去重、可取消</strong>。队列消息是「阅后即焚」的，但工单要回答「这条 trace 被哪些评估器评过、跑成功没、产出哪条分」——这些都需要一行<strong>持久、可更新</strong>的记录。<code>jobOutputScoreId</code> 和 <code>executionTraceId</code> 两个外链，让你能从「一条分」反查「哪个工单、哪个评估器、哪次裁判调用产生了它」，<strong>全链路可审计</strong>。<br><br>
  <strong>最微妙的一处：无限循环防护。</strong> 评估本身要调 LLM，而 Langfuse 会观测每一次 LLM 调用——于是裁判的调用<strong>也变成一条 trace</strong>。若不拦截，这条「评估产生的 trace」又会触发评估，套娃到天荒地老。Langfuse 的解法是给内部 trace 打上 <code>langfuse-</code> 环境前缀，并在创建器入口直接挡掉。<strong>一个能观测一切的系统，必须小心别把自己卷进去</strong>——这是自指系统的经典陷阱。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>评估是事件驱动的</strong>：trace 写入（TraceUpsert）触发 <code>createEvalJobs</code>，把一条 trace 扇出到项目内所有 ACTIVE 评估器，一对多创建工单。</li>
    <li><strong>两级队列</strong>：第一级「创建器」轻快地决定「该评谁」（匹配+建单），第二级「执行队列」带延迟/采样/重试地真正调 LLM——解耦让系统能扛量、能重试、能限流。</li>
    <li><strong>三道闸</strong>：去重（同 trace 多事件不重复评）、采样（<code>config.sampling</code> 概率控成本）、延迟（<code>config.delay</code> 等数据到齐）；外加反向的「取消」（后续事件让 trace 不再匹配 → CANCELLED）。</li>
    <li><strong>filter 匹配优先在内存做</strong>：用缓存的 trace + <code>InMemoryFilterService.evaluateFilter</code>，只有复杂过滤才回 ClickHouse 查——省一次次的库查。</li>
    <li><strong>JobExecution 是落库的状态机</strong>：PENDING→COMPLETED/ERROR/CANCELLED，限流则 DELAYED 后重试；完成时双向链接 <code>jobOutputScoreId</code> 与 <code>executionTraceId</code>，全链路可审计。</li>
    <li><strong>无限循环防护</strong>：评估自身的 LLM 调用也会成为 trace；用 <code>langfuse-</code> 环境前缀在创建器入口挡掉，避免「评估触发评估」的自指套娃。</li>
  </ul>
</div>
""")

_EN30.append(r"""
<p class="lead">
Last lesson covered "how one verdict runs", but left a big question: <strong>who triggers it? when? which traces get evaluated?</strong> You can't click "evaluate" on every trace by hand. This lesson is the <strong>scheduling pipeline</strong>—how a trace event automatically fans out into "which evaluators should judge it", opens a <strong>work ticket</strong> (JobExecution) for each, queues it, and finally produces a score.
We'll see <code>createEvalJobs</code>' fan-out and matching, the three gates of <strong>dedup / sampling / delay</strong>, JobExecution's <strong>status lifecycle</strong> (PENDING→COMPLETED/ERROR/CANCELLED/DELAYED), and a subtle but crucial <strong>infinite-loop safeguard</strong>—because evaluation itself produces traces.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Picture the <strong>QC dispatch</strong> on a factory line. Each time a product rolls off (a trace event arrives), the <strong>dispatcher</strong> (<code>createEvalJobs</code>) pulls out all <strong>active QC procedures</strong> (ACTIVE evaluators) and asks of each "does this product fall within this procedure's scope?" (match the trace by filter).
  For matches, it opens a <strong>QC ticket</strong> (JobExecution, initially PENDING) into a <strong>queue basket</strong> (the execution queue)—but through three gates: <strong>don't re-open a ticket already opened</strong> (dedup), <strong>decide by sampling rate</strong> whether to inspect at all (sampling), and <strong>let the ticket wait a bit</strong> before doing it (delay, until the product fully sets).
  If the product is later <strong>pulled off the line</strong> (a second event makes the trace no longer match), an un-run ticket is <strong>voided</strong> (CANCELLED). The neatest fail-safe: the QC process itself yields a "product" (evaluation also generates a trace), and you <strong>must stop it, or QC triggers QC, nesting forever</strong>.
</div>
""")

_EN30.append(r"""
<h2>From one event to a queue of tickets: two-stage queues</h2>
<p>Evaluation is <strong>event-driven</strong>. When a trace is written (a <code>TraceUpsert</code> event, downstream of Lesson 14's ingestion queue), the worker's "creator" runs <code>createEvalJobs</code>. It doesn't evaluate directly—it splits the work into <strong>two queue stages</strong>: the first decides "whom to evaluate" (create tickets), the second does "the actual judging" (execution). This separation is the key to scaling, retrying, and sampling.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Two-stage queues: a trace-upsert event triggers createEvalJobs, fanning out to all ACTIVE evaluators in the project; each is matched by filter and passes dedup/sampling/delay gates, creating a PENDING JobExecution into the execution queue; the execution consumer runs LLM-as-a-judge and on completion writes the score and marks COMPLETED">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Two-stage queues: create tickets → execute evaluation</text>
  <rect x="16" y="40" width="120" height="48" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="76" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">trace written</text><text x="76" y="76" text-anchor="middle" font-size="6.8" fill="var(--muted)">TraceUpsert event</text>
  <rect x="160" y="34" width="150" height="60" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="235" y="54" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">① creator</text><text x="235" y="70" text-anchor="middle" font-size="7" fill="var(--accent-ink)">createEvalJobs</text><text x="235" y="84" text-anchor="middle" font-size="6.6" fill="var(--muted)">fan out to all ACTIVE evaluators</text>
  <rect x="160" y="104" width="150" height="92" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="235" y="122" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">per evaluator</text><text x="235" y="138" text-anchor="middle" font-size="6.8" fill="var(--muted)">filter matches trace?</text><text x="235" y="154" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">gate1 dedup</text><text x="235" y="168" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">gate2 sampling</text><text x="235" y="182" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">gate3 delay</text>
  <rect x="356" y="104" width="150" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="431" y="124" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">② JobExecution</text><text x="431" y="140" text-anchor="middle" font-size="7" fill="var(--muted)">status = PENDING</text><text x="431" y="152" text-anchor="middle" font-size="6.6" fill="var(--muted)">Postgres row + into exec queue</text>
  <rect x="356" y="40" width="150" height="50" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-dasharray="4 3"/><text x="431" y="59" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">execution queue</text><text x="431" y="75" text-anchor="middle" font-size="6.6" fill="var(--muted)">EvaluationExecution (delayable)</text>
  <rect x="552" y="92" width="152" height="80" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="628" y="112" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">③ exec consumer</text><text x="628" y="128" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">runs the L29 judge pipeline</text><text x="628" y="142" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">write score → ingestion queue</text><text x="628" y="158" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">mark COMPLETED + record scoreId</text>
  <line x1="136" y1="64" x2="158" y2="64" stroke="var(--teal)" stroke-width="1.5"/><polygon points="158,64 149,60 149,68" fill="var(--teal)"/>
  <line x1="235" y1="94" x2="235" y2="102" stroke="var(--faint)" stroke-width="1.3"/><polygon points="235,104 231,95 239,95" fill="var(--faint)"/>
  <line x1="310" y1="135" x2="354" y2="135" stroke="var(--blue)" stroke-width="1.5"/><polygon points="354,135 345,131 345,139" fill="var(--blue)"/>
  <line x1="431" y1="104" x2="431" y2="92" stroke="var(--faint)" stroke-width="1.3"/><polygon points="431,90 427,99 435,99" fill="var(--teal)"/>
  <line x1="506" y1="80" x2="550" y2="110" stroke="var(--accent)" stroke-width="1.5"/><polygon points="550,110 541,106 544,114" fill="var(--accent)"/>
  <text x="360" y="226" text-anchor="middle" font-size="8" fill="var(--faint)">stage one only decides "whom to evaluate, open a ticket?" (light, fast, pure Postgres); stage two calls the LLM (slow, may fail, must retry)</text>
  <text x="360" y="242" text-anchor="middle" font-size="8" fill="var(--faint)">two-stage split = decouple "scheduling" from "doing the work", each scaling/retrying/rate-limiting independently</text>
</svg>
<div class="figcap"><b>Creation and execution split</b>: in <code>worker/src/queues/evalQueue.ts</code>, <code>TraceUpsert</code> (:25)/<code>CreateEvalQueue</code> (:98) trigger <code>createEvalJobs</code>; it emits PENDING tickets into the <code>EvaluationExecution</code> queue (consumed at :126). Large projects can also offload to <code>EvaluationExecutionSecondaryQueue</code> (:151) for isolation.</div>
</div>

<div class="layers">
  <div class="layer l-part"><div class="lh"><span class="badge">fan-out</span><span class="name">pull all active evaluators</span></div><div class="ld"><code>createEvalJobs</code> first queries all JobConfigurations in this project with <code>jobType=EVAL</code>, <code>status=ACTIVE</code>, not <code>blockedAt</code>. One trace may hit several evaluators at once (e.g. "helpfulness" + "toxicity"), so it's a one-to-many fan-out. If there are none, it <strong>caches "no evaluators for this project"</strong> to skip the empty query on every future trace.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">match</span><span class="name">does this trace fit the evaluator's target</span></div><div class="ld">Each evaluator carries a <strong>filter</strong> (e.g. "environment=production and name=chat"). The system prefers to judge <strong>in memory</strong> using the cached trace (<code>InMemoryFilterService.evaluateFilter</code>, :422); only when the filter needs a DB lookup does it go back to ClickHouse. Continue only on a match, else skip.</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">create</span><span class="name">open a PENDING ticket and enqueue</span></div><div class="ld">After the three gates (next section), it creates a <code>JobExecution(status=PENDING)</code> row in Postgres and pushes its id into the execution queue with a <code>config.delay</code> ms delay. Why persist the ticket: it is <strong>stateful and auditable</strong>—later you can ask "which evaluators evaluated this trace, and with what outcome".</div></div>
</div>

<p>Who triggers this creator? Not only "a new trace arrived live". <code>createEvalJobs</code> has three entry points (<code>evalQueue.ts</code>), and a <code>sourceEventType</code> field records where it came from:</p>
<div class="cols">
  <div class="col"><h4>live trace (trace-upsert)</h4><p>The common case: a user's real call writes a trace, caught by <code>evalJobTraceCreatorQueueProcessor</code>. This is also the entry needing the <code>langfuse-</code> loop guard.</p></div>
  <div class="col"><h4>dataset run (dataset-run-item-upsert)</h4><p>When running experiments, each dataset item passing through the model also triggers evaluation (Lesson 35). Caught by <code>evalJobDatasetCreatorQueueProcessor</code> with a <code>datasetItemId</code>—which is why variable mapping can read dataset_item columns.</p></div>
  <div class="col"><h4>backfill (CreateEvalQueue)</h4><p>After creating/changing an evaluator, to also score <strong>historic</strong> traces, this queue drives it; <code>timeScope</code> controls whether an evaluator scores only new data or history too.</p></div>
</div>
""")

# (en sec2/3/spark below)

_EN30.append(r"""
<h2>Three gates: dedup, sampling, delay</h2>
<p>A match doesn't mean a ticket opens immediately. Before creating, <code>createEvalJobs</code> chains three gates—each solving a real production problem:</p>

<table class="t">
  <thead><tr><th>gate</th><th>what it asks</th><th>if it fails</th><th>problem solved</th></tr></thead>
  <tbody>
    <tr><td><b>① dedup</b></td><td>does a ticket for this (evaluator, trace) already exist?</td><td>skip, don't create</td><td>multiple events on the same trace (create, update) shouldn't trigger several evals</td></tr>
    <tr><td><b>② sampling</b></td><td><code>Math.random() &gt; config.sampling</code>?</td><td>not sampled in, skip</td><td>evaluation costs LLM money; sampling only 10% keeps cost in check</td></tr>
    <tr><td><b>③ delay</b></td><td>(doesn't block, defers)</td><td>ticket enqueued with <code>config.delay</code> ms</td><td>wait until all of a trace's observations have arrived, to avoid judging half the data</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalService.ts</span><span class="ln">three gates + create + enqueue</span></div>
  <pre class="code"><span class="cm">// gate1 dedup: from the batch-queried existing tickets, skip if one exists</span>
<span class="kw">if</span> (existingJob.length &gt; 0) { logger.debug(<span class="st">"already exists"</span>); <span class="kw">continue</span>; }

<span class="cm">// gate2 sampling: sampling∈[0,1] is the keep probability; skip if not sampled</span>
<span class="kw">if</span> (Number(config.sampling) !== 1) {
  <span class="kw">if</span> (Math.random() &gt; Number(config.sampling)) { <span class="kw">continue</span>; }   <span class="cm">// sampled out</span>
}

<span class="cm">// create: one PENDING JobExecution row in Postgres</span>
<span class="kw">await</span> prisma.jobExecution.create({ data: {
  id: jobExecutionId, projectId, jobConfigurationId: config.id,
  jobInputTraceId: event.traceId, jobTemplateId: config.evalTemplateId,
  status: <span class="st">"PENDING"</span>, startTime: <span class="kw">new</span> Date() } });

<span class="cm">// gate3 delay: push to the execution queue with config.delay ms</span>
<span class="kw">await</span> EvalExecutionQueue.getInstance({ shardingKey })?.add(
  QueueName.EvaluationExecution,
  { payload: { projectId, jobExecutionId, delay: config.delay } },
  { delay: config.delay });   <span class="cm">// milliseconds</span></pre>
</div>

<p>There's also a "reverse gate": if a trace later <strong>no longer matches</strong> the evaluator's filter (a second trace event changed its attributes, kicking it out of the target set) and it already had a ticket, the system marks that <strong>un-run ticket CANCELLED</strong> (via <code>updateMany</code> excluding COMPLETED, to avoid touching finished ones). The evaluation target set is <strong>dynamic</strong>—selected can become deselected, making scheduling resilient to "data arriving late, attributes changing late".</p>
""")

_EN30.append(r"""
<h2>A ticket's life: the state machine and the infinite-loop safeguard</h2>
<p>JobExecution is a <strong>state machine</strong>. It is born PENDING, with four possible endings; in between it may go DELAYED on rate-limit and retry. Below is its full lifecycle:</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="JobExecution state machine: PENDING after creation enters execution; success becomes COMPLETED recording the produced scoreId; a non-retryable error or exhausted retry budget becomes ERROR; deselected by a later event becomes CANCELLED; a rate-limit becomes DELAYED retrying after about 120 minutes back into execution">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">JobExecution status lifecycle</text>
  <rect x="40" y="100" width="110" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="95" y="120" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">PENDING</text><text x="95" y="135" text-anchor="middle" font-size="6.6" fill="var(--muted)">on create</text>
  <rect x="220" y="100" width="120" height="46" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="280" y="120" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">executing</text><text x="280" y="135" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">runs the L29 judge</text>
  <rect x="420" y="34" width="130" height="44" rx="9" fill="var(--teal)" opacity="0.18" stroke="var(--teal)" stroke-width="2"/><text x="485" y="53" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">COMPLETED ✓</text><text x="485" y="68" text-anchor="middle" font-size="6.4" fill="var(--muted)">records jobOutputScoreId</text>
  <rect x="420" y="92" width="130" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="485" y="110" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">DELAYED</text><text x="485" y="124" text-anchor="middle" font-size="6.0" fill="var(--muted)">rate-limit, retry ~120min</text>
  <rect x="420" y="146" width="130" height="40" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="485" y="164" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ERROR ✗</text><text x="485" y="178" text-anchor="middle" font-size="6.0" fill="var(--muted)">non-retryable/budget out</text>
  <rect x="220" y="170" width="120" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="280" y="188" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">CANCELLED</text><text x="280" y="201" text-anchor="middle" font-size="6.0" fill="var(--muted)">deselected by later event</text>
  <line x1="150" y1="123" x2="218" y2="123" stroke="var(--accent)" stroke-width="1.6"/><polygon points="218,123 209,119 209,127" fill="var(--accent)"/>
  <line x1="340" y1="110" x2="418" y2="62" stroke="var(--teal)" stroke-width="1.6"/><polygon points="418,62 408,62 412,70" fill="var(--teal)"/>
  <line x1="340" y1="118" x2="418" y2="112" stroke="var(--faint)" stroke-width="1.4"/><polygon points="418,112 409,108 409,116" fill="var(--faint)"/>
  <line x1="340" y1="130" x2="418" y2="162" stroke="var(--accent)" stroke-width="1.4"/><polygon points="418,162 409,158 408,166" fill="var(--accent)"/>
  <path d="M 485 92 Q 380 70 300 100" fill="none" stroke="var(--teal)" stroke-width="1.3" stroke-dasharray="3 2"/><polygon points="300,100 309,97 305,92" fill="var(--teal)"/><text x="392" y="80" text-anchor="middle" font-size="6.2" fill="var(--teal)">retry back to exec</text>
  <line x1="120" y1="146" x2="250" y2="168" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="4 3"/><polygon points="250,168 240,166 243,174" fill="var(--faint)"/>
  <text x="360" y="230" text-anchor="middle" font-size="8" fill="var(--faint)">four endings + one retryable middle state; the DELAYED→exec loop makes rate-limits non-fatal, just "try later"</text>
</svg>
<div class="figcap"><b>The status enum is from the real schema</b>: <code>JobExecutionStatus = { COMPLETED, ERROR, PENDING, CANCELLED, DELAYED }</code> (<code>schema.prisma:1080-1086</code>). On success <code>evalCompletion.ts:82-92</code> writes the score into the ingestion queue, then marks the ticket COMPLETED and fills <code>jobOutputScoreId</code> and <code>executionTraceId</code>—the ticket is now <strong>bidirectionally linked</strong> to "the score it produced" and "the judge's own trace".</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/evaluation/evalService.ts:240 · evalCompletion.ts:82</span><span class="ln">loop guard + finish</span></div>
  <pre class="code"><span class="cm">// loop guard: internal traces from trace-upsert whose env starts with "langfuse" → create no eval ticket</span>
<span class="cm">// otherwise: user trace → eval → eval's own trace → triggers eval again → nesting forever</span>
<span class="kw">if</span> (sourceEventType === <span class="st">"trace-upsert"</span> &amp;&amp;
    event.traceEnvironment?.startsWith(<span class="st">"langfuse"</span>)) {
  <span class="kw">return</span>;   <span class="cm">// skip: this is a trace produced by evaluation itself</span>
}

<span class="cm">// finish: score into the ingestion queue, ticket marked COMPLETED and bidirectionally linked</span>
<span class="kw">await</span> deps.enqueueScoreIngestion({ projectId, scoreId, eventId });
<span class="kw">await</span> deps.updateJobExecution({ id: jobExecutionId, projectId, data: {
  status: <span class="st">"COMPLETED"</span>, endTime: <span class="kw">new</span> Date(),
  jobOutputScoreId,                       <span class="cm">// ← links to "the score produced"</span>
  executionTraceId: result.executionTraceId } });  <span class="cm">// ← links to "the judge's own trace"</span></pre>
</div>
""")

_EN30.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why split into "creation" and "execution" queues rather than evaluate in one step?</strong> Because the two are <strong>fundamentally different</strong>. Creation (matching, dedup, sampling) is <strong>light, fast, pure-database</strong> work, cheap to re-run on failure; execution (calling the LLM) is <strong>slow, costly, rate-limited, may time out</strong>.
  Mixed together, the slow drags down the fast, the expensive can't be sampled separately, and failures can't be retried independently. Split: stage one decides "whom to evaluate" at high throughput, stage two digests slowly with <strong>delay, sampling, independent retry, even offload to a secondary queue</strong>. This is Lesson 14's "queue decoupling" replayed in the eval domain.<br><br>
  <strong>Why must a JobExecution live in Postgres, not just be a queue message?</strong> Because it must be <strong>stateful, auditable, dedup-able, cancellable</strong>. A queue message is "read once, gone", but a ticket must answer "which evaluators evaluated this trace, did it succeed, which score did it produce"—all needing a <strong>durable, updatable</strong> row. The two foreign links <code>jobOutputScoreId</code> and <code>executionTraceId</code> let you trace from "a score" back to "which ticket, which evaluator, which judge call produced it"—<strong>fully auditable end to end</strong>.<br><br>
  <strong>The subtlest part: the infinite-loop safeguard.</strong> Evaluation calls the LLM, and Langfuse observes every LLM call—so the judge's call <strong>becomes a trace too</strong>. Unstopped, that "eval-produced trace" would trigger evaluation again, nesting endlessly. Langfuse's fix: tag internal traces with a <code>langfuse-</code> environment prefix and block them right at the creator's entry. <strong>A system that can observe everything must be careful not to observe itself into a loop</strong>—the classic trap of self-referential systems.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Evaluation is event-driven</strong>: a trace write (TraceUpsert) triggers <code>createEvalJobs</code>, fanning one trace out to all ACTIVE evaluators in the project, creating tickets one-to-many.</li>
    <li><strong>Two-stage queues</strong>: stage one "creator" lightly decides "whom to evaluate" (match + create ticket), stage two "execution queue" actually calls the LLM with delay/sampling/retry—decoupling lets the system scale, retry, and rate-limit.</li>
    <li><strong>Three gates</strong>: dedup (multiple events on one trace don't re-evaluate), sampling (<code>config.sampling</code> probability to control cost), delay (<code>config.delay</code> to wait for data); plus a reverse "cancel" (a later event makes the trace no longer match → CANCELLED).</li>
    <li><strong>Filter matching prefers memory</strong>: cached trace + <code>InMemoryFilterService.evaluateFilter</code>, going back to ClickHouse only for complex filters—saving repeated DB queries.</li>
    <li><strong>JobExecution is a persisted state machine</strong>: PENDING→COMPLETED/ERROR/CANCELLED, or DELAYED then retry on rate-limit; on completion it bidirectionally links <code>jobOutputScoreId</code> and <code>executionTraceId</code>—auditable end to end.</li>
    <li><strong>Infinite-loop safeguard</strong>: evaluation's own LLM call also becomes a trace; a <code>langfuse-</code> environment prefix blocks it at the creator's entry, avoiding "eval triggers eval" self-referential nesting.</li>
  </ul>
</div>
""")

LESSON_30 = {"zh": "\n".join(_ZH30), "en": "\n".join(_EN30)}
