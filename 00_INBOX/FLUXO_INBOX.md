---
tipo: documentacao_sistema
categoria: workflow
tags: [inbox, organizacao, fluxo]
status: ativo
version: 1.0
criado: 2026-04-14
---

# Fluxo da Caixa de Entrada - SECRETARIO-AGENTE-LKE

## Propósito

O sistema de caixa de entrada (`00_INBOX/`) gerencia demandas, notas de sessões e pedidos que chegam ao Secretário-Agente LKE.

---

## Estrutura de Pastas

```
00_INBOX/
├── 01_ARQUIVADAS/     # Demandas resolvidas (não se misturam com pendentes)
│   └── *.md           # Notas com status: resolved no frontmatter
├── STATUS_ATUAL.md    # Visão geral do sistema
└── [demandas].md      # Demandas pendentes (status: pending)
```

---

## Regras de Frontmatter

### Para TODAS as notas na 00_INBOX

```yaml
---
status: pending | resolved | in_progress
created: YYYY-MM-DD
resolved: YYYY-MM-DD (apenas se status: resolved)
related: [lista de notas relacionadas]
tags: [classificacao]
tipo: demanda | sessao | analise | proposta | delegacao
---
```

### Classificação de Status

| Status | Significado | Local |
|--------|-------------|-------|
| `pending` | Aguardando ação | `00_INBOX/` |
| `in_progress` | Sendo trabalhada | `00_INBOX/` |
| `resolved` | Concluída, arquivada | `00_INBOX/01_ARQUIVADAS/` |

---

## Tipos de Notas

1. **demanda** - Pedido de ação ou tarefa
2. **sessao** - Registro de sessão de trabalho
3. **analise** - Análise técnica ou investigação
4. **proposta** - Sugestão ou alternativa
5. **delegacao** - Tarefa delegada de outro agente

---

## Wikilinks e Relacionamentos

Use wikilinks `[[Nome da Nota]]` para conectar notas relacionadas.

### Campo `related` no Frontmatter

```yaml
related:
  - "[[INSTALACAO_SKILL_STEALTH_BROWSER_20260414]]"
  - "[[AVALIACAO_STEALTH_BROWSER_20260414]]"
```

---

## Fluxo de Arquivamento

1. **Nota criada** → status: `pending`
2. **Trabalho iniciado** → status: `in_progress`
3. **Tarefa concluída** → status: `resolved`
4. **Arquivamento** → mover para `01_ARQUIVADAS/`

### Critérios para Arquivamento

- Demanda foi atendida completamente
- Não há próximos passos pendentes
- Resultado foi documentado em local apropriado (README, commits, etc.)

---

## Notas que NÃO são arquivadas

- Planos de longo prazo (devem ir para `90_META/`)
- Documentação de referência (devem ir para `10_REFERENCIAS/`)
- Relatórios finais (devem ir para `40_DOCUMENTOS/`)

---

## Manutenção

- Revisar semanalmente a 00_INBOX
- Arquivar notas resolvidas
- Atualizar status das pendentes
- Verificar conflitos entre próximos passos
