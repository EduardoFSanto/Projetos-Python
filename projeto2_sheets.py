"""
🚀 PROJETO 2: Cotação de Moedas + Google Sheets
================================================

OBJETIVO:
- Buscar cotações de moedas na API (como Projeto 1)
- Salvar automaticamente no Google Sheets
- Aprender: autenticação, manipulação de planilhas, automação

NOVOS CONCEITOS:
- Service Account (autenticação sem login manual)
- gspread (biblioteca para Google Sheets)
- Append (adicionar linhas em planilha)

PRÉ-REQUISITOS:
- Seguir TODOS os passos do arquivo SETUP_GOOGLE_SHEETS.md
- Ter o arquivo credentials.json na mesma pasta deste arquivo
"""

import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ============================================
# 🔑 PARTE 1: AUTENTICAÇÃO COM GOOGLE SHEETS
# ============================================

def conectar_google_sheets():
    """
    Conecta com o Google Sheets usando Service Account
    
    COMO FUNCIONA:
    1. Define quais APIs vamos usar (Sheets + Drive)
    2. Lê o arquivo credentials.json (nossa "chave de acesso")
    3. Autoriza o acesso
    4. Retorna um cliente conectado
    
    RETORNA:
    - client: Objeto para manipular planilhas
    """
    
    # Define o escopo (quais permissões precisamos)
    # spreadsheets = planilhas | drive = Google Drive
    escopo = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    
    try:
        # Lê as credenciais do arquivo JSON
        # Este arquivo tem a "identidade" do nosso bot
        credenciais = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json',  # Nome do arquivo de credenciais
            escopo               # Permissões necessárias
        )
        
        # Autoriza e cria o cliente
        client = gspread.authorize(credenciais)
        
        print("✅ Conectado ao Google Sheets com sucesso!")
        return client
    
    except FileNotFoundError:
        print("❌ ERRO: Arquivo 'credentials.json' não encontrado!")
        print("   Siga os passos do arquivo SETUP_GOOGLE_SHEETS.md")
        return None
    
    except Exception as erro:
        print(f"❌ Erro ao conectar: {erro}")
        return None


# ============================================
# 💰 PARTE 2: BUSCAR COTAÇÕES (do Projeto 1)
# ============================================

