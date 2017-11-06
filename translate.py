# coding=UTF-8

import os
import codecs
import shutil
import tkMessageBox
import Tkinter
import tkFileDialog
from Tkinter import *

FILE_CODING = "utf-8"  # 翻译文本编码格式(默认UTF-8)
ITEM_SEPARATOR = "\t"  # 列表间的分隔符
OUTPUT_FORMAT_IOS = "iOS"
OUTPUT_FORMAT_ANDROID = "Android"


class I18NTranslator:
    # 初始化
    def __init__(self):
        self.langls = []  # 语言的list
        self.infols = []  # 信息的list
        self.cur_dir = os.path.split(os.path.realpath(__file__))[0]  # 脚本当前的路径       

    # 解析txt文本
    def parse_txt_file(self, txt_fname):
        # 读取文本信息
        cwd = os.path.dirname(sys.argv[0])
        txt_fd = codecs.open(os.path.join(cwd, txt_fname), 'r', FILE_CODING)
        # 读取每一行的数据
        ls = [line.strip().encode(FILE_CODING) for line in txt_fd]
        txt_fd.close()

        # 对第一行的数据进行划分,获取语言列表
        self.langls = ls[0].split(ITEM_SEPARATOR)[1:]

        for i in range(len(self.langls)):
            if self.langls[i] == "中文":
                self.langls[i] = "zh"
            elif self.langls[i] == "英文":
                self.langls[i] = "en"
            elif self.langls[i] == "韩文":
                self.langls[i] = "ko"
            elif self.langls[i] == "日文":
                self.langls[i] = "ja"
            elif self.langls[i] == "俄语":
                self.langls[i] = "ru"
            elif self.langls[i] == "西班牙语":
                self.langls[i] = "es"

        for lang in self.langls:
            print("langls:{}".format(lang))

        null_ls = []
        # 对每一行的数据进行分割,将数据存入list(第一列为键,其他列为值)
        for i in ls[1:]:
            subls = i.split(ITEM_SEPARATOR)
            if subls[0] != "-":
                self.infols.append({"key": subls[0], "value": subls[1:]})
            else:
                null_ls.append({"key": subls[0], "value": subls[1:]})

    # 拼接字符生成xml文本(Android)
    def generate_xml(self, lang):
        stringls = []
        # 对应的语言索引位置
        langls_index = self.langls.index(lang)
        for info in self.infols:
            key = info["key"]
            try:
                value = info["value"][langls_index]
                # Android的单引号需要转义处理
                if "\'" in value:
                    value = value.replace("\'", "\\\'")
            except IndexError:  # 防止空列越界
                value = ""

            # 拼接每一行的文本
            str = "<string name=\"{k}\">{v}</string>\n".format(k=key, v=value)
            stringls.append(str)

        # 拼接字符串
        text = "<resources>\n\t" + "\t".join(stringls) + "</resources>\n"
        return text

    # 生成键值对的txt文本(iOS)
    def generate_txt(self, lang):
        stringls = []
        # 对应的语言索引位置
        langls_index = self.langls.index(lang)
        for info in self.infols:
            key = info["key"]
            try:
                value = info["value"][langls_index]
                # iOS的双引号需要转义处理
                if "\"" in value:
                    value = value.replace("\"", "\\\"")
            except IndexError:  # 防止空列越界
                value = ""

            # 拼接每一行的文本
            str = "\"{k}\" = \"{v}\";\n".format(k=key, v=value)
            stringls.append(str)

        # 拼接字符串
        text = "".join(stringls)
        return text

    # 按语言分别生成对应的翻译文本
    def build_translated_file(self, form):
        # 切换到脚本的路径
        os.chdir(self.cur_dir)        
        # 建立父文件夹,并切换到该目录下
        if form == OUTPUT_FORMAT_ANDROID:
            dir_path = os.path.join(self.cur_dir, OUTPUT_FORMAT_ANDROID)
        else:
            dir_path = os.path.join(self.cur_dir, OUTPUT_FORMAT_IOS)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        os.chdir(dir_path)

        # 移除子目录下所有的文件, 防止写入时发生冲突
        lsdir = os.listdir('.')
        for i in lsdir:
            try:
                # 删除时进行异常处理，防止崩溃（Mac下会自动生成.DS_Store文件）
                shutil.rmtree(i)
            except Exception as e:
                print(e)

        # 生成对应语言的文本
        for lang in self.langls:
            # # 生成根据后缀名生成相应格式的文本
            if form == OUTPUT_FORMAT_ANDROID:
                text = self.generate_xml(lang)
                dir_name = "values-" + lang
                file = "strings.xml"
            else:
                text = self.generate_txt(lang)
                dir_name = lang + ".lproj"
                file = "Localizable.strings"

            # 根据语言,建立相应的文件夹目录
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

            # 新建文本,并将数据写入
            txtfd = open(os.path.join(dir_name, file), 'w')
            txtfd.write(text)
            txtfd.close()


