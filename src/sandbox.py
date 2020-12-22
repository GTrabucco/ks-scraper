from gut.scenario import Scenario
from gut.team import Team
from gut.league import League
import statistics 
from datetime import date, datetime, timedelta
from gut.rotation import Rotation
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
from logistic_regression_tests import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
from scipy.optimize import fmin_tnc
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix

season = "2019"

#t = Scenario("pthree pointers attempted>=44 and pTPP >=38")
#t = Team("Celtics", season=season)
t = League(start_date='2017-01-01', end_date='2020-10-11')
#print(game.pbp())

#X = []
#Y = []

count = len(t.schedule)
data = []
for matchup in t.schedule:
	print(matchup.date, count)
	team = Team(matchup.team, end_date=matchup.date, start_date=matchup.date-timedelta(days=15))
	#opp = Team(matchup.opponent, season=season, end_date=matchup.date, start_date=matchup.date-timedelta(days=15))
	last_matchup = None
	try:
		last_matchup = team.schedule[-1:][0]
		#opp_last_matchup = opp.schedule[-1:][0]
	except:
		continue

	players = []
	opp_players = []
	for i in matchup.lineup.starters:
		players.append(i.player_id)

	#for i in matchup.opponent_lineup.starters:
	#	opp_players.append(i.player_id)

	#r = Rotation(players, matchup.team, matchup.season)
	#o_r = Rotation(opp_players, matchup.opponent, matchup.season)

	#v = r.get_formatted_data() + o_r.get_formatted_data()

	if last_matchup == None:
		last_matchup_pfs = 0
		last_matchup_ftas = 0
		last_matchup_assists = 0
		last_matchup_turnovers = 0
		last_matchup_3pas = 0
	else:
		last_matchup_pfs = last_matchup.pfs
		last_matchup_ftas = last_matchup.ftas
		last_matchup_assists = last_matchup.assists
		last_matchup_turnovers = last_matchup.turnovers
		last_matchup_3pas = last_matchup.fg3as
		last_matchup_stls = last_matchup.stls

	outcome = 0
	if matchup.ou_record == 'O':
		outcome = 1
	
	data.append(np.array([last_matchup_turnovers]+[last_matchup_assists]+[outcome]))
	count = count - 1

df = pd.DataFrame(data)
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

def accuracy(y_true, y_pred):
	accuracy = np.sum(y_true == y_pred) / len(y_true)
	return accuracy

regressor = LogisticRegression(lr=0.0001, n_iters=1000)
regressor.fit(x_train, y_train)
predictions = regressor.predict(x_test)
print('record', accuracy(y_test, predictions))

exit()
logisticRegr = LogisticRegression()
logisticRegr.fit(x_train, y_train)

score = logisticRegr.score(x_test, y_test)
print(score)

overs = df.loc[y == 1]
unders = df.loc[y == 0]

X_seq = np.linspace(X.min(),X.max(),300).reshape(-1,1)
polyreg=make_pipeline(PolynomialFeatures(2),LogisticRegression())
polyreg.fit(X,y)

plt.scatter(overs.iloc[:, 0], overs.iloc[:, 1], s=None, label='Over')
plt.scatter(unders.iloc[:, 0], unders.iloc[:, 1], s=None, label='Under')

X = np.c_[np.ones((X.shape[0], 1)), X]
y = y[:, np.newaxis]
theta = np.zeros((X.shape[1], 1))


overs_df = overs.to_numpy()
overs_graph = np.c_[np.ones((overs_df.shape[0], 1)), overs_df]

x_values = [np.min(X[:, 1] - 2), np.max(X[:, 2] + 2)]
y_values = - (parameters[0] + np.dot(parameters[1], x_values)) / parameters[2]

plt.plot(x_values, y_values, label='Decision Boundary')
plt.xlabel('previous turnovers')
plt.ylabel('previous assists')
plt.legend()
plt.show()

exit()






















su_wins = 0
ats_wins = 0
su_losses = 0
ats_losses = 0
ou_wins = 0
ou_losses =0
units = 0

