# -*- coding: utf-8 -*-
from datetime import datetime
import maya
from time import mktime

def timeOffset(localDateTime, offsetMinutes = -540, offsetSecs = 0):
    lts = int(mktime(localDateTime.timetuple())) + int(offsetMinutes * 60) + int(offsetSecs)
    return datetime.fromtimestamp(lts)


def toDt(dateStr:str) -> datetime:
    # try:
        return maya.parse(dateStr).datetime()
    # except Exception:
    #     print('error! test')
    #     quit(1)

