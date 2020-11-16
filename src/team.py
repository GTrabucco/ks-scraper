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

PATH = f'../data/teams/{name}/{name}.csv'

class Team(Base):
	def __init__(self, name):
		super().__init(name, PATH)
