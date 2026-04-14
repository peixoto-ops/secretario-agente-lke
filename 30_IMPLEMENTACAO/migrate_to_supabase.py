#!/usr/bin/env python3
"""
Script de migração: SQLite local → Supabase PostgreSQL

Popula as tabelas do Supabase com dados existentes no secretario.db
Schema baseado na estrutura definida em SUPABASE_SCHEMA.sql
"""

import os
import json
import sqlite3
import uuid
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv()

DB_LOCAL = Path(__file__).parent.parent / "10_REFERENCIAS" / "secretario.db"

def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY são obrigatórios")
    return create_client(url, key)

def get_sqlite():
    return sqlite3.connect(DB_LOCAL)

def migrate_clients(sb: Client, cursor):
    """Migra clientes do SQLite para Supabase"""
    cursor.execute("""
        SELECT id, nome, cpf, rg, telefone, email, profissao, 
               endereco, cidade, uf, cep, observacoes, ativo, criado_em
        FROM clientes
        WHERE ativo = 1
    """)
    
    clients = cursor.fetchall()
    migrated = 0
    
    for c in clients:
        try:
            # Montar address_json
            address_json = None
            if c[7] or c[8] or c[9] or c[10]:
                address_json = {
                    "logradouro": c[7],
                    "cidade": c[8],
                    "uf": c[9],
                    "cep": c[10]
                }
            
            data = {
                "id": str(uuid.uuid4()),
                "full_name": c[1],
                "document_id": c[2],  # CPF
                "email": c[5],
                "address_json": address_json
            }
            
            # Remover None values
            data = {k: v for k, v in data.items() if v is not None}
            
            resp = sb.table("clients").insert(data).execute()
            migrated += 1
            print(f"  ✓ {c[1]}")
            
        except Exception as e:
            print(f"  ✗ {c[1]}: {str(e)[:60]}")
    
    return migrated

def migrate_repositories(sb: Client, cursor):
    """Migra repositórios do SQLite para Supabase"""
    cursor.execute("""
        SELECT id, nome, owner, descricao, prioridade, ativo, criado_em
        FROM repositorios
        WHERE ativo = 1
    """)
    
    repos = cursor.fetchall()
    migrated = 0
    
    # Mapeamento de nodes (assumir padrão por owner)
    node_map = {
        "peixoto-ops": "Aspire",
        "p31x070": "Inspirion"
    }
    
    # Mapeamento de paths
    path_map = {
        "secretario-agente-lke": "/media/peixoto/Portable/secretario-agente-lke",
        "ekwrio": "/media/peixoto/Portable/ekwrio",
        "inv_sa_02": "/media/peixoto/Portable/lke_master_vault",
        "lke-processos-hub": "/home/peixoto/repos/lke-processos-hub",
        "caso-leonardo-tepedino": "/media/peixoto/Portable/caso-leonardo-tepedino",
        "case-diane-nicola-ops": "/media/peixoto/Portable/case-diane-nicola-ops",
        "ecosystem-dashboard": "/home/peixoto/repos/ecosystem-dashboard",
        "lke_master_vault": "/media/peixoto/Portable/lke_master_vault",
        "patterns-juridicos-v2": "/home/peixoto/repos/patterns-juridicos-v2",
        "caso-loreto-vivas": "/media/peixoto/Portable/caso-loreto-vivas"
    }
    
    for r in repos:
        try:
            repo_name = r[1]
            owner = r[2]
            
            data = {
                "id": str(uuid.uuid4()),
                "name": repo_name,
                "physical_path": path_map.get(repo_name, f"/media/peixoto/Portable/{repo_name}"),
                "node_name": node_map.get(owner, "Aspire"),
                "repo_type": "OBSIDIAN" if "caso" in repo_name or "case" in repo_name else "GITHUB",
                "metadata": {
                    "owner": owner,
                    "description": r[3],
                    "priority": r[4],
                    "sqlite_id": r[0]
                }
            }
            
            resp = sb.table("repositories").insert(data).execute()
            migrated += 1
            print(f"  ✓ {owner}/{repo_name}")
            
        except Exception as e:
            print(f"  ✗ {r[2]}/{r[1]}: {str(e)[:60]}")
    
    return migrated

def migrate_matters(sb: Client, cursor):
    """Migra processos do SQLite para Supabase"""
    cursor.execute("""
        SELECT id, numero, tribunal, classe, assunto, orgao_julgador,
               relator, origem, fase, situacao, data_distribuicao, 
               valor_causa, criado_em
        FROM processos
    """)
    
    matters = cursor.fetchall()
    migrated = 0
    
    for m in matters:
        try:
            # Montar case_summary com informações relevantes
            summary_parts = []
            if m[3]: summary_parts.append(f"Classe: {m[3]}")
            if m[4]: summary_parts.append(f"Assunto: {m[4]}")
            if m[5]: summary_parts.append(f"Órgão: {m[5]}")
            if m[6]: summary_parts.append(f"Relator: {m[6]}")
            
            data = {
                "id": str(uuid.uuid4()),
                "title": f"Processo {m[1]} - {m[2]}",
                "court_id": m[1],  # número CNJ
                "status": (m[9] or "ACTIVE").upper(),
                "case_summary": " | ".join(summary_parts) if summary_parts else None
            }
            
            # Remover None values
            data = {k: v for k, v in data.items() if v is not None}
            
            resp = sb.table("matters").insert(data).execute()
            migrated += 1
            print(f"  ✓ {m[1]} ({m[2]})")
            
        except Exception as e:
            print(f"  ✗ {m[1]}: {str(e)[:60]}")
    
    return migrated

