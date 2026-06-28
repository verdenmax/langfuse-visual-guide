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
<div class="fig">
<svg viewBox="0 0 720 188" role="img" aria-label="prompt 版本历史真实例子：prompt support-reply 有 v1/v2/v3 三个不可变版本，最新在上；每行有 version、labels、commitMessage、创建者与时间；v3 钉着 production+latest 标签并高亮。字段取自 schema.prisma 的 Prompt，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：一个 prompt 的版本历史</text>
  <rect x="20" y="30" width="680" height="24" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="34" y="46" font-size="9" font-weight="700" fill="var(--accent-ink)">prompt · name=support-reply · type=text · 3 versions</text>
  <rect x="20" y="58" width="680" height="20" fill="var(--panel-2)"/>
  <text x="40" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">version</text>
  <text x="120" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">labels</text>
  <text x="330" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">commitMessage</text>
  <text x="560" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">createdBy · createdAt</text>
  <rect x="20" y="80" width="680" height="28" fill="var(--accent-soft)" stroke="var(--line)" stroke-width="0.5"/>
  <text x="40" y="98" font-size="9" font-weight="700" fill="var(--accent-ink)">v3</text>
  <rect x="120" y="85" width="70" height="17" rx="8" fill="var(--accent)" opacity="0.18"/><text x="155" y="97" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent)">production</text>
  <rect x="196.0" y="85" width="48" height="17" rx="8" fill="var(--blue)" opacity="0.18"/><text x="220" y="97" text-anchor="middle" font-size="7" font-weight="700" fill="var(--blue)">latest</text>
  <text x="330" y="98" font-size="7.6" fill="var(--ink)">收紧退款措辞</text>
  <text x="560" y="98" font-size="7.2" fill="var(--muted)">alice · 2026-06-20</text>
  <rect x="20" y="108" width="680" height="28" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
  <text x="40" y="126" font-size="9" font-weight="700" fill="var(--accent-ink)">v2</text>
  <rect x="120" y="113" width="53" height="17" rx="8" fill="var(--amber)" opacity="0.18"/><text x="147" y="125" text-anchor="middle" font-size="7" font-weight="700" fill="var(--amber)">staging</text>
  <text x="330" y="126" font-size="7.6" fill="var(--ink)">加一句共情开场</text>
  <text x="560" y="126" font-size="7.2" fill="var(--muted)">bob · 2026-06-12</text>
  <rect x="20" y="136" width="680" height="28" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
  <text x="40" y="154" font-size="9" font-weight="700" fill="var(--accent-ink)">v1</text>
  <text x="120" y="154" font-size="7.4" fill="var(--faint)">（无）</text>
  <text x="330" y="154" font-size="7.6" fill="var(--ink)">初版</text>
  <text x="560" y="154" font-size="7.2" fill="var(--muted)">alice · 2026-06-01</text>
  <text x="34" y="178" font-size="7.4" fill="var(--muted)">版本不可变递增（unique projectId+name+version）；production / latest 是可移动指针，现都指向 v3</text>
</svg>
<div class="figcap"><b>版本历史就是一段「prompt 的 git log」</b>（字段取自 <code>schema.prisma</code> 的 <code>Prompt</code>：<code>version</code>/<code>labels</code>/<code>commitMessage</code>/<code>createdBy</code>；<b>值为示例</b>）：每次保存生成一个<b>不可变</b>的新版本（<code>@@unique([projectId,name,version])</code>），最新在上。<code>production</code>、<code>latest</code> 不是版本号而是<b>可移动的标签指针</b>——发布＝把 <code>production</code> 移到某版，回滚＝移回去，应用代码只认标签。这张表正是上面「git 式模型」的<b>真实数据形态</b>。</div>
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
  <rect x="30" y="50" width="180" height="80" rx="10" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="120" y="72" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">应用代码（不变）</text><text x="120" y="92" text-anchor="middle" font-size="7.2" fill="var(--muted)">get("greeting",</text><text x="120" y="106" text-anchor="middle" font-size="7.2" fill="var(--muted)">  label="production")</text><text x="120" y="122" text-anchor="middle" font-size="6.5" fill="var(--faint)">只认指针，不认版本号</text>
  <rect x="280" y="56" width="160" height="68" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="78" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">production 指针</text><text x="360" y="97" text-anchor="middle" font-size="7" fill="var(--accent-ink)">运营在 UI 上移动</text><text x="360" y="111" text-anchor="middle" font-size="6.5" fill="var(--muted)">当前 → v5</text>
  <rect x="510" y="40" width="180" height="44" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="600" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--muted)">v4（旧·可回滚目标）</text><text x="600" y="74" text-anchor="middle" font-size="6.5" fill="var(--faint)">移回即秒回滚</text>
  <rect x="510" y="96" width="180" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="600" y="114" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">v5（新·现役）</text><text x="600" y="130" text-anchor="middle" font-size="6.5" fill="var(--muted)">production 现在指这</text>
  <line x1="210" y1="90" x2="278" y2="90" stroke="var(--blue)" stroke-width="1.5"/><polygon points="278,90 269,86 269,94" fill="var(--blue)"/>
  <line x1="440" y1="100" x2="508" y2="115" stroke="var(--teal)" stroke-width="1.5"/><polygon points="508,115 499,113 501,121" fill="var(--teal)"/>
  <line x1="440" y1="86" x2="508" y2="65" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/><polygon points="508,65 499,65 502,72" fill="var(--faint)"/><text x="474" y="70" text-anchor="middle" font-size="6.5" fill="var(--muted)">回滚</text>
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
  <rect x="40" y="44" width="180" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="130" y="64" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">父 prompt：客服-退款</text><text x="130" y="82" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">引用「系统开场白」</text><text x="130" y="94" text-anchor="middle" font-size="6.5" fill="var(--muted)">+ 自己的退款逻辑</text>
  <rect x="40" y="116" width="180" height="56" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="130" y="136" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">父 prompt：客服-投诉</text><text x="130" y="154" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">也引用「系统开场白」</text><text x="130" y="166" text-anchor="middle" font-size="6.5" fill="var(--muted)">+ 自己的投诉逻辑</text>
  <rect x="380" y="80" width="200" height="56" rx="10" fill="var(--bg)" stroke="var(--blue)" stroke-width="2"/><text x="480" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">子 prompt：系统开场白</text><text x="480" y="118" text-anchor="middle" font-size="6.8" fill="var(--muted)">「你是友好的客服助手…」</text><text x="480" y="130" text-anchor="middle" font-size="6.5" fill="var(--faint)">写一次，被多处引用</text>
  <line x1="220" y1="72" x2="378" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,100 369,98 371,106" fill="var(--accent)"/><text x="300" y="78" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">childLabel=production（浮动）</text>
  <line x1="220" y1="144" x2="378" y2="116" stroke="var(--accent)" stroke-width="1.4"/><polygon points="378,116 369,116 372,124" fill="var(--accent)"/><text x="300" y="148" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">childVersion=3（钉死）</text>
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
<div class="fig">
<svg viewBox="0 0 720 188" role="img" aria-label="Prompt version-history real example: prompt support-reply has three immutable versions v1/v2/v3, newest on top; each row shows version, labels, commitMessage, author and time; v3 pins the production+latest labels and is highlighted. Fields from the Prompt model in schema.prisma, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: a prompt's version history</text>
  <rect x="20" y="30" width="680" height="24" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="34" y="46" font-size="9" font-weight="700" fill="var(--accent-ink)">prompt · name=support-reply · type=text · 3 versions</text>
  <rect x="20" y="58" width="680" height="20" fill="var(--panel-2)"/>
  <text x="40" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">version</text>
  <text x="120" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">labels</text>
  <text x="330" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">commitMessage</text>
  <text x="560" y="72" font-size="7.6" font-weight="700" fill="var(--ink)">createdBy · createdAt</text>
  <rect x="20" y="80" width="680" height="28" fill="var(--accent-soft)" stroke="var(--line)" stroke-width="0.5"/>
  <text x="40" y="98" font-size="9" font-weight="700" fill="var(--accent-ink)">v3</text>
  <rect x="120" y="85" width="70" height="17" rx="8" fill="var(--accent)" opacity="0.18"/><text x="155" y="97" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent)">production</text>
  <rect x="196.0" y="85" width="48" height="17" rx="8" fill="var(--blue)" opacity="0.18"/><text x="220" y="97" text-anchor="middle" font-size="7" font-weight="700" fill="var(--blue)">latest</text>
  <text x="330" y="98" font-size="7.6" fill="var(--ink)">tighten refund wording</text>
  <text x="560" y="98" font-size="7.2" fill="var(--muted)">alice · 2026-06-20</text>
  <rect x="20" y="108" width="680" height="28" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
  <text x="40" y="126" font-size="9" font-weight="700" fill="var(--accent-ink)">v2</text>
  <rect x="120" y="113" width="53" height="17" rx="8" fill="var(--amber)" opacity="0.18"/><text x="147" y="125" text-anchor="middle" font-size="7" font-weight="700" fill="var(--amber)">staging</text>
  <text x="330" y="126" font-size="7.6" fill="var(--ink)">add an empathy line</text>
  <text x="560" y="126" font-size="7.2" fill="var(--muted)">bob · 2026-06-12</text>
  <rect x="20" y="136" width="680" height="28" fill="var(--bg)" stroke="var(--line)" stroke-width="0.5"/>
  <text x="40" y="154" font-size="9" font-weight="700" fill="var(--accent-ink)">v1</text>
  <text x="120" y="154" font-size="7.4" fill="var(--faint)">(none)</text>
  <text x="330" y="154" font-size="7.6" fill="var(--ink)">initial version</text>
  <text x="560" y="154" font-size="7.2" fill="var(--muted)">alice · 2026-06-01</text>
  <text x="34" y="178" font-size="7.4" fill="var(--muted)">versions are immutable &amp; incrementing (unique projectId+name+version); production / latest are movable pointers, both on v3 now</text>
</svg>
<div class="figcap"><b>The version history is a "git log for your prompt"</b> (fields from the <code>Prompt</code> model in <code>schema.prisma</code>: <code>version</code>/<code>labels</code>/<code>commitMessage</code>/<code>createdBy</code>; <b>values illustrative</b>): each save creates a new <b>immutable</b> version (<code>@@unique([projectId,name,version])</code>), newest on top. <code>production</code> and <code>latest</code> are not version numbers but <b>movable label pointers</b> — a release moves <code>production</code> onto a version, a rollback moves it back, and app code only knows the label. This table is the <b>concrete data form</b> of the git-style model above.</div>
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


# ══════════════════════════════════════════════════════════════════════
# L38 · Prompt 服务与缓存 / Prompt serving & caching
# ══════════════════════════════════════════════════════════════════════
_ZH38 = []
_EN38 = []

_ZH38.append(r"""
<p class="lead">
上一课让你能<strong>安全地管</strong> prompt。但生产里有个现实问题：应用可能<strong>每一次 LLM 调用都要先取一次 prompt</strong>（「给我 production 那版」）。如果每次都去 Postgres 查一遍，既慢、又把数据库压垮。这一课讲 <strong>PromptService</strong> 怎么用 Redis 把 prompt 服务做得又快又稳，重点是两个机制：经典的 <strong>read-through 缓存</strong>，和一个极其优雅的<strong>「换命名空间，而非逐个删 key」</strong>的 epoch 失效策略。
中间还会看到第 37 课依赖的「下半场」：被引用的子 prompt 在服务时会被<strong>解析内联</strong>成一个完整 prompt，而正是这个「一份 prompt 可能横跨多个名字」的事实，逼出了那个聪明的失效设计。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  prompt 服务像图书馆的<strong>热门书快取架</strong>。读者（应用）来借书（prompt），管理员先看<strong>快取架</strong>（Redis）上有没有：有就<strong>秒递</strong>，没有才跑去<strong>大书库</strong>（Postgres）取一本、顺手在快取架放一份，下个人就快了。
  难题来了：一本书<strong>出了新版</strong>，怎么让大家别再借到旧版？满架去翻、把旧版一本本抽走<strong>太难了</strong>——何况一本书里还可能<strong>夹着别本书的章节</strong>（第 37 课的依赖），牵一发动全身。图书馆的妙招是：给整个快取架挂一块<strong>新的「版本号牌」</strong>。旧号牌下的书<strong>没人再认</strong>（按规则只认当前号牌），它们不必清理、放着自然过期就行；而所有新借的，都从<strong>挂着新号牌的货架</strong>走。<strong>换块牌子，比逐本抽书，快太多也稳太多。</strong>
</div>
""")

# (L38 sections below)

