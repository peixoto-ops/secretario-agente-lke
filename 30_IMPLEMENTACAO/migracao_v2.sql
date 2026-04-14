-- Migração V2 - Secretário-Agente LKE
-- Tabelas para processos, clientes, prazos e vínculos
-- Data: 2026-04-14

-- ============================================================
-- TABELA: processos
-- Processos judiciais vinculados aos repositórios
-- ============================================================
CREATE TABLE IF NOT EXISTS processos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL UNIQUE,
    tribunal TEXT NOT NULL,
    classe TEXT,
    assunto TEXT,
    orgao_julgador TEXT,
    relator TEXT,
    origem TEXT,
    fase TEXT,
    situacao TEXT,
    data_distribuicao DATE,
    valor_causa REAL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABELA: clientes
-- Clientes do escritório
-- ============================================================
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT UNIQUE,
    rg TEXT,
    nacionalidade TEXT DEFAULT 'Brasileira',
    estado_civil TEXT,
    profissao TEXT,
    data_nascimento DATE,
    email TEXT,
    telefone TEXT,
    endereco TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    observacoes TEXT,
    preferencia_contato TEXT,
    ativo BOOLEAN DEFAULT 1,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABELA: prazos
-- Prazos processuais e administrativos
-- ============================================================
CREATE TABLE IF NOT EXISTS prazos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    processo_id INTEGER,
    descricao TEXT NOT NULL,
    data_limite DATE NOT NULL,
    hora_limite TEXT,
    tipo TEXT CHECK(tipo IN ('processual', 'administrativo', 'interno', 'outro')),
    prioridade INTEGER DEFAULT 5,
    status TEXT CHECK(status IN ('pendente', 'cumprido', 'vencido', 'cancelado')),
    responsavel TEXT,
    observacoes TEXT,
    cumprido_em TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (processo_id) REFERENCES processos(id)
);

-- ============================================================
-- TABELA: vinculos_repositorio_processo
-- Relaciona repositórios a processos
-- ============================================================
CREATE TABLE IF NOT EXISTS vinculos_repositorio_processo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repositorio_id INTEGER NOT NULL,
    processo_id INTEGER NOT NULL,
    papel TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (repositorio_id) REFERENCES repositorios(id),
    FOREIGN KEY (processo_id) REFERENCES processos(id),
    UNIQUE(repositorio_id, processo_id)
);

-- ============================================================
-- TABELA: vinculos_cliente_processo
-- Relaciona clientes a processos
-- ============================================================
CREATE TABLE IF NOT EXISTS vinculos_cliente_processo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    processo_id INTEGER NOT NULL,
    qualidade TEXT NOT NULL,
    posicao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (processo_id) REFERENCES processos(id),
    UNIQUE(cliente_id, processo_id)
);

-- ============================================================
-- TABELA: comunicacoes
-- Registro de comunicações com clientes
-- ============================================================
CREATE TABLE IF NOT EXISTS comunicacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    processo_id INTEGER,
    tipo TEXT CHECK(tipo IN ('telefone', 'email', 'whatsapp', 'reuniao', 'outro')),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resumo TEXT,
    responsavel TEXT,
    seguimento BOOLEAN DEFAULT 0,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (processo_id) REFERENCES processos(id)
);

-- ============================================================
-- ÍNDICES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_processos_numero ON processos(numero);
CREATE INDEX IF NOT EXISTS idx_processos_tribunal ON processos(tribunal);
CREATE INDEX IF NOT EXISTS idx_clientes_cpf ON clientes(cpf);
CREATE INDEX IF NOT EXISTS idx_clientes_nome ON clientes(nome);
CREATE INDEX IF NOT EXISTS idx_prazos_data_limite ON prazos(data_limite);
CREATE INDEX IF NOT EXISTS idx_prazos_status ON prazos(status);
CREATE INDEX IF NOT EXISTS idx_prazos_processo ON prazos(processo_id);
CREATE INDEX IF NOT EXISTS idx_comunicacoes_cliente ON comunicacoes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_comunicacoes_processo ON comunicacoes(processo_id);

-- ============================================================
-- VERSÃO DO SCHEMA
-- ============================================================
CREATE TABLE IF NOT EXISTS schema_versao (
    versao INTEGER PRIMARY KEY,
    descricao TEXT,
    aplicado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_versao (versao, descricao) VALUES (2, 'Adicionadas tabelas: processos, clientes, prazos, vinculos, comunicacoes');
