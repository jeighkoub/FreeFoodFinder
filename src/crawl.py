from distutils.log import error
import re
import shutil
import requests

from Mode import *; 
from urllib.parse import urlparse; 
import urllib

from bs4 import BeautifulSoup
import sys
import os 
import json

from preprocess import process_web_page_content

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    
url_expression = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def extract_domain(url:str)-> str:
    '''
    Takes a full url (ex: https://youtube.com/watch/Xv58673/) return a domain (ex: youtube.com)
    '''
    parsed_domain = urlparse(url)
    domain = parsed_domain.netloc or parsed_domain.path # Just in case, for urls without scheme
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        return '.'.join(domain_parts[-(2 if domain_parts[-1] in {
            'com', 'net', 'org', 'io', 'ly', 'me', 'sh', 'fm', 'us'} else 3):])
    return domain

def updateDisallowedUrls(domain: str, disallowedUrls: 'list[str]') -> None: 
        '''
        Access the robots.txt of a domain and append disallowed endpoints to the disallowedUrls list
        '''
        if (domain in disallowedUrls):
            return 
        try:
            disallowedUrls[domain] = []
            robotsPage = requests.get("https://" + domain + "/robots.txt", headers=headers)
            robotsTxt=robotsPage.text
            for line in robotsTxt.split("\n"):
                if line.startswith('Disallow'):
                    disallowed = line.split(':')[1]
                    if (disallowed.startswith(" ")):
                        disallowed = disallowed[1:]
                    disallowed = disallowed.split(' ')[0]
                    disallowedUrls[domain].append("https://" + domain + disallowed)
        except Exception as e: 
            print("Robots Txt Failed for " + domain + ": " + str(e))

def url_meets_prerequisites(url: str, ignoredDomains: 'list[str]',ignoredEndpoints: 'list[str]', disallowedUrls: 'dict[str,str]') -> bool:

    #check url string matches a url expression
    if (re.match(url_expression, url)):
        extracted_domain = extract_domain(url)
        if (extracted_domain not in ignoredDomains):
            updateDisallowedUrls(domain=extracted_domain, disallowedUrls=disallowedUrls)
            if (url not in disallowedUrls):
                if not any(ele in url for ele in ignoredEndpoints):
                    extension = url.split(".")[-1].lower()    
                    if (extension != "mp3" and extension != "mp4"):
                        return True

    return False


def writeBack(crawled: 'dict[str]', startRange: int, outputFile: str):
    dirname = os.getcwd()
    saveDirectory = dirname + "/../crawlData/"+ outputFile + "/"
                               
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
                              
    with open(saveDirectory+ "crawledUrls"+"_"+str(startRange) + ".json", "a") as f: 
        json_dict = json.dumps(crawled)
        f.write(json_dict)
    f.close()
    crawled.clear()

def writeBackImages(imgs: 'list[str]', outputFile: str):
    dirname = os.getcwd()
    saveDirectory = dirname + "/../crawlData/"+ outputFile + "/ImageData/"                           
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
                              
    with open(saveDirectory+ "crawledImgUrls"+".txt", "a") as f:
        for imgUrl in imgs:
            f.write(imgUrl + "\n")
    f.close() 
    imgs.clear() 
    
# Like in lecture
def linkCanonicalization(url):
  # ending directory normalize
  if(len(url) > 1 and url[-1] == '/'):
    url = url[:-1]
  # Internal page fragments
  url = url.split('#')[0]
  return url

