from scenario import Scenario
from team import Team
from league import League
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
import statsmodels.api as sm

scenario = Scenario("pthree pointers attempted>=44 and pTPP >=38")




dps_sum = []
dpa_sum = []
margin_list = []

for s in scenario.schedule:
	team = Team(s.team)
	print(team.name, s.date)
	end_index = [x.date for x in team.schedule].index(s.date)
	start_index = end_index-15

	if start_index < 0:
		start_index = 0

	last_n_games = team.get_matchups_by_range(team.schedule[start_index].date, team.schedule[end_index-1].date)

	t = sum(x.dps for x in last_n_games)
	d = sum(x.dpa for x in last_n_games)
	dps_sum.append(t)
	dpa_sum.append(d)
	margin_list.append(team.schedule[end_index].ou_margin)
exit()

data = {'DPA L15': dpa_sum,
        'DPS L15': dps_sum,
        'Margin': margin_list}

df = pd.DataFrame(data,columns=['DPA L15','DPS L15','Margin'])

X = df[['DPA L15','DPS L15']] # here we have 2 variables for multiple regression. If you just want to use one variable for simple linear regression, then use X = df['Interest_Rate'] for example.Alternatively, you may add additional variables within the brackets
Y = df['Margin']
 
# with sklearn
regr = linear_model.LinearRegression()
regr.fit(X, Y)

print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

# prediction with sklearn
New_Line = -4
New_DPS_L15 = 2.3
print ('Predicted Margin: \n', regr.predict([[New_Line, New_DPS_L15]]))

# with statsmodels
X = sm.add_constant(X) # adding a constant
 
model = sm.OLS(Y, X).fit()
predictions = model.predict(X) 
 
print_model = model.summary()
print(print_model)
