# Supabase - Banco de Dados do Secretário-Agente

> "Cérebro relacional" do sistema de orquestração jurídica

---

## Visão Geral

O Supabase hospeda o banco de dados PostgreSQL que serve como memória operacional de longo prazo do Secretário-Agente. Diferente de arquivos Markdown desestruturados, o banco relacional permite:

- **Consultas cirúrgicas** sem onerar a janela de contexto do agente
- **Relacionamentos explícitos** entre entidades (cliente ↔ processo ↔ repositório)
- **Integridade referencial** garantida por FKs
- **Acesso remoto** via API REST (PostgREST)

---

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIs...
```

**Nunca commite o `.env`** - ele está protegido por `.gitignore`.

### Instalação

```bash
cd /media/peixoto/Portable/secretario-agente-lke
python3 -m venv venv
source venv/bin/activate
pip install supabase python-dotenv
```

---

## Schema do Banco

### Diagrama ER

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   clients   │────<│  client_mat...  │>────│   matters    │
└─────────────┘     └─────────────────┘     └──────────────┘
                                               │
                                               │
                                          ┌────┴─────┐
                                          │repos...  │
                                          └──────────┘

┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   tools     │────<│ agent_skills │     │vault_cred... │
└─────────────┘     └──────────────┘     └──────────────┘

┌──────────────────┐
│  work_sessions   │ ← Log de atividades
└──────────────────┘
```

### Tabelas

#### `clients` - Clientes e Qualificações

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `full_name` | TEXT | Nome completo |
| `document_id` | TEXT | CPF/CNPJ (único) |
| `professional_license` | TEXT | OAB, etc. |
| `email` | TEXT | Email de contato |
| `address_json` | JSONB | Endereço estruturado |
| `law_areas` | TEXT[] | Áreas de atuação |

#### `repositories` - Repositórios e Cofres

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `name` | TEXT | Nome do repositório |
| `physical_path` | TEXT | Caminho no filesystem |
| `node_name` | TEXT | Node do cluster (Aspire/Inspirion) |
| `repo_type` | TEXT | OBSIDIAN, GITHUB, ZOTERO, FILESYSTEM |

#### `matters` - Processos e Casos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `client_id` | UUID | FK para cliente |
| `title` | TEXT | Título do caso |
| `court_id` | TEXT | Número CNJ |
| `status` | TEXT | ACTIVE, CLOSED, SUSPENDED |
| `repository_id` | UUID | FK para repositório |
| `case_summary` | TEXT | Resumo do caso |

#### `tools` - Ferramentas

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `name` | TEXT | Nome da ferramenta |
| `command_prefix` | TEXT | Comando de invocação |
| `description` | TEXT | Descrição |
| `is_active` | BOOLEAN | Se está ativa |

#### `agent_skills` - Skills de Agentes

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `name` | TEXT | Nome da skill |
| `description` | TEXT | Descrição |
| `input_schema` | JSONB | Schema YAML esperado |
| `tool_id` | UUID | FK para ferramenta |

#### `vault_credentials` - Credenciais (Referências)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `service_name` | TEXT | Nome do serviço |
| `credential_id` | TEXT | Referência segura (NÃO o valor) |
| `metadata` | JSONB | Metadados adicionais |

#### `work_sessions` - Log de Sessões

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `matter_id` | UUID | FK para processo |
| `skill_used` | UUID | FK para skill |
| `agent_name` | TEXT | Nome do agente |
| `input_payload` | JSONB | Dados de entrada |
| `output_summary` | TEXT | Resumo da saída |
| `execution_time_ms` | INTEGER | Tempo de execução |

---

## Uso do Client Python

### Importação Básica

```python
from hermes_supabase_client import HermesClient

client = HermesClient()
```

### Consultar Contexto de Processo

```python
# Buscar contexto completo de um caso
context = client.fetch_matter_context("Leonardo Tepedino")
print(context)
# Retorna: title, court_id, status, case_summary, client, repository
```

