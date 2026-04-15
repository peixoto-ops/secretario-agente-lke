# Guia Rápido - Supabase Client

> Comandos essenciais para usar o banco de dados

---

## Setup Inicial

```bash
# Entrar no ambiente
cd /media/peixoto/Portable/secretario-agente-lke
source venv/bin/activate

# Verificar conexão
python 30_IMPLEMENTACAO/hermes_supabase_client.py matters
```

---

## Comandos CLI

| Comando | Descrição |
|---------|-----------|
| `python hermes_supabase_client.py matters` | Lista processos |
| `python hermes_supabase_client.py matter "<nome>"` | Busca contexto |
| `python hermes_supabase_client.py clients` | Lista clientes |
| `python hermes_supabase_client.py repos` | Lista repositórios |
| `python hermes_supabase_client.py tools` | Lista ferramentas |
| `python hermes_supabase_client.py sessions` | Sessões recentes |

---

## Uso em Python

```python
from hermes_supabase_client import HermesClient

client = HermesClient()

# Buscar contexto de processo
context = client.fetch_matter_context("Leonardo")

# Listar repositórios
repos = client.list_repositories()

# Descobrir caminho de repo
path = client.get_repository_path("ekwrio")

# Registrar sessão
client.log_session(
    agent_name="Hermes",
    output_summary="Análise concluída",
    execution_time_ms=2700000
)
```

---

## Troubleshooting

| Erro | Solução |
|------|---------|
| "Variáveis ausentes" | Verificar `.env` existe |
| "Column not found" | Schema mudou, verificar dashboard |
| "JWT expired" | Regenerar Service Role Key |

---

## Dashboard

https://supabase.com/dashboard

- Table Editor: Editar dados visualmente
- SQL Editor: Queries ad-hoc
- API: Documentação PostgREST
