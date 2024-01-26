import os
import json
import cloudscraper
import time
import tempfile
import signal
from catbox import Uploader
from hashlib import sha256

# Initialize Catbox uploader
uploader = Uploader(token='')

scraper = cloudscraper.create_scraper()
cnt = 0
readme = ""
data = {}

def get_file_hash(file_path):
    # Compute SHA256 hash of the file
    hasher = sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def getBranchByCollegeId(collegeId):
    global cnt
    if(cnt==50):
        cnt = 0
        time.sleep(60)
    cnt += 1
    url = 'https://fresources.tech/api/trpc/example.getBranchNamesByCollegeId?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22collegeId%22%3A%22'
    url += collegeId
    url += '%22%7D%7D%7D'
    try:
        response = scraper.get(url)
    except:
        print("---------------------------")
        print(url)
        print("---------------------------")
        raise Exception("Maza nahi aaya 0")
    res = response.text
    res = json.loads(res)
    return res

def getCourseByBranchId(branchId):
    global cnt
    if(cnt==20):
        cnt = 0
        time.sleep(60)
    cnt += 1
    url = 'https://fresources.tech/api/trpc/example.getCourseByBranchId?batch=1&input={%220%22:{%22json%22:{%22branchId%22:%22'
    url += branchId
    url += '%22}}}'
    try:
        response = scraper.get(url)
    except:
        print("---------------------------")
        print(url)
        print("---------------------------")
    res = response.text
    res = json.loads(res)
    return res

def getResourceByCourseId(courseId):
    global cnt
    if(cnt==20):
        cnt = 0
        time.sleep(60)
    cnt += 1
    url = 'https://fresources.tech/api/trpc/example.getResourcesByCourseId?batch=1&input={%220%22:{%22json%22:{%22courseId%22:%22'
    url += courseId
    url += '%22}}}'
    try:
        response = scraper.get(url)
    except:
        print("---------------------------")
        print(url)
        print("---------------------------")
    res = response.text
    res = json.loads(res)
    return res

def download_and_upload(url, data_dir, filename):
    try:
        response = scraper.get(url)
        content = response.content

        # Create a temporary file in the specified directory
        temp_file_path = os.path.join(data_dir, filename)
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(content)

        # Check if the file is already uploaded
        file_hash = get_file_hash(temp_file_path)
        if filename not in files_info:
            # If the file is not uploaded, upload it
            upload = uploader.upload(file_type='pdf', file_raw=content)
            files_info[filename] = {'hash': file_hash, 'link': upload['file']}
            print(f"Uploaded file to Catbox: {upload['file']}")
        else:
            # If the file is already uploaded, use the existing link
            if files_info[filename]['hash'] != file_hash:
                # If the hash is different, upload a new version of the file
                upload = uploader.upload(file_type='pdf', file_raw=content)
                files_info[filename] = {'hash': file_hash, 'link': upload['file']}
                print(f"Uploaded new version of file to Catbox: {upload['file']}")
            else:
                # If the hash is the same, use the existing link
                print(f"File already uploaded. Using existing link: {files_info[filename]['link']}")

        # Remove the temporary file
        os.remove(temp_file_path)

        return files_info[filename]['link']
    except Exception as e:
        print(f"Failed to download or upload file: {e}")
        return None

def sanitize(x):
    return x.replace(":", "-").replace(" ", "-").replace("/", "-").replace('"', "-")

collegeIds = {
    "DTU": "63066b819cbab109372b8256",
    "NSUT": "63066b809cbab109372b824e",
    "IIITD": "63066b809cbab109372b824d",
    "IGDTUW": "63066b809cbab109372b824c"
}

cnt_failure = 0
files_info = {}

def cleanup_and_exit(signum, frame):
    global cnt_failure
    print(f"Cleaning up due to interrupt signal (SIGINT)")
    
    # Save files_info to a JSON file
    with open("files_info.json", "w") as files_info_file:
        json.dump(files_info, files_info_file, indent=4)
    print("Saved files_info data to: files_info.json")

    # Update README file
    readme_path = "./README.md"
    with open(readme_path, "w") as readme_f:
        readme_f.write(readme)
    print(f"Updated README file: {readme_path}")

    cnt_failure += 1
    print(f"Failure Count: {cnt_failure}")
    exit(0)

# Register the cleanup_and_exit function to handle SIGINT
signal.signal(signal.SIGINT, cleanup_and_exit)

while True:
    try:
        data_dir = "./data"
        os.makedirs(data_dir, exist_ok=True)
        print(f"Processing started at: {time.ctime()}")
        for i in collegeIds:
            college_data = {}
            print(f"Processing college: {i}")
            res_b = getBranchByCollegeId(collegeIds[i])
            res_b_path = f"{data_dir}/{i}_branches.json"
            with open(res_b_path, "w") as f1:
                json.dump(res_b, f1, indent=4)
            print(f"Saved branches data to: {res_b_path}")

            res_b = res_b[0]['result']['data']['json']
            for j in res_b:
                branch_data = {}
                j_name = sanitize(j['name'])
                print(f" Processing branch: {j_name}")
                res_c = getCourseByBranchId(j['id'])
                res_c_path = f"{data_dir}/{i}_{j_name}_courses.json"
                with open(res_c_path, "w") as f2:
                    json.dump(res_c, f2, indent=4)
                print(f"Saved courses data to: {res_c_path}")

                res_c = res_c[0]['result']['data']['json']['courses']
                for c in res_c:
                    course_data = {}
                    c_name = sanitize(c['name'])
                    print(f"     Processing course: {c_name}")
                    res_r = getResourceByCourseId(c['id'])
                    res_r_path = f"{data_dir}/{i}_{j_name}_{c_name}_resources.json"
                    with open(res_r_path, "w") as f3:
                        json.dump(res_r, f3, indent=4)
                    print(f"Saved resources data to: {res_r_path}")

                    res_r = res_r[0]['result']['data']['json']
                    resources = []
                    for reso in res_r:
                        reso = reso['resource']
                        resource_data = {}
                        r_type = f"{data_dir}/{i}_{j_name}_{c_name}_{reso['type']}"
                        r_name = sanitize(reso['name'])
                        print(f"    Processing resource - Type: {reso['type']}, Name: {r_name}")
                        file_link = download_and_upload(reso['url'], data_dir, r_name)
                        if file_link:
                            resources.append({'name': r_name, 'link': file_link})
                            readme += f"\t\t- [{r_name}]({file_link})\n"

                    course_data[c_name] = resources
                    branch_data[j_name] = course_data
                college_data[i] = branch_data
            data[i] = college_data

        print(f"Processing completed at: {time.ctime()}")
        print(f"Cleaning up data directory: {data_dir}")
        # Clean up the data directory
        for file in os.listdir(data_dir):
            file_path = os.path.join(data_dir, file)
            os.remove(file_path)
        os.rmdir(data_dir)

        # Save files_info to a JSON file
        with open("files_info.json", "w") as files_info_file:
            json.dump(files_info, files_info_file, indent=4)
        print("Saved files_info data to: files_info.json")

        # Update README file
        readme_path = "./README.md"
        with open(readme_path, "w") as readme_f:
            readme_f.write(readme)
        print(f"Updated README file: {readme_path}")

        # Save data to a JSON file
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
        print("Saved data to: data.json")

        break
    except Exception as err:
        print(f"Error during execution: {err}")
        cnt_failure += 1
        print(f"Failure Count: {cnt_failure}")
        time.sleep(60)
