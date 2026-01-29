# Moltbot 项目管理系统 - 开发版 Docker 部署

## 项目概述

这是一个基于 Django 开发的项目管理系统，用于记录和跟踪 Moltbot 处理的项目。

## 开发版 Docker 部署说明

开发版 Docker 配置支持代码热更新，当代码更改时无需重新构建镜像。

### 启动开发版服务

```bash
# 启动开发版服务（支持代码热更新）
docker-compose -f docker-compose.dev.yml up -d

# 查看服务状态
docker-compose -f docker-compose.dev.yml ps

# 查看服务日志
docker-compose -f docker-compose.dev.yml logs -f web
```

### 访问应用

- 应用地址: http://localhost:8000
- 数据库: SQLite (持久化到 ./db_data/)

### 停止服务

```bash
# 停止开发版服务
docker-compose -f docker-compose.dev.yml down
```

### 卷挂载说明

开发版配置包含以下卷挂载：

- `.: /app` - 挂载整个项目目录，实现代码热更新
- `./media: /app/media` - 持久化媒体文件
- `./static: /app/static` - 持久化静态文件
- `./db_data: /app/db_data` - 持久化数据库文件

### 特性

- **代码热更新** - 修改代码后无需重建容器
- **数据持久化** - 数据库、静态文件和媒体文件持久化存储
- **开发友好** - 使用Django开发服务器，便于调试

## 生产版 vs 开发版

- **开发版** (docker-compose.dev.yml): 适合开发调试，支持代码热更新
- **生产版** (docker-compose.yml): 适合生产部署，使用 Gunicorn 服务器

## 环境变量

- `DEBUG=1`: 启用调试模式
- `DATABASE_URL=sqlite:////app/db_data/db.sqlite3`: SQLite数据库路径