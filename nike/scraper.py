from bs4 import BeautifulSoup
import json
import os
import sys
import time
from selenium import webdriver
import xml.etree.ElementTree as xml
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By

driver  = '../geckodriver'

listUrl = 'https://www.nike.cl/buscapagina?fq=C%3a%2f2%2f3%2f&PS=100&sl=64632ac1-3290-4350-939a-ed5983d913ed&cc=1&sm=0&PageNumber={}'

detailUrl = 'https://www.nike.cl/api/catalog_system/pub/products/variations/{}'

skuUrl = 'https://www.nike.cl/produto/sku/{}'

addToCart = 'https://www.nike.cl/checkout/cart/add?sku={}&qty=1&seller=1&redirect={}&sc=1'

def last_shoes():
    i = 1
    ids = []

    while True:
        res = browser.get(listUrl.format(i))
        res = browser.page_source
        page = BeautifulSoup(res, 'html.parser')
        products = page.find_all('div', class_='item')

        if products:
            for product in products:
                ids.append(product["id"][8:])
        else:
            break
        i+=1

    return ids;

def get_details(productID):

    browser.get(detailUrl.format(productID))

    try:
        jsonShoe = json.loads(browser.find_element(By.TAG_NAME, "body").text)
        variants = jsonShoe['skus']
    except Exception as e:
        return {"ERROR": "La id del producto no se encuentra: "+str(productID), "Exception": str(e)}

    shoe = {}
    v = []

    for variant in variants:
        sku = variant['sku']

        try:
            browser.get(skuUrl.format(sku))
            jsonVariant = json.loads(browser.find_element(By.TAG_NAME, 'body').text)

            skuName = variant['skuname']
            ini = skuName.index(':')
            fin = skuName.index('-')
            skuName = "US " + skuName[ini+1:fin-1]

            v.append({
                'sku':sku,
                'stock':jsonVariant[0]['SkuSellersInformation'][0]['AvailableQuantity'],
                'cartUrl': addToCart.format(sku, "true"),
                'size': skuName,
                'available':variant['available']
                })
        except Exception as e:
            v.append(json_err("El sku no se encuentra: "+str(sku), e))

    try:
        price = jsonVariant[0]['SkuSellersInformation'][0]['ListPrice']
    except Exception as e:
        price = '--'

    shoe = {
        'id': productID,
        'name' : jsonShoe['name'],
        'price' : price,
        'img' : jsonShoe['skus'][0]['image'],
        'variants' : v
    }

    return shoe;

def get_news():
    newList = last_shoes()
    f = open('list.json', "r")
    oldList = json.loads(f.read())

    news    = [i for i in newList if i not in oldList]
    deleted = [i for i in oldList if i not in newList]
    shoes = []

    if news != []:
        with open('list.json', 'w', encoding='utf-8') as f:
            json.dump(newList, f, indent=4, ensure_ascii=False)

        for shoeId in news:
            shoes.append(get_details(shoeId))

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(shoes, f, indent=4, ensure_ascii=False)

    if deleted != []:
        with open('list.json', 'w', encoding='utf-8') as f:
            json.dump(newList, f, indent=4, ensure_ascii=False)

    return json.dumps(shoes)

def json_err(msg, e):
    return json.dumps({'ERROR': msg, 'Exception': str(e)})

try:
    binary = FirefoxBinary(driver)
    browser = webdriver.Firefox()
    browser.minimize_window()
except Exception as e:
    print (json_err('Driver error', e))
    quit()

#Consulta
if len(sys.argv) == 2:
    if sys.argv[1] == 'news':
        try:
            print (get_news())
        except Exception as e:
            print (json_err('Python scraper error', e))
            browser.quit()
    elif sys.argv[1] == 'restock':
        try:
            f = open('monitored-skus.json', "r")
            skus = json.loads(f.read())
            f.close()

            avaibles = restock(skus)
            skus = [i for i in skus if i not in avaibles]

            with open('monitored-skus.json', 'w', encoding='utf-8') as f:
                json.dump(skus, f, indent=4, ensure_ascii=False)

            print(avaibles)
        except Exception as e:
            print (json_err('Python scraper error', e))
            browser.quit()
    elif sys.argv[1] == 'test':
        errors = 0
        good = 0
        for i in range(25):
            f = open('monitored-skus.json', "r")
            skus = json.loads(f.read())
            f.close()
            res = restock(["1105", "13020"])
            list = json.loads(res)
            print(res)
            if len(list) != 1:
                errors = errors + 1
                print ('Error')
            else:
                good = good + 1
                print('Good')

        print('Good:', good)
        print('Errors', errors)
        print('AVG:', good / errors * 100)
elif len(sys.argv) == 3:
    if sys.argv[1] == 'check':
        try:
            skus = [sys.argv[2]]
            print (restock(skus))
        except Exception as e:
            print (json_err('Python scraper error', e))
            browser.quit()

#Cerrar driver y display
browser.quit()
sys.stdout.flush()
