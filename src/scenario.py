import csv
from matchup import Matchup
from base import Base

PATH = f'../data/scenarios/{scenario}/data.csv'

class Scenario(Base):
	def __init__(self, scenario):
		super().__init__(scenario, PATH)