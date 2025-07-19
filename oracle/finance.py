import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

@st.cache_data(show_spinner=False)
def get_data(symbol):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY,
        'datatype': 'json',
        'outputsize': 'compact'
    }

    resposta = requests.get(url, params=params)

    if resposta.status_code != 200:
        raise Exception('Erro ao obter dados')
    

    dados = resposta.json()
    

    if 'Time Series (Daily)' not in dados:
        raise Exception('Simbolo inválido')

    df = pd.DataFrame.from_dict(dados['Time Series (Daily)'], orient='index')
    df = df.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    })

    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df = df.sort_index()

    return df

def app():
    st.subheader('💹 Oráculo Financeiro')
    st.write('Informe o código do ativo. Para ações brasileiras, adicione `.SA` (ex: PETR4.SA).')
    symbol_input = st.text_area('Código dos ativos:', value='PETR4.SA, VALE.SA')


    if symbol_input:
        try:

            symbols = [s.strip().upper() for s in symbol_input.split(',') if s.strip()]
            
            for symbol in symbols:
                st.divider()
                st.markdown(f'## 📈 {symbol}')
                df = get_data(symbol)

                ultimo = df['Close'].iloc[-1]
                primeiro = df['Close'].iloc[0]
                total_perf = (ultimo / primeiro - 1)


                if ultimo > 0:
                    st.markdown(f"**🔼 Preço atual:** :green[{ultimo:.2f}]")
                elif ultimo < 0:
                    st.markdown(f"**🔽 Preço atual:** :red[{ultimo:.2f}]")
                else:
                    st.markdown(f"**➖ Preço atual:** {ultimo:.2f}")


                if total_perf > 0:
                    st.markdown(f"**🔼 Retorno nos últimos dias:** :green[{total_perf:.2%}]")
                elif total_perf < 0:
                    st.markdown(f"**🔽 Retorno nos últimos dias:** :red[{total_perf:.2%}]")
                else:
                    st.markdown(f"**➖ Retorno nos últimos dias:** {total_perf:.2%}")

                st.markdown(f'### 📊 Histórico de preços')
                st.line_chart(df["Close"], height=250, use_container_width=True)

                st.markdown(f'### 📊 Histórico de volumes')
                st.bar_chart(df["Volume"], height=250, use_container_width=True)

        except Exception as e:
            st.error(f'Erro: {e}')