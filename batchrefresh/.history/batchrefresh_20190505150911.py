# -*- coding: utf-8 -*-
import decorator
import sys
import os
import queue

"""Main module."""

# 设置配置对象
refresh_config = {
    # 源数据导入设置,包括待导入的数据源文件路径,tfl文件路径,tfl文件中数据文件路径，
    # tableau_prep_cli文件路径,flow.json文件路径
    'export': {
        # 该目录下每个子目录名称为学院名
        'source-data-path': r'E:\newjincin\projects\ros\doc\18届数据\分院系',
        'copylist':[
            {
                'from':'',
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
@decorator.timing
def main():
    # 设置任务队列
    #获取子目录列表,加入到队列
    dirlist=os.listdir(refresh_config['export']['source-data-path'])
    print(dirlist)
    taskqueue=queue.Queue()
    for onedir in dirlist:
        if(os.path.isdir(onedir)):
            taskqueue.put(onedir)
    taskqueue.to
    print(taskqueue)
    
    # 执行复制操作
    # 执行脚本命令,发布数据源
    # 调用报告生成接口
    print("执行完毕!")


main()
