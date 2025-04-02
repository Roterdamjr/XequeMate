Como interromper a funcao se der erro em: 
def fn_inserir_ordem(tipo_ativo, ativo, tipo_ordem, quantidade, preco):

    query = Query()

    resultado_validacao = fn_validacao('A', 'BBDC4', 'C')

    if resultado_validacao['valido']:
        print("Validação bem-sucedida.")
    else:
        print(resultado_validacao['mensagem'])
