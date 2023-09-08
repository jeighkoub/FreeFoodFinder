import sys 
import os
import re
from collections import defaultdict

from bs4 import BeautifulSoup 
from stemmer import PorterStemmer
stopwords = ["on", "by", "we","a","all","an","and","any","are","as","at","be","been","but","by ","few","from","for","have","he","her","here","him","his","how","i","in","is","it","its","many","me","my","none","of","on ","or","our","she","some","the","their","them","there","they","that","this","to","us","was","what","when","where","which","who","why","will","with","you","your", "s"]

webStopwords = ["contact", "share"]

punctuation = [".",",","\'","\"","?","!"]

commonContractions = {
        "ain't": "am not",
        "aren't": "are not",
        "can't": "can not",
        "could've": "could have",
        "couldn't": "could not",
        "didn't": "did not", 
        "don't": "do not",
        "doesn't": "does not",
        "hadn't": "had not", 
        "hasn't": "has not", 
        "haven't": "have not", 
        "he'd": "he would",
        "here's": "here is",
        "how'd": "how did", 
        "how'll": "how will", 
        "how're": "how are",
        "i'd": "I would", 
        "i'll": "I will", 
        "i'm": "I am", 
        "i've": "I have", 
        "isn't": "Is not", 
        "it'd": "It would", 
        "it'll": "it will", 
        "it's": "it is", 
        "let's": "let us", 
        "ma'am": "madam", 
        "mayn't": "may not", 
        "may've": "may have", 
        "might've": "might have", 
        "mustn't": "must not", 
        "must've": "must have", 
        "needn't": "need not", 
        "o'clock": "of the clock", 
        "shalln't": "shall not", 
        "shan't": "shall not", 
        "she'll": "she will", 
        "she's": "she is",
        "she'd": "she had", 
        "should've": "should have", 
        "shouldn't": "should not", 
        "that'll": "that will", 
        "there're": "there are", 
        "there'll": "there will", 
        "they're": "they are", 
        "they've": "they have", 
        "that'd": "that would", 
        "wasn't": "was not", 
        "weren't": "were not", 
        "what'd": "what did", 
        "what've": "what have", 
        "when's": "when is", 
        "where'd": "where did", 
        "where'll": "where will", 
        "which's": "which is", 
        "which've": "which have", 
        "who'll": "who will", 
        "who're": "who are", 
        "who's": "who is", 
        "who've": "who have",
        "why'd": "why did", 
        "wouldn't": "would not", 
        "won't": "will not",
        "you've": "you have", 
        "you're": "you are"
        }

#removes SGML tags 
#input string, output string
def removeSGML(data):
    return re.sub(r'<.*>', '', data)
#tokenizes input string, returns list of tokens 
#should separate punctuation from words when punctuation isnt included in word (ex: Friday, = Friday ,) (ex: U.S.A. = U.S.A.) 
#should not tokenize acronyms, abbreviations, numbers
#tokenize apostrophe (I'm -> I am), (Sunday's -> Sunday 's)
#input string, output list of tokens
def tokenizeText(data):
    contractionsLower = dict((k.lower(),v.lower()) for k,v in commonContractions.items())
    tokens = data.split()
    for i in range(0,len(tokens)):
        #expand if contraction 
        if tokens[i].lower() in contractionsLower:
            expanded = commonContractions[tokens[i].lower()].split()
            tokens[i] = expanded[0]
            for i in range(1, len(expanded)):
                tokens.append(expanded[i])
        #if we end with punctuation and the word does not resemble and acronym/abbreviation, tokenize it  
        if (tokens[i][-1] in punctuation and not re.match(r'(?:[a-zA-Z]\.){2,}', tokens[i])):
            temp = tokens[i]
            tokens[i] = temp[0:len(temp) -1 :1]
            tokens.append(temp[-1])
        #tokenize apostrophe
        if (len(tokens[i]) >=2 and tokens[i][-2] == '\''):
                temp = tokens[i]
                tokens[i] = temp[0:len(temp) -2: 1]
                tokens.append(temp[len(temp) -2:])
    return tokens 

#removes stopwords
#input list of tokens, output list of tokens 
def removeStopwords(tokens):
    for word in stopwords: 
        tokens = list(filter((word).__ne__,tokens))
    return tokens 

#stems the words 
#input list of tokens, output list of stemmed tokens 
def stemWords(tokens):
    returnList = []
    for token in tokens:
        p = PorterStemmer()
        returnList.append ( p.stem(token,0,len(token)-1) )   
        
    return returnList

def processFile(fName):
    text_file = open(fName)
    data = text_file.read()
    text_file.close()
    data = removeSGML(data)
    data = tokenizeText(data)
    data = removeStopwords(data)
    data = stemWords(data)
    return data 

#generate the stats as stated in the spec 
def genStats(statsTable): 
    f = open("preprocess.output",'w')
    f.write("Words " + str(sum(statsTable.values())) + "\n")
    f.write("Vocabulary " + str(len(statsTable)) + "\n") 
    f.write("Top 50 Words\n")
    sorted_table = sorted(statsTable.items(), key=lambda x:x[1], reverse=True)
    removedPunctuation = list(sorted_table);
    #CODE FOR min number of words accounting for 25% of total 
    #fraction = 0.0
    #count = 0
    #total = 0
    #while (fraction < .25): 
    #    total += removedPunctuation[count][1]
    #    fraction = total / sum(statsTable.values())
    #    count += 1
    #print(count)
    #print(fraction)
    #########################################################
    topFifty = (removedPunctuation)[0:50]
    for i in topFifty:
        f.write(i[0] + " " + str(i[1]) +"\n") 
    f.close()
#main program should open folder of data, read one file at a time
#for each file apply removeSGML,tokenizeText,removeStopwords,stemWords\
#should have code to calc num words in collection 
#should have code to determine vocabulary size 
#should have code to determine most frequen 50 words in collection w/ frequencies listed in reverse order from most to least
#produce file called preprocess output with the following format: 
#Words [total num of words] 
#Vocabulary [total num of unique words] 
#Top 50 Words
#Word1 [word 1 freq] 
#word2 [word 2 freq]
#etc


def process_web_page_content(page_content: BeautifulSoup) -> 'list[str]':
    pageTxt = re.sub(r"\n+", "\n", page_content.get_text())
    pageTxt = re.sub(r" +"," ",  pageTxt)
    pageTxt = re.sub(r"[^\w\s]"," ",  pageTxt)
    tokens = tokenizeText(pageTxt)  
    for i in range(0,len(tokens)):
        if (tokens[i] in punctuation):
            tokens.remove(tokens[i])
        else:
            tokens[i] = tokens[i].lower()
    tokens = removeStopwords(tokens)
    tokens = stemWords(tokens)
    return tokens

def main():
    statsTable = {}
    if len(sys.argv) == 2: 
        directory = sys.argv[1]
        for entry in os.scandir(directory): 
            #sanity check to ensure data is a file
            if entry.is_file():
                tempList = processFile(entry)
                for token in tempList:
                    #remove any punctuation tokens generated in the token process before counting vocab 
                    if not token in punctuation and not token == " " and not token == '': 
                        if token in statsTable: 
                            statsTable[token] += 1
                        else:
                            statsTable[token] = 1
            else:
                print(entry.path + " is not a file")
        genStats(statsTable)
    else:
        sys.stderr.write("Usage: python3 preprocess.py [Path to directory containing data files]\n")

if __name__ =="__main__":
    main()
