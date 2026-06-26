"""Part 9 — 自动化与集成 / Automation & integrations. Lessons L44–L47.

Same authoring pattern as part1..part8: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L44 · 自动化与 webhook / Automations & webhooks
# ══════════════════════════════════════════════════════════════════════
_ZH44 = []
_EN44 = []

_ZH44.append(r"""
<p class="lead">
第 33 课的监控告警要送到人手里、prompt 改了要通知外部系统、新 trace 来了要触发下游流程——这些「<strong>当 X 发生，就做 Y</strong>」的联动，由 Langfuse 的<strong>自动化（Automation）</strong>驱动：一个 <strong>Trigger（触发器，何时）</strong>绑一个 <strong>Action（动作，做什么）</strong>。这一课讲它的数据模型，但真正的重头戏，是一个绕不开的<strong>安全</strong>话题：当 Action 是 <strong>webhook</strong>（让 Langfuse 的服务器去访问<strong>用户填的任意 URL</strong>）时，怎么防住 <strong>SSRF</strong>——别让用户把你的服务器当跳板，去打内网、偷云凭证。
你会看到一套教科书级的<strong>纵深防御</strong>：协议白名单、端口白名单、内网 IP 黑名单、云元数据地址黑名单、解析失败即拦截，再加上超时、重试、签名、自动停用。「用户给我们一个 URL、我们去请求它」——这是所有 Web 系统里最危险的功能之一，这一课讲清楚它该怎么做才安全。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  自动化像家里的<strong>「智能联动」</strong>：当门铃响（Trigger），就开走廊灯（Action）。简单、好用。但 webhook 这种 Action 藏着一个危险：它让 Langfuse 的服务器，去访问<strong>用户填写的任意地址</strong>。
  这就好比你雇了个<strong>跑腿小哥</strong>，他会忠实地去你写的<strong>任何地址</strong>送信。平时没问题——可要是有人写的地址是「<strong>去公司机房，把保险柜钥匙拍张照带回来</strong>」（指向<strong>内网服务</strong>或<strong>云厂商的元数据接口</strong>），小哥照办，机密就泄了。这就是 <strong>SSRF（服务端请求伪造）</strong>：攻击者借你的服务器之手，去够它自己够不到的内部资源。防住它的办法，是给小哥一张<strong>「禁止前往」清单</strong>：本机地址、内网地址、那个专门存着云凭证的 <code>169.254.169.254</code>……一律不去，地址看不懂的也一律不去（<strong>宁可错拦，不可放过</strong>）。
</div>
""")

# (L44 sections below)

_ZH44.append(r"""
<h2>自动化 = 触发器 → 动作</h2>
<p>数据模型是经典的「IFTTT」三件套。<strong>Trigger</strong> 定义「<strong>何时</strong>」：<code>eventSource</code>（什么对象，如 trace、prompt）+ <code>eventActions</code>（什么变化，如 created/updated/deleted）+ <code>filter</code>（额外条件）。<strong>Action</strong> 定义「<strong>做什么</strong>」：<code>type</code>（WEBHOOK / SLACK / GITHUB_DISPATCH）+ <code>config</code>（如 webhook 的 url/method/headers/secretId）。<strong>Automation</strong> 把一个 Trigger 绑到一个 Action。每次触发，留一条 <strong>AutomationExecution</strong> 记录（状态、输入、输出、报错）。</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="自动化模型：一个事件发生，Trigger 按 eventSource/eventActions/filter 判断是否匹配，匹配则触发 Action（WEBHOOK/SLACK/GITHUB_DISPATCH），每次执行留一条 AutomationExecution 记录状态">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">当 X 发生（Trigger）→ 就做 Y（Action）</text>
  <rect x="20" y="80" width="120" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="80" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">一个事件</text><text x="80" y="116" text-anchor="middle" font-size="6.4" fill="var(--muted)">监控告警/prompt改/新trace</text>
  <rect x="170" y="68" width="160" height="74" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="250" y="88" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">Trigger（何时）</text><text x="250" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">eventSource: trace/prompt</text><text x="250" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">eventActions: created/updated</text><text x="250" y="131" text-anchor="middle" font-size="6.4" fill="var(--muted)">filter: 额外条件 · status ACTIVE</text>
  <rect x="360" y="62" width="170" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="445" y="80" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Action（做什么）</text><text x="445" y="94" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">WEBHOOK / SLACK / GITHUB_DISPATCH</text>
  <rect x="360" y="110" width="170" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="445" y="127" text-anchor="middle" font-size="6.8" fill="var(--muted)">config: { url, method, headers, secretId }</text><text x="445" y="138" text-anchor="middle" font-size="6.0" fill="var(--faint)">每种 type 的结构化配置</text>
  <rect x="560" y="76" width="140" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="630" y="96" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">AutomationExecution</text><text x="630" y="113" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">status: PENDING→COMPLETED/ERROR</text><text x="630" y="126" text-anchor="middle" font-size="6.2" fill="var(--muted)">input/output/error 留痕</text>
  <line x1="140" y1="105" x2="168" y2="105" stroke="var(--teal)" stroke-width="1.4"/><polygon points="168,105 159,101 159,109" fill="var(--teal)"/>
  <line x1="330" y1="95" x2="358" y2="85" stroke="var(--blue)" stroke-width="1.4"/><polygon points="358,85 349,84 351,92" fill="var(--blue)"/><text x="345" y="78" text-anchor="middle" font-size="6" fill="var(--blue)">匹配则</text>
  <line x1="530" y1="92" x2="558" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="558,100 549,97 550,105" fill="var(--accent)"/>
  <text x="360" y="172" text-anchor="middle" font-size="8" fill="var(--faint)">Automation 把一个 Trigger 绑一个 Action；这正是第33课监控告警「发布到 WebhookQueue 后」的去处——由某个 webhook Action 投递出去</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">AutomationExecution 像第30课 JobExecution、第32课标注 item——又一个「落库的执行记录」状态机</text>
