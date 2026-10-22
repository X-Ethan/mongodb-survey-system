# 基于 MongoDB 的问卷系统

## 项目简介
简化版在线问卷系统，支持用户注册登录、创建问卷、添加单选/多选/填空题、发布问卷、填写提交、查看统计。

## 技术栈
- 后端：Python + FastAPI
- 数据库：MongoDB
- 认证：JWT + bcrypt

## 环境要求
- Python 3.10+
- MongoDB 运行在 localhost:27017

## 安装与运行
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pymongo pydantic "python-jose[cryptography]" "passlib[bcrypt]" "bcrypt==4.0.1"
uvicorn main:app --reload
```

## 主要接口
- POST /register 注册
- POST /login 登录（返回 JWT）
- POST /surveys 创建问卷
- POST /surveys/{id}/questions 添加题目
- POST /surveys/{id}/publish 发布
- POST /surveys/{id}/responses 提交答卷
- GET /surveys/{id}/stats 查看统计

## 测试说明
使用 curl 测试了注册、登录、创建问卷、添加三种题型、发布、提交答卷、统计查询，均返回预期结果。

## 作者
谢之恒 10245501428
