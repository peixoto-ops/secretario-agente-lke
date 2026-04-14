#!/usr/bin/env python3
"""
Relatório Matinal Consolidado - Secretário-Agente LKE
Integra: Google Calendar, Google Tasks, GitHub, CNJ API
"""

import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import subprocess

# Paths
TOKEN_PATH = "/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/token.json"
CLIENT_SECRET_PATH = "/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/client_secret.json"

# Repositórios monitorados
REPOS = {
    "case-diane-nicola-ops": "peixoto-ops/case-diane-nicola-ops",
    "case-patricia-w-vs-cedae-serasa-ops": "peixoto-ops/case-patricia-w-vs-cedae-serasa-ops",
    "caso-leonardo-tepedino": "p31x070/caso-leonardo-tepedino",
    "inv_sa_02": "peixoto-ops/inv_sa_02",
    "lke-processos-hub": "peixoto-ops/lke-processos-hub",
    "ekwrio": "peixoto-ops/ekwrio",
    "secretario-agente-lke": "peixoto-ops/secretario-agente-lke"
}

def get_credentials(scopes):
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    with open(CLIENT_SECRET_PATH) as f:
        client_data = json.load(f)
    installed = client_data.get("installed", {})
    return Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=installed.get("client_id"),
        client_secret=installed.get("client_secret"),
        scopes=scopes
    )

def get_calendar_events():
    """Busca eventos do Google Calendar"""
    try:
        creds = get_credentials(["https://www.googleapis.com/auth/calendar"])
        service = build("calendar", "v3", credentials=creds)
        
        now = datetime.utcnow()
        end = now + timedelta(days=7)
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',
            timeMax=end.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    except Exception as e:
        return [{"error": str(e)}]

def get_tasks():
    """Busca tarefas do Google Tasks"""
    try:
        creds = get_credentials(["https://www.googleapis.com/auth/tasks"])
        service = build("tasks", "v1", credentials=creds)
        
        results = service.tasklists().list(maxResults=10).execute()
        lists = results.get("items", [])
        
        tasks_data = []
        for l in lists:
            tasks = service.tasks().list(tasklist=l["id"], maxResults=20, showCompleted=False).execute()
            items = tasks.get("items", [])
            tasks_data.append({
                "list": l["title"], 
                "tasks": [{"title": t["title"], "due": t.get("due", "")} for t in items]
            })
        return tasks_data
    except Exception as e:
        return [{"error": str(e)}]

