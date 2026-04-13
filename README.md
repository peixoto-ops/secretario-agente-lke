# SECRETÁRIO-AGENTE LKE

> Sistema de automação de agenda e acompanhamento cruzado de projetos jurídicos

---

## Estrutura de Diretórios

```
secretario-agente-lke/
│
├── 00_INBOX/                    # Entrada de demandas e inputs
│
├── 10_REFERENCIAS/              # Documentação de referência
│   ├── credentials/             # CREDENCIAIS SENSÍVEIS (gitignored)
│   │   ├── client_secret.json   # OAuth 2.0 Client Secret
│   │   ├── infoclient.txt       # Info do Client ID
│   │   └── README.md            # Documentação das credenciais
│   └── STATUS_CREDENCIAIS_GOOGLE.md
│
├── 20_PROPOSTAS/                # Propostas e alternativas
│   └── PROPOSTA_SECRETARIO_AGENTE.md
│
├── 30_IMPLEMENTACAO/            # Scripts e código
│   └── coletor_github.py
│
├── 40_DOCUMENTOS/               # Relatórios gerados
│   ├── relatorio_consolidado.json
│   ├── RELATORIO_SECRETARIO_AGENTE.md
│   └── RELATORIO_SECRETARIO_AGENTE.pdf
│
├── 50_CRON_JOBS/                # Configurações cron
│   └── secretario-diario.sh
│
├── 60_DIAGNOSTICOS/             # Logs e diagnósticos
│
├── 90_META/                     # Documentação meta
│   └── CATALOGO_REPOSITORIOS.md
│
└── .gitignore                   # Proteção de credenciais
```

---

## Função do Secretário-Agente

### Guardião de Credenciais

O Secretário-Agente é o **guardião centralizado** de todas as credenciais e tokens do ecossistema peixoto-ops:

- Google Workspace OAuth2
- API Keys (quando necessário)
- Tokens de autenticação

**Local seguro:** `10_REFERENCIAS/credentials/` (protegido por .gitignore)

### Gerenciador de Agenda

Integração com:
- Google Calendar (eventos, prazos)
- Google Tasks (tarefas, pendências)
- GitHub (commits, issues, projetos)

### Gerador de Relatórios

Entrega diária via Telegram:
- Resumo executivo
- Prioridades urgentes
- Atividades do dia anterior
- Ações sugeridas

---

## Próximos Passos

1. [ ] Autenticar OAuth2 com novo Client ID
2. [ ] Testar acesso ao Google Calendar
3. [ ] Testar acesso ao Google Tasks
4. [ ] Implementar coleta de dados GitHub
5. [ ] Configurar cron job diário
6. [ ] Primeira execução automatizada

---

## Segurança

**NUNCA** commitar arquivos em `10_REFERENCIAS/credentials/`

Para verificar proteção:
```bash
cd /media/peixoto/Portable/secretario-agente-lke
git status
# credentials/ não deve aparecer
```
