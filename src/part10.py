"""Part 10 — 平台与运维 / Platform & Operations. Lessons L48–L53.

Same authoring pattern as part1..part9: each lesson assembles its bilingual body
from ``_ZHn`` / ``_ENn`` section lists, then exports ``LESSON_NN = {"zh","en"}``.
All technical claims are grounded in the real langfuse/langfuse source.
"""

# ══════════════════════════════════════════════════════════════════════
# L48 · 鉴权与会话 / Auth & sessions
# ══════════════════════════════════════════════════════════════════════
_ZH48 = []
_EN48 = []

# (L48 sections below)

_ZH48.append(r"""
<p class="lead">
从这一部分起，我们换上<strong>运维者</strong>的视角，看这个平台自己是怎么被「管」起来的。第一个问题最根本：<strong>谁能进来？</strong> 这一课讲鉴权（authentication，「你是谁」）与会话（session，「进来后这张身份凭证怎么发、怎么带」）。Langfuse 用 <strong>NextAuth</strong> 托管登录，给你两条进门的路：<strong>邮箱密码</strong>，或十几种 <strong>SSO（单点登录）</strong>提供商（Google、GitHub、Okta、Azure AD、Keycloak、WorkOS…）。登进来后，它发的不是一个数据库 session id，而是一张 <strong>JWT</strong>——自带签名、自带身份信息的「凭证」。
最妙的是登录成功那一刻的 <strong>session 回调</strong>：它顺手把你所属的<strong>组织/项目成员关系</strong>查出来塞进会话——这正是下一课 RBAC（你能干什么）的<strong>输入</strong>。这一课还藏着几处教科书级的安全细节，比如「用户不存在也照样算一遍密码哈希」防的是什么。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  鉴权就像<strong>进一栋写字楼</strong>。门口前台要先确认「你是你」：要么你<strong>自报家门 + 出示密码</strong>（邮箱密码登录），要么你亮出一张<strong>可信第三方发的证件</strong>——比如政府身份证、公司工牌（这就是 SSO：把「证明你是谁」外包给 Google/Okta 这些可信机构，前台只认它们的背书）。
  确认身份后，前台给你一张<strong>访客牌</strong>。这张牌有两种做法：一种是牌上只印个编号，你每次刷门都得让前台<strong>翻登记簿查这编号对应谁</strong>（数据库 session，每次校验都查库）；另一种是牌上<strong>直接印好你的姓名、所属部门，还压了防伪钢印</strong>，门禁一扫即知、无需回前台查（这就是 <strong>JWT</strong>：自带信息 + 签名防篡改）。Langfuse 用的是后者。而且发牌那一刻，前台特意在牌背面写清你<strong>是哪几个部门/项目的成员</strong>——下一课的门禁（RBAC）就靠读这行字，决定你能推开哪些门。
</div>
""")

# (L48 sec1 below)

