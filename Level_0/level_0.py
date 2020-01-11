import requests

URL = "http://158.69.76.135/level0.php"

payload = {"id": "1091", "holdthedoor": "Submit+Query"}

for i in range(1024):
    response = requests.post(URL, data=payload)
    if response.status_code == 200:
        print("{:d} The request has succeeded.".format(i))
    else:
        print("{:d} The request has fail.".format(i))
        break