</svg>
<div class="figcap"><b>Trigger → Action 的 IFTTT 模型</b>：<code>schema.prisma:1635</code> Trigger（eventSource/eventActions/filter/status）、<code>:1613</code> Action（type WEBHOOK/SLACK/GITHUB_DISPATCH + config Json）、<code>:1659</code> Automation（绑定二者）、<code>:1690</code> AutomationExecution（PENDING/COMPLETED/ERROR/CANCELLED + input/output/error）。第 33 课监控告警就经此投递。</div>
</div>

<div class="layers">
  <div class="layer l-main"><div class="lh"><span class="badge">何时</span><span class="name">Trigger</span></div><div class="ld">守着事件流：<code>eventSource</code>（盯哪类对象）+ <code>eventActions</code>（哪种变化）+ <code>filter</code>（更细的条件，和第 23 课同款过滤）。<code>status=ACTIVE</code> 才生效——可随时停用而不删除。</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">做什么</span><span class="name">Action</span></div><div class="ld">三种动作类型：<strong>WEBHOOK</strong>（调用户给的 URL，本课重点）、<strong>SLACK</strong>（发到频道，第 45 课）、<strong>GITHUB_DISPATCH</strong>（触发 GitHub workflow）。<code>config</code> 用结构化 JSON 存各自参数，<code>secretId</code> 指向加密保管的密钥（第 39 课）。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">留痕</span><span class="name">AutomationExecution</span></div><div class="ld">每次触发都落一行：状态机 PENDING→COMPLETED/ERROR/CANCELLED，连 <code>input</code>/<code>output</code>/<code>error</code> 一并存——和第 30 课 JobExecution、第 32 课标注 item 是同一种「有状态、可追溯的执行记录」。</div></div>
</div>
""")

# (L44 sec2 ssrf below)

_ZH44.append(r"""
<h2>webhook 的命门：纵深防御挡住 SSRF</h2>
<p>WEBHOOK 这个 Action，本质是「让 Langfuse 的服务器去请求一个<strong>用户填的 URL</strong>」。这是 <strong>SSRF（Server-Side Request Forgery，服务端请求伪造）</strong>的经典温床：攻击者把 URL 填成 <code>http://169.254.169.254/...</code>（云元数据接口，能拿到你的临时 AK/SK）或 <code>http://localhost:6379</code>（你的内部 Redis），借你服务器之手够到它本不该够到的东西。Langfuse 的防御不是一道墙，而是<strong>层层叠叠的多道闸</strong>——任何一道漏了，还有下一道。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="webhook SSRF 纵深防御：一个用户填的 URL 要依次通过协议白名单(仅http/https)、端口白名单(仅80/443)、主机名黑名单(localhost/metadata)、IP CIDR 黑名单(内网/loopback/link-local)、解析失败即拦截，全过才放行请求，任一不过即拒绝">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">用户填的 URL 要闯过五道闸，全过才放行</text>
  <rect x="20" y="44" width="120" height="150" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="80" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">用户填的 URL</text><text x="80" y="84" text-anchor="middle" font-size="6.2" fill="var(--muted)">合法：</text><text x="80" y="96" text-anchor="middle" font-size="5.8" fill="var(--teal)">https://hooks.x.com/…</text><text x="80" y="120" text-anchor="middle" font-size="6.2" fill="var(--muted)">恶意：</text><text x="80" y="132" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">http://169.254.169.254</text><text x="80" y="144" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">http://localhost:6379</text><text x="80" y="156" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">file:///etc/passwd</text>
  <rect x="165" y="44" width="100" height="44" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="215" y="62" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">闸1 协议</text><text x="215" y="76" text-anchor="middle" font-size="6.0" fill="var(--muted)">仅 http/https</text>
  <rect x="165" y="96" width="100" height="44" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="215" y="114" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">闸2 端口</text><text x="215" y="128" text-anchor="middle" font-size="6.0" fill="var(--muted)">仅 80 / 443</text>
  <rect x="165" y="148" width="100" height="44" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="215" y="166" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">闸3 主机名</text><text x="215" y="180" text-anchor="middle" font-size="5.6" fill="var(--muted)">黑 localhost/metadata</text>
  <rect x="290" y="70" width="110" height="44" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="345" y="88" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">闸4 IP 段</text><text x="345" y="102" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">黑 内网/loopback/link-local</text>
  <rect x="290" y="124" width="110" height="44" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="345" y="142" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">闸5 fail-closed</text><text x="345" y="156" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">解析不了？直接拦</text>
  <rect x="430" y="80" width="120" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="490" y="100" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">全过 → 放行请求</text><text x="490" y="116" text-anchor="middle" font-size="6.0" fill="var(--muted)">带超时/重试/签名</text>
  <rect x="430" y="146" width="120" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="490" y="164" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">任一不过 → 拒绝</text><text x="490" y="178" text-anchor="middle" font-size="6.0" fill="var(--muted)">恶意 URL 全被挡在外</text>
  <rect x="580" y="100" width="120" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="640" y="120" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">外部接收方</text><text x="640" y="136" text-anchor="middle" font-size="6.0" fill="var(--muted)">验签确认来自 Langfuse</text>
  <line x1="140" y1="115" x2="163" y2="100" stroke="var(--faint)" stroke-width="1"/><line x1="265" y1="92" x2="288" y2="100" stroke="var(--faint)" stroke-width="1"/><line x1="400" y1="120" x2="428" y2="115" stroke="var(--accent)" stroke-width="1.3"/><polygon points="428,115 419,112 420,120" fill="var(--accent)"/><line x1="550" y1="110" x2="578" y2="120" stroke="var(--teal)" stroke-width="1.3"/><polygon points="578,120 569,117 570,125" fill="var(--teal)"/>
  <text x="360" y="216" text-anchor="middle" font-size="8" fill="var(--faint)">关键：IP 校验在「请求时」对解析出的真实 IP 做，防 DNS-rebinding（域名先解析成合法 IP、临门一脚切到内网 IP）</text>