count = len(t.schedule)
for matchup in t.schedule:
	print(matchup.date, count)
	team = Team(matchup.team, season=season, end_date=matchup.date-timedelta(days=1), last_n_games = 15)
	#team = t
	opp = Team(matchup.opponent, season=season, end_date=matchup.date-timedelta(days=1), last_n_games = 15)
	site = 1
	streak = 0
	opp_streak = 0
	streak_type = ""

	if matchup.site == 'home':
		t_dps_avg_l5 = 0
		o_dps_avg_l5 = 0
		
		for i in team.get_home_matchups()[-3:]:
			t_dps_avg_l5 = t_dps_avg_l5 + i.dps

		for i in opp.get_away_matchups()[-3:]:
			o_dps_avg_l5 = o_dps_avg_l5 + i.dps

		t_dps_avg_l5 = t_dps_avg_l5/3
		o_dps_avg_l5 = o_dps_avg_l5/3

		t_dpa_avg_l5 = 0
		o_dpa_avg_l5 = 0

		for i in team.get_home_matchups()[-3:]:	
			t_dpa_avg_l5 = t_dpa_avg_l5 + i.dpa

		for i in opp.get_away_matchups()[-3:]:
			o_dpa_avg_l5 = o_dpa_avg_l5 + i.dpa

		t_dpa_avg_l5 = t_dpa_avg_l5/3
		o_dpa_avg_l5 = o_dpa_avg_l5/3

		team_avg_total = team.avg_home_total
		opp_avg_total = opp.avg_away_total
		team_avg_line = team.avg_home_line
		opp_avg_line = opp.avg_away_line
		team_avg_score = team.avg_home_score
		opp_avg_score = opp.avg_away_score
		team_avg_opp_score = team.avg_home_opp_score
		opp_avg_opp_score = opp.avg_away_opp_score

		team_reversed_schedule = team.get_home_matchups()
		team_reversed_schedule.reverse()
		opp_reversed_schedule = opp.get_away_matchups()
		opp_reversed_schedule.reverse()

		for i in team_reversed_schedule:
			if streak == 0:
				streak_type = i.su_record
				if streak_type == "W":
					streak = 1
				else:
					streak = -1
			elif streak_type == i.su_record:
				if streak_type == "W":
					streak = streak + 1
				else:
					streak = streak - 1
			else:
				break

		streak_type = ""
		for i in opp_reversed_schedule:
			if opp_streak == 0:
				streak_type = i.su_record
				if streak_type == "W":
					opp_streak = 1
				else:
					opp_streak = -1
			elif streak_type == i.su_record:
				if streak_type == "W":
					opp_streak = opp_streak + 1
				else:
					opp_streak = opp_streak - 1
			else:
				break

	if matchup.site == 'away':
		site = -1
		t_dps_avg_l5 = 0
		o_dps_avg_l5 = 0

		for i in team.get_away_matchups()[-3:]:
			t_dps_avg_l5 = t_dps_avg_l5 + i.dps

		for i in opp.get_home_matchups()[-3:]:
			o_dps_avg_l5 = o_dps_avg_l5 + i.dps

		t_dps_avg_l5 = t_dps_avg_l5/3
		o_dps_avg_l5 = o_dps_avg_l5/3

		t_dpa_avg_l5 = 0
		o_dpa_avg_l5 = 0

		for i in team.get_away_matchups()[-3:]:
			t_dpa_avg_l5 = t_dpa_avg_l5 + i.dpa

		for i in opp.get_home_matchups()[-3:]:
			o_dpa_avg_l5 = o_dpa_avg_l5 + i.dpa

		t_dpa_avg_l5 = t_dpa_avg_l5/3
		o_dpa_avg_l5 = o_dpa_avg_l5/3

		team_avg_total = team.avg_away_total
		opp_avg_total = opp.avg_home_total
		team_avg_line = team.avg_away_line
		opp_avg_line = opp.avg_home_line
		team_avg_score = team.avg_away_score
		opp_avg_score = opp.avg_home_score
		team_avg_opp_score = team.avg_away_opp_score
		opp_avg_opp_score = opp.avg_home_opp_score

		team_reversed_schedule = team.get_away_matchups()
		team_reversed_schedule.reverse()
		opp_reversed_schedule = opp.get_home_matchups()
		opp_reversed_schedule.reverse()

		for i in team_reversed_schedule:
			if streak == 0:
				streak_type = i.su_record
				if streak_type == "W":
					streak = 1
				else:
					streak = -1
			elif streak_type == i.su_record:
				if streak_type == "W":
					streak = streak + 1
				else:
					streak = streak - 1
			else:
				break

		streak_type = ""
		for i in opp_reversed_schedule:
			if opp_streak == 0:
				streak_type = i.su_record
				if streak_type == "W":
					opp_streak = 1
				else:
					opp_streak = -1
			elif streak_type == i.su_record:
				if streak_type == "W":
					opp_streak = opp_streak + 1
				else:
					opp_streak = opp_streak - 1
			else:
				break

	last_matchup = None
	try:
		last_matchup = team.schedule[-1:][0]
		opp_last_matchup = opp.schedule[-1:][0]
	except:
		continue

	t_ou_record = (team.ou_overs/(team.ou_overs + team.ou_unders + team.ou_pushes)) if team.ou_overs > 0 else 0
	opp_ou_record = (opp.ou_overs/(opp.ou_overs + opp.ou_unders + opp.ou_pushes)) if opp.ou_overs > 0 else 0

	players = []
	opp_players = []
	for i in matchup.lineup.starters:
		players.append(i.player_id)

	for i in matchup.opponent_lineup.starters:
		opp_players.append(i.player_id)

	r = Rotation(players, matchup.team, matchup.season)
	o_r = Rotation(opp_players, matchup.opponent, matchup.season)

	v = r.get_formatted_data() + o_r.get_formatted_data()

	if last_matchup == None:
		last_matchup_pfs = 0
		last_matchup_ftas = 0
		last_matchup_assists = 0
		last_matchup_turnovers = 0
		last_matchup_3pas = 0
	else:
		last_matchup_pfs = last_matchup.pfs
		last_matchup_ftas = last_matchup.ftas
		last_matchup_assists = last_matchup.assists
		last_matchup_turnovers = last_matchup.turnovers
		last_matchup_3pas = last_matchup.fg3as

	if opp_last_matchup == None:
		opp_last_matchup_pfs = 0
		opp_last_matchup_ftas = 0
		opp_last_matchup_assists = 0
		opp_last_matchup_turnovers = 0
		opp_last_matchup_3pas = 0
	else:
		opp_last_matchup_pfs = opp_last_matchup.pfs
		opp_last_matchup_ftas = opp_last_matchup.ftas
		opp_last_matchup_assists = opp_last_matchup.assists
		opp_last_matchup_turnovers = opp_last_matchup.turnovers
		opp_last_matchup_3pas = opp_last_matchup.fg3as

	outcome = 0
	if matchup.ou_record == 'O':
		outcome = 1

	if streak != 0:
		streak = streak/3

	if opp_streak != 0:
		opp_streak = opp_streak/3

	#x_row = np.array(v+[team.win_pct, opp.win_pct, matchup.line/18, site, t_ou_record, opp_ou_record, t_dps_avg_l5, o_dps_avg_l5, t_dpa_avg_l5, o_dpa_avg_l5, team_avg_line, opp_avg_line])
	x_row = np.array(v+[matchup.total, last_matchup_3pas, last_matchup_assists])
	y_row = np.array([outcome])
	X.append(x_row)
	Y.append(y_row)
	count = count - 1

