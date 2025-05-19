from db_funcoes import fn_buscar_venda_compras_vazia_tuplas 
from teste2 import fn_ordem_acao_insert_test, fn_ordem_acao_update_test, fn_ordem_opcao_insert_test, fn_ordem_opcao_update_test

ativo, tipo_ativo ,tipo_ordem,data,quantidade,preco, strike  = 'SLCE3', "Ação","Vender", '02/06/2025',100, 18.71, 20.01

tuplas_id_nome , _ = fn_buscar_venda_compras_vazia_tuplas()
mapa_nome_para_id = {nome: id_ for id_, nome in tuplas_id_nome}

nome_selecionado = 'ALOS3'

if tipo_ativo == "Ação" and tipo_ordem == "Comprar":
    retorno = fn_ordem_acao_insert_test(data, ativo , quantidade, preco)

elif tipo_ativo == "Ação" and tipo_ordem == "Vender":
    acoes_sem_venda , _  = fn_buscar_venda_compras_vazia_tuplas()
    id_acao =[id for id, at in acoes_sem_venda if at == ativo][0]
    retorno = fn_ordem_acao_update_test(data,  preco, id_acao)


elif tipo_ativo == "Opção" and tipo_ordem == "Comprar":
    _ , opcoes_sem_compra  = fn_buscar_venda_compras_vazia_tuplas()
    id_ativo =[id for id, at in opcoes_sem_compra if at == ativo][0]
    retorno = fn_ordem_opcao_update_test (data, preco,id_ativo)

else:
    _ , opcoes_sem_compra  = fn_buscar_venda_compras_vazia_tuplas()
    id_acao = mapa_nome_para_id[nome_selecionado]
    retorno = fn_ordem_opcao_insert_test (data, ativo, quantidade, preco, strike, id_acao)
