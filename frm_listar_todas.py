import streamlit as st
from db_funcoes import fn_inserir_ordem,fn_buscar_todas,fn_buscar_venda_compras_vazia

def listar_todas():
    todas_acoes, todas_opcoes = fn_buscar_todas()

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