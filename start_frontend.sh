#!/bin/bash

# 银行客户咨询助手 - 前端启动脚本

echo "正在启动前端服务..."

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "错误: 未找到Node.js，请先安装Node.js"
    exit 1
fi

# 进入frontend目录
cd frontend

# 检查node_modules是否存在
if [ ! -d "node_modules" ]; then
    echo "正在安装Node.js依赖..."
    npm install
fi

# 启动开发服务器
echo "前端服务启动在 http://localhost:3000"
npm start

