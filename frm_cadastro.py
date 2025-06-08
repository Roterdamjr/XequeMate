import streamlit as st
from db_funcoes import fn_ordem_acao_insert, fn_ordem_acao_update, fn_ordem_opcao_insert, fn_ordem_opcao_update, fn_buscar_todas,fn_buscar_venda_compras_vazia_tuplas,fn_buscar_venda_compras_vazia
import datetime
import pandas as pd
from funcoes import fn_busca_mapa_precos_atuais,fn_obter_strike
import numpy as np


def exibir_tela():
    todas_acoes, todas_opcoes = fn_buscar_todas()

    col1, col2 = st.columns(2)
    with col1:
        tipo_ativo = st.radio("Tipo de Ativo", ("Ação", "Opção"))
    with col2:
        tipo_ordem = st.radio("Tipo de Ordem", ("Comprar", "Vender"))


    col_data, col_ativo, col_quantidade, col_preco,col_strike, col_acao_pai  = st.columns(6)

    ativo = ''

    acoes_venda_vazia, opcoes_compra_vazia = fn_buscar_venda_compras_vazia()
    
    # popula dict 'mapa_nome_para_id' com id_ativo e nome das acoes ainda não vendidas
    tuplas_id_nome , _ = fn_buscar_venda_compras_vazia_tuplas()
    mapa_nome_para_id = {nome: id_ for id_, nome in tuplas_id_nome}


    with col_ativo:
        # Lógica para exibir a caixa de texto ou listbox
        if tipo_ativo == "Ação" and tipo_ordem == "Comprar":
            ativo = st.text_input("Ativo")
        elif tipo_ativo == "Ação" and tipo_ordem == "Vender":
            resultados = acoes_venda_vazia
            lista = [item['ativo'] for item in resultados]
            ativo = st.selectbox("Ativos", lista)
        elif tipo_ativo == "Opção" and tipo_ordem == "Comprar":
            resultados = opcoes_compra_vazia
            lista = [item['ativo'] for item in resultados]
            ativo = st.selectbox("Ativos", lista)
        else:
            ativo = st.text_input("Ativo")

    with col_data:
        hoje = datetime.date.today()
        hoje_formatada = hoje.strftime("%d/%m/%Y")
        data = st.text_input("Data", value=hoje_formatada)

    with col_quantidade:
        quantidade = st.number_input("Qtd", min_value=1, max_value=9999, step=1)

    with col_preco:
        preco = st.number_input("Preço", min_value=0.01, max_value=9999.99, step=0.01)

    with col_strike:
        if tipo_ativo == "Opção" and tipo_ordem == "Vender":
            strike = st.number_input("Strike", min_value=0.01, max_value=9999.99, step=0.01)

    with col_acao_pai:
        if tipo_ativo == "Opção" and tipo_ordem == "Vender":
            nome_selecionado = st.selectbox("Escolha a ação", list(mapa_nome_para_id.keys()))


    # botão com a cor definida
    if tipo_ordem == "Comprar":
        button_color = "blue"
    else:
        button_color = "red"


    sigla_tipo_ordem = 'C' if tipo_ordem == "Comprar" else 'V'
    sigla_tipo_ativo = 'A' if tipo_ativo == "Ação" else 'O'

    if st.button(tipo_ordem,  help=None, on_click=None, disabled=False, key=None):
        if tipo_ativo == "Ação" and tipo_ordem == "Comprar":
            retorno = fn_ordem_acao_insert(data, ativo , quantidade, preco)

        elif tipo_ativo == "Ação" and tipo_ordem == "Vender":
            acoes_sem_venda , _  = fn_buscar_venda_compras_vazia_tuplas()
            id_acao =[id for id, at in acoes_sem_venda if at == ativo][0]
            retorno = fn_ordem_acao_update(data,  preco, id_acao)
            st.write(id_acao)
            
        elif tipo_ativo == "Opção" and tipo_ordem == "Comprar":
            _ , opcoes_sem_compra  = fn_buscar_venda_compras_vazia_tuplas()
            id_ativo =[id for id, at in opcoes_sem_compra if at == ativo][0]
            retorno = fn_ordem_opcao_update(data, preco,id_ativo)

        else:
            _ , opcoes_sem_compra  = fn_buscar_venda_compras_vazia_tuplas()
            id_acao = mapa_nome_para_id[nome_selecionado]
            retorno = fn_ordem_opcao_insert (data, ativo, quantidade, preco, strike, id_acao)
            
        st.write(retorno['mensagem']) 

        #atualiza o Dataframe com preccos atuais
        st.session_state.df_precos = fn_busca_mapa_precos_atuais()
        st.write( 'atualizando precos') 
    exibe_grade()

    ################  Adiciona estilo CSS para alterar a cor do botão
    st.markdown(f"""
        <style>
            div.stButton > button:first-child {{
                background-color: {button_color};
                color: white;
            }}
        </style>
    """, unsafe_allow_html=True)

def exibe_grade():
    acoes, opcoes = fn_buscar_venda_compras_vazia()
    df_precos_atuais = st.session_state.df_precos

    if acoes:
        df = pd.DataFrame(acoes)
        
        df['strike'] = df['id_ativo'].apply(fn_obter_strike)

        # Faz o merge trazendo a coluna 'preco_ativo' do df_precos
        df = df.merge(
            df_precos_atuais[['ativo', 'preco_atual']], 
            on='ativo', 
            how='left')

        df['resultado'] = (df[['preco_atual', 'strike']].min(axis=1) - df['compra']) * df['quantidade']
        
        df['result_perc'] = round(100 * (df['preco_atual'] / df['compra'] - 1), 2)

        # Calcula os totais
        total_resultado = df['resultado'].sum()
        total_investido = (df['quantidade'] * df['compra']).sum()
        result_perc_total = round(100 * total_resultado / total_investido , 2)

        total_row = pd.DataFrame([{
            'data_compra' : np.nan,
            'data_venda': np.nan,
            'ativo': 'TOTAL',
            'quantidade': np.nan,
            'compra': np.nan,
            'preco_atual': np.nan,
            'resultado': total_resultado,     
            'result_perc': result_perc_total 
        }])
        
        df_total = pd.concat([df, total_row], ignore_index=True)
        df_total = df_total.drop(columns=['data_venda', 'id_ativo'])
        df['result_perc_str'] = df['result_perc'].astype(str) + '%'

        st.dataframe(df_total)
    else:
        st.warning("Nenhuma ação registrada no momento.")

    if opcoes:
        df_opcoes = pd.DataFrame(opcoes)
        df_opcoes = df_opcoes.drop(columns=['data_compra', 'id_acao'])
        st.dataframe(df_opcoes)
    else:
        st.warning("Nenhuma opção registrada no momento.")