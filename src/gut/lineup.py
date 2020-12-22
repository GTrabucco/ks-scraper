from gut.player import Player
import statistics 

class Lineup():
	def __init__(self, df, lineup_type):
		self.lineup = []
		self.lineup_type = lineup_type
		self._initialize_lineup(df)
		self.starters = [i for i in self.lineup if i.is_starter == True]
		self.pts = sum([i.pts for i in self.lineup if i.pts > 0])
		self.fga = sum([i.fga for i in self.lineup if i.pts > 0])
		self.fta = sum([i.fta for i in self.lineup if i.pts > 0])
		self.ts = self.pts / (2 * (self.fga + (.44 * self.fta)))

	def _initialize_lineup(self, df):
		for index, row in df.iterrows():
			try:
				player = Player(row, self.lineup_type)
				self.lineup.append(player)
			except Exception as e:
				print('lineup _initialize_lineup', e, row)

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
