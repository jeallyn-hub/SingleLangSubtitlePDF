#!/usr/bin/env python3
# 打包脚本 - 将单语言字幕转PDF工具打包成exe

import os
import subprocess
import sys

def build_exe():
    """打包程序为exe文件"""
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=单语言字幕转PDF',
        '--add-data=src;src',
        '--hidden-import=fpdf',
        '--hidden-import=tkinter',
        'main.py'
    ]
    
    print("🚀 开始打包...")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 打包成功!")
        print(f"输出目录: dist/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败!")
        print(f"错误信息: {e.stderr}")
        return False

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build_exe()