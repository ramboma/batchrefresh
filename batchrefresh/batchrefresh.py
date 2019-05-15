# -*- coding: utf-8 -*-
import decorator
import sys
import os
import queue
import logging
import copy
import threading

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
            'planId':'39','reportname':'{}专业2018届本科毕业生社会需求与人才培养调研结果'
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
    #如果学院下的所有专业都完成了,删除该学院
    delete_key_list=[]
    for dirobj in dirlist:
        completeCount=0
        majorCount=len(dirlist[dirobj])
        for major in dirlist[dirobj]:
            if major['status']==1:
                completeCount+=1
        if completeCount==majorCount:
            delete_key_list.append(dirobj)
    print(delete_key_list)
    for deleteitem in delete_key_list:
        dirlist.pop(deleteitem)
    print_and_info(dirlist)
    taskqueue=queue.Queue()
    noinqueue=[]#['沙钢钢铁学院','社会学院','体育学院','外国语学院']#不生成的学院列表
    for onedir in dirlist:
        if onedir not in noinqueue:
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
                    major_generate(majorname,mapperObj,collegename)
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
    # 生成线程
    threads=[]
    # 调用报告生成接口
    for output_config in major_report_config['output_report_config']:
        reportid=output_config['planId']
        reportname=output_config['reportname'].format(majorname)

        reportconfig=copy.deepcopy(major_report_config['http_config'])
        reportconfig['generate_param']['planId']=reportid
        reportconfig['generate_param']['generateName']=reportname
        #下载报告到学院名的目录中,便于管理
        downloadpath=reportconfig['download_filename']
        split_path_list=os.path.split(downloadpath)
        prepart=split_path_list[0]
        afterpart=split_path_list[1]
        reportconfig['download_filename']=prepart+'\\'+collegename+'\\'+afterpart
        #新的下载路径如果不存在就新建一个
        new_downloadpath=prepart+'\\'+collegename
        if os.path.isdir(new_downloadpath)==False:
            os.mkdir(new_downloadpath)
        print('new path is '+new_downloadpath)

        workthread=threading.Thread(target=httpinvoke.wrap_generate_and_download_report,args=(reportconfig,))
        threads.append(workthread)
        #httpinvoke.wrap_generate_and_download_report(reportconfig)
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    mapperObj.set_major_status(majorname,1)
    print_and_info("------------------------")
    print_and_info("执行完毕!")

