import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import pprint
import json
import csv
import pandas as pd




def main():
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    urls = {
        2009 : 'https://dblp.org/db/journals/tvcg/tvcg15.html',
        2010 : 'https://dblp.org/db/journals/tvcg/tvcg16.html',
        2011 : 'https://dblp.org/db/journals/tvcg/tvcg17.html',
        2012 : 'https://dblp.org/db/journals/tvcg/tvcg18.html',
        2013 : 'https://dblp.org/db/journals/tvcg/tvcg19.html',
        2014 : 'https://dblp.org/db/journals/tvcg/tvcg20.html',
        2015 : 'https://dblp.org/db/journals/tvcg/tvcg21.html',
        2016 : 'https://dblp.org/db/journals/tvcg/tvcg22.html',
        2017 : 'https://dblp.org/db/journals/tvcg/tvcg23.html',
        2018 : 'https://dblp.org/db/journals/tvcg/tvcg24.html',
        2019 : 'https://dblp.org/db/journals/tvcg/tvcg25.html'
    }

    year_list = []
    session_list = []
    title_list = []
    abstract_list = []
    author_list = []
    doi_list = []

    for i in range(2009, 2020):
        driver.get(urls[i])
        content = driver.page_source
        soup = BeautifulSoup(content,"lxml")
        li_list = soup.findAll("li",class_="entry article")
        cites = soup.findAll("cite")
        ul_list = soup.findAll("ul", class_="publ-list")

        print(len(li_list))
        print(len(cites))
        print(len(ul_list))


        for li in li_list:
            authors = li.find("cite").findAll("span",attrs={"itemprop": "author"})
            title = li.find("cite").find("span",class_="title").text
            doi = li.find("nav",class_="publ").find("a").get('href')
            authors_string = ""
            #print(title)
            #print(doi)

            for j in range(len(authors)):
                author_name = authors[j].find("span",attrs={"itemprop": "name"}).text
                if j < len(authors)-1:
                    authors_string += author_name + ","
                else:
                    authors_string += author_name

            #print(authors_string)
            #print("\n")
            year_list.append(i)
            session_list.append("N/A")
            title_list.append(title)
            abstract_list.append("N/A")
            author_list.append(authors_string)
            doi_list.append(doi)



    df = pd.DataFrame({'year': year_list, 'session': session_list, 'title': title_list,
                       'abstract': abstract_list, 'author': author_list, 'doi': doi_list})
    df.to_csv('tvcg_dblp_2009_2019.csv', index=False, encoding='utf-8')



if __name__ == '__main__':
    main()
