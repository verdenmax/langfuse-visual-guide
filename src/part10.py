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


# ══════════════════════════════════════════════════════════════════════
# L49 · RBAC · API key · SCIM
# ══════════════════════════════════════════════════════════════════════
_ZH49 = []
_EN49 = []

# (L49 sections below)

_ZH49.append(r"""
<p class="lead">
上一课解决了「你是谁」，这一课解决「<strong>你能干什么</strong>」——授权（authorization）。Langfuse 有<strong>两类「客人」</strong>要授权：<strong>人</strong>（在 UI 里点点点的用户）和<strong>机器</strong>（用 SDK 上报数据、调 API 的程序）。两类客人走两套授权机制：人靠 <strong>RBAC（基于角色的访问控制）</strong>——把细粒度的<strong>权限点（scope）</strong>打包成<strong>角色（OWNER/ADMIN/MEMBER/VIEWER）</strong>，再看你在某项目里是什么角色；机器靠 <strong>API key</strong>——一对 <code>pk-lf-…</code>/<code>sk-lf-…</code> 密钥，背后藏着一个相当讲究的<strong>两层哈希</strong>设计（一层为了「查得快」，一层为了「存得安全」）。最后再看一眼 <strong>SCIM</strong>：让企业的身份系统能<strong>自动开通/注销</strong> Langfuse 用户。
这一课你会反复看到两条安全信条：<strong>最小权限</strong>（默认只给够用的）与<strong>纵深防御</strong>（前端藏、后端拦，两道都做）。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  还是那栋写字楼。上一课你已进了门、拿到访客牌，这一课讲<strong>这张牌能开哪些门</strong>。
  对<strong>人</strong>，楼里用「<strong>岗位</strong>」管权限：前台、员工、主管、老板各是一个<strong>角色</strong>，每个角色预先配好「能进哪些房间」的一串钥匙（<strong>scope</strong>）。你不必逐人发钥匙，只要给人定个岗位，钥匙串就自动跟过来——这就是 RBAC。而且门禁做了<strong>两道</strong>：门上贴的指示牌会把你进不去的房间<strong>直接不显示</strong>（前端按角色隐藏按钮，体验好），但真正拦你的是<strong>门锁本身</strong>（后端强制校验，安全）——光把指示牌撕了可没用。
  对<strong>机器</strong>（比如夜里自动来送货的机器人），楼里发的是一张<strong>门禁卡</strong>（API key）。卡片本体（密钥明文）只在发卡那一刻给你一次，之后楼里只留<strong>两份「指纹」</strong>：一份是<strong>快速比对用的卡号哈希</strong>（刷卡时一秒查到是谁），一份是<strong>慢而安全的加盐指纹</strong>（万一卡号库泄露也反推不出原卡）。
</div>
""")

# (L49 sec1 below)

_ZH49.append(r"""
<h2>人的授权：角色 → 一串 scope</h2>
<p>RBAC 的核心是一张映射表 <code>projectRoleAccessRights: Record&lt;Role, ProjectScope[]&gt;</code>：把每个<strong>角色</strong>映射到一串<strong>权限点（scope）</strong>。scope 是细粒度的「资源:动作」字符串，如 <code>traces:delete</code>、<code>prompts:CUD</code>、<code>apiKeys:read</code>、<code>project:delete</code>。角色从权大到权小是 <strong>OWNER → ADMIN → MEMBER → VIEWER → NONE</strong>：OWNER 拿到几乎全部 scope，VIEWER 只拿到一堆 <code>*:read</code>（只读），NONE 是空数组（什么都不能）。判权限时不直接问「你是不是 OWNER」，而是问「你的角色里<strong>有没有这个 scope</strong>」——这样加新功能只需给相关角色<strong>添一个 scope</strong>，不必到处改「if 角色==X」。</p>

<p>更关键的是<strong>同一个权限点要在两处校验</strong>，这是纵深防御：前端用 React hook <code>useHasProjectAccess</code> 决定「这个删除按钮要不要显示」（体验：没权限就别给看），后端在每个 tRPC resolver 里用 <code>throwIfNoProjectAccess</code> <strong>强制拦截</strong>（安全：没权限就抛 <code>FORBIDDEN</code>）。前端的隐藏只是体面，<strong>真正挡住越权的是后端那道</strong>——因为前端代码在用户机器上，可被绕过。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="RBAC：用户在某项目的角色OWNER/ADMIN/MEMBER/VIEWER/NONE映射到一串scope权限点(traces:delete等)，判权限问角色是否含该scope；同一scope两处校验：前端useHasProjectAccess隐藏按钮(体验)、后端throwIfNoProjectAccess抛FORBIDDEN(安全)">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">角色打包 scope；同一权限前后端两道校验</text>
  <rect x="24" y="44" width="120" height="150" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="84" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">角色（由大到小）</text>
  <rect x="36" y="72" width="96" height="20" rx="4" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="84" y="86" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--accent-ink)">OWNER（几乎全部）</text>
  <rect x="36" y="96" width="96" height="20" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="84" y="110" text-anchor="middle" font-size="6.6" fill="var(--ink)">ADMIN</text>
  <rect x="36" y="120" width="96" height="20" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="84" y="134" text-anchor="middle" font-size="6.6" fill="var(--ink)">MEMBER</text>
  <rect x="36" y="144" width="96" height="20" rx="4" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="84" y="158" text-anchor="middle" font-size="6.6" fill="var(--teal)">VIEWER（仅 *:read）</text>
  <rect x="36" y="168" width="96" height="20" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="84" y="182" text-anchor="middle" font-size="6.6" fill="var(--muted)">NONE（空 []）</text>
  <rect x="190" y="80" width="170" height="110" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="275" y="100" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">scope 权限点（细粒度）</text><text x="275" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">traces:delete · prompts:CUD</text><text x="275" y="131" text-anchor="middle" font-size="6.4" fill="var(--muted)">apiKeys:read · project:delete</text><text x="275" y="144" text-anchor="middle" font-size="6.4" fill="var(--muted)">datasets:CUD · scores:CUD …</text><text x="275" y="164" text-anchor="middle" font-size="6.2" fill="var(--faint)">projectRoleAccessRights</text><text x="275" y="176" text-anchor="middle" font-size="6.2" fill="var(--faint)">Record&lt;Role, Scope[]&gt;</text>
  <rect x="410" y="56" width="285" height="58" rx="9" fill="var(--teal)" opacity="0.13" stroke="var(--teal)"/><text x="552" y="76" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">① 前端 useHasProjectAccess</text><text x="552" y="92" text-anchor="middle" font-size="6.4" fill="var(--muted)">没权限就隐藏按钮（体验）</text><text x="552" y="104" text-anchor="middle" font-size="6.0" fill="var(--faint)">React hook · 可被绕过，仅体面</text>
  <rect x="410" y="124" width="285" height="64" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="552" y="144" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">② 后端 throwIfNoProjectAccess</text><text x="552" y="160" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">没权限抛 TRPCError FORBIDDEN（安全）</text><text x="552" y="174" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">每个 tRPC resolver 强制·真正的闸</text>
  <line x1="144" y1="120" x2="188" y2="120" stroke="var(--accent)" stroke-width="1.3"/><polygon points="188,120 179,116 179,124" fill="var(--accent)"/>
  <line x1="360" y1="110" x2="408" y2="85" stroke="var(--teal)" stroke-width="1.2"/><polygon points="408,85 399,85 403,93" fill="var(--teal)"/>
  <line x1="360" y1="150" x2="408" y2="155" stroke="var(--accent)" stroke-width="1.3"/><polygon points="408,155 399,151 399,159" fill="var(--accent)"/>
  <text x="360" y="218" text-anchor="middle" font-size="8" fill="var(--faint)">判权限问「角色里有没有这个 scope」，而非「是不是某角色」——加功能只需给角色添 scope</text>
  <text x="360" y="234" text-anchor="middle" font-size="8" fill="var(--faint)">前端隐藏可被绕过（代码在用户机器上），真正挡越权的是后端那道——纵深防御</text>
</svg>
<div class="figcap"><b>角色→scope + 双查</b>：<code>projectAccessRights.ts:91</code> <code>projectRoleAccessRights: Record&lt;Role, ProjectScope[]&gt;</code>（OWNER:92 / ADMIN:150 / MEMBER:207 / VIEWER:251 仅 read / NONE:271 空）；<code>checkProjectAccess.ts:28</code> <code>throwIfNoProjectAccess</code>（服务端，抛 <code>TRPCError FORBIDDEN</code>）+ <code>:42</code> <code>useHasProjectAccess</code>（前端 hook，隐藏 UI）。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/rbac/constants/projectAccessRights.ts · utils/checkProjectAccess.ts</span><span class="ln">角色→scope + 强制校验</span></div>
  <pre class="code"><span class="cm">// scope 是细粒度「资源:动作」串；角色 = 一串 scope 的打包</span>
<span class="kw">export const</span> projectScopes = [<span class="st">"traces:delete"</span>, <span class="st">"prompts:CUD"</span>, <span class="st">"apiKeys:read"</span>,
                              <span class="st">"project:delete"</span>, <span class="st">"datasets:CUD"</span>, …] <span class="kw">as const</span>;

<span class="kw">export const</span> projectRoleAccessRights: Record&lt;Role, ProjectScope[]&gt; = {
  OWNER:  [ <span class="cm">/* 几乎全部 scope */</span> ],
  ADMIN:  [ … ],   MEMBER: [ … ],
  VIEWER: [ <span class="st">"project:read"</span>, <span class="st">"prompts:read"</span>, … <span class="cm">/* 只有 *:read */</span> ],
  NONE:   [],      <span class="cm">// 什么都不能</span>
};

<span class="cm">// 后端：每个 tRPC resolver 调用，无权限即抛 FORBIDDEN（真正的闸）</span>
<span class="kw">export const</span> <span class="fn">throwIfNoProjectAccess</span> = (p) =&gt; {
  <span class="kw">if</span> (!<span class="fn">hasProjectAccess</span>(p))
    <span class="kw">throw new</span> <span class="fn">TRPCError</span>({ code: <span class="st">"FORBIDDEN"</span>, message: <span class="st">"… no access …"</span> });
};
<span class="cm">// 前端：同款判断的 React hook，用来隐藏没权限的按钮（仅体验）</span>
<span class="kw">export const</span> <span class="fn">useHasProjectAccess</span> = ({ projectId, scope }) =&gt; { … };</pre>
</div>

<div class="cols">
  <div class="col"><h4>👑 OWNER / ADMIN</h4><p>几乎全部 scope：建删项目、管成员与 API key、增删改一切资源。OWNER 是项目主人，ADMIN 略少（如不能删项目）。</p></div>
  <div class="col"><h4>✍️ MEMBER</h4><p>日常干活的角色：能读、能增删改大多数业务资源（trace/prompt/dataset/score…），但<strong>管不了成员与项目设置</strong>这类治理类操作。</p></div>
  <div class="col"><h4>👁️ VIEWER / NONE</h4><p>VIEWER 只拿一堆 <code>*:read</code>——<strong>看得见、改不了</strong>，适合审计/旁观者。NONE 是空数组，连看都不行——最小权限的下限。</p></div>
</div>
""")

# (L49 sec2 below)

_ZH49.append(r"""
<h2>机器的授权：API key 的两层哈希</h2>
<p>程序用 API key 认证：<code>generateKeySet</code> 生成一对 <code>pk-lf-{uuid}</code>（public）/<code>sk-lf-{uuid}</code>（secret）。secret 明文<strong>只在创建那一刻返回一次</strong>，之后库里只存它的三种衍生物：<strong>① <code>fastHashedSecretKey</code></strong>= <code>createShaHash(sk, SALT)</code>（sha256，<strong>确定性</strong>，给「查得快」用）；<strong>② <code>hashedSecretKey</code></strong>= bcrypt 哈希（<strong>加盐慢</strong>，给「存得安全」用）；<strong>③ <code>displaySecretKey</code></strong>= 打码串（如 <code>sk-lf-...abc</code>，给 UI 显示）。</p>

<p>为什么要两种哈希？因为「快查」和「安全」是<strong>一对矛盾</strong>。bcrypt 每次加随机盐、故意很慢——安全，但<strong>没法拿它做数据库查找</strong>（同一个 key 每次 bcrypt 结果都不同，你只能一行行比对，O(n)）。sha256 是确定性的——同一个 key 永远算出同一个值，<strong>能直接当索引/缓存键 O(1) 查到</strong>，且因为算的是「key 本身 + 盐」，库泄露也反推不出原 key。于是请求来时：先 <code>createShaHash</code> 算出快哈希，<strong>先查 Redis、没有再查 Postgres</strong>；命中即拿到这把 key 的 scope。老格式的 key（只有 bcrypt 哈希）会用 <code>verifySecretKey</code> 验一次、然后<strong>顺手补上快哈希「升级」</strong>。还有个小心机：查不到的 key 在 Redis 里存一个 <code>API_KEY_NON_EXISTENT</code> 哨兵，<strong>防止有人拿一堆不存在的 key 反复砸数据库</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="API key两层哈希：创建时generateKeySet生成pk-lf/sk-lf，secret明文只返回一次，库里存fastHashedSecretKey(sha256确定性快查)+hashedSecretKey(bcrypt加盐安全)+displaySecretKey(打码显示)；验证时算sha快哈希先查Redis再查PG命中拿scope，老key用bcrypt验后升级补快哈希，不存在的key缓存哨兵防刷库">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">一层为「查得快」，一层为「存得安全」</text>
  <rect x="24" y="44" width="180" height="150" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">创建时（generateKeySet）</text><text x="114" y="80" text-anchor="middle" font-size="6.6" fill="var(--muted)">pk-lf-{uuid} / sk-lf-{uuid}</text><text x="114" y="92" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">sk 明文只返回这一次！</text>
  <rect x="34" y="100" width="160" height="26" rx="4" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="114" y="111" text-anchor="middle" font-size="6.2" font-weight="700" fill="var(--accent-ink)">① fastHashedSecretKey</text><text x="114" y="121" text-anchor="middle" font-size="5.6" fill="var(--muted)">sha256(sk,SALT) 确定性·快查</text>
  <rect x="34" y="130" width="160" height="26" rx="4" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="114" y="141" text-anchor="middle" font-size="6.2" font-weight="700" fill="var(--teal)">② hashedSecretKey</text><text x="114" y="151" text-anchor="middle" font-size="5.6" fill="var(--muted)">bcrypt 加盐慢·安全</text>
  <rect x="34" y="160" width="160" height="26" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="114" y="171" text-anchor="middle" font-size="6.2" font-weight="700" fill="var(--accent-ink)">③ displaySecretKey</text><text x="114" y="181" text-anchor="middle" font-size="5.6" fill="var(--muted)">sk-lf-...abc 打码显示</text>
  <rect x="250" y="60" width="150" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="325" y="80" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">请求带 sk 来</text><text x="325" y="96" text-anchor="middle" font-size="6.2" fill="var(--muted)">createShaHash(sk,SALT)</text>
  <rect x="250" y="124" width="150" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="325" y="141" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">先查 Redis</text><text x="325" y="155" text-anchor="middle" font-size="6.0" fill="var(--muted)">命中即拿 scope（O(1)）</text>
  <rect x="250" y="172" width="150" height="38" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="325" y="188" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">没有→查 Postgres</text><text x="325" y="201" text-anchor="middle" font-size="5.8" fill="var(--muted)">按 fastHashedSecretKey 索引</text>
  <rect x="440" y="70" width="255" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="567" y="88" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">老格式 key（仅 bcrypt）</text><text x="567" y="103" text-anchor="middle" font-size="6.2" fill="var(--muted)">verifySecretKey 验一次 → 补 fastHash「升级」</text>
  <rect x="440" y="126" width="255" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="567" y="144" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">查不到 → 缓存哨兵</text><text x="567" y="159" text-anchor="middle" font-size="6.0" fill="var(--muted)">API_KEY_NON_EXISTENT 防刷库</text>
  <rect x="440" y="180" width="255" height="40" rx="9" fill="var(--teal)" opacity="0.13" stroke="var(--teal)"/><text x="567" y="197" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--teal)">拿到 scope → 放行/拒绝</text><text x="567" y="211" text-anchor="middle" font-size="6.0" fill="var(--muted)">机器也有自己的权限范围</text>
  <line x1="204" y1="118" x2="248" y2="95" stroke="var(--accent)" stroke-width="1.2"/><polygon points="248,95 239,95 243,103" fill="var(--accent)"/>
  <line x1="325" y1="110" x2="325" y2="122" stroke="var(--accent)" stroke-width="1.2"/><polygon points="325,122 321,113 329,113" fill="var(--accent)"/>
  <line x1="400" y1="144" x2="438" y2="100" stroke="var(--faint)" stroke-width="1"/><line x1="400" y1="150" x2="438" y2="148" stroke="var(--faint)" stroke-width="1"/>
</svg>
<div class="figcap"><b>两层哈希</b>：<code>apiKeys.ts:19</code> <code>generateKeySet</code>（pk-lf/sk-lf）；<code>:41 createAndAddApiKeysToDb</code> 存 <code>hashedSecretKey</code>(bcrypt :13) / <code>displaySecretKey</code> / <code>fastHashedSecretKey</code>(<code>createShaHash</code> sha256 :31)，盐 <code>env.SALT</code>。验证 <code>apiAuth.ts:75 verifyAuthHeaderAndReturnScope</code>：<code>:97</code> 算快哈希、Redis→PG 查（<code>:107</code> 老 key <code>verifySecretKey</code> + <code>:141</code> 升级补 fastHash），不存在缓存 <code>API_KEY_NON_EXISTENT</code>。</div>
</div>
<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>请求带 sk 来</h4><p>算 <code>createShaHash(sk, env.SALT)</code> 得到确定性的快哈希——这把 key 的「卡号」。</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>先查 Redis，没有再查 PG</h4><p>用快哈希当键，先问 Redis 缓存；未命中再按 <code>fastHashedSecretKey</code> 索引查 Postgres。命中即拿到这把 key 的 scope。</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>老格式 key：bcrypt 验 + 升级</h4><p>只有 bcrypt 哈希的旧 key，用 <code>verifySecretKey</code> 慢验一次，然后顺手补上快哈希「升级」，下次就走快路。</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>查不到：缓存哨兵</h4><p>不存在的 key 在 Redis 存 <code>API_KEY_NON_EXISTENT</code>，挡住「拿一堆假 key 反复砸数据库」的攻击。最后据 scope 放行或拒绝。</p></div></div>
</div>
""")

