"""Part 7 — Prompt 管理与 Playground / Prompts & Playground. Lessons L37–L39.

Same authoring pattern as part1..part6: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L37 · Prompt 管理（版本·label·依赖） / Prompt management
# ══════════════════════════════════════════════════════════════════════
_ZH37 = []
_EN37 = []

_ZH37.append(r"""
<p class="lead">
上一部分反复在「考」一个东西——<strong>prompt</strong>。它是你和模型对话的「脚本」，是 LLM 应用里<strong>改动最频繁</strong>的部分：一个词的措辞、一句指令的增删，都可能让效果天差地别。这一课讲 Langfuse 怎么像 <strong>git 管代码</strong>一样管 prompt：<strong>不可变的版本</strong>、<strong>可移动的 label</strong>、每次改动的 commit message，外加让一个 prompt <strong>引用另一个</strong>的依赖组合。
理解了这套「版本控制」模型，你就握住了「<strong>安全地改 prompt</strong>」的关键——能发布、能秒回滚、能精确复现任意历史版本，而这一切都不需要改一行应用代码。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  prompt 管理几乎就是<strong>专为 prompt 定制的 git</strong>。每次你改 prompt 并保存，就生成一个<strong>新版本</strong>（像一次 commit，编号自增、内容<strong>永不再改</strong>），还能附一句<strong>改动说明</strong>（commitMessage）。
  而「<code>production</code>」「<code>staging</code>」这些 <strong>label</strong>，就像 git 的<strong>分支 / 标签</strong>——它们是<strong>可移动的指针</strong>，每个指向某一个版本。把 <code>production</code> 指向 v5，就等于「<strong>发布</strong>」了 v5；发现不对，把它指回 v4，就是「<strong>秒回滚</strong>」——而你的应用代码<strong>一个字都不用动</strong>，因为它只认「给我 production 那版」，不认具体版本号。
  你甚至能让一个 prompt <strong>引用</strong>另一个（依赖），就像代码里 <code>import</code> 一个公共模块——公共的开场白写一次，处处复用。
</div>
""")

# (L37 sections below)

_ZH37.append(r"""
<h2>不可变的版本 + 可移动的 label</h2>
<p>一个 prompt 由 <code>(name, version)</code> 唯一确定（<code>@@unique([projectId, name, version])</code>）。新建一版时，version = <strong>上一版 + 1</strong>——版本号自增、内容一旦写下<strong>永不再改</strong>。而 <code>labels</code> 是一个字符串数组，关键规则是：<strong>同一个 label 在一个 name 下只能指向一个版本</strong>。所以当你给新版打上 <code>production</code> 标签，系统会<strong>自动把这个标签从旧版上摘掉</strong>——label 就这样「移动」到了新版。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="prompt 的 git 式模型：版本 v1 v2 v3 沿时间轴不可变递增，production 和 latest 等 label 是可移动指针；把 production 从 v2 移到 v3 即发布新版，移回 v2 即回滚，应用代码只认 label 不认版本号">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">版本不可变（自增），label 可移动（唯一指针）</text>
  <line x1="40" y1="150" x2="690" y2="150" stroke="var(--faint)" stroke-width="1.5"/><polygon points="690,150 682,146 682,154" fill="var(--faint)"/><text x="688" y="168" text-anchor="end" font-size="7" fill="var(--muted)">时间 / 版本</text>
  <rect x="70" y="116" width="120" height="34" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="130" y="137" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">v1（旧）</text>
  <rect x="290" y="116" width="120" height="34" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="350" y="137" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">v2（旧）</text>
  <rect x="510" y="116" width="120" height="34" rx="7" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="570" y="137" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">v3（最新）</text>
  <rect x="500" y="40" width="140" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="570" y="59" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">label: latest</text><line x1="570" y1="70" x2="570" y2="114" stroke="var(--blue)" stroke-width="1.3"/><polygon points="570,114 566,105 574,105" fill="var(--blue)"/>
  <rect x="280" y="76" width="140" height="30" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="350" y="95" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">label: production</text><line x1="350" y1="106" x2="350" y2="114" stroke="var(--accent)" stroke-width="1.3"/><polygon points="350,114 346,105 354,105" fill="var(--accent)"/>
  <path d="M 410 91 Q 480 70 560 105" fill="none" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 3"/><polygon points="560,105 551,103 553,111" fill="var(--accent)"/><text x="492" y="74" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">发布：把 production 移到 v3</text>
  <text x="360" y="196" text-anchor="middle" font-size="8" fill="var(--faint)">应用代码只说「给我 production 那版」——发布 = 移 label 到 v3，回滚 = 移回 v2，代码一行不改</text>
