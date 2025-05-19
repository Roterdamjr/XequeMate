import streamlit as st
from funcoes import fn_popula_dados
import pandas as pd

    
def exibir_desempenho():

    df_ativos = fn_popula_dados (st.session_state.df_precos)
 
    df_ativos['resultado'] = pd.to_numeric(df_ativos['resultado'], errors='coerce')
    totalizadores = df_ativos.groupby(['id_ativo'], as_index=False)['resultado'].sum()
 
    # Adiciona uma coluna para indicar que é total
    totalizadores['tipo'] = 'Total'
    df_ativos['tipo'] = 'Detalhe'

    df_total = pd.concat([df_ativos, totalizadores], ignore_index=True)

    df_total = df_total.sort_values(by=['id_ativo', 'tipo'], ascending=[True, True])
    df_total = df_total.drop(columns=['tipo','id_ativo','data_compra','data_venda'])

    colunas = ['ativo','quantidade','compra','venda','strike','preco_atual']
    df_total[colunas] = df_total[colunas].fillna('')

    
    st.dataframe(df_total)
