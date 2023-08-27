import requests

url = "https://fresources.tech/api/resource-views"

payload = "{\"fileId\":\"28fbf93fef5e778f657acda61430aa962fd76ba4f408fd4634bd231ea207a2a7dbe4f41e7b5334facdc379f0dfca9eb4e504fb0c8a2dab8dd342266d77caa873ef0adc09b2c7a9a462386ac5822237cea7bc9d28975bad0abe0051f0a7ee545647f7809c6940d7d061eb785327221aa8ec5399130789bc2a0c48e03eae518044f4f8f6be9926c5fc88268d4a09fb43dc890497873170b30393f009af45610082\"}"
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
