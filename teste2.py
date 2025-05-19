
def fn_ordem_acao_insert_test(data, ativo,  quantidade, preco):
        print('insert -> ', 
              ' data_compra: ' , data,
            ' data_venda: ' , '',
            ' ativo:' , ativo,
            ' quantidade: ' , quantidade,
            ' compra:' , preco)

def fn_ordem_acao_update_test(data, preco,id_acao):
        print('update-> ', 
              ' venda:' , preco, 
              ' data_venda:', data,
              ' id_acao:', id_acao)
 

def fn_ordem_opcao_insert_test(data, ativo, quantidade, preco, strike, id_acao):

        print('insert -> ',
            ' data_compra:' , '' ,
            ' data_venda:' , data,
            ' ativo:', ativo,
            ' quantidade:', quantidade,
            ' venda:', preco,
            ' strike:', strike,
            ' id_acao:' , id_acao
        )

    
def fn_ordem_opcao_update_test(data, preco,  id_ativo):
    print('update-> ',
          ' compra:', preco, 
          ' data_compra: ', data , 
          ' id_ativo:', id_ativo)