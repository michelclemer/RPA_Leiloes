from datetime import datetime

import mysql.connector

from apscheduler.schedulers.blocking import BlockingScheduler
def Heruko():
    mydb = mysql.connector.connect(
        host='',
        user='',
        password='',
        database='',
    )
    return mydb

mydb = Heruko()
cursor = mydb.cursor()

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
    if int(dia) < 10:
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

def my_job(text):
    print('AQUI')


sched = BlockingScheduler()
def running(cursor):
    cursor.execute("SELECT id, closure,link  FROM db")
    datas = cursor.fetchall()

    for i in datas:
        a = i[1]

        try:
            if a != None:
                args_date = format_data(a)
                print(args_date)
                sched.add_job(my_job, 'date', run_date=datetime(int(args_date[0]),int(args_date[1]),int(args_date[2]),int(args_date[3]),int(args_date[4]), 0), args=['text'])
                print(a)
        except:
            pass




running(cursor)
sched.start()

# The job will be executed on November 6th, 2009



