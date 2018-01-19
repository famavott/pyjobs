"""Module to scrape job postings."""
import csv

import os

from bs4 import BeautifulSoup

import requests


def indeed_search(query, location):
    """Find jobs that match query passed."""
    indeed_url = 'http://www.indeed.com/jobs?q={0}&l={1}&sort=date&start='.format(query, location)
    post_url = 'http://www.indeed.com'
    r = requests.get(indeed_url)
    soup = BeautifulSoup(r.text, 'lxml')
    organic = soup.find_all('div', {'data-tn-component': 'organicJob'})

    companies = [x.span.text.strip() for x in organic]
    loc = soup.find_all('span', {'class': 'location'})
    locations = [x.text for x in loc]
    all_attrs = [x.h2.a.attrs for x in organic]
    info = [{'title': x['title'], 'link': post_url + x['href']} for x in all_attrs]

    # add company and location to info dictionary
    [info[i].update({'company': companies[i]}) for i, x in enumerate(info)]
    [info[i].update({'location': locations[i]}) for i, x in enumerate(info)]
    return info


def indeed_output(info):
    """Print jobs fetched from indeed to terminal."""
    columns = ['title', 'link', 'company', 'location']
    path = os.getcwd()
    csv_file = path + '/csv/indeed.csv'
    for dic in info:
        print('----------------------------')
        for key in dic:
            print('{}: {}'.format(key, dic[key]))
    dict_to_csv(csv_file, columns, info)


def dict_to_csv(csv_file, columns, info):
    """Write info dictionary results to csv file."""
    try:
        with open(csv_file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for data in info:
                writer.writerow(data)
    except IOError:
        print('I/O error')
    return


if __name__ == '__main__':
    import sys
    indeed_output(indeed_search(sys.argv[1], sys.argv[2]))
