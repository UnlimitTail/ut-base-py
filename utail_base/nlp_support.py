# -*- coding: utf-8 -*-
# nlp_support

from konlpy.tag import Komoran
import logging
import threading

log = logging.getLogger(__name__)


class NLPManager:
    def __init__(self, userdic=None):
        self._komoran = Komoran(userdic=userdic)

    def getTags(self, sentences, filterFunc=None, tagsMax=3):
        sentences = sentences.replace('\n', '')
        wordsMap = dict()
        result = self._komoran.pos(sentences)
        for v in result:
            # NN:명사, OL:외국어
            # if 'NN' in v[1] or 'OL' in v[1]:
            # NNG 일반명사   NNP 고유명사
            if 'NNP' == v[1] or 'NNG' == v[1]:
                if v[0] in wordsMap:
                    wordsMap[str(v[0])] = int(wordsMap[str(v[0])]) + 1
                else:
                    wordsMap[str(v[0])] = 1

        wordsList = list()
        for key, value in wordsMap.items():
            wordsList.append([value, key])

        if filterFunc is not None:
            filterFunc(wordsList)

        wordsList.sort(reverse=True)
        slicedList = wordsList[int(0):int(tagsMax)]

        returnValue = list()
        for v in slicedList:
            returnValue.append(v[1])

        return returnValue


    @staticmethod
    def getTagsStatic(sentences, userdic=None, filterFunc=None, tagsMax=3):
        sentences = sentences.replace('\n', '')
        komoran = Komoran(userdic=userdic)
        
        wordsMap = dict()
        # result = kkma.pos(sentences)
        result = komoran.pos(sentences)
        for v in result:
            # NN:명사, OL:외국어
            # if 'NN' in v[1] or 'OL' in v[1]:
            # NNG 일반명사   NNP 고유명사
            if 'NNP' == v[1] or 'NNG' == v[1]:
                if v[0] in wordsMap:
                    wordsMap[str(v[0])] = int(wordsMap[str(v[0])]) + 1
                else:
                    wordsMap[str(v[0])] = 1

        wordsList = list()
        for key, value in wordsMap.items():
            wordsList.append([value, key])

        if filterFunc is not None:
            filterFunc(wordsList)

        wordsList.sort(reverse=True)
        slicedList = wordsList[int(0):int(tagsMax)]

        returnValue = list()
        for v in slicedList:
            returnValue.append(v[1])

        return returnValue

if __name__ == "__main__":
    print(NLPManager.getTagsStatic('나는 아무런 생각이 없다. 왜냐하면 아무런 생각이 없기 때문이다.'))
    
        




class NLPManagerPoolBaseClass:
	pass

class NLPManagerPoolSingleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(NLPManagerPoolSingleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]


class NLPManagerPool(NLPManagerPoolBaseClass, metaclass=NLPManagerPoolSingleton):
    def __init__(self):
        log.info('Create NLPManagerPool ... ')
        self._lock = threading.Lock()

        self._map = dict()


    def createPool(self, threadName):
        with self._lock:
            self._map[threadName] = NLPManager()

    def get(self, threadName):
        with self._lock:
            return self._map[threadName]
