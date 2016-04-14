# coding: utf-8
import nltk
from nltk.corpus import stopwords
import pandas
import numpy as np
import re
import string
from datetime import timedelta
#To sort words according to their frequency
from sortedcontainers import  SortedSet
from indexer.bow import WordFrequency

__authors__ = "Adrien Guille, Nicolas Dugué"
__email__ = "adrien.guille@univ-lyon2.fr"


class Corpus:
    MAX_FEATURES = 5000
    TWITTER_TOKENS = ['rt', 'via', '@', '..', '...']
    LANGUAGE = 'english'

    def __init__(self, source_file_path, min_absolute_frequency=4, max_relative_frequency=0.5):
        self.stop_words = self.TWITTER_TOKENS
        self.stop_words.extend(list(string.punctuation))
        self.stop_words.extend(stopwords.words(self.LANGUAGE))
        print 'Stop words:', self.stop_words
        self.df = pandas.read_csv(source_file_path, sep='\t', encoding='utf-8')
        self.df['date'] = pandas.to_datetime(self.df.date)
        self.size = self.df.count(0)[0]
        self.start_date = self.df['date'].min()
        self.end_date = self.df['date'].max()
        print 'Corpus: %i tweets, spanning from %s to %s' % (self.size, self.start_date, self.end_date)
        
        #A SortedSet of WordFrequency that are tuple (words, frequency)
        self.vocabulary=SortedSet()
        
        for i in range(0, self.size):
            #Remove links
            text = re.sub(r'(?:https?\://)\S+', '', self.df.iloc[i]['text'])
            self.df.loc[i, 'text'] = text
            words = self.tokenize(text)
            for word in set(words):
                #remove stop words
                if word not in self.stop_words:
                    wf=WordFrequency(word)
                    #If wf is already in the vocabulary, it won't be added again. Otherwise it will be added with frequency=0 
                    self.vocabulary.add(wf)
                    #Add 1 to the frequency
                    self.vocabulary[self.vocabulary.index(wf)].incrFrequecy()
                    
        print 'Complete vocabulary: %i unique words' % len(self.vocabulary)
        #We delete the less frequent words to keep MAX_FEATURES words as features
        if len(self.vocabulary) > self.MAX_FEATURES:
            for i in range(self.MAX_FEATURES, len(self.vocabulary)):
                del self.vocabulary[len(self.vocabulary) - 1]
                
        print 'Pruned vocabulary: %i unique words' % len(self.vocabulary)
        self.time_slice_count = None
        self.tweet_count = None
        self.global_freq = None
        self.mention_freq = None
        self.time_slice_length = None

    def discretize(self, time_slice_length):
        self.time_slice_length = time_slice_length
        time_delta = (self.end_date - self.start_date)
        time_delta = time_delta.total_seconds()/60
        self.time_slice_count = int(time_delta/float(time_slice_length)) + 1
        self.tweet_count = np.zeros(self.time_slice_count, dtype=np.int)
        self.global_freq = np.zeros((len(self.vocabulary), self.time_slice_count), dtype=np.short)
        self.mention_freq = np.zeros((len(self.vocabulary), self.time_slice_count), dtype=np.short)
        self.df['time_slice'] = 0
        print 'Time-slices: %i' % self.time_slice_count
        for i in range(0, self.size):
            tweet_date = self.df.iloc[i]['date']
            time_delta = (tweet_date - self.start_date)
            time_delta = time_delta.total_seconds()/60
            time_slice = int(time_delta/time_slice_length)
            self.df.loc[i, 'time_slice'] = time_slice
            self.tweet_count[time_slice] = self.tweet_count.item(time_slice) + 1
            words = self.tokenize(self.df.iloc[i]['text'])
            mention = '@' in words
            for word in set(words):
                wf=WordFrequency(word)
                if wf in self.vocabulary:
                    row = self.vocabulary.index(wf)
                    column = time_slice
                    self.global_freq[row, column] = self.global_freq.item((row, column)) + 1
                    if mention:
                        self.mention_freq[row, column] = self.mention_freq.item((row, column)) + 1

    def cooccurring_words(self, event, p):
        main_word = event[2].getWord().replace(')', '').replace('(', '')
        filtered_df_0 = self.df.loc[self.df['time_slice'].isin(range(event[1][0], event[1][1]))]
        filtered_df = filtered_df_0.loc[filtered_df_0['text'].str.contains(main_word)]
        tmp_vocabulary = {}
        for i in range(0, filtered_df.count(0)[0]):
            words = self.tokenize(filtered_df.iloc[i]['text'])
            for word in set(words):
                wf=WordFrequency(word)
                if wf in self.vocabulary:
                    word_frequency = 0
                    if tmp_vocabulary.get(word) is not None:
                        word_frequency = tmp_vocabulary.get(word)
                    word_frequency += 1
                    tmp_vocabulary[word] = word_frequency
        freq = []
        for word, frequency in tmp_vocabulary.iteritems():
            freq.append((word, frequency))
        freq.sort(key=lambda tup: tup[1])
        freq.reverse()
        top_cooccurring_words = []
        for i in range(1, p):
            top_cooccurring_words.append(freq[i][0])
        return top_cooccurring_words

    def to_date(self, time_slice):
        a_date = self.start_date + + timedelta(minutes=time_slice*self.time_slice_length)
        return str(a_date)

    @staticmethod
    def tokenize(text):
        tokens = nltk.wordpunct_tokenize(text)
        text = nltk.Text(tokens)
        words = [w.lower() for w in text]
        return words

if __name__ == '__main__':
    my_corpus = Corpus('/Users/adrien/Desktop/messages1.csv')
    my_corpus.discretize(30)
