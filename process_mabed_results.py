import pickle
import re
import sys
import json


event_regex = '(.+?) - (.+?): (.+?) \((.*?)\)\)'
related_word_regex = '(.+?)\((0\.\d+)'


def process_related_word(related_word):

    match = re.match(related_word_regex, related_word)
    if not match:
        print('error parsing related word: %s', related_word)
        sys.exit(1)

    word = match.group(1)
    magnitude = match.group(2)
    return word.strip(), magnitude


def get_events(mabed_events):
    stdout_ = sys.stdout #Keep track of the previous value.
    sys.stdout = open('tmp_file.txt', 'w') # Something here that provides a write method.
    mabed_events.print_events()
    # calls to print, ie import module1
    sys.stdout = stdout_ # restore the previous stdout.

    events = []
    with open('tmp_file.txt', 'r') as f:
        events = f.readlines()[1:]

    return events


if __name__ == '__main__':
    with open('results.pickle', 'rb') as pickle_in:
        mabed_results = pickle.load(pickle_in)
        events = get_events(mabed_results)

    if not events:
        print('no events found')

    processed_events = []
    for event in events:
        match = re.search(event_regex, event)
        if not match:
            print('error parsing event: %s', event)

        start_date = match.group(1).strip()
        end_date = match.group(2).strip()
        main_words_group = match.group(3)
        main_words = [word.strip() for word in main_words_group.split(',')]
        related_words = [process_related_word(related_word) for related_word in match.group(4).split(',')]

        processed_events.append({'start_date': start_date, 'end_date': end_date, 'main_words': main_words,
                                 'related_words': [{'word': r_w[0],
                                                    'magnitude': r_w[1]} for r_w in related_words]})

    print(processed_events)

    with open('events.json', 'w') as f:
        json.dump(processed_events, f)