scaler = MinMaxScaler()
table = X
df = pd.DataFrame(table)

ytable = pd.DataFrame(Y)
ytable.columns = ['outcome']
#df = df.transpose()
df.columns = ['fga', 'fgpct', 'fg3a', 'fg3_pct', 'efg_pct', 'total', 'lm_3pa', 'lm_ast']

df[['fga', 'fgpct', 'fg3a', 'fg3_pct', 'efg_pct', 'total', 'lm_3pa', 'lm_ast']] = scaler.fit_transform(df[['fga', 'fgpct', 'fg3a', 'fg3_pct', 'efg_pct', 'total', 'lm_3pa', 'lm_ast']])

x_vars=df
y_var=ytable

xTrain,xValid,yTrain,yValid = train_test_split(x_vars, y_var, train_size=.5, random_state=2)

LogitModel=LogisticRegression()

LogitModel.fit(xTrain, yTrain)

predictions=LogitModel.predict(xTrain)
result = accuracy_score(yTrain, predictions)
print('result', result)

yfga = ytable['outcome']

xTrain1,xValid1,yTrain,yValid = train_test_split(df, yfga, train_size=.6, random_state=2)

#Logit_fga = sm.Logit(yTrain,xTrain1)
#rrr = Logit_fga.fit()
#print(rrr.summary())




#X = sm.add_constant(X)
#model = sm.OLS(Y, X)
#results = model.fit()
#print(results.params)
#print(results.summary())


