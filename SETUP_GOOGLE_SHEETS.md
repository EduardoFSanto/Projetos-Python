# 🔧 SETUP: Google Sheets API - Guia Completo

## 📋 PASSO 1: Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Select a project"** (topo da página)
3. Clique em **"NEW PROJECT"**
4. Nome do projeto: `automacao-sheets-python`
5. Clique em **"CREATE"**

---

## 📋 PASSO 2: Habilitar Google Sheets API

1. No menu lateral, vá em: **APIs & Services > Library**
2. Busque: `Google Sheets API`
3. Clique nela e depois em **"ENABLE"**
4. Repita para: `Google Drive API` (necessário para criar/acessar planilhas)

---

## 📋 PASSO 3: Criar Credenciais (Service Account)

### Por que Service Account?

- É como um "robô" que acessa as planilhas por você
- Não precisa de login manual toda vez
- Ideal para automações

### Criando:

1. Vá em: **APIs & Services > Credentials**
2. Clique em **"CREATE CREDENTIALS"**
3. Escolha: **"Service Account"**
4. Preencha:
   - Service account name: `python-sheets-bot`
   - ID: (deixe gerar automaticamente)
5. Clique em **"CREATE AND CONTINUE"**
6. Role: Escolha **"Editor"** (ou pule esta etapa)
7. Clique em **"DONE"**

---

## 📋 PASSO 4: Baixar Arquivo de Credenciais (JSON)

1. Na tela **Credentials**, clique na service account criada
2. Vá na aba **"KEYS"**
3. Clique em **"ADD KEY" > "Create new key"**
4. Escolha formato: **JSON**
5. Clique em **"CREATE"**
6. Um arquivo JSON será baixado automaticamente

### ⚠️ IMPORTANTE:

- Renomeie o arquivo para: `credentials.json`
- Mova para a pasta: `c:\Users\Eduardo\projetos-python\`
- **NUNCA compartilhe este arquivo!** (é como uma senha)

---

## 📋 PASSO 5: Instalar Bibliotecas Python

Abra o terminal no VS Code e execute:

```bash
pip install gspread oauth2client
```

### O que cada uma faz:

- `gspread`: Biblioteca para manipular Google Sheets
- `oauth2client`: Gerencia autenticação com Google

---

## 📋 PASSO 6: Criar uma Planilha de Teste

1. Acesse: https://sheets.google.com/
2. Crie uma nova planilha
3. Nomeie: `Cotacoes Moedas`

### 🔑 ETAPA CRÍTICA - Compartilhar com o Bot:

1. Abra o arquivo `credentials.json` que você baixou
2. Procure por: `"client_email": "python-sheets-bot@..."`
3. **COPIE** esse email completo
4. Na planilha Google Sheets, clique em **"Compartilhar"**
5. **COLE** o email do bot
6. Permissão: **"Editor"**
7. Clique em **"Enviar"**

### Por que fazer isso?

- O bot precisa de permissão para acessar a planilha
- É como adicionar um colaborador

---

## 📋 PASSO 7: Copiar ID da Planilha

Na URL da planilha, copie o ID:

```
https://docs.google.com/spreadsheets/d/[ESTE_É_O_ID]/edit
```

Exemplo:

```
https://docs.google.com/spreadsheets/d/1aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV2wX3yZ/edit
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                      Este é o ID da planilha
```

---

## ✅ CHECKLIST FINAL

Antes de rodar o código Python, confirme:

- [ ] Projeto criado no Google Cloud Console
- [ ] Google Sheets API habilitada
- [ ] Google Drive API habilitada
- [ ] Service Account criada
- [ ] Arquivo `credentials.json` baixado e na pasta do projeto
- [ ] Bibliotecas instaladas (`pip install gspread oauth2client`)
- [ ] Planilha criada no Google Sheets
- [ ] Planilha compartilhada com o email do bot
- [ ] ID da planilha copiado

---

## 🎯 PRÓXIMO PASSO

Agora você está pronto para rodar o arquivo `projeto2_sheets.py`!
