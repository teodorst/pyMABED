# coding: utf-8

# std
import time
import argparse
import os

# web
from flask import Flask, render_template
from flask_frozen import Freezer

# mabed
import mabed.io as io

__author__ = "Adrien Guille"
__email__ = "adrien.guille@univ-lyon2.fr"

event_browser = Flask(__name__, static_folder='browser/static', template_folder='browser/templates')


@event_browser.route('/')
def index():
    print(event_descriptions)
    return render_template('template.html',
                           events=event_descriptions,
                           event_impact='[' + ','.join(impact_data) + ']',
                           k=mabed.k,
                           theta=mabed.theta,
                           sigma=mabed.sigma)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Build event browser')
    p.add_argument('i', metavar='input', type=str, help='Input pickle file')
    p.add_argument('--o', metavar='output', type=str, help='Output html directory', default=None)
    args = p.parse_args()
    mabed = io.load_events(args.i)

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
                if value < 0:
                    value = 0
            formatted_anomaly.append('['+str(formatted_dates[i])+','+str(value)+']')
        impact_data.append('{"key":"' + main_term + '", "values":[' + ','.join(formatted_anomaly) + ']}')

    event_browser.run(debug=False, host='localhost', port=2016)

    if args.o is not None:
        os.makedirs(args.o)
        print('Freezing event browser...')
        event_browser_freezer = Freezer(event_browser)
        event_browser.debug = False
        event_browser.config['ASSETS_DEBUG'] = False
        event_browser_freezer.freeze()
        print('Done.')
