import time
import collections
import heruko as h
import pandas as pd
import mysql.connector

def heruko():
    mydb = mysql.connector.connect(
        host=''
             '',
        user=''
             '',
        password=''
                 '',
        database='',
    )
    return mydb
mydb = heruko()

#create_movies_table_query = """
    #SELECT * FROM nike
   # ""
#with mydb.cursor() as cursor:
    #cursor.execute(create_movies_table_query)
    #print(cursor.fetchall())
    #mydb.commit()

#mydb = heruko()

def add_devices():
    df = pd.read_csv('gam43607.csv')
    cols_base = ['Lot #','Model', 'Item Description', 'Capacity', 'Grade', 'Carrier']
    cols_file = []
    for i in df.columns:
        cols_file.append(i)
    tm = len(df)
    items = [item for item, count in collections.Counter(cols_base + cols_file).items() if count > 1]
    data = {}
    for i in range(tm):
        for j in items:
            data[j] = df[str(j)][i]
    print(data)
#add_devices()

def read_csv(preco):
    cols_base = ['Model', 'Item Description', 'Capacity', 'Grade', 'Carrier']
    item_db = 'carrier,grade,capacity,description'
    df = pd.read_csv('gam43607.csv')
    dados_banco = h.consult(mydb)
    print("Banco --> ", dados_banco)
    values = []
    item = {}
    cols_file = []
    for i in df.columns:
        cols_file.append(i)
    tm = len(df)
    items = [item for item, count in collections.Counter(cols_base + cols_file).items() if count > 1]
    items.append('Lot #')
    items.append('Model #')

    for i in range(tm):
        print("[+] Verificando Manifest")
        for j in items:
            #if "Item Description" in str(j):
                #value  = (str(df[str(j)][i]).split(' '))[-1:]
                #item[j] = value[0]
            #else:
            item[j] = df[str(j)][i]
            # print(f"{j} --> ", df[str(j)][i])

        print(item)
        item['preco'] = preco
        item['frete'] = 3.60
        item['liquidity'] = 10
        item['imported'] = 1
        for i in dados_banco:
            validar_produto = 0
            model,carrier,grade,capacity,description = i
            description = (str(description).split(' '))[:-1]
            description = ' '.join(description)
            print(description)
            if str(carrier) ==  item["Carrier"]:
                validar_produto +=1
                print("Carrier --> ", carrier)
            if str(capacity) == item["Capacity"]:
                validar_produto+=1
                print("Capacity --> ", capacity)
            if str(grade) == item["Grade"]:
                validar_produto+=1
                print("Grade --> ", grade)
            if str(item["Item Description"]) in str(description):
                validar_produto+=1
                print("Description --> ", description)
            if validar_produto  < 4:
                print()
            print("------------------------")
        values.append(item)
        print(item)
        item = {}
        time.sleep(2)






read_csv('')