</svg>
<div class="figcap"><b>git 式版本控制</b>：version 自增不可变（<code>latestPrompt.version + 1</code>）；label 唯一、可移动——给新版打 <code>production</code> 会从旧版自动摘除该标签（<code>removeLabelsFromPreviousPromptVersions</code>）。新建版本默认带 <code>latest</code> 标签。源码：<code>createPrompt.ts:88-181</code>、<code>constants.ts:1-2</code>（<code>PRODUCTION_LABEL/LATEST_PROMPT_LABEL</code>）。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/prompts/server/actions/createPrompt.ts</span><span class="ln">版本自增 + label 移动</span></div>
  <pre class="code"><span class="cm">// 找到当前最新版，新版号 = 它 + 1（首版为 1）——版本号自增、内容不可变</span>
<span class="kw">const</span> latestPrompt = <span class="kw">await</span> prisma.prompt.findFirst({ where: {…name}, orderBy: [{ version: <span class="st">"desc"</span> }] });
version: latestPrompt?.version ? latestPrompt.version + 1 : 1,

<span class="cm">// 新建的 prompt 永远带上 'latest' 标签</span>
<span class="kw">const</span> finalLabels = [...labels, <span class="st">LATEST_PROMPT_LABEL</span>];   <span class="cm">// "latest"</span>

<span class="cm">// 关键：label 在一个 name 下唯一 —— 给新版打的 label，要从旧版上摘掉</span>
<span class="kw">await</span> removeLabelsFromPreviousPromptVersions({ …, labelsToRemove: finalLabels });
<span class="cm">// 于是 production 这个指针「移动」到了新版，旧版不再带它</span></pre>
</div>

<table class="t">
  <thead><tr><th>git 概念</th><th>prompt 管理对应</th><th>说明</th></tr></thead>
  <tbody>
    <tr><td>commit</td><td><code>version</code></td><td>不可变快照，编号自增，内容永不再改</td></tr>
    <tr><td>commit message</td><td><code>commitMessage</code></td><td>每次改动的一句说明，留痕可追溯</td></tr>
    <tr><td>branch / tag</td><td><code>labels</code>（production/latest…）</td><td>可移动指针，每 name 下唯一，指向某版</td></tr>
    <tr><td>仓库级标签</td><td><code>tags</code></td><td>跨所有版本一致（贴在 name 上，非某一版）</td></tr>
    <tr><td>import 模块</td><td><code>PromptDependency</code></td><td>一个 prompt 引用另一个，组合复用</td></tr>
  </tbody>
</table>
<p>把这张对照表记在心里，prompt 管理就不再是新概念——它就是你已经熟悉的 git，只不过管的不是代码，而是「和模型对话的脚本」。</p>
""")

_ZH37.append(r"""
<h2>按 label 取：让「发布」和「写代码」彻底分家</h2>
<p>这套 git 式模型最大的实用价值，藏在<strong>应用怎么取 prompt</strong>里。生产代码<strong>不该</strong>写死「给我 v5」——而该写「给我 <code>production</code> 那版」。于是「用哪一版」这个决定，从<strong>代码部署</strong>里被剥离出来，变成一次<strong>移动 label 的运营动作</strong>。发布和回滚因此快到秒级，且<strong>不经过任何代码改动、CI、上线流程</strong>。</p>