# (L49 sec3 below)

_ZH49.append(r"""
<h2>SCIM：让企业身份系统自动开通用户</h2>
<p>大企业有几千名员工，进出职频繁。靠管理员手动在 Langfuse 里一个个加人、离职再删人，既慢又容易漏（漏删 = 离职员工还能访问，是安全隐患）。<strong>SCIM（System for Cross-domain Identity Management，跨域身份管理系统）</strong>是一套标准协议，让企业的身份中枢（如 Okta、Azure AD）能<strong>自动</strong>把「谁该有账号」同步过来：入职自动开通、离职自动注销。Langfuse 在 <code>web/src/pages/api/public/scim/*</code> 实现了 SCIM 的标准端点——<code>Users</code>（增删查用户）、<code>ServiceProviderConfig</code>/<code>ResourceTypes</code>/<code>Schemas</code>（向 IdP 自描述「我支持哪些 SCIM 能力」）。这属于企业级（EE）能力，正好引出下一课的「开源核与权益」。</p>

<table class="t">
  <thead><tr><th>授权对象</th><th>机制</th><th>怎么判</th><th>关键设计</th></tr></thead>
  <tbody>
    <tr><td><b>人</b>（UI 用户）</td><td>RBAC 角色→scope</td><td>角色里有没有该 scope</td><td>前端隐藏 + 后端强制（纵深防御）</td></tr>
    <tr><td><b>机器</b>（SDK/API）</td><td>API key（pk/sk）</td><td>sk 的快哈希查到 key、读其 scope</td><td>两层哈希：sha256 快查 + bcrypt 安全</td></tr>
    <tr><td><b>企业批量</b></td><td>SCIM 协议</td><td>由 IdP 推送增删用户</td><td>入职自动开通、离职自动注销（EE）</td></tr>
  </tbody>
</table>

<p>把三行读完，你会发现授权这件事被拆得很清爽：<strong>不同类型的「客人」用不同的机制，但都落到同一个问题——「这次操作，在不在你的权限范围内」</strong>。RBAC 给人发「角色」、API key 给机器发「带 scope 的密钥」、SCIM 让这套人员名册能被企业自动维护。三者各司其职，又都服务于「<strong>每个主体只拿够用的权限</strong>」这条最小权限原则。</p>
""")

_ZH49.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么 API key 要同时存「sha256 快哈希」和「bcrypt 慢哈希」两份，不能只留一份？</strong> 因为这两份分别解决一对<strong>互相打架</strong>的需求。bcrypt 的安全来自它<strong>每次都加随机盐、且故意算得很慢</strong>——这让暴力破解变得不划算，但也带来一个副作用：同一个 key 每次 bcrypt 出来的值都不同，所以<strong>你没法拿它当数据库查找条件</strong>，只能把库里每一行都 bcrypt-compare 一遍（O(n)，每次认证扫全表，灾难）。而 API 认证是<strong>极高频</strong>的（每条上报的 trace 都要验一次 key），必须 O(1) 查到。sha256(key, SALT) 正好补上：它<strong>确定性</strong>——同一个 key 永远算出同一个值，于是能直接当索引、当 Redis 缓存键，一步查到；同时因为算的是「<strong>密钥本身</strong>」而非可枚举的东西，加上盐，库泄露也反推不出原 key。所以最终方案是<strong>分工</strong>：sha256 负责「在海量 key 里 O(1) 找到是哪一把」，bcrypt 负责「对老格式 key 做加盐慢验证」。<strong>当「快」和「安全」打架时，不是二选一，而是用两种工具各管一段。</strong><br><br>
  <strong>RBAC 为什么前端、后端都要查一遍？只在后端查不够吗、岂不是重复？</strong> 两道查的<strong>目的根本不同</strong>，缺一不可。<strong>后端那道是安全闸</strong>：tRPC resolver 里的 <code>throwIfNoProjectAccess</code> 是真正不可绕过的强制——因为它跑在服务器上。<strong>前端那道是体验</strong>：<code>useHasProjectAccess</code> 把你没权限的按钮直接<strong>不显示</strong>，让你不会点了之后才吃一个红色报错。关键认知是：<strong>前端的权限判断只是「礼貌」，绝不能当作安全</strong>——因为前端代码整个跑在用户的浏览器里，用户可以改它、可以直接构造请求绕过 UI。所以「前端隐藏」必须始终有「后端强制」兜底。很多越权漏洞，恰恰来自开发者只在前端藏了按钮、却忘了在后端加校验——以为「按钮没了就进不去」，殊不知接口是裸的。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>授权 = 你能干什么</strong>：两类对象——人（UI 用户）走 RBAC，机器（SDK/API）走 API key；外加 SCIM 让企业身份系统自动维护用户。共同目标：最小权限。</li>
    <li><strong>RBAC 角色→scope</strong>：<code>projectRoleAccessRights: Record&lt;Role, Scope[]&gt;</code> 把 OWNER/ADMIN/MEMBER/VIEWER/NONE 各映射到一串细粒度 scope（<code>traces:delete</code> 等，VIEWER 仅 read、NONE 空）。判权限问「角色含不含该 scope」，加功能只需添 scope。</li>
    <li><strong>纵深防御：前后端双查</strong>：前端 <code>useHasProjectAccess</code> 隐藏按钮（体验），后端 <code>throwIfNoProjectAccess</code> 抛 FORBIDDEN（安全）。前端可被绕过，<strong>真正的闸是后端</strong>——前端隐藏永远要有后端强制兜底。</li>
    <li><strong>API key 两层哈希</strong>：<code>fastHashedSecretKey</code>=sha256(确定性，给 O(1) 快查、可缓存) + <code>hashedSecretKey</code>=bcrypt(加盐慢，安全) + <code>displaySecretKey</code>(打码显示)。sk 明文只在创建时返回一次；验证先算快哈希查 Redis→PG，老 key 用 bcrypt 验后升级，不存在的 key 缓存哨兵防刷库。</li>
    <li><strong>SCIM 企业自动化</strong>：标准协议让 Okta/Azure AD 等自动开通/注销 Langfuse 用户（入职即有、离职即无），避免手动加删的遗漏。属 EE 能力，引出下一课开源核与权益。</li>
  </ul>
