# -*- coding: utf-8 -*-
import decorator
import sys
import os
import queue
import datacopy
import publish

"""Main module."""

# 设置配置对象
refresh_config = {
    # 源数据导入设置,包括待导入的数据源文件路径,tfl文件路径,tfl文件中数据文件路径，
    # tableau_prep_cli文件路径,flow.json文件路径
    'export': {
        # 该目录下每个子目录名称为学院名
        'source-base-path': r'E:\newjincin\projects\ros\doc\18届数据\分院系',
        # 目标基础路径
        'target-base-path': r'E:\newjincin\projects\ros\doc\18届数据\分院系',
        'copylist':[
            {
                'type':'relative',#绝对路径absolute还是相对路径relative,是相对路径的话,from会加上source-base-path,to会加上target-base-path
                'from':'*',#所有路径
                'to':''#路径
            },
            {
                'type':'relative',#绝对路径absolute还是相对路径relative,是相对路径的话,from会加上source-base-path,to会加上target-base-path
                'from':'主字典表.xlsx',#单个文件
                'to':''
            }
        ]
    },
    'publish': {
        'cli-path': r'D:\ProgramFiles\Tableau\Tableau Prep Builder 2019.1\scripts\tableau-prep-cli.bat',
        'param': ' -c flow.json ',
        'tlf-path': '',
        # tlf依赖的数据文件路径,源数据文件会覆盖此文件夹
        'data-path': ''
    },
    # 调用报告生成接口设置
    'invoke': {
        'url': 'http://10.10.3.225:8086',
        'cookie': '',
        'prefix': '',
        'subfix': ''
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
    dirlist=os.listdir(refresh_config['export']['source-data-path'])
    print(dirlist)
    taskqueue=queue.Queue()
    for onedir in dirlist:
        if os.path.isdir(onedir) and onedir<>'空学院':
            taskqueue.put(onedir)

    print("------------------------")
    while True:
        item=taskqueue.get()
        if item is None:
            break
        #操作当前目录
        print(item)
        # 执行复制操作
        datacopy.copy_dictory_to_target(item.source,item.target)
        # 执行脚本命令,发布数据源
        cmdline=refresh_config['publish']['cli-path']
        publishresult=publish.exec_publish(cmdline)
        if publishresult==False:
            print("更新数据源失败")
        # 调用报告生成接口
    
    print("------------------------")
    print("执行完毕!")

if __name__ == "__main__":
    college_batch_generate()