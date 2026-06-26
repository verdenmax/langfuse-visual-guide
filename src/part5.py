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


# ══════════════════════════════════════════════════════════════════════
# L31 · 代码 eval / Code-based evaluation
# ══════════════════════════════════════════════════════════════════════
_ZH31 = []
_EN31 = []

_ZH31.append(r"""
<p class="lead">
不是所有「好不好」都得请 LLM 来判。很多质量信号是<strong>客观、确定</strong>的：回答是不是合法 JSON？有没有泄露邮箱地址？长度超没超限？字段齐不齐？这些根本不需要一个会胡思乱想的裁判——写<strong>一段代码</strong>算就行，确定、快、还不花 LLM 的钱。这就是<strong>代码 eval（code-based evaluation）</strong>。
但这里藏着一个尖锐的问题：评估器的代码是<strong>用户写的</strong>，平台要去<strong>执行别人的代码</strong>——这是天大的安全风险。所以这一课的主角是两样东西：一个把「在哪跑、怎么跑」抽象掉的 <strong>dispatcher（派发器）</strong>，和一个把用户代码关起来跑的<strong>沙箱</strong>。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  上一课的 LLM-as-judge 像请一位<strong>人类评委</strong>：主观、有判断力，但每次可能给不同的分、还得付出场费。代码 eval 则像用一把<strong>标准量规 / 卡尺</strong>：客观、同一个零件量一百次都是同一个读数、几乎不要钱。
  量规适合量「尺寸合不合格」这种<strong>确定</strong>的事，评委适合判「设计美不美」这种<strong>主观</strong>的事——两者互补，不是替代。
  但有个麻烦：这把卡尺是<strong>别人寄来的</strong>，你不敢直接插到主控机上用（万一它内藏恶意指令？）。稳妥做法是放进一间<strong>隔离的检验室</strong>（沙箱）里跑，门一关、还掐断电话线（禁网络）——它只能量你递进去的零件、把读数递出来，<strong>碰不到外面任何东西</strong>。
</div>
""")

_ZH31.append(r"""
<h2>两种裁判：确定的代码 vs 概率的 LLM</h2>
<p>第 29、31 课其实是<strong>同一个 score 的两种生产方式</strong>。它们都接在第 30 课那条调度流水线后面——区别只在「执行」那一步：LLM-as-judge 调一个模型，代码 eval 跑一段函数。选哪种，取决于你要评的东西是<strong>主观</strong>还是<strong>客观</strong>：</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="同一条 trace 可走两条评判路径：LLM-as-judge 调用一个模型做主观、语义的判断；代码 eval 在沙箱里跑一段确定性函数做客观、规则的判断；两条路最终都产出 source=EVAL 的 score 落进同一张 scores 表">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一条 trace，两种评判，殊途同归</text>
  <rect x="290" y="36" width="140" height="40" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="360" y="55" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">一条 trace 的输入/输出</text><text x="360" y="69" text-anchor="middle" font-size="6.8" fill="var(--muted)">待评的回答</text>
  <rect x="40" y="96" width="280" height="62" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="180" y="115" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">LLM-as-judge（第 29 课）</text><text x="180" y="132" text-anchor="middle" font-size="7.2" fill="var(--accent-ink)">概率的 · 主观/语义 · 花 LLM 钱</text><text x="180" y="147" text-anchor="middle" font-size="6.8" fill="var(--muted)">有用性 / 语气 / 是否答非所问</text>
  <rect x="400" y="96" width="280" height="62" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="540" y="115" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">代码 eval（本课）</text><text x="540" y="132" text-anchor="middle" font-size="7.2" fill="var(--muted)">确定的 · 客观/规则 · 几乎免费</text><text x="540" y="147" text-anchor="middle" font-size="6.8" fill="var(--faint)">合法 JSON / 含邮箱 / 长度 / 精确匹配</text>
  <rect x="270" y="176" width="180" height="28" rx="8" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="360" y="194" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">都产出 source=EVAL 的 score</text>
  <line x1="320" y1="66" x2="200" y2="94" stroke="var(--accent)" stroke-width="1.4"/><polygon points="200,94 209,90 205,86" fill="var(--accent)"/>
  <line x1="400" y1="66" x2="520" y2="94" stroke="var(--blue)" stroke-width="1.4"/><polygon points="520,94 515,86 511,90" fill="var(--blue)"/>
  <line x1="180" y1="158" x2="300" y2="176" stroke="var(--faint)" stroke-width="1.3"/><polygon points="300,176 291,173 294,181" fill="var(--faint)"/>
  <line x1="540" y1="158" x2="420" y2="176" stroke="var(--faint)" stroke-width="1.3"/><polygon points="420,176 429,173 426,181" fill="var(--faint)"/>
</svg>
<div class="figcap"><b>互补，不是替代</b>：能用规则说清的（格式、长度、关键词、精确匹配）交给代码 eval——确定、快、免费；说不清、要语义理解的（有用性、语气、相关性）交给 LLM-as-judge。两者都接第 30 课调度流水线，只是「执行」步不同。</div>
</div>

<table class="t">
  <thead><tr><th>维度</th><th>LLM-as-judge（第 29 课）</th><th>代码 eval（本课）</th></tr></thead>
  <tbody>
    <tr><td>评判方式</td><td>调一个模型做语义判断</td><td>跑一段你写的函数</td></tr>
    <tr><td>确定性</td><td>概率的（同输入可能不同分）</td><td><b>确定的</b>（同输入恒同分）</td></tr>
    <tr><td>擅长</td><td>主观：有用性、语气、相关性</td><td>客观：合法 JSON、含 PII、长度、精确/正则匹配</td></tr>
    <tr><td>成本/速度</td><td>每次一次 LLM 调用，慢、花钱</td><td>一次函数执行，快、几乎免费</td></tr>
    <tr><td>风险</td><td>模型会错判、有偏好</td><td>要执行<b>用户代码</b>→必须沙箱隔离</td></tr>
  </tbody>
</table>
""")

# (L31 sec2 dispatcher below)

_ZH31.append(r"""
<h2>dispatcher：把「在哪跑」抽象掉的策略模式</h2>
<p>worker 不该关心用户代码到底跑在 AWS Lambda 还是本地——它只想说一句「把这段代码连同输入跑一下，给我分数」。这就是 <strong>dispatcher 接口</strong>：一个极简的契约 <code>{ name, dispatch(input) }</code>。底下挂着两个实现，<code>resolveConfiguredCodeEvalDispatcher()</code> 按环境变量选一个——这是教科书式的<strong>策略模式</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="代码 eval 的策略模式：worker 调用统一的 CodeEvalDispatcher 接口的 dispatch 方法，底层由 resolveConfiguredCodeEvalDispatcher 按环境变量选择 AwsLambda 派发器(按语言调 python/node Lambda 沙箱)或本地 vm 派发器(名为 insecure-local，仅 TS/JS)">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一个接口，两种执行后端（策略模式）</text>
  <rect x="280" y="34" width="160" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="53" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">worker 执行步</text><text x="360" y="68" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">dispatcher.dispatch(payload)</text>
  <rect x="250" y="92" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--ink)" stroke-width="1.6"/><text x="360" y="108" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">interface CodeEvalDispatcher</text><text x="360" y="120" text-anchor="middle" font-size="6.6" fill="var(--muted)">{ name; dispatch(input): Promise&lt;{scores}&gt; }</text>
  <rect x="40" y="150" width="300" height="56" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="190" y="169" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">AwsLambdaCodeEvalDispatcher</text><text x="190" y="185" text-anchor="middle" font-size="6.8" fill="var(--muted)">name="aws-lambda" · 按语言调 Lambda 沙箱</text><text x="190" y="198" text-anchor="middle" font-size="6.4" fill="var(--faint)">python→executor-python · TS→executor-node（生产）</text>
  <rect x="380" y="150" width="300" height="56" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="5 3"/><text x="530" y="169" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">LocalCodeEvalDispatcher</text><text x="530" y="185" text-anchor="middle" font-size="6.8" fill="var(--muted)">name="insecure-local" · node vm 跑</text><text x="530" y="198" text-anchor="middle" font-size="6.4" fill="var(--faint)">仅 TS/JS · 名字直说「不安全」，仅本地开发</text>
  <line x1="360" y1="78" x2="360" y2="90" stroke="var(--faint)" stroke-width="1.4"/><polygon points="360,92 356,83 364,83" fill="var(--faint)"/>
  <line x1="300" y1="126" x2="190" y2="148" stroke="var(--blue)" stroke-width="1.4"/><polygon points="190,148 199,144 195,140" fill="var(--blue)"/>
  <line x1="420" y1="126" x2="530" y2="148" stroke="var(--accent)" stroke-width="1.4"/><polygon points="530,148 525,140 521,144" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>策略模式</b>：worker 只依赖 <code>CodeEvalDispatcher</code> 接口（<code>codeEvalDispatcherTypes.ts:119-121</code>）。<code>resolveConfiguredCodeEvalDispatcher</code>（<code>codeEvalDispatchers.ts:13</code>）按 <code>env.LANGFUSE_CODE_EVAL_DISPATCHER</code> 选 Lambda（生产，强隔离）或本地 vm（开发，<b>名字就叫 insecure-local</b>）。换后端不动 worker 一行。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/evals/codeEvalDispatcherTypes.ts · codeEvalDispatchers.ts</span><span class="ln">接口 + 选择</span></div>
  <pre class="code"><span class="cm">// 极简契约：名字 + 一个 dispatch 方法，返回 { scores:[…] }</span>
<span class="kw">export interface</span> <span class="fn">CodeEvalDispatcher</span> {
  name: string;
  dispatch(input: DispatchInput): Promise&lt;DispatchResult&gt;;   <span class="cm">// DispatchResult = { scores: 至少1条 }</span>
}

<span class="cm">// 按环境变量选实现——策略模式的「选择点」</span>
<span class="kw">export function</span> <span class="fn">resolveConfiguredCodeEvalDispatcher</span>(): CodeEvalDispatcher | null {
  <span class="kw">if</span> (dispatcher === <span class="st">"insecure-local"</span>) <span class="kw">return new</span> LocalCodeEvalDispatcher();  <span class="cm">// node vm，仅 TS/JS</span>
  <span class="kw">if</span> (dispatcher === <span class="st">"aws-lambda"</span>) <span class="kw">return new</span> AwsLambdaCodeEvalDispatcher({
    functionNameByLanguage: { PYTHON: <span class="st">"…-python"</span>, TYPESCRIPT: <span class="st">"…-node"</span> } });
}</pre>
</div>
""")

# (L31 sec3 sandbox below)

_ZH31.append(r"""
<h2>沙箱的铁律：禁网络、限大小、限时</h2>
<p>既然要跑用户代码，平台就得用一圈<strong>硬约束</strong>把它框死。这些约束不是 UI 提示，而是<strong>执行层强制</strong>的——超了就直接报特定错误码。最值得玩味的是「禁网络」：它<strong>一箭双雕</strong>，既挡住安全风险，又保住确定性。</p>

<table class="t">
  <thead><tr><th>铁律</th><th>具体限制</th><th>为什么</th></tr></thead>
  <tbody>
    <tr><td><b>禁网络</b></td><td>评估器代码<b>不准发任何网络请求</b>（TIMEOUT 错误里明说）</td><td>① 安全：防数据外泄、防 SSRF ② 确定性：网络=不确定+可能永不返回</td></tr>
    <tr><td>限时</td><td>必须在配置的运行时限内跑完，否则 TIMEOUT</td><td>防死循环 / 卡死占住沙箱</td></tr>
    <tr><td>源码大小</td><td>≤ 256 KB（SOURCE_TOO_LARGE）</td><td>评估器应短小，不是塞个大程序进来</td></tr>
    <tr><td>输入大小</td><td>≤ 5.5 MB（PAYLOAD_TOO_LARGE，含源码+变量）</td><td>限制单次投喂量，护住派发链路</td></tr>
    <tr><td>结果大小</td><td>≤ 256 KB（RESULT_TOO_LARGE）</td><td>返回的是分数，不该是海量数据</td></tr>
    <tr><td>结果格式</td><td>必须 <code>{ scores: [≥1 条] }</code>，每条带 name/dataType/value 且类型匹配（INVALID_RESULT）</td><td>不规整就没法归一成 score</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">codeEvalDispatcherTypes.ts · localCodeEvalDispatcher.ts</span><span class="ln">限制常量 + 沙箱执行</span></div>
  <pre class="code"><span class="cm">// 三道大小红线（字节），执行层强制（codeEvalDispatcherTypes.ts:4-6）</span>
CODE_EVAL_SOURCE_MAX_BYTES          = 256 * 1024;        <span class="cm">// 源码 ≤256KB</span>
CODE_EVAL_DISPATCH_PAYLOAD_MAX_BYTES = 5.5 * 1024 * 1024; <span class="cm">// 输入 ≤5.5MB</span>
CODE_EVAL_DISPATCH_RESULT_MAX_BYTES  = 256 * 1024;        <span class="cm">// 结果 ≤256KB</span>

<span class="cm">// 本地派发器：用 node 的 vm 跑，带超时；名字诚实地叫 "insecure-local"</span>
<span class="kw">import</span> * <span class="kw">as</span> vm <span class="kw">from</span> <span class="st">"node:vm"</span>;
<span class="kw">const</span> context = vm.createContext({ <span class="cm">/* 受限的全局，无 fetch/require */</span> });
vm.runInContext(<span class="st">"evaluate(payload)"</span>, context, { timeout });  <span class="cm">// 跑用户的 evaluate()，结果须是 {scores}</span></pre>
</div>

<p>跑完之后呢？和第 29 课<strong>完全一样</strong>：拿到的 <code>{scores:[…]}</code> 归一成 score、标 <code>source=EVAL</code>、经第 12 课摄取链路回流 scores 表。代码 eval 并没有另起炉灶——它只是把第 30 课调度流水线里「执行」那一步，从「调 LLM」换成「dispatch 到沙箱」。<strong>同一套调度、同一种 score、同一条回流</strong>，只是裁判从「概率的模型」换成了「确定的函数」。这就是为什么 Langfuse 能把两种评估塞进同一个 JobExecution 状态机里。</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>取变量</h4><p>和裁判流水线同源：按变量映射从 trace/observation 取出 input/output 等列（<code>extractObservationVariables</code>）。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>组 payload</h4><p>把用户的评估器源码 + 取到的变量 + <code>runtime.language</code> 打包成 <code>CodeEvalPayload</code>，先过大小红线（源码≤256KB、整体≤5.5MB）。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>dispatch 到沙箱</h4><p><code>dispatcher.dispatch(payload)</code>：Lambda 按语言调 python/node 函数，或本地 vm 跑——禁网络、限时。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>校验结果</h4><p>返回必须是 <code>{scores:[≥1]}</code>，逐条校验 name/dataType/value 且类型匹配、结果≤256KB（<code>parseDispatchResult</code>）。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>归一 + 回流</h4><p>和第 29 课同款：标 <code>source=EVAL</code>，经摄取链路写回 scores 表，工单标 COMPLETED。</p></div></div>
</div>
""")

