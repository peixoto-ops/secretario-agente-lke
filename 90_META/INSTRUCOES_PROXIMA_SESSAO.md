---
data: 2026-04-14
tipo: instrucoes-proxima-sessao
projeto: secretario-agente-lke
sessao_anterior: T1.5.4+
---

# Instruções para Próxima Sessão - Secretário-Agente LKE

## 1. Repositório de Trabalho

```bash
cd /media/peixoto/Portable/secretario-agente-lke
```

## 2. Estado Atual do Projeto

### O que foi feito nesta sessão:
- Site narrativo criado e publicado em https://keen-refuge-kfr6.here.now/
- README atualizado com roadmap e link para demonstração
- Documentação de instruções para continuidade

### O que está pendente (do último diagnóstico):

**Fase 2 - Integração (em andamento):**
1. Integrar como skill do Hermes Agent
2. Implementar funções de escrita (criar registros no Supabase)
3. Configurar Row Level Security (RLS)
4. Primeira execução automatizada via cron

## 3. Tarefas Prioritárias

### Prioridade 1: Criar Skill Hermes `secretario-agente-lke`

**Local:** `~/.hermes/skills/secretario-agente-lke/SKILL.md`

**Funcionalidades da skill:**
- Carregar credenciais do guardião (`10_REFERENCIAS/credentials/`)
- Coletar dados de:
  - GitHub API (commits recentes, issues)
  - Google Calendar (eventos do dia)
  - Google Tasks (tarefas pendentes)
  - Supabase (processos, clientes)
- Gerar relatório consolidado
- Entregar via Telegram

### Prioridade 2: Implementar Script Principal

**Arquivo:** `30_IMPLEMENTACAO/secretario.py`

**Funções necessárias:**
```python
def coletar_github() -> dict
def coletar_google_calendar() -> dict
def coletar_google_tasks() -> dict
def coletar_supabase() -> dict
def gerar_relatorio(dados: dict) -> str
def enviar_telegram(relatorio: str) -> bool
```

### Prioridade 3: Configurar Cron Job

**Horário recomendado:** 06:00 (segunda a sexta)

```bash
# Exemplo de cron
0 6 * * 1-5 /media/peixoto/Portable/secretario-agente-lke/50_CRON_JOBS/secretario-diario.sh
```

## 4. Arquivos de Referência

| Arquivo | Propósito |
|---------|-----------|
| `10_REFERENCIAS/credentials/client_secret.json` | OAuth2 Google |
| `10_REFERENCIAS/credentials/token.json` | Token de acesso |
| `30_IMPLEMENTACAO/hermes_supabase_client.py` | Client Supabase |
| `40_DOCUMENTOS/DIAGNOSTICO_CAPACIDADES_T1.5.3.md` | Diagnóstico completo |
| `20_PROPOSTAS/PROPOSTA_SECRETARIO_AGENTE.md` | Proposta original |

## 5. Comandos Úteis

```bash
# Ativar ambiente
cd /media/peixoto/Portable/secretario-agente-lke
source venv/bin/activate

# Testar client Supabase
python 30_IMPLEMENTACAO/hermes_supabase_client.py matters

# Verificar token Google
python -c "
import json
from pathlib import Path
token = json.loads(Path('10_REFERENCIAS/credentials/token.json').read_text())
print(f'Token válido até: {token.get(\"expiry\", \"N/A\")}')
"

# Publicar atualização do site
cd site-narrativo && ~/.agents/skills/here-now/scripts/publish.sh . --slug keen-refuge-kfr6
```

## 6. Estrutura de Relatório Esperada

```
══════════════════════════════════════════════════
RELATÓRIO MATINAL - DD/MM/AAAA
══════════════════════════════════════════════════

📅 AGENDA DO DIA
├─ 09:00 | Compromisso X
└─ 14:00 | Audiência Y

📋 TAREFAS PENDENTES (N)
├─ 🔴 HOJE: X tarefas
├─ 🟡 AMANHÃ: Y tarefas
└─ ⚪ SEM PRAZO: Z tarefas

📁 REPOSITÓRIOS ATIVOS
├─ projeto-1: ATIVO (1 dia)
├─ projeto-2: LATENTE (3 dias)
└─ projeto-3: ATIVO (2 dias)

⚖️ PRAZOS PROCESSUAIS
├─ 3059343-57.2026.8.19.0001: N dias restantes
└─ (outros processos...)

⚡ AÇÕES SUGERIDAS
1. Ação prioritária 1
2. Ação prioritária 2
3. Ação prioritária 3

══════════════════════════════════════════════════
Gerado por Secretário-Agente LKE
══════════════════════════════════════════════════
```

## 7. Integrações Configuradas

| Serviço | Status | Observação |
|---------|--------|------------|
| Google Calendar | ✅ OK | Token validado |
| Google Tasks | ✅ OK | 17 tarefas pendentes |
| Supabase | ✅ OK | Client funcionando |
| GitHub API | ✅ OK | gh CLI disponível |
| Telegram | ✅ OK | Hermes entrega nativo |

## 8. Próximos Passos Detalhados

### Passo 1: Carregar Skill Existente

Antes de criar nova skill, verificar skills relacionadas:
```bash
# Ver skills disponíveis
hermes skills list | grep -i secre
hermes skills list | grep -i google
hermes skills list | grep -i telegram
```

### Passo 2: Template de Skill

Usar como base: `~/.hermes/skills/google-workspace/SKILL.md`

### Passo 3: Testar Fluxo Manual

Antes de automatizar, testar manualmente:
```bash
# Coletar dados
python 30_IMPLEMENTACAO/secretario.py --coletar

# Gerar relatório
python 30_IMPLEMENTACAO/secretario.py --relatorio

# Enviar (dry-run)
python 30_IMPLEMENTACAO/secretario.py --enviar --dry-run
```

## 9. Decisões Pendentes

| Decisão | Contexto | Recomendação |
|---------|----------|--------------|
| Horário cron | Matinal vs noturno | 06:00 (matinal) |
| Frequência | Diário vs alternado | Diário útil |
| Formato output | Texto vs Markdown | Markdown |
| Entrega | Telegram apenas vs múltiplos | Telegram principal |

## 10. Contatos e Referências

- **Projeto:** peixoto-ops/secretario-agente-lke
- **Supabase Dashboard:** https://supabase.com/dashboard
- **Google Cloud Console:** https://console.cloud.google.com
- **Site Demonstração:** https://keen-refuge-kfr6.here.now/

---

**Documento preparado para continuidade do projeto**
**Data:** 2026-04-14
**Sessão anterior:** Criação do site narrativo e atualização de documentação
