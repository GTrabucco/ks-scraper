from base import Base
import statistics

class Team(Base):
	def __init__(self, name, at_date = None):
		self.name = name
		self.at_date = at_date
		super().__init__(name, f'../data/teams/{name}/{name}.csv', self.at_date)
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