# (L31 spark+key below)

_ZH31.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么要 dispatcher 这层抽象，而不是直接调 Lambda？</strong> 因为「在哪跑用户代码」是个会变的决策：云上用 Lambda（强隔离、按需扩容），自托管的人可能没有 Lambda、只想本地跑。把执行后端藏在 <code>{name, dispatch}</code> 接口后，worker 的逻辑<strong>对后端一无所知</strong>——换实现、加新沙箱（比如未来的 WASM runtime），都不动调用方一行。这正是策略模式的价值：<strong>让「怎么做」可替换，而「做什么」稳定</strong>。<br><br>
  <strong>为什么本地派发器要起名 "insecure-local"？</strong> 这是一处难得的<strong>诚实</strong>。Node 的 <code>vm</code> 模块<strong>不是真正的安全沙箱</strong>——有经验的人能从 vm context 里逃逸。Langfuse 不藏着掖着，直接把「不安全」写进名字，等于在源码里贴了张警告条：<strong>这条路只配本地开发，生产请用 Lambda 那种真隔离</strong>。命名即文档，把风险摆在最显眼处。<br><br>
  <strong>为什么「禁网络」这条铁律最关键？</strong> 它一刀解决两个问题。<strong>安全上</strong>：用户代码一旦能联网，就能把你递进去的 trace 数据（可能含敏感信息）偷偷外传，或拿沙箱当跳板打内网（SSRF）。<strong>确定性上</strong>：评估的灵魂是「同输入恒同分」，而网络请求<strong>天生不确定</strong>——接口会抖、会超时、会返回不同结果，甚至「可能永不返回」（源码原话）。掐断网络，等于同时焊死了安全口子和不确定性源头。<strong>一条约束，两重收益</strong>——好的限制往往如此。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>代码 eval = 确定性评估</strong>：用一段函数算分，适合客观/规则类信号（合法 JSON、含 PII、长度、精确/正则匹配）；与 LLM-as-judge（概率/主观）互补，不是替代。</li>
    <li><strong>同一条流水线</strong>：它接在第 30 课调度流水线后，只把「执行」步从「调 LLM」换成「dispatch 到沙箱」；结果同样归一成 <code>source=EVAL</code> 的 score 回流——同一个 JobExecution 状态机。</li>
    <li><strong>dispatcher 策略模式</strong>：worker 只依赖 <code>{name, dispatch}</code> 接口；<code>resolveConfiguredCodeEvalDispatcher</code> 按环境变量选 <code>AwsLambda</code>（生产，按语言调 python/node 沙箱）或本地 <code>vm</code>。换后端不动调用方。</li>
    <li><strong>本地派发器叫 "insecure-local"</strong>：node 的 <code>vm</code> 不是真沙箱，名字直说「不安全」——只配本地开发，生产用 Lambda 真隔离。命名即警告。</li>
    <li><strong>沙箱铁律</strong>：禁网络、限时、源码 ≤256KB、输入 ≤5.5MB、结果 ≤256KB、结果须是 <code>{scores:[≥1]}</code>。其中「禁网络」一箭双雕——既防数据外泄/SSRF，又保住「同输入恒同分」的确定性。</li>
  </ul>
</div>
""")

_EN31.append(r"""
<p class="lead">
Not every "is it good" needs an LLM to judge. Many quality signals are <strong>objective and deterministic</strong>: is the answer valid JSON? did it leak an email address? is it over the length limit? are the fields complete? These need no daydreaming judge—just <strong>a piece of code</strong> to compute, deterministic, fast, and free of LLM cost. This is <strong>code-based evaluation</strong>.
But there's a sharp problem here: the evaluator code is <strong>written by users</strong>, and the platform must <strong>execute someone else's code</strong>—an enormous security risk. So this lesson's protagonists are two things: a <strong>dispatcher</strong> that abstracts away "where and how it runs", and a <strong>sandbox</strong> that runs user code under lock and key.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Last lesson's LLM-as-judge is like hiring a <strong>human judge</strong>: subjective, with judgment, but may score differently each time and charges an appearance fee. Code eval is like using a <strong>standard gauge / caliper</strong>: objective, the same reading a hundred times on the same part, nearly free.
  A gauge suits <strong>deterministic</strong> things like "is the dimension within spec", a judge suits <strong>subjective</strong> things like "is the design beautiful"—complementary, not substitutes.
  But there's a catch: this caliper was <strong>mailed in by someone else</strong>, and you dare not plug it straight into the control machine (what if it hides malicious instructions?). The safe move is to run it in an <strong>isolated inspection room</strong> (sandbox), door shut, phone line cut (no network)—it can only measure the part you hand in and hand the reading back, <strong>touching nothing outside</strong>.
</div>
""")

_EN31.append(r"""
<h2>Two judges: deterministic code vs probabilistic LLM</h2>
<p>Lessons 29 and 31 are really <strong>two ways of producing the same score</strong>. Both hang off Lesson 30's scheduling pipeline—the only difference is the "execution" step: LLM-as-judge calls a model, code eval runs a function. Which to pick depends on whether what you're evaluating is <strong>subjective</strong> or <strong>objective</strong>:</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="One trace can take two judging paths: LLM-as-judge calls a model for subjective, semantic judgment; code eval runs a deterministic function in a sandbox for objective, rule-based judgment; both paths produce a source=EVAL score into the same scores table">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">one trace, two judges, same destination</text>
  <rect x="290" y="36" width="140" height="40" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="360" y="55" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">a trace's input/output</text><text x="360" y="69" text-anchor="middle" font-size="6.8" fill="var(--muted)">the answer to judge</text>
  <rect x="40" y="96" width="280" height="62" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="180" y="115" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">LLM-as-judge (Lesson 29)</text><text x="180" y="132" text-anchor="middle" font-size="7.2" fill="var(--accent-ink)">probabilistic · subjective/semantic · costs LLM</text><text x="180" y="147" text-anchor="middle" font-size="6.8" fill="var(--muted)">helpfulness / tone / off-topic?</text>
  <rect x="400" y="96" width="280" height="62" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="540" y="115" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--ink)">code eval (this lesson)</text><text x="540" y="132" text-anchor="middle" font-size="7.2" fill="var(--muted)">deterministic · objective/rule · nearly free</text><text x="540" y="147" text-anchor="middle" font-size="6.8" fill="var(--faint)">valid JSON / has email / length / exact match</text>
  <rect x="270" y="176" width="180" height="28" rx="8" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="360" y="194" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">both produce a source=EVAL score</text>
  <line x1="320" y1="66" x2="200" y2="94" stroke="var(--accent)" stroke-width="1.4"/><polygon points="200,94 209,90 205,86" fill="var(--accent)"/>
  <line x1="400" y1="66" x2="520" y2="94" stroke="var(--blue)" stroke-width="1.4"/><polygon points="520,94 515,86 511,90" fill="var(--blue)"/>
  <line x1="180" y1="158" x2="300" y2="176" stroke="var(--faint)" stroke-width="1.3"/><polygon points="300,176 291,173 294,181" fill="var(--faint)"/>
  <line x1="540" y1="158" x2="420" y2="176" stroke="var(--faint)" stroke-width="1.3"/><polygon points="420,176 429,173 426,181" fill="var(--faint)"/>
</svg>
<div class="figcap"><b>Complementary, not substitutes</b>: what rules can express (format, length, keywords, exact match) goes to code eval—deterministic, fast, free; what needs semantic understanding (helpfulness, tone, relevance) goes to LLM-as-judge. Both attach to Lesson 30's scheduling pipeline, differing only at the "execution" step.</div>
</div>

<table class="t">
  <thead><tr><th>dimension</th><th>LLM-as-judge (Lesson 29)</th><th>code eval (this lesson)</th></tr></thead>
  <tbody>
    <tr><td>how it judges</td><td>calls a model for semantic judgment</td><td>runs a function you wrote</td></tr>
    <tr><td>determinism</td><td>probabilistic (same input may differ)</td><td><b>deterministic</b> (same input, same score)</td></tr>
    <tr><td>good at</td><td>subjective: helpfulness, tone, relevance</td><td>objective: valid JSON, has PII, length, exact/regex match</td></tr>
    <tr><td>cost/speed</td><td>one LLM call each, slow, costs money</td><td>one function run, fast, nearly free</td></tr>
    <tr><td>risk</td><td>the model misjudges, has biases</td><td>must execute <b>user code</b> → must sandbox</td></tr>
  </tbody>
</table>
""")

_EN31.append(r"""
<h2>The dispatcher: a strategy pattern that abstracts away "where it runs"</h2>
<p>The worker shouldn't care whether user code runs on AWS Lambda or locally—it just wants to say "run this code with this input and give me scores". That is the <strong>dispatcher interface</strong>: a minimal contract <code>{ name, dispatch(input) }</code>. Two implementations hang beneath it, and <code>resolveConfiguredCodeEvalDispatcher()</code> picks one by env var—a textbook <strong>strategy pattern</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="Code eval's strategy pattern: the worker calls the unified CodeEvalDispatcher interface's dispatch method; underneath, resolveConfiguredCodeEvalDispatcher picks by env var the AwsLambda dispatcher (invoking per-language python/node Lambda sandboxes) or the local vm dispatcher (named insecure-local, TS/JS only)">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">one interface, two execution backends (strategy pattern)</text>
  <rect x="280" y="34" width="160" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="53" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">worker exec step</text><text x="360" y="68" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">dispatcher.dispatch(payload)</text>
  <rect x="250" y="92" width="220" height="34" rx="8" fill="var(--bg)" stroke="var(--ink)" stroke-width="1.6"/><text x="360" y="108" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">interface CodeEvalDispatcher</text><text x="360" y="120" text-anchor="middle" font-size="6.6" fill="var(--muted)">{ name; dispatch(input): Promise&lt;{scores}&gt; }</text>
  <rect x="40" y="150" width="300" height="56" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="190" y="169" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">AwsLambdaCodeEvalDispatcher</text><text x="190" y="185" text-anchor="middle" font-size="6.8" fill="var(--muted)">name="aws-lambda" · per-language Lambda sandbox</text><text x="190" y="198" text-anchor="middle" font-size="6.4" fill="var(--faint)">python→executor-python · TS→executor-node (prod)</text>
  <rect x="380" y="150" width="300" height="56" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="5 3"/><text x="530" y="169" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">LocalCodeEvalDispatcher</text><text x="530" y="185" text-anchor="middle" font-size="6.8" fill="var(--muted)">name="insecure-local" · runs on node vm</text><text x="530" y="198" text-anchor="middle" font-size="6.4" fill="var(--faint)">TS/JS only · name admits "insecure", local dev only</text>
  <line x1="360" y1="78" x2="360" y2="90" stroke="var(--faint)" stroke-width="1.4"/><polygon points="360,92 356,83 364,83" fill="var(--faint)"/>
  <line x1="300" y1="126" x2="190" y2="148" stroke="var(--blue)" stroke-width="1.4"/><polygon points="190,148 199,144 195,140" fill="var(--blue)"/>
  <line x1="420" y1="126" x2="530" y2="148" stroke="var(--accent)" stroke-width="1.4"/><polygon points="530,148 525,140 521,144" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>Strategy pattern</b>: the worker depends only on the <code>CodeEvalDispatcher</code> interface (<code>codeEvalDispatcherTypes.ts:119-121</code>). <code>resolveConfiguredCodeEvalDispatcher</code> (<code>codeEvalDispatchers.ts:13</code>) picks by <code>env.LANGFUSE_CODE_EVAL_DISPATCHER</code>: Lambda (production, strong isolation) or local vm (dev, <b>literally named insecure-local</b>). Swapping backends changes not a line of the worker.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/evals/codeEvalDispatcherTypes.ts · codeEvalDispatchers.ts</span><span class="ln">interface + selection</span></div>
  <pre class="code"><span class="cm">// minimal contract: a name + one dispatch method returning { scores:[…] }</span>
<span class="kw">export interface</span> <span class="fn">CodeEvalDispatcher</span> {
  name: string;
  dispatch(input: DispatchInput): Promise&lt;DispatchResult&gt;;   <span class="cm">// DispatchResult = { scores: at least 1 }</span>
}

<span class="cm">// pick the impl by env var — the strategy pattern's "selection point"</span>
<span class="kw">export function</span> <span class="fn">resolveConfiguredCodeEvalDispatcher</span>(): CodeEvalDispatcher | null {
  <span class="kw">if</span> (dispatcher === <span class="st">"insecure-local"</span>) <span class="kw">return new</span> LocalCodeEvalDispatcher();  <span class="cm">// node vm, TS/JS only</span>
  <span class="kw">if</span> (dispatcher === <span class="st">"aws-lambda"</span>) <span class="kw">return new</span> AwsLambdaCodeEvalDispatcher({
    functionNameByLanguage: { PYTHON: <span class="st">"…-python"</span>, TYPESCRIPT: <span class="st">"…-node"</span> } });
}</pre>
</div>
""")

_EN31.append(r"""
<h2>The sandbox's iron rules: no network, size caps, time limit</h2>
<p>Since it runs user code, the platform must box it in with <strong>hard constraints</strong>. These aren't UI hints—they're <strong>enforced at the execution layer</strong>: exceed one and you get a specific error code. The most intriguing is "no network": it <strong>kills two birds</strong>, blocking security risk and preserving determinism.</p>

<table class="t">
  <thead><tr><th>iron rule</th><th>the limit</th><th>why</th></tr></thead>
  <tbody>
    <tr><td><b>no network</b></td><td>evaluator code <b>may make no network requests</b> (stated in the TIMEOUT error)</td><td>① security: prevent data exfiltration & SSRF ② determinism: network = nondeterministic + may never return</td></tr>
    <tr><td>time limit</td><td>must finish within the configured runtime, else TIMEOUT</td><td>prevent infinite loops / hangs holding the sandbox</td></tr>
    <tr><td>source size</td><td>≤ 256 KB (SOURCE_TOO_LARGE)</td><td>an evaluator should be small, not a whole program</td></tr>
    <tr><td>input size</td><td>≤ 5.5 MB (PAYLOAD_TOO_LARGE, source + variables)</td><td>cap per-run feed, protect the dispatch path</td></tr>
    <tr><td>result size</td><td>≤ 256 KB (RESULT_TOO_LARGE)</td><td>it returns scores, not bulk data</td></tr>
    <tr><td>result shape</td><td>must be <code>{ scores: [≥1] }</code>, each with name/dataType/value of matching type (INVALID_RESULT)</td><td>malformed can't normalize into a score</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">codeEvalDispatcherTypes.ts · localCodeEvalDispatcher.ts</span><span class="ln">limit constants + sandbox run</span></div>
  <pre class="code"><span class="cm">// three size red-lines (bytes), enforced at the execution layer (codeEvalDispatcherTypes.ts:4-6)</span>
