import csv
from gut.matchup import Matchup
import dateutil.parser
from datetime import date, datetime, timedelta
from abc import ABC, abstractmethod
import statistics
import re

DATA_START_DATE = '1/1/2015'

class Base(ABC):
	def __init__(self, name, path, start_date = None, end_date = None, season = None, last_n_matchups = None, load_lineup=False):
		self.name = name
		self.schedule = []
		self.path = path
		self.start_date = start_date if isinstance(start_date, date) or start_date == None else datetime.strptime(start_date, '%Y-%m-%d').date()
		self.end_date = end_date if isinstance(end_date, date) or end_date == None else datetime.strptime(end_date, '%Y-%m-%d').date()
		self.season = int(season) if season != None else None
		self.last_n_matchups = last_n_matchups
		self.load_lineup = load_lineup
		self._initialize_data()

	def _initialize_data(self):
		self._initialize_schedule()

	def _insert_matchup(self, matchup, count):
		self.schedule.append(matchup)

	def _initialize_schedule(self):
		try:
			with open(self.path, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				next(reader, None)
				count = 1
				for raw_row in reversed(list(csv.reader(csvfile))):
					row = str(raw_row).split(',')
					d = row[0] + row[1] + row[3]
					formatted_date = re.sub('[^0-9a-zA-Z]+', '', d)
					matchup_date = datetime.strptime(datetime.strptime(formatted_date, "%b%d%Y").strftime("%m/%d/%Y"), "%m/%d/%Y").date()
					matchup_season = int(row[6])
					if (self.start_date is not None and self.start_date < matchup_date or (self.season is not None and matchup_season > self.season) ):
						continue
					elif self.end_date is not None and self.end_date > matchup_date or (self.season is not None and matchup_season < self.season or (self.last_n_matchups is not None and count > self.last_n_matchups)):
						break
					else:
						m = Matchup(matchup_date, row[5], matchup_season, row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], self.load_lineup)		
						self._insert_matchup(m, count)
						count = count + 1

			csvfile.close()
		except Exception as e:
			print('_initialize_schedule()', raw_row, e)
			exit()

	def get_matchup_by_date(self, date):	
		try:
			formatted_date = dateutil.parser.parse(date).strftime("%m/%d/%Y")
			matchup = [x for x in self.schedule if x.date == formatted_date][0]
			return matchup
		except IndexError as e:
			print(f'Matchup on: {date} does not exist')
		except Exception as e:
			print('get_matchup_by_date()', date, e)

	def get_last_n_matchups(self, n, site=None):
		try:			
			if site is not None:
				schedule = sorted([x for x in self.schedule if x.site == site], key=lambda x: x.date, reverse=False)
			else:
				schedule = sorted(self.schedule, key=lambda x: x.date, reverse=False)
			matchups = schedule[-n-1:-1]
			return matchups
		except Exception as e:
			print('get_last_n_matchups', n, e)

	def get_matchups_against_opponent(self, opponent_name, start_date = DATA_START_DATE, end_date = str(date.today())):
		try:
			formatted_start_date = dateutil.parser.parse(start_date).strftime("%m/%d/%Y")
			formatted_end_date = dateutil.parser.parse(end_date).strftime("%m/%d/%Y")
			matchups = [x for x in self.schedule if x.opponent == opponent_name and x.date >= formatted_start_date and x.date <= formatted_end_date]	
			return matchups
		except Exception as e:
			print('get_matchup_by_opponent()', opponent_name, e)

	def get_home_matchups(self):
		return [i for i in self.schedule if i.site == 'home']

	def get_away_matchups(self):
		return [i for i in self.schedule if i.site == 'away']