_ZH38.append(r"""
<h2>read-through 缓存：先问 Redis，没有再回库</h2>
<p>核心方法是 <code>PromptService.getPrompt</code>，它实现教科书式的 <strong>read-through（读穿透）</strong>缓存：先查 Redis，命中就直接返回；<strong>未命中</strong>才回 Postgres 查（<code>findPrompt</code>），查到后<strong>顺手写进 Redis</strong>（带 TTL），下一次同样的请求就走缓存了。缓存开不开由 <code>LANGFUSE_CACHE_PROMPT_ENABLED</code> 控制，每条缓存活多久由 <code>LANGFUSE_CACHE_PROMPT_TTL_SECONDS</code> 控制。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="read-through 缓存流程：应用请求 production 的 prompt，PromptService 先查 Redis，命中则秒返回；未命中则查 Postgres、把结果写进 Redis（带 TTL）再返回，下次同请求即命中">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">read-through：缓存命中走捷径，未命中回库并回填</text>
  <rect x="30" y="86" width="130" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="106" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">应用</text><text x="95" y="122" text-anchor="middle" font-size="6.6" fill="var(--muted)">getPrompt(production)</text>
  <rect x="220" y="80" width="150" height="60" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="295" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">PromptService</text><text x="295" y="117" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">① 先查 Redis</text><text x="295" y="129" text-anchor="middle" font-size="6.5" fill="var(--muted)">命中→返回</text>
  <rect x="430" y="40" width="150" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="505" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Redis 缓存</text><text x="505" y="76" text-anchor="middle" font-size="6.5" fill="var(--muted)">毫秒级 · 带 TTL</text>
  <rect x="430" y="130" width="150" height="48" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="505" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">Postgres（权威）</text><text x="505" y="166" text-anchor="middle" font-size="6.5" fill="var(--muted)">未命中才查</text>
  <line x1="160" y1="110" x2="218" y2="110" stroke="var(--blue)" stroke-width="1.5"/><polygon points="218,110 209,106 209,114" fill="var(--blue)"/>
  <line x1="370" y1="95" x2="428" y2="70" stroke="var(--accent)" stroke-width="1.5"/><polygon points="428,70 419,69 421,77" fill="var(--accent)"/><text x="399" y="78" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">① 命中</text>
  <line x1="370" y1="120" x2="428" y2="150" stroke="var(--teal)" stroke-width="1.3" stroke-dasharray="3 2"/><polygon points="428,150 419,148 421,156" fill="var(--teal)"/><text x="396" y="142" text-anchor="middle" font-size="6.5" fill="var(--teal)">② 未命中→查库</text>
  <path d="M 505 130 Q 560 110 580 90" fill="none" stroke="var(--accent)" stroke-width="1.3" stroke-dasharray="4 3"/><polygon points="580,90 572,95 578,98" fill="var(--accent)"/><text x="600" y="112" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">③ 回填 Redis</text>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">绝大多数请求走 ①（毫秒、不碰库）；只有缓存冷/失效后第一笔走 ②③——数据库压力被缓存挡在前面</text>
</svg>
<div class="figcap"><b>读穿透 + 回填</b>：<code>getPrompt</code> 先 <code>getCachedPrompt</code>，命中即返回；未命中走 <code>findPrompt</code>（DB）再 <code>cachePrompt</code>（<code>redis.set(key, value, "EX", ttlSeconds)</code>）。开关 <code>LANGFUSE_CACHE_PROMPT_ENABLED</code>、时长 <code>LANGFUSE_CACHE_PROMPT_TTL_SECONDS</code>。源码：<code>PromptService/index.ts:49-86,166-173</code>。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 212" role="img" aria-label="缓存命中与未命中的延迟对比真实例子：命中走 Redis 约 1 毫秒秒回，未命中要查 Postgres 再回填 Redis 约 25 毫秒，约 25 倍差距；稳态命中率约 98%；TTL 3600 秒、epoch 轮换即失效。延迟与命中率为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：命中 vs 未命中的延迟</text>
  <text x="20" y="56" font-size="8.5" font-weight="700" fill="var(--accent-ink)">cache HIT</text><text x="20" y="68" font-size="7" fill="var(--muted)">Redis</text>
  <rect x="210" y="46" width="18" height="22" rx="4" fill="var(--accent)" opacity="0.85"/><text x="236" y="61" font-size="8" font-weight="700" fill="var(--accent-ink)">~1 ms · 秒回</text>
  <text x="20" y="98" font-size="8.5" font-weight="700" fill="var(--amber)">cache MISS</text><text x="20" y="110" font-size="7" fill="var(--muted)">查 PG+回填</text>
  <rect x="210" y="88" width="460" height="22" rx="4" fill="var(--amber)" opacity="0.8"/><text x="678" y="103" font-size="8" font-weight="700" fill="var(--amber)">~25 ms</text>
  <rect x="210" y="120" width="150" height="20" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="285" y="134" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">≈ 25× 更快</text>
  <text x="20" y="166" font-size="8" font-weight="700" fill="var(--ink)">稳态命中率</text>
  <rect x="210" y="156" width="460" height="16" rx="8" fill="var(--panel-2)"/><rect x="210" y="156" width="451" height="16" rx="8" fill="var(--accent)" opacity="0.55"/><text x="676" y="168" font-size="8" font-weight="700" fill="var(--accent-ink)">≈ 98%</text>
  <line x1="20" y1="184" x2="700" y2="184" stroke="var(--line)"/>
  <text x="20" y="200" font-size="7.4" fill="var(--muted)">TTL 3600s（1h，LANGFUSE_CACHE_PROMPT_TTL_SECONDS）· 改 prompt → 轮换项目级 epoch → 旧 key 瞬间失效，无需逐个删</text>
</svg>
<div class="figcap"><b>缓存把「每次都查库」变成「几乎不查库」</b>（延迟/命中率<b>为示例</b>，机制取自 <code>PromptService</code>）：命中走 Redis 约 <code>1ms</code> 秒回，未命中才查 Postgres 再回填、约 <code>25ms</code>——相差约 <b>25 倍</b>。稳态命中率高（图中 ≈98%），意味着<b>绝大多数取 prompt 的请求都不碰数据库</b>。两道保险：<code>TTL 3600s</code> 兜底过期，改 prompt 时<b>轮换项目级 epoch</b>让旧 key 瞬间失效（上面 epoch 图的实际收益）。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/PromptService/index.ts</span><span class="ln">getPrompt 读穿透</span></div>
  <pre class="code"><span class="kw">public async</span> <span class="fn">getPrompt</span>(params): Promise&lt;PromptResult | null&gt; {
  <span class="kw">if</span> (this.cacheEnabled) {
    <span class="kw">const</span> cachedPrompt = <span class="kw">await</span> this.getCachedPrompt(params);   <span class="cm">// ① 先问 Redis</span>
    <span class="kw">if</span> (cachedPrompt) <span class="kw">return</span> cachedPrompt;                     <span class="cm">// 命中 → 秒返回，不碰库</span>
  }
  <span class="kw">const</span> dbPrompt = <span class="kw">await</span> this.findPrompt(params);              <span class="cm">// ② 未命中 → 查 Postgres</span>
  <span class="kw">if</span> (this.cacheEnabled &amp;&amp; dbPrompt)
    <span class="kw">await</span> this.cachePrompt({ ...params, prompt: dbPrompt });    <span class="cm">// ③ 回填 Redis（带 TTL）</span>
  <span class="kw">return</span> dbPrompt;
}
<span class="cm">// cachePrompt: redis.set(key, value, "EX", this.ttlSeconds)  —— 每条缓存自带过期</span></pre>
</div>

<table class="t">
  <thead><tr><th>情形</th><th>走哪条路</th><th>延迟</th><th>碰 Postgres 吗</th></tr></thead>
  <tbody>
    <tr><td><b>缓存命中</b>（绝大多数）</td><td>Redis 直接返回</td><td>毫秒级</td><td>否</td></tr>
    <tr><td><b>缓存未命中</b>（冷启/刚失效）</td><td>查 DB → 回填 Redis → 返回</td><td>一次 DB 往返</td><td>是（仅这一笔）</td></tr>
    <tr><td><b>TTL 到期</b></td><td>下次读变未命中，自动回填</td><td>同上，单笔</td><td>是（单笔）</td></tr>
  </tbody>
</table>
<p>一句话：<strong>数据库只在「第一笔」承压，之后全被 Redis 接住</strong>。这正是 read-through 的价值——把一个「每次调用都要读」的高频访问，摊薄成「每个 TTL 周期一次 DB 读」。</p>
""")

_ZH38.append(r"""
<h2>解析：把依赖内联成一个完整 prompt</h2>
<p>第 37 课说 prompt 能引用别的 prompt。但应用最终拿到的，得是一个<strong>完整、自包含</strong>的 prompt——不能让运行时还去现凑那些被引用的片段。所以服务时有一步<strong>解析（resolve）</strong>：<code>buildAndResolvePromptGraph</code> 沿着依赖图把每个被引用的子 prompt 找出来、<strong>内联</strong>进父 prompt，得到一个「展开后」的成品。两道安全闸不可少：<strong>嵌套深度上限</strong>（<code>MAX_PROMPT_NESTING_DEPTH</code>）和<strong>环检测</strong>（<code>seen</code> 集合），防止 A 依赖 B、B 又依赖 A 把服务拖死。</p>

<div class="fig">
<svg viewBox="0 0 720 195" role="img" aria-label="prompt 依赖解析：父 prompt 引用两个子 prompt，buildAndResolvePromptGraph 沿依赖图把子 prompt 内联进父，得到展开后的完整 prompt；过程有嵌套深度上限和 seen 环检测两道闸；缓存与返回的都是这个 resolved 成品">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">解析：沿依赖图内联，产出一个自包含的成品</text>
  <rect x="30" y="48" width="150" height="100" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="105" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">父 prompt</text><rect x="44" y="78" width="122" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="105" y="94" text-anchor="middle" font-size="6.5" fill="var(--muted)">引用 子A（label）</text><rect x="44" y="108" width="122" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="105" y="124" text-anchor="middle" font-size="6.5" fill="var(--muted)">引用 子B（version）</text>
  <rect x="270" y="60" width="160" height="76" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="350" y="80" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">buildAndResolvePromptGraph</text><text x="350" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">沿图找子 prompt 内联</text><text x="350" y="113" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">闸1 深度上限</text><text x="350" y="126" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">闸2 seen 环检测</text>
  <rect x="520" y="60" width="170" height="76" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="605" y="84" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">resolved prompt</text><text x="605" y="102" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">子片段已全部内联</text><text x="605" y="116" text-anchor="middle" font-size="6.5" fill="var(--muted)">完整、自包含</text><text x="605" y="129" text-anchor="middle" font-size="6.5" fill="var(--faint)">← 缓存/返回的就是它</text>
  <line x1="180" y1="98" x2="268" y2="98" stroke="var(--accent)" stroke-width="1.4"/><polygon points="268,98 259,94 259,102" fill="var(--accent)"/>
  <line x1="430" y1="98" x2="518" y2="98" stroke="var(--teal)" stroke-width="1.5"/><polygon points="518,98 509,94 509,102" fill="var(--teal)"/>
  <text x="360" y="178" text-anchor="middle" font-size="8" fill="var(--faint)">关键事实：一个 resolved prompt 可能横跨好几个 prompt 名字——这正是下一节失效设计要项目级的根因</text>
</svg>
<div class="figcap"><b>解析 = 把组合展开成成品</b>：<code>buildAndResolvePromptGraph</code> 沿第 37 课的依赖图把子 prompt 内联进父，得到 <code>resolvedPrompt</code>；<code>MAX_PROMPT_NESTING_DEPTH</code> 限深、<code>seen</code> 集合防环。<strong>缓存与返回的都是这个展开后的成品</strong>。源码：<code>PromptService/index.ts:132-144,236+</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/PromptService/index.ts</span><span class="ln">解析 + 两道闸</span></div>
  <pre class="code"><span class="cm">// 解析：返回把依赖内联后的成品</span>
<span class="kw">public async</span> <span class="fn">resolvePrompt</span>(prompt) {
  <span class="kw">const</span> promptGraph = <span class="kw">await</span> this.buildAndResolvePromptGraph(...);
  <span class="kw">return</span> { ...prompt, prompt: promptGraph.resolvedPrompt };   <span class="cm">// 子片段已内联</span>
}
<span class="cm">// 沿依赖图递归内联，两道安全闸：</span>
<span class="kw">if</span> (level &gt;= <span class="st">MAX_PROMPT_NESTING_DEPTH</span>) <span class="kw">throw</span> …;   <span class="cm">// 闸1：嵌套太深就停</span>
<span class="kw">const</span> seen = <span class="kw">new</span> Set&lt;string&gt;();                    <span class="cm">// 闸2：记录已访问，A→B→A 立刻识破</span></pre>
</div>

<div class="cols">
  <div class="col"><h4>为什么服务时才解析</h4><p>依赖在数据库里存的是「引用关系」（按 label/version 指向 child）。但 child 的 label 会移动、内容会变——所以只能在<strong>取用的那一刻</strong>才把当前的 child 拉出来内联，得到此刻正确的成品。</p></div>
  <div class="col"><h4>闸 1：深度上限</h4><p><code>MAX_PROMPT_NESTING_DEPTH</code> 限制依赖嵌套层数。防止有人把依赖链拉得过深，导致一次解析要拉几十个 prompt、拖垮服务。</p></div>
  <div class="col"><h4>闸 2：环检测</h4><p><code>seen</code> 集合记录已访问的 prompt。一旦出现 A 依赖 B、B 又依赖 A 的环，立刻识破并报错——否则递归会无限打转。</p></div>
</div>
""")

