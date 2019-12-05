import subprocess
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages")
from pyquery import PyQuery as pq 
import urllib.request, urllib.error, urllib.parse
import re
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime
import time
import csv
import psutil
from csv import reader, writer


CHROME_DRIVER_PATH = '../driver/chromedriver'

def initialize():	
	current_date = datetime.date.today()
	current_date += datetime.timedelta(days=-1)
	initial = sys.argv[1]
	if initial == 'init':
		date_time_str = '2019-12-04'
		date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d').date()
		open_page(date_time_obj, current_date)
	elif initial == 'comp':
		append_data()
	else:
		open_page(current_date, current_date)

def load_driver():
	url = f"https://killersports.com/nba/query"
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument("disable-infobars")
	chrome_options.add_argument("--disable-extensions")
	chrome_options.add_argument("--disable-web-security")
	chrome_options.add_argument("--allow-running-insecure-content")
	browser = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=chrome_options)
	browser.get(url)
	wait = ui.WebDriverWait(browser,10).until(EC.presence_of_element_located((By.NAME, 'sdql')))
	return browser

def append_data():
	m = open('../data/master/master.csv', 'w')
	writer = csv.writer(m)
	writer.writerow(['Date',
					 'Link',
					 'Day',
					 'Season',
					 'Team',
					 'Opp',
					 'Site',
					 'Final',
					 'Rest',
					 'Line',
					 'Total',
					 'SUm',
					 'ATSm',
					 'OUm',
					 'DPS',
					 'DPA',
					 'SUr',
					 'ATSr',
					 'OUr',
					 'ot'])
	for file in os.listdir("../data/sub"):
		if file.endswith('.csv'):
			reader = csv.reader(open(f"../data/sub/{file}", "r"), delimiter=" ")
			next(reader)
			for row in reader:
				writer.writerow(row)			
	print('done')

def open_page(starting_date, current_date):
	browser = load_driver()	
	while starting_date <= current_date:
		print(starting_date)
		date = starting_date.strftime("%Y%m%d").replace('-','')
		try:
			wait = ui.WebDriverWait(browser,10).until(EC.presence_of_element_located((By.NAME, 'sdql')))
			time.sleep(5)
			browser.find_element(By.NAME, 'sdql').send_keys(f'date={date}')
			submit_data = browser.find_element(By.NAME, 'submit').click()
			time.sleep(1)
		except Exception as e:
			print('could not submit data', e)
			starting_date += datetime.timedelta(days=1)

		try:
			browser.find_element(By.NAME, 'sdql').clear()
			record_table_xpath = '//table[@id="DT_Table"]'
			record_table = browser.find_element_by_xpath(record_table_xpath).text
			write_to_csv(record_table, date)
			submit_data = browser.find_element(By.NAME, 'submit').click()
			starting_date += datetime.timedelta(days=1)
		except:
			print('error', date)
			starting_date += datetime.timedelta(days=1)

def write_to_csv(row, date):
	row = row.split(' ')
	with open(f'../data/sub/{date}.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow(row)


initialize()
