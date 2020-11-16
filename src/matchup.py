import re
import dateutil.parser
import datetime

class Matchup():
	def __init__(self, date, day, season, opponent, site, final_score, rest, line, total, su_margin, ats_margin, ou_margin, dps, dpa, su_record, ats_record, ou_record, ot):
		formatted_date = re.sub('[^0-9a-zA-Z]+', '', date)
		self.date = datetime.datetime.strptime(formatted_date, "%b%d%Y").strftime("%m/%d/%Y")
		self.day = day
		self.season = season
		self.opponent = opponent
		self.site = site
		self.score = final_score.split('-')[0]
		self.opponent_score = final_score.split('-')[1]
		self.rest = rest.split('&')[0]
		self.opponent_rest = rest.split('&')[1]
		self.line = float(line)
		self.total = float(total)
		self.su_margin = su_margin
		self.ats_margin = ats_margin
		self.ou_margin = ou_margin
		self.dps = dps
		self.dpa = dpa
		self.su_record = su_record
		self.ats_record = ats_record
		self.ou_record = ou_record
		self.ot = re.sub('[^0-9a-zA-Z]+', '', ot)



