# STATUS DE CREDENCIAIS GOOGLE WORKSPACE

**Data:** 2026-04-13  
**Status:** REVOGAR E RE-CRIAR

---

## Situação Atual

As credenciais OAuth2 do Google Workspace foram expostas no repositório `peixoto-ops/ecosystem-dashboard` e foram revogadas/movidas para local seguro.

---

## Localização Segura

Todas as credenciais agora estão em:
```
~/.hermes/secrets/
├── client_secret.json      (OAuth Client Secret - A REVOGAR)
├── google_client_secret.json (OAuth Client Secret - A REVOGAR)
├── google_token.json       (Access Token - A REVOGAR)
└── token.pickle            (OAuth Token - A REVOGAR)
```

Permissões: 600 (apenas owner pode ler/escrever)

---

## Ação Imediata Necessária

### PASSO 1: Revogar no Google Cloud Console

1. Acesse: https://console.cloud.google.com/apis/credentials
2. Localize o projeto com Client ID: `1278080408490-t8gvhpt99q0pg5bfv4diutl8lk74k054`
3. DELETE o OAuth 2.0 Client ID existente
4. Crie NOVO OAuth 2.0 Client ID

### PASSO 2: Configurar Escopos

Scopos necessários para o Secretário-Agente:
```
https://www.googleapis.com/auth/calendar      # Google Calendar
https://www.googleapis.com/auth/tasks         # Google Tasks
https://www.googleapis.com/auth/spreadsheets  # Google Sheets
https://www.googleapis.com/auth/drive         # Google Drive
https://www.googleapis.com/auth/gmail.readonly # Gmail (leitura)
```

### PASSO 3: Salvar Novas Credenciais

```bash
# Após download do novo client_secret.json:
mv ~/Downloads/client_secret*.json ~/.hermes/secrets/client_secret.json
chmod 600 ~/.hermes/secrets/client_secret.json
```

### PASSO 4: Re-autenticar

O Hermes Agent solicitará nova autenticação OAuth2 na próxima vez que acessar o Google Workspace.

---

## Configuração Correta do Hermes

O Hermes Agent espera encontrar credenciais em:
- `~/.hermes/secrets/client_secret.json` (OAuth Client)
- `~/.hermes/secrets/google_token.json` (gerado após autenticação)

**NUNCA** colocar estes arquivos em:
- Repositórios Git
- Pastas sincronizadas (Dropbox, Google Drive, etc.)
- Diretórios de projetos

---

## Proteções Implementadas

1. `.gitignore` global em `~/.hermes/.gitignore`
2. `.gitignore` local em cada repositório
3. Credenciais movidas para `~/.hermes/secrets/`
4. Documentação do incidente em ecosystem-dashboard

---

## Referência

- Incidente documentado: `/media/peixoto/Portable/ecosystem-dashboard/docs/SECURITY_INCIDENT_20260413.md`
- Skill Google Workspace: `google-workspace`
- Configuração Hermes: `~/.hermes/config.yaml`

---

**Próxima ação:** Aguardando revogação manual no Google Cloud Console
