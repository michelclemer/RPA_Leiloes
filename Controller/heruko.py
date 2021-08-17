from datetime import datetime

import mysql.connector


def heruko():
    mydb = mysql.connector.connect(
        host='',
        user='',
        password='',
        database='',
    )
    return mydb
mydb = heruko()
#cursor = mydb.cursor()


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
        print(data)
        if len(data) > 0:
            return 0
        else:
            return 1





# exists

def update_table(db, link, current_bid):

    #    INSERT INTO leila (id, nome, link, preco) VALUES ('2', 'Apple iPhone 12, Verizon - 40 Units - A/B Condition - Dallas, TX', 'https://bstock.com/gamestop/auction/auction/view/id/38746/', '13.55')
    #UPDATE leila SET preco = '2000' WHERE link='https://bstock.com/gamestop/auction/auction/view/id/38746/';
    data = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    create_movies_table_query = "UPDATE db SET updated_at=%s,current_bid=%s WHERE link=%s"

    values = (data , current_bid ,str(link))
    cursor = db.cursor()
    cursor.execute(create_movies_table_query, values)

def add_column(db, col):
    sqlq = f"ALTER TABLE db ADD {col} VARCHAR(255)"
    with db.cursor() as cursor:
        cursor.execute(sqlq)
        db.commit()

