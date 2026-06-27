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

<svg viewBox="0 0 720 220" role="img" aria-label="同一个 id item-42 的三个版本在时间轴上各占一个有效区间：v1 从 t1 到 t2、v2 从 t2 到 t3、v3 从 t3 起 validTo 为 null 是当前版；查现在就 WHERE validTo IS NULL 得 v3，查 t2 时刻就找 validFrom 小于等于 t2 小于 validTo 得 v2，历史可复现">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">同一个 id 三版，靠 validTo 是否为空分「当前 vs 历史」</text>
  <line x1="70" y1="126" x2="680" y2="126" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="676" y="120" font-size="9.5" text-anchor="end" fill="var(--muted)">时间 →</text>
  <rect x="90" y="72" width="156" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="168" y="92" font-size="10" text-anchor="middle" fill="var(--muted)">题干 v1（历史）</text>
  <rect x="250" y="72" width="156" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="328" y="92" font-size="10" text-anchor="middle" fill="var(--muted)">题干 v2（历史）</text>
  <rect x="410" y="72" width="240" height="32" rx="6" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="530" y="92" font-size="10" text-anchor="middle" fill="var(--accent-ink)">题干 v3 · validTo=null ✓ 当前</text>
  <line x1="90" y1="66" x2="90" y2="132" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <line x1="250" y1="66" x2="250" y2="132" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <line x1="410" y1="66" x2="410" y2="132" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <line x1="650" y1="66" x2="650" y2="132" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <text x="90" y="146" font-size="9.5" text-anchor="middle" fill="var(--ink)">t1</text>
  <text x="250" y="146" font-size="9.5" text-anchor="middle" fill="var(--ink)">t2</text>
  <text x="410" y="146" font-size="9.5" text-anchor="middle" fill="var(--ink)">t3</text>
  <text x="650" y="146" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">现在</text>
  <text x="70" y="176" font-size="10" fill="var(--ink)">查「现在」：WHERE validTo IS NULL → v3</text>
  <text x="70" y="198" font-size="10" fill="var(--ink)">查「t2 时刻」：validFrom ≤ t2 &lt; validTo → v2（历史可复现）</text>
</svg>
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

<svg viewBox="0 0 720 220" role="img" aria-label="the same id item-42 has three versions each occupying a valid interval on the time axis: v1 from t1 to t2, v2 from t2 to t3, and v3 from t3 onward with validTo null as the current version; to ask now use WHERE validTo IS NULL to get v3, to ask at t2 find validFrom less than or equal to t2 less than validTo to get v2, so history is reproducible">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">same id, three versions; current vs history by whether validTo is null</text>
  <line x1="70" y1="126" x2="680" y2="126" stroke="var(--faint)" stroke-width="1.5"></line>
  <text x="676" y="120" font-size="9.5" text-anchor="end" fill="var(--muted)">time →</text>
  <rect x="90" y="72" width="156" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="168" y="92" font-size="10" text-anchor="middle" fill="var(--muted)">question v1 (history)</text>
  <rect x="250" y="72" width="156" height="32" rx="6" fill="var(--bg)" stroke="var(--faint)"></rect>
  <text x="328" y="92" font-size="10" text-anchor="middle" fill="var(--muted)">question v2 (history)</text>
  <rect x="410" y="72" width="240" height="32" rx="6" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="530" y="92" font-size="10" text-anchor="middle" fill="var(--accent-ink)">question v3 · validTo=null ✓ current</text>
  <line x1="90" y1="66" x2="90" y2="132" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <line x1="250" y1="66" x2="250" y2="132" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <line x1="410" y1="66" x2="410" y2="132" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <line x1="650" y1="66" x2="650" y2="132" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 3"></line>
  <text x="90" y="146" font-size="9.5" text-anchor="middle" fill="var(--ink)">t1</text>
  <text x="250" y="146" font-size="9.5" text-anchor="middle" fill="var(--ink)">t2</text>
  <text x="410" y="146" font-size="9.5" text-anchor="middle" fill="var(--ink)">t3</text>
  <text x="650" y="146" font-size="9.5" text-anchor="middle" fill="var(--accent-ink)">now</text>
  <text x="70" y="176" font-size="10" fill="var(--ink)">ask "now": WHERE validTo IS NULL → v3</text>
  <text x="70" y="198" font-size="10" fill="var(--ink)">ask "at t2": validFrom ≤ t2 &lt; validTo → v2 (reproducible history)</text>
</svg>
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


# ══════════════════════════════════════════════════════════════════════
# L35 · dataset run 与 run item / Dataset runs & run items
# ══════════════════════════════════════════════════════════════════════
_ZH35 = []
_EN35 = []

_ZH35.append(r"""
<p class="lead">
上一课造好了「考卷」（数据集）。这一课讲怎么「<strong>考一场试</strong>」——一次 <strong>dataset run（数据集运行）</strong>就是拿整套题把应用从头到尾考一遍。重点有两个：每道题考一次会产生<strong>一条真实 trace</strong>，而 <strong>dataset run item</strong> 正是把「哪场考试 × 哪道题 → 哪份答卷（trace）」三者钉在一起的那条记录；以及，这些 run item 会被<strong>镜像到 ClickHouse</strong>，连同题面一起<strong>快照</strong>下来，好让「按这场考试汇总所有题的分数」又快又可复现。
理解了 run 与 run item，你就接上了第 30 课那条 <code>dataset-run-item-upsert</code> 评估触发器——<strong>跑一场实验，分数会自动评出来</strong>。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  数据集是<strong>试卷</strong>，一次 run 就是<strong>一场考试</strong>：用某个特定的模型 / prompt 配置，把卷子上每道题都答一遍。每道题答完，都留下一份完整的<strong>答卷</strong>（一条 trace，记着完整的输入输出与每一步）。
  <strong>run item</strong> 就像「<strong>答题卡存根</strong>」：它不存答案本身，只记一个三元对应——「<strong>这是第 3 场考试、第 7 道题、对应第 920 号答卷</strong>」。等阅卷老师（第 29–32 课的评分）给每份答卷打了分，把<strong>同一场考试所有题的分一汇总</strong>，就得到这场考试的<strong>总评</strong>（这次 run 平均分 0.82）。于是「换个模型再考一场，总评涨了还是跌了」一目了然——这正是下一课「实验对比」的基础。
</div>
""")

# (L35 sections below)

_ZH35.append(r"""
<h2>三元链接：哪场考试 × 哪道题 → 哪份答卷</h2>
<p><strong>DatasetRuns</strong> 很简单：一场考试有 name、description、metadata，归属某个 dataset；同一数据集下 run 名唯一（<code>[datasetId, projectId, name]</code>）。真正的关键是 <strong>DatasetRunItems</strong>：它把 <code>datasetRunId</code> + <code>datasetItemId</code> 连到一个 <code>traceId</code>（外加可选 <code>observationId</code>）。换句话说，<strong>每一对（run × item）都对应一条真实 trace</strong>——run item 就是这个三元关系的载体。</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="dataset run 模型：一个数据集的多道题在一次 run 中各被执行一次，每次执行产生一条 trace；DatasetRunItem 把 datasetRunId 加 datasetItemId 连到 traceId，形成 run×item→trace 的三元链接；多次 run 用不同配置考同一套题">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一次 run = 拿整套题考一遍，每题留一条 trace</text>
  <rect x="20" y="46" width="120" height="150" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="80" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">数据集</text><rect x="34" y="74" width="92" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="91" text-anchor="middle" font-size="7" fill="var(--ink)">item 1</text><rect x="34" y="106" width="92" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="123" text-anchor="middle" font-size="7" fill="var(--ink)">item 2</text><rect x="34" y="138" width="92" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="155" text-anchor="middle" font-size="7" fill="var(--ink)">item 3</text><text x="80" y="184" text-anchor="middle" font-size="6.6" fill="var(--muted)">考卷（第34课）</text>
  <rect x="300" y="40" width="150" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="375" y="59" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">run「gpt-4o 场」</text>
  <rect x="290" y="80" width="170" height="116" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="375" y="98" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">run items（答题卡存根）</text><text x="375" y="118" text-anchor="middle" font-size="6.6" fill="var(--muted)">run×item1 → trace A</text><text x="375" y="136" text-anchor="middle" font-size="6.6" fill="var(--muted)">run×item2 → trace B</text><text x="375" y="154" text-anchor="middle" font-size="6.6" fill="var(--muted)">run×item3 → trace C</text><text x="375" y="178" text-anchor="middle" font-size="6.4" fill="var(--faint)">datasetRunId+datasetItemId→traceId</text>
  <rect x="560" y="74" width="140" height="40" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="630" y="91" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">trace A/B/C</text><text x="630" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">每题一条真实 trace</text>
  <rect x="560" y="128" width="140" height="36" rx="8" fill="var(--bg)" stroke="var(--blue)" stroke-dasharray="3 2"/><text x="630" y="145" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">run「claude 场」…</text><text x="630" y="158" text-anchor="middle" font-size="6.2" fill="var(--muted)">同套题换配置再考</text>
  <line x1="140" y1="120" x2="288" y2="120" stroke="var(--accent)" stroke-width="1.4"/><polygon points="288,120 279,116 279,124" fill="var(--accent)"/><text x="214" y="113" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">执行每道题</text>
  <line x1="460" y1="130" x2="558" y2="100" stroke="var(--teal)" stroke-width="1.4"/><polygon points="558,100 549,99 552,107" fill="var(--teal)"/>
  <text x="360" y="222" text-anchor="middle" font-size="8" fill="var(--faint)">run item 不存答案本身，只存「run×item→trace」的三元对应——答案在它指向的那条 trace 里</text>
</svg>
<div class="figcap"><b>run item = 三元链接的载体</b>：<code>schema.prisma:719</code> DatasetRuns（[datasetId, projectId, name] 唯一），<code>:739</code> DatasetRunItems 把 <code>datasetRunId</code>+<code>datasetItemId</code> 连到 <code>traceId</code>(+observationId)。一次 run 把整套题各执行一次，每次产出一条真实 trace；run item 记下「哪场×哪题→哪条 trace」。</div>
</div>

<div class="layers">
  <div class="layer l-part"><div class="lh"><span class="badge">一场考试</span><span class="name">DatasetRuns</span></div><div class="ld">一次 run 代表「用某套固定配置（模型/prompt/版本）把整个数据集跑一遍」。它有 name（如「gpt-4o-2025-baseline」）、description、metadata，归属一个 dataset。同一数据集下 run 名唯一，方便你按名字回溯每次实验。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">答题卡存根</span><span class="name">DatasetRunItems</span></div><div class="ld">连接器：<code>datasetRunId</code>（哪场）+ <code>datasetItemId</code>（哪题）→ <code>traceId</code>（哪份答卷）。它本身不存输入输出——那些都在它指向的 trace 里。它只负责把「实验 / 题目 / 执行记录」三者牢牢绑定，让你能从一场 run 顺藤摸到每道题的完整执行细节。</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">复用一切</span><span class="name">trace 就是普通 trace</span></div><div class="ld">妙在 run 产生的 trace 和生产 trace<strong>毫无二致</strong>——同样的观测树（第 13、25 课）、同样能挂 score（第 28 课）、同样走摄取链路（第 12 课）。实验不是另一套系统，而是「用数据集喂出来的一批普通 trace」，前 5 部分的能力全部复用。</div></div>
</div>
""")

