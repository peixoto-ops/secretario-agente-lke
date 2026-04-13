# SECRETÁRIO-AGENTE LKE

## Proposta de Sistema de Automação de Agenda

**Data:** 13 de Abril de 2026  
**Autor:** Hermes Agent  
**Versão:** 1.0

---

## Sumário Executivo

Este documento apresenta a proposta do **Secretário-Agente LKE**, um sistema automatizado de gestão de agenda e acompanhamento cruzado de projetos para o ecossistema peixoto-ops.

O sistema foi projetado para resolver o problema de visibilidade e priorização em um ambiente com múltiplos projetos jurídicos simultâneos.

---

## 1. Problema Identificado

### Situação Atual

- **135 repositórios** no ecossistema (p31x070, peixoto-ops, neaigd)
- ~20 projetos prioritários com atividade regular
- Planejamento diário sujeito a imprevistos (saúde, demandas urgentes)
- Nova demanda = necessidade de readequação rápida
- Falta de visibilidade cruzada entre projetos
- Rastreamento manual de commits e progresso

### Dor Principal

*"Hoje tinha um planejamento, mas devido ao cansaço acordei mais tarde, tive vários imprevistos em casa, então meu plano precisaria de ajuste."*

**Tradução:** Necessidade de um sistema que:
1. Detecte mudanças de contexto
2. Reordene prioridades automaticamente
3. Mantenha visão consolidada de todos os projetos
4. Gere relatórios para tomada de decisão

---

## 2. Solução Proposta

### Conceito

Um agente automatizado que opera como **secretário executivo**, executando diariamente via cron job para:

1. Consolidar estado de todos os projetos
2. Gerar relatório de situação
3. Priorizar tarefas do dia seguinte
4. Detectar pendências e prazos
5. Entregar relatório via Telegram

### Arquitetura Híbrida (Aprovada)

| Componente | Descrição | Frequência |
|------------|-----------|------------|
| Cron Job Noturno | Automação garantida | 22:00 diário |
| Ativação Manual | Flexibilidade total | Sob demanda |
| Telegram Delivery | Comunicação nativa | Automático |

---

## 3. Alternativas Avaliadas

### Alternativa A: Agente Autônomo 24/7

- Status: **DESCARTADO**
- Motivo: Complexidade alta, consumo de recursos

### Alternativa B: Sob Demanda

- Status: **COMPLEMENTO**
- Motivo: Útil mas não resolve automatização

### Alternativa C: Híbrida

- Status: **APROVADA**
- Motivo: Melhor custo-benefício para realidade atual

---

## 4. Funcionalidades

### Coleta Automatizada

| Fonte | Dados Coletados | Frequência |
|-------|-----------------|------------|
| GitHub API | Commits, Issues, PRs | Diária |
| Git Local | Branches, status | Diária |
| inv_sa_02 | Andamentos processuais | Diária |
| Cron Jobs | Status de jobs | Tempo real |
| Google Calendar | Eventos, prazos | Diária |

### Saídas

**Relatório Diário (Telegram):**
- Resumo executivo
- Prioridades urgentes
- Atividades do dia anterior
- Ações sugeridas

---

## 5. Estrutura de Diretórios

```
/media/peixoto/Portable/secretario-agente-lke/
├── 00_INBOX/              # Entrada de demandas
├── 10_REFERENCIAS/        # Documentação de referência
├── 20_PROPOSTAS/          # Propostas e alternativas
├── 30_IMPLEMENTACAO/      # Scripts e código
├── 40_DOCUMENTOS/         # Relatórios gerados
├── 50_CRON_JOBS/          # Configurações cron
├── 60_DIAGNOSTICOS/       # Logs e diagnósticos
└── 90_META/               # Documentação meta
```

---

## 6. Roadmap

| Fase | Período | Objetivo |
|------|---------|----------|
| 1 | Semana 1 | MVP - estrutura, coletor básico |
| 2 | Semana 2 | Automação - cron, Telegram |
| 3 | Semana 3-4 | Inteligência - padrões, priorização |
| 4 | Futuro | Evolução - agente 24/7, dashboard |

---

## 7. Integrações

- **Hermes Agent:** Skill dedicada para secretário
- **OpenCode:** Delegação de tarefas específicas
- **Google Workspace:** Calendar, Tasks, Drive
- **GitHub:** API, Webhooks, Actions

---

## 8. Estatísticas do Ecossistema

| Organização | Repositórios |
|-------------|--------------|
| p31x070 | 42 |
| peixoto-ops | 50 |
| neaigd | 43 |
| **Total** | **135** |

**Projetos Prioritários:** ~20

---

## 9. Referência Importante

> **inv_sa_02** (peixoto-ops/inv_sa_02)  
> Ponto de início para buscas sobre andamentos processuais.  
> Todos os andamentos processuais devem ser rastreados a partir deste repositório.

---

## 10. Próximos Passos

1. Validar proposta com usuário
2. Criar repositório Git local
3. Implementar primeiro script de coleta
4. Testar cron job básico
5. Refinar iterativamente

---

## 11. Decisões Pendentes

1. Horário do cron: 22:00 ou 06:00?
2. Frequência: Diário ou dia-sim-dia-não?
3. Formato: Texto simples ou markdown?
4. Idioma: PT-BR ou EN para relatórios?

---

**Documento gerado automaticamente por Hermes Agent**  
**Metodologia: LKE v5.0 / Cognição Desacoplada**