_ZH48.append(r"""
<h2>两条进门的路：密码与 SSO</h2>
<p>Langfuse 用 <strong>NextAuth</strong>（next-auth）作为鉴权框架，在 <code>auth.ts</code> 里注册了一长串 <strong>provider（登录方式）</strong>：一个 <strong>CredentialsProvider</strong>（邮箱密码）、一个 <strong>EmailProvider</strong>（邮件魔法链接），外加十几种 <strong>SSO</strong>——Google、GitHub、GitLab、Okta、Authentik、OneLogin、Auth0、Cognito、Azure AD、Keycloak、WorkOS、WordPress。SSO 的意义是把「证明你是谁」<strong>外包</strong>给企业已经信任的身份提供商（IdP），员工不用再记一套新密码。这些 provider 分两类来源：<strong>静态</strong>（由环境变量配好）和<strong>动态</strong>（从数据库读取、运行时合并进来），后者让多租户云上的每个组织能配自己的 SSO。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="鉴权入口：用户从两条路进门，邮箱密码(CredentialsProvider，bcrypt校验)或十几种SSO提供商(Google/GitHub/Okta/AzureAD等，外包给可信IdP)，都汇入NextAuth，校验通过后发JWT会话；SSO可被强制(实例级/域名级/EE多租户)">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">谁能进来：两条路汇入 NextAuth</text>
  <rect x="30" y="50" width="160" height="60" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="110" y="70" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① 邮箱密码</text><text x="110" y="86" text-anchor="middle" font-size="6.4" fill="var(--muted)">CredentialsProvider</text><text x="110" y="98" text-anchor="middle" font-size="6.2" fill="var(--muted)">bcrypt 校验（本课重点）</text>
  <rect x="30" y="130" width="160" height="78" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)" stroke-width="2"/><text x="110" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">② SSO（十几种）</text><text x="110" y="166" text-anchor="middle" font-size="6.2" fill="var(--muted)">Google/GitHub/Okta</text><text x="110" y="178" text-anchor="middle" font-size="6.2" fill="var(--muted)">Azure AD/Keycloak/WorkOS…</text><text x="110" y="192" text-anchor="middle" font-size="6.0" fill="var(--faint)">外包给可信 IdP，不记新密码</text>
  <rect x="280" y="92" width="170" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="365" y="114" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">NextAuth</text><text x="365" y="131" text-anchor="middle" font-size="6.4" fill="var(--muted)">统一鉴权框架</text><text x="365" y="144" text-anchor="middle" font-size="6.4" fill="var(--muted)">static + dynamic provider</text><text x="365" y="156" text-anchor="middle" font-size="6.0" fill="var(--faint)">扩展 PrismaAdapter 落库</text>
  <rect x="540" y="100" width="160" height="58" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="620" y="122" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">发 JWT 会话</text><text x="620" y="138" text-anchor="middle" font-size="6.2" fill="var(--muted)">自带签名 + 身份信息</text><text x="620" y="150" text-anchor="middle" font-size="6.0" fill="var(--faint)">下一节细讲</text>
  <line x1="190" y1="92" x2="278" y2="116" stroke="var(--blue)" stroke-width="1.4"/><polygon points="278,116 269,114 271,122" fill="var(--blue)"/>
  <line x1="190" y1="160" x2="278" y2="140" stroke="var(--teal)" stroke-width="1.4"/><polygon points="278,140 269,140 273,148" fill="var(--teal)"/>
  <line x1="450" y1="128" x2="538" y2="128" stroke="var(--accent)" stroke-width="1.4"/><polygon points="538,128 529,124 529,132" fill="var(--accent)"/>
  <rect x="280" y="186" width="170" height="48" rx="8" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="365" y="204" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">SSO 可被强制</text><text x="365" y="218" text-anchor="middle" font-size="6.0" fill="var(--muted)">实例级 / 域名级 / EE 多租户</text><text x="365" y="228" text-anchor="middle" font-size="5.8" fill="var(--faint)">禁掉密码登录、必须走 SSO</text>
  <line x1="365" y1="166" x2="365" y2="184" stroke="var(--faint)" stroke-width="1" stroke-dasharray="2 2"/>
</svg>
<div class="figcap"><b>登录入口</b>：<code>auth.ts:24-38</code> 导入 14 种 provider（Credentials/Email + 12 SSO）。静态 provider 由 env 配置，动态 SSO provider 运行时从库读取并合并（<code>auth.ts:739</code> 附近 <code>[...staticProviders, ...dynamicSsoProviders]</code>）。可强制 SSO：<code>AUTH_DISABLE_USERNAME_PASSWORD</code>（实例级）、<code>getSSOBlockedDomains()</code>（域名级）、<code>getSsoAuthProviderIdForDomain</code>（EE 多租户）。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">自有</span><span class="name">CredentialsProvider（邮箱密码）</span></div><div class="ld">最基础的一条路：用户名+密码。密码用 <strong>bcrypt</strong> 加盐哈希存库，登录时比对。下一节会看到它周围一圈安全护栏（SSO 强制、时序攻击防护、SSO 用户拦截）。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">外包</span><span class="name">SSO 提供商（十几种）</span></div><div class="ld">把「证明身份」交给企业已信任的 IdP。员工用已有的 Google/Okta/Azure 账号一键登入，不必再设新密码——既省心又更安全（IdP 那边通常有 MFA、统一注销等企业级管控）。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">落库</span><span class="name">扩展 PrismaAdapter</span></div><div class="ld">NextAuth 用 <code>PrismaAdapter</code> 把用户/账号关系存进 Postgres，Langfuse 还<strong>包了一层</strong>（<code>extendedPrismaAdapter</code>）定制账号绑定/字段清洗逻辑——把第三方 IdP 的用户安全地落到自己的 User 表。</div></div>
</div>
""")

# (L48 sec2 below)

