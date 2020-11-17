from base import Base

class League(Base):
	def __init__(self, at_date):
		super().__init('master', path='../data/master/master.csv', at_date)