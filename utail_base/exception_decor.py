# -*- coding: utf-8 -*-
import functools
from timeit import default_timer as timer

def exception(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.error(err)
                raise
        return wrapper
    return decorator


def exceptionDB(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.error(err)
                return None
            finally:
                if args[0] is not None:
                    args[0].close()
        return wrapper
    return decorator


def task_timeChecker(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            startTime = timer()
            try:
                func(*args, **kwargs)

                endTime = timer()
                return (True, endTime - startTime)
            except Exception as inst:
                logger.error(inst.args)
                return (False, 0)
        return wrapper
    return decorator