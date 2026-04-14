# SECRETÁRIO-AGENTE LKE

> Sistema de automação de agenda e acompanhamento cruzado de projetos jurídicos

---

## Estrutura de Diretórios

```
secretario-agente-lke/
│
├── 00_INBOX/                    # Caixa de entrada de demandas
│   ├── 01_ARQUIVADAS/           # Demandas resolvidas (não se misturam)
│   ├── FLUXO_INBOX.md           # Documentação do fluxo
│   ├── STATUS_ATUAL.md          # Visão geral do sistema
│   └── [demandas pendentes].md  # Notas com status: pending
│
├── 10_REFERENCIAS/              # Documentação de referência
│   ├── credentials/             # CREDENCIAIS SENSÍVEIS (gitignored)
│   ├── secretario.db            # SQLite local (LEGADO)
│   └── STATUS_CREDENCIAIS_GOOGLE.md
│
├── 20_PROPOSTAS/                # Propostas e alternativas
│   └── PROPOSTA_SECRETARIO_AGENTE.md
│
├── 30_IMPLEMENTACAO/            # Scripts e código
│   ├── hermes_supabase_client.py
│   ├── migrate_to_supabase.py
│   ├── secretario_cli.py
│   └── coletor_github.py
│
├── 40_DOCUMENTOS/               # Relatórios e documentação
│   ├── 41_supabase/
│   │   ├── MANUAL_SUPABASE.md
│   │   ├── SCHEMA_POSTGRESQL.md
│   │   └── GUIA_RAPIDO.md
│   └── ...
│
├── 50_CRON_JOBS/                # Configurações cron
├── 60_DIAGNOSTICOS/             # Logs e diagnósticos
├── 90_META/                     # Documentação meta
│
├── site-narrativo/              # Site de demonstração
├── .env                         # Variáveis de ambiente (gitignored)
├── .gitignore                   # Proteção de credenciais
└── README.md                    # Este arquivo
```

---

## Fluxo da Caixa de Entrada

Ver [[00_INBOX/FLUXO_INBOX.md]] para documentação completa.

### Status das Notas

| Status | Significado | Local |
|--------|-------------|-------|
| `pending` | Aguardando ação | `00_INBOX/` |
| `in_progress` | Sendo trabalhada | `00_INBOX/` |
| `resolved` | Concluída, arquivada | `00_INBOX/01_ARQUIVADAS/` |

---

## Arquitetura Atual

### Cérebro Relacional (Supabase/PostgreSQL)

O sistema foi migrado de SQLite para PostgreSQL no Supabase, criando um "cérebro relacional" que permite:

- **Consultas estruturadas** sem onerar contexto do agente
- **Relacionamentos explícitos** entre entidades
- **Acesso remoto** via API REST
- **Dashboard** para visualização e edição

### Entidades Principais

| Tabela | Descrição |
|--------|-----------|
| `clients` | Clientes e qualificações |
| `repositories` | Repositórios e cofres (paths, nodes) |
| `matters` | Processos judiciais |
| `tools` | Ferramentas (fabric, hermes, zotero) |
| `agent_skills` | Skills de agentes |
| `vault_credentials` | Referências de credenciais |
| `work_sessions` | Log de sessões |

---

## Uso do Client Python

### CLI de Teste

```bash
cd /media/peixoto/Portable/secretario-agente-lke
source venv/bin/activate

python 30_IMPLEMENTACAO/hermes_supabase_client.py matters
python 30_IMPLEMENTACAO/hermes_supabase_client.py matter "Leonardo"
python 30_IMPLEMENTACAO/hermes_supabase_client.py clients
python 30_IMPLEMENTACAO/hermes_supabase_client.py repos
python 30_IMPLEMENTACAO/hermes_supabase_client.py tools
python 30_IMPLEMENTACAO/hermes_supabase_client.py sessions
```

### Uso Programático

