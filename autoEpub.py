import os
import shutil

import tkinter as tk
from tkinter import filedialog

import random
import _thread

import time
from PIL import Image



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.protocol("WM_DELETE_WINDOW", self.beforeQuit)
        self.master = master
        self.img_directory = ""
        self.pack()        
        self.create_widgets()
        
        self.uuid = ""
        self.coverImgName = ""


        self.OEBPS_dir = r"temp/OEBPS/"
        self.Images_dir = r"temp/OEBPS/Images/"
        self.Text_dir = r"temp/OEBPS/Text/"


        # self.initNewBook()

    def initNewBook(self):
        self.NCX = ""

        self.TOC = '''<?xml version="1.0"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
\t<title>Table of Contents</title>
\t<link href="../Styles/sgc-toc.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="sgc-toc-title">Table of Contents</div>
'''


        self.opfHead = ""

        self.manifest = '''  <manifest>
\t<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
\t<item id="cover.xhtml" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>
\t<item id="sgc-toc.css" href="Styles/sgc-toc.css" media-type="text/css"/>
\t<item id="TOC.xhtml" href="Text/TOC.xhtml" media-type="application/xhtml+xml"/>

'''

        self.spine = '''  <spine toc="ncx">
\t<itemref idref="cover.xhtml"/>
\t<itemref idref="TOC.xhtml"/>
'''

    def create_widgets(self):

        self.mode = tk.IntVar()
        self.rb_anthology = tk.Radiobutton(self,text="anthology",value=1,variable=self.mode)
        self.rb_anthology.pack(side="top")
        self.rb_offprint = tk.Radiobutton(self,text="offprint",value=2,variable=self.mode,command = self.offprintMode)
        self.rb_offprint.pack(side="top")
        self.mode.set(1)
        # print(self.ao_flag.get())#1

        # 获取文件
        self.bt_chooseBookDir = tk.Button(self,font=('JetBrains Mono', 12))
        self.bt_chooseBookDir['width'] = 20
        self.bt_chooseBookDir['height'] = 1
        self.bt_chooseBookDir["text"] = "chooseBook"
        self.bt_chooseBookDir["command"] = self.getImgDirectory
        self.bt_chooseBookDir.pack(side="top") 
        
      
      
        self.label_title = tk.Label(self,text="title",anchor="w",width=55,font=('Hiragino Sans GB W3', 10)).pack()
        self.et_title=tk.Entry(self,show=None, width=40,font=('Hiragino Sans GB W3', 12))
        self.et_title.pack()
        self.et_title.insert(0,"アンソロジー")

        self.label_creator = tk.Label(self,text="creator",anchor="w",width=55,font=('Hiragino Sans GB W3', 10)).pack()
        self.et_creator=tk.Entry(self,show=None, width=40,font=('Hiragino Sans GB W3', 12))
        self.et_creator.pack()
        self.et_creator.insert(0,"KOH")

        self.label_language = tk.Label(self,text="language",anchor="w",width=55,font=('Hiragino Sans GB W3', 10)).pack()
        self.et_language=tk.Entry(self,show=None, width=40,font=('Hiragino Sans GB W3', 12))
        self.et_language.pack()
        self.et_language.insert(0,"ja")

        self.label_date = tk.Label(self,text="date",anchor="w",width=55,font=('Hiragino Sans GB W3', 10)).pack()
        self.et_date=tk.Entry(self,show=None, width=40,font=('Hiragino Sans GB W3', 12))
        self.et_date.pack()
        self.et_date.insert(0,time.strftime("%Y-%m-%d", time.localtime()))

      
        self.bt_chooseCover = tk.Button(self,text="ChooseCover",font=('JetBrains Mono', 12),width=20,height=1,command=self.chooseCover).pack(side="bottom")
        
    def offprintMode(self):
      self.rb_anthology.config(state=tk.DISABLED)
      self.rb_offprint.config(state=tk.DISABLED)

      self.master.geometry("%dx%d+%d+0" %(self.master.winfo_screenwidth()/2,self.master.winfo_screenheight(),self.master.winfo_screenwidth()/2))
      
      self.count = -1

      self.chap_NO = tk.IntVar()
      self.chap_NO.set(-1)

      self.chapterList = []
      self.cptIndexRbtList = []
      self.ncx_chapContent = []
      self.toc_chapContent = []

      #add new chapter button
      self.bt_chooseChapterIndex = tk.Button(self,text="appendChapter",font=('JetBrains Mono', 12),width=20,height=1,command=self.addChapter).pack()
      
      #为空时为空字符
      for i in range(6):
        self.addChapter()
        
    def addChapter(self):
      
      if self.count==-1:
        self.count += 1
        self.chapterList.append(tk.Entry(self,show=None,width=40,font=('Hiragino Sans GB W3', 12),\
          validate="focusout",validatecommand=self.recursion))    
        self.chapterList[self.count].pack()
        self.chapterList[self.count].insert(0,"その%d" % (self.count+1))
      else:
        self.count += 1
        self.chapterList.append(tk.Entry(self,show=None, width=40,font=('Hiragino Sans GB W3', 12)))    
        self.chapterList[self.count].pack()
        self.chapterList[self.count].insert(0,"その%d" % (self.getNextNO()))

      
      self.cptIndexRbtList.append(tk.Radiobutton(self,text="choose%d" % (self.count+1),variable = self.chap_NO,value=self.count,\
        indicatoron=False,anchor="w",width=43,font=('Hiragino Sans GB W3', 12),\
        command=lambda:self.chooseChapter(self.chap_NO.get())))
      self.cptIndexRbtList[self.count].pack()
      

      self.ncx_chapContent.append("")
      self.toc_chapContent.append("")

      if self.count >= 8:
        for eachChapter,eachIndex in zip(self.chapterList,self.cptIndexRbtList):
          eachChapter.config(font=('Hiragino Sans GB W3', 8))
          eachIndex.config(font=('Hiragino Sans GB W3', 8))

    def recursion(self):
      
      chapStr = self.chapterList[0].get()
    
      try:
        if len(chapStr) <= 5 and chapStr[:2] == "その":
          NO = int(chapStr[2:])
          for each in self.chapterList[1:] :
            NO += 1
            each.delete(0, 'end')
            each.insert(0,"その%d" %(NO))
      except BaseException as e:
        print(e)
      finally:
        return True
          
    def getNextNO(self):
      lastNO = self.chapterList[self.count-1].get()
      if lastNO[:2] == "その":
        return int(lastNO[2:])+1
      else:
        return self.count+1

    def getImgDirectory(self):
       
        self.initNewBook()

        if self.img_directory != "" :
          initdir = os.path.dirname(self.img_directory)
          self.img_directory = str(tk.filedialog.askdirectory(title=u'选择文件',initialdir=os.path.normpath(initdir)))
        else:
          self.img_directory = str(tk.filedialog.askdirectory(title=u'选择文件'))

        if self.img_directory == "":
            return               
        
        print("getDirectory: "+self.img_directory)
        if self.mode.get() == 2:
          self.et_title.delete(0,'end')
          self.et_creator.delete(0,'end')
          self.et_title.insert(0,self.img_directory[self.img_directory.rfind("/")+1:])
          self.et_creator.insert(0,"Konoha")
        #生成目录结构，复制两个固定文件
        _thread.start_new_thread(self.createDirectoryTree,())
        # self.createDirectoryTree()

    def createDirectoryTree(self):
        #获取uuid
        self.uuid = self.createUUID()
        
        if os.path.exists("temp/"):
            # shutil.rmtree("temp/")
            os.system("rmdir /s/q temp")
        #     print("temp目录已存在")
        #     return
        # else:
        #     os.mkdir("temp/")

        #这个复制的时候会自动生成目录
        # shutil.copytree("resources/","temp/")
        os.system("xcopy /ei resources temp")
        print(">>>epub框架部署完毕")

        # shutil.copytree(self.img_directory,self.Images_dir)
        os.system('copy "{}" temp\\OEBPS\\Images'.format(self.img_directory.replace("/","\\")))
        print(">>>图片文件导入完毕")

        self.createXHTML()
        print(">>>opf_ncx构建完毕")
    

    def createUUID(self) -> str:
        #UUID样例urn:uuid:7f9dda2f-ec04-4309-a7d8-3eb7e0c609c8
        #8-4-4-4-12

        strSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        p1 = ''.join(random.sample(strSet,8))
        p2 = ''.join(random.sample(strSet,4))
        p3 = ''.join(random.sample(strSet,4))
        p4 = ''.join(random.sample(strSet,4))
        p5 = ''.join(random.sample(strSet,12))
        return "{}-{}-{}-{}-{}".format(p1,p2,p3,p4,p5)




    def createXHTML(self):
        postfix = '1001'
        count = 0      
        count_chapters = 1
        newfilename = ""

        #初始化NCX
        self.NCX = '''<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd"><ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
  <head>
    <meta content="urn:uuid:{uuid}" name="dtb:uid"/>
    <meta content="0" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>Unknown</text>
  </docTitle>
  <navMap>

'''.format(uuid = self.uuid)

        #遍历图片文件夹
        for img in os.listdir(self.Images_dir):
            # print(choice_file[-8:])            
            #如果是每个本子的第一页，那么就为其生成目录

            if self.mode.get() == 2:
              newfilename = img

            elif postfix == img[-8:-4]:           
                #1 提取章节名，不要文件1001.jpg的后缀
                chapter = img[:-8]

                #2 目录计数器+1，代表进入了一个新的章节，重命名，并保留新名字
                count += 1
                newfilename = str(count*1000)+img[-8:]
                os.rename(self.Images_dir + img , self.Images_dir+newfilename)#加上原来的后缀名
                # print(img+"----->"+newfilename)  

                #3 用新名字，章节名，生成目录、TOC目录
                self.NCX += '''    <navPoint id="navPoint-{count}" playOrder="{count}">
      <navLabel>
        <text>{chapter}</text>
      </navLabel>
      <content src="Text/page{fileName}.xhtml"/>
    </navPoint>

'''.format(count = count,chapter=chapter,fileName = newfilename)
                
                #TOC目录
                self.TOC += '''<div class="sgc-toc-level-1">
  <a href="page{fileName}.xhtml">{chapter}</a>
</div>
'''.format(fileName = newfilename,chapter=chapter)
            
                
            # 如果不是本子第一页，那么只改名
            else:
                newfilename = str(count*1000)+img[-8:]               
                os.rename(self.Images_dir + img , self.Images_dir+newfilename)#加上原来的后缀名
                # print(img+"----->"+newfilename)

            #将图片文件纳入manifest清单
            imgType = 'jpeg'
            if newfilename[-3:]=='png':
                imgType = 'png'
            self.manifest += '''
\t<item id="x{0}" href="Images/{0}" media-type="image/{1}"/>
'''.format(newfilename,imgType)
            # print(">>>Img {}引用成功".format(newname))


            #最后生成xhtml文件
            #根据改名后的图片名生成xhtml的内容
            html_content = '''<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
\t<title>page_{}</title>
\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
\t<div style="text-align: center; padding: 0pt; margin: 0pt;">
\t\t<img src="../Images/{}" alt="Images to epub"/>
\t</div>       
</body>
</html>'''.format(count_chapters,newfilename)  
            
            #xhtml内容write to文件
            htmlFileName = 'page{}.xhtml'.format(newfilename)
            htmlFilePath = self.Text_dir+htmlFileName
            count_chapters += 1
            with open(htmlFilePath,'w',encoding='utf-8') as file_object:
                file_object.write(html_content)
            # print(">>>XHTML {}生成成功".format(htmlFilePath))


            #将xhtml文件纳入manifest清单
            self.manifest += '''\t<item id="{0}" href="Text/{0}" media-type="application/xhtml+xml"/>
'''.format(htmlFileName)


            #主心骨结构
            self.spine += '''\t<itemref idref="{}"/>
'''.format(htmlFileName)

        #至此，结束for循环

        

        #收尾
        self.manifest += "  </manifest>\n\n"
        self.spine += "  </spine>\n\n"


        if self.mode.get() == 1:
            self.TOC += "</body></html>"
            self.NCX += '''  </navMap>\n</ncx>'''
            with open(self.Text_dir+"TOC.xhtml",'w',encoding='utf-8') as opf:
                    opf.write(self.TOC)
            with open(self.OEBPS_dir+"toc.ncx",'w',encoding='utf-8') as opf:
                opf.write(self.NCX)


    def chooseChapter(self,count:int = 1):
      
      filedialog_title = "选择章节"
      chapterIndexPath = filedialog.askopenfilename(title = filedialog_title,multiple=False,\
          initialdir = self.Images_dir,filetypes=[("图片文件",('.jpg','.png')),('All Files', '*')])
      if chapterIndexPath=="":
          return
      chapterIndexImgName = chapterIndexPath[chapterIndexPath.rfind("/")+1:]

      self.cptIndexRbtList[count].config(bd=5)
      
      chapter = self.chapterList[self.chap_NO.get()].get()

      #主目录
      self.ncx_chapContent[count] = '''    <navPoint id="navPoint-{count}" playOrder="{count}">
      <navLabel>
        <text>{chapter}</text>
      </navLabel>
      <content src="Text/page{fileName}.xhtml"/>
    </navPoint>

'''.format(count = count+1,chapter=chapter,fileName = chapterIndexImgName)
#count+1是因为那边是从0开始算的（list的下标
                
      #TOC目录
      self.toc_chapContent[count] = '''<div class="sgc-toc-level-1">
  <a href="page{fileName}.xhtml">{chapter}</a>
</div>
'''.format(fileName = chapterIndexImgName,chapter=chapter)
      

    def chooseCover(self):
        
        filedialog_title = "选择封面图片"
        coverImgPath = filedialog.askopenfilename(title = filedialog_title,multiple=False,\
           initialdir = self.Images_dir,filetypes=[("图片文件",('.jpg','.png')),('All Files', '*')])
        if coverImgPath=="":
            return
        # coverImgPath = "D:/##resource/##getPic/autoEpub/temp/OEBPS/Images/10001001.jpg"
        self.coverImgName = coverImgPath[coverImgPath.rfind("/")+1:]#从路径中取文件名


        if self.mode.get() == 2:
          #添加章节
            for eachTOC,eachNCX in zip(self.toc_chapContent,self.ncx_chapContent):
              if eachTOC!="":
                self.TOC += eachTOC
                self.NCX += eachNCX
            self.TOC += "</body></html>"
            self.NCX += '''  </navMap>\n</ncx>'''
            with open(self.Text_dir+"TOC.xhtml",'w',encoding='utf-8') as opf:
                    opf.write(self.TOC)
            with open(self.OEBPS_dir+"toc.ncx",'w',encoding='utf-8') as opf:
                opf.write(self.NCX)

        
        img = Image.open(coverImgPath)
        coverWidth = img.size[0]
        coverHeight = img.size[1]
        img.close()

        coverXHTML_content = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Cover</title>
