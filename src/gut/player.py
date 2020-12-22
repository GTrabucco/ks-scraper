import math

class Player():
	def __init__(self, row, lineup_type):
		try:
			row = row.drop(['note'], errors='ignore')
			self.player_id = row['player_id']
			self.mp = row['mp']
			self.is_home = row['is_home']
			self.is_starter = row['is_starter']
			if lineup_type == 'basic':
				self.fg = row['fg']
				self.fga = row['fga']
				self.fg_pct = row['fg_pct']
				self.fg3 = row['fg3']
				self.fg3a = row['fg3a']
				self.fg3_pct = row['fg3_pct']
				self.ft = row['ft']
				self.fta = row['fta']
				self.ft_pct = row['ft_pct']
				self.orb = row['orb']
				self.drb = row['drb']
				self.trb = row['trb']
				self.ast = row['ast']
				self.stl = row['stl']
				self.blk = row['blk']
				self.tov = row['tov']
				self.pf = row['pf']
				self.pts = row['pts']
				self.plus_minus = row['plus_minus']
				self.player_name = row['player_name']
				self.team_id = row['team_id']

			elif lineup_type == 'advanced':
				self.ts_pct = row['ts_pct']
				self.efg_pct = row['efg_pct']
				self.off_rtg = row['off_rtg']
				self.def_rtg = row['def_rtg']
		except Exception as e:
			print('player class', e)
			exit()

	def update_stats(self, row):
		self.mp = self.mp + (row.mp if not math.isnan(row.mp) else 0)
		self.fg = self.fg + (row.fg if not math.isnan(row.fg) else 0)
		self.fga = self.fga + (row.fga if not math.isnan(row.fga) else 0)
		self.fg_pct = self.fg_pct + (row.fg_pct if not math.isnan(row.fg_pct) else 0)
		self.fg3 = self.fg3 + (row.fg3 if not math.isnan(row.fg3) else 0)
		self.fg3a = self.fg3a + (row.fg3a if not math.isnan(row.fg3a) else 0)
		self.fg3_pct = self.fg3_pct + (row.fg3_pct if not math.isnan(row.fg3_pct) else 0)
		self.ft = self.ft + (row.ft if not math.isnan(row.ft) else 0)
		self.fta = self.fta + (row.fta if not math.isnan(row.fta) else 0)
		self.ft_pct = self.ft_pct + (row.ft_pct if not math.isnan(row.ft_pct) else 0)
		self.orb = self.orb + (row.orb if not math.isnan(row.orb) else 0)
		self.drb = self.drb + (row.drb if not math.isnan(row.drb) else 0)
		self.trb = self.trb + (row.trb if not math.isnan(row.trb) else 0)
		self.ast = self.ast + (row.ast if not math.isnan(row.ast) else 0)
		self.stl = self.stl + (row.stl if not math.isnan(row.stl) else 0)
		self.blk = self.blk + (row.blk if not math.isnan(row.blk) else 0)
		self.tov = self.tov + (row.tov if not math.isnan(row.tov) else 0)
		self.pf = self.pf + (row.pf if not math.isnan(row.pf) else 0)
		self.pts = self.pts + (row.pts if not math.isnan(row.pts) else 0)
		self.plus_minus = self.plus_minus + (row.plus_minus if not math.isnan(row.plus_minus) else 0)
