# 纯图片制作epub电子书
##用途：轻小说扫图或漫画生成epub电子书

###两个应用exe和py各一份，有python的可以用py，没有的可以用exe。

##生成xhtml是指，利用sigil等专业软件制作epub时的辅助脚本。[相关视频](https://www.bilibili.com/video/BV1qf4y1j72F)


##autoEpub，顾名思义，我觉得sigil导入图片太慢了，于是解析了epub的基本格式后我直接写了个全自动生成epub的脚本。
##这个因为是自用的，所以没写太多说明。基本就是这样：开始先选模式，Anthony模式是指，一些本子合集做成epub时，要求所有本子在一个文件夹下，单个本子命名为1001到100n。(太复杂了，这个和我其他脚本是联动的，所以一般人用不上，虽然这种脚本也没几个人需要把)
##offprint模式就是单行本，就是一本正经的小说或漫画扫图，然后选择目录，填写标题，作者，然后编辑目录，可以选择文件（选择中使用大图模式可以清晰的看到你要选的目录），然后选择生成目录就已经完成了所有的制作。
##最终会在原图片目录的父目录中出现一本epub文件。
