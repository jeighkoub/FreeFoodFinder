
from enum import Enum
import argparse
from genericpath import isfile
import json
import os
from preprocess import *
import math

def determineRelevancyBoolean(content_dict: dict, imageDir = None) -> 'list[str]':
    relevantUrls = [] 

    for url, content in content_dict.items(): 

        #if ("free" in content and ("food" in content or "breakfast" in content or "dinner" in content or "bagels" in content) ):
        if is_umich_file_relevent(url, content):
            relevantUrls.append(url)
    return relevantUrls

# check for umich specific keywords & suchs
def is_umich_file_relevent(url, link_content):
    """a page will be marked as “relevant” if the following information can be found: 
    Source URL,  Date and Time, Keywords such as “Event”, “Food”,  and “Free”, 
    A location within some distance to the query or entered location, Host Organization
    """

    #key words to look 
    # "beverag"
    food_words = ["food", "breakfast", "snacks", "lunch", "dinner", "groceries", "bagel", "coffee", "donut", "treat", "buffet", "cream"]
    keys = [["free", "event"], ["umix"], ["rackham"], ["event"]]

    bad_words = ["exhibition"]
    bad_links = ["day", "month", "week", "list", "map", "group", "json", "csv", "rss", "ical", "umma", "event-tags", "event-archive", "programs"]
    
    
    for combo in keys:
        # if word from key + any word from food_words
        if all(ele in link_content for ele in combo): 
            if any(ele in link_content for ele in food_words) and not any(ele in link_content for ele in bad_words): 
                # print(combo)
                if "event" in url and not any(ele in url for ele in bad_links):
                    return True

    return False

def determineRelevancyBayes(model: json, content_dict: json, combined : bool, imageDir = None) -> 'list[str]':
    
    eventClassProbability = model["eventClassProbability"]
    nonEventClassProbability = model["nonEventClassProbability"]

    pWordGivenEvent = model["pWordGivenEvent"]
    pWordGivenNonEvent = model["pWordGivenNonEvent"]

    vocab = model["vocab"]

    numEventWords = model["numEventWords"]
    numNonEventWords = model["numNonEventWords"]

    # TODO take the log of these?
    probEvent = math.log10(eventClassProbability)
    probNotEvent = math.log10(nonEventClassProbability)

    print(eventClassProbability)
    print(nonEventClassProbability)

    relevantUrls = []
    vocab_size = len(vocab)

    #take a url and its content, run it through the model 
    for url, content in content_dict.items(): 
        for token in content: 
            if token in pWordGivenEvent: 
                probEvent += math.log10(pWordGivenEvent[token])
            else:
                probEvent += math.log10(1 / ((numEventWords + vocab_size)))
            
            if token in pWordGivenNonEvent: 
                probNotEvent += math.log10(pWordGivenNonEvent[token])
            else: 
                probNotEvent += math.log10(1/ ((numNonEventWords + vocab_size)))
        
        if (probEvent > probNotEvent):
            # The if statement below causes determine relevancy to both run naiveBayes and check for keywords if the "combined" flag is set
            if combined and is_umich_file_relevent(url, content):
                relevantUrls.append(url)
            else: 
                relevantUrls.append(url)
    
    return relevantUrls

def main(): 
    parser = argparse.ArgumentParser(description="Given a list of urls and page content, determine relevant urls", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("urlDirectory", help="Directory containing JSON files of urls to be analyzed")
    parser.add_argument("-n", "--naive-bayes", help="Tells the program to use the Naive Bayes model provided as a JSON file to classify URLS")
    parser.add_argument("-b", "--boolean", action="store_true", help = "use simple keyword detection to classify urls")
    parser.add_argument("-c", "--combined",  help="check for the presence of keywords on top of naiveBayes classification, takes path to json model file")
    parser.add_argument("-i", "--image", type=str, help="Check url for associated images in directory provided")
    args = vars(parser.parse_args())
    urlDirectory= args["urlDirectory"]

    imageDir = args["image"]      

    content_dict = {}

    for fileName in os.listdir(urlDirectory):
        if (os.path.isfile(urlDirectory + "/" + fileName)):
            with open( urlDirectory + fileName) as f: 
                jsonData = json.loads(f.read())
                for key,value in jsonData.items(): 
                    content_dict[key] = value
            f.close()

    with open("ALL_URLS.txt", "w") as a:
        for key, value in content_dict.items():
            a.write(key + "\n")
    a.close()
    print(args)
    if args["boolean"] == True:
        fileExt = "boolean" 
        relevant_urls = determineRelevancyBoolean(content_dict=content_dict, imageDir=imageDir)

    elif not args["naive_bayes"] == None or not args["combined"] == None: 
        if not args["naive_bayes"] == None:
            with open(args["naive_bayes"]) as a:
                model = json.load(a)  
            fileExt = "naive_bayes" 
            relevant_urls = determineRelevancyBayes(model=model, content_dict=content_dict, imageDir=imageDir, combined=False)
            a.close()
        else:
            with open(args["combined"]) as a:
                model = json.load(a)  
            fileExt = "combined"
            relevant_urls = determineRelevancyBayes(model=model, content_dict=content_dict, imageDir=imageDir, combined=True)      
            a.close()   
    else:
        print("Mode not Set")
        exit(1)

    saveFile = "../RelevancyData/RelevantUrls." + fileExt 

    if not os.path.exists("../RelevancyData/"):
        os.makedirs("../RelevancyData/")
    with open(saveFile , "w") as a: 
        for line in relevant_urls: 
            a.write(line + "\n")
    a.close()

    return 0 

if __name__=="__main__":
    exit (main())