from db_funcoes import fn_buscar_todas
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
    return df