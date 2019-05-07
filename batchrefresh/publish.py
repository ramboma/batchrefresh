import subprocess
import decorator

@decorator.exception
def exec_publish(cmdline):#执行发布脚本并返回
    execresult=subprocess.getstatusoutput(cmdline)
    print(execresult)
    # 如果执行错误,那么输出错误信息并返回False
    '''
    (0, 'Preparing to run the flow : /Users/rambo/Documents/tableauproj/shandong.tfl\nLoading the flow.\nLoaded the flow.\nUpdated the connections with supplied credentials.\nEstablished input connections with remote data sources.\nKeychainStore Ignored Exception: java.security.cert.CertificateParsingException: java.io.IOException: Duplicate extensions not allowed\nSigned in successfully as tabadmin to site ros(ros)\nChecking the flow document for errors.\nFlow Document has no errors.\nPreparing to execute the flow.\nFlow Execution Status: Running\nFlow Execution Status: Running\nFlow Execution Status: Running\nFlow Execution Status: Running\nFlow Execution Status: Finished\nFinished running the flow successfully.')
    '''
    # 执行正确,返回True
    return True
def test():
    #cmdline=r'"D:\ProgramFiles\Tableau\Tableau Prep Builder 2019.1\scripts\tableau-prep-cli.bat" -c "flow.json" -t "flow.tfl"'
    cmdline=r'"/Applications/Tableau Prep Builder 2019.1.app/Contents/scripts/tableau-prep-cli" -c "/Users/rambo/Documents/tableauproj/flow.json" -t "/Users/rambo/Documents/tableauproj/shandong.tfl"'
    exec_publish(cmdline)

if __name__ == "__main__":
    test()
