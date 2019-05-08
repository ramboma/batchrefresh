# -*- coding: utf-8 -*-
import decorator
import sys
import os
import queue
import fileexport
import publish

"""Main module."""

college_report_config={
    # 该目录下每个子目录名称为学院名
    'source-base-path': r'E:\newjincin\projects\ros\doc\18届数据\分院系',
    'exportconfig':{
    "exportlist": [
        {
            'from': r'e:\newjincin\projects\ros\doc\16届数据\分院系\{}\主数据源.xlsx',
            'to': r'e:\newjincin\projects\ros\doc\refresh\datasource\16届数据\分院系',
            'type': 'file'
        },
        {
            'from': r'E:\newjincin\projects\ros\doc\17届数据\分院系\{}\主数据源.xlsx',
            'to': r'e:\newjincin\projects\ros\doc\refresh\datasource\17届数据\分院系',
            'type': 'file'
        },
        {
            'from': r'E:\newjincin\projects\ros\doc\18届数据\分院系\{}',
            'to': r'e:\newjincin\projects\ros\doc\refresh\datasource\18届数据\分院系',
            'type': 'directory'
        }
    ],
    },
    'college_alias':{"传媒学院": ['凤凰传媒学院']},#学院改名

    'prep_cli_path':r'"D:\ProgramFiles\Tableau\Tableau Prep Builder 2019.1\scripts\tableau-prep-cli.bat" -c "{}" -t "{}"',
    'tfl_path':r'e:\newjincin\projects\ros\doc\refresh\tfl\学院\学院.tfl',
    'flow_path':r'e:\newjincin\projects\ros\doc\refresh\tfl\学院\flow.json',

    'http_config':{
        'generate_url':'http://10.10.3.225:19700/v1/planProcessInfo/generatePlanWord',
        #planId(方案id)必填,报告名由学院名+报告+yyyy-MM-dd组成
        'generate_param':{"planId":"27","generateName":""},
        'searchstatus_url':'http://10.10.3.225:19700/v1/planProcessInfo/getByUser/{}',
        'download_url':'http://10.10.3.225:19700/v1/planProcessInfo/downloadPlanWord',
        'download_param':{"planProcessInfoId":"{}"},
        'download_filename':r'e:\newjincin\projects\ros\doc\refresh\output\分学院\{}.docx',
        'cookies':{
            'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTcxNDIwMzl9.UwU11TRLhf5W23E9JRlJiUdl34CNdlsW8tZVMpprn81oEgjg1YJjgFpT6jVPYQ4YCegz3mK2oBvn_0kWaNDuhdJnXGuYELuxh8niVRCVlC4Zp7Lq4F3s3WPAWc4RPxR-nLODKfRFFmHT5af0CJcr35VhjRAp8QZjNSH8KvYGvFY',
            'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
            'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTcxNDIwMzl9.UwU11TRLhf5W23E9JRlJiUdl34CNdlsW8tZVMpprn81oEgjg1YJjgFpT6jVPYQ4YCegz3mK2oBvn_0kWaNDuhdJnXGuYELuxh8niVRCVlC4Zp7Lq4F3s3WPAWc4RPxR-nLODKfRFFmHT5af0CJcr35VhjRAp8QZjNSH8KvYGvFY',
        }
    }
}


#执行学院报告生成
@decorator.timing
def college_batch_generate():
    # 设置任务队列
    # 查找是否有未完成的队列文件,有则加载,无则初始化队列
    # taskqueuename='first'
    # exectype=0 # 0为新的执行任务 1为继续执行中断的任务
    # taskqueuepath=r'c:\{}.txt'.format(taskqueuename)
    #获取学院子目录列表,加入到队列
    dirlist=os.listdir(college_report_config['source-base-path'])
    print(dirlist)
    taskqueue=queue.Queue()
    for onedir in dirlist:
        if onedir=='传媒学院':
        #if onedir!='空学院':
            taskqueue.put(onedir)
            print(onedir)

    print("------------------------")
    while True:
        if taskqueue.empty():
            print('任务队列执行完毕!')
            break
        item=taskqueue.get()
        if item is None:
            break
        #操作当前目录
        print(item)
        # 执行复制操作
        fileexport.college_filecopy(item,college_report_config['exportconfig'],college_report_config['college_alias'])
        # 执行脚本命令,发布数据源
        cmdline=college_report_config['publish']['cli-path']
        publishresult=publish.exec_publish(cmdline)
        if publishresult==False:
            print("更新数据源失败")
        # 调用报告生成接口
    '''
    print("------------------------")
    print("执行完毕!")

if __name__ == "__main__":
    college_batch_generate()