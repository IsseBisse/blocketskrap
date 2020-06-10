import PageGetter
from PageStructureHandler import PageStructureHandler

WATCH_ITEMS = [
	{"url": "https://www.blocket.se/annonser/hela_sverige/elektronik/ljud_bild/foto_videokameror?cg=5042&q=fuji%2A",
	"json_path": "fuji__hela_sverige__foto_videokameror.json"},
	# {"url": "https://www.blocket.se/annonser/stockholm/elektronik/ljud_bild/foto_videokameror?cg=5042&q=fuji%2A&r=11",
	# "json_path": "fuji__stockholm__foto_videokameror.json"}
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
			contents = PageGetter.get_page_contents(link)
			all_ad_contents.append(contents)
		
			if i % div == 0:
				print("%d " % i, end="")

		print("Appending to database file... ", end="")
		PageGetter.append_page_contents_to_file(item["json_path"], all_ad_contents)
		print("Done!")

	del structure_handler

if __name__ == '__main__':
	main()