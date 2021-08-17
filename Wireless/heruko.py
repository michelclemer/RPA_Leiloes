import collections
import os
import time
from datetime import datetime
from os import listdir
from os.path import isfile, join
import mysql.connector
import pandas as pd

def heruko():
    mydb = mysql.connector.connect(
        host='',
        user='',
        password='',
        database='',
    )
    return mydb

def format_data(date):
    data, hora  = str(date).split(' ')
    ano, mes, dia = str(data).split('-')
    data_formatado = []
    if int(mes) < 10:
        try:
            mes = str(mes).replace('0', '')
        except:
            pass
    data_formatado.append(ano)
    data_formatado.append(mes)
    if int(dia)< 10:
        try:
            dia = str(dia).replace('0','')
        except:
            pass
    data_formatado.append(dia)
    hora, min, seg = str(hora).split(':')
    if int(hora) <10:
        try:
            hora = str(hora).replace('0','')
        except:
            pass
    data_formatado.append(hora)
    if int(min) < 10:
        try:
            min = str(min).replace('0', '')
        except:
            pass
    data_formatado.append(min)
    return data_formatado

#cursor.execute("SELECT id, closure,link  FROM auctions")
#datas = cursor.fetchall()
#data_link_id = []

def value_exist(db, link):
    sqlq = f"select (1) from db where link='{link}'"
    con =[]
    with db.cursor() as cursor:
        cursor.execute(sqlq)
        data = cursor.fetchall()
        if len(data) > 0:
            return 1
        else:
            return 0



def consult(db):
    sqlq = "select id,model,carrier,grade,capacity,description from db"
    with db.cursor() as cursor:
        cursor.execute(sqlq)
        req = cursor.fetchall()
        return  req

def get_link_id(db, link):
    sqlq = f"select id from db where link = '{link}'"
    print("Buscando ID")
    with db.cursor() as cursor:
        cursor.execute(sqlq)
        req = cursor.fetchall()
        return req[0][0]

def update_table(db, link, current_bid):


    data = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    create_movies_table_query = "UPDATE db SET updated_at=%s,current_bid=%s WHERE link=%s"

    values = (data , current_bid ,str(link))
    cursor = db.cursor()
    cursor.execute(create_movies_table_query, values)

def action_devices(db,values, link):
    #db  = heruko()

    id = get_link_id(db, link)
    print("ID >>", id)
    print("Lista --> ", values)
    date_ = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    sql = ('INSERT INTO `db` (`quantity`, `lote`, `auction_id`, `device_id`, `updated_at`) VALUES (%s, %s, %s, %s, %s)')
    val = (str(values["Qty"]), str(values["lote"]), str(id), str(values["device_id"]), str(date_))
    #print(str(values['Qty']), str(values['lote']), str(id), str(values['device_id']), str(date_))
    print("Inserindo Device")

    with db.cursor() as cursor:
        cursor.execute(sql, val)
        db.commit()
        print("Inserido ok")

def consult3():
    h = heruko()
    cursor = h.cursor()


    cursor.execute("select * from db WHERE datee BETWEEN '2021-08-10 00:00:00' and '2021-08-14 00:00:00'")


    print(cursor.fetchall())

consult3()

def read_csv(mydb, preco, data_, file_name, link):
    p = (str(preco)[1:]).replace(',', '.')
    preco = str(('{:.2f}'.format(float(p))))
    cols_base = ['Model', 'Item Description', 'Capacity', 'Grade', 'Carrier', 'Qty']
    item_db = 'carrier,grade,capacity,description'
    print("File ", file_name)


    df = pd.read_csv(str(file_name))
    dados_banco = consult(mydb)

    #print("Banco --> ", dados_banco)
    values = []
    item = {}
    cols_file = []
    id_banco = 0
    list_action_devices = {}
    for i in df.columns:
        cols_file.append(i)
    tm = len(df)
    items = [item for item, count in collections.Counter(cols_base + cols_file).items() if count > 1]
    items.append('Lot #')
    items.append('Model #')
    item["Carrier"] = ''

    item["Capacity"] = ''
    item["Grade"] = ''
    item["Item Description"] = ''
    item['Lot #'] = ''
    item['Qty'] = ''
    for i in range(tm):
        print("[+] Verificando Manifest")
        for j in items:
            #if "Item Description" in str(j):
                #value  = (str(df[str(j)][i]).split(' '))[-1:]
                #item[j] = value[0]
            #else:
            try:
                item[j] = df[str(j)][i]
            except:
                continue
            # print(f"{j} --> ", df[str(j)][i])


        item['preco'] = preco
        item['frete'] = '3.60'
        item['liquidity'] = '10'
        item['imported'] = '1'
        try:
            item['Model #'] = str(item['Model #'])
        except:
            pass
        existe = 0

        for j in dados_banco:
            #print("Banco --> ", i)
            validar_produto = 0
            id,model,carrier,grade,capacity,description = j
            id_banco = id
            description = str(description).split(' ')
            description = ' '.join(description)
            #print("Desc Banco ==>" ,description)
            #print("Index ", dados_banco.index(j))
            #print("Desc Item ==> ", item["Item Description"])
            if str(carrier) ==  item["Carrier"]:
                validar_produto +=1
                #print("Carrier --> ", carrier)
            if str(capacity) == item["Capacity"]:
                validar_produto+=1
                #print("Capacity --> ", capacity)
            if str(grade) == item["Grade"]:
                validar_produto+=1
                #print("Grade --> ", grade)
            if  str(item["Item Description"]) in str(description):
                validar_produto+=1

            if validar_produto == 4:
                existe+=1


                break
        if existe == 0:
            print("Adicionando devices")
            db = heruko()
            add_manifest_valeus(db, item, data_)
            db.close()
            time.sleep(2)
            #print(" [ -- ]Ainda não existe ")
            #print(item)
            print("------------------------")
        else:
            list_action_devices['Qty'] = item['Qty']
            list_action_devices['lote'] = item['Lot #']
            list_action_devices['device_id'] = id_banco

            action_devices(mydb, list_action_devices, link)

            print("==========")
            print("Já existe")
            print("ID --> ", id_banco)
            existe += 1

            print(item)
            print("===========")
            time.sleep(5)
        # print(item)

        # time.sleep(2)
        values.append(item)
        clear_files_csv()

def add_manifest_valeus(db, values, date_):
    if str(values["Capacity"])  == 'nan':
        values["Capacity"] = ''
    print((values["Lot #"], values["Carrier"], values["Grade"], values["Capacity"],values["Item Description"],  values["preco"], values["frete"], values["liquidity"], values["imported"], date_))
    date_ = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    sql = ('INSERT INTO `db` (`model`, `carrier`, `grade`, `capacity`, `description`,`retail`, `freight`, `liquidity`, `imported`, `created_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    values = (str(values["Lot #"]), values["Carrier"], values["Grade"], values["Capacity"],values["Item Description"],  values["preco"], values["frete"], values["liquidity"], values["imported"], date_)
    cursor = db.cursor()
    cursor.execute(sql, values)
    db.commit()




def clear_files_csv():
    print("Limpado arquivos .csv")
    time.sleep(1)
    onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]
    for i in onlyfiles:
        if '.csv' in str(i):
            os.remove(i)
