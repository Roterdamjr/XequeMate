import streamlit as st
from funcoes import fn_obter_strike ,fn_busca_ativo_pai
from db_funcoes import fn_buscar_todas
import pandas as pd
from datetime import datetime
import numpy as np

def exibir_desempenho():

    df_precos_atuais = st.session_state.df_precos
    todas_acoes, todas_opcoes = fn_buscar_todas()

    if todas_acoes:
        df_acoes = pd.DataFrame(todas_acoes)
        df_acoes = df_acoes[['id_ativo','data_compra',  'data_venda',  'ativo','quantidade','compra','venda']]
        
        # obtem strike
        df_acoes['strike'] = df_acoes['id_ativo'].apply(fn_obter_strike)
 
        df_acoes = df_acoes.merge(
            df_precos_atuais[['ativo', 'preco_atual']], 
            on='ativo', 
            how='left')
        
        # acrescenta coluna "reulstados"
        # se acao ja foi vendida resultado = venda -compra
        # senão, resultado =  menor valor entre strike e preço atual - compra
        df_acoes['resultado'] = np.where(
            df_acoes['venda'].notna(),  # Se já houve venda
            (df_acoes['venda'] - df_acoes['compra']) * df_acoes['quantidade'],
            (df_acoes[['preco_atual', 'strike']].min(axis=1) - df_acoes['compra']) * df_acoes['quantidade']
            )

    if todas_opcoes:
        df_opcoes = pd.DataFrame(todas_opcoes)
        df_opcoes = df_opcoes.rename(columns={'id_acao': 'id_ativo'})
        df_opcoes=df_opcoes[['id_ativo','data_compra',  'data_venda',  'ativo','quantidade','compra','venda','strike']]

        # preenche com zeros campos vazios
        df_opcoes['compra'] = pd.to_numeric(df_opcoes['compra'], errors='coerce').fillna(0.0)

        # acrescenta coluna "reulstados"
        df_opcoes['resultado'] = (df_opcoes['venda'] - df_opcoes['compra']) * df_opcoes['quantidade']

    df_ativos = pd.concat([df_acoes , df_opcoes], ignore_index=True)

    df_ativos['ativo_pai'] = df_ativos['ativo'].apply(lambda x: fn_busca_ativo_pai(x)['ativo'])

    df_ativos['dt_compra_pai'] = df_ativos['ativo'].apply(lambda x: fn_busca_ativo_pai(x)['data_compra'])
#    df_ativos['dt_compra_pai'] = df_ativos['dt_compra_pai'] .apply(lambda x : datetime.strptime(x, "%d/%m/%Y")) #convertte pra data
    df_ativos['dt_compra_pai'] = pd.to_datetime(df_ativos['dt_compra_pai'], format="%d/%m/%Y")

    
    df_ativos = df_ativos.sort_values(['dt_compra_pai', 'id_ativo'])
    df_ativos = df_ativos.drop(columns=['dt_compra_pai', 'ativo_pai'])

 
    st.dataframe(df_ativos)
