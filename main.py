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
import streamlit as st
from PIL import Image
import pandas as pd
import subprocess
import sys
from streamlit import cli as stcli


def scrap(dataframe_input):
    # 1. Funções de apoio -------------------------------------------------------------------------------------------------------
    def selectxpath(browser, xpath):  ##Recebe o browser e qual o xpath do elemento e retorna o elemento
        delay = 8  # seconds
        try:
            WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            print("Loading took too much time!")
        return browser.find_element_by_xpath(xpath)

    def selectDate(browser, date, date2, tipo):
        ##Abre a caixa com as datas
        searchElem = selectxpath(browser,
                                 '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/input')

        browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

        date = str(date)
        date = date[:10]



        ##Marca a caixa com a data escolhida
        date = datetime.strptime(date, '%Y-%m-%d')



        today = datetime.today().strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        deltaMonth = (date.year - today.year) * 12 + (date.month - today.month)

        if deltaMonth >= 1:
            k = 1
            while k < deltaMonth:
                k += 1
                # clica no next:
                searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')

                browser.execute_script("arguments[0].click();", searchElem)  # clica no botão para direita

                searchElem = selectxpath(browser,
                                         '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/input')
                browser.execute_script("arguments[0].click();", searchElem)  # abrea a caixa dnv

            # coloca a data:
            searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
                date.day) + ']/div')  # coloca a data
        else:
            searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(
                date.day) + ']/div')

        browser.execute_script("arguments[0].click();", searchElem)

        # volta
        if tipo ==1:
            date2 = str(date2)
            date2 = date2[:10]
            date2 = datetime.strptime(date2, '%Y-%m-%d')
            deltaMonth_2 = (date2.year - date.year) * 12 + (date2.month - date.month)

            searchElem = selectxpath(browser,
                                     '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div/input')
            browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

            if deltaMonth_2 >= 1:
                k = 1
                while k < deltaMonth_2:
                    k += 1
                    # clica no next:
                    searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')
                    time.sleep(1)
                    browser.execute_script("arguments[0].click();", searchElem)  # clica no botão para direita

                    searchElem = selectxpath(browser,
                                             '/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div/div/div/div/input')
                    browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

                searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
                    date2.day) + ']/div')  # coloca a data
            else:
                searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(
                    date2.day) + ']/div')
            browser.execute_script("arguments[0].click();", searchElem)

    # 2. Input dos dados / Interface-Gráfica------------------------------------------------------------------------------------------------

    #dados = pd.read_excel('test_dados.xlsx', header=0)
    input_dados = dataframe_input
    #print(dados)

    Saidas = list(input_dados['Cidade_Origem'])
    Destinos = list(input_dados['Cidade_Destino'])
    datasSaidas = list(input_dados['Data_Saida'])
    datasVoltas = list(input_dados['Data_Retorno'])
    tipos = list(input_dados['Tipo'])

    datasSaidas = pd.to_datetime(datasSaidas, format='%d/%m/%Y')
    datasVoltas = pd.to_datetime(datasVoltas, format='%d/%m/%Y')

    # listas para salvar informação
    aeroporto_in = []
    aeroporto_out = []
    preco_ = []
    id_list = []
    cidades_saida = []
    cidades_chegada = []
    hoje = []
    Passagens_por_busca = []
    id_unique = []

    browser1 = webdriver.Chrome('chromedriver.exe')
    for i in range(len(Saidas)):

        Saida = ' ' + Saidas[i]
        Destino = ' ' + Destinos[i]
        dataS = datasSaidas[i]
        dataV = datasVoltas[i]
        tipo = int(tipos[i])

        id = f'000{i}FPA '

        # 3. Abre o Browser (chrome versão 96)--------------------------------------------------------------------------------------
        # options = Options()
        # options.add_argument('--headless') apaga o navegador
        browser1.get('https://www.decolar.com/')
        browser1.delete_all_cookies()

        ida_e_volta = str(tipo)  # Quando é 2 faz só ida

        ##Marcar box só de ida
        searchElem1 = selectxpath(browser1, f'/html/body/div[4]/div/div/div/div/div[1]/div/span[{ida_e_volta}]/label/i')
        browser1.execute_script("arguments[0].click();", searchElem1)

        ##origem
        # acha elemnto
        searchElem1 = selectxpath(browser1,
                                  "/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/div/input")

        # clica
        browser1.execute_script("arguments[0].click();", searchElem1)
        # limpa elemento
        searchElem1.clear()
        time.sleep(1.5)
        searchElem1.clear()
        # Imprime busca
        searchElem1.send_keys(Saida)
        time.sleep(1)
        # Procura
        searchElem1.send_keys(Keys.ENTER)
        time.sleep(1)

        ##Destino
        # searchElem1 = selectxpath(browser1,                                  '/html/body/div[4]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div/input')
        searchElem1 = selectxpath(browser1,
                                  "/html/body/div[4]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div[2]/div/div/input")

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

        selectDate(browser1, dataS, dataV, tipo)

        ## Pesquisar
        searchElem1 = selectxpath(browser1, '/html/body/div[4]/div/div/div/div/div[2]/div[3]/button/em')
        browser1.execute_script("arguments[0].click();", searchElem1)

        ##Scrool
        time.sleep(4)
        browser1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

        # 5. Sopa Bonita ---------------------------------------------------------------------------------------------------------
        page_content = browser1.page_source

        site = BeautifulSoup(page_content, 'html.parser')
        passagens = site.find_all('div', {'class': 'cluster-container COMMON'})


        Passagens_por_busca.append(len(passagens))
        id_unique.append(id)


        for passagem in passagens:
            preco_passagem = passagem.find('span', attrs={'class': 'amount price-amount'})
            aeroporto = passagem.find_all('span', attrs={'class': 'airport route-info-item route-info-item-airport'})
            cidade_saida = passagem.find('span', attrs={'class': "city-departure route-info-item route-info-item-city-departure"})
            cidade_chegada = passagem.find('span',attrs={'class': "city-arrival route-info-item route-info-item-city-arrival"})
            id_list.append(id)
            aeroporto_in.append(aeroporto[0].text)
            aeroporto_out.append(aeroporto[1].text)
            preco_.append(float(preco_passagem.text.replace('.', '')))
            # link_list.append(link['href']) não usado por enquanto
            cidades_saida.append(cidade_saida.text)
            cidades_chegada.append(cidade_chegada.text)
            hoje.append(datetime.today().strftime('%Y-%m-%d'))

    # 5. Output ---------------------------------------------------------------------------------------------------------
    browser1.close()
    dados_voos = {'id': id_list, 'Cidade_saida': cidades_saida, 'Cidade_Chegada': cidades_chegada,
                  'Aeroporto_chegada': aeroporto_in, 'aeroporto_saida': aeroporto_out, 'Preco_Passagem': preco_,
                  'Data_Pesquisa': hoje}
    dados_frame_resultados = pd.DataFrame(dados_voos)

    dict_quantidade_passagens = {'ID': id_unique, 'Quantidade de Passagens Encontradas': Passagens_por_busca}

    data_frame_qnt_passagens = pd.DataFrame(dict_quantidade_passagens)

    #print(dados_frame)
    #dados_frame.to_excel('output.xlsx', index=False)
    return dados_frame_resultados, data_frame_qnt_passagens

