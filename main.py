import PageGetter
from PageStructureHandler import PageStructureHandler
import DataBaseHandler

WATCH_ITEMS = [
	# {"url": "https://www.blocket.se/annonser/hela_sverige/elektronik/ljud_bild/foto_videokameror?cg=5042&q=fuji%2A",
	# "json_path": "fuji__hela_sverige__foto_videokameror.json",
	# "descriptor": PageGetter.BASIC_ITEM_DESCRIPTORS},
	{"url": "https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cg=1020&mys=2008&q=v70",
	"json_path": "v70__hela_sverige__post2008.json",
	"descriptor": PageGetter.CAR_DESCRIPTORS}
	
	]

def main():
	structure_handler = PageStructureHandler()

	for item in WATCH_ITEMS:
		ad_links = structure_handler.get_all_ads(item["url"])
		
		num_links = len(ad_links)
		div = 10 if num_links < 500 else 100
		print("Getting %d ad contents..." % num_links)
		print("Ads completed: ")

		all_ad_contents = list()
		for i, link in enumerate(ad_links):
			contents = PageGetter.get_page_contents(link, item["descriptor"])
			all_ad_contents.append(contents)
		
			if i % div == 0:
				print("%d " % i, end="")

		print("Appending to database file... ", end="")
		DataBaseHandler.append_page_contents_to_file(item["json_path"], all_ad_contents)
		print("Done!")

	del structure_handler

if __name__ == '__main__':
	main()