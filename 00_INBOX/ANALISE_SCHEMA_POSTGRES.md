# Análise do Schema PostgreSQL Proposto

**Data:** 2026-04-14
**Contexto:** Transição de SQLite para PostgreSQL como "cérebro" do Secretário-Agente

---

## Proposta Original

```sql
CREATE TABLE Clientes (
    id UUID PRIMARY KEY,
    nome VARCHAR(255),
    cnpj CHAR(14),
    criado_em TIMESTAMP
);

CREATE TABLE Repositórios (
    id UUID PRIMARY KEY,
    cliente_id UUID,
    url TEXT,
    branch_main VARCHAR(50)
);

CREATE TABLE Processos (
    id UUID PRIMARY KEY,
    cliente_id UUID,
    status ENUM,
    prioridade INT
);

CREATE TABLE Ferramentas (
    id UUID PRIMARY KEY,
    nome VARCHAR(100),
    versao VARCHAR(20)
);

CREATE TABLE Skills (
    id UUID PRIMARY KEY,
    ferramenta_id UUID,
    complexidade INT
);

CREATE TABLE Credenciais (
    id UUID PRIMARY KEY,
    processo_id UUID,
    hash TEXT
);

CREATE TABLE Sessões (
    id UUID PRIMARY KEY,
    skill_id UUID,
    data_inicio TIMESTAMP
);
```

---

## Análise Crítica

### Pontos Fortes

1. **UUID como PK** - Ideal para distribuição e merge de dados
2. **Separação clara de domínios** - Clientes, Processos, Ferramentas são entidades distintas
3. **Relacionamentos explícitos** - FKs bem definidas

### Problemas Identificados

#### 1. **Repositórios × Processos** - Relação N:N faltando

Um repositório pode conter múltiplos processos (ex: `inv_sa_02` tem vários processos de inventário). E um processo pode ter múltiplos repositórios (ex: repositório do caso + repositório de precedentes).

**Correção:** Tabela de vínculo.

#### 2. **Processos faltando campos críticos**

Número CNJ, tribunal, classe, assunto, valor da causa, data distribuição - essenciais para orquestração.

#### 3. **Credenciais × Processos** - Cardinalidade errada

Credenciais (OAuth, API keys) são por SERVIÇO, não por processo. Google Workspace serve todo o ecossistema, não um processo específico.

**Correção:** `servico VARCHAR` + possivelmente `cliente_id` para credenciais de cliente específico.

#### 4. **Sessões × Skills** - Muito restritivo

Sessão de trabalho pode envolver múltiplas skills (ex: sessão T1.1 usa `secretario-agente` + `legal-commit` + `fabric`). E uma skill pode ser usada em múltiplas sessões.

**Correção:** Relação N:N via `sessao_skills`.

#### 5. **Ferramentas isoladas** - Sem ligação com uso real

De onde vêm as ferramentas? Como o agente sabe qual usar? Faltam metadados de invocação.

---

## Proposta de Schema Revisado

