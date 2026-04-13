#!/usr/bin/env python3
"""
Validação completa do acesso ao Google Workspace
Executa testes em todos os serviços: Calendar, Tasks, Drive, Sheets, Gmail
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Paths absolutos
CREDENTIALS_DIR = Path('/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials')
TOKEN_PATH = CREDENTIALS_DIR / 'token.json'
CLIENT_SECRET_PATH = CREDENTIALS_DIR / 'client_secret.json'

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def print_header():
    print("=" * 60)
    print(" VALIDAÇÃO GOOGLE WORKSPACE")
    print("=" * 60)
    print()

def get_credentials():
    """Carrega credenciais do token"""
    from google.oauth2.credentials import Credentials
    
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH) as f:
            token_data = json.load(f)
        
        creds = Credentials(
            token=token_data.get('access_token'),
            refresh_token=token_data.get('refresh_token'),
            token_uri='https://oauth2.googleapis.com/token',
            client_id=None,  # Será preenchido se necessário
            client_secret=None,
            scopes=SCOPES
        )
        return creds
    return None

def test_calendar(creds):
    """Testa acesso ao Google Calendar"""
    try:
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=creds)
        
        # Listar próximos 5 eventos
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return True, f"{len(events)} eventos próximos", events
    except Exception as e:
        return False, str(e), None

def test_tasks(creds):
    """Testa acesso ao Google Tasks"""
    try:
        from googleapiclient.discovery import build
        service = build('tasks', 'v1', credentials=creds)
        
        # Listar tasklists
        result = service.tasklists().list().execute()
        lists = result.get('items', [])
        
        total_tasks = 0
        details = []
        for tasklist in lists[:3]:  # Limitar a 3 listas
            tasks = service.tasks().list(tasklist=tasklist['id']).execute()
            task_count = len(tasks.get('items', []))
            total_tasks += task_count
            details.append(f"{tasklist['title']} ({task_count})")
        
        return True, f"{len(lists)} listas, {total_tasks} tarefas", details
    except Exception as e:
        return False, str(e), None

def test_drive(creds):
    """Testa acesso ao Google Drive"""
    try:
        from googleapiclient.discovery import build
        service = build('drive', 'v3', credentials=creds)
        
        # Listar pastas
        results = service.files().list(
            q="mimeType='application/vnd.google-apps.folder' and trashed=false",
            pageSize=10,
            fields="files(id, name)"
        ).execute()
        
        folders = results.get('files', [])
        folder_names = [f['name'] for f in folders[:5]]
        return True, f"{len(folders)} pastas acessíveis", folder_names
    except Exception as e:
        return False, str(e), None

def test_sheets(creds):
    """Testa acesso ao Google Sheets"""
    try:
        from googleapiclient.discovery import build
        
        # Listar planilhas via Drive API
        drive_service = build('drive', 'v3', credentials=creds)
        
        results = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
            pageSize=10,
            fields="files(id, name)"
        ).execute()
        
        sheets = results.get('files', [])
        sheet_names = [s['name'] for s in sheets[:5]]
        return True, f"{len(sheets)} planilhas acessíveis", sheet_names
    except Exception as e:
        return False, str(e), None

def test_gmail(creds):
    """Testa acesso ao Gmail"""
    try:
        from googleapiclient.discovery import build
        service = build('gmail', 'v1', credentials=creds)
        
        # Listar mensagens não lidas
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=10
        ).execute()
        
        messages = results.get('messages', [])
        return True, f"{len(messages)} emails não lidos", messages
    except Exception as e:
        return False, str(e), None

def main():
    print_header()
    
    # Verificar se token existe
    if not TOKEN_PATH.exists():
        print("❌ Token não encontrado - execute auth_google_headless.py primeiro")
        return
    
    print(f"📁 Token: {TOKEN_PATH}")
    print()
    
    # Carregar credenciais
    creds = get_credentials()
    if not creds:
        print("❌ Não foi possível carregar token")
        return
    
    # Executar testes
    tests = [
        ("Calendar", test_calendar),
        ("Tasks", test_tasks),
        ("Drive", test_drive),
        ("Sheets", test_sheets),
        ("Gmail", test_gmail)
    ]
    
    results = []
    for i, (name, test_func) in enumerate(tests, 1):
        print(f"[{i}/5] {name}...", end=" ", flush=True)
        try:
            success, message, data = test_func(creds)
            if success:
                print(f"✅ OK ({message})")
                if data and isinstance(data, list) and len(data) > 0:
                    for item in data[:3]:
                        if isinstance(item, str):
                            print(f"      └─ {item}")
                results.append(True)
            else:
                print(f"❌ ERRO: {message}")
                results.append(False)
        except Exception as e:
            print(f"❌ EXCEÇÃO: {str(e)[:50]}")
            results.append(False)
    
    # Resumo
    print()
    print("=" * 60)
    if all(results):
        print("✅ TODOS OS SERVIÇOS ACESSÍVEIS")
        print("=" * 60)
        print()
        print("📝 Próximos passos:")
        print("   1. Implementar coleta automatizada")
        print("   2. Configurar cron job noturno")
        print("   3. Integrar com relatório diário")
    else:
        failed = sum(1 for r in results if not r)
        print(f"⚠️ {failed} SERVIÇO(S) COM PROBLEMAS")
        print("=" * 60)
    print()

if __name__ == '__main__':
    main()
