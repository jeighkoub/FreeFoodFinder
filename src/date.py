import datetime
import json

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

#find date in crawled urls json file and return it as a datetime object 
def find_date(url, json_file):

    day = ""
    month = ""
    year = ""
    
    dayNum = -1
    monthNum = -1
    yearNum = -1


    with open(json_file) as f:
        data = json.load(f)
        for index, item in enumerate(data[url]):
            
            #check if item is a month name
            if item in months:
                month = item
                monthNum = (months.index(item) % 12) + 1
                
                # get day and year
            
            # number can be day or year or neither
            elif item.isdigit():
                #check if number is a day
                if int(item) <= 31 and int(item) > 0:
                    day = item
                    dayNum = int(item)
                #check if number is a modern year
                elif int(item) > 2021 and int(item) < 2100:
                    year = item
                    yearNum = int(item)


            