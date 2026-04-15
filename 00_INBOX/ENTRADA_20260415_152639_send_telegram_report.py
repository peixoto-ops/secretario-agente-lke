#!/usr/bin/env python3
"""
Script para enviar relatório da sessão T1.2 via Telegram
"""

import requests
import json
import os
from pathlib import Path

def send_telegram_message(message, chat_id=None, bot_token=None):
    """
    Envia mensagem via Telegram Bot API
    
    Args:
        message: Texto da mensagem
        chat_id: ID do chat (opcional - buscar de variável de ambiente)
        bot_token: Token do bot (opcional - buscar de variável de ambiente)
    """
    # Tentar obter credenciais de variáveis de ambiente
    if not bot_token:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not chat_id:
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '+5521969191621')
    
    if not bot_token:
        print("❌ Token do bot Telegram não encontrado")
        print("Defina a variável de ambiente TELEGRAM_BOT_TOKEN")
        return False
    
    # URL da API do Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Preparar dados
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get('ok'):
            print(f"✅ Mensagem enviada para chat_id: {chat_id}")
            return True
        else:
            print(f"❌ Erro ao enviar: {result}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def send_file_via_telegram(file_path, chat_id=None, bot_token=None, caption=""):
    """
    Envia arquivo via Telegram (PDF, imagem, etc.)
    """
    if not bot_token:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    
    if not chat_id:
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '+5521969191621')
    
    if not bot_token:
        print("❌ Token do bot Telegram não encontrado")
        return False
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    # Determinar tipo de arquivo
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.pdf':
        method = 'sendDocument'
        file_type = 'document'
    elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
        method = 'sendPhoto'
        file_type = 'photo'
    else:
        method = 'sendDocument'
        file_type = 'document'
    
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    
    try:
        with open(file_path, 'rb') as file:
            files = {file_type: file}
            data = {'chat_id': chat_id}
            if caption:
                data['caption'] = caption
            
            response = requests.post(url, files=files, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                print(f"✅ Arquivo enviado: {file_path}")
                return True
            else:
                print(f"❌ Erro ao enviar arquivo: {result}")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao enviar arquivo: {e}")
        return False

def main():
    """Função principal"""
    print("📱 Enviando relatório da sessão T1.2 via Telegram")
    print("=" * 50)
    
    # Caminhos dos arquivos
    base_dir = Path("/media/peixoto/Portable/secretario-agente-lke")
    resumo_file = base_dir / "resumo_telegram_T1_2.txt"
    pdf_file = base_dir / "relatorio_T1_2.pdf"
    html_file = base_dir / "here_now_T1_2.html"
    
    # Ler mensagem do arquivo
    if resumo_file.exists():
        with open(resumo_file, 'r', encoding='utf-8') as f:
            message = f.read()
        
        print("📝 Enviando resumo da sessão...")
        success = send_telegram_message(message)
        
        if success:
            print("✅ Resumo enviado com sucesso!")
            
            # Tentar enviar PDF
            if pdf_file.exists():
                print(f"📄 Enviando PDF: {pdf_file}")
                caption = "📊 Relatório completo da sessão T1.2 - Validação Linear ↔ GitHub"
                send_file_via_telegram(pdf_file, caption=caption)
            
            # Informar sobre página HTML
            if html_file.exists():
                html_content = f"""🌐 Página here.now disponível localmente:
<code>{html_file}</code>

Para visualizar:
1. Abra o arquivo em um navegador
2. Ou sirva com: python3 -m http.server 8000
3. Acesse: http://localhost:8000/{html_file.name}</code>"""
                
                send_telegram_message(html_content)
        else:
            print("⚠️ Não foi possível enviar via Telegram. Verifique as credenciais.")
            print("\n📋 Mensagem para envio manual:")
            print("=" * 50)
            print(message)
            print("=" * 50)
    else:
        print(f"❌ Arquivo não encontrado: {resumo_file}")

if __name__ == "__main__":
    main()