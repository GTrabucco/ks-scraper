from matchup import Matchup
import csv

DATA_START_DATE = '1/1/2015'

class Base():
	def __init__(self, name, path):
		self.name = name
		self.schedule = []
		self.path = path
		self._initialize_schedule()

	def _insert_matchup(self, matchup):
		self.schedule.append(matchup)

	def _initialize_schedule(self):
		try:
			with open(self.path, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				next(reader, None)
				for raw_row in reader:
					row = str(raw_row).split(',')
					m = Matchup(row[0] + row[1] + row[3], row[5], row[6], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22])
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
	    schedule = sorted(self.schedule, key=lambda x: x.date, reverse=False)
	    matchups = schedule[-n:]
	    return matchups


	def get_matchups_against_opponent(self, opponent_name, start_date = DATA_START_DATE, end_date = str(date.today())):
		try:
			formatted_start_date = dateutil.parser.parse(start_date).strftime("%m/%d/%Y")
			formatted_end_date = dateutil.parser.parse(end_date).strftime("%m/%d/%Y")
			matchups = [x for x in self.schedule if x.opponent == opponent_name and x.date >= formatted_start_date and x.date <= formatted_end_date]	
			return matchups
		except Exception as e:
			print('get_matchup_by_opponent()', opponent_name, e)