</svg>
<div class="figcap"><b>纵深防御，层层设防</b>：<code>validateWebhookURL</code>（<code>validation.ts:35</code>）只放 http/https、只放端口 80/443；<code>ipBlocking.ts</code> 的 <code>isHostnameBlocked</code> 黑掉 localhost / <code>metadata.google.internal</code> / <code>169.254.169.254</code>，<code>isIPBlocked</code> 黑掉 RFC1918 内网、loopback、link-local 等 CIDR，<b>且 IP 解析失败就默认拦截</b>（fail-closed）。校验在请求时对真实 IP 做，防 DNS-rebinding。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/webhooks/ipBlocking.ts · validation.ts</span><span class="ln">SSRF 防御</span></div>
  <pre class="code"><span class="cm">// 闸4：黑名单 CIDR——内网、本机、云元数据所在的链路本地段全拦</span>
<span class="kw">const</span> BLOCKED_CIDRS = [<span class="st">"10.0.0.0/8"</span>, <span class="st">"127.0.0.0/8"</span>, <span class="st">"169.254.0.0/16"</span><span class="cm">/* AWS/GCP 元数据 */</span>,
                       <span class="st">"172.16.0.0/12"</span>, <span class="st">"192.168.0.0/16"</span>, <span class="st">"::1/128"</span>, …];
<span class="kw">export function</span> <span class="fn">isIPBlocked</span>(ip) { <span class="cm">/* 命中任一段 → true；解析失败 → 也 true（宁可错拦）*/</span> }

<span class="cm">// 闸3：主机名黑名单——连域名都直接禁</span>
<span class="kw">const</span> blockedPatterns = [<span class="st">"localhost"</span>, <span class="st">"*.localhost"</span>,
  <span class="st">"metadata.google.internal"</span>, <span class="st">"169.254.169.254"</span>, …];   <span class="cm">// 云元数据端点</span>

<span class="cm">// 闸1+2：协议与端口白名单（validation.ts）</span>
<span class="kw">if</span> (!<span class="st">["http:", "https:"]</span>.includes(protocol)) <span class="kw">throw</span> <span class="st">"Only HTTP and HTTPS allowed"</span>;
<span class="kw">if</span> (![<span class="st">80, 443</span>].includes(port))            <span class="kw">throw</span> <span class="st">"Only ports 80 and 443 allowed"</span>;</pre>
</div>

<div class="cols">
  <div class="col"><h4>☁️ 云元数据接口</h4><p><code>169.254.169.254</code> / <code>metadata.google.internal</code>——AWS/GCP 实例元数据。最致命：能拿到机器的<strong>临时云凭证(AK/SK)</strong>，进而接管整个云账号。被主机名黑名单 + link-local CIDR(<code>169.254.0.0/16</code>)<strong>双重</strong>拦截。</p></div>
  <div class="col"><h4>🔌 内网服务</h4><p><code>localhost:6379</code> 的 Redis、内部管理后台、数据库……往往因为「反正在内网」而不设防。被 loopback(<code>127.0.0.0/8</code>) + RFC1918(<code>10/8</code>,<code>172.16/12</code>,<code>192.168/16</code>) CIDR 黑名单拦截。</p></div>
  <div class="col"><h4>📄 非 HTTP 协议</h4><p><code>file:///etc/passwd</code> 读本地文件、<code>gopher://</code> 打其它 TCP 服务……被<strong>协议白名单</strong>(仅 http/https)从源头掐死，连解析 IP 都轮不到。</p></div>
</div>
""")

# (L44 sec3 defense below)

_ZH44.append(r"""
<h2>不止 SSRF：投递还要稳、要可信</h2>
<p>挡住 SSRF 只是「不出事」。要让 webhook 真正<strong>可靠又可信</strong>，投递环节还有几道操作性的硬化——它们共同构成「请求外部世界」这件事的完整工程姿态：</p>

