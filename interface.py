import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np


def main():
    st.title("Pragmatis Consultoria - Squad Anaytics")
    foto = Image.open('logo_analytics.png')
    st.image(foto, caption='Squad Analytics', use_column_width=False)

    menu = ["Fligh Web Scraping", "Hotel Web Scraping"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Fligh Web Scraping":
        st.header("Fligh Web Scraping")
        st.write('Olá, seja bem vindo a nossa ferramenta de web scraping para passagens áreas, novas features estão sendo implementadas em caso de bugs reporte para para sergio.campos@pragmatis.com.br')

        st.write("Para essa análise é necessário que o arquivo de input dos dados possua o formato abaixo, fique atendo ao cabeçalho das colunas esses não devem ser alterados:")

        input_template = {
        'Cidade_Origem': ['São Paulo', 'Recife','Belém','Brasilia'],
        'Cidade_Destino': ['Rio de Janeiro', 'Brasilia', 'São Paulo', 'Curitiba'],
        'Data_Origem': ['2022-01-27','2022-01-27','2022-01-27','2022-01-27'],
        'Data_Destino':['2022-01-27','2022-01-27','2022-01-27','2022-01-27']}

        st.table(input_template)

        st.subheader('Configurações:')

        opções = st.radio("Sites:",(
            "'https://www.decolar.com/",
            "https://123milhas.com/",
            "https://www.google.com/flights" ) )

        st.write('Por favor insira abaixo abaixo o arquivo de input com as informações necessárias para busca, ele deve seguir o template indicado acima:')

        input = st.file_uploader("Insira o input (.xlsx)", type ='xlsx')

        if input:
            df = pd.read_excel(input)
            st.table(df)

        st.multiselect("Selecione o tipo de busca desejado:", ('Ida e volta', 'Só de ida'))
        st.write("Para realizar o scraping desejado basta clicar no botão abaixo e aguardar a busca ser realizada:")

        st.button("Scraping")

        st.subheader('Resultados:')

        df = pd.DataFrame(
            np.random.randn(15, 4),
            columns=('col_%d' % i for i in range(4))
        )
        # tabelas interativas
        st.table(df)

        st.line_chart(df)

        st.bar_chart(df)

        st.area_chart(df)


if __name__ == '__main__':
    main()