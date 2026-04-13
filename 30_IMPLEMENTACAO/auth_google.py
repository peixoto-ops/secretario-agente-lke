#!/usr/bin/env python3
"""
Autenticação OAuth2 para Google Workspace
Gera token.json a partir do client_secret.json

Uso:
    python3 auth_google.py
    
Resultado:
    - Abre navegador para autenticação
    - Gera token.json em 10_REFERENCIAS/credentials/
"""

import os
import sys
from pathlib import Path

# Paths absolutos
CREDENTIALS_DIR = Path('/media/peixoto/Portable/secretario-agente-lke/10_REFERENCIAS/credentials')
CLIENT_SECRET_PATH = CREDENTIALS_DIR / 'client_secret.json'
TOKEN_PATH = CREDENTIALS_DIR / 'token.json'

# Escopos necessários para todos os serviços
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def main():
    print("=" * 50)
    print("AUTENTICAÇÃO GOOGLE WORKSPACE")
    print("=" * 50)
    print()
    
    # Verificar se client_secret existe
    if not CLIENT_SECRET_PATH.exists():
        print(f"❌ ERRO: client_secret.json não encontrado em:")
        print(f"   {CLIENT_SECRET_PATH}")
        sys.exit(1)
    
    print(f"✅ Credenciais encontradas: {CLIENT_SECRET_PATH}")
    print()
    print("📂 Escopos solicitados:")
    for scope in SCOPES:
        service = scope.split('/')[-1].split('.')[0]
        print(f"   • {service.upper()}: {scope}")
    print()
    print("🌐 Iniciando autenticação OAuth2...")
    print("   Um navegador será aberto para você autorizar o acesso.")
    print()
    
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        
        # Verificar se já existe token válido
        creds = None
        if TOKEN_PATH.exists():
            print("📋 Token existente encontrado. Verificando validade...")
            try:
                creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
                if creds and creds.valid:
                    print("✅ Token ainda é válido!")
                    print(f"   Expira em: {creds.expiry}")
                    resposta = input("\nDeseja re-autenticar? (s/N): ").strip().lower()
                    if resposta != 's':
                        print("✅ Mantendo token atual.")
                        return creds
                    creds = None  # Forçar re-autenticação
            except Exception as e:
                print(f"⚠️ Token existente inválido: {e}")
                creds = None
        
        # Se não há credenciais válidas, autenticar
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Atualizando token expirado...")
                creds.refresh(Request())
            else:
                print("🔐 Iniciando fluxo de autorização...")
                print("   (Modo console - copie a URL para o navegador)")
                print()
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CLIENT_SECRET_PATH), SCOPES
                )
                # Usar run_console em vez de run_local_server
                creds = flow.run_console()
            
            # Salvar token
            TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
            TOKEN_PATH.write_text(creds.to_json())
            TOKEN_PATH.chmod(0o600)  # Permissões restritas
            
            print()
            print("=" * 50)
            print("✅ AUTENTICAÇÃO CONCLUÍDA!")
            print("=" * 50)
            print(f"📁 Token salvo em: {TOKEN_PATH}")
            print(f"🔒 Permissões: 600 (apenas proprietário)")
            print(f"⏰ Expira em: {creds.expiry}")
            print()
            print("▶️  Próximo passo: execute validate_workspace.py")
            
        return creds
        
    except ImportError as e:
        print(f"❌ ERRO: Biblioteca não instalada: {e}")
        print()
        print("Instale com:")
        print("  pip install google-auth google-auth-oauthlib google-auth-httplib2")
        print("  pip install google-api-python-client")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERRO durante autenticação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
