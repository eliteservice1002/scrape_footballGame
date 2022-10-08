import sys
import csv
import time
import datetime
from urllib.error import HTTPError
# selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# selenium config
options = Options()
options.headless = True
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
# variable
lines = []
FIELD_NAME = ["time", "country", "country_abb", "competition", "site", "team1", "team2", "result1", "resultX", "result2"]

def query_unibet(url, country, country_abb, competition):
    teamNames = []
    resArr = []
    try:
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
          end_data("unibet", team1, team2, result1, result2, resultX, country, country_abb, competition)

        
    except Exception as e:
        print(u'error in unibet')
        print(e)
        pass

def query_bwin(url, country, country_abb, competition):
    teamNames = []
    resArr = []
    try:
        driver.get(url)
        driver.implicitly_wait(10) # seconds
        time.sleep(1)
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
          end_data("bwin", team1, team2, result1, result2, resultX, country, country_abb, competition)

    except Exception as e:
        print(u'error in bwin')
        print(e)
        pass

def query_toto(url, country, country_abb, competition):
    teamNames = []
    resArr = []
    try:
        driver.get(url)
        driver.implicitly_wait(10) # seconds

        try:
            # click accept cookie btn
            cookieBtn = driver.find_element_by_id('accept-cookie-consent')
            if cookieBtn:
                cookieBtn.click()
        except Exception as e:
            print(u'no cookie button, will continue')
            pass

        # disable right panel
        rightPanel = driver.find_element_by_class_name('right-panels-group.my-bets--floating')
        if rightPanel:
            driver.execute_script("arguments[0].setAttribute('style', 'display:none')", rightPanel)
        # count elements
        lists = driver.find_elements_by_class_name('event-list__item__content')
        length = len(lists)
        length1 = length

        # click see more button

        # element = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "content-loader__load-more")))
        # element.click()

        moreBtn = driver.find_elements_by_class_name('content-loader__load-more')
        if len(moreBtn):
            moreBtn[0].click()

        while length1 == length:
            time.sleep(1)
            lists = driver.find_elements_by_class_name('event-list__item__content')
            length1 = len(lists)

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
          end_data("toto", team1, team2, result1, result2, resultX, country, country_abb, competition)

        
    except Exception as e:
        print(u'error in toto')
        print(e)
        pass

def query_betsson(url, country, country_abb, competition):
    teamNames = []
    resArr = []
    try:
        driver.get(url)
        driver.implicitly_wait(10) # seconds

        # print ("Headless Chrome Initialized")
        # print(driver.get_window_size())
        # driver.set_window_size(1920, 1080)
        # size = driver.get_window_size()
        # print("Window size: width = {}px, height = {}px".format(size["width"], size["height"]))

        time.sleep(1)
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
          end_data("betsson", team1, team2, result1, result2, resultX, country, country_abb, competition)

        driver.execute_script("window.scrollTo(0,700);")
        time.sleep(1)
        lists = driver.find_elements_by_class_name(
            "obg-event-row-event-container")
        
    except Exception as e:
        print(u'error in betsson')
        print(e)
        pass

# write in csv file
def end_data(name, team1, team2, result1, result2, resultX, country, country_abb, competition ):

    x = datetime.datetime.now()
    with open('football_v2.csv', "a", encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=FIELD_NAME)

        writer.writerow({
            'time': x.strftime("%G%m%d%H%M%S"),
            'country':country,
            'country_abb':country_abb,
            'competition':competition,
            'site': name,
            'team1': team1,
            'team2': team2,
            'result1': result1,
            'resultX': resultX,
            'result2': result2
        })
    print('end_data')

def main():

    try:
        with open("links_test.csv", "r") as f:
            reader = csv.reader(f, delimiter="\t")
            for i, line in enumerate(reader):
                lines.append(line[0])
        for line in lines:
            fields = line.split(',')
            print(fields)
            site_name = fields[0]
            country_abb = fields[1]
            country = fields[2]
            competition = fields[3]
            site_url = fields[4]

            if site_name == 'Toto':
                query_toto(site_url, country, country_abb, competition)
            elif site_name == 'Unibet':
                query_unibet(site_url, country, country_abb, competition)
            elif site_name == 'Bwin':
                query_bwin(site_url, country, country_abb, competition)
            elif site_name == 'Betsson':
                query_betsson(site_url, country, country_abb, competition)
            else:
                continue
            
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