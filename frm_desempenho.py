import streamlit as st
from funcoes import fn_obter_strike ,fn_busca_ativo_pai
from db_funcoes import fn_buscar_todas
import pandas as pd
from datetime import datetime

def exibir_desempenho():

    df_precos_atuais = st.session_state.df_precos
    todas_acoes, todas_opcoes = fn_buscar_todas()

    if todas_acoes:
        df_acoes = pd.DataFrame(todas_acoes)
        
        # obtem strike
        df_acoes['strike'] = df_acoes['ativo'].apply(obter_strike)

        df_acoes = df_acoes.merge(
            df_precos_atuais[['ativo', 'preco_atual']], 
            on='ativo', 
            how='left')

        df_acoes['resultado'] = (df_acoes[['preco_atual', 'strike']].min(axis=1) - df_acoes['compra']) * df_acoes['quantidade']

    if todas_opcoes:
        df_opcoes = pd.DataFrame(todas_opcoes)
        df_opcoes['resultado'] = df_opcoes['venda'] * df_opcoes['quantidade']

    df_total = pd.concat([df_acoes , df_opcoes], ignore_index=True)

    df_total['ativo_pai'] = df_total['ativo'].apply(lambda x: fn_busca_ativo_pai(x)['ativo'])

    df_total['dt_compra_pai'] = df_total['ativo'].apply(lambda x: fn_busca_ativo_pai(x)['data_compra'])
    #convertte pra data
    df_total['dt_compra_pai'] = df_total['dt_compra_pai'] .apply(lambda x : datetime.strptime(x, "%d/%m/%Y"))
    
    df_total = df_total.sort_values(['dt_compra_pai', 'ativo'])
    df_total = df_total.drop(columns=['ativo_pai', 'dt_compra_pai'])
    
    st.dataframe(df_total)
