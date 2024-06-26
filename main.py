import time, os, json

# from hashUtil import get_file_hash
from data import collegeIds, file_path, hash_file_path
from fresourcesUtil import FresourcesUtil
from uploader import CatboxUploader
from processor import DataProcessor
from hashUtil import HashUtil

# Example usage:
api_handler = FresourcesUtil()  # Replace with your actual instantiation code
upload_handler = CatboxUploader()
hash_util = HashUtil(hash_file_path)
data_processor = DataProcessor(api_handler, upload_handler, hash_util)
data = data_processor.process_all_colleges(collegeIds)
# hash_util.commit()

with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print(f"JSON data has been written to '{file_path}'")