```python
from hermes_supabase_client import HermesClient

client = HermesClient()

# Buscar contexto de processo
context = client.fetch_matter_context("Caso Leonardo")

# Listar repositórios
repos = client.list_repositories(node="Aspire")

# Descobrir caminho físico
path = client.get_repository_path("ekwrio")
# Retorna: {"physical_path": "/media/peixoto/Portable/ekwrio", ...}

# Registrar sessão de trabalho
client.log_session(
    matter_id="uuid",
    agent_name="Hermes",
    output_summary="Análise concluída"
)
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

## Migração Realizada

### Dados Migrados (SQLite → Supabase)

| Tabela | Registros |
|--------|-----------|
| `clients` | 4 |
| `repositories` | 10 |
| `matters` | 1 |
| `work_sessions` | 2 |
| `tools` | 4 |
| `vault_credentials` | 3 |

---

## Roadmap

### Fase 1 - Fundação ✅ (Concluída)

- [x] Estrutura de diretórios Johnny.Decimal
- [x] Autenticar OAuth2 com Google Workspace
- [x] Testar acesso ao Google Calendar
- [x] Testar acesso ao Google Tasks
- [x] Migrar para Supabase/PostgreSQL
- [x] Criar client Python para consultas
- [x] Implementação inicial do módulo de redistribuição
- [x] Instalar e avaliar skill stealth-browser
- [x] Atualização do Zotero 9 com integridade preservada

### Fase 2 - Integração ◐ (Em Andamento)

- [ ] Integrar como skill do Hermes Agent
- [ ] Implementar funções de escrita (criar registros)
- [ ] Configurar Row Level Security (RLS)
- [ ] Primeira execução automatizada via cron
- [ ] Debuggar CLI `cmd_cliente()`
- [ ] Implementar comando `add-repo` no CLI
- [ ] Criar hook git post-commit para registro automático

### Fase 3 - Inteligência (Futuro)

- [ ] Detecção de padrões de atividade
- [ ] Priorização automática de tarefas
- [ ] Sugestões de ação contextuais
- [ ] Dashboard web interativo
- [ ] Avaliar API Jusbrasil comercial (alternativa ao stealth-browser para STJ)
- [ ] Investigar playwright-scraper como alternativa OSINT

---

## Demandas Pendentes (00_INBOX)

| Nota | Status | Próximos Passos |
|------|--------|-----------------|
| VERIFICACAO_RESPOSTA_GEMINI | pending | Verificar manualmente Google Drive |
| RELATORIO_SESSAO_20260414 | in_progress | Debuggar CLI cliente |
| PROXIMA_SESSAO_CASO_LORETO | pending | Implementar add-repo |
| ANALISE_SCHEMA_POSTGRES | pending | Decidir hospedagem final |
| Docker Kali no Inspirion | pending | Avaliar necessidade vs API Jusbrasil |

---

## Demonstração

**Site Narrativo:** https://keen-refuge-kfr6.here.now/

---

## Segurança

**NUNCA** commitar:
- `10_REFERENCIAS/credentials/` (OAuth secrets)
- `.env` (variáveis de ambiente)
- `venv/` (ambiente virtual)

---

## Documentação

- **[Manual Supabase](40_DOCUMENTOS/41_supabase/MANUAL_SUPABASE.md)** - Documentação completa
- **[Schema PostgreSQL](40_DOCUMENTOS/41_supabase/SCHEMA_POSTGRESQL.md)** - Definição das tabelas
- **[Guia Rápido](40_DOCUMENTOS/41_supabase/GUIA_RAPIDO.md)** - Comandos essenciais
- **[Fluxo Inbox](00_INBOX/FLUXO_INBOX.md)** - Sistema de demandas

---

## Dependências

```bash
pip install supabase python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
python -c "from supabase import create_client; print('OK')"
```

---

## Histórico de Versões

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.3 | 2026-04-14 | Fluxo de inbox com arquivamento, notas organizadas |
| 1.2 | 2026-04-14 | Site narrativo publicado, roadmap atualizado |
| 1.1 | 2026-04-14 | Migração para Supabase, client Python |
| 1.0 | 2026-04-13 | Versão inicial com SQLite e Google Workspace |
