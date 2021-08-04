#==============文件的相关操作==================

#   文件夹：
#创建一个文件夹，路径表示方式通常使用\\或者/，防止路径中的首字母存在转义
os.mkdir("e:\\testdir")

#删除一个文件夹(空文件夹) rmdir
os.rmdir("e:\\testdir")
#如果需要删除一个文件os.remove()
#如果需要删除一个非空文件夹，则需要删除目录树，需要导入shutil模块，shutil.rmtree()

#文件、文件夹更名 rename()
os.rename("e:/testdir","e:/test/1")

#查文件名   返回值是一个列表(返回指定目录中的所有目录名和文件名)
print(os.listdir("e:")) #查找e盘所有文件夹名和文件名

#   文件：
#创建文件
get_file=open("e:/test/test.xlsx","w")
print(get_file)  #打印的是一个文件流对象，可以以此来进行写的操作
get_file.write("hello world!")
#文件流的创建是需要分配内存空调关键进行储存，该文件流对象是不会在使用完毕之后自动
#   销毁或自动释放的，也就是说在使用完文件流后需要使用close()手动关闭文件流对象。
get_file.close()
#   为防止文件流未关闭则会使用with语句完成；在使用完毕后会自动进行关闭操作
#语法：with open语句 as 对象引用名
#           语句块
with open("e:/test/day1.py","w") as file1:
    file1.write("今天是个好日子！")

#防止转义还可以在字符串前加一个r   eg:with open(r"e:\test\day1.py","w") as fil1
# read      读文件的所有内容       read(4):表示读文件的前4个字节（此处默认值为-1）
#readline   读取该文件的一行内容(默认为第一行,默认参数为-1)  如果重新声明参数，则表示字节数
#readlines 读取该文件的所有内容，并且返回一个列表，每一行代表一个元素，且最后列表的最后一个元素为空
"""
    #注意注意！！在使用流读取文件内容的时候，如果已经有将文件中的内容全部读取完毕后，则该对象中不存在的内容，并且指针此时已经在
    #   最后一行，所以后续读取文件的代码的结果就是空值
"""

#isdir  isfile  exists  测试文件或文件夹是否存在的三个方法：
#isfile 只用于判断文件是否存在
#isdir  只用于判断文件夹是否存在
#exists 即可判断文件也可以判断文件夹
print(os.path.exists(r"D:\pythontest\day1.txt"))


