FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY backend/ ./

# 创建数据目录和生成示例数据
RUN mkdir -p ../data && python ../scripts/create_sample_data.py

# 暴露端口
EXPOSE 5001

# 启动应用
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]