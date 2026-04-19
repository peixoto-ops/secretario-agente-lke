# STATUS DE CREDENCIAIS GOOGLE WORKSPACE

**Data:** 2026-04-18 
**Status:** CONFIGURADO - Credenciais em ~/.hermes/

---

## Situacao Atual (ATUALIZADO)

As credenciais OAuth2 do Google Workspace foram movidas para `~/.hermes/` seguindo o padrao do Hermes Agent. O secretario-agente-lke agora mantem APENAS BACKUP.

---

## Localizacao de Trabalho

**Local principal:** `~/.hermes/`
```
~/.hermes/
├── google_token.json # Token OAuth principal
├── google_client_secret.json # OAuth Client Secret
└── gws_credentials.json # Formato gws (Google Workspace CLI)
```

---

## Backup

**Local de backup:** `10_REFERENCIAS/credentials/`
```
10_REFERENCIAS/credentials/
├── client_secret.json # Backup do client secret
├── token_novo.json # Backup do token
├── gws_credentials_novo.json # Backup formato gws
└── (arquivos antigos - podem ser removidos)
```

**NOTA:** Este diretorio e APENAS BACKUP. Skills devem usar `~/.hermes/google_*.json`.

---

## Client ID Atual

- **ID do cliente:** `127808408490-om4169fu4f3ltta2jop1j7nrf22jf12f.apps.googleusercontent.com`
- **Criado em:** 2026-04-18
- **Escopos configurados:**
 - `https://www.googleapis.com/auth/calendar`
 - `https://www.googleapis.com/auth/tasks`
 - `https://www.googleapis.com/auth/spreadsheets`
 - `https://www.googleapis.com/auth/drive`
 - `https://www.googleapis.com/auth/gmail.readonly`

---

## Protecao Implementada

1. Credenciais em `~/.hermes/` (permissao 600)
2. Backup em `10_REFERENCIAS/credentials/` (fora do git)
3. `.gitignore` protege arquivos de credenciais
4. Permissoes restritas (700/600)

---

## Razao da Mudanca

Em 2026-04-18, foi identificado que manter credenciais no secretario-agente-lke criava friccao:
- Skills precisavam de links simbolicos
- Dependencia de repositorio externo
- Nao seguia o padrao do Hermes (auth.json, config.yaml em ~/.hermes/)

A decisao foi mover para `~/.hermes/` para:
- Eliminar friccao
- Seguir padrao Hermes
- Autonomia das skills
- Simplicidade (sem links simbolicos)

---

## Referencia

- Skill atualizada: `secretario-agente-lke`
- Padrao Hermes: `~/.hermes/auth.json` com `credential_pool`