<div class="cols">
  <div class="col"><h4>按 label 取（生产推荐）</h4><p><code>get("greeting", label="production")</code>：应用永远只认 <code>production</code> 指针，谁指过去就用谁。换版本是运营在 UI 上移 label，应用<strong>无感</strong>。这是「配置与代码分离」的教科书。</p></div>
  <div class="col"><h4>按 version 取（钉死）</h4><p><code>get("greeting", version=5)</code>：精确锁定第 5 版，永不漂移。适合需要绝对可复现的场景（如一次正式实验、一篇论文的复现）。</p></div>
  <div class="col"><h4>protected labels（防误操作）</h4><p><code>PromptProtectedLabels</code> 让你把 <code>production</code> 等关键 label 设为「受保护」——移动它需要更高权限，避免新人手滑把没测过的版本推上线。</p></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 180" role="img" aria-label="按 label 取的解耦：应用代码固定请求 production 标签，标签当前指向哪个版本由运营在 UI 决定；发布是把 production 从 v4 移到 v5，回滚是移回 v4，全程不改代码不重新部署">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">「用哪版」从代码部署里剥离，变成移 label 的运营动作</text>
  <rect x="30" y="50" width="180" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="120" y="72" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">应用代码（不变）</text><text x="120" y="92" text-anchor="middle" font-size="7.2" fill="var(--muted)">get("greeting",</text><text x="120" y="106" text-anchor="middle" font-size="7.2" fill="var(--muted)">  label="production")</text><text x="120" y="122" text-anchor="middle" font-size="6.4" fill="var(--faint)">只认指针，不认版本号</text>
  <rect x="280" y="56" width="160" height="68" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="78" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">production 指针</text><text x="360" y="97" text-anchor="middle" font-size="7" fill="var(--accent-ink)">运营在 UI 上移动</text><text x="360" y="111" text-anchor="middle" font-size="6.4" fill="var(--muted)">当前 → v5</text>
  <rect x="510" y="40" width="180" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">v4（旧·可回滚目标）</text><text x="600" y="74" text-anchor="middle" font-size="6.4" fill="var(--faint)">移回即秒回滚</text>
  <rect x="510" y="96" width="180" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="114" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">v5（新·现役）</text><text x="600" y="130" text-anchor="middle" font-size="6.4" fill="var(--muted)">production 现在指这</text>
  <line x1="210" y1="90" x2="278" y2="90" stroke="var(--blue)" stroke-width="1.5"/><polygon points="278,90 269,86 269,94" fill="var(--blue)"/>
  <line x1="440" y1="100" x2="508" y2="115" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,115 499,113 501,121" fill="var(--teal)"/>
  <line x1="440" y1="86" x2="508" y2="65" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/><polygon points="508,65 499,65 502,72" fill="var(--faint)"/><text x="474" y="70" text-anchor="middle" font-size="6" fill="var(--muted)">回滚</text>
</svg>
<div class="figcap"><b>配置与代码分离</b>：应用按 <code>label="production"</code> 取，指针指向哪版由运营在 UI 决定。发布 = 移 label 到 v5；回滚 = 移回 v4——秒级、零代码、零部署。关键 label 可用 <code>PromptProtectedLabels</code> 加权限门槛。</div>
</div>
""")

# (L37 sec3 dependency below)

_ZH37.append(r"""
<h2>依赖：让一个 prompt 引用另一个</h2>
<p>prompt 多了会有重复——同一段「你是一个友好的客服助手……」开场白，可能出现在十个 prompt 里。改一次得改十处，极易漏。<code>PromptDependency</code> 解决这个：一个 prompt（parent）可以<strong>引用</strong>另一个 prompt（child），引用时既能<strong>按版本钉死</strong>（<code>childVersion</code>），也能<strong>按 label 浮动</strong>（<code>childLabel</code>）。这就像代码里 <code>import</code> 一个公共模块——公共片段写一次，处处复用。</p>

<div class="fig">
<svg viewBox="0 0 720 195" role="img" aria-label="prompt 依赖图：一个父 prompt 引用公共的系统开场白子 prompt，引用可按版本钉死或按 label 浮动；钉版本则稳定，跟 label 则子 prompt 升级时父 prompt 自动获得更新">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">prompt 组合：公共片段写一次，处处引用</text>
  <rect x="40" y="44" width="180" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="130" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">父 prompt：客服-退款</text><text x="130" y="82" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">引用「系统开场白」</text><text x="130" y="94" text-anchor="middle" font-size="6.4" fill="var(--muted)">+ 自己的退款逻辑</text>
  <rect x="40" y="116" width="180" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="130" y="136" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">父 prompt：客服-投诉</text><text x="130" y="154" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">也引用「系统开场白」</text><text x="130" y="166" text-anchor="middle" font-size="6.4" fill="var(--muted)">+ 自己的投诉逻辑</text>
  <rect x="380" y="80" width="200" height="56" rx="10" fill="var(--bg)" stroke="var(--blue)" stroke-width="2"/><text x="480" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">子 prompt：系统开场白</text><text x="480" y="118" text-anchor="middle" font-size="6.8" fill="var(--muted)">「你是友好的客服助手…」</text><text x="480" y="130" text-anchor="middle" font-size="6.4" fill="var(--faint)">写一次，被多处引用</text>
  <line x1="220" y1="72" x2="378" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,100 369,98 371,106" fill="var(--accent)"/><text x="300" y="78" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">childLabel=production（浮动）</text>
  <line x1="220" y1="144" x2="378" y2="116" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,116 369,116 372,124" fill="var(--accent)"/><text x="300" y="148" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">childVersion=3（钉死）</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">跟 label：子 prompt 升级，父自动获得新开场白 · 钉版本：父永远用第3版开场白，不受子升级影响</text>
