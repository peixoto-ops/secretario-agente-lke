# SECRETÁRIO-AGENTE LKE

> Sistema de automação de agenda e acompanhamento cruzado de projetos jurídicos

---

## Estrutura de Diretórios

```
secretario-agente-lke/
│
├── 00_INBOX/                    # Entrada de demandas e inputs
│   ├── ANALISE_SCHEMA_POSTGRES.md
│   └── STATUS_ATUAL.md
│
├── 10_REFERENCIAS/              # Documentação de referência
│   ├── credentials/             # CREDENCIAIS SENSÍVEIS (gitignored)
│   │   ├── client_secret.json   # OAuth 2.0 Client Secret
│   │   ├── infoclient.txt       # Info do Client ID
│   │   └── README.md            # Documentação das credenciais
│   ├── secretario.db            # SQLite local (LEGADO)
│   └── STATUS_CREDENCIAIS_GOOGLE.md
│
├── 20_PROPOSTAS/                # Propostas e alternativas
│   └── PROPOSTA_SECRETARIO_AGENTE.md
│
├── 30_IMPLEMENTACAO/            # Scripts e código
│   ├── hermes_supabase_client.py  # Client Python para Supabase
│   ├── migrate_to_supabase.py     # Script de migração SQLite→Supabase
│   ├── secretario_cli.py          # CLI legado (SQLite)
│   └── coletor_github.py          # Coleta de dados GitHub
│
├── 40_DOCUMENTOS/               # Relatórios e documentação
│   ├── 41_supabase/             # Documentação do Supabase
│   │   ├── MANUAL_SUPABASE.md   # Manual completo
│   │   ├── SCHEMA_POSTGRESQL.md # Schema do banco
│   │   └── GUIA_RAPIDO.md       # Comandos essenciais
│   ├── DIAGNOSTICO_CAPACIDADES_T1.5.3.md
│   ├── ANALISE_AUTOMACAO_LKE_GH_OPS_AUDITOR.md
│   ├── relatorio_consolidado.json
│   └── RELATORIO_SECRETARIO_AGENTE.md
│
├── 40_Documentos/               # Análises adicionais
│
├── 50_CRON_JOBS/                # Configurações cron
│   └── secretario-diario.sh
│
├── 60_DIAGNOSTICOS/             # Logs e diagnósticos
│
├── 90_META/                     # Documentação meta
│   ├── CATALOGO_REPOSITORIOS.md
│   ├── ESTRUTURA_JOHNNY_DECIMAL.md
│   └── SESSAO_PRATICA_T1.5.4_20260413.md
│
├── site-narrativo/              # Site de demonstração
│   ├── index.html
│   └── css/style.css
│
├── .env                         # Variáveis de ambiente (gitignored)
├── .gitignore                   # Proteção de credenciais
├── venv/                        # Ambiente virtual Python
└── README.md                    # Este arquivo
```

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

# Comandos disponíveis
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

**Referências no banco:** A tabela `vault_credentials` armazena apenas REFERÊNCIAS, nunca os valores.

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

### Repositórios Mapeados

| Nome | Node | Path |
|------|------|------|
| ekwrio | Aspire | /media/peixoto/Portable/ekwrio |
| caso-leonardo-tepedino | Inspirion | /media/peixoto/Portable/caso-leonardo-tepedino |
| caso-loreto-vivas | Inspirion | /media/peixoto/Portable/caso-loreto-vivas |
| lke-processos-hub | Aspire | /home/peixoto/repos/lke-processos-hub |
| secretary-agente-lke | Aspire | /media/peixoto/Portable/secretario-agente-lke |
| ... | ... | ... |

---

## Roadmap Atualizado

### Fase 1 - Fundação ✅ (Concluída)
- [x] Estrutura de diretórios Johnny.Decimal
- [x] Autenticar OAuth2 com Google Workspace
- [x] Testar acesso ao Google Calendar
- [x] Testar acesso ao Google Tasks
- [x] Migrar para Supabase/PostgreSQL
- [x] Criar client Python para consultas
- [x] Implementação inicial do módulo de redistribuição

### Fase 2 - Integração ◐ (Em Andamento)
- [ ] Integrar como skill do Hermes Agent
- [ ] Implementar funções de escrita (criar registros)
- [ ] Configurar Row Level Security (RLS)
- [ ] Primeira execução automatizada via cron
- [x] Análise de automação lke_gh_ops_auditor

### Fase 3 - Inteligência (Futuro)
- [ ] Detecção de padrões de atividade
- [ ] Priorização automática de tarefas
- [ ] Sugestões de ação contextuais
- [ ] Dashboard web interativo

---

## Demonstração

**Site Narrativo:** https://keen-refuge-kfr6.here.now/

Site criado com here.now contando a história do projeto. Expira em 24h (modo anônimo).

Para tornar permanente: https://here.now/claim?slug=keen-refuge-kfr6&token=e26c5535ee229050a12145c03c06ed946ecf4804eca414be948c73ada2d23e77

---

## Segurança

**NUNCA** commitar:
- `10_REFERENCIAS/credentials/` (OAuth secrets)
- `.env` (variáveis de ambiente)
- `venv/` (ambiente virtual)

Para verificar proteção:
```bash
cd /media/peixoto/Portable/secretario-agente-lke
git status
# credentials/ e .env não devem aparecer
```

---

## Documentação

- **[Manual Supabase](40_Documentos/41_supabase/MANUAL_SUPABASE.md)** - Documentação completa
- **[Schema PostgreSQL](40_Documentos/41_supabase/SCHEMA_POSTGRESQL.md)** - Definição das tabelas
- **[Guia Rápido](40_Documentos/41_supabase/GUIA_RAPIDO.md)** - Comandos essenciais
- **[Diagnóstico T1.5.3](40_DOCUMENTOS/DIAGNOSTICO_CAPACIDADES_T1.5.3.md)** - Capacidades e possibilidades

---

## Dependências

```bash
# Instalar dependências
pip install supabase python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# Verificar instalação
python -c "from supabase import create_client; print('OK')"
```

---

## Histórico de Versões

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.2 | 2026-04-14 | Site narrativo publicado, roadmap atualizado, análise automação |
| 1.1 | 2026-04-14 | Migração para Supabase, client Python |
| 1.0 | 2026-04-13 | Versão inicial com SQLite e Google Workspace |