CODE_EVAL_SOURCE_MAX_BYTES          = 256 * 1024;        <span class="cm">// source ≤256KB</span>
CODE_EVAL_DISPATCH_PAYLOAD_MAX_BYTES = 5.5 * 1024 * 1024; <span class="cm">// input ≤5.5MB</span>
CODE_EVAL_DISPATCH_RESULT_MAX_BYTES  = 256 * 1024;        <span class="cm">// result ≤256KB</span>

<span class="cm">// local dispatcher: runs on node's vm with a timeout; honestly named "insecure-local"</span>
<span class="kw">import</span> * <span class="kw">as</span> vm <span class="kw">from</span> <span class="st">"node:vm"</span>;
<span class="kw">const</span> context = vm.createContext({ <span class="cm">/* restricted globals, no fetch/require */</span> });
vm.runInContext(<span class="st">"evaluate(payload)"</span>, context, { timeout });  <span class="cm">// run user's evaluate(), result must be {scores}</span></pre>
</div>

<p>And after it runs? <strong>Exactly like Lesson 29</strong>: the returned <code>{scores:[…]}</code> normalizes into scores tagged <code>source=EVAL</code> and flows back through Lesson 12's ingestion path into the scores table. Code eval starts no new machinery—it just swaps Lesson 30's "execution" step from "call the LLM" to "dispatch to the sandbox". <strong>Same scheduling, same score, same flow-back</strong>, only the judge changes from "a probabilistic model" to "a deterministic function". That's why Langfuse fits both evaluation kinds into the same JobExecution state machine.</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>extract variables</h4><p>Same origin as the judge pipeline: pull input/output etc. from the trace/observation per the variable mapping (<code>extractObservationVariables</code>).</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>build payload</h4><p>Pack the user's evaluator source + extracted variables + <code>runtime.language</code> into a <code>CodeEvalPayload</code>, first checking size red-lines (source ≤256KB, total ≤5.5MB).</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>dispatch to sandbox</h4><p><code>dispatcher.dispatch(payload)</code>: Lambda invokes the per-language python/node function, or the local vm runs it—no network, time-limited.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>validate result</h4><p>The return must be <code>{scores:[≥1]}</code>, each score's name/dataType/value validated with matching type, result ≤256KB (<code>parseDispatchResult</code>).</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>normalize + flow back</h4><p>Just like Lesson 29: tag <code>source=EVAL</code>, write back to the scores table via the ingestion path, mark the ticket COMPLETED.</p></div></div>
</div>
""")

_EN31.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why the dispatcher abstraction instead of calling Lambda directly?</strong> Because "where to run user code" is a decision that changes: cloud uses Lambda (strong isolation, on-demand scaling), while self-hosters may lack Lambda and just want to run locally. Hiding the execution backend behind a <code>{name, dispatch}</code> interface keeps the worker's logic <strong>oblivious to the backend</strong>—swapping impls or adding a new sandbox (say a future WASM runtime) changes not a line of the caller. That's the value of the strategy pattern: <strong>make "how" replaceable while "what" stays stable</strong>.<br><br>
  <strong>Why name the local dispatcher "insecure-local"?</strong> A rare bit of <strong>honesty</strong>. Node's <code>vm</code> module is <strong>not a real security sandbox</strong>—the experienced can escape a vm context. Langfuse doesn't hide it; it writes "insecure" right into the name, like a warning sticker in the source: <strong>this path is fit only for local dev; for production use real isolation like Lambda</strong>. Naming as documentation, putting the risk where it's most visible.<br><br>
  <strong>Why is "no network" the most crucial iron rule?</strong> It solves two problems at a stroke. <strong>On security</strong>: once user code can reach the network, it could quietly exfiltrate the trace data you fed it (possibly sensitive) or use the sandbox as a springboard into your internal network (SSRF). <strong>On determinism</strong>: the soul of evaluation is "same input, same score", yet network requests are <strong>inherently nondeterministic</strong>—endpoints flake, time out, return different results, even "may never return" (the source's own words). Cutting the network welds shut both the security hole and the source of nondeterminism. <strong>One constraint, two payoffs</strong>—good restrictions often are.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Code eval = deterministic evaluation</strong>: a function computes the score, suited to objective/rule signals (valid JSON, has PII, length, exact/regex match); complementary to LLM-as-judge (probabilistic/subjective), not a substitute.</li>
    <li><strong>Same pipeline</strong>: it attaches to Lesson 30's scheduling pipeline, swapping only the "execution" step from "call the LLM" to "dispatch to the sandbox"; results likewise normalize into <code>source=EVAL</code> scores that flow back—the same JobExecution state machine.</li>
    <li><strong>Dispatcher strategy pattern</strong>: the worker depends only on the <code>{name, dispatch}</code> interface; <code>resolveConfiguredCodeEvalDispatcher</code> picks by env var <code>AwsLambda</code> (production, per-language python/node sandbox) or local <code>vm</code>. Swapping backends doesn't touch the caller.</li>
    <li><strong>The local dispatcher is named "insecure-local"</strong>: node's <code>vm</code> isn't a real sandbox, and the name says so—fit only for local dev; production uses real Lambda isolation. Naming as warning.</li>
    <li><strong>Sandbox iron rules</strong>: no network, time limit, source ≤256KB, input ≤5.5MB, result ≤256KB, result must be <code>{scores:[≥1]}</code>. "No network" kills two birds—blocking exfiltration/SSRF and preserving "same input, same score" determinism.</li>
  </ul>
</div>
""")

LESSON_31 = {"zh": "\n".join(_ZH31), "en": "\n".join(_EN31)}


# ══════════════════════════════════════════════════════════════════════
# L32 · 人工标注 / Human annotation
# ══════════════════════════════════════════════════════════════════════
_ZH32 = []
_EN32 = []

_ZH32.append(r"""
<p class="lead">
前三课让机器自动打分——LLM 当裁判、代码做确定性检查。但有些判断<strong>离不开人</strong>：建立可信的 ground truth（基准答案）、审核「AI 到底判得对不对」、处理 AI 拿不准的边界情形、给训练/对齐采人类偏好。这一课讲第 28 课埋下的<strong>第三种 score 来源——人工标注（source=ANNOTATION）</strong>，以及把「请人评审」这件本质上<strong>无序又易冲突</strong>的事，组织成有序流程的工具：<strong>标注队列（annotation queue）</strong>。
重点有三：队列的<strong>数据模型</strong>（绑一组 score config、装一批待评对象）、一个有意思的<strong>5 分钟时间锁</strong>（人类尺度的并发控制），以及人工分如何和前两课的 EVAL 分<strong>同表汇合</strong>——从而成为校准 AI 裁判的标尺。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  标注队列像医院的<strong>待会诊病历筐</strong>。每份需要人来看的病历（一条 trace、一次 observation、或整个 session）被放进筐里排队；筐口贴着一张<strong>统一的评分表</strong>（队列绑定的 score config，决定医生要填哪几项、每项什么刻度）。
  医生从筐里<strong>取一份</strong>来看，系统立刻给这份病历<strong>上锁 5 分钟</strong>——这样另一位医生同时来取时，不会拿到同一份重复会诊；而要是这位医生中途走开了，锁会自动过期，病历重新可领，<strong>不会被永久占住</strong>。
  看完，医生<strong>填表打分、可附一句评语</strong>，把病历标成「已会诊」，并记下<strong>是谁看的</strong>。这些人工评分和前两课 AI 评的分<strong>进同一本病案室</strong>（scores 表）——于是你能把「人怎么判的」和「AI 怎么判的」摆在一起对照，看 AI 靠不靠谱。
</div>
""")

_ZH32.append(r"""
<h2>合上闭环：第三种来源，也是「标尺的标尺」</h2>
<p>第 28 课说 score 有三种来源：API、EVAL、ANNOTATION。前面几课讲完了 EVAL（裁判与代码），这一课补上 ANNOTATION。三者<strong>同表、同 config、同一把尺</strong>——但人工分有个独特角色：它常被当作 <strong>ground truth</strong>，用来回答第 29 课留下的问题「<strong>AI 裁判靠不靠谱</strong>」。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="三种 score 来源 API、EVAL、ANNOTATION 汇入同一张 scores 表；人工标注的分常作为 ground truth，与 EVAL 的 AI 裁判分在同一批对象上对照，用来校准裁判是否可信">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">三来源汇合，人工分还兼任「裁判的标尺」</text>
  <rect x="30" y="40" width="150" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="105" y="61" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">API（你亲手提交）</text>
  <rect x="30" y="84" width="150" height="34" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="105" y="105" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">EVAL（AI 裁判 / 代码）</text>
  <rect x="30" y="128" width="150" height="34" rx="7" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="105" y="149" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">ANNOTATION（人工·本课）</text>
  <rect x="250" y="78" width="150" height="56" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="325" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">scores 表（第 8 课宽表）</text><text x="325" y="117" text-anchor="middle" font-size="7" fill="var(--muted)">同名同 config → 可比</text>
  <rect x="468" y="44" width="232" height="58" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-dasharray="5 3"/><text x="584" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">人工分 = ground truth</text><text x="584" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">在同一批 trace 上</text><text x="584" y="93" text-anchor="middle" font-size="7" fill="var(--accent-ink)">和 EVAL 分对照</text>
  <rect x="468" y="116" width="232" height="44" rx="10" fill="var(--bg)" stroke="var(--accent)"/><text x="584" y="134" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">→ 校准 AI 裁判是否可信</text><text x="584" y="150" text-anchor="middle" font-size="6.8" fill="var(--muted)">人机不一致处，正是裁判要改进的地方</text>
  <line x1="180" y1="57" x2="248" y2="92" stroke="var(--faint)" stroke-width="1.3"/><line x1="180" y1="101" x2="248" y2="104" stroke="var(--accent)" stroke-width="1.3"/><line x1="180" y1="145" x2="248" y2="118" stroke="var(--accent)" stroke-width="1.6"/>
  <line x1="400" y1="98" x2="466" y2="78" stroke="var(--accent)" stroke-width="1.4"/><polygon points="466,78 457,77 460,85" fill="var(--accent)"/>
  <line x1="584" y1="102" x2="584" y2="114" stroke="var(--faint)" stroke-width="1.3"/><polygon points="584,116 580,107 588,107" fill="var(--accent)"/>
  <text x="360" y="195" text-anchor="middle" font-size="8" fill="var(--faint)">人工标注又慢又贵，所以通常只评一小撮关键样本——但这一小撮是衡量 AI 裁判的「金标准」</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">三来源各取所长：API 灵活、EVAL 可扩展、ANNOTATION 最权威</text>
</svg>
<div class="figcap"><b>第三种来源，闭合第 28 课的环</b>：人工分与 API、EVAL 分写进同一张 scores 表（<code>ScoreSourceArray=["API","EVAL","ANNOTATION"]</code>，<code>scores.ts:4</code>），享受同一 config 校验。它最大的价值是当 <b>ground truth</b>——在同一批对象上和 AI 裁判分对照，量出裁判的可信度。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">建基准</span><span class="name">ground truth</span></div><div class="ld">很多评估要有「标准答案」才谈得上准不准。人类专家在一小撮代表性样本上打的分，就是这把<strong>金标准</strong>——AI 裁判、回归测试、模型对比都拿它当参照系。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">审裁判</span><span class="name">审核 AI 判得对不对</span></div><div class="ld">第 29 课问过「裁判自己靠不靠谱」。答案就在这：把同一批 trace 既让 AI 裁判评、又让人评，<strong>看两者一致不一致</strong>。不一致的地方，要么改 prompt、要么换模型——人工标注是<strong>校准裁判的反馈回路</strong>。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">啃边界</span><span class="name">AI 拿不准的情形</span></div><div class="ld">对那些 AI 反复打分摇摆、或明显需要领域知识/价值判断的样本，直接交给人。人工标注专攻<strong>机器最不擅长的长尾</strong>，把宝贵人力花在刀刃上。</div></div>
</div>
""")

# (L32 sec2 model below)

_ZH32.append(r"""
<h2>队列的数据模型：一张评分表 + 一筐待评对象</h2>
<p>标注队列的数据模型只有两个主角。<strong>AnnotationQueue</strong> 是「评审任务」本身：有名字、描述，最关键是一组 <code>scoreConfigIds</code>——它<strong>绑定第 28 课的 score config</strong>，规定这个队列里每位评审员要填哪几项分、每项什么刻度（统一了大家的尺）。<strong>AnnotationQueueItem</strong> 是「筐里的一份待评对象」：指向一条 trace/observation/session，带一个 PENDING→COMPLETED 的状态。</p>

<table class="t">
  <thead><tr><th>字段</th><th>含义</th><th>为什么重要</th></tr></thead>
  <tbody>
    <tr><td colspan="3" style="background:var(--purple-soft);font-weight:700">AnnotationQueue（评审任务）</td></tr>
    <tr><td><code>name / description</code></td><td>队列名与说明</td><td>一个项目可有多个队列（如「事实性核查」「语气审查」）</td></tr>
    <tr><td><code>scoreConfigIds[]</code></td><td>绑定的一组 score config</td><td><b>统一评分表</b>：所有评审员按同一组 config 打分，分数才可比（呼应第 28 课）</td></tr>
    <tr><td colspan="3" style="background:var(--blue-soft);font-weight:700">AnnotationQueueItem（一份待评对象）</td></tr>
    <tr><td><code>objectType / objectId</code></td><td>评的是什么：TRACE / OBSERVATION / SESSION</td><td>三种粒度都能评——整条对话、某一步、或整个会话</td></tr>
    <tr><td><code>status</code></td><td>PENDING / COMPLETED</td><td>队列的进度就是「还剩多少 PENDING」</td></tr>
    <tr><td><code>lockedAt / lockedByUserId</code></td><td>谁在看、何时锁的</td><td>下一节的 <b>5 分钟锁</b>，防两人重复标注</td></tr>
    <tr><td><code>annotatorUserId / completedAt</code></td><td>谁评的、何时完成</td><td>可审计：每条人工分都知道出自谁手</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma:582-633</span><span class="ln">两个模型 + 两个枚举</span></div>
  <pre class="code"><span class="kw">model</span> AnnotationQueue {
  name           String
  scoreConfigIds String[]   <span class="cm">// ← 绑定第28课的 score config，统一这个队列的评分表</span>
  annotationQueueItem  AnnotationQueueItem[]
  annotationQueueAssignment AnnotationQueueAssignment[]  <span class="cm">// 队列指派给哪些评审员</span>
}
<span class="kw">model</span> AnnotationQueueItem {
  objectId   String;  objectType AnnotationQueueObjectType   <span class="cm">// 评的对象</span>
  status     AnnotationQueueStatus @default(PENDING)          <span class="cm">// PENDING → COMPLETED</span>
  lockedAt   DateTime?;  lockedByUserId  String?              <span class="cm">// ← 软锁（5分钟）</span>
  annotatorUserId String?;  completedAt DateTime?            <span class="cm">// 谁评的、何时完成</span>
}
<span class="kw">enum</span> AnnotationQueueObjectType { TRACE  OBSERVATION  SESSION }
<span class="kw">enum</span> AnnotationQueueStatus     { PENDING  COMPLETED }</pre>
</div>

<p>还有第三个模型 <code>AnnotationQueueAssignment</code>：把队列<strong>指派给特定评审员</strong>。于是「谁该评哪个队列」也是结构化的——不是发个链接全凭自觉，而是平台记录在案的分工。</p>
""")

