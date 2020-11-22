from gut.player import Player

class Lineup():
	def __init__(self, df):
		self.lineup = []
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
		self._initialize_lineup(df)

	def _initialize_lineup(self, df):
		for index, row in df.iterrows():
			try:
				player = Player(row)
				self.lineup.append(player)
			except Exception as e:
				print('_initialize_lineup', e, row)

	def get_starters(self):
		return [i for i in self.lineup if i.is_starter == True]
