from gut.base import Base
import statistics

class Team(Base):
	def __init__(self, name=None, start_date = None, end_date = None, season=None, last_n_matchups=None, load_lineup=False):
		self.name = name
		self.start_date = start_date
		self.end_date = end_date
		self.season = season
		self.last_n_matchups = last_n_matchups
		self.load_lineup = load_lineup
		super().__init__(name, f'../data/teams/{name}/{name}.csv', self.start_date, self.end_date, self.season, self.last_n_matchups, self.load_lineup)
		
	def get_wins(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'W')

	def get_losses(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'L')

	def get_point_diff(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else sum([x.su_margin for x in schedule])
	
	def get_ats_home_wins(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ats_record == 'W')

	def get_ats_home_losses(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ats_record == 'L')

	def get_ats_away_wins(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ats_record == 'W')

	def get_ats_away_losses(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ats_record == 'L')

	def get_ts_pct(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.ts for x in schedule]) 

	def get_home_ts_pct(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 or len([x.line for x in schedule]) == 0 else statistics.mean([x.ts for x in schedule])
	
	def get_away_ts_pct(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 or len([x.line for x in schedule]) == 0 else statistics.mean([x.ts for x in schedule]) 

	def get_home_wins(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'W')

	def get_home_losses(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'L')

	def get_home_point_diff(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum([x.su_margin for x in schedule])

	def get_away_wins(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'W')

	def get_away_losses(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'L')

	def get_away_point_diff(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum([x.su_margin for x in schedule])

	def get_ou_overs(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ou_record == 'O')

	def get_ou_unders(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ou_record == 'U')

	def get_home_ou_overs(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ou_record == 'O')

	def get_home_ou_unders(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ou_record == 'U')

	def get_away_ou_overs(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ou_record == 'O')

	def get_away_ou_unders(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ou_record == 'U')

	def get_ats_wins(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.ats_record == 'W')

	def get_ats_losses(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else sum(1 for x in schedule if x.su_record == 'L')

	def get_avg_assists(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.assists for x in schedule])

	def get_avg_turnovers(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.turnovers for x in schedule])

	def get_avg_fta(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.ftas for x in schedule])

	def get_avg_pfs(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.pfs for x in schedule])

	def get_avg_assists(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.assists for x in schedule])

	def get_avg_fg3a(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.fg3as for x in schedule])

	def get_avg_line(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.line for x in schedule])

	def get_avg_home_line(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 or len([x.line for x in schedule]) == 0 else statistics.mean([x.line for x in schedule])

	def get_avg_away_line(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 or len([x.line for x in schedule]) == 0 else statistics.mean([x.line for x in schedule])	

	def get_avg_total(self, n=None):
		schedule = self.get_last_n_matchups(n)
		return 0 if len(schedule) == 0 else statistics.mean([x.total for x in schedule])

	def get_avg_home_total(self, n=None):
		schedule = self.get_last_n_matchups(n, 'home')
		return 0 if len(schedule) == 0 or len([x.total for x in schedule]) == 0 else statistics.mean([x.total for x in schedule])

	def get_avg_away_total(self, n=None):
		schedule = self.get_last_n_matchups(n, 'away')
		return 0 if len(schedule) == 0 or len([x.total for x in schedule]) == 0 else statistics.mean([x.total for x in schedule])	

	def get_matchups_against_opp_by_opp_win_pct(self, win_pct):
		matchups = []
		for i in schedule:
			opponent = Team(i.opponent, end_date=i.date, season=i.season)
			if opponent.win_pct >= win_pct:
				matchups.append(i)
		return matchups

	def get_ats_streak(self, n=None):
		streak = 0
		rec = ''
		for i in self.get_last_n_matchups(n):
			if i.ats_record == 'L':
				if streak == 0:
					rec = 'L'
				if rec != 'L':
					return streak
				streak = streak - 1
			elif i.ats_record == 'W':
				if streak == 0:
					rec = 'W'
				if rec != 'W':
					return streak				
				streak = streak + 1
		return streak

	def get_ou_streak(self, n=None):
		streak = 0
		rec = ''
		for i in self.get_last_n_matchups(n):
			if i.ou_record == 'O':
				if streak == 0:
					rec = 'O'
				if rec != 'O':
					return streak
				streak = streak + 1
			elif i.ou_record == 'U':
				if streak == 0:
					rec = 'U'
				if rec != 'U':
					return streak				
				streak = streak - 1
		return streak