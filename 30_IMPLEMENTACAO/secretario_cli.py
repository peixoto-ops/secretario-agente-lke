#!/usr/bin/env python3
"""
Secretário-Agente LKE - CLI para consultas e registro
Banco de dados de memória operacional
"""

import sqlite3
import argparse
import subprocess
import json
import re
from datetime import datetime, date
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "10_REFERENCIAS" / "secretario.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def extrair_numero_processo(texto):
    """Extrai número CNJ de processo do texto"""
    # Padrão CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO
    pattern = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
    match = re.search(pattern, texto)
    return match.group(0) if match else None

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

def cmd_add_repo(args):
    """Cadastra novo repositório"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar se já existe
    cursor.execute("SELECT id FROM repositorios WHERE nome = ?", (args.nome,))
    if cursor.fetchone():
        print(f"❌ Repositório '{args.nome}' já cadastrado")
        conn.close()
        return
    
    cursor.execute("""
        INSERT INTO repositorios (nome, owner, descricao, prioridade, ativo)
        VALUES (?, ?, ?, ?, 1)
    """, (args.nome, args.owner, args.descricao, args.prioridade))
    
    repo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Repositório cadastrado: ID {repo_id}")
    print(f" Nome: {args.nome}")
    print(f" Owner: {args.owner}")
    if args.descricao:
        print(f" Descrição: {args.descricao}")

def cmd_processo(args):
    """Cadastra ou consulta processo"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if hasattr(args, 'add') and args.add:
        # Cadastrar novo processo
        cursor.execute("SELECT id FROM processos WHERE numero = ?", (args.numero,))
        if cursor.fetchone():
            print(f"❌ Processo '{args.numero}' já cadastrado")
            conn.close()
            return
        
        cursor.execute("""
            INSERT INTO processos (numero, tribunal, classe, assunto, orgao_julgador, 
                                   relator, origem, fase, situacao, data_distribuicao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (args.numero, args.tribunal, args.classe, args.assunto, args.orgao,
              args.relator, args.origem, args.fase, args.situacao, args.data_dist))
        
        proc_id = cursor.lastrowid
        conn.commit()
        print(f"✅ Processo cadastrado: ID {proc_id}")
        print(f" Número: {args.numero}")
        print(f" Tribunal: {args.tribunal}")
        conn.close()
        return
        # Vincular processo a repositório
        cursor.execute("SELECT id FROM processos WHERE numero = ?", (args.numero,))
        proc = cursor.fetchone()
        if not proc:
            print(f"❌ Processo '{args.numero}' não encontrado")
            conn.close()
            return
        
        cursor.execute("SELECT id FROM repositorios WHERE nome = ?", (args.repo,))
        repo = cursor.fetchone()
        if not repo:
            print(f"❌ Repositório '{args.repo}' não encontrado")
            conn.close()
            return
        
        try:
            cursor.execute("""
                INSERT INTO vinculos_repositorio_processo (repositorio_id, processo_id, papel)
                VALUES (?, ?, ?)
            """, (repo[0], proc[0], args.papel or 'principal'))
            conn.commit()
            print(f"✅ Processo vinculado ao repositório")
        except sqlite3.IntegrityError:
            print(f"⚠️ Vínculo já existe")
        
        conn.close()
        return
    
    if args.numero:
        # Consultar processo específico
        cursor.execute("""
            SELECT id, numero, tribunal, classe, assunto, orgao_julgador, 
                   relator, fase, situacao, data_distribuicao
            FROM processos WHERE numero = ?
        """, (args.numero,))
        proc = cursor.fetchone()
        
        if not proc:
            print(f"❌ Processo não encontrado: {args.numero}")
            conn.close()
            return
        
        print(f"\n📋 PROCESSO: {proc[1]}")
        print("=" * 60)
        print(f" Tribunal: {proc[2]}")
        if proc[3]: print(f" Classe: {proc[3]}")
        if proc[4]: print(f" Assunto: {proc[4]}")
        if proc[5]: print(f" Órgão: {proc[5]}")
        if proc[6]: print(f" Relator: {proc[6]}")
        if proc[7]: print(f" Fase: {proc[7]}")
        if proc[8]: print(f" Situação: {proc[8]}")
        if proc[9]: print(f" Distribuição: {proc[9]}")
        
        # Buscar clientes vinculados
        cursor.execute("""
            SELECT c.nome, vcp.qualidade, vcp.posicao
            FROM vinculos_cliente_processo vcp
            JOIN clientes c ON vcp.cliente_id = c.id
            WHERE vcp.processo_id = ?
        """, (proc[0],))
        
        clientes = cursor.fetchall()
        if clientes:
            print("\n CLIENTES:")
            for c in clientes:
                print(f" • {c[0]} ({c[1]}) - {c[2] or 'N/A'}")
        
        # Buscar prazos
        cursor.execute("""
            SELECT descricao, data_limite, status, tipo
            FROM prazos WHERE processo_id = ?
            ORDER BY data_limite
        """, (proc[0],))
        
        prazos = cursor.fetchall()
        if prazos:
            print("\n PRAZOS:")
            for p in prazos:
                status_icon = "✓" if p[2] == "cumprido" else "⏰" if p[2] == "pendente" else "❌"
                print(f" {status_icon} {p[0]}: {p[1]} ({p[3]})")
        
        conn.close()
        return
    
    # Listar processos
    cursor.execute("""
        SELECT p.numero, p.tribunal, p.classe, p.situacao,
               GROUP_CONCAT(c.nome, ', ') as clientes
        FROM processos p
        LEFT JOIN vinculos_cliente_processo vcp ON p.id = vcp.processo_id
        LEFT JOIN clientes c ON vcp.cliente_id = c.id
        GROUP BY p.id
        ORDER BY p.numero
    """)
    
    print("\n📋 PROCESSOS CADASTRADOS")
    print("=" * 60)
    for row in cursor.fetchall():
        situacao = row[3] or "N/A"
        clientes = row[4] or "Sem clientes"
        print(f" {row[0]} [{row[1]}] - {row[2] or 'N/A'}")
        print(f"  Situação: {situacao} | Clientes: {clientes}")
    
    conn.close()

def cmd_cliente(args):
    """Cadastra ou consulta cliente"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if hasattr(args, 'add') and args.add:
        # Cadastrar novo cliente
        if args.cpf:
            cursor.execute("SELECT id FROM clientes WHERE cpf = ?", (args.cpf,))
            if cursor.fetchone():
                print(f"❌ Cliente com CPF '{args.cpf}' já cadastrado")
                conn.close()
                return
        
        cursor.execute("""
            INSERT INTO clientes (nome, cpf, rg, telefone, email, profissao, 
                                  endereco, cidade, uf, cep, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (args.nome, args.cpf, args.rg, args.telefone, args.email, args.profissao,
              args.endereco, args.cidade, args.uf, args.cep, args.obs))
        
        cli_id = cursor.lastrowid
        conn.commit()
        print(f"✅ Cliente cadastrado: ID {cli_id}")
        print(f" Nome: {args.nome}")
    if args.cpf: print(f" CPF: {args.cpf}")
    conn.close()
    return
    
    if hasattr(args, 'vincular') and args.vincular:
        conn = get_connection()
        cursor = conn.cursor()
        # Vincular cliente a processo
        cursor.execute("SELECT id FROM clientes WHERE id = ?", (args.cliente_id,))
        cli = cursor.fetchone()
        if not cli:
            print(f"❌ Cliente ID {args.cliente_id} não encontrado")
            conn.close()
            return
        
        cursor.execute("SELECT id FROM processos WHERE numero = ?", (args.processo,))
        proc = cursor.fetchone()
        if not proc:
            print(f"❌ Processo '{args.processo}' não encontrado")
            conn.close()
            return
        
        try:
            cursor.execute("""
                INSERT INTO vinculos_cliente_processo (cliente_id, processo_id, qualidade, posicao)
                VALUES (?, ?, ?, ?)
            """, (cli[0], proc[0], args.qualidade, args.posicao))
            conn.commit()
            print(f"✅ Cliente vinculado ao processo")
        except sqlite3.IntegrityError:
            print(f"⚠️ Vínculo já existe")
        
    conn.close()
    return
    
    if hasattr(args, 'nome') and args.nome or hasattr(args, 'cpf') and args.cpf:
        conn = get_connection()
        cursor = conn.cursor()
        # Buscar cliente específico
        if args.cpf:
            cursor.execute("SELECT * FROM clientes WHERE cpf = ?", (args.cpf,))
        else:
            cursor.execute("SELECT * FROM clientes WHERE nome LIKE ?", (f"%{args.nome}%",))
        
        cli = cursor.fetchone()
        if not cli:
            print(f"❌ Cliente não encontrado")
            conn.close()
            return
        
        cols = ['id', 'nome', 'cpf', 'rg', 'nacionalidade', 'estado_civil', 
                'profissao', 'data_nascimento', 'email', 'telefone', 
                'endereco', 'cidade', 'uf', 'cep', 'observacoes', 'preferencia_contato', 'ativo']
        cli_dict = dict(zip(cols, cli))
        
        print(f"\n👤 CLIENTE: {cli_dict['nome']}")
        print("=" * 60)
        print(f" ID: {cli_dict['id']}")
        if cli_dict['cpf']: print(f" CPF: {cli_dict['cpf']}")
        if cli_dict['telefone']: print(f" Telefone: {cli_dict['telefone']}")
        if cli_dict['email']: print(f" Email: {cli_dict['email']}")
        if cli_dict['profissao']: print(f" Profissão: {cli_dict['profissao']}")
        if cli_dict['endereco']: print(f" Endereço: {cli_dict['endereco']}, {cli_dict['cidade']}/{cli_dict['uf']}")
        
        # Buscar processos vinculados
        cursor.execute("""
            SELECT p.numero, p.tribunal, vcp.qualidade, vcp.posicao
            FROM vinculos_cliente_processo vcp
            JOIN processos p ON vcp.processo_id = p.id
            WHERE vcp.cliente_id = ?
        """, (cli_dict['id'],))
        
        processos = cursor.fetchall()
        if processos:
            print("\n PROCESSOS:")
            for p in processos:
                print(f" • {p[0]} [{p[1]}] - {p[2]} ({p[3]})")
        
    conn.close()
    return
    
    # Fechar conexão inicial antes do bloco de listagem
    conn.close()
    
    # Listar clientes
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, cpf, telefone, 
               (SELECT COUNT(*) FROM vinculos_cliente_processo vcp WHERE vcp.cliente_id = c.id) as processos
        FROM clientes c
        WHERE ativo = 1
        ORDER BY nome
    """)
    
    print("\n👤 CLIENTES CADASTRADOS")
    print("=" * 60)
    for row in cursor.fetchall():
        print(f" [{row[0]}] {row[1]} | CPF: {row[2] or 'N/A'} | Tel: {row[3] or 'N/A'} | {row[4]} processo(s)")
    
    conn.close()

def cmd_prazo(args):
    """Cadastra ou consulta prazos"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if args.add:
        # Adicionar prazo
        processo_id = None
        if args.processo:
            cursor.execute("SELECT id FROM processos WHERE numero = ?", (args.processo,))
            proc = cursor.fetchone()
            if proc:
                processo_id = proc[0]
        
        cursor.execute("""
            INSERT INTO prazos (processo_id, descricao, data_limite, hora_limite, tipo, prioridade, status, responsavel)
            VALUES (?, ?, ?, ?, ?, ?, 'pendente', ?)
        """, (processo_id, args.descricao, args.data, args.hora, args.tipo or 'processual', args.prioridade or 5, args.responsavel))
        
        conn.commit()
        print(f"✅ Prazo cadastrado: {args.descricao}")
        print(f" Data limite: {args.data} {args.hora or ''}")
        conn.close()
        return
    
    if args.cumprir:
        cursor.execute("UPDATE prazos SET status = 'cumprido', cumprido_em = CURRENT_TIMESTAMP WHERE id = ?", (args.cumprir,))
        conn.commit()
        print(f"✅ Prazo {args.cumprir} marcado como cumprido")
        conn.close()
        return
    
    # Listar prazos pendentes
    cursor.execute("""
        SELECT p.id, p.descricao, p.data_limite, p.hora_limite, p.tipo, 
               pr.numero as processo, p.responsavel,
               JULIANDAY(p.data_limite) - JULIANDAY('now') as dias_restantes
        FROM prazos p
        LEFT JOIN processos pr ON p.processo_id = pr.id
        WHERE p.status = 'pendente'
        ORDER BY p.data_limite
    """)
    
    print("\n⏰ PRAZOS PENDENTES")
    print("=" * 60)
    
    hoje = date.today()
    for row in cursor.fetchall():
        prazo_id, desc, data_lim, hora, tipo, proc, resp, dias = row
        dias = dias or 0
        
        if dias < 0:
            urgencia = "🔴 VENCIDO"
        elif dias < 3:
            urgencia = "🟠 URGENTE"
        elif dias < 7:
            urgencia = "🟡 PRÓXIMO"
        else:
            urgencia = "🟢 NORMAL"
        
        data_fmt = f"{data_lim} {hora or ''}".strip()
        proc_fmt = f"[{proc}]" if proc else ""
        resp_fmt = f"({resp})" if resp else ""
        
        print(f" [{prazo_id}] {desc[:40]}")
        print(f"     {data_fmt} | {tipo} | {urgencia} {proc_fmt} {resp_fmt}")
        print(f"     Dias restantes: {int(dias)}")
        print()
    
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
    
    # Comando: add-repo
    p_add_repo = subparsers.add_parser("add-repo", help="Cadastra repositório")
    p_add_repo.add_argument("nome", help="Nome do repositório")
    p_add_repo.add_argument("owner", help="Owner do repositório")
    p_add_repo.add_argument("--descricao", help="Descrição")
    p_add_repo.add_argument("--prioridade", type=int, default=5, help="Prioridade (1-5)")
    p_add_repo.set_defaults(func=cmd_add_repo)
    
    # Comando: processo
    p_processo = subparsers.add_parser("processo", help="Consulta/cadastra processos")
    p_processo.add_argument("--numero", help="Número CNJ do processo")
    p_processo.add_argument("--add", action="store_true", help="Cadastrar novo processo")
    p_processo.add_argument("--tribunal", help="Tribunal")
    p_processo.add_argument("--classe", help="Classe processual")
    p_processo.add_argument("--assunto", help="Assunto")
    p_processo.add_argument("--orgao", help="Órgão julgador")
    p_processo.add_argument("--relator", help="Relator")
    p_processo.add_argument("--origem", help="Origem")
    p_processo.add_argument("--fase", help="Fase atual")
    p_processo.add_argument("--situacao", help="Situação")
    p_processo.add_argument("--data-dist", help="Data distribuição")
    p_processo.add_argument("--vincular", action="store_true", help="Vincular a repositório")
    p_processo.add_argument("--repo", help="Repositório para vínculo")
    p_processo.add_argument("--papel", help="Papel do vínculo")
    p_processo.set_defaults(func=cmd_processo)
    
    # Comando: cliente
    p_cliente = subparsers.add_parser("cliente", help="Consulta/cadastra clientes")
    p_cliente.add_argument("--add", action="store_true", help="Cadastrar novo cliente")
    p_cliente.add_argument("--nome", help="Nome do cliente (busca ou cadastro)")
    p_cliente.add_argument("--cpf", help="CPF do cliente")
    p_cliente.add_argument("--rg", help="RG do cliente")
    p_cliente.add_argument("--telefone", help="Telefone")
    p_cliente.add_argument("--email", help="Email")
    p_cliente.add_argument("--profissao", help="Profissão")
    p_cliente.add_argument("--endereco", help="Endereço")
    p_cliente.add_argument("--cidade", help="Cidade")
    p_cliente.add_argument("--uf", help="UF")
    p_cliente.add_argument("--cep", help="CEP")
    p_cliente.add_argument("--obs", help="Observações")
    p_cliente.add_argument("--vincular", action="store_true", help="Vincular a processo")
    p_cliente.add_argument("--cliente-id", type=int, help="ID do cliente")
    p_cliente.add_argument("--processo", help="Número do processo")
    p_cliente.add_argument("--qualidade", help="Qualidade no processo")
    p_cliente.add_argument("--posicao", help="Posição processual")
    p_cliente.set_defaults(func=cmd_cliente)
    
    # Comando: prazo
    p_prazo = subparsers.add_parser("prazo", help="Gestão de prazos")
    p_prazo.add_argument("--add", action="store_true", help="Adicionar prazo")
    p_prazo.add_argument("--processo", help="Número do processo")
    p_prazo.add_argument("--descricao", help="Descrição do prazo")
    p_prazo.add_argument("--data", help="Data limite (YYYY-MM-DD)")
    p_prazo.add_argument("--hora", help="Hora limite")
    p_prazo.add_argument("--tipo", help="Tipo (processual, administrativo, interno)")
    p_prazo.add_argument("--prioridade", type=int, help="Prioridade (1-5)")
    p_prazo.add_argument("--responsavel", help="Responsável")
    p_prazo.add_argument("--cumprir", type=int, help="ID do prazo a marcar cumprido")
    p_prazo.set_defaults(func=cmd_prazo)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
