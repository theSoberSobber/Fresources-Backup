from hashlib import sha256
import json, os
from logger import log

class HashUtil:
    def __init__(self, hash_file_path):
        self.hash_file_path = hash_file_path
        self.hash_resource_map = self.load_hash_file()

    def get_file_hash(self, file_path):
        # Compute SHA256 hash of the file
        hasher = sha256()
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def load_hash_file(self):
        try:
            with open(self.hash_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def contains(self, hash_value):
        return hash_value in self.hash_resource_map

    def get(self, hash_value):
        return self.hash_resource_map.get(hash_value, {})

    def add(self, hash_value, resource_dict):
        self.hash_resource_map[hash_value] = resource_dict
        self.commit()

    def commit(self):
        with open(self.hash_file_path, 'w') as file:
            json.dump(self.hash_resource_map, file)

if __name__ == "__main__":
    # Specify a temporary file path for testing
    test_file_path = 'test_hash_file.json'

    # Initialize HashUtil
    hash_util = HashUtil(test_file_path)

    cnt=0
    # Test contains, get, and add methods
    assert not hash_util.contains('hash123')
    log(0, f"Assertion {cnt}", "PASSED")
    cnt+=1
    assert hash_util.get('hash123') == {}
    log(0, f"Assertion {cnt}", "PASSED")
    cnt+=1
    
    resource_dict = {'name': 'Test Resource', 'type': 'Document', 'url': 'https://example.com'}
    hash_util.add('hash123', resource_dict)
    
    assert hash_util.contains('hash123')
    log(0, f"Assertion {cnt}", "PASSED")
    cnt+=1
    assert hash_util.get('hash123') == resource_dict
    log(0, f"Assertion {cnt}", "PASSED")
    cnt+=1

    # Commit changes to file
    hash_util.commit()

    # Initialize a new HashUtil instance to test loading from file
    new_hash_util = HashUtil(test_file_path)

    # Test if changes were committed and loaded successfully
    assert new_hash_util.contains('hash123')
    log(0, f"Assertion {cnt}", "PASSED")
    cnt+=1
    assert new_hash_util.get('hash123') == resource_dict
    log(0, f"Assertion {cnt}", "PASSED")
    cnt+=1

    # Clean up: Delete the temporary file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)