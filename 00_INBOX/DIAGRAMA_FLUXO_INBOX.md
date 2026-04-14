---
status: active
created: 2026-04-14
tipo: documentacao_sistema
tags: [fluxo, inbox, mermaid, diagrama]
related:
  - "[[FLUXO_INBOX]]"
---

# Diagrama do Fluxo da Inbox

## Visão Geral do Sistema

```mermaid
flowchart TD
    subgraph ENTRADA["📥 ENTRADA DE DEMANDAS"]
        A[Nota/Disputa Criada] --> B{Classificar Tipo}
        B -->|demanda| C[Tarefa/Pedido]
        B -->|sessao| D[Registro de Sessão]
        B -->|analise| E[Análise Técnica]
        B -->|proposta| F[Sugestão/Alternativa]
        B -->|delegacao| G[Tarefa Delegada]
    end

    subgraph PROCESSAMENTO["⚙️ PROCESSAMENTO"]
        C & D & E & F & G --> H[Adicionar Frontmatter]
        H --> I[status: pending]
        I --> J[Colocar em 00_INBOX/]
    end

    subgraph TRABALHO["🔧 EM ANDAMENTO"]
        J --> K{Iniciar Trabalho?}
        K -->|Sim| L[status: in_progress]
        K -->|Não| J
        L --> M[Executar Tarefa]
        M --> N{Concluído?}
        N -->|Não| L
        N -->|Sim| O[status: resolved]
    end

    subgraph ARQUIVAMENTO["📁 ARQUIVAMENTO"]
        O --> P[Mover para 01_ARQUIVADAS/]
        P --> Q[Adicionar data resolved]
        Q --> R[Adicionar commits relacionados]
        R --> S[Arquivado ✓]
    end

    subgraph CONFLITOS["⚠️ VERIFICAÇÃO DE CONFLITOS"]
        T[Próximos Passos] --> U{Já Previsto?}
        U -->|Sim| V[Atualizar Roadmap]
        U -->|Não| W{Conflita?}
        W -->|Sim| X[Resolver Conflito]
        W -->|Não| Y[Adicionar ao Roadmap]
        X --> Y
    end

    M --> T
```

---

## Ciclo de Vida de uma Nota

```mermaid
stateDiagram-v2
    [*] --> pending: Nota criada
    pending --> in_progress: Trabalho iniciado
    in_progress --> pending: Bloqueado/Espera
    in_progress --> resolved: Tarefa concluída
    resolved --> [*]: Arquivado em 01_ARQUIVADAS/
    
    pending --> pending: Atualização de próximos passos
    in_progress --> in_progress: Progresso documentado
```

---

## Estrutura de Pastas

```mermaid
graph LR
    subgraph INBOX["00_INBOX/"]
        PEND[Pendentes<br/>status: pending]
        PROG[Em Progresso<br/>status: in_progress]
        ARQ[01_ARQUIVADAS/<br/>status: resolved]
    end
    
    subgraph META["90_META/"]
        PLAN[Planos de Longo Prazo]
    end
    
    subgraph REF["10_REFERENCIAS/"]
        DOC[Documentação de Referência]
    end
    
    subgraph DOCS["40_DOCUMENTOS/"]
        REL[Relatórios Finais]
    end
    
    PEND -->|"Não arquivar"| META
    PEND -->|"Não arquivar"| REF
    ARQ -->|"Só resolvidos"| REL
```

---

## Frontmatter Obrigatório

```mermaid
classDiagram
    class NotaInbox {
        +status: pending | in_progress | resolved
        +created: YYYY-MM-DD
        +tipo: demanda | sessao | analise | proposta | delegacao
        +tags: string[]
        +related: wikilink[]
        +proximos_passos: string[]
    }
    
    class NotaArquivada {
        +status: resolved
        +resolved: YYYY-MM-DD
        +commits: string[]
    }
    
    NotaInbox <|-- NotaArquivada
```

---

## Processo de Decisão

```mermaid
flowchart LR
    A[Nova Demanda] --> B{Já existe similar?}
    B -->|Sim| C[Adicionar related]
    B -->|Não| D[Criar nova nota]
    C --> E[Verificar próximos passos]
    D --> E
    E --> F{Conflita com existente?}
    F -->|Sim| G[Resolver conflito]
    F -->|Não| H[Adicionar ao Roadmap]
    G --> H
```

---

## Regras de Ouro

1. **Separar** resolvidos de pendentes (nunca misturar)
2. **Wikilinks** para conectar notas relacionadas
3. **Frontmatter** completo em todas as notas
4. **Próximos passos** sempre verificados contra Roadmap
5. **Commits** referenciados nas notas arquivadas

---

*Diagrama criado para documentar o sistema de inbox do secretario-agente-lke*
