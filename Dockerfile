# 使用官方 Python 基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 更新包列表並安裝必要的包
RUN apt-get update && \
    apt-get install -y fonts-noto-cjk fontconfig && \
    fc-cache -fv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 複製應用程式代碼
COPY . .

# 暴露應用程式埠
EXPOSE 8000

# 設置啟動命令
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]