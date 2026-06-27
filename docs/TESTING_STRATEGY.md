# Testing Strategy

本文档规定本项目的测试策略、测试范围、测试命名、Mock 策略和 CI 要求。

本项目是 AI B2B 销售开发助手，核心风险包括：

- AI 输出不稳定
- 第三方 Provider 失败
- 数据库状态错误
- 后台任务失败
- Lead 评分逻辑不一致
- Gmail Draft 误创建
- 用户审核流程被绕过

测试目标不是追求形式上的覆盖率，而是保证核心业务流程稳定、可维护、可部署。

---

## 1. Testing Goals

测试必须保证：

1. 核心业务流程可以正常运行。
2. 数据状态转换正确。
3. AI Draft 不会绕过人工审核。
4. Gmail 只会创建 Draft，不会发送邮件。
5. Provider 可以被 Mock，不依赖真实第三方服务。
6. 数据库 migration 可以正常执行。
7. API 返回结构稳定。
8. 前端核心页面可以完成主要操作。
9. 后台任务失败时不会破坏数据。
10. 部署前可以通过自动化测试发现明显错误。

---

## 2. Test Types

项目测试分为以下几类：

- Unit Tests
- Service Tests
- Repository Tests
- API Tests
- Database Tests
- Provider Mock Tests
- AI Output Validation Tests
- Background Job Tests
- Frontend Component Tests
- End-to-End Smoke Tests

MVP 阶段不需要追求复杂 E2E 自动化，但必须覆盖核心业务流程。

---

## 3. Backend Testing

后端测试重点：

- Service 层业务规则
- Repository 层数据读写
- API route 输入输出
- 数据状态转换
- Provider mock 行为
- 后台任务执行结果
- AI 输出 schema validation
- Alembic migration

后端测试建议目录：

```text
backend/tests/
  unit/
  services/
  repositories/
  api/
  providers/
  jobs/
  database/
  fixtures/
```

---

## 4. Frontend Testing

前端测试重点：

- 页面能正常渲染
- 表单校验正确
- API loading / error / empty 状态正确
- 用户审核按钮行为正确
- Lead 列表和详情展示正确
- Gmail Draft eligibility 展示正确
- 不允许用户误操作自动发送邮件

前端测试建议目录：

```text
frontend/src/__tests__/
frontend/src/components/__tests__/
frontend/src/pages/__tests__/
```

MVP 阶段前端测试优先级：

1. 核心页面 smoke test
2. 关键组件 render test
3. 用户审核操作测试
4. API mock 测试

---

## 5. Unit Test Rules

Unit Test 应测试单个函数或单个类的行为。

规则：

1. 不连接真实数据库。
2. 不调用真实 AI API。
3. 不调用真实搜索 API。
4. 不调用真实 Gmail API。
5. 不依赖网络。
6. 输入和输出必须明确。
7. 测试名称必须描述业务行为。

推荐命名方式：

- test_should_create_knowledge_draft_from_valid_input
- test_should_not_confirm_ai_draft_without_user_action
- test_should_reject_lead_when_required_fields_missing
- test_should_not_create_gmail_draft_without_selected_valid_email_contact

---

## 6. Service Test Rules

Service Test 用于测试业务逻辑。

Service 层必须测试：

- Company Knowledge Draft 生成流程
- Product Card 生成流程
- Campaign 创建流程
- Lead 基础验证流程
- Lead Scoring 流程
- Lead Review 流程
- Gmail Draft eligibility
- Task 状态转换

Service Test 规则：

1. 使用 mock repository 或 test database。
2. 使用 mock provider。
3. 不直接调用第三方服务。
4. 必须检查数据库状态或返回对象状态。
5. 必须覆盖失败场景。
6. 必须覆盖权限或 owner_id / workspace_id 占位逻辑。

---

## 7. Repository Test Rules

Repository Test 用于测试数据库读写逻辑。

必须测试：

- create
- get by id
- list
- update
- soft delete if applicable
- filter by workspace_id / owner_id
- unique constraint
- foreign key constraint
- pagination

Repository Test 可以使用测试数据库，但不能使用生产数据库。

测试数据库规则：

1. 必须和生产数据库类型一致，优先使用 PostgreSQL。
2. 测试数据必须可重复创建和清理。
3. 不允许测试连接真实生产数据。
4. 每个测试应尽量隔离。
5. 测试结束后必须清理数据或回滚事务。

---

## 8. API Test Rules

API Test 用于测试 FastAPI route。

必须测试：

- request validation
- response schema
- success response
- error response
- not found
- invalid status transition
- missing required fields
- pagination
- filtering
- workspace_id / owner_id isolation