# (L35 sec2 CH mirror below)

_ZH35.append(r"""
<h2>镜像到 ClickHouse：连题面一起快照下来</h2>
<p>run item 在 Postgres 有一份（关系真相），但要算「这场考试平均分多少、和上一场比涨跌如何」，得在<strong>海量 run item × 海量 score</strong> 上做聚合——这是 OLAP 活，归 ClickHouse（第 17、22 课）。所以 run item 被<strong>镜像</strong>到 CH 的 <code>dataset_run_items_rmt</code> 表。最值得玩味的是：这张表不只存 id，还<strong>反范式地把 run 字段和题面快照</strong>了进来。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="run item 镜像到 ClickHouse：PG 里的 DatasetRunItem 被同步到 CH dataset_run_items_rmt 表，该表反范式地内联了 run 名/描述等不可变字段，以及数据项的 input/expectedOutput 快照；用 ReplacingMergeTree 去重；按 project/dataset/run 排序便于聚合">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">镜像 + 反范式快照：聚合快、且记住当时题面</text>
  <rect x="30" y="50" width="170" height="120" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="115" y="70" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">Postgres（真相）</text><text x="115" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">DatasetRunItem</text><text x="115" y="106" text-anchor="middle" font-size="6.6" fill="var(--muted)">runId + itemId + traceId</text><text x="115" y="124" text-anchor="middle" font-size="6.6" fill="var(--faint)">只存关系，瘦</text><text x="115" y="150" text-anchor="middle" font-size="6.4" fill="var(--muted)">事务性强一致</text>
  <rect x="290" y="36" width="200" height="148" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="390" y="56" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">ClickHouse: dataset_run_items_rmt</text><text x="390" y="76" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">id/run/item/trace_id …</text><rect x="304" y="86" width="172" height="40" rx="6" fill="var(--bg)" stroke="var(--accent)"/><text x="390" y="102" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">反范式：run name/desc 内联</text><text x="390" y="118" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">+ item input/expectedOutput 快照</text><text x="390" y="142" text-anchor="middle" font-size="6.6" fill="var(--muted)">ReplacingMergeTree(event_ts,is_deleted)</text><text x="390" y="158" text-anchor="middle" font-size="6.4" fill="var(--muted)">ORDER BY project/dataset/run/id</text><text x="390" y="174" text-anchor="middle" font-size="6.4" fill="var(--faint)">为聚合而生，胖</text>
  <rect x="560" y="64" width="140" height="56" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="630" y="84" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">按 run 聚合分数</text><text x="630" y="100" text-anchor="middle" font-size="6.4" fill="var(--muted)">JOIN scores → avg</text><text x="630" y="113" text-anchor="middle" font-size="6.4" fill="var(--muted)">这场均分 0.82</text>
  <line x1="200" y1="110" x2="288" y2="110" stroke="var(--accent)" stroke-width="1.5"/><polygon points="288,110 279,106 279,114" fill="var(--accent)"/><text x="244" y="103" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">镜像</text>
  <line x1="490" y1="110" x2="558" y2="92" stroke="var(--teal)" stroke-width="1.5"/><polygon points="558,92 549,91 552,99" fill="var(--teal)"/>
  <text x="360" y="204" text-anchor="middle" font-size="8" fill="var(--faint)">快照题面的妙处：即便日后题被改新版（第34课），这条 run item 仍记着「当时考的到底是什么」——可复现再加一道保险</text>
</svg>
<div class="figcap"><b>反范式 = 用空间换聚合速度 + 记忆</b>：CH 表内联了不可变的 run 字段与 <b>item input/expectedOutput 快照</b>（注释原文「denormalized … but snapshots are relevant」）。即使题目日后升新版，这场 run 仍记得当时题面——第 34 课的「可复现」在这里再上一道保险。引擎 ReplacingMergeTree（第 17 课同款）。源码：<code>clickhouse/migrations/clustered/0024_dataset_run_items.up.sql</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/clickhouse/migrations/clustered/0024_dataset_run_items.up.sql</span><span class="ln">CH 镜像表</span></div>
  <pre class="code"><span class="kw">CREATE TABLE</span> dataset_run_items_rmt (
  id String, project_id String, dataset_run_id String,
  dataset_item_id String, dataset_id String, trace_id String, observation_id Nullable(String),
  <span class="cm">-- 反范式：不可变的 run 字段直接内联（省一次 JOIN）</span>
  dataset_run_name String, dataset_run_description Nullable(String), dataset_run_created_at DateTime64(3),
  <span class="cm">-- 快照：题面在「当时」的样子（即便日后改版也记得考的是什么）</span>
  dataset_item_input Nullable(String) CODEC(ZSTD(3)),
  dataset_item_expected_output Nullable(String) CODEC(ZSTD(3)),
  event_ts DateTime64(3), is_deleted UInt8
) <span class="kw">ENGINE</span> = ReplicatedReplacingMergeTree(event_ts, is_deleted)   <span class="cm">-- 同 id 多次写，留最新（第17课）</span>
<span class="kw">ORDER BY</span> (project_id, dataset_id, dataset_run_id, id);   <span class="cm">-- 排序键贴合「按 run 聚合」</span></pre>
</div>

<table class="t">
  <thead><tr><th>维度</th><th>Postgres（DatasetRunItem）</th><th>ClickHouse（dataset_run_items_rmt）</th></tr></thead>
  <tbody>
    <tr><td>角色</td><td>关系真相、事务一致</td><td>聚合副本、为 OLAP 而生</td></tr>
    <tr><td>存什么</td><td>瘦：runId+itemId+traceId 等关系</td><td>胖：再内联 run 名/描述 + 题面快照</td></tr>
    <tr><td>引擎</td><td>行存、强一致</td><td>ReplacingMergeTree(event_ts, is_deleted)</td></tr>
    <tr><td>擅长</td><td>精确读单条、外键约束</td><td>「按 run 分组求平均」扫一遍即得</td></tr>
  </tbody>
</table>
<p>这正是第 22 课「双存储」格局在实验域的复刻：<strong>Postgres 当权威、ClickHouse 当快照</strong>。两边不是竞争而是分工——一处保对、一处保快。</p>
""")

_ZH35.append(r"""
<h2>跑一场实验，分数自动评出：run 级聚合</h2>
<p>run item 指向 trace，trace 上挂着 score（第 28 课）。把这条链走完，就能算出<strong>每场 run 的平均分</strong>——这正是 <code>dataset-run-items.ts</code> 在做的：JOIN scores 表，按 score 名求平均（<code>agg_scores_avg</code>）。而分数是<strong>怎么来的</strong>？回想第 30 课：创建 run item 会发出 <code>dataset-run-item-upsert</code> 事件，自动触发评估器给这条 run 的 trace 打分。于是<strong>跑一场实验，分数会自动评出来</strong>，无需手动。</p>

<svg viewBox="0 0 720 230" role="img" aria-label="跑一场实验的聚合链路：数据集 N 道题，run 逐题跑应用各产出一条 trace，自动评分（L29-32）给每条 trace 挂上 score，再按 run 聚合 JOIN scores 对每个 score 名求平均得到 agg_scores_avg，例如 helpfulness 0.82、toxicity 0.03，交给 L36 做实验对比">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="14" y="52" width="150" height="72" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="89" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">数据集</text>
  <text x="89" y="98" font-size="9.5" text-anchor="middle" fill="var(--muted)">N 道题 item</text>
  <rect x="182" y="52" width="164" height="72" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="264" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">run（一场考试）</text>
  <text x="264" y="96" font-size="9.5" text-anchor="middle" fill="var(--muted)">逐题跑应用</text>
  <text x="264" y="112" font-size="9.5" text-anchor="middle" fill="var(--muted)">→ 每题一条 trace</text>
  <rect x="364" y="52" width="164" height="72" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="446" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">自动评分</text>
  <text x="446" y="96" font-size="9.5" text-anchor="middle" fill="var(--muted)">L29–32 评出 score</text>
  <text x="446" y="112" font-size="9.5" text-anchor="middle" fill="var(--muted)">→ 挂回这条 trace</text>
  <rect x="546" y="52" width="158" height="72" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="625" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">按 run 聚合</text>
  <text x="625" y="96" font-size="9.5" text-anchor="middle" fill="var(--muted)">JOIN scores</text>
  <text x="625" y="112" font-size="9.5" text-anchor="middle" fill="var(--muted)">avg(value) by name</text>
  <line x1="164" y1="88" x2="182" y2="88" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="346" y1="88" x2="364" y2="88" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="528" y1="88" x2="546" y2="88" stroke="var(--teal)" stroke-width="2"></line>
  <rect x="180" y="156" width="320" height="46" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="340" y="176" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">agg_scores_avg</text>
  <text x="340" y="194" font-size="9.5" text-anchor="middle" fill="var(--ink)">[[helpfulness, 0.82], [toxicity, 0.03]]</text>
  <line x1="625" y1="124" x2="440" y2="156" stroke="var(--accent)" stroke-width="1.5"></line>
  <text x="560" y="184" font-size="10" fill="var(--muted)">→ 交给 L36 对比</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>建 run + 逐题执行</h4><p>新建一场 run（<code>createOrFetchDatasetRun</code>），对每道 item 用目标配置跑一次应用，产出一条 trace。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>建 run item（钉住版本）</h4><p>记下 run×item→traceId，并钉住该 item 的 <code>validFrom</code>（第34课）。镜像进 CH，快照题面。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>自动触发评估</h4><p>run item 落库发出 <code>dataset-run-item-upsert</code> 事件 → 第30课 createEvalJobs 给这条 trace 排评估工单。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>评分回流</h4><p>裁判 / 代码 / 人工（第29–32课）评出 score，经摄取链路挂回这条 trace。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>按 run 聚合</h4><p><code>dataset-run-items.ts</code> JOIN scores、按名求平均（<code>agg_scores_avg</code>），得「这场 run 平均分」——交给第36课对比。</p></div></div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/repositories/dataset-run-items.ts</span><span class="ln">按 run 聚合分数</span></div>
  <pre class="code"><span class="cm">// 每场 run 的平均分：JOIN scores、按 score 名求平均 → agg_scores_avg</span>
<span class="kw">type</span> DatasetRunRecord = {
  agg_scores_avg: Array&lt;[string, number]&gt;;   <span class="cm">// 如 [["helpfulness", 0.82], ["toxicity", 0.03]]</span>
  scores: ScoreAggregate; …
};
<span class="cm">// scoresCte：对数值分按 (name, avg_value) 聚合</span>
WITH scores_aggregated AS ( SELECT …, avg(value) AS scores_avg … GROUP BY name )
<span class="cm">// 于是「gpt-4o 场 vs claude 场」可以直接比 agg_scores_avg —— 下一课的实验对比</span></pre>
</div>

<p>至此，Part 6 的前两课拼出了完整的<strong>实验骨架</strong>：数据集（考卷，第34课）→ run（一场考试）→ run item（答题卡存根，把题与答卷钉一起）→ trace（答卷）→ 自动评分（第29–32课）→ 按 run 聚合（这场总评）。下一课只剩最后一步：把多场 run 的总评<strong>并排对比</strong>，挑出最优配置——这就是「实验」。</p>
""")