def get_github_activity():
    """Busca última atividade dos repositórios"""
    activity = {}
    for name, repo in REPOS.items():
        try:
            result = subprocess.run(
                f'gh api repos/{repo}/commits -q ".[0] | {{date: .commit.author.date, message: .commit.message[:50]}}"',
                shell=True, capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                date_str = data.get("date", "")
                if date_str:
                    commit_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    days_ago = (datetime.now(commit_date.tzinfo) - commit_date).days
                    activity[name] = {
                        "date": date_str[:10],
                        "days_ago": days_ago,
                        "message": data.get("message", "")
                    }
        except:
            activity[name] = {"error": "não encontrado"}
    return activity

def format_report(calendar_events, tasks_data, github_activity):
    """Formata relatório consolidado"""
    now = datetime.now()
    
    lines = []
    lines.append("═" * 50)
    lines.append(f"RELATÓRIO MATINAL - {now.strftime('%d/%m/%Y')}")
    lines.append("═" * 50)
    
    # CALENDAR
    lines.append("")
    lines.append("📅 AGENDA")
    lines.append("-" * 50)
    if not calendar_events or calendar_events[0].get("error"):
        lines.append("  Nenhum evento ou erro de conexão")
    else:
        today = now.strftime('%Y-%m-%d')
        tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
        
        for event in calendar_events[:5]:
            start = event.get('start', {})
            date = start.get('dateTime', start.get('date', ''))[:10]
            time = start.get('dateTime', '')[11:16] if 'T' in start.get('dateTime', '') else ''
            
            if date == today:
                date_label = "HOJE"
            elif date == tomorrow:
                date_label = "AMANHÃ"
            else:
                date_label = date
            
            lines.append(f"  {date_label} {time} | {event.get('summary', 'Sem título')}")
    
    # TASKS
    lines.append("")
    lines.append("📋 TAREFAS PENDENTES")
    lines.append("-" * 50)
    total_tasks = 0
    today_tasks = 0
    overdue_tasks = 0
    
    today_str = now.strftime('%Y-%m-%d')
    
    for list_data in tasks_data:
        if list_data.get("error"):
            lines.append(f"  Erro: {list_data['error']}")
            continue
        
        list_name = list_data.get("list", "Lista")
        tasks = list_data.get("tasks", [])
        total_tasks += len(tasks)
        
        if tasks:
            lines.append(f"\n  📁 {list_name} ({len(tasks)} tarefas)")
            for t in tasks[:5]:
                due = t.get("due", "")
                if due:
                    due_date = due[:10]
                    if due_date < today_str:
                        status = "🔴 ATRASADA"
                        overdue_tasks += 1
                    elif due_date == today_str:
                        status = "🟡 HOJE"
                        today_tasks += 1
                    else:
                        status = f"📅 {due_date}"
                else:
                    status = "⚪ sem prazo"
                
                lines.append(f"    □ {t['title'][:35]}... {status}")
    
    lines.append("")
    lines.append(f"  Total: {total_tasks} tarefas | 🔴 {overdue_tasks} atrasadas | 🟡 {today_tasks} hoje")
    
    # GITHUB
    lines.append("")
    lines.append("📁 REPOSITÓRIOS")
    lines.append("-" * 50)
    
    sorted_repos = sorted(github_activity.items(), key=lambda x: x[1].get("days_ago", 999))
    
    for name, data in sorted_repos:
        if data.get("error"):
            lines.append(f"  {name}: ⚪ não encontrado")
        else:
            days = data.get("days_ago", 999)
            if days == 0:
                status = "🟢 ATIVO HOJE"
            elif days <= 2:
                status = f"🟡 {days}d"
            elif days <= 7:
                status = f"🟠 {days}d"
            else:
                status = f"🔴 {days}d"
            
            lines.append(f"  {name}: {status} | {data.get('message', '')[:30]}...")
    
    # ALERTAS
    lines.append("")
    lines.append("⚠️ ALERTAS")
    lines.append("-" * 50)
    
    alerts = []
    
    # Casos parados > 7 dias
    for name, data in github_activity.items():
        if data.get("days_ago", 0) > 7:
            alerts.append(f"  🔴 {name}: {data['days_ago']} dias sem movimento")
    
    # Tarefas atrasadas
    if overdue_tasks > 0:
        alerts.append(f"  🔴 {overdue_tasks} tarefas atrasadas")
    
    # Tarefas para hoje vs repo parado
    for list_data in tasks_data:
        for t in list_data.get("tasks", []):
            due = t.get("due", "")
            if due and due[:10] == today_str:
                # Verificar se tem repo correspondente parado
                task_lower = t["title"].lower()
                for repo_name in REPOS:
                    if repo_name.replace("-", " ").replace("_", " ")[:10] in task_lower.replace("-", " "):
                        if github_activity.get(repo_name, {}).get("days_ago", 0) > 2:
                            alerts.append(f"  ⚠️ Tarefa HOJE + Repo parado: {repo_name}")
    
    if alerts:
        lines.extend(alerts)
    else:
        lines.append("  ✅ Nenhum alerta")
    
    lines.append("")
    lines.append("═" * 50)
    
    return "\n".join(lines)

def main():
    print("Coletando dados...")
    
    calendar_events = get_calendar_events()
    tasks_data = get_tasks()
    github_activity = get_github_activity()
    
    report = format_report(calendar_events, tasks_data, github_activity)
    
    print(report)
    
    # Salvar relatório
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_path = f"/media/peixoto/Portable/secretario-agente-lke/40_DOCUMENTOS/relatorio_{timestamp}.md"
    
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Relatório salvo: {output_path}")

if __name__ == "__main__":
    main()
