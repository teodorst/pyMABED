# coding: utf-8
from mabed import MABED
from corpus import Corpus
from flask import Flask, render_template
import time, datetime

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

# load and prepare a tweet corpus
my_corpus = Corpus('input/messages2.csv')
my_corpus.discretize(120)
print 'Stop words:', my_corpus.stop_words
print 'Corpus: %i tweets, spanning from %s to %s' % (my_corpus.size, my_corpus.start_date, my_corpus.end_date)
print 'Vocabulary: %i unique tokens' % len(my_corpus.vocabulary)

# run MABED
mabed = MABED(my_corpus)
events = mabed.run(k=10, theta=0.6, sigma=0.6)

# instantiate a Flask Web server
app = Flask(__name__, static_folder='browser/static', template_folder='browser/templates')

# format data
js_elements = []
formatted_dates = []
for i in range(0, my_corpus.time_slice_count):
    formatted_dates.append(long(time.mktime(my_corpus.to_date(i).timetuple())))
for event in events:
    main_term = event[2]
    raw_anomaly = event[4]
    formatted_anomaly = []
    time_interval = event[1]
    for i in range(0, my_corpus.time_slice_count):
        value = 0
        if time_interval[0] <= i <= time_interval[1]:
            value = raw_anomaly[i]
        formatted_anomaly.append('['+str(formatted_dates[i])+','+str(value)+']')
    js_elements.append('{"key":"'+main_term+'", "values":['+','.join(formatted_anomaly)+']}')


@app.route('/')
def index():
    return render_template('event_impact.html', event_impact='['+','.join(js_elements)+']')

if __name__ == '__main__':
    # Access the browser at http://localhost:2016/
    app.run(debug=True, host='localhost', port=2016)