# (L35 spark+key below)

_ZH35.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么要专门建一个 run item 表，而不是直接给 trace 打个「属于哪场实验」的标签？</strong> 因为这是个<strong>多对多</strong>的关系，而且要支撑高效聚合。一条 trace 概念上属于「某场 run 的某道题」，但「run」「item」「trace」各自都是独立演化的实体（题会改版、run 会重跑、trace 有完整生命周期）。用一张专门的连接表（run item）承载这个三元关系，既让三者解耦、各自独立，又给了你一个干净的聚合入口：要算「这场考了哪些题、平均分多少」，只需扫这张表 JOIN 一下 score，而不用在庞大的 trace 海里捞带特定标签的针。<strong>关系独立建模，是它能被高效查询和聚合的前提。</strong><br><br>
  <strong>为什么 CH 镜像表要反范式地把 run 字段和题面「快照」进去？</strong> 两个理由叠加。其一是<strong>聚合速度</strong>（第 17、22 课的老主题）：把 run name、题面直接内联，算「按 run 分组的平均分」时省掉一次次回表 JOIN——OLAP 就吃这一套。其二更微妙，是<strong>记忆</strong>：题目会改版（第 34 课），但一场三月的实验，理应永远记得它三月考的是<strong>那时</strong>的题面。把 input/expectedOutput 在 run 时<strong>快照</strong>进 run item，等于给「可复现」再上一道保险——即便原题后来面目全非，这场实验的语境也分毫不失。<strong>快照不是冗余，而是把「当时的真相」固化下来。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>run = 一场考试</strong>：<code>DatasetRuns</code> 用某套固定配置把整个数据集跑一遍；同一数据集下 run 名唯一，便于按名回溯每次实验。</li>
    <li><strong>run item = 三元链接的载体</strong>：<code>DatasetRunItems</code> 把 <code>datasetRunId</code>+<code>datasetItemId</code>→<code>traceId</code> 钉在一起，自己不存输入输出——答案在它指向的 trace 里。这让 run/item/trace 三者解耦又可聚合。</li>
    <li><strong>run 的 trace 就是普通 trace</strong>：同样的观测树、同样能挂 score、同样走摄取链路——实验复用前 5 部分的全部能力，不是另起一套系统。</li>
    <li><strong>镜像到 CH 并反范式快照</strong>：<code>dataset_run_items_rmt</code>（ReplacingMergeTree）内联 run 字段 + <strong>快照题面 input/expectedOutput</strong>——既加速「按 run 聚合」，又让实验永远记得当时考的是什么（可复现加保险）。</li>
    <li><strong>跑一场实验分数自动评出</strong>：建 run item 发 <code>dataset-run-item-upsert</code> 事件 → 第30课自动排评估 → 评分回流 → <code>dataset-run-items.ts</code> JOIN scores 按名求平均（<code>agg_scores_avg</code>）得「这场总评」，交给第36课对比。</li>
  </ul>
</div>
""")

_EN35.append(r"""
<p class="lead">
The last lesson built the "exam paper" (the dataset). This lesson is about how to "<strong>sit an exam</strong>"—a <strong>dataset run</strong> takes the whole set and quizzes the app end to end. Two focuses: each question, run once, produces <strong>a real trace</strong>, and a <strong>dataset run item</strong> is the record that pins "which exam × which question → which answer sheet (trace)" together; and these run items are <strong>mirrored to ClickHouse</strong>, <strong>snapshotting</strong> the question text along with them, so that "aggregate all questions' scores for this exam" is both fast and reproducible.
Once you grasp runs and run items, you connect to Lesson 30's <code>dataset-run-item-upsert</code> eval trigger—<strong>run an experiment and the scores get computed automatically</strong>.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  A dataset is the <strong>exam paper</strong>; a run is <strong>one sitting of the exam</strong>: with a specific model / prompt config, answer every question on the paper. Each answered question leaves a complete <strong>answer sheet</strong> (a trace recording the full input/output and every step).
  A <strong>run item</strong> is like an "<strong>answer-card stub</strong>": it doesn't store the answer itself, only a three-way correspondence—"<strong>this is exam #3, question #7, matching answer sheet #920</strong>". Once the graders (Lessons 29–32's scoring) score each sheet, <strong>aggregating all questions' scores for the same exam</strong> yields the exam's <strong>overall grade</strong> (this run averaged 0.82). So "swap a model, sit another exam—did the grade rise or fall" is obvious—exactly the basis for the next lesson's "experiment comparison".
</div>
""")

_EN35.append(r"""
<h2>The three-way link: which exam × which question → which answer sheet</h2>
<p><strong>DatasetRuns</strong> is simple: a sitting has a name, description, metadata, belongs to a dataset; run names are unique within a dataset (<code>[datasetId, projectId, name]</code>). The real key is <strong>DatasetRunItems</strong>: it links <code>datasetRunId</code> + <code>datasetItemId</code> to a <code>traceId</code> (plus an optional <code>observationId</code>). In other words, <strong>every (run × item) pair maps to one real trace</strong>—the run item is the carrier of this three-way relation.</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="dataset run model: a dataset's questions are each executed once in a run, each execution producing a trace; a DatasetRunItem links datasetRunId plus datasetItemId to a traceId, forming the run×item→trace three-way link; multiple runs quiz the same set with different configs">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">a run = quiz the whole set once, each question leaving a trace</text>
  <rect x="20" y="46" width="120" height="150" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="80" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">dataset</text><rect x="34" y="74" width="92" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="91" text-anchor="middle" font-size="7" fill="var(--ink)">item 1</text><rect x="34" y="106" width="92" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="123" text-anchor="middle" font-size="7" fill="var(--ink)">item 2</text><rect x="34" y="138" width="92" height="26" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="80" y="155" text-anchor="middle" font-size="7" fill="var(--ink)">item 3</text><text x="80" y="184" text-anchor="middle" font-size="6.6" fill="var(--muted)">exam paper (L34)</text>
  <rect x="300" y="40" width="150" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="375" y="59" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">run "gpt-4o sitting"</text>
  <rect x="290" y="80" width="170" height="116" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="375" y="98" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">run items (answer-card stubs)</text><text x="375" y="118" text-anchor="middle" font-size="6.6" fill="var(--muted)">run×item1 → trace A</text><text x="375" y="136" text-anchor="middle" font-size="6.6" fill="var(--muted)">run×item2 → trace B</text><text x="375" y="154" text-anchor="middle" font-size="6.6" fill="var(--muted)">run×item3 → trace C</text><text x="375" y="178" text-anchor="middle" font-size="6.2" fill="var(--faint)">datasetRunId+datasetItemId→traceId</text>
  <rect x="560" y="74" width="140" height="40" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="630" y="91" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">trace A/B/C</text><text x="630" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">one real trace per question</text>
  <rect x="560" y="128" width="140" height="36" rx="8" fill="var(--bg)" stroke="var(--blue)" stroke-dasharray="3 2"/><text x="630" y="145" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">run "claude sitting"…</text><text x="630" y="158" text-anchor="middle" font-size="6.2" fill="var(--muted)">same set, new config</text>
  <line x1="140" y1="120" x2="288" y2="120" stroke="var(--accent)" stroke-width="1.4"/><polygon points="288,120 279,116 279,124" fill="var(--accent)"/><text x="214" y="113" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">execute each question</text>
  <line x1="460" y1="130" x2="558" y2="100" stroke="var(--teal)" stroke-width="1.4"/><polygon points="558,100 549,99 552,107" fill="var(--teal)"/>
  <text x="360" y="222" text-anchor="middle" font-size="8" fill="var(--faint)">a run item stores no answer—only the "run×item→trace" correspondence; the answer is in the trace it points to</text>
</svg>
<div class="figcap"><b>run item = carrier of the three-way link</b>: <code>schema.prisma:719</code> DatasetRuns (unique [datasetId, projectId, name]), <code>:739</code> DatasetRunItems links <code>datasetRunId</code>+<code>datasetItemId</code> to <code>traceId</code>(+observationId). A run executes the whole set once, each producing a real trace; the run item records "which exam × which question → which trace".</div>
</div>

<div class="layers">
  <div class="layer l-part"><div class="lh"><span class="badge">an exam</span><span class="name">DatasetRuns</span></div><div class="ld">A run means "with a fixed config (model/prompt/version), run the whole dataset once". It has a name (e.g. "gpt-4o-2025-baseline"), description, metadata, belongs to a dataset. Run names are unique per dataset, so you can trace each experiment by name.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">answer-card stub</span><span class="name">DatasetRunItems</span></div><div class="ld">The connector: <code>datasetRunId</code> (which exam) + <code>datasetItemId</code> (which question) → <code>traceId</code> (which sheet). It stores no input/output—those are in the trace it points to. It only binds "experiment / question / execution record" together, letting you follow a run down to each question's full execution detail.</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">reuse all</span><span class="name">the trace is an ordinary trace</span></div><div class="ld">The beauty: a run's traces are <strong>indistinguishable</strong> from production traces—same observation tree (Lessons 13, 25), same ability to attach scores (Lesson 28), same ingestion path (Lesson 12). Experiments aren't a separate system but "a batch of ordinary traces fed by a dataset", reusing all of the first five parts.</div></div>
