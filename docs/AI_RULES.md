# AI Rules

本文档规定本项目中所有 AI 功能的行为边界、输入输出规则、人工审核要求和禁止行为。

本项目的 AI 不是自动销售系统，而是辅助用户完成：

- 公司资料理解
- 销售知识整理
- Product Card 生成
- Campaign 建议
- 客户匹配判断
- 推荐理由生成
- 风险提示生成
- Gmail Draft 草稿生成

AI 的所有输出默认都是 Draft，必须经过用户确认后，才能进入下一步流程。

---

## 1. Core Principles

AI 功能必须遵守以下原则：

1. AI 只能辅助判断，不能替代用户做最终商业决策。
2. AI 输出不能直接写入 Confirmed Knowledge，必须先作为 Draft。
3. AI 不允许编造公司信息、客户信息、联系方式、网站证据或邮箱地址。
4. AI 判断必须尽量基于可追溯来源，例如用户上传资料、公司官网内容、搜索结果、抓取文本。
5. AI 输出必须区分事实、推理和建议。
6. AI 不允许自动发送邮件。
7. AI 不允许读取、同步、移动、标记、修改、删除或发送 Gmail 邮件，只允许生成 Gmail Draft。
8. AI 不允许绕过人工审核流程。
9. AI 评分必须可解释，不能只返回一个分数。
10. AI 失败时必须返回清晰错误，而不是生成不可靠结果。

---

## 2. AI Output States

项目中 AI 生成内容必须区分状态。

### 2.1 Draft

AI 生成但未经过用户确认的内容。

包括：

- Company Knowledge Draft
- Product Card Draft
- Campaign Draft
- Lead Match Reason Draft
- Outreach Email Draft

Draft 内容不能作为最终事实使用。

### 2.2 Confirmed

用户确认后的内容。

包括：

- Confirmed Company Knowledge
- Confirmed Product Card
- Confirmed Campaign

在数据模型中应明确映射为：

- `product_cards.status = confirmed`
- `campaigns.status = confirmed`

后续 AI 评分和邮件生成只能基于 Confirmed 内容，而不是直接基于未确认 Draft。

### 2.3 Rejected

用户明确拒绝的 AI 输出。

Rejected 内容不能继续参与后续流程，除非用户重新编辑并确认。

此通用状态不适用于 Product Card。Product Card 只使用 `draft` 和 `confirmed`；不需要的 Product Card 通过删除处理，不产生 `rejected` 状态。

---

## 3. Company Knowledge Rules

AI 从用户输入资料中生成公司知识时，必须遵守：

1. 只能基于用户提供的资料、官网内容或明确来源生成。
2. 不确定的信息必须标记为 uncertain。
3. 不能把营销描述自动当作事实。
4. 不能自动补充用户没有提供的信息。
5. 不能擅自扩展公司业务范围。
6. 必须保留来源引用，例如 uploaded_file、website_url、manual_text。
7. 用户确认前，所有内容只能是 Draft。

Company Knowledge 应尽量包含：

- 公司名称
- 公司简介
- 产品或服务
- 目标客户
- 行业
- 地区
- 价值主张
- 核心优势
- 常见应用场景
- 不适合的客户类型
- 风险或限制

---

## 4. Product Card Rules

Product Card 用于描述一个可销售的产品或服务。

AI 生成 Product Card 时必须遵守：

1. Product Card 必须来自 Confirmed Company Knowledge。
2. 不能凭空创建不存在的产品。
3. 每个 Product Card 应聚焦一个明确产品、服务或解决方案。
4. Product Card 必须方便后续 Campaign 和 Lead Scoring 使用。
5. 不确定的卖点不能写成确定事实。
6. Product Card 生成后必须由用户确认。
7. AI 生成的 Product Card 必须设置 `source_type = ai_generated`、`status = draft`，AI 不得自动确认。
8. 用户手动添加产品是长期保留的独立入口，使用 `source_type = manual`、`status = draft`，不能因提供 AI 生成功能而移除。
9. 只有 `confirmed` Product Card 才能用于 Campaign；Product Card 不使用 reject/rejected 业务状态。

Product Card 应包含：

- product_name
- description
- target_customer
- pain_points
- value_proposition
- use_cases
- differentiators
- unsuitable_customers
- keywords
- evidence_sources

Product Card AI output mapping:

- The fields above describe the AI output schema. They are not automatically
  database columns.
- Service logic must map AI output into the persisted Product Card draft fields,
  such as `name`, `description`, `target_customer`, `pain_points`,
  `value_proposition`, `use_cases`, `differentiators`, and
  `source_knowledge_item_ids`.
