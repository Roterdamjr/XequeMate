import streamlit as st
from db_funcoes import fn_inserir_ordem_acao,fn_buscar_todas
import pandas as pd

def exibir_historico():
    todas_acoes, todas_opcoes = fn_buscar_todas()
    df_precos_atuais = st.session_state.df_precos

    if todas_acoes:
        df = pd.DataFrame(todas_acoes)

        df = df.merge(
            df_precos_atuais[['ativo', 'preco_atual']], 
            on='ativo', 
            how='left')

        df['resultado'] = df['venda'] - df['compra']
        
        st.dataframe(df)
    else:
        st.warning("Nenhuma ação registrada no momento.")

    if todas_opcoes:
        df = pd.DataFrame(todas_opcoes)
        df['resultado'] = df['venda'] - df['compra']
        st.dataframe(df)
    else:
        st.warning("Nenhuma ação registrada no momento.")