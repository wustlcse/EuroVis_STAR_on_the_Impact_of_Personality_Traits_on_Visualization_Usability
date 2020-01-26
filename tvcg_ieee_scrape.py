import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pprint
import json
import csv
import re
import pandas as pd


def main():
    year_list = []
    session_list = []
    title_list = []
    abstract_list = []
    author_list = []
    doi_list = []
    driver = webdriver.Chrome("/usr/local/bin/chromedriver")
    #issuetry = open("issuetry.txt","x")
    driver.get("https://ieeexplore.ieee.org/xpl/issues?punumber=2945&isnumber=8946776")
    issue_link_list = []
    for i in reversed(range(2,13)):
        current_xpath = "/html/body/div[5]/div/div/div/div[5]/div[2]/xpl-root/div/xpl-xpl-delegate/xpl-journals/div/div[1]/div[3]/section/xpl-past-issue/section/div/div[1]/div/div[2]/ul/li[" + str(i) +"]"
        current_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, current_xpath)))
        current_element.click()
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        for issue_link in soup.find("div", class_="u-mt-2 issue-list").findAll("a"):
            issue_link_list.append("https://ieeexplore.ieee.org" + issue_link.get('href'))
    #print(*issue_link_list, sep = "\n")
    wait = WebDriverWait(driver, 20)
    for i in range(len(issue_link_list)):
        driver.get(issue_link_list[i])
        popular_as_pin_xpath = "/html/body/div[5]/div/div/div/div[5]/div[2]/xpl-root/div/xpl-xpl-delegate/xpl-journals/div/div[1]/div[3]/section/xpl-journal-toc/div/div[2]/div/xpl-issue-search-results/main/div[1]/xpl-issue-search-dashboard/div/div[2]/div[1]/div/div/span[1]"
        popular_as_pin_element = wait.until(EC.presence_of_element_located((By.XPATH, popular_as_pin_xpath)))
        content = driver.page_source
        soup = BeautifulSoup(content, "lxml")
        #issuetry.write(content)
        papers = soup.find_all("div",class_="List-results-items")
        for paper in papers:
            title = paper.find("h2").select_one('[xplmathjax]').text
            doi = paper.find("h2").select_one('[xplmathjax]').get('href')
            if doi is None:
                doi = "No doi"
            year = paper.find("span",string=re.compile("Year")).text[-4:]
            authors = paper.find("xpl-authors-name-list").find_all("a")
            #abstract = paper.select_one('div.js-displayer-content.u-mt-1.stats-SearchResults_DocResult_ViewMore')
            abstract = paper.find('div',class_='stats-SearchResults_DocResult_ViewMore')
            authors_string = ""
            abstract_text = ""
            if abstract is not None:
                abstract_text = abstract.find("span").string
            else:
                abstract_text = "No Abstract"
            for author in authors:
                author_text = author.find("span").text
                authors_string += author_text+","
            year_list.append(year)
            session_list.append("No Sessions")
            title_list.append(title)
            abstract_list.append(abstract_text)
            author_list.append(authors_string)
            #print(doi)
            doi_list.append("https://ieeexplore.ieee.org"+doi)
            #https://ieeexplore.ieee.org/xpl/tocresult.jsp?isnumber=6479163&punumber=2945
    df = pd.DataFrame({'year': year_list, 'session': session_list, 'title': title_list,
                       'abstract': abstract_list, 'author': author_list, 'doi': doi_list})
    df.to_csv('tvcg_ieee_digitallibrary_2009_2019.csv', index=False, encoding='utf-8')





























if __name__ == '__main__':
        main()