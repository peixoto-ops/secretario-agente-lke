#!/usr/bin/env python3
"""
Autenticação OAuth2 para Google Workspace (Headless)
Fluxo manual para ambientes sem navegador

Uso:
    python3 auth_google_headless.py
    
Resultado:
    - Gera URL de autorização
    - Aguarda código de autorização
    - Salva token.json
"""

import os
import sys
import json
from pathlib import Path

# Paths absolutos
CREDENTIALS_DIR = Path('/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials')
CLIENT_SECRET_PATH = CREDENTIALS_DIR / 'client_secret.json'
TOKEN_PATH = CREDENTIALS_DIR / 'token.json'

# Escopos necessários
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def main():
    print("=" * 60)
    print("AUTENTICAÇÃO GOOGLE WORKSPACE (Headless Mode)")
    print("=" * 60)
    print()
    
    # Verificar se client_secret existe
    if not CLIENT_SECRET_PATH.exists():
        print(f"❌ ERRO: client_secret.json não encontrado")
        sys.exit(1)
    
    # Carregar client_secret
    with open(CLIENT_SECRET_PATH) as f:
        client_config = json.load(f)
    
    client_id = client_config['installed']['client_id']
    client_secret = client_config['installed']['client_secret']
    redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    # Construir URL de autorização manualmente
    from urllib.parse import urlencode, quote
    
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth?" +
        urlencode({
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': ' '.join(SCOPES),
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }, quote_via=quote)
    )
    
    print("🔑 PASSO 1: Autorizar aplicação")
    print()
    print("1. Copie a URL abaixo")
    print("2. Cole no seu navegador")
    print("3. Autorize o acesso")
    print("4. Copie o código de autorização")
    print()
    print("-" * 60)
    print(auth_url)
    print("-" * 60)
    print()
    
    # Solicitar código de autorização
    auth_code = input("Cole aqui o código de autorização: ").strip()
    
    if not auth_code:
        print("❌ Código não fornecido")
        sys.exit(1)
    
    print()
    print("🔄 Trocando código por token...")
    
    # Trocar código por token
    import requests
    
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        'code': auth_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code != 200:
        print(f"❌ Erro ao obter token: {response.text}")
        sys.exit(1)
    
    token_data = response.json()
    
    # Salvar token
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(json.dumps(token_data, indent=2))
    TOKEN_PATH.chmod(0o600)
    
    print()
    print("=" * 60)
    print("✅ AUTENTICAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"📁 Token salvo em: {TOKEN_PATH}")
    print(f"🔒 Permissões: 600 (apenas proprietário)")
    print()
    print("▶️  Próximo passo: python3 validate_workspace.py")

if __name__ == '__main__':
    main()
