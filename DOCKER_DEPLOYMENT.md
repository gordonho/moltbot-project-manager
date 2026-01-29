# Docker 部署文档

## 部署概述

Moltbot Project Management System 已成功容器化并使用 Docker 部署。

## 部署详情

- **镜像名称**: moltbot-project-manager-web
- **运行端口**: 8000 (映射到主机端口 8000)
- **数据库**: SQLite (持久化存储)
- **Web 服务器**: Gunicorn (3个工作进程)
- **容器状态**: 正常运行

## 部署文件

1. **Dockerfile** - 定义容器镜像构建过程
2. **docker-compose.simple.yml** - 定义服务编排配置
3. **requirements.txt** - Python 依赖列表
4. **db.sqlite3** - 持久化数据库文件

## 访问方式

- 应用地址: http://localhost:8000
- 管理后台: http://localhost:8000/admin

## 管理命令

```bash
# 启动服务
docker-compose -f docker-compose.simple.yml up -d

# 停止服务
docker-compose -f docker-compose.simple.yml down

# 查看日志
docker-compose -f docker-compose.simple.yml logs -f

# 重建镜像
docker-compose -f docker-compose.simple.yml build --no-cache
```

## 数据持久化

数据库文件 (`db.sqlite3`) 和媒体文件已配置为持久化存储，不会因容器重启而丢失。

## 状态

✅ **部署完成** - 服务正常运行