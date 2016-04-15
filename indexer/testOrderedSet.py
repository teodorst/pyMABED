'''
Created on Apr 14, 2016

@author: dugue
'''
from sortedcontainers import  SortedSet
from bow import WordFrequency



w1=WordFrequency("le",200)
w2=WordFrequency("et",220)
w3=WordFrequency("a", 25)

wordSet=SortedSet()
wordSet.add(w3)
wordSet.add(w1)
wordSet.add(w2)
wordSet.add(w3)
wordSet.add(w3)
wordSet.add(w1)
wordSet.add(w2)
w3=WordFrequency("a", 21)
wordSet.add(w3)
w3=WordFrequency("b", 25)
wordSet.add(w3)
w3=WordFrequency("b", 20)
wordSet.add(w3)
w3=WordFrequency("ab", 25)
wordSet.add(w3)
_set="Set : "
for i in range(len(wordSet)):
    _set+= str(wordSet[i])
print _set+"\n"
    
w4=WordFrequency("ab", 1)
print w4, " in set ? ", w4 in wordSet, wordSet.index(w4)
w4=WordFrequency("ab", 200000)
print w4, " in set ? ",w4 in wordSet, wordSet.index(w4)
w4=WordFrequency("pooooop", 25)
print w4, " in set ? ", w4 in wordSet
w4=WordFrequency("le", 0)
print w4, " in set ? ",w4 in wordSet, "position : ", wordSet.index(w4)
w4=WordFrequency("le", 25)
print w4, " in set ? ",w4 in wordSet, "position : ", wordSet.index(w4)
wordSet[wordSet.index(w4)].increment_frequency()



w4=WordFrequency("le", 25)
wordSet.add(w4)
wordSet[wordSet.index(w4)].increment_frequency()

_set="Set : "
for i in range(len(wordSet)):
    _set+= str(wordSet[i])
print _set+"\n"

w4=WordFrequency("O", 0)
wordSet.add(w4)
wordSet[wordSet.index(w4)].increment_frequency()

_set="Set : "
for i in range(len(wordSet)):
    _set+= str(wordSet[i])
print _set+"\n"

