from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	df = pd.read_csv("Spam-Classification-Flask/Dataset/spam.csv", encoding="latin-1")
	df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)
	
	# Features and Labels
	df['label'] = df['class'].map({'ham': 0, 'spam': 1})
	X = df['message']
	y = df['label']
	
	# Extract Feature With CountVectorizer
	cv = CountVectorizer()
	X = cv.fit_transform(X)  # Fit the Data
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=99)
	
	# Naive Bayes Classifierpy
	clf = MultinomialNB()
	clf.fit(X_train, y_train)
	clf.score(X_test, y_test)
	accuracy = clf.score(X_test, y_test)
	size = df.shape
	print('accuracy= ', accuracy*100)
	print("Training size = ", size)
	if request.method == 'POST':
		message = request.form['message']
		# print(message)
		data = [message]
		# print(data)
		vect = cv.transform(data).toarray()
		# print(vect)
		my_prediction = clf.predict(vect)
	return render_template('index.html', prediction=my_prediction)

app.run(debug=True)