_ZH38.append(r"""
<h2>epoch 失效：换命名空间，而非逐个删 key</h2>
<p>缓存最难的永远是<strong>失效</strong>：prompt 一改（新版、移 label），旧缓存就得作废。难点在于——一个 resolved prompt 可能<strong>横跨好几个名字</strong>（因为依赖），你根本说不清「该删哪些 key」。Langfuse 的解法漂亮得近乎狡黠：缓存 key 里嵌一个<strong>项目级的 epoch（纪元）令牌</strong>；失效时<strong>不删任何 key</strong>，只是把这个 epoch 令牌<strong>换成一个新随机值</strong>——于是所有旧 key 瞬间「失联」（新读写都用新 epoch、落在新命名空间），旧的放着自然按 TTL 过期。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="epoch 失效：缓存 key 形如 prompt:项目:epoch:名字:版本；prompt 变更时 invalidateCache 把项目级 epoch 令牌从 e1 转成 e2，所有带 e1 的旧 key 不再被读到、按 TTL 自然过期，新读写都落在 e2 命名空间">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">失效 = 转 epoch 令牌（换命名空间），不删 key</text>
  <rect x="40" y="40" width="640" height="30" rx="7" fill="var(--bg)" stroke="var(--accent)"/><text x="360" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">缓存 key 形如：prompt : {projectId} : {epoch} : {promptName} : {version|label}</text>
  <rect x="60" y="92" width="270" height="80" rx="10" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="195" y="112" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">旧 epoch = e1（失联）</text><text x="195" y="132" text-anchor="middle" font-size="6.6" fill="var(--muted)">prompt:proj:e1:greeting:production</text><text x="195" y="148" text-anchor="middle" font-size="6.6" fill="var(--muted)">prompt:proj:e1:refund:production</text><text x="195" y="164" text-anchor="middle" font-size="6.5" fill="var(--faint)">没人再读 → 按 TTL 自然过期</text>
  <rect x="390" y="92" width="270" height="80" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="525" y="112" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">新 epoch = e2（现役）</text><text x="525" y="132" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">prompt:proj:e2:greeting:production</text><text x="525" y="148" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">…新读写都落这里（先 miss 再回填）</text><text x="525" y="164" text-anchor="middle" font-size="6.5" fill="var(--muted)">相当于一整片干净缓存</text>
  <line x1="330" y1="132" x2="388" y2="132" stroke="var(--accent)" stroke-width="2"/><polygon points="388,132 379,128 379,136" fill="var(--accent)"/><text x="359" y="124" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--accent-ink)">转 epoch</text>
  <text x="360" y="194" text-anchor="middle" font-size="8" fill="var(--faint)">epoch 是项目级的（不是 prompt 级）——因为 resolved prompt 跨多名字，任一变更都得让整片缓存翻篇；O(1)，无需扫描/删除</text>
</svg>
<div class="figcap"><b>O(1) 失效，无需扫库删 key</b>：<code>invalidateCache</code> 只对项目级 epoch 键 <code>SET</code> 一个新随机令牌（48 位熵）。旧 epoch 的 key 不再被任何读命中，靠各自 TTL 自然消亡；epoch 键本身 TTL 7 天。<code>getOrCreateEpoch</code> 用 <code>SET NX</code> 处理并发初始化。源码：<code>PromptService/index.ts:179-260</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/PromptService/index.ts</span><span class="ln">epoch 失效 + key</span></div>
  <pre class="code"><span class="cm">// 失效：不删 key，只把项目级 epoch 令牌转成新随机值 → 全部旧 key 失联</span>
<span class="kw">public async</span> <span class="fn">invalidateCache</span>({ projectId }) {
  <span class="kw">await</span> this.redis.set(this.getEpochKey({ projectId }), this.newEpochToken(),
                       <span class="st">"EX"</span>, this.epochTtlSeconds);   <span class="cm">// epoch 键活 7 天</span>
}
<span class="cm">// key 里嵌 epoch：epoch 一变，整片命名空间就翻篇</span>
getCacheKey = `prompt:${projectId}:${epoch}:${promptName}:${version ?? label}`;
<span class="cm">// epoch 项目级（非 prompt 级）：因为 resolved prompt 跨多名字，任一变更都要整体失效</span>
getEpochKey = `prompt_cache_epoch:${projectId}`;</pre>
</div>

<p>这套设计把「失效一片关联复杂的缓存」从一个<strong>难解的精确删除问题</strong>，变成了一次<strong>O(1) 的令牌替换</strong>。代价仅仅是旧 key 在过期前还短暂占着点内存——用一点点内存的浪费，换来失效逻辑的<strong>极致简单与正确</strong>。这是分布式缓存里一个非常值得收进工具箱的招式。</p>

<table class="t">
  <thead><tr><th>对比</th><th>逐个删 key（朴素做法）</th><th>转 epoch（Langfuse）</th></tr></thead>
  <tbody>
    <tr><td>失效复杂度</td><td>需找出所有受影响 key，O(N) 且要扫描</td><td>SET 一个新令牌，O(1)</td></tr>
    <tr><td>依赖追踪</td><td>必须反查「哪些 resolved 成品含此 child」</td><td>完全不必——整片命名空间翻篇</td></tr>
    <tr><td>漏删风险</td><td>漏一个就有人读到陈旧 prompt</td><td>不可能漏，旧 key 一律失联</td></tr>
    <tr><td>代价</td><td>逻辑复杂、易错</td><td>旧 key 过期前占点内存（自动消亡）</td></tr>
  </tbody>
</table>
""")

# (L38 spark+key below)

_ZH38.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么用「转 epoch」失效，而不是老老实实把旧 key 删掉？</strong> 因为<strong>精确删除在这里几乎不可行</strong>。一个被服务的 prompt 是<strong>解析后的成品</strong>，可能内联了好几个别的 prompt（第 37 课依赖）。当你改动其中任意一个 child，所有<strong>间接依赖它的 resolved 成品</strong>都该失效——但你很难反查「到底哪些 key 受了牵连」，更别说它们还散落在不同名字下。「逐个找出来删」既慢又容易漏，漏一个就意味着<strong>有人读到了陈旧的 prompt</strong>。转 epoch 把这个难题一刀斩断：<strong>不去找、不去删，直接换一片新命名空间</strong>，旧的全部作废、自然过期。失效从此是 O(1) 的、绝不漏的。代价是旧 key 过期前的一点内存浪费——这是教科书级的「<strong>用空间换正确性与简单性</strong>」。<br><br>
  <strong>为什么 epoch 是「项目级」而不是「prompt 级」？</strong> 正是上面那个原因的直接推论。如果 epoch 按单个 prompt 名字隔离，那改 child prompt 时，你又得去想「哪些 parent 依赖了它、要不要也转它们的 epoch」——依赖追踪的难题原地复活。把 epoch 放在<strong>项目这个粒度</strong>，意味着「这个项目里任何一个 prompt 有变动，整个项目的 prompt 缓存就翻篇」。粒度粗了点、偶尔会多失效一些本可保留的缓存，但换来的是<strong>彻底不必追踪依赖关系</strong>的确定性。在「失效少一点」和「永不读到陈旧数据」之间，它果断选了后者——对 prompt 这种<strong>正确性远比缓存命中率重要</strong>的数据，这个取舍无比正确。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>prompt 服务必须快</strong>：生产可能每次 LLM 调用都取 prompt，直接打 Postgres 太慢太重，故 <code>PromptService</code> 用 Redis 缓存挡在前面。</li>
    <li><strong>read-through 缓存</strong>：<code>getPrompt</code> 先查 Redis、命中即返回；未命中回 Postgres 再回填 Redis（<code>SET EX ttl</code>）。开关 <code>LANGFUSE_CACHE_PROMPT_ENABLED</code>、时长 <code>..._TTL_SECONDS</code>。</li>
    <li><strong>服务时解析依赖</strong>：<code>buildAndResolvePromptGraph</code> 把被引用的子 prompt 内联成自包含成品，带<strong>深度上限 + seen 环检测</strong>两道闸；缓存/返回的都是这个 resolved 成品。</li>
    <li><strong>epoch 失效（招式精髓）</strong>：缓存 key 嵌项目级 epoch 令牌；失效时<strong>不删 key</strong>，只把令牌转成新随机值——旧 key 全部失联、按 TTL 自然过期。O(1)、绝不漏、无需扫描。</li>
    <li><strong>epoch 项目级的根因</strong>：resolved prompt 跨多名字，精确删除/prompt 级隔离都要追踪依赖；项目级 epoch 用「多失效一点」换「彻底不必追踪 + 永不读到陈旧」——对 prompt 这种正确性优先的数据是正确取舍。</li>
  </ul>
