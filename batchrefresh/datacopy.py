import os
import decorator
import shutil

@decorator.exception
def copy_dictory_to_target(source,target):
   # 删除目标目录
   shutil.rmtree(target)
   # 拷贝目录到目标目录 
   os.mkdir(target)
   src_files = os.listdir(source)
   for file_name in src_files:
        full_file_name = os.path.join(source, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, target)
   print("copy {} to {} completed!".format(source,target))

def test():
    source=r"c:\test1"
    target=r"c:\test2"
    filename=source+r'\hello.txt'
    if os.path.exists(filename):
        os.remove(filename)
    if os.path.exists(source):
        shutil.rmtree(source)
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(source)
    os.mkdir(target)
    f=open(filename,"w+")
    f.write("hello")
    f.close()
    print("begin test")
    copy_dictory_to_target(source,target)
if __name__ == "__main__":
    test()
