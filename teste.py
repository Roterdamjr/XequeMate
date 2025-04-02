


from tinydb import TinyDB, Query

def fn_buscar_venda_vazia_ou_ausente():
    db_acoes = TinyDB('acoes.json')
    tabela = db_acoes.table('_default')
    query = Query()
    consulta = (~query.has('venda')) | (query.venda == None)
    print("Consulta:", consulta) # mostre a consulta que sera executada
    print("tabela:", tabela.all()) # mostre todo o conteudo da tabela
    resultados = tabela.search(consulta)
    return resultados

ret = fn_buscar_venda_vazia_ou_ausente()

print(ret)