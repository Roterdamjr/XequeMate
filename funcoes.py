from db_funcoes import fn_buscar_todas, fn_buscar_venda_compras_vazia
import pandas as pd
import yfinance as yf


def fn_buscar_preco_atual(ticker):
    try:
        ticker += '.SA'
        dados = yf.Ticker(ticker).history(period="1d")
        return round(dados['Close'].iloc[-1], 2) if not dados.empty else None
    except Exception as e:
        print(f"Erro ao buscar {ticker}: {e}")
        return None

def fn_busca_mapa_precos_atuais():
    todas_acoes, _ = fn_buscar_todas()
    df = pd.DataFrame(todas_acoes)
    df['preco_atual'] = df['ativo'].apply(fn_buscar_preco_atual)
    df_precos_unicos = df[['ativo', 'preco_atual']].drop_duplicates()
    return df_precos_unicos


def obter_strike(ativo):
    opcoes = fn_busca_opcoes_da_acao(ativo)
    return opcoes['strike'] if opcoes else None

def fn_busca_opcoes_da_acao(acao):
    #recebe uma Acao e retorna todas opcoes correpondentes 
    if len(acao) < 4:
        return None
    
    radical = acao[:4]
    _ , opcoes = fn_buscar_todas()
    
    return  [op for op in opcoes if op['ativo'][:4] == radical]

    #opcao = lista[-1] if lista else None
    #return opcao





def fn_busca_ativo_pai(ativo):
    #retorna dicionario que é a Acao, vendida ou não, correspondente ao parametro

    todas_acoes, _ = fn_buscar_todas()
    radical = ativo[:4]

    if len(ativo) == 5:
        df_acoes = pd.DataFrame(todas_acoes)
        dt_compra = df_acoes.loc[df_acoes['ativo'] == ativo].iloc[0][0]
        return {'ativo': ativo,  'data_compra': dt_compra} 
    else:
        lista = [acao for acao in todas_acoes if acao['ativo'][:4] == radical]
        return dict(lista[0])

def fn_busca_acao_nao_vendida_da_opcao(opcao):
    if len(opcao) < 4:
        return None
    
    radical = opcao[:4]
    acoes , _ = fn_buscar_venda_compras_vazia()
    lista = [ac for ac in acoes if ac['ativo'][:4] == radical]
    acao = lista[-1] if lista else None
    return acao  

