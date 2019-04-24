# -*- coding: utf-8 -*-
from threading import Event, Thread

def call_repeatedly(intervalSec, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(intervalSec): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set