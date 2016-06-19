# coding: utf-8

# std
import timeit
import argparse
import pickle

# mabed
from mabed.corpus import Corpus
from mabed.mabed import MABED

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Perform mention-anomaly-based event detection (MABED)')
    p.add_argument('i', metavar='input', type=str, help='Input csv file')
    p.add_argument('k', metavar='top_k_events', type=int, help='Number of top events to detect')
    p.add_argument('--o', metavar='output', type=str, help='Output pickle file', default=None)
    p.add_argument('--tsl', metavar='time_slice_length', type=int, help='Time-slice length, default to 30 (minutes)', default=30)
    p.add_argument('--p', metavar='p', type=int, help='Number of candidate words per event, default to 10', default=10)
    p.add_argument('--t', metavar='theta', type=float, help='Theta, default to 0.6', default=0.6)
    p.add_argument('--s', metavar='sigma', type=float, help='Sigma, default to 0.6', default=0.6)
    args = p.parse_args()

    print('Loading corpus...')
    start_time = timeit.default_timer()
    my_corpus = Corpus(args.i)
    elapsed = timeit.default_timer() - start_time
    print('Corpus loaded in %f seconds.' % elapsed)

    time_slice_length = args.tsl
    print('Partitioning tweets into %d-minute time-slices...' % time_slice_length)
    start_time = timeit.default_timer()
    my_corpus.discretize(time_slice_length)
    print('   Time-slices: %i' % my_corpus.time_slice_count)
    elapsed = timeit.default_timer() - start_time
    print('Partitioning done in %f seconds.' % elapsed)

    print('Running MABED...')
    k = args.k
    p = args.p
    theta = args.t
    sigma = args.s
    start_time = timeit.default_timer()
    mabed = MABED(my_corpus)
    mabed.run(k=k, p=p, theta=theta, sigma=sigma)
    mabed.print_events()
    elapsed = timeit.default_timer() - start_time
    print('Event detection performed in %f seconds.' % elapsed)

    if args.o is not None:
        pickle.dump(mabed, open(args.o, 'wb'))
        print('Events saved in %s' % args.o)
