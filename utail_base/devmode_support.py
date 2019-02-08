import os
import utail_base
import logging
import html
import re
from .string_support import clean_html
import threading
from timeit import default_timer as timer
from .web_support import HttpError
from .selenium_pool import SeleniumPool

def processBootStrap(useChdir=True, useLogger=True, logFilePath='/tmp/logFileName.log', filePath=''):
    if useChdir is True:
        dir_path = os.path.dirname(os.path.realpath(filePath))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        os.chdir(parent_path)

    if useLogger is True:
        # setup logging
        utail_base.setup_logging(default_level=logging.INFO)
        utail_base.setup_logging_root(loggingLv=logging.DEBUG, filePath=logFilePath)


def dataValidatorDefault(ent):
    # {
    #     'key':tp.getCurrentURL(),
    #     'category1':'ex_noti',
    #     'category2':'coinone',
    #     'url':tp.getCurrentURL(),
    #     'title':noticeTitle, 
    #     'created':int(mktime(noticeTime.timetuple())),
    #     'locale':'ko',
    #     'text': detailTagSoup.get_text(separator='\n'),
    #     'tags':['coinone', '코인원']
    # }
    pass




def runProcess(log, file, process_task, postBehavior, params, convFunc = None, validator = dataValidatorDefault):
    def tpHandlerPrintOnce(tp):
        import json
        for ent in tp._contents:
            ent['text'] = clean_html(ent['text'])
            convFunc(ent)
            validator(ent)
            log.debug(json.dumps(ent))
            
    def tpHandlerPrint(tp):
        import json
        for ent in tp._contents:
            ent['text'] = clean_html(ent['text'])
            convFunc(ent)
            validator(ent)
        log.debug(json.dumps(tp._contents))

    def tpHandlerReport(tp):
        from utail_base import http_send
        for ent in tp._contents:
            #ent['text'] = html.unescape(ent['text'])\
            ent['text'] = clean_html(ent['text'])
            convFunc(ent)
            validator(ent)
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


def runTest(log, process_task, postBehavior, pjs, convFunc = None, validator = dataValidatorDefault):
    spool = SeleniumPool(str(pjs['webdriverPath']))
    spool.createPool(str(threading.get_ident()))
    runProcess(log, "scriptTest", process_task, postBehavior, pjs, convFunc, validator)