_ZH48.append(r"""
<h2>密码登录的一圈安全护栏</h2>
<p>别小看「邮箱密码」这条最朴素的路——它的 <code>authorize</code> 函数里藏着一圈值得细品的安全设计。<strong>先是三道 SSO 强制闸</strong>：实例级禁用密码登录（<code>AUTH_DISABLE_USERNAME_PASSWORD</code>）、域名级黑名单（某些公司域名必须走 SSO）、EE 多租户强制（某域名配了专属 SSO 就不许用密码）。<strong>再是一处教科书级的时序攻击防护</strong>：万一用户不存在，代码<strong>照样跑一遍密码哈希</strong>再报错——这样「用户不存在」和「密码错」两条失败路径耗时相近，攻击者就<strong>没法靠响应快慢来探测某个邮箱是否注册过</strong>。<strong>还有一处</strong>：若用户的 <code>password</code> 字段是 null，说明 ta 是用 SSO 注册的，明确提示「请用你绑定的 IdP 登录」。全过了才用 <strong>bcrypt</strong> 比对密码。</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>SSO 强制三连查</h4><p>实例禁密码？域名在 SSO 黑名单？该域名配了 EE 专属 SSO？——命中任一条，直接拒绝并提示走 SSO。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>查用户 + 时序防护</h4><p>按邮箱查 User。<strong>查不到也照算一遍 <code>hashPassword</code></strong> 再报「Invalid credentials」——让失败耗时恒定，堵住「靠响应快慢枚举注册邮箱」的旁路。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>SSO 用户拦截</h4><p>若 <code>dbUser.password === null</code>，此人是 SSO 注册的、本就没密码——明确引导「请用绑定的身份提供商登录」，而非含糊报错。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>bcrypt 比对</h4><p><code>verifyPassword</code> 用 bcrypt <code>compare</code> 比对（存储时 <code>hash(password, 12)</code> 12 轮加盐）。不符即「Invalid credentials」。全过才放行。</p></div></div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/auth.ts · credentialsServerUtils.ts</span><span class="ln">authorize 安全护栏</span></div>
  <pre class="code"><span class="kw">async</span> <span class="fn">authorize</span>(credentials) {
  <span class="cm">// 1) SSO 强制：实例级 / 域名级 / EE 多租户</span>
  <span class="kw">if</span> (env.AUTH_DISABLE_USERNAME_PASSWORD === <span class="st">"true"</span>) <span class="kw">throw</span> <span class="st">"… use SSO"</span>;
  <span class="kw">if</span> (getSSOBlockedDomains().includes(domain))         <span class="kw">throw</span> <span class="st">"… use SSO"</span>;
  <span class="kw">if</span> (<span class="kw">await</span> <span class="fn">getSsoAuthProviderIdForDomain</span>(domain))     <span class="kw">throw</span> ENTERPRISE_SSO_REQUIRED_MESSAGE;

  <span class="kw">const</span> dbUser = <span class="kw">await</span> prisma.user.<span class="fn">findUnique</span>({ where: { email: email.toLowerCase() } });
  <span class="kw">if</span> (!dbUser) {
    <span class="kw">await</span> <span class="fn">hashPassword</span>(credentials.password);  <span class="cm">// 用户不存在也算一遍哈希 → 防时序枚举</span>
    <span class="kw">throw</span> <span class="st">"Invalid credentials"</span>;
  }
  <span class="kw">if</span> (dbUser.password === <span class="kw">null</span>) <span class="kw">throw</span> <span class="st">"Please sign in with your identity provider…"</span>;  <span class="cm">// SSO 用户</span>

  <span class="kw">const</span> ok = <span class="kw">await</span> <span class="fn">verifyPassword</span>(credentials.password, dbUser.password);  <span class="cm">// bcrypt compare</span>
  <span class="kw">if</span> (!ok) <span class="kw">throw</span> <span class="st">"Invalid credentials"</span>;
  <span class="kw">return</span> userObj;   <span class="cm">// 通过 → NextAuth 据此发会话</span>
}

<span class="cm">// credentialsServerUtils.ts：bcrypt 12 轮加盐</span>
<span class="kw">export async function</span> <span class="fn">hashPassword</span>(pw) { <span class="kw">return</span> <span class="fn">hash</span>(pw, <span class="st">12</span>); }
<span class="kw">export async function</span> <span class="fn">verifyPassword</span>(pw, hashed) { <span class="kw">return</span> <span class="fn">compare</span>(pw, hashed); }</pre>
</div>
""")

# (L48 sec3 below)

_ZH48.append(r"""
<h2>会话 = JWT + 一次「身份注入」</h2>
<p>登录通过后，NextAuth 发的是一张 <strong>JWT</strong>（<code>session.strategy: "jwt"</code>），有效期 <code>maxAge = AUTH_SESSION_MAX_AGE × 60</code> 秒。JWT 的好处是<strong>无状态</strong>：凭证本身带着签名和身份信息，服务端验签即可，不必每次请求都查一遍 session 表——这对要水平扩展的多实例部署尤其友好。真正的点睛之笔在 <strong>session 回调</strong>：每次构建会话时，它按邮箱查出该用户的 <code>organizationMemberships → projects</code> 和 <code>ProjectMemberships</code>，<strong>把「你属于哪些组织、哪些项目、是什么角色」一并塞进 session 对象</strong>。这一步，正是把「你是谁」（本课鉴权）接到「你能干什么」（下一课 RBAC）的<strong>那根线</strong>——下一课的 <code>throwIfNoProjectAccess</code> 读的就是这里注入的成员关系与角色。</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="JWT会话流：登录通过后NextAuth发JWT(无状态、自带签名和身份、maxAge过期)，session回调每次构建会话时查出用户的组织成员关系organizationMemberships→projects和ProjectMemberships注入session，成为下一课RBAC的输入">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">发 JWT + 注入成员关系 → 接到 RBAC</text>
  <rect x="30" y="70" width="140" height="56" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="100" y="90" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">登录通过</text><text x="100" y="106" text-anchor="middle" font-size="6.2" fill="var(--muted)">密码或 SSO</text><text x="100" y="117" text-anchor="middle" font-size="6.0" fill="var(--faint)">authorize 返回 user</text>
  <rect x="200" y="62" width="160" height="72" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="280" y="82" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">发 JWT 会话</text><text x="280" y="98" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">strategy: "jwt"（无状态）</text><text x="280" y="110" text-anchor="middle" font-size="6.2" fill="var(--muted)">自带签名 + 身份信息</text><text x="280" y="123" text-anchor="middle" font-size="6.0" fill="var(--faint)">maxAge 过期即失效</text>
  <rect x="390" y="50" width="180" height="96" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="480" y="70" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">session 回调（注入身份）</text><text x="480" y="87" text-anchor="middle" font-size="6.2" fill="var(--muted)">查 organizationMemberships</text><text x="480" y="99" text-anchor="middle" font-size="6.2" fill="var(--muted)">→ projects（未删的）</text><text x="480" y="111" text-anchor="middle" font-size="6.2" fill="var(--muted)">+ ProjectMemberships</text><text x="480" y="127" text-anchor="middle" font-size="6.0" fill="var(--faint)">「属于哪些组织/项目·什么角色」</text><text x="480" y="138" text-anchor="middle" font-size="6.0" fill="var(--faint)">一并塞进 session</text>
  <rect x="600" y="74" width="100" height="50" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="650" y="94" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">→ 第49课 RBAC</text><text x="650" y="110" text-anchor="middle" font-size="5.8" fill="var(--muted)">据角色判 scope</text>
  <line x1="170" y1="98" x2="198" y2="98" stroke="var(--teal)" stroke-width="1.4"/><polygon points="198,98 189,94 189,102" fill="var(--teal)"/>
  <line x1="360" y1="98" x2="388" y2="98" stroke="var(--accent)" stroke-width="1.4"/><polygon points="388,98 379,94 379,102" fill="var(--accent)"/>
  <line x1="570" y1="98" x2="598" y2="98" stroke="var(--blue)" stroke-width="1.4"/><polygon points="598,98 589,94 589,102" fill="var(--blue)"/>
  <text x="360" y="170" text-anchor="middle" font-size="8" fill="var(--faint)">JWT 无状态 = 可水平扩展（验签即可，不必每请求查 session 表）；session 回调把鉴权结果「翻译」成 RBAC 的输入</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">这个 session 回调用 instrumentAsync 包裹（第51课的 OTel 包装器）——平台连自己的登录都在自观测</text>
</svg>
<div class="figcap"><b>JWT + 身份注入</b>：<code>auth.ts:743</code> <code>session.strategy:"jwt"</code>、<code>:744</code> <code>maxAge:AUTH_SESSION_MAX_AGE*60</code>；session 回调（<code>:747</code> 起）查 <code>organizationMemberships</code>（含未删 <code>projects</code>，按 createdAt desc）+ <code>ProjectMemberships</code> 注入 session。回调体被 <code>instrumentAsync("next-auth-session")</code> 包裹（自观测，见第 51 课）。</div>
</div>

<table class="t">
  <thead><tr><th>会话做法</th><th>数据库 session（牌上印编号）</th><th>JWT（牌上印信息+钢印）← Langfuse</th></tr></thead>
  <tbody>
    <tr><td>每次请求</td><td>拿 id 回数据库查一遍</td><td>本地验签即可，<b>无需查库</b></td></tr>
    <tr><td>水平扩展</td><td>多实例需共享 session 存储</td><td><b>天然友好</b>：任一实例独立验签</td></tr>
    <tr><td>即时吊销</td><td>删库里那行即刻失效</td><td>较难（需等过期或额外黑名单机制）</td></tr>
    <tr><td>身份信息</td><td>查库时一并取</td><td><b>session 回调</b>注入组织/项目成员关系</td></tr>
  </tbody>
</table>
""")

