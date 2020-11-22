from gut.base import Base

class Scenario(Base):
	def __init__(self, scenario, start_date = None, end_date = None, season=None):
		self.scenario = scenario
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		super().__init__(scenario, f'../data/scenarios/{scenario}/data.csv', self.start_date, self.end_date, self.season)
