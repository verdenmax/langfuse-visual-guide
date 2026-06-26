"""Part 6 — 数据集与实验 / Datasets & experiments. Lessons L34–L36.

Same authoring pattern as part1..part5: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L34 · 数据集与数据项 / Datasets & items
# ══════════════════════════════════════════════════════════════════════
_ZH34 = []
_EN34 = []

_ZH34.append(r"""
<p class="lead">
评估需要「考题」。你想知道改了 prompt、换了模型之后应用变好还是变差——就得有一套<strong>固定的测试用例</strong>反复地考它。这套测试用例，就是<strong>数据集（dataset）</strong>；其中每一道题，就是一个<strong>数据项（dataset item）</strong>：一份输入 + 一份期望输出。
这一课讲数据集和数据项的<strong>数据模型</strong>，重点是两个让人眼前一亮的设计：数据项可以从<strong>真实的生产 trace「提拔」</strong>成测试用例（线上遇到的难题，直接变成回归测试题），以及数据项是<strong>版本化</strong>的——改一次题留一版历史，于是「上次实验用的到底是哪版题」永远查得到。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  数据集像一套<strong>标准试卷</strong>。每道题（item）有<strong>题干</strong>（input）和<strong>参考答案</strong>（expectedOutput）。出题有两种来路：你可以<strong>现编</strong>一道，也可以把线上真实遇到的、应用答砸了的难题（一条 trace）<strong>原样收录</strong>进卷子——「生产事故」就这样变成了「回归考题」。
  最讲究的是改题规则：当你修订一道题，系统<strong>不会抹掉旧版</strong>，而是给旧版盖一个「<strong>有效截止</strong>」的戳、再另起一张新版。于是这道题的每一版都留着，「<strong>三月那次考试用的是哪一版题干</strong>」永远翻得出来——这对「实验要可复现」是命根子。
</div>
""")

# (L34 sections appended below)

_ZH34.append(r"""
<h2>数据集 = 一组测试用例，题可以从生产「捡」</h2>
<p>数据模型很直观：一个 <strong>Dataset</strong> 装着一组 <strong>DatasetItem</strong>。Dataset 有名字、描述，还能挂 <code>inputSchema</code> / <code>expectedOutputSchema</code> 给题目定个格式规范。每个 DatasetItem 的核心是三样：<code>input</code>（题干）、<code>expectedOutput</code>（参考答案）、<code>metadata</code>（旁注）。但真正巧妙的是另外两个字段：<code>sourceTraceId</code> 和 <code>sourceObservationId</code>——它们记着「这道题是从哪条真实 trace 来的」。</p>

<div class="fig">
<svg viewBox="0 0 720 235" role="img" aria-label="数据集模型：一个 Dataset 含多个 DatasetItem，每个 item 有 input/expectedOutput/metadata；item 可以现编，也可以从一条真实生产 trace 经 sourceTraceId 提拔而来，把线上难题变成回归测试用例">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">数据集装一组测试用例，题可现编也可从生产捡</text>
  <rect x="250" y="36" width="220" height="48" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="56" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">Dataset（一套试卷）</text><text x="360" y="73" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">name · 描述 · input/expectedOutput Schema</text>
  <rect x="40" y="110" width="200" height="56" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">DatasetItem A（现编）</text><text x="140" y="146" text-anchor="middle" font-size="6.8" fill="var(--muted)">input + expectedOutput</text><text x="140" y="159" text-anchor="middle" font-size="6.6" fill="var(--faint)">手动出的题</text>
  <rect x="260" y="110" width="200" height="56" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">DatasetItem B</text><text x="360" y="146" text-anchor="middle" font-size="6.8" fill="var(--muted)">input + expectedOutput</text><text x="360" y="159" text-anchor="middle" font-size="6.6" fill="var(--faint)">metadata 旁注</text>
  <rect x="480" y="110" width="200" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="580" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">DatasetItem C（从生产捡）</text><text x="580" y="146" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">sourceTraceId → 某条真实 trace</text><text x="580" y="159" text-anchor="middle" font-size="6.4" fill="var(--muted)">线上难题变回归题</text>
  <rect x="480" y="186" width="200" height="34" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="580" y="206" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">一条生产 trace（第 13 课）</text>
  <line x1="320" y1="84" x2="160" y2="108" stroke="var(--faint)" stroke-width="1.2"/><line x1="360" y1="84" x2="360" y2="108" stroke="var(--faint)" stroke-width="1.2"/><line x1="400" y1="84" x2="560" y2="108" stroke="var(--faint)" stroke-width="1.2"/>
  <line x1="580" y1="186" x2="580" y2="168" stroke="var(--accent)" stroke-width="1.5"/><polygon points="580,166 576,175 584,175" fill="var(--accent)"/><text x="638" y="180" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">提拔</text>
  <text x="360" y="230" text-anchor="middle" font-size="8" fill="var(--faint)">「生产即测试源」：把线上真实答砸的 case 一键收录成考题，让回归测试紧贴真实分布</text>
