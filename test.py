from tinydb import TinyDB

db = TinyDB('acoes.json')
db.truncate()

# Insere dados de ações
db.insert({
    'ativo': 'PETR4',
    'quantidade': 100,
    'compra': 30.50,
    'venda': 31.00,
    'preco_atual': 30.75
})
db.insert({
    'ativo': 'VALE3',
    'quantidade': 50,
    'compra': 80.20,
    'venda': 81.50,
    'preco_atual': 80.80
})

db = TinyDB('opcoes.json')
db.truncate()
db.insert({
    'ativo': 'PETRC123',
    'quantidade': 200,
    'compra': 2.50,
    'venda': 2.80,
    'preco_atual': 2.65
})
db.insert({
    'ativo': 'VALEP456',
    'quantidade': 150,
    'compra': 1.80,
    'venda': 2.00,
    'preco_atual': 1.90
})

print("Dados inseridos com sucesso!")