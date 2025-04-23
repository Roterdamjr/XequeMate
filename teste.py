from db_funcoes import fn_inserir_ordem,fn_buscar_todas,fn_buscar_venda_compras_vazia
import datetime
import pandas as pd
from funcoes import fn_busca_mapa_precos_atuais,fn_busca_opcao_da_acao,fn_busca_ativo_pai


todas_acoes, todas_opcoes = fn_buscar_todas()
df_acoes = pd.DataFrame(todas_acoes)
df = df_acoes.loc[df_acoes['ativo'] == 'BBDC4'].iloc[0][0]


print((df))


