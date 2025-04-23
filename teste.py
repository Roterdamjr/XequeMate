import streamlit as st
from funcoes import obter_strike ,fn_busca_ativo_pai,fn_busca_mapa_precos_atuais
from db_funcoes import fn_buscar_todas
import pandas as pd
from datetime import datetime
from tinydb import TinyDB,Query
from datetime import datetime

db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

def fn_busca_opcoes_da_acao(id_acao):
    query = Query()
    return db_opcoes.search(query.id_acao == id_acao)


print( fn_busca_opcoes_da_acao(1))