</div>
""")

_EN49.append(r"""
<p class="lead">
The previous lesson settled "who you are"; this one settles "<strong>what you can do</strong>" — authorization. Langfuse has <strong>two kinds of "guests"</strong> to authorize: <strong>humans</strong> (users clicking around the UI) and <strong>machines</strong> (programs reporting data via SDK, calling the API). The two take two authorization mechanisms: humans rely on <strong>RBAC (role-based access control)</strong> — packaging fine-grained <strong>permission points (scopes)</strong> into <strong>roles (OWNER/ADMIN/MEMBER/VIEWER)</strong>, then checking your role in a given project; machines rely on <strong>API keys</strong> — a <code>pk-lf-…</code>/<code>sk-lf-…</code> key pair backed by a rather thoughtful <strong>two-tier hash</strong> design (one tier for "fast lookup," one for "secure storage"). Finally a glance at <strong>SCIM</strong>: letting an enterprise's identity system <strong>auto-provision/deprovision</strong> Langfuse users.
You'll repeatedly see two security creeds here: <strong>least privilege</strong> (grant only what's needed by default) and <strong>defense in depth</strong> (hide on the front end, block on the back end — do both).
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Same office building. Last lesson you got in and received a visitor badge; this lesson is about <strong>which doors that badge opens</strong>.
  For <strong>humans</strong>, the building manages access by "<strong>job role</strong>": front-desk, employee, supervisor, boss are each a <strong>role</strong>, and each role is pre-fitted with a string of keys (<strong>scopes</strong>) for "which rooms you may enter." You don't hand out keys person by person — just assign a person a job, and the key ring follows automatically — that's RBAC. And door access is done <strong>twice</strong>: the signpost on the door simply <strong>doesn't display</strong> rooms you can't enter (the front end hides buttons by role, nice UX), but what actually stops you is <strong>the lock itself</strong> (the back end enforces, security) — tearing off the signpost gets you nowhere.
  For <strong>machines</strong> (say a delivery robot that comes at night), the building issues an <strong>access card</strong> (API key). The card itself (the secret in cleartext) is given to you only once at issuance; afterward the building keeps only <strong>two "fingerprints"</strong>: one is a <strong>card-number hash for fast matching</strong> (instantly find who it is on swipe), the other a <strong>slow, salted fingerprint</strong> (even if the card-number store leaks, the original card can't be reverse-derived).
</div>

<h2>Authorizing humans: a role → a string of scopes</h2>
<p>RBAC's core is one mapping table <code>projectRoleAccessRights: Record&lt;Role, ProjectScope[]&gt;</code>: mapping each <strong>role</strong> to a string of <strong>permission points (scopes)</strong>. A scope is a fine-grained "resource:action" string, like <code>traces:delete</code>, <code>prompts:CUD</code>, <code>apiKeys:read</code>, <code>project:delete</code>. Roles run most-to-least powerful: <strong>OWNER → ADMIN → MEMBER → VIEWER → NONE</strong>: OWNER gets almost all scopes, VIEWER gets only a pile of <code>*:read</code> (read-only), NONE is an empty array (nothing). When checking permission you don't ask "are you OWNER" but "does your role <strong>contain this scope</strong>" — so adding a feature only means <strong>adding a scope</strong> to the relevant roles, not editing "if role==X" everywhere.</p>

<p>More crucially, <strong>the same permission point is checked in two places</strong> — this is defense in depth: the front end uses the React hook <code>useHasProjectAccess</code> to decide "should this delete button show" (UX: don't show what you can't do), the back end uses <code>throwIfNoProjectAccess</code> in every tRPC resolver to <strong>enforce</strong> (security: throw <code>FORBIDDEN</code> if no access). Front-end hiding is just courtesy; <strong>what actually blocks privilege escalation is the back end</strong> — because front-end code runs on the user's machine and can be bypassed.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="RBAC: a user's role in a project OWNER/ADMIN/MEMBER/VIEWER/NONE maps to a string of scope permission points (traces:delete etc), checking permission asks whether the role contains the scope; same scope checked in two places: front end useHasProjectAccess hides buttons (UX), back end throwIfNoProjectAccess throws FORBIDDEN (security)">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Roles package scopes; same permission checked front + back</text>
  <rect x="24" y="44" width="120" height="150" rx="9" fill="var(--bg)" stroke="var(--accent)"/><text x="84" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">roles (most→least)</text>
  <rect x="36" y="72" width="96" height="20" rx="4" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="84" y="86" text-anchor="middle" font-size="6.6" font-weight="700" fill="var(--accent-ink)">OWNER (almost all)</text>
  <rect x="36" y="96" width="96" height="20" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="84" y="110" text-anchor="middle" font-size="6.6" fill="var(--ink)">ADMIN</text>
  <rect x="36" y="120" width="96" height="20" rx="4" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="84" y="134" text-anchor="middle" font-size="6.6" fill="var(--ink)">MEMBER</text>
  <rect x="36" y="144" width="96" height="20" rx="4" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="84" y="158" text-anchor="middle" font-size="6.6" fill="var(--teal)">VIEWER (only *:read)</text>
  <rect x="36" y="168" width="96" height="20" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="84" y="182" text-anchor="middle" font-size="6.6" fill="var(--muted)">NONE (empty [])</text>
  <rect x="190" y="80" width="170" height="110" rx="9" fill="var(--purple-soft)" stroke="var(--accent)" stroke-width="2"/><text x="275" y="100" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">scope points (fine-grained)</text><text x="275" y="118" text-anchor="middle" font-size="6.4" fill="var(--muted)">traces:delete · prompts:CUD</text><text x="275" y="131" text-anchor="middle" font-size="6.4" fill="var(--muted)">apiKeys:read · project:delete</text><text x="275" y="144" text-anchor="middle" font-size="6.4" fill="var(--muted)">datasets:CUD · scores:CUD …</text><text x="275" y="164" text-anchor="middle" font-size="6.2" fill="var(--faint)">projectRoleAccessRights</text><text x="275" y="176" text-anchor="middle" font-size="6.2" fill="var(--faint)">Record&lt;Role, Scope[]&gt;</text>
  <rect x="410" y="56" width="285" height="58" rx="9" fill="var(--teal)" opacity="0.13" stroke="var(--teal)"/><text x="552" y="76" text-anchor="middle" font-size="8" font-weight="700" fill="var(--teal)">① front: useHasProjectAccess</text><text x="552" y="92" text-anchor="middle" font-size="6.4" fill="var(--muted)">hide the button if no access (UX)</text><text x="552" y="104" text-anchor="middle" font-size="6.0" fill="var(--faint)">React hook · bypassable, courtesy only</text>
  <rect x="410" y="124" width="285" height="64" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="552" y="144" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">② back: throwIfNoProjectAccess</text><text x="552" y="160" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">throw TRPCError FORBIDDEN if no access (security)</text><text x="552" y="174" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">enforced in every tRPC resolver · the real gate</text>
  <line x1="144" y1="120" x2="188" y2="120" stroke="var(--accent)" stroke-width="1.3"/><polygon points="188,120 179,116 179,124" fill="var(--accent)"/>
  <line x1="360" y1="110" x2="408" y2="85" stroke="var(--teal)" stroke-width="1.2"/><polygon points="408,85 399,85 403,93" fill="var(--teal)"/>
  <line x1="360" y1="150" x2="408" y2="155" stroke="var(--accent)" stroke-width="1.3"/><polygon points="408,155 399,151 399,159" fill="var(--accent)"/>
  <text x="360" y="218" text-anchor="middle" font-size="8" fill="var(--faint)">Ask "does the role contain this scope," not "is it some role" — adding a feature just adds a scope to a role</text>
  <text x="360" y="234" text-anchor="middle" font-size="8" fill="var(--faint)">Front-end hiding is bypassable (code runs on the user's machine); the real escalation block is the back end — defense in depth</text>
</svg>
<div class="figcap"><b>Role→scope + dual check</b>: <code>projectAccessRights.ts:91</code> <code>projectRoleAccessRights: Record&lt;Role, ProjectScope[]&gt;</code> (OWNER:92 / ADMIN:150 / MEMBER:207 / VIEWER:251 read-only / NONE:271 empty); <code>checkProjectAccess.ts:28</code> <code>throwIfNoProjectAccess</code> (server, throws <code>TRPCError FORBIDDEN</code>) + <code>:42</code> <code>useHasProjectAccess</code> (front-end hook, hides UI).</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/rbac/constants/projectAccessRights.ts · utils/checkProjectAccess.ts</span><span class="ln">role→scope + enforced check</span></div>
  <pre class="code"><span class="cm">// a scope is a fine-grained "resource:action" string; a role = a package of scopes</span>
<span class="kw">export const</span> projectScopes = [<span class="st">"traces:delete"</span>, <span class="st">"prompts:CUD"</span>, <span class="st">"apiKeys:read"</span>,
                              <span class="st">"project:delete"</span>, <span class="st">"datasets:CUD"</span>, …] <span class="kw">as const</span>;

<span class="kw">export const</span> projectRoleAccessRights: Record&lt;Role, ProjectScope[]&gt; = {
  OWNER:  [ <span class="cm">/* almost all scopes */</span> ],
  ADMIN:  [ … ],   MEMBER: [ … ],
  VIEWER: [ <span class="st">"project:read"</span>, <span class="st">"prompts:read"</span>, … <span class="cm">/* only *:read */</span> ],
  NONE:   [],      <span class="cm">// nothing allowed</span>
};

<span class="cm">// back end: called in every tRPC resolver, throws FORBIDDEN on no access (the real gate)</span>
<span class="kw">export const</span> <span class="fn">throwIfNoProjectAccess</span> = (p) =&gt; {
  <span class="kw">if</span> (!<span class="fn">hasProjectAccess</span>(p))
    <span class="kw">throw new</span> <span class="fn">TRPCError</span>({ code: <span class="st">"FORBIDDEN"</span>, message: <span class="st">"… no access …"</span> });
};
<span class="cm">// front end: same check as a React hook, to hide buttons without access (UX only)</span>
<span class="kw">export const</span> <span class="fn">useHasProjectAccess</span> = ({ projectId, scope }) =&gt; { … };</pre>
</div>

<div class="cols">
  <div class="col"><h4>👑 OWNER / ADMIN</h4><p>Almost all scopes: create/delete projects, manage members and API keys, CRUD every resource. OWNER is the project owner; ADMIN is slightly less (e.g. can't delete the project).</p></div>
  <div class="col"><h4>✍️ MEMBER</h4><p>The everyday working role: can read and CUD most business resources (trace/prompt/dataset/score…), but <strong>can't manage members or project settings</strong> — those governance operations.</p></div>
  <div class="col"><h4>👁️ VIEWER / NONE</h4><p>VIEWER gets only a pile of <code>*:read</code> — <strong>can see, can't change</strong>, fit for audit/observers. NONE is an empty array — can't even see — the floor of least privilege.</p></div>
</div>
""")

_EN49.append(r"""
<h2>Authorizing machines: the API key's two-tier hash</h2>
<p>Programs authenticate with an API key: <code>generateKeySet</code> generates a pair <code>pk-lf-{uuid}</code> (public) / <code>sk-lf-{uuid}</code> (secret). The secret in cleartext is <strong>returned only once, at creation</strong>; afterward the DB stores only three derivatives: <strong>① <code>fastHashedSecretKey</code></strong> = <code>createShaHash(sk, SALT)</code> (sha256, <strong>deterministic</strong>, for "fast lookup"); <strong>② <code>hashedSecretKey</code></strong> = bcrypt hash (<strong>salted, slow</strong>, for "secure storage"); <strong>③ <code>displaySecretKey</code></strong> = a masked string (e.g. <code>sk-lf-...abc</code>, for UI display).</p>

<p>Why two hashes? Because "fast lookup" and "security" are <strong>a contradiction</strong>. bcrypt adds a random salt each time and is deliberately slow — secure, but <strong>you can't use it as a database lookup</strong> (the same key bcrypts to a different value each time, so you can only compare row by row, O(n)). sha256 is deterministic — the same key always computes the same value, so it can be <strong>used directly as an index/cache key for O(1) lookup</strong>, and since it hashes "the key itself + salt," a store leak can't reverse-derive the key. So when a request arrives: first <code>createShaHash</code> computes the fast hash, then <strong>look up Redis first, falling back to Postgres</strong>; a hit yields that key's scopes. Legacy-format keys (with only the bcrypt hash) are verified once with <code>verifySecretKey</code>, then <strong>conveniently "upgraded" by storing the fast hash</strong>. One more trick: a not-found key stores an <code>API_KEY_NON_EXISTENT</code> sentinel in Redis to <strong>stop someone hammering the database with piles of nonexistent keys</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 250" role="img" aria-label="API key two-tier hash: at creation generateKeySet makes pk-lf/sk-lf, the secret cleartext is returned only once, the DB stores fastHashedSecretKey (sha256 deterministic fast lookup) + hashedSecretKey (bcrypt salted secure) + displaySecretKey (masked); at verification compute the sha fast hash, look up Redis then PG, on hit get scopes, legacy keys verified by bcrypt then upgraded with the fast hash, nonexistent keys cache a sentinel to stop DB hammering">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">One tier for "fast lookup," one for "secure storage"</text>
  <rect x="24" y="44" width="180" height="150" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="114" y="62" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">at creation (generateKeySet)</text><text x="114" y="80" text-anchor="middle" font-size="6.6" fill="var(--muted)">pk-lf-{uuid} / sk-lf-{uuid}</text><text x="114" y="92" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">sk cleartext returned only once!</text>
  <rect x="34" y="100" width="160" height="26" rx="4" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="114" y="111" text-anchor="middle" font-size="6.2" font-weight="700" fill="var(--accent-ink)">① fastHashedSecretKey</text><text x="114" y="121" text-anchor="middle" font-size="5.6" fill="var(--muted)">sha256(sk,SALT) deterministic·fast</text>
  <rect x="34" y="130" width="160" height="26" rx="4" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="114" y="141" text-anchor="middle" font-size="6.2" font-weight="700" fill="var(--teal)">② hashedSecretKey</text><text x="114" y="151" text-anchor="middle" font-size="5.6" fill="var(--muted)">bcrypt salted slow·secure</text>
  <rect x="34" y="160" width="160" height="26" rx="4" fill="var(--bg)" stroke="var(--faint)"/><text x="114" y="171" text-anchor="middle" font-size="6.2" font-weight="700" fill="var(--accent-ink)">③ displaySecretKey</text><text x="114" y="181" text-anchor="middle" font-size="5.6" fill="var(--muted)">sk-lf-...abc masked display</text>
  <rect x="250" y="60" width="150" height="50" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="325" y="80" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">request brings sk</text><text x="325" y="96" text-anchor="middle" font-size="6.2" fill="var(--muted)">createShaHash(sk,SALT)</text>
  <rect x="250" y="124" width="150" height="40" rx="8" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="325" y="141" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">look up Redis first</text><text x="325" y="155" text-anchor="middle" font-size="6.0" fill="var(--muted)">hit → get scopes (O(1))</text>
  <rect x="250" y="172" width="150" height="38" rx="8" fill="var(--bg)" stroke="var(--accent)"/><text x="325" y="188" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">miss → query Postgres</text><text x="325" y="201" text-anchor="middle" font-size="5.8" fill="var(--muted)">indexed by fastHashedSecretKey</text>
  <rect x="440" y="70" width="255" height="46" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="567" y="88" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">legacy key (bcrypt only)</text><text x="567" y="103" text-anchor="middle" font-size="6.2" fill="var(--muted)">verifySecretKey once → add fastHash "upgrade"</text>
  <rect x="440" y="126" width="255" height="44" rx="9" fill="var(--bg)" stroke="var(--accent)" stroke-dasharray="4 3"/><text x="567" y="144" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">not found → cache a sentinel</text><text x="567" y="159" text-anchor="middle" font-size="6.0" fill="var(--muted)">API_KEY_NON_EXISTENT, stop DB hammering</text>
  <rect x="440" y="180" width="255" height="40" rx="9" fill="var(--teal)" opacity="0.13" stroke="var(--teal)"/><text x="567" y="197" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--teal)">get scopes → allow/deny</text><text x="567" y="211" text-anchor="middle" font-size="6.0" fill="var(--muted)">machines also have their own scope range</text>
  <line x1="204" y1="118" x2="248" y2="95" stroke="var(--accent)" stroke-width="1.2"/><polygon points="248,95 239,95 243,103" fill="var(--accent)"/>
  <line x1="325" y1="110" x2="325" y2="122" stroke="var(--accent)" stroke-width="1.2"/><polygon points="325,122 321,113 329,113" fill="var(--accent)"/>
  <line x1="400" y1="144" x2="438" y2="100" stroke="var(--faint)" stroke-width="1"/><line x1="400" y1="150" x2="438" y2="148" stroke="var(--faint)" stroke-width="1"/>
</svg>
<div class="figcap"><b>Two-tier hash</b>: <code>apiKeys.ts:19</code> <code>generateKeySet</code> (pk-lf/sk-lf); <code>:41 createAndAddApiKeysToDb</code> stores <code>hashedSecretKey</code>(bcrypt :13) / <code>displaySecretKey</code> / <code>fastHashedSecretKey</code>(<code>createShaHash</code> sha256 :31), salt <code>env.SALT</code>. Verify <code>apiAuth.ts:75 verifyAuthHeaderAndReturnScope</code>: <code>:97</code> compute fast hash, Redis→PG lookup (<code>:107</code> legacy key <code>verifySecretKey</code> + <code>:141</code> upgrade with fastHash), nonexistent cached as <code>API_KEY_NON_EXISTENT</code>.</div>
</div>

<div class="vflow">
  <div class="step"><div class="num">1</div><div class="sc"><h4>Request brings sk</h4><p>Compute <code>createShaHash(sk, env.SALT)</code> for the deterministic fast hash — this key's "card number."</p></div></div>
  <div class="step"><div class="num">2</div><div class="sc"><h4>Look up Redis first, then PG</h4><p>Using the fast hash as the key, ask the Redis cache first; on a miss, query Postgres indexed by <code>fastHashedSecretKey</code>. A hit yields this key's scopes.</p></div></div>
  <div class="step"><div class="num">3</div><div class="sc"><h4>Legacy key: bcrypt verify + upgrade</h4><p>A legacy key with only a bcrypt hash is slow-verified once via <code>verifySecretKey</code>, then conveniently "upgraded" by adding the fast hash, taking the fast path next time.</p></div></div>
  <div class="step"><div class="num">4</div><div class="sc"><h4>Not found: cache a sentinel</h4><p>A nonexistent key stores <code>API_KEY_NON_EXISTENT</code> in Redis, blocking "hammer the DB with piles of fake keys." Finally allow or deny by scope.</p></div></div>
</div>
""")

_EN49.append(r"""
<h2>SCIM: letting the enterprise identity system auto-provision users</h2>
<p>A large enterprise has thousands of employees, joining and leaving constantly. Relying on an admin to manually add people one by one in Langfuse and delete them on departure is slow and error-prone (a missed deletion = a departed employee still has access, a security hazard). <strong>SCIM (System for Cross-domain Identity Management)</strong> is a standard protocol letting an enterprise's identity hub (Okta, Azure AD) <strong>automatically</strong> sync "who should have an account": auto-provision on joining, auto-deprovision on leaving. Langfuse implements the standard SCIM endpoints in <code>web/src/pages/api/public/scim/*</code> — <code>Users</code> (create/delete/list users), <code>ServiceProviderConfig</code>/<code>ResourceTypes</code>/<code>Schemas</code> (self-describe to the IdP "which SCIM capabilities I support"). This is an enterprise (EE) capability, neatly leading into the next lesson's "open-core & entitlements."</p>

<table class="t">
  <thead><tr><th>Subject</th><th>Mechanism</th><th>How it's judged</th><th>Key design</th></tr></thead>
  <tbody>
    <tr><td><b>Humans</b> (UI users)</td><td>RBAC role→scope</td><td>does the role contain the scope</td><td>front-end hide + back-end enforce (defense in depth)</td></tr>
    <tr><td><b>Machines</b> (SDK/API)</td><td>API key (pk/sk)</td><td>sk's fast hash finds the key, read its scopes</td><td>two-tier hash: sha256 fast lookup + bcrypt secure</td></tr>
    <tr><td><b>Enterprise bulk</b></td><td>SCIM protocol</td><td>IdP pushes user create/delete</td><td>auto-provision on join, auto-deprovision on leave (EE)</td></tr>
  </tbody>
</table>

<p>Read the three rows and you'll find authorization cleanly decomposed: <strong>different kinds of "guests" use different mechanisms, but all reduce to one question — "is this operation within your permission range?"</strong> RBAC gives humans a "role," API keys give machines a "scoped secret," SCIM lets that roster be auto-maintained by the enterprise. Each does its job, and all serve the least-privilege principle of "<strong>every subject gets only the privileges it needs</strong>."</p>
""")

_EN49.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why store both a "sha256 fast hash" and a "bcrypt slow hash" for an API key — why not just one?</strong> Because the two solve a pair of <strong>conflicting</strong> needs. bcrypt's security comes from <strong>adding a random salt each time and being deliberately slow</strong> — making brute force uneconomical, but with a side effect: the same key bcrypts to a different value each time, so <strong>you can't use it as a database lookup condition</strong>; you'd bcrypt-compare every row (O(n), scanning the whole table per auth, a disaster). And API auth is <strong>extremely high-frequency</strong> (every reported trace verifies a key once), so it must find the key in O(1). sha256(key, SALT) fills the gap exactly: it's <strong>deterministic</strong> — the same key always computes the same value, so it can be an index or a Redis cache key for a one-step lookup; and since it hashes "<strong>the secret itself</strong>" rather than something enumerable, plus salt, a store leak can't reverse the key. So the final design is a <strong>division of labor</strong>: sha256 handles "O(1) find which key it is among millions," bcrypt handles "salted slow verification for legacy keys." <strong>When "fast" and "secure" conflict, it's not either/or but two tools each owning a segment.</strong><br><br>
  <strong>Why does RBAC check both front end and back end — isn't checking only the back end enough, isn't it duplicate?</strong> The two checks have <strong>fundamentally different purposes</strong>, both indispensable. <strong>The back-end check is the security gate</strong>: <code>throwIfNoProjectAccess</code> in tRPC resolvers is the truly un-bypassable enforcement — because it runs on the server. <strong>The front-end check is UX</strong>: <code>useHasProjectAccess</code> simply <strong>doesn't show</strong> the buttons you can't use, sparing you a red error after clicking. The key realization: <strong>a front-end permission check is only "politeness," never security</strong> — because front-end code runs entirely in the user's browser; the user can modify it or craft requests directly to bypass the UI. So "front-end hiding" must always have "back-end enforcement" behind it. Many privilege-escalation bugs come precisely from a developer hiding a button on the front end but forgetting to add the back-end check — thinking "no button means no entry," while the endpoint sits exposed.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Authorization = what you can do</strong>: two subjects — humans (UI users) take RBAC, machines (SDK/API) take API keys; plus SCIM for the enterprise identity system to auto-maintain users. Shared goal: least privilege.</li>
    <li><strong>RBAC role→scope</strong>: <code>projectRoleAccessRights: Record&lt;Role, Scope[]&gt;</code> maps OWNER/ADMIN/MEMBER/VIEWER/NONE each to a string of fine-grained scopes (<code>traces:delete</code> etc, VIEWER read-only, NONE empty). Check "does the role contain the scope"; adding a feature just adds a scope.</li>
    <li><strong>Defense in depth: dual check</strong>: front-end <code>useHasProjectAccess</code> hides buttons (UX), back-end <code>throwIfNoProjectAccess</code> throws FORBIDDEN (security). The front end is bypassable; <strong>the real gate is the back end</strong> — front-end hiding must always have back-end enforcement behind it.</li>
    <li><strong>API key two-tier hash</strong>: <code>fastHashedSecretKey</code>=sha256 (deterministic, for O(1) fast lookup, cacheable) + <code>hashedSecretKey</code>=bcrypt (salted slow, secure) + <code>displaySecretKey</code> (masked display). The sk cleartext is returned only at creation; verification computes the fast hash, looks up Redis→PG, legacy keys verified by bcrypt then upgraded, nonexistent keys cached as a sentinel to stop DB hammering.</li>
    <li><strong>SCIM enterprise automation</strong>: a standard protocol letting Okta/Azure AD auto-provision/deprovision Langfuse users (have on joining, gone on leaving), avoiding manual add/delete misses. An EE capability, leading into the next lesson's open-core & entitlements.</li>
  </ul>
</div>
""")

LESSON_49 = {"zh": "\n".join(_ZH49), "en": "\n".join(_EN49)}


# ══════════════════════════════════════════════════════════════════════
# L50 · 开源核与权益 / Open-core & entitlements
# ══════════════════════════════════════════════════════════════════════
_ZH50 = []
_EN50 = []

# (L50 sections below)

_ZH50.append(r"""
<p class="lead">
Langfuse 是<strong>开源</strong>的——你现在读的这套源码，从摄取到查询、从评估到自动化，<strong>全都摆在公开仓库里</strong>。但它又是一家<strong>公司</strong>，得靠卖东西活下去。这两件事怎么共存？答案是 <strong>open-core（开源核）</strong>商业模式：核心免费开源，少数<strong>企业级功能</strong>（审计日志、数据保留策略、多租户 SSO、admin API…）需要<strong>付费计划或企业许可证</strong>才能启用。妙的是，这些「付费功能」的代码<strong>也是开源的、就在这个仓库里</strong>——你能读、能学，但要在生产里用，得有相应的 <strong>plan（计划）</strong>。
这一课讲这套「门票系统」怎么用极少的代码实现：一张 <code>entitlementAccess</code> 总表把每个 plan 映射到「能用哪些功能、各有什么额度」，一个 <code>hasEntitlement()</code> 函数就是所有功能门口的那道闸。还会看到自托管版怎么用一把 <code>langfuse_ee_</code> 开头的许可证密钥解锁企业功能。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  open-core 像一家<strong>「菜谱全公开的餐厅」</strong>：它把<strong>所有菜的做法</strong>都印在墙上、任人抄走自己回家做（开源——代码全公开、可自托管）。那它靠什么赚钱？靠<strong>会员制的「招牌服务」</strong>：普通客人能吃到绝大多数菜（免费核心功能），但某些<strong>高级服务</strong>——比如「专属包厢」「无限续杯」「私人厨师上门」（审计日志、无限额度、多租户 SSO）——得<strong>办张会员卡（plan）</strong>才享受。
  关键在于餐厅怎么<strong>验会员</strong>：门口不是每个服务各设一个保安，而是<strong>一张总表</strong>写明「金卡能享哪些服务、银卡哪些、普通客人哪些」，再加<strong>一个统一的验卡动作</strong>——你点任何高级服务，服务员都只做同一件事：<strong>查你的卡在不在这张服务的允许名单里</strong>（<code>hasEntitlement</code>）。自己在家照菜谱做（自托管）也想解锁高级服务？那得买一张<strong>「企业授权证书」</strong>（<code>langfuse_ee_</code> 许可证密钥）。
</div>
""")

# (L50 sec1 below)

_ZH50.append(r"""
<h2>开源核：全代码开放，少数功能按 plan 解锁</h2>
<p>先厘清一个常见误解：open-core <strong>不是「一半开源一半闭源」</strong>。Langfuse 这个仓库里<strong>所有功能的代码都是开放的</strong>——包括那些「企业级」功能。区别只在<strong>运行时能不能启用</strong>：每个组织挂着一个 <code>plan</code>，免费的默认是 <code>"oss"</code>（自托管开源版），付费的有云上三档 <code>cloud:hobby / core / pro / enterprise</code>，以及自托管两档 <code>self-hosted:pro / enterprise</code>。<code>isCloudPlan</code> / <code>isSelfHostedPlan</code> 这两个小助手按前缀区分它们。功能用不用得了，全看你的 plan 在不在那张允许名单里。</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="开源核模型：整个仓库代码全开放(核心+企业级功能都能读)，但运行时按组织的plan解锁——oss免费(自托管开源)、cloud三档(hobby/core/pro/enterprise)、self-hosted两档(pro/enterprise)；plan决定能启用哪些entitlement">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">代码全公开；功能按 plan 解锁</text>
  <rect x="30" y="40" width="300" height="180" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="180" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">整个仓库（全部开源）</text>
  <rect x="48" y="74" width="264" height="48" rx="7" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="180" y="94" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">免费核心（人人可用）</text><text x="180" y="110" text-anchor="middle" font-size="6.2" fill="var(--muted)">摄取·查询·评估·prompt·dashboard…</text>
  <rect x="48" y="130" width="264" height="78" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="180" y="150" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">企业级功能（代码也开源！）</text><text x="180" y="166" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">审计日志·数据保留·多租户SSO</text><text x="180" y="178" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">admin API·定时blob导出·UI定制…</text><text x="180" y="194" text-anchor="middle" font-size="6.0" fill="var(--faint)">能读能学，但启用要 plan/license</text>
  <rect x="390" y="46" width="305" height="168" rx="10" fill="var(--bg)" stroke="var(--accent)"/><text x="542" y="66" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">组织的 plan 决定能启用哪些</text>
  <rect x="406" y="78" width="135" height="30" rx="6" fill="var(--teal)" opacity="0.13" stroke="var(--teal)"/><text x="473" y="97" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--teal)">oss（默认·免费）</text>
  <rect x="552" y="78" width="130" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="617" y="91" text-anchor="middle" font-size="6.4" fill="var(--ink)">cloud:hobby/core</text><text x="617" y="102" text-anchor="middle" font-size="5.6" fill="var(--muted)">云·入门</text>
  <rect x="406" y="116" width="135" height="32" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="473" y="129" text-anchor="middle" font-size="6.4" fill="var(--ink)">cloud:pro/enterprise</text><text x="473" y="140" text-anchor="middle" font-size="5.6" fill="var(--muted)">云·高级</text>
  <rect x="552" y="116" width="130" height="32" rx="6" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="617" y="129" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">self-hosted:pro</text><text x="617" y="140" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">/enterprise</text>
  <text x="542" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">isCloudPlan / isSelfHostedPlan 按前缀区分</text>
  <text x="542" y="188" text-anchor="middle" font-size="6.6" fill="var(--faint)">plan 越高，allow 名单越长、额度越大</text>
  <text x="542" y="204" text-anchor="middle" font-size="6.6" fill="var(--faint)">下一节：entitlementAccess 总表 + hasEntitlement 闸</text>
  <line x1="330" y1="168" x2="388" y2="130" stroke="var(--accent)" stroke-width="1.3"/><polygon points="388,130 379,131 383,138" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>开源核分层</b>：代码全在仓库里（<code>web/src/features/entitlements/*</code>、<code>packages/shared/src/server/ee/*</code> 也开源）。Plan 见 <code>plans.ts:21</code>（<code>type Plan = keyof typeof planLabels</code>，含 cloud:hobby/core/pro/enterprise + self-hosted:pro/enterprise），默认 <code>"oss"</code>；<code>plans.ts:26-27</code> <code>isCloudPlan</code>/<code>isSelfHostedPlan</code> 按前缀判断。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">免费</span><span class="name">oss 开源核（默认 plan）</span></div><div class="ld">自托管下来直接能用的全部核心：摄取、查询、评估、prompt、dashboard、自动化……占了功能的绝大多数。组织没有付费 plan 时，<code>plan ?? "oss"</code> 兜底到这里——<strong>默认落到免费，而非默认付费</strong>。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">付费</span><span class="name">cloud / self-hosted 各档</span></div><div class="ld">云上 hobby→core→pro→enterprise、自托管 pro→enterprise，逐级解锁更多企业功能、放宽更多额度。同一套代码，按 plan 给不同组织开不同的「门」。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">透明</span><span class="name">企业功能也开源</span></div><div class="ld">关键区别于「闭源商业版」：审计日志、数据保留、多租户 SSO 这些企业功能的<strong>代码同样公开</strong>，放在 <code>ee/</code> 与 <code>shared/.../ee/</code>。你能审计、能学习、能给自己改——只是生产启用需要授权。</div></div>
</div>
""")

# (L50 sec2 below)

_ZH50.append(r"""
<h2>一张总表 + 一道闸：entitlementAccess 与 hasEntitlement</h2>
<p>整套「门票系统」的心脏，是一张 <code>entitlementAccess: Record&lt;Plan, {entitlements, entitlementLimits}&gt;</code> 总表，把<strong>每个 plan</strong> 映射到两样东西：<strong>① entitlements</strong>（二元开关：某功能<strong>有/没有</strong>，如 <code>data-retention</code>、<code>audit-logs</code>、<code>admin-api</code>）；<strong>② entitlementLimits</strong>（数值额度：某资源<strong>能用多少</strong>，如 <code>organization-member-count</code>、<code>data-access-days</code>、<code>monitor-count</code>，值是<strong>数字</strong>表示有上限，或 <code>false</code> 表示无限）。比如 <code>cloud:hobby</code> 限 2 个成员、30 天数据、1 个标注队列；<code>cloud:core</code> 放宽到成员无限、90 天；<code>cloud:pro</code> 再加上 <code>data-retention</code> 功能。</p>

<p>所有功能门口就一道闸：<code>hasEntitlement({ sessionUser, orgId, entitlement })</code>。它的逻辑朴素得让人安心：<strong>① admin 直接放行</strong>；<strong>② 找到所属组织、取其 <code>plan</code>，没有就兜底成 <code>"oss"</code></strong>；<strong>③ 查这个 plan 的 entitlements 名单里<strong>含不含</strong>所求功能</strong>。就这三步。功能代码里不写「if plan==pro」散落各处，而是统一问这道闸——和第 49 课 RBAC「问 scope」如出一辙：<strong>把「谁能用什么」收敛到一张表 + 一个函数</strong>。</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="entitlement闸：功能代码调hasEntitlement(orgId,entitlement)，先admin放行，再取org.plan(无则oss兜底)，查entitlementAccess[plan].entitlements是否includes该功能，是则放行否则拒绝；entitlementLimits管数值额度number或false无限">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">所有功能共用一道闸：hasEntitlement</text>
  <rect x="24" y="60" width="150" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="82" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">功能代码</text><text x="99" y="98" text-anchor="middle" font-size="6.2" fill="var(--muted)">想用 data-retention？</text><text x="99" y="109" text-anchor="middle" font-size="6.0" fill="var(--faint)">先问闸</text>
  <rect x="205" y="48" width="170" height="92" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="290" y="68" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">hasEntitlement</text><text x="290" y="85" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">① admin？→ 直接放行</text><text x="290" y="99" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">② org.plan ?? "oss"</text><text x="290" y="113" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">③ 查 plan 名单 includes?</text><text x="290" y="130" text-anchor="middle" font-size="5.8" fill="var(--faint)">默认兜底到免费，不是付费</text>
  <rect x="410" y="44" width="285" height="68" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="552" y="62" text-anchor="middle" font-size="7.8" font-weight="700" fill="var(--accent-ink)">entitlementAccess 总表 Record&lt;Plan,…&gt;</text><text x="552" y="79" text-anchor="middle" font-size="6.2" fill="var(--muted)">cloud:hobby → {entitlements:[…], limits:{members:2,days:30}}</text><text x="552" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">cloud:core → {…, members:false(无限), days:90}</text><text x="552" y="105" text-anchor="middle" font-size="6.2" fill="var(--muted)">cloud:pro → {+data-retention, queues:false}</text>
  <rect x="410" y="124" width="285" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="552" y="141" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">entitlementLimits：数值额度</text><text x="552" y="155" text-anchor="middle" font-size="6.0" fill="var(--muted)">number=有上限 · false=无限（hasEntitlementLimit 查）</text>
  <rect x="205" y="166" width="170" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="290" y="184" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">含 → 放行 / 不含 → 拒绝</text><text x="290" y="198" text-anchor="middle" font-size="6.0" fill="var(--muted)">功能据此显示/启用或隐藏/禁用</text>
  <line x1="174" y1="88" x2="203" y2="92" stroke="var(--accent)" stroke-width="1.3"/><polygon points="203,92 194,88 194,96" fill="var(--accent)"/>
  <line x1="375" y1="92" x2="408" y2="86" stroke="var(--accent)" stroke-width="1.3"/><polygon points="408,86 399,84 400,92" fill="var(--accent)"/>
  <line x1="290" y1="140" x2="290" y2="164" stroke="var(--teal)" stroke-width="1.3"/><polygon points="290,164 286,155 294,155" fill="var(--teal)"/>
</svg>
<div class="figcap"><b>总表 + 闸</b>：<code>entitlements.ts:54</code> <code>entitlementAccess: Record&lt;Plan, {entitlements, entitlementLimits}&gt;</code>（entitlements:6 二元功能、entitlementLimits:38 数值额度 <code>number|false</code>）。<code>hasEntitlement.ts:17</code>：<code>:18</code> admin→true、<code>:25</code> <code>org.plan ?? "oss"</code>、<code>:40</code> <code>entitlementAccess[plan].entitlements.includes(entitlement)</code>。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/entitlements/constants/entitlements.ts · server/hasEntitlement.ts</span><span class="ln">总表 + 闸</span></div>
  <pre class="code"><span class="cm">// 二元功能开关 + 数值额度（number=有上限 / false=无限）</span>
<span class="kw">export const</span> entitlements = [<span class="st">"audit-logs"</span>, <span class="st">"data-retention"</span>, <span class="st">"admin-api"</span>,
  <span class="st">"cloud-multi-tenant-sso"</span>, <span class="st">"scheduled-blob-exports"</span>, …] <span class="kw">as const</span>;

<span class="kw">export const</span> entitlementAccess: Record&lt;Plan, {…}&gt; = {
  <span class="st">"cloud:hobby"</span>: { entitlements: […], entitlementLimits: {
                     <span class="st">"organization-member-count"</span>: <span class="st">2</span>, <span class="st">"data-access-days"</span>: <span class="st">30</span> } },
  <span class="st">"cloud:core"</span>:  { entitlements: […], entitlementLimits: {
                     <span class="st">"organization-member-count"</span>: <span class="kw">false</span><span class="cm">/*无限*/</span>, <span class="st">"data-access-days"</span>: <span class="st">90</span> } },
  <span class="st">"cloud:pro"</span>:   { entitlements: [… <span class="st">"data-retention"</span>], … },
  <span class="cm">// self-hosted:pro/enterprise, cloud:enterprise …</span>
};

<span class="cm">// 所有功能门口的同一道闸</span>
<span class="kw">export const</span> <span class="fn">hasEntitlement</span> = (p) =&gt; {
  <span class="kw">if</span> (p.sessionUser.admin) <span class="kw">return true</span>;                 <span class="cm">// admin 直接放行</span>
  <span class="kw">const</span> plan = org?.plan ?? <span class="st">"oss"</span>;                     <span class="cm">// 默认兜底到免费版</span>
  <span class="kw">return</span> entitlementAccess[plan].entitlements.<span class="fn">includes</span>(p.entitlement);
};</pre>
</div>

<div class="cols">
  <div class="col"><h4>🔘 entitlement（二元）</h4><p>某功能<strong>有或没有</strong>：<code>audit-logs</code>、<code>data-retention</code>、<code>admin-api</code>、<code>cloud-multi-tenant-sso</code>…由 <code>hasEntitlement</code> 查「plan 名单含不含」，返回 true/false。</p></div>
  <div class="col"><h4>🔢 entitlementLimit（数值）</h4><p>某资源<strong>能用多少</strong>：<code>organization-member-count</code>、<code>data-access-days</code>、<code>monitor-count</code>…值是 <strong>number</strong>（有上限）或 <code>false</code>（无限），由 <code>hasEntitlementLimit</code> 查。</p></div>
  <div class="col"><h4>🔑 license（自托管）</h4><p>自托管解锁企业层：<code>LANGFUSE_EE_LICENSE_KEY</code> 以 <code>langfuse_ee_</code> 开头才算企业（<code>langfuse_pro_</code> 不算）；Cloud 任何区域天然有企业功能。</p></div>
</div>
""")

# (L50 sec3 below)

_ZH50.append(r"""
<h2>自托管的解锁钥匙：EE 许可证</h2>
<p>云上版本由 Langfuse 托管，plan 写在数据库里。但<strong>自己部署</strong>的版本怎么证明「我买了企业版」？靠一把<strong>许可证密钥</strong>。<code>isEnterpriseLicenseAvailable()</code> 的判断很干脆：<strong>① 是 Langfuse Cloud（任何区域）→ 直接有企业功能</strong>；<strong>② 自托管 → 看环境变量 <code>LANGFUSE_EE_LICENSE_KEY</code> 是否以 <code>langfuse_ee_</code> 开头</strong>。注意一个细节：<code>langfuse_pro_</code> 开头的 Pro 许可证<strong>不算</strong>企业级——前缀本身就编码了授权层级。这把钥匙插对了，自托管实例才解锁那些企业 entitlement。</p>

<table class="t">
  <thead><tr><th>问题</th><th>open-core 的答案</th></tr></thead>
  <tbody>
    <tr><td>企业功能的代码闭源吗？</td><td><b>不</b>，全在公开仓库（<code>ee/</code>、<code>shared/.../ee/</code>），能读能学能自改</td></tr>
    <tr><td>那靠什么区分免费/付费？</td><td>运行时的 <b>plan</b> + <code>hasEntitlement</code> 闸，而非「代码有没有」</td></tr>
    <tr><td>没有 plan 的组织怎么办？</td><td><code>plan ?? "oss"</code> <b>兜底到免费</b>——默认最安全的（最少权益），不是默认付费</td></tr>
    <tr><td>自托管怎么解锁企业版？</td><td>设 <code>LANGFUSE_EE_LICENSE_KEY=langfuse_ee_…</code>（Pro 的 <code>langfuse_pro_</code> 不算企业）</td></tr>
    <tr><td>EE 代码放哪、谁能依赖它？</td><td>独立包 <code>@langfuse/ee</code>；依赖方向 <code>web → @langfuse/ee → @langfuse/shared</code></td></tr>
  </tbody>
</table>

<p>把这张表连起来看，open-core 的精巧就清楚了：<strong>「能不能用」与「有没有代码」彻底解耦</strong>。代码 100% 公开（透明、可审计、社区可贡献），而商业边界靠一层<strong>轻薄的运行时门控</strong>（plan + entitlement + license）划出。这让 Langfuse 既是真开源、又能有可持续的商业模式——两者不矛盾。</p>
""")

_ZH50.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>为什么把「能不能用某功能」做成一道统一的 <code>hasEntitlement</code> 闸 + 一张 <code>entitlementAccess</code> 总表，而不是在每个功能里各自写「if plan == pro」？</strong> 这和第 49 课 RBAC 用「角色→scope」是同一种智慧，原因也一样：<strong>收敛权威、便于演进与审计</strong>。商业 plan 会变——加一档套餐、调一次额度、把某功能从 pro 下放到 core，都是常事。如果「pro 才能用 X」这种判断散落在几十处功能代码里，每次调整都要全仓库搜改，极易漏、易错、还难复盘「到底哪个 plan 能用什么」。把它收进一张声明式总表后：调整商业策略=改这张表的一行，功能代码完全不动；想知道「pro 包含什么」=读表的一行。<strong>把易变的商业规则从稳定的功能逻辑里抽出来、集中声明，是让系统能跟上商业节奏的关键。</strong><br><br>
  <strong>为什么没有 plan 的组织要默认兜底成 <code>"oss"</code>（免费），而不是报错或默认给最高权限？</strong> 这是一个<strong>「fail-safe（失败安全）」默认值</strong>的选择，方向很重要。如果默认给最高权限，一旦某组织的 plan 字段因 bug、迁移、数据缺失而读不到，它就会<strong>意外解锁所有付费功能</strong>——商业上漏损、安全上越权。如果默认报错，又会让「绝大多数自托管开源用户」（他们本就该是 oss）寸步难行。兜底到 <code>"oss"</code> 恰好两全：开源用户开箱即用（这是最常见、最该顺滑的路径），而付费功能<strong>默认是关的</strong>、必须由明确的 plan 或 license 主动打开。<strong>安全的默认值，应该是「权限最小、影响最轻」的那一个</strong>——entitlement 默认关、登录默认拒、IP 解析失败默认拦（第 44 课），都是同一条原则的不同侧影。
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>open-core ≠ 半闭源</strong>：Langfuse 全部功能（含企业级）的代码都在公开仓库，可读可学可自改。免费与付费的区别在<strong>运行时能否启用</strong>，不在「有没有代码」。</li>
    <li><strong>plan 分层</strong>：组织挂一个 <code>plan</code>，默认 <code>"oss"</code>（免费自托管），付费有 cloud:hobby/core/pro/enterprise + self-hosted:pro/enterprise；<code>isCloudPlan</code>/<code>isSelfHostedPlan</code> 按前缀分。</li>
    <li><strong>总表 + 一道闸</strong>：<code>entitlementAccess: Record&lt;Plan,{entitlements, entitlementLimits}&gt;</code> 把每个 plan 映射到「有哪些二元功能 + 各资源额度(number/false无限)」；<code>hasEntitlement</code>（admin→true、<code>plan ?? "oss"</code>、<code>includes</code>）是所有功能共用的那道闸——收敛权威、便于演进，同第49课 RBAC 一脉。</li>
    <li><strong>EE 许可证</strong>：<code>isEnterpriseLicenseAvailable</code>——Cloud(任何区域)有企业功能；自托管看 <code>LANGFUSE_EE_LICENSE_KEY</code> 是否 <code>langfuse_ee_</code> 开头（<code>langfuse_pro_</code> 不算企业，前缀编码授权层级）。</li>
    <li><strong>fail-safe 默认</strong>：无 plan 兜底到 <code>"oss"</code>（最小权益、付费功能默认关），而非默认报错或默认全开——与「登录默认拒、IP 解析失败默认拦」同源的安全默认观。EE 代码在独立包 <code>@langfuse/ee</code>，依赖方向 <code>web→ee→shared</code>。</li>
  </ul>
</div>
""")

_EN50.append(r"""
<p class="lead">
Langfuse is <strong>open source</strong> — the source you're reading, from ingestion to query, from evaluation to automation, is <strong>all laid out in a public repo</strong>. Yet it's also a <strong>company</strong> that must sell something to survive. How do these coexist? The answer is the <strong>open-core</strong> business model: the core is free and open, while a few <strong>enterprise features</strong> (audit logs, data-retention policy, multi-tenant SSO, admin API…) require a <strong>paid plan or enterprise license</strong> to enable. The clever part: the code for these "paid features" is <strong>also open, right here in this repo</strong> — you can read and learn it, but to use it in production you need the corresponding <strong>plan</strong>.
This lesson shows how that "ticket system" is implemented with very little code: one <code>entitlementAccess</code> master table mapping each plan to "which features, with what limits," and one <code>hasEntitlement()</code> function that is the single gate in front of every feature. You'll also see how a self-hosted version unlocks enterprise features with a license key starting with <code>langfuse_ee_</code>.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Open-core is like a <strong>"restaurant with a fully-public recipe book"</strong>: it prints <strong>every dish's recipe</strong> on the wall, free for anyone to copy and cook at home (open source — code fully public, self-hostable). So how does it make money? Through a <strong>membership for "signature service"</strong>: regular guests can eat the vast majority of dishes (free core features), but some <strong>premium services</strong> — a "private room," "unlimited refills," "a personal chef at home" (audit logs, unlimited quotas, multi-tenant SSO) — require a <strong>membership card (plan)</strong>.
  The key is how the restaurant <strong>verifies membership</strong>: not a separate bouncer per service, but <strong>one master table</strong> stating "gold card enjoys these services, silver these, regular guests these," plus <strong>one unified card-check action</strong> — for any premium service, the waiter does the same one thing: <strong>check whether your card is on that service's allow list</strong> (<code>hasEntitlement</code>). Cooking from the recipe at home (self-hosting) and want premium service too? Then buy an <strong>"enterprise license certificate"</strong> (a <code>langfuse_ee_</code> license key).
</div>

<h2>Open core: all code open, a few features unlocked by plan</h2>
<p>First clear up a common misconception: open-core is <strong>not "half open-source, half closed"</strong>. In this Langfuse repo <strong>all features' code is open</strong> — including the "enterprise" ones. The difference is only <strong>whether they can be enabled at runtime</strong>: each org carries a <code>plan</code>, free defaults to <code>"oss"</code> (self-hosted open-source), paid has three cloud tiers <code>cloud:hobby / core / pro / enterprise</code> plus two self-hosted <code>self-hosted:pro / enterprise</code>. The helpers <code>isCloudPlan</code> / <code>isSelfHostedPlan</code> distinguish them by prefix. Whether a feature works hinges entirely on whether your plan is on its allow list.</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="Open-core model: the entire repo code is open (core + enterprise features both readable), but unlocked at runtime by the org's plan — oss free (self-hosted open-source), cloud tiers (hobby/core/pro/enterprise), self-hosted tiers (pro/enterprise); the plan decides which entitlements can be enabled">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Code all public; features unlocked by plan</text>
  <rect x="30" y="40" width="300" height="180" rx="10" fill="var(--blue-soft)" stroke="var(--blue)" stroke-width="2"/><text x="180" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--ink)">the entire repo (all open source)</text>
  <rect x="48" y="74" width="264" height="48" rx="7" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="180" y="94" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">free core (everyone)</text><text x="180" y="110" text-anchor="middle" font-size="6.2" fill="var(--muted)">ingest·query·eval·prompt·dashboard…</text>
  <rect x="48" y="130" width="264" height="78" rx="7" fill="var(--accent-soft)" stroke="var(--accent)"/><text x="180" y="150" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">enterprise features (code also open!)</text><text x="180" y="166" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">audit logs·data retention·multi-tenant SSO</text><text x="180" y="178" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">admin API·scheduled blob export·UI customization…</text><text x="180" y="194" text-anchor="middle" font-size="6.0" fill="var(--faint)">read & learn, but enabling needs plan/license</text>
  <rect x="390" y="46" width="305" height="168" rx="10" fill="var(--bg)" stroke="var(--accent)"/><text x="542" y="66" text-anchor="middle" font-size="8.5" font-weight="700" fill="var(--accent-ink)">the org's plan decides what can be enabled</text>
  <rect x="406" y="78" width="135" height="30" rx="6" fill="var(--teal)" opacity="0.13" stroke="var(--teal)"/><text x="473" y="97" text-anchor="middle" font-size="6.8" font-weight="700" fill="var(--teal)">oss (default · free)</text>
  <rect x="552" y="78" width="130" height="30" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="617" y="91" text-anchor="middle" font-size="6.4" fill="var(--ink)">cloud:hobby/core</text><text x="617" y="102" text-anchor="middle" font-size="5.6" fill="var(--muted)">cloud · entry</text>
  <rect x="406" y="116" width="135" height="32" rx="6" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="473" y="129" text-anchor="middle" font-size="6.4" fill="var(--ink)">cloud:pro/enterprise</text><text x="473" y="140" text-anchor="middle" font-size="5.6" fill="var(--muted)">cloud · premium</text>
  <rect x="552" y="116" width="130" height="32" rx="6" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="617" y="129" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">self-hosted:pro</text><text x="617" y="140" text-anchor="middle" font-size="6.0" fill="var(--accent-ink)">/enterprise</text>
  <text x="542" y="172" text-anchor="middle" font-size="6.6" fill="var(--muted)">isCloudPlan / isSelfHostedPlan distinguish by prefix</text>
  <text x="542" y="188" text-anchor="middle" font-size="6.6" fill="var(--faint)">higher plan = longer allow list, larger quotas</text>
  <text x="542" y="204" text-anchor="middle" font-size="6.6" fill="var(--faint)">next: entitlementAccess master table + hasEntitlement gate</text>
  <line x1="330" y1="168" x2="388" y2="130" stroke="var(--accent)" stroke-width="1.3"/><polygon points="388,130 379,131 383,138" fill="var(--accent)"/>
