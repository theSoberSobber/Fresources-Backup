import time, os, json, sys

# from hashUtil import get_file_hash
from data import collegeIds
from fresourcesUtil import FresourcesUtil
from uploader import CatboxUploader
from processor import DataProcessor
from hashUtil import HashUtil

file_path = "data-" + sys.argv[1] + ".json"
hash_file_path = "hashmap-" + sys.argv[1] + ".json"

# Example usage:
api_handler = FresourcesUtil()  # Replace with your actual instantiation code
upload_handler = CatboxUploader()
hash_util = HashUtil(hash_file_path)
data_processor = DataProcessor(api_handler, upload_handler, hash_util)

oneDict = {}
oneDict[sys.argv[1]] = collegeIds[sys.argv[1]];

data = data_processor.process_all_colleges(oneDict)

with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON data has been written to '{file_path}'")
print(f"JSOn hash data has been written to '{hash_file_path}'")