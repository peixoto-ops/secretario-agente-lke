#!/usr/bin/env python3
"""
Secretário-Agente LKE - Coletor GitHub
Extrai informações de todos os repositórios do ecossistema peixoto-ops
"""

import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuração
DIAS_LOOKBACK = 7
OUTPUT_DIR = Path("/media/peixoto/Portable/secretario-agente-lke/40_DOCUMENTOS")
REPOS_PRIORITARIOS = [
    "peixoto-ops/inv_sa_02",
    "peixoto-ops/ekwrio",
    "peixoto-ops/caso-loreto-vivas",
    "peixoto-ops/case-diane-nicola-ops",
    "peixoto-ops/lke-processos-hub",
    "peixoto-ops/ecosystem-dashboard",
    "peixoto-ops/deep-research-lke",
    "peixoto-ops/lke_master_vault",
    "peixoto-ops/mrsa",
    "peixoto-ops/session-plans",
]

def run_gh_command(cmd):
    """Executa comando gh e retorna JSON"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout) if result.stdout.strip() else []
        return []
    except Exception as e:
        print(f"Erro: {e}")
        return []

def get_repo_commits(repo, days=7):
    """Obtém commits recentes de um repositório"""
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    cmd = f'gh api repos/{repo}/commits --paginate -q ".[] | select(.commit.author.date >= \"{since_date}\")"'
    # Simplificado para demo
    cmd = f'gh api repos/{repo}/commits -q ".[:10]"'
    return run_gh_command(cmd)

def get_repo_issues(repo):
    """Obtém issues abertas"""
    cmd = f'gh issue list -R {repo} --state open --json number,title,updatedAt -q ".[:5]"'
    return run_gh_command(cmd)

def analyze_project_health(repo, commits, issues):
    """Analisa saúde do projeto"""
    dias_sem_commit = 0
    if commits:
        last_commit_date = commits[0].get("commit", {}).get("author", {}).get("date", "")
        if last_commit_date:
            last = datetime.fromisoformat(last_commit_date.replace("Z", "+00:00"))
            dias_sem_commit = (datetime.now(last.tzinfo) - last).days
    
    return {
        "repositorio": repo,
        "commits_recentes": len(commits),
        "issues_abertas": len(issues),
        "dias_sem_commit": dias_sem_commit,
        "status": "ativo" if dias_sem_commit < 3 else ("atento" if dias_sem_commit < 7 else "latente")
    }

def main():
    """Executa coleta completa"""
    print("=== Secretário-Agente LKE - Coleta GitHub ===")
    print(f"Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    resultados = {
        "data_coleta": datetime.now().isoformat(),
        "projetos": []
    }
    
    for repo in REPOS_PRIORITARIOS:
        print(f"\nProcessando: {repo}")
        commits = get_repo_commits(repo)
        issues = get_repo_issues(repo)
        health = analyze_project_health(repo, commits, issues)
        resultados["projetos"].append(health)
        print(f"  Status: {health['status']} | Commits: {health['commits_recentes']} | Issues: {health['issues_abertas']}")
    
    # Salvar resultados
    output_file = OUTPUT_DIR / f"coleta_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Coleta salva em: {output_file}")
    return resultados

if __name__ == "__main__":
    main()