</svg>
<div class="figcap"><b>Open-core layering</b>: the code is all in the repo (<code>web/src/features/entitlements/*</code>, <code>packages/shared/src/server/ee/*</code> are open too). Plans at <code>plans.ts:21</code> (<code>type Plan = keyof typeof planLabels</code>, including cloud:hobby/core/pro/enterprise + self-hosted:pro/enterprise), defaulting to <code>"oss"</code>; <code>plans.ts:26-27</code> <code>isCloudPlan</code>/<code>isSelfHostedPlan</code> judge by prefix.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">free</span><span class="name">oss open core (default plan)</span></div><div class="ld">Everything a self-host install runs out of the box: ingestion, query, eval, prompt, dashboard, automation… the vast majority of features. When an org has no paid plan, <code>plan ?? "oss"</code> falls back here — <strong>defaulting to free, not to paid</strong>.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">paid</span><span class="name">cloud / self-hosted tiers</span></div><div class="ld">Cloud hobby→core→pro→enterprise, self-hosted pro→enterprise, progressively unlocking more enterprise features and loosening more quotas. Same code, different "doors" opened for different orgs by plan.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">transparent</span><span class="name">enterprise features are open too</span></div><div class="ld">The key difference from a "closed-source commercial edition": the <strong>code</strong> for audit logs, data retention, multi-tenant SSO is <strong>equally public</strong>, in <code>ee/</code> and <code>shared/.../ee/</code>. You can audit, learn, and modify it for yourself — only production enablement needs a license.</div></div>
</div>
""")

_EN50.append(r"""
<h2>One master table + one gate: entitlementAccess and hasEntitlement</h2>
<p>The heart of the whole "ticket system" is one <code>entitlementAccess: Record&lt;Plan, {entitlements, entitlementLimits}&gt;</code> master table, mapping <strong>each plan</strong> to two things: <strong>① entitlements</strong> (binary switches: a feature <strong>on/off</strong>, like <code>data-retention</code>, <code>audit-logs</code>, <code>admin-api</code>); <strong>② entitlementLimits</strong> (numeric quotas: how much of a resource you may use, like <code>organization-member-count</code>, <code>data-access-days</code>, <code>monitor-count</code> — the value is a <strong>number</strong> for a cap, or <code>false</code> for unlimited). For example <code>cloud:hobby</code> caps at 2 members, 30 days of data, 1 annotation queue; <code>cloud:core</code> loosens to unlimited members, 90 days; <code>cloud:pro</code> additionally adds the <code>data-retention</code> feature.</p>

<p>There's just one gate in front of every feature: <code>hasEntitlement({ sessionUser, orgId, entitlement })</code>. Its logic is reassuringly plain: <strong>① admin passes outright</strong>; <strong>② find the owning org, take its <code>plan</code>, falling back to <code>"oss"</code> if none</strong>; <strong>③ check whether this plan's entitlements list <strong>includes</strong> the requested feature</strong>. Just those three steps. Feature code doesn't scatter "if plan==pro" everywhere but asks this one gate — exactly like Lesson 49's RBAC "ask the scope": <strong>converge "who can use what" into one table + one function</strong>.</p>

<div class="fig">
<svg viewBox="0 0 720 230" role="img" aria-label="entitlement gate: feature code calls hasEntitlement(orgId,entitlement), admin passes first, then take org.plan (fall back to oss if none), check whether entitlementAccess[plan].entitlements includes the feature, allow if yes else deny; entitlementLimits manage numeric quotas number or false unlimited">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">All features share one gate: hasEntitlement</text>
  <rect x="24" y="60" width="150" height="56" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="99" y="82" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">feature code</text><text x="99" y="98" text-anchor="middle" font-size="6.2" fill="var(--muted)">want data-retention?</text><text x="99" y="109" text-anchor="middle" font-size="6.0" fill="var(--faint)">ask the gate first</text>
  <rect x="205" y="48" width="170" height="92" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="290" y="68" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">hasEntitlement</text><text x="290" y="85" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">① admin? → pass outright</text><text x="290" y="99" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">② org.plan ?? "oss"</text><text x="290" y="113" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">③ plan list includes?</text><text x="290" y="130" text-anchor="middle" font-size="5.8" fill="var(--faint)">defaults to free, not paid</text>
  <rect x="410" y="44" width="285" height="68" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="552" y="62" text-anchor="middle" font-size="7.8" font-weight="700" fill="var(--accent-ink)">entitlementAccess master Record&lt;Plan,…&gt;</text><text x="552" y="79" text-anchor="middle" font-size="6.2" fill="var(--muted)">cloud:hobby → {entitlements:[…], limits:{members:2,days:30}}</text><text x="552" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">cloud:core → {…, members:false(unlimited), days:90}</text><text x="552" y="105" text-anchor="middle" font-size="6.2" fill="var(--muted)">cloud:pro → {+data-retention, queues:false}</text>
  <rect x="410" y="124" width="285" height="40" rx="9" fill="var(--bg)" stroke="var(--faint)"/><text x="552" y="141" text-anchor="middle" font-size="7" font-weight="700" fill="var(--accent-ink)">entitlementLimits: numeric quotas</text><text x="552" y="155" text-anchor="middle" font-size="6.0" fill="var(--muted)">number=capped · false=unlimited (hasEntitlementLimit checks)</text>
  <rect x="205" y="166" width="170" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="290" y="184" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--teal)">includes → allow / not → deny</text><text x="290" y="198" text-anchor="middle" font-size="6.0" fill="var(--muted)">feature shows/enables or hides/disables</text>
  <line x1="174" y1="88" x2="203" y2="92" stroke="var(--accent)" stroke-width="1.3"/><polygon points="203,92 194,88 194,96" fill="var(--accent)"/>
  <line x1="375" y1="92" x2="408" y2="86" stroke="var(--accent)" stroke-width="1.3"/><polygon points="408,86 399,84 400,92" fill="var(--accent)"/>
  <line x1="290" y1="140" x2="290" y2="164" stroke="var(--teal)" stroke-width="1.3"/><polygon points="290,164 286,155 294,155" fill="var(--teal)"/>
</svg>
<div class="figcap"><b>Master table + gate</b>: <code>entitlements.ts:54</code> <code>entitlementAccess: Record&lt;Plan, {entitlements, entitlementLimits}&gt;</code> (entitlements:6 binary features, entitlementLimits:38 numeric quotas <code>number|false</code>). <code>hasEntitlement.ts:17</code>: <code>:18</code> admin→true, <code>:25</code> <code>org.plan ?? "oss"</code>, <code>:40</code> <code>entitlementAccess[plan].entitlements.includes(entitlement)</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">web/src/features/entitlements/constants/entitlements.ts · server/hasEntitlement.ts</span><span class="ln">master table + gate</span></div>
  <pre class="code"><span class="cm">// binary feature switches + numeric quotas (number=capped / false=unlimited)</span>
<span class="kw">export const</span> entitlements = [<span class="st">"audit-logs"</span>, <span class="st">"data-retention"</span>, <span class="st">"admin-api"</span>,
  <span class="st">"cloud-multi-tenant-sso"</span>, <span class="st">"scheduled-blob-exports"</span>, …] <span class="kw">as const</span>;

<span class="kw">export const</span> entitlementAccess: Record&lt;Plan, {…}&gt; = {
  <span class="st">"cloud:hobby"</span>: { entitlements: […], entitlementLimits: {
                     <span class="st">"organization-member-count"</span>: <span class="st">2</span>, <span class="st">"data-access-days"</span>: <span class="st">30</span> } },
  <span class="st">"cloud:core"</span>:  { entitlements: […], entitlementLimits: {
                     <span class="st">"organization-member-count"</span>: <span class="kw">false</span><span class="cm">/*unlimited*/</span>, <span class="st">"data-access-days"</span>: <span class="st">90</span> } },
  <span class="st">"cloud:pro"</span>:   { entitlements: [… <span class="st">"data-retention"</span>], … },
  <span class="cm">// self-hosted:pro/enterprise, cloud:enterprise …</span>
};