t2 = League(season="2018")
#t2 = Team("Celtics", season="2018")
for matchup in t2.schedule:
	team = Team(matchup.team, season=season, end_date=matchup.date-timedelta(days=1), last_n_games = 15)
	opp = Team(matchup.opponent, season=season, end_date=matchup.date-timedelta(days=1), last_n_games = 15)
	players = []
	opp_players = []
	for i in matchup.lineup.starters:
		players.append(i.player_id)

	for i in matchup.opponent_lineup.starters:
		opp_players.append(i.player_id)

	r = Rotation(players, matchup.team, matchup.season)
	o_r = Rotation(opp_players, matchup.opponent, matchup.season)

	v = r.get_formatted_data()

	last_matchup = None
	try:
		last_matchup = team.schedule[-1:][0]
		opp_last_matchup = opp.schedule[-1:][0]
	except:
		continue

	t_ou_record = (team.ou_overs/(team.ou_overs + team.ou_unders + team.ou_pushes)) if team.ou_overs > 0 else 0
	opp_ou_record = (opp.ou_overs/(opp.ou_overs + opp.ou_unders + opp.ou_pushes)) if opp.ou_overs > 0 else 0

	players = []
	opp_players = []
	for i in matchup.lineup.starters:
		players.append(i.player_id)

	for i in matchup.opponent_lineup.starters:
		opp_players.append(i.player_id)

	r = Rotation(players, matchup.team, matchup.season)
	o_r = Rotation(opp_players, matchup.opponent, matchup.season)

	v = r.get_formatted_data()

	if last_matchup == None:
		last_matchup_pfs = 0
		last_matchup_ftas = 0
		last_matchup_assists = 0
		last_matchup_turnovers = 0
		last_matchup_3pas = 0
	else:
		last_matchup_pfs = last_matchup.pfs
		last_matchup_ftas = last_matchup.ftas
		last_matchup_assists = last_matchup.assists
		last_matchup_turnovers = last_matchup.turnovers
		last_matchup_3pas = last_matchup.fg3as

	if opp_last_matchup == None:
		opp_last_matchup_pfs = 0
		opp_last_matchup_ftas = 0
		opp_last_matchup_assists = 0
		opp_last_matchup_turnovers = 0
		opp_last_matchup_3pas = 0
	else:
		opp_last_matchup_pfs = opp_last_matchup.pfs
		opp_last_matchup_ftas = opp_last_matchup.ftas
		opp_last_matchup_assists = opp_last_matchup.assists
		opp_last_matchup_turnovers = opp_last_matchup.turnovers
		opp_last_matchup_3pas = opp_last_matchup.fg3as


	test = model.predict(results.params, [[v+[matchup.total, last_matchup_3pas, last_matchup_assists]]])

	if test > 0 and matchup.ou_margin > 0:
		ou_wins = ou_wins + 1
		units = units + 1
	elif test < 0 and matchup.ou_margin < 0:
		ou_wins = ou_wins + 1
		units = units + 1
	else:
		ou_losses = ou_losses + 1
		units = units - 1.1

	count = count - 1

print(ou_wins, ou_losses)
print(units)
exit()
if test < matchup.su_margin:
	print('ats win su win', test, matchup.su_margin)
	ats_wins = ats_wins + 1
	units = units + 1
elif test < 0 and matchup.su_margin < 0:
	print('ats loss. su win', test, matchup.su_margin)
	su_wins = su_wins + 1
	ats_losses = ats_losses + 1
	units = units - 1.1
elif test > 0 and matchup.su_margin > 0:
	print('ats loss. su win', test, matchup.su_margin)
	su_wins = su_wins + 1
	ats_losses = ats_losses + 1
	units = units - 1.1
else:
	print('ats loss. su loss', test, matchup.su_margin)
	ats_losses = ats_losses + 1
	su_losses = su_losses + 1
	units = units - 1.1

print('su record', su_wins, su_losses)
print('ats record', ats_wins, ats_losses)
print('units', units)



#model = sm.OLS(Y, X).fit()
#predictions = model.predict(X) 
 
#print_model = model.summary()
#print(print_model)


# with sklearn
#regr = linear_model.LinearRegression()
#regr.fit(new_data, n_Y)

#print('Intercept: \n', regr.intercept_)
#print('Coefficients: \n', regr.coef_)

# prediction with sklearn

#print ('Predicted Margin: \n', regr.predict([[-7, 9, 17, 1, -4.22, 4.14]]))

# with statsmodels