<table class="t">
  <thead><tr><th>硬化</th><th>怎么做</th><th>防什么</th></tr></thead>
  <tbody>
    <tr><td><b>SSRF 防御</b></td><td>协议/端口白名单 + IP/主机名黑名单 + fail-closed（上一节）</td><td>借你服务器打内网、偷云凭证</td></tr>
    <tr><td><b>签名</b></td><td>用密钥对 payload 算 HMAC，放进 <code>x-langfuse-signature</code> 头</td><td>接收方可验签——确认确实来自 Langfuse、未被篡改</td></tr>
    <tr><td><b>超时</b></td><td><code>AbortController</code> + <code>LANGFUSE_WEBHOOK_TIMEOUT_MS</code></td><td>对方慢/挂起时不拖死 worker</td></tr>
    <tr><td><b>重试</b></td><td><code>backOff</code> 指数退避</td><td>对方临时抖动时最终送达</td></tr>
    <tr><td><b>状态校验</b></td><td>要求返回 2xx，否则记 ERROR</td><td>悄悄失败被当成功</td></tr>
    <tr><td><b>自动停用</b></td><td>反复失败的 trigger 自动禁用</td><td>对着一个已死的端点无限锤</td></tr>
  </tbody>
</table>

<p>把这张表读完，你会发现一条清晰的工程信条：<strong>凡是「向外部世界发起请求」，都要当成不可信、不可靠来对待</strong>。外部 URL 可能是恶意的（→ SSRF 防御）、可能很慢（→ 超时）、可能临时挂（→ 重试）、可能永久挂（→ 自动停用）；而你发出去的东西，对方也需要确认是不是真的来自你（→ 签名）。每一道防护都对应一种「外部世界会怎么坑你」的具体设想——<strong>安全与健壮，从来不是一个开关，而是一摞针对具体威胁的具体防护</strong>。</p>
""")

_ZH44.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么 SSRF 值得动用这么多道防御？它到底有多危险？</strong> 因为它能把一个看似无害的功能（「我们帮你回调一个 URL」）变成<strong>直通你内网核心的隧道</strong>。最致命的目标是 <code>169.254.169.254</code>——AWS/GCP 的<strong>实例元数据接口</strong>：任何能让你服务器去请求它的人，都可能拿到这台机器的<strong>临时云凭证（AK/SK）</strong>，进而接管你的整个云账号。其次是内网服务：你的 Redis、内部管理后台、数据库，往往因为「反正在内网」而<strong>不设防</strong>——可一旦攻击者能借你的 webhook 之手去请求它们，这层「内网即安全」的假设就崩了。SSRF 的可怕，正在于它<strong>绕过了所有边界</strong>：防火墙挡的是外面进来的，而 SSRF 是<strong>从你内部往外打</strong>，畅通无阻。所以它配得上纵深防御——而且每道闸都要<strong>fail-closed</strong>：拿不准的、解析不了的，<strong>一律当危险处理</strong>。安全代码的默认答案是「拒绝」，不是「放行」。<br><br>
  <strong>为什么校验要放在「请求时」对解析出的真实 IP 做，而不是创建 webhook 时检查一下 URL 就完事？</strong> 因为有个阴险的攻击叫 <strong>DNS-rebinding（DNS 重绑定）</strong>：攻击者控制一个域名，<strong>创建 webhook 时</strong>把它解析到一个合法的公网 IP（顺利过审），等到 Langfuse <strong>真正发请求时</strong>，再把这个域名<strong>临门一脚切换</strong>解析到 <code>169.254.169.254</code> 或内网 IP。如果你只在创建时校验，就被这一手骗过去了。Langfuse 的做法是把 IP 校验下沉到<strong>实际发起请求的那一刻</strong>，对<strong>当时真正解析出的 IP</strong> 判定——攻击者再怎么切换 DNS，临门那一刻的真实 IP 也逃不过这道闸。<strong>安全检查必须贴着「真正危险动作发生的那一刻」做，而不是提前在一个可能已经过期的快照上做。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>自动化 = Trigger → Action</strong>：经典 IFTTT 模型。<code>Trigger</code>（eventSource/eventActions/filter 定「何时」）绑 <code>Action</code>（WEBHOOK/SLACK/GITHUB_DISPATCH 定「做什么」），<code>AutomationExecution</code> 留每次执行的状态记录。第 33 课监控告警经此投递。</li>
    <li><strong>webhook 的命门是 SSRF</strong>：让服务器请求用户填的 URL，攻击者可借此打内网、偷 <code>169.254.169.254</code> 的云凭证——「用户给 URL 我们去请求」是 Web 系统最危险的功能之一。</li>
    <li><strong>纵深防御挡 SSRF</strong>：协议白名单（http/https）+ 端口白名单（80/443）+ 主机名黑名单（localhost/metadata）+ IP CIDR 黑名单（内网/loopback/link-local）+ <strong>fail-closed</strong>（解析不了就拦）。任一道都可能救命。</li>
    <li><strong>校验在请求时做</strong>：对实际解析出的真实 IP 判定，防 DNS-rebinding（创建时解析到合法 IP、请求时切到内网）。安全检查要贴着危险动作发生的那一刻。</li>
    <li><strong>投递还要稳要可信</strong>：HMAC 签名（<code>x-langfuse-signature</code>，让接收方验真）+ 超时 + 指数退避重试 + 2xx 校验 + 反复失败自动停用——向外部世界发请求，一律当不可信、不可靠对待。</li>
  </ul>
</div>
""")

