# STATUS DE CREDENCIAIS GOOGLE WORKSPACE

**Data:** 2026-04-13  
**Status:** CONFIGURADO - Aguardando autenticação OAuth2

---

## Situação Atual

As credenciais OAuth2 do Google Workspace estão configuradas no repositório do Secretário-Agente LKE, que atua como guardião centralizado de todas as chaves do ecossistema.

---

## Localização Segura

Todas as credenciais estão em:
```
/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/
├── client_secret.json      # OAuth 2.0 Client Secret (NOVO)
├── infoclient.txt          # Informações do Client ID
└── README.md               # Documentação
```

Permissões:
- Diretório: `700` (apenas owner)
- Arquivos: `600` (apenas owner)

---

## Novo Client ID

- **ID do cliente:** `127808408490-48rukppfn2d0eo7po8obmc4ld16b6e8e.apps.googleusercontent.com`
- **Criado em:** 2026-04-13
- **Escopos configurados:**
  - `https://www.googleapis.com/auth/calendar`
  - `https://www.googleapis.com/auth/tasks`
  - `https://www.googleapis.com/auth/spreadsheets`
  - `https://www.googleapis.com/auth/drive`
  - `https://www.googleapis.com/auth/gmail.readonly`

---

## Proteção Implementada

1. `.gitignore` no repositório protege `credentials/`
2. Permissões restritas (700/600)
3. Credenciais antigas revogadas e removidas
4. Incidente documentado em ecosystem-dashboard

---

## Próximo Passo

Executar autenticação OAuth2 para gerar o token de acesso:

```bash
cd /media/peixoto/Portable/secretario-agente-lke
python3 30_IMPLEMENTACAO/auth_google.py
```

O token gerado será salvo em `10_REFERENCIAS/credentials/token.json`.

---

## Referência

- Incidente documentado: `peixoto-ops/ecosystem-dashboard/docs/SECURITY_INCIDENT_20260413.md`
- Repositório guardião: `secretario-agente-lke`