def testdeletelist():
    dirlist={'沙钢钢铁学院': [{'major': '冶金工程', 'status': 1}, {'major': '金属材料工程', 'status': 1}], '体育学院': [{'major': '武术与民族传统体育', 'status': 1}, {'major': '体育教育', 'status': 1}, {'major': '运动训练', 'status': 1}, {'major': '运动人体科学', 'status': 1}], '外国语学院': [{'major': '法语(法英双语)', 'status': 1}, {'major': '西班牙语', 'status': 1}, {'major': '日语', 'status': 1}, {'major': '翻译', 'status': 1}, {'major': '俄语(俄英双语)', 'status': 1}, {'major': '朝鲜语', 'status': 1}, {'major': '德语', 'status': 1}, {'major': '英语', 'status': 1}, {'major': '英语(师范)', 'status': 1}], '社会学院': [{'major': '历史学(师范)', 'status': 1}, {'major': '劳动与社会保障', 'status': 1}, {'major': '信息资源管理', 'status': 0}, {'major': '档案学', 'status': 0}, {'major': '旅游管理', 'status': 0}, {'major': '社会学', 'status': 0}], '文学院': [{'major': '汉语言文学', 'status': 0}, {'major': '汉语国际教育', 'status': 0}, {'major': '汉语言文学(基地)', 'status': 0}, {'major': '汉语言文学(师范)', 'status': 0}], '计算机科学与技术学院': [{'major': '信息管理与信息系统', 'status': 0}, {'major': '物联网工程', 'status': 0}, {'major': '软件工程(嵌入式软件人才培养)', 'status': 0}, {'major': '网络工程', 'status': 0}, {'major': '软件工程', 'status': 0}, {'major': '计算机科学与技术', 'status': 0}], '材料与化学化工学部': [{'major': '无机非金属材料工程', 'status': 0}, {'major': '化学工程与工艺', 'status': 0}, {'major': '应用化学', 'status': 0}, {'major': '环境工程', 'status': 0}, {'major': '高分子材料与工程', 'status': 0}, {'major': '材料科学与工程', 'status': 0}, {'major': '材料化学', 'status': 0}, {'major': '功能材料', 'status': 0}, {'major': '化学', 'status': 0}], '艺术学院': [{'major': '艺术设计学', 'status': 0}, {'major': '视觉传达设计', 'status': 0}, {'major': '服装与服饰设计', 'status': 0}, {'major': '环境设计', 'status': 0}, {'major': '美术学(师范)', 'status': 0}, {'major': '产品设计', 'status': 0}, {'major': '数字媒体艺术', 'status': 0}, {'major': '服装与服饰设计(时装表演与服装设计)', 'status': 0}, {'major': '美术学', 'status': 0}], '王健法学院': [{'major': '知识产权', 'status': 0}, {'major': '法学', 'status': 0}], '机电工程学院': [{'major': '机械电子工程', 'status': 0}, {'major': '工业工程', 'status': 0}, {'major': '电气工程及其自动化', 'status': 0}, {'major': '材料成型及控制工程', 'status': 0}, {'major': '机械工程', 'status': 0}], '纺织与服装工程学院': [{'major': '服装设计与工程', 'status': 0}, {'major': '纺织工程', 'status': 0}, {'major': '纺织工程(中外合作办学项目)', 'status': 0}, {'major': '非织造材料与工程', 'status': 0}, {'major': '轻化工程', 'status': 0}], '物理与光电·能源学部': [{'major': '物理学(师范)', 'status': 0}, {'major': '物理学', 'status': 0}, {'major': '光电信息科学与工程', 'status': 0}, {'major': '电子信息科学与技术', 'status': 0}, {'major': '新能源材料与器件', 'status': 0}, {'major': '能源与动力工程', 'status': 0}, {'major': '测控技术与仪器', 'status': 0}], '教育学院': [{'major': '应用心理学', 'status': 0}, {'major': '教育学(师范)', 'status': 0}, {'major': '教育技术学(师范)', 'status': 0}], '轨道交通学院': [{'major': '车辆工程', 'status': 0}, {'major': '电气工程与智能控制', 'status': 0}, {'major': '工程管理', 'status': 0}, {'major': '建筑环境与能源应用工程', 'status': 0}, {'major': '通信工程(城市轨道交通通信信号)', 'status': 0}, {'major': '交通运输', 'status': 0}], '数学科学学院': [{'major': '金融数学', 'status': 0}, {'major': '信息与计算科学', 'status': 0}, {'major': '数学与应用数学(基地)', 'status': 0}, {'major': '统计学', 'status': 0}, {'major': '数学与应用数学(师范)', 'status': 0}], '政治与公共管理学院': [{'major': '物流管理(中外合作办学项目)', 'status': 0}, {'major': '城市管理', 'status': 0}, {'major': '物流管理', 'status': 0}, {'major': '行政管理', 'status': 0}, {'major': '思想政治教育', 'status': 0}, {'major': '人力资源管理', 'status': 0}, {'major': '哲学', 'status': 0}, {'major': '管理科学', 'status': 0}, {'major': '公共事业管理', 'status': 0}], '传媒学院': [{'major': '广告学', 'status': 0}, {'major': '新闻学', 'status': 0}, {'major': '广播电视学', 'status': 0}, {'major': '播音与主持艺术', 'status': 0}], '医学部': [{'major': '食品质量与安全', 'status': 0}, {'major': '生物信息学', 'status': 0}, {'major': '法医学', 'status': 0}, {'major': '护理学', 'status': 0}, {'major': '生物科学', 'status': 0}, {'major': '医学影像学', 'status': 0}, {'major': '药学', 'status': 0}, {'major': '预防医学', 'status': 0}, {'major': '口腔医学', 'status': 0}, {'major': '生物技术', 'status': 0}, {'major': '中药学', 'status': 0}, {'major': '医学检验技术', 'status': 0}, {'major': '生物制药', 'status': 0}, {'major': '临床医学', 'status': 0}, {'major': '放射医学', 'status': 0}], '金螳螂建筑学院': [{'major': '城乡规划', 'status': 0}, {'major': '建筑学(室内设计)', 'status': 0}, {'major': '园艺', 'status': 0}, {'major': '风景园林', 'status': 0}, {'major': '建筑学', 'status': 0}], '电子信息学院': [{'major': '电子科学与技术', 'status': 0}, {'major': '信息工程', 'status': 0}, {'major': '通信工程', 'status': 0}, {'major': '电子信息工程', 'status': 0}, {'major': '微电子科学与工程', 'status': 0}, {'major': '通信工程(嵌入式软件人才培养)', 'status': 0}], '音乐学院': [{'major': '音乐表演', 'status': 0}, {'major': '音乐学(师范)', 'status': 0}], '东吴商学院(财经学院)': [{'major': '市场营销', 'status': 0}, {'major': '金融学(中外合作办学项目)', 'status': 0}, {'major': '会计学', 'status': 0}, {'major': '财政学', 'status': 0}, {'major': '工商管理', 'status': 0}, {'major': '财务管理', 'status': 0}, {'major': '国际经济与贸易', 'status': 0}, {'major': '金融学', 'status': 0}, {'major': '经济学', 'status': 0}, {'major': '电子商务', 'status': 0}]}
    print(len(dirlist))
    delete_key_list=[]
    for dirobj in dirlist:
        completeCount=0
        majorCount=len(dirlist[dirobj])
        for major in dirlist[dirobj]:
            if major['status']==1:
                completeCount+=1
        if completeCount==majorCount:
            delete_key_list.append(dirobj)
    print(delete_key_list)
    for deleteitem in delete_key_list:
        dirlist.pop(deleteitem)
    print(dirlist)
    print(len(dirlist))

if __name__ == "__main__":
    college_batch_generate(type=2)
    #mapperObj=majorcollege2dict(college_major_mapping_path)
    #major_generate('播音与主持艺术',mapperObj,'文学院')
    #testdeletelist()