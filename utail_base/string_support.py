# -*- coding: utf-8 -*-

import re

def clean_html(raw_html, pattern = '<.*?>'):
    cleanr = re.compile(pattern)
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


class TextManipBaseClass:
	pass

class TextManipSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(TextManipSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class TextManip(TextManipBaseClass, metaclass=TextManipSingleton):
    def __init__(self):
        self._dics = dict()
    
    def makeDic(
        self, log, 
        *args   # (dicName, filePath)
        ):

        for i in range(len(args)):
            dicName = args[i][0]
            if dicName in self._dics:
                log.debug('dic({}) alreay done.'.format(dicName))
                continue

            dic = dict()

            f = open(args[i][1], 'r')
            while True:
                line = f.readline()
                if not line:
                    break
                dic[line.strip()] = 0
            f.close()

            if 0 < len(dic):
                self._dics[dicName] = dic
                log.debug('made dictionary({}). words:{}'.format(dicName, len(dic)))

    def exists(self, dicName, word):
        if word in self._dics[dicName]:
            return True
        else:
            return False