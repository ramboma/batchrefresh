# -*- coding: utf-8 -*-
import decorator
import sys
import os
import queue

import fileexport
import publish
import httpinvoke
import majorcollege2dict

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
    'college_alias':{"传媒学院": ['凤凰传媒学院'],
        "轨道交通学院":['城市轨道交通学院']
    },#学院改名

    'prep_cli_path':r'"D:\Program Files\Tableau\TableauPrepBuilder2019\scripts\tableau-prep-cli.bat" -c "{}" -t "{}"',
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
            'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc2MjQ5MjR9.e5oUR-ih4YDyrPHPDlFnrqiNQ-NyUDFCrN4-HNSmJJ-yPjtWVXHwx3KO-fxFsalZJhmdTT6gJnL-7qoMgJdTBuOws93m6f8qLkqc9hYffBmUrXW3yANBShUOn2-Y7Fu8GxMMpllpCdp6_ef9X7SBjC5JphXyKPtScM3UkrmxcHY',
            'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
            'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc2MjQ5MjR9.e5oUR-ih4YDyrPHPDlFnrqiNQ-NyUDFCrN4-HNSmJJ-yPjtWVXHwx3KO-fxFsalZJhmdTT6gJnL-7qoMgJdTBuOws93m6f8qLkqc9hYffBmUrXW3yANBShUOn2-Y7Fu8GxMMpllpCdp6_ef9X7SBjC5JphXyKPtScM3UkrmxcHY',
        }
    },
    #输出的报告类型配置,planid是使用的方案,reportname是生成报告的格式,{}用专业名称填充
    'output_report_config':[
        {
            'planId':'48','reportname':'{}2018届本科毕业生社会需求与人才培养调研结果'
        },
        {
            'planId':'51','reportname':'{}2016-2018届本科毕业生调研结果对比分析'
        }
    ]

}
major_report_config={
    # 该目录下每个子目录名称为专业名
    'source-base-path': r'E:\newjincin\projects\ros\doc\18届数据\分专业',
    'exportconfig':{
    "exportlist": [
        {
            'from': r'e:\newjincin\projects\ros\doc\16届数据\分专业\{}\主数据源.xlsx',
            'to': r'e:\newjincin\projects\ros\doc\refresh\datasource\16届数据\分专业',
            'type': 'file'
        },
        {
            'from': r'E:\newjincin\projects\ros\doc\17届数据\分专业\{}\主数据源.xlsx',
            'to': r'e:\newjincin\projects\ros\doc\refresh\datasource\17届数据\分专业',
            'type': 'file'
        },
        {
            'from': r'E:\newjincin\projects\ros\doc\18届数据\分专业\{}',
            'to': r'e:\newjincin\projects\ros\doc\refresh\datasource\18届数据\分专业',
            'type': 'directory'
        }
    ],
    },
    'major_alias':{},#专业改名

    'prep_cli_path':r'"D:\Program Files\Tableau\TableauPrepBuilder2019\scripts\tableau-prep-cli.bat" -c "{}" -t "{}"',
    'tfl_path':r'e:\newjincin\projects\ros\doc\refresh\tfl\专业\专业.tfl',
    'flow_path':r'e:\newjincin\projects\ros\doc\refresh\tfl\专业\flow.json',

    'http_config':{
        'generate_url':'http://10.10.3.225:19700/v1/planProcessInfo/generatePlanWord',
        #planId(方案id)必填,报告名由学院名+报告+yyyy-MM-dd组成
        'generate_param':{"planId":"27","generateName":""},
        'searchstatus_url':'http://10.10.3.225:19700/v1/planProcessInfo/getByUser/{}',
        'download_url':'http://10.10.3.225:19700/v1/planProcessInfo/downloadPlanWord',
        'download_param':{"planProcessInfoId":"{}"},
        'download_filename':r'e:\newjincin\projects\ros\doc\refresh\output\分专业\{}.docx',
        'cookies':{
            'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc2MjQ5MjR9.e5oUR-ih4YDyrPHPDlFnrqiNQ-NyUDFCrN4-HNSmJJ-yPjtWVXHwx3KO-fxFsalZJhmdTT6gJnL-7qoMgJdTBuOws93m6f8qLkqc9hYffBmUrXW3yANBShUOn2-Y7Fu8GxMMpllpCdp6_ef9X7SBjC5JphXyKPtScM3UkrmxcHY',
            'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
            'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc2MjQ5MjR9.e5oUR-ih4YDyrPHPDlFnrqiNQ-NyUDFCrN4-HNSmJJ-yPjtWVXHwx3KO-fxFsalZJhmdTT6gJnL-7qoMgJdTBuOws93m6f8qLkqc9hYffBmUrXW3yANBShUOn2-Y7Fu8GxMMpllpCdp6_ef9X7SBjC5JphXyKPtScM3UkrmxcHY',
        }
    },
    #输出的报告类型配置,planid是使用的方案,reportname是生成报告的格式,{}用专业名称填充
    'output_report_config':[
        {
            'planId':'39','reportname':'{}专业2018届本科毕业生社会需求与人才培养调研结果'
        },
        {
            'planId':'50','reportname':'{}专业2016-2018届本科毕业生调研结果对比分析'
        }
    ]
}
college_major_mapping_path=r'e:\newjincin\projects\ros\doc\refresh\datasource\18届数据\院系-专业对照表.xlsx'

