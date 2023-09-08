import argparse



def main(): 

    parser = argparse.ArgumentParser(description="Given a list of known correct urls and scraped urls, calculate the precision and recall", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("knownEventUrls", help="File containing urls of known event listings")
    parser.add_argument("fileToCheck", help="List of URLS that have been determined relevant by some algorithm")

    args= vars(parser.parse_args())

    with open(args["knownEventUrls"]) as f: 
        knownEventUrls = f.readlines()
    f.close()
    with open(args["fileToCheck"]) as a: 
        urlsToCheck = a.readlines()
    a.close()

    # write output
    relevent_returned = open('relevent_returned.output', "w+")
    relevent_not_returned = open('relevent_not_returned.output', "w+")
    irrelevent_returned = open('irrelevent_returned.output', "w+")
    
    num_relevent_and_returned = 0

    for url in knownEventUrls:
        if url in urlsToCheck:
            num_relevent_and_returned += 1
            relevent_returned.write(url)
        else:
            relevent_not_returned.write(url)

    for url in urlsToCheck:
        if url not in knownEventUrls:
            irrelevent_returned.write(url)
    
  

    num_relevent = len(knownEventUrls)
    num_returned = len(urlsToCheck)

    recall = num_relevent_and_returned / num_relevent
    precision = num_relevent_and_returned / num_returned

    print("Precision: " + str(precision))
    print("Recall: " + str(recall))


    return 0

if __name__=="__main__":
    exit(main())