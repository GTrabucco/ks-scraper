import re
import dateutil.parser
import datetime
from gut.nba_teams import NBA_TEAMS
from gut.lineup import Lineup
import sportsref
import os.path
import csv
import pandas as pd
import pathlib

class Matchup():
	def __init__(self, date, day, season, team, opponent, site, final_score, rest, line, total, su_margin, ats_margin, ou_margin, dps, dpa, su_record, ats_record, ou_record, ot):
		self.date = date
		self.day = day
		self.season = season
		self.team = team
		self.opponent = opponent
		self.site = site
		self.score = float(final_score.split('-')[0])
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
		self.turnovers = 0
		self.assists = 0
		self.ftas = 0
		self.pfs = 0
		self.fg3as = 0
		self.stls = 0
		self._get_lineup_info()

	def _get_lineup_info(self):
		team_id = 0
		for abbr, name in NBA_TEAMS.items():
			if self.team == name and self.site == 'home':
				team_id = abbr
			if self.opponent == name and self.site == 'away':
				team_id = abbr

		boxscore_id = self.date.strftime(f"%Y%m%d{team_id}")
		path = os.path.abspath(os.path.join(os.path.dirname(__file__),f"../../data/boxscores/{self.season}/{boxscore_id}.csv"))
		try:
			if not os.path.isfile(path):
				b = sportsref.nba.BoxScore(boxscore_id)
				lineups = b.basic_stats()
				lineups.to_csv(path, index=False, header=True)
		except Exception as e:
			print('get_lineup_info', e, self.team, self.opponent)

		lineups = pd.read_csv(path)
		self.lineup = Lineup(lineups.loc[lineups['is_home'] == (self.site == 'home')])
		self.turnovers = sum([player.tov for player in self.lineup.lineup if player.tov > 0])
		self.assists = sum([player.ast for player in self.lineup.lineup if player.ast > 0])
		self.ftas = sum([player.fta for player in self.lineup.lineup if player.fta > 0])
		self.pfs = sum([player.pf for player in self.lineup.lineup if player.pf > 0])
		self.fg3as = sum([player.fg3a for player in self.lineup.lineup if player.fg3a > 0])
		self.stls = sum([player.stl for player in self.lineup.lineup if player.stl > 0])
		self.opponent_lineup = Lineup(lineups.loc[lineups['is_home'] != (self.site == 'home')])