</head>
<body>
  <div style="text-align: center; padding: 0pt; margin: 0pt;">
    <svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 {width} {height}" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
      <image width="{width}" height="{height}" xlink:href="../Images/{coverImgName}"/>
    </svg>
  </div>
</body>
</html>
'''.format(width = coverWidth,height = coverHeight,coverImgName = self.coverImgName)

        #生成cover.xhtml文件
        with open(self.Text_dir+"cover.xhtml",'w',encoding='utf-8') as opf:
            opf.write(coverXHTML_content)

        
        #生成opf的head
        self.opfHead = '''<?xml version="1.0" encoding="utf-8"?>
<package version="2.0" unique-identifier="BookId" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:language>{language}</dc:language>
    <dc:title>{title}</dc:title>
    <dc:creator>{creator}</dc:creator>
    <dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:{uuid}</dc:identifier>
    <meta name="cover" content="x{coverImg}"/>
    <meta content="1.5.1" name="Sigil version"/>
    <dc:date opf:event="modification" xmlns:opf="http://www.idpf.org/2007/opf">{date}</dc:date>
  </metadata>

'''.format(language = self.et_language.get(),title = self.et_title.get(),\
      creator = self.et_creator.get(),uuid = self.uuid,coverImg=self.coverImgName,date = self.et_date.get())

        self.opfHead += self.manifest
        self.opfHead += self.spine

        #收尾
        self.opfHead += '''  <guide>
    <reference type="cover" title="Cover" href="Text/cover.xhtml"/>
    <reference type="toc" title="Table of Contents" href="Text/TOC.xhtml"/>
  </guide>
  
</package>
        '''
        
        with open(self.OEBPS_dir+"content.opf",'w',encoding='utf-8') as opf:
            opf.write(self.opfHead)
        print(">>>content.opf生成")

        # return

        # self.bt_chooseBookDir.config(state=tk.DISABLED)

        print(">>>开始打包")
        
        epubFileName = self.et_title.get()+".epub"
        cmd_7z = 'cd temp && 7z a "{}" -mmt16'.format(epubFileName)
        # print(cmd_7z)
        os.system(cmd_7z)

        cmd_mv_rm = 'move "temp\\{}" "{}" && rmdir /s/q temp'.format(\
          epubFileName , os.path.dirname(self.img_directory))   

        _thread.start_new_thread(os.system,(cmd_mv_rm,))
        

        print(">>>{}制作完成！".format(epubFileName))
        print("-----------finish-----------")
        
    def beforeQuit(self):
      if os.path.exists("temp/"):
        # shutil.rmtree("temp/")
        os.system("rmdir /s/q temp")
      super().quit()
        
             
if __name__ == '__main__':
    root = tk.Tk()
    root.title("autoEpub  |  by Konoha")
    root.geometry("500x400+650+300")
    
    app =  Application(master=root)
    app.mainloop()