</svg>
<div class="figcap"><b>题从哪来</b>：<code>schema.prisma:685</code> 的 DatasetItem 有 <code>input</code>/<code>expectedOutput</code>/<code>metadata</code>，外加 <code>sourceTraceId</code>/<code>sourceObservationId</code>——后两者让你把一条真实 trace（第 13 课）<b>提拔</b>成测试用例。Dataset（<code>:661</code>）还能用 <code>inputSchema</code>/<code>expectedOutputSchema</code> 约束题目格式。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">题干 + 答案</span><span class="name">input / expectedOutput</span></div><div class="ld">一个 item 的本体：<code>input</code> 喂给应用的输入、<code>expectedOutput</code> 你期望它给出的参考答案。评估时就拿应用的真实输出和 expectedOutput 对照（或交给第 29–31 课的评判）。<code>metadata</code> 放标签、难度等旁注。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">从生产捡</span><span class="name">sourceTraceId / sourceObservationId</span></div><div class="ld">这是数据集最有生命力的来源：在 trace 详情里看到一个应用答砸的真实案例，<strong>一键收录</strong>成 item，<code>sourceTraceId</code> 记下出处。于是你的测试集<strong>紧贴真实流量分布</strong>，而不是凭空想象的玩具题。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">状态</span><span class="name">DatasetStatus</span></div><div class="ld">item 有 ACTIVE / ARCHIVED 两态：归档不删除、只是退出测试集，历史与关联仍在。数据集本身也能挂 schema（<code>inputSchema</code>/<code>expectedOutputSchema</code>）给新题定规矩。</div></div>
</div>

<p>一个建好的数据集能干三件大事——它是 Part 6 后两课的地基：</p>
<div class="cols">
  <div class="col"><h4>回归测试</h4><p>改 prompt / 换模型后，把整套题重跑一遍，对照分数有没有掉——防止「修了一个 bug，带崩三个 case」。</p></div>
  <div class="col"><h4>实验对比</h4><p>同一套题，用不同配置各跑一次（第 35–36 课的 run），把多次结果并排比，挑出最优组合。</p></div>
  <div class="col"><h4>few-shot 示例库</h4><p>数据项的 input/expectedOutput 也能当作 prompt 里的<strong>示例</strong>（第 37 课），让模型照着标准答案的样子答。</p></div>
