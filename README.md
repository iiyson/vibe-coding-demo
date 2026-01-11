# Vibe Coding Demo

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

### Project Overview
This project is a containerized web application for managing shape data. It features a unified login system that distinguishes between Administrators and regular Users. Admins can manage (Create, Read, Update, Delete) shape records, while Users can only view them. The system uses a modern blue-themed UI and renders shapes dynamically using HTML5 Canvas.

### Technology Stack
- **Frontend**:
    - Framework: [Vue 3](https://vuejs.org/) (Composition API)
    - Build Tool: [Vite](https://vitejs.dev/)
    - Styling: CSS3 (Custom variables, Responsive design)
    - Communication: [Axios](https://axios-http.com/)
    - Graphics: HTML5 Canvas (Dynamic shape rendering)
    - Deployment: [Nginx](https://www.nginx.com/) (Serving static files & Reverse Proxy)
- **Backend**:
    - Framework: [Django 5.x](https://www.djangoproject.com/)
    - API: [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
    - Database: [MySQL 8.0](https://www.mysql.com/)
    - Authentication: Token-based authentication
- **Containerization**:
    - [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

### Project Structure
```text
alphv_intern_app/
├── backend/                # Django Backend
│   ├── backend/            # Project configuration (settings, urls, etc.)
│   ├── shapes/             # Shapes application (models, views, serializers)
│   └── manage.py
├── frontend/               # Vue 3 Frontend
│   ├── src/                # Source code
│   │   ├── components/     # UI Components (ShapeCanvas, AdminPortal, etc.)
│   │   ├── App.vue         # Main entry component
│   │   └── main.js
│   ├── nginx.conf          # Nginx configuration for production
│   └── Dockerfile          # Multi-stage build for frontend
├── Dockerfile              # Backend Dockerfile
├── docker-compose.yml      # Docker orchestration
└── requirements.txt        # Python dependencies
```

### Functional Modules
1.  **Authentication**:
    - Unified login and registration interface.
    - Role-based redirection based on the `is_admin` field.
2.  **Admin Portal**:
    - Full CRUD (Create, Read, Update, Delete) operations for shape items.
    - Real-time form validation.
    - Automatic polling for data updates.
3.  **User Portal**:
    - Read-only access to the shape items list.
4.  **Shape Rendering**:
    - Dynamic drawing of Circle, Square, and Triangle on Canvas based on user-selected color and type.

### Database Schema
#### User Table (Custom User Model)
| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | CharField | Unique username |
| `password` | CharField | Hashed password |
| `is_admin` | BooleanField | Flag to distinguish Admin from User |

#### ShapeItem Table
| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | CharField | Name of the shape record |
| `color` | CharField | Color code (e.g., #ff0000) |
| `shape_type` | CharField | Type of shape (circle, square, triangle) |
| `timestamp` | DateTimeField | Recording time |

### Example Credentials
| Role | Username | Password |
| :--- | :--- | :--- |
| **Admin** | `admin` | `admin` |
| **User** | `user` | `userpwd` |

---

<a name="chinese"></a>
## 中文

### 项目概览
本项目是一个容器化的图形数据管理 Web 应用。它具有统一的登录系统，通过用户表中的 `is_admin` 字段区分管理员和普通用户。管理员可以管理（增删改查）图形记录，而普通用户仅能查看。系统采用现代化的蓝色主题 UI，并使用 HTML5 Canvas 动态渲染图形。

### 技术栈
- **前端**:
    - 框架: [Vue 3](https://vuejs.org/) (Composition API)
    - 构建工具: [Vite](https://vitejs.dev/)
    - 样式: CSS3 (自定义变量, 响应式设计)
    - 通信: [Axios](https://axios-http.com/)
    - 图形渲染: HTML5 Canvas (动态绘制)
    - 部署: [Nginx](https://www.nginx.com/) (提供静态文件服务及反向代理)
- **后端**:
    - 框架: [Django 5.x](https://www.djangoproject.com/)
    - API: [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
    - 数据库: [MySQL 8.0](https://www.mysql.com/)
    - 认证: 基于 Token 的认证机制
- **容器化**:
    - [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

### 项目结构
```text
alphv_intern_app/
├── backend/                # Django 后端
│   ├── backend/            # 项目配置 (settings, urls 等)
│   ├── shapes/             # 图形应用 (models, views, serializers)
│   └── manage.py
├── frontend/               # Vue 3 前端
│   ├── src/                # 源代码
│   │   ├── components/     # UI 组件 (ShapeCanvas, AdminPortal 等)
│   │   ├── App.vue         # 主入口组件
│   │   └── main.js
│   ├── nginx.conf          # 生产环境 Nginx 配置
│   └── Dockerfile          # 前端多阶段构建 Dockerfile
├── Dockerfile              # 后端 Dockerfile
├── docker-compose.yml      # Docker 编排文件
└── requirements.txt        # Python 依赖
```

### 功能模块
1.  **身份认证**:
    - 统一的登录和注册界面。
    - 根据 `is_admin` 字段进行角色路由跳转。
2.  **管理员门户**:
    - 图形条目的全权 CRUD（增删改查）操作。
    - 实时表单验证。
    - 自动轮询更新数据。
3.  **用户门户**:
    - 只读查看图形条目列表。
4.  **图形渲染**:
    - 根据用户选择的颜色和形状类型，在 Canvas 上动态绘制圆形、正方形和三角形。

### 数据库表结构
#### User 用户表 (自定义模型)
| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `username` | CharField | 唯一用户名 |
| `password` | CharField | 加密后的密码 |
| `is_admin` | BooleanField | 区分管理员与普通用户的标志 |

#### ShapeItem 图形条目表
| 字段 | 类型 | 说明 |
| :--- | :--- | :--- |
| `name` | CharField | 记录名称 |
| `color` | CharField | 颜色代码 (如 #ff0000) |
| `shape_type` | CharField | 图形类型 (circle, square, triangle) |
| `timestamp` | DateTimeField | 记录时间 |

### 示例账户
| 角色 | 用户名 | 密码 |
| :--- | :--- | :--- |
| **管理员** | `admin` | `admin` |
| **普通用户** | `user` | `userpwd` |
