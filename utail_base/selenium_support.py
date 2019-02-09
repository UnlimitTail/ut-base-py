# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep

class SeleniumUtils:

    @staticmethod
    def _elmt(func, name, retryCnt, retryWaitSec):
        currentLoopCnt = 0

        while True:
            currentLoopCnt = currentLoopCnt + 1
            try:
                return func(name)
            except NoSuchElementException:
                
                sleep(retryWaitSec)

                if retryCnt > currentLoopCnt:
                    continue
                
                return None


    @staticmethod
    def _elmts(func, name, retryCnt, retryWaitSec):
        currentLoopCnt = 0

        while True:
            currentLoopCnt = currentLoopCnt + 1
            ret = func(name)
            if ret:
                return ret

            sleep(retryWaitSec)

            if retryCnt > currentLoopCnt:
                continue
                
            return None



    @staticmethod
    def elmt_class(root, className, retryCnt=3, retryWaitSec=3):
        return SeleniumUtils._elmt(root.find_element_by_class_name, className, retryCnt, retryWaitSec)


    @staticmethod
    def elmt_tag(root, tagName, retryCnt=3, retryWaitSec=3):
        return SeleniumUtils._elmt(root.find_element_by_tag_name, tagName, retryCnt, retryWaitSec)

    
    @staticmethod
    def elmts_class(root, className, retryCnt=3, retryWaitSec=3):
        return SeleniumUtils._elmts(root.find_element_by_class_name, className, retryCnt, retryWaitSec)


    @staticmethod
    def elmts_tag(root, tagName, retryCnt=3, retryWaitSec=3):
        return SeleniumUtils._elmts(root.find_element_by_tag_name, tagName, retryCnt, retryWaitSec)

