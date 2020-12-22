from gut.scenario import Scenario
from gut.team import Team
from gut.league import League
from gut.rotation import Rotation
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

#win-loss percentage of home team games
#point differential per game of home team
#win-loss percentage of previous 8 games for visitor
#the win-loss percentage as visitor or home as the respective situation of the teams

#t = League(start_date='2020-10-11', end_date='2017-08-11')
#t = Team("Celtics", season="2019")
#t = Scenario("pthree pointers attempted>=44 and pTPP >=38")

lines_by_season = [[], [], [], [], []]

data_by_season = [[], [], [], [], []]

def calculate():
	season = 2015
	test_index = 4
	while test_index >= 0:
		print('Test on:', season)
		season = season + 1
		scaler = MinMaxScaler()
		train_lines = []
		train_data = []
		test_lines = []
		test_data = []

		# split data to train and test
		# line data needs to be feature scaled first before joining data
		for i in range(len(lines_by_season)):
			if i != test_index:
				train_lines.append(lines_by_season[i])
			else:
				test_lines.append(lines_by_season[i])

		data_by_season_copy = copy.deepcopy(data_by_season)
		test_data = data_by_season_copy.pop(test_index)
		train_data = np.array(np.concatenate(data_by_season_copy, axis=0))
		scaled_train_lines = scaler.fit_transform(np.concatenate(train_lines))
		scaled_test_lines = scaler.transform(test_lines[0])
		true_data = []

		for x,y in zip(scaled_train_lines, train_data):
			k = np.concatenate([x,y])
			true_data.append(k)

		df = pd.DataFrame(true_data)
		x_train = df.iloc[:, : -1]
		y_train = df.iloc[:, -1]

		# test
		test_true_data = []
		for i,j in zip(scaled_test_lines, test_data):
			k = np.concatenate((i, j), axis=0)
			test_true_data.append(k)

		test_df = pd.DataFrame(test_true_data)
		x_test = test_df.iloc[:, : -1]
		y_test = test_df.iloc[:, -1]

		clf = LogisticRegression(random_state=0).fit(x_train, y_train)
		score = clf.score(x_test, y_test)
		y_pred_probs = clf.predict_proba(x_test)
		wins = 0
		losses = 0
		for i,j in zip(y_pred_probs, y_test): 
			if i[1] <= .4:
				if j == 0:
					wins = wins + 1
				else:
					losses = losses + 1
			elif i[1] >= .6:
				if j == 1:
					wins = wins + 1
				else:
					losses = losses + 1

		print('Overall:', score)
		print('Confident:', wins, losses, wins/(wins+losses))
		model = sm.OLS(y_test, x_test)
		results = model.fit()
		print(results.summary())
		print()
		print()
		print()
		#plot_confusion_matrix(clf, x_test, y_test)
		#plt.show()
		test_index = test_index - 1

def go(t):
	count = int(len(t.schedule)/2)
	data = []
	lines = []
	test_data = []
	test_lines = []
	season_index = 0
	current_season = ""
	for matchup in t.schedule[::2]:
		print(matchup.date, count)

		if current_season == "":
			current_season = matchup.season
		elif current_season != matchup.season:
			season_index = season_index + 1
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
			ts_ats_record = 0 if team.get_ats_home_wins() == 0 else team.get_ats_home_wins() / (team.get_ats_home_wins() + team.get_ats_home_losses())
			os_ats_record = 0 if opp.get_ats_away_wins() == 0 else opp.get_ats_away_wins() / (opp.get_ats_away_wins() + opp.get_ats_away_losses())

			# home team win pct
			ht_wp = 0 if team.ats_wins == 0 else team.get_ats_wins() / (team.get_ats_wins() + team.get_ats_losses())

			# home team avg point differential
			#ht_pd = team.get_point_diff()/len(team.schedule)

			t_avg_ls = team.get_avg_home_line()
			o_avg_ls = opp.get_avg_away_line()
			ts_ts_pct = team.get_home_ts_pct()
			os_ts_pct = opp.get_away_ts_pct()

		elif matchup.site == 'away':
			os_ats_record = 0 if opp.get_ats_home_wins() == 0 else opp.get_ats_home_wins() / (opp.get_ats_home_wins() + opp.get_ats_home_losses())
			ts_ats_record = 0 if team.get_ats_away_wins() == 0 else team.get_ats_away_wins() / (team.get_ats_away_wins() + team.get_ats_away_losses())

			# home team win pct
			ht_wp = 0 if opp.get_ats_wins() == 0 else opp.get_ats_wins() / (opp.get_ats_wins() + opp.get_ats_losses())

			t_avg_ls = team.get_avg_away_line()
			o_avg_ls = opp.get_avg_home_line()
			ts_ts_pct = team.get_away_ts_pct()
			os_ts_pct = opp.get_home_ts_pct()

		#team last 8 games
		#t_ats_pd_l8 = 0 if len(team.schedule) == 0 else statistics.mean([x.ats_margin for x in team.get_last_n_matchups(8)])

		#opp last 8 games
		#o_ats_pd_l8 = 0 if len(opp.schedule) == 0 else statistics.mean([x.ats_margin for x in opp.get_last_n_matchups(8)])

		#team last 8 games
		#t_hw_l8 = 0 if len(team.schedule) == 0 else sum(1 for x in team.get_last_n_matchups(8) if x.ats_record == 'W')

		#opp last 8 games
		#o_aw_l8 = 0 if len(opp.schedule) == 0 else sum(1 for x in opp.get_last_n_matchups(8) if x.ats_record == 'W')

		# team away win pct last 8 win pct
		#t_wp_l8 = 0 if t_hw_l8 == 0 else t_hw_l8/8
		#o_wp_l8 = 0 if o_aw_l8 == 0 else o_aw_l8/8

		t_ats_record = 0 if team.get_ats_wins() == 0 else team.get_ats_wins() / (team.get_ats_wins() + team.get_ats_losses())
		o_ats_record = 0 if opp.get_ats_wins() == 0 else opp.get_ats_wins() / (opp.get_ats_wins() + opp.get_ats_losses())

		t_wp = 0 if team.get_wins() == 0 else team.get_wins() / (team.get_wins() + team.get_losses())
		o_wp = 0 if opp.get_wins() == 0 else opp.get_wins() / (opp.get_wins() + opp.get_losses())

		team_ats_streak = team.get_ats_streak()
		opp_ats_streak = opp.get_ats_streak()

		season_length = 82
		if matchup.season == "2019":
			season_length = 68

		if len(team.schedule) < season_length/3:
			time_of_season = 0
		elif len(team.schedule) < 2*(season_length/3):
			time_of_season = .5
		else:
			time_of_season = 1

		lines_by_season[season_index].append(np.array([team_ats_streak, opp_ats_streak, matchup.line]))
		data_by_season[season_index].append(np.array([ts_ts_pct, os_ts_pct, time_of_season, t_wp, o_ats_record, ts_ats_record, os_ats_record, outcome]))

		count = count - 1

t = League(start_date='2020-10-20', end_date='2015-10-10')
#t = Team("Celtics", start_date='2020-10-11', end_date='2015-10-11')
go(t)
calculate()