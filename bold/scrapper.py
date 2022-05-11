import json
import requests

api = 'https://api.cxl8rgz-articulos1-p1-public.model-t.cc.commerce.ondemand.com'
listUrl = api+"/rest/v2/boldb2cstore/products/search?fields=products(url,code,name,price(value),images(url),stock(FULL))&query=:DEFAULT:allCategories:boldMarcas&currentPage={}&pageSize=100&lang=es_CL&curr=CLP"

listCodes = api + "/rest/v2/boldb2cstore/products/search?fields=products(code)&query=:DEFAULT:allCategories:boldMarcas&currentPage={}&pageSize=100&lang=es_CL&curr=CLP"

detailUrl = api + "/rest/v2/boldb2cstore/products/ADGW3518?fields=code,name,summary,price(formattedValue,DEFAULT),regularPrice(formattedValue),images(galleryIndex,FULL),badges,potentialPromotions(DEFAULT),formattedDiscount,categories(FULL),url,purchasable,baseOptions(DEFAULT),baseProduct,variantOptions(DEFAULT),variantType,averageRating,stock(DEFAULT),description,availableForPickup,numberOfReviews,manufacturer,priceRange,multidimensional,configuratorType,configurable,tags,maxOrderQuantity&lang=es_CL&curr=CLP"

def last_shoes():
    page = 1
    empty = False
    shoes = []

    while not empty:
        res = requests.get(listUrl.format(page))
        products = res.json()['products']

        if(len(products) <= 0):
            break;

        for i in products:
            #product = parse_product(i)
            shoes.append(i['code'])
        page = page + 1

    return shoes

def get_details(code):
    res = requests.get(detailUrl.format(code))
    rawProduct = res.json()
    variants = rawProduct['variantOptions']
    sizes = []
    stockTotal = 0

    for v in variants:
        stock = v['stock']["stockLevel"]
        stockTotal = stockTotal + stock

        variant = {
          'code'  : v['code'],
          'stock' : stock,
          'size'  : v['variantOptionQualifiers'][0]["value"],
          'url'   : "https://bold.cl"+ v['url']
        }
        sizes.append(variant)
    product = parse_product(rawProduct)
    product['variants'] = sizes
    product['stock'] = stockTotal

    return product

def parse_product(i):

    try:
        name = i['name']
    except Exception as e:
        name = 'err'
    try:
        price = i['price']['value']
    except Exception as e:
        price = 'err'
    try:
        code = i['code']
    except Exception as e:
        code = 'err'
    try:
        stock = i['stock']['stockLevel']
    except Exception as e:
        stock = 'err'
    try:
        image = api+i['images'][0]['url']
    except Exception as e:
        image = 'err'
    try:
        url = "http://bold.cl"+i['url']
    except Exception as e:
        url = 'err'

    product = {
        'name':  name,
        'price': price,
        'code':  code,
        'stock': stock,
        'image': image,
        'url':   url
    }
    return product

print(json.dumps(get_details('NIDC8902200'),indent=4, ensure_ascii=False))
with open('list.json', 'w', encoding='utf-8') as f:
    json.dump(last_shoes(), f, indent=4, ensure_ascii=False)
print('Consulta realizada')
