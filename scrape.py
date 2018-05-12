"""Module to scrape job postings."""
import csv

import datetime

import os

from bs4 import BeautifulSoup

import requests

import yagmail


def indeed_search(query, cities, pref_titles):
    """Find jobs that match query passed on indeed."""
    holder = []
    for city in cities:
        indeed_url = (r'https://www.indeed.com/jobs?as_and={0}'
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
        holder.append(city_info)

    combined_list = [item for sublist in holder for item in sublist]
    return filter_by_title(combined_list, pref_titles)


def builtin_search(pref_titles):
    """Find jobs from builtin Chicago."""
    cities = ['chicago']
    holder = []
    for city in cities:
        if city == 'chicago':
            builtin_url = (r'https://www.builtinchicago.org/jobs?f[0]=job-category_106')
            post_url = 'https://www.builtinchicago.org'
        r = requests.get(builtin_url)
        soup = BeautifulSoup(r.text, 'lxml')

        original = soup.find_all('div', class_='original')
        temp_dict = [{'link': post_url + x.a['href']} for x in original][3:]
        titles = [x.h2.text for x in original][3:]

        for div in soup.find_all('div', class_='original'):
            companies = [x.text for x in soup.find_all(class_='company-title')][3:]
            locations = [x.text for x in soup.find_all(class_='job-location')][3:]
            dates = [x.text for x in soup.find_all(class_='job-date')]

        [temp_dict[i].update({'company': companies[i]}) for i, x in enumerate(temp_dict)]
        [temp_dict[i].update({'title': titles[i]}) for i, x in enumerate(temp_dict)]
        [temp_dict[i].update({'location': locations[i]}) for i, x in enumerate(temp_dict)]
        [temp_dict[i].update({'date': dates[i]}) for i, x in enumerate(temp_dict)]
        city_dict = [x for x in temp_dict if 'hours' in x['date']]
        holder.append(city_dict)
    combined_list = [item for sublist in holder for item in sublist]
    return filter_by_title(combined_list, pref_titles)


def craigslist_search(pref_titles):
    """Find jobs from craigslist posted on day of search."""
    cl_url = r'https://chicago.craigslist.org/search/jjj?query=python&sort=date&postedToday=1'
    r = requests.get(cl_url)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find_all('li', class_='result-row')
    combined_list = []
    for job in results:
        target = job.find('a', class_='result-title hdrlnk')
        ind_dict = {}
        ind_dict['link'] = target['href']
        ind_dict['title'] = target.text
        combined_list.append(ind_dict)
    return filter_by_title(combined_list, pref_titles)


def matter_search(pref_titles):
    """Find jobs from mattter job board posted on day of search."""
    base_url = 'https://matter.health'
    matter_url = r'https://matter.health/job-board/#jobs'
    r = requests.get(matter_url)
    soup = BeautifulSoup(r.text, 'lxml')
    results = soup.find_all('div', class_='jobline')
    combined_list = []
    for job in results:
        ind_dict = {}
        ind_dict['link'] = base_url + job.a['href']
        ind_dict['title'] = job.find('p', class_='cappedLink').text
        ind_dict['company'] = job.find('div', class_='job__company').p.text
        combined_list.append(ind_dict)
    return filter_by_title(combined_list, pref_titles)


def filter_by_title(combined_list, pref_titles):
    """Include substrings of preferred titles to filter list."""
    final_list = []
    for dic in combined_list:
        for title in pref_titles:
            if title in dic['title'].lower():
                final_list.append(dic)
    return final_list


def dict_to_csv(csv_file, columns, final_list):
    """Write final_list dictionary results to csv file."""
    try:
        with open(csv_file, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            for data in final_list:
                writer.writerow(data)
    except IOError:
        print('I/O error')
    return


def send_email():
    """Send csv to recipient with yagmail."""
    try:
        yag = yagmail.SMTP(os.environ.get('gmail_user'), os.environ.get('gmail_pass'))
        date = f'{datetime.date.today():%m_%d}'
        csv_attachment = f'/Users/mfavoino/coding_practice/pyjobs/csv/{date}_roles.csv'
        contents = ['<h3>Open CSV in Google Sheets</h3>']
        yag.send('mattfavoino@gmail.com',
                 f'Job Results for {date}',
                 contents,
                 attachments=f'/Users/mfavoino/coding_practice/pyjobs/csv/{date}_roles.csv')
    except Exception:
        print('An error occured attempting to send the email.')


def output(final_list):
    """Call dict_to_csv and complete by sending email."""
    columns = ['title', 'link', 'company', 'location', 'date']
    date = f'{datetime.date.today():%m_%d}'
    csv_file = f'/Users/mfavoino/coding_practice/pyjobs/csv/{date}_roles.csv'

    # calls to write dictionary to csv
    dict_to_csv(csv_file, columns, final_list)


if __name__ == '__main__':
    pref_titles = ['python developer',
                   'software developer',
                   'software engineer',
                   'full-stack',
                   'python engineer',
                   'junior developer',
                   'junior software',
                   'backend devleoper',
                   'full stack']
    cities = ['chicago']

    indeed_results = indeed_search('python', cities, pref_titles)
    builtin_results = builtin_search(pref_titles)
    craigslist_results = craigslist_search(pref_titles)
    matter_results = matter_search(pref_titles)

    output(indeed_results)
    output(builtin_results)
    output(craigslist_results)
    output(matter_results)
    send_email()
