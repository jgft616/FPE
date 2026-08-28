#!/bin/bash
cd "$(dirname "$0")"
echo "============================================"
echo "  PlatoRelay 绕过工具"
echo "============================================"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[!] 需要安装 Python 3"
    exit 1
fi

# 安装依赖
if [ ! -d "venv" ]; then
    echo "[1/3] 创建虚拟环境..."
    python3 -m venv venv
fi

echo "[2/3] 安装依赖..."
./venv/bin/pip install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt 2>/dev/null

echo "[3/3] 启动服务器..."
echo ""
echo "  网址: http://localhost:5000"
echo "  API: http://localhost:5000/api/bypass"
echo "============================================"
echo ""

./venv/bin/python server.py 2>/dev/null || python3 server.py
