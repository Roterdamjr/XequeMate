from ordem import fn_validacao,fn_inserir_ordem

#print(fn_validacao('A','BBDC4','V'))
#fn_inserir_ordem('A','BBDC4','C',500,60.00)
#fn_inserir_ordem('A','BBDC4','V',500,70.00)

#fn_inserir_ordem('O','CYREA123','V',100, .10)
#fn_inserir_ordem('O','CYREA123','C',100, .15)
#fn_inserir_ordem('O','CYREB123',V',100, .10)
#fn_inserir_ordem('O','CYREB123','C', 100, .08)

retorno = fn_inserir_ordem('A','PETR4','V',100, .25)
print( retorno['mensagem']) 