</div>
""")

# (L34 sec2 versioning below)

_ZH34.append(r"""
<h2>版本化：改一次题，关旧版、开新版</h2>
<p>数据项最精巧的设计是<strong>版本化</strong>。看主键就懂了：<code>@@id([id, projectId, validFrom])</code>——同一道题（同 <code>id</code>）可以有<strong>多行</strong>，靠 <code>validFrom</code> 区分版本。每行还有一个 <code>validTo</code>：为空（<code>null</code>）的那行就是<strong>当前生效</strong>版。改题时，系统在一个事务里做两步——给旧版盖上 <code>validTo</code>（关闭它的有效区间）、再插入一行新版。这正是数据库里经典的「<strong>缓慢变化维 / 双时态</strong>」手法。</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="数据项版本化时间轴：同一道题 id 有多个版本，每版有 validFrom 到 validTo 的有效区间，当前版的 validTo 为空；改题时旧版盖上 validTo、新版以 validFrom 开始；一次 dataset run 钉住某个 validFrom 所以永远看到当时那版">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">同一道题 id 的版本时间轴（validFrom → validTo）</text>
  <line x1="40" y1="150" x2="690" y2="150" stroke="var(--faint)" stroke-width="1.5"/><polygon points="690,150 682,146 682,154" fill="var(--faint)"/><text x="690" y="168" text-anchor="end" font-size="7" fill="var(--muted)">时间</text>
  <rect x="60" y="60" width="200" height="40" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="160" y="78" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">版本 1（旧）</text><text x="160" y="92" text-anchor="middle" font-size="6.6" fill="var(--muted)">validFrom=t1 · validTo=t2</text>
  <rect x="290" y="60" width="200" height="40" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="390" y="78" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">版本 2（旧）</text><text x="390" y="92" text-anchor="middle" font-size="6.6" fill="var(--muted)">validFrom=t2 · validTo=t3</text>
  <rect x="520" y="60" width="170" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="605" y="78" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">版本 3（当前）</text><text x="605" y="92" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">validFrom=t3 · validTo=null</text>
  <line x1="160" y1="100" x2="160" y2="150" stroke="var(--faint)" stroke-width="1" stroke-dasharray="3 2"/><text x="70" y="120" font-size="6.6" fill="var(--muted)">t1</text>
  <line x1="390" y1="100" x2="390" y2="150" stroke="var(--faint)" stroke-width="1" stroke-dasharray="3 2"/><text x="300" y="120" font-size="6.6" fill="var(--muted)">t2 关旧·开新</text>
  <line x1="605" y1="100" x2="605" y2="150" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 2"/><text x="528" y="120" font-size="6.6" fill="var(--accent-ink)">t3 关旧·开新</text>
  <rect x="300" y="160" width="180" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="390" y="179" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">3 月的 run 钉住 validFrom=t2</text>
  <line x1="390" y1="160" x2="390" y2="102" stroke="var(--blue)" stroke-width="1.2"/><polygon points="390,100 386,109 394,109" fill="var(--blue)"/>
</svg>
<div class="figcap"><b>双时态版本</b>：当前版 = <code>validTo IS NULL</code> 的那行。改题在事务里「关旧版（盖 validTo）+ 插新版（新 validFrom）」。一次 dataset run <b>钉住</b>某个 <code>validFrom</code>，所以它永远看到「当时那版题」——这正是第 30 课 eval 用 <code>datasetItemValidFrom</code> 的原因。源码：<code>dataset-items.ts:418-470</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/repositories/dataset-items.ts:418-470</span><span class="ln">VERSIONED 写入</span></div>
  <pre class="code"><span class="cm">// 在一个事务里：先关旧版，再插新版（缓慢变化维 Type 2）</span>
<span class="kw">await</span> prisma.$transaction(<span class="kw">async</span> (tx) =&gt; {
  <span class="cm">// 0. 找到当前生效版（validTo 为空的那行）</span>
  <span class="kw">const</span> current = <span class="kw">await</span> tx.datasetItem.findFirst({
    where: { id: itemId, projectId, validTo: <span class="kw">null</span> }, orderBy: { validFrom: <span class="st">"desc"</span> } });
  <span class="kw">const</span> newValidFrom = <span class="kw">new</span> Date(Math.max(Date.now(), baseTs + 1));

  <span class="cm">// 1. 给旧版盖上 validTo —— 关闭它的有效区间</span>
  <span class="kw">if</span> (current) <span class="kw">await</span> tx.datasetItem.update({ where: {…current.validFrom}, data: { validTo: newValidFrom } });

  <span class="cm">// 2. 插入新版 —— validFrom = 刚才那个时刻，validTo 默认 null（成为新的当前版）</span>
  <span class="kw">await</span> tx.datasetItem.create({ data: { ...itemData, validFrom: newValidFrom } });
});</pre>
</div>

