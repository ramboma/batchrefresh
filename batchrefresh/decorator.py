import functools
import logging
from time import time
import util
 
 
def exception(function):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            util.print_and_info(err)
 
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
        util.print_and_info('elapse time is {} seconds'.format(end-start))
        return result
    return wrapper
@timing
def test_timing_stub():
    print("test timing stub!")

@exception
def test_exception_stub():
    print("test exception stub!")
    errorresult=1/0

if __name__ == "__main__":
    test_timing_stub()
    test_exception_stub()
