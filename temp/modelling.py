import json
import re

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

with open("data/v70__hela_sverige__post2008.json") as json_file:
	data = json.load(json_file)

valid_age = [4, 12]
valid_data = list()
for i, item in enumerate(reversed(data)):
	if ("price" in item and "general" in item):
		item["details"] = parse_car_details(item["general"])
	
		if "Ålder" in item["details"] and item["details"]["Ålder"] >= valid_age[0] and item["details"]["Ålder"] <= valid_age[1]: 
			valid_data.append(item)
		
num_items = len(valid_data)
print(num_items)
Y = np.array([item["price"] for item in valid_data])
X = np.array([[item["details"]["Ålder"], item["details"]["Miltal"]] for item in valid_data])

# plt.subplot(211)
# plt.plot(X[:,0], Y, 'o')

# plt.subplot(212)
# plt.plot(X[:,1], Y, 'o')
# plt.show()

fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(X[:,0], X[:,1], Y)
plt.show()