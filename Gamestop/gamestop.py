import os

import heruko as he
import json
import random
import time
from datetime import datetime
import mysql.connector
from fake_headers import Headers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
import requests
from bs4 import BeautifulSoup
import pandas as pd
desktop = []
mobile = []


class EARLY:
    def __init__(self, driver):

        # self.driver = driver
        self.driver = driver
        # driver = webdriver.Firefox()

        print("")

    def find_elem(self, locator, timeout=10):
        elem = WebDriverWait(self.driver, timeout).until(visibility_of_element_located(locator))
        return elem

    def run_find_click(self, locator):
        c = self.find_elem(locator)
        c.click()

    def run_find_write(self, locator, keys):
        self.find_elem(locator).clear()
        self.find_elem(locator).send_keys(keys)

    def get_value(self, locator):
        return self.find_elem(locator).get_attribute('href')

    def clear_field(self, locator):
        self.find_elem(locator).clear()

    def validar_url(self, url):
        if self.driver.current_url == url:
            print("url: ", url)
            return 1
        else:
            print("Url not : ", url)
            return 0




def download_manifest(driver, name):
    print("Fazendo download ", name)
    manifest = driver.find_element_by_id('manifest-download-btn-top')
    mani = str(manifest.get_attribute("onclick")).split("'")[1]
    with requests.get(mani, stream=True) as r:
        r.raise_for_status()
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)



def filter_iphone(driver):
    models = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for lis in models:
        if '?model=' in str(lis.get_attribute("href")):
            links.append(lis.get_attribute("href"))
    iphone_links = []
    for l in links:
        req = requests.get(l)
        soup = BeautifulSoup(req.content, 'lxml')
        for i in soup.find_all('a'):

            if 'iPhone' in str(i.text):
                iphone_links.append(l)
                print(l)
    res = []
    [res.append(x) for x in iphone_links if x not in res]

    return res

def save_json(name, data):
    f = open(str(name), 'w')
    f.write(json.dumps(data))
    f.close()
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
    dia, mes, ano = str(data).split('/')
    hora, min, seg = str(hora).split(':')
    data_formatado = f'{ano}-{mes}-{dia} {hora}:{min}:{seg}'
    return data_formatado


def gamestop():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=r"C:\Users\Admin\Documents\chrome\chromedriver.exe")


    site = EARLY(driver)
    url = 'https://auth.bstock.com/oauth2/authorize?client_id=1b094c5f-c8a6-416c-8c62-4dc77ca88ce9&redirect_uri=https%3A%2F%2Fbstock.com%2Fgamestop%2Fsso%2Findex%2Flogin%2F&scope=offline_access&response_type=code&state=isHome&mp_logo=https%3A%2F%2Fbstock.com%2Fgamestop%2Fskin%2Ffrontend%2Fbstock%2Fauction%2Fimages%2Flogo.png&site_abb=gam&_ga=2.166534142.1794073461.1627852184-598900122.1623332325'
    json_data = {}
    data_ = {}
    driver.get(url)
    site.run_find_write((By.ID, 'loginId'), '')
    site.run_find_write((By.ID, 'password'), '')
    site.run_find_click((By.XPATH, '/html/body/main/div[2]/div/form/button'))
    all_iphones = filter_iphone(driver)
    links_prods = []
    verifi_dupli = ''
    for iphone in all_iphones:
        driver.get(iphone)
        elems = driver.find_elements_by_xpath("//a[@href]")

        for elem in elems:
            if 'auction/auction/view' in str(elem.get_attribute("href")):
                links_prods.append(elem.get_attribute("href"))

    res = []
    [res.append(x) for x in links_prods if x not in res]
    print(res)

    for i in res:

        data_['link'] = str(i)
        driver.get(i)
        try:
            data_['frete'] = 30.00
            data_['rate'] = 0.00
            data_['limit_bid'] = None
            data_['status'] = 0
            data_['company_id'] = 1
            data_['created_at'] = None
            data_['delete_at'] = None
            data_['reason'] = None

            titulo = site.find_elem((By.XPATH, '//*[@id="top"]/body/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]'))

            data_['Nome'] = titulo.text
            preco_atual = site.find_elem(
                (By.XPATH, '//*[@id="top"]/body/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[6]/div[1]/div[2]'))
            data_['current_bid'] = str(str(preco_atual.text).replace('$', '')).replace(',', '.')
            data_['current_bid'] = float(data_['current_bid'])
            hora_fechamento = site.find_elem((By.XPATH, '//*[@id="auction_end_time"]'))
            dat = str(hora_fechamento.text)[4:]
            data_['created_at'] = str(format_data(dat))
            print(dat)
            data_['close_date'] = str(format_data(dat))
            data_['updated_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # json_data[res.index(i)] = data_
            download_manifest(driver,str(res.index(i))+".csv")
            print("---------")
            print("Acessando: ", i)
            mydb = heruko()
            cursor = mydb.cursor()
            if he.value_exist(mydb, data_['link']):

                print("[+] Atualizando no Banco de dados")
                he.update_table(mydb, data_['link'], data_['current_bid'])
                he.read_csv(mydb, data_['current_bid'], str(format_data(dat)),  str(res.index(i))+".csv", str(i))
                print("---------")
                continue

            print("[+]Adicionando novo produto")

            sql = (
                'INSERT INTO `db` (`name`, `link`, `freight`, `rate`, `current_bid`, `limit_bid`, `closure`, `reason`, `status`, `company_id`, `created_at`, `updated_at`, `deleted_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
            values = (
            data_['Nome'], data_['link'], data_['frete'], data_['rate'], data_['current_bid'], data_['limit_bid'],
            data_['close_date'], data_['reason'], data_['status'], data_['company_id'], data_['close_date'],
            data_['updated_at'], data_['delete_at'], )
            cursor.execute(sql, values)
            time.sleep(2)
            mydb.commit()
            mydb = heruko()
            he.read_csv(mydb, data_['current_bid'], str(format_data(dat)), str(res.index(i))+".csv", str(i))
        # values = (295,'michel','https://bstock.com/gamestop/auction/view/id/37925/',0.00,0.00,100.00,None,'2021-03-04 23:22:00',None,'0',1,'2021-03-04 23:22:48','2021-03-05 00:09:01','2021-03-05 00:09:01',)

        except Exception as a:
            print(a)
            print("[-] Dados não disponíveis. Link: ", i)

        data_ = {}
    return json_data
gamestop()