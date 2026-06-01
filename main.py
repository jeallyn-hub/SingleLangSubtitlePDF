# 主启动文件
import sys
import os

def check_dependencies():
    """检查依赖是否安装"""
    try:
        from fpdf import FPDF
        return True
    except ImportError:
        return False

def main():
    """主函数"""
    print("="*60)
    print("    单语言字幕转PDF工具 v1.0.0")
    print("    Single Language Subtitle to PDF")
    print("="*60)
    
    if not check_dependencies():
        print("❌ 缺少依赖库 fpdf2")
        print("请运行: pip install fpdf2")
        input("按 Enter 键退出...")
        sys.exit(1)
    
    try:
        import tkinter as tk
        from src.ui.gui import SingleLangPDFGUI
        print("🚀 正在启动可视化界面...")
        root = tk.Tk()
        app = SingleLangPDFGUI(root)
        root.mainloop()
    except ImportError as e:
        print(f"❌ 无法启动GUI: {e}")
        input("按 Enter 键退出...")

if __name__ == "__main__":
    main()