# (L32 sec3 lock below)

_ZH32.append(r"""
<h2>5 分钟软锁：人类尺度的并发控制</h2>
<p>多个评审员同时盯着一个队列，怎么避免两人评到同一份、白费功夫？数据库的事务锁太重、也不贴合「人看一会儿」的节奏。Langfuse 用一个轻巧的<strong>时间软锁</strong>：评审员打开一份 item，就写上 <code>lockedByUserId</code> 和 <code>lockedAt</code>；判断「是否被锁」时，只认<strong>最近 5 分钟内</strong>的锁。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="5 分钟软锁：评审员A 打开一份 item 写入 lockedAt，5 分钟内该 item 对评审员B 显示为已锁定、跳过；若 A 中途离开，锁超过 5 分钟自动过期，item 重新可领，不会被永久占住">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">软锁 = lockedByUserId + lockedAt，只在 5 分钟内有效</text>
  <rect x="40" y="40" width="120" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="100" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">评审员 A 打开</text><text x="100" y="72" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">写 lockedAt=now</text>
  <rect x="210" y="40" width="300" height="40" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">item 锁定中（lockedAt &gt; now − 5min）</text><text x="360" y="72" text-anchor="middle" font-size="6.8" fill="var(--muted)">其他人看到「已锁」，跳过这份</text>
  <rect x="560" y="40" width="130" height="40" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="625" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">A 评完 → COMPLETED</text><text x="625" y="72" text-anchor="middle" font-size="6.6" fill="var(--muted)">记 annotatorUserId</text>
  <rect x="210" y="110" width="300" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="5 3"/><text x="360" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">若 A 中途离开……</text><text x="360" y="146" text-anchor="middle" font-size="6.8" fill="var(--muted)">5 分钟后锁自动过期，item 重新可领——不会被永久占住</text>
  <rect x="40" y="112" width="120" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="100" y="130" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">评审员 B 来取</text><text x="100" y="144" text-anchor="middle" font-size="6.6" fill="var(--muted)">锁过期→可领</text>
  <line x1="160" y1="60" x2="208" y2="60" stroke="var(--accent)" stroke-width="1.5"/><polygon points="208,60 199,56 199,64" fill="var(--accent)"/>
  <line x1="510" y1="60" x2="558" y2="60" stroke="var(--teal)" stroke-width="1.5"/><polygon points="558,60 549,56 549,64" fill="var(--teal)"/>
  <line x1="360" y1="80" x2="360" y2="108" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/>
  <line x1="160" y1="132" x2="208" y2="132" stroke="var(--blue)" stroke-width="1.4"/><polygon points="208,132 199,128 199,136" fill="var(--blue)"/>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">不是数据库事务锁，而是一个「带过期时间的标记」——贴合人类「看几分钟」的节奏，且永不死锁</text>
  <text x="360" y="201" text-anchor="middle" font-size="8" fill="var(--faint)">关掉浏览器、网断了都不要紧：锁会自己消失</text>
</svg>
<div class="figcap"><b>软锁，不是硬锁</b>：<code>isItemLocked</code> 只认 <code>lockedAt</code> 在最近 5 分钟内的锁（<code>annotationQueueItemsRouter.ts:34-36</code>）。它解决「人类并发」——多人同评一个队列不撞车，又因为<b>会自动过期</b>，绝不会因某人关了页面而把 item 永久占死。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">annotationQueueItemsRouter.ts:34 · scores/hooks/useScoreMutations.ts:39</span><span class="ln">软锁 + 出分</span></div>
  <pre class="code"><span class="cm">// 软锁：只有「最近 5 分钟内被锁」才算锁定——超时自动失效</span>
<span class="kw">const</span> <span class="fn">isItemLocked</span> = (item) =&gt;
  item.lockedByUserId &amp;&amp; item.lockedAt &amp;&amp;
  <span class="kw">new</span> Date(item.lockedAt) &gt; <span class="kw">new</span> Date(Date.now() - <span class="st">5 * 60 * 1000</span>);   <span class="cm">// 5 分钟窗口</span>

<span class="cm">// 评完：item 标 COMPLETED 并记下评审员</span>
{ status: AnnotationQueueStatus.COMPLETED, annotatorUserId: ctx.session.user.id }

<span class="cm">// 评审员填的每个分：source=ANNOTATION，且带 authorUserId（谁打的）</span>
createAnnotationScore({ source: <span class="st">"ANNOTATION"</span>, authorUserId, name, value, dataType, comment });
<span class="cm">// → 和第29课 EVAL 分一样，归一后经第12课摄取链路回流同一张 scores 表</span></pre>
</div>

<p>评审员填的分，<code>source</code> 标成 <code>ANNOTATION</code>、带上 <code>authorUserId</code>（哪位评审员），还能附 <code>comment</code> 写理由——和第 29 课 EVAL 分一样，最终都归一成 score、经第 12 课摄取链路回流<strong>同一张 scores 表</strong>。至此，第 28 课的三种来源全部到齐：<strong>API、EVAL、ANNOTATION 殊途同归，同表、同尺、可比</strong>。Part 5 的主线——「把『发生了什么』变成『做得多好』」——到这里画上闭环。</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>进入被指派的队列</h4><p>评审员看到指派给自己的队列（<code>AnnotationQueueAssignment</code>）和里面待评的 PENDING item。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>领一份 → 自动上锁</h4><p>打开一份 item，系统写 <code>lockedByUserId/lockedAt</code>，5 分钟内别人看到「已锁」、跳过。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>看对象</h4><p>按 <code>objectType</code> 展开要评的 TRACE / OBSERVATION / SESSION——直接复用第 25、26 课的详情视图。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>按 config 打分 + 评语</h4><p>填队列绑定的每个 score config，可附 <code>comment</code>。分即时写成 <code>source=ANNOTATION</code>、带 <code>authorUserId</code>。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>提交 → 跳下一份</h4><p>item 标 <code>COMPLETED</code> + 记 <code>annotatorUserId/completedAt</code>，锁释放，自动推进队列里下一份 PENDING。</p></div></div>
</div>
""")

# (L32 spark+key below)

_ZH32.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么用「5 分钟时间软锁」，而不是数据库事务锁或永久占用标记？</strong> 因为这把锁要适配的是<strong>人</strong>，不是机器。数据库事务锁是毫秒级的、占着连接，根本扛不住「人看几分钟」的时长。而如果用永久标记（「A 正在看」直到 A 主动释放），一旦 A 关了浏览器、断了网、或干脆忘了——这份 item 就被<strong>永久占死</strong>，再没人能领。时间软锁两头讨好：5 分钟够一个人看完一份、避免并发撞车；又因为<strong>会自动过期</strong>，任何意外都只会让锁「自愈」，绝不死锁。这是一个把「乐观并发 + 租约（lease）」思想用在人类工作流上的漂亮小设计——<strong>锁的粒度，要匹配被锁者的节奏</strong>。<br><br>
  <strong>为什么人工分一定要和 AI 评的分进同一张表、用同一套 config？</strong> 因为只有同尺，才能<strong>对照</strong>。把人评的「金标准」和 AI 裁判的分摆在同一批 trace 上，一减就知道裁判哪里偏了——这正是第 29 课「怎么信任 AI 裁判」的答案：<strong>用人工标注当裁判的标尺</strong>。如果两边各用各的存储、各打各的刻度，这种校准根本无从谈起。Langfuse 让三种来源（API/EVAL/ANNOTATION）共享一张 scores 表、一套 score config，本质上就是为了让<strong>「人怎么看」和「机器怎么看」永远可以放在一起比较</strong>——评估体系的可信度，最终落在这一点上。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>人工标注 = 第三种 score 来源（ANNOTATION）</strong>：补上第 28 课三来源的最后一块。它最贵也最权威，常用作 ground truth——既建基准、又审核「AI 裁判判得对不对」、还啃 AI 拿不准的长尾。</li>
    <li><strong>标注队列把无序的评审变有序</strong>：<code>AnnotationQueue</code> 绑一组 <code>scoreConfigIds</code>（统一评分表）；<code>AnnotationQueueItem</code> 指向一个 TRACE/OBSERVATION/SESSION，带 PENDING→COMPLETED 状态；<code>AnnotationQueueAssignment</code> 把队列指派给评审员。</li>
    <li><strong>5 分钟软锁 = 人类并发控制</strong>：打开即写 <code>lockedAt</code>，<code>isItemLocked</code> 只认最近 5 分钟内的锁。多人同评不撞车，又因自动过期而<strong>永不死锁</strong>——锁的粒度匹配人的节奏。</li>
    <li><strong>出分同归</strong>：评审员按 config 打的分 <code>source=ANNOTATION</code>、带 <code>authorUserId</code> 与可选 <code>comment</code>，item 标 COMPLETED + 记 annotatorUserId；分经第 12 课摄取链路回流<strong>同一张 scores 表</strong>。</li>
    <li><strong>闭环</strong>：API/EVAL/ANNOTATION 三来源同表、同尺、可比——人工分因此能当 AI 裁判的标尺。这正是评估可信度的基石，也为 Part 5「把发生变成做得多好」收尾。</li>
  </ul>
</div>
""")

_EN32.append(r"""
<p class="lead">
The last three lessons let machines score automatically—an LLM as judge, code for deterministic checks. But some judgments <strong>require a human</strong>: establishing trustworthy ground truth, auditing "is the AI actually right", handling edge cases the AI is unsure about, collecting human preferences for training/alignment. This lesson covers the <strong>third score source planted in Lesson 28—human annotation (source=ANNOTATION)</strong>, and the tool that turns the inherently <strong>unordered and collision-prone</strong> act of "asking people to review" into an orderly process: the <strong>annotation queue</strong>.
Three focuses: the queue's <strong>data model</strong> (bound to a set of score configs, holding a batch of objects to review), an interesting <strong>5-minute time lock</strong> (human-scale concurrency control), and how human scores <strong>converge in the same table</strong> as the previous lessons' EVAL scores—becoming the yardstick to calibrate the AI judge.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  An annotation queue is like a hospital's <strong>basket of charts awaiting consultation</strong>. Each chart needing human eyes (a trace, an observation, or a whole session) queues in the basket; the basket bears a <strong>uniform scoring sheet</strong> (the queue's bound score configs, deciding which items each doctor must fill and on what scale).
  A doctor <strong>takes one</strong> to review, and the system immediately <strong>locks that chart for 5 minutes</strong>—so another doctor taking one at the same time won't get the same chart twice; and if this doctor wanders off, the lock auto-expires and the chart becomes available again, <strong>never permanently held</strong>.
  After reviewing, the doctor <strong>fills the sheet, may add a note</strong>, marks the chart "consulted", and records <strong>who reviewed it</strong>. These human scores go into the <strong>same records room</strong> (the scores table) as the AI scores from the last lessons—so you can lay "how the human judged" and "how the AI judged" side by side and see whether the AI is reliable.
</div>
""")

_EN32.append(r"""
<h2>Closing the loop: the third source, and the "yardstick for yardsticks"</h2>
<p>Lesson 28 said a score has three sources: API, EVAL, ANNOTATION. The earlier lessons finished EVAL (judge and code); this one fills in ANNOTATION. All three are <strong>same-table, same-config, one ruler</strong>—but human scores have a unique role: they're often used as <strong>ground truth</strong>, answering the question Lesson 29 left open, "<strong>is the AI judge reliable</strong>".</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="Three score sources API, EVAL, ANNOTATION converge into the same scores table; human-annotation scores often serve as ground truth, compared against the EVAL AI-judge scores on the same objects to calibrate the judge's trustworthiness">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">three sources converge; human scores also serve as "the judge's yardstick"</text>
  <rect x="30" y="40" width="150" height="34" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="105" y="61" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">API (you submit)</text>
  <rect x="30" y="84" width="150" height="34" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="105" y="105" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">EVAL (AI judge / code)</text>
  <rect x="30" y="128" width="150" height="34" rx="7" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="105" y="149" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">ANNOTATION (human·here)</text>
  <rect x="250" y="78" width="150" height="56" rx="10" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="325" y="100" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">scores table (L8 wide table)</text><text x="325" y="117" text-anchor="middle" font-size="7" fill="var(--muted)">same name+config → comparable</text>
  <rect x="468" y="44" width="232" height="58" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-dasharray="5 3"/><text x="584" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">human scores = ground truth</text><text x="584" y="80" text-anchor="middle" font-size="7" fill="var(--accent-ink)">on the same traces</text><text x="584" y="93" text-anchor="middle" font-size="7" fill="var(--accent-ink)">compared with EVAL scores</text>
  <rect x="468" y="116" width="232" height="44" rx="10" fill="var(--bg)" stroke="var(--accent)"/><text x="584" y="134" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">→ calibrate if the AI judge is trustworthy</text><text x="584" y="150" text-anchor="middle" font-size="6.6" fill="var(--muted)">human-AI disagreements are where the judge must improve</text>
  <line x1="180" y1="57" x2="248" y2="92" stroke="var(--faint)" stroke-width="1.3"/><line x1="180" y1="101" x2="248" y2="104" stroke="var(--accent)" stroke-width="1.3"/><line x1="180" y1="145" x2="248" y2="118" stroke="var(--accent)" stroke-width="1.6"/>
  <line x1="400" y1="98" x2="466" y2="78" stroke="var(--accent)" stroke-width="1.4"/><polygon points="466,78 457,77 460,85" fill="var(--accent)"/>
  <line x1="584" y1="102" x2="584" y2="114" stroke="var(--faint)" stroke-width="1.3"/><polygon points="584,116 580,107 588,107" fill="var(--accent)"/>
  <text x="360" y="195" text-anchor="middle" font-size="8" fill="var(--faint)">human annotation is slow and costly, so usually only a small key sample is reviewed—but that sample is the "gold standard" for the AI judge</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">three sources, each its strength: API flexible, EVAL scalable, ANNOTATION most authoritative</text>
