from base import Base

class Scenario(Base):
	def __init__(self, scenario, at_date = None):
		self.scenario = scenario
		self.at_date = at_date
		super().__init__(scenario, f'../data/scenarios/{scenario}/data.csv', self.at_date)
