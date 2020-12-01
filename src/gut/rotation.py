from pyquery import PyQuery as pq
import sportsref
from gut.nba_teams import NBA_TEAMS
import statistics
import os
import csv

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
		lineup = lineup.replace('[','')
		lineup = lineup.replace(']','')
		lineup = lineup.replace('\'','')
		lineup = lineup.split(',')
		self.mp = float(lineup[1].replace(':', '.'))
		self.pts = float(lineup[2].replace('+',''))
		self.fg = float(lineup[3].replace('+',''))
		self.fga = float(lineup[4].replace('+',''))
		self.fg_pct = float(lineup[5].replace('+',''))
		self.fg3 = float(lineup[6].replace('+',''))
		self.fg3a = float(lineup[7].replace('+',''))
		self.fg3_pct = float(lineup[8].replace('+',''))
		self.efg_pct = float(lineup[9].replace('+',''))
		self.ft = float(lineup[10].replace('+',''))
		self.fta = float(lineup[11].replace('+',''))
		self.ft_pct = float(lineup[12].replace('+',''))
		self.orb = float(lineup[13].replace('+',''))
		self.orb_pct = float(lineup[14].replace('+',''))
		self.drb = float(lineup[15].replace('+',''))
		self.drb_pct = float(lineup[16].replace('+',''))
		self.trb = float(lineup[17].replace('+',''))
		self.trb_pct = float(lineup[18].replace('+',''))
		self.ast = float(lineup[19].replace('+',''))
		self.stl = float(lineup[20].replace('+',''))
		self.blk = float(lineup[21].replace('+',''))
		self.tov = float(lineup[22].replace('+',''))
		self.pf = float(lineup[23].replace('+',''))

	def _normalize_data(self, data):
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
			path = os.path.abspath(os.path.join(os.path.dirname(__file__),f"../../data/rotations/{self.season}/{self.team}.csv"))
			try:
				if not os.path.isfile(path):
					url = f"https://www.basketball-reference.com/teams/{self.team}/{int(self.season)+1}/lineups/"
					doc = pq(sportsref.utils.get_html(url))
					table = doc('table#lineups_5-man_')
					columns = [th.text() for th in table('thead tr').eq(1).items('th')]
					data = [
						[sportsref.utils.flatten_links(td) for td in tr('th > a, td').items()]
						for tr in table('tbody tr').items()
					]

					with open(path, 'w') as myfile:
					    wr = csv.writer(myfile)
					    wr.writerow(data)
			except Exception as e:
				print('get_lineup_info', e, self.team, self.opponent)

			data = None

			with open(path, 'r') as myfile:
			    reader = csv.reader(myfile)
			    for row in reader:
			    	data = row

			if len(data) > 0:
				for lineup in data:
					rotation = lineup.split(',')[0]
					if '|' in rotation:
						r = rotation.replace('[','')
						r = r.replace('\'', '')
						r = r.split('|')
						if set(r) == set(self.lineup):
							self._set_rotation_stats(lineup)
							break

	def get_formatted_data(self):
		#return [self.pts/111]
		return [#self.mp/48, 
				#self.pts/111, 
				#self.fg/41, 
				self.fga, 
				self.fg_pct, 
				#self.fg3/12, 
				self.fg3a, 
				self.fg3_pct, 
				self.efg_pct, 
				#self.ft/18, 
				#self.fta/23,
				#self.ft_pct/.77,
				#self.orb/10,
				#self.orb_pct/23
				#self.drb/35,
				#self.trb/45,
				#self.ast/24,
				#self.stl/8,
				#self.blk/5,
				#self.tov/15,
				#self.pf/21]
				]


