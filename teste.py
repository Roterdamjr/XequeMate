from db_funcoes import fn_inserir_ordem,fn_buscar_todas,fn_buscar_venda_compras_vazia
import pandas as pd
import yfinance as yf


def listar_todas():
    todas_acoes, todas_opcoes = fn_buscar_todas()

    if todas_acoes:
        df = pd.DataFrame(todas_acoes)
        df['resultado'] = df['venda'] - df['compra']

        print(df)
    else:
        print("Nenhuma ação registrada no momento.")

    if todas_opcoes:
        df = pd.DataFrame(todas_opcoes)
        print(df)
    else:
        print("Nenhuma ação registrada no momento.")


def fn_buscar_preco_atual(ticker):
    try:
        ticker+='.SA'
        dados = yf.Ticker(ticker).history(period="1d")
        return round(dados['Close'].iloc[-1] ,2) if not dados.empty else None
    except Exception as e:
        print(f"Erro ao buscar {ticker}: {e}")
        return None


def fn_busca_mapa_precos_atuais():
    todas_acoes, _ = fn_buscar_todas()

    df = pd.DataFrame(todas_acoes)
    df['preco_atual'] = df['ativo'].apply(fn_buscar_preco_atual)
    return df

#elimina duplicatas
df_precos_atuais = fn_busca_mapa_precos_atuais()
todas_acoes, _ = fn_buscar_todas()
df = pd.DataFrame(todas_acoes)
df['preco_atual'] = df_precos_atuais['ativo'].map(
    df_precos_atuais.drop_duplicates('ativo', keep='last').set_index('ativo')['preco_atual']
)

print(df)

# Mostra o resultado
print(df)



#listar_todas()