- AI output fields that do not have current Product Card database columns, such
  as `unsuitable_customers`, `keywords`, and `evidence_sources`, must be mapped
  into existing fields or kept out of persistence until the data model is
  explicitly extended.
- Persisted Product Cards only support `draft` and `confirmed`. There is no
  `rejected` Product Card status and no Product Card reject endpoint.

---

## 5. Campaign Rules

Campaign 是用户要开发客户的具体销售方向。

AI 可以根据 Confirmed Knowledge 和 Product Card 生成 Campaign 建议，但必须遵守：

1. Campaign 只能作为建议，不能自动执行。
2. 用户必须可以修改 Campaign。
3. 用户确认 Campaign 后，系统才能开始搜索客户。
4. Campaign 必须明确目标市场、目标行业、客户类型和开发目标。
5. Campaign 不能过度宽泛。
6. Campaign 不能包含违法、骚扰或误导性销售目标。

Campaign 应包含：

- campaign_name
- product_card_id
- target_country
- target_region
- target_industry
- target_company_type
- target_role
- search_keywords
- qualification_criteria
- outreach_angle
- lead_limit

Campaign AI output mapping:

- `product_card_id` is the required Product Card link for a Campaign draft.
- `target_country` and `target_region` are separate fields. Do not use
  `target_country_or_region` as the persisted field name.
- AI-only suggestion fields such as `campaign_goal`,
  `target_customer_profile`, `customer_pain_points`, `exclusion_rules`, and
  `scoring_focus` may appear in AI output, but they must be mapped by service
  logic into the Campaign draft fields unless the data model later adds them.
- AI must not treat Campaign as a CRM sequence, automatic follow-up workflow,
  bulk email workflow, or auto-send workflow.

---

## 6. Lead Discovery AI Rules

Lead Discovery 阶段可以使用 AI 辅助判断候选客户是否值得进入评分流程。

AI 必须遵守：

1. 不允许编造候选客户。
2. 候选客户必须来自搜索结果、网站抓取结果或用户导入数据。
3. 必须保存候选客户来源。
4. 网站无法访问时，不能强行评分为高匹配。
5. 公司信息不足时，应标记为 insufficient_data。
6. 明显不符合 Campaign 的客户应在基础验证阶段过滤。
7. 不允许直接使用 LinkedIn API。
8. 不允许使用 Google Sheets 作为数据流转工具。

---

### LinkedIn Rules

- 禁止使用 LinkedIn API。
- 禁止使用 LinkedIn scraping。
- 禁止使用 LinkedIn crawler。
- 禁止使用 LinkedIn bot。
- 禁止使用 LinkedIn browser automation。
- 禁止使用 LinkedIn browser extension automation。
- 禁止 automated LinkedIn login。
- 禁止 automated LinkedIn search。
- 禁止 automated LinkedIn profile extraction。
- 禁止 automated LinkedIn contact downloading。
- 禁止 automated LinkedIn messaging。
- 禁止 automated LinkedIn connection requests。
- 允许用户手动粘贴公开 LinkedIn URL。
- 系统只允许把该 URL 作为 manual reference 保存，并在前端展示给用户人工审核。
- LinkedIn URL 不能作为 Gmail Draft recipient 或 Gmail Draft eligibility。
- AI 不能要求 system、crawler、provider 或 browser 自动访问 LinkedIn。

---

## 7. Lead Scoring Rules

AI Scoring 的目标是判断客户与 Campaign 的匹配程度。

评分必须包含：

- 总分
- 匹配等级
- 推荐理由
- 网站证据
- 风险提示
- 不确定点
- 下一步建议

推荐评分结构：

| Score Range | Meaning |
|---|---|
| 80 - 100 | High Fit |
| 60 - 79 | Medium Fit |
| 40 - 59 | Low Fit |
| 0 - 39 | Not Recommended |

AI 评分规则：

1. 不能只返回分数。
2. 必须说明为什么推荐或不推荐。
3. 必须引用网站证据或抓取文本。
4. 如果证据不足，不能给高分。
5. 如果客户行业、规模、地区或需求不匹配，必须扣分。
6. 如果客户信息不完整，必须明确说明。
7. 分数不能完全由模型自由判断，应尽量遵守统一 scoring rubric。
8. 不允许为了让结果看起来更好而提高分数。

AI recommendation and human review status are separate:

- AI scoring may produce only `lead_scores.recommendation`.
- Allowed AI recommendation values are `recommended`, `maybe`,
  `not_recommended`, and `needs_manual_review`.
