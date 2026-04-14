#!/usr/bin/env python3
"""
Secretário-Agente LKE - CLI para consultas e registro
Banco de dados de memória operacional
"""

import sqlite3
import argparse
import subprocess
import json
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "10_REFERENCIAS" / "secretario.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def cmd_repos(args):
    """Lista repositórios monitorados"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if args.ativos:
        cursor.execute("""
            SELECT nome, owner, descricao, prioridade 
            FROM repositorios 
            WHERE ativo = 1 
            ORDER BY prioridade, nome
        """)
    else:
        cursor.execute("""
            SELECT nome, owner, descricao, prioridade, ativo 
            FROM repositorios 
            ORDER BY prioridade, nome
        """)
    
    print("\n📁 REPOSITÓRIOS MONITORADOS")
    print("=" * 60)
    for row in cursor.fetchall():
        if len(row) > 4:
            status = "✓" if row[4] else "○"
            prio = f"[{row[3]}]"
        else:
            status = "✓"
            prio = ""
        print(f"  {status} {prio} {row[1]}/{row[0]}")
        if row[2]:
            print(f"      {row[2][:50]}...")
    conn.close()

def cmd_sessao(args):
    """Registra nova sessão de trabalho"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Buscar repo_id se especificado
    repo_id = None
    if args.repo:
        cursor.execute("SELECT id FROM repositorios WHERE nome = ?", (args.repo,))
        result = cursor.fetchone()
        if result:
            repo_id = result[0]
    
    cursor.execute("""
        INSERT INTO sessoes (data, titulo, resumo_fabric, repositorio_id, tipo, duracao_minutos)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date.today().isoformat(),
        args.titulo,
        args.resumo,
        repo_id,
        args.tipo,
        args.duracao
    ))
    
    sessao_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Sessão registrada: ID {sessao_id}")
    print(f"   Data: {date.today()}")
    print(f"   Título: {args.titulo}")
    if args.resumo:
        print(f"   Resumo: {args.resumo[:80]}...")

def cmd_log(args):
    """Registra atividade (commit, push, etc)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Buscar repo_id
    cursor.execute("SELECT id FROM repositorios WHERE nome = ?", (args.repo,))
    result = cursor.fetchone()
    if not result:
        print(f"❌ Repositório '{args.repo}' não encontrado")
        conn.close()
        return
    
    repo_id = result[0]
    
    cursor.execute("""
        INSERT INTO atividade_logs (repositorio_id, tipo, mensagem, hash_git, autor, metadados)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        repo_id,
        args.tipo,
        args.mensagem,
        args.hash,
        args.autor or "hermes",
        args.meta
    ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Atividade registrada: {args.tipo} em {args.repo}")

def cmd_resumo(args):
    """Gera resumo via Fabric e registra"""
    texto = args.texto
    if not texto:
        # Lê de stdin
        import sys
        texto = sys.stdin.read()
    
    if not texto.strip():
        print("❌ Forneça texto via --texto ou pipe")
        return
    
    # Chamar Fabric
    try:
        result = subprocess.run(
            ["fabric", "-p", "summarize_bottom_up", "-s", "-g=pt-br"],
            input=texto,
            capture_output=True,
            text=True,
            timeout=30
        )
        resumo = result.stdout.strip()
        
        if args.registrar:
            # Registrar no banco
            conn = get_connection()
            cursor = conn.cursor()
            
            # Buscar ou criar sessão de hoje
            cursor.execute("""
                SELECT id FROM sessoes WHERE data = ? ORDER BY id DESC LIMIT 1
            """, (date.today().isoformat(),))
            
            sessao = cursor.fetchone()
            sessao_id = sessao[0] if sessao else None
            
            if sessao_id:
                cursor.execute("""
                    UPDATE sessoes SET resumo_fabric = ? WHERE id = ?
                """, (resumo, sessao_id))
                conn.commit()
                print(f"✅ Resumo registrado na sessão {sessao_id}")
            
            conn.close()
        
        print("\n📝 RESUMO FABRIC:")
        print("=" * 60)
        print(resumo)
        
    except FileNotFoundError:
        print("❌ Fabric não encontrado. Instale com: pip install fabric")
    except subprocess.TimeoutExpired:
        print("❌ Timeout ao chamar Fabric")

def cmd_query(args):
    """Executa query SQL direta"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(args.sql)
        
        if args.sql.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description] if cursor.description else []
            
            if args.json:
                result = [dict(zip(cols, row)) for row in rows]
                print(json.dumps(result, indent=2, default=str))
            else:
                if cols:
                    print(" | ".join(cols))
                    print("-" * 80)
                for row in rows[:50]:  # Limita output
                    print(" | ".join(str(c) for c in row))
                if len(rows) > 50:
                    print(f"... e mais {len(rows) - 50} linhas")
        else:
            conn.commit()
            print(f"✅ Query executada. Linhas afetadas: {cursor.rowcount}")
            
    except sqlite3.Error as e:
        print(f"❌ Erro SQL: {e}")
    finally:
        conn.close()

def cmd_status(args):
    """Mostra status geral do sistema"""
    conn = get_connection()
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("📊 STATUS SECRETÁRIO-AGENTE LKE")
    print("=" * 60)
    
    # Estatísticas
    cursor.execute("SELECT COUNT(*) FROM repositorios WHERE ativo = 1")
    repos_ativos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM sessoes")
    total_sessoes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM atividade_logs")
    total_logs = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM sessoes 
        WHERE data >= date('now', '-7 days')
    """)
    sessoes_semana = cursor.fetchone()[0]
    
    print(f"\n  📁 Repositórios ativos: {repos_ativos}")
    print(f"  📅 Total de sessões: {total_sessoes}")
    print(f"  📝 Atividades logadas: {total_logs}")
    print(f"  ⏰ Sessões esta semana: {sessoes_semana}")
    
    # Últimas sessões
    cursor.execute("""
        SELECT data, titulo, tipo, r.nome 
        FROM sessoes s 
        LEFT JOIN repositorios r ON s.repositorio_id = r.id
        ORDER BY data DESC LIMIT 5
    """)
    
    print("\n  📋 ÚLTIMAS SESSÕES:")
    for row in cursor.fetchall():
        repo = f"({row[3]})" if row[3] else ""
        print(f"     {row[0]} [{row[2]}] {row[1][:30]}... {repo}")
    
    # Atividade recente
    cursor.execute("""
        SELECT r.nome, al.tipo, al.mensagem, al.timestamp 
        FROM atividade_logs al
        JOIN repositorios r ON al.repositorio_id = r.id
        ORDER BY al.timestamp DESC LIMIT 5
    """)
    
    print("\n  🔧 ATIVIDADE RECENTE:")
    for row in cursor.fetchall():
        msg = row[2][:30] if row[2] else ""
        print(f"     {row[0]}: [{row[1]}] {msg}...")
    
    print("\n" + "=" * 60)
    conn.close()

def main():
    parser = argparse.ArgumentParser(
        description="Secretário-Agente LKE - CLI de memória operacional"
    )
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")
    
    # Comando: repos
    p_repos = subparsers.add_parser("repos", help="Lista repositórios")
    p_repos.add_argument("--ativos", action="store_true", help="Só ativos")
    p_repos.set_defaults(func=cmd_repos)
    
    # Comando: sessao
    p_sessao = subparsers.add_parser("sessao", help="Registra sessão")
    p_sessao.add_argument("--titulo", required=True, help="Título da sessão")
    p_sessao.add_argument("--repo", help="Repositório relacionado")
    p_sessao.add_argument("--tipo", default="livre", help="Tipo (T1.1, T1.2, etc)")
    p_sessao.add_argument("--duracao", type=int, default=45, help="Duração em minutos")
    p_sessao.add_argument("--resumo", help="Resumo da sessão")
    p_sessao.set_defaults(func=cmd_sessao)
    
    # Comando: log
    p_log = subparsers.add_parser("log", help="Registra atividade")
    p_log.add_argument("--repo", required=True, help="Repositório")
    p_log.add_argument("--tipo", required=True, help="Tipo (commit, push, etc)")
    p_log.add_argument("--mensagem", required=True, help="Mensagem")
    p_log.add_argument("--hash", help="Hash git")
    p_log.add_argument("--autor", help="Autor")
    p_log.add_argument("--meta", help="Metadados JSON")
    p_log.set_defaults(func=cmd_log)
    
    # Comando: resumo
    p_resumo = subparsers.add_parser("resumo", help="Gera resumo via Fabric")
    p_resumo.add_argument("--texto", help="Texto para resumir")
    p_resumo.add_argument("--registrar", action="store_true", help="Registra na sessão atual")
    p_resumo.set_defaults(func=cmd_resumo)
    
    # Comando: query
    p_query = subparsers.add_parser("query", help="Executa query SQL")
    p_query.add_argument("sql", help="Query SQL")
    p_query.add_argument("--json", action="store_true", help="Output em JSON")
    p_query.set_defaults(func=cmd_query)
    
    # Comando: status
    p_status = subparsers.add_parser("status", help="Mostra status geral")
    p_status.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
