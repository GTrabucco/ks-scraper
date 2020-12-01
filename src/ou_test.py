from gut.scenario import Scenario
from gut.team import Team
from gut.league import League
from logistic_regression_tests import LogisticRegression
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

prev_turnovers = input("Enter Previous Turnovers: ")
prev_assists = input("Enter Previous Assists: ")

#t = League(start_date='2017-01-01', end_date='2020-10-11')
t = Team("Celtics", season="2019")

count = len(t.schedule)
data = []
for matchup in t.schedule:
	print(matchup.date, count)
	team = Team(matchup.team, end_date=matchup.date, start_date=matchup.date-timedelta(days=15))
	last_matchup = None
	try:
		last_matchup = team.schedule[-1:][0]
	except:
		continue

	players = []
	opp_players = []
	for i in matchup.lineup.starters:
		players.append(i.player_id)

	if last_matchup == None:
		last_matchup_assists = 0
		last_matchup_turnovers = 0
	else:
		last_matchup_assists = last_matchup.assists
		last_matchup_turnovers = last_matchup.turnovers

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

input_data = []
input_data.append(np.array([int(prev_turnovers), int(prev_assists)]))

predict = regressor.predict_print(input_data)
if predict[0] == 0:
	print('The GUT likes the Under')
else:
	print('The GUT likes the Over')