- Human review sets `leads.review_status` separately, with values
  `unreviewed`, `approved`, `rejected`, and `needs_manual_review`.
- `needs_manual_review` in AI recommendation means AI uncertainty or risk.
  `needs_manual_review` in human review status means the user kept the lead in
  a manual workflow state.
- Only `leads.review_status = approved` can proceed to Outreach Draft or Gmail
  Draft creation.

---

## 8. Evidence Rules

所有 AI 推荐理由都必须尽量绑定证据。

证据可以来自：

- 客户官网
- 用户上传资料
- 搜索结果摘要
- 抓取页面文本
- 已确认知识库
- 已确认 Campaign

证据必须满足：

1. 可追溯。
2. 和推荐理由相关。
3. 不应过度引用无关网页内容。
4. 不应把推理包装成事实。
5. 不应引用不存在的页面。
6. 如果证据不足，必须写明 evidence_insufficient。

推荐输出结构：

- claim
- evidence_text
- source_url
- confidence
- explanation

---

## 9. Risk Rules

AI 必须为 Lead 输出风险提示。

常见风险包括：

- 网站信息不足
- 客户业务方向不明确
- 客户可能不是目标买家
- 客户地区不符合 Campaign
- 客户规模可能不合适
- 客户行业相关性弱
- 找不到可靠联系方式
- 只能找到 contact form
- 邮箱来源不可靠
- 公司可能已经不是活跃状态

风险提示不能被隐藏。

---

## 10. Outreach Email Rules

AI 可以生成开发信草稿，但必须遵守：

1. 只能为 Approved Lead 生成邮件草稿。
2. 必须基于已选定的有效联系人记录，而不是只依赖 Lead 级布尔字段。
3. 必须有 Confirmed Product Card。
4. 必须有 Confirmed Campaign。
5. 必须有有效的 outreach angle。
6. 邮件必须作为 Gmail Draft 创建。
7. 不允许自动发送邮件。
8. 不允许自动修改已存在邮件。
9. 不允许自动删除邮件。
10. 不允许读取或同步 Gmail inbox。
11. 不允许 track replies 或 monitor replies。
12. Gmail OAuth scope 必须限制为创建草稿所需的最小权限，例如
    `gmail.compose`。
13. 不允许伪造双方关系。
14. 不允许声称已经沟通过，除非系统中有明确记录。
15. 不允许使用虚假的客户痛点。
16. 不允许使用过度夸张或误导性承诺。
17. 邮件内容必须允许用户最终审核。

Gmail Draft eligibility：

A selected valid email contact means the contact passed as `contact_id` for the
current Outreach Draft or Gmail Draft action and validated by the backend. It
does not mean `contacts.selected = true`; the contacts table must not add a
selected boolean.

Lead / Contact / Outreach Draft 必须同时满足：

- `lead.review_status = approved`
- the frontend passed `contact_id`
- the selected contact belongs to the approved lead
- `contact.contact_type = email`
- `contact.status = valid`
- the contact is not blocked, invalid, unverified, LinkedIn, phone,
  contact form, or manual-review-only
- `outreach_drafts.contact_id` stores the selected contact after validation
- `outreach_drafts.subject` is not empty
- `outreach_drafts.body` is not empty
- 不存在同一 lead / contact / outreach draft 已经创建 Gmail Draft 的重复记录

只有 `contact.contact_type = email` 且 `contact.status = valid` 的联系人可以用于 Gmail Draft。
只有 LinkedIn contact 且没有 valid email contact 的 lead 不能创建 Gmail Draft。
rejected、unreviewed、needs_manual_review lead 不能创建 Gmail Draft。

不符合条件的 Lead 不能创建 Gmail Draft。

---

## 11. Provider / Adapter Rules

所有 AI、搜索、爬虫、邮箱查找、Gmail Draft 功能都必须通过 Provider 或 Adapter 封装。

禁止在 Service 中直接调用第三方 SDK。

必须封装的能力包括：

- LLM Provider
- Search Provider
- Crawler Provider
- Email Finder Provider
- Email Verification Provider
- Gmail Draft Provider
- Storage Provider
- Task Queue Provider

Provider 规则：

1. Service 只依赖接口，不依赖具体第三方实现。
2. 第三方 API Key 只能从环境变量读取。
3. Provider 必须有 mock 实现，方便测试。
4. Provider 失败时必须返回统一错误。
5. Provider 不能直接写数据库。
6. Provider 不能直接决定业务状态。
7. 第三方返回结果必须经过 Service 层验证后才能入库。

