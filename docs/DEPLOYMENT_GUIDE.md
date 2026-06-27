# Deployment Guide

本文档规定本项目的本地开发、环境变量、Docker、数据库迁移、生产部署、健康检查、日志、安全配置和回滚规则。

本项目从 MVP 阶段开始就按照可部署标准设计，避免后期从 prototype 改成生产项目时大改架构。

---

## 1. Deployment Goals

部署目标：

1. 本地可以稳定运行。
2. 生产环境可以使用 Docker 部署。
3. PostgreSQL 从第一版开始作为主数据库。
4. Redis 用于后台任务队列。
5. Alembic 管理数据库迁移。
6. 所有密钥通过环境变量管理。
7. 前后端配置分离。
8. 健康检查清晰。
9. 日志可以用于排查错误。
10. 出错时可以回滚到上一个稳定版本。

---

## 2. Environments

项目至少区分以下环境：

### 2.1 Local Development

用于本地开发。

特点：

- 可使用 Docker Compose 启动 PostgreSQL 和 Redis
- Backend 使用 FastAPI dev server
- Frontend 使用 Vite dev server
- 使用本地 .env
- 可以使用 mock provider
- 不连接生产数据库

### 2.2 Test

用于自动化测试。

特点：

- 使用独立测试数据库
- 不调用真实第三方 API
- 使用 mock provider
- 测试结束后清理数据

### 2.3 Production

用于正式部署。

特点：

- 使用生产 PostgreSQL
- 使用生产 Redis
- 使用真实环境变量
- 禁用 debug mode
- 启用日志
- 启用健康检查
- 不使用 mock provider，除非明确配置为 fallback

---

## 3. Required Services

项目运行需要以下服务：

- Frontend: React + TypeScript + Vite
- Backend: FastAPI
- Database: PostgreSQL
- Migration: Alembic
- Queue foundation: Redis
- Background worker: planned RQ worker, not yet wired into the current repository runtime
- Storage: Local or external storage through StorageProvider
- AI Provider: through LLM Provider interface
- Search Provider: through Search Provider interface
- Crawler Provider: through Crawler Provider interface
- Gmail Draft Provider: through Gmail Provider interface

MVP 不需要：

- Kubernetes
- microservices
- LangGraph
- full CRM
- automatic email sending
- LinkedIn API
- Google Sheets

---

## 4. Environment Variables

所有配置必须通过环境变量读取。

禁止把 API Key、密码、token 写死在代码中。

推荐环境变量：

### 4.1 Backend

- APP_ENV
- APP_NAME
- APP_DEBUG
- BACKEND_HOST
- BACKEND_PORT
- FRONTEND_URL
- DATABASE_URL
- REDIS_URL
- SECRET_KEY
- CORS_ALLOWED_ORIGINS

### 4.2 Database

- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT

### 4.3 AI Provider

- LLM_PROVIDER
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GEMINI_API_KEY
- LLM_MODEL
- LLM_TIMEOUT_SECONDS

只配置实际使用的 provider key。

### 4.4 Search / Crawler Provider

- SEARCH_PROVIDER
- SEARCH_API_KEY
- CRAWLER_PROVIDER
- CRAWLER_API_KEY
- CRAWLER_TIMEOUT_SECONDS

### 4.5 Gmail Draft

- GMAIL_CLIENT_ID
- GMAIL_CLIENT_SECRET
- GMAIL_REDIRECT_URI
- GMAIL_TOKEN_STORAGE_PATH

Gmail scope 只能包含创建草稿所需权限，不允许添加 send / modify / delete 权限。

### 4.6 Runtime Limits

- MAX_LEADS_PER_CAMPAIGN
- MAX_CRAWL_PAGES_PER_LEAD
- MAX_AI_TOKENS_PER_TASK
- TASK_TIMEOUT_SECONDS
- ENABLE_MOCK_PROVIDERS

---

## 5. Local Development Setup

本地开发推荐流程：

1. 复制环境变量文件。
2. 启动 PostgreSQL 和 Redis。
3. 安装 backend dependencies。
4. 运行 Alembic migration。
5. 启动 FastAPI。
6. 安装 frontend dependencies。
7. 启动 Vite frontend。

