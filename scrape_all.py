# -*- coding: utf-8 -*-

from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import csv
import time
import datetime
# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


FIELD_NAME = ["site", "team1", "team2", "result1", "resultX", "result2","time"]
# selenium config
options = Options()
options.headless = True
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
# driver.set_page_load_timeout(10000)

def query_unibet():
    print('in unibet')
    teamNames = []
    resArr = []
    try:
        url = "https://www.unibet.com/betting/sports/filter/football/netherlands/matches"
        driver.get(url)
        driver.implicitly_wait(10) # seconds

        lists = driver.find_elements_by_class_name(
            "fa117")
        for list in lists:

            teams = list.find_elements_by_class_name("af24c")
            for team in teams:
                teamName = team.get_attribute("innerHTML")
                teamNames.append(teamName)

            results = list.find_elements_by_class_name("_5a5c0")

            for result in results:
                res = result.get_attribute("innerHTML")
                resArr.append(res)

        i=0
        while i < len(teamNames) / 2:
          team1 = teamNames[i * 2]
          team2 = teamNames[i * 2 + 1]
          result1 = resArr[i * 3]
          resultX = resArr[i * 3 + 1]
          result2 = resArr[i * 3 + 2]
          i+=1
          end_data("unibet", team1, team2, result1, result2, resultX)

        
    except Exception as e:
        print(u'error in response')
        print(e)
        pass

def query_bwin():
    print('in bwin')
    teamNames = []
    resArr = []
    try:
        url = "https://sports.bwin.com/en/sports/football-4/betting/netherlands-36/eredivisie-102847"
        driver.get(url)
        driver.implicitly_wait(10) # seconds
        time.sleep(5)
        lists = driver.find_elements_by_class_name(
            "grid-event-wrapper")
        for list in lists:

            teams = list.find_elements_by_class_name("participant-container")
            for team in teams:
                teamName = team.get_attribute("innerText")
                teamNames.append(teamName)

            results = list.find_elements_by_class_name("option-indicator")

            for result in results:
                res = result.get_attribute("innerText")
                resArr.append(res)

        i=0
        while i < len(teamNames) / 2:
          team1 = teamNames[i * 2]
          team2 = teamNames[i * 2 + 1]
          result1 = resArr[i * 3]
          resultX = resArr[i * 3 + 1]
          result2 = resArr[i * 3 + 2]
          i+=1
          end_data("bwin", team1, team2, result1, result2, resultX)

        
    except Exception as e:
        print(u'error in response')
        print(e)
        pass

def query_toto():
    print('in toto')
    teamNames = []
    resArr = []
    try:
        url = "https://sport.toto.nl/wedden/sport/1176/nederland-eredivisie/wedstrijden"
        driver.get(url)
        driver.implicitly_wait(10) # seconds

        # click accept cookie btn
        cookieBtn = driver.find_element_by_id('accept-cookie-consent')
        if cookieBtn:
            cookieBtn.click()
        # disable right panel
        rightPanel = driver.find_element_by_class_name('right-panels-group.my-bets--floating')
        if rightPanel:
            driver.execute_script("arguments[0].setAttribute('style', 'display:none')", rightPanel)
        # click see more button
        moreBtn = driver.find_elements_by_class_name('content-loader__load-more')
        if len(moreBtn):
            moreBtn[0].click()

        time.sleep(5)
        lists = driver.find_elements_by_class_name('event-list__item__content')

        # lists = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "event-list__item__content"))
        # )
        # print(len(lists))    
        for list in lists:

            teams = list.find_elements_by_class_name("event-card__body__name__home")
            teamName = teams[0].get_attribute("innerHTML")
            teamNames.append(teamName)

            teams = list.find_elements_by_class_name("event-card__body__name__away")
            teamName = teams[0].get_attribute("innerHTML")
            teamNames.append(teamName)

            results = list.find_elements_by_class_name("button--outcome__price")
            for result in results:
                res = result.get_attribute("innerHTML")
                resArr.append(res)

        i=0
        while i < len(teamNames) / 2:
          team1 = teamNames[i * 2]
          team2 = teamNames[i * 2 + 1]
          result1 = resArr[i * 3]
          resultX = resArr[i * 3 + 1]
          result2 = resArr[i * 3 + 2]
          i+=1
          end_data("toto", team1, team2, result1, result2, resultX)

        
    except Exception as e:
        print(u'error in response')
        print(e)
        pass


# write in csv file
def end_data(Name, team1, team2, result1, result2, resultX ):

    x = datetime.datetime.now()
    # print(x.strftime("%G%m%d%H%M%S"))
    with open('football.csv', "a", encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=FIELD_NAME)

        writer.writerow({
            'site': Name,
            'team1': team1,
            'team2': team2,
            'result1': result1,
            'resultX': resultX,
            'result2': result2,
            'time': x.strftime("%G%m%d%H%M%S")
        })

def main():

    try:
        query_unibet()
        print('unibet done')
        query_toto()
        print('toto done')
        query_bwin()
        print('bwin done')
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

    # close selenium
    driver.quit()

# main entry
if __name__ == '__main__':
    main()
