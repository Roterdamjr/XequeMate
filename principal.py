import streamlit as st

from db_funcoes import fn_inserir_ordem,fn_buscar_todas,fn_buscar_venda_compras_vazia

todas_acoes, todas_opcoes = fn_buscar_todas()

col1, col2 = st.columns(2)
with col1:
    tipo_ativo = st.radio("Tipo de Ativo", ("Ação", "Opção"))
with col2:
    tipo_ordem = st.radio("Tipo de Ordem", ("Comprar", "Vender"))


col_ativo, col_quantidade, col_preco,col_strike  = st.columns(4)

ativo = ''

acoes_venda_vazia, opcoes_comra_vaiza = fn_buscar_venda_compras_vazia()
with col_ativo:
    # Lógica para exibir a caixa de texto ou listbox
    if tipo_ativo == "Ação" and tipo_ordem == "Comprar":
        ativo = st.text_input("Ativo")
    elif tipo_ativo == "Ação" and tipo_ordem == "Vender":
        resultados = acoes_venda_vazia
        lista = [item['ativo'] for item in resultados]
        ativo = st.selectbox("Ativos", lista)
    elif tipo_ativo == "Opção" and tipo_ordem == "Comprar":
        resultados = opcoes_comra_vaiza
        lista = [item['ativo'] for item in resultados]
        ativo = st.selectbox("Ativos", lista)
    else:
        ativo = st.text_input("Ativo")

with col_quantidade:
    quantidade = st.number_input("Qtd.", min_value=1, max_value=9999, step=1)

with col_preco:
    preco = st.number_input("Preço", min_value=0.01, max_value=9999.99, step=0.01)

with col_strike:
    if tipo_ativo == "Opção" and tipo_ordem == "Vender":
        strike = st.number_input("Strike", min_value=0.01, max_value=9999.99, step=0.01)


if tipo_ordem == "Comprar":
    button_color = "blue"
else:
    button_color = "red"

# botão com a cor definida
sigla_tipo_ordem = 'C' if tipo_ordem == "Comprar" else 'V'
sigla_tipo_ativo = 'A' if tipo_ativo == "Ação" else 'O'

if st.button(tipo_ordem,  help=None, on_click=None, disabled=False, key=None):
    if tipo_ativo == "Opção" and tipo_ordem == "Vender":
        retorno = fn_inserir_ordem(sigla_tipo_ativo, ativo ,sigla_tipo_ordem, quantidade, preco, strike)
    else:
        retorno = fn_inserir_ordem(sigla_tipo_ativo, ativo ,sigla_tipo_ordem, quantidade, preco)

    st.write( retorno['mensagem']) 
 
 ####################### grade ###################

if todas_acoes:
    import pandas as pd
    df = pd.DataFrame(todas_acoes)
    st.dataframe(df)
else:
    st.warning("Nenhuma ação registrada no momento.")

if todas_opcoes:
    import pandas as pd
    df = pd.DataFrame(todas_opcoes)
    st.dataframe(df)
else:
    st.warning("Nenhuma ação registrada no momento.")



################  Adiciona estilo CSS para alterar a cor do botão
st.markdown(f"""
    <style>
        div.stButton > button:first-child {{
            background-color: {button_color};
            color: white;
        }}
    </style>
""", unsafe_allow_html=True)
