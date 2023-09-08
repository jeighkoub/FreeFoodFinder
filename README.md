This Project consists of 3 major components: 

The Web Crawler - crawl.py: 

    1. The web crawler is used to gather a collection of URLS to test for relevancy
    
    2. The crawler is seeded with a set of URLs and explores new pages that these seed Urls point to
    
    3. In order to increase the efficiency of the crawler, a list of Ignored Domains (ex: youtube.com), and a list of ignored endpoints (ex: about/) can be supplied to the crawler. Any urls matching these criteria will not be added to the crawler data and will not be explored further. The purpose of this is to prune irrelvant branches from the network of nodes that the crawler can search. 
    
    4. The crawler can also be given a Mode to run in, either BFS or DFS, corresponding to the search mode that the crawler will use. This was done in order to allow for experimentation to improve the maximum recall of the system. Ultimately, it was found that DFS is not super effective for the context of this project, as DFS causes the crawler to quickly jump to irrelevant webpages. 

    4. Run the crawler using the following format: 
            python3 crawl.py seedFile ignoredDomains ignoredEndpoints Mode[bfs,dfs] outputFile 
            python3 crawl.py myseedURLS.txt ignoredDomains.txt ignoredEndpoints.txt dfs outputFiles

    5. Running the command above will create a directory called crawlData/[name of outputfile]/ 
        - The crawler will writeback a JSON dictionary containing  URL-processedContent pairs, where processedContent is the tokenized content of the webpage found at the URL. 
        - Writebacks occur every 100 URLS collected 
    
    6. The crawler will also pull any url that links to an image and save this in a seperate file under crawlData/[outputFileName]/imageData, this list of URLs can be passed to getImageText.py
        - getImageText.py runs the list of imageUrls and creates a list jsonObject of url, tokenized content pairs to be processed. This was determined to be very slow, and did not significantly improve recall,  and was not used in the final data. 



The Relevancy Decider - determineRelevancy.py: 

    1. The relevancy decider is used to provide a list of relevant urls. A url is decided to be relevant if the decider classifies it as an event that is providing free food. 
    
    2. The relevancy decider has three main modes: naive_bayes and "boolean" and "combined", where boolean just checks if the presence of certain keywords is true or false 

    3. The program can be run in naiveBayes mode as follows: 
        - python3 determineRelevancy.py -n trainingData.json [path to list of crawlerData]
        - The trainingData.json file is generated via trainNaiveBayes.py, this program takes in a list of known free-food event urls and a list of random webpages to traing the classifier, both of these sets were manually collected and can be found under /NaiveBayesTrainingData/, the output is a json object containing all of the numbers needed to create a naiveBayes model 
    
    4. The program can be run in "boolean" mode as follows: 
        - python3 determineRelevancy.py -b [path to crawlerData]
        - This method searches through each url's processed content and compares it to a set of manually generated keywords in order to determine url relevancy

        python3 determineRelevancy.py -b ../crawlData/BFS_Data/
        
        python3 determineRelevancy.py -b ../crawlData/BFS_Data/

    5. The relevancy decider has an optional "combined" flag, that runs the keyword relevancy function on top of the naiveBayes classification. The different methods allowed by this program were used to experiment and determine which methodology obtained the best precision and recall. 



Precision and Recall Calculator: 

    - This program is used to calculate the precions and recall for each of the sets of urls returned from determineRelevancy.py 

    - use python3 calcPrecisionRecall.py -h for more information 

    python3 calcPrecisionRecall.py ../RelevancyData/All_Free_Food_Events_from_events.umich.txt ../RelevancyData/RelevantUrls.boolean



