import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

ROOT_URL = 'http://www.blocket.se/'

class Category:

	def __init__(self, name, path):
		self.name = name
		self.path = path

		self.parent = None
		self.children = []

	def __str__(self):
		return "%s @ %s" % (self.name, self.href)

def get_categories(driver):
	# Open categories menu
	categories_button = driver.find_element_by_class_name("dTOiRs")
	categories_button.click()

	# Get category elements
	category_picker = driver.find_element_by_class_name("fvdgvT")
	all_children_by_tag = category_picker.find_elements_by_tag_name("a")
	
	# Parse category elements
	all_categories = list()
	for child in all_children_by_tag:
		name = child.text
		href = child.get_property("href")
		
		all_categories.append(Category(name, href))

	return all_categories

def main():
	# Setup
	opts = Options()
	#opts.set_headless()
	driver = Chrome(executable_path='chromedriver', options=opts)  # Optional argument, if not specified will search path.
	driver.get(ROOT_URL)

	# Accept GDPR settings
	gdpr_button = driver.find_element_by_class_name("gENsPd")
	gdpr_button.click()

	all_categories = get_categories(driver)
	for cat in all_categories:
		print(cat)

if __name__ == '__main__':
	main()