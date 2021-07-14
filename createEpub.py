# coding=UTF-8
# author : Konoha 2021年7月14日00:03:48
import os
import sys

import tkinter as tk
from tkinter import filedialog
import shutil
 
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.filePath = tk.StringVar()
        self.pack()
        self.create_widgets()
        
 
    def create_widgets(self):
        # 获取文件
        self.getFile_bt = tk.Button(self)
        self.getFile_bt['width'] = 15
        self.getFile_bt['height'] = 1
        self.getFile_bt["text"] = "打开"
        self.getFile_bt["command"] = self._getFile
        self.getFile_bt.pack(side="top")
        
        self.esc_bt = tk.Button(self)
        self.esc_bt['width'] = 15
        self.esc_bt['height'] = 1
        self.esc_bt["text"] = "关闭"
        self.esc_bt["command"] = super().quit
        self.esc_bt.pack(side="bottom")
 
        # 显示文件路径
        self.filePath_en = tk.Entry(self,  width = 140)
        self.filePath_en.pack(side="top")
 
        self.filePath_en.delete(0, "end")
        self.filePath_en.insert(0, "请选择文件")

        scrolly = tk.Scrollbar(self)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_en = tk.Listbox(self,yscrollcommand=scrolly.set,width = 120)
        self.listbox_en.pack(side=tk.LEFT, padx=5, pady=5)
        self.listbox_en.delete(0, "end")
        
        scrolly.config(command=self.listbox_en.yview)
        
        
        
 
 
    # 打开文件并显示路径
    def _getFile(self):
        default_dir = r"文件路径"
        self.filePath = tk.filedialog.askdirectory(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
        print(self.filePath)
        self.filePath_en.delete(0, "end")
        self.filePath_en.insert(0, self.filePath)
        self._createHTML()

    
    def _createHTML(self):
        folderName = str(self.filePath)
        if folderName == "":
            self.listbox_en.insert(tk.END,"该目录下没有文件!")
            return

        htmlFilePath = 'HTMLpage'
        if not os.path.exists(htmlFilePath):
            os.mkdir(htmlFilePath)
        else:
            shutil.rmtree(htmlFilePath)
            os.mkdir(htmlFilePath)

        fileNameList = os.listdir(folderName)
        count = 1
        for imgFileName in fileNameList:
            html_content = '''
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
\t<title>page_{}</title>
\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
\t<div>
\t\t<img src="../Images/{}" alt="Images to epub"/>
\t</div>       
</body>
</html>'''.format(count,imgFileName)  
            
            htmlFilename = 'HTMLpage/page{}.xhtml'.format(imgFileName)
            count += 1
            
            with open(htmlFilename,'w',encoding='utf-8') as file_object:
                file_object.write(html_content)
            self.listbox_en.insert(tk.END,htmlFilename+"生成成功")
 
root = tk.Tk()
root.title("creatEpubHTML")
root.geometry("800x400+300+300")
 
app =  Application(master=root)
app.mainloop()