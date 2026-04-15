#!/usr/bin/env python3
"""
processador_inbox.py - Processa arquivos da inbox e atualiza Supabase

Lê cada arquivo.md em 00_INBOX/, extrai informações processuais,
atualiza matters no Supabase, e arquiva em 01_ARQUIVADAS/.

Uso:
    source venv/bin/activate
    python3 processador_inbox.py

Fluxo:
1. Lê arquivo .md da inbox
2. Extrai: número processo, partes, prazos, status, resumo
3. Busca matter no Supabase (ou cria se não existir)
4. Atualiza matter com novos dados
5. Arquiva em 01_ARQUIVADAS/ com status processado
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# Setup paths
BASE_DIR = Path(__file__).parent
INBOX = BASE_DIR / '00_INBOX'
ARQUIVADAS = BASE_DIR / '01_ARQUIVADAS'

# Carrega .env do caminho absoluto
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ .env carregado: {env_path}")
else:
    print(f"❌ .env não encontrado em {env_path}")
    sys.exit(1)

# Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
# Tenta múltiplas variações de chaves
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_SERVICE_ROLE_KEY') or os.getenv('SUPABASE_KEY')
print(f"🔗 Supabase URL: {SUPABASE_URL[:30]}...")
print(f"🔑 Chave carregada: {'✅' if SUPABASE_KEY else '❌'}")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Erro: SUPABASE_URL ou SUPABASE_KEY não configurados no .env")
    sys.exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def extrair_dados_arquivo(conteudo: str) -> dict:
    """Extrai dados processuais de um arquivo .md"""
    dados = {
        'numero_processo': None,
        'partes': [],
        'prazos': [],
        'status': 'DESCONHECIDO',
        'resumo': '',
        'urgencia': 'normal',
        'tags': []
    }
    
    # Extrai número do processo (padrão CNJ ou similar)
    match_proc = re.search(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})', conteudo)
    if match_proc:
        dados['numero_processo'] = match_proc.group(1)
    
    # Extrai partes (autor, réu, etc)
    for linha in conteudo.split('\n'):
        if 'autor' in linha.lower() or 'réu' in linha.lower() or 'requerente' in linha.lower():
            dados['partes'].append(linha.strip())
    
    # Extrai prazos
    for linha in conteudo.split('\n'):
        if 'prazo' in linha.lower() and 'dia' in linha.lower():
            dados['prazos'].append(linha.strip())
    
    # Detecta urgência
    if any(termo in conteudo.lower() for termo in ['urgente', 'liminar', 'tutela', 'prioridade']):
        dados['urgencia'] = 'urgente'
        dados['tags'].append('urgente')
    
    # Extrai resumo (primeiro parágrafo após título)
    match_resumo = re.search(r'#+\s+(.*?)\n\n(.*?)(?=\n#|\Z)', conteudo, re.DOTALL)
    if match_resumo:
        dados['resumo'] = match_resumo.group(2).strip()[:500]  # Limita a 500 chars
    
    # Extrai tags se houver
    match_tags = re.search(r'tags:\s*(.*?)\n', conteudo, re.IGNORECASE)
    if match_tags:
        dados['tags'] = [t.strip() for t in match_tags.group(1).split(',')]
    
    return dados

def buscar_matter(processo_id: str = None, termo_busca: str = None) -> dict:
    """Busca matter no Supabase por processo ou termo."""
    try:
        if processo_id:
            result = supabase.table('matters').select('*').eq('reference_number', processo_id).execute()
            if result.data:
                return result.data[0]
        
        if termo_busca:
            result = supabase.table('matters').select('*').ilike('%' + termo_busca[:50] + '%', column='title').execute()
            if result.data:
                return result.data[0]
        
        return None
    except Exception as e:
        print(f"⚠️  Erro ao buscar matter: {e}")
        return None

def criar_matter(dados: dict, titulo: str) -> dict:
    """Cria novo matter no Supabase."""
    try:
        matter_data = {
            'title': titulo[:200],
            'status': 'EM ANDAMENTO',
            'case_summary': dados.get('resumo', '')[:2000],
            'reference_number': dados.get('numero_processo'),
            'priority': 1 if dados.get('urgencia') == 'urgente' else 3,
            'tags': ','.join(dados.get('tags', []))
        }
        
        result = supabase.table('matters').insert(matter_data).execute()
        print(f"✅ Matter criado: {result.data[0]['id']}")
        return result.data[0]
    except Exception as e:
        print(f"❌ Erro ao criar matter: {e}")
        return None

def atualizar_matter(matter_id: str, dados: dict) -> bool:
    """Atualiza matter existente com novos dados."""
    try:
        update_data = {
            'case_summary': dados.get('resumo', '')[:2000],
            'priority': 1 if dados.get('urgencia') == 'urgente' else 3,
            'updated_at': datetime.now().isoformat()
        }
        
        if dados.get('tags'):
            update_data['tags'] = ','.join(dados.get('tags', []))
        
        result = supabase.table('matters').update(update_data).eq('id', matter_id).execute()
        print(f"✅ Matter atualizado: {matter_id}")
        return True
    except Exception as e:
        print(f"❌ Erro ao atualizar matter: {e}")
        return False

def arquivar_processado(arquivo_origem: Path, dados_processamento: dict) -> bool:
    """Move arquivo processado para pasta de arquivadas."""
    try:
        nome_final = f"PROCESSADO_{arquivo_origem.stem}.md"
        destino = ARQUIVADAS / nome_final
        
        # Adiciona cabeçalho de processamento
        conteudo_original = arquivo_origem.read_text(encoding='utf-8')
        cabecalho = f"""---