def buscar_cotacao_dolar():
    """
    Busca a cotação atual do Dólar (USD/BRL)
    
    RETORNA:
    - dict com 'moeda', 'valor' e 'data_hora'
    - None em caso de erro
    """
    
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    
    try:
        resposta = requests.get(url, timeout=5)
        resposta.raise_for_status()
        
        dados = resposta.json()
        cotacao = float(dados['USDBRL']['bid'])
        
        # Retorna um dicionário com as informações
        return {
            'moeda': 'USD/BRL',
            'valor': cotacao,
            'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
    
    except requests.exceptions.RequestException as erro:
        print(f"❌ Erro ao buscar cotação: {erro}")
        return None


# ============================================
# 📊 PARTE 3: SALVAR NO GOOGLE SHEETS
# ============================================

def salvar_cotacao_na_planilha(client, cotacao_info):
    """
    Salva a cotação em uma planilha do Google Sheets
    
    PARÂMETROS:
    - client: Cliente conectado ao Google Sheets
    - cotacao_info: Dicionário com dados da cotação
    
    NOVO CONCEITO: append_row()
    - Adiciona uma nova linha no final da planilha
    - É como pressionar "Enter" e escrever na próxima linha
    """
    
    # ⚠️ IMPORTANTE: Substitua pelo ID da sua planilha!
    # Veja no arquivo SETUP_GOOGLE_SHEETS.md como copiar o ID
    PLANILHA_ID = '1ENHCxP6I2uOsXuTEey6sb_VQ2vCQEFcQqvAayxBId5w'
    
    try:
        # Abre a planilha pelo ID
        planilha = client.open_by_key(PLANILHA_ID)
        
        # Pega a primeira aba (worksheet)
        aba = planilha.sheet1
        
        # Verifica se é a primeira vez (cria cabeçalho)
        # get_all_values() retorna todas as linhas da planilha
        todas_linhas = aba.get_all_values()
        
        if len(todas_linhas) == 0:
            # Se a planilha estiver vazia, cria o cabeçalho
            cabecalho = ['Data/Hora', 'Moeda', 'Cotação']
            aba.append_row(cabecalho)
            print("📋 Cabeçalho criado na planilha")
        
        # Prepara os dados para adicionar
        # A ordem deve seguir as colunas: Data/Hora | Moeda | Cotação
        nova_linha = [
            cotacao_info['data_hora'],
            cotacao_info['moeda'],
            cotacao_info['valor']
        ]
        
        # Adiciona a linha na planilha
        aba.append_row(nova_linha)
        
        print(f"✅ Cotação salva: {cotacao_info['moeda']} = R$ {cotacao_info['valor']}")
        print(f"   Horário: {cotacao_info['data_hora']}")
    
    except gspread.exceptions.SpreadsheetNotFound:
        print("❌ ERRO: Planilha não encontrada!")
        print("   Verifique se:")
        print("   1. O ID está correto")
        print("   2. A planilha foi compartilhada com o email do bot")
    
    except Exception as erro:
        print(f"❌ Erro ao salvar na planilha: {erro}")


# ============================================
# 🎯 FUNÇÃO PRINCIPAL
# ============================================

def main():
    """
    Função principal que orquestra todo o processo
    
    FLUXO:
    1. Conecta com Google Sheets
    2. Busca cotação do dólar
    3. Salva na planilha
    """
    
    print("=" * 50)
    print("🚀 PROJETO 2: Cotações → Google Sheets")
    print("=" * 50)
    print()
    
    # Passo 1: Conectar com Google Sheets
    print("📡 Conectando ao Google Sheets...")
    client = conectar_google_sheets()
    
    if not client:
        print("\n⚠️ Não foi possível conectar. Verifique o setup.")
        return
    
    print()
    
    # Passo 2: Buscar cotação
    print("💰 Buscando cotação do dólar...")
    cotacao = buscar_cotacao_dolar()
    
    if not cotacao:
        print("\n⚠️ Não foi possível buscar a cotação.")
        return
    
    print(f"   Dólar agora: R$ {cotacao['valor']:.2f}")
    print()
    
    # Passo 3: Salvar na planilha
    print("💾 Salvando na planilha...")
    salvar_cotacao_na_planilha(client, cotacao)
    
    print()
    print("=" * 50)
    print("✅ Processo concluído!")
    print("   Verifique sua planilha no Google Sheets")
    print("=" * 50)


# ============================================
# 🚀 EXECUÇÃO
# ============================================

if __name__ == "__main__":
    main()


"""
📚 CONCEITOS APRENDIDOS:

1. SERVICE ACCOUNT
   - "Robô" que acessa Google Sheets sem login manual
   - Ideal para automações
   - Precisa de permissão (compartilhar planilha)

2. GSPREAD
   - Biblioteca Python para Google Sheets
   - Principais métodos:
     * authorize() = conecta
     * open_by_key() = abre planilha por ID
     * append_row() = adiciona linha
     * get_all_values() = lê tudo

3. OAUTH2CLIENT
   - Gerencia autenticação com Google
   - ServiceAccountCredentials = credenciais do bot

4. FLUXO DE AUTOMAÇÃO
   - API externa (buscar dados)
   - Processamento (formatar dados)
   - API Google (salvar resultados)

🎯 PRÓXIMOS DESAFIOS:

NÍVEL 1 (Fácil):
- Adicionar mais moedas (EUR, GBP)
- Formatar valor com 2 casas decimais na planilha

NÍVEL 2 (Médio):
- Criar função que roda a cada X minutos
- Adicionar coluna "Variação" comparando com última cotação

NÍVEL 3 (Avançado):
- Criar gráfico automático na planilha
- Enviar alerta se cotação passar de X reais

💪 DICA DO MENTOR:
Execute este script várias vezes e veja a planilha
sendo preenchida automaticamente. É mágico! ✨
"""