</svg>
<div class="figcap"><b>The third source, closing Lesson 28's loop</b>: human scores join API and EVAL scores in the same scores table (<code>ScoreSourceArray=["API","EVAL","ANNOTATION"]</code>, <code>scores.ts:4</code>), validated by the same config. Their biggest value is as <b>ground truth</b>—compared against AI-judge scores on the same objects to measure the judge's trustworthiness.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">baseline</span><span class="name">ground truth</span></div><div class="ld">Many evaluations need a "correct answer" before "how accurate" means anything. Scores from human experts on a small representative sample are that <strong>gold standard</strong>—AI judges, regression tests, and model comparisons all use it as their frame of reference.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">audit</span><span class="name">check if the AI is right</span></div><div class="ld">Lesson 29 asked "is the judge itself reliable". The answer is here: have both the AI judge and humans score the same traces and <strong>see whether they agree</strong>. Where they don't, fix the prompt or change the model—human annotation is the <strong>feedback loop that calibrates the judge</strong>.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">long tail</span><span class="name">cases the AI is unsure about</span></div><div class="ld">For samples where the AI's score keeps wavering, or that clearly need domain knowledge / value judgment, hand them straight to humans. Human annotation specializes in the <strong>long tail machines are worst at</strong>, spending scarce human effort where it matters most.</div></div>
</div>
""")

# (en sec2/3/spark below)

_EN32.append(r"""
<h2>The queue's data model: one scoring sheet + a basket of objects</h2>
<p>The annotation queue's data model has just two protagonists. <strong>AnnotationQueue</strong> is the "review task" itself: a name, a description, and crucially a set of <code>scoreConfigIds</code>—it <strong>binds Lesson 28's score configs</strong>, dictating which scores each reviewer in this queue must fill and on what scale (unifying everyone's ruler). <strong>AnnotationQueueItem</strong> is "one object to review in the basket": pointing at a trace/observation/session, with a PENDING→COMPLETED status.</p>

<table class="t">
  <thead><tr><th>field</th><th>meaning</th><th>why it matters</th></tr></thead>
  <tbody>
    <tr><td colspan="3" style="background:var(--purple-soft);font-weight:700">AnnotationQueue (review task)</td></tr>
    <tr><td><code>name / description</code></td><td>queue name and notes</td><td>a project can have several queues (e.g. "fact-check", "tone review")</td></tr>
    <tr><td><code>scoreConfigIds[]</code></td><td>the bound set of score configs</td><td><b>uniform scoring sheet</b>: all reviewers score by the same configs, so scores are comparable (echoing Lesson 28)</td></tr>
    <tr><td colspan="3" style="background:var(--blue-soft);font-weight:700">AnnotationQueueItem (one object to review)</td></tr>
    <tr><td><code>objectType / objectId</code></td><td>what's reviewed: TRACE / OBSERVATION / SESSION</td><td>three granularities—whole conversation, one step, or whole session</td></tr>
    <tr><td><code>status</code></td><td>PENDING / COMPLETED</td><td>queue progress is "how many PENDING remain"</td></tr>
    <tr><td><code>lockedAt / lockedByUserId</code></td><td>who's viewing, locked when</td><td>the next section's <b>5-minute lock</b>, preventing double-annotation</td></tr>
    <tr><td><code>annotatorUserId / completedAt</code></td><td>who reviewed, finished when</td><td>auditable: every human score knows whose hand it came from</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma:582-633</span><span class="ln">two models + two enums</span></div>
  <pre class="code"><span class="kw">model</span> AnnotationQueue {
  name           String
  scoreConfigIds String[]   <span class="cm">// ← binds Lesson 28's score configs, unifying this queue's sheet</span>
  annotationQueueItem  AnnotationQueueItem[]
  annotationQueueAssignment AnnotationQueueAssignment[]  <span class="cm">// which reviewers the queue is assigned to</span>
}
<span class="kw">model</span> AnnotationQueueItem {
  objectId   String;  objectType AnnotationQueueObjectType   <span class="cm">// the reviewed object</span>
  status     AnnotationQueueStatus @default(PENDING)          <span class="cm">// PENDING → COMPLETED</span>
  lockedAt   DateTime?;  lockedByUserId  String?              <span class="cm">// ← soft lock (5 minutes)</span>
  annotatorUserId String?;  completedAt DateTime?            <span class="cm">// who reviewed, finished when</span>
}
<span class="kw">enum</span> AnnotationQueueObjectType { TRACE  OBSERVATION  SESSION }
<span class="kw">enum</span> AnnotationQueueStatus     { PENDING  COMPLETED }</pre>
</div>

<p>There's a third model, <code>AnnotationQueueAssignment</code>: it <strong>assigns a queue to specific reviewers</strong>. So "who should review which queue" is structured too—not a link shared on the honor system, but a division of labor the platform records.</p>
""")

_EN32.append(r"""
<h2>The 5-minute soft lock: human-scale concurrency control</h2>
<p>With several reviewers eyeing one queue, how do you stop two from annotating the same item and wasting effort? A database transaction lock is too heavy and ill-fitting for the "a person reads for a while" rhythm. Langfuse uses a light <strong>time-based soft lock</strong>: a reviewer opens an item and it stamps <code>lockedByUserId</code> and <code>lockedAt</code>; judging "is it locked" only counts a lock from the <strong>last 5 minutes</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="The 5-minute soft lock: reviewer A opens an item writing lockedAt; within 5 minutes the item shows as locked to reviewer B and is skipped; if A leaves, the lock expires after 5 minutes and the item becomes available again, never permanently held">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">soft lock = lockedByUserId + lockedAt, valid only within 5 minutes</text>
  <rect x="40" y="40" width="120" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="100" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">reviewer A opens</text><text x="100" y="72" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">write lockedAt=now</text>
  <rect x="210" y="40" width="300" height="40" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="58" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">item locked (lockedAt &gt; now − 5min)</text><text x="360" y="72" text-anchor="middle" font-size="6.8" fill="var(--muted)">others see "locked", skip this one</text>
  <rect x="560" y="40" width="130" height="40" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="625" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">A done → COMPLETED</text><text x="625" y="72" text-anchor="middle" font-size="6.6" fill="var(--muted)">record annotatorUserId</text>
  <rect x="210" y="110" width="300" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="5 3"/><text x="360" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">if A leaves midway…</text><text x="360" y="146" text-anchor="middle" font-size="6.8" fill="var(--muted)">lock auto-expires after 5 min, item available again—never permanently held</text>
  <rect x="40" y="112" width="120" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="100" y="130" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">reviewer B takes</text><text x="100" y="144" text-anchor="middle" font-size="6.6" fill="var(--muted)">lock expired→available</text>
  <line x1="160" y1="60" x2="208" y2="60" stroke="var(--accent)" stroke-width="1.5"/><polygon points="208,60 199,56 199,64" fill="var(--accent)"/>
  <line x1="510" y1="60" x2="558" y2="60" stroke="var(--teal)" stroke-width="1.5"/><polygon points="558,60 549,56 549,64" fill="var(--teal)"/>
  <line x1="360" y1="80" x2="360" y2="108" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/>
  <line x1="160" y1="132" x2="208" y2="132" stroke="var(--blue)" stroke-width="1.4"/><polygon points="208,132 199,128 199,136" fill="var(--blue)"/>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">not a DB transaction lock but a "marker with an expiry"—fits the human "read for a few minutes" rhythm and never deadlocks</text>
  <text x="360" y="201" text-anchor="middle" font-size="8" fill="var(--faint)">closing the browser or losing the network doesn't matter: the lock vanishes on its own</text>
</svg>
<div class="figcap"><b>A soft lock, not a hard one</b>: <code>isItemLocked</code> only counts a lock whose <code>lockedAt</code> is within the last 5 minutes (<code>annotationQueueItemsRouter.ts:34-36</code>). It solves "human concurrency"—several people on one queue don't collide—and because it <b>auto-expires</b>, it never holds an item permanently just because someone closed their tab.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">annotationQueueItemsRouter.ts:34 · scores/hooks/useScoreMutations.ts:39</span><span class="ln">soft lock + emit score</span></div>
  <pre class="code"><span class="cm">// soft lock: only a "locked within the last 5 minutes" counts as locked—auto-expires</span>
<span class="kw">const</span> <span class="fn">isItemLocked</span> = (item) =&gt;
  item.lockedByUserId &amp;&amp; item.lockedAt &amp;&amp;
  <span class="kw">new</span> Date(item.lockedAt) &gt; <span class="kw">new</span> Date(Date.now() - <span class="st">5 * 60 * 1000</span>);   <span class="cm">// 5-minute window</span>

<span class="cm">// on finish: mark item COMPLETED and record the reviewer</span>
{ status: AnnotationQueueStatus.COMPLETED, annotatorUserId: ctx.session.user.id }

<span class="cm">// each score the reviewer fills: source=ANNOTATION, with authorUserId (who scored)</span>
createAnnotationScore({ source: <span class="st">"ANNOTATION"</span>, authorUserId, name, value, dataType, comment });
<span class="cm">// → like Lesson 29's EVAL scores, normalized and flowed back via L12 ingestion into one scores table</span></pre>
</div>

<p>The scores a reviewer fills have <code>source</code> set to <code>ANNOTATION</code>, carry an <code>authorUserId</code> (which reviewer), and may attach a <code>comment</code> with the reasoning—just like Lesson 29's EVAL scores, all normalized into scores and flowed back through Lesson 12's ingestion path into <strong>the same scores table</strong>. With that, all three sources from Lesson 28 are present: <strong>API, EVAL, ANNOTATION all converge—same table, same ruler, comparable</strong>. Part 5's through-line—"turn what happened into how well"—comes full circle here.</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>enter your assigned queue</h4><p>A reviewer sees the queues assigned to them (<code>AnnotationQueueAssignment</code>) and the PENDING items inside.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>take one → auto-lock</h4><p>Opening an item stamps <code>lockedByUserId/lockedAt</code>; for 5 minutes others see "locked" and skip it.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>review the object</h4><p>Per <code>objectType</code>, expand the TRACE / OBSERVATION / SESSION to review—reusing Lessons 25 & 26's detail views.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>score by config + comment</h4><p>Fill each of the queue's bound score configs, optionally with a <code>comment</code>. The scores are written as <code>source=ANNOTATION</code> with <code>authorUserId</code>.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>submit → next item</h4><p>The item is marked <code>COMPLETED</code> with <code>annotatorUserId/completedAt</code>, the lock releases, and the next PENDING item in the queue advances automatically.</p></div></div>
</div>
""")

_EN32.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why a "5-minute time-based soft lock" instead of a DB transaction lock or a permanent-hold marker?</strong> Because this lock must fit <strong>people</strong>, not machines. A DB transaction lock is millisecond-scale and ties up a connection—it can't survive "a person reading for minutes". And a permanent marker ("A is viewing" until A explicitly releases) means that once A closes the browser, loses network, or simply forgets, the item is <strong>held forever</strong> and no one can take it. The time-based soft lock pleases both ends: 5 minutes is enough for one person to finish one item and avoid collisions; and because it <strong>auto-expires</strong>, any mishap merely lets the lock "self-heal", never deadlocking. It's a neat application of "optimistic concurrency + a lease" to a human workflow—<strong>the granularity of a lock should match the rhythm of who it locks</strong>.<br><br>
  <strong>Why must human scores go into the same table and use the same config as AI scores?</strong> Because only with one ruler can you <strong>compare</strong>. Lay the human "gold standard" and the AI judge's scores on the same batch of traces, and a subtraction tells you where the judge is biased—this is the answer to Lesson 29's "how to trust the AI judge": <strong>use human annotation as the judge's yardstick</strong>. If each side used its own storage and its own scale, such calibration would be impossible. Langfuse having the three sources (API/EVAL/ANNOTATION) share one scores table and one set of configs is, at heart, to keep <strong>"how humans see it" and "how machines see it" always comparable side by side</strong>—the trustworthiness of the whole evaluation system ultimately rests on this.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Human annotation = the third score source (ANNOTATION)</strong>: the last piece of Lesson 28's three sources. The most costly and most authoritative, often used as ground truth—setting baselines, auditing "is the AI judge right", and handling the AI's uncertain long tail.</li>
    <li><strong>The annotation queue makes unordered review orderly</strong>: <code>AnnotationQueue</code> binds a set of <code>scoreConfigIds</code> (uniform sheet); <code>AnnotationQueueItem</code> points at a TRACE/OBSERVATION/SESSION with a PENDING→COMPLETED status; <code>AnnotationQueueAssignment</code> assigns queues to reviewers.</li>
    <li><strong>The 5-minute soft lock = human concurrency control</strong>: opening stamps <code>lockedAt</code>, and <code>isItemLocked</code> only counts a lock from the last 5 minutes. Many can review one queue without colliding, and because it auto-expires it <strong>never deadlocks</strong>—the lock's granularity matches the human rhythm.</li>
    <li><strong>Scores converge</strong>: a reviewer's config-driven scores carry <code>source=ANNOTATION</code>, an <code>authorUserId</code>, and an optional <code>comment</code>; the item is marked COMPLETED with annotatorUserId; the scores flow back through Lesson 12's ingestion into <strong>the same scores table</strong>.</li>
    <li><strong>The loop closes</strong>: API/EVAL/ANNOTATION are same-table, same-ruler, comparable—so human scores can serve as the AI judge's yardstick. This is the bedrock of evaluation trust, and it caps Part 5's "turn what happened into how well".</li>
  </ul>
</div>
""")

LESSON_32 = {"zh": "\n".join(_ZH32), "en": "\n".join(_EN32)}


# ══════════════════════════════════════════════════════════════════════
# L33 · 监控器与告警 / Monitors & alerting
# ══════════════════════════════════════════════════════════════════════
_ZH33 = []
_EN33 = []

_ZH33.append(r"""
<p class="lead">
Part 5 让你能给质量<strong>打分</strong>了——但分数躺在库里，你不可能一直盯着看。这一课讲 Part 5 的收尾，也是让评估<strong>真正起作用</strong>的最后一环：<strong>监控器（monitor）</strong>。它是「主动」的那一半——按固定节奏盯着某个指标或分数，一旦<strong>越过你设的线</strong>，就主动发出告警。一句话：把质量监测从「<strong>你去拉</strong>」（看仪表盘）变成「<strong>它来推</strong>」（异常即告警）。
我们会看到一个优雅的复用：<strong>monitor 本质上是一个「会自己盯着自己」的仪表盘组件</strong>；一台把指标值映射成 OK/WARNING/ALERT 的<strong>严重度状态机</strong>；以及一条「<strong>只在状态变化时才告警</strong>、并把投递解耦出去」的链路。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  仪表盘（第 40 课）像一份<strong>体检报告</strong>：你主动去翻，才知道指标如何。监控器则像一只<strong>可穿戴心率警报器</strong>：它<strong>自己盯着</strong>，平时不吭声，一旦心率冲出安全区间就<strong>主动报警</strong>——你不必时时盯屏。
  你给它设三样东西：<strong>正常的边界</strong>（阈值，如「错误率别超 5%」）、<strong>多久测一次</strong>（cadence，如每 5 分钟）、<strong>看最近多久的数据</strong>（window，如过去 1 小时）。它每到点就量一次、和边界比一比，得出一个<strong>严重度</strong>（正常 / 警告 / 告警）。
  贴心的是：它只在<strong>状态发生变化</strong>时响一声（从「正常」变「告警」才推送），而不是每 5 分钟都吵你一遍；要是异常一直不好，你还能设「<strong>每隔一阵再提醒一次</strong>」（renotify）。报警铃本身也不直接接到某一个设备——而是发到一个<strong>统一的通知中枢</strong>，再由它转给短信、Slack 或值班系统。
</div>
""")

