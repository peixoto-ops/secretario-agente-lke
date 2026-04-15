---
data: 2026-04-13
tipo: sessao-pratica
status: em-andamento
tags:
- secretaria
- workflow
- redistribuicao
- planejamento
projeto: secretario-agente-lke
sessao: T1.5.4
---

# Sessão Prática - Redistribuição de Tarefas - 2026-04-13

## Contexto

Esta é uma sessão prática do Secretário-Agente LKE. Diferente das sessões de desenvolvimento e testes anteriores (T1.5.1 a T1.5.3), esta sessão tem propósito operacional: resolver uma questão prática de redistribuição de tarefas.

### Diferenciais desta Sessão

- **Propósito:** Resolver problema real, não testar infraestrutura
- **Metodologia:** Anotar lições para reutilização futura
- **Objetivo:** Estabelecer padrão para sessões práticas do Secretário

---

## 📊 Situação Atual

### Google Tasks - 17 Tarefas Pendentes

#### Lista de luizpeixoto.adv (17 tarefas)

| # | Tarefa | Prazo | Caso Relacionado | Prioridade |
|---|--------|-------|------------------|------------|
| 1 | Catalogar Documentos (Tabela MRSA) - Dianne Nicola | 2026-04-13 | case-diane-nicola-ops | 🔴 HOJE |
| 2 | Onboarding e Criação de Repositório - Paulo Saad | 2026-04-14 | (novo caso) | 🟡 AMANHÃ |
| 3 | Solicitar Documentos (Execução INSS) - Roberta | 2026-04-14 | (execução) | 🟡 AMANHÃ |
| 4 | Processar Ação Anulatória ICMBio - Patrícia Wasserman | 2026-04-13 | case-patricia-w-vs-cedae-serasa-ops | 🔴 HOJE |
| 5 | [DEEP WORK] Patrícia Wasserman: Automação Ação ICMBio | 2026-04-13 | case-patricia-w-vs-cedae-serasa-ops | 🔴 HOJE |
| 6 | [PESQUISA] Prova Digital e Cadeia de Custódia (Tepedino) | 2026-04-13 | caso-leonardo-tepedino | 🔴 HOJE |
| 7 | Processar Inventários (Linha do Tempo e Habilitação) - Família Sá | 2026-04-13 | inv_sa_02 | 🔴 HOJE |
| 8 | [DEEP WORK] Família Sá: MRSA e Habilitação | 2026-04-13 | inv_sa_02 | 🔴 HOJE |
| 9 | [DEEP WORK] Família Sá: Finalizar Linha do Tempo MRSA | 2026-04-13 | inv_sa_02 | 🔴 HOJE |
| 10 | [OPS/LKE] Teste lke-ingest e Normalização de Vaults | 2026-04-13 | lke-processos-hub | 🔴 HOJE |

### GitHub - Commits Recentes por Caso

#### caso-leonardo-tepedino (p31x070)
- Último commit: `2026-04-10T22:15:25Z` (3 dias atrás)
- Status: LATENTE (mais de 3 dias sem commit)
- Últimos trabalhos:
  - Análise de planilhas de prestação de contas agropecuárias
  - Pesquisa sobre eficácia da ação de prestação de contas
  - Comandos de commits individuais

#### Processo CNJ: 3059343-57.2026.8.19.0001
- **Ação:** Exigir Contas
- **Autor:** Leonardo Azeredo Lopes Tepedino
- **Ré:** Ana Paula de Azeredo Lopes Tepedino
- **Juízo:** 41ª Vara Cível da Capital
- **Status:** Aguardando emenda à inicial (15 dias a contar de 09/04/2026)
- **Prazo crítico:** ~24/04/2026

---

## 🎯 Tarefas da Sessão

### 1. Caso Leonardo Tepedino - Termo Inicial

**Objetivo:** Localizar o termo inicial fixado para recalcular planejamento.

**Situação identificada:**
- O processo foi distribuído em **02/04/2026**
- O despacho de emenda à inicial foi em **09/04/2026**
- Prazo de 15 dias para emenda
- **Termo inicial provável:** 09/04/2026 (data da intimação)

