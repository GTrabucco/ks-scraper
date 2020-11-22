from gut.scenario import Scenario
from gut.team import Team
from gut.league import League
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
import statsmodels.api as sm
import statistics 
from datetime import date, datetime, timedelta

t = Team("Celtics", start_date="2015-03-20", end_date="2015-05-20")
#print(game.pbp())

for i in t.schedule[4].lineup.lineup:
	print(i.player_name, i.trb)

exit()

X = []
Y = []
count = 0
for matchup in t.schedule:
	team = Team(matchup.team, season="2019", end_date=matchup.date-timedelta(days=1))
	opp = Team(matchup.opponent, season="2019", end_date=matchup.date-timedelta(days=1))
	site = 1
	if matchup.site == 'home':
		t_dps_avg_l5 = 0
		o_dps_avg_l5 = 0
		
		for i in team.get_away_matchups()[-2:]:
			t_dps_avg_l5 = t_dps_avg_l5 + i.dps

		for i in team.get_away_matchups()[-2:]:
			o_dps_avg_l5 = o_dps_avg_l5 + i.dps

		t_dps_avg_l5 = t_dps_avg_l5/2
		o_dps_avg_l5 = o_dps_avg_l5/2

		t_dpa_avg_l5 = 0
		o_dpa_avg_l5 = 0

		for i in team.get_home_matchups()[-2:]:	
			t_dpa_avg_l5 = t_dpa_avg_l5 + i.dpa

		for i in team.get_away_matchups()[-2:]:
			o_dpa_avg_l5 = o_dpa_avg_l5 + i.dpa

		t_dpa_avg_l5 = t_dpa_avg_l5/2
		o_dpa_avg_l5 = o_dpa_avg_l5/2

		team_avg_total = team.avg_home_total
		opp_avg_total = opp.avg_away_total
		team_avg_line = team.avg_home_line
		opp_avg_line = opp.avg_away_line

	if matchup.site == 'away':
		site = -1
		t_dps_avg_l5 = 0
		o_dps_avg_l5 = 0

		for i in team.get_away_matchups()[-2:]:
			t_dps_avg_l5 = t_dps_avg_l5 + i.dps

		for i in team.get_home_matchups()[-2:]:
			o_dps_avg_l5 = o_dps_avg_l5 + i.dps

		t_dps_avg_l5 = t_dps_avg_l5/2
		o_dps_avg_l5 = o_dps_avg_l5/2

		t_dpa_avg_l5 = 0
		o_dpa_avg_l5 = 0

		for i in team.get_away_matchups()[-2:]:
			t_dpa_avg_l5 = t_dpa_avg_l5 + i.dpa

		for i in team.get_home_matchups()[-2:]:
			o_dpa_avg_l5 = o_dpa_avg_l5 + i.dpa

		t_dpa_avg_l5 = t_dpa_avg_l5/2
		o_dpa_avg_l5 = o_dpa_avg_l5/2

		team_avg_total = team.avg_away_total
		opp_avg_total = opp.avg_home_total
		team_avg_line = team.avg_away_line
		opp_avg_line = opp.avg_home_line

	t_ou_record = (team.ou_overs/(team.ou_overs + team.ou_unders + team.ou_pushes)) if team.ou_overs > 0 else 0
	opp_ou_record = (opp.ou_overs/(opp.ou_overs + opp.ou_unders + opp.ou_pushes)) if opp.ou_overs > 0 else 0

	x_row = np.array([team.win_pct, opp.win_pct, matchup.line, t_dps_avg_l5, o_dps_avg_l5, t_dpa_avg_l5, o_dpa_avg_l5, team_avg_line, opp_avg_line])
	y_row = np.array([matchup.su_margin])
	X.append(x_row)
	Y.append(y_row)
	count = count + 1


# with sklearn
#regr = linear_model.LinearRegression()
#regr.fit(new_data, n_Y)

#print('Intercept: \n', regr.intercept_)
#print('Coefficients: \n', regr.coef_)

# prediction with sklearn

#print ('Predicted Margin: \n', regr.predict([[-7, 9, 17, 1, -4.22, 4.14]]))

# with statsmodels

corr = np.corrcoef(X, rowvar=0)
w, v = np.linalg.eig(corr)
print(w)

 
model = sm.OLS(Y, X).fit()
predictions = model.predict(X) 
 
print_model = model.summary()
print(print_model)
