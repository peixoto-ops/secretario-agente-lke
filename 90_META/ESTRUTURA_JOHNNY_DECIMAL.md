# Estrutura Johnny.Decimal - Secretário-Agente LKE

Este diretório segue o sistema Johnny.Decimal para organização.

## Categorias

| Categoria | Descrição |
|-----------|-----------|
| **00-09** | Entrada, Inbox, Captura |
| **10-19** | Referências, Documentação Base |
| **20-29** | Propostas, Planejamento |
| **30-39** | Implementação, Código |
| **40-49** | Documentos Gerados, Outputs |
| **50-59** | Automação, Cron Jobs |
| **60-69** | Diagnósticos, Logs |
| **90-99** | Meta, Configuração |

## Diretórios

### 00_INBOX
Entrada de demandas e inputs manuais.

### 10_REFERENCIAS
Documentação de referência, incluindo credenciais sensíveis.

### 20_PROPOSTAS
Propostas de soluções, alternativas avaliadas.

### 30_IMPLEMENTACAO
Scripts Python, código do agente.

### 40_DOCUMENTOS
Relatórios gerados, outputs do sistema.

### 50_CRON_JOBS
Configurações de automação e cron jobs.

### 60_DIAGNOSTICOS
Logs de execução, diagnósticos de erro.

### 90_META
Documentação sobre a própria estrutura.

---

## Convenções

1. Arquivos em `credentials/` nunca são commitados
2. Logs em `60_DIAGNOSTICOS/` são rotativos
3. Relatórios em `40_DOCUMENTOS/` seguem padrão de nomenclatura com data
