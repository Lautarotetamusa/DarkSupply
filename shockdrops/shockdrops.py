import requests
import json

addToCart = 'https://nikeclprod.myvtex.com/checkout/cart/add?sku={}&qty=1&seller=1&redirect={}&sc=1'
cartUrl   = 'https://nikeclprod.myvtex.com/api/checkout/pub/orderForm/{}?allowOutdatedData=paymentData'

# Funcion auxiliar para manejar errores #
def json_err(msg, e):
    return json.dumps({'ERROR': msg, 'Exception': str(e)})

# Crea un nuevo carro #
# Devuelve el ofid del mismo #
def new_cart(skus):
    res = requests.get(addToCart.format(skus[0], 'false'))   #Agregamos el primer elemento y guardamos el ofid
    ofid = res.cookies.get_dict()['checkout.vtex.com']       #Generamos un nuevo carro con un nuevo ofid

    skus.pop(0)
    add(skus, ofid)   #Pasamos la lista sin el primer elemento
    return ofid

# Lista los skus actualmente monitoreados #
# Lo saca del carro virtual #
def list():
    with open('ofid', 'r') as f:
        ofid = f.read().replace('\n','').split('__ofid=')[1]
    res  = json.loads(requests.get(cartUrl.format(ofid)).text)

    skus = []
    for i in res['items']:
        skus.append(i['id'])

    return skus

# Agrega skus al carrito #
# Si no le pasamos ofid lo hace con el id del archivo #
# Sino crea un carro nuevo y agrega todos ahi #
def add(skus, ofid=''):
    if skus == []:  #Si no hay skus salimos de la funcion
        return

    if ofid == '':
        with open('ofid', 'r') as f:
            cookie = {'checkout.vtex.com': f.read().replace('\n', '')}
    else:
        cookie = {'checkout.vtex.com': ofid}

    for sku in skus:
        res = requests.get(addToCart.format(sku, 'false'), cookies=cookie)

# Elimia skus del carro #
# Crea un nuevo carro con los skus que estaban - los a eliminar #
def remove(to_remove):
    actual = list()    #Buscamos los skus actuales
    skus = [i for i in actual if i not in to_remove]    #Creamos una nueva lista

    ofid = new_cart(skus)           #Generamos un nuevo carro con la nueva lista
    with open('ofid', 'w') as f:    #Escribimos el nuevo ofid en el archivo
        f.write(ofid)

# Realiza la consulta para ver si los pares estan o no disponibles  #
# Si pasamos skus entonces hace un chequeo en un carro nuevo        #
# Si no pasamos nada usa el carro con el id del archivo ./ofid      #
def restock(skus=[]):
    if skus != []: #Si pasamos skus es para hacer un checkeo
        ofid = new_cart(skus)   #Generamos un carrito nuevo
    else:
        with open('ofid', 'r') as f:
            ofid = f.read()

    ofid = ofid.replace('\n','').split('__ofid=')[1]
    res  = json.loads(requests.get(cartUrl.format(ofid)).text)

    avaiblesSkus = []
    for i in res['items']:
        #If the product is avaible
        if( i['availability'] == "available" ):
            rawName = i['name']

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

            listprice = str(i['listPrice'])
            price = "$"+(listprice[-len(listprice):-5]) +"."+(listprice[-5:-2])
            avaiblesSkus.append({
                'img':   i['imageUrl'],
                'cartUrl': addToCart.format(i['id'], "True"),
                'price': price,
                'available': i['availability'],
                'sku':   i['id'],
                'name':  name,
                'size':  size,
                'color': color
            })

    return avaiblesSkus