</svg>
<div class="figcap"><b>组合即复用</b>：<code>schema.prisma:864</code> 的 PromptDependency 用 <code>parentId</code> + <code>childName</code> + <code>childLabel</code>（浮动）<b>或</b> <code>childVersion</code>（钉死）描述引用。浮动让公共片段一改处处更新，钉定让父 prompt 不受子升级影响——和第一节的 label/version 取舍如出一辙。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma:864 · createPrompt.ts</span><span class="ln">依赖：浮动 or 钉死</span></div>
  <pre class="code"><span class="kw">model</span> PromptDependency {
  parentId  String   <span class="cm">// 引用方（父 prompt）</span>
  childName String   <span class="cm">// 被引用的 prompt 名</span>
  childLabel   String?  <span class="cm">// 二选一：按 label 浮动（如 "production"），子升级父自动跟</span>
  childVersion Int?     <span class="cm">// 或：按 version 钉死（如 3），父永远用这版，不漂移</span>
}
<span class="cm">// 创建时按 dep.type 决定钉哪种（createPrompt.ts）</span>
...(dep.type === <span class="st">"version"</span> ? { childVersion: dep.version } : { childLabel: dep.label })</pre>
</div>

<p>把这套机制串起来，「安全地改 prompt」就成了一条清晰的流水线——这也正好衔接后两课的 Playground（第39课）与整个 Part 6 的实验：</p>
<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>编辑 → 存为新版</h4><p>改完保存即生成新 version（自增、带 commitMessage），旧版原封不动留存。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>在 Playground 试</h4><p>新版先在 Playground（第39课）手动试几条，或拉进数据集跑实验（第36课）量化对比。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>满意 → 移 production label</h4><p>确认更好，把 <code>production</code> 指针移到新版——线上应用下一次取 prompt 即生效，零部署。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>出问题 → 秒回滚</h4><p>万一线上表现不对，把 <code>production</code> 移回旧版即可——旧版一直在，回滚不丢数据、不等发布。</p></div></div>
</div>
""")

_ZH37.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么版本要不可变、而 label 要可移动？</strong> 这套「不可变实体 + 可移动指针」是版本控制的精髓，git 如此、第 34 课的数据项版本如此、这里的 prompt 亦如此。<strong>不可变</strong>保证了「可复现」：v5 永远是 v5，你三个月前生产用的那版，今天一字不差地还能调出来复盘。<strong>可移动的 label</strong>则提供了「可演进」：现实需要一个稳定的名字（<code>production</code>）来指代「当前现役」，而现役会变。两者结合，你既能<strong>大胆迭代</strong>（每改一版都安全留存），又能<strong>安心运营</strong>（用 label 平滑切换、随时回滚）。把不可变与可变这对矛盾，干净地分配到「版本」和「label」两个概念上——这是数据建模的优雅。<br><br>
  <strong>为什么「按 label 取」是生产解耦的关键？</strong> 因为它把<strong>「用哪一版 prompt」这个决定，从代码里彻底搬走了</strong>。如果应用写死 <code>version=5</code>，那换 prompt 就得改代码、过 CI、重新部署——慢、重、还得工程师在场。而写 <code>label="production"</code>，换版本就变成运营在 UI 上点一下移个指针：<strong>秒级生效、可回滚、非工程师也能做</strong>。这正是「配置与代码分离」的威力——把<strong>变化频繁的东西（prompt 内容）</strong>从<strong>变化缓慢的东西（应用代码）</strong>里剥离，各自用最适合的节奏演进。<code>PromptProtectedLabels</code> 再给关键 label 加一道权限门，让「秒级发布」既灵活又不失控。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>prompt = 专为 prompt 定制的 git</strong>：<code>(name, version)</code> 唯一；版本号<strong>自增、内容不可变</strong>，附 commitMessage——每次改动都安全留存、可精确复现。</li>
    <li><strong>label 是可移动指针</strong>：<code>production</code>/<code>latest</code> 等 label 在一个 name 下唯一，指向某一版；给新版打 label 会自动从旧版摘除（<code>removeLabelsFromPreviousPromptVersions</code>）——移 label = 发布 / 回滚。</li>
    <li><strong>按 label 取 = 配置与代码分离</strong>：生产写 <code>get(label="production")</code>，换版本只需运营移指针——秒级、零代码、零部署、可回滚；按 <code>version</code> 取则用于绝对复现。</li>
    <li><strong>protected labels 防误操作</strong>：<code>PromptProtectedLabels</code> 给 <code>production</code> 等关键 label 加权限门槛，避免误把未测版本推上线。</li>
    <li><strong>依赖 = prompt 组合复用</strong>：<code>PromptDependency</code> 让父 prompt 引用子 prompt，按 <code>childLabel</code> 浮动或 <code>childVersion</code> 钉死——公共片段写一次处处用，取舍逻辑和 label/version 一脉相承。</li>
  </ul>
</div>
""")

