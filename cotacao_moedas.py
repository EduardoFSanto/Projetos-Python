# cotacao_moedas.py
"""
🎯 OBJETIVO: Entender requisições HTTP e manipulação de JSON
📚 CONCEITOS: GET requests, headers, JSON parsing, tratamento de erros
"""

import requests
from datetime import datetime

def buscar_cotacao(moeda_origem="USD", moeda_destino="BRL"):
    """
    Busca cotação de moedas usando a API pública AwesomeAPI
    
    Args:
        moeda_origem (str): Moeda de origem (ex: USD, EUR)
        moeda_destino (str): Moeda de destino (ex: BRL, USD)
    
    Returns:
        dict: Dados da cotação ou None em caso de erro
    """
    # URL da API - note o f-string para interpolação
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda_origem}-{moeda_destino}"
    
    try:
        # Fazendo a requisição GET
        # timeout evita travamento infinito
        resposta = requests.get(url, timeout=10)
        
        # Verifica se a resposta foi bem-sucedida (status 200-299)
        resposta.raise_for_status()
        
        # Converte JSON para dicionário Python
        dados = resposta.json()
        
        return dados
        
    except requests.exceptions.Timeout:
        print("⏰ Erro: A API demorou muito para responder")
        return None
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e}")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return None


def formatar_cotacao(dados):
    """
    Formata os dados da API de forma legível
    """
    if not dados:
        return "Sem dados para exibir"
    
    # A API retorna uma chave como "USDBRL"
    chave = list(dados.keys())[0]
    cotacao = dados[chave]
    
    resultado = f"""
    💰 COTAÇÃO ATUAL
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Par: {cotacao['code']} → {cotacao['codein']}
    Valor: R$ {float(cotacao['bid']):.2f}
    Variação: {float(cotacao['pctChange']):.2f}%
    Atualização: {cotacao['create_date']}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    return resultado


if __name__ == "__main__":
    print("🌍 Buscando cotação do dólar...")
    
    # Busca a cotação
    dados = buscar_cotacao("USD", "BRL")
    
    # Exibe de forma formatada
    print(formatar_cotacao(dados))
    
    # 🎯 DESAFIO EXTRA: Tente buscar EUR-BRL também!