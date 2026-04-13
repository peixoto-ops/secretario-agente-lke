# Proposta: Secretário-Agente LKE

> Sistema de automação de agenda e acompanhamento cruzado de projetos
> Versão: 1.0 | Data: 2026-04-13

---

## 1. Contexto e Problema

### Situação Atual
- Múltiplos repositórios ativos (135 total, ~20 prioritários)
- Planejamento diário sujeito a imprevistos (saúde, demandas urgentes)
- Nova demanda = necessidade de readequação rápida
- Falta de visibilidade cruzada entre projetos
- Rastreamento manual de commits e progresso

### Dor Principal
> "Hoje tinha um planejamento, mas devido ao cansaço acordei mais tarde, tive vários imprevistos em casa, então meu plano precisaria de ajuste."

**Tradução**: Necessidade de um sistema que:
1. Detecte mudanças de contexto
2. Reordene prioridades automaticamente
3. Mantenha visão consolidada de todos os projetos
4. Gere relatórios para tomada de decisão

---

## 2. Solução Proposta: Secretário-Agente LKE

### Conceito
Um agente automatizado que opera como "secretário executivo", executando diariamente via cron job para:

1. **Consolidar estado de todos os projetos**
2. **Gerar relatório de situação**
3. **Propriorizar tarefas do dia seguinte**
4. **Detectar pendências e prazos**
5. **Entregar relatório via Telegram**

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    SECRETÁRIO-AGENTE LKE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   GitHub    │    │   Cron      │    │  Telegram   │     │
│  │   API       │───▶│   Job       │───▶│  Delivery   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                  │                  ▲            │
│         ▼                  ▼                  │            │
│  ┌─────────────┐    ┌─────────────┐           │            │
│  │   Git Log   │    │   Hermes    │───────────┘            │
│  │   Parser    │    │   Agent     │                        │
│  └─────────────┘    └─────────────┘                        │
│         │                  │                                │
│         ▼                  ▼                                │
│  ┌─────────────────────────────────────────────────┐       │
│  │              BASE DE CONHECIMENTO               │       │
│  │  /media/peixoto/Portable/secretario-agente-lke  │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Funcionalidades Principais

### 3.1 Coleta Automatizada

| Fonte | Dados Coletados | Frequência |
|-------|-----------------|------------|
| GitHub API | Commits, Issues, PRs | Diária |
| Git Local | Branches, status | Diária |
| inv_sa_02 | Andamentos processuais | Diária |
| Cron Jobs | Status de jobs | Tempo real |
| Google Calendar | Eventos, prazos | Diária |

### 3.2 Processamento

**Análise de Commits:**
```python
# Padrão de extração
for commit in recent_commits:
    projeto = extrair_projeto(commit.repo)
    tipo = classificar_commit(commit.message)  # feat, fix, docs, etc
    prioridade = inferir_prioridade(commit.message)
    registrar_atividade(projeto, tipo, prioridade, commit.timestamp)
```

**Detecção de Padrões:**
- Projetos sem atividade há X dias
- Commits não semânticos
- Prazos próximos sem movimento
- Conflitos de agenda

### 3.3 Saídas

**Relatório Diário (Telegram):**
```
═══════════════════════════════════════
    BOLETIM DIÁRIO - 14/04/2026
═══════════════════════════════════════

📊 RESUMO EXECUTIVO
├─ 5 projetos ativos com commits
├─ 2 projetos sem movimento há 7+ dias
└─ 3 prazos próximos (ver DETALHES)

🔴 PRIORIDADES URGENTES
1. inv_sa_02 - Prazo: 18/04
2. ekwrio - Aguardando proposta
3. caso-loreto-vivas - Aguardando docs

📋 ATIVIDADES DE ONTEM
├─ inv_sa_02: 3 commits (auditoria)
├─ lke-processos-hub: 1 commit (docs)
└─ deep-research-lke: 2 commits (feat)

⚡ AÇÕES SUGERIDAS
1. Revisar proposta EKWRio
2. Atualizar docs loreto-vivas
3. Verificar cron jobs inativos

═══════════════════════════════════════
    Gerado por Secretário-Agente LKE
═══════════════════════════════════════
```

---

## 4. Alternativas Avaliadas

### Alternativa A: Agente Autônomo Contínuo

**Descrição:** Agente rodando 24/7 com monitoramento em tempo real.

**Vantagens:**
- Resposta imediata a mudanças
- Detecção de urgências em tempo real
- Integração contínua

**Desvantagens:**
- Maior complexidade
- Consumo de recursos
- Potencial spam de notificações