</div>
""")

# (en sec2/3/spark below)

_EN35.append(r"""
<h2>Mirror to ClickHouse: snapshotting the question text too</h2>
<p>A run item lives in Postgres (the relational truth), but to compute "what's this exam's average score, up or down from last time" you must aggregate over <strong>masses of run items × masses of scores</strong>—an OLAP job, belonging to ClickHouse (Lessons 17, 22). So run items are <strong>mirrored</strong> to CH's <code>dataset_run_items_rmt</code> table. The intriguing part: this table stores not just ids but <strong>denormalizes the run fields and snapshots the question text</strong> into it.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="run items mirrored to ClickHouse: a PG DatasetRunItem is synced into the CH dataset_run_items_rmt table, which denormalizes immutable run fields like name/description plus snapshots of the item's input/expectedOutput; deduped via ReplacingMergeTree; ordered by project/dataset/run for aggregation">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">mirror + denormalized snapshot: fast aggregation, and remembers the question</text>
  <rect x="30" y="50" width="170" height="120" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="115" y="70" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">Postgres (truth)</text><text x="115" y="90" text-anchor="middle" font-size="7" fill="var(--muted)">DatasetRunItem</text><text x="115" y="106" text-anchor="middle" font-size="6.6" fill="var(--muted)">runId + itemId + traceId</text><text x="115" y="124" text-anchor="middle" font-size="6.6" fill="var(--faint)">stores only relations, thin</text><text x="115" y="150" text-anchor="middle" font-size="6.4" fill="var(--muted)">transactional, consistent</text>
  <rect x="290" y="36" width="200" height="148" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="390" y="56" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">CH: dataset_run_items_rmt</text><text x="390" y="76" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">id/run/item/trace_id …</text><rect x="304" y="86" width="172" height="40" rx="6" fill="var(--bg)" stroke="var(--accent)"/><text x="390" y="102" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">denormalized: run name/desc inlined</text><text x="390" y="118" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">+ item input/expectedOutput snapshot</text><text x="390" y="142" text-anchor="middle" font-size="6.4" fill="var(--muted)">ReplacingMergeTree(event_ts,is_deleted)</text><text x="390" y="158" text-anchor="middle" font-size="6.2" fill="var(--muted)">ORDER BY project/dataset/run/id</text><text x="390" y="174" text-anchor="middle" font-size="6.4" fill="var(--faint)">built for aggregation, fat</text>
  <rect x="560" y="64" width="140" height="56" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="630" y="84" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">aggregate by run</text><text x="630" y="100" text-anchor="middle" font-size="6.4" fill="var(--muted)">JOIN scores → avg</text><text x="630" y="113" text-anchor="middle" font-size="6.4" fill="var(--muted)">this run averaged 0.82</text>
  <line x1="200" y1="110" x2="288" y2="110" stroke="var(--accent)" stroke-width="1.5"/><polygon points="288,110 279,106 279,114" fill="var(--accent)"/><text x="244" y="103" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">mirror</text>
  <line x1="490" y1="110" x2="558" y2="92" stroke="var(--teal)" stroke-width="1.5"/><polygon points="558,92 549,91 552,99" fill="var(--teal)"/>
  <text x="360" y="204" text-anchor="middle" font-size="8" fill="var(--faint)">snapshot's payoff: even if the question is later versioned up (L34), this run item still remembers "what was actually tested then"—reproducibility, doubly insured</text>
</svg>
<div class="figcap"><b>denormalize = trade space for aggregation speed + memory</b>: the CH table inlines immutable run fields and <b>snapshots item input/expectedOutput</b> (the source comment: "denormalized … but snapshots are relevant"). Even if the question is later versioned up, this run still remembers the question text then—Lesson 34's reproducibility, doubly insured. Engine ReplacingMergeTree (same as Lesson 17). Source: <code>clickhouse/migrations/clustered/0024_dataset_run_items.up.sql</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/clickhouse/migrations/clustered/0024_dataset_run_items.up.sql</span><span class="ln">CH mirror table</span></div>
  <pre class="code"><span class="kw">CREATE TABLE</span> dataset_run_items_rmt (
  id String, project_id String, dataset_run_id String,
  dataset_item_id String, dataset_id String, trace_id String, observation_id Nullable(String),
  <span class="cm">-- denormalized: immutable run fields inlined (saves a JOIN)</span>
  dataset_run_name String, dataset_run_description Nullable(String), dataset_run_created_at DateTime64(3),
  <span class="cm">-- snapshot: the question text "as of then" (remembers what was tested even after a version bump)</span>
  dataset_item_input Nullable(String) CODEC(ZSTD(3)),
  dataset_item_expected_output Nullable(String) CODEC(ZSTD(3)),
  event_ts DateTime64(3), is_deleted UInt8
) <span class="kw">ENGINE</span> = ReplicatedReplacingMergeTree(event_ts, is_deleted)   <span class="cm">-- many writes per id, keep latest (L17)</span>
<span class="kw">ORDER BY</span> (project_id, dataset_id, dataset_run_id, id);   <span class="cm">-- sort key fits "aggregate by run"</span></pre>
</div>

<table class="t">
  <thead><tr><th>dimension</th><th>Postgres (DatasetRunItem)</th><th>ClickHouse (dataset_run_items_rmt)</th></tr></thead>
  <tbody>
    <tr><td>role</td><td>relational truth, transactional</td><td>aggregation copy, built for OLAP</td></tr>
    <tr><td>stores</td><td>thin: runId+itemId+traceId relations</td><td>fat: also inlines run name/desc + question snapshot</td></tr>
    <tr><td>engine</td><td>row store, strongly consistent</td><td>ReplacingMergeTree(event_ts, is_deleted)</td></tr>
    <tr><td>good at</td><td>exact single-row reads, FK constraints</td><td>"group by run, average" in one scan</td></tr>
  </tbody>
</table>
<p>This is Lesson 22's "dual-store" pattern replayed in the experiment domain: <strong>Postgres as the authority, ClickHouse as the snapshot</strong>. The two don't compete but divide labor—one keeps it correct, one keeps it fast.</p>
""")

_EN35.append(r"""
<h2>Run an experiment, scores compute themselves: run-level aggregation</h2>
<p>A run item points to a trace, the trace carries scores (Lesson 28). Walk that chain and you can compute <strong>each run's average score</strong>—exactly what <code>dataset-run-items.ts</code> does: JOIN the scores table, average by score name (<code>agg_scores_avg</code>). And where do the scores come from? Recall Lesson 30: creating a run item emits a <code>dataset-run-item-upsert</code> event, automatically triggering evaluators to score this run's traces. So <strong>run an experiment and the scores compute themselves</strong>, no manual work.</p>

<svg viewBox="0 0 720 230" role="img" aria-label="the experiment aggregation chain: a dataset of N questions, a run executes the app per item producing one trace each, auto-scoring (L29-32) attaches a score to each trace, then per-run aggregation JOINs scores and averages by name into agg_scores_avg, e.g. helpfulness 0.82 and toxicity 0.03, handed to L36 for experiment comparison">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <rect x="14" y="52" width="150" height="72" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="89" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">dataset</text>
  <text x="89" y="98" font-size="9.5" text-anchor="middle" fill="var(--muted)">N items</text>
  <rect x="182" y="52" width="164" height="72" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="264" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">run (one exam)</text>
  <text x="264" y="96" font-size="9.5" text-anchor="middle" fill="var(--muted)">app per item</text>
  <text x="264" y="112" font-size="9.5" text-anchor="middle" fill="var(--muted)">→ one trace each</text>
  <rect x="364" y="52" width="164" height="72" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="446" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">auto-scoring</text>
  <text x="446" y="96" font-size="9.5" text-anchor="middle" fill="var(--muted)">L29–32 → score</text>
  <text x="446" y="112" font-size="9.5" text-anchor="middle" fill="var(--muted)">→ back onto trace</text>
  <rect x="546" y="52" width="158" height="72" rx="9" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="625" y="76" font-size="11" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">aggregate per run</text>
  <text x="625" y="96" font-size="9.5" text-anchor="middle" fill="var(--muted)">JOIN scores</text>
  <text x="625" y="112" font-size="9.5" text-anchor="middle" fill="var(--muted)">avg(value) by name</text>
  <line x1="164" y1="88" x2="182" y2="88" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="346" y1="88" x2="364" y2="88" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="528" y1="88" x2="546" y2="88" stroke="var(--teal)" stroke-width="2"></line>
  <rect x="180" y="156" width="320" height="46" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="340" y="176" font-size="10" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">agg_scores_avg</text>
  <text x="340" y="194" font-size="9.5" text-anchor="middle" fill="var(--ink)">[[helpfulness, 0.82], [toxicity, 0.03]]</text>
  <line x1="625" y1="124" x2="440" y2="156" stroke="var(--accent)" stroke-width="1.5"></line>
  <text x="556" y="184" font-size="10" fill="var(--muted)">→ to L36 compare</text>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>create run + execute per question</h4><p>Create a run (<code>createOrFetchDatasetRun</code>), run the app once per item with the target config, producing a trace.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>create run item (pin the version)</h4><p>Record run×item→traceId, pinning the item's <code>validFrom</code> (L34). Mirror into CH, snapshot the question.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>auto-trigger evaluation</h4><p>Persisting the run item emits a <code>dataset-run-item-upsert</code> event → Lesson 30's createEvalJobs queues eval for this trace.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>scores flow back</h4><p>Judge / code / human (Lessons 29–32) produce scores, attached back to this trace via the ingestion path.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>aggregate by run</h4><p><code>dataset-run-items.ts</code> JOINs scores, averages by name (<code>agg_scores_avg</code>), yielding "this run's average"—handed to Lesson 36 for comparison.</p></div></div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/repositories/dataset-run-items.ts</span><span class="ln">aggregate scores by run</span></div>
  <pre class="code"><span class="cm">// each run's average: JOIN scores, average by score name → agg_scores_avg</span>