<span class="cm">// the same one gate in front of every feature</span>
<span class="kw">export const</span> <span class="fn">hasEntitlement</span> = (p) =&gt; {
  <span class="kw">if</span> (p.sessionUser.admin) <span class="kw">return true</span>;                 <span class="cm">// admin passes outright</span>
  <span class="kw">const</span> plan = org?.plan ?? <span class="st">"oss"</span>;                     <span class="cm">// default fall back to free</span>
  <span class="kw">return</span> entitlementAccess[plan].entitlements.<span class="fn">includes</span>(p.entitlement);
};</pre>
</div>

<div class="cols">
  <div class="col"><h4>🔘 entitlement (binary)</h4><p>A feature <strong>on or off</strong>: <code>audit-logs</code>, <code>data-retention</code>, <code>admin-api</code>, <code>cloud-multi-tenant-sso</code>… <code>hasEntitlement</code> checks "is it in the plan's list", returning true/false.</p></div>
  <div class="col"><h4>🔢 entitlementLimit (numeric)</h4><p>How much of a resource: <code>organization-member-count</code>, <code>data-access-days</code>, <code>monitor-count</code>… the value is a <strong>number</strong> (capped) or <code>false</code> (unlimited), checked by <code>hasEntitlementLimit</code>.</p></div>
  <div class="col"><h4>🔑 license (self-host)</h4><p>Self-hosting unlocks the enterprise tier: <code>LANGFUSE_EE_LICENSE_KEY</code> must start with <code>langfuse_ee_</code> to count as enterprise (<code>langfuse_pro_</code> doesn't); Cloud in any region has enterprise features natively.</p></div>
</div>
""")

_EN50.append(r"""
<h2>The self-hosted unlock key: the EE license</h2>
<p>The cloud version is hosted by Langfuse, with the plan written in the database. But how does a <strong>self-deployed</strong> version prove "I bought enterprise"? Via a <strong>license key</strong>. <code>isEnterpriseLicenseAvailable()</code>'s decision is crisp: <strong>① is it Langfuse Cloud (any region) → enterprise features directly</strong>; <strong>② self-hosted → check whether the env var <code>LANGFUSE_EE_LICENSE_KEY</code> starts with <code>langfuse_ee_</code></strong>. Note one detail: a Pro license starting with <code>langfuse_pro_</code> does <strong>not</strong> count as enterprise — the prefix itself encodes the authorization tier. With this key plugged in correctly, a self-hosted instance unlocks those enterprise entitlements.</p>

<table class="t">
  <thead><tr><th>Question</th><th>Open-core's answer</th></tr></thead>
  <tbody>
    <tr><td>Is enterprise-feature code closed?</td><td><b>No</b>, all in the public repo (<code>ee/</code>, <code>shared/.../ee/</code>), readable, learnable, self-modifiable</td></tr>
    <tr><td>Then what distinguishes free/paid?</td><td>the runtime <b>plan</b> + <code>hasEntitlement</code> gate, not "whether the code exists"</td></tr>
    <tr><td>What about orgs with no plan?</td><td><code>plan ?? "oss"</code> <b>falls back to free</b> — defaults to the safest (least entitlement), not to paid</td></tr>
    <tr><td>How does self-hosting unlock enterprise?</td><td>set <code>LANGFUSE_EE_LICENSE_KEY=langfuse_ee_…</code> (Pro's <code>langfuse_pro_</code> isn't enterprise)</td></tr>
    <tr><td>Where's EE code, who can depend on it?</td><td>a separate package <code>@langfuse/ee</code>; dependency direction <code>web → @langfuse/ee → @langfuse/shared</code></td></tr>
  </tbody>
</table>

<p>Connect the rows and open-core's elegance is clear: <strong>"can use" and "has code" are fully decoupled</strong>. The code is 100% public (transparent, auditable, community-contributable), while the commercial boundary is drawn by a <strong>thin runtime gate</strong> (plan + entitlement + license). This lets Langfuse be truly open source AND have a sustainable business model — the two aren't in conflict.</p>
""")

_EN50.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Why make "can you use a feature" a unified <code>hasEntitlement</code> gate + one <code>entitlementAccess</code> master table, rather than "if plan == pro" in each feature?</strong> Same wisdom as Lesson 49's RBAC "role→scope," for the same reason: <strong>converge authority, ease evolution and auditing</strong>. Commercial plans change — adding a tier, adjusting a quota, demoting a feature from pro to core are all routine. If "pro can use X" judgments are scattered across dozens of feature sites, every change means a repo-wide search-and-edit, easy to miss, error-prone, and hard to review "which plan can use what." Folding it into one declarative master table: change commercial strategy = edit one row of this table, feature code untouched; want to know "what does pro include" = read one row. <strong>Extracting volatile commercial rules from stable feature logic and declaring them centrally is the key to keeping the system in step with the business.</strong><br><br>
  <strong>Why does an org with no plan default to <code>"oss"</code> (free), rather than erroring or defaulting to the highest privileges?</strong> This is a <strong>"fail-safe" default</strong> choice, and the direction matters. Default to the highest privileges and the moment an org's plan field can't be read (a bug, a migration, missing data), it <strong>accidentally unlocks all paid features</strong> — a commercial leak and a privilege overreach. Default to erroring and you stall "the vast majority of self-hosted open-source users" (who should be oss anyway). Falling back to <code>"oss"</code> gets both right: open-source users work out of the box (the most common, smoothest path), while paid features are <strong>off by default</strong>, opened only by an explicit plan or license. <strong>A safe default should be the one with "least privilege, lightest impact"</strong> — entitlement defaults off, login defaults deny, IP-resolution failure defaults block (Lesson 44) — all facets of the same principle.
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Open-core ≠ half-closed</strong>: all Langfuse features' code (incl. enterprise) is in the public repo, readable, learnable, self-modifiable. Free vs paid lies in <strong>runtime enablement</strong>, not "whether the code exists."</li>
    <li><strong>Plan tiering</strong>: an org carries a <code>plan</code>, defaulting to <code>"oss"</code> (free self-host), paid has cloud:hobby/core/pro/enterprise + self-hosted:pro/enterprise; <code>isCloudPlan</code>/<code>isSelfHostedPlan</code> split by prefix.</li>
    <li><strong>Master table + one gate</strong>: <code>entitlementAccess: Record&lt;Plan,{entitlements, entitlementLimits}&gt;</code> maps each plan to "which binary features + each resource's quota (number/false unlimited)"; <code>hasEntitlement</code> (admin→true, <code>plan ?? "oss"</code>, <code>includes</code>) is the shared gate in front of every feature — converging authority, easing evolution, of one lineage with Lesson 49's RBAC.</li>
    <li><strong>EE license</strong>: <code>isEnterpriseLicenseAvailable</code> — Cloud (any region) has enterprise features; self-hosting checks whether <code>LANGFUSE_EE_LICENSE_KEY</code> starts with <code>langfuse_ee_</code> (<code>langfuse_pro_</code> isn't enterprise; the prefix encodes the tier).</li>
    <li><strong>Fail-safe default</strong>: no plan falls back to <code>"oss"</code> (least entitlement, paid features off by default), not defaulting to error or all-on — the same safe-default view as "login defaults deny, IP-resolution failure defaults block." EE code lives in a separate package <code>@langfuse/ee</code>, dependency direction <code>web→ee→shared</code>.</li>
  </ul>
</div>
""")