API Test 规则：

1. Route 不应包含复杂业务逻辑。
2. Route 应调用 Service。
3. API 测试不应调用真实第三方 Provider。
4. 错误响应必须稳定。
5. HTTP status code 必须符合语义。

推荐状态码：

- 200 OK
- 201 Created
- 400 Bad Request
- 404 Not Found
- 409 Conflict
- 422 Validation Error
- 500 Internal Server Error

---

## 9. AI Output Validation Tests

AI 输出不能直接信任，必须测试 schema validation。

必须测试：

1. AI 返回完整 JSON。
2. AI 返回缺失字段。
3. AI 返回错误字段类型。
4. AI 返回 invalid JSON。
5. AI 返回空内容。
6. AI 返回编造来源。
7. AI 返回没有 evidence 的高分结果。
8. AI 返回不确定内容时是否被正确标记。
9. AI 失败时是否不会写入成功状态。

AI 测试不应测试模型“聪不聪明”，而应测试系统如何处理 AI 输出。

---

## 10. Provider Mock Strategy

所有第三方服务必须通过 Provider / Adapter Mock 测试。

必须 Mock 的 Provider：

- LLM Provider
- Search Provider
- Crawler Provider
- Email Finder Provider
- Email Verification Provider
- Gmail Draft Provider
- Storage Provider
- Task Queue Provider

Mock Provider 应覆盖：

- success
- timeout
- rate limit
- invalid response
- empty result
- partial result
- provider unavailable

测试中禁止：

- 使用真实 OpenAI / Claude / Gemini API
- 使用真实 Gmail API
- 使用真实搜索 API
- 使用真实邮箱查找 API
- 使用真实付费爬虫 API

---

## 11. Gmail Draft Testing Rules

Gmail 功能是高风险功能，必须严格测试。

Gmail Draft eligibility must be based on a selected valid email contact.

- `lead.review_status = approved`
- selected contact exists
- `contact.contact_type = email`
- `contact.status = valid`
- outreach draft subject/body 非空
- 不存在同一 `lead_id + campaign_id + contact_id` 已创建的 `gmail_draft_created` 记录

必须测试：

1. Approved Lead + selected valid email contact can create a Gmail Draft.
2. No selected contact cannot create a Gmail Draft.
3. Selected contact is not `contact_type = email` cannot create a Gmail Draft.
4. Selected email contact is not `status = valid` cannot create a Gmail Draft.
5. Lead not approved cannot create a Gmail Draft.
6. Existing `gmail_draft_created` record for the same `lead_id + campaign_id + contact_id` cannot create a duplicate Draft.
7. Empty subject cannot create a Gmail Draft.
8. Empty body cannot create a Gmail Draft.
9. Gmail Provider failure moves the task or draft status to failed.
10. The system must not contain or call Gmail send / modify / delete behavior.
11. LinkedIn contact, contact form, or manual review contact cannot be used as a Gmail Draft recipient.

禁止测试中调用真实 Gmail。

---

## 12. Background Job Testing

后台任务包括：

- crawling job
- lead discovery job
- lead scoring job
- contact finding job
- outreach draft job

后台任务测试必须覆盖：

- pending -> running -> completed
- pending -> running -> failed
- retryable error
- non-retryable error
- partial success
- task log
- job result
- idempotency

后台任务规则：

1. Job 不能执行不可逆外部动作。
2. Job 失败不能导致数据状态混乱。
3. Job 必须记录错误原因。
4. Job 应支持重新运行。
5. Job 应避免重复创建相同结果。
6. Job 中第三方调用必须使用 Provider。

---

## 13. Database and Migration Testing

数据库使用 PostgreSQL，migration 使用 Alembic。

必须测试：

- alembic upgrade head
- alembic downgrade if supported
- 新表创建
- 新字段默认值
- foreign key
- index
- enum or status constraints
- nullable / non-nullable constraints
- migration 不丢失重要数据

规则：

1. 每次修改 models 后必须检查 migration。
2. 不允许手动改生产数据库结构。
3. migration 文件必须进入版本控制。
4. migration 名称应描述变更内容。
5. 删除字段或表必须谨慎，MVP 阶段优先 soft delete 或保留兼容。

### SQLite and PostgreSQL Boundary

SQLite 可以继续用于快速 unit、service 和 route 行为测试，但不能替代 PostgreSQL schema validation。

必须明确：

- `Base.metadata.create_all()` 只验证当前 ORM metadata 可以创建表，不等于执行 Alembic migration。
- SQLite in-memory tests 不能证明 migration 能在 PostgreSQL 上运行。
- SQLite 不能作为 JSON/JSONB、foreign key、check constraint、index、constraint name 或 migration order 的最终依据。
- PostgreSQL 是生产目标和数据库行为的最终标准。

