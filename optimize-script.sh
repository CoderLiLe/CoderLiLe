#!/bin/bash
# GitHub 仓库优化脚本
# Usage: ./optimize-script.sh [--push]

set -euo pipefail

PUSH="${1:-}"

echo "🚀 开始优化 CoderLiLe/CoderLiLe 仓库..."

if [ ! -f "README.md" ]; then
    echo "❌ 错误：未找到 README.md 文件"
    exit 1
fi

cp README.md README.md.backup
trap 'rm -f README.md.backup' EXIT

echo "📝 运行 README 优化脚本..."
python3 optimize-readme.py

if git diff --quiet README.md; then
    echo "✅ README.md 已是最新状态，无需优化。"
    exit 0
fi

echo "📊 检测到 README.md 有变更："
git diff --stat README.md

git config --local user.email "liledeveloper@163.com" 2>/dev/null || true
git config --local user.name "LiLe" 2>/dev/null || true

TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
git add README.md optimize-readme.py optimize-script.sh
git commit -m "📈 优化 README（${TIMESTAMP}）

- 更新技能徽章分组
- 添加图片懒加载
- 更新最后修改时间"

echo "✅ 变更已提交到本地仓库。"

if [ "$PUSH" = "--push" ]; then
    echo "🚀 推送到 GitHub..."
    git push origin main
    echo "✅ 已成功推送到 GitHub！"
else
    echo "ℹ️  使用 --push 参数可自动推送到远程。"
fi
