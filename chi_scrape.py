import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import pprint
import json
import csv


def main():
    filepath = './acm-iui-2016.html'
    iui = []
    """  for CHI """

    urls = {
        2019 : 'https://dl.acm.org/citation.cfm?id=3290605&preflayout=flat',
        2018 : 'https://dl.acm.org/citation.cfm?id=3173574&preflayout=flat',
        2017 : 'https://dl.acm.org/citation.cfm?id=3025453&preflayout=flat',
        2016 : 'https://dl.acm.org/citation.cfm?id=2858036&preflayout=flat',
        2015 : 'https://dl.acm.org/citation.cfm?id=2702123&preflayout=flat',
        2014 : 'https://dl.acm.org/citation.cfm?id=2556288&preflayout=flat',
        2013 : 'https://dl.acm.org/citation.cfm?id=2470654&preflayout=flat',
        2012 : 'https://dl.acm.org/citation.cfm?id=2207676&preflayout=flat',
        2011 : 'https://dl.acm.org/citation.cfm?id=1978942&preflayout=flat',
        2010 : 'https://dl.acm.org/citation.cfm?id=1753326&preflayout=flat',
        2009 : 'https://dl.acm.org/citation.cfm?id=1518701&preflayout=flat'
    }

    driver = webdriver.Chrome("/usr/local/bin/chromedriver")

    for i in range(2009, 2020):
        driver.get(urls[i])
        content = driver.page_source
        data = get_data(content.split('\n'), i)
        iui.append({
            'year': i,
            'papers': data[0],
            'count': data[1]
        })
        # pprint.pprint(json.dumps(iui))

    # write json file
    f = open("chi2009-2019.json", "w")
    f.write(json.dumps(iui))
    f.close()

    # write cvs file
    fields = ['year', 'session', 'title', 'abstract', 'authors', 'doi']

    output = csv.writer(open('chi2009-2019.csv', 'w'))
    output.writerow(fields)
    for year in iui:
        for paper in year['papers']:
            paper['authors'] = ','.join(paper['authors'])
            output.writerow([paper[key] for key in fields if key in paper])

    # soup_page = BeautifulSoup(content)
    # print(soup_page.prettify())

    # f = open(filepath, "r")
    # content = f.read()
    # print(content)


def get_data(content, year):
    papers = []
    count = 0
    paper_count = 0
    reading = False
    current_session = ''

    while count < len(content):

        line = content[count]

        # ignore everything before this
        if line.find('SESSION') != -1:
            reading = True
            current_session = BeautifulSoup(line, 'lxml').find('strong').text

        if year==2019 and line.find('Translational') != -1:
            reading = True
            current_session = "None"


        if not reading:
            count += 1
            continue

        if line.find('citation.cfm') != -1 and line.find('padding-left:20'):
            # new paper
            title = BeautifulSoup(line, 'lxml').text.strip()
            # print(title)
            papers.append(
                {
                    'year': year,
                    'authors': [],
                    'title': title,
                    'abstract': '',
                    'doi': '',
                    'session': current_session
                }
            )
            done = False

            while count < len(content) and not done:

                # print("Line {}: {}".format(count, line.strip()))

                if line.find('SESSION') != -1:
                    current_session = BeautifulSoup(line, 'lxml').find('strong').text


                line = content[count]
                count += 1

                soup = BeautifulSoup(line, 'lxml')
                # print(soup)
                if (line.find('author_page') != -1):
                    papers[paper_count]['authors'].append(soup.text.strip().replace(',', ''))
                if (line.find('doi.org') != -1):
                    papers[paper_count]['doi'] = soup.find('a')['href'].strip()
                if (line.find('toHide') != -1):
                    papers[paper_count]['abstract'] = soup.text.replace('expand', '').strip()
                    done = True
            # print(papers[paper_count])
            paper_count += 1

        count += 1
    return papers, paper_count


if __name__ == '__main__':
    main()

