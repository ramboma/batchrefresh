# -*- coding: utf-8 -*-
import decorator

"""Main module."""

@decorator.timing
def main():
    #设置配置对象
    config={
        #
        "source":{

        },
        "target":{

        },
        "publish":{

        },
        "invoke":{

        }
    }
    #设置任务队列
    #执行复制操作
    #执行脚本命令,发布数据源
    #调用报告生成接口
    print("执行完毕!")
main()