import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import re

class PageStructureHandler:

	def __init__(self):
		# Setup
		opts = Options()
		#opts.set_headless()
		self.driver = Chrome(executable_path='chromedriver', options=opts)  # Optional argument, if not specified will search path.

	def __delete__(self):
		self.driver.close()

	"""
	Category handling

	TODO: Add a category scraper to enable a simplified search function which generates correct URLs from region, category,
	searchword etc.
	"""
	CATEGORY_ROOT_URL = 'http://www.blocket.se/'

	class Category:

		def __init__(self, name, path):
			self.name = name
			self.path = path

			self.parent = None
			self.children = []

		def __str__(self):
			return "%s @ %s" % (self.name, self.href)

	def get_categories(self):
		self.driver.get(CATEGORY_ROOT_URL)

		# Accept GDPR settings
		gdpr_button = self.driver.find_element_by_class_name("gENsPd")
		if gdpr_button:
			gdpr_button.click()


		# Open categories menu
		categories_button = self.driver.find_element_by_class_name("dTOiRs")
		categories_button.click()

		# Get category elements
		category_picker = self.driver.find_element_by_class_name("fvdgvT")
		all_children_by_tag = category_picker.find_elements_by_tag_name("a")
		
		# Parse category elements
		all_categories = list()
		for child in all_children_by_tag:
			href = child.get_property("href")
			
			all_categories.append(Category(name, href))

		return all_categories

	"""
	Ad handling

	Get all available ads from a search page URL (manually selected by the user)
	"""
	def get_all_ads(self, first_search_page_url):

		self.driver.get(first_search_page_url)

		# Get number of pages
		page_buttons = self.driver.find_elements_by_class_name("Pagination__Button-uamu6s-1")
		num_pages = 1
		p = re.compile(r"page=(\d+)")
		for button in page_buttons:
			href = button.get_property("href")

			# Check if link to next page
			if href:
				match = p.search(href)

				if match:
					page_num = int(match.group(1))
					num_pages = max(page_num, num_pages)

		print("Num pages:", num_pages)

		# all_links = self.driver.find_elements_by_tag_name("a")
		# ad_links = list()
		# for link in all_links:
		# 	href = link.get_property("href")
			
		# 	if "/annons/" in href:
		# 		ad_links.append(href)

		# print(ad_links)

if __name__ == '__main__':
	URLs = ["https://www.blocket.se/annonser/hela_sverige?page=124&q=v70",
		"https://www.blocket.se/annonser/hela_sverige/elektronik/ljud_bild/foto_videokameror?cg=5042&q=fuji%2A",
		"https://www.blocket.se/annonser/hela_sverige/fritid_hobby/cyklar?cg=6060&q=focus"]

	structure_handler = PageStructureHandler()

	for url in URLs:
		structure_handler.get_all_ads(url)
	
	del structure_handler