from  funcoes import fn_busca_mapa_precos_atuais,fn_popula_dados
import pandas as pd

df_precos = fn_busca_mapa_precos_atuais()
df_ativos = fn_popula_dados (df_precos)


df_ativos['resultado'] = pd.to_numeric(df_ativos['resultado'], errors='coerce')
totalizadores = df_ativos.groupby(['id_ativo'], as_index=False)['resultado'].sum()

# Adiciona uma coluna para indicar que é total
totalizadores['tipo'] = 'Total'
df_ativos['tipo'] = 'Detalhe'

df_total = pd.concat([df_ativos, totalizadores], ignore_index=True)

# popula df_ativos_vendidas e df_ativos_nao_vendidos
acoes_vendidas = df_total[(df_total["tipo_ativo"] == "acao") & (df_total["venda"].notna())]
ids_ativos_vendidos = acoes_vendidas["id_ativo"].unique()
df_ativos_vendidos = df_total[df_total["id_ativo"].isin(ids_ativos_vendidos)]
df_ativos_nao_vendidos = df_total[~df_total["id_ativo"].isin(ids_ativos_vendidos)]

df_ativos_nao_vendidos['resultado']



soma = df_ativos_nao_vendidos[df_ativos_nao_vendidos['tipo'] == 'Detalhe']['resultado'].sum()
print(soma)

print(soma)



