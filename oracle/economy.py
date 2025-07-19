import streamlit as st
import requests
import pandas as pd

def carregar_serie(codigo_serie):
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json'
    r = requests.get(url)

    try:
        dados = r.json()
        if isinstance(dados, list):

            df = pd.DataFrame(r.json())
            df['valor'] = df['valor'].astype(float)
            df['data'] = pd.to_datetime(df['data'], dayfirst=True)
            df = df.sort_values('data')
            return df
        else:
            st.error(f'Erro ao obter dados da API para a série {codigo_serie} Não está no formato esperado.')
            return pd.DataFrame()
    
    except Exception as e:
        st.error(f'Erro ao carrgar dados da série {codigo_serie}: {e}')
        return pd.DataFrame()
            

def mostrar_ipca():
    st.markdown('## 📊 IPCA - Inflação')
    dados = carregar_serie(433)

    meses = st.slider('Selecione quantos meses visualizar', 6, 36, 12)
    ultimos = dados.tail(meses)

    st.line_chart(ultimos.set_index('data')['valor'], height=300)

    atual = ultimos['valor'].iloc[-1]
    anterior = ultimos['valor'].iloc[-2]
    variacao = atual - anterior
    percentual = (variacao / anterior) * 100

    if atual > anterior:
        st.markdown(f'**🔼 Último IPCA:** :red[{atual:.2f}]')
        st.markdown(f'**📈 Variação mensal:** :red[{percentual:.2f}]')
    elif atual < anterior:
        st.markdown(f'**🔽 Último IPCA:** :green[{atual:.2f}]')
        st.markdown(f'**📉 Variação mensal:** :green[{percentual:.2f}]')
    else:
        st.markdown(f'**➖ Último IPCA:** {atual:.2f}')
        st.markdown(f'**📉 Variação mensal:** {percentual:.2f}')
        
    
    dados['ano'] = dados['data'].dt.year
    ipca_anual = dados.groupby('ano')['valor'].sum().reset_index()

    st.markdown('### 📊 IPCA acumulado por ano')
    st.bar_chart(ipca_anual.set_index('ano')['valor'])


    st.download_button(
        label='📥 Baixar dados do IPCA (.csv)',
        data=dados.to_csv(index=False),
        file_name='ipca.csv',
        mime='text/csv'
    )


def mostrar_selic():
    st.markdown('## 💰 Taxa SELIC')
    dados = carregar_serie(4189)
    if dados.empty:
        return
    ultimos = dados.tail(12)


    st.line_chart(ultimos.set_index('data')['valor'], height=300)

    atual = ultimos['valor'].iloc[-1]
    anterior = ultimos['valor'].iloc[-2]

    if atual > anterior:
        st.markdown(f'**🔼 Última SELIC:** :red[{atual:.2f}%]')
    elif atual < anterior:
        st.markdown(f'**🔽 Última SELIC:** :green[{atual:.2f}%]')
    else:
        st.markdown(f'**➖ Última SELIC:** {atual:.2f}%')

    st.download_button(
        label='📥 Baixar dados da SELIC (.csv)',
        data=dados.to_csv(index=False),
        file_name='selic.csv',
        mime='text/csv'
    )


def mostrar_pib():
    st.markdown('## 🧠 PIB Trimestral (Brasil)')
    dados = carregar_serie(7326)
    dados = dados[dados['data'].dt.year >= 2019]

    dados['trimestre'] = dados['data'].dt.to_period('Q').astype(str)
    pib_trim = dados.groupby('trimestre')['valor'].sum()

    st.bar_chart(pib_trim)

    atual = pib_trim.iloc[-1]
    anterior = pib_trim.iloc[-2]
    variacao = atual - anterior
    perc = (variacao / anterior) * 100

    if perc > 0:
        st.markdown(f'**📈 Variação PIB trimestral:** :green[{perc:.2f}%]')
    elif perc < 0:
        st.markdown(f'**📉 Variação PIB trimestral:** :red[{perc:.2f}%]')
    else:
        st.markdown(f'**➖ Variação PIB trimestral:** {perc:.2f}%')


    st.download_button(
        label='📥 Baixar dados do PIB (.csv)',
        data=dados.to_csv(index=False),
        file_name='pib.csv',
        mime='text/csv'
    )

def app():
    st.title('💰 Oráculo Econômico')
    tabs = st.tabs(['📌 IPCA', '📉 SELIC', '📊 PIB'])

    with tabs[0]:
        mostrar_ipca()

    with tabs[1]:
        mostrar_selic()

    with tabs[2]:
        mostrar_pib()