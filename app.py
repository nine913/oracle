import streamlit as st
from oracle import economy_app, finance_app, clima_app

def main():
    st.set_page_config(page_title='Oráculo',
                       layout='wide',
                       page_icon='🔮')
    st.title('🔮 Oráculo')
    st.markdown('### Um hub de insights financeiros, econômicos e climáticos em tempo real')

    menu = st.sidebar.selectbox(
        '🔍 Escolha o oráculo:',
        ['Oráculo Econômico', 'Oráculo Financeiro', 'Oráculo Climático']
    )

    if menu == 'Oráculo Econômico':
        economy_app()

    elif menu == 'Oráculo Financeiro':
        finance_app()

    elif menu == 'Oráculo Climático':
        clima_app()

if __name__ == '__main__':
    main()