</div>
""")

_EN38.append(r"""
<p class="lead">
The last lesson let you <strong>manage</strong> prompts safely. But production has a real problem: an app may <strong>fetch a prompt before every single LLM call</strong> ("give me the production one"). Hitting Postgres each time is slow and crushes the database. This lesson is about how <strong>PromptService</strong> uses Redis to make prompt serving fast and steady, focusing on two mechanisms: the classic <strong>read-through cache</strong>, and an exceptionally elegant <strong>"swap the namespace, don't delete keys one by one"</strong> epoch invalidation strategy.
Along the way we'll see Lesson 37's dependencies' "second half": referenced child prompts are <strong>resolved and inlined</strong> into one complete prompt at serving time—and it's precisely this fact, "one prompt may span multiple names", that forces the clever invalidation design.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Prompt serving is like a library's <strong>popular-books fast-access shelf</strong>. A reader (the app) comes to borrow a book (prompt); the librarian first checks the <strong>fast shelf</strong> (Redis): if it's there, <strong>hand it over instantly</strong>; if not, run to the <strong>main stacks</strong> (Postgres) to fetch one and drop a copy on the fast shelf, so the next person is quick.
  Then the hard part: a book gets a <strong>new edition</strong>—how do you stop everyone from still borrowing the old one? Combing the whole shelf to pull old editions one by one is <strong>too hard</strong>—besides, one book may have <strong>chapters of other books tucked inside</strong> (Lesson 37's dependencies), so one change ripples everywhere. The library's trick: hang a <strong>new "edition tag"</strong> on the entire fast shelf. Books under the old tag are <strong>no longer recognized</strong> (the rule only honors the current tag); they needn't be cleaned, just left to expire; and every new borrow goes through the <strong>shelf with the new tag</strong>. <strong>Swapping a tag is far faster and steadier than pulling books one by one.</strong>
</div>
""")

_EN38.append(r"""
<h2>The read-through cache: ask Redis first, fall back to the DB</h2>
<p>The core method is <code>PromptService.getPrompt</code>, a textbook <strong>read-through</strong> cache: check Redis first, return on a hit; only on a <strong>miss</strong> go back to Postgres (<code>findPrompt</code>), and after fetching, <strong>write it into Redis</strong> (with a TTL), so the next identical request hits the cache. Whether the cache is on is controlled by <code>LANGFUSE_CACHE_PROMPT_ENABLED</code>, and how long each entry lives by <code>LANGFUSE_CACHE_PROMPT_TTL_SECONDS</code>.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="Read-through cache flow: the app requests the production prompt, PromptService checks Redis first, returning instantly on a hit; on a miss it queries Postgres, writes the result into Redis (with TTL) and returns, so the next identical request hits">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">read-through: hit takes the shortcut, miss falls back and backfills</text>
  <rect x="30" y="86" width="130" height="48" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="95" y="106" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">app</text><text x="95" y="122" text-anchor="middle" font-size="6.6" fill="var(--muted)">getPrompt(production)</text>
  <rect x="220" y="80" width="150" height="60" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="295" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">PromptService</text><text x="295" y="117" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">① check Redis first</text><text x="295" y="129" text-anchor="middle" font-size="6.4" fill="var(--muted)">hit→return</text>
  <rect x="430" y="40" width="150" height="48" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="505" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Redis cache</text><text x="505" y="76" text-anchor="middle" font-size="6.4" fill="var(--muted)">millisecond · with TTL</text>
  <rect x="430" y="130" width="150" height="48" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="505" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">Postgres (authority)</text><text x="505" y="166" text-anchor="middle" font-size="6.4" fill="var(--muted)">queried only on a miss</text>
  <line x1="160" y1="110" x2="218" y2="110" stroke="var(--blue)" stroke-width="1.5"/><polygon points="218,110 209,106 209,114" fill="var(--blue)"/>
  <line x1="370" y1="95" x2="428" y2="70" stroke="var(--accent)" stroke-width="1.5"/><polygon points="428,70 419,69 421,77" fill="var(--accent)"/><text x="399" y="78" text-anchor="middle" font-size="6" fill="var(--accent-ink)">① hit</text>
  <line x1="370" y1="120" x2="428" y2="150" stroke="var(--teal)" stroke-width="1.3" stroke-dasharray="3 2"/><polygon points="428,150 419,148 421,156" fill="var(--teal)"/><text x="396" y="142" text-anchor="middle" font-size="6" fill="var(--teal)">② miss→DB</text>
  <path d="M 505 130 Q 560 110 580 90" fill="none" stroke="var(--accent)" stroke-width="1.3" stroke-dasharray="4 3"/><polygon points="580,90 572,95 578,98" fill="var(--accent)"/><text x="600" y="112" text-anchor="middle" font-size="6" fill="var(--accent-ink)">③ backfill Redis</text>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">the vast majority of requests take ① (millisecond, no DB); only the first after a cold/invalidated cache takes ②③—DB load is shielded behind the cache</text>
</svg>
<div class="figcap"><b>read-through + backfill</b>: <code>getPrompt</code> first <code>getCachedPrompt</code>, returns on a hit; on a miss runs <code>findPrompt</code> (DB) then <code>cachePrompt</code> (<code>redis.set(key, value, "EX", ttlSeconds)</code>). Toggle <code>LANGFUSE_CACHE_PROMPT_ENABLED</code>, duration <code>LANGFUSE_CACHE_PROMPT_TTL_SECONDS</code>. Source: <code>PromptService/index.ts:49-86,166-173</code>.</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 212" role="img" aria-label="Cache hit vs miss latency real example: a hit goes to Redis in about 1 ms and returns instantly, a miss must query Postgres then backfill Redis in about 25 ms, roughly 25x slower; steady-state hit rate about 98%; TTL 3600 seconds, epoch rotation invalidates instantly. Latencies and hit rate illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: cache hit vs miss latency</text>
  <text x="20" y="56" font-size="8.5" font-weight="700" fill="var(--accent-ink)">cache HIT</text><text x="20" y="68" font-size="7" fill="var(--muted)">Redis</text>
  <rect x="210" y="46" width="18" height="22" rx="4" fill="var(--accent)" opacity="0.85"/><text x="236" y="61" font-size="8" font-weight="700" fill="var(--accent-ink)">~1 ms · instant</text>
  <text x="20" y="98" font-size="8.5" font-weight="700" fill="var(--amber)">cache MISS</text><text x="20" y="110" font-size="7" fill="var(--muted)">PG+backfill</text>
  <rect x="210" y="88" width="460" height="22" rx="4" fill="var(--amber)" opacity="0.8"/><text x="678" y="103" font-size="8" font-weight="700" fill="var(--amber)">~25 ms</text>
  <rect x="210" y="120" width="150" height="20" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="285" y="134" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">≈ 25× faster</text>
  <text x="20" y="166" font-size="8" font-weight="700" fill="var(--ink)">hit rate</text>
  <rect x="210" y="156" width="460" height="16" rx="8" fill="var(--panel-2)"/><rect x="210" y="156" width="451" height="16" rx="8" fill="var(--accent)" opacity="0.55"/><text x="676" y="168" font-size="8" font-weight="700" fill="var(--accent-ink)">≈ 98%</text>
  <line x1="20" y1="184" x2="700" y2="184" stroke="var(--line)"/>
  <text x="20" y="200" font-size="7.4" fill="var(--muted)">TTL 3600s (1h, LANGFUSE_CACHE_PROMPT_TTL_SECONDS) · change a prompt → rotate the project epoch → old keys invalidate instantly, no per-key delete</text>
</svg>
<div class="figcap"><b>The cache turns "hit the DB every time" into "almost never"</b> (latency/hit-rate <b>illustrative</b>; mechanism from <code>PromptService</code>): a hit returns from Redis in about <code>1ms</code>, only a miss queries Postgres and backfills at about <code>25ms</code> — roughly <b>25x</b>. A high steady-state hit rate (≈98% here) means <b>the vast majority of prompt fetches never touch the database</b>. Two safeguards: <code>TTL 3600s</code> as a backstop, and <b>rotating the project epoch</b> on a prompt change to invalidate old keys instantly (the concrete payoff of the epoch figure above).</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/PromptService/index.ts</span><span class="ln">getPrompt read-through</span></div>
  <pre class="code"><span class="kw">public async</span> <span class="fn">getPrompt</span>(params): Promise&lt;PromptResult | null&gt; {
  <span class="kw">if</span> (this.cacheEnabled) {
    <span class="kw">const</span> cachedPrompt = <span class="kw">await</span> this.getCachedPrompt(params);   <span class="cm">// ① ask Redis first</span>
    <span class="kw">if</span> (cachedPrompt) <span class="kw">return</span> cachedPrompt;                     <span class="cm">// hit → return instantly, no DB</span>
  }
  <span class="kw">const</span> dbPrompt = <span class="kw">await</span> this.findPrompt(params);              <span class="cm">// ② miss → query Postgres</span>
  <span class="kw">if</span> (this.cacheEnabled &amp;&amp; dbPrompt)
    <span class="kw">await</span> this.cachePrompt({ ...params, prompt: dbPrompt });    <span class="cm">// ③ backfill Redis (with TTL)</span>
  <span class="kw">return</span> dbPrompt;
}
<span class="cm">// cachePrompt: redis.set(key, value, "EX", this.ttlSeconds)  — every entry self-expires</span></pre>
</div>

<table class="t">
  <thead><tr><th>case</th><th>which path</th><th>latency</th><th>touches Postgres?</th></tr></thead>
  <tbody>
    <tr><td><b>cache hit</b> (vast majority)</td><td>Redis returns directly</td><td>milliseconds</td><td>no</td></tr>
    <tr><td><b>cache miss</b> (cold/just invalidated)</td><td>query DB → backfill Redis → return</td><td>one DB round-trip</td><td>yes (only this one)</td></tr>
    <tr><td><b>TTL expiry</b></td><td>next read becomes a miss, auto-backfills</td><td>same, single request</td><td>yes (single)</td></tr>
  </tbody>
</table>
<p>In a phrase: <strong>the database only bears "the first request", then Redis catches them all</strong>. That's the value of read-through—amortizing a "read on every call" high-frequency access into "one DB read per TTL period".</p>
""")

# (en sec2/3/spark below)

_EN38.append(r"""
<h2>Resolution: inline dependencies into one complete prompt</h2>
<p>Lesson 37 said prompts can reference other prompts. But what the app ultimately gets must be a <strong>complete, self-contained</strong> prompt—the runtime can't be left to assemble the referenced snippets on the fly. So serving includes a <strong>resolve</strong> step: <code>buildAndResolvePromptGraph</code> walks the dependency graph, finds each referenced child, and <strong>inlines</strong> it into the parent, producing an "expanded" finished product. Two safety gates are essential: a <strong>nesting depth cap</strong> (<code>MAX_PROMPT_NESTING_DEPTH</code>) and <strong>cycle detection</strong> (a <code>seen</code> set), preventing A-depends-on-B-depends-on-A from hanging the service.</p>

<div class="fig">
<svg viewBox="0 0 720 195" role="img" aria-label="Prompt dependency resolution: a parent prompt references two children, buildAndResolvePromptGraph walks the graph and inlines the children into the parent, producing an expanded complete prompt; the process has a nesting depth cap and a seen cycle check; what is cached and returned is this resolved product">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">resolve: inline along the graph, produce a self-contained product</text>
  <rect x="30" y="48" width="150" height="100" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="105" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">parent prompt</text><rect x="44" y="78" width="122" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="105" y="94" text-anchor="middle" font-size="6.2" fill="var(--muted)">refs child A (label)</text><rect x="44" y="108" width="122" height="24" rx="5" fill="var(--bg)" stroke="var(--faint)"/><text x="105" y="124" text-anchor="middle" font-size="6.2" fill="var(--muted)">refs child B (version)</text>
  <rect x="270" y="60" width="160" height="76" rx="9" fill="var(--bg)" stroke="var(--teal)" stroke-width="2"/><text x="350" y="80" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">buildAndResolvePromptGraph</text><text x="350" y="98" text-anchor="middle" font-size="6.6" fill="var(--muted)">walk graph, inline children</text><text x="350" y="113" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">gate1 depth cap</text><text x="350" y="126" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">gate2 seen cycle check</text>
  <rect x="520" y="60" width="170" height="76" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="605" y="84" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">resolved prompt</text><text x="605" y="102" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">all child snippets inlined</text><text x="605" y="116" text-anchor="middle" font-size="6.4" fill="var(--muted)">complete, self-contained</text><text x="605" y="129" text-anchor="middle" font-size="6.2" fill="var(--faint)">← this is what's cached/returned</text>
  <line x1="180" y1="98" x2="268" y2="98" stroke="var(--accent)" stroke-width="1.4"/><polygon points="268,98 259,94 259,102" fill="var(--accent)"/>
  <line x1="430" y1="98" x2="518" y2="98" stroke="var(--teal)" stroke-width="1.5"/><polygon points="518,98 509,94 509,102" fill="var(--teal)"/>
  <text x="360" y="178" text-anchor="middle" font-size="8" fill="var(--faint)">key fact: a resolved prompt may span several prompt names—the very reason the next section's invalidation is project-scoped</text>
</svg>
<div class="figcap"><b>resolution = expand composition into a product</b>: <code>buildAndResolvePromptGraph</code> walks Lesson 37's dependency graph, inlining children into the parent to get <code>resolvedPrompt</code>; <code>MAX_PROMPT_NESTING_DEPTH</code> caps depth, a <code>seen</code> set blocks cycles. <strong>What's cached and returned is this expanded product</strong>. Source: <code>PromptService/index.ts:132-144,236+</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/PromptService/index.ts</span><span class="ln">resolve + two gates</span></div>
  <pre class="code"><span class="cm">// resolve: return the product with dependencies inlined</span>
<span class="kw">public async</span> <span class="fn">resolvePrompt</span>(prompt) {
  <span class="kw">const</span> promptGraph = <span class="kw">await</span> this.buildAndResolvePromptGraph(...);
  <span class="kw">return</span> { ...prompt, prompt: promptGraph.resolvedPrompt };   <span class="cm">// children inlined</span>
}
<span class="cm">// recursively inline along the graph, two safety gates:</span>
<span class="kw">if</span> (level &gt;= <span class="st">MAX_PROMPT_NESTING_DEPTH</span>) <span class="kw">throw</span> …;   <span class="cm">// gate1: stop if nesting too deep</span>
<span class="kw">const</span> seen = <span class="kw">new</span> Set&lt;string&gt;();                    <span class="cm">// gate2: track visited, catch A→B→A instantly</span></pre>
</div>

<div class="cols">
  <div class="col"><h4>why resolve at serving time</h4><p>Dependencies are stored in the DB as "reference relations" (pointing to a child by label/version). But a child's label moves and its content changes—so only at <strong>the moment of fetching</strong> can you pull the current child and inline it, getting the product correct as of now.</p></div>
  <div class="col"><h4>gate 1: depth cap</h4><p><code>MAX_PROMPT_NESTING_DEPTH</code> limits dependency nesting levels. It prevents someone from making the chain so deep that one resolution pulls dozens of prompts and drags down the service.</p></div>
  <div class="col"><h4>gate 2: cycle detection</h4><p>The <code>seen</code> set records visited prompts. The instant a cycle appears—A depends on B, B depends on A—it's caught and errors out; otherwise the recursion spins forever.</p></div>
</div>
""")

_EN38.append(r"""
<h2>Epoch invalidation: swap the namespace, don't delete keys one by one</h2>
<p>The hardest part of caching is always <strong>invalidation</strong>: when a prompt changes (new version, label move), the old cache must be voided. The difficulty—a resolved prompt may <strong>span several names</strong> (via dependencies), so you can't even say "which keys to delete". Langfuse's solution is elegant to the point of slyness: embed a <strong>project-scoped epoch token</strong> in the cache key; to invalidate, <strong>delete no keys</strong>, just rotate that epoch token to <strong>a new random value</strong>—so all old keys are instantly "orphaned" (new reads/writes use the new epoch in a new namespace), and the old ones simply expire by TTL.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="Epoch invalidation: a cache key looks like prompt:project:epoch:name:version; on a prompt change invalidateCache rotates the project-scoped epoch token from e1 to e2, so all old e1 keys are no longer read and expire by TTL, while new reads/writes land in the e2 namespace">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">invalidate = rotate the epoch token (swap namespace), delete no keys</text>
  <rect x="40" y="40" width="640" height="30" rx="7" fill="var(--bg)" stroke="var(--accent)"/><text x="360" y="60" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">cache key looks like: prompt : {projectId} : {epoch} : {promptName} : {version|label}</text>
  <rect x="60" y="92" width="270" height="80" rx="10" fill="var(--bg)" stroke="var(--faint)" stroke-dasharray="4 3"/><text x="195" y="112" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--muted)">old epoch = e1 (orphaned)</text><text x="195" y="132" text-anchor="middle" font-size="6.4" fill="var(--muted)">prompt:proj:e1:greeting:production</text><text x="195" y="148" text-anchor="middle" font-size="6.4" fill="var(--muted)">prompt:proj:e1:refund:production</text><text x="195" y="164" text-anchor="middle" font-size="6.4" fill="var(--faint)">no one reads them → expire by TTL</text>
  <rect x="390" y="92" width="270" height="80" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="525" y="112" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">new epoch = e2 (active)</text><text x="525" y="132" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">prompt:proj:e2:greeting:production</text><text x="525" y="148" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">…new reads/writes land here (miss then backfill)</text><text x="525" y="164" text-anchor="middle" font-size="6.4" fill="var(--muted)">effectively a clean cache</text>
  <line x1="330" y1="132" x2="388" y2="132" stroke="var(--accent)" stroke-width="2"/><polygon points="388,132 379,128 379,136" fill="var(--accent)"/><text x="359" y="124" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--accent-ink)">rotate epoch</text>
  <text x="360" y="194" text-anchor="middle" font-size="8" fill="var(--faint)">the epoch is project-scoped (not prompt-scoped)—because a resolved prompt spans names, any change must turn the whole page; O(1), no scan/delete</text>
</svg>
<div class="figcap"><b>O(1) invalidation, no scan-and-delete</b>: <code>invalidateCache</code> just <code>SET</code>s a new random token (48 bits of entropy) on the project-scoped epoch key. Keys under the old epoch are no longer hit by any read and die off by their own TTL; the epoch key itself has a 7-day TTL. <code>getOrCreateEpoch</code> uses <code>SET NX</code> for concurrent initialization. Source: <code>PromptService/index.ts:179-260</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/services/PromptService/index.ts</span><span class="ln">epoch invalidation + key</span></div>
  <pre class="code"><span class="cm">// invalidate: delete no keys, just rotate the project-scoped epoch token → all old keys orphaned</span>
<span class="kw">public async</span> <span class="fn">invalidateCache</span>({ projectId }) {
  <span class="kw">await</span> this.redis.set(this.getEpochKey({ projectId }), this.newEpochToken(),
                       <span class="st">"EX"</span>, this.epochTtlSeconds);   <span class="cm">// epoch key lives 7 days</span>
}
<span class="cm">// embed epoch in the key: change the epoch and the whole namespace turns the page</span>
getCacheKey = `prompt:${projectId}:${epoch}:${promptName}:${version ?? label}`;
<span class="cm">// epoch project-scoped (not prompt-scoped): a resolved prompt spans names, so any change invalidates all</span>
getEpochKey = `prompt_cache_epoch:${projectId}`;</pre>
</div>

<p>This design turns "invalidating a tangle of related caches" from an <strong>intractable precise-deletion problem</strong> into an <strong>O(1) token swap</strong>. The only cost is old keys briefly occupying a little memory until they expire—trading a touch of wasted memory for invalidation logic that is <strong>maximally simple and correct</strong>. It's a distributed-caching move well worth adding to your toolbox.</p>

<table class="t">
  <thead><tr><th>comparison</th><th>delete keys one by one (naive)</th><th>rotate epoch (Langfuse)</th></tr></thead>
  <tbody>
    <tr><td>invalidation complexity</td><td>find all affected keys, O(N) with a scan</td><td>SET one new token, O(1)</td></tr>
    <tr><td>dependency tracking</td><td>must reverse-lookup "which resolved products contain this child"</td><td>none needed—the whole namespace turns the page</td></tr>
    <tr><td>miss risk</td><td>one miss serves a stale prompt</td><td>impossible to miss, all old keys orphaned</td></tr>
    <tr><td>cost</td><td>complex, error-prone logic</td><td>old keys hold a little memory until expiry (auto-die)</td></tr>
  </tbody>
