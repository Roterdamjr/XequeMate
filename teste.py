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

df_acoes = pd.DataFrame(todas_acoes)
df_acoes = df_acoes[['id_ativo','data_compra',  'data_venda',  'ativo','quantidade','compra','venda']]


df_opcoes = pd.DataFrame(todas_opcoes)
df_opcoes = df_opcoes.rename(columns={'id_acao': 'id_ativo'})
df_opcoes=df_opcoes[['id_ativo','data_compra',  'data_venda',  'ativo','quantidade','compra','venda','strike']]


df_ativos = pd.concat([df_acoes , df_opcoes], ignore_index=True)

print(df_ativos)