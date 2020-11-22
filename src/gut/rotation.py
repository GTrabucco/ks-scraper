from pyquery import PyQuery as pq
import sportsref
from gut.nba_teams import NBA_TEAMS
import statistics

class Rotation():
	# lineup should be a string list of the player_ids of the 5 man rotation
	def __init__(self, lineup, team, season):
		self.lineup = lineup
		for abbr, name in NBA_TEAMS.items():
			if team == name:
				self.team = abbr[1:]
		self.season = season
		self.mp = 0
		self.pts = 0
		self.fg = 0
		self.fga = 0
		self.fg_pct = 0
		self.fg3 = 0
		self.fg3a = 0
		self.fg3_pct = 0
		self.efg_pct = 0
		self.ft = 0
		self.fta = 0
		self.ft_pct = 0
		self.orb = 0
		self.orb_pct = 0
		self.drb = 0
		self.drb_pct = 0
		self.trb = 0
		self.trb_pct = 0
		self.ast = 0
		self.stl = 0
		self.blk = 0
		self.tov = 0
		self.pf = 0
		self._initialize_rotation()

	def _set_rotation_stats(self, lineup):
		self.mp = lineup[1]
		self.pts = lineup[2]
		self.fg = lineup[3]
		self.fga = lineup[4]
		self.fg_pct = lineup[5]
		self.fg3 = lineup[6]
		self.fg3a = lineup[7]
		self.fg3_pct = lineup[8]
		self.efg_pct = lineup[9]
		self.ft = lineup[10]
		self.fta = lineup[11]
		self.ft_pct = lineup[12]
		self.orb = lineup[13]
		self.orb_pct = lineup[14]
		self.drb = lineup[15]
		self.drb_pct = lineup[16]
		self.trb = lineup[17]
		self.trb_pct = lineup[18]
		self.ast = lineup[19]
		self.stl = lineup[20]
		self.blk = lineup[21]
		self.tov = lineup[22]
		self.pf = lineup[23]

	def _scale_data(self, data):
		mp_highest = float(data[0][1].replace(':', '.'))
		avg = statistics.mean([float(i[1].replace(':','.')) for i in data[:-1]])
		mp_min = float(data[-2][1].replace(':', '.'))
		for row in data:		
			for i, item in enumerate(row):
				if i == 1:
					row[1] = (float(item.replace(':','.')) - avg)/(mp_highest - mp_min)
				elif i > 1:
					row[i] = float(item.replace('+','')) * row[1]

		return data

	def _initialize_rotation(self):
		if len(self.lineup) > 5 or len(self.lineup) == 0:
			print('Invalid rotation')
		else:
			url = f"https://www.basketball-reference.com/teams/{self.team}/{int(self.season)+1}/lineups/"
			doc = pq(sportsref.utils.get_html(url))
			table = doc('table#lineups_5-man_')
			columns = [th.text() for th in table('thead tr').eq(1).items('th')]
			data = [
				[sportsref.utils.flatten_links(td) for td in tr('th > a, td').items()]
				for tr in table('tbody tr').items()
			]

			if len(data) > 0:
				scaled_data = self._scale_data(data)
				for lineup in scaled_data:
					rotation = lineup[0]
					if '|' in rotation:
						r = rotation.split('|')
						if set(r) == set(self.lineup):
							self._set_rotation_stats(lineup)
							break