</table>
""")

_EN38.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why invalidate by "rotating the epoch" rather than dutifully deleting the old keys?</strong> Because <strong>precise deletion is nearly infeasible here</strong>. A served prompt is a <strong>resolved product</strong> that may inline several other prompts (Lesson 37 dependencies). When you change any one child, all <strong>resolved products that indirectly depend on it</strong> should be invalidated—but you can barely reverse-lookup "which keys are affected", let alone the fact that they're scattered across different names. "Find them one by one and delete" is slow and miss-prone, and one miss means <strong>someone reads a stale prompt</strong>. Rotating the epoch cuts the knot: <strong>don't search, don't delete, just swap to a fresh namespace</strong>; the old ones are all voided and expire naturally. Invalidation is now O(1) and never misses. The cost is a little wasted memory before old keys expire—a textbook "<strong>trade space for correctness and simplicity</strong>".<br><br>
  <strong>Why is the epoch "project-scoped" rather than "prompt-scoped"?</strong> A direct corollary of the above. If the epoch were isolated per prompt name, then on changing a child prompt you'd again have to figure out "which parents depend on it, and should I rotate their epochs too"—the dependency-tracking problem reborn. Putting the epoch at <strong>project granularity</strong> means "any prompt change in this project turns the page on the whole project's prompt cache". A bit coarse—occasionally invalidating caches that could have been kept—but it buys the certainty of <strong>never needing to track dependencies at all</strong>. Between "invalidate a little less" and "never read stale data", it firmly chooses the latter—exactly right for prompts, where <strong>correctness matters far more than cache hit rate</strong>.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Prompt serving must be fast</strong>: production may fetch a prompt on every LLM call; hitting Postgres directly is too slow and heavy, so <code>PromptService</code> puts a Redis cache in front.</li>
    <li><strong>Read-through cache</strong>: <code>getPrompt</code> checks Redis first, returns on a hit; on a miss falls back to Postgres then backfills Redis (<code>SET EX ttl</code>). Toggle <code>LANGFUSE_CACHE_PROMPT_ENABLED</code>, duration <code>..._TTL_SECONDS</code>.</li>
    <li><strong>Resolve dependencies at serving time</strong>: <code>buildAndResolvePromptGraph</code> inlines referenced children into a self-contained product, with a <strong>depth cap + seen cycle check</strong>; what's cached/returned is this resolved product.</li>
    <li><strong>Epoch invalidation (the gem)</strong>: the cache key embeds a project-scoped epoch token; to invalidate, <strong>delete no keys</strong>, just rotate the token to a new random value—all old keys orphaned, expiring by TTL. O(1), never misses, no scan.</li>
    <li><strong>Why epoch is project-scoped</strong>: a resolved prompt spans names, so precise deletion / prompt-scoped isolation would require dependency tracking; project-scoped epoch trades "a little over-invalidation" for "no tracking + never stale"—the right call for correctness-first data like prompts.</li>
  </ul>
</div>
""")

LESSON_38 = {"zh": "\n".join(_ZH38), "en": "\n".join(_EN38)}


# ══════════════════════════════════════════════════════════════════════
# L39 · Playground 与 LLM 连接（加密·schema·tool） / Playground & LLM connections
# ══════════════════════════════════════════════════════════════════════
_ZH39 = []
_EN39 = []

_ZH39.append(r"""
<p class="lead">
这一课收尾 Part 7，也收尾整条「开发者工作流」弧线。<strong>Playground（游乐场）</strong>是你<strong>交互式试 prompt</strong> 的地方——敲几句消息、选个模型、点运行、看回复，满意了再去版本化（第 37 课）、跑实验（第 36 课）。但要让任何<strong>服务端 LLM 调用</strong>成真，背后得先有两样东西：一个<strong>安全存好的 LLM 连接</strong>（你的 provider 凭证），以及一批定义好的<strong>结构化输出 schema 与工具</strong>。
这一课讲它们，重点落在一个绕不开的安全话题：provider 的 API key 是<strong>能花你真金白银</strong>的「皇冠明珠」，Langfuse 怎么把它<strong>加密</strong>着存、又在该用的那一刻安全地取出来用。你还会看到一个贯穿全书的收束：Playground、评估（第 29 课）、实验（第 36 课）<strong>共用同一套 LLM 调用引擎</strong>。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  Playground 像一台「<strong>驾驶模拟器 + 钥匙保险柜</strong>」。<strong>模拟器</strong>（playground）让你在正式上路（版本化、上线）之前反复<strong>试驾</strong>（试 prompt）——而且用的就是真车的<strong>同一台引擎</strong>（和评估、实验同一套 <code>fetchLLMCompletion</code>），所以模拟里跑顺了，上路也跑得顺。
  可发动引擎得用<strong>钥匙</strong>（provider 的 API key）。这把钥匙太值钱了——谁拿到都能开你的车、花你的油钱，所以它被<strong>锁进保险柜</strong>（AES 加密存储）。平时柜子只在表面露出钥匙串<strong>末尾几位</strong>（<code>displaySecretKey</code>）供你辨认是哪把，<strong>真要发动的那一刻</strong>才把真钥匙取出来（解密）插进引擎。<strong>钥匙从不在外面裸放，只在点火的瞬间现身。</strong>
</div>
""")

# (L39 sections below)

_ZH39.append(r"""
<h2>一台引擎，三个消费者</h2>
<p>Playground 看着像个独立的小工具，底下却<strong>复用了和评估、实验完全相同的 LLM 调用核心</strong>——<code>fetchLLMCompletion</code>。它的 <code>chatCompletionHandler</code> 把你在界面上敲的消息、选的模型、配的 <code>tools</code> 和 <code>structuredOutputSchema</code> 一并交给这个核心。于是第 29 课的裁判、第 36 课的实验、和这里的 Playground，本质上是<strong>同一台引擎的三个消费者</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="一台 LLM 引擎三个消费者：Playground 的交互试验、第29课的 LLM 裁判、第36课的 prompt 实验，都调用同一个 fetchLLMCompletion 核心，再由它带着解密后的凭证去调各家 provider">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">同一套 fetchLLMCompletion，被三处共用</text>
  <rect x="30" y="44" width="180" height="40" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="120" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Playground（本课）</text><text x="120" y="76" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">交互试 prompt</text>
  <rect x="30" y="92" width="180" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="120" y="110" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">LLM 裁判（第29课）</text><text x="120" y="124" text-anchor="middle" font-size="6.6" fill="var(--muted)">结构化输出评分</text>
  <rect x="30" y="140" width="180" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="120" y="158" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">prompt 实验（第36课）</text><text x="120" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">逐题跑 prompt</text>
  <rect x="290" y="84" width="170" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="375" y="106" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">fetchLLMCompletion</text><text x="375" y="124" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">统一的 LLM 调用核心</text>
  <rect x="540" y="60" width="150" height="34" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="615" y="81" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">OpenAI</text>
  <rect x="540" y="100" width="150" height="34" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="615" y="121" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">Anthropic</text>
  <rect x="540" y="140" width="150" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="615" y="161" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--muted)">…（按 adapter）</text>
  <line x1="210" y1="64" x2="288" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="288,100 279,96 280,104" fill="var(--accent)"/>
  <line x1="210" y1="112" x2="288" y2="112" stroke="var(--blue)" stroke-width="1.4"/><polygon points="288,112 279,108 279,116" fill="var(--blue)"/>
  <line x1="210" y1="160" x2="288" y2="124" stroke="var(--blue)" stroke-width="1.4"/><polygon points="288,124 280,128 279,120" fill="var(--blue)"/>
  <line x1="460" y1="104" x2="538" y2="80" stroke="var(--teal)" stroke-width="1.3"/><line x1="460" y1="112" x2="538" y2="116" stroke="var(--teal)" stroke-width="1.3"/><line x1="460" y1="120" x2="538" y2="152" stroke="var(--faint)" stroke-width="1.2"/>
  <text x="360" y="198" text-anchor="middle" font-size="8" fill="var(--faint)">一台引擎统一封装：凭证解密、provider 适配、结构化输出、工具调用、流式——三处复用，不重复造轮子</text>
</svg>
<div class="figcap"><b>一个核心，三处复用</b>：<code>web/src/features/playground/server/chatCompletionHandler.ts:19,69-86</code> 直接调 <code>fetchLLMCompletion</code>，传入 <code>tools</code> 与 <code>structuredOutputSchema</code>。这与第 29 课裁判的 <code>callLLM</code>、第 36 课实验的模型调用，<b>底层是同一台引擎</b>——凭证解密、provider 适配都只写一遍。</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 222" role="img" aria-label="Playground 请求真实例子：左边是 LlmApiKeys 连接（provider=openai、adapter=openai、displaySecretKey 掩码 sk…a1b2、secretKey 以 AES-256-GCM 加密），右边是请求参数（model=gpt-4o、temperature=0.2、maxTokens=512、system+user 消息）；两者汇入 fetchLLMCompletion，调用前一刻才解密凭证，返回内容与 usage。字段取自 LlmApiKeys 模型，值为示例">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">示例：一次 Playground 请求</text>
  <rect x="18" y="32" width="330" height="126" rx="9" fill="var(--bg)" stroke="var(--blue)"/>
  <text x="32" y="50" font-size="8.5" font-weight="700" fill="var(--blue)">LLM connection · LlmApiKeys</text>
  <text x="32" y="68" font-size="7.6" fill="var(--muted)">provider</text><text x="170" y="68" font-size="7.6" font-family="monospace" fill="var(--ink)">openai</text>
  <text x="32" y="86" font-size="7.6" fill="var(--muted)">adapter</text><text x="170" y="86" font-size="7.6" font-family="monospace" fill="var(--ink)">openai</text>
  <text x="32" y="104" font-size="7.6" fill="var(--muted)">displaySecretKey</text><text x="170" y="104" font-size="7.6" font-family="monospace" fill="var(--ink)">sk-…a1b2</text>
  <text x="32" y="122" font-size="7.6" fill="var(--muted)">baseURL</text><text x="170" y="122" font-size="7.6" font-family="monospace" fill="var(--ink)">（默认）</text>
  <rect x="30" y="138" width="306" height="14" rx="7" fill="var(--amber-soft)"/><text x="36" y="148" font-size="6.6" fill="var(--amber)">🔒 secretKey: AES-256-GCM 加密存储，调用前一刻才解密</text>
  <rect x="360" y="32" width="342" height="126" rx="9" fill="var(--bg)" stroke="var(--accent)"/>
  <text x="374" y="50" font-size="8.5" font-weight="700" fill="var(--accent-ink)">请求参数</text>
  <text x="374" y="68" font-size="7.6" fill="var(--muted)">model</text><text x="500" y="68" font-size="7.6" font-family="monospace" fill="var(--ink)">gpt-4o</text>
  <text x="374" y="86" font-size="7.6" fill="var(--muted)">temperature</text><text x="500" y="86" font-size="7.6" font-family="monospace" fill="var(--ink)">0.2</text>
  <text x="374" y="104" font-size="7.6" fill="var(--muted)">maxTokens</text><text x="500" y="104" font-size="7.6" font-family="monospace" fill="var(--ink)">512</text>
  <rect x="372" y="120" width="318" height="32" rx="6" fill="var(--code-bg)"/><text x="380" y="133" font-size="6.8" font-family="monospace" fill="var(--code-ink)">messages: [{role:&quot;system&quot;, …},</text><text x="380" y="146" font-size="6.8" font-family="monospace" fill="var(--code-ink)">  {role:&quot;user&quot;, content:&quot;退款？&quot;}]</text>
  <path d="M360 175 L300 175 L300 185 L420 185" fill="none" stroke="var(--line)" stroke-width="1.4"/>
  <rect x="250" y="170" width="220" height="28" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="360" y="188" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">fetchLLMCompletion()</text>
  <text x="360" y="212" text-anchor="middle" font-size="7.4" fill="var(--muted)">同一引擎也被第29课裁判、第36课实验复用——连接定义一次，处处可用</text>
  <rect x="490" y="170" width="212" height="28" rx="8" fill="var(--panel-2)" stroke="var(--accent)"/><text x="500" y="183" font-size="6.8" font-family="monospace" fill="var(--ink)">→ { content:&quot;30 days…&quot;,</text><text x="500" y="194" font-size="6.8" font-family="monospace" fill="var(--muted)">     usage:{ in:42,out:18 } }</text>
</svg>
<div class="figcap"><b>Playground 就是把「连接 + 参数」喂给统一引擎</b>（字段取自 <code>LlmApiKeys</code> 模型；<b>值为示例</b>）：左边的<b>连接</b>来自 <code>LlmApiKeys</code>——<code>provider</code>/<code>adapter</code> 选定接口，<code>secretKey</code> 以 <code>AES-256-GCM</code> 加密落库、只在调用前一刻解密，UI 只看得到掩码的 <code>displaySecretKey</code>；右边是<b>请求参数</b>（<code>model</code>/<code>temperature</code>/<code>maxTokens</code> + 消息）。两者汇入 <code>fetchLLMCompletion()</code>——<b>同一个引擎</b>也被第 29 课的裁判、第 36 课的实验复用。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/playground/server/chatCompletionHandler.ts</span><span class="ln">Playground 调同一核心</span></div>
  <pre class="code"><span class="kw">import</span> { fetchLLMCompletion } <span class="kw">from</span> <span class="st">"@langfuse/shared/src/server"</span>;   <span class="cm">// 和评估/实验同一个</span>

<span class="kw">const</span> fetchLLMCompletionParams = { messages, modelParams, <span class="cm">/* 你在界面配的 */</span>
  tools,                  <span class="cm">// 来自 LlmTool（函数调用定义）</span>
  structuredOutputSchema  <span class="cm">// 来自 LlmSchema（结构化输出，呼应第29课）</span>
};
<span class="kw">if</span> (structuredOutputSchema) {
  <span class="kw">const</span> result = <span class="kw">await</span> fetchLLMCompletion({ ...fetchLLMCompletionParams, structuredOutputSchema });
}
<span class="cm">// Playground 不过是这台引擎的「交互式前台」——同一引擎，换个用法</span></pre>
</div>

<table class="t">
  <thead><tr><th>消费者</th><th>它把什么交给引擎</th><th>典型用途</th></tr></thead>
  <tbody>
    <tr><td><b>Playground</b>（本课）</td><td>你界面上敲的 messages + 选的模型 + tools/schema</td><td>交互试 prompt，发布前手动验证</td></tr>
    <tr><td><b>LLM 裁判</b>（第29课）</td><td>编译后的评分 prompt + 结构化输出 schema</td><td>自动给 trace 评分（source=EVAL）</td></tr>
    <tr><td><b>prompt 实验</b>（第36课）</td><td>填好变量的 prompt + 被考的 provider/model</td><td>逐题跑出一场 run 供对比</td></tr>
  </tbody>
</table>
<p>三者要解决的业务问题各不相同，但「怎么调一个 LLM」这件苦活——选 adapter、解密凭证、拼请求、收流式、要结构化——<strong>都压进同一个 <code>fetchLLMCompletion</code></strong>。这就是好抽象的标志：上层千变万化，底座岿然不动。</p>
""")

