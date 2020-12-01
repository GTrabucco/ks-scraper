from gut.base import Base
import statistics

class Team(Base):
	def __init__(self, name, start_date = None, end_date = None, season=None):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		super().__init__(name, f'../data/teams/{name}/{name}.csv', self.start_date, self.end_date, self.season)
		self.avg_assists = 0 if len(self.schedule) == 0 else statistics.mean([x.assists for x in self.schedule])
		self.avg_turnovers = 0 if len(self.schedule) == 0 else statistics.mean([x.turnovers for x in self.schedule])
		self.avg_fta = 0 if len(self.schedule) == 0 else statistics.mean([x.ftas for x in self.schedule])
		self.avg_pfs = 0 if len(self.schedule) == 0 else statistics.mean([x.pfs for x in self.schedule])
		self.avg_assists = 0 if len(self.schedule) == 0 else statistics.mean([x.assists for x in self.schedule])
		self.avg_fg3a = 0 if len(self.schedule) == 0 else statistics.mean([x.fg3as for x in self.schedule])
	
	def get_matchups_against_opp_by_opp_win_pct(self, win_pct):
		matchups = []
		for i in self.schedule:
			opponent = Team(i.opponent, end_date=i.date, season=i.season)
			if opponent.win_pct >= win_pct:
				matchups.append(i)
		return matchups