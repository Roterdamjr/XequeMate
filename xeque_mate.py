import streamlit as st
from frm_cadastro import exibir_tela
from frm_historico import exibir_historico
from frm_desempenho import exibir_desempenho
import yfinance as yf

from funcoes import fn_busca_mapa_precos_atuais


st.set_page_config(
    page_title="Controle de Ordens",
    layout="wide"  # <- isso aqui é o que ativa a tela cheia
)

# ---------- Inicialização (executa só uma vez) ----------
if 'df_precos' not in st.session_state:
    with st.spinner("Buscando preços atuais..."):
        st.session_state.df_precos = fn_busca_mapa_precos_atuais()
       
# ---------- Menu lateral ----------
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma tela:", ("Cadastro", "Histórico", "Desempenho", "Ranking"))

# ---------- Roteamento de telas ----------
if opcao == "Cadastro":
    exibir_tela()
elif opcao == "Histórico":
    exibir_historico()
elif opcao == "Desempenho":
    exibir_desempenho()
elif opcao == "Ranking":
    exibir_tela()
