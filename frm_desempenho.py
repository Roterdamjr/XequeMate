import streamlit as st
from funcoes import fn_popula_dados



def exibir_desempenho():

    df_ativos = fn_popula_dados (st.session_state.df_precos)
 
    st.dataframe(df_ativos)
