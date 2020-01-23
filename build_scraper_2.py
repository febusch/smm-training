import requests
from bs4 import BeautifulSoup
from math import floor
from datetime import datetime, timedelta


def main():
    """
    Use this function to build are scraper for suedostschweizjobs.ch.
    The objective is to print the number of ads in the past 7 days.
    To achieve this, with the 'requests' and the 'bs4' modules.

    In this example, we have to iterate over pages. Parsing of HTML code has to be done.
    """

    max_page_count = get_max_page_count()

    jobs = []

    for i in range(max_page_count):

        print("{}%\tFound {} job(s)".format(int(i/max_page_count*100), len(jobs)))
        current_page = page_source(i)
        articles = current_page.find_all('article')

        for article in articles:
            article = article.find('div', {'class': 'job__content clearfix'})

            date = article.find('span', {'class': 'date'}).text
            date = date.strip().replace(",", "")
            date = datetime.strptime(date, '%d.%m.%Y').date()

            a_week_ago = datetime.now().date() - timedelta(days=7)

            if date >= a_week_ago:

                job = {
                    "startDate": str(date),
                    "title": article.find('a', {'class': 'recruiter-job-link'}).text,
                    "url": article.find('a').get('href')
                }

                try:
                    job["location"] = article.find('div',  {'class': 'location'}).text.replace("\n", "")

                except AttributeError:
                    job["location"] = None

                try:
                    job["recruiter"] = article.find('span',  {'class': 'recruiter-company-profile-job-organization'}).text.replace("\n", ""),

                except AttributeError:
                    job["recruiter"] = None

                jobs.append(job)

    return jobs


def page_source(n):

    page = requests.get('https://www.suedostschweizjobs.ch/jobs?page=' + str(n)).text
    source = BeautifulSoup(page, "lxml")

    return source


def get_max_page_count():

    soup = page_source(0)

    job_count_string = soup.find('h1', {'class': 'search-result-header'}).text
    job_count_int = int(job_count_string.replace(" Jobs", "").replace("'", ""))
    job_count = floor(job_count_int / 20)

    return job_count


if __name__ == '__main__':

    allJobs = main()
    print(len(allJobs))
    print(allJobs)
