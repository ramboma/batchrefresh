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

            },
            "target":{

            },
            "publish":{
                "cli-path":import functools
import logging
 
def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler("/path/to/test.log")
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
 
 
def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)
 
            # re-raise the exception
            raise
    return wrapper

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