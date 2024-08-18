#!/bin/bash

# 更新包列表
sudo apt-get update

# 安裝 SimHei 字型
sudo apt-get install -y fonts-wqy-zenhei

# 安裝 Noto Sans CJK 字型
sudo apt-get install -y fonts-noto-cjk

# 清理字型緩存
sudo fc-cache -fv