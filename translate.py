# coding=UTF-8

import Tkinter, Tkconstants, tkFileDialog
import ttk

import sys
import os
import re
import codecs
import shutil
import tkMessageBox
from Tkinter import *
from xml.dom.minidom import Document

FILE_CODING = "utf-8"  # 翻译文本编码格式(默认UTF-8)
ITEM_SEPARATOR = "\t"  # 列表间的分隔符
OUTPUT_FORMAT_IOS = "iOS"
OUTPUT_FORMAT_ANDROID = "Android"


class unicodetxt_to_formattxt_obj:
    # 初始化
    def __init__(self):
        self.langls = []  # 语言的list
        self.infols = []  # 信息的list

    # 解析txt文本
    def parse_txt_file(self, txt_fname):
        # 读取文本信息
        cwd = os.path.dirname(sys.argv[0])
        self.txt_fd = codecs.open(os.path.join(cwd, txt_fname), 'r', FILE_CODING)

        # 读取每一行的数据
        ls = [line.strip().encode(FILE_CODING) for line in self.txt_fd]
        self.txt_fd.close()

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

                # for i in null_ls:
                #     self.infols.append(i)

    # 使用库生成xml文本(Android)
    def generate_xml_with_lib(self, lang):
        # 新建xml文档
        doc = Document()
        resources = doc.createElement("resources")
        doc.appendChild(resources)

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

            stringele = doc.createElement("string")  # 添加元素
            stringele.setAttribute("name", key)  # 添加并设置属性
            text_node = doc.createTextNode(value)  # 生成节点字符串
            stringele.appendChild(text_node)  # 添加文本节点
            resources.appendChild(stringele)  # 在xml中添加此行数据

        # 拼接字符串
        uglyXml = doc.toprettyxml(indent='  ')
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        prettyXml = text_re.sub('>\g<1></', uglyXml)
        return prettyXml

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
        # 获取当前路径
        dir = os.path.split(os.path.realpath(__file__))[0]
        # 建立父文件夹,并切换到该目录下
        if form == OUTPUT_FORMAT_ANDROID:
            dir_path = os.path.join(dir, OUTPUT_FORMAT_ANDROID)
        else:
            dir_path = os.path.join(dir, OUTPUT_FORMAT_IOS)
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
class TkFileDialogExample(Tkinter.Frame):
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

        # 添加一个label、entry、button到frame中
        fileFrame = Frame(root)
        fileFrame.pack()
        label = Label(fileFrame, text="path:")
        tvPath = Entry(fileFrame, textvariable=self.path_text)
        btnGetPath = Button(fileFrame, text="select", command=self.select_file)
        label.grid(row=1, column=1)
        tvPath.grid(row=1, column=2)
        btnGetPath.grid(row=1, column=3)

        # 添加一个多选按钮和单选按钮到frame1
        frame1 = Frame(root)
        frame1.pack()  # 看下面的解释（包管理器）
        self.value_ios = IntVar()
        self.value_android = IntVar()
        self.value_ios.set(1)
        self.value_android.set(1)
        tvOutput = Label(frame1, text="Output Format：")
        cbIOS = Checkbutton(frame1, text=OUTPUT_FORMAT_IOS, variable=self.value_ios)
        cbAndroid = Checkbutton(frame1, text=OUTPUT_FORMAT_ANDROID, variable=self.value_android)
        # 将cbtBold排列在frame1的网格第一行第一列（网格管理器也会在下面有解释）
        tvOutput.grid(row=1, column=1)
        cbIOS.grid(row=1, column=2)
        cbAndroid.grid(row=1, column=3)

        # 创建按钮(text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数)
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        Tkinter.Button(self, text='Start', command=self.begin_transform).pack(**button_opt)

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
                obj = unicodetxt_to_formattxt_obj()
                obj.parse_txt_file(self.file_path)
                # 根据选择的格式进行输出
                if opt_ios:
                    obj.build_translated_file(OUTPUT_FORMAT_IOS)
                    print("iOS Finish")
                if opt_android:
                    obj.build_translated_file(OUTPUT_FORMAT_ANDROID)
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
    TkFileDialogExample(root).pack()
    root.mainloop()
