#!/bin/bash
# Secretário-Agente LKE - Job Diário
# Executado via cron às 22:00

set -e

# Configurações
SECRETARIO_DIR="/media/peixoto/Portable/secretario-agente-lke"
LOG_DIR="$SECRETARIO_DIR/60_DIAGNOSTICOS"
DATE_STAMP=$(date +%Y%m%d_%H%M%S)

echo "========================================="
echo "SECRETÁRIO-AGENTE LKE - EXECUÇÃO DIÁRIA"
echo "Data/Hora: $(date)"
echo "========================================="

# 1. Coletar dados do GitHub
echo ""
echo "[1/4] Coletando dados do GitHub..."
cd "$SECRETARIO_DIR/30_IMPLEMENTACAO"
python3 coletor_github.py 2>&1 | tee "$LOG_DIR/coleta_${DATE_STAMP}.log"

# 2. Coletar dados locais (git status)
echo ""
echo "[2/4] Verificando repositórios locais..."
for repo_dir in /media/peixoto/Portable/*/; do
    if [ -d "$repo_dir/.git" ]; then
        repo_name=$(basename "$repo_dir")
        echo "  - $repo_name: $(cd "$repo_dir" && git status --short 2>/dev/null | wc -l) arquivos modificados"
    fi
done

# 3. Gerar relatório consolidado
echo ""
echo "[3/4] Gerando relatório..."
# Aqui entraria a chamada para o Hermes gerar o relatório
# hermes --skill secretario-agente --task gerar-relatorio

# 4. Enviar via Telegram
echo ""
echo "[4/4] Enviando para Telegram..."
# curl ou hermes delivery

echo ""
echo "✅ Execução concluída em $(date)"
echo "Logs salvos em: $LOG_DIR"