_ZH48.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么用 JWT 无状态会话，而不是传统的数据库 session？</strong> 核心是<strong>可扩展性</strong>。数据库 session 的做法是：发一个随机 id 给浏览器，服务端把「这个 id 对应哪个用户」存进库，之后每次请求都拿 id <strong>回库查一遍</strong>。这在单机上没问题，但 Langfuse 要跑<strong>多个 web 实例</strong>横向扩展——若用 DB session，每个实例每次请求都得访问共享的 session 存储，它就成了瓶颈和单点。JWT 把身份信息<strong>直接印在凭证里、用密钥签名防篡改</strong>，任何一个实例<strong>本地验签</strong>就能确认「你是谁」，无需回头查库——这正是无状态架构能水平扩展的关键。代价是<strong>即时吊销变难</strong>（凭证已发出去就在有效期内一直有效），所以 JWT 会配一个不太长的 <code>maxAge</code>，用「短有效期 + 到期重签」来折中。<strong>无状态换来了扩展性，用有效期换回了一部分可控性。</strong><br><br>
  <strong>「用户不存在也照样跑一遍密码哈希」这种看似浪费的代码，到底在防什么？</strong> 防的是<strong>时序侧信道攻击（timing attack）</strong>下的<strong>用户枚举</strong>。bcrypt 故意很慢（12 轮）。如果「用户不存在」时直接报错返回、「用户存在但密码错」时才慢慢算一遍 bcrypt，那两条失败路径的<strong>响应时间会有可观差异</strong>——攻击者拿一堆邮箱来试，<strong>响应快的就是没注册、响应慢的就是已注册</strong>，于是不费密码就摸清了「哪些邮箱在你这注册过」（这本身就是隐私泄露，也是后续撞库的弹药）。对策很简单却很专业：<strong>让两条失败路径耗时相近</strong>——用户不存在时也白算一遍 hash。安全工程里，<strong>「错误也要长得一样、慢得一样」</strong>，是一条容易被忽略却很重要的原则。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>鉴权 = 你是谁</strong>：NextAuth 托管，两条进门路——CredentialsProvider（邮箱密码）+ 十几种 SSO（Google/Okta/Azure AD/Keycloak/WorkOS…，把「证明身份」外包给可信 IdP）。provider 有静态(env)与动态(DB)两源。</li>
    <li><strong>密码登录的安全护栏</strong>：SSO 强制三道闸（实例级 <code>AUTH_DISABLE_USERNAME_PASSWORD</code> / 域名黑名单 / EE 多租户）；<strong>时序攻击防护</strong>（用户不存在也跑一遍 bcrypt 防枚举）；SSO 用户拦截（password=null 引导走 IdP）；最后 bcrypt(12 轮) 比对。</li>
    <li><strong>会话 = JWT</strong>：<code>strategy:"jwt"</code> 无状态、自带签名与身份、<code>maxAge</code> 过期。相比 DB session，天然适合多实例水平扩展（本地验签免查库），代价是即时吊销较难（用短有效期折中）。</li>
    <li><strong>session 回调注入身份</strong>：构建会话时查 <code>organizationMemberships→projects</code> + <code>ProjectMemberships</code> 塞进 session——这是把「你是谁」接到下一课「你能干什么」(RBAC) 的那根线。</li>
    <li><strong>连登录都自观测</strong>：session 回调用 <code>instrumentAsync</code>（第 51 课的 OTel 包装器）包裹，给登录链路也挂上 span。平台对自己的可观测，无处不在。</li>
  </ul>
