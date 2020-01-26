from pyquery import PyQuery as pq 
import urllib.request, urllib.error, urllib.parse
import datetime
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import time

date = str(datetime.datetime.now().date()).replace('-','')
KURL=f"https://killersports.com/nba/query?sdql=date%3D{date}+and+H&submit=++S+D+Q+L+%21++"
OPP_URL = "https://stats.nba.com/teams/opponent/?Season=2019-20&SeasonType=Regular%20Season&Location="
T_URL="https://stats.nba.com/teams/traditional/?Season=2019-20&SeasonType=Regular%20Season&Location="
CHROME_DRIVER_PATH = '../driver/chromedriver'
matchups = []

def get_stats(home_team, location, road_team):
	home_team_row = get_row(T_URL+"Home", home_team)
	home_team_opp_row = get_row(OPP_URL+"Home", home_team)
	road_team_row = get_row(T_URL+"Road", road_team)
	road_team_opp_row = get_row(OPP_URL+"Road", road_team)
	print(home_team_row)
	print(home_team_opp_row)
	print(road_team_row)
	print(road_team_opp_row)


def get_row(url, team1):
	browser = load_driver(url, "class")
	page = pq(browser.page_source)
	table = page("table")
	for i in table("tr").items():
		if team1 in i.text():
			return i.text().split()[6:]
	browser.quit()

def load_driver(url, by):
	chrome_options = Options()
	#chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument("disable-infobars")
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--disable-web-security")
	chrome_options.add_argument("--allow-running-insecure-content")
	browser = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_options)
	browser.get(url)
	if by == "name":
		wait = ui.WebDriverWait(browser,10).until(EC.presence_of_element_located((By.NAME, 'sdql')))
	elif by == "class":
		wait = ui.WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, "//table")))

	return browser

browser = load_driver(KURL, "name")

wait = ui.WebDriverWait(browser,10).until(EC.presence_of_element_located((By.NAME, 'sdql')))

try:
	page = pq(browser.page_source)
	table = page('#DT_Table')
	body = table('tbody')
	for row in body('tr').items():
		matchups.append([row('td').eq(4).text(), row('td').eq(5).text()])
except:
	print('error retrieving data')

for i in matchups:
	get_stats(i[0], "Home", i[1])
	break

print() 
