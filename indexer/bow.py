# coding: utf-8
'''
Created on Apr 14, 2016

@author: dugue
'''


class WordFrequency:
    def __init__(self, word, frequency=1):
        self.__word = word
        self.frequency = frequency
        
    def increment_frequency(self):
        self.frequency += 1
    
    # For quick search in set
    def __hash__(self):
        return self.__word.__hash__()
    
    # For sort in set
    def __cmp__(self, other):
        if self.__word == other.__word:
            return 0
        else:
            value = self.frequency - other.frequency
            if value == 0:
                return self.__word.__hash__() - other.__word.__hash__()
            return value
    
    def get_word(self):
        return self.__word
    
    def get_frequency(self):
        return self.frequency
    
    #For quick search in set
    def __lt__(self, other):
        return self.__word.__hash__() < other.__word.__hash__()
    
    def __str__(self):
        return "{ "+self.__word+" , "+ str(self.frequency)+"} "
