#!/bin/bash

# 银行客户咨询助手 - 后端启动脚本

echo "正在启动后端服务..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import flask" 2>/dev/null; then
    echo "正在安装Python依赖..."
    pip3 install -r requirements.txt
fi

# 检查数据文件是否存在
if [ ! -f "data/customers.xlsx" ]; then
    echo "数据文件不存在，正在创建示例数据..."
    python3 scripts/create_sample_data.py
fi

# 进入backend目录并启动服务
cd backend
# 使用5001端口，避免与macOS AirPlay Receiver冲突
export PORT=5001
python3 app.py

