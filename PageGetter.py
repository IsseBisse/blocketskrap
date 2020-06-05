import requests
from bs4 import BeautifulSoup
import re

def get_page_contents(URL):

	# Parse page
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	
	items = [{"tag": "h1", "class_regex": ".*gjFLVU", "info_key": "heading"},
		{"tag": "div", "class_regex": ".*EkzGO", "info_key": "price"},
		{"tag": "div", "class_regex": ".*bYSeDO", "info_key": "description"}]
	
	info = dict()
	for item in items:
		regex = re.compile(item["class_regex"])
		for part in soup.find_all(item["tag"], {"class": regex}):
			info[item["info_key"]] = part.get_text()

	return info

if __name__ == '__main__':
	
	URLs = ["https://www.blocket.se/annons/goteborg/fujinon_xf_18_135_3_5_5_6_r_lm_ois_wr/89807514",
		"https://www.blocket.se/annons/goteborg/sony_fe_28_f_2/90267510",
		"https://www.blocket.se/annons/goteborg/sony_e_50mm_f_1_8_oss/90267495"]

	items = list()
	for url in URLs:
		items.append(get_page_contents(url))

	print(items)