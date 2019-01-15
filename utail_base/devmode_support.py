import os
import utail_base
import logging
import html

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
    def tpHandlerPrint(tp):
        import json
        log.debug(json.dumps(tp._contents))

    def tpHandlerReport(tp):
        from utail_base import http_send
        for ent in tp._contents:
            ent['text'] = html.unescape(ent['text'])
            http_send(params['reportURL'], ent, 'json', 'PUT')

    if postBehavior == "report":
        postHandler = tpHandlerReport
    else:
        postHandler = tpHandlerPrint

    resultPair = process_task(params,
    postTPHandler=postHandler
    )

    if resultPair[0] is True:
        log.debug('task successed!~ scriptName:{} / elapsed sec : {}'.format(os.path.basename(file), resultPair[1]))
    else:
        log.debug('task failed.')    