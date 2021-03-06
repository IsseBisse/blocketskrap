import tensorflow as tf
from tensorflow import keras
import keras.wrappers.scikit_learn as kw_learn
import sklearn.model_selection as model_sel

import json
import re
import numpy as np

'''
DATA
'''
def parse_car_details(detail_string):

	# Split detail string into parts
	pattern = re.compile(" [A-Z]")
	split_points = [0] + [match.start() for match in pattern.finditer(detail_string)]
	parts = [detail_string[i:j] for i,j in zip(split_points, split_points[1:]+[None])]

	# Trim spaces
	parts[1:] = [item[1:] for item in parts[1:]]
	
	# Split "category" an value
	pattern = re.compile("[a-z][A-Z0-9]")
	details = dict()
	for item in parts:
		match = pattern.search(item)

		if match:
			split_point = match.start() + 1
			char = {item[:split_point]: item[split_point:]}

			# Change data type of certain characteristics
			if "Miltal" in char:
				if char["Miltal"] == "Mer än 50 000":
					char["Miltal"] = 50000

				else:
					char["Miltal"] = int(char["Miltal"].split(" - ")[0].replace(" ", ""))

			elif "Hästkrafter" in char:
				char["Hästkrafter"] = int(char["Hästkrafter"])

			elif "Modellår" in char:
				char["Ålder"] = 2020 - int(char["Modellår"])


			details.update(char)

	return details

def load_and_preprocess(path):

	with open(path) as json_file:
		data = json.load(json_file)

	valid_age = [4, 12]
	valid_data = list()
	for i, item in enumerate(reversed(data)):
		if ("price" in item and "general" in item):
			item["details"] = parse_car_details(item["general"])
		
			if "Ålder" in item["details"] and item["details"]["Ålder"] >= valid_age[0] and item["details"]["Ålder"] <= valid_age[1]: 
				valid_data.append(item)

	num_items = len(valid_data)
	Y = np.array([item["price"] for item in valid_data])
	X = np.array([[item["details"]["Ålder"], item["details"]["Miltal"]] for item in valid_data])

	return (X, Y)

'''
MODEL
'''
def create_model(input_shape):

	model = keras.Sequential([
		keras.layers.Dense(5, input_dim=input_shape, activation="relu"),
		keras.layers.Dense(5, activation="relu"),
		keras.layers.Dense(1)])

	model.compile(loss="mean_squared_error", optimizer="adam")

	return model

def evaluate_model(model, X, Y):
	# evaluate model
	estimator = kw_learn.KerasRegressor(build_fn=model, epochs=100, batch_size=5, verbose=0)
	kfold = model_sel.KFold(n_splits=10)
	results = model_sel.cross_val_score(estimator, X, Y, cv=kfold)
	print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))

def main():
	# Load data
	path = "../data/v70__hela_sverige__post2008.json"
	(X, Y) = load_and_preprocess(path)

	# Create model
	model = create_model(X.shape[1])
	evaluate_model(model, X, Y)

if __name__ == '__main__':
	main()