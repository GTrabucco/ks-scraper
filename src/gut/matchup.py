import re
import dateutil.parser
import datetime
from gut.nba_teams import NBA_TEAMS
from gut.lineup import Lineup
import sportsref

class Matchup():
	def __init__(self, date, day, season, team, opponent, site, final_score, rest, line, total, su_margin, ats_margin, ou_margin, dps, dpa, su_record, ats_record, ou_record, ot):
		formatted_date = re.sub('[^0-9a-zA-Z]+', '', date)
		self.date = datetime.datetime.strptime(datetime.datetime.strptime(formatted_date, "%b%d%Y").strftime("%m/%d/%Y"), "%m/%d/%Y").date()
		self.day = day
		self.season = season
		self.team = team
		self.opponent = opponent
		self.site = site
		self.score = final_score.split('-')[0]
		self.opponent_score = float(final_score.split('-')[1])
		self.rest = float(rest.split('&')[0].replace('', '0'))
		self.opponent_rest = float(rest.split('&')[1].replace('', '0'))
		self.line = float(line)
		self.total = float(total)
		self.su_margin = float(su_margin)
		self.ats_margin = float(ats_margin)
		self.ou_margin = float(ou_margin)
		self.dps = float(dps)
		self.dpa = float(dpa)
		self.su_record = su_record
		self.ats_record = ats_record
		self.ou_record = ou_record
		self.ot = re.sub('[^0-9a-zA-Z]+', '', ot)
		self.lineup = []
		self.opponent_lineup = []
		self._get_lineup_info()

	def _get_lineup_info(self):
		team_id = 0
		for abbr, name in NBA_TEAMS.items():
			if self.team == name and self.site == 'home':
				team_id = abbr
			if self.opponent == name and self.site == 'away':
				team_id = abbr

		boxscore_id = self.date.strftime(f"%Y%m%d{team_id}")

		b = sportsref.nba.BoxScore(boxscore_id)
		try:
			lineups = b.basic_stats()
			self.lineup = Lineup(lineups.loc[lineups['is_home'] == (self.site == 'home')])
			self.opponent_lineup = Lineup(lineups.loc[lineups['is_home'] == (self.site == 'home')])
		except Exception as e:
			print('get_lineup_info', e, self.team, self.opponent)