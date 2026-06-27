# Backend

Current implemented backend slices:

- `company`: company profile create, list, get, and update
- `sources`: company-owned text/URL source create, list, and get
- `knowledge`: deterministic source-to-draft creation, status-filtered listing, confirm, and reject
- `products`: confirmed-knowledge-only deterministic Product Card generation, manual Product Card creation, list, get, patch/edit, confirm, and delete

Current Product Card backend behavior:

- Product Cards support only `draft` and `confirmed` statuses.
- `rejected` is not a valid Product Card status, and there is no Product Card reject endpoint.
- Delete replaces the legacy reject/rejected behavior.
- AI-generated Product Cards are created from confirmed company knowledge and start with `status = draft` and `source_type = ai_generated`.
- Manual Product Cards are user-created, belong to a company, and start with `status = draft` and `source_type = manual`.
- Product Cards support list, get, patch/edit, confirm, and delete.
- PATCH edits only user-editable Product Card fields and must not change status, source type, source knowledge, or company ownership.
- Confirm is idempotent: confirming an already confirmed Product Card returns the current confirmed record.
- Draft Product Cards can be deleted. Confirmed Product Cards can be deleted only when no Campaign has ever referenced them; otherwise deletion returns HTTP `409`.
- Campaign is still a later phase. Only confirmed Product Cards may be selected by Campaign when that module is implemented.

Phases 1B and 2 intentionally do not include document parsing, OCR, crawling, real LLM calls, external integrations, or frontend workflow pages.

这是基于 FastAPI 的后端基础实现，当前提供：

- 基础应用入口
- `/health`、`/health/db`、`/health/redis` 健康检查
- 配置、数据库、日志与错误处理基础层
- `company` 模块的最小可工作垂直切片
- Alembic 初始化配置和 `company_profiles` 基线 migration
- 模块化单体目录结构

当前仍未完成的部分包括：其余业务模块、多数 provider 的真实实现、后台 worker、以及前端业务页面。
