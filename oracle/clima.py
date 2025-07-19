import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')

def app():
    st.subheader('☁️ Oráculo do Clima')
    cidade = st.text_input('Informe a cidade:', value='Belém')

    if cidade:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric'
        response = requests.get(url)


        if response.status_code != 200:
            st.error('Cidade não encontrada.')
            return
        

        dados = response.json()
        descricao = dados['weather'][0]['description'].capitalize()
        temp = dados['main']['temp']
        umidade = dados['main']['humidity']

        st.write(f'🌡️ Temperatura: {temp}ºC')
        st.write(f'💧 Umidade: {umidade}%')
        st.write(f'🌤️ Descrição: {descricao}')