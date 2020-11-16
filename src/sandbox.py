from matchup import Matchup
from scenario import Scenario
from team import Team
from league import League


t = Team("Celtics")
matchups = t.schedule

dps_sum = []
dpa_sum = []
margin_list = []

for i,x in enumerate(matchups):
	if i < 15:
		continue
	last_n_games = matchups[i-15:i]
	t = sum(x.dps for x in last_n_games)
	d = sum(x.dpa for x in last_n_games)
	dps_sum.append(t)
	dpa_sum.append(d)
	margin_list.append(x.ou_margin)

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
