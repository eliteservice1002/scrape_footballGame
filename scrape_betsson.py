# -*- coding: utf-8 -*-

from __future__ import print_function


import sys
import csv
import time
import datetime
# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
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
options.add_argument("--start-maximized")
options.add_argument("window-size=1920,1080")
driver = webdriver.Chrome(options=options)


def query_betsson():
    print('in betsson')
    teamNames = []
    resArr = []
    try:
        url = "https://www.betsson.com/en/sportsbook/football/netherlands/netherlands-eredivisie"
        driver.get(url)
        driver.implicitly_wait(10) # seconds

        # print ("Headless Chrome Initialized")
        # print(driver.get_window_size())
        # driver.set_window_size(1920, 1080)
        # size = driver.get_window_size()
        # print("Window size: width = {}px, height = {}px".format(size["width"], size["height"]))

        time.sleep(5)
        lists = driver.find_elements_by_class_name(
            "obg-event-row-event-container")
        for list in lists:

            teams = list.find_elements_by_class_name("obg-event-info-participant-label")
            for team in teams:
                teamName = team.get_attribute("innerText")
                teamNames.append(teamName)

            results = list.find_elements_by_class_name("obg-numeric-change")
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
          end_data("betsson", team1, team2, result1, result2, resultX)

        driver.execute_script("window.scrollTo(0,700);")
        time.sleep(5)
        lists = driver.find_elements_by_class_name(
            "obg-event-row-event-container")
        
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
        print('betsson start')
        query_betsson()
        print('betsson done')

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