_EN37.append(r"""
<p class="lead">
The previous part kept "examining" one thing—the <strong>prompt</strong>. It's the "script" of your conversation with the model, the <strong>most frequently changed</strong> part of an LLM app: rewording one word, adding or removing one instruction, can swing the outcome wildly. This lesson is about how Langfuse manages prompts like <strong>git manages code</strong>: <strong>immutable versions</strong>, <strong>movable labels</strong>, a commit message per change, plus dependency composition that lets one prompt <strong>reference another</strong>.
Grasp this "version control" model and you hold the key to "<strong>changing prompts safely</strong>"—you can release, roll back instantly, and reproduce any historical version exactly, all without touching a line of application code.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Prompt management is almost <strong>git tailored for prompts</strong>. Each time you edit a prompt and save, it creates a <strong>new version</strong> (like a commit—an auto-incrementing number, content <strong>never changed again</strong>), with an optional <strong>change note</strong> (commitMessage).
  And labels like "<code>production</code>" / "<code>staging</code>" are like git's <strong>branches / tags</strong>—they're <strong>movable pointers</strong>, each pointing to one version. Point <code>production</code> at v5 and you've "<strong>released</strong>" v5; if something's wrong, point it back at v4 for an "<strong>instant rollback</strong>"—and your application code <strong>doesn't change one character</strong>, because it asks for "the production one", not a specific version number.
  You can even have one prompt <strong>reference</strong> another (a dependency), like <code>import</code>-ing a shared module in code—write the shared preamble once, reuse it everywhere.
</div>
""")

