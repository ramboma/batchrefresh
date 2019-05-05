import functools
import logging
from time import time
 
def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("decorator")
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler("decorator.log")
 
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
def timing(function):
    """
    A decorator that wraps the function proc time in function and logs 
    function's input arguments
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start=time()
        result=function(*args, **kwargs)
        end=time()
        print('elapse time is {} seconds'.format(end-start))
        return result
    return wrapper
