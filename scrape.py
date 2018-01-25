"""Module to scrape job postings."""
import csv

import datetime

import os

from bs4 import BeautifulSoup

import requests

import yagmail


def indeed_search(query, cities, pref_titles):
    """Find jobs that match query passed on indeed."""
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

    combined_list = [item for sublist in info for item in sublist]
    return filter_by_title(combined_list, pref_titles)


def teamwork_search(pref_titles):
    """Find jobs that match query passed on teamwork online."""
    teamwork_url = (r'https://www.teamworkonline.com/jobs-in-sports'
                    '?utf8=%E2%9C%93&employment_opportunity_search%5Bquery%'
                    '5D=&employment_opportunity_search%5Blocation%5D%5Bname'
                    '%5D=&employment_opportunity_search%5Blocation%5D%5Badm'
                    'inistrative_division%5D=&employment_opportunity_search'
                    '%5Blocation%5D%5Blatitude%5D=&employment_opportunity_s'
                    'earch%5Blocation%5D%5Blongitude%5D=&employment_opportu'
                    'nity_search%5Bexclude_united_states_opportunities%5D=0'
                    '&employment_opportunity_search%5Bcategory_id%5D=332&co'
                    'mmit=Search&employment_opportunity_search%5Bcareer_level_id%5D=')
    post_url = 'https://www.teamworkonline.com'
    r = requests.get(teamwork_url)
    soup = BeautifulSoup(r.text, 'lxml')
    jobs = soup.find_all('li', class_='result-item')

    links = [x.a.attrs for x in jobs]
    final_dict = [{'link': post_url + x['href']} for x in links]
    companies = [x.find('div', class_='result-name').text for x in jobs]
    titles = [x.find('div', class_='result-position').text for x in jobs]

    [final_dict[i].update({'company': companies[i]}) for i, x in enumerate(final_dict)]
    [final_dict[i].update({'title': titles[i]}) for i, x in enumerate(final_dict)]
    return final_dict


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
    """Send csv to recipient."""
    try:
        yag = yagmail.SMTP(os.environ.get('gmail_user'), os.environ.get('gmail_pass'))
        date = f'{datetime.date.today():%m_%d}'
        csv_attachment = f'/Users/mfavoino/coding_practice/pyjobs/csv/{date}_indeed.csv'
        contents = ['<h3>Open CSV in Google Sheets</h3>']
        yag.send('mattfavoino@gmail.com',
                 f'Job Results for {date}',
                 contents,
                 attachments=f'/Users/mfavoino/coding_practice/pyjobs/csv/{date}_indeed.csv')
    except Exception:
        print('An error occured attempting to send the email.')


def output(final_list):
    """Call dict_to_csv and complete by sending email."""
    columns = ['title', 'link', 'company', 'location']
    date = f'{datetime.date.today():%m_%d}'
    csv_file = f'/Users/mfavoino/coding_practice/pyjobs/csv/{date}_indeed.csv'

    # calls to write dictionary to csv and then send email
    dict_to_csv(csv_file, columns, final_list)


if __name__ == '__main__':
    pref_titles = ['accounting manager', 'controller', 'financial reporting']
    cities = ['boise', 'chicago', 'denver']

    indeed_results = (indeed_search('accounting', cities, pref_titles))
    teamwork_results = teamwork_search(pref_titles)

    output(indeed_results)
    output(teamwork_results)
    send_email()
