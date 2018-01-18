"""Module to scrape job postings."""
from bs4 import BeautifulSoup

import requests


def indeed_search(query, location):
    """Find jobs that match query passed."""
    print('Be patient.')
    indeed_url = 'http://www.indeed.com/jobs?q={0}&l={1}&sort=date&start='.format(query, location)
    r = requests.get(indeed_url + query)
    soup = BeautifulSoup(r.text, 'lxml')
    organic = soup.find_all('div', {'data-tn-component': 'organicJob'})
    companies = [x.span.text.strip() for x in organic]
    details = [x.h2.a.attrs for x in organic]
    [details[i].update({'company': companies[i]}) for i, x in enumerate(details)]

    company = [x['company'] for x in details]
    title = [x['title'] for x in details]
    link = [x['href'] for x in details]

    for i in range(len(company)):
        print('Company: ' + company[i])
        print('Title: ' + title[i])
        print('Link: ' + indeed_url + link[i])

    # for dic in details:
    #     while :
    #         print('Company: ' + dic['company'])
    #         print('Title: ' + dic['title'])
    #         print('Link: ' + indeed_url + dic['href'])


if __name__ == '__main__':
    import sys
    indeed_search(sys.argv[1], sys.argv[2])
