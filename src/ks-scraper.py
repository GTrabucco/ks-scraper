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
from datetime import date

NCAABB_QUERIES = ['season>=2016 and rank > 11 and o:rank = None and H and conference = B10 and line > -8',
'season>=2016 and rank<=25 and o:rank=None and D']

NBA_QUERIES = ['season>=2016 and p:assists >= 27 and p:turnovers <=5',
'season>=2016 and p:assists >= 31 and p:turnovers <=7',
'season>=2016 and p:assists >= 22 and p:turnovers >=25',
'season>=2016 and p:assists <= 21 and p:turnovers >=25',
'season>=2016 and p:assists <= 10 and p:turnovers <=13',
'game number<=22 and HF and p:L and season>=2016 and line>=-4 and WP<o:WP',
'season>=2016 and HF and op:A and opp:A',
'season>=2016 and HD and op:A and opp:A',
'season>=2016 and HF and op:A and opp:A and oppp:A',
'season>=2016 and HD and op:A and opp:A and oppp:A',
'sorted(list:p:free throws attempted) [-2]>=13',
'tS(assists-14>=turnovers,N=4)=4 and season>=2016',
'p:ats streak>=5 and p:ats margin<=-12 and season>=2016',
'p:fouls<10 and season>=2016',
'p:dps>30 and rest=1 and season>=2016',
'max:p:free throws attempted>=19 and max:p:free throws made<=15 and season>=2016',
'tS(BL>=5 and L, N=4)=4 and season>=2016',
'p:rebounds-po:rebounds<-25 and season>=2016',
'p:assists>=25 and p:turnovers>=25 and p:overtime<1  and season>=2016',
'max:p:free throws attempted/p:free throws attempted>.5 and p:FTA>=29 and season>=2016',
'p:FTA - tA(p:FTA)>=20 and season>=2016',
'p:W and p:line>=10 and season>=2016',
'15>=streak>=12 and season>=2016',
'season >=2016 and p:dps < -25',
'season >=2016 and p:dpa > 30',
'total > 230 and (day=\'Friday\' or day=\'Saturday\') and line <-9',
'total > 230 and day=\'Friday\' and line <-9',
'sorted(list:po:points) [-4]>=20 and season>=2016',
'p:three pointers attempted>=44 and p:TPP >=38 and season >=2016',
'p:dpa<-2 and p:overtime>=1 and rest<=1 and season >= 2016',
'max:p:minutes<29 and rest=0 and F and season>=2016',
'season >= 2016 and total > 230',
'max:p:field goals made<=6 and p:points>=110 and season >=2016',
'p:assists>=27 and p:turnovers<=5 and season >=2016'
'sorted(list:p:three pointers made) [-3]>=4 and season>=2016',
'tS(DW,N=3)=3 and season>=2016',
'p:blocks=0 and po:FGP>=53 and season>=2016',
'HD and p:margin>=10 and p:PTP>30 and p:TPP > 36.75 and season>=2016',
'rest = 0 and o:rest > 0 and HD and game number >= 27',
'p:points > 104 and pp:points > 104 and ppp:points > 104 and AF and season>=2016',
'season>=2016 and HF and line <-10 and game number >=27 and o:rest =0',
'tA(points, N=3) >120 and HF and season>=2016 and rest<=o:rest and F',
'-3 <= line <= 3 and rest=0 and p:W and p:D and po:PIP >=50 and season>=2016',
'p:DPS<0 and pp:DPS<-25 and season>=2016'
'Sum(A@team and season,N=5) >= 4 and Sum(L@team and season,N=5) >= 3 and rest = 0 and AF',
'(p:points+po:points)-(Average(points@season)*2)<=-45 and p:W and season>=2016',
'A and p:A and p:A and rest =0 and season>=2016',
'sorted(list:p:assists) [-2]>=9 and p:W and playoffs=0 and season>=2016',
'HD and p:margin at the half>=20 and WP<60',
'p:rebounds < po:rebounds and HD and p:DW and op:L',
'p:rebounds < po:rebounds and HD and p:DW and op:W',
'D and n:site streak >= 1 and streak > 0',
'D and n:site streak >= 1 and streak > 0 and n:rest < 2 and season > 2014',
'AASB and tS(ATSW, N=5) >=4 and rest>=4 and season>=2016 and REG and month=2',
'Min(ATR@team and season, N=2) >2.75 and REG and season>=2016 and p:W'
]

