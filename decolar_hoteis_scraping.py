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
    searchElem = selectxpath(browser,'/html/body/div[4]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/input')

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

            searchElem = selectxpath(browser,'/html/body/div[4]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/input')

            browser.execute_script("arguments[0].click();", searchElem)  # abrea a caixa dnv

        #coloca a data:
        searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
            date.day) + ']/div') #coloca a data
    else:
        searchElem = selectxpath(browser,'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(date.day) + ']/div')
    browser.execute_script("arguments[0].click();", searchElem)

    # volta

    deltaMonth_2 = (date2.year - date.year) * 12 + (date2.month - date.month)

    searchElem = selectxpath(browser,'/html/body/div[4]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/input')
    browser.execute_script("arguments[0].click();", searchElem) # Abrir a caixa

    if deltaMonth_2 >= 1:
        k = 1
        while k < deltaMonth_2:
            k += 1
        #clica no next:
            searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')
            time.sleep(1)
            browser.execute_script("arguments[0].click();", searchElem) # clica no botão para direita

            searchElem = selectxpath(browser,'/html/body/div[4]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/input')
            browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

        searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
            date2.day) + ']/div') #coloca a data
    else:
        searchElem = selectxpath(browser,'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(date2.day) + ']/div')
    browser.execute_script("arguments[0].click();", searchElem)



#2. Input dos dados-----------------------------------------------------------------------------------------------

dados = pd.read_excel('input_hoteis.xlsx', header=0)
print(dados)

Cidades_destinos = list(dados['Cidade_Destino'])
Datas_Check_in = list(dados['Data_Checkin'])
Datas_Check_out = list(dados['Data_Checkout'])

Datas_Check_in = pd.to_datetime(Datas_Check_in, format='%d/%m/%Y')
Datas_Check_out = pd.to_datetime(Datas_Check_out, format='%d/%m/%Y')

#Listas para salvar informações relevantes:

Hotel_name = []
Hotel_price = []
Hotel_distance_from_center = []
Hotel_link = []
Hotel_number_reviews = []
Hotel_score = []
id_list = []
hoje = []
#Quantidade de Pesquisas
quantidade_pesquisas = range(len(Cidades_destinos))



for i in quantidade_pesquisas:
    browser1 = webdriver.Chrome('chromedriver.exe')

    Cidade_destino = ' ' + Cidades_destinos[i]
    Data_Check_in = Datas_Check_in[i]
    Data_Check_out = Datas_Check_out[i]

    id = id = f'000{i}FPA '

#3 Interação com o Browser----------------------------------------------------------------------------------

    browser1.get('https://www.decolar.com/hoteis/')
    browser1.delete_all_cookies()
    #3.1 Clica para buscar apenas hoteis: aparentemente isso aparece umas vezes outras não
    #searchElem1 = selectxpath(browser1,'/html/body/div[4]/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[2]')
    #browser1.execute_script("arguments[0].click();", searchElem1)
    #3.2. Insere a cidade de destino:
    searchElem1 = selectxpath(browser1,'/html/body/div[4]/div/div/div[1]/div/div/div[2]/div[1]/div/div/div/input')
    browser1.execute_script("arguments[0].click();", searchElem1)
    searchElem1.clear()
    time.sleep(1)
    searchElem1.clear()
    searchElem1.send_keys(Cidade_destino)
    time.sleep(1)
    # Procura
    searchElem1.send_keys(Keys.ENTER)
    time.sleep(1)

    #3.3. Insere as datas:

    selectDate(browser1, Data_Check_in, Data_Check_out)

    #3.4. Clica no botão de buscar
    searchElem1 = selectxpath(browser1, '/html/body/div[4]/div/div/div[1]/div/div/div[2]/button/em')
    browser1.execute_script("arguments[0].click();", searchElem1)


#4.  sopa bonita-----------------------------------------------------------------------------------------------------------

    page_content = browser1.page_source
    site = BeautifulSoup(page_content, 'html.parser')

    #4.1 Interage pelas telas pegando os dados:
    pages = 2
    for page in range(pages):
        time.sleep(2)
        browser1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        page_content = browser1.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        hoteis = site.find_all('div',{'class':"cluster-container -eva-3-shadow-line"})

        for hotel in hoteis:
            Hotel_name.append(hotel.find('span', {'class': 'accommodation-name -eva-3-ellipsis'}))
            Hotel_price.append(hotel.find('span', {'class': 'main-value'}))
            Hotel_distance_from_center.append(hotel.find('span', {'class': '-eva-3-tc-gray-2'}))
            Hotel_link.append(hotel.find('a'))
            id_list.append(id)
            hoje.append(datetime.today().strftime('%Y-%m-%d'))

            #Hotel_number_reviews.append(hoteis.find('span', {'class': 'accommodation-name -eva-3-ellipsis'}))
            #Hotel_score.append(hoteis.find('span', {'class': 'accommodation-name -eva-3-ellipsis'}))


        searchElem1 = selectxpath(browser1, '/html/body/aloha-app-root/aloha-results/div/div/div/div[2]/div[2]/aloha-list-view-container/div[5]/aloha-paginator-container/aloha-paginator/div/ul/li[5]/a')
        browser1.execute_script("arguments[0].click();", searchElem1)

#5. Output ---------------------------------------------------------------------------------------------------------
browser1.close()

print(len(id_list), len(Hotel_name), len(Hotel_price), len(Hotel_distance_from_center))
dados_hoteis = {'id': id_list,'Hotel_name':Hotel_name, 'Hotel_price':Hotel_price, 'Hotel_distance_from_center': Hotel_distance_from_center}
dados_frame = pd.DataFrame(dados_hoteis)
print(dados_frame)
dados_frame.to_excel('output.xlsx', index=False)



"""
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




"""
