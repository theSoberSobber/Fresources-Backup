from hashlib import sha256

def get_file_hash(file_path):
    # Compute SHA256 hash of the file
    hasher = sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()