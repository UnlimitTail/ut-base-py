# -*- coding: utf-8 -*-

import json
import logging
import requests
import shutil
import urllib.request

"""
 http, https url 파일 다운로드
"""
def download_file(url, downloadPath, fileOpenMode = 'wb',
auth_verify=False, auth_id='usrname', auth_pw='password'
):
    try:
        r = requests.get(url, auth=(auth_id, auth_pw), verify=auth_verify,stream=True)
        r.raw.decode_content = True        
        with open(downloadPath, fileOpenMode) as f:
            shutil.copyfileobj(r.raw, f)
    except Exception as inst:
        logging.error(inst.args)
        return False

    return True

"""
 http send
"""
def http_send(url, body='', content_type='json', method='POST'):
    req = urllib.request.Request(url, method=method)

    if content_type == 'json':
        req.add_header('Content-Type', 'application/json; charset=utf-8')

    try:
        if len(body) > 0:
            jsonbody = json.dumps(body)
            jsonbodyAsBytes = jsonbody.encode('utf-8')
            req.add_header('Content-Length', len(jsonbodyAsBytes))
            return urllib.request.urlopen(req, jsonbodyAsBytes)
        else:
            return urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        logging.getLogger(__name__).error(err.code)
        return None
    except urllib.error.URLError as err:
        logging.getLogger(__name__).error(err.reason)
        return None
    except Exception as inst:
        logging.error(inst.args)
        return None



    
    