_ZH39.append(r"""
<h2>皇冠明珠：API key 的加密存储</h2>
<p>要调任何 provider，都得带上它的 API key。这把 key 是<strong>能直接花你钱、动你账号</strong>的最高敏感数据，绝不能明文躺在数据库里。Langfuse 的 <code>LlmApiKeys</code> 表把它<strong>加密</strong>存进 <code>secretKey</code> 字段，加密用的是 <strong>AES-256-GCM</strong>——一种<strong>认证加密</strong>：既保密、又能用一个 <strong>authTag</strong> 检测密文有没有被篡改。同时另存一个<strong>脱敏</strong>的 <code>displaySecretKey</code>（只露末尾几位）专供 UI 展示，让你认得出是哪把钥匙，却看不到全貌。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="API key 加密存储：明文 key 经 AES-256-GCM 加密（随机 IV + 256 位密钥），产出 iv:密文:authTag 存进 secretKey 字段；另存脱敏 displaySecretKey 供 UI 展示；真正调用 provider 前的那一刻才 decrypt 还原明文">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">明文只在「存」和「用」的瞬间存在，库里永远是密文</text>
  <rect x="30" y="48" width="140" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="100" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">明文 API key</text><text x="100" y="83" text-anchor="middle" font-size="6.6" fill="var(--muted)">sk-abc...xyz</text>
  <rect x="230" y="40" width="170" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="315" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">AES-256-GCM 加密</text><text x="315" y="77" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">随机 IV（每次不同）</text><text x="315" y="90" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">+ authTag 防篡改</text>
  <rect x="460" y="40" width="230" height="60" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="575" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">secretKey（库里只存这个）</text><text x="575" y="75" text-anchor="middle" font-size="6.5" fill="var(--muted)">iv : 密文 : authTag（全 hex）</text><text x="575" y="90" text-anchor="middle" font-size="6.5" fill="var(--muted)">看不懂、改不了、对不上就拒绝</text>
  <rect x="230" y="120" width="170" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="138" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">displaySecretKey</text><text x="315" y="152" text-anchor="middle" font-size="6.5" fill="var(--muted)">脱敏：sk-…xyz（供 UI 认）</text>
  <rect x="460" y="120" width="230" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="575" y="138" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">用时才 decrypt</text><text x="575" y="152" text-anchor="middle" font-size="6.5" fill="var(--accent-ink)">调 provider 前一刻还原明文，用完即弃</text>
  <line x1="170" y1="70" x2="228" y2="70" stroke="var(--accent)" stroke-width="1.5"/><polygon points="228,70 219,66 219,74" fill="var(--accent)"/>
  <line x1="400" y1="70" x2="458" y2="70" stroke="var(--teal)" stroke-width="1.5"/><polygon points="458,70 449,66 449,74" fill="var(--teal)"/>
  <line x1="100" y1="92" x2="100" y2="140" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/><line x1="100" y1="140" x2="228" y2="140" stroke="var(--blue)" stroke-width="1.2"/><polygon points="228,140 219,136 219,144" fill="var(--blue)"/>
  <line x1="575" y1="100" x2="575" y2="118" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 2"/><polygon points="575,120 571,111 579,111" fill="var(--accent)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">数据库被脱库也只拿到密文；没有 ENCRYPTION_KEY（独立保管），密文就是一堆乱码</text>
</svg>
<div class="figcap"><b>认证加密 + 脱敏展示 + 即用即解</b>：<code>encrypt()</code>（<code>encryption.ts:18-35</code>）用 AES-256-GCM，每次生成随机 12 字节 IV，输出 <code>iv:encrypted:authTag</code>。<code>secretKey</code> 存密文、<code>displaySecretKey</code> 存脱敏串（<code>schema.prisma:299</code> LlmApiKeys）。<code>ENCRYPTION_KEY</code> 是 256 位、独立于库保管。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/encryption/encryption.ts:18-35</span><span class="ln">AES-256-GCM 加密</span></div>
  <pre class="code"><span class="kw">export function</span> <span class="fn">encrypt</span>(plainText: string): string {
  <span class="kw">const</span> iv = crypto.randomBytes(<span class="st">12</span>);                       <span class="cm">// 每次随机 IV → 同明文每次密文都不同</span>
  <span class="kw">const</span> cipher = crypto.createCipheriv(<span class="st">"aes-256-gcm"</span>,
    Buffer.from(ENCRYPTION_KEY, <span class="st">"hex"</span>), iv);              <span class="cm">// 256 位密钥，独立于数据库保管</span>
  <span class="kw">let</span> encrypted = cipher.update(plainText, <span class="st">"utf8"</span>, <span class="st">"hex"</span>) + cipher.final(<span class="st">"hex"</span>);
  <span class="kw">const</span> authTag = cipher.getAuthTag();                     <span class="cm">// GCM 认证标签 → 解密时校验，篡改即报错</span>
  <span class="kw">return</span> iv.toString(<span class="st">"hex"</span>) + <span class="st">":"</span> + encrypted + <span class="st">":"</span> + authTag.toString(<span class="st">"hex"</span>);
}
<span class="cm">// 存进 LlmApiKeys.secretKey；调 provider 前一刻才 decrypt（fetchLLMCompletion 内）</span></pre>
</div>

<table class="t">
  <thead><tr><th>在哪</th><th>key 以什么形态出现</th><th>谁能看到</th></tr></thead>
  <tbody>
    <tr><td>数据库（<code>secretKey</code>）</td><td><b>密文</b> iv:密文:authTag</td><td>脱库者只拿到乱码（无 ENCRYPTION_KEY 解不开）</td></tr>
    <tr><td>UI（<code>displaySecretKey</code>）</td><td><b>脱敏串</b> sk-…xyz</td><td>你能认出是哪把，但看不到全貌</td></tr>
    <tr><td>调 provider 前一刻</td><td><b>明文</b>（瞬时）</td><td>仅内存里短暂存在，用完即弃</td></tr>
  </tbody>
</table>
<p>一把 key、三种形态，各就各位：<strong>静态存储只见密文、人看只见脱敏、明文只在点火的一瞬现身</strong>。把「明文的暴露面」压到几乎为零，正是凭证管理的核心纪律。</p>
""")

_ZH39.append(r"""
<h2>可复用的积木：结构化 schema 与工具</h2>
<p>除了凭证，现代 LLM 调用还常带两样东西：<strong>结构化输出 schema</strong>（要求模型按固定 JSON 形状返回，第 29 课裁判正靠它）和<strong>工具/函数定义</strong>（让模型能「调用」外部能力）。Langfuse 把它们也建成可复用的实体——<code>LlmSchema</code> 和 <code>LlmTool</code>，于是你在 Playground 里定义一次，评估、实验里都能直接拿来用。</p>

<svg viewBox="0 0 720 220" role="img" aria-label="三块可复用积木 LlmApiKeys 连接、LlmSchema 结构化输出、LlmTool 工具函数，汇入统一的 fetchLLMCompletion 引擎，被 Playground、评估（L29 裁判）、实验（L36 对比）三个消费者共用，在 Playground 定义一次别处直接复用">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">三块可复用积木 → 一台引擎 → 三个消费者</text>
  <rect x="16" y="44" width="176" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="104" y="62" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">LlmApiKeys · 连接</text>
  <text x="104" y="79" font-size="8.5" text-anchor="middle" fill="var(--muted)">凭证 · adapter · baseURL</text>
  <rect x="16" y="98" width="176" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="104" y="116" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">LlmSchema · 结构化输出</text>
  <text x="104" y="133" font-size="8.5" text-anchor="middle" fill="var(--muted)">{score, reasoning}</text>
  <rect x="16" y="152" width="176" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="104" y="170" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">LlmTool · 工具/函数</text>
  <text x="104" y="187" font-size="8.5" text-anchor="middle" fill="var(--muted)">名字 + 参数 schema</text>
  <rect x="256" y="86" width="190" height="72" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="351" y="116" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">fetchLLMCompletion</text>
  <text x="351" y="136" font-size="9.5" text-anchor="middle" fill="var(--muted)">统一引擎</text>
  <rect x="512" y="44" width="192" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="608" y="62" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Playground</text>
  <text x="608" y="79" font-size="8.5" text-anchor="middle" fill="var(--muted)">交互试 prompt</text>
  <rect x="512" y="98" width="192" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="608" y="116" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">评估（L29 裁判）</text>
  <text x="608" y="133" font-size="8.5" text-anchor="middle" fill="var(--muted)">靠 schema 稳定返回</text>
  <rect x="512" y="152" width="192" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="608" y="170" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">实验（L36 对比）</text>
  <text x="608" y="187" font-size="8.5" text-anchor="middle" fill="var(--muted)">逐题跑应用</text>
  <line x1="192" y1="66" x2="256" y2="100" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="192" y1="120" x2="256" y2="122" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="192" y1="174" x2="256" y2="144" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="446" y1="100" x2="512" y2="66" stroke="var(--teal)" stroke-width="2"></line>
  <line x1="446" y1="122" x2="512" y2="120" stroke="var(--teal)" stroke-width="2"></line>
  <line x1="446" y1="144" x2="512" y2="174" stroke="var(--teal)" stroke-width="2"></line>
</svg>

<div class="cols">
  <div class="col"><h4>LlmSchema · 结构化输出</h4><p>定义模型必须遵守的 JSON 形状（如 <code>{score, reasoning}</code>）。这正是第 29 课裁判能稳定返回「分数+理由」的底层依赖——同一套 schema 机制，被裁判与 Playground 共用。</p></div>
  <div class="col"><h4>LlmTool · 函数/工具</h4><p>定义模型可调用的工具签名（名字、参数 schema）。让模型在 Playground 里就能演示「函数调用」式的 agent 行为，定义沉淀下来供别处复用。</p></div>
  <div class="col"><h4>LlmApiKeys · 连接</h4><p>加密保管的 provider 凭证 + <code>adapter</code>（抽象 openai/anthropic 等接口）+ 可选 <code>baseURL</code>（接自建/代理端点）。三处 LLM 调用的共同底座。</p></div>
</div>

<p>这三块积木——连接、schema、工具——加上统一的 <code>fetchLLMCompletion</code> 引擎，构成了 Langfuse 里<strong>一切服务端 LLM 调用的公共底座</strong>。到这里，Part 7（乃至前七部分的「开发者工作流」主线）合拢成一个闭环：在 <strong>Playground</strong> 里交互地试 prompt → 满意了<strong>版本化</strong>（第 37 课）→ 拉进数据集<strong>跑实验</strong>对比（第 36 课）→ 用 <strong>label</strong> 安全发布（第 37 课）→ 上线后被<strong>观测</strong>（第一~四部分）、<strong>评估</strong>（第五部分）、必要时<strong>告警</strong>（第 33 课）。一个完整的、有数据支撑、可安全迭代的 LLM 工程生命周期，至此严丝合缝。</p>
""")

_ZH39.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么用 AES-256-GCM 这种「认证加密」，而不是普通的对称加密？</strong> 因为对 API key 这种数据，<strong>光保密还不够，还要防篡改</strong>。普通加密（如 AES-CBC）能保证「别人看不懂密文」，但<strong>挡不住有人偷偷改几个字节</strong>——改完你解密出来可能是另一串看似合法的乱码，悄无声息地出错。GCM 模式在加密的同时算一个 <strong>authTag（认证标签）</strong>，解密时一并校验：密文哪怕被动一个比特，校验就失败、直接拒绝。于是你得到的不只是「保密」，还有「<strong>完整性保证</strong>」——拿到的明文要么和当初存的<strong>一模一样</strong>、要么干脆报错，绝不会是被悄悄篡改过的版本。对凭证这种「错一点就酿大祸」的数据，认证加密是底线。<br><br>
  <strong>为什么每次加密都用一个随机 IV，还要单存一个脱敏的 displaySecretKey？</strong> 随机 <strong>IV（初始向量）</strong>解决的是「<strong>同样的明文，每次加密出来的密文都不同</strong>」——否则两个一样的 key 会有一样的密文，攻击者一眼就能看出「这俩用了同一把钥匙」，泄露信息。每次换随机 IV，让密文彻底无规律可循。而 <code>displaySecretKey</code> 则解决一个很实际的体验问题：你在 UI 上得能<strong>认出</strong>「这是哪把 key」，但又<strong>不该</strong>为了显示就把整把 key 解密暴露。于是单存一个脱敏串（只露末尾几位），<strong>展示用脱敏版、调用才解密真版</strong>——安全与可用，两头都顾上了。这套「明文只在存入和点火的瞬间存在、其余时间只见密文与脱敏」的纪律，正是处理一切敏感凭证的范式。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>Playground = 同一引擎的交互式前台</strong>：<code>chatCompletionHandler</code> 复用和评估（第29课）、实验（第36课）完全相同的 <code>fetchLLMCompletion</code> 核心——一台引擎，三个消费者，凭证解密/provider 适配只写一遍。</li>
    <li><strong>API key 加密存储</strong>：<code>LlmApiKeys.secretKey</code> 用 <strong>AES-256-GCM</strong>（认证加密）存密文，<code>displaySecretKey</code> 存脱敏串供 UI，<code>adapter</code> 抽象 provider 接口、<code>baseURL</code> 接自建端点。</li>
    <li><strong>认证加密防篡改</strong>：GCM 的 <code>authTag</code> 让解密时能检出密文是否被动过——保密之外再加「完整性保证」，对凭证这种数据是底线。</li>
    <li><strong>随机 IV + 即用即解</strong>：每次随机 IV 让同明文密文各异、不泄露信息；明文只在「存入」与「调用前一刻」短暂存在，库里和 UI 上永远只见密文 / 脱敏串。</li>
    <li><strong>可复用积木 + 闭环</strong>：<code>LlmSchema</code>（结构化输出，呼应第29课）、<code>LlmTool</code>（函数调用）一次定义处处复用。Playground→版本化→实验→label 发布→观测/评估/告警，开发者工作流至此合拢成完整闭环。</li>
  </ul>
