#!/bin/bash

# 更新包列表
sudo apt-get update

# 安裝 Noto Sans CJK 字型
sudo apt-get install -y fonts-noto-cjk

# 清理字型緩存
sudo fc-cache -fv

# 檢查字型文件是否存在
if [ -f "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc" ]; then
    echo "Noto Sans CJK SC 字型安裝成功"
else
    echo "Noto Sans CJK SC 字型安裝失敗"
    exit 1
fi