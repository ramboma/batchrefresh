# -*- coding: utf-8 -*-
import decorator

"""Main module."""

@decorator.timing
def main():
    #设置配置对象
    config={
        #源数据导入设置,包括待导入的数据源文件路径,tfl文件路径,tfl文件中数据文件路径，
        # tableau_prep_cli文件路径,flow.json文件路径
        "export":{
            "source":{
                "source-data-path":"E:\newjincin\projects\ros\doc\18届数据\分院系",#gai

            },
            "target":{

            },
            "publish":{
                "cli-path":"D:\ProgramFiles\Tableau\Tableau Prep Builder 2019.1\scripts\tableau-prep-cli.bat",
                "param":" -c flow.json ",
                "tlf-path":""
            }
        },
        #调用报告生成接口设置
        "invoke":{

        }
    }
    #设置任务队列
    #执行复制操作
    #执行脚本命令,发布数据源
    #调用报告生成接口
    print("执行完毕!")
main()