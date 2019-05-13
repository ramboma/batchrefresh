import json
from collections import namedtuple
import os
import shutil
import logging

loglevel_dict={
        'info':logging.INFO,
        'debug':logging.DEBUG,
        'error':logging.ERROR,
        'warn':logging.WARN,
        'fatal':logging.FATAL
    }

def _json_object_hook(d): 
    return namedtuple('X', d.keys())(*d.values())
def json2obj(data): 
    return json.loads(data, object_hook=_json_object_hook)

def xcopy(src,dest):
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest)
def print_and_info(msg,product_type='log'):
    #logger=create_logger(logging.INFO,product_type)
    print(msg)
    #logger.info(msg)

def create_logger(loglevel,product_type):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(product_type)
    logger.setLevel(loglevel)
     
    # create the logging file handler
    fh = logging.FileHandler("{}.log".format(product_type))
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
if __name__ == "__main__":
    print_and_info("test info","util")