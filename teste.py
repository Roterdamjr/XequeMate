import streamlit as st
from funcoes import fn_obter_strike ,fn_busca_ativo_pai,fn_busca_mapa_precos_atuais
from db_funcoes import fn_buscar_todas,fn_buscar_venda_compras_vazia,fn_buscar_opcoes_por_id_acao
import pandas as pd

from tinydb import TinyDB,Query
from datetime import datetime

db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

def fn_buscar_opcoes_por_id_acao(id_acao: str):
    # retorna uma lista de dicionarios
    opcoes = db_opcoes.all()
    return [op for op in opcoes if op.get('id_acao') == id_acao]

def fn_obter_strike(id_ativo):
    opcoes = fn_buscar_opcoes_por_id_acao(id_ativo)
    if not opcoes:
        return None
    # traz a opcao mais recente
    opcoes.sort(key=lambda x: datetime.strptime(x['data_venda'], '%d/%m/%Y'), reverse=True)
    return opcoes[0]['strike']  

df = pd.DataFrame(db_acoes)
df['strike'] = df['ativo'].apply(fn_obter_strike)

# Faz o merge trazendo apenas a coluna 'preco_ativo' do df_precos
df = df.merge(
    df_precos_atuais[['ativo', 'preco_atual']], 
    on='ativo', 
    how='left')

print( fn_obter_strike('1'))

