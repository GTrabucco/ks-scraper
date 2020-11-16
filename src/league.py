import csv
from matchup import Matchup

class League():
	def __init__(self):
		self.schedule = []
		self._initialize_schedule()

	def _insert_matchup(self, matchup):
		self.schedule.append(matchup)

	def _initialize_schedule(self):
		try:
			with open(f'../data/master/master.csv', 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
				next(reader, None)
				for raw_row in reader:
					row = str(raw_row).split(',')
					m = Matchup(row[0] + row[1] + row[3], row[5], row[6], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22])
					self._insert_matchup(m)
			csvfile.close()
		except Exception as e:
			print('_initialize_schedule()', e)