</div>
""")

_EN48.append(r"""
<p class="lead">
From this part on, we put on the <strong>operator's</strong> hat and look at how the platform itself is "managed." The first question is the most fundamental: <strong>who gets in?</strong> This lesson covers authentication ("who are you") and the session ("once in, how is that identity credential issued and carried"). Langfuse uses <strong>NextAuth</strong> to host login, giving you two ways in: <strong>email + password</strong>, or a dozen-plus <strong>SSO (single sign-on)</strong> providers (Google, GitHub, Okta, Azure AD, Keycloak, WorkOS…). Once in, it issues not a database session id but a <strong>JWT</strong> — a "credential" carrying its own signature and identity info.
The cleverest touch is the <strong>session callback</strong> at the moment of successful login: it conveniently queries your <strong>organization/project memberships</strong> and stuffs them into the session — exactly the <strong>input</strong> for the next lesson's RBAC (what you can do). This lesson also hides a few textbook security details, like what "hash the password even when the user doesn't exist" actually guards against.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Authentication is like <strong>entering an office building</strong>. The front desk must first confirm "you are you": either you <strong>state your name + show a password</strong> (email-password login), or you present a <strong>credential issued by a trusted third party</strong> — a government ID, a corporate badge (that's SSO: outsourcing "prove who you are" to trusted bodies like Google/Okta, and the front desk just trusts their endorsement).
  After confirming identity, the desk gives you a <strong>visitor badge</strong>. There are two ways to make this badge: one prints only a number, and every time you swipe a door the front desk must <strong>look up the registry to see whom that number maps to</strong> (database session, a DB lookup on every check); the other <strong>prints your name and department right on it, stamped with an anti-forgery seal</strong>, so the door scanner knows instantly without phoning the desk (that's <strong>JWT</strong>: self-carried info + a tamper-proof signature). Langfuse uses the latter. And at the moment of issuing the badge, the desk deliberately writes on the back <strong>which departments/projects you belong to</strong> — the next lesson's door access (RBAC) reads exactly that line to decide which doors you may push open.
</div>

<h2>Two ways in: password and SSO</h2>
<p>Langfuse uses <strong>NextAuth</strong> (next-auth) as its auth framework, registering a long list of <strong>providers (login methods)</strong> in <code>auth.ts</code>: one <strong>CredentialsProvider</strong> (email-password), one <strong>EmailProvider</strong> (magic-link email), plus a dozen-plus <strong>SSO</strong> — Google, GitHub, GitLab, Okta, Authentik, OneLogin, Auth0, Cognito, Azure AD, Keycloak, WorkOS, WordPress. The point of SSO is to <strong>outsource</strong> "prove who you are" to an identity provider (IdP) the enterprise already trusts, so employees don't memorize yet another password. These providers come from two sources: <strong>static</strong> (configured by env vars) and <strong>dynamic</strong> (read from the DB and merged at runtime), the latter letting each org on multi-tenant cloud configure its own SSO.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="Auth entry: a user enters via two paths, email-password (CredentialsProvider, bcrypt verify) or a dozen-plus SSO providers (Google/GitHub/Okta/AzureAD etc, outsourced to a trusted IdP), both flowing into NextAuth which issues a JWT session on success; SSO can be enforced (instance-level/domain-level/EE multi-tenant)">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Who gets in: two paths into NextAuth</text>
  <rect x="30" y="50" width="160" height="60" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="110" y="70" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--ink)">① email + password</text><text x="110" y="86" text-anchor="middle" font-size="6.4" fill="var(--muted)">CredentialsProvider</text><text x="110" y="98" text-anchor="middle" font-size="6.2" fill="var(--muted)">bcrypt verify (this lesson's focus)</text>
  <rect x="30" y="130" width="160" height="78" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)" stroke-width="2"/><text x="110" y="150" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--teal)">② SSO (a dozen-plus)</text><text x="110" y="166" text-anchor="middle" font-size="6.2" fill="var(--muted)">Google/GitHub/Okta</text><text x="110" y="178" text-anchor="middle" font-size="6.2" fill="var(--muted)">Azure AD/Keycloak/WorkOS…</text><text x="110" y="192" text-anchor="middle" font-size="6.0" fill="var(--faint)">outsourced to trusted IdP, no new password</text>
  <rect x="280" y="92" width="170" height="74" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="365" y="114" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">NextAuth</text><text x="365" y="131" text-anchor="middle" font-size="6.4" fill="var(--muted)">unified auth framework</text><text x="365" y="144" text-anchor="middle" font-size="6.4" fill="var(--muted)">static + dynamic providers</text><text x="365" y="156" text-anchor="middle" font-size="6.0" fill="var(--faint)">extended PrismaAdapter persists</text>
  <rect x="540" y="100" width="160" height="58" rx="10" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="620" y="122" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">issue JWT session</text><text x="620" y="138" text-anchor="middle" font-size="6.2" fill="var(--muted)">self-signed + identity info</text><text x="620" y="150" text-anchor="middle" font-size="6.0" fill="var(--faint)">next section details it</text>
  <line x1="190" y1="92" x2="278" y2="116" stroke="var(--blue)" stroke-width="1.4"/><polygon points="278,116 269,114 271,122" fill="var(--blue)"/>
  <line x1="190" y1="160" x2="278" y2="140" stroke="var(--teal)" stroke-width="1.4"/><polygon points="278,140 269,140 273,148" fill="var(--teal)"/>
  <line x1="450" y1="128" x2="538" y2="128" stroke="var(--accent)" stroke-width="1.4"/><polygon points="538,128 529,124 529,132" fill="var(--accent)"/>
  <rect x="280" y="186" width="170" height="48" rx="8" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="365" y="204" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">SSO can be enforced</text><text x="365" y="218" text-anchor="middle" font-size="6.0" fill="var(--muted)">instance / domain / EE multi-tenant</text><text x="365" y="228" text-anchor="middle" font-size="5.8" fill="var(--faint)">disable password login, force SSO</text>
  <line x1="365" y1="166" x2="365" y2="184" stroke="var(--faint)" stroke-width="1" stroke-dasharray="2 2"/>
