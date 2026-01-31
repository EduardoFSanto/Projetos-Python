"""
🚀 PROJETO 3: Automação Trello
================================

OBJETIVO:
- Criar cards no Trello automaticamente
- Integrar com APIs REST (POST requests)
- Gerenciar credenciais com .env

NOVOS CONCEITOS:
- Variáveis de ambiente (.env)
- POST requests (criar dados)
- Trello API
- python-dotenv

PRÉ-REQUISITOS:
- Ter conta no Trello
- API Key e Token gerados
- Arquivo .env configurado
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# ============================================
# 🔑 PARTE 1: CARREGAR CREDENCIAIS
# ============================================

def carregar_credenciais():
    """
    Carrega credenciais do arquivo .env
    
    POR QUÊ .env?
    - Não expõe secrets no código
    - Fácil de mudar sem alterar código
    - Padrão profissional
    
    RETORNA:
    - dict com API_KEY, TOKEN, BOARD_ID, LIST_ID
    """
    
    # Carrega variáveis do arquivo .env
    load_dotenv()
    
    # Lê cada variável
    credenciais = {
        'api_key': os.getenv('TRELLO_API_KEY'),
        'token': os.getenv('TRELLO_TOKEN'),
        'board_id': os.getenv('TRELLO_BOARD_ID'),
        'list_id': os.getenv('TRELLO_LIST_ID')
    }
    
    # Valida se todas foram encontradas
    if not all(credenciais.values()):
        print("❌ ERRO: Credenciais faltando no arquivo .env")
        print("   Verifique se todas as variáveis estão definidas")
        return None
    
    print("✅ Credenciais carregadas com sucesso!")
    return credenciais


# ============================================
# 📝 PARTE 2: CRIAR CARD NO TRELLO
# ============================================

def criar_card_trello(nome, descricao, credenciais):
    """
    Cria um card no Trello
    
    NOVO CONCEITO: POST request
    - GET = buscar dados (Projeto 1)
    - POST = criar/enviar dados (NOVO!)
    
    PARÂMETROS:
    - nome: Título do card
    - descricao: Descrição do card
    - credenciais: Dict com API key, token, list_id
    
    RETORNA:
    - True se sucesso, False se erro
    """
    
    # URL da API do Trello para criar cards
    url = "https://api.trello.com/1/cards"
    
    # Parâmetros da requisição
    # ⚠️ ATENÇÃO: POST usa 'data' ou 'json', não 'params'
    parametros = {
        'key': credenciais['api_key'],
        'token': credenciais['token'],
        'idList': credenciais['list_id'],  # Em qual lista criar
        'name': nome,                       # Título do card
        'desc': descricao                   # Descrição
    }
    
    try:
        # POST request (diferente do GET que usamos antes!)
        resposta = requests.post(url, params=parametros, timeout=10)
        
        # Verifica se deu certo
        resposta.raise_for_status()
        
        # Pega dados do card criado
        card_criado = resposta.json()
        
        print(f"✅ Card criado com sucesso!")
        print(f"   Título: {card_criado['name']}")
        print(f"   URL: {card_criado['url']}")
        
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP ao criar card: {e}")
        print(f"   Resposta: {resposta.text}")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
        return False


# ============================================
# 🎯 FUNÇÃO PRINCIPAL
# ============================================

def main():
    """
    Função principal - cria um card de teste
    """
    
    print("=" * 50)
    print("🚀 PROJETO 3: Automação Trello")
    print("=" * 50)
    print()
    
    # Passo 1: Carregar credenciais
    print("🔑 Carregando credenciais...")
    credenciais = carregar_credenciais()
    
    if not credenciais:
        print("\n⚠️ Configure o arquivo .env primeiro!")
        return
    
    print()
    
    # Passo 2: Criar card de teste
    print("📝 Criando card de teste...")
    
    nome = f"🤖 Card Automático - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    descricao = """
    Este card foi criado automaticamente por Python! 🐍
    
    ✅ Integração com Trello API funcionando
    ✅ POST requests implementados
    ✅ Credenciais seguras com .env
    
    Projeto 3 - Automação Trello
    """
    
    sucesso = criar_card_trello(nome, descricao, credenciais)
    
    print()
    
    if sucesso:
        print("=" * 50)
        print("✅ Sucesso! Verifique seu board no Trello!")
        print("=" * 50)
    else:
        print("=" * 50)
        print("❌ Algo deu errado. Verifique os logs acima.")
        print("=" * 50)


# ============================================
# 🚀 EXECUÇÃO
# ============================================

if __name__ == "__main__":
    main()


"""
📚 CONCEITOS APRENDIDOS:

1. VARIÁVEIS DE AMBIENTE (.env)
   - Separar secrets do código
   - python-dotenv para carregar
   - Nunca commitar credenciais

2. POST REQUEST
   - GET = buscar dados
   - POST = criar/enviar dados
   - Usa 'params' ou 'json' em requests.post()

3. TRELLO API
   - API Key + Token para autenticação
   - Estrutura: boards > lists > cards
   - Endpoints RESTful

🎯 PRÓXIMOS DESAFIOS:

NÍVEL 1 (Fácil):
- Modificar descrição do card
- Adicionar due date (prazo)
- Criar em lista diferente

NÍVEL 2 (Médio):
- Criar card a partir de cotação
  (se dólar > R$ 5.50 → cria alerta)
- Ler tarefas de planilha → criar cards

NÍVEL 3 (Avançado):
- Mover cards entre listas
- Adicionar labels e membros
- Criar checklist automático

💪 DICA DO MENTOR:
Roda esse script várias vezes e veja os cards
aparecendo no Trello. Depois vamos integrar
com o Projeto 2 (Sheets)! ✨
"""