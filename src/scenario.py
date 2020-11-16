import csv
from matchup import Matchup
from base import Base

class Scenario(Base):
	def __init__(self, scenario):
		super().__init__(scenario, f'../data/scenarios/{scenario}/data.csv')