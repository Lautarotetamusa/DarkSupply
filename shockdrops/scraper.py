import time
import json
import sys

sys.path.append(".")
import shockdrops as s

# print(getattr(s, 'restock')())

#Consultas
try:
    opt = sys.argv[1]

    if opt == 'restock': #Funcion principal
        print (json.dumps(s.restock()))

    elif opt == 'check':  #Checkear si una lista de productos esta disponible
        skus = sys.argv[2:]
        print (json.dumps(s.restock(skus=skus)))

    elif opt == 'add':    #Añadir un sku a la lista
        added = sys.argv[2:]
        s.add(added)

    elif opt == 'remove': #Remover un sku de la lista
        skus = sys.argv[2:]
        s.remove(skus)

    elif opt == 'list':   #Listar los skus
        print (json.dumps(s.list()))

    elif opt == 'test':   #Hace la consulta mostrando el tiempo
        start = time.time()
        print(json.dumps(s.restock()))
        print(time.time() - start)

except Exception as e:
    print (s.json_err('Python s error', e))

sys.stdout.flush()
