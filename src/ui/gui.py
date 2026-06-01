# 图形界面模块
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from src.parser.subtitle_parser import parse_subtitle_file, detect_language, validate_file_path
from src.pdf.generator import create_single_lang_pdf
from src.config.settings import SUPPORTED_EXTENSIONS, OUTPUT_DIR

class SingleLangPDFGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("单语言字幕转PDF工具")
        self.root.geometry("900x600")
        
        self.source_file = tk.StringVar()
        self.language = tk.StringVar(value="english")
        self.preview_text_var = tk.StringVar()
        self.parsed_lines = []
        
        self.document_title = tk.StringVar(value="字幕文档")
        self.output_filename = tk.StringVar()
        
        self.create_widgets()
    
    def _browse_file(self, var):
        """通用文件浏览方法"""
        filename = filedialog.askopenfilename(
            title="选择字幕文件",
            filetypes=[
                ("所有支持的文件", "*.srt *.ass *.txt *.lrc"),
                ("SRT字幕", "*.srt"),
                ("ASS字幕", "*.ass"),
                ("LRC歌词", "*.lrc"),
                ("文本文件", "*.txt")
            ]
        )
        if filename:
            var.set(filename)
            
            base_name = os.path.splitext(os.path.basename(filename))[0]
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.lrc':
                self.output_filename.set(f"{base_name}_歌词")
            else:
                self.output_filename.set(f"{base_name}_字幕")
            
            try:
                content = parse_subtitle_file(filename)
                if content:
                    detected_lang = detect_language('\n'.join(content))
                    self.language.set(detected_lang)
            except Exception as e:
                messagebox.showwarning("警告", f"检测语言失败: {str(e)}")
    
    def browse_source_file(self):
        """浏览字幕文件"""
        self._browse_file(self.source_file)
    
    def open_output_dir(self):
        """打开输出目录"""
        if os.path.exists(OUTPUT_DIR):
            os.startfile(OUTPUT_DIR)
        else:
            messagebox.showwarning("警告", "输出目录不存在")
    
    def preview_content(self):
        """预览内容"""
        try:
            file_path = self.source_file.get()
            if not file_path:
                messagebox.showwarning("警告", "请选择字幕文件")
                return
            
            self.parsed_lines = parse_subtitle_file(file_path)
            
            self._display_preview()
            
        except Exception as e:
            messagebox.showerror("错误", f"解析失败: {str(e)}")
    
    def _display_preview(self):
        """显示预览内容"""
        if not self.parsed_lines:
            self.preview_text_var.set("未解析到任何内容")
            self._update_preview_text()
            return
        
        preview_lines = []
        for i, line in enumerate(self.parsed_lines[:10], 1):
            preview_lines.append(f"{i}. {line}")
        
        preview_lines.append(f"\n共解析到 {len(self.parsed_lines)} 条内容")
        self.preview_text_var.set("\n".join(preview_lines))
        self._update_preview_text()
    
    def generate_pdf(self):
        """生成PDF"""
        if not self.parsed_lines:
            messagebox.showwarning("警告", "请先预览内容")
            return
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        try:
            output_name = self.output_filename.get().strip()
            if not output_name:
                base_name = os.path.splitext(os.path.basename(self.source_file.get()))[0]
                output_name = f"{base_name}_字幕"
            
            doc_title = self.document_title.get().strip()
            lang = self.language.get()
            
            output_path = create_single_lang_pdf(
                self.parsed_lines, 
                output_name + ".pdf", 
                doc_title,
                lang
            )
            messagebox.showinfo("成功", f"PDF已生成！\n\n{output_path}")
            
            os.startfile(OUTPUT_DIR)
        except Exception as e:
            messagebox.showerror("错误", f"生成PDF失败: {str(e)}")
    
    def create_widgets(self):
        """创建界面组件"""
        self.create_file_selection()
        self.create_language_selection()
        self.create_document_settings()
        self.create_preview_area()
        self.create_button_area()
    
    def create_file_selection(self):
        """创建文件选择区域"""
        file_frame = ttk.LabelFrame(self.root, text="文件选择")
        file_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="we")
        
        ttk.Label(file_frame, text="字幕文件：").grid(row=0, column=0, sticky="w", padx=10)
        
        self.source_entry = ttk.Entry(file_frame, textvariable=self.source_file, width=50)
        self.source_entry.grid(row=0, column=1, pady=5, sticky="we", padx=5)
        
        self.browse_source_button = ttk.Button(file_frame, text="浏览", command=self.browse_source_file)
        self.browse_source_button.grid(row=0, column=2, pady=5, padx=5)
    
    def create_language_selection(self):
        """创建语言选择区域"""
        lang_frame = ttk.LabelFrame(self.root, text="语言设置")
        lang_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="we")
        
        ttk.Label(lang_frame, text="目标语言：").grid(row=0, column=0, sticky="w", padx=10)
        
        ttk.Radiobutton(lang_frame, text="英语", variable=self.language, value="english").grid(row=0, column=1, padx=10)
        ttk.Radiobutton(lang_frame, text="日语", variable=self.language, value="japanese").grid(row=0, column=2, padx=10)
        ttk.Radiobutton(lang_frame, text="中文", variable=self.language, value="chinese").grid(row=0, column=3, padx=10)
    
    def create_document_settings(self):
        """创建文档设置区域"""
        settings_frame = ttk.LabelFrame(self.root, text="文档设置")
        settings_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="we")
        
        ttk.Label(settings_frame, text="文档标题：").grid(row=0, column=0, padx=10, sticky="w")
        self.title_entry = ttk.Entry(settings_frame, textvariable=self.document_title, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="输出文件名：").grid(row=1, column=0, padx=10, sticky="w")
        self.filename_entry = ttk.Entry(settings_frame, textvariable=self.output_filename, width=40)
        self.filename_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(settings_frame, text=".pdf").grid(row=1, column=2, padx=5)
    
    def create_preview_area(self):
        """创建预览区域"""
        preview_frame = ttk.LabelFrame(self.root, text="内容预览")
        preview_frame.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        self.preview_text = tk.Text(preview_frame, wrap="word", height=15)
        self.preview_text.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(preview_frame, command=self.preview_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.preview_text.config(yscrollcommand=scrollbar.set)
        
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        self.preview_text_var.trace("w", lambda *args: self._update_preview_text())
    
    def _update_preview_text(self):
        """更新预览文本框内容"""
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, self.preview_text_var.get())
    
    def create_button_area(self):
        """创建按钮区域"""
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="预览内容", command=self.preview_content).pack(side="left", padx=10)
        ttk.Button(button_frame, text="生成PDF", command=self.generate_pdf).pack(side="left", padx=10)
        ttk.Button(button_frame, text="打开输出目录", command=self.open_output_dir).pack(side="left", padx=10)