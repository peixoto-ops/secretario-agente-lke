# Guia de Estilo — Convenção de Commits Jurídicos LKE v2.0

> **Uso:** Este arquivo é injetado como contexto no Fabric via flag `-C commits_juridicos.md` ao invocar o pattern `lke_git_commiter`. Ele define as regras soberanas de categorização, tamanho e rodapé que o pattern deve seguir.

---

## 1. Estrutura Geral

```
<type>(<scope>): <descrição>

<corpo explicando o "porquê" em bullet points>

[rodapé opcional com Project:, Relates-to: e Project-Status:]
```

---

## 2. Tipos (`<type>`)

### 2.1 Commits Jurídicos — limite de **120 caracteres** no cabeçalho
Use verbosidade para preservar precisão processual.

| Tipo          | Quando usar                                                         |
|---------------|---------------------------------------------------------------------|
| `docs`        | Documentação processual, manuais, guias operacionais                |
| `plan`        | Planejamento estratégico, roadmap, checklists de fase               |
| `ingest`      | Importação, OCR, conversão de documentos brutos do caso             |
| `research`    | Pesquisa jurídica genérica                                          |
| `precedent`   | Jurisprudência e precedentes (STJ, STF, TJ)                        |
| `doctrine`    | Doutrina jurídica                                                   |
| `legislation` | Análise ou referência a normas e leis                               |
| `analysis`    | Análise técnica ou estratégica do caso                              |
| `draft`       | Rascunho de peça processual                                         |
| `petition`    | Petição finalizada ou em versão avançada                            |
| `audit`       | Auditoria de documentos, metadados ou fluxo                         |
| `review`      | Revisão e validação de conteúdo jurídico                            |

### 2.2 Commits Técnicos — limite de **72 caracteres** no cabeçalho
Use concisão; detalhes vão no corpo.

| Tipo       | Quando usar                                               |
|------------|-----------------------------------------------------------|
| `feat`     | Nova funcionalidade no sistema/scripts                    |
| `fix`      | Correção de bug ou dado incorreto                         |
| `refactor` | Reorganização de código ou estrutura sem mudança funcional|
| `test`     | Adição ou atualização de testes                           |
| `chore`    | Tarefas de manutenção (configs, deps, gitignore)          |
| `style`    | Formatação, espaçamento, sem alteração lógica             |
| `perf`     | Otimização de performance                                 |
| `ci`       | Alterações em pipelines CI/CD e GitHub Actions            |
| `build`    | Alterações no sistema de build                            |

---

## 3. Escopos (`<scope>`)

**Regra absoluta:** apenas letras minúsculas e hífens (`^[a-z\-]+$`). Sem underlines, números ou maiúsculas.

### Escopos por domínio

| Escopo                   | Domínio                                           |
|--------------------------|---------------------------------------------------|
| `caso-dianne`            | Fatos e estratégia do caso Dianne Nicola          |
| `caso-sion`              | Societário / Administradora Sion Ltda.            |
| `tese-uniao-estavel`     | Tese de União Estável / Separação de Fato         |
| `tese-patrimonio`        | Tese patrimonial / inventário                     |
| `peticao-inicial`        | Petição inicial do inventário                     |
| `evidencias`             | Documentos de prova                               |
| `precedentes-stj`        | Jurisprudência STJ                                |
| `kanban`                 | Gestão do Kanban no GitHub Projects               |
| `patterns`               | Patterns do Fabric                                |
| `system`                 | Infraestrutura e configuração do sistema LKE      |
| `agents`                 | Agentes e orquestração do OpenCode                |
| `templates`              | Templates de notas e peças processuais            |
| `workflows`              | GitHub Actions e automações                       |
| `vault`                  | Estrutura e organização do vault Obsidian         |

---

## 4. Corpo do Commit

- Use marcadores (`-`) para listar o que foi feito.
- Explique o **"porquê"**, não apenas o "o quê".
- Para commits jurídicos: referencie teses, artigos de lei, precedentes quando relevante.
- Máximo recomendado: 72 caracteres por linha no corpo.

**Exemplo:**
```
- Adiciona declaração de separação de fato fundamentada no Art. 1.723 CC
- Remove duplicata importada via Drive em 2026-02-13
- Atualiza hash de rastreabilidade após edição do frontmatter
```

---

## 5. Rodapé (Kanban + Projeto)

O rodapé ativa os workflows do GitHub Actions (GraphQL V2). Deve estar separado do corpo por **uma linha em branco**.

### 5.1 Propriedade `project:` no frontmatter (agnosticismo de projeto)
Quando as notas modificadas possuem `project:` no frontmatter YAML, o valor é auto-extraído pelo pattern e inserido como primeira linha do rodapé:

```
Project: https://github.com/orgs/peixoto-ops/projects/16
Relates-to: Título da tarefa ou numero
Project-Status: In progress
```

Se `project:` não estiver presente nas notas, o rodapé começa com `Relates-to:` diretamente.

### 5.2 Valores válidos para `Project-Status:`

| Status       | Quando usar                                         |
|--------------|-----------------------------------------------------|
| `Backlog`    | Tarefa registrada mas não iniciada                  |
| `Ready`      | Pronta para execução                                |
| `In progress`| Em execução neste commit                            |
| `In review`  | Aguardando revisão                                  |
| `Done`       | Concluída                                           |

### 5.3 Regras absolutas do rodapé
- Se `Relates-to:` estiver presente, `Project-Status:` é **obrigatório** na linha seguinte.
- Se `Project:` estiver presente, deve ser a **primeira linha** do rodapé.
- Nunca invente URLs de projeto; se não houver `project:` no frontmatter, omita `Project:`.

---

## 6. Exemplos Completos

### Commit jurídico (com `project:` no frontmatter)
```
analysis(tese-uniao-estavel): Estruturação da tese de separação de fato com base em provas documentais - Dianne Nicola

- Consolida declarações de testemunhas com endereços distintos desde 2018
- Mapeia ausência de comunhão de vida nas contas bancárias do período
- Vincula ao Art. 1.723 §1º CC e precedente REsp 1.847.626/SP (STJ)

Project: https://github.com/orgs/peixoto-ops/projects/16
Relates-to: T1-004 Depoimento estruturado da cliente
Project-Status: In progress
```

### Commit técnico (sem `project:` — arquivo de sistema)
```
feat(patterns): adicionar extração de project: do frontmatter no lke_git_commiter

- Torna o rodapé de projeto auto-descoberto a partir das notas
- Elimina necessidade de injeção manual de PROJECT METADATA
```

### Commit jurídico (sem `project:` no frontmatter)
```
ingest(evidencias): importação de 3 contratos societários da Mazer pré-óbito para análise forense

- Digitalização dos contratos de 2019, 2021 e 2022 via OCR
- Aplicado hash SHA-256 para cadeia de custódia

Relates-to: Auditoria Contábil Pré-Óbito
Project-Status: In progress
```

---

## 7. Regras Absolutas (Nunca Violar)

1. **Escopo sem underline:** `caso-dianne` ✅ | `caso_dianne` ❌
2. **Cabeçalho jurídico ≤ 120 chars**, técnico ≤ 72 chars.
3. **`Project-Status:` sempre após `Relates-to:`** (mesma sequência).
4. **`Project:` nunca inventado** — apenas se extraído do frontmatter.
5. **Idioma:** Português do Brasil em toda a mensagem.
6. **Sem blocos de código** na saída — retornar apenas a string crua do commit.
