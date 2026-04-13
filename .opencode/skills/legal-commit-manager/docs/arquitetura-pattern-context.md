# Arquitetura: Pattern `lke_git_commiter` ↔ Contexto `commits_juridicos.md`

> **Propósito deste documento:** Registrar como o pattern Fabric e o arquivo de convenção interagem, o papel de cada um no fluxo de commits, e como a propriedade `project:` do frontmatter torna o modelo agnóstico ao projeto.

---

## 1. Visão Geral do Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│  git diff --cached                                              │
│       │                                                         │
│       ▼                                                         │
│  fabric -p lke_git_commiter -C commits_juridicos.md            │
│       │              │                                          │
│       │              └── CONTEXT: convenção de commits         │
│       │                   (tipos, escopos, limites, rodapé)    │
│       │                                                         │
│       ▼                                                         │
│  [Pattern extrai project: do frontmatter das notas no diff]    │
│       │                                                         │
│       ▼                                                         │
│  Mensagem de commit gerada → git commit -F -                    │
└─────────────────────────────────────────────────────────────────┘
```

**Comando de invocação:**
```bash
# Requer que o pattern e o contexto já estejam instalados (ver seção 6).
git diff --cached | fabric -p lke_git_commiter -C ~/.config/fabric/contexts/commits_juridicos.md
```

---

## 2. O Pattern: `lke_git_commiter/system.md`

### Localização
- **Canônico no repo:** `.opencode/skills/legal-commit-manager/patterns/lke_git_commiter/system.md`  ← **incluído neste repositório**
- **Instalado no Fabric:** `~/.config/fabric/patterns/lke_git_commiter/system.md`

### Responsabilidades do Pattern
O pattern é a **inteligência** do sistema. Ele recebe o diff bruto e o contexto da convenção e produz a mensagem final. Suas responsabilidades são:

| Responsabilidade                       | Descrição                                                                      |
|----------------------------------------|--------------------------------------------------------------------------------|
| Categorização semântica                | Escolhe `<type>` e `<scope>` corretos com base na convenção                    |
| Limites híbridos de tamanho            | 120 chars para jurídico, 72 para técnico                                       |
| Extração de `project:` do frontmatter  | Lê automaticamente a URL do projeto das notas modificadas                      |
| Geração do rodapé Kanban               | Estrutura `Project:`, `Relates-to:` e `Project-Status:` para o GitHub Actions |
| Validação antes da saída               | Verifica escopo (regex), tamanho do cabeçalho e consistência do rodapé         |

### O que o Pattern **não** faz
- Não executa `git commit` — apenas gera a string da mensagem.
- Não conhece a convenção de commits por si só — ela é injetada pelo contexto.
- Não busca o projeto no ambiente — ele lê do frontmatter das notas no diff.

---

## 3. O Contexto: `commits_juridicos.md`

### Localização
- **Canônico no repo:** `.opencode/skills/legal-commit-manager/references/commits_juridicos.md`  ← **incluído neste repositório**
- **Instalado no Fabric:** `~/.config/fabric/contexts/commits_juridicos.md`

### Responsabilidades do Contexto
O contexto é a **lei** do sistema. Ele não tem inteligência — é puro dado declarativo que governa o comportamento do pattern. Suas responsabilidades são:

| Responsabilidade                   | Descrição                                                                  |
|------------------------------------|----------------------------------------------------------------------------|
| Declarar os tipos jurídicos        | `docs`, `plan`, `ingest`, `research`, `petition`, `draft`, `audit`, etc.   |
| Declarar os tipos técnicos         | `feat`, `fix`, `refactor`, `test`, `chore`, etc.                           |
| Definir os escopos válidos         | Lista de escopos com regra de nomenclatura (só minúsculas e hífens)        |
| Fixar limites de tamanho por tipo  | 120 chars para jurídico, 72 para técnico                                   |
| Definir os valores de status Kanban| `Backlog`, `Ready`, `In progress`, `In review`, `Done`                     |
| Fornecer exemplos concretos        | Exemplos do caso Dianne Nicola para calibrar o estilo de saída             |

### O que o Contexto **não** faz
- Não é executado — é apenas lido pelo pattern como referência.
- Não precisa mudar quando o projeto muda (a URL de projeto vem do frontmatter).
- Não conhece os arquivos modificados — isso é responsabilidade do pattern.

---

## 4. Agnosticismo via `project:` no Frontmatter

### O Problema Anterior
Na versão anterior do pattern, o vínculo com o GitHub Project era um dado **externo**, injetado manualmente como "PROJECT METADATA (opcional)":
```
# chamada anterior — projeto hardcoded ou injetado manualmente
echo "$DIFF" | fabric -p lke_git_commiter -C commits_juridicos.md \
  --variable "project_url=https://github.com/orgs/peixoto-ops/projects/16"