LESSON_50 = {"zh": "\n".join(_ZH50), "en": "\n".join(_EN50)}


# ══════════════════════════════════════════════════════════════════════
# L51 · 自我可观测与配置 / Self-observability & config
# ══════════════════════════════════════════════════════════════════════
_ZH51 = []
_EN51 = []

# (L51 sections below)

_ZH51.append(r"""
<p class="lead">
Langfuse 是一个<strong>帮你观测 LLM 应用</strong>的工具。那它自己出问题时，靠什么观测<strong>自己</strong>？答案很「自洽」：它用<strong>同一套可观测性手段</strong>观测自身——<strong>OpenTelemetry（OTel）的链路追踪 + 结构化日志 + 指标</strong>。这一课讲两件让平台「对运维者透明」的事：① <strong>自我可观测</strong>——你早就见过的 <code>instrumentAsync</code>（第30课eval、第33课告警、第46课集成、第48课登录都用它）其实是个 OTel span 包装器，把每个关键操作都变成一条可追踪的 span；而它的日志更妙，<strong>每一行都自动带上当前的 trace_id/span_id</strong>，让「日志」和「链路」一键互跳。② <strong>配置即校验</strong>——所有环境变量都过一遍 <strong>Zod</strong> 校验，配错了<strong>启动时就当场报错</strong>，而不是跑着跑着神秘崩溃。
一句话：成熟的平台不仅能被观测，还<strong>吃自己的狗粮</strong>（dogfooding）；不仅能跑，还在跑之前<strong>检查好自己的每一项配置</strong>。
</p>

<div class="card analogy">
  <div class="tag">📋 生活类比</div>
  想象一位<strong>专给别人体检的医生</strong>。最有说服力的，是他<strong>自己也定期体检、且用的是同一套仪器</strong>——这就是 dogfooding：观测工具观测自己。Langfuse 给每个内部操作都贴上一个<strong>「计时手环」</strong>（OTel span：何时开始、耗时多久、有没有出错），出问题时能精确还原「慢在哪一步」。
  更贴心的是它的<strong>「病历」（日志）</strong>：每条日志都自动盖上<strong>当次就诊的编号</strong>（trace_id/span_id）。于是你在一堆日志里看到一条报错，<strong>顺着这个编号就能跳到对应的完整链路</strong>看清前因后果；反过来从链路也能找到相关日志——两本账自动对得上号。
  而配置校验，像医院<strong>开诊前的设备自检</strong>：开机时先把所有仪器参数（环境变量）逐一核对，<strong>缺一个、错一个就当场亮红灯不开诊</strong>，绝不带病上岗、看到一半才发现某台机器没插电。
</div>
""")

# (L51 sec1 below)

_ZH51.append(r"""
<h2>自我可观测：instrumentAsync 这把「计时手环」</h2>
<p>翻回前面几课，你会发现一个反复出现的名字：<code>instrumentAsync</code>。第30课 eval 处理、第33课告警状态机、第46课集成的逐项目任务、第48课登录的 session 回调——全都用它包了一层。现在揭晓它是什么：一个 <strong>OpenTelemetry span 包装器</strong>。你把一段异步逻辑交给它，它就：<strong>开一条 span</strong>（记下名字、开始时刻、span 类型）、运行你的逻辑、<strong>自动捕获异常</strong>（出错就 <code>traceException</code> 记到 span 上再抛出）、最后 <strong>span.end()</strong> 收尾。于是每个被包裹的操作，都在 OTel 里留下一条「<strong>何时开始、耗时多久、成功还是抛错</strong>」的可追踪记录。这正是 Langfuse 观测<strong>自己</strong>的方式——和它帮你观测 LLM 应用，是同一套 trace/span 思路。</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="instrumentAsync是OTel span包装器：把一段异步逻辑包起来，开span记名字/开始/类型，运行逻辑，出错自动traceException记到span，结束span.end；处处复用——eval(L30)、告警(L33)、集成(L46)、登录(L48)，加上recordGauge/Increment/Histogram指标和getTracer">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">把每个关键操作变成一条可追踪的 span</text>
  <rect x="250" y="40" width="220" height="120" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">instrumentAsync(ctx, fn)</text>
  <rect x="266" y="72" width="188" height="22" rx="5" fill="var(--bg)" stroke="var(--accent)"/><text x="360" y="87" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">① 开 span（名字·开始时刻·kind）</text>
  <rect x="266" y="98" width="188" height="22" rx="5" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="360" y="113" text-anchor="middle" font-size="6.6" fill="var(--teal)">② 运行你的逻辑 await fn(span)</text>
  <rect x="266" y="124" width="188" height="22" rx="5" fill="var(--bg)" stroke="var(--accent)"/><text x="360" y="139" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">③ 出错 traceException → ④ span.end()</text>
  <rect x="30" y="58" width="170" height="92" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="115" y="76" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--ink)">处处复用</text><text x="115" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">eval 处理（第30课）</text><text x="115" y="104" text-anchor="middle" font-size="6.2" fill="var(--muted)">告警状态机（第33课）</text><text x="115" y="116" text-anchor="middle" font-size="6.2" fill="var(--muted)">集成逐项目（第46课）</text><text x="115" y="128" text-anchor="middle" font-size="6.2" fill="var(--muted)">登录 session 回调（第48课）</text><text x="115" y="142" text-anchor="middle" font-size="5.8" fill="var(--faint)">同一个包装器，全局一致</text>
  <rect x="520" y="58" width="175" height="92" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="607" y="76" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">同模块还提供</text><text x="607" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">getCurrentSpan / getTracer</text><text x="607" y="104" text-anchor="middle" font-size="6.2" fill="var(--muted)">traceException</text><text x="607" y="116" text-anchor="middle" font-size="6.2" fill="var(--muted)">recordGauge / Increment</text><text x="607" y="128" text-anchor="middle" font-size="6.2" fill="var(--muted)">recordHistogram（指标）</text><text x="607" y="142" text-anchor="middle" font-size="5.8" fill="var(--faint)">trace + metrics 一站齐</text>
  <line x1="200" y1="104" x2="248" y2="104" stroke="var(--blue)" stroke-width="1.4"/><polygon points="248,104 239,100 239,108" fill="var(--blue)"/>
  <line x1="470" y1="104" x2="518" y2="104" stroke="var(--accent)" stroke-width="1.4"/><polygon points="518,104 509,100 509,108" fill="var(--accent)"/>
  <text x="360" y="184" text-anchor="middle" font-size="8" fill="var(--faint)">startNewTrace 开新根 trace，或从 traceContext 续上游链路（分布式追踪跨服务串起来）</text>
  <text x="360" y="202" text-anchor="middle" font-size="8" fill="var(--faint)">Langfuse 观测自己，用的就是它帮你观测 LLM 应用的同一套 OTel trace/span——dogfooding</text>
  <text x="360" y="220" text-anchor="middle" font-size="8" fill="var(--faint)">它甚至能反向「摄取」OTel：OtelIngestionProcessor 让你的 OTel 数据直接进 Langfuse（两头都说 OTel）</text>
</svg>
<div class="figcap"><b>instrumentAsync 包装器</b>：<code>instrumentation/index.ts:54</code> <code>instrumentAsync</code>（<code>startActiveSpan</code> 开 span、<code>startNewTrace</code> 开根 trace 或从 <code>traceContext</code> 续、<code>catch</code> 内 <code>traceException</code> 再抛、<code>span.end()</code>）。同模块：<code>:140</code> getCurrentSpan、<code>:142</code> traceException、<code>:263</code> getTracer、<code>:328/343/354</code> recordGauge/Increment/Histogram。OTel 摄取见 <code>otel/OtelIngestionProcessor.ts</code>。</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">追踪</span><span class="name">instrumentAsync（span 包装器）</span></div><div class="ld">把异步逻辑包成一条 OTel span：自动计时、自动 catch 异常记到 span、自动结束。<code>startNewTrace</code> 开新根、或从上游 <code>traceContext</code> 续——<strong>跨服务的分布式追踪</strong>就这么串起来。前面四课用的都是它。</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">指标</span><span class="name">recordGauge / Increment / Histogram</span></div><div class="ld">trace 之外还有 metrics：用 <code>recordIncrement</code> 计数（如「处理了多少条」）、<code>recordGauge</code> 记瞬时值（如队列深度）、<code>recordHistogram</code> 记分布（如耗时 P95）。同一个 instrumentation 模块一站提供。</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">双向</span><span class="name">既发也收 OTel</span></div><div class="ld">Langfuse 不只用 OTel 观测自己（<strong>发</strong>出 span），还能<strong>接收</strong> OTel：<code>OtelIngestionProcessor</code> 让你把应用的 OTel 数据直接喂进 Langfuse。两头都说 OTel 这门通用语言——既是工具的自洽，也是生态的开放。</div></div>
</div>
""")

# (L51 sec2 below)

