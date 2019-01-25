# -*- coding: utf-8 -*-
import datetime
from dateutil import tz
import pytz

def localTimeToUTCTime(localDateTime, localTimeZone = pytz.timezone('Asia/Seoul')):
    # localDT = localDateTime.replace(tzinfo=tz.tzlocal())
    localDT = localDateTime.replace(tzinfo=localTimeZone)
    return localDT.astimezone(tz.tzutc())