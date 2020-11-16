import csv
from matchup import Matchup
from base import Base

PATH = f'../data/master/master.csv'

class League(Base):
	def __init__(self):
		super().__init('master', PATH)