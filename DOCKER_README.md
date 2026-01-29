# Moltbot 项目管理系统 - Docker 部署

## 项目概述

这是一个基于 Django 开发的项目管理系统，用于记录和跟踪 Moltbot 处理的项目。

## Docker 部署说明

### 启动服务

```bash
# 启动服务（后台运行）
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f web
```

### 访问应用

- 应用地址: http://localhost:8000
- 数据库: PostgreSQL (内部访问)

### 停止服务

```bash
# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

### 项目特性

- **项目管理**: 创建、编辑、删除项目
- **状态跟踪**: 支持待处理、处理中、已完成、已取消等状态
- **搜索功能**: 跨标题、描述、结果和备注字段进行全文搜索
- **分页功能**: 每页显示10个项目，支持分页浏览
- **状态过滤**: 按项目状态筛选显示
- **统计功能**: 显示各状态项目数量的可视化统计
- **实时更新**: 可在列表页直接更新项目状态

## 目录结构

- `docker-compose.yml` - Docker Compose 配置
- `Dockerfile` - Web 服务构建文件
- `requirements.txt` - Python 依赖
- `project_manager/` - Django 项目配置
- `projects/` - Django 应用代码
- `static/` - 静态文件

## 数据库迁移

如果需要从 SQLite 迁移到 PostgreSQL，可以使用以下步骤：

```bash
# 进入容器
docker-compose exec web bash

# 导出 SQLite 数据
python manage.py dumpdata > backup.json

# 应用数据库迁移
python manage.py migrate
```

## 环境变量

- `DJANGO_SECRET_KEY`: Django 密钥
- `DJANGO_DEBUG`: 调试模式 (True/False)
- `POSTGRES_DB`: 数据库名
- `POSTGRES_USER`: 数据库用户
- `POSTGRES_PASSWORD`: 数据库密码