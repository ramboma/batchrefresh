import subprocess
import decorator

@decorator.exception
def exec_publish(cmdline):#执行发布脚本并返回
    execresult=subprocess.getstatusoutput(cmdline)
    print(execresult)
    # 如果执行错误,那么输出错误信息并返回False
    # 执行正确,返回True
    return True
def test():
    cmdline=r'"D:\ProgramFiles\Tableau\Tableau Prep Builder 2019.1\scripts\tableau-prep-cli.bat" -c "flow.json" -t "flow.tfl"'
    exec_publish(cmdline)

if __name__ == "__main__":
    test()
