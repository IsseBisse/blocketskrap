import os
import json

DATA_ROOT = "data/"

# DEPRECATED: Each ad url contains a unique id so this isn't needed
# def calculate_checksum(content):
# 	# TODO: Check which parts of an ad can't be altered and calculate checksum based on these
# 	keys = ["heading", "time"]
# 	pass

def remove_duplicates(old_content, append_content):
	old_content_ids = [cont["id"] for cont in old_content]
	filtered_append_content = list()

	for cont in append_content:
		if cont["id"] not in old_content_ids:
			filtered_append_content.append(cont)

	return filtered_append_content

def append_page_contents_to_file(path, append_content):
	
	path = os.path.join(DATA_ROOT, path)

	if not os.path.exists(path) or os.path.getsize(path) == 0:
		with open(path, "w") as new_json_file:
			new_json_file.write("[]")

	with open(path, "r") as old_json_file:
		old_content = json.load(old_json_file)

	append_content = remove_duplicates(old_content, append_content)
	old_content += (append_content)

	with open(path, "w") as json_file:
		json.dump(old_content, json_file)	