_EN44.append(r"""
<p class="lead">
Lesson 33's monitor alerts need to reach a human, a changed prompt needs to notify an external system, a new trace needs to kick off a downstream flow — all these "<strong>when X happens, do Y</strong>" linkages are driven by Langfuse <strong>Automations</strong>: a <strong>Trigger (when)</strong> bound to an <strong>Action (what to do)</strong>. This lesson covers the data model, but the real headline act is an unavoidable <strong>security</strong> topic: when the Action is a <strong>webhook</strong> (Langfuse's server fetches a <strong>user-supplied arbitrary URL</strong>), how do you stop <strong>SSRF</strong> — keeping users from turning your server into a springboard to hit the internal network and steal cloud credentials.
You'll see textbook-grade <strong>defense in depth</strong>: a protocol allowlist, a port allowlist, an internal-IP blocklist, a cloud-metadata-address blocklist, fail-closed on unparseable hosts, plus timeouts, retries, signing, and auto-disable. "A user gives us a URL and we fetch it" is one of the most dangerous features in any web system — this lesson spells out how to do it safely.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  An automation is like a <strong>"smart home linkage"</strong>: when the doorbell rings (Trigger), turn on the hallway light (Action). Simple, handy. But a webhook Action hides a danger: it makes Langfuse's server fetch <strong>any address the user types in</strong>.
  It's like hiring an <strong>errand runner</strong> who faithfully delivers a letter to <strong>any address you write down</strong>. Usually fine — but if someone writes "<strong>go to the company server room and snap a photo of the safe key</strong>" (pointing at an <strong>internal service</strong> or the <strong>cloud provider's metadata endpoint</strong>), the runner complies and the secret leaks. That's <strong>SSRF (Server-Side Request Forgery)</strong>: the attacker borrows your server's hands to reach internal resources it could never reach on its own. The defense is to hand the runner a <strong>"do-not-go" list</strong>: localhost, internal addresses, that <code>169.254.169.254</code> that holds cloud credentials… all off-limits — and anything whose address can't be understood is off-limits too (<strong>better to wrongly block than to let through</strong>).
</div>

<h2>Automation = trigger → action</h2>
<p>The data model is the classic "IFTTT" trio. A <strong>Trigger</strong> defines "<strong>when</strong>": <code>eventSource</code> (which object, e.g. trace, prompt) + <code>eventActions</code> (which change, e.g. created/updated/deleted) + <code>filter</code> (extra conditions). An <strong>Action</strong> defines "<strong>what to do</strong>": <code>type</code> (WEBHOOK / SLACK / GITHUB_DISPATCH) + <code>config</code> (e.g. a webhook's url/method/headers/secretId). An <strong>Automation</strong> binds one Trigger to one Action. Every firing leaves an <strong>AutomationExecution</strong> record (status, input, output, error).</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="Automation model: an event happens, the Trigger decides whether it matches by eventSource/eventActions/filter, on match it fires the Action (WEBHOOK/SLACK/GITHUB_DISPATCH), and each run leaves an AutomationExecution record">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">When X happens (Trigger) → do Y (Action)</text>
  <rect x="20" y="80" width="120" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="80" y="100" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">an event</text><text x="80" y="116" text-anchor="middle" font-size="6.4" fill="var(--muted)">alert / prompt change / new trace</text>
  <rect x="170" y="68" width="160" height="74" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="250" y="88" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">Trigger (when)</text><text x="250" y="105" text-anchor="middle" font-size="6.4" fill="var(--muted)">eventSource: trace/prompt</text><text x="250" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">eventActions: created/updated</text><text x="250" y="131" text-anchor="middle" font-size="6.4" fill="var(--muted)">filter: extra cond · status ACTIVE</text>
  <rect x="360" y="62" width="170" height="40" rx="9" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="445" y="80" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">Action (what)</text><text x="445" y="94" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">WEBHOOK / SLACK / GITHUB_DISPATCH</text>
  <rect x="360" y="110" width="170" height="34" rx="8" fill="var(--bg)" stroke="var(--faint)"/><text x="445" y="127" text-anchor="middle" font-size="6.8" fill="var(--muted)">config: { url, method, headers, secretId }</text><text x="445" y="138" text-anchor="middle" font-size="6.0" fill="var(--faint)">structured config per type</text>
  <rect x="560" y="76" width="140" height="60" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="630" y="96" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">AutomationExecution</text><text x="630" y="113" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">status: PENDING→COMPLETED/ERROR</text><text x="630" y="126" text-anchor="middle" font-size="6.2" fill="var(--muted)">input/output/error kept</text>
  <line x1="140" y1="105" x2="168" y2="105" stroke="var(--teal)" stroke-width="1.4"/><polygon points="168,105 159,101 159,109" fill="var(--teal)"/>
  <line x1="330" y1="95" x2="358" y2="85" stroke="var(--blue)" stroke-width="1.4"/><polygon points="358,85 349,84 351,92" fill="var(--blue)"/><text x="345" y="78" text-anchor="middle" font-size="6" fill="var(--blue)">on match</text>
  <line x1="530" y1="92" x2="558" y2="100" stroke="var(--accent)" stroke-width="1.4"/><polygon points="558,100 549,97 550,105" fill="var(--accent)"/>
  <text x="360" y="172" text-anchor="middle" font-size="8" fill="var(--faint)">An Automation binds one Trigger to one Action; this is exactly where Lesson 33's alert goes "after publishing to WebhookQueue" — delivered by some webhook Action</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">AutomationExecution is like Lesson 30's JobExecution and Lesson 32's annotation item — yet another "persisted execution record" state machine</text>
</svg>
<div class="figcap"><b>The IFTTT Trigger → Action model</b>: <code>schema.prisma:1635</code> Trigger (eventSource/eventActions/filter/status), <code>:1613</code> Action (type WEBHOOK/SLACK/GITHUB_DISPATCH + config Json), <code>:1659</code> Automation (binds the two), <code>:1690</code> AutomationExecution (PENDING/COMPLETED/ERROR/CANCELLED + input/output/error). Lesson 33's monitor alerts are delivered through exactly this path.</div>
</div>

<div class="layers">
  <div class="layer l-main"><div class="lh"><span class="badge">when</span><span class="name">Trigger</span></div><div class="ld">Watches the event stream: <code>eventSource</code> (which object class) + <code>eventActions</code> (which change) + <code>filter</code> (finer conditions, same filtering as Lesson 23). Only fires when <code>status=ACTIVE</code> — you can pause it anytime without deleting.</div></div>
  <div class="layer l-core"><div class="lh"><span class="badge">what</span><span class="name">Action</span></div><div class="ld">Three action types: <strong>WEBHOOK</strong> (call the user's URL, this lesson's focus), <strong>SLACK</strong> (post to a channel, Lesson 45), <strong>GITHUB_DISPATCH</strong> (trigger a GitHub workflow). <code>config</code> stores each one's params as structured JSON; <code>secretId</code> points to an encrypted-at-rest secret (Lesson 39).</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">audit</span><span class="name">AutomationExecution</span></div><div class="ld">Every firing writes a row: a state machine PENDING→COMPLETED/ERROR/CANCELLED, storing <code>input</code>/<code>output</code>/<code>error</code> too — the same kind of "stateful, traceable execution record" as Lesson 30's JobExecution and Lesson 32's annotation item.</div></div>
</div>
""")

