import numpy as np

class LogisticRegression:
	def __init__(self, lr=0.01, n_iters=1000):
		self.lr = lr
		self.n_iters = n_iters
		self.weights = None
		self.bias = None

	def fit(self, X, y):
		# init parameters
		n_samples, n_features = X.shape
		self.weights = np.zeros(n_features)
		self.bias = 0

		# graident descent
		for _ in range(self.n_iters):
			linear_model = np.dot(X, self.weights) + self.bias
			y_predicted = self._sigmoid(linear_model)

			dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
			db = (1 / n_samples) * np.sum(y_predicted - y)

			self.weights -= self.lr * dw
			self.bias -= self.lr * db

	def predict(self, X):
		linear_model = np.dot(X, self.weights) + self.bias
		y_predicted = self._sigmoid(linear_model)
		y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
		return y_predicted_cls

	def predict_print(self, X):
		linear_model = np.dot(X, self.weights) + self.bias
		y_predicted = self._sigmoid(linear_model)
		confidence = ""
		if y_predicted[0] > 0.5:
			confidence = '{:.1%}'.format(abs(y_predicted[0]))
		else:
			confidence = '{:.1%}'.format(abs(1 - y_predicted[0]))

		print('GUT Confidence:', confidence)

		y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
		return y_predicted_cls

	def _sigmoid(self, x):
		return 1 / (1 + np.exp(-x))