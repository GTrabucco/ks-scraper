from gut.base import Base
from gut.team import Team

class League(Base):
	def __init__(self, start_date = None, end_date = None, season=None):
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		self.teams = []
		super().__init__('master', '../data/master/master.csv', start_date, end_date, season)
		self._initialize_teams()

	def _initialize_teams(self):
		for matchup in self.schedule:
			if len(self.teams) == 30:
				break
			else:
				team = matchup.team
				exists = len([i for i in self.teams if i.name == team]) > 0
				if exists != True:
					t = Team(team, start_date=self.start_date, end_date=self.end_date, season=self.season, load_lineup=True)
					print('Populating team:', team)
					self.teams.append(t)
				else:
					continue

