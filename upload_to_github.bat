@echo off
chcp 65001
echo ================================================
echo         单语言字幕转PDF工具 - GitHub上传脚本
echo ================================================
echo.
echo 使用说明：
echo 1. 在GitHub上创建仓库后获取仓库地址
echo 2. 将下方的REPO_URL替换为你的仓库地址
echo 3. 运行此脚本上传代码
echo.

set "REPO_URL=你的GitHub仓库地址"

echo 初始化Git仓库...
git init

echo 添加文件...
git add .

echo 提交代码...
git commit -m "Initial commit - 单语言字幕转PDF工具"

echo 添加远程仓库...
git remote add origin %REPO_URL%

echo 推送到GitHub...
git push -u origin main

echo.
echo 上传完成！
pause