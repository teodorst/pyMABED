# coding: utf-8
import timeit
from mabed.corpus import Corpus
from mabed.mabed import MABED

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

print('Loading corpus...')
start_time = timeit.default_timer()
my_corpus = Corpus('input/messages3.csv')
elapsed = timeit.default_timer() - start_time
print('Corpus loaded in %f seconds.' % elapsed)

time_slice_length = 30
print('Partitioning tweets into %d-minute time-slices...' % time_slice_length)
start_time = timeit.default_timer()
my_corpus.discretize(time_slice_length)
print('   Time-slices: %i' % my_corpus.time_slice_count)
elapsed = timeit.default_timer() - start_time
print('Partitioning done in %f seconds.' % elapsed)

print('Running MABED...')
k = 10
theta = 0.6
sigma = 0.6
start_time = timeit.default_timer()
mabed = MABED(my_corpus)
mabed.run(k=k, theta=theta, sigma=sigma)
mabed.print_events()
elapsed = timeit.default_timer() - start_time
print('Event detection performed in %f seconds.' % elapsed)
