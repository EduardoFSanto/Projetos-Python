"""
🚀 PROJETO 3.5: INTEGRAÇÃO COMPLETA
====================================

SISTEMA: Monitor de Cotação com Alertas Automáticos

FLUXO:
1. Busca cotação do dólar (AwesomeAPI)
2. Salva na planilha Google Sheets
3. Se cotação > R$ 5.50 → Cria card de alerta no Trello
4. Registra tudo com logs
"""

import requests
import gspread
import os
from datetime import datetime
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Carrega variáveis de ambiente
load_dotenv()

# Limite de alerta para dólar
LIMITE_DOLAR = 5.50

def buscar_cotacao_dolar():
    """Busca cotação atual do dólar"""
    print("💰 Buscando cotação do dólar...")
    
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        
        dados = resposta.json()
        cotacao = dados['USDBRL']
        
        resultado = {
            'valor': float(cotacao['bid']),
            'variacao': float(cotacao['pctChange']),
            'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        print(f"✅ Cotação obtida: R$ {resultado['valor']:.2f}")
        return resultado
        
    except Exception as e:
        print(f"❌ Erro ao buscar cotação: {e}")
        return None


def salvar_no_sheets(cotacao):
    """Salva cotação no Google Sheets"""
    print("📊 Salvando na planilha...")
    
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json',
            scope
        )
        
        client = gspread.authorize(creds)
        
        # ID DA SUA PLANILHA
        planilha = client.open_by_key('1ENHCxP6I2uOsXuTEey6sb_VQ2vCQEFcQqvAayxBId5w')
        sheet = planilha.sheet1
        
        linha = [
            cotacao['data_hora'],
            f"R$ {cotacao['valor']:.2f}",
            f"{cotacao['variacao']:.2f}%",
            "🚨 ALERTA!" if cotacao['valor'] > LIMITE_DOLAR else "Normal"
        ]
        
        sheet.append_row(linha)
        
        print(f"✅ Dados salvos na planilha!")
        return True
        
    except FileNotFoundError:
        print("⚠️ Arquivo credentials.json não encontrado")
        return False
        
    except Exception as e:
        print(f"⚠️ Erro ao salvar no Sheets: {e}")
        return False


def criar_alerta_trello(cotacao):
    """Cria card de alerta no Trello se necessário"""
    
    # Verifica se precisa criar alerta
    if cotacao['valor'] <= LIMITE_DOLAR:
        print(f"✅ Cotação normal (R$ {cotacao['valor']:.2f} ≤ R$ {LIMITE_DOLAR:.2f})")
        print("   Não é necessário criar alerta no Trello")
        return False
    
    print(f"🚨 ALERTA! Cotação acima do limite (R$ {cotacao['valor']:.2f} > R$ {LIMITE_DOLAR:.2f})")
    print("📝 Criando card de alerta no Trello...")
    
    # Carregar credenciais do Trello
    api_key = os.getenv('TRELLO_API_KEY')
    token = os.getenv('TRELLO_TOKEN')
    list_id = os.getenv('TRELLO_LIST_ID')
    
    if not all([api_key, token, list_id]):
        print("⚠️ Credenciais do Trello não encontradas no .env")
        return False
    
    # Preparar dados do card
    url = "https://api.trello.com/1/cards"
    
    tendencia = "📈" if cotacao['variacao'] > 0 else "📉"
    
    nome = f"🚨 ALERTA: Dólar em R$ {cotacao['valor']:.2f}"
    
    descricao = f"""
## 🚨 Alerta de Cotação

**Valor atual:** R$ {cotacao['valor']:.2f}  
**Variação:** {cotacao['variacao']:.2f}% {tendencia}  
**Limite configurado:** R$ {LIMITE_DOLAR:.2f}  
**Data/Hora:** {cotacao['data_hora']}

---

### ⚠️ Ação Recomendada:
- Verificar se é momento de compra/venda
- Analisar tendência do mercado
- Consultar assessor financeiro se necessário

---

*Card criado automaticamente pelo sistema de monitoramento Python* 🐍
"""
    
    parametros = {
        'key': api_key,
        'token': token,
        'idList': list_id,
        'name': nome,
        'desc': descricao,
        'pos': 'top'
    }
    
    try:
        resposta = requests.post(url, params=parametros, timeout=10)
        resposta.raise_for_status()
        
        card = resposta.json()
        
        print(f"✅ Card de alerta criado com sucesso!")
        print(f"   URL: {card['url']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar card no Trello: {e}")
        return False


def executar_monitoramento():
    """Executa o fluxo completo de monitoramento"""
    
    print("=" * 60)
    print("🚀 SISTEMA DE MONITORAMENTO DE COTAÇÃO")
    print("=" * 60)
    print()
    
    # PASSO 1: Buscar cotação
    cotacao = buscar_cotacao_dolar()
    
    if not cotacao:
        print("\n❌ Falha ao buscar cotação. Encerrando.")
        return
    
    print()
    
    # PASSO 2: Salvar no Google Sheets
    salvar_no_sheets(cotacao)
    
    print()
    
    # PASSO 3: Verificar se precisa criar alerta no Trello
    alerta_criado = criar_alerta_trello(cotacao)
    
    print()
    print("=" * 60)
    
    # RESUMO FINAL
    if alerta_criado:
        print("✅ MONITORAMENTO CONCLUÍDO - ALERTA CRIADO!")
        print(f"   Dólar: R$ {cotacao['valor']:.2f} (acima do limite)")
        print("   🚨 Verifique o card no Trello!")
    else:
        print("✅ MONITORAMENTO CONCLUÍDO - SITUAÇÃO NORMAL")
        print(f"   Dólar: R$ {cotacao['valor']:.2f}")
        print("   ✅ Dados salvos na planilha")
    
    print("=" * 60)


def testar_alerta():
    """Função de teste que simula uma cotação alta"""
    print("🧪 MODO DE TESTE - Simulando cotação alta")
    print()
    
    cotacao_teste = {
        'valor': 5.75,
        'variacao': 2.5,
        'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    
    print(f"💰 Cotação simulada: R$ {cotacao_teste['valor']:.2f}")
    print()
    
    criar_alerta_trello(cotacao_teste)


if __name__ == "__main__":
    # MODO NORMAL - Busca cotação real
    # executar_monitoramento()
    
    # MODO TESTE - Simula cotação alta para testar
    testar_alerta()
"""
📚 CONCEITOS APRENDIDOS NESTA INTEGRAÇÃO:

1. ORQUESTRAÇÃO DE SERVIÇOS
   - Coordenar múltiplas APIs em um fluxo
   - Error handling independente por serviço

2. CONDITIONAL AUTOMATION
   - Automação baseada em regras de negócio
   - Ações automáticas baseadas em dados

3. REAL-WORLD INTEGRATION
   - APIs diferentes trabalhando juntas
   - Fluxo de dados entre sistemas

💪 PARABÉNS!
Você criou uma AUTOMAÇÃO REAL que integra 3 serviços!
"""