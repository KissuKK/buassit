# 在 Zeabur 上部署银行客户咨询助手

本文档将指导您如何将银行客户咨询助手部署到 Zeabur 云平台。

## 项目架构

这是一个全栈应用，包含：
- **前端**：React 应用（端口 3000）
- **后端**：Flask API（端口 5001）

## 部署前准备

1. **GitHub 仓库**：
   - 确保您的代码已推送至 GitHub 公开或私有仓库
   - 如果尚未创建，请将项目推送到 GitHub

2. **Zeabur 账户**：
   - 访问 [Zeabur 官网](https://zeabur.com/zh-cn)
   - 使用 GitHub 账户登录

3. **环境变量准备**（可选，用于 NLP 功能）：
   - 如果您想使用自然语言查询功能，需要 DashScope API Key
   - 在 `backend/.env` 文件中设置 `DASHSCOPE_API_KEY`

## 部署步骤

### 1. 连接 GitHub 仓库

1. 登录 Zeabur 控制台
2. 点击 "Create Project"
3. 选择 "GitHub" 并授权连接
4. 选择您的银行客户咨询助手仓库

### 2. 配置后端服务

1. 在项目页面点击 "Create Service"
2. Zeabur 应能自动检测到后端 Flask 应用
3. 选择 `backend` 目录作为服务根目录
4. 确保构建方式为 Docker，使用 `backend/Dockerfile`
5. 设置端口为 5001
6. 在 "Environment Variables" 中添加：
   - `PORT`: `5001`
   - `DASHSCOPE_API_KEY`: （如果您有 API Key）

### 3. 配置前端服务

1. 在同一项目中再次点击 "Create Service"
2. 选择 `frontend` 目录
3. 确保构建方式为 Docker，使用 `frontend/Dockerfile`
4. 设置端口为 3000
5. 在 "Environment Variables" 中添加：
   - `PORT`: `3000`
   - `REACT_APP_API_URL`: `<后端服务的 URL>`

### 4. 配置前端代理（重要）

由于前端需要访问后端 API，您需要在前端环境中设置正确的 API 地址：

1. 在前端服务的环境变量中添加：
   - `REACT_APP_API_URL`: 后端服务的完整 URL（例如：https://your-backend-subdomain.zeabur.app）

### 5. 构建和部署

1. 配置完成后，Zeabur 会自动开始构建过程
2. 您可以在控制台查看构建日志
3. 构建成功后，服务会自动部署

## 部署后配置

### API 代理配置

如果前端无法访问后端 API，请确保：

1. 在前端环境变量中设置了正确的后端 API URL
2. 后端的 CORS 设置允许前端域名访问

### 数据文件

系统会自动创建示例数据文件 `data/customers.xlsx`，但如果需要使用自定义数据：

1. 您可以将您的 Excel 数据文件上传到部署后的系统
2. 或者通过环境变量指定数据文件位置

## 故障排除

### 常见问题

1. **前端无法访问后端 API**：
   - 检查前端环境变量中的 `REACT_APP_API_URL` 是否正确
   - 确认后端服务已正常运行

2. **构建失败**：
   - 检查 Dockerfile 是否正确
   - 确认所有依赖项都已正确指定

3. **端口错误**：
   - 确保后端使用 `$PORT` 环境变量指定的端口
   - 检查 Zeabur 服务配置中的端口设置

### 环境变量参考

后端服务需要的环境变量：
- `PORT`: 服务端口（默认 5001）
- `DASHSCOPE_API_KEY`: DashScope API Key（可选）

前端服务需要的环境变量：
- `PORT`: 服务端口（默认 3000）
- `REACT_APP_API_URL`: 后端 API 的完整 URL

## 访问您的应用

部署完成后，您将获得两个 URL：
- 前端 URL：用于访问用户界面
- 后端 URL：用于 API 访问

## 更新应用

当您推送新代码到 GitHub 仓库时，Zeabur 会自动检测更改并重新构建部署。

## 注意事项

1. **数据持久性**：在 Zeabur 免费层上，文件系统是临时的，每次部署都会重置。如果需要持久化数据，需要使用外部数据库服务。
2. **API 限制**：如果使用 DashScope API，请注意 API 调用限制。
3. **SSL 证书**：Zeabur 会自动为您的域名提供 SSL 证书。