### Listar Entidades

```python
# Listar processos ativos
matters = client.list_matters(status="ACTIVE")

# Listar clientes
clients = client.list_clients()

# Listar repositórios
repos = client.list_repositories(node="Aspire")

# Listar ferramentas
tools = client.list_tools()
```

### Buscar Caminho de Repositório

```python
# Descobrir onde estão os documentos
path = client.get_repository_path("ekwrio")
# Retorna: {"physical_path": "/media/peixoto/Portable/ekwrio", "node_name": "Aspire"}
```

### Registrar Sessão de Trabalho

```python
# Log de atividade
client.log_session(
    matter_id="uuid-do-processo",
    agent_name="Hermes",
    input_payload={"tipo": "T1.1", "duracao": 45},
    output_summary="Análise documental concluída",
    execution_time_ms=2700000
)
```

### Buscar Referência de Credencial

```python
# Obter referência (NÃO o valor) de credencial
cred = client.get_credential_ref("GOOGLE_WORKSPACE")
# Retorna: {"service_name": "GOOGLE_WORKSPACE", "credential_id": "client_secret.json"}
```

---

## CLI de Teste

O client inclui um CLI para validação rápida:

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

---

## Migração de Dados

O script `migrate_to_supabase.py` foi usado para migrar dados do SQLite local:

```bash
python 30_IMPLEMENTACAO/migrate_to_supabase.py
```

**Dados migrados:**
- 4 clientes
- 10 repositórios
- 1 processo judicial
- 2 sessões de trabalho
- 4 ferramentas
- 3 referências de credenciais

---

## Integração com Hermes Agent

Para usar dentro do Hermes, importe o client:

```python
# Em uma skill do Hermes
from hermes_supabase_client import HermesClient

def skill_context_lookup(matter_name: str):
    client = HermesClient()
    context = client.fetch_matter_context(matter_name)
    return context
```

O Hermes pode então:
1. Consultar o banco antes de operar
2. Descobrir paths de repositórios
3. Registrar suas atividades
4. Manter integridade de contexto

---

## Dashboard Supabase

Acesse o dashboard em: https://supabase.com/dashboard

Funcionalidades úteis:
- **Table Editor** - Editar dados visualmente
- **SQL Editor** - Executar queries ad-hoc
- **API** - Documentação PostgREST
- **Logs** - Monitorar acessos

---

## Boas Práticas

### Segurança

1. **Nunca** commite o `.env`
2. **Nunca** armazene valores de credenciais no banco - apenas referências
3. Use `SUPABASE_SERVICE_ROLE_KEY` apenas em ambiente local
4. Em produção, use `SUPABASE_ANON_KEY` com RLS

### Queries

1. Use índices para buscas frequentes
2. Filtre por status quando possível
3. Limite resultados com `.limit(N)`
4. Use `.select()` específico, nunca `*`

### Manutenção

1. Rode vacuum periodicamente
2. Monitore tamanho das tabelas
3. Archive sessões antigas (> 90 dias)
4. Backup automático do Supabase

---

## Troubleshooting

### Erro: "Variáveis ausentes"

```bash
# Verifique se o .env existe e tem as variáveis
cat .env
# Deve mostrar SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY
```

### Erro: "Column not found"

O schema pode ter mudado. Verifique no dashboard do Supabase se as colunas existem.

### Erro: "JWT expired"

O token pode ter expirado. Gere uma nova Service Role Key no dashboard.

---

## Próximos Passos

- [ ] Integrar como skill do Hermes Agent
- [ ] Implementar funções de escrita (criar registros)
- [ ] Adicionar relacionamentos cliente-processo
- [ ] Configurar Row Level Security (RLS)
- [ ] Implementar busca full-text

---

## Referências

- [Supabase Docs](https://supabase.com/docs)
- [PostgREST](https://postgrest.org)
- [PostgreSQL JSONB](https://www.postgresql.org/docs/current/datatype-json.html)