</div>
""")

_EN39.append(r"""
<p class="lead">
This lesson caps Part 7 and the whole "developer workflow" arc. The <strong>Playground</strong> is where you <strong>interactively test a prompt</strong>—type a few messages, pick a model, hit run, see the response, and once satisfied, go version it (Lesson 37) and run an experiment (Lesson 36). But for any <strong>server-side LLM call</strong> to happen, two things must exist behind the scenes: a <strong>safely stored LLM connection</strong> (your provider credentials), and a set of defined <strong>structured-output schemas and tools</strong>.
This lesson covers them, focusing on an unavoidable security topic: a provider's API key is a "crown jewel" that can <strong>spend your real money</strong>, so how does Langfuse store it <strong>encrypted</strong> and safely retrieve it at the moment of use. You'll also see a guide-wide convergence: the Playground, evaluation (Lesson 29), and experiments (Lesson 36) <strong>share one LLM-call engine</strong>.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  The Playground is like a "<strong>driving simulator + key safe</strong>". The <strong>simulator</strong> (playground) lets you <strong>test-drive</strong> (test a prompt) repeatedly before going on the road (versioning, shipping)—and it uses the real car's <strong>same engine</strong> (the same <code>fetchLLMCompletion</code> as evals and experiments), so what runs smoothly in the sim runs smoothly on the road.
  But starting the engine needs a <strong>key</strong> (the provider's API key). This key is too valuable—anyone holding it can drive your car and burn your fuel—so it's <strong>locked in a safe</strong> (AES-encrypted storage). The safe normally exposes only the key ring's <strong>last few digits</strong> (<code>displaySecretKey</code>) so you can tell which key it is, and only at the <strong>moment of ignition</strong> is the real key taken out (decrypted) and put into the engine. <strong>The key is never left bare outside—it appears only in the instant of ignition.</strong>
</div>
""")

_EN39.append(r"""
<h2>One engine, three consumers</h2>
<p>The Playground looks like a standalone little tool, but underneath it <strong>reuses the exact same LLM-call core as evals and experiments</strong>—<code>fetchLLMCompletion</code>. Its <code>chatCompletionHandler</code> hands the messages you typed, the model you picked, and the <code>tools</code> and <code>structuredOutputSchema</code> you configured to this core. So Lesson 29's judge, Lesson 36's experiment, and the Playground here are essentially <strong>three consumers of one engine</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 210" role="img" aria-label="One LLM engine, three consumers: the Playground's interactive testing, Lesson 29's LLM judge, and Lesson 36's prompt experiment all call the same fetchLLMCompletion core, which then carries the decrypted credentials to call each provider">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">one fetchLLMCompletion, shared by three</text>
  <rect x="30" y="44" width="180" height="40" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="120" y="62" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Playground (this lesson)</text><text x="120" y="76" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">interactive prompt testing</text>
  <rect x="30" y="92" width="180" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="120" y="110" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">LLM judge (Lesson 29)</text><text x="120" y="124" text-anchor="middle" font-size="6.6" fill="var(--muted)">structured-output scoring</text>
  <rect x="30" y="140" width="180" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="120" y="158" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">prompt experiment (L36)</text><text x="120" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">run a prompt per question</text>
  <rect x="290" y="84" width="170" height="56" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="375" y="106" text-anchor="middle" font-size="9.5" font-weight="700" fill="var(--accent-ink)">fetchLLMCompletion</text><text x="375" y="124" text-anchor="middle" font-size="6.8" fill="var(--accent-ink)">the unified LLM-call core</text>
  <rect x="540" y="60" width="150" height="34" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="615" y="81" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">OpenAI</text>
  <rect x="540" y="100" width="150" height="34" rx="8" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="615" y="121" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--teal)">Anthropic</text>
  <rect x="540" y="140" width="150" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="615" y="161" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--muted)">… (by adapter)</text>
  <line x1="210" y1="64" x2="288" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="288,100 279,96 280,104" fill="var(--accent)"/>
  <line x1="210" y1="112" x2="288" y2="112" stroke="var(--blue)" stroke-width="1.4"/><polygon points="288,112 279,108 279,116" fill="var(--blue)"/>
  <line x1="210" y1="160" x2="288" y2="124" stroke="var(--blue)" stroke-width="1.4"/><polygon points="288,124 280,128 279,120" fill="var(--blue)"/>
  <line x1="460" y1="104" x2="538" y2="80" stroke="var(--teal)" stroke-width="1.3"/><line x1="460" y1="112" x2="538" y2="116" stroke="var(--teal)" stroke-width="1.3"/><line x1="460" y1="120" x2="538" y2="152" stroke="var(--faint)" stroke-width="1.2"/>
  <text x="360" y="198" text-anchor="middle" font-size="8" fill="var(--faint)">one engine wraps it all: credential decryption, provider adaptation, structured output, tool calls, streaming—reused by three, no reinventing</text>
</svg>
<div class="figcap"><b>one core, three reuses</b>: <code>web/src/features/playground/server/chatCompletionHandler.ts:19,69-86</code> directly calls <code>fetchLLMCompletion</code>, passing <code>tools</code> and <code>structuredOutputSchema</code>. This shares the <b>same engine</b> with Lesson 29's judge <code>callLLM</code> and Lesson 36's experiment model call—credential decryption and provider adaptation written once.</div>
</div>
<div class="fig">
<svg viewBox="0 0 720 222" role="img" aria-label="Playground request real example: left is the LlmApiKeys connection (provider=openai, adapter=openai, masked displaySecretKey sk…a1b2, secretKey encrypted with AES-256-GCM), right is the request params (model=gpt-4o, temperature=0.2, maxTokens=512, system+user messages); both feed fetchLLMCompletion, which decrypts the credential only at call time and returns content and usage. Fields from the LlmApiKeys model, values illustrative">
  <text x="360" y="20" text-anchor="middle" font-size="13" font-weight="700" fill="var(--accent-ink)">Example: one Playground request</text>
  <rect x="18" y="32" width="330" height="126" rx="9" fill="var(--bg)" stroke="var(--blue)"/>
  <text x="32" y="50" font-size="8.5" font-weight="700" fill="var(--blue)">LLM connection · LlmApiKeys</text>
  <text x="32" y="68" font-size="7.6" fill="var(--muted)">provider</text><text x="170" y="68" font-size="7.6" font-family="monospace" fill="var(--ink)">openai</text>
  <text x="32" y="86" font-size="7.6" fill="var(--muted)">adapter</text><text x="170" y="86" font-size="7.6" font-family="monospace" fill="var(--ink)">openai</text>
  <text x="32" y="104" font-size="7.6" fill="var(--muted)">displaySecretKey</text><text x="170" y="104" font-size="7.6" font-family="monospace" fill="var(--ink)">sk-…a1b2</text>
  <text x="32" y="122" font-size="7.6" fill="var(--muted)">baseURL</text><text x="170" y="122" font-size="7.6" font-family="monospace" fill="var(--ink)">(default)</text>
  <rect x="30" y="138" width="306" height="14" rx="7" fill="var(--amber-soft)"/><text x="36" y="148" font-size="6.6" fill="var(--amber)">🔒 secretKey: AES-256-GCM encrypted, decrypted at call time</text>
  <rect x="360" y="32" width="342" height="126" rx="9" fill="var(--bg)" stroke="var(--accent)"/>
  <text x="374" y="50" font-size="8.5" font-weight="700" fill="var(--accent-ink)">request params</text>
  <text x="374" y="68" font-size="7.6" fill="var(--muted)">model</text><text x="500" y="68" font-size="7.6" font-family="monospace" fill="var(--ink)">gpt-4o</text>
  <text x="374" y="86" font-size="7.6" fill="var(--muted)">temperature</text><text x="500" y="86" font-size="7.6" font-family="monospace" fill="var(--ink)">0.2</text>
  <text x="374" y="104" font-size="7.6" fill="var(--muted)">maxTokens</text><text x="500" y="104" font-size="7.6" font-family="monospace" fill="var(--ink)">512</text>
  <rect x="372" y="120" width="318" height="32" rx="6" fill="var(--code-bg)"/><text x="380" y="133" font-size="6.8" font-family="monospace" fill="var(--code-ink)">messages: [{role:&quot;system&quot;, …},</text><text x="380" y="146" font-size="6.8" font-family="monospace" fill="var(--code-ink)">  {role:&quot;user&quot;, content:&quot;Refund?&quot;}]</text>
  <path d="M360 175 L300 175 L300 185 L420 185" fill="none" stroke="var(--line)" stroke-width="1.4"/>
  <rect x="250" y="170" width="220" height="28" rx="8" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="1.6"/><text x="360" y="188" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">fetchLLMCompletion()</text>
  <text x="360" y="212" text-anchor="middle" font-size="7.4" fill="var(--muted)">the same engine is reused by L29 judge and L36 experiments — define a connection once, reuse everywhere</text>
  <rect x="490" y="170" width="212" height="28" rx="8" fill="var(--panel-2)" stroke="var(--accent)"/><text x="500" y="183" font-size="6.8" font-family="monospace" fill="var(--ink)">→ { content:&quot;30 days…&quot;,</text><text x="500" y="194" font-size="6.8" font-family="monospace" fill="var(--muted)">     usage:{ in:42,out:18 } }</text>
</svg>
<div class="figcap"><b>The Playground just feeds "connection + params" into one shared engine</b> (fields from the <code>LlmApiKeys</code> model; <b>values illustrative</b>): the <b>connection</b> on the left comes from <code>LlmApiKeys</code> — <code>provider</code>/<code>adapter</code> pick the interface, <code>secretKey</code> is stored <code>AES-256-GCM</code>-encrypted and decrypted only at call time, while the UI only ever sees the masked <code>displaySecretKey</code>; the <b>request params</b> on the right are <code>model</code>/<code>temperature</code>/<code>maxTokens</code> plus messages. Both flow into <code>fetchLLMCompletion()</code> — the <b>same engine</b> reused by Lesson 29's judge and Lesson 36's experiments.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/playground/server/chatCompletionHandler.ts</span><span class="ln">Playground calls the same core</span></div>
  <pre class="code"><span class="kw">import</span> { fetchLLMCompletion } <span class="kw">from</span> <span class="st">"@langfuse/shared/src/server"</span>;   <span class="cm">// same as evals/experiments</span>

<span class="kw">const</span> fetchLLMCompletionParams = { messages, modelParams, <span class="cm">/* configured in the UI */</span>
  tools,                  <span class="cm">// from LlmTool (function-call definitions)</span>
  structuredOutputSchema  <span class="cm">// from LlmSchema (structured output, echoing Lesson 29)</span>
};
<span class="kw">if</span> (structuredOutputSchema) {
  <span class="kw">const</span> result = <span class="kw">await</span> fetchLLMCompletion({ ...fetchLLMCompletionParams, structuredOutputSchema });
}
<span class="cm">// the Playground is just this engine's "interactive front desk"—same engine, different use</span></pre>
</div>

<table class="t">
  <thead><tr><th>consumer</th><th>what it hands the engine</th><th>typical use</th></tr></thead>
  <tbody>
    <tr><td><b>Playground</b> (this lesson)</td><td>messages you typed + model picked + tools/schema</td><td>interactive prompt testing, manual pre-release validation</td></tr>
    <tr><td><b>LLM judge</b> (Lesson 29)</td><td>the compiled scoring prompt + structured-output schema</td><td>auto-scoring traces (source=EVAL)</td></tr>
    <tr><td><b>prompt experiment</b> (Lesson 36)</td><td>the variable-filled prompt + the provider/model under test</td><td>run a run per question for comparison</td></tr>
  </tbody>