_EN44.append(r"""
<h2>The webhook's Achilles heel: defense in depth stops SSRF</h2>
<p>The WEBHOOK Action is, in essence, "make Langfuse's server fetch a <strong>user-supplied URL</strong>." That's the classic breeding ground for <strong>SSRF (Server-Side Request Forgery)</strong>: an attacker sets the URL to <code>http://169.254.169.254/...</code> (the cloud metadata endpoint, which yields your temporary AK/SK) or <code>http://localhost:6379</code> (your internal Redis), reaching — through your server's hands — things it should never reach. Langfuse's defense isn't one wall but <strong>layer upon layer of gates</strong> — if any one leaks, the next still holds.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="webhook SSRF defense in depth: a user-supplied URL must pass in order a protocol allowlist (http/https only), a port allowlist (80/443 only), a hostname blocklist (localhost/metadata), an IP CIDR blocklist (private/loopback/link-local), and fail-closed on unparseable; only if all pass is the request sent, otherwise rejected">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">The user URL must clear five gates; only all-pass is let through</text>
  <rect x="20" y="44" width="120" height="150" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="80" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">user-supplied URL</text><text x="80" y="84" text-anchor="middle" font-size="6.2" fill="var(--muted)">legit:</text><text x="80" y="96" text-anchor="middle" font-size="5.8" fill="var(--teal)">https://hooks.x.com/…</text><text x="80" y="120" text-anchor="middle" font-size="6.2" fill="var(--muted)">malicious:</text><text x="80" y="132" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">http://169.254.169.254</text><text x="80" y="144" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">http://localhost:6379</text><text x="80" y="156" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">file:///etc/passwd</text>
  <rect x="165" y="44" width="100" height="44" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="215" y="62" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">gate1 protocol</text><text x="215" y="76" text-anchor="middle" font-size="6.0" fill="var(--muted)">http/https only</text>
  <rect x="165" y="96" width="100" height="44" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="215" y="114" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">gate2 port</text><text x="215" y="128" text-anchor="middle" font-size="6.0" fill="var(--muted)">80 / 443 only</text>
  <rect x="165" y="148" width="100" height="44" rx="7" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="215" y="166" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--ink)">gate3 hostname</text><text x="215" y="180" text-anchor="middle" font-size="5.6" fill="var(--muted)">block localhost/metadata</text>
  <rect x="290" y="70" width="110" height="44" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="345" y="88" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">gate4 IP range</text><text x="345" y="102" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">block private/loopback/link-local</text>
  <rect x="290" y="124" width="110" height="44" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="345" y="142" text-anchor="middle" font-size="7.5" font-weight="700" fill="var(--accent-ink)">gate5 fail-closed</text><text x="345" y="156" text-anchor="middle" font-size="5.6" fill="var(--accent-ink)">can't resolve? block it</text>
  <rect x="430" y="80" width="120" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="490" y="100" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">all pass → send</text><text x="490" y="116" text-anchor="middle" font-size="6.0" fill="var(--muted)">with timeout/retry/signature</text>
  <rect x="430" y="146" width="120" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="490" y="164" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">any fail → reject</text><text x="490" y="178" text-anchor="middle" font-size="6.0" fill="var(--muted)">malicious URLs all blocked</text>
  <rect x="580" y="100" width="120" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="640" y="120" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">external receiver</text><text x="640" y="136" text-anchor="middle" font-size="6.0" fill="var(--muted)">verifies it's from Langfuse</text>
  <line x1="140" y1="115" x2="163" y2="100" stroke="var(--faint)" stroke-width="1"/><line x1="265" y1="92" x2="288" y2="100" stroke="var(--faint)" stroke-width="1"/><line x1="400" y1="120" x2="428" y2="115" stroke="var(--accent)" stroke-width="1.3"/><polygon points="428,115 419,112 420,120" fill="var(--accent)"/><line x1="550" y1="110" x2="578" y2="120" stroke="var(--teal)" stroke-width="1.3"/><polygon points="578,120 569,117 570,125" fill="var(--teal)"/>
  <text x="360" y="216" text-anchor="middle" font-size="8" fill="var(--faint)">Key: the IP check runs "at request time" on the actually-resolved IP, defeating DNS-rebinding (resolve to a legit IP first, switch to an internal IP at the last second)</text>
</svg>
<div class="figcap"><b>Defense in depth, gate after gate</b>: <code>validateWebhookURL</code> (<code>validation.ts:35</code>) allows only http/https and only ports 80/443; <code>ipBlocking.ts</code>'s <code>isHostnameBlocked</code> blocks localhost / <code>metadata.google.internal</code> / <code>169.254.169.254</code>, and <code>isIPBlocked</code> blocks RFC1918 private ranges, loopback, link-local and other CIDRs, <b>and defaults to blocking when IP resolution fails</b> (fail-closed). The check runs at request time on the real IP, defeating DNS-rebinding.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/webhooks/ipBlocking.ts · validation.ts</span><span class="ln">SSRF defense</span></div>
  <pre class="code"><span class="cm">// gate4: blocklisted CIDRs — private, loopback, and the link-local cloud metadata range</span>
<span class="kw">const</span> BLOCKED_CIDRS = [<span class="st">"10.0.0.0/8"</span>, <span class="st">"127.0.0.0/8"</span>, <span class="st">"169.254.0.0/16"</span><span class="cm">/* AWS/GCP metadata */</span>,
                       <span class="st">"172.16.0.0/12"</span>, <span class="st">"192.168.0.0/16"</span>, <span class="st">"::1/128"</span>, …];
<span class="kw">export function</span> <span class="fn">isIPBlocked</span>(ip) { <span class="cm">/* in any range → true; resolution fails → also true (rather block) */</span> }

<span class="cm">// gate3: hostname blocklist — even the domain name is forbidden</span>
<span class="kw">const</span> blockedPatterns = [<span class="st">"localhost"</span>, <span class="st">"*.localhost"</span>,
  <span class="st">"metadata.google.internal"</span>, <span class="st">"169.254.169.254"</span>, …];   <span class="cm">// cloud metadata endpoints</span>

<span class="cm">// gate1+2: protocol and port allowlists (validation.ts)</span>
<span class="kw">if</span> (!<span class="st">["http:", "https:"]</span>.includes(protocol)) <span class="kw">throw</span> <span class="st">"Only HTTP and HTTPS allowed"</span>;
<span class="kw">if</span> (![<span class="st">80, 443</span>].includes(port))            <span class="kw">throw</span> <span class="st">"Only ports 80 and 443 allowed"</span>;</pre>
</div>

<div class="cols">
  <div class="col"><h4>☁️ cloud metadata endpoint</h4><p><code>169.254.169.254</code> / <code>metadata.google.internal</code> — AWS/GCP instance metadata. The deadliest: yields the machine's <strong>temporary cloud credentials (AK/SK)</strong> and from there takeover of the whole cloud account. Blocked <strong>twice</strong>: hostname blocklist + link-local CIDR (<code>169.254.0.0/16</code>).</p></div>
  <div class="col"><h4>🔌 internal services</h4><p><code>localhost:6379</code> Redis, internal admin panels, databases… often undefended on the assumption "it's internal anyway." Blocked by loopback (<code>127.0.0.0/8</code>) + RFC1918 (<code>10/8</code>, <code>172.16/12</code>, <code>192.168/16</code>) CIDR blocklist.</p></div>
  <div class="col"><h4>📄 non-HTTP protocols</h4><p><code>file:///etc/passwd</code> to read local files, <code>gopher://</code> to hit other TCP services… killed at the source by the <strong>protocol allowlist</strong> (http/https only) — it never even reaches IP resolution.</p></div>
</div>
""")