# 选择文件的图形界面
class SelectFileDialog(Tkinter.Frame):
    def __init__(self, root):
        self.file_path = ""  # 文件路径
        self.path_text = StringVar()  # 路径显示文本
        # 定义文件操作的相关属性
        self.file_opt = options = {}
        options['parent'] = root
        options['defaultextension'] = '.txt'  # 限制只能选择txt文本
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]  # 文本选择类型
        options['initialdir'] = '.'  # 默认当前目录
        options['initialfile'] = 'example.txt'  # 默认选中的文件
        options['title'] = 'Please select a document'

        # 初始化窗口
        Tkinter.Frame.__init__(self, root)
        root.title("Multinational Translation Generator")

        # 添加一个label、entry、button到fileFrame中
        fileFrame = Frame(root)
        fileFrame.pack()
        label = Label(fileFrame, text="path:")
        tvPath = Entry(fileFrame, textvariable=self.path_text)
        btnGetPath = Button(fileFrame, text="select", command=self.select_file)
        label.grid(row=1, column=1)
        tvPath.grid(row=1, column=2)
        btnGetPath.grid(row=1, column=3)

        # 添加两个多选按钮到formatFrame
        formatFrame = Frame(root)
        formatFrame.pack()
        self.value_ios = IntVar()
        self.value_android = IntVar()
        self.value_ios.set(1)
        self.value_android.set(1)
        tvOutput = Label(formatFrame, text="Output Format：")
        cbIOS = Checkbutton(formatFrame, text=OUTPUT_FORMAT_IOS, variable=self.value_ios)
        cbAndroid = Checkbutton(formatFrame, text=OUTPUT_FORMAT_ANDROID, variable=self.value_android)
        # 使用网格管理器排列按钮
        tvOutput.grid(row=1, column=1)
        cbIOS.grid(row=1, column=2)
        cbAndroid.grid(row=1, column=3)

        # 创建Start按钮
        Tkinter.Button(self, text='Start', command=self.begin_transform).pack()

    # 获取文件路径
    def select_file(self):
        self.file_path = tkFileDialog.askopenfilename(**self.file_opt)
        self.path_text.set(self.file_path)

    # 开始转换
    def begin_transform(self):
        if self.file_path:
            opt_ios = self.value_ios.get() == 1
            opt_android = self.value_android.get() == 1
            if opt_ios or opt_android:
                translator = I18NTranslator()
                translator.parse_txt_file(self.file_path)
                # 根据选择的格式进行输出
                if opt_ios:
                    translator.build_translated_file(OUTPUT_FORMAT_IOS)
                    print("iOS Finish")
                if opt_android:
                    translator.build_translated_file(OUTPUT_FORMAT_ANDROID)
                    print("Android Finish")
                # 完成提示
                title = "Message"
                tips_string = "Translation Done"
                tkMessageBox.showinfo(title=title, message=tips_string)
        else:
            title = "Error"
            tips_string = "The file path cannot be empty"
            tkMessageBox.showerror(title=title, message=tips_string)


if __name__ == '__main__':
    root = Tkinter.Tk()
    SelectFileDialog(root).pack()
    root.mainloop()
