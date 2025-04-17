
from tinydb import TinyDB,Query

db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

def apaga_banco():
    db_acoes.truncate()
    db_opcoes.truncate()

def fn_buscar_venda_compras_vazia():
    acoes = db_acoes.all()
    opcoes = db_opcoes.all()
    return [r for r in acoes if 'venda' not in r], [r for r in opcoes if 'compra' not in r]

def fn_buscar_todas():
    return db_acoes.all(),db_opcoes.all()
  
    
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

def fn_inserir_ordem(data, tipo_ativo, ativo, tipo_ordem, quantidade, preco, strike=0):

    query = Query()

    resultado_validacao = fn_validacao(tipo_ativo, ativo, tipo_ordem)

    if  not resultado_validacao['valido']:
        return {'mensagem': resultado_validacao['mensagem']}

    if (tipo_ativo == 'A') and tipo_ordem == 'C':
        print('inserindo')
        db_acoes.insert({
            'data_compra' : data,
            'data_venda' : '',
            'ativo': ativo,
            'quantidade': quantidade,
            'compra': preco
        })

    elif (tipo_ativo == 'A') and tipo_ordem == 'V':
        db_acoes.update({'venda': preco, 'data_venda': data}, query.ativo == ativo)
 

    elif (tipo_ativo == 'O') and tipo_ordem == 'C':
        db_opcoes.update({'compra': preco, 'data_compra': data}, query.ativo == ativo)

    elif (tipo_ativo == 'O') and tipo_ordem == 'V':
        db_opcoes.insert({
            'data_compra' : '' ,
            'data_venda' : data,
            'ativo': ativo,
            'quantidade': quantidade,
            'venda': preco,
            'strike' : strike
        })

    return {'valido': True, 'mensagem': resultado_validacao['mensagem']}
    



