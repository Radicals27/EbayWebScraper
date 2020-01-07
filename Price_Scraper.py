import csv
import urllib.request
from bs4 import BeautifulSoup
import time

item_links = []     #Stores the names of each result/item
price_links = []    #Stores the price (AUD) of each result

#Get the URL of the search results for "rtx 2080" graphics card
website = "https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=rtx+2080&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=gtx+2080"

#Try/catch block for a partial download of the website, if partially downloaded - continue, don't crash
try:
    page = urllib.request.urlopen(website)
except (http.client.IncompleteRead) as e:
    page = e.partial

soup = BeautifulSoup(page, 'lxml')

#To make things clearer, put all <a> tags and <span> tags into their own lists
all_a_tags = soup.find_all("a")
all_span_tags = soup.find_all("span")

#Search through all the <a> tags for each item/result and append it to item_links list
for link in all_a_tags:
    try:
         tester = link.get("href")
         if "https://www.ebay.com.au/itm/" in link.get("href"):     #Check for duplicate entries
             if link.get("href") in item_links:
                 print("duplicate found")
             else:
                item_links.append(link.get("href"))
    except:
        tester = None

#Wait 3 seconds as to not overload the eBay server
time.sleep(3)

#Repeat for the prices and append this next to their respective item
for link in all_span_tags:
    try:
         tester = link.get("class")
         if "item__price" in str(link):
             split_link = str(link).split('>')
             split_link = split_link[1].split('<')
             price_links.append(split_link[0])
    except:
        tester = None

#Print out the number of items found
print("Items collected: ", len(item_links))
print("Prices collected: ", len(price_links))

#Open a new .csv file and append these items and prices to it
with open('All_items.csv', 'a', newline='\n') as csvFile: 
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='excel')

    for i in item_links:
        writer.writerow([i, price_links[item_links.index(i)]])

csvFile.close()
