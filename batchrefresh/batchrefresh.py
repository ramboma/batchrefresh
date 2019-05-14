# -*- coding: utf-8 -*-
import decorator
import sys
import os
import queue
import logging

import fileexport
import publish
import httpinvoke
from majorcollege2dict import majorcollege2dict

import util

"""Main module."""


logger=util.create_logger(logging.INFO,__name__)
back_logger=util.create_logger(logging.INFO,'back_logger')

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
            'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc5Njg5MjN9.bIf4Rni6TEGfcSSHtif9upUpOz_zPXMUNp98F4dJ8waMn6NVNwpM50ZG3kuPd3PSEnNrcN5j2s3pFaaMpMC8YL23fWac1lA_EvKUYg3VvzMBgjOQKhnnV20OeC6e8bvHN6qfGbNEBxgARLuz3T8dpyk1GULuZNjinTr4BxJjH7g',
            'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
            'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc5Njg5MjN9.bIf4Rni6TEGfcSSHtif9upUpOz_zPXMUNp98F4dJ8waMn6NVNwpM50ZG3kuPd3PSEnNrcN5j2s3pFaaMpMC8YL23fWac1lA_EvKUYg3VvzMBgjOQKhnnV20OeC6e8bvHN6qfGbNEBxgARLuz3T8dpyk1GULuZNjinTr4BxJjH7g',
        }
    },
    #输出的报告类型配置,planid是使用的方案,reportname是生成报告的格式,{}用专业名称填充
    'output_report_config':[
        {
            'planId':'48','reportname':'{}2018届本科毕业生社会需求与人才培养质量报告'
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
            'Admin-Token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc5Njg5MjN9.bIf4Rni6TEGfcSSHtif9upUpOz_zPXMUNp98F4dJ8waMn6NVNwpM50ZG3kuPd3PSEnNrcN5j2s3pFaaMpMC8YL23fWac1lA_EvKUYg3VvzMBgjOQKhnnV20OeC6e8bvHN6qfGbNEBxgARLuz3T8dpyk1GULuZNjinTr4BxJjH7g',
            'JSESSIONID':'F420351B4AD953795A66AC498B0FF18E',
            'token':'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyb3MtbWFqb3IiLCJ1c2VySWQiOiI2ODI5MDMiLCJuYW1lIjoiUk9T5pON5L2c5Lq65ZGYIiwicm9sZXMiOlt7ImlkIjoyOSwiY29kZSI6bnVsbCwibmFtZSI6IlJPUyIsInN0YXR1cyI6bnVsbCwiY29sbGVnZUxpc3QiOm51bGwsIm1hbmFnZVNjb3BlTGlzdCI6bnVsbH1dLCJyb2xlVHlwZSI6IjAiLCJleHAiOjE1NTc5Njg5MjN9.bIf4Rni6TEGfcSSHtif9upUpOz_zPXMUNp98F4dJ8waMn6NVNwpM50ZG3kuPd3PSEnNrcN5j2s3pFaaMpMC8YL23fWac1lA_EvKUYg3VvzMBgjOQKhnnV20OeC6e8bvHN6qfGbNEBxgARLuz3T8dpyk1GULuZNjinTr4BxJjH7g',
        }
    },
    #输出的报告类型配置,planid是使用的方案,reportname是生成报告的格式,{}用专业名称填充
    'output_report_config':[
        {
            'planId':'39','reportname':'{}专业2018届本科毕业生社会需求与人才培养质量报告'
        },
        {
            'planId':'50','reportname':'{}专业2016-2018届本科毕业生调研结果对比分析'
        }
    ]
}
college_major_mapping_path=r'e:\newjincin\projects\ros\doc\refresh\datasource\18届数据\院系-专业对照表.xlsx'

def print_and_info(msg):
    logger.info(msg)
    print(msg)
def backlog(msg):
    back_logger.info(msg)
