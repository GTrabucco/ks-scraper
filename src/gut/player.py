class Player():
	def __init__(self, row):
		try:
			row = row.drop(['note'], errors='ignore')
			self.ast = row[0]
			self.blk = row[1]
			self.drb = row[2]
			self.fg = row[3]
			self.fg3 = row[4]
			self.fg3_pct = row[5]
			self.fg3a = row[6]
			self.fg_pct = row[7]
			self.fga = row[8]
			self.ft = row[9]
			self.ft_pct = row[10]
			self.fta = row[11]
			self.is_home = row[12]
			self.is_starter = row[13]
			self.mp = row[14]
			self.orb = row[15]
			self.pf = row[16]
			self.player_id = row[17]
			self.player_name = row[18]
			self.plus_minus = row[19]
			self.pts = row[20]
			self.stl = row[21]
			self.team_id = row[22]
			self.tov = row[23]
			self.trb = row[24]
		except Exception as e:
			print('player class', e, row)
