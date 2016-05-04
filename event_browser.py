# coding: utf-8
import time
import timeit

from flask import Flask, render_template

from mabed.corpus import Corpus
from mabed.mabed import MABED
from mabed import utils

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
elapsed = timeit.default_timer() - start_time
print('Top %d events detected in %f seconds.' % (k, elapsed))


# format data
event_descriptions = []
impact_data = []
formatted_dates = []
for i in range(0, mabed.corpus.time_slice_count):
    formatted_dates.append(int(time.mktime(mabed.corpus.to_date(i).timetuple()))*1000)
for event in mabed.events:
    mag = event[0]
    main_term = event[2]
    raw_anomaly = event[4]
    formatted_anomaly = []
    time_interval = event[1]
    related_terms = []
    for related_term in event[3]:
        related_terms.append(related_term[0]+' ('+str("{0:.2f}".format(related_term[1]))+')')
    event_descriptions.append((mag,
                               str(mabed.corpus.to_date(time_interval[0])),
                               str(mabed.corpus.to_date(time_interval[1])),
                               main_term,
                               ', '.join(related_terms)))
    for i in range(0, mabed.corpus.time_slice_count):
        value = 0
        if time_interval[0] <= i <= time_interval[1]:
            value = raw_anomaly[i]
        formatted_anomaly.append('['+str(formatted_dates[i])+','+str(value)+']')
    impact_data.append('{"key":"' + main_term + '", "values":[' + ','.join(formatted_anomaly) + ']}')

# instantiate a Flask Web server
app = Flask(__name__, static_folder='browser/static', template_folder='browser/templates')


@app.route('/')
def index():
    return render_template('template.html',
                           events=event_descriptions,
                           event_impact='['+','.join(impact_data) + ']',
                           k=k,
                           theta=theta,
                           sigma=sigma)

if __name__ == '__main__':
    # Access the browser at http://localhost:2016/
    app.run(debug=False, host='localhost', port=2016)
