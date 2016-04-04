# -*- coding: utf-8 -*-
import time


def timeit(func):
    """
    Time of execution
    """
    def timed(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print func.__name__, end - start
        return result

    return timed
