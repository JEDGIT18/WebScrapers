import requests
import re
import sys
import winsound
import linecache
import os
from bs4 import BeautifulSoup

EbayFw = open('ebayitems.txt', 'w')  # makes or writes a file
keyword = input("What do you want to search: ")
while True:
    try:
        maxPages = int(input("How many pages of results do you want: "))
        costMax = float(input("Max price: "))
        costMin = float(input("Min price: "))
        break
    except ValueError:
        print("these values must be Numbers!!")

def tradeSpiderEbay(maxPages):
    page = 1
    while page <= maxPages:
        print("Page: ", page)
        url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + keyword + '&_sacat=0&LH_TitleDesc=0&LH_TitleDesc=0&_pgn=' + str(page)
        srcCode = requests.get(url)
        plainTxt = srcCode.text
        soup = BeautifulSoup(plainTxt,"html.parser")
        for link in soup.findAll('a', {'class': 's-item__link'}):
            href = link.get('href')
            if grabEbayItemPrice(href) != None and grabEbayItemPrice(href) >= costMin and grabEbayItemPrice(href) <= costMax:

                print(grabEbayItemName(href) + " Cost is: " + str(grabEbayItemPrice(href)) + " Link: " + href)
                EbayFw.write(grabEbayItemName(href) + " Cost is: " + str(grabEbayItemPrice(href)) + " Link: " + href + '\n')  # writes to file


        page += 1
    clearscreen()
    print('\n')


def grabEbayItemName(itemUrl):
    srcCode = requests.get(itemUrl)
    plainTxt = srcCode.text
    soup = BeautifulSoup(plainTxt, "html.parser" )
    for itemName in soup.findAll('h1', {'id': 'itemTitle'}):
        return itemName.text.replace("Details about", "")
    # for link in soup.findAll('a', href = True):
    #     href = link.get('href')
    #     if len(href) > 16:
    #         print(href)


def grabEbayItemPrice(itemUrl):
    srcCode = requests.get(itemUrl)
    plainTxt = srcCode.text
    soup = BeautifulSoup(plainTxt, "html.parser" )
    for itemName in soup.findAll('div', {'class': 'u-flL w29 vi-price '}):
        price = itemName.text[5:]
        price = re.sub('[^\d\.]', '', price)
        price = float(price)
        price = round(price, 2)
        return price

def clearscreen(numlines=100):
  """Clear the console.
numlines is an optional argument used only as a fall-back.
"""
# Thanks to Steven D'Aprano, http://www.velocityreviews.com/forums

  if os.name == "posix":
    # Unix/Linux/MacOS/BSD/etc
    os.system('clear')
  elif os.name in ("nt", "dos", "ce"):
    # DOS/Windows
    os.system('CLS')
  else:
    # Fallback for other operating systems.
    print('\n' * numlines)
tradeSpiderEbay(maxPages)
winsound.Beep(400, 500)

while True:
    find = input("search through results: y/n ")
    print(find)
    if find == "n":
        break
    elif find == "y":
        typeS = input("search based on what keyword: ")
        key = input("Name: ")
        with open('ebayitems.Txt', 'r') as myFile:
            for line in myFile:
                if key.lower() in line.lower():
                    print(line)









































