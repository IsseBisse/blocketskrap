import unittest
import sys
import shutil
import json
import os

sys.path.insert(1, "../")
import DataBaseHandler


class TestDatabase(unittest.TestCase):

	OLD_CONTENT_PATH = "append_content_test_old.json"
	NEW_CONTENT_PATH = "append_content_test_new.json"
	OUTPUT_CONTENT_PATH = "append_content_test_merge.json"

	def tearDown(self):
		os.remove(self.OUTPUT_CONTENT_PATH)

	def test_append(self):
		
		# Setup
		shutil.copyfile(self.OLD_CONTENT_PATH, self.OUTPUT_CONTENT_PATH)
		with open(self.NEW_CONTENT_PATH, "r") as json_file:
			new_content = json.load(json_file)
		
		with open(self.OLD_CONTENT_PATH, "r") as json_file:
			old_content = json.load(json_file)

		new_ids = [cont["id"] for cont in new_content]
		old_ids = [cont["id"] for cont in old_content]
		true_ids = sorted(list(set(new_ids + old_ids)))
		num_unique_ids = len(true_ids)

		DataBaseHandler.append_page_contents_to_file(self.OUTPUT_CONTENT_PATH, new_content)

		# Data check
		with open(self.OUTPUT_CONTENT_PATH, "r") as json_file:
			output_content = json.load(json_file)
		output_ids = [cont["id"] for cont in output_content]
		
		# Print compare data
		for i, id_ in enumerate(output_ids):
			true_ind = "/" if id_ not in true_ids else true_ids.index(id_)
			old_ind = "/" if id_ not in old_ids else old_ids.index(id_)
			new_ind = "/" if id_ not in new_ids else new_ids.index(id_)

			print("%d: %s - true: %s - new: %s - old: %s" % (i, id_, true_ind, new_ind, old_ind))

		# Check length
		self.assertEqual(len(output_content), num_unique_ids)

if __name__ == '__main__':
	unittest.main()