_EN44.append(r"""
<h2>Beyond SSRF: delivery must be reliable and trustworthy</h2>
<p>Blocking SSRF only gets you "no disaster." To make webhooks truly <strong>reliable and trustworthy</strong>, the delivery path needs several more operational hardenings — together they form the complete engineering posture for "calling the outside world":</p>

<table class="t">
  <thead><tr><th>Hardening</th><th>How</th><th>Guards against</th></tr></thead>
  <tbody>
    <tr><td><b>SSRF defense</b></td><td>protocol/port allowlist + IP/hostname blocklist + fail-closed (previous section)</td><td>using your server to hit the internal net, steal cloud creds</td></tr>
    <tr><td><b>Signing</b></td><td>HMAC the payload with a secret, put it in <code>x-langfuse-signature</code></td><td>receiver can verify — confirm it really came from Langfuse, untampered</td></tr>
    <tr><td><b>Timeout</b></td><td><code>AbortController</code> + <code>LANGFUSE_WEBHOOK_TIMEOUT_MS</code></td><td>a slow/hung peer dragging down the worker</td></tr>
    <tr><td><b>Retry</b></td><td><code>backOff</code> exponential backoff</td><td>eventual delivery through a peer's transient blip</td></tr>
    <tr><td><b>Status check</b></td><td>require a 2xx, else record ERROR</td><td>silent failures counted as success</td></tr>
    <tr><td><b>Auto-disable</b></td><td>a repeatedly-failing trigger gets disabled</td><td>hammering a dead endpoint forever</td></tr>
  </tbody>
</table>

<p>Read that table and a clear engineering creed emerges: <strong>anything that "issues a request to the outside world" must be treated as untrusted and unreliable</strong>. An external URL may be malicious (→ SSRF defense), may be slow (→ timeout), may blip (→ retry), may be permanently down (→ auto-disable); and what you send out, the peer in turn needs to confirm actually came from you (→ signing). Each guard corresponds to a concrete hypothesis about "how the outside world will hurt you" — <strong>security and robustness are never one switch, but a stack of specific defenses against specific threats</strong>.</p>
""")

