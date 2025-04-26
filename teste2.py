
from db_funcoes import fn_buscar_venda_compras_vazia,fn_buscar_opcoes_por_id_acao
from funcoes import fn_obter_strike
from tinydb import TinyDB,Query
import streamlit as st



db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

op = fn_obter_strike('15')
print(op)
