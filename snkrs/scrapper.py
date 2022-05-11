from bs4 import BeautifulSoup
import json
from selenium import webdriver
from time import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By

driver = '../geckodriver'

url = 'https://www.nike.cl/api/catalog_system/pub/products/search/snkrs/calzado?map=c,c&&_from=0&_to=49'
cartUrl = 'https://www.nike.cl/checkout/cart/add?sku={}&qty=1&seller=1&sc=1'

def last_shoes():

    try:
        browser.get(url)
        content = browser.page_source

        page = BeautifulSoup(content, 'html.parser')
        jsonRes = page.find(id='json').text
        list = json.loads(jsonRes)
    except Exception as e:
        return []

    products = []
    for i in list:
        totalStock = 0
        variants = []
        for scVariant in i['items']:
            try:
                stock = scVariant['sellers'][0]['commertialOffer']['AvailableQuantity']
                sku = scVariant['itemId']
                variant = {
                    'sku':       scVariant['itemId'],
                    'size':      scVariant['talle'][0],
                    'color':     scVariant['color'][0],
                    'cartUrl':   cartUrl.format(sku),
                    'stock':     stock
                }
            except Exception as e:
                variant = {'ERROR': 'error obtaining variant data', 'Exception': str(e)}

            totalStock += stock
            variants.append(variant)

        listprice = str(i['items'][0]['sellers'][0]['commertialOffer']['ListPrice'])
        price = "$"+(listprice[-len(listprice):-5]) +"."+(listprice[-5:-2])

        try:
            imgId = i['items'][0]['images'][0]['imageId']
            product = {
                'id':    i['productId'],
                'name':  i['productName'],
                'url':   'https://nike.cl/'+i['linkText']+'/p',
                'price': price,
                'stock': totalStock,
                'img':  'https://nikeclprod.vteximg.com.br/arquivos/ids/{}/'.format(imgId),
                'releaseDate': i['releaseDate'][0:19],
                'variants': variants
            }
        except Exception as e:
            product = {'ERROR': 'error obtaining product data', 'Exception': str(e)}

        products.append(product)
    return products

def get_news():
    newList = last_shoes()

    if newList == []:
        return {"ERROR": "Error getting last shoes"}

    f = open('./list.json', "r")
    oldList = json.loads(f.read())

    news    = [i for i in newList if i not in oldList]
    deleted = [i for i in oldList if i not in newList]


    if (news != []) or (deleted != []):
        with open('./list.json', 'w', encoding='utf-8') as f:
            json.dump(newList, f, indent=4, ensure_ascii=False)

    return json.dumps(news)

def json_err(msg, e):
    return json.dumps({'ERROR': msg, 'Exception': str(e)})

try:
    binary = FirefoxBinary(driver)
    browser = webdriver.Firefox()
    browser.minimize_window()
except Exception as e:
    print (json_err('Driver error', e))
    quit()


try:
    print(get_news())
except Exception as e:
    print (json_err("Error in scraper", e))

browser.quit()
