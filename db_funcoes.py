from tinydb import TinyDB,Query

db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

def apaga_banco():
    db_acoes.truncate()
    db_opcoes.truncate()

def fn_buscar_venda_compras_vazia():
    #retorna duas listas de dicionario
    acoes = db_acoes.all()
    opcoes = db_opcoes.all()
    return [r for r in acoes if 'venda' not in r], [r for r in opcoes if 'compra' not in r]

def fn_buscar_venda_compras_vazia_tuplas():
    #retorna tuplas (id,ativo)
    acoes_sem_venda = [
        (doc.doc_id, doc['ativo']) 
        for doc in db_acoes.all() 
        if not doc.get('data_venda')
    ]
    opcoes_sem_compra = [
        (doc.doc_id, doc['ativo']) 
        for doc in db_opcoes.all() 
        if not doc.get('compra')
    ]
    return acoes_sem_venda, opcoes_sem_compra

def fn_buscar_todas():
    return db_acoes.all(),db_opcoes.all()
  
def fn_buscar_opcoes_por_id_acao(id_acao: str):
    # retorna uma lista de dicionarios
    opcoes = db_opcoes.all()
    return [op for op in opcoes if op.get('id_acao') == id_acao]

def fn_buscar_acao_por_id_opcao(id_opcao):
    # retorna a acao no formato tinydb.table.Document
    opcao = db_opcoes.get(doc_id=int(id_opcao))
    if not opcao or "id_acao" not in opcao:
        return None
    
    id_acao = opcao["id_acao"]
    return db_acoes.get(doc_id=int(id_acao))

def fn_validacao(tipo_ativo, ativo, tipo_ordem):
    query = Query()
    msg= ''

    if (tipo_ativo == 'A') and tipo_ordem == 'C':
        resultados = db_acoes.search(query.ativo == ativo)

        # se existe reg e venda vazio -> erro
        if bool(resultados):
            registro = resultados[-1] #pega ultima ocorrencia
            if registro.get('venda') is None or registro.get('venda') == '':
                return {'valido': False, 'mensagem': 'Esta ação já foi comprada.'}

    if (tipo_ativo == 'A') and tipo_ordem == 'V':
        resultados = db_acoes.search(query.ativo == ativo)

        # se não existe reg  -> erro
        if not bool(resultados):        
            return {'valido': False, 'mensagem': 'Esta ação não foi vendida.'}

         #  se existe reg e venda não vazio -> erro
        if bool(resultados):
            registro = resultados[-1] #pega ultima ocorrencia
            if registro.get('venda') is not None:
                return {'valido': False, 'mensagem': 'Esta ação já foi vendida.Compra:'+ str(registro.get('venda'))}

    if (tipo_ativo == 'O') and tipo_ordem == 'C':
        resultados = db_opcoes.search(query.ativo == ativo)

        # se não existe reg  -> erro
        if not bool(resultados):        
            return {'valido': False, 'mensagem': 'Esta opção não foi vendida.'}
        #  se existe reg e compra não vazio -> erro
        if bool(resultados):
            registro = resultados[-1] #pega ultima ocorrencia
            if registro.get('compra') is not None:
                return {'valido': False, 'mensagem': 'Esta opção já foi recomprada'}


    if (tipo_ativo == 'O') and tipo_ordem == 'V':
        resultados = db_opcoes.search(query.ativo == ativo)
        # se existe reg  -> erro
        if bool(resultados):        
            return {'valido': False, 'mensagem': 'Esta opção já foi vendida.'}

    return {'valido': True,'mensagem': 'Registro lançado!'}

def fn_inserir_ordem_acao(data, ativo, tipo_ordem, quantidade, preco):

    query = Query()
    resultado_validacao = fn_validacao('A', ativo, tipo_ordem)

    if  not resultado_validacao['valido']:
        return {'mensagem': resultado_validacao['mensagem']}

    if tipo_ordem == 'C':
        print('inserindo')
        db_acoes.insert({
            'data_compra' : data,
            'data_venda' : '',
            'ativo': ativo,
            'quantidade': quantidade,
            'compra': preco
        })
    else:
        db_acoes.update({'venda': preco, 'data_venda': data}, query.ativo == ativo)
 
    return {'valido': True, 'mensagem': resultado_validacao['mensagem']}

def fn_inserir_ordem_opcao(data, ativo, tipo_ordem, quantidade, preco, strike, id_acao):
    
    query = Query()
    resultado_validacao = fn_validacao('O', ativo, tipo_ordem)

    if  not resultado_validacao['valido']:
        return {'mensagem': resultado_validacao['mensagem']}

    if tipo_ordem == 'C':
        db_opcoes.update({'compra': preco, 'data_compra': data}, query.ativo == ativo)
    else:
        db_opcoes.insert({
            'data_compra' : '' ,
            'data_venda' : data,
            'ativo': ativo,
            'quantidade': quantidade,
            'venda': preco,
            'strike' : strike,
            'id_acao': id_acao
        })
        
    return {'valido': True, 'mensagem': resultado_validacao['mensagem']}