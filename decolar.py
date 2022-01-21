from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time


#1. Funções de apoio -------------------------------------------------------------------------------------------------------
def selectxpath(browser, xpath):  ##Recebe o browser e qual o xpath do elemento e retorna o elemento
    delay = 8  # seconds
    try:
        WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        print("Loading took too much time!")
    return browser.find_element_by_xpath(xpath)

def selectDate(browser, date,date2):
    ##Abre a caixa com as datas
    searchElem = selectxpath(browser,'/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/input')


    browser.execute_script("arguments[0].click();", searchElem) # Abrir a caixa

    date = str(date)
    date = date[:10]
    date2= str(date2)
    date2 = date2[:10]


    ##Marca a caixa com a data escolhida
    date = datetime.strptime(date, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')

    today = datetime.today().strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    deltaMonth = (date.year - today.year) * 12 + (date.month - today.month)


    if deltaMonth >= 1:
        k = 1
        while k < deltaMonth:
            k += 1
        #clica no next:
            searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')

            browser.execute_script("arguments[0].click();", searchElem) # clica no botão para direita

            searchElem = selectxpath(browser,
                                     '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/input')
            browser.execute_script("arguments[0].click();", searchElem)  # abrea a caixa dnv

        #coloca a data:
        searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
            date.day) + ']/div') #coloca a data
    else:
        searchElem = selectxpath(browser,'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(date.day) + ']/div')
    browser.execute_script("arguments[0].click();", searchElem)

    # volta

    deltaMonth_2 = (date2.year - date.year) * 12 + (date2.month - date.month)

    searchElem = selectxpath(browser,'/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div/input')
    browser.execute_script("arguments[0].click();", searchElem) # Abrir a caixa

    if deltaMonth_2 >= 1:
        k = 1
        while k < deltaMonth_2:
            k += 1
        #clica no next:
            searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')
            time.sleep(1)
            browser.execute_script("arguments[0].click();", searchElem) # clica no botão para direita

            searchElem = selectxpath(browser,
                                     '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div/input')
            browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

        searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
            date2.day) + ']/div') #coloca a data
    else:
        searchElem = selectxpath(browser,'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(date2.day) + ']/div')
    browser.execute_script("arguments[0].click();", searchElem)

#2. Input dos dados / Interface-Gráfica------------------------------------------------------------------------------------------------

dados = pd.read_excel('test_dados.xlsx', header=0)
print(dados)

Saidas = list(dados['Cidade_Origem'])
Destinos = list(dados['Cidade_Destino'])
datasSaidas = list(dados['Data_Saída'])
datasVoltas = list(dados['Data_Retorno'])

datasSaidas = pd.to_datetime(datasSaidas, format='%d/%m/%Y')
datasVoltas = pd.to_datetime(datasVoltas, format='%d/%m/%Y')

#listas para salvar informação
aeroporto_in = []
aeroporto_out = []
preco_ = []
id_list = []
link_list = []
cidades_saida = []
cidades_chegada = []
hoje = []

browser1 = webdriver.Chrome('chromedriver.exe')
for i in range(len(Saidas)):

    Saida = ' ' + Saidas[i]
    Destino = ' ' + Destinos[i]
    #dataS = ['2022-01-25']
    #datav = ['2022-01-27']
    dataS = datasSaidas[i]
    dataV = datasVoltas[i]

    id = f'000{i}FPA '

    #3. Abre o Browser (chrome versão 96)--------------------------------------------------------------------------------------
    #options = Options()
    #options.add_argument('--headless') apaga o navegador
    browser1.get('https://www.decolar.com/')
    browser1.delete_all_cookies()

    ida_e_volta = '1' #Quando é 2 faz só ida

    ##Marcar box só de ida
    searchElem1 = selectxpath(browser1,f'/html/body/div[4]/div/div/div/div/div[1]/div/span[{ida_e_volta}]/label/i')
    browser1.execute_script("arguments[0].click();", searchElem1)

    ##origem
    #acha elemnto
    searchElem1 = selectxpath(browser1,"/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/input")

    #clica
    browser1.execute_script("arguments[0].click();", searchElem1)
    # limpa elemento
    searchElem1.clear()
    time.sleep(1.5)
    searchElem1.clear()
    #Imprime busca
    searchElem1.send_keys(Saida)
    time.sleep(1)
    #Procura
    searchElem1.send_keys(Keys.ENTER)
    time.sleep(1)

    ##Destino
    #searchElem1 = selectxpath(browser1,                                  '/html/body/div[4]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div/input')
    searchElem1 = selectxpath(browser1,"/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div/input")

    # clica
    browser1.execute_script("arguments[0].click();", searchElem1)
    # limpa elemento
    searchElem1.clear()
    time.sleep(1.5)
    searchElem1.clear()
    # Imprime busca
    searchElem1.send_keys(Destino)
    time.sleep(1)
    # Procura
    searchElem1.send_keys(Keys.ENTER)
    time.sleep(1)

    ##data de ida#########################
    selectDate(browser1, dataS, dataV)

    ## Pesquisar
    searchElem1 = selectxpath(browser1, '/html/body/div[4]/div/div/div/div/div[2]/div[3]/button/em')
    browser1.execute_script("arguments[0].click();", searchElem1)

    ##Scrool
    time.sleep(3)
    browser1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

    #5. Sopa Bonita ---------------------------------------------------------------------------------------------------------
    page_content = browser1.page_source

    site = BeautifulSoup(page_content, 'html.parser')
    #print(site.prettify())
    passagens = site.find_all('div', {'class':'cluster-container COMMON'})
    print(len(passagens))

    for passagem in passagens:
        #aeroporto_chegada = passagem.find('h2', attrs={'class': 'ui-search-item__title'})
        #aeroporto_saida = passagem.find('span', attrs={'class': 'popup-airport'})

        preco_passagem = passagem.find('span', attrs={'class': 'amount price-amount'})
        aeroporto = passagem.find_all('span', attrs={'class':'airport route-info-item route-info-item-airport'})
        #link = passagem.find('a', attrs={'class': '-md eva-3-btn -primary'})
        cidade_saida = passagem.find('span', attrs = {'class': "city-departure route-info-item route-info-item-city-departure"})
        cidade_chegada = passagem.find('span', attrs = {'class':"city-arrival route-info-item route-info-item-city-arrival"})

        id_list.append(tag)
        aeroporto_in.append(aeroporto[0].text)
        aeroporto_out.append(aeroporto[1].text)
        preco_.append(float(preco_passagem.text.replace('.','')))
        #link_list.append(link['href']) não usado por enquanto
        cidades_saida.append(cidade_saida.text)
        cidades_chegada.append(cidade_chegada.text)
        hoje.append(datetime.today().strftime('%Y-%m-%d'))

#?5. Output ---------------------------------------------------------------------------------------------------------
browser1.close()
dados_voos = {'id': id_list,'Cidade_saida':cidades_saida, 'Cidade_Chegada':cidades_chegada, 'Aeroporto_chegada': aeroporto_in, 'aeroporto_saida': aeroporto_out, 'Preco_Passagem': preco_, 'Data_Pesquisa': hoje}
dados_frame = pd.DataFrame(dados_voos)
print(dados_frame)
dados_frame.to_excel('output.xlsx', index=False)

