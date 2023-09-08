import argparse
from distutils import extension
import shutil
import requests
import json 
from preprocess import * 

import easyocr
from PIL import Image
import requests
from io import BytesIO

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}



def recognize_text(img_path):
    '''loads an image and recognizes text.'''
    
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path)

def overlay_ocr_text(img_path):
    '''loads an image, recognizes text, and overlays the text on the image.'''
    
    # recognize text
    result = recognize_text(img_path)
    # if OCR prob is over 0.5, overlay bounding box and text
    words = ""
    for (bbox, text, prob) in result:
        if prob >= 0.5:
            # display 
            words += text.lower() + " "
    return words

# Input Image URL
# output dictionary of words
def text_recognition(image_url):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
    response = requests.get(image_url, headers=headers, timeout=15)
    img = Image.open(BytesIO(response.content))
    img = img.convert('RGB')
    img.save("1.jpg")
    
    words = overlay_ocr_text("1.jpg")
    return words

def getImageData(imageUrls: 'list[str]'):

    imageDataDict = {}

    for imageUrl in imageUrls:
        res = requests.get(url=imageUrl, stream = True, timeout=3)
        if res.status_code == 200: 
            extension = imageUrl.split(".")[-1].lower()
            if (extension == "jpg"):
                res = requests.get(url=imageUrl, stream = True, timeout=3)
                if res.status_code == 200: 
                    tempfile = "temp." + extension
                    with open(tempfile, 'wb') as f: 
                        shutil.copyfileobj(res.raw, f) 
                    print("Downloaded: " + imageUrl)
                    try: 
                        tokens = overlay_ocr_text(tempfile)
                        tokens = process_web_page_content(tokens)
                        imageDataDict[imageUrl] = tokens
                        print(tokens)
                    except Exception as e: 
                        print(str(e))

    return imageDataDict

def main():
    parser = argparse.ArgumentParser(description="Given a list of image urls, download the image, run it through OCR and tokenize the data", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("imageUrlFile", help="File containing urls of images")
    parser.add_argument("outputFile", help="File to write json object containing {\"url\": [tokenList]} pairs")
    args = vars(parser.parse_args())

    imageUrls = []
    with open(args["imageUrlFile"]) as f: 
        for line in f.readlines():
            imageUrls.append(line.strip("\n"))
    f.close()
    imageDataDict = getImageData(imageUrls)
    
    with open(args["outputFile"] + ".json") as a: 
        json_dict = json.dumps(imageDataDict)
        a.write(json_dict)
    a.close()
   
    return 0

if __name__=="__main__":
    exit(main())