<p>为什么大费周章不直接「原地改」？因为<strong>实验必须可复现</strong>。你三月跑了一次实验、打了分；六月改了几道题再跑一次。如果题是「原地改」的，那三月那次的分就<strong>失去了语境</strong>——你不知道它当时考的是哪版题，两次实验根本没法公平比较。版本化把每道题的每一版都钉在时间轴上，于是「三月的 run 用的是 t2 版、六月的 run 用的是 t3 版」清清楚楚，历史结论永远可解释。</p>

<table class="t">
  <thead><tr><th>id（逻辑题）</th><th>validFrom</th><th>validTo</th><th>是否当前</th><th>内容</th></tr></thead>
  <tbody>
    <tr><td>item-42</td><td>t1</td><td>t2</td><td>否（历史）</td><td>题干 v1</td></tr>
    <tr><td>item-42</td><td>t2</td><td>t3</td><td>否（历史）</td><td>题干 v2</td></tr>
    <tr><td>item-42</td><td>t3</td><td><b>null</b></td><td><b>是 ✓</b></td><td>题干 v3（当前）</td></tr>
  </tbody>
</table>
<p>三行<strong>同一个 id</strong>、不同 <code>validFrom</code>，靠 <code>validTo</code> 是否为空区分「当前 vs 历史」。查「现在这道题长啥样」就 <code>WHERE validTo IS NULL</code>；查「t2 那次实验用的是啥」就找 <code>validFrom ≤ t2 &lt; validTo</code> 的那行——一张表同时回答「现在」和「任意历史时刻」两个问题，这就是双时态的威力。</p>
""")

# (L34 spark+key below)

_ZH34.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么数据项要版本化，而不是简单地原地更新？</strong> 一句话：<strong>为了让历史实验永远可解释、可复现</strong>。评估的全部价值在于「比较」——这次比上次好还是差。但如果测试题本身会被悄悄改掉，那「上次」的分数就成了无根之木：你不知道它当时考的是什么，自然没法和「这次」公平对比。版本化用 <code>validFrom/validTo</code> 给每道题的每一版钉上时间区间，让每次 run 都能<strong>钉死</strong>它当时用的那一版（第 30 课 eval 取数据时正是带着 <code>datasetItemValidFrom</code> 精确回放）。这是「不可变历史 + 可移动当前指针」的经典思路，和第 37 课的 prompt 版本、git 的 commit 是同一种工程信念：<strong>真相一旦记录就不抹改，要变就追加新版本</strong>。<br><br>
  <strong>为什么要让数据项能从真实 trace「提拔」？</strong> 因为<strong>最好的测试题就藏在生产事故里</strong>。凭空想象的测试用例往往覆盖不到真实用户那些刁钻的、长尾的输入；而线上每一次应用答砸的 trace，都是一道现成的、带着真实分布的好题。<code>sourceTraceId</code> 让「发现问题 → 收录成回归题 → 下次改进后验证」形成闭环——观测平台不只让你看见问题，还顺手把问题变成防止它复发的「疫苗」。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>数据集 = 一组测试用例</strong>：Dataset 装一组 DatasetItem，每个 item = <code>input</code>（题干）+ <code>expectedOutput</code>（参考答案）+ <code>metadata</code>。它是评估的「考卷」，配合第 28–32 课的 score 用。</li>
    <li><strong>题可从生产「提拔」</strong>：<code>sourceTraceId</code>/<code>sourceObservationId</code> 让你把一条真实 trace（第 13 课）一键收录成测试用例——回归集紧贴真实流量分布，而非凭空臆造。</li>
    <li><strong>数据项是版本化的</strong>：主键 <code>(id, projectId, validFrom)</code> 让同一道题多版本共存；当前版 = <code>validTo IS NULL</code>。改题在事务里「关旧版（盖 validTo）+ 插新版」——缓慢变化维 / 双时态。</li>
    <li><strong>版本化是为了可复现</strong>：一次 run 钉住某个 <code>validFrom</code>，永远看到「当时那版题」（第 30 课 eval 用 <code>datasetItemValidFrom</code> 精确回放）。历史实验因此永远可解释、可公平对比。</li>
    <li><strong>不可变历史 + 可移动指针</strong>：和第 37 课 prompt 版本、git commit 同一种信念——真相记录后不抹改，变更追加新版本。</li>
  </ul>
</div>
""")

