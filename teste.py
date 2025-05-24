from  funcoes import fn_busca_mapa_precos_atuais,fn_popula_dados

df_precos = fn_busca_mapa_precos_atuais()

df_ativos = fn_popula_dados (df_precos)

print(df_ativos)