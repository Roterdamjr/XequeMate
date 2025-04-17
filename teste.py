from db_funcoes import fn_inserir_ordem,fn_buscar_todas,fn_buscar_venda_compras_vazia
import datetime
import pandas as pd
from funcoes import fn_busca_mapa_precos_atuais,fn_busca_opcao_da_acao
 
acoes, opcoes = fn_buscar_venda_compras_vazia()
df = pd.DataFrame(acoes)

df_precos_atuais = fn_busca_mapa_precos_atuais()
df_merge = df.merge(
    df_precos_atuais[['ativo', 'preco_atual']], 
    on='ativo', 
    how='left')

#print(df)
print(df_merge)