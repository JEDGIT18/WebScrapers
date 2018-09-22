import requests
import re
import sys
import winsound
import linecache
import os
from bs4 import BeautifulSoup


walmartFw = open('walmartitems.txt', 'w')  # makes or writes a file
while True:
    try:
        maxPages = int(input("How many pages of results do you want: "))
        costMax = float(input("Max price: "))
        costMin = float(input("Min price: "))
        break
    except ValueError:
        print("these values must be Numbers!!")

def tradeSpiderWal(maxPages):
    page = 1
    while page <= maxPages:
        print("Page: ", page)
        url = 'https://www.walmart.com/browse/video-games/refurbished-preowned-video-games-consoles-accessories/2636_1056224?grid=false&page='+str(page)+'&sort=new#searchProductResult'
        srcCode = requests.get(url)
        plainTxt = srcCode.text
        print("get")
        soup = BeautifulSoup(plainTxt,"html.parser")
        for link in soup.findAll('a', {'class': 'product-title-link line-clamp line-clamp-2'}):
            href = 'https://www.walmart.com/'+link.get('href')
            if grabWalItemPrice(href) != None and grabWalItemPrice(href) >= costMin and grabWalItemPrice(href) <= costMax:

                print(grabWalItemName(href) + " Cost is: " + str(grabWalItemPrice(href)) + " Link: " + href)
                walmartFw.write(grabWalItemName(href) + " Cost is: " + str(grabWalItemPrice(href)) + " Link: " + href + '\n')  # writes to file


        page += 1
    clearscreen()
    print('\n')

def grabWalItemName(itemUrl):
    srcCode = requests.get(itemUrl)
    plainTxt = srcCode.text
    soup = BeautifulSoup(plainTxt, "html.parser" )
    for itemName in soup.findAll('h1', {'class': 'prod-ProductTitle no-margin font-normal heading-a'}):
        return itemName.text.replace("Details about", "")
    # for link in soup.findAll('a', href = True):
    #     href = link.get('href')
    #     if len(href) > 16:
    #         print(href)


def grabWalItemPrice(itemUrl):
    srcCode = requests.get(itemUrl)
    plainTxt = srcCode.text
    soup = BeautifulSoup(plainTxt, "html.parser" )
    for itemName in soup.findAll('span', {'class': 'price-group'}):
        price = itemName.text[1:]
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
tradeSpiderWal(maxPages)
winsound.Beep(400, 500)

while True:
    find = input("search through results: y/n ")
    print(find)
    if find == "n":
        break
    elif find == "y":
        typeS = input("search based on what keyword: ")
        key = input("Name: ")
        with open('walmartitems.Txt', 'r') as myFile:
            for line in myFile:
                if key.lower() in line.lower():
                    print(line)
