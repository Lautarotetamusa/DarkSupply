from bs4 import BeautifulSoup
import json
import requests
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import

driver = '../geckodriver';

searchUrl = 'https://u.braindw.com/els/nikeclprod?ft={}&_from=0&qt=500&sc=1&refreshmetadata=true&aggregations=true&hash=nikecl_produccion_j4ufe&objecttype=vtex'

searchs = ['Jordan 1', 'Dunk', 'Air Force 1']

def get_shoes(search):
    source = requests.get(searchUrl.format(search))
    res = json.loads(source.text)

    list = res['hits']['hits']
    products = []

    for i in list:
        item = i['_source']

        variants = []
        for scVariant in item['items']:
            variant = {
                'sku':       scVariant['itemId'],
                'size':      scVariant['talle'][0],
                'color':     scVariant['color'][0],
                'cartUrl':   scVariant['sellers'][0]['addToCartLink'],
                'stock':     scVariant['sellers'][0]['commertialOffer']['AvailableQuantity']
            }
            variants.append(variant)

        url = 'https://nike.cl/'+item['linkText']+'/p'

        product = {
            'id':    item['productId'],
            'name':  item['productName'],
            'url':   url,
            'price': item['items'][0]['sellers'][0]['commertialOffer']['ListPrice'],
            'img':   item['items'][0]['images'][0]['imageUrl'],
            'releaseDate': item['releaseDate'],
            'variants': variants
        }

        products.append(product)

    return products