示例流程：

PowerShell example from the project root:

    Copy-Item .env.example .env

    docker compose up -d postgres redis

    Set-Location backend
    python -m pip install -e .
    python -m alembic -c alembic.ini upgrade head
    python -m uvicorn app.main:app --reload

    Set-Location ..\frontend
    npm install
    npm run dev

本地开发注意事项：

1. 不要连接生产数据库。
2. 不要使用生产 API Key。
3. AI / Search / Gmail 功能可以优先使用 mock provider。
4. 每次修改数据库模型后，必须生成 migration。
5. 前端 API base URL 必须指向本地 backend。

---

## 6. Docker Compose

项目应提供 docker-compose.yml，用于本地和简单服务器部署。

推荐包含服务：

- frontend
- backend
- postgres
- redis
- worker（planned, not currently included in `docker-compose.yml`）

### 6.1 Backend Container

Backend container 应负责：

- 启动 FastAPI API server
- 读取环境变量
- 连接 PostgreSQL
- 连接 Redis
- 暴露健康检查接口

Backend container 不应该：

- 写死数据库连接
- 自动调用真实 AI Provider
- 自动发送邮件
- 跳过 migration 检查

### 6.2 Worker Container (Future / Planned)

当前仓库尚未提供可运行的 worker service。

当后续引入 worker 时，应负责：

- 执行 RQ 后台任务
- 调用 Provider 接口
- 更新任务状态
- 记录任务日志

Worker container 不应该：

- 直接调用第三方 SDK 绕过 Provider
- 执行 Gmail send
- 操作 Google Sheets
- 使用 LinkedIn API

### 6.3 PostgreSQL Container

PostgreSQL container 用于本地开发或简单部署。

生产环境可以使用：

- Docker PostgreSQL
- managed PostgreSQL
- self-hosted PostgreSQL

无论使用哪种方式，都必须保证：

- 数据持久化
- 定期备份
- 不暴露公网端口，除非有安全配置
- 使用强密码

### 6.4 Redis Container

Redis 用于任务队列。

Redis 要求：

- 不存储长期业务数据
- 生产环境设置密码或限制访问
- 不暴露公网端口
- 出错时任务状态需要能在数据库中恢复或追踪

---

## 7. Database Migration

数据库迁移使用 Alembic。

规则：

1. 所有表结构变更必须通过 migration。
2. 不允许直接手动修改生产数据库结构。
3. migration 文件必须提交到版本控制。
4. migration 应在部署前测试。
5. 生产部署时先备份数据库，再执行 migration。
6. 高风险 migration 需要准备 rollback 方案。

常用命令：

    alembic revision --autogenerate -m "describe change"
    alembic upgrade head
    alembic downgrade -1

部署前必须确认：

- migration 可以在空数据库运行
- migration 可以在已有数据的数据库运行
- migration 不会误删重要数据
- model 与数据库结构一致

### 7.1 PostgreSQL Migration Smoke Test

SQLite migration tests and offline PostgreSQL SQL generation are useful prechecks, but neither proves that a migration runs successfully against a real PostgreSQL server.

Required smoke-test flow:

1. Start an isolated PostgreSQL test database.
2. Configure the backend and Alembic to use that test database.
3. Run `alembic upgrade head`.
4. Inspect new tables, JSON/JSONB columns, foreign keys, indexes, check constraints, constraint names, and revision order.
5. Optionally run `alembic downgrade -1` when the migration supports downgrade.
6. Run `alembic upgrade head` again.
7. Run the critical backend tests against the verified schema where practical.

Release gates:

- Before Phase 3: recommended foundation hardening for the current migrations.
- Before Phase 11 deployment work is considered complete: required verification.
- Before Phase 12 MVP stabilization exits: required verification.

Full CI automation may be added later, but deployment readiness must not be claimed from SQLite-only checks.

---

## 8. Production Deployment Flow

推荐生产部署流程：

