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


def _win_set_time(time_tuple):
    pass
    # import pywin32
    # # http://timgolden.me.uk/pywin32-docs/win32api__SetSystemTime_meth.html
    # # pywin32.SetSystemTime(year, month , dayOfWeek , day , hour , minute , second , millseconds )
    # dayOfWeek = datetime.datetime(time_tuple).isocalendar()[2]
    # pywin32.SetSystemTime( time_tuple[:2] + (dayOfWeek,) + time_tuple[2:])

def _linux_set_time(time_tuple):
    import ctypes
    import ctypes.util
    import time

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = int( time.mktime( datetime( *time_tuple[:6]).timetuple() ) )
    ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))


def timeSync(log, platform):
    if not platform.startswith('linux'):
        return

    log.info('start syncTime for LINUX')

    import ntplib
    from time import ctime
    from datetime import datetime
    
    c = ntplib.NTPClient()
    # r = c.request('kr.pool.ntp.org', version=3)
    r = c.request('europe.pool.ntp.org', version=3)
    dt = datetime.fromtimestamp(r.tx_time)

    log.info('current time(prev sync): {}'.format(datetime.now() ) )
    _linux_set_time(dt.timetuple())
    log.info('current time(after sync): {}'.format(datetime.now() ) )
