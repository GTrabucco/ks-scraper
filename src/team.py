import csv
from matchup import Matchup
import dateutil.parser
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
import statsmodels.api as sm
from base import Base

DATA_START_DATE = '1/1/2015'

class Team(Base):
	def __init__(self, name):
		super().__init(name, f'../data/teams/{name}/{name}.csv' )

	def get_matchups_against_opponent(self, opponent_name, start_date = DATA_START_DATE, end_date = str(date.today())):
		try:
			formatted_start_date = dateutil.parser.parse(start_date).strftime("%m/%d/%Y")
			formatted_end_date = dateutil.parser.parse(end_date).strftime("%m/%d/%Y")
			matchups = [x for x in self.schedule if x.opponent == opponent_name and x.date >= formatted_start_date and x.date <= formatted_end_date]	
			return matchups
		except Exception as e:
			print('get_matchup_by_opponent()', opponent_name, e)