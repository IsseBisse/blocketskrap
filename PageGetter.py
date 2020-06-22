import requests
from bs4 import BeautifulSoup
import re

from datetime import datetime

import locale
# NOTE: computer locale settings must be set to swedish for this to work
# Explicitly setting sv_SE for some reason doesn't work...
locale.setlocale(locale.LC_ALL, "")

BASIC_ITEM_DESCRIPTORS = [{"tag": "h1", "class_regex": ".*gjFLVU", "info_key": "heading"},
	{"tag": "div", "class_regex": ".*EkzGO", "info_key": "price", "process": lambda price: int(price.split(" kr")[0].replace(" ", ""))},
	{"tag": "a", "class_regex": ".*cwhgTa", "info_key": "location", "process": lambda loc: loc.split(" (")[0]},
	{"tag": "span", "class_regex": ".*ZAknf", "info_key": "time", "process": lambda time: "%s " % datetime.now().year + time.split(": ")[1]},
	{"tag": "div", "class_regex": ".*bYSeDO", "info_key": "description"}
	]

CAR_DESCRIPTORS = [{"tag": "h1", "class_regex": ".*gjFLVU", "info_key": "heading"},
	{"tag": "div", "class_regex": ".*EkzGO", "info_key": "price", "process": lambda price: int(price.split(" kr")[0].replace(" ", ""))},
	{"tag": "a", "class_regex": ".*cwhgTa", "info_key": "location", "process": lambda loc: loc.split(" (")[0]},
	{"tag": "span", "class_regex": ".*ZAknf", "info_key": "time", "process": lambda time: "%s " % datetime.now().year + time.split(": ")[1]},
	{"tag": "div", "class_regex": ".*bYSeDO", "info_key": "description"},
	{"tag": "div", "class_regex": ".*gWITvi", "info_key": "general"}
	]

def get_page_contents(url, descriptors):

	# Parse page
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	id_ = url.split("/")[-1]
	contents = {"id": id_, "url": url}
	for item in descriptors:
		regex = re.compile(item["class_regex"])
		
		for part in soup.find_all(item["tag"], {"class": regex}):
			raw_text = part.get_text()

			if "process" in item:
				contents[item["info_key"]] = item["process"](raw_text)

			else:
				contents[item["info_key"]] = raw_text

	return contents

if __name__ == '__main__':
	
	BASIC_URLs = [
		"https://www.blocket.se/annons/goteborg/fujinon_xf_18_135_3_5_5_6_r_lm_ois_wr/89807514",
		"https://www.blocket.se/annons/goteborg/sony_fe_28_f_2/90267510",
		"https://www.blocket.se/annons/goteborg/sony_e_50mm_f_1_8_oss/90267495"
		]

	CAR_URLs = [
		"https://www.blocket.se/annons/ostergotland/volvo_v70_d5_summum_/69067350",
		"https://www.blocket.se/annons/orebro/volvo_v70_2_0_bi_fuel_momentum_218hk/85804568"
		]

	# for url in BASIC_URLs:
	# 	contents = get_page_contents(url, BASIC_ITEM_DESCRIPTORS)
	# 	append_page_contents_to_file("test.json", contents)

	for url in CAR_URLs:
		contents = get_page_contents(url, CAR_DESCRIPTORS)
		#append_page_contents_to_file("test.json", contents)
		print(contents)