<span class="kw">type</span> DatasetRunRecord = {
  agg_scores_avg: Array&lt;[string, number]&gt;;   <span class="cm">// e.g. [["helpfulness", 0.82], ["toxicity", 0.03]]</span>
  scores: ScoreAggregate; …
};
<span class="cm">// scoresCte: aggregate numeric scores as (name, avg_value)</span>
WITH scores_aggregated AS ( SELECT …, avg(value) AS scores_avg … GROUP BY name )
<span class="cm">// so "gpt-4o sitting vs claude sitting" compares directly on agg_scores_avg — next lesson's comparison</span></pre>
</div>

<p>With that, Part 6's first two lessons assemble the full <strong>experiment skeleton</strong>: dataset (exam paper, L34) → run (a sitting) → run item (answer-card stub, pinning question to sheet) → trace (the sheet) → auto-scoring (Lessons 29–32) → aggregate by run (the exam's grade). The next lesson is the last step: place multiple runs' grades <strong>side by side</strong> and pick the best config—that's an "experiment".</p>
""")

_EN35.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why build a dedicated run-item table rather than just tag a trace with "which experiment it belongs to"?</strong> Because it's a <strong>many-to-many</strong> relation that must support efficient aggregation. A trace conceptually belongs to "some question of some run", but "run", "item", and "trace" each evolve independently (questions get versioned, runs get re-run, traces have full lifecycles). A dedicated junction table (the run item) carrying this three-way relation both keeps the three decoupled and independent, and gives you a clean aggregation entry: to compute "which questions this exam covered, what the average is", just scan this table and JOIN scores—rather than fishing for tagged needles in a vast trace ocean. <strong>Modeling the relation independently is the precondition for efficient query and aggregation.</strong><br><br>
  <strong>Why does the CH mirror table denormalize and "snapshot" the run fields and question text?</strong> Two compounding reasons. One is <strong>aggregation speed</strong> (Lessons 17, 22's old theme): inlining run name and question text saves repeated back-to-table JOINs when computing "average grouped by run"—OLAP thrives on this. The other is subtler, <strong>memory</strong>: questions get versioned (Lesson 34), but a March experiment ought to forever remember the question text it tested <strong>then</strong>. Snapshotting input/expectedOutput into the run item at run time doubly insures "reproducibility"—even if the original question later changes beyond recognition, this experiment's context is preserved intact. <strong>The snapshot isn't redundancy but freezing "the truth as of then".</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A run = an exam sitting</strong>: <code>DatasetRuns</code> runs the whole dataset with a fixed config; run names are unique per dataset, so each experiment is traceable by name.</li>
    <li><strong>A run item = carrier of the three-way link</strong>: <code>DatasetRunItems</code> pins <code>datasetRunId</code>+<code>datasetItemId</code>→<code>traceId</code>, storing no input/output—the answer is in the trace it points to. This keeps run/item/trace decoupled yet aggregatable.</li>
    <li><strong>A run's trace is an ordinary trace</strong>: same observation tree, same scores, same ingestion path—experiments reuse all of the first five parts, not a separate system.</li>
    <li><strong>Mirror to CH with a denormalized snapshot</strong>: <code>dataset_run_items_rmt</code> (ReplacingMergeTree) inlines run fields + <strong>snapshots question input/expectedOutput</strong>—both speeding "aggregate by run" and making an experiment forever remember what it tested (reproducibility, insured).</li>
    <li><strong>Run an experiment, scores auto-compute</strong>: creating a run item emits <code>dataset-run-item-upsert</code> → Lesson 30 auto-queues eval → scores flow back → <code>dataset-run-items.ts</code> JOINs scores, averages by name (<code>agg_scores_avg</code>) into "this run's grade", handed to Lesson 36 for comparison.</li>
  </ul>
</div>
""")

LESSON_35 = {"zh": "\n".join(_ZH35), "en": "\n".join(_EN35)}


# ══════════════════════════════════════════════════════════════════════
# L36 · 实验与对比 / Experiments & comparison
# ══════════════════════════════════════════════════════════════════════
_ZH36 = []
_EN36 = []

_ZH36.append(r"""
<p class="lead">
前两课造好了「考卷」（数据集）和「考试机制」（run）。这一课讲怎么用它们<strong>做决策</strong>——这就是<strong>实验（experiment）</strong>。一次实验，就是拿一个具体的 <strong>prompt + 模型</strong>配置，在整个数据集上自动跑一遍（产出一次 run），再把<strong>多次 run 并排对比</strong>，挑出最优的那套。它把「改 prompt、换模型到底好不好」从<strong>拍脑袋</strong>变成<strong>有数据</strong>——这是 LLM 工程里最接近「科学方法」的一环。
重点有三：实验是怎么<strong>服务端自动跑</strong>的（把题目填进 prompt 变量、调 LLM、产 trace）；评分怎么<strong>自动接上</strong>（复用第 30、35 课）；以及对比怎么用 <strong>baseline + 增量</strong>让你一眼看出涨跌。这一课也为 Part 7 的 prompt 管理埋下伏笔——实验里被考的那个 prompt，正是下一课的主角。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  实验像一场严谨的 <strong>A/B 对照试验</strong>。同一套题（数据集），A 组用「gpt-4o + prompt v1」、B 组用「claude + prompt v2」，各自<strong>认真考一场</strong>。
  你不用亲自监考：系统自动<strong>替你出题</strong>（把每道题的输入填进 prompt 的变量空格）、自动<strong>阅卷</strong>（第 29–32 课的评分）、自动<strong>算总评</strong>（第 35 课按 run 聚合）。最后把两组成绩单<strong>并排摊开</strong>，还允许你钦定一组当<strong>基准（baseline）</strong>，其余组就显示「比基准高了多少 / 低了多少」。
  于是那个让无数人纠结的问题——「我这个 prompt 改动，到底是变好了还是变坏了？」——不再靠感觉，而是<strong>一张并排的、带增量的成绩单</strong>说了算。
</div>
""")

# (L36 sections below)

_ZH36.append(r"""
<h2>服务端自动跑：把题填进 prompt 变量，逐题调 LLM</h2>
<p>Langfuse 的实验可以<strong>完全在服务端跑</strong>：你只需选一个数据集、一个带变量的 prompt、一个模型，剩下的交给 worker。<code>createExperimentJobClickhouse</code>（由 <code>ExperimentCreate</code> 队列驱动）会逐道题做三步：把这道题的 <code>input</code> 填进 prompt 的变量空格、用你选的 provider/model 调一次 LLM、把结果写成一条 trace + run item。</p>

<div class="fig">
<svg viewBox="0 0 720 235" role="img" aria-label="服务端 prompt 实验：对数据集每道题，replaceVariablesInPrompt 把 item.input 填进 prompt 的变量占位符，用选定 provider/model 调 LLM，产出一条 trace（环境标 PromptExperiments、链接 prompt、钉住 item 版本）和一个 run item">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">逐题：填变量 → 调 LLM → 产 trace + run item</text>
  <rect x="30" y="44" width="150" height="56" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="105" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">prompt（带变量）</text><text x="105" y="80" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">"回答 {{question}}"</text><text x="105" y="93" text-anchor="middle" font-size="6.4" fill="var(--muted)">第37课的 prompt</text>
  <rect x="30" y="116" width="150" height="50" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="105" y="135" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">dataset item.input</text><text x="105" y="151" text-anchor="middle" font-size="6.6" fill="var(--muted)">{question: "退款政策?"}</text>
  <rect x="225" y="80" width="150" height="56" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="300" y="100" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">replaceVariablesInPrompt</text><text x="300" y="116" text-anchor="middle" font-size="6.6" fill="var(--muted)">填空 → 完整 messages</text><text x="300" y="128" text-anchor="middle" font-size="6.4" fill="var(--faint)">"回答 退款政策?"</text>
  <rect x="420" y="80" width="130" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="485" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">调 LLM</text><text x="485" y="116" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">provider/model</text><text x="485" y="128" text-anchor="middle" font-size="6.4" fill="var(--muted)">被考的配置</text>
  <rect x="588" y="58" width="112" height="44" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="644" y="76" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">trace</text><text x="644" y="91" text-anchor="middle" font-size="6.0" fill="var(--muted)">env=PromptExperiments</text>
  <rect x="588" y="112" width="112" height="44" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="644" y="130" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">run item</text><text x="644" y="145" text-anchor="middle" font-size="6.0" fill="var(--muted)">钉住 item 版本</text>
  <line x1="180" y1="72" x2="223" y2="100" stroke="var(--faint)" stroke-width="1.2"/><line x1="180" y1="141" x2="223" y2="116" stroke="var(--faint)" stroke-width="1.2"/>
  <line x1="375" y1="108" x2="418" y2="108" stroke="var(--teal)" stroke-width="1.5"/><polygon points="418,108 409,104 409,112" fill="var(--teal)"/>
  <line x1="550" y1="100" x2="586" y2="86" stroke="var(--accent)" stroke-width="1.4"/><polygon points="586,86 577,85 580,93" fill="var(--accent)"/><line x1="550" y1="116" x2="586" y2="128" stroke="var(--blue)" stroke-width="1.2"/>
  <text x="360" y="192" text-anchor="middle" font-size="8" fill="var(--faint)">trace 还链接了被考的 prompt（第37课）、metadata 钉住 item 的 validFrom（第34/35课的版本回放）</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">环境标成 PromptExperiments —— 这正是第30课「langfuse- 前缀防无限循环」要识别的内部环境之一</text>
</svg>
<div class="figcap"><b>实验 = 服务端逐题跑 prompt</b>：<code>processLLMCall</code>（由 <code>processItem</code> 委派）调 <code>replaceVariablesInPrompt(prompt, item.input, …)</code> 填变量，用 <code>config.provider/model</code> 调 LLM，写出 trace（<code>environment=PromptExperiments</code>，链接 <code>prompt</code>，metadata 含 <code>itemVersion=item.validFrom</code>）。源码：<code>worker/src/features/experiments/experimentServiceClickhouse.ts:154-225,287</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/experiments/experimentServiceClickhouse.ts</span><span class="ln">processLLMCall 核心（processItem 委派）</span></div>
  <pre class="code"><span class="cm">// 1) 把这道题的 input 填进 prompt 的变量空格 → 完整 messages</span>
messages = replaceVariablesInPrompt(
  config.validatedPrompt, datasetItem.input, config.allVariables, config.placeholderNames);

<span class="cm">// 2) 组 trace：标实验环境、链接被考 prompt、钉住 item 版本</span>
traceSinkParams = {
  environment: <span class="st">LangfuseInternalTraceEnvironment.PromptExperiments</span>,
  traceId, prompt: config.prompt,
  experimentContext: { …, itemVersion: convert...(datasetItem.validFrom), itemExpectedOutput } };

<span class="cm">// 3) 用被考的 provider/model 调 LLM（结果写成这条 trace + run item）</span>
modelParams = { provider: config.provider, model: config.model,
  adapter: config.validatedApiKey.adapter, ...config.model_params };</pre>
</div>

<table class="t">
  <thead><tr><th>维度</th><th>服务端实验（本课主线）</th><th>远程 / SDK 实验</th></tr></thead>
  <tbody>
    <tr><td>谁跑应用</td><td>Langfuse worker（用你选的 prompt/模型）</td><td>你自己的代码 / 外部系统</td></tr>
    <tr><td>怎么触发</td><td>UI 点「跑」→ <code>ExperimentCreate</code> 队列</td><td>数据集的 <code>remoteExperimentUrl</code> 回调你的服务</td></tr>
    <tr><td>适合</td><td>纯 prompt/模型对比，零代码</td><td>复杂自定义链路（多步 agent、检索等）</td></tr>
    <tr><td>共同点</td><td colspan="2">都产出 run + run item + trace，都走同一套自动评分与对比——下游完全一致</td></tr>
  </tbody>
</table>
<p>两种模式殊途同归：无论谁来跑应用，最终都落成第 35 课的 run item + trace，享受同一套自动评分（第 30 课）与对比视图。<strong>「怎么产生答卷」可以不同，「怎么评判与对比」完全统一</strong>——又一次「一个下游，多个上游」的解耦。</p>
""")

