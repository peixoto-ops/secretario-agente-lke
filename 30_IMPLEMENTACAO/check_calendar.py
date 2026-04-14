#!/usr/bin/env python3
"""Verifica eventos do Google Calendar"""

import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
TOKEN_PATH = "/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/token.json"
CLIENT_SECRET_PATH = "/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials/client_secret.json"

def main():
    # Carregar credenciais
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    
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
    
    service = build("calendar", "v3", credentials=creds)
    
    # Buscar eventos dos próximos 7 dias
    now = datetime.utcnow()
    end = now + timedelta(days=7)
    
    print("=" * 50)
    print("GOOGLE CALENDAR - EVENTOS PRÓXIMOS")
    print("=" * 50)
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now.isoformat() + 'Z',
        timeMax=end.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print("\nNenhum evento nos próximos 7 dias")
        return []
    
    # Agrupar por data
    events_by_date = {}
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if 'T' in start:
            date_str = start[:10]
            time_str = start[11:16]
        else:
            date_str = start
            time_str = "dia todo"
        
        if date_str not in events_by_date:
            events_by_date[date_str] = []
        
        events_by_date[date_str].append({
            "time": time_str,
            "summary": event.get('summary', 'Sem título'),
            "location": event.get('location', '')
        })
    
    # Exibir organizado por data
    today = now.strftime('%Y-%m-%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    
    for date_str in sorted(events_by_date.keys()):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        weekday = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'][date_obj.weekday()]
        
        if date_str == today:
            print(f"\n📅 HOJE ({date_str} - {weekday})")
        elif date_str == tomorrow:
            print(f"\n📅 AMANHÃ ({date_str} - {weekday})")
        else:
            print(f"\n📅 {date_str} ({weekday})")
        
        print("-" * 40)
        for evt in events_by_date[date_str]:
            print(f"  🕐 {evt['time']} | {evt['summary']}")
            if evt['location']:
                print(f"      📍 {evt['location']}")
    
    print("\n" + "=" * 50)
    print(f"TOTAL: {len(events)} eventos nos próximos 7 dias")
    print("=" * 50)
    
    return events_by_date

if __name__ == "__main__":
    main()
