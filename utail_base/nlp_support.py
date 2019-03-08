# -*- coding: utf-8 -*-
# nlp_support

from konlpy.tag import Kkma

class NLPManager:
    def __init__(self, idx):
        self._idx = idx
        self._kkma = Kkma()

    def getTags(self, sentences, tagsMax=3):
        wordsMap = dict()
        result = self._kkma.pos(sentences)
        for v in result:
            # NN:명사, OL:외국어
            if 'NN' in v[1] or 'OL' in v[1]:
                if v[0] in wordsMap:
                    wordsMap[v[0]] = wordsMap[v[0]] + 1
                else:
                    wordsMap[v[0]] = 1

        wordsList = list()
        for key, value in wordsMap.items():
            wordsList.append([value, key])

        wordsList.sort(reverse=True)
        return wordsList[0:tagsMax]

    @staticmethod
    def getTagsStatic(sentences, tagsMax=3):
        kkma = Kkma()
        wordsMap = dict()
        result = kkma.pos(sentences)
        for v in result:
            # NN:명사, OL:외국어
            if 'NN' in v[1] or 'OL' in v[1]:
                if v[0] in wordsMap:
                    wordsMap[v[0]] = wordsMap[v[0]] + 1
                else:
                    wordsMap[v[0]] = 1

        wordsList = list()
        for key, value in wordsMap.items():
            wordsList.append([value, key])

        wordsList.sort(reverse=True)
        return wordsList[0:tagsMax]


if __name__ == "__main__":
    print(NLPManager.getTagsStatic('나는 아무런 생각이 없다. 왜냐하면 아무런 생각이 없기 때문이다.'))
    
        
