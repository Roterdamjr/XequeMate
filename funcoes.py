from db_funcoes import fn_buscar_todas, fn_buscar_venda_compras_vazia,fn_buscar_opcoes_por_id_acao
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np

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


def fn_obter_strike(id_ativo):
    opcoes = fn_buscar_opcoes_por_id_acao(id_ativo)
    if not opcoes:
        return None
    # traz a opcao mais recente
    opcoes.sort(key=lambda x: datetime.strptime(x['data_venda'], '%d/%m/%Y'), reverse=True)
    return opcoes[0]['strike']  


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

def fn_popula_dados(df_precos_atuais):
    # popula dataframe com todoas as informações necessarias
    todas_acoes, todas_opcoes = fn_buscar_todas()

    if (not todas_acoes) or (not todas_opcoes):
        return False
    
     ##############  acoes ##############
    df_acoes = pd.DataFrame(todas_acoes)
    df_acoes = df_acoes[['id_ativo','data_compra',  'data_venda',  'ativo','quantidade','compra','venda']]
    
        # obtem strike
    df_acoes['strike'] = df_acoes['id_ativo'].apply(fn_obter_strike)

    df_acoes = df_acoes.merge(
        df_precos_atuais[['ativo', 'preco_atual']], 
        on='ativo', 
        how='left')
    
        # acrescenta coluna "reulstados"
        # se acao ja foi vendida resultado = venda -compra
        # senão, resultado =  menor valor entre strike e preço atual - compra
    df_acoes['resultado'] = np.where(
        df_acoes['venda'].notna(),  # Se já houve venda
        (df_acoes['venda'] - df_acoes['compra']) * df_acoes['quantidade'],
        (df_acoes[['preco_atual', 'strike']].min(axis=1) - df_acoes['compra']) * df_acoes['quantidade']
        )
    df_acoes['tipo_ativo'] = 'acao'

    ##############  opcoes ##############
    df_opcoes = pd.DataFrame(todas_opcoes)
    df_opcoes = df_opcoes.rename(columns={'id_acao': 'id_ativo'})
    df_opcoes=df_opcoes[['id_ativo','data_compra',  'data_venda',  'ativo','quantidade','compra','venda','strike']]

        # preenche com zeros campos vazios
    df_opcoes['compra'] = pd.to_numeric(df_opcoes['compra'], errors='coerce').fillna(0.0)

        # acrescenta coluna "reulstados"
    df_opcoes['resultado'] = (df_opcoes['venda'] - df_opcoes['compra']) * df_opcoes['quantidade']
    df_opcoes['tipo_ativo'] = 'opcao'
    
    ############### concatena acoes e opcoes ###############################
    df_ativos = pd.concat([df_acoes , df_opcoes], ignore_index=True)

    df_ativos['ativo_pai'] = df_ativos['ativo'].apply(lambda x: fn_busca_ativo_pai(x)['ativo'])

    df_ativos['dt_compra_pai'] = df_ativos['ativo'].apply(lambda x: fn_busca_ativo_pai(x)['data_compra'])
    df_ativos['dt_compra_pai'] = pd.to_datetime(df_ativos['dt_compra_pai'], format="%d/%m/%Y")

    df_ativos['resultado'] = df_ativos['resultado'].map('{:.2f}'.format)
    df_ativos['strike'] = df_ativos['strike'].map('{:.2f}'.format)


    df_ativos = df_ativos.sort_values(['dt_compra_pai', 'id_ativo'])
    df_ativos = df_ativos.drop(columns=['dt_compra_pai', 'ativo_pai'])

    return df_ativos