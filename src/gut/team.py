from gut.base import Base

class Team(Base):
	def __init__(self, name, start_date = None, end_date = None, season=None):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		super().__init__(name, f'../data/teams/{name}/{name}.csv', self.start_date, self.end_date, self.season)
	
	def get_matchups_against_opp_by_opp_win_pct(self, win_pct):
		matchups = []
		for i in self.schedule:
			opponent = Team(i.opponent, end_date=i.date, season=i.season)
			if opponent.win_pct >= win_pct:
				matchups.append(i)
		return matchups