</svg>
<div class="figcap"><b>Login entry</b>: <code>auth.ts:24-38</code> imports 14 providers (Credentials/Email + 12 SSO). Static providers come from env; dynamic SSO providers are read from the DB and merged at runtime (around <code>auth.ts:739</code>, <code>[...staticProviders, ...dynamicSsoProviders]</code>). SSO can be enforced: <code>AUTH_DISABLE_USERNAME_PASSWORD</code> (instance), <code>getSSOBlockedDomains()</code> (domain), <code>getSsoAuthProviderIdForDomain</code> (EE multi-tenant).</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">own</span><span class="name">CredentialsProvider (email-password)</span></div><div class="ld">The most basic path: username + password. The password is stored as a <strong>bcrypt</strong> salted hash and compared on login. The next section shows a ring of security guardrails around it (SSO enforcement, timing-attack defense, SSO-user interception).</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">outsource</span><span class="name">SSO providers (a dozen-plus)</span></div><div class="ld">Hand "prove identity" to an IdP the enterprise already trusts. Employees log in with their existing Google/Okta/Azure account in one click, no new password — easier and safer (the IdP typically has MFA, unified sign-out, and other enterprise controls).</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">persist</span><span class="name">extended PrismaAdapter</span></div><div class="ld">NextAuth uses <code>PrismaAdapter</code> to store user/account relations in Postgres; Langfuse <strong>wraps another layer</strong> (<code>extendedPrismaAdapter</code>) with custom account-linking/field-cleanup logic — safely landing third-party IdP users into its own User table.</div></div>
</div>
""")

_EN48.append(r"""
<h2>A ring of security guardrails around password login</h2>
<p>Don't underestimate the plainest path, "email-password" — its <code>authorize</code> function hides a ring of security design worth savoring. <strong>First, three SSO-enforcement gates</strong>: instance-level disabling of password login (<code>AUTH_DISABLE_USERNAME_PASSWORD</code>), a domain-level blocklist (certain company domains must use SSO), and EE multi-tenant enforcement (a domain configured with a dedicated SSO can't use passwords). <strong>Then a textbook timing-attack defense</strong>: if the user doesn't exist, the code <strong>still runs the password hash</strong> before erroring — so "user doesn't exist" and "wrong password" take similar time, and an attacker <strong>can't probe whether an email is registered by response speed</strong>. <strong>And one more</strong>: if the user's <code>password</code> field is null, they signed up via SSO, so explicitly prompt "please sign in with your linked IdP." Only after all that does it <strong>bcrypt</strong>-compare the password.</p>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>Triple SSO-enforcement check</h4><p>Instance disables passwords? Domain on the SSO blocklist? Domain configured with a dedicated EE SSO? — hit any one, reject immediately and prompt for SSO.</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>Look up user + timing defense</h4><p>Find User by email. <strong>If not found, still run <code>hashPassword</code></strong> before throwing "Invalid credentials" — keeping failure time constant, blocking the "enumerate registered emails by response speed" side channel.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Intercept SSO users</h4><p>If <code>dbUser.password === null</code>, this person signed up via SSO and has no password — explicitly guide "please sign in with your linked identity provider," rather than a vague error.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>bcrypt compare</h4><p><code>verifyPassword</code> uses bcrypt <code>compare</code> (stored as <code>hash(password, 12)</code>, 12 salted rounds). A mismatch is "Invalid credentials." Only all-pass lets you in.</p></div></div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/server/auth.ts · credentialsServerUtils.ts</span><span class="ln">authorize security guardrails</span></div>
  <pre class="code"><span class="kw">async</span> <span class="fn">authorize</span>(credentials) {
  <span class="cm">// 1) SSO enforcement: instance / domain / EE multi-tenant</span>
  <span class="kw">if</span> (env.AUTH_DISABLE_USERNAME_PASSWORD === <span class="st">"true"</span>) <span class="kw">throw</span> <span class="st">"… use SSO"</span>;
  <span class="kw">if</span> (getSSOBlockedDomains().includes(domain))         <span class="kw">throw</span> <span class="st">"… use SSO"</span>;
  <span class="kw">if</span> (<span class="kw">await</span> <span class="fn">getSsoAuthProviderIdForDomain</span>(domain))     <span class="kw">throw</span> ENTERPRISE_SSO_REQUIRED_MESSAGE;

  <span class="kw">const</span> dbUser = <span class="kw">await</span> prisma.user.<span class="fn">findUnique</span>({ where: { email: email.toLowerCase() } });
  <span class="kw">if</span> (!dbUser) {
    <span class="kw">await</span> <span class="fn">hashPassword</span>(credentials.password);  <span class="cm">// hash even if user absent → defeat timing enumeration</span>
    <span class="kw">throw</span> <span class="st">"Invalid credentials"</span>;
  }
  <span class="kw">if</span> (dbUser.password === <span class="kw">null</span>) <span class="kw">throw</span> <span class="st">"Please sign in with your identity provider…"</span>;  <span class="cm">// SSO user</span>

  <span class="kw">const</span> ok = <span class="kw">await</span> <span class="fn">verifyPassword</span>(credentials.password, dbUser.password);  <span class="cm">// bcrypt compare</span>
  <span class="kw">if</span> (!ok) <span class="kw">throw</span> <span class="st">"Invalid credentials"</span>;
  <span class="kw">return</span> userObj;   <span class="cm">// pass → NextAuth issues a session from this</span>
}