### PostgreSQL Migration Smoke Test

每个包含 migration 的重要 backend phase 完成后，应使用独立 PostgreSQL 测试数据库执行 smoke test。

最低验证流程：

1. 启动或创建独立 PostgreSQL 测试数据库。
2. 执行 `alembic upgrade head`。
3. 检查新表、字段、foreign key、index、check constraint 和实际 constraint name。
4. 如果 migration 支持 downgrade，可执行 `alembic downgrade -1`。
5. 再次执行 `alembic upgrade head`。
6. 运行关键 backend tests。

阶段要求：

- Phase 3 前：recommended foundation hardening。
- Phase 11 deployment 前：required verification。
- Phase 12 MVP stabilization：required exit check。
- 当前可以暂不实现完整 CI，但不能用 SQLite 或 PostgreSQL offline SQL generation 代替真实 PostgreSQL smoke test。

---

## 14. Test Data Rules

测试数据必须清晰、可重复。

建议 fixtures：

- sample company profile
- sample company knowledge draft
- sample confirmed knowledge
- sample product card
- sample campaign
- sample valid lead
- sample invalid lead
- sample scored lead
- sample approved lead
- sample rejected lead
- sample outreach draft

测试数据不能包含：

- 真实 API Key
- 真实客户隐私数据
- 真实个人邮箱
- 生产数据库内容
- 敏感商业信息

---

## 15. CI Requirements

CI 至少应运行：

1. backend lint
2. backend unit tests
3. backend API tests
4. frontend lint
5. frontend build
6. frontend basic tests
7. alembic migration check

MVP 阶段推荐 CI 命令：

Backend:

- run backend tests
- run type check if configured
- run lint if configured
- run alembic upgrade head on test database

Frontend:

- run npm install
- run npm run lint
- run npm run build
- run npm test if configured

CI 不能依赖真实第三方 API。

---

## 16. Manual Testing Checklist

在重要功能完成后，必须进行手动测试。

核心手动测试流程：

1. 创建 Company Profile。
2. 上传或输入公司资料。
3. 生成 Company Knowledge Draft。
4. 用户确认 Knowledge。
5. 生成 Product Card。
6. 用户确认 Product Card。
7. 创建 Campaign。
8. 搜索候选客户。
9. 抓取客户网站。
10. 执行基础验证。
11. 执行 AI Scoring。
12. 查看 Lead 推荐理由、证据、风险。
13. Approve Lead。
14. 生成 Gmail Draft。
15. 确认 Gmail Draft 没有自动发送。

---

## 17. Definition of Done

一个功能完成必须满足：

1. 代码实现完成。
2. 核心测试通过。
3. 错误场景有处理。
4. 不绕过人工审核。
5. 不直接调用真实第三方 SDK。
6. 不引入 Google Sheets。
7. 不引入 LinkedIn API。
8. 不自动发送邮件。
9. 数据库 migration 已生成并测试。
10. API schema 和前端调用一致。
11. 文档如有必要已更新。
12. 对包含重要 migration 的阶段，已记录或完成真实 PostgreSQL migration smoke test；未完成时必须明确列为 blocker 或 backlog。

---

## 18. Codex Checklist

每次开发前后，Codex 必须检查：

- [ ] 是否为新功能添加了对应测试？
- [ ] 是否覆盖成功场景和失败场景？
- [ ] 是否使用 mock provider，而不是真实第三方 API？
- [ ] 是否没有在测试中调用真实 Gmail？
- [ ] 是否测试了 AI invalid JSON / missing fields？
- [ ] 是否测试了 Gmail Draft eligibility？
- [ ] 是否测试了人工审核状态转换？
- [ ] 是否测试了后台任务 failed 状态？
- [ ] 是否检查了 Alembic migration？
- [ ] ORM model 与 migration 的 check constraint 最终名称是否一致？
- [ ] 如果新增重要 migration，是否运行了真实 PostgreSQL migration smoke test，或明确记录尚未完成？
- [ ] 是否没有把 SQLite `create_all()` 或 in-memory tests 当作 PostgreSQL migration 验证？
- [ ] 是否确认 frontend build 可以通过？
- [ ] 是否确认 backend tests 可以通过？
- [ ] 是否没有引入 Google Sheets？
- [ ] 是否没有引入 LinkedIn API？
- [ ] 是否没有自动发送邮件？
- [ ] 是否没有把 AI Draft 当作 Confirmed 内容？
