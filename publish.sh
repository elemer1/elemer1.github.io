#!/bin/bash

# 自动发布脚本
# 双击或运行此脚本即可自动 push 所有更改到 GitHub

cd "$(dirname "$0")"

echo "======================================"
echo "  开始发布到 GitHub Pages"
echo "======================================"
echo ""

# 检查是否有更改
if [[ -z $(git status -s) ]]; then
    echo "✓ 没有需要发布的更改"
    echo ""
    echo "按任意键退出..."
    read -n 1
    exit 0
fi

# 显示更改的文件
echo "以下文件将被发布："
echo "--------------------------------------"
git status -s
echo "--------------------------------------"
echo ""

# 添加所有更改
echo "正在添加文件..."
git add .

# 提交更改（使用当前时间作为提交信息）
COMMIT_MSG="Update content - $(date '+%Y-%m-%d %H:%M:%S')"
echo "正在提交: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# 推送到 GitHub
echo "正在推送到 GitHub..."
git push

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "  ✓ 发布成功！"
    echo "======================================"
    echo ""
    echo "你的网站将在 1-2 分钟后更新"
    echo "访问: https://elemer1.github.io"
else
    echo ""
    echo "======================================"
    echo "  ✗ 发布失败"
    echo "======================================"
    echo ""
    echo "请检查网络连接或 Git 配置"
fi

echo ""
echo "按任意键退出..."
read -n 1
