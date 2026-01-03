# 安装与配置指南

## 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 后端配置

### 1. 安装Python依赖

```bash
pip install -r requirements.txt
```

或者使用虚拟环境：

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置DashScope API Key

复制 `.env.example` 文件为 `.env`：

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，填入你的DashScope API Key：

```
DASHSCOPE_API_KEY=sk-your-api-key-here
```

**注意**: 如果没有DashScope API Key，系统仍可运行，但会使用简化的规则匹配进行自然语言查询解析。

### 3. 准备数据文件

确保 `data/customers.xlsx` 文件存在。如果不存在，运行以下命令创建示例数据：

```bash
python3 scripts/create_sample_data.py
```

数据文件格式：
- Sheet名称: `customers` 或 `客户信息`
- 必需的列: `user_id`, `user_name`, `asset_scale`, `trading_frequency`, `risk_preference`
- 可选Sheet: `events` 或 `行为事件` (行为事件数据)

### 4. 启动后端服务

```bash
cd backend
python app.py
```

后端服务默认运行在 `http://localhost:5001`（使用5001端口避免与macOS AirPlay Receiver冲突）

## 前端配置

### 1. 安装Node.js依赖

```bash
cd frontend
npm install
```

### 2. 配置API地址（可选）

如果需要修改后端API地址，创建 `.env` 文件：

```bash
cd frontend
echo "REACT_APP_API_URL=http://localhost:5001/api" > .env
```

### 3. 启动前端开发服务器

```bash
npm start
```

前端应用默认运行在 `http://localhost:3000`

## 使用说明

### 自然语言查询

在"自然语言查询"标签页中，输入自然语言问题，例如：
- "姓李的客户有谁"
- "稳健型客户有哪些"
- "资产规模大于100万的客户"

系统会使用DashScope API（如果已配置）或规则匹配将自然语言转换为查询条件。

### 单客户查询

在"单客户查询"标签页中，输入客户ID或客户名称进行查询。

### 批量客户查询

在"批量客户查询"标签页中，可以：
1. 手动输入：每行一个客户ID或客户名称
2. 文件上传：
   - Excel文件：支持.xlsx/.xls格式，需包含"客户ID"或"客户名称"列
   - 文本文件：支持.txt格式，每行一个客户ID或客户名称

## 故障排除

### 后端无法启动

1. 检查Python依赖是否已安装
2. 检查端口5000是否被占用
3. 检查数据文件路径是否正确

### 前端无法连接后端

1. 确认后端服务已启动
2. 检查 `frontend/.env` 中的API地址配置
3. 检查浏览器控制台的错误信息

### 自然语言查询不准确

1. 确认DashScope API Key已正确配置
2. 如果未配置API Key，系统使用简化的规则匹配，准确度较低
3. 建议使用更明确的关键词，如"姓X的"、"稳健型"等

