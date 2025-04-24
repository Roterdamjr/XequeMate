import streamlit as st
from funcoes import fn_obter_strike ,fn_busca_ativo_pai,fn_busca_mapa_precos_atuais
from db_funcoes import fn_buscar_todas,fn_buscar_venda_compras_vazia,fn_buscar_opcoes_por_id_acao
import pandas as pd

from tinydb import TinyDB,Query
from datetime import datetime


db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

def fn_buscar_todas():
    # retorna uma lista de dicionarios com todas acoes, incluido o campo id_ativo 
    # e uma lista de dicionarios com todas opoes
    lista_com_id  = [
            {**doc, "id_ativo": str(doc.doc_id)}  # ou sem str() se quiser manter como int
            for doc in db_acoes.all()
        ]
    return lista_com_id, db_opcoes.all()

def fn_buscar_venda_compras_vazia():
   acoes, opcoes = fn_buscar_todas()
  
   acoes_sem_venda = [acao for acao in acoes if acao.get("data_venda", "").strip() == ""]
   opcoes_sem_compra = [opcao for opcao in opcoes if opcao.get("data_compra", "").strip() == ""]
   return acoes_sem_venda,opcoes_sem_compra

acoes,opcoes = fn_buscar_venda_compras_vazia()
df = pd.DataFrame(acoes)
print(df)

