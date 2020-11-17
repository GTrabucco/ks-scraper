from base import Base
import statistics

class Team(Base):
	def __init__(self, name, start_date = None, end_date = None, season=None):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		super().__init__(name, f'../data/teams/{name}/{name}.csv', self.start_date, self.end_date, self.season)
		self.wins = len([x for x in self.schedule if x.su_record == 'W'])
		self.losses = len([x for x in self.schedule if x.su_record == 'L'])
		self.ats_wins = len([x for x in self.schedule if x.ats_record == 'W'])
		self.ats_losses = len([x for x in self.schedule if x.ats_record == 'L'])
		self.ats_pushes = len([x for x in self.schedule if x.ats_record == 'P'])
		self.ou_overs = len([x for x in self.schedule if x.ou_record == 'O'])
		self.ou_unders = len([x for x in self.schedule if x.ou_record == 'U'])
		self.ou_pushes = len([x for x in self.schedule if x.ou_record == 'P'])
		self.ou_unders = len([x for x in self.schedule if x.ou_record == 'U'])
		self.avg_total = 0 if len(self.schedule) == 0 else statistics.mean([x.total for x in self.schedule])
		self.avg_line = 0 if len(self.schedule) == 0 else statistics.mean([x.line for x in self.schedule])