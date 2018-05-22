[![Build Status](https://travis-ci.org/famavott/pyjobs.svg?branch=master)](https://travis-ci.org/famavott/pyjobs)

Job Scraper
---
### Description

A simple scraper for job postings from Indeed, Craigslist, Built In Chicago, 1871, and Matter. Provided a search term to query, cities, and substrings to look for in the job title, it writes the results to a csv, and then emails it to a recipient using yagmail.

The script excludes sponsored postings, includes jobs within a 25 radius of the provided cities, and only grabs postings from the last day.

Can easily be setup as a cron job to run on a schedule.

### Author
---
* [famavott](https://github.com/famavott/pyjobs)

### Dependencies
---
* requests
* bs4 (BeautifulSoup)
* yagmail

### Getting Started
---
##### *Prerequisites*
* [python (3.6+)](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/)
* [git](https://git-scm.com/)

##### *Installation*
First, clone the project repo from Github. Then, change directories into the cloned repository. To accomplish this, execute these commands:

`$ git clone https://github.com/famavott/pyjobs.git`

`$ cd pyjobs`

Now now that you have cloned your repo and changed directories into the project, create a virtual environment named "ENV", and install the project requirements into your environment.

`$ python3 -m venv ENV`

`$ source ENV/bin/activate`

`$ pip install -r requirements.txt`

Manipulate the search terms in the `if __name__ == '__main__'`
block, and then call the script from the command line.

### License
---
This project is licensed under MIT License - see the LICENSE.md file for details.

*This README was generated using [writeme.](https://github.com/chelseadole/write-me)*