_EN37.append(r"""
<h2>Immutable versions + movable labels</h2>
<p>A prompt is uniquely identified by <code>(name, version)</code> (<code>@@unique([projectId, name, version])</code>). On creating a version, version = <strong>previous + 1</strong>—the number auto-increments, and once written the content is <strong>never changed again</strong>. <code>labels</code> is a string array, with the key rule: <strong>a given label can point to only one version under a name</strong>. So when you tag a new version with <code>production</code>, the system <strong>automatically strips that label from the old version</strong>—the label thus "moves" to the new one.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="The git-style prompt model: versions v1 v2 v3 increment immutably along a timeline; labels like production and latest are movable pointers; moving production from v2 to v3 is a release, moving it back to v2 is a rollback, with app code only knowing the label not the version number">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">versions immutable (auto-increment), labels movable (unique pointers)</text>
  <line x1="40" y1="150" x2="690" y2="150" stroke="var(--faint)" stroke-width="1.5"/><polygon points="690,150 682,146 682,154" fill="var(--faint)"/><text x="688" y="168" text-anchor="end" font-size="7" fill="var(--muted)">time / version</text>
  <rect x="70" y="116" width="120" height="34" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="130" y="137" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">v1 (old)</text>
  <rect x="290" y="116" width="120" height="34" rx="7" fill="var(--bg)" stroke="var(--faint)"/><text x="350" y="137" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">v2 (old)</text>
  <rect x="510" y="116" width="120" height="34" rx="7" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="570" y="137" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">v3 (latest)</text>
  <rect x="500" y="40" width="140" height="30" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="570" y="59" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">label: latest</text><line x1="570" y1="70" x2="570" y2="114" stroke="var(--blue)" stroke-width="1.3"/><polygon points="570,114 566,105 574,105" fill="var(--blue)"/>
  <rect x="280" y="76" width="140" height="30" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="350" y="95" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">label: production</text><line x1="350" y1="106" x2="350" y2="114" stroke="var(--accent)" stroke-width="1.3"/><polygon points="350,114 346,105 354,105" fill="var(--accent)"/>
  <path d="M 410 91 Q 480 70 560 105" fill="none" stroke="var(--accent)" stroke-width="1.4" stroke-dasharray="4 3"/><polygon points="560,105 551,103 553,111" fill="var(--accent)"/><text x="492" y="74" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">release: move production to v3</text>
  <text x="360" y="196" text-anchor="middle" font-size="8" fill="var(--faint)">app code just says "give me the production one"—release = move the label to v3, rollback = move it back to v2, no code change</text>
</svg>
<div class="figcap"><b>git-style version control</b>: version auto-increments and is immutable (<code>latestPrompt.version + 1</code>); a label is unique and movable—tagging a new version with <code>production</code> auto-strips it from the old one (<code>removeLabelsFromPreviousPromptVersions</code>). A new version always gets the <code>latest</code> label. Source: <code>createPrompt.ts:88-181</code>, <code>constants.ts:1-2</code> (<code>PRODUCTION_LABEL/LATEST_PROMPT_LABEL</code>).</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/prompts/server/actions/createPrompt.ts</span><span class="ln">version increment + label move</span></div>
  <pre class="code"><span class="cm">// find the current latest version; new = it + 1 (first is 1)—number auto-increments, content immutable</span>
<span class="kw">const</span> latestPrompt = <span class="kw">await</span> prisma.prompt.findFirst({ where: {…name}, orderBy: [{ version: <span class="st">"desc"</span> }] });
version: latestPrompt?.version ? latestPrompt.version + 1 : 1,

<span class="cm">// a newly created prompt always gets the 'latest' label</span>
<span class="kw">const</span> finalLabels = [...labels, <span class="st">LATEST_PROMPT_LABEL</span>];   <span class="cm">// "latest"</span>

<span class="cm">// key: a label is unique per name — labels put on the new version must be stripped from old ones</span>
<span class="kw">await</span> removeLabelsFromPreviousPromptVersions({ …, labelsToRemove: finalLabels });
<span class="cm">// so the production pointer "moves" to the new version; old versions no longer carry it</span></pre>
</div>

<table class="t">
  <thead><tr><th>git concept</th><th>prompt management counterpart</th><th>note</th></tr></thead>
  <tbody>
    <tr><td>commit</td><td><code>version</code></td><td>immutable snapshot, auto-incrementing number, content never changed</td></tr>
    <tr><td>commit message</td><td><code>commitMessage</code></td><td>a note per change, leaving a traceable trail</td></tr>
    <tr><td>branch / tag</td><td><code>labels</code> (production/latest…)</td><td>movable pointers, unique per name, pointing to a version</td></tr>
    <tr><td>repo-level labels</td><td><code>tags</code></td><td>consistent across all versions (on the name, not a version)</td></tr>
    <tr><td>import a module</td><td><code>PromptDependency</code></td><td>one prompt references another, composition reuse</td></tr>
  </tbody>
</table>
<p>Keep this mapping in mind and prompt management is no longer a new concept—it's the git you already know, just managing not code but "the script of your conversation with the model".</p>
""")

# (en sec2/3/spark below)

_EN37.append(r"""
<h2>Fetch by label: fully divorce "releasing" from "writing code"</h2>
<p>This git-style model's biggest practical value hides in <strong>how the app fetches a prompt</strong>. Production code <strong>shouldn't</strong> hardcode "give me v5"—it should say "give me the <code>production</code> one". So the decision of "which version to use" is lifted out of <strong>code deployment</strong> into a <strong>label-moving operations action</strong>. Releases and rollbacks thus become second-scale, and <strong>bypass any code change, CI, or deploy flow</strong>.</p>

<div class="cols">
  <div class="col"><h4>fetch by label (production-preferred)</h4><p><code>get("greeting", label="production")</code>: the app only ever knows the <code>production</code> pointer, using whatever it points to. Switching versions is operations moving a label in the UI, with the app <strong>oblivious</strong>. A textbook of "config-code separation".</p></div>
  <div class="col"><h4>fetch by version (pinned)</h4><p><code>get("greeting", version=5)</code>: locks exactly to version 5, never drifting. Suits absolute-reproducibility scenarios (a formal experiment, reproducing a paper).</p></div>
  <div class="col"><h4>protected labels (against fat-fingering)</h4><p><code>PromptProtectedLabels</code> lets you mark key labels like <code>production</code> as "protected"—moving it needs higher permission, preventing a newcomer from accidentally shipping an untested version.</p></div>
</div>

<div class="fig">
<svg viewBox="0 0 720 180" role="img" aria-label="Fetch-by-label decoupling: app code fixedly requests the production label, with which version it currently points to decided by operations in the UI; a release moves production from v4 to v5, a rollback moves it back to v4, all without code change or redeploy">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">"which version" lifted out of code deploy into a label-move ops action</text>
  <rect x="30" y="50" width="180" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="120" y="72" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">app code (unchanged)</text><text x="120" y="92" text-anchor="middle" font-size="7.2" fill="var(--muted)">get("greeting",</text><text x="120" y="106" text-anchor="middle" font-size="7.2" fill="var(--muted)">  label="production")</text><text x="120" y="122" text-anchor="middle" font-size="6.4" fill="var(--faint)">knows the pointer, not the version</text>
  <rect x="280" y="56" width="160" height="68" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="78" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">production pointer</text><text x="360" y="97" text-anchor="middle" font-size="7" fill="var(--accent-ink)">operations moves it in the UI</text><text x="360" y="111" text-anchor="middle" font-size="6.4" fill="var(--muted)">currently → v5</text>
  <rect x="510" y="40" width="180" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">v4 (old · rollback target)</text><text x="600" y="74" text-anchor="middle" font-size="6.4" fill="var(--faint)">move back = instant rollback</text>
  <rect x="510" y="96" width="180" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="114" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">v5 (new · active)</text><text x="600" y="130" text-anchor="middle" font-size="6.4" fill="var(--muted)">production points here now</text>
  <line x1="210" y1="90" x2="278" y2="90" stroke="var(--blue)" stroke-width="1.5"/><polygon points="278,90 269,86 269,94" fill="var(--blue)"/>
  <line x1="440" y1="100" x2="508" y2="115" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,115 499,113 501,121" fill="var(--teal)"/>
  <line x1="440" y1="86" x2="508" y2="65" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/><polygon points="508,65 499,65 502,72" fill="var(--faint)"/><text x="474" y="70" text-anchor="middle" font-size="6" fill="var(--muted)">rollback</text>
</svg>
<div class="figcap"><b>config-code separation</b>: the app fetches by <code>label="production"</code>, with which version the pointer targets decided by operations in the UI. Release = move the label to v5; rollback = move it back to v4—second-scale, zero-code, zero-deploy. Key labels can be gated via <code>PromptProtectedLabels</code>.</div>
</div>
""")

