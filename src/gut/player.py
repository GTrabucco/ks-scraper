class Player():
	def __init__(self, row):
		try:
			row = row.drop(['note'], errors='ignore')
			self.player_id = row[0]
			self.mp = row[1]
			self.fg = row[2]
			self.fga = row[3]
			self.fg_pct = row[4]
			self.fg3 = row[5]
			self.fg3a = row[6]
			self.fg3_pct = row[7]
			self.ft = row[8]
			self.fta = row[9]
			self.ft_pct = row[10]
			self.orb = row[11]
			self.drb = row[12]
			self.trb = row[13]
			self.ast = row[14]
			self.stl = row[15]
			self.blk = row[16]
			self.tov = row[17]
			self.pf = row[18]
			self.pts = row[19]
			self.plus_minus = row[20]
			self.player_name = row[21]
			self.team_id = row[22]
			self.is_home = row[23]
			self.is_starter = row[24]
		except Exception as e:
			print('player class', e, row)