_ZH33.append(r"""
<h2>一台会自己盯着自己的仪表盘组件</h2>
<p>monitor 最妙的设计，是它<strong>直接复用了仪表盘的查询形状</strong>。源码注释写得明明白白：Monitor 的查询字段「mirrors DashboardWidget」——同样的 <code>view</code>（看 observation 还是 score）、<code>filters</code>（过滤哪些数据）、<code>metric</code>（算什么指标）。区别只在于：仪表盘组件等你<strong>打开页面</strong>才算一次；monitor 则由一个<strong>调度器</strong>按 <code>cadenceMs</code> 反复地算、并把结果拿去<strong>比阈值</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 235" role="img" aria-label="监控流水线：调度器每到 nextRunAt 就把到期的 monitor 入队；处理器用与仪表盘相同的 view/filters/metric 在最近 windowMs 窗口算出一个指标值；computeSeverity 按 operator 比 alert/warning 阈值得出严重度；只有严重度变化才发告警到 WebhookQueue 再转投递">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">监控流水线：定时算指标 → 比阈值 → 变化才告警</text>
  <rect x="20" y="40" width="140" height="58" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="90" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">① 调度器</text><text x="90" y="76" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">nextRunAt 到期</text><text x="90" y="89" text-anchor="middle" font-size="6.8" fill="var(--muted)">claim 后入队 MonitorJob</text>
  <rect x="190" y="34" width="160" height="70" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="270" y="54" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">② 处理器算指标</text><text x="270" y="70" text-anchor="middle" font-size="6.6" fill="var(--muted)">view/filters/metric</text><text x="270" y="82" text-anchor="middle" font-size="6.6" fill="var(--muted)">（= 仪表盘组件的查询）</text><text x="270" y="95" text-anchor="middle" font-size="6.6" fill="var(--muted)">在最近 windowMs 窗口</text>
  <rect x="380" y="40" width="150" height="58" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="455" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">③ computeSeverity</text><text x="455" y="76" text-anchor="middle" font-size="6.6" fill="var(--muted)">value &lt;op&gt; 阈值</text><text x="455" y="89" text-anchor="middle" font-size="6.6" fill="var(--muted)">→ OK/WARNING/ALERT</text>
  <rect x="560" y="40" width="140" height="58" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="630" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">④ 状态机</text><text x="630" y="76" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">严重度变了吗？</text><text x="630" y="89" text-anchor="middle" font-size="6.6" fill="var(--muted)">变了才 emit 告警</text>
  <rect x="250" y="150" width="220" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-width="1.6"/><text x="360" y="169" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">⑤ WebhookQueue → 自动化</text><text x="360" y="184" text-anchor="middle" font-size="6.6" fill="var(--muted)">解耦投递：Slack / webhook（第 44 课）</text>
  <line x1="160" y1="69" x2="188" y2="69" stroke="var(--accent)" stroke-width="1.5"/><polygon points="188,69 179,65 179,73" fill="var(--accent)"/>
  <line x1="350" y1="69" x2="378" y2="69" stroke="var(--blue)" stroke-width="1.5"/><polygon points="378,69 369,65 369,73" fill="var(--blue)"/>
  <line x1="530" y1="69" x2="558" y2="69" stroke="var(--teal)" stroke-width="1.5"/><polygon points="558,69 549,65 549,73" fill="var(--teal)"/>
  <line x1="630" y1="98" x2="450" y2="148" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 3"/><polygon points="450,148 459,146 456,139" fill="var(--accent)"/><text x="556" y="128" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">仅当 emit=true</text>
  <text x="360" y="216" text-anchor="middle" font-size="8" fill="var(--faint)">仪表盘组件「等你看」；monitor 多了①调度 + ③④阈值与状态机——于是它「自己看，异常才喊你」</text>
  <text x="360" y="229" text-anchor="middle" font-size="8" fill="var(--faint)">同一套查询机制，pull（仪表盘）与 push（监控）两种姿态</text>
</svg>
<div class="figcap"><b>monitor = 自带调度与阈值的仪表盘组件</b>。<code>schema.prisma:1752</code> 的 Monitor 把 <code>view/filters/metric</code>（注释原文 <i>mirrors DashboardWidget</i>）和 <code>windowMs/cadenceMs/thresholdOperator/alertThreshold</code> 装在一起。worker 端 <code>monitorQueue.ts</code> 的 <code>MonitorProcessor.process</code> 跑②③④，越线才发⑤。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">看什么</span><span class="name">view / filters / metric</span></div><div class="ld">和仪表盘组件同款的查询三件套：<code>view</code> 决定盯 OBSERVATIONS 还是 SCORES_NUMERIC / SCORES_CATEGORICAL（<strong>能直接监控 Part 5 算出的分数</strong>），<code>filters</code> 圈定范围，<code>metric</code> 定义算什么（如平均分、错误率、P95 延迟）。一个 monitor 就是「一条仪表盘曲线 + 一条警戒线」。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">怎么测</span><span class="name">window / cadence</span></div><div class="ld"><code>windowMs</code> 是<strong>看最近多久</strong>的数据（滑动窗口，如过去 1 小时），<code>cadenceMs</code> 是<strong>多久测一次</strong>（如每 5 分钟）。两者解耦：你可以每 5 分钟、回看 1 小时——窗口给平滑、节奏给及时。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">何时响</span><span class="name">threshold / severity</span></div><div class="ld"><code>thresholdOperator</code>（GT/GTE/LT/LTE/EQ/NEQ）+ <code>alertThreshold</code>（必填）+ <code>warningThreshold</code>（选填两档）决定指标值落进哪个<strong>严重度</strong>。再由状态机决定<strong>这次要不要真的发告警</strong>（下两节细讲）。</div></div>
</div>
""")

# (L33 sec2 severity below)

_ZH33.append(r"""
<h2>严重度状态机：从指标值到 OK / WARNING / ALERT</h2>
<p>算出指标值后，<code>computeSeverity</code> 把它映射成一个<strong>严重度</strong>。逻辑很干净：先看值在不在（处理「没数据」），再按 operator 依次比<strong>告警线、警告线</strong>——撞上告警线就 ALERT，撞上警告线就 WARNING，都没撞就 OK。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="严重度状态机：指标值为空时按 noData 模式处理为 NO_DATA、补零或沿用上次；非空时若满足告警阈值则 ALERT、满足警告阈值则 WARNING、否则 OK；另有用户手动的 PAUSED 与初始 UNKNOWN">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">MonitorSeverity 六态（computeSeverity + 状态机）</text>
  <rect x="40" y="44" width="150" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="115" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">指标值 value？</text><text x="115" y="76" text-anchor="middle" font-size="6.6" fill="var(--muted)">先判空</text>
  <rect x="40" y="104" width="150" height="44" rx="9" fill="var(--bg)" stroke="var(--ink)" stroke-dasharray="4 3"/><text x="115" y="122" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">NO_DATA</text><text x="115" y="137" text-anchor="middle" font-size="6.2" fill="var(--muted)">按 noData 模式：补零/沿用/标无数据</text>
  <rect x="270" y="40" width="150" height="36" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="345" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ALERT</text>
  <rect x="270" y="90" width="150" height="36" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"/><text x="345" y="112" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">WARNING</text>
  <rect x="270" y="140" width="150" height="36" rx="9" fill="var(--teal)" opacity="0.18" stroke="var(--teal)"/><text x="345" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">OK</text>
  <rect x="500" y="60" width="90" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="545" y="81" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">PAUSED</text>
  <rect x="500" y="110" width="90" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="545" y="131" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">UNKNOWN</text>
  <text x="610" y="78" font-size="6.4" fill="var(--muted)">用户暂停</text><text x="600" y="128" font-size="6.4" fill="var(--muted)">初始/未知</text>
  <line x1="115" y1="84" x2="115" y2="102" stroke="var(--faint)" stroke-width="1.2"/><text x="150" y="98" font-size="6.2" fill="var(--muted)">空</text>
  <line x1="190" y1="58" x2="268" y2="58" stroke="var(--accent)" stroke-width="1.4"/><polygon points="268,58 259,54 259,62" fill="var(--accent)"/><text x="229" y="52" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">撞告警线</text>
  <line x1="190" y1="70" x2="268" y2="106" stroke="var(--accent)" stroke-width="1.2"/><polygon points="268,106 259,102 258,110" fill="var(--accent)"/><text x="226" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">撞警告线</text>
  <line x1="190" y1="78" x2="268" y2="156" stroke="var(--teal)" stroke-width="1.2"/><polygon points="268,156 259,153 258,161" fill="var(--teal)"/><text x="220" y="140" text-anchor="middle" font-size="6.2" fill="var(--teal)">都没撞</text>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">三个「生命周期态」NO_DATA/PAUSED/UNKNOWN + 三个「比阈值得到的态」ALERT/WARNING/OK</text>
</svg>
<div class="figcap"><b>六态严重度</b>：<code>MonitorSeverity = { PAUSED, UNKNOWN, NO_DATA, OK, WARNING, ALERT }</code>（<code>schema.prisma:1736</code>）。<code>computeSeverity</code> 先按 <code>noData</code> 模式处理空值，再按 operator 比 alert / warning 阈值。先比 ALERT 后比 WARNING——<strong>就高不就低</strong>，确保最严重的状态优先。</div>
</div>

<table class="t">
  <thead><tr><th>配置项</th><th>取值</th><th>作用</th></tr></thead>
  <tbody>
    <tr><td><code>thresholdOperator</code></td><td>GT / GTE / LT / LTE / EQ / NEQ</td><td>怎么比：错误率用 GT「超过」，成功率用 LT「低于」</td></tr>
    <tr><td><code>alertThreshold</code> / <code>warningThreshold</code></td><td>两条线（警告可选）</td><td>两档预警：先黄牌后红牌，给你缓冲</td></tr>
    <tr><td><code>noData.mode</code></td><td>SUBSTITUTE_ZERO / LAST_SEVERITY / SHOW_NO_DATA / NOTIFY_NO_DATA</td><td>没数据时怎么办：补 0 再判 / 沿用上次 / 标「无数据」/ 还为无数据告警</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/features/monitors/processor/computeSeverity.ts</span><span class="ln">值 → 严重度</span></div>
  <pre class="code"><span class="cm">// 空值：按 monitor 的 noData 模式决定</span>
<span class="kw">if</span> (value === <span class="kw">null</span>) {
  <span class="kw">if</span> (mode === <span class="st">"SUBSTITUTE_ZERO"</span>) value = 0;          <span class="cm">// 当作 0 继续比</span>
  <span class="kw">else if</span> (mode === <span class="st">"LAST_SEVERITY"</span>) <span class="kw">return</span> prevSeverity;  <span class="cm">// 沿用上次</span>
  <span class="kw">else</span> <span class="kw">return</span> <span class="st">"NO_DATA"</span>;                              <span class="cm">// 标记无数据</span>
}
<span class="cm">// 非空：先比告警线、再比警告线——就高不就低</span>
<span class="kw">if</span> (matches(value, operator, alertThreshold))   <span class="kw">return</span> <span class="st">"ALERT"</span>;
<span class="kw">if</span> (warningThreshold !== <span class="kw">null</span> &amp;&amp;
    matches(value, operator, warningThreshold))  <span class="kw">return</span> <span class="st">"WARNING"</span>;
<span class="kw">return</span> <span class="st">"OK"</span>;
<span class="cm">// matches: GT→value&gt;th, LT→value&lt;th, …（六种 operator）</span></pre>
</div>

<p>把抽象配置落到真实场景，三个典型 monitor 长这样——注意前两个直接盯着 Part 5 算出的<strong>分数</strong>：</p>
<div class="cols">
  <div class="col"><h4>有用性均分掉了</h4><p><code>view=SCORES_NUMERIC</code>，metric=「有用性」平均分，<code>operator=LT</code>，warning 0.75 / alert 0.70。窗口 1 小时、每 5 分钟测。<strong>质量回归的第一道哨兵。</strong></p></div>
  <div class="col"><h4>毒性通过率不达标</h4><p><code>view=SCORES_NUMERIC</code>（布尔分的通过率），metric=「无毒」占比，<code>operator=LT</code>，alert 0.95。安全红线一破即告警。</p></div>
  <div class="col"><h4>错误率飙升</h4><p><code>view=OBSERVATIONS</code>，metric=错误占比，<code>operator=GT</code>，alert 5%。不依赖 score，直接盯第 13 课的 observation 状态——上游一抖就知道。</p></div>
</div>
""")