_EN34.append(r"""
<p class="lead">
Evaluation needs "exam questions". To know whether your app got better or worse after you changed a prompt or swapped a model, you need a <strong>fixed set of test cases</strong> to quiz it on repeatedly. That set is a <strong>dataset</strong>; each question in it is a <strong>dataset item</strong>: one input + one expected output.
This lesson covers the <strong>data model</strong> of datasets and items, focusing on two delightful designs: an item can be <strong>"promoted" from a real production trace</strong> into a test case (a hard case you hit in production becomes a regression test), and items are <strong>versioned</strong>—editing a question keeps a version of history, so "which version of the question did last experiment use" is always answerable.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  A dataset is like a <strong>standard exam paper</strong>. Each question (item) has a <strong>prompt</strong> (input) and a <strong>reference answer</strong> (expectedOutput). Questions come two ways: you can <strong>write</strong> one, or you can <strong>capture verbatim</strong> a real, botched case from production (a trace) into the paper—a "production incident" thus becomes a "regression question".
  The most careful part is the edit rule: when you revise a question, the system <strong>does not erase the old version</strong>—it stamps the old one with a "<strong>valid-until</strong>" and starts a new version. So every version of the question is kept, and "<strong>which version of the prompt did the March exam use</strong>" is always retrievable—lifeblood for "experiments must be reproducible".
</div>
""")