_ZH51.append(r"""
<h2>日志的点睛：每行自动盖上 trace_id</h2>
<p>Langfuse 的日志用 <strong>winston</strong>，按环境变量出 <strong>text</strong>（开发，人读友好）或 <strong>json</strong>（生产，机器可解析）两种格式，级别由 <code>LANGFUSE_LOG_LEVEL</code> 控制。但真正的点睛之笔是一个叫 <code>tracingFormat</code> 的自定义格式器：<strong>每写一行日志，它都去问一句「当前有没有活跃的 OTel span？」——有就把这条 span 的 <code>trace_id</code> 和 <code>span_id</code> 自动塞进这行日志</strong>（还顺带塞一份 Datadog 风格的 <code>dd.trace_id</code>）。</p>

<p>这一下，<strong>「日志」和「链路追踪」这两本账就自动对上了号</strong>。排查线上问题时，这是天大的便利：你在海量日志里发现一条报错 → 顺着它带的 <code>trace_id</code> → 一键跳到那次请求的<strong>完整链路</strong>，看清它走了哪些服务、每步耗时、错在第几跳；反过来，盯着一条慢链路，也能精准捞出它沿途打的所有日志。没有这层关联，日志和链路就是两座孤岛，排查全靠手工对时间戳——又慢又易错。一行不起眼的「自动注入」，省下的是无数个深夜的对账之苦。</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="日志自动关联trace：winston的tracingFormat每写一行日志就查当前活跃OTel span，把trace_id/span_id(及dd.trace_id)注入该行；于是从一条报错日志顺trace_id一键跳到完整链路，反向也能从链路捞出沿途日志；格式text(开发)或json(生产)由env控制">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">日志 ⇄ 链路：自动对上号，一键互跳</text>
  <rect x="24" y="44" width="200" height="96" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="124" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">winston logger</text><text x="124" y="82" text-anchor="middle" font-size="6.4" fill="var(--muted)">text（开发·人读）/ json（生产·机读）</text><text x="124" y="96" text-anchor="middle" font-size="6.2" fill="var(--muted)">级别 LANGFUSE_LOG_LEVEL</text><text x="124" y="112" text-anchor="middle" font-size="6.4" font-weight="700" fill="var(--accent-ink)">tracingFormat 格式器</text><text x="124" y="126" text-anchor="middle" font-size="6.0" fill="var(--faint)">每行：问「有活跃 span 吗？」</text>
  <rect x="270" y="56" width="180" height="72" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="76" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">注入 trace 标识</text><text x="360" y="93" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">trace_id · span_id</text><text x="360" y="106" text-anchor="middle" font-size="6.2" fill="var(--muted)">+ dd.trace_id（Datadog 风格）</text><text x="360" y="120" text-anchor="middle" font-size="6.0" fill="var(--faint)">getCurrentSpan() 拿当前 span</text>
  <rect x="496" y="44" width="200" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="596" y="62" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--teal)">日志 → 链路</text><text x="596" y="77" text-anchor="middle" font-size="6.0" fill="var(--muted)">见报错日志，顺 trace_id 跳完整链路</text>
  <rect x="496" y="96" width="200" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="596" y="114" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">链路 → 日志</text><text x="596" y="129" text-anchor="middle" font-size="6.0" fill="var(--muted)">盯一条慢链路，捞出沿途所有日志</text>
  <line x1="224" y1="92" x2="268" y2="92" stroke="var(--accent)" stroke-width="1.4"/><polygon points="268,92 259,88 259,96" fill="var(--accent)"/>
  <line x1="450" y1="80" x2="494" y2="68" stroke="var(--teal)" stroke-width="1.3"/><polygon points="494,68 485,67 487,75" fill="var(--teal)"/>
  <line x1="450" y1="104" x2="494" y2="115" stroke="var(--accent)" stroke-width="1.3"/><polygon points="494,115 485,112 486,120" fill="var(--accent)"/>
  <text x="360" y="166" text-anchor="middle" font-size="8" fill="var(--faint)">没有这层关联，日志和链路是两座孤岛，排查靠手工对时间戳——又慢又易错</text>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">一行「自动注入」，换来无数次「从这条错日志，直达那次请求全貌」的顺滑排查</text>
  <text x="360" y="204" text-anchor="middle" font-size="8" fill="var(--faint)">这正是可观测性的「三支柱」协同：traces + logs（+ metrics）互相打通才好用</text>
</svg>
<div class="figcap"><b>日志关联 trace</b>：<code>logger.ts</code> winston，<code>tracingFormat</code>（<code>:6</code> 起）每行调 <code>getCurrentSpan()</code>，有 span 就注入 <code>trace_id/span_id</code> 与 <code>dd.trace_id/dd.span_id</code>；格式 <code>textLoggerFormat</code>（<code>:31</code>）或 jsonLoggerFormat 由 <code>LANGFUSE_LOG_FORMAT</code> 选、级别由 <code>LANGFUSE_LOG_LEVEL</code> 定。</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/logger.ts</span><span class="ln">日志自动注入 trace 标识</span></div>
  <pre class="code"><span class="cm">// 自定义格式器：每写一行日志，自动盖上当前 span 的 trace/span id</span>
<span class="kw">const</span> <span class="fn">tracingFormat</span> = () =&gt; winston.format((info) =&gt; {
  <span class="kw">const</span> span = <span class="fn">getCurrentSpan</span>();                       <span class="cm">// 当前活跃的 OTel span</span>
  <span class="kw">if</span> (span) {
    <span class="kw">const</span> { spanId, traceId } = span.<span class="fn">spanContext</span>();
    info[<span class="st">"trace_id"</span>] = traceId;  info[<span class="st">"span_id"</span>] = spanId;  <span class="cm">// 注入！</span>
    info[<span class="st">"dd.trace_id"</span>] = …;                          <span class="cm">// 顺带 Datadog 风格</span>
  }
  <span class="kw">return</span> info;
})();

<span class="cm">// 格式按 env 选 text(开发) / json(生产)；级别按 env</span>
<span class="kw">const</span> format = env.LANGFUSE_LOG_FORMAT === <span class="st">"text"</span> ? textLoggerFormat : jsonLoggerFormat;
<span class="kw">export const</span> logger = winston.<span class="fn">createLogger</span>({ level: env.LANGFUSE_LOG_LEVEL, format,
                                          transports: [<span class="kw">new</span> winston.transports.<span class="fn">Console</span>()] });</pre>
</div>

<div class="cols">
  <div class="col"><h4>🔗 traces（链路）</h4><p>一次请求/任务走过的完整路径与各步耗时。由 <code>instrumentAsync</code> 的 span 拼成——回答「慢在哪一步、错在第几跳」。</p></div>
  <div class="col"><h4>📝 logs（日志）</h4><p>离散的事件记录（含报错）。winston 输出，且每行自动带 <code>trace_id</code>——回答「具体发生了什么」，并能跳回对应链路。</p></div>
  <div class="col"><h4>📊 metrics（指标）</h4><p>聚合的数值趋势：计数、瞬时值、分布。<code>recordIncrement/Gauge/Histogram</code> 上报——回答「整体健康吗、量级多大、P95 几何」。</p></div>
</div>
""")

# (L51 sec3 below)

_ZH51.append(r"""
<h2>配置即校验：让错配在启动时就暴露</h2>
<p>一个平台有几十上百个环境变量（数据库地址、Redis、密钥、各种开关）。如果哪个填错了、漏填了，最糟的情况是<strong>程序照样启动，跑到半路才神秘崩溃</strong>——而且报的错往往离真正的根因十万八千里。Langfuse 的对策是<strong>把所有 env 都过一遍 Zod 校验</strong>：共享层用 <code>EnvSchema = z.object({...})</code> 声明每个变量的类型与约束（如 <code>REDIS_PORT</code> 用 <code>z.coerce.number()</code> 把字符串转数字、<code>REDIS_TLS_ENABLED</code> 只能是 <code>"true"|"false"</code>）；web 层用 <code>@t3-oss/env-nextjs</code> 的 <code>createEnv</code> 把 env 分成 <strong>server</strong>（仅服务端，如 <code>DATABASE_URL</code>）和 <strong>client</strong>（可进浏览器，须 <code>NEXT_PUBLIC_</code> 前缀）两类。</p>

<p>这带来两个硬好处：① <strong>fail-fast（快速失败）</strong>——配置不合法，<strong>启动那一刻就当场报清晰的错</strong>（「DATABASE_URL 不是合法 URL」），而不是带病运行、半夜崩给你看。② <strong>server/client 边界</strong>——<code>createEnv</code> 强制区分「只能在服务端用的密钥」和「能打进前端包的公开配置」，<strong>从机制上防止你手滑把数据库密码泄露进浏览器</strong>。配置不再是「一堆 <code>process.env.XXX</code> 散落各处、类型全靠猜」，而是一份<strong>声明式、类型安全、边界清晰</strong>的契约。</p>

<table class="t">
  <thead><tr><th>没有校验（裸 process.env）</th><th>Langfuse 的 Zod 校验</th></tr></thead>
  <tbody>
    <tr><td>错配可能跑到半路才崩</td><td><b>fail-fast</b>：启动时当场报清晰的错</td></tr>
    <tr><td><code>process.env.X</code> 类型永远是 string|undefined</td><td><b>类型安全</b>：z.coerce 转数字、z.enum 限取值</td></tr>
    <tr><td>密钥可能手滑打进前端包</td><td><b>server/client 边界</b>：createEnv 强制隔离</td></tr>
    <tr><td>有哪些配置、什么含义，全靠翻代码</td><td><b>声明式契约</b>：一份 schema 即文档</td></tr>
  </tbody>
</table>

<p>把「可观测」和「配置校验」放在同一课，是因为它们朝着<strong>同一个方向</strong>使劲：<strong>让系统对运维者「透明、可预期、早暴露问题」</strong>。可观测让你在<strong>运行时</strong>看清系统在干什么、慢在哪、错在哪；配置校验让你在<strong>启动时</strong>就堵住一整类「配错了」的低级故障。一个管运行期、一个管启动期，合起来就是「这个平台好不好运维」的底色。</p>
""")

_ZH51.append(r"""
<div class="card spark">
  <div class="tag">🎯 设计取舍</div>
  <strong>Langfuse 自己就是个可观测性工具，为什么还要费力用 OTel 观测自己？这种 dogfooding 值得吗？</strong> 太值了，而且不只是「显得自洽」。<strong>第一，它是最严苛的自测</strong>：当你每天用自己的产品扛自己的生产负载，产品的毛病你会第一个、最痛地感受到——这种「自己人先吃苦」的反馈，比任何用户调研都快、都真。<strong>第二，技术上极其顺滑</strong>：Langfuse 本就讲 OTel 这门语言（它能<strong>摄取</strong>你的 OTel 数据），于是观测自己时复用同一套 trace/span 概念，几乎零额外认知成本——发出去的 span 和收进来的 span 是同构的。<strong>第三，它逼着把可观测做成「随手可用」</strong>：正因为内部到处要用，<code>instrumentAsync</code> 才被打磨成一个包一下就行的薄包装，而不是每处手写一堆 OTel 样板。<strong>一个工具最好的广告，是它自己离不开它。</strong><br><br>
  <strong>为什么要花力气把 env 做成 Zod 校验 + server/client 分离，直接读 <code>process.env.XXX</code> 不是更省事？</strong> 因为「省事」省的是<strong>写的时候</strong>，赔的是<strong>出事的时候</strong>。裸读 <code>process.env</code> 有三宗罪：① 类型永远是 <code>string | undefined</code>，你以为是数字的端口其实是字符串，比较、运算处处埋雷；② 错配<strong>不会立刻报错</strong>——少配一个 <code>DATABASE_URL</code>，应用照启动，直到第一次查库才崩，而那时的错误信息离根因很远，排查能耗掉半天；③ 最危险的是<strong>边界失守</strong>：一个本该只在服务端用的密钥，手滑加了 <code>NEXT_PUBLIC_</code> 或被打进客户端 bundle，就<strong>泄露给了所有访问者</strong>。Zod + <code>createEnv</code> 一次性解决：启动时校验（fail-fast）、自动类型推导（类型安全）、强制 server/client 隔离（防泄露）。<strong>把「配置」当成需要校验的「输入」来对待，而不是一堆可以随便读的全局字符串——这是把低级故障挡在生产之外的关键一步。</strong>
</div>

<div class="card key">
  <div class="tag">🎯 本课要点</div>
  <ul>
    <li><strong>自我可观测（dogfooding）</strong>：Langfuse 用它帮你观测 LLM 应用的<strong>同一套 OTel</strong> 观测自己。<code>instrumentAsync</code>（instrumentation/index.ts:54）是个 span 包装器——开 span、跑逻辑、自动 traceException、span.end，第30/33/46/48 课都在用。</li>
    <li><strong>trace + metrics 一站齐</strong>：同模块还有 <code>getCurrentSpan</code>/<code>traceException</code>/<code>getTracer</code> 和 <code>recordGauge/Increment/Histogram</code>（指标）。还能反向<strong>摄取</strong> OTel（OtelIngestionProcessor）——两头都说 OTel。</li>
    <li><strong>日志自动关联 trace</strong>：winston 的 <code>tracingFormat</code> 每行日志都注入当前 span 的 <code>trace_id/span_id</code>（含 dd.* Datadog 风格）。于是日志↔链路一键互跳——排查线上问题的天大便利。格式 text/json、级别由 env 定。</li>
    <li><strong>配置即校验</strong>：所有 env 过 Zod（共享 <code>EnvSchema = z.object</code>、web <code>createEnv</code> 分 server/client）。好处：<strong>fail-fast</strong>（启动即报错而非半路崩）、<strong>类型安全</strong>（z.coerce/z.enum）、<strong>server/client 边界</strong>（防密钥泄露进前端）。</li>
    <li><strong>同一个方向</strong>：可观测管「运行时透明」、配置校验管「启动时堵错」，合起来决定「这平台好不好运维」。把配置当「需要校验的输入」而非「随便读的全局字符串」。</li>
  </ul>
</div>
""")

_EN51.append(r"""
<p class="lead">
Langfuse is a tool that <strong>helps you observe LLM applications</strong>. So when it itself has a problem, how does it observe <strong>itself</strong>? The answer is fittingly self-consistent: it uses the <strong>same observability means</strong> to observe itself — <strong>OpenTelemetry (OTel) distributed tracing + structured logging + metrics</strong>. This lesson covers two things that make the platform "transparent to operators": ① <strong>self-observability</strong> — the <code>instrumentAsync</code> you've long seen (Lesson 30 eval, Lesson 33 alerts, Lesson 46 integrations, Lesson 48 login all use it) is actually an OTel span wrapper turning every key operation into a traceable span; and its logging is cleverer still, <strong>auto-stamping each line with the current trace_id/span_id</strong>, so "logs" and "traces" jump to each other in one click. ② <strong>config as validation</strong> — all environment variables pass through <strong>Zod</strong> validation, so a misconfiguration <strong>errors out at boot, on the spot</strong>, rather than crashing mysteriously mid-run.
In a sentence: a mature platform is not only observable but <strong>eats its own dog food</strong> (dogfooding); not only runs, but <strong>checks every one of its configs before running</strong>.
</p>

<div class="card analogy">
  <div class="tag">📋 Analogy</div>
  Picture a <strong>doctor who gives others checkups</strong>. The most convincing one <strong>also gets regular checkups himself, using the same instruments</strong> — that's dogfooding: the observability tool observing itself. Langfuse puts a <strong>"timing wristband"</strong> on every internal operation (an OTel span: when it started, how long it took, whether it errored), so on a problem it can precisely reconstruct "which step was slow."
  Even more thoughtful is its <strong>"medical record" (logs)</strong>: each log line is auto-stamped with the <strong>visit number</strong> (trace_id/span_id). So when you spot one error among a pile of logs, <strong>follow that number to jump to the full corresponding trace</strong> and see the whole cause-and-effect; conversely, from a trace you can find related logs — the two ledgers auto-reconcile.
  And config validation is like the hospital's <strong>pre-opening equipment self-check</strong>: at startup it cross-checks every instrument's parameters (env vars) one by one, and <strong>if one is missing or wrong, it flashes red and doesn't open</strong> — never operating impaired, never discovering halfway that a machine wasn't plugged in.
</div>
""")

_EN51.append(r"""
<h2>Self-observability: the "timing wristband" instrumentAsync</h2>
<p>Flip back through earlier lessons and you'll see a recurring name: <code>instrumentAsync</code>. Lesson 30's eval processing, Lesson 33's alert state machine, Lesson 46's per-project integration jobs, Lesson 48's login session callback — all wrap a layer with it. Now the reveal: it's an <strong>OpenTelemetry span wrapper</strong>. Hand it a piece of async logic and it: <strong>opens a span</strong> (records name, start time, span kind), runs your logic, <strong>auto-captures exceptions</strong> (on error, <code>traceException</code> records it on the span then rethrows), and finally <strong>span.end()</strong> wraps up. So every wrapped operation leaves a traceable record in OTel of "<strong>when it started, how long it took, success or threw</strong>." This is exactly how Langfuse observes <strong>itself</strong> — the same trace/span thinking it uses to observe your LLM apps for you.</p>

<div class="fig">
<svg viewBox="0 0 720 240" role="img" aria-label="instrumentAsync is an OTel span wrapper: wrap a piece of async logic, open a span recording name/start/kind, run the logic, on error auto-traceException onto the span, end with span.end; reused everywhere — eval(L30), alerts(L33), integrations(L46), login(L48), plus recordGauge/Increment/Histogram metrics and getTracer">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Turn every key operation into a traceable span</text>
  <rect x="250" y="40" width="220" height="120" rx="10" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="60" text-anchor="middle" font-size="9" font-weight="700" fill="var(--accent-ink)">instrumentAsync(ctx, fn)</text>
  <rect x="266" y="72" width="188" height="22" rx="5" fill="var(--bg)" stroke="var(--accent)"/><text x="360" y="87" text-anchor="middle" font-size="6.6" fill="var(--accent-ink)">① open span (name·start·kind)</text>
  <rect x="266" y="98" width="188" height="22" rx="5" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="360" y="113" text-anchor="middle" font-size="6.6" fill="var(--teal)">② run your logic await fn(span)</text>
  <rect x="266" y="124" width="188" height="22" rx="5" fill="var(--bg)" stroke="var(--accent)"/><text x="360" y="139" text-anchor="middle" font-size="6.2" fill="var(--accent-ink)">③ on error traceException → ④ span.end()</text>
  <rect x="30" y="58" width="170" height="92" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="115" y="76" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--ink)">reused everywhere</text><text x="115" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">eval processing (L30)</text><text x="115" y="104" text-anchor="middle" font-size="6.2" fill="var(--muted)">alert state machine (L33)</text><text x="115" y="116" text-anchor="middle" font-size="6.2" fill="var(--muted)">per-project integration (L46)</text><text x="115" y="128" text-anchor="middle" font-size="6.2" fill="var(--muted)">login session callback (L48)</text><text x="115" y="142" text-anchor="middle" font-size="5.8" fill="var(--faint)">same wrapper, globally consistent</text>
  <rect x="520" y="58" width="175" height="92" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="607" y="76" text-anchor="middle" font-size="7.6" font-weight="700" fill="var(--accent-ink)">same module also offers</text><text x="607" y="92" text-anchor="middle" font-size="6.2" fill="var(--muted)">getCurrentSpan / getTracer</text><text x="607" y="104" text-anchor="middle" font-size="6.2" fill="var(--muted)">traceException</text><text x="607" y="116" text-anchor="middle" font-size="6.2" fill="var(--muted)">recordGauge / Increment</text><text x="607" y="128" text-anchor="middle" font-size="6.2" fill="var(--muted)">recordHistogram (metrics)</text><text x="607" y="142" text-anchor="middle" font-size="5.8" fill="var(--faint)">trace + metrics in one place</text>
  <line x1="200" y1="104" x2="248" y2="104" stroke="var(--blue)" stroke-width="1.4"/><polygon points="248,104 239,100 239,108" fill="var(--blue)"/>
  <line x1="470" y1="104" x2="518" y2="104" stroke="var(--accent)" stroke-width="1.4"/><polygon points="518,104 509,100 509,108" fill="var(--accent)"/>
  <text x="360" y="184" text-anchor="middle" font-size="8" fill="var(--faint)">startNewTrace opens a new root trace, or continues the upstream chain from traceContext (distributed tracing stitched across services)</text>
  <text x="360" y="202" text-anchor="middle" font-size="8" fill="var(--faint)">Langfuse observes itself with the very same OTel trace/span it uses to observe your LLM apps — dogfooding</text>
  <text x="360" y="220" text-anchor="middle" font-size="8" fill="var(--faint)">It can even "ingest" OTel in reverse: OtelIngestionProcessor lets your OTel data flow straight into Langfuse (both ends speak OTel)</text>
</svg>
<div class="figcap"><b>The instrumentAsync wrapper</b>: <code>instrumentation/index.ts:54</code> <code>instrumentAsync</code> (<code>startActiveSpan</code> opens a span, <code>startNewTrace</code> opens a root trace or continues from <code>traceContext</code>, <code>catch</code> calls <code>traceException</code> then rethrows, <code>span.end()</code>). Same module: <code>:140</code> getCurrentSpan, <code>:142</code> traceException, <code>:263</code> getTracer, <code>:328/343/354</code> recordGauge/Increment/Histogram. OTel ingestion at <code>otel/OtelIngestionProcessor.ts</code>.</div>
</div>

<div class="layers">
  <div class="layer l-core"><div class="lh"><span class="badge">trace</span><span class="name">instrumentAsync (span wrapper)</span></div><div class="ld">Wraps async logic into an OTel span: auto-timing, auto-catch exceptions onto the span, auto-end. <code>startNewTrace</code> opens a new root, or continues from the upstream <code>traceContext</code> — that's how <strong>cross-service distributed tracing</strong> is stitched. The previous four lessons all use it.</div></div>
  <div class="layer l-main"><div class="lh"><span class="badge">metrics</span><span class="name">recordGauge / Increment / Histogram</span></div><div class="ld">Beyond traces there are metrics: <code>recordIncrement</code> for counts (e.g. "how many processed"), <code>recordGauge</code> for instantaneous values (e.g. queue depth), <code>recordHistogram</code> for distributions (e.g. P95 latency). The same instrumentation module offers them all.</div></div>
  <div class="layer l-part"><div class="lh"><span class="badge">two-way</span><span class="name">emits and receives OTel</span></div><div class="ld">Langfuse not only uses OTel to observe itself (<strong>emitting</strong> spans), it also <strong>receives</strong> OTel: <code>OtelIngestionProcessor</code> lets you feed your app's OTel data straight into Langfuse. Both ends speak the universal OTel language — the tool's self-consistency and the ecosystem's openness.</div></div>
</div>
""")

