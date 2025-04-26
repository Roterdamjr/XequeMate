import streamlit as st
from funcoes import fn_obter_strike ,fn_busca_ativo_pai,fn_busca_mapa_precos_atuais
from db_funcoes import fn_buscar_todas,fn_buscar_venda_compras_vazia,fn_buscar_opcoes_por_id_acao
import pandas as pd
import numpy as np
from tinydb import TinyDB,Query
from datetime import datetime


db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

df_precos_atuais = df_precos = fn_busca_mapa_precos_atuais()
todas_acoes, todas_opcoes = fn_buscar_todas()

if todas_acoes:
    df_acoes = pd.DataFrame(todas_acoes)
    
    # obtem strike
    df_acoes['strike'] = df_acoes['id_ativo'].apply(fn_obter_strike)

    df_acoes = df_acoes.merge(
        df_precos_atuais[['ativo', 'preco_atual']], 
        on='ativo', 
        how='left')

    df_acoes['resultado'] = (df_acoes[['preco_atual', 'strike']].min(axis=1) - df_acoes['compra']) * df_acoes['quantidade']


    # Suponho que exista a coluna 'venda' (preço da venda) no df
    df_acoes['resultado'] = np.where(
        df_acoes['venda'].notna(),  # Se já houve venda
        (df_acoes['venda'] - df_acoes['compra']) * df_acoes['quantidade'],
        (df_acoes[['preco_atual', 'strike']].min(axis=1) - df_acoes['compra']) * df_acoes['quantidade']
    )

print(df_acoes)