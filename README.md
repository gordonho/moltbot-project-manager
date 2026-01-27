# Moltbot 项目管理系统

这是一个基于 Django 开发的项目管理应用程序，用于记录和跟踪 Moltbot 处理的项目，便于后续审查。

## 功能特点

- 创建、编辑、删除项目
- 跟踪项目状态（待处理、处理中、已完成、已取消）
- 记录项目处理结果和备注
- 响应式 Web 界面
- Django 管理后台支持

## 安装和运行

### 1. 克隆项目

```bash
git clone https://github.com/gordonho/moltbot-project-manager.git
cd moltbot-project-manager
```

### 2. 创建虚拟环境并安装依赖

```bash
python3 -m venv venv
source venv/bin/activate  # 在 Windows 上使用: venv\Scripts\activate
pip install django
```

### 3. 运行数据库迁移

```bash
python manage.py migrate
```

### 4. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

### 5. 启动开发服务器

```bash
python manage.py runserver
```

然后访问 http://127.0.0.1:8000/ 查看应用，或访问 http://127.0.0.1:8000/admin/ 访问管理后台。

## 使用说明

1. 通过 Web 界面创建新项目或编辑现有项目
2. 在项目详情中记录处理结果和备注
3. 使用状态字段跟踪项目进度
4. 利用管理后台进行高级管理操作

## 技术栈

- Python 3
- Django 4.x
- Bootstrap 5
- SQLite (默认数据库)

## 许可证

MIT License