```
Isso criava acoplamento: mudar de projeto exigia mudar o comando de invocação ou o script.

### A Solução: Frontmatter como SSOT do Projeto
Cada nota agora declara a qual projeto pertence diretamente no seu frontmatter YAML:
```yaml
---
id: 20260301-analise-sion
title: "Análise de Red Flags Contábeis - Sion Ltda."
project: https://github.com/orgs/peixoto-ops/projects/16
---
```

O pattern percorre os blocos `---` do diff, extrai o primeiro `project:` encontrado e o injeta no rodapé como `Project: <url>`.

### Benefícios
| Benefício                     | Impacto                                                                            |
|-------------------------------|------------------------------------------------------------------------------------|
| **Comando invariante**        | O comando `fabric -p lke_git_commiter -C commits_juridicos.md` nunca muda          |
| **Reutilizável em outros casos** | Basta as notas do novo caso terem `project:` diferente — sem alterar o pattern  |
| **Rastreabilidade na nota**   | A nota carrega seu próprio vínculo de projeto, visível no Obsidian                 |
| **Commits auto-documentados** | O histórico Git mostra qual projeto cada commit alimenta, sem metadado externo     |

### Comportamento quando `project:` está ausente
Se nenhuma nota no diff tiver `project:`, o pattern omite a linha `Project:` do rodapé silenciosamente — o rodapé começa com `Relates-to:`. Nunca é inventado um valor.

---

## 5. Responsabilidade de Cada Arquivo no Repositório

```
.opencode/skills/legal-commit-manager/
├── patterns/
│   └── lke_git_commiter/
│       └── system.md          ← PATTERN: inteligência, extrai project: do frontmatter
├── references/
│   └── commits_juridicos.md   ← CONTEXTO: convenção soberana de tipos, escopos, limites
└── docs/
    └── arquitetura-pattern-context.md   ← ESTE ARQUIVO: documentação da interação
```

---

## 6. Instalação / Sincronização com o Fabric

Para que o Fabric reconheça o pattern e o contexto, copie-os para os diretórios globais:

```bash
# Instalar o pattern
cp .opencode/skills/legal-commit-manager/patterns/lke_git_commiter/system.md \
   ~/.config/fabric/patterns/lke_git_commiter/system.md

# Instalar o contexto
cp .opencode/skills/legal-commit-manager/references/commits_juridicos.md \
   ~/.config/fabric/contexts/commits_juridicos.md
```

Após instalar, valide com:
```bash
fabric -l | grep lke_git_commiter          # confirma que o pattern está listado
fabric --listcontexts | grep commits       # confirma que o contexto está disponível
```

---

## 7. Referências

- [danielmiessler/fabric](https://github.com/danielmiessler/fabric) — framework que executa o pattern
- [GitHub Projects v16 — Peixoto-Ops](https://github.com/orgs/peixoto-ops/projects/16) — projeto atual do caso
- `commits_juridicos.md` — convenção soberana de commits (este repositório)
- `lke_git_commiter/system.md` — pattern Fabric (este repositório)