processado_em: {datetime.now().isoformat()}
matter_id: {dados_processamento.get('matter_id')}
status_supabase: {dados_processamento.get('status_supabase', 'desconhecido')}
---

{conteudo_original}
"""
        destino.write_text(cabecalho, encoding='utf-8')
        arquivo_origem.unlink()  # Remove original
        
        print(f"📁 Arquivado: {arquivo_origem.name} → {nome_final}")
        return True
    except Exception as e:
        print(f"❌ Erro ao arquivar {arquivo_origem}: {e}")
        return False

def processar_arquivo(arquivo: Path) -> dict:
    """Processa um único arquivo da inbox."""
    print(f"\n📄 Processando: {arquivo.name}")
    
    # Lê arquivo
    try:
        conteudo = arquivo.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Erro ao ler {arquivo}: {e}")
        return {'status': 'erro', 'erro': str(e)}
    
    # Extrai dados
    dados = extrair_dados_arquivo(conteudo)
    print(f"   Dados extraídos: processo={dados['numero_processo']}, urgência={dados['urgencia']}")
    
    # Gera título a partir do nome do arquivo
    titulo = arquivo.stem.replace('_', ' ').replace('ENTRADA_', '').replace('.md', '')[:200]
    
    # Busca ou cria matter
    matter = buscar_matter(dados.get('numero_processo'), titulo)
    
    resultado = {
        'arquivo': arquivo.name,
        'matter_id': None,
        'status_supabase': 'nao_criado',
        'dados': dados
    }
    
    if matter:
        print(f"   ✅ Matter encontrado: {matter['id']}")
        atualizar_matter(matter['id'], dados)
        resultado['matter_id'] = matter['id']
        resultado['status_supabase'] = 'atualizado'
    else:
        print(f"   ⚠️  Matter não encontrado, criando...")
        novo_matter = criar_matter(dados, titulo)
        if novo_matter:
            resultado['matter_id'] = novo_matter['id']
            resultado['status_supabase'] = 'criado'
    
    # Arquiva
    if resultado['status_supabase'] in ['atualizado', 'criado']:
        arquivar_processado(arquivo, resultado)
        resultado['status'] = 'sucesso'
    else:
        resultado['status'] = 'parcial'
    
    return resultado

def main():
    print("=" * 60)
    print("🔄 PROCESSADOR DE INBOX - SECRETÁRIO AGENTE LKE")
    print("=" * 60)
    print(f"Inbox: {INBOX}")
    print(f"Supabase: {SUPABASE_URL}")
    print("=" * 60)
    
    if not INBOX.exists():
        print("❌ Inbox não encontrada!")
        sys.exit(1)
    
    # Processa todos .md da inbox
    arquivos = list(INBOX.glob('*.md'))
    
    if not arquivos:
        print("📭 Inbox vazia!")
        return
    
    print(f"\n📬 Arquivos na inbox: {len(arquivos)}")
    
    resultados = []
    for arquivo in arquivos:
        resultado = processar_arquivo(arquivo)
        resultados.append(resultado)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DO PROCESSAMENTO")
    print("=" * 60)
    
    sucessos = sum(1 for r in resultados if r['status'] == 'sucesso')
    parciais = sum(1 for r in resultados if r['status'] == 'parcial')
    erros = sum(1 for r in resultados if r['status'] == 'erro')
    
    print(f"Sucesso: {sucessos}")
    print(f"Parcial: {parciais}")
    print(f"Erros: {erros}")
    
    print("\n✅ Processamento concluído!")

if __name__ == '__main__':
    main()
