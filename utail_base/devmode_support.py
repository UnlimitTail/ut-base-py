import os
import utail_base
import logging
import html
import re
from .string_support import clean_html
import threading
from timeit import default_timer as timer
from .web_support import HttpError

def processBootStrap(useChdir=True, useLogger=True, logFilePath='/tmp/logFileName.log', filePath=''):
    if useChdir is True:
        dir_path = os.path.dirname(os.path.realpath(filePath))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        os.chdir(parent_path)

    if useLogger is True:
        # setup logging
        utail_base.setup_logging(default_level=logging.INFO)
        utail_base.setup_logging_root(loggingLv=logging.DEBUG, filePath=logFilePath)


def runProcess(log, file, process_task, postBehavior, params):
    def tpHandlerPrintOnce(tp):
        import json
        for ent in tp._contents:
            ent['text'] = clean_html(ent['text'])
            log.debug(json.dumps(ent))
            
    def tpHandlerPrint(tp):
        import json
        for ent in tp._contents:
            ent['text'] = clean_html(ent['text'])
        log.debug(json.dumps(tp._contents))

    def tpHandlerReport(tp):
        from utail_base import http_send
        for ent in tp._contents:
            #ent['text'] = html.unescape(ent['text'])\
            ent['text'] = clean_html(ent['text'])
            http_send(params['reportURL'], ent, 'json', 'PUT')

    if postBehavior == "report":
        postHandler = tpHandlerReport
    elif postBehavior == "printOnce":
        postHandler = tpHandlerPrintOnce
    else:
        postHandler = tpHandlerPrint

    
    startTime = timer()
    log.debug('start module : ' + __file__)

    try:
        process_task(params, 
        postTPHandler=postHandler, 
        TLS=threading.local(), 
        )

        log.debug('clean-end module({}) elapsed Time : {}'.format(__file__, timer() - startTime ))
        return True

    except HttpError as inst:
        errorMsg = 'code:{} / msg:{} / <{}>:({}) / {}'.format(inst.code, inst.message, inst.filename, inst.line, inst.function)

        log.error(errorMsg)

        # http error(429) : Too Many Requests
        if "429" == str(inst.code):
            log.error('Too Many Requests. targetFile : {}'.format(__file__))
        else:
            log.error('Http Error. targetFile : {} summary:{}'.format(__file__, inst.getErrorString()))
            
    except Exception as inst:
        errorMsg = 'failed process_task(not defined exception). target:{}, msg:{}'.format(__file__, inst.args)

        log.error(errorMsg)
    
    log.debug('failed-end module({}) elapsed Time : {}'.format(__file__, timer() - startTime ))
    return False

