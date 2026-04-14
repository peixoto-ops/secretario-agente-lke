---
status: pending
created: 2026-04-14
tipo: analise
tags: [postgresql, schema, supabase, migracao]
related:
  - "[[STATUS_ATUAL]]"
  - "[[FLUXO_INBOX]]"
proximos_passos:
  - Decidir hospedagem final
  - Configurar RLS
  - Atualizar CLI para SQLAlchemy
---

# Análise do Schema PostgreSQL Proposto

**Data:** 2026-04-14
**Contexto:** Transição de SQLite para PostgreSQL como "cérebro" do Secretário-Agente

---

## Status: PARCIALMENTE IMPLEMENTADO

O schema foi implementado no Supabase, mas alguns aspectos ainda estão pendentes:

### Implementado ✅
- Tabelas principais (clients, repositories, matters, tools, agent_skills, vault_credentials, work_sessions)
- Migração de dados do SQLite
- Client Python para consultas

### Pendente ❌
- Decisão sobre hospedagem (Supabase vs Neon vs Railway)
- Row Level Security (RLS)
- Funções de escrita via CLI
- Relacionamentos N:N completos (cliente_processo, repositorio_processo)

---

## Proposta de Schema Revisado

O schema revisado está documentado em `40_Documentos/41_supabase/SCHEMA_POSTGRESQL.md`

### Principais Tabelas

| Tabela | Descrição |
|--------|-----------|
| `clientes` | Clientes e qualificações |
| `repositorios` | Repositórios e cofres |
| `processos` | Processos judiciais |
| `prazos` | Prazos processuais |
| `comunicacoes` | Comunicações com clientes |
| `ferramentas` | Catálogo de ferramentas |
| `skills` | Capacidades injetáveis |
| `credenciais` | Vault de credenciais |
| `sessoes` | Sessões de trabalho |

---

## Comparativo: SQLite vs PostgreSQL

| Aspecto | SQLite (atual) | PostgreSQL (proposto) |
|---------|----------------|----------------------|
| UUID | INTEGER AUTOINCREMENT | uuid_generate_v4() |
| ENUM | TEXT CHECK | ENUM nativo |
| Arrays | Não suporta | TEXT[] nativo |
| JSON | Não suporta | JSONB nativo |
| Relações N:N | Tabela manual | FK + UNIQUE |
| Full-text | FTS5 básico | tsvector avançado |

---

## Próximos Passos

1. [ ] Decidir hospedagem (Supabase, Neon, Railway, self-hosted)
2. [ ] Criar database e aplicar migration completa
3. [ ] Migrar dados existentes do SQLite
4. [ ] Atualizar CLI para usar psycopg2/sqlalchemy
5. [ ] Implementar queries de uso comum

---

## Decisão Arquitetural

**Resposta recomendada:** Camada Python com SQLAlchemy.

**Motivos:**
1. Validação de dados antes de persistir
2. Lógica de negócio encapsulada
3. Facilita migração futura (ORM abstrai SQL)
4. Integração com skills existentes

**Arquitetura:**
```
Hermes → Python (SQLAlchemy) → PostgreSQL
 ↑
 Skills/CLI
```
