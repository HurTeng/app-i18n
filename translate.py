#coding=UTF-8

import Tkinter, Tkconstants, tkFileDialog
import ttk

from format import unicodetxt_to_formattxt_obj

TEXT_FILE_NAME = "strings.xml"
TEXT_FILE_DIR_PREFIX = "values-"

class TkFileDialogExample(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)

        # 添加标题
        root.title("多语言翻译自动生成器")

        # 下拉选择框
        lable = ttk.Label(root, text="请选择输出格式:")
        lable.pack()  # pack()方法把Widget加入到父容器中，并实现布局

        variable = Tkinter.StringVar(root)
        formatChosen = ttk.Combobox(root, textvariable=variable, state='readonly')
        formatChosen['values'] = ("xml", "txt")  # 设置下拉列表的值
        formatChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
        formatChosen.pack()
        self.formatChosen = formatChosen

        # 创建按钮(text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数)
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}
        Tkinter.Button(self, text='选择源文件', command=self.select_file).pack(**button_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

        # This is only available on the Macintosh, and only when Navigation Services are installed.
        #options['message'] = 'message'

        # if you use the multiple file version of the module functions this option is set automatically.
        #options['multiple'] = 1

        # defining options for opening a directory
        self.dir_opt = options = {}
        options['initialdir'] = 'C:\\'
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'

    def select_file(self):
        # 获取文件路径
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        if filename:
            obj = unicodetxt_to_formattxt_obj()
            obj.parse_txt_file(filename)
            form = self.formatChosen.get()  # 生成的文件格式
            obj.build_xml_file(form)



if __name__ == '__main__':
    root = Tkinter.Tk()
    TkFileDialogExample(root).pack()
    root.mainloop()
