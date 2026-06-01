# LRC歌词解析模块
import re
import os

# LRC时间戳格式正则表达式（支持1-3位小数）
LRC_TIMESTAMP_PATTERN = re.compile(r'\[(\d{2}):(\d{2})\.(\d{1,3})\]')

# LRC标签格式（如 [ti:歌曲名]）
LRC_TAG_PATTERN = re.compile(r'\[([a-zA-Z]+):(.+)\]')

def parse_lrc_to_text(lrc_content):
    """解析LRC歌词文件，提取纯文本内容"""
    lines = lrc_content.split('\n')
    result = []
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue
        
        # 跳过标签行（如 [ti:歌曲名]、[ar:歌手名]）
        if LRC_TAG_PATTERN.match(line):
            continue
        
        # 移除时间戳，提取歌词内容
        # 可能有多个时间戳，如 [00:01.00][00:02.00]歌词
        text = LRC_TIMESTAMP_PATTERN.sub('', line).strip()
        
        if text:
            result.append(text)
    
    return '\n'.join(result)

def read_lrc_file(file_path):
    """读取LRC文件内容"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
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
    
    return parse_lrc_to_text(content)

def extract_lrc_metadata(lrc_content):
    """提取LRC文件的元数据信息"""
    lines = lrc_content.split('\n')
    metadata = {}
    
    for line in lines:
        match = LRC_TAG_PATTERN.match(line)
        if match:
            key = match.group(1).lower()
            value = match.group(2).strip()
            metadata[key] = value
    
    return metadata

def parse_lrc_file(file_path):
    """解析LRC文件，返回歌词文本行列表"""
    content = read_lrc_file(file_path)
    lines = content.strip().split('\n')
    
    result = []
    for line in lines:
        line = line.strip()
        if line:
            result.append(line)
    
    return result