**Dados úteis para o futuro:**
- Registrar a data da intimação como marco para cálculo de prazos
- Criar template de cálculo de prazos processuais

### 2. Atualização de Processos via CNJ

**Ferramenta:** `automate_reports -n <numero_processo>`
**Status:** ✅ Funcionando

**Processo testado:** 3059343-57.2026.8.19.0001
- Relatório gerado com sucesso
- Informações atualizadas capturadas

### 3. Google Contatos - Atualização de Cadastro

**Pendente:** Atualizar dados de cadastro com informações obtidas do CNJ

---

## 📝 Dados Úteis para Futuro

### Padrões Identificados

1. **Token Google Workspace:** O token.json precisa de client_id e client_secret para refresh automático
2. **Tarefas Google:** Integradas com workflow jurídico - prazos sincronizados
3. **API CNJ:** Funciona via `automate_reports` - executar periodicamente

### Estrutura de Dados Recomendada

```yaml
caso:
  nome: caso-leonardo-tepedino
  processo_cnj: 3059343-57.2026.8.19.0001
  repositorio: p31x070/caso-leonardo-tepedino
  tipo_acao: Exigir Contas
  prazo_atual:
    tipo: emenda_inicial
    data_intimacao: 2026-04-09
    prazo_dias: 15
    data_limite: 2026-04-24
  status: aguardando_emenda
```

---

## 🔄 Como Escalar o Trabalho

### 1. Criar Skill Hermes: `secretario-agente-lke`

**Função:** Coletar dados de múltiplas fontes e gerar relatório

**Fontes:**
- Google Tasks (tarefas pendentes)
- GitHub API (commits recentes)
- API CNJ (andamentos processuais)
- Git local (status dos repositórios)

### 2. Cron Job Diário

**Horário recomendado:** 06:00 (matinal)
**Formato:** `0 6 * * 1-5` (segunda a sexta)

### 3. Output Padronizado

```
══════════════════════════════════════════════════
RELATÓRIO MATINAL - DD/MM/AAAA
══════════════════════════════════════════════════

📅 AGENDA DO DIA
├─ 09:00 | Compromisso X
└─ 14:00 | Audiência Y

📋 TAREFAS PENDENTES (17)
├─ 🔴 HOJE: 10 tarefas
├─ 🟡 AMANHÃ: 5 tarefas
└─ ⚪ SEM PRAZO: 2 tarefas

📁 REPOSITÓRIOS ATIVOS
├─ caso-leonardo-tepedino: LATENTE (3 dias)
├─ inv_sa_02: ATIVO (1 dia)
└─ ekwrio: ATIVO (2 dias)

⚖️ PRAZOS PROCESSUAIS
├─ 3059343-57.2026.8.19.0001: 11 dias restantes
└─ (outros processos...)

══════════════════════════════════════════════════
```

### 4. Armazenamento de Dados

**Diretório:** `/media/peixoto/Portable/secretario-agente-lke/40_DOCUMENTOS/`
**Formato:** JSON + Markdown
**Nomenclatura:** `YYYY-MM-DD_relatorio.json` / `.md`

---

## ⏭️ Próximos Passos

1. [ ] Criar skill `secretario-agente-lke` no Hermes
2. [ ] Implementar script `secretario.py` principal
3. [ ] Configurar cron job matinal
4. [ ] Testar entrega via Telegram
5. [ ] Documentar fluxo completo

---

## 📊 Métricas da Sessão

- **Duração:** ~45 minutos
- **Dados coletados:** GitHub commits, Google Tasks, CNJ API
- **Problemas resolvidos:** Token refresh, API integration
- **Lições aprendidas:** 3

---

## 🔗 Referências

- Proposta: `20_PROPOSTAS/PROPOSTA_SECRETARIO_AGENTE.md`
- Diagnóstico: `40_DOCUMENTOS/DIAGNOSTICO_CAPACIDADES_T1.5.3.md`
- Validação: `40_DOCUMENTOS/validacao_workspace_T1.5.3.md`
