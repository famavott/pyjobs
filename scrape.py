"""Module to scrape job postings."""
import csv

import os

from bs4 import BeautifulSoup

import requests

import yagmail


def indeed_search(query, cities):
    """Find jobs that match query passed."""
    for city in cities:
        indeed_url = (
            'https://www.indeed.com/jobs?as_and={0}'
            '&as_phr=&as_any=&as_not=&as_ttl=&as_cm'
            'p=&jt=fulltime&st=&sr=directhire&salar'
            'y=&radius=25&l={1}&fromage=1&limit=50&'
            'sort=date&psf=advsrch').format(query, city).replace(' ', '+')
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


# def send_email():
#     """Send csv to recipient."""
#     try:
#         yag = yagmail.SMTP(os.environ.get('gmail_user'), os.environ.get('gmail_pass'))
#         path = os.getcwd()
#         csv_attachment = path + '/csv/indeed.csv'
#         contents = ['The csv is attached. Open in Google Sheets.']
#         yag.send('keeley.favoino@gmail.com', "Indeed: Accounting Manager", contents, csv_attachment)
#     except Exception:
#         print('An error occured attempting to send the email.')


if __name__ == '__main__':
    cities = ['boise', 'chicago', 'denver']
    indeed_output(indeed_search('accounting manager', cities))
    # indeed_output(indeed_search(sys.argv[1], sys.argv[2]))
    # send_email()
