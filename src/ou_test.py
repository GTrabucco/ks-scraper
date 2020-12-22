from gut.scenario import Scenario
from gut.team import Team
from gut.league import League
from gut.rotation import Rotation
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from sklearn.feature_selection import VarianceThreshold
import seaborn as sns
import matplotlib.pyplot as plt 
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
import statistics
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

#win-loss percentage of home team games
#point differential per game of home team
#win-loss percentage of previous 8 games for visitor
#the win-loss percentage as visitor or home as the respective situation of the teams


#t = League(start_date='2020-10-11', end_date='2017-08-11')

#t = Team("Celtics", season="2019")
#t = Scenario("pthree pointers attempted>=44 and pTPP >=38")

def calculate(train_data, train_lines, test_data, test_lines):
	# train
	print(len(train_data), len(train_lines), len(test_data), len(test_lines))
	mm_scaler = MinMaxScaler()
	lines_scaled = mm_scaler.fit_transform(train_lines)

	true_data = []
	for i,j in zip(lines_scaled, train_data):
		k = np.concatenate((i, j), axis=0)
		true_data.append(k)

	df = pd.DataFrame(true_data)
	x_train = df.iloc[:, : -1]
	y_train = df.iloc[:, -1]

	# test
	test_mm_scaler = MinMaxScaler()
	test_lines_scaled = mm_scaler.fit_transform(test_lines)

	test_true_data = []
	for i,j in zip(test_lines_scaled, test_data):
		k = np.concatenate((i, j), axis=0)
		test_true_data.append(k)

	test_df = pd.DataFrame(test_true_data)
	x_test = df.iloc[:, : -1]
	y_test = df.iloc[:, -1]

	#x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

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

	print(wins, losses)
	print(score)
	model = sm.OLS(y_test, x_test)
	results = model.fit()
	print(results.summary())


def go(t):
	count = len(t.schedule)
	data = []
	lines = []
	test_data = []
	test_lines = []
	for matchup in t.schedule:
		#print(matchup.date, count)
		team = Team(matchup.team, season=matchup.season, start_date=matchup.date-timedelta(days=1))
		opp = Team(matchup.opponent, season=matchup.season, start_date=matchup.date-timedelta(days=1))

		if len(team.schedule) < 8 or len(opp.schedule) < 8:
			count = count - 1
			continue

		outcome = 0
		if matchup.ou_record == 'O':
			outcome = 1
		
		if matchup.site == 'home':
			ts_ou_record = 0 if team.home_ou_overs == 0 else team.home_ou_overs / (team.home_ou_overs + team.home_ou_unders)
			os_ou_record = 0 if opp.away_ou_overs == 0 else opp.away_ou_overs / (opp.away_ou_overs + opp.away_ou_unders)

			# home team win pct
			ht_wp = 0 if team.ats_wins == 0 else team.ats_wins / (team.ats_wins + team.ats_losses)

			# home team avg point differential
			ht_pd = team.point_diff/len(team.schedule)

			t_avg_ls = team.avg_home_line
			o_avg_ls = opp.avg_away_line

		elif matchup.site == 'away':
			os_ou_record = 0 if opp.home_ou_overs == 0 else opp.home_ou_overs / (opp.home_ou_overs + opp.home_ou_unders)
			ts_ou_record = 0 if team.away_ou_overs == 0 else team.away_ou_overs / (team.away_ou_overs + team.away_ou_unders)

			# home team win pct
			ht_wp = 0 if opp.ats_wins == 0 else opp.ats_wins / (opp.ats_wins + opp.ats_losses)

			t_avg_ls = team.avg_away_line
			o_avg_ls = opp.avg_home_line

		#team last 8 games
		t_ou_pd_l8 = 0 if len(team.schedule) == 0 else statistics.mean([x.ou_margin for x in team.get_last_n_matchups(8)])

		#opp last 8 games
		o_ou_pd_l8 = 0 if len(opp.schedule) == 0 else statistics.mean([x.ou_margin for x in opp.get_last_n_matchups(8)])

		#team last 8 games
		t_ou_l8 = 0 if len(team.schedule) == 0 else sum(1 for x in team.get_last_n_matchups(8) if x.ou_record == 'O')

		#opp last 8 games
		o_ou_l8 = 0 if len(opp.schedule) == 0 else sum(1 for x in opp.get_last_n_matchups(8) if x.ou_record == 'O')

		# team away win pct last 8 win pct
		t_oup_l8 = 0 if t_ou_l8 == 0 else t_ou_l8/8
		o_oup_l8 = 0 if o_ou_l8 == 0 else o_ou_l8/8

		t_ou_record = 0 if team.ou_overs == 0 else team.ou_overs / (team.ou_overs + team.ou_unders)
		o_ou_record = 0 if opp.ou_overs == 0 else opp.ou_overs / (opp.ou_overs + opp.ou_unders)

		t_wp = 0 if team.wins == 0 else team.wins / (team.wins + team.losses)
		o_wp = 0 if opp.wins == 0 else opp.wins / (opp.wins + opp.losses)

		if matchup.season != "2019":
			lines.append(np.array([team.get_ou_streak()]+[opp.get_ou_streak()]+[matchup.total]))
			data.append(np.array([o_ou_record]+[outcome]))
		else:
			test_lines.append(np.array([team.get_ou_streak()]+[opp.get_ou_streak()]+[matchup.total]))
			test_data.append(np.array([o_ou_record]+[outcome]))

		count = count - 1

	calculate(data, lines, test_data, test_lines)

seasons = ["2019", "2018", "2017", "2016"]
for i in seasons:
	print(i)
	t = League(start_date='2020-10-11', end_date='2015-10-01')
	#t = Team("Celtics", start_date='2020-10-11', end_date='2016-10-25')
	go(t)
	exit()