_EN34.append(r"""
<h2>A dataset = a set of test cases, and questions can be "picked" from production</h2>
<p>The data model is intuitive: a <strong>Dataset</strong> holds a set of <strong>DatasetItems</strong>. A Dataset has a name, a description, and can attach <code>inputSchema</code> / <code>expectedOutputSchema</code> to give questions a format spec. Each DatasetItem's core is three things: <code>input</code> (the prompt), <code>expectedOutput</code> (the reference answer), <code>metadata</code> (side notes). But the truly clever fields are two others: <code>sourceTraceId</code> and <code>sourceObservationId</code>—they record "which real trace this question came from".</p>

<div class="fig">
<svg viewBox="0 0 720 235" role="img" aria-label="Dataset model: a Dataset holds many DatasetItems, each with input/expectedOutput/metadata; an item can be authored, or promoted from a real production trace via sourceTraceId, turning a production hard case into a regression test case">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">a dataset holds test cases; questions authored or picked from production</text>
  <rect x="250" y="36" width="220" height="48" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="56" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">Dataset (an exam paper)</text><text x="360" y="73" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">name · description · input/expectedOutput Schema</text>
  <rect x="40" y="110" width="200" height="56" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="140" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">DatasetItem A (authored)</text><text x="140" y="146" text-anchor="middle" font-size="6.8" fill="var(--muted)">input + expectedOutput</text><text x="140" y="159" text-anchor="middle" font-size="6.6" fill="var(--faint)">hand-written question</text>
  <rect x="260" y="110" width="200" height="56" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="360" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">DatasetItem B</text><text x="360" y="146" text-anchor="middle" font-size="6.8" fill="var(--muted)">input + expectedOutput</text><text x="360" y="159" text-anchor="middle" font-size="6.6" fill="var(--faint)">metadata side notes</text>
  <rect x="480" y="110" width="200" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="580" y="130" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">DatasetItem C (from production)</text><text x="580" y="146" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">sourceTraceId → a real trace</text><text x="580" y="159" text-anchor="middle" font-size="6.4" fill="var(--muted)">production hard case → regression q</text>
  <rect x="480" y="186" width="200" height="34" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="580" y="206" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">a production trace (Lesson 13)</text>
  <line x1="320" y1="84" x2="160" y2="108" stroke="var(--faint)" stroke-width="1.2"/><line x1="360" y1="84" x2="360" y2="108" stroke="var(--faint)" stroke-width="1.2"/><line x1="400" y1="84" x2="560" y2="108" stroke="var(--faint)" stroke-width="1.2"/>
  <line x1="580" y1="186" x2="580" y2="168" stroke="var(--accent)" stroke-width="1.5"/><polygon points="580,166 576,175 584,175" fill="var(--accent)"/><text x="632" y="180" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">promote</text>
  <text x="360" y="230" text-anchor="middle" font-size="8" fill="var(--faint)">"production as test source": capture a real botched case into a question, keeping regression tests close to the real distribution</text>
</svg>
<div class="figcap"><b>Where questions come from</b>: <code>schema.prisma:685</code>'s DatasetItem has <code>input</code>/<code>expectedOutput</code>/<code>metadata</code>, plus <code>sourceTraceId</code>/<code>sourceObservationId</code>—the latter let you <b>promote</b> a real trace (Lesson 13) into a test case. A Dataset (<code>:661</code>) can also constrain question format via <code>inputSchema</code>/<code>expectedOutputSchema</code>.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">prompt + answer</span><span class="name">input / expectedOutput</span></div><div class="ld">An item's body: <code>input</code> is fed to the app, <code>expectedOutput</code> is the reference answer you expect. Evaluation compares the app's real output against expectedOutput (or hands it to Lessons 29–31's judges). <code>metadata</code> holds tags, difficulty, and other notes.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">from production</span><span class="name">sourceTraceId / sourceObservationId</span></div><div class="ld">The dataset's most vital source: spotting a real botched case in a trace detail, you <strong>capture it in one click</strong> as an item, with <code>sourceTraceId</code> recording its origin. So your test set <strong>hugs the real traffic distribution</strong>, not imagined toy questions.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">status</span><span class="name">DatasetStatus</span></div><div class="ld">An item is ACTIVE / ARCHIVED: archiving doesn't delete—it just retires the item from the test set, keeping history and links. The dataset itself can attach a schema (<code>inputSchema</code>/<code>expectedOutputSchema</code>) to set rules for new questions.</div></div>
</div>

<p>A built dataset can do three big things—it's the foundation for the next two lessons of Part 6:</p>
<div class="cols">
  <div class="col"><h4>regression testing</h4><p>After changing a prompt / swapping a model, re-run the whole set and check whether scores dropped—preventing "fix one bug, break three cases".</p></div>
  <div class="col"><h4>experiment comparison</h4><p>The same set, run once per config (Lessons 35–36's runs), with multiple results placed side by side to pick the best combination.</p></div>
  <div class="col"><h4>few-shot example bank</h4><p>An item's input/expectedOutput can also serve as <strong>examples</strong> in a prompt (Lesson 37), letting the model answer in the shape of the reference answers.</p></div>
</div>
""")

# (en sec2 + spark below)