def crawl(queue: 'list[str]', mode: Mode, stop: bool, ignoredDomains: 'list[str]', ignoredEndpoints: 'list[str]', disallowedUrls: 'dict[str,str]', outputFile: str) -> None:
    crawled = {}
    visited = {}
    imgs = []
    seenImgs = []
    count = 0
    new = 0
    while not stop: 
        if (len(queue) > 0):
            if mode == Mode.BFS: 
                url = queue.pop(0)
            elif mode == Mode.DFS:
                url = queue.pop()
            else: 
                url = None
                error("Unrecognized Mode")
                return 1
            # I(Adel) added this. You can check. From here
            url = linkCanonicalization(url)
            #checcking https and http and duplicates
            http = url.split('//')
            if(len(http) > 1):
                if (url.split('//')[1] in visited):
                    continue
                visited[url.split('//')[1]] = True
            else:
                visited[url.split('//')[0]] = True
            # To here
            print(url)
            try: 
                web_page = requests.get(url,headers=headers, timeout=5)
                if (web_page.status_code == 200):
                    processed_content = BeautifulSoup(web_page.content,"html.parser")
                    for link in processed_content.find_all(["a","img"]):  
                        if link.name == "a":
                            extracted_link = link.get("href")
                            if (extracted_link != None):
                                if (extracted_link.startswith('/')):
                                    extracted_link = urllib.parse.urljoin(url,extracted_link)
                                if ('http' in extracted_link):
                                    if url_meets_prerequisites(extracted_link, ignoredDomains=ignoredDomains,ignoredEndpoints=ignoredEndpoints, disallowedUrls=disallowedUrls) and extracted_link not in crawled and extracted_link not in queue:
                                        queue.append(extracted_link) 
                        elif link.name == "img":
                            imgLink = link.get("src")
                            if imgLink != None:
                                if (imgLink.startswith('/')):
                                    imgLink = urllib.parse.urljoin(url,imgLink)
                                extension = imgLink.split(".")[-1].lower()    
                                if ('http' in imgLink and (extension == "jpeg" or extension == "jpg" or extension == "png")):
                                    if url_meets_prerequisites(imgLink, ignoredDomains=ignoredDomains,ignoredEndpoints=ignoredEndpoints, disallowedUrls=disallowedUrls) and imgLink not in seenImgs:
                                        imgs.append(imgLink)  
                                        seenImgs.append(imgLink)
                    tokens = process_web_page_content(processed_content)
                    crawled[url] = tokens
            except Exception as e: 
                print(str(e))
        if (len(crawled) > 100):
            new = new + len(crawled)
            print("Writing back urls: " + str(count) + "-" + str(new))
            count = new
            writeBack(crawled, new, outputFile)
        if (len(imgs) > 100):
            writeBackImages(imgs, outputFile=outputFile)
        if (len(crawled) % 10 == 0 and len(crawled) > 0):
            print("urls Crawled: " + str(len(crawled)))
        if (len(imgs) % 10 == 0 and len(imgs) > 0):
            print("imgaes Crawled: " + str(len(imgs)))
            

def main():

    if (len(sys.argv) != 6):
        print("Usage: python3 crawl.py seedFile ignoredDomains ignoredEndpoints Mode[bfs,dfs] outputFile")
        exit(1)
    if (sys.argv[4].lower() == "bfs"):
        mode = Mode.BFS
    elif sys.argv[4].lower() == "dfs":
        mode = Mode.DFS
    else: 
        mode = None 
    
    seedFile = sys.argv[1]
    ignoreDomainsFile = sys.argv[2]
    ignoreEndpointsFile = sys.argv[3]

    outputFile = sys.argv[5]

    with open(seedFile) as f: 
        queue = [line.strip() for line in f]
        if (mode == Mode.DFS): 
            queue.reverse()
    f.close()
    with open(ignoreDomainsFile) as a: 
        ignoredDomains = [line.strip() for line in a]
    a.close()
    with open(ignoreEndpointsFile) as e: 
        ignoredEndpoints = [line.strip() for line in e]
    e.close()

    print("Seeding crawler with: " + str(queue))
    print("Ignoring Domains: " + str(ignoredDomains))
    print("Ignoring Endpoints: " + str(ignoredEndpoints))

    crawl(queue=queue, mode=mode, stop=False, ignoredDomains=ignoredDomains,ignoredEndpoints=ignoredEndpoints, disallowedUrls={}, outputFile=outputFile)
    
    return 0 




if __name__=="__main__":
    exit (main())