_EN37.append(r"""
<h2>Dependencies: let one prompt reference another</h2>
<p>With many prompts comes duplication—the same "You are a friendly support assistant…" preamble might appear in ten prompts. Editing it once means editing ten places, easy to miss. <code>PromptDependency</code> solves this: a prompt (parent) can <strong>reference</strong> another prompt (child), either <strong>pinned by version</strong> (<code>childVersion</code>) or <strong>floating by label</strong> (<code>childLabel</code>). It's like <code>import</code>-ing a shared module in code—write the shared snippet once, reuse it everywhere.</p>

<div class="fig">
<svg viewBox="0 0 720 195" role="img" aria-label="Prompt dependency graph: parent prompts reference a shared system-preamble child prompt; references can pin a version or float by label; pinning is stable, while following a label means the parent auto-updates when the child upgrades">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">prompt composition: write the shared snippet once, reference everywhere</text>
  <rect x="40" y="44" width="180" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="130" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">parent: support-refund</text><text x="130" y="82" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">references "system preamble"</text><text x="130" y="94" text-anchor="middle" font-size="6.4" fill="var(--muted)">+ its own refund logic</text>
  <rect x="40" y="116" width="180" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="130" y="136" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">parent: support-complaint</text><text x="130" y="154" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">also references "system preamble"</text><text x="130" y="166" text-anchor="middle" font-size="6.4" fill="var(--muted)">+ its own complaint logic</text>
  <rect x="380" y="80" width="200" height="56" rx="10" fill="var(--bg)" stroke="var(--blue)" stroke-width="2"/><text x="480" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">child: system preamble</text><text x="480" y="118" text-anchor="middle" font-size="6.8" fill="var(--muted)">"You are a friendly support assistant…"</text><text x="480" y="130" text-anchor="middle" font-size="6.4" fill="var(--faint)">written once, referenced by many</text>
  <line x1="220" y1="72" x2="378" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,100 369,98 371,106" fill="var(--accent)"/><text x="300" y="78" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">childLabel=production (floating)</text>
  <line x1="220" y1="144" x2="378" y2="116" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,116 369,116 372,124" fill="var(--accent)"/><text x="300" y="148" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">childVersion=3 (pinned)</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">follow a label: child upgrades, parent auto-gets new preamble · pin a version: parent always uses preamble v3, unaffected by upgrades</text>
</svg>
<div class="figcap"><b>composition is reuse</b>: <code>schema.prisma:864</code>'s PromptDependency uses <code>parentId</code> + <code>childName</code> + <code>childLabel</code> (floating) <b>or</b> <code>childVersion</code> (pinned). Floating makes a shared snippet update everywhere on one edit; pinning shields a parent from a child upgrade—mirroring the first section's label/version trade-off.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/prisma/schema.prisma:864 · createPrompt.ts</span><span class="ln">dependency: floating or pinned</span></div>
  <pre class="code"><span class="kw">model</span> PromptDependency {
  parentId  String   <span class="cm">// the referrer (parent prompt)</span>
  childName String   <span class="cm">// the referenced prompt's name</span>
  childLabel   String?  <span class="cm">// one of: float by label (e.g. "production"), parent follows child upgrades</span>
  childVersion Int?     <span class="cm">// or: pin by version (e.g. 3), parent always uses this, no drift</span>
}
<span class="cm">// on create, dep.type decides which to pin (createPrompt.ts)</span>
...(dep.type === <span class="st">"version"</span> ? { childVersion: dep.version } : { childLabel: dep.label })</pre>
</div>

<p>String this mechanism together and "changing a prompt safely" becomes a clear pipeline—dovetailing with the next lessons' Playground (L39) and all of Part 6's experiments:</p>
<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>edit → save as a new version</h4><p>Saving an edit creates a new version (auto-incrementing, with a commitMessage); the old version is preserved intact.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>try in the Playground</h4><p>Try the new version on a few cases in the Playground (L39), or pull it into a dataset to run an experiment (L36) for a quantitative comparison.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>satisfied → move the production label</h4><p>Confirmed better, move the <code>production</code> pointer to the new version—the production app's next prompt fetch picks it up, zero-deploy.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>trouble → instant rollback</h4><p>If production misbehaves, move <code>production</code> back to the old version—the old one is always there, rollback loses no data and waits for no release.</p></div></div>
</div>
""")

