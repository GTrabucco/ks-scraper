from gut.player import Player

class Lineup():
	def __init__(self, df):
		self.lineup = []
		self._initialize_lineup(df)
		self.starters = [i for i in self.lineup if i.is_starter == True]

	def _initialize_lineup(self, df):
		for index, row in df.iterrows():
			try:
				player = Player(row)
				self.lineup.append(player)
			except Exception as e:
				print('_initialize_lineup', e, row)

	# lineup needs to be a list of strings == 5 containing player_ids
	def get_rotation_data(self, lineup, team, season):
		if len(lineup) < 5 or len(lineup) > 5:
			print('get_rotation_data', 'invalid lineup')
		else:
			r = Rotation(lineup, team, season)

	def get_starters_rotation_data(self, team, season):
		if len(lineup) < 5 or len(lineup) > 5:
			print('get_rotation_data', 'invalid lineup')
		else:
			r = Rotation(lineup, team, season)