_EN44.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why does SSRF warrant so many layers of defense? How dangerous is it, really?</strong> Because it can turn a seemingly harmless feature ("we'll call a URL back for you") into a <strong>tunnel straight into your network's core</strong>. The deadliest target is <code>169.254.169.254</code> — AWS/GCP's <strong>instance metadata endpoint</strong>: anyone who can make your server fetch it may obtain the machine's <strong>temporary cloud credentials (AK/SK)</strong> and from there take over your entire cloud account. Next come internal services: your Redis, internal admin panels, databases — often <strong>undefended</strong> on the assumption "it's internal anyway." Once an attacker can use your webhook's hands to reach them, that "internal = safe" assumption collapses. SSRF is terrifying precisely because it <strong>bypasses every boundary</strong>: a firewall blocks what comes in from outside, but SSRF <strong>attacks outward from inside you</strong>, unimpeded. So it earns defense in depth — and every gate must be <strong>fail-closed</strong>: anything uncertain or unparseable is <strong>treated as dangerous</strong>. The default answer of secure code is "deny," not "allow."<br><br>
  <strong>Why run the check "at request time" on the resolved real IP, instead of validating the URL once at webhook-creation time?</strong> Because of an insidious attack called <strong>DNS-rebinding</strong>: the attacker controls a domain, resolves it to a legitimate public IP <strong>at creation time</strong> (passing review smoothly), then <strong>at the last second when Langfuse actually sends the request</strong> flips that domain to resolve to <code>169.254.169.254</code> or an internal IP. If you only validate at creation, this sleight of hand fools you. Langfuse pushes the IP check down to <strong>the very moment the request is issued</strong>, judging the <strong>IP actually resolved then</strong> — no matter how the attacker swaps DNS, the real IP at that instant can't slip past this gate. <strong>Security checks must hug "the moment the truly dangerous action happens," not be done early on a possibly-stale snapshot.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Automation = Trigger → Action</strong>: the classic IFTTT model. A <code>Trigger</code> (eventSource/eventActions/filter defines "when") binds an <code>Action</code> (WEBHOOK/SLACK/GITHUB_DISPATCH defines "what"); <code>AutomationExecution</code> keeps a status record of each run. Lesson 33's monitor alerts are delivered through this.</li>
    <li><strong>The webhook's Achilles heel is SSRF</strong>: making the server fetch a user-supplied URL lets an attacker hit the internal net and steal <code>169.254.169.254</code>'s cloud credentials — "user gives a URL, we fetch it" is one of the most dangerous web features.</li>
    <li><strong>Defense in depth stops SSRF</strong>: protocol allowlist (http/https) + port allowlist (80/443) + hostname blocklist (localhost/metadata) + IP CIDR blocklist (private/loopback/link-local) + <strong>fail-closed</strong> (can't resolve → block). Any one gate may be the lifesaver.</li>
    <li><strong>Check at request time</strong>: judge the actually-resolved real IP to defeat DNS-rebinding (resolve to a legit IP at creation, switch to internal at request). Security checks hug the moment the danger happens.</li>
    <li><strong>Delivery must be reliable and trustworthy too</strong>: HMAC signing (<code>x-langfuse-signature</code>, lets the receiver verify) + timeout + exponential-backoff retry + 2xx check + auto-disable on repeated failure — treat every outbound request as untrusted and unreliable.</li>
  </ul>
</div>
""")

LESSON_44 = {"zh": "\n".join(_ZH44), "en": "\n".join(_EN44)}
