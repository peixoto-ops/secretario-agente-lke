#!/usr/bin/env python3
"""
Script para registrar conhecimento no Mem0 sobre o ecossistema LKE.
Versão: Usa OpenRouter para embeddings (via OpenAI client).

Para usar, configure:
  export OPENAI_API_KEY="${OPENROUTER_API_KEY}"
  export OPENAI_BASE_URL="https://openrouter.ai/api/v1"

Executar: python mem0_knowledge_openrouter.py
"""

from mem0 import Memory
import os

def main():
    # Configura OpenRouter como backend
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not openrouter_key:
        # Tenta ler do .env
        env_path = os.path.expanduser("~/.hermes/.env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("OPENROUTER_API_KEY="):
                        openrouter_key = line.split("=", 1)[1].strip()
                        break
    
    if not openrouter_key:
        print("ERRO: OPENROUTER_API_KEY não encontrado")
        print("Configure em ~/.hermes/.env ou export OPENROUTER_API_KEY=...")
        return
    
    # Configura ambiente para Mem0 usar OpenRouter
    os.environ["OPENAI_API_KEY"] = openrouter_key
    os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
    
    user_id = "luiz_peixoto"
    
    # Inicializa Mem0 com configuração customizada
    config = {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "lke_knowledge",
                "embedding_model_dims": 1536  # OpenAI compatible
            }
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-ada-002"
            }
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": "openai/gpt-4o-mini",
                "temperature": 0.1
            }
        }
    }
    
    print("Inicializando Mem0 com OpenRouter...")
    m = Memory.from_config(config)
    
    # Conhecimento sobre o processo de auditoria
    knowledge_items = [
        "lke-ops-audit-vault é o repositório de relatórios de governança do ecossistema LKE em /media/peixoto/Portable/lke-ops-audit-vault/. Atualizado às 23h pelo cron lke-ops-auditor-diario.",
        "Auditados pelo lke-ops-auditor: lke_master_vault, costum_patterns, secretario-agente-lke, lke-processos-hub, ecosystem-dashboard. Cada um gera report_*.md com diagnóstico estratégico.",
        "costum_patterns contém patterns Fabric: lke_yaml_parser, redacao-juridica-atomica, peixoto-snapshot, analyze_ops_governance_report. Alto valor para automação jurídica.",
        "secretario-agente-lke: sistema de automação com Google Workspace (Calendar, Tasks, Gmail, Drive). Relatório matinal às 06h via cron secretario-matinal-lke.",
        "Google Drive Talk_Gemini_Hermes (ID: 1a1SCXw7ozp2nKKQCZNf0Z6ozfl27zwBW): pasta de comunicação Gemini-Hermes com subpastas hermes_para_gemini e gemini_para_hermes.",
        "Luiz Peixoto: advogado OAB/RJ 94719, metodologia LKE v5.0/Cognição Desacoplada, MRSA, filosofia Excelência Radical e Anti-fragilidade."
    ]
    
    print("Registrando conhecimento...")
    for item in knowledge_items:
        m.add(item, user_id=user_id)
        print(f"  + OK")
    
    print("\nVerificando memórias...")
    results = m.search("lke", user_id=user_id)
    print(f"Total de memórias: {len(results)}")
    
    print("\nMem0 configurado com sucesso!")

if __name__ == "__main__":
    main()
