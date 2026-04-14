# Schema PostgreSQL - Secretário-Agente LKE

> Definição completa das tabelas no Supabase

---

## Script de Criação

```sql
-- Extensão para geração de UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabela de Clientes e Qualificações
CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    document_id TEXT UNIQUE,              -- CPF/CNPJ ou OAB
    professional_license TEXT,            -- Ex: OAB/RJ 94719
    email TEXT,
    address_json JSONB,                   -- Armazena logradouro, CEP, etc.
    law_areas TEXT[],                     -- Ex: ARRAY['Digital', 'Constitutional']
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabela de Repositórios e Cofres
CREATE TABLE IF NOT EXISTS repositories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    physical_path TEXT NOT NULL,          -- Caminho no cluster (ex: /mnt/vaults/obsidian)
    node_name TEXT NOT NULL,              -- Aspire ou Inspirion
    repo_type TEXT CHECK (repo_type IN ('OBSIDIAN', 'GITHUB', 'ZOTERO', 'FILESYSTEM')),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Tabela de Processos e Casos (Matters)
CREATE TABLE IF NOT EXISTS matters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    court_id TEXT,                        -- Número do processo
    status TEXT DEFAULT 'ACTIVE',
    repository_id UUID REFERENCES repositories(id),
    case_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Tabela de Ferramentas e Configurações (Tools)
CREATE TABLE IF NOT EXISTS tools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,            -- Ex: fabric, zotero-cli
    command_prefix TEXT,                  -- Ex: 'fabric --stream'
    description TEXT,
    config_path TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- 5. Tabela de Skills de Agentes
CREATE TABLE IF NOT EXISTS agent_skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,            -- Nome do pattern/skill
    description TEXT,
    input_schema JSONB,                   -- Definição dos campos YAML esperados
    tool_id UUID REFERENCES tools(id),
    system_prompt TEXT,                   -- Instruções base da skill
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Tabela de Credenciais e Acessos (Vault)
CREATE TABLE IF NOT EXISTS vault_credentials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    service_name TEXT NOT NULL,           -- Ex: 'OPENAI_API', 'SUPABASE_KEY'
    credential_id TEXT NOT NULL,          -- Referência segura ou ID externo
    metadata JSONB,                       -- Informações de expiração, escopo, etc.
    last_used TIMESTAMPTZ
);

-- 7. Tabela de Log de Sessões e Auditoria
CREATE TABLE IF NOT EXISTS work_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    matter_id UUID REFERENCES matters(id),
    skill_used UUID REFERENCES agent_skills(id),
    agent_name TEXT DEFAULT 'Hermes',
    input_payload JSONB,
    output_summary TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Tabela de Vínculo Cliente-Processo (N:N)
CREATE TABLE IF NOT EXISTS client_matters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    matter_id UUID REFERENCES matters(id) ON DELETE CASCADE,
    role TEXT,                            -- 'author', 'defendant', 'interested'
    UNIQUE(client_id, matter_id)
);
```

---

## Índices Recomendados

```sql
-- Busca por nome de cliente
CREATE INDEX idx_clients_full_name ON clients(full_name);

-- Busca por documento
CREATE INDEX idx_clients_document ON clients(document_id);

-- Busca por status de processo
CREATE INDEX idx_matters_status ON matters(status);

-- Busca por título de processo
CREATE INDEX idx_matters_title ON matters(title);

-- Busca por nome de repositório
CREATE INDEX idx_repos_name ON repositories(name);

-- Sessões recentes
CREATE INDEX idx_sessions_created ON work_sessions(created_at DESC);

-- Credenciais por serviço
CREATE INDEX idx_creds_service ON vault_credentials(service_name);
```

---

## Views Úteis

### View: Processos com Cliente e Repositório

```sql
CREATE VIEW v_matters_full AS
SELECT 
    m.id,
    m.title,
    m.court_id,
    m.status,
    m.case_summary,
    c.full_name AS client_name,
    c.document_id AS client_document,
    r.name AS repo_name,
    r.physical_path,
    r.node_name
FROM matters m
LEFT JOIN clients c ON m.client_id = c.id
LEFT JOIN repositories r ON m.repository_id = r.id;
```

### View: Sessões com Detalhes

```sql
CREATE VIEW v_sessions_full AS
SELECT 
    s.id,
    s.agent_name,
    s.output_summary,
    s.execution_time_ms,
    s.created_at,
    m.title AS matter_title,
    sk.name AS skill_name
FROM work_sessions s
LEFT JOIN matters m ON s.matter_id = m.id
LEFT JOIN agent_skills sk ON s.skill_used = sk.id
ORDER BY s.created_at DESC;
```

---

## Funções Auxiliares

### Trigger: Auto-update timestamp

```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_clients_updated
    BEFORE UPDATE ON clients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### Função: Buscar contexto completo

```sql
CREATE OR REPLACE FUNCTION get_matter_context(p_title TEXT)
RETURNS TABLE (
    matter_id UUID,
    matter_title TEXT,
    court_id TEXT,
    status TEXT,
    summary TEXT,
    client_name TEXT,
    repo_path TEXT,
    repo_node TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.title,
        m.court_id,
        m.status,
        m.case_summary,
        c.full_name,
        r.physical_path,
        r.node_name
    FROM matters m
    LEFT JOIN clients c ON m.client_id = c.id
    LEFT JOIN repositories r ON m.repository_id = r.id
    WHERE m.title ILIKE '%' || p_title || '%';
END;
$$ LANGUAGE plpgsql;
```

---

## Dados Iniciais

### Ferramentas

```sql
INSERT INTO tools (name, command_prefix, description) VALUES
('fabric', 'fabric --stream', 'AI augmentation patterns'),
('hermes', 'hermes', 'Hermes Agent CLI'),
('legal-commit', 'legal_commit', 'Semantic commits for legal documents'),
('zotero-cli', 'zotero', 'Reference management');
```

### Referências de Credenciais

```sql
INSERT INTO vault_credentials (service_name, credential_id, metadata) VALUES
('GOOGLE_WORKSPACE', 'client_secret.json', '{"location": "10_REFERENCIAS/credentials/"}'),
('SUPABASE', 'env:SUPABASE_SERVICE_ROLE_KEY', '{"type": "service_role"}'),
('GITHUB', 'env:GITHUB_TOKEN', '{"scope": "repo,workflow"}');
```

---

## Row Level Security (RLS)

Para ambientes multi-usuário:

```sql
-- Habilitar RLS
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE matters ENABLE ROW LEVEL SECURITY;
ALTER TABLE repositories ENABLE ROW LEVEL SECURITY;

-- Política: Usuário só vê seus próprios dados
CREATE POLICY clients_isolation ON clients
    USING (auth.uid()::text = (metadata->>'user_id'));

-- Política: Admin vê tudo
CREATE POLICY clients_admin ON clients
    USING (auth.jwt()->>'role' = 'admin');
```

---

## Backup e Manutenção

### Backup Automático

O Supabase faz backup automático diário. Para backup manual:

```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Manutenção

```sql
-- Vacuum analyze (otimização)
VACUUM ANALYZE clients;
VACUUM ANALYZE matters;
VACUUM ANALYZE work_sessions;

-- Reindex
REINDEX TABLE clients;
REINDEX TABLE matters;
```

---

## Notas de Versão

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0 | 2026-04-14 | Schema inicial, migração do SQLite |
