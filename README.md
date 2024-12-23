# 阿巴语言转换器 (Aba Language Converter)

一个将中文转换为阿巴语言（及反向转换）的图形界面工具。

## 功能特点

- 支持中文到阿巴语言的转换
- 支持阿巴语言到中文的转换
- 保留声调信息
- 考虑汉字结构
- 现代化的图形界面
- 内置编码对照表

## 安装说明

1. 确保已安装 Python 3.6 或更高版本
2. 克隆仓库：
```bash
git clone https://github.com/yourusername/aba-converter.git
cd aba-converter
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

运行程序：
```bash
python aba_gui.py
```

### 中文转阿巴语言
1. 在输入框中输入中文文本
2. 点击"转换为阿巴语言"按钮
3. 在输出框中查看转换结果

### 阿巴语言转中文
1. 在输入框中输入阿巴语言编码
2. 点击"转换为中文"按钮
3. 在输出框中查看转换结果

## 编码规则

### 声调表示
- 第一声：一个点 (.)
- 第二声：两个点 (..)
- 第三声：三个点 (...)
- 第四声：四个点 (....)

### 结构编码
- 独体字：阿
- 左右结构：阿巴
- 上下结构：巴阿
- 左中右结构：阿巴阿
- 上中下结构：巴阿巴
- 全包围结构：巴巴
等...

## 注意事项

1. 由于汉字博大精深，一个拼音可能对应多个汉字，转换回中文时可能与原文有所不同
2. 阿巴语言保留了声调信息，但在转换时可能因为多音字而产生歧义
3. 建议在使用时先尝试短句转换，理解转换规则后再尝试长句

## 开发说明

本项目使用 PyQt6 构建图形界面，使用 pypinyin 处理拼音转换，使用 Pinyin2Hanzi 进行拼音到汉字的转换。

### 主要依赖
- PyQt6: 图形界面框架
- pypinyin: 汉字转拼音
- Pinyin2Hanzi: 拼音转汉字

## License

MIT License

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 作者

[你的名字]