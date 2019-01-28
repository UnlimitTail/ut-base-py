# -*- coding: utf-8 -*-
import logging
import queue
from selenium import webdriver
import threading

log = logging.getLogger(__name__)

class SeleniumPoolBaseClass:
	pass

class SeleniumPoolSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(SeleniumPoolSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class SeleniumPool(SeleniumPoolBaseClass, metaclass=SeleniumPoolSingleton):
    def __init__(self, webDriverPath, poolCnt=0):

        self._lock = threading.Lock()

        self._poolCnt = poolCnt
        self._webDriverPath = webDriverPath


        self._options = webdriver.ChromeOptions()
        self._options.add_argument('headless')
        self._options.add_argument('window-size=1920x1080')
        self._options.add_argument("disable-gpu")
        self._options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        self._options.add_argument("lang=ko_KR")

        if 0 < self._poolCnt:
            self._q = queue.Queue()

            with self._lock:
                for i in range(self._poolCnt):
                    i

                    log.debug('chrome driver loading... ')
                    driver = webdriver.Chrome(self._webDriverPath, chrome_options=self._options)
                    driver.implicitly_wait(5)

                    self._q.put(driver)
        else:
            self._map = dict()

    def createPool(self, threadID):
        log.debug('chrome driver loading... ')

        driver = webdriver.Chrome(self._webDriverPath, chrome_options=self._options)

        with self._lock:
            self._map[str(threadID)] = driver

        driver.implicitly_wait(5)

    def getDriver(self, threadID):
        with self._lock:
            return self._map[str(threadID)]

    @staticmethod
    def clearResource(driverPath):
        driver = webdriver.Chrome(driverPath)
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
    
        
            
    # def alloc(self):
    #     with self._lock:
    #         print('q size : {}'.format(self._q.qsize()))
    #         return self._q.get()

    # def free(self, driver):
    #     with self._lock:
    #         self._q.put(driver)

    



