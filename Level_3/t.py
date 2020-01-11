#!/usr/bin/python3
import pytesseract
import os
import argparse
try:
    import Image, ImageOps, ImageEnhance, imread, ImageFilter
except ImportError:
    from PIL import Image, ImageOps, ImageEnhance, ImageFilter

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
    image = Image.open(path).convert('RGB')
    image = ImageOps.autocontrast(image)

    filename = "{}.png".format(os.getpid())
    image.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    return text

def solve_captcha_1(path):

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
    image = Image.open(path)  
    out = image.filter(ImageFilter.BLUR)
    out = out.convert('RGB')

    # out = out.point(lambda x: 0 if x<136 else 255, "1")

    # width, height = out.size
    # out = out.resize((width*5, height*5), Image.NEAREST)

    out.save("captcha_modified.png")

    text = pytesseract.image_to_string(Image.open("captcha_modified.png"))
    return text


def solve_captcha_2(path):

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

    filename = "{}.png".format(os.getpid())
    img.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    return text


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
    args = vars(argparser.parse_args())
    path = args["image"]
    print('-- Resolving')
    captcha_text = solve_captcha_2(path)
    print('-- Result: {}'.format(captcha_text))