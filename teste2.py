
from db_funcoes import fn_buscar_venda_compras_vazia
from tinydb import TinyDB,Query
import streamlit as st

db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')


def fn_buscar_venda_compras_vazia_tuplas():
    #retorna tuplas (id,ativo)
    acoes_sem_venda = [
        (doc.doc_id, doc['ativo']) 
        for doc in db_acoes.all() 
        if not doc.get('data_venda')
    ]
    opcoes_sem_compra = [
        (doc.doc_id, doc['ativo']) 
        for doc in db_opcoes.all() 
        if not doc.get('compra')
    ]
    return acoes_sem_venda, opcoes_sem_compra

tuplas_id_nome , _ = fn_buscar_venda_compras_vazia_tuplas()
mapa_nome_para_id = {nome: id_ for id_, nome in tuplas_id_nome}



# Exibe só os nomes na interface
nome_selecionado = st.selectbox("Escolha a ação", list(mapa_nome_para_id.keys()))

if st.button("Confirmar seleção"):
    id_selecionado = mapa_nome_para_id[nome_selecionado]
    st.write(f"Ação selecionada: {nome_selecionado} (ID: {id_selecionado})")