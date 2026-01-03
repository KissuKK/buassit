# 银行客户咨询助手

一个基于React + Flask + DashScope的银行客户咨询助手应用，支持自然语言查询、单客户查询和批量客户查询。

## 技术栈

- **前端**: React + Ant Design
- **后端**: Python Flask
- **数据层**: Pandas (读取Excel文件)
- **大模型**: DashScope API (阿里云通义千问)

## 项目结构

```
bankcca/
├── frontend/              # React前端应用
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── services/      # API服务
│   │   └── App.js
│   └── package.json
├── backend/               # Flask后端API
│   ├── app.py            # Flask主应用
│   ├── data_service.py   # 数据服务
│   ├── nlp_service.py    # NLP服务
│   └── .env.example      # 环境变量示例
├── data/                  # Excel数据文件
│   └── customers.xlsx    # 客户数据
├── scripts/               # 工具脚本
│   └── create_sample_data.py
├── requirements.txt       # Python依赖
├── start_backend.sh      # 后端启动脚本
├── start_frontend.sh     # 前端启动脚本
├── SETUP.md              # 详细配置说明
└── README.md
```

## 功能特性

1. **自然语言查询**: 支持通过自然语言查询客户信息
2. **单客户查询**: 根据客户名称或ID查询单个客户详细信息
3. **批量客户查询**: 支持手动输入或文件上传批量查询

## 快速开始

详细安装配置请参考 [SETUP.md](SETUP.md)

### 后端

```bash
# 安装依赖
pip install -r requirements.txt

# 配置API Key（可选，用于自然语言查询）
cd backend
cp .env.example .env
# 编辑.env文件，填入DashScope API Key

# 创建示例数据（如果数据文件不存在）
python3 ../scripts/create_sample_data.py

# 启动服务
python app.py
```

### 前端

```bash
cd frontend
npm install
npm start
```

访问 http://localhost:3000 查看应用

## 数据模型

### 用户信息
- user_id: 用户ID
- user_name: 用户名称
- asset_scale: 资产规模
- trading_frequency: 交易频率
- risk_preference: 风险偏好

### 行为事件
- event_time: 事件时间
- event_type: 事件类型
- event_detail: 事件详情
- user_id: 用户ID
- user_name: 用户名称

