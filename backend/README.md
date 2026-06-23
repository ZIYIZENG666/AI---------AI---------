# Backend

这是基于 FastAPI 的后端基础实现，当前提供：

- 基础应用入口
- `/health`、`/health/db`、`/health/redis` 健康检查
- 配置、数据库、日志与错误处理基础层
- `company` 模块的最小可工作垂直切片
- Alembic 初始化配置和 `company_profiles` 基线 migration
- 模块化单体目录结构

当前仍未完成的部分包括：其余业务模块、多数 provider 的真实实现、后台 worker、以及前端业务页面。