_ZH36.append(r"""
<h2>对比：选一组当基准，其余看增量</h2>
<p>实验跑完，每条 trace 经第 30、35 课<strong>自动评分并按 run 聚合</strong>，于是每场 run 都有了一张「成绩单」（各 score 名的平均分）。对比的精髓不是看绝对分，而是<strong>并排 + 增量</strong>：你钦定一场 run 当 <strong>baseline（基准）</strong>，其余各场就显示「比基准高/低多少」。Langfuse 的实验对比页（<code>ExperimentComparisonSelector</code> / <code>ExperimentBaselineControls</code> / <code>ExperimentChartsGrid</code>）正是干这个的。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="实验对比：多场 run 并排，选一场为 baseline，其余 run 的每个 score 显示相对 baseline 的增量（绿升红降），让 prompt/模型改动的好坏一眼可判">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">并排成绩单 + 相对基准的增量</text>
  <rect x="40" y="44" width="180" height="150" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="130" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">run A（baseline）</text><text x="130" y="82" text-anchor="middle" font-size="6.8" fill="var(--muted)">gpt-4o + prompt v1</text><line x1="56" y1="92" x2="204" y2="92" stroke="var(--faint)"/><text x="130" y="110" text-anchor="middle" font-size="7.5" fill="var(--ink)">有用性 0.78</text><text x="130" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">毒性通过 0.96</text><text x="130" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">延迟 1.2s</text><text x="130" y="178" text-anchor="middle" font-size="6.6" fill="var(--blue)">★ 基准（其余跟它比）</text>
  <rect x="270" y="44" width="180" height="150" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="360" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">run B</text><text x="360" y="82" text-anchor="middle" font-size="6.8" fill="var(--muted)">claude + prompt v2</text><line x1="286" y1="92" x2="434" y2="92" stroke="var(--faint)"/><text x="360" y="110" text-anchor="middle" font-size="7.5" fill="var(--ink)">有用性 0.85 <tspan fill="var(--teal)">▲+0.07</tspan></text><text x="360" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">毒性通过 0.97 <tspan fill="var(--teal)">▲+0.01</tspan></text><text x="360" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">延迟 2.1s <tspan fill="var(--accent-ink)">▼+0.9</tspan></text><text x="360" y="178" text-anchor="middle" font-size="6.6" fill="var(--muted)">更准但更慢</text>
  <rect x="500" y="44" width="180" height="150" rx="10" fill="var(--bg)" stroke="var(--faint)"/><text x="590" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--muted)">run C</text><text x="590" y="82" text-anchor="middle" font-size="6.8" fill="var(--muted)">gpt-4o + prompt v3</text><line x1="516" y1="92" x2="664" y2="92" stroke="var(--faint)"/><text x="590" y="110" text-anchor="middle" font-size="7.5" fill="var(--ink)">有用性 0.74 <tspan fill="var(--accent-ink)">▼−0.04</tspan></text><text x="590" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">毒性通过 0.96 —</text><text x="590" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">延迟 1.1s <tspan fill="var(--teal)">▲−0.1</tspan></text><text x="590" y="178" text-anchor="middle" font-size="6.6" fill="var(--muted)">这版 prompt 反而退步</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">绝对分难判好坏，增量一目了然：B 用准度换了延迟、C 的 prompt 改动是负优化——决策有据可依</text>
</svg>
<div class="figcap"><b>对比靠「基准 + 增量」</b>：钦定一场 run 为 baseline，其余每个 score 显示相对增量（升/降）。源码：<code>web/src/features/experiments/components/</code> 的 <code>ExperimentBaselineControls</code>、<code>ExperimentComparisonSelector</code>、<code>ExperimentChartsGrid</code>。</div>
</div>

<div class="cols">
  <div class="col"><h4>选 baseline</h4><p><code>ExperimentBaselineControls</code> 让你钦定一场 run 当参照系——通常是「线上现役」那套配置，于是所有候选都和「现状」比，回答「换了会更好吗」。</p></div>
  <div class="col"><h4>挑要比的 run</h4><p><code>ExperimentComparisonSelector</code> 选若干场 run 并排。同一套题、不同配置，公平可比（因为第 34 课的版本化保证了考的是同一批题）。</p></div>
  <div class="col"><h4>看多维增量</h4><p><code>ExperimentChartsGrid</code> 把每个 score 维度画成对比图。好坏往往是<strong>多维权衡</strong>（更准但更慢更贵），增量视图让取舍一目了然。</p></div>
</div>
""")

# (L36 sec3 loop below)

_ZH36.append(r"""
<h2>闭环：一套科学的「改前先验证」方法</h2>
<p>把 Part 6 三课串起来，你得到的是一台<strong>持续改进的飞轮</strong>。它让「优化 LLM 应用」这件本来很玄的事，落地成一个可重复、有数据支撑的工程流程：</p>

<svg viewBox="0 0 720 230" role="img" aria-label="持续改进飞轮五步循环：① 攒数据集（L34 把生产里答砸的 case 提拔成测试题）→ ② 跑实验（本课服务端 run）→ ③ 自动评分（L30/35 聚合成绩单）→ ④ 对比决策（baseline 加增量，更好才上线）→ ⑤ 上线遇新难 case 回流第 1 步，飞轮越转应用越稳">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <text x="360" y="112" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">持续改进飞轮</text>
  <text x="360" y="132" font-size="9.5" text-anchor="middle" fill="var(--muted)">把「能打分」升级成「能用分做决策」</text>
  <rect x="282" y="31" width="156" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="50" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">① 攒数据集</text>
  <text x="360" y="67" font-size="9" text-anchor="middle" fill="var(--muted)">L34 提拔生产 case</text>
  <rect x="478" y="75" width="156" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="556" y="94" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">② 跑实验</text>
  <text x="556" y="111" font-size="9" text-anchor="middle" fill="var(--muted)">本课 · 服务端 run</text>
  <rect x="396" y="173" width="156" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="474" y="192" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">③ 自动评分</text>
  <text x="474" y="209" font-size="9" text-anchor="middle" fill="var(--muted)">L30/35 聚合成绩单</text>
  <rect x="168" y="173" width="156" height="46" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="246" y="192" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">④ 对比决策</text>
  <text x="246" y="209" font-size="9" text-anchor="middle" fill="var(--muted)">baseline + 增量</text>
  <rect x="86" y="75" width="156" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="164" y="94" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">⑤ 遇新难 case</text>
  <text x="164" y="111" font-size="9" text-anchor="middle" fill="var(--muted)">回流第 1 步</text>
  <line x1="438" y1="58" x2="478" y2="86" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="520" y1="121" x2="498" y2="173" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="396" y1="196" x2="324" y2="196" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="200" y1="173" x2="176" y2="121" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="224" y1="86" x2="282" y2="60" stroke="var(--accent)" stroke-width="2"></line>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>攒数据集</h4><p>把真实生产里答砸的 case 提拔成测试题（第34课），让考卷紧贴真实分布。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>跑实验</h4><p>对一个候选 prompt/模型配置，服务端在整套题上跑一场 run（本课），产出一批 trace。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>自动评分</h4><p>第30、35课自动给每条 trace 评分、按 run 聚合出这场的成绩单。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>对比决策</h4><p>和 baseline（现役配置）并排看增量：真的更好就上线，退步就否决——不靠感觉。</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>回到第1步</h4><p>上线后又会遇到新的难 case，再提拔成题……飞轮转起来，应用越改越稳。</p></div></div>
</div>

<p>这就是 Part 6 的全部价值：它把第 5 部分「能给质量打分」升级成「<strong>能用分数做决策</strong>」。而被实验反复考的那个核心变量——<strong>prompt</strong>——正是下一部分（Part 7）的主角：它怎么版本化、怎么被高速服务、怎么在 Playground 里交互调试。评估告诉你「现在多好」，实验告诉你「改了会不会更好」，而 prompt 管理则给了你「<strong>安全地改</strong>」的底气。</p>
""")