_ZH33.append(r"""
<h2>只在变化时告警，且把投递解耦出去</h2>
<p>算出严重度，<strong>不等于</strong>就要发告警。如果每 5 分钟算一次、每次都因为「还在 ALERT」而推一条，你的 Slack 会被刷爆。<code>applyStateMachine</code> 解决这个：它对比<strong>上一次和这一次的严重度</strong>，原则上<strong>只在状态发生变化时才发</strong>（OK→ALERT 发、ALERT→ALERT 不发）；若异常持续，再按 <code>renotify</code> 策略<strong>隔一阵补一次</strong>。而且，被暂停（PAUSED）的 monitor 直接跳过——不覆盖用户意图。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="状态机决定是否发告警：上次 OK 这次 ALERT 则发；上次 ALERT 这次仍 ALERT 默认不发、除非 renotify 周期到；恢复为 OK 也发一条；告警统一发到 WebhookQueue，再由自动化转投递到 Slack 或 webhook">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">变化才 emit · 投递走统一队列</text>
  <rect x="30" y="44" width="150" height="40" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="105" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">上次 OK → 这次 ALERT</text><text x="105" y="76" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">变化 → 发！</text>
  <rect x="30" y="92" width="150" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="105" y="110" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">ALERT → 仍 ALERT</text><text x="105" y="124" text-anchor="middle" font-size="6.6" fill="var(--muted)">默认不发（防刷屏）</text>
  <rect x="30" y="140" width="150" height="40" rx="9" fill="var(--amber-soft)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="105" y="158" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">持续异常 + renotify 到点</text><text x="105" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">补一次提醒</text>
  <rect x="250" y="80" width="160" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="330" y="102" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">emit 决策</text><text x="330" y="119" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">applyStateMachine</text><text x="330" y="132" text-anchor="middle" font-size="6.4" fill="var(--muted)">PAUSED 直接跳过</text>
  <rect x="470" y="60" width="220" height="42" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="1.6"/><text x="580" y="79" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">WebhookQueue（统一通知中枢）</text><text x="580" y="94" text-anchor="middle" font-size="6.4" fill="var(--muted)">monitor 只管发布，不管怎么投</text>
  <rect x="470" y="116" width="105" height="38" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="522" y="139" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">Slack</text>
  <rect x="585" y="116" width="105" height="38" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="637" y="139" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">webhook</text>
  <line x1="180" y1="64" x2="248" y2="98" stroke="var(--teal)" stroke-width="1.4"/><polygon points="248,98 239,95 242,103" fill="var(--teal)"/>
  <line x1="180" y1="160" x2="248" y2="124" stroke="var(--accent)" stroke-width="1.3"/><polygon points="248,124 239,124 243,131" fill="var(--accent)"/>
  <line x1="410" y1="98" x2="468" y2="84" stroke="var(--accent)" stroke-width="1.5"/><polygon points="468,84 459,82 461,90" fill="var(--accent)"/>
  <line x1="560" y1="102" x2="535" y2="114" stroke="var(--blue)" stroke-width="1.2"/><line x1="600" y1="102" x2="625" y2="114" stroke="var(--blue)" stroke-width="1.2"/>
  <text x="360" y="194" text-anchor="middle" font-size="8" fill="var(--faint)">「变化才发」防刷屏 + 「统一队列再分发」让 monitor 不必认识每种投递渠道（第 44 课自动化）</text>
</svg>
<div class="figcap"><b>两层克制</b>：<code>applyStateMachine</code>（<code>processor/applyStateMachine.ts</code>）按「严重度是否变化 + renotify」决定 <code>emit</code>，PAUSED 不覆盖用户意图；真要发时，<code>monitorQueue.ts</code> 只把告警<b>发布到 WebhookQueue</b>，由自动化系统（Trigger→Action）决定投到 Slack 还是 webhook。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">processor/applyStateMachine.ts · worker/src/queues/monitorQueue.ts</span><span class="ln">是否发 + 怎么发</span></div>
  <pre class="code"><span class="cm">// 是否发：暂停跳过；否则按「严重度变化 + renotify」决定 emit</span>
<span class="kw">if</span> (prev.severity === <span class="st">"PAUSED"</span>) <span class="kw">return</span> { emit: <span class="kw">false</span>, … };   <span class="cm">// 不覆盖用户意图</span>
<span class="kw">const</span> severityChanged = prev.severity !== next.severity;
<span class="kw">const</span> emit = shouldEmit({ prev, next, prevAlertedAt, renotify, … });  <span class="cm">// 变化或到点才 true</span>

<span class="cm">// 怎么发：monitor 不直接发 Slack，只发布到 WebhookQueue（解耦投递）</span>
<span class="kw">const</span> processor = <span class="kw">new</span> MonitorProcessor(prisma, <span class="kw">async</span> (input) =&gt; {
  <span class="kw">await</span> webhookQueue.add(QueueName.WebhookQueue, { payload: input, … });
});
<span class="kw">await</span> processor.process(job.data.payload, <span class="kw">new</span> Date());   <span class="cm">// 算指标→定severity→（必要时）发布</span></pre>
</div>

<p>这条链路把 Part 5 推到了终点：从第 28 课「一个 score 长什么样」，到 29–32 课「四种方式生产 score」，再到这一课「<strong>盯着这些分数/指标，越线就主动喊人</strong>」。评估终于<strong>闭环成行动</strong>——你不再只是<strong>能</strong>看到质量，而是质量一掉，系统就<strong>替你</strong>看到、并立刻通知你。而「发布到 WebhookQueue、由自动化转投递」这一步，正好接上 Part 7 的自动化与集成（第 44 课）——监控只是众多「会触发自动化的事件源」之一。</p>
""")

# (L33 spark+key below)

_ZH33.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么 monitor 要复用仪表盘的查询形状，而不是自成一套？</strong> 因为「监控的指标」和「仪表盘看的指标」<strong>本来就是同一个东西</strong>——平均分、错误率、P95 延迟。让 Monitor 的 <code>view/filters/metric</code> 直接 mirror DashboardWidget，意味着：你在仪表盘上画得出的任何曲线，都能<strong>一键变成一个会自己盯着的告警</strong>；底层那套 ClickHouse 查询机制只写一遍、两处复用。<strong>pull 与 push 共享同一个指标定义</strong>，这是少有的「既省代码又顺直觉」的设计。<br><br>
  <strong>为什么只在「状态变化」时告警，而不是每次越线都发？</strong> 因为<strong>告警疲劳</strong>是监控系统的头号杀手。如果错误率持续高，每 5 分钟一条「还在告警」，工程师很快就会把整个频道静音——于是真正的新问题也被淹没。「变化才发 + renotify 周期补发」让每条告警都<strong>携带信息量</strong>（状态真的变了），既不漏报、又不刷屏。severity 做成<strong>状态机</strong>而非每次重算的瞬时值，正是为了能问出「<strong>和上次比变了吗</strong>」这个关键问题。<br><br>
  <strong>为什么告警不直接发 Slack，而要先发布到 WebhookQueue？</strong> 又是那个贯穿全书的信念——<strong>解耦</strong>。monitor 的职责是「判断要不要告警」，<strong>不该</strong>关心「告警怎么送到人手里」（Slack？webhook？邮件？值班系统？）。把告警发布到统一队列，再由自动化系统（第 44 课的 Trigger→Action）决定投递渠道，于是：投递方式可独立演进、可重试、可对接任意新渠道，而 monitor 一行不改。<strong>判断与投递分离</strong>，和第 30 课「创建与执行分离」、第 12 课「一个入口多个生产者」是同一种架构品味。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>monitor = 主动的评估</strong>：把质量监测从「你去拉仪表盘」变成「它来推告警」。按 <code>cadenceMs</code> 定时在最近 <code>windowMs</code> 窗口算指标，越线即告警。</li>
    <li><strong>复用仪表盘查询形状</strong>：<code>view/filters/metric</code> 注释原文「mirrors DashboardWidget」——能画成曲线的指标就能变成告警；<code>view</code> 含 SCORES_NUMERIC/CATEGORICAL，<strong>可直接监控 Part 5 算出的分数</strong>。</li>
    <li><strong>严重度状态机</strong>：<code>computeSeverity</code> 按 operator（GT/GTE/LT/LTE/EQ/NEQ）先比告警线、再比警告线，得 OK/WARNING/ALERT；空值按 <code>noData</code> 模式处理（补零/沿用/标无数据）；另有 PAUSED/UNKNOWN 生命周期态。</li>
    <li><strong>只在变化时告警</strong>：<code>applyStateMachine</code> 比上次与这次的严重度，原则上<strong>变化才发</strong>，持续异常按 <code>renotify</code> 补发，PAUSED 不覆盖——根治告警疲劳。</li>
    <li><strong>解耦投递</strong>：monitor 只把告警发布到 <code>WebhookQueue</code>，由自动化（第 44 课 Trigger→Action）转投 Slack / webhook。判断与投递分离，呼应第 30 课「创建/执行分离」。</li>
    <li><strong>Part 5 闭环</strong>：从「score 的模型」（28）→「四种生产 score 的方式」（29–32）→「盯着 score/指标主动告警」（33）。评估从「能看见质量」升级为「质量一掉就被通知」——真正成为行动。</li>
  </ul>
</div>
""")

_EN33.append(r"""
<p class="lead">
Part 5 let you <strong>score</strong> quality—but scores sit in a database, and you can't watch them forever. This lesson caps Part 5 and adds the last link that makes evaluation <strong>actually act</strong>: the <strong>monitor</strong>. It's the "active" half—watching a metric or score on a fixed cadence, and when it <strong>crosses a line you set</strong>, raising an alert on its own. In one phrase: turn quality monitoring from "<strong>you pull</strong>" (look at a dashboard) into "<strong>it pushes</strong>" (alert on anomaly).
We'll see an elegant reuse: <strong>a monitor is essentially a dashboard widget that watches itself</strong>; a <strong>severity state machine</strong> mapping a metric value into OK/WARNING/ALERT; and a path that "<strong>only alerts on a state change</strong> and decouples delivery away".
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  A dashboard (Lesson 40) is like a <strong>checkup report</strong>: you flip it open to learn how things are. A monitor is like a <strong>wearable heart-rate alarm</strong>: it <strong>watches on its own</strong>, stays quiet, and the moment your rate leaves the safe zone it <strong>sounds an alert</strong>—you needn't stare at a screen.
  You set it three things: the <strong>normal boundary</strong> (threshold, e.g. "error rate under 5%"), <strong>how often to measure</strong> (cadence, e.g. every 5 minutes), and <strong>how far back to look</strong> (window, e.g. the past hour). At each tick it measures once, compares against the boundary, and yields a <strong>severity</strong> (OK / warning / alert).
  The thoughtful bit: it only beeps when the <strong>state changes</strong> (it pushes when "OK" becomes "alert"), not every 5 minutes; and if the anomaly persists, you can set it to "<strong>remind again every so often</strong>" (renotify). The alarm bell itself isn't wired to one device either—it goes to a <strong>unified notification hub</strong>, which forwards to SMS, Slack, or an on-call system.
</div>
""")

_EN33.append(r"""
<h2>A dashboard widget that watches itself</h2>
<p>The neatest part of a monitor is that it <strong>directly reuses the dashboard's query shape</strong>. The source comment says it plainly: a Monitor's query fields "mirror DashboardWidget"—the same <code>view</code> (observations or scores), <code>filters</code> (which data), <code>metric</code> (what to compute). The only difference: a dashboard widget computes once when you <strong>open the page</strong>; a monitor is computed repeatedly by a <strong>scheduler</strong> per <code>cadenceMs</code> and the result is taken to <strong>compare against a threshold</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 235" role="img" aria-label="The monitor pipeline: a scheduler enqueues due monitors at nextRunAt; the processor computes a metric value over the recent windowMs using the same view/filters/metric as a dashboard; computeSeverity compares it to the alert/warning thresholds by operator to yield a severity; only a severity change emits an alert to the WebhookQueue for delivery">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">monitor pipeline: scheduled metric → threshold → alert only on change</text>
  <rect x="20" y="40" width="140" height="58" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="90" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">① scheduler</text><text x="90" y="76" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">nextRunAt due</text><text x="90" y="89" text-anchor="middle" font-size="6.8" fill="var(--muted)">claim → enqueue MonitorJob</text>
  <rect x="190" y="34" width="160" height="70" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="270" y="54" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">② processor computes</text><text x="270" y="70" text-anchor="middle" font-size="6.6" fill="var(--muted)">view/filters/metric</text><text x="270" y="82" text-anchor="middle" font-size="6.6" fill="var(--muted)">(= a dashboard widget's query)</text><text x="270" y="95" text-anchor="middle" font-size="6.6" fill="var(--muted)">over the recent windowMs</text>
  <rect x="380" y="40" width="150" height="58" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="455" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">③ computeSeverity</text><text x="455" y="76" text-anchor="middle" font-size="6.6" fill="var(--muted)">value &lt;op&gt; threshold</text><text x="455" y="89" text-anchor="middle" font-size="6.6" fill="var(--muted)">→ OK/WARNING/ALERT</text>
  <rect x="560" y="40" width="140" height="58" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="630" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">④ state machine</text><text x="630" y="76" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">did severity change?</text><text x="630" y="89" text-anchor="middle" font-size="6.6" fill="var(--muted)">emit only if so</text>
  <rect x="250" y="150" width="220" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-width="1.6"/><text x="360" y="169" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">⑤ WebhookQueue → automation</text><text x="360" y="184" text-anchor="middle" font-size="6.6" fill="var(--muted)">decoupled delivery: Slack / webhook (Lesson 44)</text>
  <line x1="160" y1="69" x2="188" y2="69" stroke="var(--accent)" stroke-width="1.5"/><polygon points="188,69 179,65 179,73" fill="var(--accent)"/>
  <line x1="350" y1="69" x2="378" y2="69" stroke="var(--blue)" stroke-width="1.5"/><polygon points="378,69 369,65 369,73" fill="var(--blue)"/>
  <line x1="530" y1="69" x2="558" y2="69" stroke="var(--teal)" stroke-width="1.5"/><polygon points="558,69 549,65 549,73" fill="var(--teal)"/>
  <line x1="630" y1="98" x2="450" y2="148" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 3"/><polygon points="450,148 459,146 456,139" fill="var(--accent)"/><text x="556" y="128" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">only if emit=true</text>
  <text x="360" y="216" text-anchor="middle" font-size="8" fill="var(--faint)">a dashboard widget "waits for you to look"; a monitor adds ① scheduling + ③④ thresholds and state machine—so it "looks itself, calls you only on anomaly"</text>
  <text x="360" y="229" text-anchor="middle" font-size="8" fill="var(--faint)">one query mechanism, two postures: pull (dashboard) and push (monitor)</text>
</svg>
<div class="figcap"><b>monitor = a dashboard widget with built-in scheduling and thresholds</b>. <code>schema.prisma:1752</code>'s Monitor packs <code>view/filters/metric</code> (the comment literally says <i>mirrors DashboardWidget</i>) together with <code>windowMs/cadenceMs/thresholdOperator/alertThreshold</code>. On the worker, <code>monitorQueue.ts</code>'s <code>MonitorProcessor.process</code> runs ②③④ and only emits ⑤ when a line is crossed.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">what</span><span class="name">view / filters / metric</span></div><div class="ld">The same query trio as a dashboard widget: <code>view</code> decides whether to watch OBSERVATIONS or SCORES_NUMERIC / SCORES_CATEGORICAL (<strong>so it can directly monitor the scores Part 5 produced</strong>), <code>filters</code> scope the data, <code>metric</code> defines what to compute (avg score, error rate, P95 latency). A monitor is "one dashboard curve + one alarm line".</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">how</span><span class="name">window / cadence</span></div><div class="ld"><code>windowMs</code> is <strong>how far back</strong> to look (a sliding window, e.g. the past hour); <code>cadenceMs</code> is <strong>how often</strong> to measure (e.g. every 5 minutes). The two are decoupled: you can measure every 5 minutes looking back 1 hour—the window gives smoothing, the cadence gives timeliness.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">when</span><span class="name">threshold / severity</span></div><div class="ld"><code>thresholdOperator</code> (GT/GTE/LT/LTE/EQ/NEQ) + <code>alertThreshold</code> (required) + <code>warningThreshold</code> (optional two-tier) decide which <strong>severity</strong> the value falls into. The state machine then decides <strong>whether to actually send an alert this time</strong> (next two sections).</div></div>
</div>
""")

# (en sec2/3/spark below)

_EN33.append(r"""
<h2>The severity state machine: from a value to OK / WARNING / ALERT</h2>
<p>Once the metric value is computed, <code>computeSeverity</code> maps it to a <strong>severity</strong>. The logic is clean: first check whether the value exists (handle "no data"), then compare by operator against the <strong>alert line, then the warning line</strong>—hit the alert line → ALERT, hit the warning line → WARNING, neither → OK.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="Severity state machine: a null value is handled per noData mode as NO_DATA, zero-substituted, or carried over; a present value yields ALERT if it meets the alert threshold, WARNING if it meets the warning threshold, otherwise OK; plus user-set PAUSED and initial UNKNOWN">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">MonitorSeverity, six states (computeSeverity + state machine)</text>
  <rect x="40" y="44" width="150" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="115" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">metric value?</text><text x="115" y="76" text-anchor="middle" font-size="6.6" fill="var(--muted)">check null first</text>
  <rect x="40" y="104" width="150" height="44" rx="9" fill="var(--bg)" stroke="var(--ink)" stroke-dasharray="4 3"/><text x="115" y="122" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">NO_DATA</text><text x="115" y="137" text-anchor="middle" font-size="6.0" fill="var(--muted)">per noData mode: zero/carry-over/flag</text>
  <rect x="270" y="40" width="150" height="36" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="345" y="62" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ALERT</text>
  <rect x="270" y="90" width="150" height="36" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"/><text x="345" y="112" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">WARNING</text>
  <rect x="270" y="140" width="150" height="36" rx="9" fill="var(--teal)" opacity="0.18" stroke="var(--teal)"/><text x="345" y="162" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">OK</text>
  <rect x="500" y="60" width="90" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="545" y="81" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">PAUSED</text>
  <rect x="500" y="110" width="90" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="545" y="131" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">UNKNOWN</text>
  <text x="605" y="78" font-size="6.4" fill="var(--muted)">user-paused</text><text x="600" y="128" font-size="6.4" fill="var(--muted)">initial</text>
  <line x1="115" y1="84" x2="115" y2="102" stroke="var(--faint)" stroke-width="1.2"/><text x="142" y="98" font-size="6.2" fill="var(--muted)">null</text>
  <line x1="190" y1="58" x2="268" y2="58" stroke="var(--accent)" stroke-width="1.4"/><polygon points="268,58 259,54 259,62" fill="var(--accent)"/><text x="229" y="52" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">meets alert</text>
  <line x1="190" y1="70" x2="268" y2="106" stroke="var(--accent)" stroke-width="1.2"/><polygon points="268,106 259,102 258,110" fill="var(--accent)"/><text x="225" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">meets warning</text>
  <line x1="190" y1="78" x2="268" y2="156" stroke="var(--teal)" stroke-width="1.2"/><polygon points="268,156 259,153 258,161" fill="var(--teal)"/><text x="221" y="142" text-anchor="middle" font-size="6.2" fill="var(--teal)">neither</text>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">three "lifecycle" states NO_DATA/PAUSED/UNKNOWN + three "threshold-derived" states ALERT/WARNING/OK</text>
