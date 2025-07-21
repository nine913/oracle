import requests
import streamlit as st
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

try:
    API_KEY = st.secrets('OPENWEATHER_API_KEY')
except:
    load_dotenv()
    API_KEY = os.getenv('OPENWEATHER_API_KEY')

def app():
    st.subheader('🌦️ Oráculo do Clima')
    cidade = st.text_input('Informe o nome da cidade:', value='Belém')

    if not cidade:
        return
    
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    res = requests.get(url)

    if res.status_code != 200:
        st.error('Erro: Cidade não encontrada')
        return
    
    dados = res.json()
    lista = []

    for item in dados['list']:
        dt = datetime.fromtimestamp(item['dt'])
        temp = item['main']['temp']
        temp_min = item['main']['temp_min']
        temp_max = item['main']['temp_max']
        descricao = item['weather'][0]['description'].capitalize()
        umidade = item['main']['humidity']
        vento = item['wind']['speed']
        direcao = item['wind'].get('deg', 0)

        lista.append({
            'data': dt,
            'temperatura': temp,
            'Temperatura miníma': temp_min,
            'Temperatura máxima': temp_max,
            'umidade': umidade,
            'descricao': descricao,
            'vento (m/s)': vento,
            'direção do vento (°)': direcao
        })

    df = pd.DataFrame(lista)
    df['data'] = pd.to_datetime(df['data'])
    df.set_index('data', inplace=True)

    hoje = df.index[0].date()
    df_hoje = df[df.index.date == hoje]
    df_proximos = df[df.index.date > hoje]

    st.markdown('## 📍 Hoje')
    if not df_hoje.empty:
        clima_atual = df_hoje.iloc[0]

        temp_atual = clima_atual["temperatura"]
        temp_max = df_hoje["Temperatura máxima"].max()
        temp_min = df_hoje["Temperatura miníma"].min()
        descricao = clima_atual["descricao"]
        umidade = clima_atual["umidade"]
        vento = clima_atual["vento (m/s)"]
        direcao = clima_atual["direção do vento (°)"]

        st.write(f'☁️ {descricao}')
        st.markdown(f'🌡️ Temperatura atual: :green[{temp_atual:.1f}ºC] | 🔼 Máx: :red[{temp_max:.1f}ºC] | 🔽 Mín: :blue[{temp_min:.1f}ºC]')
        st.markdown(f'💧 Umidade: :blue[{umidade}%]')
        st.write(f'💨 Vento: {vento:.1f} m/s | Direção: {direcao:.0f}º')


        st.markdown('### 📈 Temperatura por hora (hoje)')
        st.line_chart(df_hoje['temperatura'])

    else:
        st.warning('Sem dados climáticos para hoje.')
        
    st.markdown('## 📅 Previsão para os próximos dias')

    previsao_dia = df_proximos.resample('D').agg({
        'temperatura': 'mean',
        'Temperatura miníma': 'min',
        'Temperatura máxima': 'max',
        'descricao': 'first',
        'vento (m/s)': 'mean',
        'direção do vento (°)': 'mean'
    }).head(5)

    for dia, row in previsao_dia.iterrows():
        st.write(f'📆 {dia.strftime('%d/%m/%Y')}')
        st.write(f'☁️ {row["descricao"]}')
        st.markdown(f'🌡️ Média: :green[{row['temperatura']:.1f}ºC] | 🔼 Máx: :red[{row['Temperatura máxima']:.1f}ºC] | 🔽 Mín: :blue[{row['Temperatura miníma']:.1f}ºC]')
        st.markdown(f'💨 Vento: {row['vento (m/s)']:.1f} m/s | Direção: {row['direção do vento (°)']:.0f}°')
        st.divider()

    st.markdown('### 📈 Gráfico de Temperaturas Diárias')
    st.line_chart(previsao_dia[['Temperatura miníma', 'temperatura', 'Temperatura máxima']])

    st.markdown('### 🕒 Previsão Horária de Temperatura (próximas 24h)')
    st.line_chart(df['temperatura'].head(24))