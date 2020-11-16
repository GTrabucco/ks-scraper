from matchup import Matchup
import csv

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