<span class="cm">// credentialsServerUtils.ts: bcrypt, 12 salted rounds</span>
<span class="kw">export async function</span> <span class="fn">hashPassword</span>(pw) { <span class="kw">return</span> <span class="fn">hash</span>(pw, <span class="st">12</span>); }
<span class="kw">export async function</span> <span class="fn">verifyPassword</span>(pw, hashed) { <span class="kw">return</span> <span class="fn">compare</span>(pw, hashed); }</pre>
</div>
""")

_EN48.append(r"""
<h2>Session = JWT + one "identity injection"</h2>
<p>After login passes, NextAuth issues a <strong>JWT</strong> (<code>session.strategy: "jwt"</code>), valid for <code>maxAge = AUTH_SESSION_MAX_AGE × 60</code> seconds. JWT's benefit is being <strong>stateless</strong>: the credential itself carries a signature and identity info, the server just verifies the signature, no need to query a session table on every request — especially friendly for horizontally-scaled multi-instance deployments. The real masterstroke is the <strong>session callback</strong>: every time it builds a session, it queries that user's <code>organizationMemberships → projects</code> and <code>ProjectMemberships</code> by email, and <strong>stuffs "which orgs, which projects, what role" into the session object</strong>. This step is exactly <strong>the wire</strong> connecting "who you are" (this lesson's auth) to "what you can do" (the next lesson's RBAC) — the next lesson's <code>throwIfNoProjectAccess</code> reads precisely the memberships and roles injected here.</p>