---

## 12. Prompt Management Rules

Prompt 必须集中管理，不能散落在业务代码中。

Prompt 应放在明确位置，例如：

- backend/app/ai/prompts/
- backend/app/modules/*/prompts/
- backend/app/core/ai/

Prompt 规则：

1. Prompt 必须有明确用途。
2. Prompt 修改应尽量可追踪。
3. Prompt 输出格式必须尽量固定。
4. 重要 AI 功能必须要求返回 JSON。
5. JSON 输出必须经过 schema validation。
6. Prompt 中必须明确禁止编造信息。
7. Prompt 中必须要求模型标记不确定内容。
8. Prompt 不能包含真实 API Key、密码或私人数据。
9. Prompt 不能绕过用户确认流程。

---

## 13. AI Error Handling Rules

AI 调用失败时，系统不能生成假结果。

常见错误包括：

- LLM API timeout
- LLM rate limit
- invalid JSON
- missing required fields
- crawler failed
- insufficient content
- provider unavailable
- email finder failed

处理规则：

1. 必须记录错误原因。
2. 必须返回用户可理解的状态。
3. 不能把失败结果标记为成功。
4. 不能自动重试无限次。
5. 后台任务失败必须进入 failed 状态。
6. 用户应能看到失败原因或简化后的错误说明。
7. 需要支持重新运行任务。

---

## 14. Human Review Rules

以下动作必须经过用户确认：

- 确认 Company Knowledge
- 确认 Product Card
- 确认 Campaign
- Approve Lead
- Reject Lead
- 创建 Gmail Draft 前的 Lead 审核
- 最终发送邮件

系统不能代替用户完成这些确认。

AI 可以提供建议，但不能自动点击确认、批准、发送或删除。

---

## 15. Forbidden Behaviors

本项目禁止以下行为：

1. 自动发送邮件。
2. 自动群发邮件。
3. 自动读取、同步、移动、标记、修改或删除 Gmail 邮件。
4. 自动发送 Gmail 邮件。
5. 使用 Google Sheets 作为核心流程。
6. 使用 LinkedIn API。
7. 编造客户信息。
8. 编造邮箱。
9. 编造网站证据。
10. 编造公司规模、收入、联系人职位。
11. 把 AI Draft 当作 Confirmed 内容。
12. 在没有证据时给高分推荐。
13. 绕过用户审核。
14. 把 Provider 写死在业务逻辑中。
15. 把 API Key 写入代码。
16. 在测试中调用真实付费 AI API。
17. 在后台任务中执行不可逆外部动作。
18. 执行 LinkedIn scraping。
19. 执行 LinkedIn browser automation。
20. 执行 LinkedIn crawler 或 LinkedIn bot。
21. 执行 LinkedIn browser extension automation。
22. 执行 automated LinkedIn login。
23. 执行 automated LinkedIn search。
24. 执行 automated LinkedIn profile extraction。
25. 执行 automated LinkedIn contact downloading。
26. 执行 automated LinkedIn messaging 或 automated LinkedIn connection requests。

---

## 16. Codex Checklist

每次开发 AI 相关功能前后，Codex 必须检查：

- [ ] AI 输出是否仍然是 Draft，而不是直接 Confirmed？
- [ ] 是否保留人工审核流程？
- [ ] 是否禁止自动发送邮件？
- [ ] 是否没有使用 Google Sheets？
- [ ] 是否没有接入 LinkedIn API？
- [ ] 是否没有实现 LinkedIn scraping、crawler、bot、browser automation 或 browser extension automation？
- [ ] AI / crawler / provider / browser 是否没有被要求自动访问 LinkedIn？
- [ ] LinkedIn URL 是否只被当作 manual reference 保存并给前端人工审核？
- [ ] 是否没有编造客户信息、邮箱或网站证据？
- [ ] 是否有 evidence / source / confidence？
- [ ] 是否有风险提示？
- [ ] 是否有 Provider / Adapter 封装？
- [ ] Service 是否没有直接调用第三方 SDK？
- [ ] Prompt 是否集中管理？
- [ ] AI JSON 输出是否经过 schema validation？
- [ ] AI 失败时是否不会生成假结果？
- [ ] 测试中是否使用 mock provider？
- [ ] Gmail Draft eligibility 是否只依赖 valid email contact，而不是 LinkedIn reference？
- [ ] Gmail 功能是否只创建 Draft，不发送、不读取、不同步、不修改、不删除？
- [ ] Gmail OAuth scope 是否限制为最小 draft creation 权限，例如
      `gmail.compose`？