</svg>
<div class="figcap"><b>Six-state severity</b>: <code>MonitorSeverity = { PAUSED, UNKNOWN, NO_DATA, OK, WARNING, ALERT }</code> (<code>schema.prisma:1736</code>). <code>computeSeverity</code> first handles null per the <code>noData</code> mode, then compares the alert / warning thresholds by operator. Alert is checked before warning—<strong>highest wins</strong>, ensuring the most severe state takes priority.</div>
</div>

<table class="t">
  <thead><tr><th>config</th><th>values</th><th>role</th></tr></thead>
  <tbody>
    <tr><td><code>thresholdOperator</code></td><td>GT / GTE / LT / LTE / EQ / NEQ</td><td>how to compare: error rate uses GT "exceeds", success rate uses LT "falls below"</td></tr>
    <tr><td><code>alertThreshold</code> / <code>warningThreshold</code></td><td>two lines (warning optional)</td><td>two-tier warning: yellow card then red card, giving you a buffer</td></tr>
    <tr><td><code>noData.mode</code></td><td>SUBSTITUTE_ZERO / LAST_SEVERITY / SHOW_NO_DATA / NOTIFY_NO_DATA</td><td>what to do with no data: treat as 0 / carry over last / flag "no data" / even alert for no data</td></tr>
  </tbody>
</table>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/features/monitors/processor/computeSeverity.ts</span><span class="ln">value → severity</span></div>
  <pre class="code"><span class="cm">// null value: decide per the monitor's noData mode</span>
<span class="kw">if</span> (value === <span class="kw">null</span>) {
  <span class="kw">if</span> (mode === <span class="st">"SUBSTITUTE_ZERO"</span>) value = 0;          <span class="cm">// treat as 0 and continue</span>
  <span class="kw">else if</span> (mode === <span class="st">"LAST_SEVERITY"</span>) <span class="kw">return</span> prevSeverity;  <span class="cm">// carry over last</span>
  <span class="kw">else</span> <span class="kw">return</span> <span class="st">"NO_DATA"</span>;                              <span class="cm">// flag no data</span>
}
<span class="cm">// present value: check alert line first, then warning line — highest wins</span>
<span class="kw">if</span> (matches(value, operator, alertThreshold))   <span class="kw">return</span> <span class="st">"ALERT"</span>;
<span class="kw">if</span> (warningThreshold !== <span class="kw">null</span> &amp;&amp;
    matches(value, operator, warningThreshold))  <span class="kw">return</span> <span class="st">"WARNING"</span>;
<span class="kw">return</span> <span class="st">"OK"</span>;
<span class="cm">// matches: GT→value&gt;th, LT→value&lt;th, … (six operators)</span></pre>
</div>

<p>Grounding the abstract config in real scenarios, three typical monitors look like this—note the first two watch the <strong>scores</strong> Part 5 produced:</p>
<div class="cols">
  <div class="col"><h4>helpfulness average dropped</h4><p><code>view=SCORES_NUMERIC</code>, metric=avg "helpfulness", <code>operator=LT</code>, warning 0.75 / alert 0.70. Window 1 hour, measured every 5 minutes. <strong>The first sentinel for quality regression.</strong></p></div>
  <div class="col"><h4>toxicity pass-rate below target</h4><p><code>view=SCORES_NUMERIC</code> (a boolean score's pass-rate), metric=share "non-toxic", <code>operator=LT</code>, alert 0.95. A safety red line alerts the moment it's crossed.</p></div>
  <div class="col"><h4>error rate spiking</h4><p><code>view=OBSERVATIONS</code>, metric=share of errors, <code>operator=GT</code>, alert 5%. No score needed—watches Lesson 13's observation status directly, so an upstream wobble shows immediately.</p></div>
</div>
""")

_EN33.append(r"""
<h2>Alert only on change, and decouple delivery away</h2>
<p>Computing a severity does <strong>not</strong> mean an alert must fire. If you compute every 5 minutes and push each time because it's "still ALERT", your Slack drowns. <code>applyStateMachine</code> fixes this: it compares <strong>the previous and current severity</strong> and, as a rule, <strong>only emits on a state change</strong> (OK→ALERT emits, ALERT→ALERT doesn't); if the anomaly persists, it tops up per the <code>renotify</code> policy. And a PAUSED monitor is skipped outright—not overwriting user intent.</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="The state machine decides whether to alert: previous OK now ALERT emits; previous ALERT still ALERT by default doesn't, unless the renotify period elapses; recovery to OK also emits; alerts all go to the WebhookQueue, which automation forwards to Slack or webhook">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">emit only on change · delivery via one queue</text>
  <rect x="30" y="44" width="150" height="40" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="105" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">prev OK → now ALERT</text><text x="105" y="76" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">change → emit!</text>
  <rect x="30" y="92" width="150" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="105" y="110" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">ALERT → still ALERT</text><text x="105" y="124" text-anchor="middle" font-size="6.6" fill="var(--muted)">default no emit (anti-spam)</text>
  <rect x="30" y="140" width="150" height="40" rx="9" fill="var(--amber-soft)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="105" y="158" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">persists + renotify due</text><text x="105" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">top up a reminder</text>
  <rect x="250" y="80" width="160" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="330" y="102" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">emit decision</text><text x="330" y="119" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">applyStateMachine</text><text x="330" y="132" text-anchor="middle" font-size="6.4" fill="var(--muted)">PAUSED skipped</text>
  <rect x="470" y="60" width="220" height="42" rx="10" fill="var(--bg)" stroke="var(--accent)" stroke-width="1.6"/><text x="580" y="79" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">WebhookQueue (one notification hub)</text><text x="580" y="94" text-anchor="middle" font-size="6.4" fill="var(--muted)">monitor only publishes, not how to deliver</text>
  <rect x="470" y="116" width="105" height="38" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="522" y="139" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">Slack</text>
  <rect x="585" y="116" width="105" height="38" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="637" y="139" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">webhook</text>
  <line x1="180" y1="64" x2="248" y2="98" stroke="var(--teal)" stroke-width="1.4"/><polygon points="248,98 239,95 242,103" fill="var(--teal)"/>
  <line x1="180" y1="160" x2="248" y2="124" stroke="var(--accent)" stroke-width="1.3"/><polygon points="248,124 239,124 243,131" fill="var(--accent)"/>
  <line x1="410" y1="98" x2="468" y2="84" stroke="var(--accent)" stroke-width="1.5"/><polygon points="468,84 459,82 461,90" fill="var(--accent)"/>
  <line x1="560" y1="102" x2="535" y2="114" stroke="var(--blue)" stroke-width="1.2"/><line x1="600" y1="102" x2="625" y2="114" stroke="var(--blue)" stroke-width="1.2"/>
  <text x="360" y="194" text-anchor="middle" font-size="8" fill="var(--faint)">"emit only on change" prevents spam + "one queue then fan out" frees the monitor from knowing each delivery channel (Lesson 44 automation)</text>
</svg>
<div class="figcap"><b>Two layers of restraint</b>: <code>applyStateMachine</code> (<code>processor/applyStateMachine.ts</code>) decides <code>emit</code> by "did severity change + renotify", and PAUSED doesn't overwrite user intent; when it does fire, <code>monitorQueue.ts</code> only <b>publishes the alert to the WebhookQueue</b>, leaving the automation system (Trigger→Action) to decide Slack vs webhook.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">processor/applyStateMachine.ts · worker/src/queues/monitorQueue.ts</span><span class="ln">whether to send + how</span></div>
  <pre class="code"><span class="cm">// whether: skip if paused; else decide emit by "severity change + renotify"</span>
<span class="kw">if</span> (prev.severity === <span class="st">"PAUSED"</span>) <span class="kw">return</span> { emit: <span class="kw">false</span>, … };   <span class="cm">// don't overwrite user intent</span>
<span class="kw">const</span> severityChanged = prev.severity !== next.severity;
<span class="kw">const</span> emit = shouldEmit({ prev, next, prevAlertedAt, renotify, … });  <span class="cm">// true only on change or due</span>

<span class="cm">// how: a monitor doesn't send Slack directly, only publishes to WebhookQueue (decoupled)</span>
<span class="kw">const</span> processor = <span class="kw">new</span> MonitorProcessor(prisma, <span class="kw">async</span> (input) =&gt; {
  <span class="kw">await</span> webhookQueue.add(QueueName.WebhookQueue, { payload: input, … });
});
<span class="kw">await</span> processor.process(job.data.payload, <span class="kw">new</span> Date());   <span class="cm">// compute→severity→(if needed) publish</span></pre>
</div>

<p>This path pushes Part 5 to its finish: from Lesson 28's "what a score looks like", through Lessons 29–32's "four ways to produce a score", to this lesson's "<strong>watch those scores/metrics and call someone the moment a line is crossed</strong>". Evaluation finally <strong>closes the loop into action</strong>—you no longer merely <strong>can</strong> see quality; the moment quality drops, the system sees it <strong>for you</strong> and notifies you at once. And the "publish to WebhookQueue, let automation deliver" step dovetails into Part 7's automation and integrations (Lesson 44)—monitoring is just one of many "event sources that can trigger automation".</p>
""")

_EN33.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why reuse the dashboard's query shape instead of inventing one?</strong> Because "a monitored metric" and "a dashboarded metric" are <strong>the same thing</strong>—avg score, error rate, P95 latency. Having Monitor's <code>view/filters/metric</code> directly mirror DashboardWidget means: any curve you can draw on a dashboard can <strong>become a self-watching alert in one click</strong>; the underlying ClickHouse query machinery is written once, reused twice. <strong>Pull and push share one metric definition</strong>—a rare "saves code and matches intuition" design.<br><br>
  <strong>Why alert only on a "state change" rather than every time a line is crossed?</strong> Because <strong>alert fatigue</strong> is a monitoring system's number-one killer. If error rate stays high and "still alerting" pings every 5 minutes, engineers soon mute the whole channel—and real new problems get buried. "Emit on change + renotify top-ups" makes every alert <strong>carry information</strong> (the state really changed), neither missing nor spamming. Making severity a <strong>state machine</strong> rather than a per-tick instantaneous value is precisely so it can ask the key question: "<strong>did it change from last time</strong>".<br><br>
  <strong>Why not send Slack directly, but publish to the WebhookQueue first?</strong> Again the belief that runs through this whole guide—<strong>decoupling</strong>. A monitor's job is "decide whether to alert"; it <strong>shouldn't</strong> care "how the alert reaches a human" (Slack? webhook? email? on-call?). Publishing alerts to one queue, with the automation system (Lesson 44's Trigger→Action) deciding the channel, means delivery can evolve independently, be retried, and connect to any new channel—while the monitor changes not a line. <strong>Decision separate from delivery</strong>, the same architectural taste as Lesson 30's "creation separate from execution" and Lesson 12's "one entry, many producers".
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A monitor = active evaluation</strong>: turn quality monitoring from "you pull a dashboard" into "it pushes an alert". It computes a metric over the recent <code>windowMs</code> per <code>cadenceMs</code>, alerting when a line is crossed.</li>
    <li><strong>Reuses the dashboard query shape</strong>: <code>view/filters/metric</code> (the comment literally says "mirrors DashboardWidget")—any chartable metric can become an alert; <code>view</code> includes SCORES_NUMERIC/CATEGORICAL, so it can <strong>directly monitor the scores Part 5 produced</strong>.</li>
    <li><strong>Severity state machine</strong>: <code>computeSeverity</code> compares the alert line then the warning line by operator (GT/GTE/LT/LTE/EQ/NEQ), yielding OK/WARNING/ALERT; null is handled per <code>noData</code> mode (zero/carry-over/flag); plus PAUSED/UNKNOWN lifecycle states.</li>
    <li><strong>Alert only on change</strong>: <code>applyStateMachine</code> compares previous and current severity, as a rule <strong>emitting only on change</strong>, topping up persistent anomalies per <code>renotify</code>, never overwriting PAUSED—curing alert fatigue.</li>
    <li><strong>Decoupled delivery</strong>: a monitor only publishes alerts to the <code>WebhookQueue</code>, with automation (Lesson 44's Trigger→Action) forwarding to Slack / webhook. Decision separate from delivery, echoing Lesson 30's "creation/execution split".</li>
    <li><strong>Part 5 closes the loop</strong>: from "the score model" (28) → "four ways to produce a score" (29–32) → "watch scores/metrics and alert actively" (33). Evaluation graduates from "can see quality" to "gets notified the moment quality drops"—truly becoming action.</li>
  </ul>
</div>
""")

LESSON_33 = {"zh": "\n".join(_ZH33), "en": "\n".join(_EN33)}
