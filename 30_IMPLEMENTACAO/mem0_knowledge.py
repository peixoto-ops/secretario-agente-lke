#!/usr/bin/env python3
"""
Script para registrar conhecimento no Mem0 sobre o ecossistema LKE.
Executar: python mem0_knowledge.py
"""

from mem0 import Memory
import os

def main():
    m = Memory()
    user_id = "luiz_peixoto"
    
    # Conhecimento sobre o processo de auditoria
    knowledge_items = [
        {
            "content": "lke-ops-audit-vault é o repositório de relatórios de governança do ecossistema LKE. Localizado em /media/peixoto/Portable/lke-ops-audit-vault/. Atualizado diariamente às 23:00 (seg-sex) pelo cron 'lke-ops-auditor-diario'. Usa o pattern Fabric 'analyze_ops_governance_report' para analisar commits e gerar insights estratégicos.",
            "metadata": {"category": "infraestrutura", "type": "audit_vault"}
        },
        {
            "content": "Auditados pelo lke-ops-auditor: lke_master_vault (vault principal), costum_patterns (patterns Fabric), secretario-agente-lke (automação), lke-processos-hub (hub central), ecosystem-dashboard (dashboard), caso-loreto-vivas (caso ativo). Cada repositório gera um report_*.md com diagnóstico, decomposição de esforço e análise de convenções LKE.",
            "metadata": {"category": "infraestrutura", "type": "repositorios_auditados"}
        },
        {
            "content": "costum_patterns é o repositório de padrões Fabric para automação jurídica. Contém: lke_yaml_parser (parser YAML), redacao-juridica-atomica (sistema modular de documentos), peixoto-snapshot (análise temporal), analyze_ops_governance_report (auditoria). Alto valor estratégico para escalabilidade.",
            "metadata": {"category": "automacao", "type": "patterns"}
        },
        {
            "content": "secretario-agente-lke é o sistema de automação administrativa. Integra Google Workspace via OAuth2 (Calendar, Tasks, Gmail, Drive, Sheets). Gera relatório matinal consolidado às 06:00 via cron 'secretario-matinal-lke'. Banco SQLite em 30_IMPLEMENTACAO/.",
            "metadata": {"category": "automacao", "type": "secretario_agente"}
        },
        {
            "content": "Cron jobs ativos: secretario-matinal-lke (06:00 seg-sex, relatório matinal), lke-ops-auditor-diario (23:00 seg-sex, auditoria de governança). Ambos entregam no Telegram 641920234.",
            "metadata": {"category": "infraestrutura", "type": "cron_jobs"}
        },
        {
            "content": "Google Drive Talk_Gemini_Hermes: Pasta para comunicação entre Gemini e Hermes. ID: 1a1SCXw7ozp2nKKQCZNf0Z6ozfl27zwBW. Subpastas: hermes_para_gemini, gemini_para_hermes. Usada para troca de documentos e pesquisas colaborativas.",
            "metadata": {"category": "colaboracao", "type": "google_drive"}
        },
        {
            "content": "Luiz Peixoto usa metodologia LKE v5.0 / Cognição Desacoplada com MRSA (Matriz Relacional de Subsunção Argumentativa). Filosofia: Excelência Radical e Anti-fragilidade. Usa legal_commit para commits semânticos jurídicos. OAB/RJ 94719.",
            "metadata": {"category": "usuario", "type": "perfil"}
        }
    ]
    
    print("Registrando conhecimento no Mem0...")
    for item in knowledge_items:
        result = m.add(
            item["content"],
            user_id=user_id,
            metadata=item["metadata"]
        )
        print(f"  + {item['metadata']['type']}: OK")
    
    print("\nBuscando para verificar...")
    search_results = m.search("lke audit", user_id=user_id)
    print(f"Memórias encontradas: {len(search_results)}")
    
    print("\nMem0 configurado com sucesso!")

if __name__ == "__main__":
    main()