def scrap_hoteis(data_frame_input):
    # 1. Funções de apoio -------------------------------------------------------------------------------------------------------
    def selectxpath(browser, xpath):  ##Recebe o browser e qual o xpath do elemento e retorna o elemento
        delay = 8  # seconds
        try:
            WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            print("Loading took too much time!")
        return browser.find_element_by_xpath(xpath)

    def selectDate(browser, date, date2):
        ##Abre a caixa com as datas
        searchElem = selectxpath(browser,
                                 '/html/body/div[4]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/input')

        browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

        date = str(date)
        date = date[:10]
        date2 = str(date2)
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
                # clica no next:
                searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')

                browser.execute_script("arguments[0].click();", searchElem)  # clica no botão para direita

                searchElem = selectxpath(browser,
                                         '/html/body/div[4]/div/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/input')

                browser.execute_script("arguments[0].click();", searchElem)  # abrea a caixa dnv

            # coloca a data:
            searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
                date.day) + ']/div')  # coloca a data
        else:
            searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(
                date.day) + ']/div')
        browser.execute_script("arguments[0].click();", searchElem)

        # volta

        deltaMonth_2 = (date2.year - date.year) * 12 + (date2.month - date.month)

        searchElem = selectxpath(browser,
                                 '/html/body/div[4]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/input')
        browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

        if deltaMonth_2 >= 1:
            k = 1
            while k < deltaMonth_2:
                k += 1
                # clica no next:
                searchElem = selectxpath(browser, '/html/body/div[6]/div[1]/div[1]/div[2]/a[2]')
                time.sleep(1)
                browser.execute_script("arguments[0].click();", searchElem)  # clica no botão para direita

                searchElem = selectxpath(browser,
                                         '/html/body/div[4]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div/div/input')
                browser.execute_script("arguments[0].click();", searchElem)  # Abrir a caixa

            searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[2]/div[3]/div[' + str(
                date2.day) + ']/div')  # coloca a data
        else:
            searchElem = selectxpath(browser, 'html/body/div[6]/div[1]/div[1]/div[2]/div[1]/div[3]/div[' + str(
                date2.day) + ']/div')
        browser.execute_script("arguments[0].click();", searchElem)

    # 2. Input dos dados-----------------------------------------------------------------------------------------------

    dados = data_frame_input
    print(dados)

    Cidades_destinos = list(dados['Cidade_Destino'])
    Datas_Check_in = list(dados['Data_Checkin'])
    Datas_Check_out = list(dados['Data_Checkout'])

    Datas_Check_in = pd.to_datetime(Datas_Check_in, format='%d/%m/%Y')
    Datas_Check_out = pd.to_datetime(Datas_Check_out, format='%d/%m/%Y')

    # Listas para salvar informações relevantes:

    Hotel_name = []
    Hotel_price = []
    Hotel_distance_from_center = []
    Hotel_link = []
    Hotel_number_reviews = []
    Hotel_score = []
    id_list = []
    hoje = []
    # Quantidade de Pesquisas
    quantidade_pesquisas = range(len(Cidades_destinos))

    for i in quantidade_pesquisas:
        browser1 = webdriver.Chrome('chromedriver.exe')

        Cidade_destino = ' ' + Cidades_destinos[i]
        Data_Check_in = Datas_Check_in[i]
        Data_Check_out = Datas_Check_out[i]

        id = id = f'000{i}FPA '

        # 3 Interação com o Browser----------------------------------------------------------------------------------

        browser1.get('https://www.decolar.com/hoteis/')
        browser1.delete_all_cookies()
        # 3.1 Clica para buscar apenas hoteis: aparentemente isso aparece umas vezes outras não
        # searchElem1 = selectxpath(browser1,'/html/body/div[4]/div/div/div[1]/div/div/div[1]/div[3]/div/div/div[2]')
        # browser1.execute_script("arguments[0].click();", searchElem1)
        # 3.2. Insere a cidade de destino:
        searchElem1 = selectxpath(browser1, '/html/body/div[4]/div/div/div[1]/div/div/div[2]/div[1]/div/div/div/input')
        browser1.execute_script("arguments[0].click();", searchElem1)
        searchElem1.clear()
        time.sleep(1)
        searchElem1.clear()
        searchElem1.send_keys(Cidade_destino)
        time.sleep(1)
        # Procura
        searchElem1.send_keys(Keys.ENTER)
        time.sleep(1)

        # 3.3. Insere as datas:

        selectDate(browser1, Data_Check_in, Data_Check_out)

        # 3.4. Clica no botão de buscar
        searchElem1 = selectxpath(browser1, '/html/body/div[4]/div/div/div[1]/div/div/div[2]/button/em')
        browser1.execute_script("arguments[0].click();", searchElem1)

        # 4.  sopa bonita-----------------------------------------------------------------------------------------------------------

        page_content = browser1.page_source
        site = BeautifulSoup(page_content, 'html.parser')

        # 4.1 Interage pelas telas pegando os dados:
        pages = 2
        for page in range(pages):
            time.sleep(2)
            browser1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            page_content = browser1.page_source
            site = BeautifulSoup(page_content, 'html.parser')

            hoteis = site.find_all('div', {'class': "cluster-container -eva-3-shadow-line"})

            for hotel in hoteis:
                Hotel_name.append(hotel.find('span', {'class': 'accommodation-name -eva-3-ellipsis'}))
                Hotel_price.append(hotel.find('span', {'class': 'main-value'}))
                Hotel_distance_from_center.append(hotel.find('span', {'class': '-eva-3-tc-gray-2'}))
                Hotel_link.append(hotel.find('a'))
                id_list.append(id)
                hoje.append(datetime.today().strftime('%Y-%m-%d'))

                # Hotel_number_reviews.append(hoteis.find('span', {'class': 'accommodation-name -eva-3-ellipsis'}))
                # Hotel_score.append(hoteis.find('span', {'class': 'accommodation-name -eva-3-ellipsis'}))

            searchElem1 = selectxpath(browser1,
                                      '/html/body/aloha-app-root/aloha-results/div/div/div/div[2]/div[2]/aloha-list-view-container/div[5]/aloha-paginator-container/aloha-paginator/div/ul/li[5]/a')
            browser1.execute_script("arguments[0].click();", searchElem1)

    # 5. Output ---------------------------------------------------------------------------------------------------------
    browser1.close()

    print(len(id_list), len(Hotel_name), len(Hotel_price), len(Hotel_distance_from_center))
    dados_hoteis = {'id': id_list, 'Hotel_name': Hotel_name, 'Hotel_price': Hotel_price,
                    'Hotel_distance_from_center': Hotel_distance_from_center}
    dados_frame = pd.DataFrame(dados_hoteis)
    #print(dados_frame)
    #to_excel('output.xlsx', index=False)

    return dados_frame