1. 拉取最新代码。
2. 检查环境变量。
3. 构建 Docker images。
4. 备份 PostgreSQL 数据库。
5. 运行 Alembic migration。
6. 启动 backend。
7. 启动 frontend。
8. 检查健康检查接口。
9. 手动测试核心流程。
10. 检查日志是否有错误。

如果后续引入 worker，再补充停止和重启 worker 的发布步骤。

示例流程：

    git pull

    docker compose build

    backup database

    docker compose run --rm backend alembic upgrade head

    docker compose up -d backend frontend

    docker compose logs -f backend

---

## 9. Health Checks

Backend 必须提供健康检查接口。

推荐接口：

- GET /health
- GET /health/db
- GET /health/redis

### 9.1 /health

检查 API 服务是否启动。

返回示例：

    {
      "status": "ok",
      "service": "backend"
    }

### 9.2 /health/db

检查数据库连接。

返回示例：

    {
      "status": "ok",
      "database": "connected"
    }

### 9.3 /health/redis

检查 Redis 连接。

返回示例：

    {
      "status": "ok",
      "redis": "connected"
    }

健康检查不能暴露敏感信息。

禁止返回：

- database password
- API Key
- token
- full connection string
- user private data

---

## 10. Logging

日志必须用于排查问题，但不能泄露敏感信息。

必须记录：

- request id
- task id
- provider name
- task status
- error type
- error message
- duration
- retry count

禁止记录：

- API Key
- Gmail token
- database password
- full email body with sensitive content
- user private files raw content
- OAuth secret

AI 相关日志应记录：

- provider
- model name
- task type
- token usage if available
- validation result
- error reason

不应完整记录用户隐私内容和完整 prompt，除非明确用于本地调试且不进入生产日志。

---

## 11. Security Rules

生产环境必须遵守：

1. APP_DEBUG=false。
2. 使用强 SECRET_KEY。
3. 数据库密码不能使用默认值。
4. API Key 只能存在环境变量或 secret manager。
5. CORS 只能允许可信 frontend domain。
6. PostgreSQL 不应直接暴露到公网。
7. Redis 不应直接暴露到公网。
8. Gmail OAuth scope 只能用于 Draft。
9. 不允许 Gmail send / modify / delete scope。
10. 不允许把 .env 提交到 Git。
11. 不允许在日志中输出 token。
12. 上传文件必须限制大小和类型。
13. 用户输入必须做 validation。
14. 后台任务必须有 timeout。
15. Provider 调用必须有 timeout。

---

## 12. Backup Strategy

生产数据库必须定期备份。

备份规则：

1. migration 前必须备份。
2. 重要版本发布前必须备份。
3. 备份文件不能公开访问。
4. 备份文件应加密或放在受保护位置。
5. 应定期测试恢复流程。
6. 备份中可能包含客户数据，必须谨慎管理。

MVP 阶段至少应支持手动备份 PostgreSQL。

---

## 13. Rollback Strategy

部署失败时，应支持回滚。

回滚对象包括：

- application code
- Docker image
- database migration
- environment variables
- worker task execution

推荐回滚流程：

1. 停止 worker，避免继续处理任务。
2. 停止 backend。
3. 恢复到上一版本 image 或 commit。
4. 如 migration 可逆，执行 downgrade。
5. 如 migration 不可逆，使用数据库备份恢复。
6. 重启 backend。
7. 重启 worker。
8. 检查健康检查。
9. 检查核心流程。

注意：

高风险数据库变更应尽量避免不可逆操作。

---

## 14. Background Worker Deployment Rules

本节是 future-facing 规则。

当前仓库还没有在 `docker-compose.yml` 中提供 worker service。

当 worker 落地后，部署时必须谨慎。

规则：

1. migration 前应停止 worker。
2. 新版本 backend 和 worker 应使用兼容代码。
3. worker 不能处理旧 schema 不兼容的任务。
4. 任务必须有 failed 状态。
5. 任务必须可重试。
6. worker 不能执行自动发送邮件。
7. worker 不能绕过人工审核。
8. worker 失败必须写入 task log。

---

## 15. Frontend Deployment

Frontend 使用 React + TypeScript + Vite。

生产部署要求：

