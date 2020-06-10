import requests
from bs4 import BeautifulSoup
import re
import os

from datetime import datetime
import locale

import json

# NOTE: computer locale settings must be set to swedish for this to work
# Explicitly setting sv_SE for some reason doesn't work...
locale.setlocale(locale.LC_ALL, "")

def get_page_contents(url):

	# Parse page
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	items = [{"tag": "h1", "class_regex": ".*gjFLVU", "info_key": "heading"},
		{"tag": "div", "class_regex": ".*EkzGO", "info_key": "price", "process": lambda price: int(price.split(" kr")[0].replace(" ", ""))},
		{"tag": "a", "class_regex": ".*cwhgTa", "info_key": "location", "process": lambda loc: loc.split(" (")[0]},
		{"tag": "span", "class_regex": ".*ZAknf", "info_key": "time", "process": lambda time: "%s " % datetime.now().year + time.split(": ")[1]},
		{"tag": "div", "class_regex": ".*bYSeDO", "info_key": "description"}
		]

	contents = dict()
	for item in items:
		regex = re.compile(item["class_regex"])
		
		for part in soup.find_all(item["tag"], {"class": regex}):
			raw_text = part.get_text()

			if "process" in item:
				contents[item["info_key"]] = item["process"](raw_text)

			else:
				contents[item["info_key"]] = raw_text

	return contents

def append_page_contents_to_file(path, append_content):
	
	if not os.path.exists(path) or os.path.getsize(path) == 0:
		with open(path, "w") as new_json_file:
			new_json_file.write("[]")

	with open(path, "r") as old_json_file:
		old_content = json.load(old_json_file)

	old_content += (append_content)

	with open(path, "w") as json_file:
		json.dump(old_content, json_file)

if __name__ == '__main__':
	
	URLs = [
		"https://www.blocket.se/annons/goteborg/fujinon_xf_18_135_3_5_5_6_r_lm_ois_wr/89807514",
		"https://www.blocket.se/annons/goteborg/sony_fe_28_f_2/90267510",
		"https://www.blocket.se/annons/goteborg/sony_e_50mm_f_1_8_oss/90267495"
		]

	for url in URLs:
		contents = get_page_contents(url)
		append_page_contents_to_file("test.json", contents)