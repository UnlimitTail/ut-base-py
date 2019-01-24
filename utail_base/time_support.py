# -*- coding: utf-8 -*-
import datetime
from dateutil import tz

def localTimeToUTCTime(localDateTime):
    localDT = localDateTime.replace(tzinfo=tz.tzlocal())
    return localDT.astimezone(tz.tzutc())