1. 使用生产 API base URL。
2. 不暴露 backend secret。
3. 不在 frontend 存储 API Key。
4. build 前必须通过 lint。
5. build 后静态文件可以由 Nginx 或其他静态服务器托管。
6. 前端必须正确处理 API error。
7. 前端页面不能展示未授权数据。

常用命令：

    npm install
    npm run build

---

## 16. Backend Deployment

Backend 使用 FastAPI。

生产部署要求：

1. 禁用 reload。
2. 禁用 debug。
3. 使用 production DATABASE_URL。
4. 使用 production REDIS_URL。
5. 启动前确认 migration 已完成。
6. Provider timeout 必须配置。
7. CORS 必须限制 domain。
8. health check 必须可访问。
9. logs 必须可查看。

---

## 17. Common Deployment Problems

### 17.1 Database connection failed

检查：

- DATABASE_URL 是否正确
- PostgreSQL container 是否启动
- 数据库用户名密码是否正确
- 网络是否连通
- migration 是否已执行

### 17.2 Redis connection failed

检查：

- REDIS_URL 是否正确
- Redis container 是否启动
- worker 是否能访问 Redis
- Redis 是否设置了密码

### 17.3 Alembic migration failed

检查：

- migration 文件是否最新
- models 是否和 migration 一致
- 数据库是否已有冲突数据
- 是否需要先备份
- 是否需要手动修复数据

### 17.4 AI Provider failed

检查：

- API Key 是否存在
- provider name 是否正确
- model name 是否正确
- 是否 rate limited
- timeout 是否过短
- mock provider 是否被错误关闭

### 17.5 Gmail Draft failed

检查：

- OAuth token 是否有效
- Gmail scope 是否正确
- 是否只使用 draft 权限
- Lead 是否 Approved
- selected contact 是否存在
- selected contact 是否 `contact_type = email`
- selected email contact 是否 `status = valid`
- subject/body 是否为空
- 是否已经存在同一 `lead_id + campaign_id + contact_id` 的 `gmail_draft_created` 记录

---

## 18. Deployment Checklist

每次部署前检查：

- [ ] 所有测试通过。
- [ ] frontend build 成功。
- [ ] backend 可以启动。
- [ ] Alembic migration 已检查。
- [ ] 重要 migration 已在独立 PostgreSQL 测试数据库运行 smoke test。
- [ ] ORM 与 migration 的 check constraint 名称一致。
- [ ] PostgreSQL 已备份。
- [ ] .env 已配置。
- [ ] APP_DEBUG=false。
- [ ] CORS domain 正确。
- [ ] Redis 可连接。
- [ ] Health check 正常。
- [ ] 没有提交 API Key。
- [ ] Gmail scope 没有 send / modify / delete。
- [ ] 没有 Google Sheets 配置。
- [ ] 没有 LinkedIn API 配置。
- [ ] 如果已引入 worker，worker 可启动且不会绕过人工审核。

---

## 19. Codex Checklist

每次修改部署相关内容前后，Codex 必须检查：

- [ ] 是否仍然使用 PostgreSQL 作为主数据库？
- [ ] 是否通过 Alembic 管理数据库结构？
- [ ] 是否没有用 SQLite 测试代替真实 PostgreSQL migration smoke test？
- [ ] 是否检查了 ORM/migration constraint 名称和 PostgreSQL 实际名称？
- [ ] 是否没有把 .env 或 secret 提交进代码？
- [ ] 是否没有写死 DATABASE_URL？
- [ ] 是否没有写死 API Key？
- [ ] 是否 Docker 配置与当前仓库一致，例如 backend / frontend / postgres / redis？
- [ ] 是否 backend 有 health check？
- [ ] 如果 worker 已实现，是否 worker 不会自动发送邮件？
- [ ] 是否 Gmail scope 只允许 Draft？
- [ ] 是否生产环境关闭 debug？
- [ ] 是否 CORS 配置安全？
- [ ] 是否 migration 前有备份提醒？
- [ ] 是否有 rollback 思路？
- [ ] 是否日志不会泄露敏感信息？
- [ ] 是否没有重新引入 Google Sheets 或 LinkedIn API？