#执行学院报告生成
@decorator.timing
def college_batch_generate(type):#type=1 只生成学院报告 2只生成专业报告 3生成学院和专业报告
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
        if onedir=='政治与公共管理学院':
        #if onedir!='空学院':
            taskqueue.put(onedir)
            print(onedir)

    print("------------------------")
    while True:
        if taskqueue.empty():
            print('任务队列执行完毕!')
            break
        collegename=taskqueue.get()
        if collegename is None:
            break
        #操作当前目录
        print(collegename)
        # 执行复制操作
        fileexport.college_filecopy(collegename,college_report_config['exportconfig'],college_report_config['college_alias'])
        # 执行脚本命令,发布数据源
        cmdline=college_report_config['prep_cli_path'].format(
            college_report_config['flow_path'],
            college_report_config['tfl_path'])
        publishresult=publish.exec_publish(cmdline)
        if publishresult==False:
            print("{}更新数据源失败".format('collegename'))
            break
        if type==1:#只生成学院报告
            college_exec_generate_report(collegename,college_report_config['output_report_config'])
        elif type==2:#只生成专业报告
            college_major_mapper=majorcollege2dict.college_major_mapping(college_major_mapping_path)
            for majorname in college_major_mapper[collegename]:
                major_generate(majorname)
        else:#学院和专业都生成
            college_exec_generate_report(collegename,college_report_config['output_report_config'])
            college_major_mapper=majorcollege2dict.college_major_mapping(college_major_mapping_path)
            for majorname in college_major_mapper[collegename]:
                major_generate(majorname)
    print("------------------------")
    print("执行完毕!")
#生成学院报告
def college_exec_generate_report(collegename,college_report_output_config):
    # 循环调用报告生成接口
    for output_config in college_report_output_config:
        reportid=output_config['planId']
        reportname=output_config['reportname'].format(collegename)

        reportconfig=college_report_config['http_config']
        reportconfig['generate_param']['planId']=reportid
        reportconfig['generate_param']['generateName']=reportname

        httpinvoke.wrap_generate_and_download_report(reportconfig)
    print('{}学院报告生成完毕!'.format(collegename))
def major_generate(majorname):
    print('开始处理{}专业---'.format(majorname))
    # 执行复制操作
    fileexport.major_filecopy(majorname,major_report_config['exportconfig'])
    # 执行脚本命令,发布数据源
    cmdline=major_report_config['prep_cli_path'].format(
        major_report_config['flow_path'],
        major_report_config['tfl_path'])
    publishresult=publish.exec_publish(cmdline)
    if publishresult==False:
        print("{}更新数据源失败".format('majorname'))
        return
    # 调用报告生成接口
    for output_config in major_report_config['output_report_config']:
        reportid=output_config['planId']
        reportname=output_config['reportname'].format(majorname)

        reportconfig=major_report_config['http_config']
        reportconfig['generate_param']['planId']=reportid
        reportconfig['generate_param']['generateName']=reportname

        httpinvoke.wrap_generate_and_download_report(reportconfig)
    print("------------------------")
    print("执行完毕!")

if __name__ == "__main__":
    college_batch_generate(type=2)
    #major_generate('播音与主持艺术')