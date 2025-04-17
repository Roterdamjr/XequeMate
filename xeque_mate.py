import streamlit as st
from frm_cadastro import exibir_tela
from frm_historico import exibir_historico
import yfinance as yf
import pandas as pd
from db_funcoes import fn_buscar_todas

# ---------- Funções auxiliares ----------

def fn_buscar_preco_atual(ticker):
    try:
        ticker += '.SA'
        dados = yf.Ticker(ticker).history(period="1d")
        return round(dados['Close'].iloc[-1], 2) if not dados.empty else None
    except Exception as e:
        print(f"Erro ao buscar {ticker}: {e}")
        return None

def fn_busca_mapa_precos_atuais():
    todas_acoes, _ = fn_buscar_todas()
    df = pd.DataFrame(todas_acoes)
    df['preco_atual'] = df['ativo'].apply(fn_buscar_preco_atual)
    return df

# ---------- Inicialização (executa só uma vez) ----------
if 'df_precos' not in st.session_state:
    with st.spinner("Buscando preços atuais..."):
        st.session_state.df_precos = fn_busca_mapa_precos_atuais()

# ---------- Menu lateral ----------
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma tela:", ("Cadastro", "Histórico", "Analise", "Ranking"))

# ---------- Roteamento de telas ----------
if opcao == "Cadastro":
    exibir_tela()
elif opcao == "Histórico":
    exibir_historico()
elif opcao == "Analise":
    exibir_tela()
elif opcao == "Ranking":
    exibir_tela()