_EN51.append(r"""
<h2>The logging masterstroke: each line auto-stamped with trace_id</h2>
<p>Langfuse's logging uses <strong>winston</strong>, emitting <strong>text</strong> (dev, human-friendly) or <strong>json</strong> (prod, machine-parseable) by env var, with level controlled by <code>LANGFUSE_LOG_LEVEL</code>. But the real masterstroke is a custom formatter called <code>tracingFormat</code>: <strong>every time it writes a log line, it asks "is there an active OTel span right now?" — if so it auto-stuffs that span's <code>trace_id</code> and <code>span_id</code> into the line</strong> (plus a Datadog-style <code>dd.trace_id</code> for good measure).</p>

<p>With that, <strong>"logs" and "distributed tracing" auto-reconcile</strong>. When debugging production issues, this is a huge convenience: you find one error among a sea of logs → follow its <code>trace_id</code> → jump in one click to that request's <strong>full trace</strong>, seeing which services it traversed, each step's latency, which hop errored; conversely, eyeing a slow trace, you can precisely scoop up all the logs it emitted along the way. Without this correlation, logs and traces are two isolated islands and debugging means manually matching timestamps — slow and error-prone. One inconspicuous line of "auto-injection" saves countless late-night reconciliation headaches.</p>

<div class="fig">
<svg viewBox="0 0 720 215" role="img" aria-label="logs auto-correlate with traces: winston's tracingFormat on each log line checks the current active OTel span and injects trace_id/span_id (and dd.trace_id) into the line; so from an error log follow trace_id to jump to the full trace in one click, and in reverse scoop logs from a trace; format text(dev) or json(prod) by env">
  <text x="360" y="18" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--accent-ink)">Logs ⇄ traces: auto-reconciled, one-click jump</text>
  <rect x="24" y="44" width="200" height="96" rx="9" fill="var(--blue-soft)" stroke="var(--blue)"/><text x="124" y="64" text-anchor="middle" font-size="8" font-weight="700" fill="var(--ink)">winston logger</text><text x="124" y="82" text-anchor="middle" font-size="6.4" fill="var(--muted)">text(dev·human) / json(prod·machine)</text><text x="124" y="96" text-anchor="middle" font-size="6.2" fill="var(--muted)">level LANGFUSE_LOG_LEVEL</text><text x="124" y="112" text-anchor="middle" font-size="6.4" font-weight="700" fill="var(--accent-ink)">tracingFormat formatter</text><text x="124" y="126" text-anchor="middle" font-size="6.0" fill="var(--faint)">each line: "any active span?"</text>
  <rect x="270" y="56" width="180" height="72" rx="9" fill="var(--accent-soft)" stroke="var(--accent)" stroke-width="2"/><text x="360" y="76" text-anchor="middle" font-size="8" font-weight="700" fill="var(--accent-ink)">inject trace ids</text><text x="360" y="93" text-anchor="middle" font-size="6.4" fill="var(--accent-ink)">trace_id · span_id</text><text x="360" y="106" text-anchor="middle" font-size="6.2" fill="var(--muted)">+ dd.trace_id (Datadog style)</text><text x="360" y="120" text-anchor="middle" font-size="6.0" fill="var(--faint)">getCurrentSpan() gets the current span</text>
  <rect x="496" y="44" width="200" height="44" rx="9" fill="var(--teal)" opacity="0.16" stroke="var(--teal)"/><text x="596" y="62" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--teal)">log → trace</text><text x="596" y="77" text-anchor="middle" font-size="6.0" fill="var(--muted)">see an error log, follow trace_id to the full trace</text>
  <rect x="496" y="96" width="200" height="44" rx="9" fill="var(--purple-soft)" stroke="var(--accent)"/><text x="596" y="114" text-anchor="middle" font-size="7.4" font-weight="700" fill="var(--accent-ink)">trace → log</text><text x="596" y="129" text-anchor="middle" font-size="6.0" fill="var(--muted)">eye a slow trace, scoop all its logs</text>
  <line x1="224" y1="92" x2="268" y2="92" stroke="var(--accent)" stroke-width="1.4"/><polygon points="268,92 259,88 259,96" fill="var(--accent)"/>
  <line x1="450" y1="80" x2="494" y2="68" stroke="var(--teal)" stroke-width="1.3"/><polygon points="494,68 485,67 487,75" fill="var(--teal)"/>
  <line x1="450" y1="104" x2="494" y2="115" stroke="var(--accent)" stroke-width="1.3"/><polygon points="494,115 485,112 486,120" fill="var(--accent)"/>
  <text x="360" y="166" text-anchor="middle" font-size="8" fill="var(--faint)">Without this correlation, logs and traces are isolated islands; debugging means manually matching timestamps — slow and error-prone</text>
  <text x="360" y="186" text-anchor="middle" font-size="8" fill="var(--faint)">One line of "auto-injection" buys countless smooth "from this error log, straight to that request's full picture" debug sessions</text>
  <text x="360" y="204" text-anchor="middle" font-size="8" fill="var(--faint)">This is the "three pillars" of observability working together: traces + logs (+ metrics) are useful only when wired to each other</text>
</svg>
<div class="figcap"><b>Logs correlate with traces</b>: <code>logger.ts</code> winston, <code>tracingFormat</code> (from <code>:6</code>) on each line calls <code>getCurrentSpan()</code>, and if there's a span injects <code>trace_id/span_id</code> and <code>dd.trace_id/dd.span_id</code>; the format <code>textLoggerFormat</code> (<code>:31</code>) or jsonLoggerFormat is chosen by <code>LANGFUSE_LOG_FORMAT</code>, level by <code>LANGFUSE_LOG_LEVEL</code>.</div>
</div>

<div class="codefile">
  <div class="cf-head"><span class="dot"></span><span class="path">packages/shared/src/server/logger.ts</span><span class="ln">logs auto-inject trace ids</span></div>
  <pre class="code"><span class="cm">// custom formatter: each log line auto-stamped with the current span's trace/span id</span>
<span class="kw">const</span> <span class="fn">tracingFormat</span> = () =&gt; winston.format((info) =&gt; {
  <span class="kw">const</span> span = <span class="fn">getCurrentSpan</span>();                       <span class="cm">// the current active OTel span</span>
  <span class="kw">if</span> (span) {
    <span class="kw">const</span> { spanId, traceId } = span.<span class="fn">spanContext</span>();
    info[<span class="st">"trace_id"</span>] = traceId;  info[<span class="st">"span_id"</span>] = spanId;  <span class="cm">// inject!</span>
    info[<span class="st">"dd.trace_id"</span>] = …;                          <span class="cm">// plus Datadog style</span>
  }
  <span class="kw">return</span> info;
})();

<span class="cm">// format chosen by env: text(dev) / json(prod); level by env</span>
<span class="kw">const</span> format = env.LANGFUSE_LOG_FORMAT === <span class="st">"text"</span> ? textLoggerFormat : jsonLoggerFormat;
<span class="kw">export const</span> logger = winston.<span class="fn">createLogger</span>({ level: env.LANGFUSE_LOG_LEVEL, format,
                                          transports: [<span class="kw">new</span> winston.transports.<span class="fn">Console</span>()] });</pre>
</div>

<div class="cols">
  <div class="col"><h4>🔗 traces</h4><p>The full path a request/job traverses with each step's latency. Stitched from <code>instrumentAsync</code>'s spans — answers "which step was slow, which hop errored."</p></div>
  <div class="col"><h4>📝 logs</h4><p>Discrete event records (incl. errors). Emitted by winston, each line auto-carrying <code>trace_id</code> — answers "what specifically happened," and can jump back to the corresponding trace.</p></div>
  <div class="col"><h4>📊 metrics</h4><p>Aggregated numeric trends: counts, instantaneous values, distributions. Reported via <code>recordIncrement/Gauge/Histogram</code> — answers "is it healthy overall, what's the volume, what's the P95."</p></div>
</div>
""")

_EN51.append(r"""
<h2>Config as validation: surface misconfig at boot</h2>
<p>A platform has dozens to hundreds of environment variables (DB address, Redis, secrets, various toggles). If one is wrong or missing, the worst case is the <strong>program starts anyway and crashes mysteriously mid-run</strong> — and the reported error is often light-years from the true root cause. Langfuse's countermeasure is to <strong>run all env through Zod validation</strong>: the shared layer uses <code>EnvSchema = z.object({...})</code> to declare each variable's type and constraints (e.g. <code>REDIS_PORT</code> uses <code>z.coerce.number()</code> to turn a string into a number, <code>REDIS_TLS_ENABLED</code> can only be <code>"true"|"false"</code>); the web layer uses <code>@t3-oss/env-nextjs</code>'s <code>createEnv</code> to split env into <strong>server</strong> (server-only, like <code>DATABASE_URL</code>) and <strong>client</strong> (may reach the browser, must have a <code>NEXT_PUBLIC_</code> prefix).</p>

<p>This brings two hard wins: ① <strong>fail-fast</strong> — invalid config <strong>errors clearly the moment of startup</strong> ("DATABASE_URL is not a valid URL"), rather than running impaired and crashing on you at midnight. ② <strong>server/client boundary</strong> — <code>createEnv</code> forces a distinction between "secrets usable only server-side" and "public config that can ship in the front-end bundle," <strong>mechanically preventing you from fat-fingering a DB password into the browser</strong>. Config is no longer "a pile of <code>process.env.XXX</code> scattered everywhere, types all guesswork" but a <strong>declarative, type-safe, boundary-clear</strong> contract.</p>

<table class="t">
  <thead><tr><th>No validation (raw process.env)</th><th>Langfuse's Zod validation</th></tr></thead>
  <tbody>
    <tr><td>misconfig may crash mid-run</td><td><b>fail-fast</b>: errors clearly at startup</td></tr>
    <tr><td><code>process.env.X</code> is always string|undefined</td><td><b>type-safe</b>: z.coerce to number, z.enum to limit values</td></tr>
    <tr><td>a secret may be fat-fingered into the front-end bundle</td><td><b>server/client boundary</b>: createEnv enforces isolation</td></tr>
    <tr><td>what configs exist and mean is buried in code</td><td><b>declarative contract</b>: one schema is the doc</td></tr>
  </tbody>
</table>

<p>Putting "observability" and "config validation" in one lesson is because they push in <strong>the same direction</strong>: <strong>making the system "transparent, predictable, early-surfacing problems" to operators</strong>. Observability lets you see at <strong>runtime</strong> what the system is doing, where it's slow, where it errored; config validation plugs at <strong>startup</strong> a whole class of "misconfigured" low-level failures. One owns the run phase, one the boot phase, and together they're the baseline of "how operable is this platform."</p>
""")

_EN51.append(r"""
<div class="card spark">
  <div class="tag">🎯 Design trade-off</div>
  <strong>Langfuse is itself an observability tool — why bother using OTel to observe itself? Is this dogfooding worth it?</strong> Very much so, and not just for "looking self-consistent." <strong>First, it's the most rigorous self-test</strong>: when you run your own product carrying your own production load every day, you feel the product's flaws first and most painfully — this "eat your own bitterness first" feedback is faster and truer than any user research. <strong>Second, it's technically seamless</strong>: Langfuse already speaks the OTel language (it can <strong>ingest</strong> your OTel data), so observing itself reuses the same trace/span concepts with near-zero extra cognitive cost — the spans it emits and the spans it ingests are isomorphic. <strong>Third, it forces observability to be "ready at hand"</strong>: precisely because it's used internally everywhere, <code>instrumentAsync</code> got polished into a thin wrap-once wrapper rather than hand-written OTel boilerplate at every site. <strong>A tool's best advertisement is that it can't live without itself.</strong><br><br>
  <strong>Why bother making env into Zod validation + server/client separation — isn't reading <code>process.env.XXX</code> directly easier?</strong> Because "easier" saves you <strong>when writing</strong> and costs you <strong>when things break</strong>. Raw <code>process.env</code> has three sins: ① the type is always <code>string | undefined</code>, so a port you think is a number is actually a string, planting landmines in comparisons and arithmetic; ② misconfig <strong>doesn't error immediately</strong> — miss a <code>DATABASE_URL</code> and the app starts anyway, crashing only on the first DB query, by which point the error message is far from the root cause and debugging eats half a day; ③ most dangerous is <strong>boundary breach</strong>: a secret meant only for the server, fat-fingered with <code>NEXT_PUBLIC_</code> or bundled into the client, <strong>leaks to every visitor</strong>. Zod + <code>createEnv</code> solves all at once: validate at startup (fail-fast), auto type inference (type-safe), enforce server/client isolation (anti-leak). <strong>Treating "config" as "input" that needs validation, rather than a pile of freely-readable global strings, is the key step to keeping low-level failures out of production.</strong>
</div>

<div class="card key">
  <div class="tag">🎯 Key points</div>
  <ul>
    <li><strong>Self-observability (dogfooding)</strong>: Langfuse observes itself with the <strong>same OTel</strong> it uses to observe your LLM apps. <code>instrumentAsync</code> (instrumentation/index.ts:54) is a span wrapper — open span, run logic, auto-traceException, span.end; used by Lessons 30/33/46/48.</li>
    <li><strong>Trace + metrics in one place</strong>: the same module also has <code>getCurrentSpan</code>/<code>traceException</code>/<code>getTracer</code> and <code>recordGauge/Increment/Histogram</code> (metrics). It can also <strong>ingest</strong> OTel in reverse (OtelIngestionProcessor) — both ends speak OTel.</li>
    <li><strong>Logs auto-correlate with traces</strong>: winston's <code>tracingFormat</code> injects the current span's <code>trace_id/span_id</code> (incl. dd.* Datadog style) into every log line. So logs↔traces jump in one click — a huge convenience for production debugging. Format text/json, level by env.</li>
    <li><strong>Config as validation</strong>: all env passes through Zod (shared <code>EnvSchema = z.object</code>, web <code>createEnv</code> splitting server/client). Wins: <strong>fail-fast</strong> (error at startup not crash mid-run), <strong>type-safe</strong> (z.coerce/z.enum), <strong>server/client boundary</strong> (prevent secrets leaking to the front end).</li>
    <li><strong>One direction</strong>: observability owns "runtime transparency," config validation owns "boot-time error-plugging," together deciding "how operable is this platform." Treat config as "input needing validation," not "freely-readable global strings."</li>
  </ul>
</div>
""")

LESSON_51 = {"zh": "\n".join(_ZH51), "en": "\n".join(_EN51)}