NFL_QUERIES = [
'A and PRSW>10 and p:A and p:rushes - tA(p:rushes) < -8 and p:TOP/60 < 27 and date>=20090927 and p:TY-po:TY > - 300',
'H and surface=grass and PRSW>10 and p:WF and tA(points,N=3)>23.5 and day=Sunday and date>=20160000',
'p:LAD and HF and tA(points,N=3)<=14 and (o:streak>-5 or streak>-5) and oS(AW)-oS(AL)<=-2 and date >= 20061126',
'surface=grass and wins>losses and NDIV and p:AF and oA(RFD) >= 6.75 and week>2 and season >= 2014',
'surface=artificial and p:WAD and tA(rushes)<34 and oA(TOP)/60>32 and p:TOP/60 <32 and o:WP>25 and season >= 2009 ',
'week=17 and PRSW>10 and wins<=8 and DIV and o:wins>=6 and -3<=line<8 and season >= 2006',
'AD and po:points >= 40 and p:HL and line <= 7 and (day=Saturday or day=Sunday)',
'PRSW <= 6 and week = 1 and ((A and 12>line>0) or (H and line >=6))',
'H and 40 <= total <= 49 and p:turnovers > 3 and op:TOM > 1 and rest > 5 and o:rest > 5 ',
'p:AL and A and season>2002 and month>10 and WP<33.3',
'p:AL and A and season>2002 and month>10 and WP<33.3 and line>-4 and line<13',
'tpS(W @ week>8 and playoffs=0) > 6 and tpS(W @ week<9) < 4 and A and month = 9',
'tpS(PO, N=1) = 0 and tppS(PO, N=1) = 0 and tpppS(PO, N=1) = 0 and NDIV and rest > o:rest and oA(o:points) > 20 and season > 2011',
'tA(o:RY,N=3)>=165','tA(o:RY,N=3)>=170','tA(o:RY,N=3)>=175','tA(o:RY,N=3)>=180','tA(o:RY,N=3)>=185','tA(o:RY,N=3)>=190','tA(o:RY,N=3)>=195',
'tA(o:RY,N=3)>=190',
'H and PRSW<6 and p:margin<=-10 and p:dpa>0 and pp:dpa>0 and not (p:RY>=100 and p:PY>=250) and date>=20131200',
'season>=2016 and p:dps > 30',
'season>=2016 and p:dps<=-25 and p:dpa>0',
'season>=2016 and p:points = 0 and p:H',
'p:points - p:total > 0 and po:points - p:total > 0',
'season >=2012 and p:points = 0 and p:H',
'week=p:week+2 and AF and playoffs=0'
'week=p:week+2 and AF and playoffs=0',
<<<<<<< HEAD
'tA(ou margin, N=2) <= -15 and tS(U,N=3) = 3 and p:L and season>=2016 and AD'
=======
'tA(ou margin, N=2) <= -15 and tS(U,N=3) = 3 and p:L and season>=2016 and AD',
'Min(ATR@team and season, N=2) >2.75 and REG and season>=2016 and p:W'
>>>>>>> 0ee00443de057b990f1f26e35ac5d50b6765075b
]

MLB_QUERIES = ['season>=2013 and HF and p:WOW and p:SF>=1 and SG>1',
'streak=-2 and H and SG=3 and season']

NBA_URL = "https://killersports.com/nba/query"

NFL_URL = "https://killersports.com/nfl/query"

NCAABB_URL = "https://killersports.com/ncaabb/query"


CHROME_DRIVER_PATH = '../driver/chromedriver'

def initialize():	
	current_date = datetime.date.today()
	current_date += datetime.timedelta(days=-1)
	try:		
		p = sys.argv[1]
	except:
		p = ''
		print('no params')
	try:
		p2 = sys.argv[2]
	except:
		p2 = ''

	if p == 'init':
		date_time_str = '2019-12-08'
		date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d').date()
		open_page(date_time_obj, current_date)
	elif p == 'comp':
		append_data(current_date)
	elif p == 'check' and p2 == 'nba':
		check_queries(NBA_QUERIES, NBA_URL)
	elif p == 'check' and p2 == 'ncaabb':
		check_queries(NCAABB_QUERIES, NCAABB_URL)
	elif p == 'check' and p2 == 'nfl':
		check_queries(NFL_QUERIES, NFL_URL)
	else:
		open_page(current_date, current_date)

def load_driver(url):
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

def append_data(current_date):
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
		first = True
		if file.endswith('.csv'):
			sub_file = open(f"../data/sub/{file}", "r")
			#file_date = datetime.datetime.strptime(os.path.splitext(file)[0], '%Y%m%d').date()
			#if file_date == current_date:
			reader = csv.reader(sub_file, delimiter=" ")
			next(reader)
			for row in reader:
				team = row[0].split(',')[7]
				team_path = f"../data/teams/{team}"
				if not os.path.isdir(team_path):
					os.makedirs(team_path)

				team_file = open(f"{team_path}/{team}.csv", 'a+')
				team_writer = csv.writer(team_file)
				team_writer.writerow(row)

				writer.writerow(row)	
			sub_file.close()
	m.close()		
	print('done')

def check_queries(queries, url):
	browser = load_driver(url)
	
	count = 0
	today = datetime.date.today()
	today = today.strftime('%b %d, %Y')

	for i in queries:
		first = True
		wait = ui.WebDriverWait(browser,10).until(EC.presence_of_element_located((By.NAME, 'sdql')))
		time.sleep(5)
		browser.find_element(By.NAME, 'sdql').send_keys(i)
		submit_data = browser.find_element(By.NAME, 'submit').click()
		time.sleep(1)
		try:
			page = pq(browser.page_source)
			table = page('#DT_Table')
			body = table('tbody')
			for row in body('tr').items():
				date = row('td').eq(0).text()
				if date == today:	
					record_page = page('#content table tbody tr').eq(1).find('tbody tr')
					if first == True:
						print(i)
						for j in record_page.items():
							print(j('th').text(), j('td').text())
						first = False
					print(row('td').text())
			print()
		except:
			print('error retrieving data')
		count = count + 1
		browser.find_element(By.NAME, 'sdql').clear()

def open_page(starting_date, current_date):
	browser = load_driver(NBA_URL)	
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
	f.close()


initialize()