</table>
<p>The three solve different business problems, but the grind of "how to call an LLM"—picking the adapter, decrypting credentials, assembling the request, receiving streams, demanding structure—is <strong>all pressed into one <code>fetchLLMCompletion</code></strong>. That's the mark of a good abstraction: the upper layers vary endlessly, the foundation stands firm.</p>
""")

# (en sec2/3/spark below)

_EN39.append(r"""
<h2>The crown jewel: encrypted storage of the API key</h2>
<p>To call any provider you must carry its API key. This key is the most sensitive data—it can <strong>directly spend your money and act on your account</strong>—and must never sit in plaintext in the database. Langfuse's <code>LlmApiKeys</code> table stores it <strong>encrypted</strong> in the <code>secretKey</code> field, using <strong>AES-256-GCM</strong>—an <strong>authenticated encryption</strong>: both confidential, and able to detect tampering via an <strong>authTag</strong>. It separately stores a <strong>masked</strong> <code>displaySecretKey</code> (only the last few digits) for the UI, so you can tell which key it is without seeing the whole thing.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="API key encrypted storage: a plaintext key is encrypted with AES-256-GCM (random IV + 256-bit key), producing iv:ciphertext:authTag stored in the secretKey field; a masked displaySecretKey is stored for the UI; only at the moment before calling the provider is it decrypted back to plaintext">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">plaintext exists only at "store" and "use"; the DB always holds ciphertext</text>
  <rect x="30" y="48" width="140" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="100" y="68" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">plaintext API key</text><text x="100" y="83" text-anchor="middle" font-size="6.6" fill="var(--muted)">sk-abc...xyz</text>
  <rect x="230" y="40" width="170" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="315" y="60" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">AES-256-GCM encrypt</text><text x="315" y="77" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">random IV (different each time)</text><text x="315" y="90" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">+ authTag anti-tamper</text>
  <rect x="460" y="40" width="230" height="60" rx="10" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="575" y="58" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">secretKey (only this in the DB)</text><text x="575" y="75" text-anchor="middle" font-size="6.2" fill="var(--muted)">iv : ciphertext : authTag (all hex)</text><text x="575" y="90" text-anchor="middle" font-size="6.2" fill="var(--muted)">unreadable, unchangeable, rejected if mismatched</text>
  <rect x="230" y="120" width="170" height="40" rx="9" fill="var(--bg)" stroke="var(--blue)"/><text x="315" y="138" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">displaySecretKey</text><text x="315" y="152" text-anchor="middle" font-size="6.2" fill="var(--muted)">masked: sk-…xyz (for the UI)</text>
  <rect x="460" y="120" width="230" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="575" y="138" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">decrypt only when used</text><text x="575" y="152" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">restore plaintext just before calling the provider, discard after</text>
  <line x1="170" y1="70" x2="228" y2="70" stroke="var(--accent)" stroke-width="1.5"/><polygon points="228,70 219,66 219,74" fill="var(--accent)"/>
  <line x1="400" y1="70" x2="458" y2="70" stroke="var(--teal)" stroke-width="1.5"/><polygon points="458,70 449,66 449,74" fill="var(--teal)"/>
  <line x1="100" y1="92" x2="100" y2="140" stroke="var(--faint)" stroke-width="1.2" stroke-dasharray="3 2"/><line x1="100" y1="140" x2="228" y2="140" stroke="var(--blue)" stroke-width="1.2"/><polygon points="228,140 219,136 219,144" fill="var(--blue)"/>
  <line x1="575" y1="100" x2="575" y2="118" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 2"/><polygon points="575,120 571,111 579,111" fill="var(--accent)"/>
  <text x="360" y="200" text-anchor="middle" font-size="8" fill="var(--faint)">a DB breach yields only ciphertext; without ENCRYPTION_KEY (kept separately), the ciphertext is gibberish</text>
</svg>
<div class="figcap"><b>authenticated encryption + masked display + decrypt-on-use</b>: <code>encrypt()</code> (<code>encryption.ts:18-35</code>) uses AES-256-GCM, generating a random 12-byte IV each time, outputting <code>iv:encrypted:authTag</code>. <code>secretKey</code> stores ciphertext, <code>displaySecretKey</code> a masked string (<code>schema.prisma:299</code> LlmApiKeys). <code>ENCRYPTION_KEY</code> is 256-bit, kept separately from the DB.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/encryption/encryption.ts:18-35</span><span class="ln">AES-256-GCM encrypt</span></div>
  <pre class="code"><span class="kw">export function</span> <span class="fn">encrypt</span>(plainText: string): string {
  <span class="kw">const</span> iv = crypto.randomBytes(<span class="st">12</span>);                       <span class="cm">// random IV each time → same plaintext, different ciphertext</span>
  <span class="kw">const</span> cipher = crypto.createCipheriv(<span class="st">"aes-256-gcm"</span>,
    Buffer.from(ENCRYPTION_KEY, <span class="st">"hex"</span>), iv);              <span class="cm">// 256-bit key, kept separately from the DB</span>
  <span class="kw">let</span> encrypted = cipher.update(plainText, <span class="st">"utf8"</span>, <span class="st">"hex"</span>) + cipher.final(<span class="st">"hex"</span>);
  <span class="kw">const</span> authTag = cipher.getAuthTag();                     <span class="cm">// GCM auth tag → verified on decrypt, errors on tampering</span>
  <span class="kw">return</span> iv.toString(<span class="st">"hex"</span>) + <span class="st">":"</span> + encrypted + <span class="st">":"</span> + authTag.toString(<span class="st">"hex"</span>);
}
<span class="cm">// stored in LlmApiKeys.secretKey; decrypted only just before calling the provider (inside fetchLLMCompletion)</span></pre>
</div>

<table class="t">
  <thead><tr><th>where</th><th>what form the key takes</th><th>who can see it</th></tr></thead>
  <tbody>
    <tr><td>database (<code>secretKey</code>)</td><td><b>ciphertext</b> iv:ciphertext:authTag</td><td>a breach yields gibberish (can't decrypt without ENCRYPTION_KEY)</td></tr>
    <tr><td>UI (<code>displaySecretKey</code>)</td><td><b>masked string</b> sk-…xyz</td><td>you can recognize which key, but not see the whole</td></tr>
    <tr><td>just before calling the provider</td><td><b>plaintext</b> (momentary)</td><td>exists briefly in memory only, discarded after</td></tr>
  </tbody>
</table>
<p>One key, three forms, each in its place: <strong>at rest only ciphertext, to a human only a mask, plaintext appearing only in the instant of ignition</strong>. Squeezing "the exposure surface of plaintext" to nearly zero is the core discipline of credential management.</p>
""")

_EN39.append(r"""
<h2>Reusable building blocks: structured schemas and tools</h2>
<p>Besides credentials, modern LLM calls often carry two things: a <strong>structured-output schema</strong> (requiring the model to return a fixed JSON shape, which Lesson 29's judge relies on) and <strong>tool/function definitions</strong> (letting the model "call" external capabilities). Langfuse models these as reusable entities too—<code>LlmSchema</code> and <code>LlmTool</code>—so you define them once in the Playground and reuse them in evals and experiments.</p>

<svg viewBox="0 0 720 220" role="img" aria-label="three reusable blocks LlmApiKeys (connection), LlmSchema (structured output) and LlmTool (tools/functions) feed one shared fetchLLMCompletion engine, consumed by three surfaces: the Playground, evaluation (L29 judge) and experiments (L36 comparison); define once in the Playground and reuse everywhere">
  <rect x="0" y="0" width="720" height="220" fill="var(--bg)"></rect>
  <text x="24" y="24" font-size="11.5" font-weight="700" fill="var(--accent-ink)">three reusable blocks → one engine → three consumers</text>
  <rect x="16" y="44" width="176" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="104" y="62" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">LlmApiKeys · connection</text>
  <text x="104" y="79" font-size="8.5" text-anchor="middle" fill="var(--muted)">creds · adapter · baseURL</text>
  <rect x="16" y="98" width="176" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="104" y="116" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">LlmSchema · structured</text>
  <text x="104" y="133" font-size="8.5" text-anchor="middle" fill="var(--muted)">{score, reasoning}</text>
  <rect x="16" y="152" width="176" height="44" rx="8" fill="var(--blue-soft)" stroke="var(--blue)"></rect>
  <text x="104" y="170" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">LlmTool · tools/fns</text>
  <text x="104" y="187" font-size="8.5" text-anchor="middle" fill="var(--muted)">name + param schema</text>
  <rect x="256" y="86" width="190" height="72" rx="10" fill="var(--accent-soft)" stroke="var(--accent)"></rect>
  <text x="351" y="116" font-size="11.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">fetchLLMCompletion</text>
  <text x="351" y="136" font-size="9.5" text-anchor="middle" fill="var(--muted)">one engine</text>
  <rect x="512" y="44" width="192" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="608" y="62" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">Playground</text>
  <text x="608" y="79" font-size="8.5" text-anchor="middle" fill="var(--muted)">test a prompt</text>
  <rect x="512" y="98" width="192" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="608" y="116" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">eval (L29 judge)</text>
  <text x="608" y="133" font-size="8.5" text-anchor="middle" fill="var(--muted)">schema → stable JSON</text>
  <rect x="512" y="152" width="192" height="44" rx="8" fill="var(--bg)" stroke="var(--teal)"></rect>
  <text x="608" y="170" font-size="10.5" font-weight="700" text-anchor="middle" fill="var(--accent-ink)">experiments (L36)</text>
  <text x="608" y="187" font-size="8.5" text-anchor="middle" fill="var(--muted)">app per item</text>
  <line x1="192" y1="66" x2="256" y2="100" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="192" y1="120" x2="256" y2="122" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="192" y1="174" x2="256" y2="144" stroke="var(--blue)" stroke-width="2"></line>
  <line x1="446" y1="100" x2="512" y2="66" stroke="var(--teal)" stroke-width="2"></line>
  <line x1="446" y1="122" x2="512" y2="120" stroke="var(--teal)" stroke-width="2"></line>
  <line x1="446" y1="144" x2="512" y2="174" stroke="var(--teal)" stroke-width="2"></line>
</svg>

<div class="cols">
  <div class="col"><h4>LlmSchema · structured output</h4><p>Defines the JSON shape the model must obey (e.g. <code>{score, reasoning}</code>). This is the underlying dependency that lets Lesson 29's judge reliably return "score + reasoning"—the same schema mechanism shared by the judge and the Playground.</p></div>
  <div class="col"><h4>LlmTool · function/tool</h4><p>Defines tool signatures the model can call (name, parameter schema). It lets the model demonstrate "function-calling" agent behavior right in the Playground, with the definition saved for reuse elsewhere.</p></div>
  <div class="col"><h4>LlmApiKeys · connection</h4><p>Encrypted provider credentials + <code>adapter</code> (abstracting the openai/anthropic/etc. interface) + optional <code>baseURL</code> (for self-hosted/proxy endpoints). The common base for all three LLM-call sites.</p></div>
</div>

<p>These three blocks—connection, schema, tool—plus the unified <code>fetchLLMCompletion</code> engine, form the <strong>common foundation for every server-side LLM call</strong> in Langfuse. Here Part 7 (and indeed the first seven parts' "developer workflow" through-line) closes into a loop: interactively test a prompt in the <strong>Playground</strong> → version it (Lesson 37) once satisfied → pull it into a dataset to <strong>run experiments</strong> and compare (Lesson 36) → release safely via a <strong>label</strong> (Lesson 37) → after shipping, get <strong>observed</strong> (Parts 1–4), <strong>evaluated</strong> (Part 5), and <strong>alerted</strong> when needed (Lesson 33). A complete, data-backed, safely-iterable LLM engineering lifecycle, sealed tight.</p>
""")

_EN39.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why use "authenticated encryption" like AES-256-GCM rather than plain symmetric encryption?</strong> Because for data like an API key, <strong>confidentiality alone isn't enough—you also need anti-tampering</strong>. Plain encryption (e.g. AES-CBC) guarantees "others can't read the ciphertext", but <strong>can't stop someone quietly altering a few bytes</strong>—after which you might decrypt to another seemingly-valid garbage string, failing silently. GCM mode computes an <strong>authTag (authentication tag)</strong> alongside encryption, verified on decrypt: flip even one bit of the ciphertext and verification fails, rejecting it outright. So you get not just "confidentiality" but "<strong>integrity guarantee</strong>"—the plaintext you get is either <strong>exactly</strong> what was stored, or an outright error, never a silently-tampered version. For credentials, where "a small error brews a big disaster", authenticated encryption is the floor.<br><br>
  <strong>Why a random IV per encryption, and why also store a masked displaySecretKey?</strong> The random <strong>IV (initialization vector)</strong> solves "<strong>the same plaintext encrypts to different ciphertext each time</strong>"—otherwise two identical keys would have identical ciphertext, and an attacker could instantly see "these two use the same key", leaking information. A fresh random IV makes ciphertext patternless. The <code>displaySecretKey</code> solves a very practical UX problem: in the UI you must <strong>recognize</strong> "which key this is", yet you <strong>shouldn't</strong> decrypt and expose the whole key just to display it. So a masked string (last few digits only) is stored separately—<strong>display the masked version, decrypt only to call</strong>—covering both security and usability. This discipline—"plaintext exists only in the instants of storing and igniting, the rest of the time only ciphertext and masks are seen"—is the paradigm for handling any sensitive credential.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Playground = the same engine's interactive front desk</strong>: <code>chatCompletionHandler</code> reuses the exact <code>fetchLLMCompletion</code> core as evals (L29) and experiments (L36)—one engine, three consumers, credential decryption/provider adaptation written once.</li>
    <li><strong>API key encrypted storage</strong>: <code>LlmApiKeys.secretKey</code> stores ciphertext via <strong>AES-256-GCM</strong> (authenticated encryption), <code>displaySecretKey</code> a masked string for the UI, <code>adapter</code> abstracts the provider interface, <code>baseURL</code> hits self-hosted endpoints.</li>
    <li><strong>Authenticated encryption is anti-tamper</strong>: GCM's <code>authTag</code> lets decryption detect whether the ciphertext was altered—integrity on top of confidentiality, the floor for credential data.</li>
    <li><strong>Random IV + decrypt-on-use</strong>: a random IV per encryption makes identical plaintext differ in ciphertext, leaking nothing; plaintext exists only briefly at "store" and "just before call", with the DB and UI only ever seeing ciphertext / masks.</li>
    <li><strong>Reusable blocks + the loop</strong>: <code>LlmSchema</code> (structured output, echoing L29), <code>LlmTool</code> (function calls) are defined once and reused everywhere. Playground→versioning→experiments→label release→observe/evaluate/alert—the developer workflow closes into a complete loop.</li>
  </ul>
</div>
""")

LESSON_39 = {"zh": "\n".join(_ZH39), "en": "\n".join(_EN39)}