def migrate_work_sessions(sb: Client, cursor):
    """Migra sessões de trabalho do SQLite para Supabase"""
    cursor.execute("""
        SELECT id, data, titulo, resumo_fabric, repositorio_id, tipo, 
               duracao_minutos, created_at
        FROM sessoes
    """)
    
    sessions = cursor.fetchall()
    migrated = 0
    
    for s in sessions:
        try:
            # Montar input_payload com informações da sessão
            input_payload = {
                "titulo": s[2],
                "tipo": s[5],
                "duracao_minutos": s[6],
                "data": s[1]
            }
            # Remover None values
            input_payload = {k: v for k, v in input_payload.items() if v is not None}
            
            data = {
                "id": str(uuid.uuid4()),
                "agent_name": "Hermes",
                "input_payload": input_payload,
                "output_summary": s[3],
                "execution_time_ms": (s[6] or 45) * 60 * 1000  # minutos → ms
            }
            
            # Remover None values do data
            data = {k: v for k, v in data.items() if v is not None}
            
            resp = sb.table("work_sessions").insert(data).execute()
            migrated += 1
            print(f"  ✓ Sessão {s[0]} - {s[2][:30] if s[2] else 'sem título'}")
            
        except Exception as e:
            print(f"  ✗ Sessão {s[0]}: {str(e)[:60]}")
    
    return migrated

def register_tools(sb: Client):
    """Registra ferramentas conhecidas"""
    tools = [
        {
            "name": "fabric",
            "command_prefix": "fabric --stream",
            "description": "AI augmentation patterns",
            "is_active": True
        },
        {
            "name": "hermes",
            "command_prefix": "hermes",
            "description": "Hermes Agent CLI",
            "is_active": True
        },
        {
            "name": "legal-commit",
            "command_prefix": "legal_commit",
            "description": "Semantic commits for legal documents",
            "is_active": True
        },
        {
            "name": "zotero-cli",
            "command_prefix": "zotero",
            "description": "Reference management",
            "is_active": True
        }
    ]
    
    migrated = 0
    for t in tools:
        try:
            resp = sb.table("tools").insert(t).execute()
            migrated += 1
            print(f"  ✓ {t['name']}")
        except Exception as e:
            if "duplicate" in str(e).lower():
                print(f"  ○ {t['name']} (já existe)")
            else:
                print(f"  ✗ {t['name']}: {str(e)[:50]}")
    
    return migrated

def register_credentials_refs(sb: Client):
    """Registra referências de credenciais (NÃO os valores)"""
    creds = [
        {
            "service_name": "GOOGLE_WORKSPACE",
            "credential_id": "client_secret.json",
            "metadata": {"location": "10_REFERENCIAS/credentials/"}
        },
        {
            "service_name": "SUPABASE",
            "credential_id": "env:SUPABASE_SERVICE_ROLE_KEY",
            "metadata": {"type": "service_role"}
        },
        {
            "service_name": "GITHUB",
            "credential_id": "env:GITHUB_TOKEN",
            "metadata": {"scope": "repo,workflow"}
        }
    ]
    
    migrated = 0
    for c in creds:
        try:
            resp = sb.table("vault_credentials").insert(c).execute()
            migrated += 1
            print(f"  ✓ {c['service_name']}")
        except Exception as e:
            if "duplicate" in str(e).lower():
                print(f"  ○ {c['service_name']} (já existe)")
            else:
                print(f"  ✗ {c['service_name']}: {str(e)[:50]}")
    
    return migrated

def main():
    print("=" * 60)
    print("MIGRAÇÃO: SQLite → Supabase")
    print("=" * 60)
    
    sb = get_supabase()
    conn = get_sqlite()
    cursor = conn.cursor()
    
    print("\n👤 Migrando CLIENTES...")
    clients_count = migrate_clients(sb, cursor)
    
    print("\n📁 Migrando REPOSITÓRIOS...")
    repos_count = migrate_repositories(sb, cursor)
    
    print("\n⚖️ Migrando PROCESSOS...")
    matters_count = migrate_matters(sb, cursor)
    
    print("\n📋 Migrando SESSÕES...")
    sessions_count = migrate_work_sessions(sb, cursor)
    
    print("\n🔧 Registrando FERRAMENTAS...")
    tools_count = register_tools(sb)
    
    print("\n🔐 Registrando CREDENCIAIS (refs)...")
    creds_count = register_credentials_refs(sb)
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("RESUMO DA MIGRAÇÃO:")
    print(f"  Clientes:     {clients_count:3d}")
    print(f"  Repositórios: {repos_count:3d}")
    print(f"  Processos:    {matters_count:3d}")
    print(f"  Sessões:      {sessions_count:3d}")
    print(f"  Ferramentas:  {tools_count:3d}")
    print(f"  Credenciais:  {creds_count:3d}")
    print("=" * 60)

if __name__ == "__main__":
    main()