#执行学院报告生成
'''
type=1 只生成学院报告 2只生成专业报告 3生成学院和专业报告
college_list 要处理的学院列表
major_list 要处理的专业列表
'''
@decorator.timing
def college_batch_generate(type):
    # 设置任务队列
    # 查找是否有未完成的队列文件,有则加载,无则初始化队列
    # taskqueuename='first'
    # exectype=0 # 0为新的执行任务 1为继续执行中断的任务
    # taskqueuepath=r'c:\{}.txt'.format(taskqueuename)

    # 读取配置文件
    mapperObj=majorcollege2dict(college_major_mapping_path)
    #获取学院子目录列表,加入到队列
    #dirlist=os.listdir(college_report_config['source-base-path'])
    dirlist=mapperObj.college_major_mapping()
    print_and_info(dirlist)
    taskqueue=queue.Queue()
    for onedir in dirlist:
        #if onedir=='政治与公共管理学院':
        taskqueue.put(onedir)
        print_and_info(onedir)

    print_and_info("------------------------")
    while True:
        if taskqueue.empty():
            print_and_info('任务队列执行完毕!')
            break
        collegename=taskqueue.get()
        if collegename is None:
            break
        #操作当前目录
        print_and_info(collegename)
        # 执行复制操作
        fileexport.college_filecopy(collegename,college_report_config['exportconfig'],college_report_config['college_alias'])
        # 执行脚本命令,发布数据源
        cmdline=college_report_config['prep_cli_path'].format(
            college_report_config['flow_path'],
            college_report_config['tfl_path'])
        publishresult=publish.exec_publish(cmdline)
        if publishresult==False:
            print_and_info("{}更新数据源失败".format(collegename))
            backlog("{}更新数据源失败".format(collegename))
            continue#一个学院更新失败后继续下一个学院
        if type==1:#只生成学院报告
            college_exec_generate_report(collegename,college_report_config['output_report_config'])
        elif type==2:#只生成专业报告
            for major_and_status in dirlist[collegename]:
                majorname=major_and_status['major']
                status=major_and_status['status']
                if status==0:
                    major_generate(majorname,mapperObj，collegename)
        else:#学院和专业都生成
            college_exec_generate_report(collegename,college_report_config['output_report_config'])
            for major_and_status in dirlist[collegename]:
                majorname=major_and_status['major']
                status=major_and_status['status']
                if status==0:
                    major_generate(majorname,mapperObj,collegename)
    print_and_info("------------------------")
    print_and_info("执行完毕!")
#生成学院报告
@decorator.timing
def college_exec_generate_report(collegename,college_report_output_config):
    # 循环调用报告生成接口
    for output_config in college_report_output_config:
        reportid=output_config['planId']
        reportname=output_config['reportname'].format(collegename)

        reportconfig=college_report_config['http_config']
        reportconfig['generate_param']['planId']=reportid
        reportconfig['generate_param']['generateName']=reportname

        httpinvoke.wrap_generate_and_download_report(reportconfig)
    print_and_info('{}学院报告生成完毕!'.format(collegename))
def major_generate(majorname,mapperObj,collegename):
    print_and_info('开始处理{}专业---'.format(majorname))
    # 执行复制操作
    fileexport.major_filecopy(majorname,major_report_config['exportconfig'])
    # 执行脚本命令,发布数据源
    cmdline=major_report_config['prep_cli_path'].format(
        major_report_config['flow_path'],
        major_report_config['tfl_path'])
    publishresult=publish.exec_publish(cmdline)
    if publishresult==False:
        print_and_info("{}更新数据源失败".format(majorname))
        backlog("{}更新数据源失败".format(majorname))
        return
    backlog("{}更新数据源成功".format(majorname))
    # 调用报告生成接口
    for output_config in major_report_config['output_report_config']:
        reportid=output_config['planId']
        reportname=output_config['reportname'].format(majorname)

        reportconfig=major_report_config['http_config']
        reportconfig['generate_param']['planId']=reportid
        reportconfig['generate_param']['generateName']=reportname
        #下载报告到学院名的目录中,便于管理
        downloadpath=reportconfig['download_filename']
        split_path_list=os.path.split(downloadpath)
        reportconfig['download_filename']=split_path_list[0]+'\\'+collegename+'\\'+split_path_list[1]
        #新的下载路径如果不存在就新建一个
        new_downloadpath=reportconfig['download_filename']=split_path_list[0]+'\\'+collegename
        if os.path.isdir(new_downloadpath)==False:
            os.mkdir(new_downloadpath)

        httpinvoke.wrap_generate_and_download_report(reportconfig)
    mapperObj.set_major_status(majorname,1)
    print_and_info("------------------------")
    print_and_info("执行完毕!")

if __name__ == "__main__":
    college_batch_generate(type=3)
    #major_generate('播音与主持艺术')