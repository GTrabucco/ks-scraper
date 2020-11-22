from gut.player import Player

class Lineup():
	def __init__(self, df):
		self.lineup = []
		self._initialize_lineup(df)

	def _initialize_lineup(self, df):
		for index, row in df.iterrows():
			try:
				player = Player(row)
				self.lineup.append(player)
			except Exception as e:
				print('_initialize_lineup', e, row)
