#!/usr/bin/env python3
"""Verifica tarefas do Google Tasks - Versão corrigida"""

import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/tasks"]
TOKEN_PATH = "/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/token.json"
CLIENT_SECRET_PATH = "/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/client_secret.json"

def main():
    # Carregar token
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    
    # Carregar client_id e client_secret do client_secret.json
    with open(CLIENT_SECRET_PATH) as f:
        client_data = json.load(f)
    
    installed = client_data.get("installed", {})
    
    creds = Credentials(
        token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=installed.get("client_id"),
        client_secret=installed.get("client_secret"),
        scopes=SCOPES
    )
    
    service = build("tasks", "v1", credentials=creds)
    
    results = service.tasklists().list(maxResults=10).execute()
    lists = results.get("items", [])
    
    print("=" * 50)
    print("GOOGLE TASKS - TAREFAS PENDENTES")
    print("=" * 50)
    
    tasks_data = []
    for l in lists:
        tasks = service.tasks().list(tasklist=l["id"], maxResults=20, showCompleted=False).execute()
        items = tasks.get("items", [])
        
        print(f"\n📋 {l['title']} ({len(items)} tarefas)")
        print("-" * 40)
        
        for t in items[:10]:
            title = t.get("title", "Sem título")
            due = t.get("due", "sem prazo")
            if due and due != "sem prazo":
                # Formatar data
                due = due[:10]  # Pegar apenas YYYY-MM-DD
            print(f"  □ {title}")
            if due and due != "sem prazo":
                print(f"    📅 {due}")
        
        tasks_data.append({
            "list": l["title"], 
            "count": len(items),
            "tasks": [
                {"title": t["title"], "due": t.get("due", "sem prazo")} 
                for t in items[:10]
            ]
        })
    
    print("\n" + "=" * 50)
    total = sum(t["count"] for t in tasks_data)
    print(f"TOTAL: {total} tarefas pendentes em {len(lists)} listas")
    print("=" * 50)

if __name__ == "__main__":
    main()
