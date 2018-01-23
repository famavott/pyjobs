"""Module to scrape job postings."""
import csv

import datetime

import os

from bs4 import BeautifulSoup

import requests

import yagmail


def indeed_search(query, cities):
    """Find jobs that match query passed."""
    info = []
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
        city_info = [{'title': x['title'], 'link': post_url + x['href']} for x in all_attrs]

        # add company and location to city_info dictionary
        [city_info[i].update({'company': companies[i]}) for i, x in enumerate(city_info)]
        [city_info[i].update({'location': locations[i]}) for i, x in enumerate(city_info)]
        info.append(city_info)
    final_list = info[0] + info[1]
    return final_list


def indeed_output(final_list):
    """Print jobs fetched from indeed to terminal."""
    jobs_for_email = []
    columns = ['title', 'link', 'company', 'location']
    path = os.getcwd()
    date = f'{datetime.date.today():%m_%d}'
    csv_file = path + f'/csv/{date}_indeed.csv'
    for dic in final_list:
        for key in dic:
            jobs_for_email.append('{}: {}'.format(key, dic[key]))
    jobs_string = '\n\n'.join(jobs_for_email)

    # calls to write dictionary to csv and then send email
    dict_to_csv(csv_file, columns, final_list)
    send_email(jobs_string)


def dict_to_csv(csv_file, columns, final_list):
    """Write final_list dictionary results to csv file."""
    try:
        with open(csv_file, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for data in final_list:
                writer.writerow(data)
    except IOError:
        print('I/O error')
    return


def send_email(jobs_string):
    """Send csv to recipient."""
    try:
        yag = yagmail.SMTP(os.environ.get('gmail_user'), os.environ.get('gmail_pass'))
        path = os.getcwd()
        date = f'{datetime.date.today():%m_%d}'
        csv_attachment = path + f'/csv/{date}_indeed.csv'
        contents = ['<h3>Open CSV in Google Sheets</h3>']
        yag.send('mattfavoino@gmail.com',
                 f'Indeed Jobs for {date}',
                 contents,
                 attachments=csv_attachment)
    except Exception:
        print('An error occured attempting to send the email.')


if __name__ == '__main__':
    indeed_output(indeed_search('software engineer', ['chicago', 'denver']))
