import matplotlib.pyplot as plt 
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
import statistics
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

def get_time_of_season(date, playoff_start_date, game_count, season_length):
	time_of_season = 0

	# playoffs
	if date >= playoff_start_date:
		#print('playoffs',  matchup.date, playoff_start_dates[season_index], game_count, season_length)			
		time_of_season = 1
	# first third of the season
	elif game_count < season_length/3:
		#print('1', matchup.date, game_count, season_length/3)
		time_of_season = 0
	# second third of the season
	elif game_count < 2*(season_length/3):
		#print('2', matchup.date, game_count, 2*(season_length/3))
		time_of_season = .33
	# last third of the season
	elif game_count <= season_length:
		#print('3', matchup.date, game_count, season_length)
		time_of_season = .66

	return time_of_season


def train_test(lines_by_season, data_by_season):
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