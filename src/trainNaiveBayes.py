
import argparse
import requests
from preprocess import * 
from bs4 import BeautifulSoup
from collections import defaultdict
import json 
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}


def trainBayes(eventFile: str, nonEventFile: str) -> dict: 


    with open(eventFile) as f: 
        eventUrls = f.readlines()
    with open(nonEventFile) as a:
        nonEventUrls = a.readlines()
    f.close()
    a.close()

    event_vocab = defaultdict(lambda: 0)
    nonEvent_vocab = defaultdict(lambda: 0)
    vocab = defaultdict(lambda: 0)

    numEventDocs = 0
    numNonEventDocs = 0

    for url in eventUrls:
        try:
            page = requests.get(url, headers=headers)
            page_content = BeautifulSoup(page.content, "html.parser")
            tokens = process_web_page_content(page_content)
            for token in tokens: 
                event_vocab[token] += 1
                vocab[token] += 1
            numEventDocs += 1
        except Exception as e:
            print(str(e))    

    for url in nonEventUrls:
        try:
            page = requests.get(url, headers=headers)
            page_content = BeautifulSoup(page.content, "html.parser")
            tokens = process_web_page_content(page_content)
            for token in tokens: 
                nonEvent_vocab[token] += 1
                vocab[token] += 1
            numNonEventDocs += 1
        except Exception as e:
            print(str(e))    

    eventWordsSize = sum(event_vocab.values())
    nonEventWordsSize = sum(nonEvent_vocab.values())

    pWordGivenEvent = {}
    pWordGivenNonEvent = {}

    for word, freq in event_vocab.items(): 
        pWordGivenEvent[word] = (freq + 1) / (eventWordsSize + len(vocab))
    for word, freq in nonEvent_vocab.items():
        pWordGivenNonEvent[word] = (freq + 1) / (nonEventWordsSize + len(vocab))


    eventClassProbability = numEventDocs / (numEventDocs + numNonEventDocs)
    nonEventClassProbability = numNonEventDocs / (numEventDocs + numNonEventDocs)

    print("Top 10 words for Free Food Events")
    count = 0
    sort =  dict(sorted(pWordGivenEvent.items(), key=lambda item: item[1], reverse=True))
    for k,v in sort.items(): 
        print(k," ", v)
        count+= 1
        if (count==10):
            break
    print("-------------------------------------------------")
    print("Top 10 words for Non Events")
    count = 0
    sort =  dict(sorted(pWordGivenNonEvent.items(), key=lambda item: item[1], reverse=True))
    for k,v in sort.items(): 
        print(k," ", v)
        count += 1
        if (count==10):
            break

    returnVals = {"numEventWords": eventWordsSize, "numNonEventWords": nonEventWordsSize, "eventClassProbability": eventClassProbability, "nonEventClassProbability": nonEventClassProbability, "pWordGivenEvent": pWordGivenEvent, "pWordGivenNonEvent": pWordGivenNonEvent, "vocab": vocab}

    return returnVals

def main():
    parser = argparse.ArgumentParser(description="Given a list of known event urls and a list of known non-event urls, train a naive bayes classifer", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("eventFile", help="File containing urls of known event listings")
    parser.add_argument("nonEventFile", help="File containing urls of known non event listings")
    parser.add_argument("output", help = "name of file to output data to - NO EXTENSION")
    args = vars(parser.parse_args())


    eventFile= args["eventFile"]
    nonEventFile = args["nonEventFile"]
    outputFile = args["output"]


    output = trainBayes(eventFile, nonEventFile)

    if not os.path.exists("../NaiveBayesTrainingData/"):
        os.makedirs("../NaiveBayesTrainingData/")
  
    with open(outputFile + ".json","w") as f: 
        json.dump(output,f, ensure_ascii=False)
    f.close()

    return 0


if __name__=="__main__":
    exit(main())