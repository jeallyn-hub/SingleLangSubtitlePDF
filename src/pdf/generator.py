# PDF生成模块
from fpdf import FPDF
from src.config.settings import *
import os

class SingleLangPDF(FPDF):
    def __init__(self, title="字幕文档", language='english'):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=MARGIN_BOTTOM)
        self.title = title
        self.language = language
        self._setup_font()
    
    def _setup_font(self):
        """设置字体 - 支持英语、日语和中文"""
        self.chinese_font_available = False
        self.japanese_font_available = False
        
        font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simhei.ttf')
        if os.path.exists(font_path):
            try:
                self.add_font('SimHei', '', font_path)
                self.chinese_font_available = True
            except Exception:
                pass
        
        font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'msgothic.ttc')
        if os.path.exists(font_path):
            try:
                self.add_font('MS Gothic', '', font_path)
                self.japanese_font_available = True
            except Exception:
                pass
    
    def _set_font(self, size=FONT_SIZE_NORMAL, style=''):
        """统一设置字体"""
        if self.language == 'japanese' and self.japanese_font_available:
            self.set_font('MS Gothic', '', size)
        elif self.chinese_font_available:
            self.set_font('SimHei', '', size)
        else:
            self.set_font(PDF_FONT, style, size)
    
    def header(self):
        """页头设计"""
        self._set_font(FONT_SIZE_TITLE, 'B')
        self.set_text_color(*COLOR_BLACK)
        self.cell(0, 10, self.title, 0, 1, 'C')
        self.ln(5)
        
        self.set_draw_color(*COLOR_GRAY)
        self.line(MARGIN_LEFT, self.get_y(), PDF_PAGE_WIDTH - MARGIN_RIGHT, self.get_y())
        self.ln(10)
    
    def footer(self):
        """页脚设计"""
        self.set_y(-15)
        # 使用支持中文的字体确保"页"字能正确显示
        if self.chinese_font_available:
            self.set_font('SimHei', '', FONT_SIZE_SMALL)
        else:
            self.set_font(PDF_FONT, '', FONT_SIZE_SMALL)
        self.set_text_color(*COLOR_GRAY)
        self.cell(0, 10, f'第 {self.page_no()} 页', 0, 0, 'C')
    
    def add_text_line(self, text, line_number=None):
        """添加一行文本内容"""
        self._set_font(FONT_SIZE_NORMAL)
        
        text_width = self.get_string_width(text)
        max_width = PDF_PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
        
        if text_width > max_width:
            lines = []
            current_line = ""
            words = text.split()
            
            for word in words:
                temp = current_line + (" " if current_line else "") + word
                if self.get_string_width(temp) <= max_width:
                    current_line = temp
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
        else:
            lines = [text]
        
        for line in lines:
            if line_number:
                self.cell(20, 8, str(line_number), 0, 0, 'R')
                self.cell(5, 8, '', 0, 0)
                self.cell(0, 8, line, 0, 1)
            else:
                self.cell(0, 8, line, 0, 1)
    
    def generate_pdf(self, text_lines, output_filename=None):
        """生成单语言PDF"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        output_path = os.path.join(OUTPUT_DIR, output_filename or DEFAULT_OUTPUT_FILENAME)
        
        self.add_page()
        
        for line in text_lines:
            if self.get_y() > PDF_PAGE_HEIGHT - MARGIN_BOTTOM - 20:
                self.add_page()
            
            self.add_text_line(line)
            self.ln(2)
        
        # 尝试输出PDF，处理权限问题
        try:
            self.output(output_path)
        except PermissionError:
            # 尝试添加时间戳避免文件名冲突
            import time
            name, ext = os.path.splitext(output_path)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"{name}_{timestamp}{ext}"
            self.output(output_path)
        
        return output_path

def create_single_lang_pdf(text_lines, output_filename=None, title=None, language='english'):
    """创建单语言PDF的便捷函数"""
    pdf_title = title if title else PDF_TITLE
    pdf = SingleLangPDF(title=pdf_title, language=language)
    return pdf.generate_pdf(text_lines, output_filename)