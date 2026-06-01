# 单语言字幕转PDF工具

Single Language Subtitle to PDF Tool

一个用于提取单语言字幕文件（SRT/ASS/LRC/TXT）并转换为纯文本PDF的工具。

## 功能特点

- 支持多种文件格式：SRT、ASS、LRC、TXT
- 自动语言检测：英语、日语、中文
- 智能过滤：自动过滤元数据、特殊符号、箭头、音符等
- 双语字幕支持：将 `\N` 换行符替换为空格
- 多语言PDF生成：支持中文、日语、英语字体

## 安装依赖

```bash
pip install fpdf2
```

## 使用方法

```bash
python main.py
```

## 支持的文件格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| SRT字幕 | `.srt` | 标准字幕格式 |
| ASS字幕 | `.ass` | 高级字幕格式 |
| LRC歌词 | `.lrc` | 歌词文件格式 |
| 文本文件 | `.txt` | 纯文本文件 |

## 过滤内容

- 箭头符号：→ ← ↑ ↓ ➡ ⬅ ⬆ ⬇ 等
- 音符符号：♪ ♫ ♬ ♩
- 角括号：<< >> ≪ ≫
- 特殊符号：【】「」『』《》
- JSON元数据：{"t":0,"c":[...]}
- 音乐元数据：编曲、演唱、和声、作词等
- 字幕元数据：字幕、翻译、校对、时间轴等

## 项目结构

```
SingleLangSubtitlePDF/
├── main.py                    # 主启动文件
├── README.md                  # 项目说明文档
├── .gitignore                 # Git忽略配置
└── src/
    ├── config/
    │   └── settings.py        # 配置常量
    ├── parser/
    │   ├── subtitle_parser.py # 字幕解析（SRT/ASS/TXT）
    │   └── lrc_parser.py      # LRC歌词解析
    ├── pdf/
    │   └── generator.py       # PDF生成器
    └── ui/
        └── gui.py             # 图形界面
```

## 开发环境

- Python 3.8+
- fpdf2 2.7.0+
- Tkinter（Python内置）

## 许可证

MIT License