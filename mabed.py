# coding: utf-8
from corpus import Corpus
import numpy as np
import utils
import stats
import networkx as nx
from indexer.bow import WordFrequency

__authors__ = "Adrien Guille, Nicolas Dugué"
__email__ = "adrien.guille@univ-lyon2.fr"


class MABED:

    def __init__(self, corpus):
        self.corpus = corpus
        self.event_graph = None
        self.redundancy_graph = None

    def run(self, k=10, theta=0.6, sigma=0.5):
        basic_events = self.phase1()
        return self.phase2(basic_events, k, theta, sigma)

    def phase1(self):
        print 'Phase 1...'
        basic_events = []
        for w in range(0, len(self.corpus.vocabulary)):
            word = self.corpus.vocabulary[w].getWord()
            mention_freq = self.corpus.mention_freq[w, :]
            total_mention_freq = np.sum(mention_freq)
            anomaly = []
            for i in range(0, self.corpus.time_slice_count):
                anomaly.append(self.anomaly(i, mention_freq[i], total_mention_freq))
            interval_max = self.maximum_contiguous_subsequence_sum(anomaly)
            if interval_max is not None:
                mag = np.sum(anomaly[interval_max[0]:interval_max[1]])
                basic_event = (mag, interval_max, word, anomaly)
                basic_events.append(basic_event)
        print 'Phase 1: %d events' % len(basic_events)
        return basic_events

    def maximum_contiguous_subsequence_sum(self, anomaly):
        interval_list = []
        l_list = []
        r_list = []
        positive_anomaly = []
        for i in range(0, self.corpus.time_slice_count):
            pa = anomaly[i]
            if pa < 0:
                pa = 0
            positive_anomaly.append(pa)
            if anomaly[i] > 0:
                k = len(interval_list)
                l_k = 0
                r_k = np.sum(anomaly[:i])
                if i > 0:
                    l_k = np.sum(anomaly[:i-1])
                j = 0
                found_j = False
                for l in range(k, 0, -1):
                    if l_list[l-1] < l_k:
                        found_j = True
                        j = l-1
                if found_j and r_list[j] < r_k:
                    interval_k = (interval_list[j][0], i)
                    for p in range(j, k+1):
                        if len(interval_list) > 0:
                            interval_list.pop()
                        if len(l_list) > 0:
                            l_list.pop()
                        if len(r_list) > 0:
                            r_list.pop()
                    interval_list.append(interval_k)
                    l_list.append(np.sum(anomaly[:interval_k[0]-1]))
                    r_list.append(np.sum(anomaly[:interval_k[1]]))
                else:
                    interval_list.append((i, i))
                    l_list.append(l_k)
                    r_list.append(r_k)
        if len(interval_list) > 0:
            interval_max = interval_list[0]
            for (a, b) in interval_list:
                if np.sum(anomaly[a:b]) > np.sum(anomaly[interval_max[0]:interval_max[1]]):
                    interval_max = (a, b)
            return interval_max
        else:
            return None

    def phase2(self, basic_events, k=10, theta=0.7, sigma=0.5):
        print 'Phase 2...'
        basic_events.sort(key=lambda tup: tup[0])
        basic_events.reverse()
        self.event_graph = nx.DiGraph(name='Event graph')
        self.redundancy_graph = nx.Graph(name='Redundancy graph')
        i = 0
        unique_events = 0
        refined_events = []
        while unique_events < k and i < len(basic_events):
            basic_event = basic_events[i]
            main_word = basic_event[2]
            candidates_words = self.corpus.cooccurring_words(basic_event, 10)
            wf=WordFrequency(main_word)
            main_word_freq = self.corpus.global_freq[self.corpus.vocabulary.index(wf), :]
            related_words = []
            for candidate_word in candidates_words:
                cw = WordFrequency(candidate_word)
                candidate_word_freq = self.corpus.global_freq[self.corpus.vocabulary.index(cw), :]
                weight = (stats.erdem_correlation(main_word_freq, candidate_word_freq) + 1) / 2
                if weight > theta:
                    related_words.append((candidate_word, weight))
            if len(related_words) > 1:
                refined_event = (basic_event[0], basic_event[1], main_word, related_words, basic_event[3])
                if self.update_graphs(refined_event, sigma):
                    refined_events.append(refined_event)
                    unique_events += 1
            i += 1
        return self.merge_redundant_events(refined_events)

    def anomaly(self, time_slice, observation, total_mention_freq):
        expectation = float(self.corpus.tweet_count[time_slice]) * (float(total_mention_freq)/(float(self.corpus.size)))
        return observation - expectation

    def update_graphs(self, event, sigma):
        redundant = False
        main_word = event[2]
        print event
        if self.event_graph.has_node(main_word):
            for related_word, weight in event[3]:
                if self.event_graph.has_edge(main_word, related_word):
                    interval_0 = self.event_graph.node[related_word]['interval']
                    interval_1 = event[1]
                    if stats.overlap_coefficient(interval_0, interval_1) > sigma:
                        self.redundancy_graph.add_node(main_word, description=event)
                        self.redundancy_graph.add_node(related_word, description=event)
                        self.redundancy_graph.add_edge(main_word, related_word)
                        redundant = True
        if not redundant:
            self.event_graph.add_node(event[2], interval=event[1], main_term=True)
            for related_word, weight in event[3]:
                self.event_graph.add_edge(related_word, event[2], weight=weight)
        return not redundant

    def merge_redundant_events(self, events):
        components = []
        for c in nx.connected_components(self.redundancy_graph):
            components.append(c)
        final_events = []
        for event in events:
            main_word = event[2]
            main_term = main_word
            for component in components:
                if main_word in component:
                    main_term = ', '.join(component)
                    break
            final_event = (event[0], event[1], main_term, event[3], event[4])
            final_events.append(final_event)
            self.print_event(final_event)
        return final_events

    def print_event(self, event):
        related_words = []
        for related_word, weight in event[3]:
            related_words.append(related_word+'('+str("{0:.2f}".format(weight))+')')
        print '%s - %s: %s (%s)' % (self.corpus.to_date(event[1][0]), self.corpus.to_date(event[1][1]), event[2], ', '.join(related_words))

if __name__ == '__main__':
    '''
    my_corpus = Corpus('input/messages3.csv')
    my_corpus.discretize(30)
    utils.save_corpus(my_corpus, 'corpus/messages3.pickle')
    '''
    my_corpus = Corpus('input/messages1.csv')
    print 'Stop words:', my_corpus.stop_words
    print 'Corpus: %i tweets, spanning from %s to %s' % (my_corpus.size, my_corpus.start_date, my_corpus.end_date)
    print 'Vocabulary: %i unique tokens' % len(my_corpus.vocabulary)
    my_corpus.discretize(30)
    mabed = MABED(my_corpus)
    mabed.run(k=10, theta=0.6, sigma=0.6)
