#!/usr/bin/env python3
"""
Validação completa do acesso ao Google Workspace
Executa testes em todos os serviços: Calendar, Tasks, Drive, Sheets, Gmail
"""

import os
import sys

# Adicionar path do credentials
CREDENTIALS_DIR = '/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials'
TOKEN_PATH = os.path.join(CREDENTIALS_DIR, 'token.json')
CLIENT_SECRET_PATH = os.path.join(CREDENTIALS_DIR, 'client_secret.json')

SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def print_header():
    print("═" * 41)
    print("   VALIDAÇÃO GOOGLE WORKSPACE")
    print("═" * 41)
    print()

def check_credentials():
    """Verifica se as credenciais existem"""
    if not os.path.exists(CLIENT_SECRET_PATH):
        print("❌ client_secret.json não encontrado")
        return False
    if not os.path.exists(TOKEN_PATH):
        print("⚠️  token.json não encontrado - execute auth_google.py primeiro")
        return False
    return True

def get_credentials():
    """Carrega credenciais do token"""
    from google.oauth2.credentials import Credentials
    
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        return creds
    return None

def test_calendar(creds):
    """Testa acesso ao Google Calendar"""
    try:
        from googleapiclient.discovery import build
        service = build('calendar', 'v3', credentials=creds)
        
        # Listar próximos 5 eventos
        events_result = service.events().list(
            calendarId='primary',
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return True, f"{len(events)} eventos encontrados"
    except Exception as e:
        return False, str(e)

def test_tasks(creds):
    """Testa acesso ao Google Tasks"""
    try:
        from googleapiclient.discovery import build
        service = build('tasks', 'v1', credentials=creds)
        
        # Listar tasklists
        result = service.tasklists().list().execute()
        lists = result.get('items', [])
        
        total_tasks = 0
        for tasklist in lists:
            tasks = service.tasks().list(tasklist=tasklist['id']).execute()
            total_tasks += len(tasks.get('items', []))
        
        return True, f"{len(lists)} listas, {total_tasks} tarefas"
    except Exception as e:
        return False, str(e)

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
        return True, f"{len(folders)} pastas acessíveis"
    except Exception as e:
        return False, str(e)

def test_sheets(creds):
    """Testa acesso ao Google Sheets"""
    try:
        from googleapiclient.discovery import build
        service = build('sheets', 'v4', credentials=creds)
        
        # Listar planilhas via Drive API
        from googleapiclient.discovery import build as drive_build
        drive_service = drive_build('drive', 'v3', credentials=creds)
        
        results = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
            pageSize=10,
            fields="files(id, name)"
        ).execute()
        
        sheets = results.get('files', [])
        return True, f"{len(sheets)} planilhas acessíveis"
    except Exception as e:
        return False, str(e)

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
        return True, f"{len(messages)} emails não lidos"
    except Exception as e:
        return False, str(e)

def main():
    print_header()
    
    # Verificar credenciais
    if not check_credentials():
        print("\n❌ Validação falhou - credenciais não configuradas")
        return
    
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
            success, message = test_func(creds)
            if success:
                print(f"✅ OK ({message})")
                results.append(True)
            else:
                print(f"❌ ERRO: {message}")
                results.append(False)
        except Exception as e:
            print(f"❌ EXCEÇÃO: {str(e)[:50]}")
            results.append(False)
    
    # Resumo
    print()
    print("═" * 41)
    if all(results):
        print("✅ TODOS OS SERVIÇOS ACESSÍVEIS")
    else:
        failed = sum(1 for r in results if not r)
        print(f"⚠️  {failed} SERVIÇO(S) COM PROBLEMAS")
    print("═" * 41)

if __name__ == '__main__':
    main()
