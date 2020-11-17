from base import Base

class Scenario(Base):
	def __init__(self, scenario, at_date = None):
		super().__init__(scenario, path=f'../data/scenarios/{scenario}/data.csv', at_date)