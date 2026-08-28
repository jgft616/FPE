# PlatoRelay 绕过工具 - 部署指南

## 方式一：Render.com（推荐，免费）

### 步骤

1. **注册 GitHub 账号**（如果还没有）
   - 访问 https://github.com/signup

2. **创建新仓库**
   - 访问 https://github.com/new
   - 仓库名填 `platoboost-bypass`
   - 选择 Public
   - 点击 Create repository

3. **上传文件**
   把以下文件全部上传到仓库：
   - `server.py`
   - `deltax.py`
   - `index.html`
   - `standalone.html`
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - `.gitignore`

4. **注册 Render.com**
   - 访问 https://render.com
   - 用 GitHub 账号登录

5. **部署**
   - 点击 New → Web Service
   - 选择刚才创建的 GitHub 仓库
   - Render 会自动检测 render.yaml 配置
   - 直接点击 Create Web Service
   - 等待 3-5 分钟构建完成

6. **获取链接**
   部署完成后 Render 会给你一个链接，格式如：
   `https://platoboost-bypass.onrender.com`

7. **分享**
   把这个链接发给别人就能用了！

---

## 方式二：本地运行

```bash
cd platoboost-bypasser
pip install -r requirements.txt
python server.py
```
浏览器打开 http://localhost:5000

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `server.py` | Flask 后端服务 |
| `deltax.py` | 绕过核心引擎 |
| `index.html` | 完整版前端页面 |
| `standalone.html` | 纯前端版页面 |
| `requirements.txt` | Python 依赖 |
| `Procfile` | 部署启动命令 |
| `render.yaml` | Render 部署配置 |

## API 接口

- `POST /api/bypass` — 绕过链接
  - 请求体: `{"url": "https://auth.platorelay.com/a?d=..."}`
  - 返回: `{"success": true, "key": "FREE_xxx", "timeLeft": "23小时59分钟"}`

- `GET /api/status` — 服务器状态
- `GET /health` — 健康检查
