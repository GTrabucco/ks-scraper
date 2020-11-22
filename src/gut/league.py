from gut.base import Base

class League(Base):
	def __init__(self, start_date = None, end_date = None, season=None):
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		super().__init__('master', '../data/master/master.csv', start_date, end_date, season)