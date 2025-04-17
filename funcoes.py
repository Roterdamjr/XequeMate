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

def fn_busca_opcao_da_acao(acao):
    if len(acao) < 4:
        return None
    
    radical = acao[:4]
    _ , opcoes = fn_buscar_venda_compras_vazia()
    
    lista = [op for op in opcoes if op['ativo'][:4]==radical]
    opcao = lista[-1] if lista else None
    return opcao

