import time
import requests
import decorator
import json
import util
import logging
import subprocess
import traceback

logger=util.create_logger(logging.INFO,'httpinvoke')
back_logger=util.create_logger(logging.INFO,'back_logger')

def print_and_info(msg):
    logger.info(msg)
    print(msg)
def backlog(msg):
    back_logger.info(msg)
def wrap_generate_and_download_report(config):
    util.print_and_info(config)
        
    generate_url=config['generate_url']
    generate_param=config['generate_param']
    searchstatus_url=config['searchstatus_url']
    download_url=config['download_url']
    download_param=config['download_param']
    download_filename=config['download_filename']
    cookies=config['cookies']

    result=''
    try:
        result=generate_report(generate_url,cookies,generate_param)
        generateResultObj=json.loads(result)
    except:
        stack_msg=traceback.format_exc()
        print_and_info(stack_msg)
        ping('10.10.3.225')
        return
    
    #判断报告生成请求是否发送成功
    if(generateResultObj['code']==0):
        print_and_info("生成报告失败!错误原因:{}".format(generateResultObj['msg']))
        return
    print_and_info('报告正在生成...')
    reportid=generateResultObj['data']
    print_and_info('报告id为{}'.format(reportid))
    #隔1秒查询一次生成状态
    repeatCount=0
    while True:
        searchstatus_url=searchstatus_url.format(reportid)
        statusResult=search_generator_status(searchstatus_url,cookies)
        statusResultObj=json.loads(statusResult)
        if(statusResultObj['code']==0):#如果调用接口失败,等待300ms重试,5次后中断
            print_and_info('生成状态调用失败,错误原因:{}'.format(statusResultObj['msg']))
            repeatCount=repeatCount+1
            if repeatCount>=15:
                break
        if(statusResultObj['data']['planProcessState']=='1'):
            print_and_info('报表生成成功!正在下载...')
            #执行下载
            download_param['planProcessInfoId']=str(reportid)
            download_report(download_url,
                            cookies,
                            download_param,
                            download_filename.format(generate_param['generateName']))
            break
        elif(statusResultObj['data']['planProcessState']=='-1'):#生成失败
            print_and_info('报表生成失败')
            break
        else:
            print('报表生成中...,信息:{}'.format(statusResultObj['data']['planProcessInfo']))
            #间隔5s再查
            time.sleep(10)
#发出生成报告请求
def generate_report(url,cookies,params=None):
    response = requests.get(url, cookies=cookies,params=params)
    print_and_info(response.text)
    result=response.text
    return result
#查询报告生成状态
def search_generator_status(searchurl,cookies):
    result=''
    try:
        searchresponse = requests.get(searchurl, cookies=cookies)
        print_and_info(searchresponse.text)
        result=searchresponse.text
    except:
        stack_msg=traceback.format_exc()
        print_and_info(stack_msg)
        ping('10.10.3.225')
    return result
#下载报告
def download_report(downloadurl,cookies,params,file_name):
    with open(file_name, "wb") as file:
        # get request
        download_response = requests.get(downloadurl, cookies=cookies,params=params)
        #print(download_response.content)
        # write to file
        file.write(download_response.content)

def ping(ipaddress):
    cmdline='ping '+ipaddress
    execresult=subprocess.getstatusoutput(cmdline)
    print_and_info(execresult)

cookies={
        'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTcxNDIwMzl9.UwU11TRLhf5W23E9JRlJiUdl34CNdlsW8tZVMpprn81oEgjg1YJjgFpT6jVPYQ4YCegz3mK2oBvn_0kWaNDuhdJnXGuYELuxh8niVRCVlC4Zp7Lq4F3s3WPAWc4RPxR-nLODKfRFFmHT5af0CJcr35VhjRAp8QZjNSH8KvYGvFY',
        'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
        'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTcxNDIwMzl9.UwU11TRLhf5W23E9JRlJiUdl34CNdlsW8tZVMpprn81oEgjg1YJjgFpT6jVPYQ4YCegz3mK2oBvn_0kWaNDuhdJnXGuYELuxh8niVRCVlC4Zp7Lq4F3s3WPAWc4RPxR-nLODKfRFFmHT5af0CJcr35VhjRAp8QZjNSH8KvYGvFY',
}
def test_generate_report():
    generate_url='http://10.10.3.225:19700/v1/planProcessInfo/generatePlanWord'
    generate_param={"planId":"27","generateName":"测试方案1-27-python生成2"}
    generate_report(generate_url, cookies=cookies,params=generate_param)
    print("test generate report success")
def test_search_generator_status():
    searchstatus_url='http://10.10.3.225:19700/v1/planProcessInfo/getByUser/253'
    search_generator_status(searchstatus_url, cookies=cookies)
    print("test search report status success")

def test_download_report():
    download_url='http://10.10.3.225:19700/v1/planProcessInfo/downloadPlanWord'
    download_param={"planProcessInfoId":"229"}
    download_filename=r'c:\test3\test3.docx'
    download_report(download_url, cookies=cookies,params=download_param,file_name=download_filename)
    print("下载成功!")
def test_wrap_generate_and_download_report():
    testconfig={
        'generate_url':'http://10.10.3.225:19700/v1/planProcessInfo/generatePlanWord',
        'generate_param':{"planId":"27","generateName":"测试方案1-27-python生成2"},
        'searchstatus_url':'http://10.10.3.225:19700/v1/planProcessInfo/getByUser/{}',
        'download_url':'http://10.10.3.225:19700/v1/planProcessInfo/downloadPlanWord',
        'download_param':{"planProcessInfoId":"{}"},
        'download_filename':r'c:\test3\{}.docx',
        'cookies':cookies
    }
    wrap_generate_and_download_report(testconfig)
    print("wrap completed!")

if __name__ == "__main__":
    #test_generate_report()
    #test_search_generator_status()
    #test_download_report()
    test_wrap_generate_and_download_report()
