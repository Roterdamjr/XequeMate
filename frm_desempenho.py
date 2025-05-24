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

    # popula df_ativos_vendidas e df_ativos_nao_vendidos
    acoes_vendidas = df_total[(df_total["tipo_ativo"] == "acao") & (df_total["venda"].notna())]
    ids_ativos_vendidos = acoes_vendidas["id_ativo"].unique()
    df_ativos_vendidos = df_total[df_total["id_ativo"].isin(ids_ativos_vendidos)]
    df_ativos_nao_vendidos = df_total[~df_total["id_ativo"].isin(ids_ativos_vendidos)]

    df_total = fn_ajusta_df(df_total)
    df_ativos_vendidos = fn_ajusta_df(df_ativos_vendidos)
    df_ativos_nao_vendidos = fn_ajusta_df(df_ativos_nao_vendidos)

   # st.dataframe(df_total)
    st.dataframe(df_ativos_vendidos)
    st.dataframe(df_ativos_nao_vendidos)

def fn_ajusta_df(df):
    df = df.sort_values(by=['id_ativo', 'tipo'], ascending=[True, True])
    df = df.drop(columns=['tipo','id_ativo','data_compra','data_venda'])

    #substituir valores ausentes (NaN) por strings vazias ('')
    colunas = ['ativo','quantidade','compra','venda','strike','preco_atual']
    df[colunas] = df[colunas].fillna('')
    return df
