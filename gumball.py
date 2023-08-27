import os, json, cloudscraper, time
from google.test import upload

scraper = cloudscraper.create_scraper()
cnt = 0

def checkNCreate(p):
    if(os.path.exists(p)==False):
        os.makedirs(p)

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

def downloadPdf(path, url):
    global cnt
    if(cnt==100):
        cnt = 0
        time.sleep(60)
    cnt += 1
    try:
        res = scraper.get(url)
    except:
        print("---------------------------")
        print(url)
        print("---------------------------")
    f = open(f'{path}', 'wb')
    f.write(res.content)

def sanitize(x):
    x = x.replace(":", "-").replace(" ", "-").replace("/", "-").replace('"', "-")
    return x

collegeIds = {
    "DTU": "63066b819cbab109372b8256",
    "NSUT": "63066b809cbab109372b824e",
    "IIITD": "63066b809cbab109372b824d",
    "IGDTUW": "63066b809cbab109372b824c"
}

cntFailure = 0

while(1):
    try:
        for i in collegeIds :
            print(i)
            checkNCreate(f"./data/{i}")
            resB = getBranchByCollegeId(collegeIds[i])
            f1 = open(f"./data/{i}/{i}.json","w")
            f1.write(json.dumps(resB, indent = 4))
            resB = resB[0]['result']['data']['json']
            for j in resB:
                print(f" {j['name']}")
                j['name']=sanitize(j['name'])
                checkNCreate(f"./data/{i}/{j['name']}")
                resC = getCourseByBranchId(j['id'])
                f2 = open(f"./data/{i}/{j['name']}/{j['name']}.json","w")
                f2.write(json.dumps(resC, indent = 4))
                resC  = resC[0]['result']['data']['json']['courses']
                for c in resC:
                    print(f"     {c['name']}")
                    c['name']=sanitize(c['name'])
                    name = f"./data/{i}/{j['name']}/{c['name']}"
                    checkNCreate(name)
                    resR = getResourceByCourseId(c['id'])
                    f3 = open(f"{name}/{c['name']}.json","w")
                    f3.write(json.dumps(resR, indent = 4))
                    resR = resR[0]['result']['data']['json']
                    for reso in resR:
                         reso = reso['resource']
                         rType = f"./data/{i}/{j['name']}/{c['name']}/{reso['type']}"
                         checkNCreate(rType)
                         reso['name'] = sanitize(reso['name'])
                         if(os.path.exists(f"{rType}/{reso['name']}")==False):
                             if("fresources" in reso['url']):
                                 print("         PDF: ", reso['name'])
                                 downloadPdf(f"{rType}/{reso['name']}", reso['url'])
                             else:
                                 print("         Playlist: ", reso['name'])
                                 f4 = open(f"{rType}/{reso['name']}", "w")
                                 f4.write(reso['url'])
        break
    except:
        cntFailure+=1
        print("Failure Count: ", cntFailure)
        time.sleep(60)
