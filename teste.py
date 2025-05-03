import streamlit as st
from funcoes import fn_obter_strike ,fn_busca_ativo_pai,fn_busca_mapa_precos_atuais,fn_popula_dados
from db_funcoes import fn_buscar_todas,fn_buscar_venda_compras_vazia,fn_buscar_opcoes_por_id_acao
import pandas as pd
import numpy as np
from tinydb import TinyDB,Query
from datetime import datetime


db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

df_precos_atuais = df_precos = fn_busca_mapa_precos_atuais()

df_ativos = fn_popula_dados (df_precos_atuais)

df_ativos['resultado'] = pd.to_numeric(df_ativos['resultado'], errors='coerce')
totalizadores = df_ativos.groupby(['id_ativo'], as_index=False)['resultado'].sum()

# Adiciona uma coluna para indicar que é total
totalizadores['tipo'] = 'Total'
df_ativos['tipo'] = 'Detalhe'

df_total = pd.concat([df_ativos, totalizadores], ignore_index=True)

df_total = df_total.sort_values(by=['id_ativo', 'tipo'], ascending=[True, True])
df_total = df_total.drop(columns=['tipo'])




print(df_total)