_ZH36.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么 Langfuse 要在服务端帮你跑实验，而不是只让你在本地跑完把结果传上来？</strong> 两种都支持（数据集上的 <code>remoteExperimentUrl</code> 就是给本地/外部跑的），但服务端跑有独特价值：<strong>零代码、强一致</strong>。产品经理或非工程师也能在 UI 上选个数据集、改个 prompt、点「跑」，不必写一行脚本；而且服务端跑能<strong>统一</strong>变量替换、版本钉定、评分调度、环境标记——把「实验该怎么做对」固化进平台，而不是指望每个人的本地脚本都写得严谨。代价是平台要承担 LLM 调用的成本与并发，所以它走 <code>ExperimentCreate</code> 队列、复用第 30 课那套调度韧性。<br><br>
  <strong>为什么对比要用「baseline + 增量」，而不是直接看绝对分？</strong> 因为<strong>绝对分几乎没有意义，相对变化才有</strong>。「有用性 0.78」是好是坏？没有参照根本说不清。但「比现役配置高了 0.07」就是一个能据以决策的事实。更重要的是，质量往往是<strong>多维权衡</strong>：B 配置更准但更慢更贵。把每个维度的增量并排摊开，决策者才能做出「这点准度提升值不值这点延迟代价」的<strong>清醒取舍</strong>——而不是被单一指标牵着走。这也呼应第 33 课监控「只在变化时告警」：<strong>有信息量的永远是「变化」，不是「绝对值」。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>实验 = prompt × 数据集 × 模型，服务端自动跑</strong>：<code>createExperimentJobClickhouse</code> 逐题用 <code>replaceVariablesInPrompt</code> 填变量、调选定 provider/model、产 trace + run item，全程零代码。</li>
    <li><strong>实验 trace 带丰富语境</strong>：环境标 <code>PromptExperiments</code>、链接被考 <code>prompt</code>（第37课）、metadata 钉住 <code>itemVersion=validFrom</code>（第34/35课的版本回放）——可复现、可追溯。</li>
    <li><strong>评分自动接上</strong>：复用第 30 课 <code>dataset-run-item-upsert</code> 触发、第 35 课按 run 聚合，跑完即有成绩单，无需手动。</li>
    <li><strong>对比靠 baseline + 增量</strong>：<code>ExperimentBaselineControls</code> 选基准、<code>ExperimentComparisonSelector</code> 挑 run、<code>ExperimentChartsGrid</code> 画多维增量——绝对分难判，相对变化才能决策。</li>
    <li><strong>Part 6 闭环</strong>：数据集→实验→评分→对比→决策→（新难 case 回流数据集）。把「能打分」升级成「能用分做决策」，下一部分的 prompt 则给你「安全地改」的底气。</li>
  </ul>
</div>
""")

_EN36.append(r"""
<p class="lead">
The last two lessons built the "exam paper" (the dataset) and the "exam mechanism" (the run). This lesson is about using them to <strong>make decisions</strong>—that's an <strong>experiment</strong>. One experiment takes a specific <strong>prompt + model</strong> config, runs it automatically over the whole dataset (producing one run), then places <strong>multiple runs side by side</strong> to pick the best. It turns "is changing this prompt or model actually better" from <strong>gut feeling</strong> into <strong>data</strong>—the closest thing to the "scientific method" in LLM engineering.
Three focuses: how an experiment <strong>runs server-side automatically</strong> (fill the question into the prompt's variables, call the LLM, produce a trace); how scoring <strong>auto-connects</strong> (reusing Lessons 30 and 35); and how comparison uses <strong>baseline + deltas</strong> so you see gains/losses at a glance. This lesson also sets up Part 7's prompt management—the prompt being tested in an experiment is the next lesson's protagonist.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  An experiment is like a rigorous <strong>A/B controlled trial</strong>. The same questions (dataset): group A uses "gpt-4o + prompt v1", group B uses "claude + prompt v2", each <strong>sits the exam properly</strong>.
  You needn't proctor yourself: the system automatically <strong>sets the questions</strong> (fills each question's input into the prompt's variable blanks), automatically <strong>grades</strong> (Lessons 29–32's scoring), automatically <strong>computes the grade</strong> (Lesson 35's aggregate-by-run). Finally it <strong>lays the report cards side by side</strong>, and lets you anoint one group as the <strong>baseline</strong>, so the rest show "how much above/below baseline".
  So the question that vexes everyone—"is my prompt change actually better or worse?"—no longer rests on feeling, but on <strong>a side-by-side report card with deltas</strong>.
</div>
""")

_EN36.append(r"""
<h2>Run server-side automatically: fill the question into prompt variables, call the LLM per item</h2>
<p>Langfuse experiments can run <strong>entirely server-side</strong>: you just pick a dataset, a prompt with variables, and a model—the worker does the rest. <code>createExperimentJobClickhouse</code> (driven by the <code>ExperimentCreate</code> queue) does three steps per question: fill the question's <code>input</code> into the prompt's variable blanks, call the LLM with your chosen provider/model, and write the result as a trace + run item.</p>

<div class="fig">
<svg viewBox="0 0 720 235" role="img" aria-label="Server-side prompt experiment: for each dataset question, replaceVariablesInPrompt fills item.input into the prompt's variable placeholders, calls the LLM with the chosen provider/model, producing a trace (environment tagged PromptExperiments, linked to the prompt, pinning the item version) and a run item">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">per question: fill variables → call LLM → produce trace + run item</text>
  <rect x="30" y="44" width="150" height="56" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="105" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">prompt (with variables)</text><text x="105" y="80" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">"answer {{question}}"</text><text x="105" y="93" text-anchor="middle" font-size="6.4" fill="var(--muted)">Lesson 37's prompt</text>
  <rect x="30" y="116" width="150" height="50" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="105" y="135" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">dataset item.input</text><text x="105" y="151" text-anchor="middle" font-size="6.6" fill="var(--muted)">{question: "refund policy?"}</text>
  <rect x="225" y="80" width="150" height="56" rx="9" fill="var(--bg)" stroke="var(--teal)"/><text x="300" y="100" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">replaceVariablesInPrompt</text><text x="300" y="116" text-anchor="middle" font-size="6.6" fill="var(--muted)">fill blanks → full messages</text><text x="300" y="128" text-anchor="middle" font-size="6.4" fill="var(--faint)">"answer refund policy?"</text>
  <rect x="420" y="80" width="130" height="56" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="485" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">call LLM</text><text x="485" y="116" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">provider/model</text><text x="485" y="128" text-anchor="middle" font-size="6.4" fill="var(--muted)">the config under test</text>
  <rect x="588" y="58" width="112" height="44" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="644" y="76" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">trace</text><text x="644" y="91" text-anchor="middle" font-size="5.8" fill="var(--muted)">env=PromptExperiments</text>
  <rect x="588" y="112" width="112" height="44" rx="8" fill="var(--bg)" stroke="var(--blue)"/><text x="644" y="130" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">run item</text><text x="644" y="145" text-anchor="middle" font-size="6.0" fill="var(--muted)">pins item version</text>
  <line x1="180" y1="72" x2="223" y2="100" stroke="var(--faint)" stroke-width="1.2"/><line x1="180" y1="141" x2="223" y2="116" stroke="var(--faint)" stroke-width="1.2"/>
  <line x1="375" y1="108" x2="418" y2="108" stroke="var(--teal)" stroke-width="1.5"/><polygon points="418,108 409,104 409,112" fill="var(--teal)"/>
  <line x1="550" y1="100" x2="586" y2="86" stroke="var(--accent)" stroke-width="1.4"/><polygon points="586,86 577,85 580,93" fill="var(--accent)"/><line x1="550" y1="116" x2="586" y2="128" stroke="var(--blue)" stroke-width="1.2"/>
  <text x="360" y="192" text-anchor="middle" font-size="8" fill="var(--faint)">the trace also links the prompt under test (L37); metadata pins the item's validFrom (L34/35 version replay)</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">environment tagged PromptExperiments — one of the internal envs Lesson 30's "langfuse- prefix loop guard" recognizes</text>
</svg>
<div class="figcap"><b>experiment = run a prompt server-side per question</b>: <code>processLLMCall</code> (delegated by <code>processItem</code>) calls <code>replaceVariablesInPrompt(prompt, item.input, …)</code> to fill variables, calls the LLM with <code>config.provider/model</code>, writes a trace (<code>environment=PromptExperiments</code>, linking <code>prompt</code>, metadata with <code>itemVersion=item.validFrom</code>). Source: <code>worker/src/features/experiments/experimentServiceClickhouse.ts:154-225,287</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">worker/src/features/experiments/experimentServiceClickhouse.ts</span><span class="ln">processLLMCall core (processItem delegates)</span></div>
  <pre class="code"><span class="cm">// 1) fill this question's input into the prompt's variable blanks → full messages</span>
messages = replaceVariablesInPrompt(
  config.validatedPrompt, datasetItem.input, config.allVariables, config.placeholderNames);

<span class="cm">// 2) build the trace: tag experiment env, link the prompt under test, pin item version</span>
traceSinkParams = {
  environment: <span class="st">LangfuseInternalTraceEnvironment.PromptExperiments</span>,
  traceId, prompt: config.prompt,
  experimentContext: { …, itemVersion: convert...(datasetItem.validFrom), itemExpectedOutput } };

<span class="cm">// 3) call the LLM with the provider/model under test (result becomes this trace + run item)</span>
modelParams = { provider: config.provider, model: config.model,
  adapter: config.validatedApiKey.adapter, ...config.model_params };</pre>
</div>

<table class="t">
  <thead><tr><th>dimension</th><th>server-side experiment (this lesson)</th><th>remote / SDK experiment</th></tr></thead>
  <tbody>
    <tr><td>who runs the app</td><td>the Langfuse worker (your chosen prompt/model)</td><td>your own code / external system</td></tr>
    <tr><td>how triggered</td><td>click "run" in the UI → <code>ExperimentCreate</code> queue</td><td>the dataset's <code>remoteExperimentUrl</code> calls back your service</td></tr>
    <tr><td>suits</td><td>pure prompt/model comparison, zero-code</td><td>complex custom pipelines (multi-step agents, retrieval, etc.)</td></tr>
    <tr><td>in common</td><td colspan="2">both produce run + run item + trace, both use the same auto-scoring and comparison—downstream is identical</td></tr>
  </tbody>
</table>
<p>Both modes converge: whoever runs the app, the result lands as Lesson 35's run item + trace, enjoying the same auto-scoring (Lesson 30) and comparison views. <strong>"How the answer sheet is produced" can differ; "how it's judged and compared" is fully unified</strong>—another "one downstream, many upstreams" decoupling.</p>
""")

# (en sec2/3/spark below)

_EN36.append(r"""
<h2>Comparison: anoint one as baseline, view the rest as deltas</h2>
<p>Once the experiment runs, each trace is <strong>auto-scored and aggregated by run</strong> via Lessons 30 and 35, so every run has a "report card" (the average of each score name). The essence of comparison isn't absolute scores but <strong>side-by-side + deltas</strong>: you anoint one run as the <strong>baseline</strong>, and the rest show "how much above/below baseline". Langfuse's experiment comparison page (<code>ExperimentComparisonSelector</code> / <code>ExperimentBaselineControls</code> / <code>ExperimentChartsGrid</code>) does exactly this.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="Experiment comparison: multiple runs side by side, one chosen as baseline, the rest showing each score's delta relative to baseline (green up, red down), making the goodness of a prompt/model change judgeable at a glance">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">side-by-side report cards + deltas vs baseline</text>
  <rect x="40" y="44" width="180" height="150" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="130" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">run A (baseline)</text><text x="130" y="82" text-anchor="middle" font-size="6.8" fill="var(--muted)">gpt-4o + prompt v1</text><line x1="56" y1="92" x2="204" y2="92" stroke="var(--faint)"/><text x="130" y="110" text-anchor="middle" font-size="7.5" fill="var(--ink)">helpfulness 0.78</text><text x="130" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">toxicity-pass 0.96</text><text x="130" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">latency 1.2s</text><text x="130" y="178" text-anchor="middle" font-size="6.6" fill="var(--blue)">★ baseline (others compared to it)</text>
  <rect x="270" y="44" width="180" height="150" rx="10" fill="var(--bg)" stroke="var(--teal)"/><text x="360" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--teal)">run B</text><text x="360" y="82" text-anchor="middle" font-size="6.8" fill="var(--muted)">claude + prompt v2</text><line x1="286" y1="92" x2="434" y2="92" stroke="var(--faint)"/><text x="360" y="110" text-anchor="middle" font-size="7.5" fill="var(--ink)">helpfulness 0.85 <tspan fill="var(--teal)">▲+0.07</tspan></text><text x="360" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">tox-pass 0.97 <tspan fill="var(--teal)">▲+0.01</tspan></text><text x="360" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">latency 2.1s <tspan fill="var(--accent-ink)">▼+0.9</tspan></text><text x="360" y="178" text-anchor="middle" font-size="6.6" fill="var(--muted)">more accurate but slower</text>
  <rect x="500" y="44" width="180" height="150" rx="10" fill="var(--bg)" stroke="var(--faint)"/><text x="590" y="64" text-anchor="middle" font-size="9" font-weight="700" fill="var(--muted)">run C</text><text x="590" y="82" text-anchor="middle" font-size="6.8" fill="var(--muted)">gpt-4o + prompt v3</text><line x1="516" y1="92" x2="664" y2="92" stroke="var(--faint)"/><text x="590" y="110" text-anchor="middle" font-size="7.5" fill="var(--ink)">helpfulness 0.74 <tspan fill="var(--accent-ink)">▼−0.04</tspan></text><text x="590" y="130" text-anchor="middle" font-size="7.5" fill="var(--ink)">tox-pass 0.96 —</text><text x="590" y="150" text-anchor="middle" font-size="7.5" fill="var(--ink)">latency 1.1s <tspan fill="var(--teal)">▲−0.1</tspan></text><text x="590" y="178" text-anchor="middle" font-size="6.6" fill="var(--muted)">this prompt regressed</text>
  <text x="360" y="208" text-anchor="middle" font-size="8" fill="var(--faint)">absolute scores are hard to judge; deltas are obvious: B traded latency for accuracy, C's prompt change is a regression—decisions grounded</text>