_EN34.append(r"""
<h2>Versioning: edit a question by closing the old version, opening a new</h2>
<p>An item's most refined design is <strong>versioning</strong>. The primary key says it all: <code>@@id([id, projectId, validFrom])</code>—the same question (same <code>id</code>) can have <strong>multiple rows</strong>, distinguished by <code>validFrom</code>. Each row also has a <code>validTo</code>: the row where it's <code>null</code> is the <strong>currently active</strong> version. On edit, the system does two steps in a transaction—stamp the old version with <code>validTo</code> (close its validity interval), then insert a new version row. This is the database's classic "<strong>slowly-changing dimension / bitemporal</strong>" technique.</p>

<div class="fig">
<svg viewBox="0 0 720 200" role="img" aria-label="Dataset item versioning timeline: the same question id has multiple versions, each with a validFrom-to-validTo interval, the current version's validTo being null; on edit the old version gets validTo and the new starts at validFrom; a dataset run pins a validFrom so it always sees that version">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">version timeline of one question id (validFrom → validTo)</text>
  <line x1="40" y1="150" x2="690" y2="150" stroke="var(--faint)" stroke-width="1.5"/><polygon points="690,150 682,146 682,154" fill="var(--faint)"/><text x="690" y="168" text-anchor="end" font-size="7" fill="var(--muted)">time</text>
  <rect x="60" y="60" width="200" height="40" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="160" y="78" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">version 1 (old)</text><text x="160" y="92" text-anchor="middle" font-size="6.6" fill="var(--muted)">validFrom=t1 · validTo=t2</text>
  <rect x="290" y="60" width="200" height="40" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="390" y="78" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">version 2 (old)</text><text x="390" y="92" text-anchor="middle" font-size="6.6" fill="var(--muted)">validFrom=t2 · validTo=t3</text>
  <rect x="520" y="60" width="170" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="605" y="78" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">version 3 (current)</text><text x="605" y="92" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">validFrom=t3 · validTo=null</text>
  <line x1="160" y1="100" x2="160" y2="150" stroke="var(--faint)" stroke-width="1" stroke-dasharray="3 2"/><text x="70" y="120" font-size="6.6" fill="var(--muted)">t1</text>
  <line x1="390" y1="100" x2="390" y2="150" stroke="var(--faint)" stroke-width="1" stroke-dasharray="3 2"/><text x="300" y="120" font-size="6.6" fill="var(--muted)">t2 close+open</text>
  <line x1="605" y1="100" x2="605" y2="150" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 2"/><text x="528" y="120" font-size="6.6" fill="var(--accent-ink)">t3 close+open</text>
  <rect x="300" y="160" width="180" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="390" y="179" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">March's run pins validFrom=t2</text>
  <line x1="390" y1="160" x2="390" y2="102" stroke="var(--blue)" stroke-width="1.2"/><polygon points="390,100 386,109 394,109" fill="var(--blue)"/>
</svg>
<div class="figcap"><b>Bitemporal versions</b>: the current version = the row with <code>validTo IS NULL</code>. An edit, in a transaction, "closes the old version (stamps validTo) + inserts a new version (new validFrom)". A dataset run <b>pins</b> a <code>validFrom</code>, so it always sees "that version of the question"—exactly why Lesson 30's eval uses <code>datasetItemValidFrom</code>. Source: <code>dataset-items.ts:418-470</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/repositories/dataset-items.ts:418-470</span><span class="ln">VERSIONED write</span></div>
  <pre class="code"><span class="cm">// in one transaction: close the old version, then insert the new (SCD Type 2)</span>
<span class="kw">await</span> prisma.$transaction(<span class="kw">async</span> (tx) =&gt; {
  <span class="cm">// 0. find the current version (the row with validTo null)</span>
  <span class="kw">const</span> current = <span class="kw">await</span> tx.datasetItem.findFirst({
    where: { id: itemId, projectId, validTo: <span class="kw">null</span> }, orderBy: { validFrom: <span class="st">"desc"</span> } });
  <span class="kw">const</span> newValidFrom = <span class="kw">new</span> Date(Math.max(Date.now(), baseTs + 1));

  <span class="cm">// 1. stamp the old version with validTo — close its validity interval</span>
  <span class="kw">if</span> (current) <span class="kw">await</span> tx.datasetItem.update({ where: {…current.validFrom}, data: { validTo: newValidFrom } });

  <span class="cm">// 2. insert the new version — validFrom = that moment, validTo defaults null (the new current)</span>
  <span class="kw">await</span> tx.datasetItem.create({ data: { ...itemData, validFrom: newValidFrom } });
});</pre>
</div>

<p>Why go to all this trouble instead of editing in place? Because <strong>experiments must be reproducible</strong>. You ran an experiment in March and got scores; in June you tweaked a few questions and ran again. If questions were "edited in place", March's scores would <strong>lose their context</strong>—you wouldn't know which version they tested, and the two experiments couldn't be compared fairly. Versioning pins every version of every question on a timeline, so "March's run used version t2, June's used t3" is crystal clear, and historical conclusions stay forever explainable.</p>

<table class="t">
  <thead><tr><th>id (logical question)</th><th>validFrom</th><th>validTo</th><th>current?</th><th>content</th></tr></thead>
  <tbody>
    <tr><td>item-42</td><td>t1</td><td>t2</td><td>no (history)</td><td>prompt v1</td></tr>
    <tr><td>item-42</td><td>t2</td><td>t3</td><td>no (history)</td><td>prompt v2</td></tr>
    <tr><td>item-42</td><td>t3</td><td><b>null</b></td><td><b>yes ✓</b></td><td>prompt v3 (current)</td></tr>
  </tbody>
</table>
<p>Three rows with the <strong>same id</strong>, different <code>validFrom</code>, distinguished as "current vs history" by whether <code>validTo</code> is null. To ask "what does this question look like now", <code>WHERE validTo IS NULL</code>; to ask "what did the t2 experiment use", find the row where <code>validFrom ≤ t2 &lt; validTo</code>—one table answers both "now" and "any historical moment", the power of bitemporal.</p>
""")