_EN37.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why are versions immutable while labels are movable?</strong> This "immutable entity + movable pointer" is the essence of version control—git is so, Lesson 34's dataset items are so, prompts here too. <strong>Immutability</strong> guarantees "reproducibility": v5 is forever v5, and the version you ran in production three months ago can be pulled up today, word for word, for a post-mortem. <strong>Movable labels</strong> provide "evolvability": reality needs a stable name (<code>production</code>) to denote "the current active one", and the active one changes. Together, you can both <strong>iterate boldly</strong> (every edit safely preserved) and <strong>operate calmly</strong> (switch smoothly via labels, roll back anytime). Cleanly assigning the immutable/mutable tension onto the two concepts "version" and "label" is the elegance of data modeling.<br><br>
  <strong>Why is "fetch by label" the key to production decoupling?</strong> Because it <strong>fully moves the decision "which prompt version to use" out of the code</strong>. If the app hardcodes <code>version=5</code>, switching prompts means changing code, passing CI, redeploying—slow, heavy, and needs an engineer present. With <code>label="production"</code>, switching becomes operations clicking a pointer-move in the UI: <strong>second-scale, rollback-able, doable by non-engineers</strong>. This is the power of "config-code separation"—lifting <strong>the frequently-changing thing (prompt content)</strong> out of <strong>the slowly-changing thing (app code)</strong>, each evolving at its own pace. <code>PromptProtectedLabels</code> then gates key labels, keeping "second-scale releases" flexible without losing control.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>A prompt = git tailored for prompts</strong>: <code>(name, version)</code> unique; the version number <strong>auto-increments, content immutable</strong>, with a commitMessage—every edit safely preserved and exactly reproducible.</li>
    <li><strong>A label is a movable pointer</strong>: <code>production</code>/<code>latest</code> labels are unique per name, pointing to one version; tagging a new version auto-strips the label from the old one (<code>removeLabelsFromPreviousPromptVersions</code>)—moving a label = release / rollback.</li>
    <li><strong>Fetch by label = config-code separation</strong>: production does <code>get(label="production")</code>, switching versions just needs operations moving a pointer—second-scale, zero-code, zero-deploy, rollback-able; fetch by <code>version</code> is for absolute reproducibility.</li>
    <li><strong>Protected labels against fat-fingering</strong>: <code>PromptProtectedLabels</code> gates key labels like <code>production</code> with permissions, preventing an untested version from being shipped by accident.</li>
    <li><strong>Dependencies = prompt composition reuse</strong>: <code>PromptDependency</code> lets a parent reference a child by <code>childLabel</code> (floating) or <code>childVersion</code> (pinned)—write a shared snippet once, reuse everywhere, with trade-off logic mirroring label/version.</li>
  </ul>
</div>
""")

LESSON_37 = {"zh": "\n".join(_ZH37), "en": "\n".join(_EN37)}