</svg>
<div class="figcap"><b>Comparison via "baseline + deltas"</b>: anoint one run as baseline, each score shows its relative delta (up/down). Source: <code>web/src/features/experiments/components/</code>'s <code>ExperimentBaselineControls</code>, <code>ExperimentComparisonSelector</code>, <code>ExperimentChartsGrid</code>.</div>
</div>

<div class="cols">
  <div class="col"><h4>pick a baseline</h4><p><code>ExperimentBaselineControls</code> lets you anoint one run as the reference—usually the "production-active" config, so all candidates compare to "the status quo", answering "would changing be better".</p></div>
  <div class="col"><h4>choose runs to compare</h4><p><code>ExperimentComparisonSelector</code> picks several runs side by side. Same questions, different configs, fairly comparable (Lesson 34's versioning guarantees they tested the same questions).</p></div>
  <div class="col"><h4>view multi-dimensional deltas</h4><p><code>ExperimentChartsGrid</code> charts each score dimension as a comparison. Goodness is often a <strong>multi-dimensional trade-off</strong> (more accurate but slower, costlier); the delta view makes the trade-off obvious.</p></div>
</div>
""")

_EN36.append(r"""
<h2>The loop: a scientific "verify before you change" method</h2>
<p>String Part 6's three lessons together and you get a <strong>continuous-improvement flywheel</strong>. It turns "optimizing an LLM app"—usually mystical—into a repeatable, data-backed engineering process:</p>

<svg viewBox="0 0 720 230" role="img" aria-label="the continuous-improvement flywheel, a five-step cycle: 1 build a dataset (L34, promote botched production cases into test questions) → 2 run an experiment (this lesson, server-side run) → 3 auto-score (L30/35 aggregate a scorecard) → 4 compare and decide (baseline plus deltas, ship only if better) → 5 hit new hard cases in production and feed them back to step 1, the flywheel making the app steadier each turn">
  <rect x="0" y="0" width="720" height="230" fill="var(--bg)"></rect>
  <text x="360" y="112" font-size="12" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">continuous-improvement flywheel</text>
  <text x="360" y="132" font-size="9.5" text-anchor="middle" fill="var(--muted)">upgrades "can score" into "can decide with scores"</text>
  <rect x="282" y="31" width="156" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="360" y="50" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">1 build dataset</text>
  <text x="360" y="67" font-size="9" text-anchor="middle" fill="var(--muted)">L34 promote prod cases</text>
  <rect x="478" y="75" width="156" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="556" y="94" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">2 run experiment</text>
  <text x="556" y="111" font-size="9" text-anchor="middle" fill="var(--muted)">this lesson · server run</text>
  <rect x="396" y="173" width="156" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"></rect>
  <text x="474" y="192" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">3 auto-score</text>
  <text x="474" y="209" font-size="9" text-anchor="middle" fill="var(--muted)">L30/35 scorecard</text>
  <rect x="168" y="173" width="156" height="46" rx="9" fill="var(--amber-soft)" stroke="var(--accent)"></rect>
  <text x="246" y="192" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">4 compare + decide</text>
  <text x="246" y="209" font-size="9" text-anchor="middle" fill="var(--muted)">baseline + deltas</text>
  <rect x="86" y="75" width="156" height="46" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="164" y="94" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">5 new hard cases</text>
  <text x="164" y="111" font-size="9" text-anchor="middle" fill="var(--muted)">feed back to step 1</text>
  <line x1="438" y1="58" x2="478" y2="86" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="520" y1="121" x2="498" y2="173" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="396" y1="196" x2="324" y2="196" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="200" y1="173" x2="176" y2="121" stroke="var(--accent)" stroke-width="2"></line>
  <line x1="224" y1="86" x2="282" y2="60" stroke="var(--accent)" stroke-width="2"></line>
</svg>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>build a dataset</h4><p>Promote real botched production cases into test questions (L34), keeping the exam close to the real distribution.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>run an experiment</h4><p>For a candidate prompt/model config, the server runs a run over the whole set (this lesson), producing a batch of traces.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>auto-score</h4><p>Lessons 30, 35 automatically score each trace and aggregate this run's report card.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>compare & decide</h4><p>Side by side with the baseline (active config), view deltas: truly better → ship, regressed → reject—not by feeling.</p></div></div>
  <div class="step"><div class="num">5</div><div class="sc"><h4>back to step 1</h4><p>After shipping you hit new hard cases, promote them into questions… the flywheel turns, the app grows steadier.</p></div></div>
</div>

<p>That's the whole value of Part 6: it upgrades Part 5's "can score quality" into "<strong>can make decisions with scores</strong>". And the core variable the experiment keeps testing—<strong>the prompt</strong>—is the protagonist of the next part (Part 7): how it's versioned, served at speed, and tuned interactively in the Playground. Evaluation tells you "how good now", experiments tell you "would changing be better", and prompt management gives you the confidence to <strong>change safely</strong>.</p>
""")

_EN36.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why does Langfuse run experiments server-side for you rather than just letting you run locally and upload results?</strong> Both are supported (the dataset's <code>remoteExperimentUrl</code> is for local/external runs), but server-side has unique value: <strong>zero-code, strongly consistent</strong>. A product manager or non-engineer can pick a dataset, tweak a prompt, and click "run" in the UI—no script needed; and server-side runs <strong>unify</strong> variable substitution, version pinning, eval scheduling, and environment tagging—baking "how to do an experiment right" into the platform, rather than hoping every person's local script is rigorous. The cost is the platform bearing LLM-call cost and concurrency, so it goes through the <code>ExperimentCreate</code> queue, reusing Lesson 30's scheduling resilience.<br><br>
  <strong>Why compare with "baseline + deltas" rather than absolute scores?</strong> Because <strong>absolute scores mean almost nothing; relative change is what matters</strong>. Is "helpfulness 0.78" good or bad? Without a reference you can't say. But "0.07 above the active config" is a fact you can act on. More importantly, quality is often a <strong>multi-dimensional trade-off</strong>: config B is more accurate but slower and costlier. Laying each dimension's delta side by side lets a decision-maker make the <strong>clear-eyed trade-off</strong> "is this much accuracy gain worth this much latency cost"—rather than being led by a single metric. This echoes Lesson 33's monitor "alert only on change": <strong>what carries information is always "the change", not "the absolute value".</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>An experiment = prompt × dataset × model, run server-side</strong>: <code>createExperimentJobClickhouse</code> per question uses <code>replaceVariablesInPrompt</code> to fill variables, calls the chosen provider/model, produces a trace + run item—all zero-code.</li>
    <li><strong>Experiment traces carry rich context</strong>: environment tagged <code>PromptExperiments</code>, linking the <code>prompt</code> under test (L37), metadata pinning <code>itemVersion=validFrom</code> (L34/35 version replay)—reproducible and traceable.</li>
    <li><strong>Scoring auto-connects</strong>: reusing Lesson 30's <code>dataset-run-item-upsert</code> trigger and Lesson 35's aggregate-by-run, a report card appears once the run finishes, no manual work.</li>
    <li><strong>Comparison via baseline + deltas</strong>: <code>ExperimentBaselineControls</code> picks the baseline, <code>ExperimentComparisonSelector</code> chooses runs, <code>ExperimentChartsGrid</code> charts multi-dimensional deltas—absolute scores are hard to judge, relative change drives decisions.</li>
    <li><strong>Part 6 closes the loop</strong>: dataset → experiment → score → compare → decide → (new hard cases flow back to the dataset). It upgrades "can score" into "can decide with scores"; the next part's prompt gives you the confidence to "change safely".</li>
  </ul>
</div>
""")

LESSON_36 = {"zh": "\n".join(_ZH36), "en": "\n".join(_EN36)}
