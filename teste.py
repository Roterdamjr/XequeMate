import streamlit as st
from funcoes import obter_strike ,fn_busca_ativo_pai,fn_busca_mapa_precos_atuais
from db_funcoes import fn_buscar_todas,fn_busca_acao_nao_vendida_da_opcao
import pandas as pd
from datetime import datetime

from datetime import datetime

id_acao = fn_busca_acao_nao_vendida_da_opcao("VULCD123").doc_id

print(id_acao)

