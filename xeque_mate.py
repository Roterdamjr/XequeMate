
import streamlit as st
from frm_cadastro import exibir_tela
from frm_listar_todas import listar_todas

st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma tela:", ("Cadastro", "ListarTodas", "Analise","Ranking"))

if opcao == "Cadastro":
    exibir_tela()
elif opcao == "ListarTodas":
    listar_todas()
elif opcao == "Analise":
    exibir_tela()
elif opcao == "Ranking":
    exibir_tela()