def main():
    st.title("Pragmatis Consultoria - Squad Anaytics")
    foto = Image.open('logo_analytics.png')
    st.image(foto, caption='Squad Analytics', use_column_width=False)

    menu = ["Fligh - Web Scraping", "Hotel - Web Scraping"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Fligh - Web Scraping":
        st.header("Fligh Web Scraping")
        st.write('Olá, seja bem vindo a nossa ferramenta de web scraping para passagens áreas, novas features estão sendo implementadas em caso de bugs reporte para: sergio.campos@pragmatis.com.br')

        st.write("Para essa análise é necessário que o arquivo de input dos dados possua o formato abaixo, a coluna tipo indica se será de ida e volta (1) ou apenas de ida (2, fique atento ao cabeçalho das colunas esses não devem ser alterados:")

        input_template = {
        'Cidade_Origem': ['São Paulo', 'Recife','Belém','Brasilia'],
        'Cidade_Destino': ['Rio de Janeiro', 'Brasilia', 'São Paulo', 'Curitiba'],
        'Data_Origem': ['2022-01-27','2022-01-27','2022-01-27','2022-01-27'],
        'Data_Destino':['2022-01-27','2022-01-27','2022-01-27','2022-01-27'],
        'Tipo':[1,1,1,2]
        }

        st.table(input_template)

        st.subheader('Configurações:')

        opções = st.radio("Sites:",(
            "'https://www.decolar.com/",
            "[Não disponível]https://123milhas.com/",))

        st.write('Por favor insira abaixo abaixo o arquivo de input com as informações necessárias para busca, ele deve seguir o template indicado acima:')

        input = st.file_uploader("Insira o input (.xlsx)", type ='xlsx')

        if input:
            df = pd.read_excel(input)
            st.table(df)


        st.write("Para realizar o scraping desejado, basta clicar no botão abaixo e aguardar a busca ser realizada:")

        go_scrap = st.button("Scraping")

        if go_scrap:
            df_result, df_qtd_passagens = scrap(df)

            st.subheader('Resultados:')


            st.write("Quantidade de passagens encontradas por busca:")

            st.table(df_qtd_passagens)

            st.write("Resultados obtidos no web scraping:")

            st.table(df_result)

            st.download_button(label = "Download CSV", data = df_result.to_csv(), mime = 'text/csv')

    if choice == "Hotel - Web Scraping":
        st.header("Hotel Web Scraping")
        st.write('Olá, seja bem vindo a nossa ferramenta de web scraping para hoteis, novas features estão sendo implementadas em caso de bugs reporte para: sergio.campos@pragmatis.com.br')

        st.write("Para essa análise é necessário que o arquivo de input dos dados possua o formato abaixo, fique atento ao cabeçalho das colunas, esses não devem ser alterados:")

        input_template = {
        'Cidade_Origem': ['São Paulo', 'Recife','Belém','Brasilia'],
        'Data_Checkin': ['Rio de Janeiro', 'Brasilia', 'São Paulo', 'Curitiba'],
        'Data_Checkout': ['2022-01-27','2022-01-27','2022-01-27','2022-01-27'],
        }

        st.table(input_template)

        st.subheader('Configurações:')

        opções = st.radio("Sites:",(
            "'https://www.decolar.com/",
            "[Não disponível]https://123milhas.com/",
            "[Não disponível]https://www.google.com/flights" ) )

        st.write('Por favor insira abaixo abaixo o arquivo de input com as informações necessárias para busca, ele deve seguir o template indicado acima:')

        input = st.file_uploader("Insira o input (.xlsx)", type ='xlsx')

        if input:
            df = pd.read_excel(input)
            st.table(df)


        st.write("Para realizar o scraping desejado, basta clicar no botão abaixo e aguardar a busca ser realizada:")

        go_scrap = st.button("Scraping")

        if go_scrap:
            df_result = scrap_hoteis(df)

            st.subheader('Resultados:')

            st.write("Resultados obtidos no web scraping:")

            st.table(df_result)

            st.download_button(label = "Download CSV", data = df_result.to_csv(), mime = 'text/csv')


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())


