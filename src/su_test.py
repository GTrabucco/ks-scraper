from gut.scenario import Scenario
from gut.team import Team
from gut.league import League
from gut.rotation import Rotation
from utility import gut_util
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
from sklearn.feature_selection import VarianceThreshold
import seaborn as sns
import matplotlib.pyplot as plt 
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
import statistics
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import os.path
import copy

lines_by_season = [[], [], [], [], []]

data_by_season = [[], [], [], [], []]

def go(t):
	count = int(len(t.schedule)/2)
	data = []
	lines = []
	test_data = []
	test_lines = []
	season_index = 0
	current_season = ""
	game_count = 82
	season_length = 0

	#playoff_start_dates = [datetime(2020,4,8), datetime(2020, 8, 17), datetime(2019, 4, 13), datetime(2018, 4, 14), datetime(2017, 4, 15), datetime(2016, 4, 16)]
	playoff_start_dates = [datetime(2020, 8, 17), datetime(2019, 4, 13), datetime(2018, 4, 14), datetime(2017, 4, 15), datetime(2016, 4, 16)]

	num_games_2020 = sum([1 for i in t.schedule[::2] if i.season == "2020" and i.date < playoff_start_dates[0].date()])
	num_games_2019 = sum([1 for i in t.schedule[::2] if i.season == "2019" and i.date < playoff_start_dates[0].date()])
	num_games_2018 = sum([1 for i in t.schedule[::2] if i.season == "2018" and i.date < playoff_start_dates[1].date()])
	num_games_2017 = sum([1 for i in t.schedule[::2] if i.season == "2017" and i.date < playoff_start_dates[2].date()])
	num_games_2016 = sum([1 for i in t.schedule[::2] if i.season == "2016" and i.date < playoff_start_dates[3].date()])
	num_games_2015 = sum([1 for i in t.schedule[::2] if i.season == "2015" and i.date < playoff_start_dates[4].date()])

	#num_games = [num_games_2020, num_games_2019, num_games_2018, num_games_2017, num_games_2016, num_games_2015]
	num_games = [num_games_2019, num_games_2018, num_games_2017, num_games_2016, num_games_2015]

	for matchup in t.schedule[::2]:
		#print(matchup.date, count)
		if count %1000 == 0:
			print(matchup.date, count)

		if current_season == "":
			current_season = matchup.season
			season_length = num_games[season_index]
			game_count = num_games[season_index]			
		elif current_season != matchup.season:
			season_index = season_index + 1
			season_length = num_games[season_index]
			game_count = num_games[season_index]
			current_season = matchup.season

		team_orig = [t for t in t.teams if t.name == matchup.team][0]
		opp_orig = [t for t in t.teams if t.name == matchup.opponent][0]

		team = copy.deepcopy(team_orig)
		opp = copy.deepcopy(opp_orig)

		team.schedule = [i for i in team.schedule if i.season == matchup.season and i.date <= matchup.date-timedelta(days=1)]  
		opp.schedule = [i for i in opp.schedule if i.season == matchup.season and i.date <= matchup.date-timedelta(days=1)] 

		if len(team.schedule) < 8 or len(opp.schedule) < 8:
			count = count - 1
			continue

		outcome = 0
		if matchup.ats_record == 'W':
			outcome = 1
		
		if matchup.site == 'home':
			ts_ats_record = 0 if team.get_ats_home_wins(n=8) == 0 else team.get_ats_home_wins(n=8) / (team.get_ats_home_wins(n=8) + team.get_ats_home_losses(n=8))
			os_ats_record = 0 if opp.get_ats_away_wins(n=8) == 0 else opp.get_ats_away_wins(n=8) / (opp.get_ats_away_wins(n=8) + opp.get_ats_away_losses(n=8))

			# home team win pct
			ht_wp = 0 if team.ats_wins == 0 else team.get_ats_wins(n=8) / (team.get_ats_wins(n=8) + team.get_ats_losses(n=8))

			t_avg_ls = team.get_avg_home_line(n=8)
			o_avg_ls = opp.get_avg_away_line(n=8)
			ts_ts_pct = team.get_home_ts_pct(n=8)
			os_ts_pct = opp.get_away_ts_pct(n=8)

		elif matchup.site == 'away':
			os_ats_record = 0 if opp.get_ats_home_wins(n=8) == 0 else opp.get_ats_home_wins(n=8) / (opp.get_ats_home_wins(n=8) + opp.get_ats_home_losses(n=8))
			ts_ats_record = 0 if team.get_ats_away_wins(n=8) == 0 else team.get_ats_away_wins(n=8) / (team.get_ats_away_wins(n=8) + team.get_ats_away_losses(n=8))

			# home team win pct
			ht_wp = 0 if opp.get_ats_wins(n=8) == 0 else opp.get_ats_wins(n=8) / (opp.get_ats_wins(n=8) + opp.get_ats_losses(n=8))

			t_avg_ls = team.get_avg_away_line(n=8)
			o_avg_ls = opp.get_avg_home_line(n=8)
			ts_ts_pct = team.get_away_ts_pct(n=8)
			os_ts_pct = opp.get_home_ts_pct(n=8)

		t_ats_record = 0 if team.get_ats_wins(n=8) == 0 else team.get_ats_wins(n=8) / (team.get_ats_wins(n=8) + team.get_ats_losses(n=8))
		o_ats_record = 0 if opp.get_ats_wins(n=8) == 0 else opp.get_ats_wins(n=8) / (opp.get_ats_wins(n=8) + opp.get_ats_losses(n=8))

		t_wp = 0 if team.get_wins(n=8) == 0 else team.get_wins(n=8) / (team.get_wins(n=8) + team.get_losses(n=8))
		o_wp = 0 if opp.get_wins(n=8) == 0 else opp.get_wins(n=8) / (opp.get_wins(n=8) + opp.get_losses(n=8))

		team_ats_streak = team.get_ats_streak(n=8)
		opp_ats_streak = opp.get_ats_streak(n=8)

		playoff_start_date = playoff_start_dates[season_index].date()
		time_of_season = gut_util.get_time_of_season(matchup.date, playoff_start_date, game_count, season_length)
		
		if time_of_season != 1:
			game_count = game_count - 1

		lines_by_season[season_index].append(np.array([team_ats_streak, opp_ats_streak, matchup.line]))
		data_by_season[season_index].append(np.array([ts_ts_pct, os_ts_pct, time_of_season, t_wp, o_ats_record, ts_ats_record, os_ats_record, outcome]))

		count = count - 1

t = League(start_date='2020-10-20', end_date='2015-10-10')
go(t)
gut_util.train_test(lines_by_season, data_by_season)