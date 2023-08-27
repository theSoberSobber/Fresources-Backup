import hashlib
import json
import magic
mime = magic.Magic(mime=True)

from Google import Create_Service
from googleapiclient.http import MediaFileUpload

API_NAME='drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

overhead = 512
TOP=1

service = Create_Service(f"secrexx-{TOP}.json", API_NAME, API_VERSION, SCOPES)

# need to call before every function (use decorators???)
def ensureSpace():
	global TOP
	while(getRemainingSpace()<=overhead):
		TOP+=1
		service = Create_Service(f"secrexx-{TOP}.json", API_NAME, API_VERSION, SCOPES)
	print(TOP)

def pprint(js):
	print(json.dumps(js, indent=4))

def hashfile(file):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f: 
        while True:
            data = f.read(BUF_SIZE)
            if not data:
            	break
            sha256.update(data)
    return sha256.hexdigest()

def createFolder(name, parent="root"):
	file_metadata = {
		'name': name,
		'mimeType': 'application/vnd.google-apps.folder',
		'parents': [parent]
	}
	service.files().create(body=file_metadata).execute()

def listAll():
	tree = {}
	listAppend('root', tree)
	return tree;

def listAppend(id, curr_node):
	curr = list(id)
	for i in curr['files']:
		uid = f"{i['name']};{i['id']}"
		if(i['mimeType'].split(".")[-1]=="folder"):
			curr_node[uid] = {}
			listAppend(i['id'], curr_node[uid])
		else:
			curr_node[uid] = "file"

def list(id):
	return service.files().list(q=f"'{id}' in parents").execute()

def uploadFile(name, path, parent):
	ext = name.split(".")[-1]
	file_metadata = {
		# hash is just to check integrity of file
		'name': f"{name};{hashfile(path)};.{ext}",
		'parents': [parent]
	}
	media = MediaFileUpload(path, mimetype=mime.from_file(path))
	file = service.files().create(
		body = file_metadata,
		media_body = media
	).execute()

def upload(name, path, parent):
	if(check(name, path, parent)==0):
		uploadFile(name, path, parent)

def getFolderId(name, parent):
	curr = list(parent)
	for i in curr['files']:
		if(i['mimeType'].split(".")[-1]=="folder" and i['name']==name):
			return i['id'];
	return -1;

def getResourceId(name, parent):
	curr = list(parent)
	for i in curr['files']:
		if(i['mimeType'].split(".")[-1]!="folder" and i['name'].split(";")[0]==name):
			return i['id'];
	return -1;

def replaceFile(file_id, path):
	media = MediaFileUpload(path, mimetype=mime.from_file(path))
	file = service.files().update(
		fileId = file_id,
		media_body = media
	).execute()

def getRemainingSpace():
	# returns in megabytes
	res = service.about().get(fields='*').execute()
	rem = int(res['storageQuota']['limit']) - int(res['storageQuota']['usage'])
	# print(f"MB: {rem/1024**2}\nGB: {rem/1024**3}\n")
	return rem/1024**2;

def changePerms(resId):
	request_body = {
		'role': 'reader',
		'type': 'anyone'
	}
	res = service.permissions().create(
		fileId = resId,
		body=request_body
	).execute()

def getResourceLink(resId):
	changePerms(resId)
	obj = service.files().get(
		fileId = resId,
		fields='webViewLink'
	).execute()
	return obj['webViewLink']

def check(name, path, parent):
	# checks a files existence and integrity
	# list and check for corresponding lock file and name for hash
	curr = list(parent)
	for i in curr['files']:
		if(i['mimeType'].split(".")[-1]!="folder" and i['name'].split(';')[1]==hashfile(path)):
			return True;
	return False;

def checkFolder(name, parent):
	curr = list(parent)
	for i in curr['files']:
		if(i['mimeType'].split(".")[-1]=="folder" and i['name']==name):
				return True;
	return False;

def checkNCreateDrive(name, parent):
	if(checkFolder(name, parent)==0):
		createFolder(name, parent)
# naming convention "name;resourceId;.extension"

# if(check("bhau.pdf", "../test.pdf", 'root')==0):
	# upload("bhau.pdf", "../test.pdf", 'root')

# upload("DTU.json;hidajsdakndasd;.json", "./data/DTU/DTU.json", 'root')

# replace(fileId, "../test.pdf")
# print(getResourceLink(resId));

# pprint(listAll())
# print(getRemainingSpace()) # print in mb
# ensureSpace();
# print(hashfile("./test.pdf"))