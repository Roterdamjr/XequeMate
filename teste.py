

from tinydb import TinyDB, Query

db_acoes = TinyDB('acoes.json')
db_opcoes  = TinyDB('opcoes.json')

def fn_buscar_venda_compras_vazia():
    acoes = db_acoes.all()
    opcoes = db_opcoes.all()
    return [r for r in acoes if 'venda' not in r], [r for r in opcoes if 'compra' not in r]


acoes,opcoes = fn_buscar_venda_compras_vazia()
lista = [item['ativo'] for item in opcoes]
print(lista)