**Veredito:** Descartado para fase inicial. Implementar como evolução futura.

---

### Alternativa B: Agente Sob Demanda (Manual)

**Descrição:** Agente ativado manualmente pelo usuário quando necessário.

**Vantagens:**
- Controle total pelo usuário
- Simplicidade de implementação
- Sem custos de infraestrutura

**Desvantagens:**
- Depende de ativação manual
- Pode ser esquecido em dias corridos
- Não aproveita automatização

**Veredito:** Útil como complemento, mas não como solução principal.

---

### Alternativa C: Híbrida (Proposta Principal)

**Descrição:** Cron job noturno + ativação manual sob demanda.

**Vantagens:**
- Automação garantida (cron diário)
- Flexibilidade (ativação manual)
- Custo controlado
- Escalável

**Desvantagens:**
- Requer configuração inicial de cron
- Duas interfaces para manter

**Veredito:** APROVADO - Melhor custo-benefício para realidade atual.

---

## 5. Implementação

### 5.1 Estrutura de Diretórios

```
/media/peixoto/Portable/secretario-agente-lke/
├── 00_INBOX/              # Entrada de demandas
├── 10_REFERENCIAS/        # Documentação de referência
├── 20_PROPOSTAS/          # Propostas e alternativas
├── 30_IMPLEMENTACAO/      # Scripts e código
│   ├── secretario.py      # Agente principal
│   ├── coletor_github.py  # Coleta de dados GitHub
│   ├── coletor_local.py   # Coleta de dados locais
│   └── gerador_relatorio.py
├── 40_DOCUMENTOS/         # Relatórios gerados
├── 50_CRON_JOBS/          # Configurações cron
├── 60_DIAGNOSTICOS/       # Logs e diagnósticos
└── 90_META/               # Documentação meta
```

### 5.2 Cron Job Sugerido

```bash
# Executar diariamente às 22:00
0 22 * * * /home/peixoto/bin/secretario-diario.sh
```

### 5.3 Fluxo de Ativação

**Automática (Cron):**
1. 22:00 - Coleta dados de todos os repositórios
2. 22:05 - Processa e analisa
3. 22:10 - Gera relatório
4. 22:15 - Envia via Telegram

**Manual (Sob Demanda):**
```bash
# Atalho: /secretario ou /agenda
hermes --skill secretario-agente
```

---

## 6. Integrações

### 6.1 Hermes Agent
- Skill dedicada para secretário
- Reutiliza ferramentas existentes (cronjob, terminal, web)
- Entrega nativa via Telegram

### 6.2 OpenCode
- Delegação de tarefas específicas
- Análise profunda de código
- Geração de documentos

### 6.3 Google Workspace
- Calendar para prazos
- Tasks para pendências
- Drive para documentos

### 6.4 GitHub
- API para commits e issues
- Webhooks para eventos
- Actions para automação

---

## 7. Roadmap

### Fase 1 - MVP (Semana 1)
- [ ] Criar estrutura de diretórios
- [ ] Implementar coletor GitHub básico
- [ ] Gerar primeiro relatório manual
- [ ] Configurar cron job inicial

### Fase 2 - Automação (Semana 2)
- [ ] Implementar coletor local (git log)
- [ ] Integrar com Google Calendar
- [ ] Criar skill Hermes dedicada
- [ ] Testar entrega via Telegram

### Fase 3 - Inteligência (Semana 3-4)
- [ ] Adicionar detecção de padrões
- [ ] Implementar priorização automática
- [ ] Criar sugestões de ação
- [ ] Refinar formatação de relatórios

### Fase 4 - Evolução (Futuro)
- [ ] Agente contínuo 24/7
- [ ] Integração com mais fontes
- [ ] Dashboard web
- [ ] API REST

---

## 8. Decisões Pendentes

1. **Horário do cron:** 22:00 ou 06:00?
2. **Frequência:** Diário ou dia-sim-dia-não?
3. **Formato:** Texto simples ou markdown?
4. **Idioma:** PT-BR ou EN para relatórios?

---

## 9. Próximos Passos

1. Validar proposta com usuário
2. Criar repositório Git local
3. Implementar primeiro script de coleta
4. Testar cron job básico
5. Refinar iterativamente

---

## 10. Referências

- Hermes Agent: Sistema de cron jobs integrado
- LKE v5.0: Metodologia de cognição desacoplada
- inv_sa_02: Referência para andamentos processuais
- Johnny.Decimal: Sistema de organização de diretórios
