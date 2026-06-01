# 字幕解析模块
import os
import re
from src.config.settings import SUPPORTED_EXTENSIONS

# 元数据过滤关键字（使用集合去重）
METADATA_KEYWORDS = {
    '字幕', '翻译', '校对', '特效', '后期', '总监', 
    '压制', '时间轴', '轴', '双语合并', 'WEB版', '外挂字幕',
    'staff', 'STAFF', 'Staff', '制作',
    # 音乐相关元数据
    '编曲', '演唱', '和声', '作词', '作曲', '混音', '母带',
    '原唱', '翻唱', '吉他', '贝斯', '鼓', '钢琴',
    '制作人', '录音', '混音师', '出品', '发行', '版权'
}

def is_json_content(text):
    """检测是否是JSON格式的元数据内容"""
    if not text or not text.strip():
        return False
    
    text = text.strip()
    
    if text.startswith('{') and text.endswith('}'):
        return True
    
    if text.startswith('[') and text.endswith(']'):
        return True
    
    return False

# 需要移除的单字符符号映射表
SINGLE_CHAR_SYMBOLS = {
    # 箭头符号
    '→': '', '←': '', '↑': '', '↓': '',
    '⇒': '', '⇐': '',
    '➡': '', '⬅': '', '⬆': '', '⬇': '',
    '↗': '', '↙': '', '↔': '', '↕': '',
    # 音符符号
    '♪': '', '♫': '', '♬': '', '♩': '',
    # 角括号（Unicode）
    '≪': '', '≫': '',
    # 其他特殊符号
    '【': '', '】': '', '「': '', '」': '',
    '『': '', '』': '', '《': '', '》': '',
    '〈': '', '〉': '',
}

# 需要移除的多字符符号列表
MULTI_CHAR_SYMBOLS = [
    '<<', '>>', '<<<', '>>>'
]

def clean_text(text):
    """清理文本中的不必要符号和字符"""
    if not text:
        return text
    
    # 如果是JSON格式内容，直接返回空
    if is_json_content(text):
        return ""
    
    # 先处理多字符符号
    for symbol in MULTI_CHAR_SYMBOLS:
        text = text.replace(symbol, '')
    
    # 使用translate方法高效移除单字符符号
    text = text.translate(str.maketrans(SINGLE_CHAR_SYMBOLS))
    
    # 移除多余的空格和换行
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def parse_srt_to_text(srt_content):
    """解析SRT字幕文件，提取纯文本内容"""
    lines = srt_content.split('\n')
    result = []
    current_subtitle = []
    
    for line in lines:
        line = line.strip()
        # 跳过空行、纯数字行（序号）、时间码行
        if not line or line.isdigit() or ' --> ' in line or re.match(r'^\d{2}:\d{2}:\d{2}', line):
            if current_subtitle:
                result.append(' '.join(current_subtitle))
                current_subtitle = []
            continue
        
        current_subtitle.append(line)
    
    if current_subtitle:
        result.append(' '.join(current_subtitle))
    
    return '\n'.join(result)

def parse_ass_to_text(ass_content):
    """解析ASS字幕文件，提取纯文本内容"""
    lines = ass_content.split('\n')
    result = []
    in_events_section = False
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        if line.startswith('[Events]'):
            in_events_section = True
            continue
        
        if in_events_section and line.startswith('['):
            break
        
        if in_events_section and line.startswith('Dialogue:'):
            parts = line.split(',', 9)
            if len(parts) >= 10:
                text = re.sub(r'{[^}]*}', '', parts[9]).strip()
                # 将ASS换行符 \N 替换为空格（处理双语字幕）
                text = text.replace(r'\N', ' ').replace(r'\n', '\n').replace(r'\h', '').replace(r'\t', '\t')
                
                if text:
                    if is_metadata_line(text):
                        continue
                    result.append(text)
    
    return '\n'.join(result)

def read_file(file_path):
    """读取文件内容，支持多种编码格式"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"不支持的文件格式: {ext}。支持的格式: {SUPPORTED_EXTENSIONS}")
    
    encodings = ['utf-8', 'utf-16', 'gbk', 'gb2312', 'big5', 'utf-8-sig']
    
    content = None
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except (UnicodeDecodeError, LookupError):
            continue
    
    if content is None:
        raise ValueError(f"无法读取文件 {file_path}，尝试了以下编码: {encodings}")
    
    if ext.lower() == '.srt':
        content = parse_srt_to_text(content)
    
    if ext.lower() == '.ass':
        content = parse_ass_to_text(content)
    
    if ext.lower() == '.lrc':
        from .lrc_parser import parse_lrc_to_text
        content = parse_lrc_to_text(content)
    
    return content

def contains_chinese(text):
    """检测文本是否包含中文字符"""
    return any('\u4e00' <= c <= '\u9fff' for c in text)

def contains_japanese(text):
    """检测文本是否包含日文字符"""
    # 日文假名范围
    return any(
        ('\u3040' <= c <= '\u30ff') or  # 平假名和片假名
        ('\u4e00' <= c <= '\u9fff') or  # 汉字（日文中也使用）
        ('\u3400' <= c <= '\u4dbf') or  # 扩展A区汉字
        ('\u20000' <= c <= '\u2a6df')   # 扩展B区汉字
        for c in text
    )

def contains_english(text):
    """检测文本是否包含英文字符"""
    return any('a' <= c.lower() <= 'z' for c in text)

def detect_language(text):
    """检测文本语言类型"""
    has_chinese = contains_chinese(text)
    has_japanese = contains_japanese(text)
    has_english = contains_english(text)
    
    # 如果有日文特征（假名），返回日语
    if has_japanese:
        for c in text:
            if '\u3040' <= c <= '\u30ff':
                return 'japanese'
    
    # 如果有中文，返回中文
    if has_chinese:
        return 'chinese'
    
    # 如果只有英文，返回英语
    if has_english and not has_chinese and not has_japanese:
        return 'english'
    
    # 默认返回英文
    return 'english'

def is_metadata_line(line):
    """判断是否是元数据行（需要过滤）"""
    if not line or not line.strip():
        return True
    
    line = line.strip()
    
    if line.startswith('(') and line.endswith(')') and len(line) <= 20:
        return True
    
    if line.startswith('第') and '章' in line:
        return True
    
    # 检查是否以数字开头的列表项（如 "1. 编曲：xxx"）
    if re.match(r'^\d+[\.\-\)]\s*', line):
        # 提取数字后的内容
        content = re.sub(r'^\d+[\.\-\)]\s*', '', line)
        # 如果包含元数据关键字，整行过滤
        if any(keyword in content for keyword in METADATA_KEYWORDS):
            return True
    
    if any(keyword in line for keyword in METADATA_KEYWORDS):
        return True
    
    return False

def parse_subtitle_file(file_path):
    """解析字幕文件，返回纯文本行列表"""
    content = read_file(file_path)
    lines = content.strip().split('\n')
    
    result = []
    for line in lines:
        line = line.strip()
        if line and not is_metadata_line(line):
            # 清理文本中的不必要符号
            cleaned_line = clean_text(line)
            if cleaned_line:
                result.append(cleaned_line)
    
    return result

def validate_file_path(file_path):
    """验证文件路径"""
    if not file_path:
        return False
    
    if not os.path.isfile(file_path):
        return False
    
    _, ext = os.path.splitext(file_path)
    return ext.lower() in SUPPORTED_EXTENSIONS