_EN34.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why version dataset items rather than simply update in place?</strong> In a phrase: <strong>to keep historical experiments forever explainable and reproducible</strong>. The whole value of evaluation is "comparison"—is this better or worse than last time. But if the test questions are silently edited, "last time"'s score becomes rootless: you don't know what it tested, and can't fairly compare with "this time". Versioning uses <code>validFrom/validTo</code> to pin a time interval on every version of every question, letting each run <strong>pin</strong> the version it used (Lesson 30's eval replays exactly via <code>datasetItemValidFrom</code>). It's the classic "immutable history + a movable current pointer", the same belief as Lesson 37's prompt versions and git commits: <strong>once truth is recorded it's not erased; to change, append a new version</strong>.<br><br>
  <strong>Why let items be "promoted" from real traces?</strong> Because <strong>the best test questions hide in production incidents</strong>. Imagined test cases rarely cover the tricky, long-tail inputs real users throw; whereas every botched production trace is a ready-made, real-distribution question. <code>sourceTraceId</code> closes the loop "find a problem → capture it as a regression question → verify after improving"—an observability platform not only lets you see problems but turns them into "vaccines" against recurrence.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A dataset = a set of test cases</strong>: a Dataset holds DatasetItems, each = <code>input</code> (prompt) + <code>expectedOutput</code> (reference answer) + <code>metadata</code>. It's the "exam paper" for evaluation, used with Lessons 28–32's scores.</li>
    <li><strong>Questions can be "promoted" from production</strong>: <code>sourceTraceId</code>/<code>sourceObservationId</code> let you capture a real trace (Lesson 13) into a test case in one click—the regression set hugs the real traffic distribution, not made-up cases.</li>
    <li><strong>Items are versioned</strong>: the key <code>(id, projectId, validFrom)</code> lets many versions of one question coexist; the current = <code>validTo IS NULL</code>. An edit, in a transaction, "closes the old (stamps validTo) + inserts the new"—slowly-changing dimension / bitemporal.</li>
    <li><strong>Versioning is for reproducibility</strong>: a run pins a <code>validFrom</code>, always seeing "that version" (Lesson 30's eval replays via <code>datasetItemValidFrom</code>). Historical experiments stay explainable and fairly comparable.</li>
    <li><strong>Immutable history + a movable pointer</strong>: the same belief as Lesson 37's prompt versions and git commits—record truth without erasing it; append a new version to change.</li>
  </ul>
</div>
""")

LESSON_34 = {"zh": "\n".join(_ZH34), "en": "\n".join(_EN34)}