<div class="fig">
<svg viewBox="0 0 720 220" role="img" aria-label="JWT session flow: after login passes NextAuth issues a JWT (stateless, self-signed with identity, maxAge expiry), the session callback on each session build queries the user's organizationMemberships→projects and ProjectMemberships and injects them into the session, becoming the next lesson's RBAC input">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Issue JWT + inject memberships → wire to RBAC</text>
  <rect x="30" y="70" width="140" height="56" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="100" y="90" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">login passes</text><text x="100" y="106" text-anchor="middle" font-size="6.2" fill="var(--muted)">password or SSO</text><text x="100" y="117" text-anchor="middle" font-size="6.0" fill="var(--faint)">authorize returns user</text>
  <rect x="200" y="62" width="160" height="72" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="280" y="82" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">issue JWT session</text><text x="280" y="98" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">strategy: "jwt" (stateless)</text><text x="280" y="110" text-anchor="middle" font-size="6.2" fill="var(--muted)">self-signed + identity info</text><text x="280" y="123" text-anchor="middle" font-size="6.0" fill="var(--faint)">maxAge expires it</text>
  <rect x="390" y="50" width="180" height="96" rx="9" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="480" y="70" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">session callback (inject identity)</text><text x="480" y="87" text-anchor="middle" font-size="6.2" fill="var(--muted)">query organizationMemberships</text><text x="480" y="99" text-anchor="middle" font-size="6.2" fill="var(--muted)">→ projects (non-deleted)</text><text x="480" y="111" text-anchor="middle" font-size="6.2" fill="var(--muted)">+ ProjectMemberships</text><text x="480" y="127" text-anchor="middle" font-size="6.0" fill="var(--faint)">"which orgs/projects · what role"</text><text x="480" y="138" text-anchor="middle" font-size="6.0" fill="var(--faint)">stuffed into the session</text>
  <rect x="600" y="74" width="100" height="50" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="650" y="94" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">→ L49 RBAC</text><text x="650" y="110" text-anchor="middle" font-size="5.8" fill="var(--muted)">judge scope by role</text>
  <line x1="170" y1="98" x2="198" y2="98" stroke="var(--teal)" stroke-width="1.4"/><polygon points="198,98 189,94 189,102" fill="var(--teal)"/>
  <line x1="360" y1="98" x2="388" y2="98" stroke="var(--accent)" stroke-width="1.4"/><polygon points="388,98 379,94 379,102" fill="var(--accent)"/>
  <line x1="570" y1="98" x2="598" y2="98" stroke="var(--blue)" stroke-width="1.4"/><polygon points="598,98 589,94 589,102" fill="var(--blue)"/>
  <text x="360" y="170" text-anchor="middle" font-size="8" fill="var(--faint)">JWT stateless = horizontally scalable (just verify the signature, no per-request session-table lookup); the session callback "translates" the auth result into RBAC's input</text>
  <text x="360" y="188" text-anchor="middle" font-size="8" fill="var(--faint)">This session callback is wrapped in instrumentAsync (Lesson 51's OTel wrapper) — the platform self-observes even its own login</text>
</svg>
<div class="figcap"><b>JWT + identity injection</b>: <code>auth.ts:743</code> <code>session.strategy:"jwt"</code>, <code>:744</code> <code>maxAge:AUTH_SESSION_MAX_AGE*60</code>; the session callback (from <code>:747</code>) queries <code>organizationMemberships</code> (with non-deleted <code>projects</code>, ordered createdAt desc) + <code>ProjectMemberships</code> into the session. The callback body is wrapped in <code>instrumentAsync("next-auth-session")</code> (self-observability, see Lesson 51).</div>
</div>

<table class="t">
  <thead><tr><th>Session approach</th><th>DB session (badge prints a number)</th><th>JWT (badge prints info + seal) ← Langfuse</th></tr></thead>
  <tbody>
    <tr><td>Per request</td><td>take the id, query the DB again</td><td>verify the signature locally, <b>no DB lookup</b></td></tr>
    <tr><td>Horizontal scaling</td><td>multi-instance needs shared session storage</td><td><b>naturally friendly</b>: any instance verifies independently</td></tr>
    <tr><td>Instant revocation</td><td>delete that DB row to invalidate immediately</td><td>harder (await expiry or an extra blocklist mechanism)</td></tr>
    <tr><td>Identity info</td><td>fetched alongside the DB lookup</td><td><b>session callback</b> injects org/project memberships</td></tr>
  </tbody>
</table>
""")

_EN48.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why use a stateless JWT session instead of a traditional database session?</strong> The core is <strong>scalability</strong>. A DB session works by: issue a random id to the browser, store "this id maps to this user" in the DB, then on every request take the id and <strong>query the DB again</strong>. Fine on one machine, but Langfuse runs <strong>multiple web instances</strong> for horizontal scaling — with DB sessions, every instance hits the shared session store on every request, making it a bottleneck and single point. JWT <strong>prints identity info right on the credential and signs it with a key to prevent tampering</strong>, so any instance can <strong>verify locally</strong> and confirm "who you are" without a DB round-trip — the key to a stateless, horizontally-scalable architecture. The cost is that <strong>instant revocation gets harder</strong> (an issued credential stays valid through its window), so JWT pairs with a not-too-long <code>maxAge</code>, splitting the difference with "short validity + re-sign on expiry." <strong>Statelessness buys scalability, paid back partly with a validity window.</strong><br><br>
  <strong>What does that seemingly-wasteful "hash the password even when the user doesn't exist" actually guard against?</strong> It guards against <strong>user enumeration</strong> via a <strong>timing side-channel attack</strong>. bcrypt is deliberately slow (12 rounds). If "user doesn't exist" errored out instantly while "user exists but wrong password" slowly ran bcrypt, the two failure paths would have a <strong>measurable time difference</strong> — an attacker trying a pile of emails sees <strong>fast = not registered, slow = registered</strong>, learning "which emails are registered here" without ever guessing a password (itself a privacy leak, and ammunition for later credential stuffing). The countermeasure is simple yet professional: <strong>make the two failure paths take similar time</strong> — run a throwaway hash even when the user is absent. In security engineering, <strong>"errors should look the same and take the same time"</strong> is an easily-overlooked but important principle.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Auth = who you are</strong>: hosted by NextAuth, two ways in — CredentialsProvider (email-password) + a dozen-plus SSO (Google/Okta/Azure AD/Keycloak/WorkOS…, outsourcing "prove identity" to a trusted IdP). Providers come from two sources: static (env) and dynamic (DB).</li>
    <li><strong>Password-login guardrails</strong>: three SSO-enforcement gates (instance-level <code>AUTH_DISABLE_USERNAME_PASSWORD</code> / domain blocklist / EE multi-tenant); <strong>timing-attack defense</strong> (run bcrypt even when the user is absent to block enumeration); SSO-user interception (password=null guides to the IdP); finally a bcrypt(12-round) compare.</li>
    <li><strong>Session = JWT</strong>: <code>strategy:"jwt"</code> stateless, self-signed with identity, <code>maxAge</code> expiry. Versus DB sessions, naturally suited to multi-instance horizontal scaling (verify locally, no DB lookup), at the cost of harder instant revocation (split with a short validity window).</li>
    <li><strong>Session callback injects identity</strong>: on session build it queries <code>organizationMemberships→projects</code> + <code>ProjectMemberships</code> into the session — the wire connecting "who you are" to the next lesson's "what you can do" (RBAC).</li>
    <li><strong>Even login self-observes</strong>: the session callback is wrapped in <code>instrumentAsync</code> (Lesson 51's OTel wrapper), attaching a span to the login path too. The platform's self-observability is everywhere.</li>
  </ul>
</div>
""")

LESSON_48 = {"zh": "\n".join(_ZH48), "en": "\n".join(_EN48)}
