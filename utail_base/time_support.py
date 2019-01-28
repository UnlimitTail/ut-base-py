# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import tz
import pytz
from time import mktime

def localTimeToUTCTime(localDateTime, localTimeZone = pytz.timezone('Asia/Seoul')):
    # localDT = localDateTime.replace(tzinfo=tz.tzlocal())
    localDT = localDateTime.replace(tzinfo=localTimeZone)
    return localDT.astimezone(tz.tzutc())

def timeOffset(localDateTime, offsetMinutes = -540):
    lts = int(mktime(localDateTime.timetuple())) + (offsetMinutes * 60)
    return datetime.fromtimestamp(lts)