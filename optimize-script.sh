#!/bin/bash
# GitHub 仓库优化脚本

set -euo pipefail

echo "🚀 开始优化 CoderLiLe/CoderLiLe 仓库..."

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误：未找到 README.md 文件"
    exit 1
fi

# 备份原始文件
cp README.md README.md.backup

# 运行 Python 优化脚本
echo "📝 运行 README 优化脚本..."
python3 optimize-readme.py

# 检查是否有变更
if git diff --quiet README.md; then
    echo "✅ README.md 已是最新状态，无需优化。"
else
    echo "📊 检测到 README.md 有变更："
    git diff --stat README.md
    
    # 配置 Git
    git config --local user.email "liledeveloper@163.com"
    git config --local user.name "LiLe"
    
    # 提交变更
    git add README.md
    git add .github/workflows/optimize-readme.yml
    git add .github/workflows/check-links.yml
    git add optimize-readme.py
    git add optimize-script.sh
    
    git commit -m "🚀 优化仓库：添加自动化工作流和 README 优化
    
    - 添加 README 优化脚本
    - 添加定期优化工作流
    - 添加链接检查工作流
    - 优化技能徽章分组
    - 更新最后修改时间"
    
    echo "✅ 变更已提交到本地仓库。"
    
    # 询问是否推送到远程
    echo ""
    echo "📤 是否推送到 GitHub 远程仓库？"
    echo "输入 'yes' 确认推送，其他任意键取消："
    read -r response
    
    if [ "$response" = "yes" ]; then
        echo "🚀 推送到 GitHub..."
        git push origin main
        echo "✅ 已成功推送到 GitHub！"
    else
        echo "⚠️  取消推送，变更仅保存在本地。"
    fi
fi

echo ""
echo "📋 优化完成总结："
echo "1. ✅ README.md 已优化（添加技能分组、图片懒加载等）"
echo "2. ✅ 添加了自动化优化工作流（每周运行）"
echo "3. ✅ 添加了链接检查工作流（每月运行）"
echo "4. ✅ 创建了优化脚本便于后续维护"
echo ""
echo "🔗 查看变更："
echo "  git log --oneline -5"
echo ""
echo "🔄 后续优化建议："
echo "1. 考虑添加更多项目展示"
echo "2. 优化统计卡片加载速度"
echo "3. 添加访客计数器"
echo "4. 集成更多开发工具徽章"