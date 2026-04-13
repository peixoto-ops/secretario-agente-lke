# SESSÃO T1.5.3 - Configuração Google Workspace

**Data planejada:** Próxima sessão  
**Duração estimada:** 45 minutos  
**Prioridade:** ALTA

---

## Objetivos

1. Autenticar OAuth2 com Google Workspace
2. Verificar acesso a todos os serviços
3. Documentar primeiro acesso bem-sucedido

---

## Checklist Pré-Sessão

### Antes de Começar

- [ ] Verificar se `client_secret.json` está em `10_REFERENCIAS/credentials/`
- [ ] Verificar permissões (600)
- [ ] Ter acesso ao navegador para autenticação OAuth
- [ ] Confirmar que as APIs estão habilitadas no Google Cloud Console:
  - [ ] Google Calendar API
  - [ ] Google Tasks API
  - [ ] Google Sheets API
  - [ ] Google Drive API
  - [ ] Gmail API

---

## Tarefas da Sessão

### T1.5.3.1 - Autenticação OAuth2 (10 min)

**Arquivo a criar:** `30_IMPLEMENTACAO/auth_google.py`

```python
#!/usr/bin/env python3
"""
Autenticação OAuth2 para Google Workspace
Gera token.json a partir do client_secret.json
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]

CREDENTIALS_PATH = '/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/client_secret.json'
TOKEN_PATH = '/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/token.json'

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Salvar token
    with open(TOKEN_PATH, 'w') as f:
        f.write(creds.to_json())
    
    print(f"✅ Token salvo em: {TOKEN_PATH}")
    return creds

if __name__ == '__main__':
    authenticate()
```

**Execução:**
```bash
cd /media/peixoto/Portable/secretario-agente-lke
python3 30_IMPLEMENTACAO/auth_google.py
```

---

### T1.5.3.2 - Teste Google Calendar (5 min)

**Arquivo a criar:** `30_IMPLEMENTACAO/test_calendar.py`

**Objetivo:** Listar próximos 5 eventos do calendário principal

**Saída esperada:**
```
📅 Google Calendar - Acesso Verificado
├─ 2026-04-14 09:00 | Reunião XYZ
├─ 2026-04-14 14:00 | Audiência ABC
└─ Total: X eventos na próxima semana
```

---

### T1.5.3.3 - Teste Google Tasks (5 min)

**Arquivo a criar:** `30_IMPLEMENTACAO/test_tasks.py`

**Objetivo:** Listar tasklists e tarefas pendentes

**Saída esperada:**
```
📋 Google Tasks - Acesso Verificado
├─ Lista: Minhas Tarefas (5 itens)
├─ Lista: Trabalho (12 itens)
└─ Total: 17 tarefas pendentes
```

---

### T1.5.3.4 - Teste Google Drive (5 min)

**Arquivo a criar:** `30_IMPLEMENTACAO/test_drive.py`

**Objetivo:** Listar pastas principais do Drive

**Saída esperada:**
```
📁 Google Drive - Acesso Verificado
├─ /Documentos (50 arquivos)
├─ /Jurídico (30 arquivos)
└─ /EKWRio (15 arquivos)
```

---

### T1.5.3.5 - Teste Google Sheets (5 min)

**Arquivo a criar:** `30_IMPLEMENTACAO/test_sheets.py`

**Objetivo:** Listar planilhas acessíveis

**Saída esperada:**
```
📊 Google Sheets - Acesso Verificado
├─ EKWRio - Controle Financeiro
├─ Dashboard Ecosystem
└─ Total: X planilhas acessíveis
```

---

### T1.5.3.6 - Teste Gmail (5 min)

**Arquivo a criar:** `30_IMPLEMENTACAO/test_gmail.py`

**Objetivo:** Listar últimos 5 emails não lidos

**Saída esperada:**
```
📧 Gmail - Acesso Verificado
├─ [juridico] Proposta EKWRio - 10:30
├─ [cliente] Documentos anexados - 09:15
└─ Total: X emails não lidos
```

---

## Script de Validação Completa

**Arquivo a criar:** `30_IMPLEMENTACAO/validate_workspace.py`

Este script executa todos os testes em sequência:

```bash
cd /media/peixoto/Portable/secretario-agente-lke
python3 30_IMPLEMENTACAO/validate_workspace.py
```

**Saída esperada:**
```
═══════════════════════════════════════
   VALIDAÇÃO GOOGLE WORKSPACE
═══════════════════════════════════════

[1/5] Calendar... ✅ OK (5 eventos)
[2/5] Tasks...    ✅ OK (17 tarefas)
[3/5] Drive...    ✅ OK (3 pastas)
[4/5] Sheets...   ✅ OK (2 planilhas)
[5/5] Gmail...    ✅ OK (3 emails)

═══════════════════════════════════════
✅ TODOS OS SERVIÇOS ACESSÍVEIS
═══════════════════════════════════════
```

---

## Dependências Python

Instalar antes da sessão:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
```

---

## Ao Final da Sessão

1. [ ] Todos os testes executados com sucesso
2. [ ] Token salvo em `10_REFERENCIAS/credentials/token.json`
3. [ ] Documentar resultado em `40_DOCUMENTOS/validacao_workspace_T1.5.3.md`
4. [ ] Commit das alterações
5. [ ] Gerar áudio resumo da sessão

---

## Encaminhamentos para Próxima Sessão

Após validação bem-sucedida:
- Implementar coleta automatizada de agenda
- Implementar coleta de tarefas
- Integrar com relatório diário
- Configurar cron job noturno

---

## Referência

- Credenciais: `10_REFERENCIAS/credentials/client_secret.json`
- Token: `10_REFERENCIAS/credentials/token.json` (a ser gerado)
- Proposta: `20_PROPOSTAS/PROPOSTA_SECRETARIO_AGENTE.md`
