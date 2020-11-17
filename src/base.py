import csv
from matchup import Matchup
import dateutil.parser
from datetime import date, datetime
from abc import ABC, abstractmethod

DATA_START_DATE = '1/1/2015'

class Base(ABC):
	def __init__(self, name, path, start_date = None, end_date = None, season=None):
		self.name = name
		self.schedule = []
		self.path = path
		self.start_date = start_date if isinstance(start_date, date) or start_date == None else datetime.strptime(start_date, '%Y-%m-%d').date()
		self.end_date = end_date if isinstance(end_date, date) or end_date == None else datetime.strptime(end_date, '%Y-%m-%d').date()
		self.season = season
		self._initialize_schedule(self.start_date, self.end_date, self.season)

	def _insert_matchup(self, matchup):
		self.schedule.append(matchup)

	def _initialize_schedule(self, start_date, end_date, season):
		try:
			with open(self.path, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				next(reader, None)
				for raw_row in reader:
					row = str(raw_row).split(',')
					m = Matchup(row[0] + row[1] + row[3], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22])	
					if (start_date is not None and start_date > m.date) or (end_date is not None and end_date < m.date) or (season is not None and m.season != season):
						continue
					self._insert_matchup(m)
			csvfile.close()
		except Exception as e:
			print('_initialize_schedule()', e)

	def get_matchup_by_date(self, date):	
		try:
			formatted_date = dateutil.parser.parse(date).strftime("%m/%d/%Y")
			matchup = [x for x in self.schedule if x.date == formatted_date][0]
			return matchup
		except IndexError as e:
			print(f'Matchup on: {date} does not exist')
		except Exception as e:
			print('get_matchup_by_date()', date, e)

	def get_last_n_matchups(self, n):
		try:			
		    schedule = sorted(self.schedule, key=lambda x: x.date, reverse=False)
		    matchups = schedule[-n:]
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