```sql
-- ============================================================
-- EXTENSÃO UUID
-- ============================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- DOMÍNIOS E TIPOS ENUM
-- ============================================================
CREATE TYPE status_processo AS ENUM ('ativo', 'arquivado', 'suspenso', 'baixado');
CREATE TYPE tipo_prazo AS ENUM ('processual', 'administrativo', 'interno');
CREATE TYPE status_prazo AS ENUM ('pendente', 'cumprido', 'vencido', 'cancelado');
CREATE TYPE tipo_comunicacao AS ENUM ('telefone', 'email', 'whatsapp', 'reuniao', 'outro');

-- ============================================================
-- CLIENTES
-- Pessoa física ou jurídica
-- ============================================================
CREATE TABLE clientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(10) CHECK(tipo IN ('pf', 'pj')) DEFAULT 'pf',
    cpf CHAR(11) UNIQUE,
    cnpj CHAR(14) UNIQUE,
    rg VARCHAR(20),
    email VARCHAR(255),
    telefone VARCHAR(20),
    endereco TEXT,
    cidade VARCHAR(100),
    uf CHAR(2),
    cep CHAR(8),
    observacoes TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- REPOSITÓRIOS
-- GitHub repos monitorados pelo sistema
-- ============================================================
CREATE TABLE repositorios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,           -- nome do repo
    owner VARCHAR(100) NOT NULL,          -- org/owner
    url TEXT NOT NULL,                    -- URL completa
    branch_main VARCHAR(50) DEFAULT 'main',
    descricao TEXT,
    prioridade INT DEFAULT 5 CHECK(prioridade BETWEEN 1 AND 5),
    tipo VARCHAR(50),                     -- 'caso', 'infraestrutura', 'template', etc.
    path_local TEXT,                      -- caminho no filesystem
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- PROCESSOS JUDICIAIS
-- ============================================================
CREATE TABLE processos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    numero_cnj VARCHAR(25) UNIQUE NOT NULL,  -- NNNNNNN-DD.AAAA.J.TR.OOOO
    tribunal VARCHAR(20) NOT NULL,
    classe VARCHAR(100),
    assunto TEXT,
    orgao_julgador VARCHAR(200),
    relator VARCHAR(200),
    origem VARCHAR(200),
    fase VARCHAR(100),
    status status_processo DEFAULT 'ativo',
    data_distribuicao DATE,
    valor_causa DECIMAL(15,2),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- VÍNCULOS (TABELAS DE RELACIONAMENTO)
-- ============================================================

-- Cliente x Processo (N:N)
CREATE TABLE cliente_processo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID NOT NULL REFERENCES clientes(id),
    processo_id UUID NOT NULL REFERENCES processos(id),
    qualidade VARCHAR(50) NOT NULL,       -- 'autor', 'reu', 'interessado', etc.
    posicao VARCHAR(100),                 -- posição processual
    UNIQUE(cliente_id, processo_id)
);

-- Repositório x Processo (N:N)
CREATE TABLE repositorio_processo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    repositorio_id UUID NOT NULL REFERENCES repositorios(id),
    processo_id UUID NOT NULL REFERENCES processos(id),
    papel VARCHAR(50) DEFAULT 'principal', -- 'principal', 'precedentes', 'anexos'
    UNIQUE(repositorio_id, processo_id)
);

-- ============================================================
-- PRAZOS
-- ============================================================
CREATE TABLE prazos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    processo_id UUID REFERENCES processos(id),
    descricao TEXT NOT NULL,
    data_limite DATE NOT NULL,
    hora_limite TIME,
    tipo tipo_prazo DEFAULT 'processual',
    prioridade INT DEFAULT 5,
    status status_prazo DEFAULT 'pendente',
    responsavel VARCHAR(100),
    observacoes TEXT,
    cumprido_em TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- COMUNICAÇÕES COM CLIENTES
-- ============================================================
CREATE TABLE comunicacoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID REFERENCES clientes(id),
    processo_id UUID REFERENCES processos(id),
    tipo tipo_comunicacao,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resumo TEXT,
    responsavel VARCHAR(100),
    seguimento BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- FERRAMENTAS (Catálogo)
-- ============================================================
CREATE TABLE ferramentas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    versao VARCHAR(20),
    caminho_executavel TEXT,             -- path para binário/script
    comando_invocacao TEXT,              -- template de comando
    requisitos TEXT,                     -- JSON com requisitos
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SKILLS (Capacidades injetáveis)
-- ============================================================
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    categoria VARCHAR(50),                -- 'juridico', 'devops', 'research', etc.
    arquivo_path TEXT,                   -- caminho para SKILL.md
    parametros_yaml TEXT,                -- template de parâmetros
    complexidade INT DEFAULT 3 CHECK(complexidade BETWEEN 1 AND 5),
    ferramentas_necessarias TEXT[],      -- array de nomes de ferramentas
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CREDENCIAIS (Vault)
-- ============================================================
CREATE TABLE credenciais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    servico VARCHAR(100) NOT NULL,       -- 'google_workspace', 'github', 'openai', etc.
    tipo VARCHAR(50) NOT NULL,           -- 'oauth2', 'api_key', 'token', etc.
    chave_ref TEXT NOT NULL,             -- referência segura (não o segredo!)
    cliente_id UUID REFERENCES clientes(id), -- NULL = credencial global
    escopo TEXT,                         -- escopo OAuth ou permissões
    expira_em TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    metadados JSONB,                     -- dados extras
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SESSÕES DE TRABALHO
-- ============================================================
CREATE TABLE sessoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    titulo VARCHAR(255),
    tipo VARCHAR(20),                    -- 'T1.1', 'T1.2', 'livre', etc.
    resumo TEXT,
    resumo_fabric TEXT,                  -- output do Fabric
    repositorio_id UUID REFERENCES repositorios(id),
    duracao_minutos INT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SESSÃO x SKILLS (N:N)
-- ============================================================
CREATE TABLE sessao_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sessao_id UUID NOT NULL REFERENCES sessoes(id),
    skill_id UUID NOT NULL REFERENCES skills(id),
    resultado TEXT,
    UNIQUE(sessao_id, skill_id)
);

-- ============================================================
-- LOGS DE ATIVIDADE
-- ============================================================
CREATE TABLE atividade_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sessao_id UUID REFERENCES sessoes(id),
    repositorio_id UUID REFERENCES repositorios(id),
    tipo VARCHAR(50) NOT NULL,           -- 'commit', 'push', 'criacao', 'edicao', etc.
    mensagem TEXT,
    hash_git VARCHAR(40),
    autor VARCHAR(100),
    metadados JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ÍNDICES
-- ============================================================
CREATE INDEX idx_clientes_nome ON clientes(nome);
CREATE INDEX idx_clientes_cpf ON clientes(cpf);
CREATE INDEX idx_clientes_cnpj ON clientes(cnpj);
CREATE INDEX idx_processos_numero ON processos(numero_cnj);
CREATE INDEX idx_processos_tribunal ON processos(tribunal);
CREATE INDEX idx_processos_status ON processos(status);
CREATE INDEX idx_prazos_data ON prazos(data_limite);
CREATE INDEX idx_prazos_status ON prazos(status);
CREATE INDEX idx_repositorios_nome ON repositorios(nome);
CREATE INDEX idx_sessoes_data ON sessoes(data);
CREATE INDEX idx_logs_timestamp ON atividade_logs(timestamp);

-- ============================================================
-- TRIGGER PARA atualizado_em
-- ============================================================
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_clientes_update
    BEFORE UPDATE ON clientes
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_processos_update
    BEFORE UPDATE ON processos
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_repositorios_update
    BEFORE UPDATE ON repositorios
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_credenciais_update
    BEFORE UPDATE ON credenciais
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

---

## Comparativo: SQLite vs PostgreSQL

| Aspecto | SQLite (atual) | PostgreSQL (proposto) |
|---------|----------------|----------------------|
| UUID | INTEGER AUTOINCREMENT | uuid_generate_v4() |
| ENUM | TEXT CHECK | ENUM nativo |
| Arrays | Não suporta | TEXT[] nativo |
| JSON | Não suporta | JSONB nativo |
| Relações N:N | Tabela manual | FK + UNIQUE |
| Timestamps | CURRENT_TIMESTAMP | CURRENT_TIMESTAMP + triggers |
| Full-text | FTS5 básico | tsvector avançado |

---

## Próximos Passos

1. [ ] Decidir hospedagem (Supabase, Neon, Railway, self-hosted)
2. [ ] Criar database e aplicar migration
3. [ ] Migrar dados existentes do SQLite
4. [ ] Atualizar CLI para usar psycopg2/sqlalchemy
5. [ ] Implementar queries de uso comum

---

## Decisão Arquitetural

**Pergunta do Gemini:** *"Você prefere intermediar o acesso através de scripts Python ou SQL direto via PostgREST?"*

**Resposta recomendada:** Camada Python com SQLAlchemy.

**Motivos:**
1. Validação de dados antes de persistir
2. Lógica de negócio encapsulada
3. Facilita migração futura (ORM abstrai SQL)
4. Integração com skills existentes
5. PostgREST é ótimo para APIs, mas este é uso interno do agente

**Arquitetura:**
```
Hermes → Python (SQLAlchemy) → PostgreSQL
         ↑
    Skills/CLI
```
