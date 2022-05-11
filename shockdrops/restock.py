import sys
import json
import requests
import time
import pickle
from selenium import webdriver
from bs4 import BeautifulSoup
import xml.etree.ElementTree as xml
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

driver  = '../geckodriver'

addToCart = 'https://www.nike.cl/checkout/cart/add?sku={}&qty=1&seller=1&redirect={}&sc=1'
cartUrl = 'https://www.nike.cl/api/checkout/pub/orderForm?refreshOutdatedData=true'

#https://www.nike.cl/checkout/cart/add?sku=14078&qty=1&seller=1&redirect=false&sc=1

def new_cart(skus):
    try:
        browser.delete_cookie('checkout.vtex.com')

        ofid = ""
        # Añadimos un sku falso al carro para poder crearlo
        if skus == []:
            uri = addToCart.format('0', "false")

        # Si no es vacio los agregamos al carro
        for sku in skus:
            uri = addToCart.format(sku, "false")

        browser.get(uri)
        page = BeautifulSoup(browser.page_source, 'html.parser')

        cookies = browser.get_cookies()
        for c in cookies:
            if(c['name'] == 'checkout.vtex.com'):
                ofid = c['value']

        #Guardar la cookie usada en el archivo
        #print("OFID", ofid)
        with open('ofid', 'w') as f:
            f.write(ofid)
    except Exception as e:
        browser.quit()
        raise

#Lo saca del carro virtual
def list_skus():
    set_cookie()
    browser.get(cartUrl)

    page = BeautifulSoup(browser.page_source, 'html.parser')
    data = page.find_all('itemmetadataresponse')
    #print(page  )

    skus = []
    #print(data)
    for i in data:
        skus.append(i.id.text)

    return skus

def restock(skus=[]):
    #Get the cart with this cookie
    if len(skus) == 0:
        #print("usando cookie")
        set_cookie()

    for sku in skus:
        #print("carrito nuevo");
        browser.get(addToCart.format(sku, 'false'))

    browser.get(cartUrl)

    page = BeautifulSoup(browser.page_source, 'html.parser')

    data     = page.find_all('itemmetadataresponse')
    metadata = page.find_all('orderitemresponse')

    avaiblesSkus = []
    for i in range(len(data)):
        rawName = data[i].find('name').text

        try:
            name  = rawName.split(' Talla:')[0]
        except Exception as e:
            json_err ("Err obtain name "+rawName, e)
            name = 'err'
        try:
            size  = rawName.split(' Talla:')[1].split(' - ')[0]
        except Exception as e:
            json_err ("Err obtain size "+rawName, e)
            size = 'err'
        try:
            color = rawName.split(' Talla:')[1].split('- Color: ')[1]
        except Exception as e:
            json_err ("Err obtain color "+rawName, e)
            color = 'err'

        listprice = metadata[i].listprice.text
        price = "$"+(listprice[-len(listprice):-5]) +"."+(listprice[-5:-2])
        product = {
            'img':   data[i].imageurl.text,
            'cartUrl': addToCart.format(metadata[i].id.text, "True"),
            'price': price,
            'available': metadata[i].availability.text,
            'sku':   data[i].id.text,
            'name':  name,
            'size':  size,
            'color': color
        }
        #print(product)
        if( metadata[i].availability.text == "available" ):
            avaiblesSkus.append(product)

    return avaiblesSkus

def json_err(msg, e):
    return json.dumps({'ERROR': msg, 'Exception': str(e)})

def set_cookie():
    browser.get(cartUrl)
    browser.delete_cookie('checkout.vtex.com')
    with open('ofid', 'r') as f:
        ofid = f.read()
    browser.add_cookie({'name': 'checkout.vtex.com', 'value': ofid})

def add_skus(skus):
    set_cookie()

    for sku in skus:
        uri = addToCart.format(sku, "false")
        browser.get(uri)

def update(upt, opt="remove"):
    #Leer desde el archivo
    with open('monitored-skus.json', 'r', encoding='utf-8') as f:
        skus = json.loads(f.read())

    if opt=="remove":
        skus = [i for i in skus if i not in upt]
        #print("NEW CART", skus)
        new_cart(skus) #Cambiar el carro
    elif opt=="add":
        skus += [i for i in upt if i not in skus]
    elif opt=="restart":
        skus = []

    #Escribir el archivo
    with open('monitored-skus.json', 'w', encoding='utf-8') as f:
        json.dump(skus, f, indent=4, ensure_ascii=False)

try:
    binary = FirefoxBinary(driver)
    browser = webdriver.Firefox()
    browser.minimize_window()
except Exception as e:
    print (json_err('Driver error', e))
    quit()

#Consulta
try:
    opt = sys.argv[1]

    if opt == 'restock': #Funcion principal
        avaibles = restock()

        #Si hay algun disponible lo sacamos de la lista y hacemos un carrito nuevo
        #if len(avaibles) > 0:
            #print([i["sku"] for i in avaibles])
            #update([i["sku"] for i in avaibles], opt="remove")
        print(json.dumps(avaibles))

    elif opt == 'check': #Checkear si una lista de productos esta disponible
        skus = sys.argv[2:]
        print (json.dumps(restock(skus=skus)))

    elif opt == 'add': #Añadir un sku a la lista
        added = sys.argv[2:]
        update(added, opt="add")
        add_skus(added)

    elif opt == 'remove': #Remover un sku de la lista
        skus = sys.argv[2:]
        #print(skus)
        update(skus, opt="remove")

    elif opt == 'list': #Listar los skus
        #print(list_skus())
        with open('monitored-skus.json', 'r', encoding='utf-8') as f:
            skus = json.loads(f.read())
        #print(skus)

    elif opt == 'restart':
        new_cart(['0'])
        update(['0'], opt="restart")
    elif opt == 'test':
        start = time.time()
        avaibles = restock()
        print(json.dumps(avaibles))
        print(time.time() - start)

except Exception as e:
    print (json_err('Python scraper error', e))
    browser.quit()

sys.stdout.flush()
browser.quit()



"""
funca
print("COOKIES VIEJAS")
browser.get(cartUrl)
print(browser.get_cookies())
print("\n\nCOOKIES CAMBIADAS")
browser.delete_cookie('checkout.vtex.com')
browser.add_cookie({'name': 'checkout.vtex.com', 'value': '__ofid=849b4dc23fb64b2a92a796c7c51a1446'})
browser.get(cartUrl)
print(browser.get_cookies())
print("\n\nPAGINA")
print(restock())
"""
