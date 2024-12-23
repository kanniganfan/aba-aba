import sys
import json
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QMessageBox, QTabWidget, QLineEdit)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
import pypinyin
sys.path.append('Pinyin2Hanzi-master')
from Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi import viterbi

class AbaConverter:
    # 字形结构映射
    STRUCTURE_TO_ABA = {
        '独体字': '阿',
        '左右结构': '阿巴',
        '上下结构': '巴阿',
        '左中右结构': '阿巴阿',
        '上中下结构': '巴阿巴',
        '全包围结构': '巴巴',
        '左包围': '阿阿巴',
        '右包围': '阿巴巴',
        '上包围': '巴阿阿',
        '下包围': '巴巴阿'
    }

    # 拼音字母到阿巴编码的映射
    PINYIN_TO_ABA = {
        'a': '阿',
        'b': '巴',
        'c': '阿巴',
        'd': '巴阿',
        'e': '阿阿',
        'f': '巴巴',
        'g': '阿阿巴',
        'h': '阿巴阿',
        'i': '巴阿阿',
        'j': '巴巴巴',
        'k': '阿阿阿',
        'l': '阿巴巴',
        'm': '巴阿巴',
        'n': '巴巴阿',
        'o': '阿阿阿阿',
        'p': '阿巴阿阿',
        'q': '阿巴巴阿',
        'r': '巴阿阿阿',
        's': '巴阿巴巴',
        't': '巴巴阿阿',
        'u': '巴巴巴巴',
        'ü': '阿阿阿巴',
        'v': '阿阿阿巴',  # v 作为 ü 的替代
        'w': '阿阿巴阿',
        'x': '阿阿巴巴',
        'y': '阿巴阿阿',
        'z': '阿巴阿巴'
    }

    # 创建反向映射
    ABA_TO_PINYIN = {v: k for k, v in PINYIN_TO_ABA.items()}

    def __init__(self):
        # 初始化 HMM 参数
        self.hmm_params = DefaultHmmParams()

    def get_character_structure(self, char):
        """获取汉字的结构（这里需要一个字形结构数据库，暂时返回默认值）"""
        return '独体字'

    def chinese_to_aba(self, text):
        """将中文转换为阿巴编码"""
        try:
            result = []
            for char in text:
                # 获取字形结构
                structure = self.get_character_structure(char)
                structure_code = self.STRUCTURE_TO_ABA[structure]
                
                # 获取拼音（带声调）
                pinyin = pypinyin.pinyin(char, style=pypinyin.Style.TONE3, heteronym=False)[0][0]
                
                # 分离声调
                tone = ''
                for i in range(5):
                    if str(i) in pinyin:
                        tone = str(i)
                        pinyin = pinyin.replace(str(i), '')
                        break
                
                # 转换每个字母到阿巴编码
                aba_parts = []
                main_vowel_found = False
                
                # 处理声母（如果是 zh, ch, sh）
                if pinyin.startswith(('zh', 'ch', 'sh')):
                    initial = pinyin[:2]
                    pinyin = pinyin[2:]
                    for letter in initial:
                        aba_parts.append(self.PINYIN_TO_ABA[letter])
                
                # 处理其他字母
                for letter in pinyin:
                    if letter in self.PINYIN_TO_ABA:
                        code = self.PINYIN_TO_ABA[letter]
                        # 如果是元音字母且还没有添加过声调
                        if letter in 'aeiouüv' and tone and not main_vowel_found:
                            code += '.' * int(tone)
                            main_vowel_found = True
                        aba_parts.append(code)
                
                # 组合编码
                full_code = f"{structure_code} {' '.join(aba_parts)}"
                result.append(full_code)
            
            return ' | '.join(result)
        except Exception as e:
            return f"转换错误: {str(e)}"

    def aba_to_chinese(self, aba_text):
        """从阿巴编码转换为中文"""
        try:
            # 从阿巴编码提取拼音
            pinyin_list = self.extract_pinyin_from_aba(aba_text)
            
            if not pinyin_list:
                return "无法识别的阿巴编码"
            
            # 去除声调数字
            clean_pinyin_list = [re.sub(r'\d', '', p) for p in pinyin_list]
            
            # 使用 viterbi 算法转换为汉字
            result = viterbi(self.hmm_params, observations=clean_pinyin_list, path_num=1)
            
            if not result:
                return "无法转换为汉字"
            
            # 返回最可能的结果
            return ''.join(result[0].path)
        except Exception as e:
            return f"转换错误: {str(e)}"

    def extract_pinyin_from_aba(self, aba_text):
        """从阿巴编码提取拼音"""
        try:
            # 按 | 分割每个字
            aba_chars = [x.strip() for x in aba_text.split('|') if x.strip()]
            pinyin_list = []
            
            for aba_char in aba_chars:
                # 分离字形结构和拼音编码
                parts = aba_char.strip().split()
                if len(parts) < 2:
                    continue
                    
                # 跳过第一个部分（结构编码）
                pinyin_parts = parts[1:]
                current_pinyin = ''
                tone = ''
                
                # 处理每个编码部分
                for part in pinyin_parts:
                    base_part = part
                    # 提取声调
                    if '....' in part:
                        tone = '4'
                        base_part = part.replace('....', '')
                    elif '...' in part:
                        tone = '3'
                        base_part = part.replace('...', '')
                    elif '..' in part:
                        tone = '2'
                        base_part = part.replace('..', '')
                    elif '.' in part:
                        tone = '1'
                        base_part = part.replace('.', '')
                    
                    # 查找对应的拼音字母
                    if base_part in self.ABA_TO_PINYIN:
                        current_pinyin += self.ABA_TO_PINYIN[base_part]
                
                if current_pinyin:
                    # 为第一个元音添加声调
                    if tone:
                        for i, char in enumerate(current_pinyin):
                            if char in 'aeiouüv':
                                current_pinyin = current_pinyin[:i+1] + tone + current_pinyin[i+1:]
                                break
                    pinyin_list.append(current_pinyin)
            
            return pinyin_list
        except Exception as e:
            print(f"解析错误: {str(e)}")
            return []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.converter = AbaConverter()
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('阿巴语言转换器')
        self.setMinimumSize(800, 600)
        
        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 添加转换标签页
        convert_tab = QWidget()
        convert_layout = QVBoxLayout(convert_tab)
        
        # 添加说明标签
        note_label = QLabel(
            "注意事项：\n"
            "1. 由于汉字博大精深，一个拼音可能对应多个汉字，转换回中文时可能与原文有所不同\n"
            "2. 阿巴语言保留了声调信息，但在转换时可能因为多音字而产生歧义\n"
            "3. 建议在使用时先尝试短句转换，理解转换规则后再尝试长句"
        )
        note_label.setStyleSheet("""
            QLabel {
                background-color: #FFF3CD;
                color: #856404;
                padding: 10px;
                border: 1px solid #FFEEBA;
                border-radius: 4px;
                margin: 5px;
            }
        """)
        note_label.setWordWrap(True)
        convert_layout.addWidget(note_label)
        
        # 输入区域
        input_label = QLabel('输入文本:')
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText('请输入要转换的文本...')
        convert_layout.addWidget(input_label)
        convert_layout.addWidget(self.input_text)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.to_aba_btn = QPushButton('转换为阿巴语言')
        self.to_chinese_btn = QPushButton('转换为中文')
        self.to_aba_btn.clicked.connect(self.to_aba)
        self.to_chinese_btn.clicked.connect(self.to_chinese)
        button_layout.addWidget(self.to_aba_btn)
        button_layout.addWidget(self.to_chinese_btn)
        convert_layout.addLayout(button_layout)
        
        # 输出区域
        output_label = QLabel('转换结果:')
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        convert_layout.addWidget(output_label)
        convert_layout.addWidget(self.output_text)
        
        # 添加标签页
        tab_widget.addTab(convert_tab, "转换")
        
        # 添加编码表标签页
        code_tab = QWidget()
        code_layout = QVBoxLayout(code_tab)
        code_text = QTextEdit()
        code_text.setReadOnly(True)
        code_text.setPlainText(self.get_code_table())
        code_layout.addWidget(code_text)
        tab_widget.addTab(code_tab, "编码表")
        
        # 将标签页添加到主布局
        layout.addWidget(tab_widget)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
        """)
        
    def to_aba(self):
        text = self.input_text.toPlainText().strip()
        if text:
            result = self.converter.chinese_to_aba(text)
            self.output_text.setPlainText(result)
        
    def to_chinese(self):
        text = self.input_text.toPlainText().strip()
        if text:
            result = self.converter.aba_to_chinese(text)
            self.output_text.setPlainText(result)
            
    def get_code_table(self):
        """返回格式化的编码表"""
        table = "拼音字母编码表：\n\n"
        table += "字母\t阿巴编码\n"
        table += "-" * 30 + "\n"
        
        for letter, code in self.converter.PINYIN_TO_ABA.items():
            table += f"{letter}\t{code}\n"
            
        table += "\n\n字形结构编码表：\n\n"
        table += "结构\t阿巴编码\n"
        table += "-" * 30 + "\n"
        
        for structure, code in self.converter.STRUCTURE_TO_ABA.items():
            table += f"{structure}\t{code}\n"
            
        return table

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
