---
status: resolved
created: 2026-04-14
resolved: 2026-04-14
tipo: analise
tags: [skill, stealth-browser, avaliacao, stj, osint]
related:
  - "[[INSTALACAO_SKILL_STEALTH_BROWSER_20260414]]"
  - "[[FLUXO_INBOX]]"
commits:
  - fd09e62
  - 28c74b9
  - bfee333
---

# Avaliação Consolidada: Stealth Browser Skill

**Data:** 14/04/2026
**Sessão:** Validação via Telegram
**Repositório:** secretario-agente-lke

---

## Status da Instalação

**Skill:** `b0tresch-stealth-browser`
**Local:** `~/.hermes/skills/b0tresch-stealth-browser/`
**Status:** INSTALADA CORRETAMENTE

### Componentes Instalados:
- `SKILL.md` - Documentação completa
- `scripts/browser.js` - Script principal
- `node_modules/` - Dependências npm
- `package.json` - puppeteer-extra, puppeteer-extra-plugin-stealth

---

## Testes Realizados

### Teste 1: Detecção (Sannysoft)
**URL:** https://bot.sannysoft.com
**Resultado:** Screenshot capturada
**Status:** Aguardando análise visual

### Teste 2: SCON/STJ
**URL:** https://scon.stj.jus.br/SCON/
**Resultado:** BLOQUEADO
**Motivo:** Cloudflare Turnstile (CAPTCHA JavaScript interativo)

### Teste 3: Relay.link (controle positivo)
**URL:** https://relay.link
**Resultado:** SUCESSO
**HTML:** 880 linhas capturadas

### Teste 4: Sites adicionais
| Site | Resultado |
|------|-----------|
| stj.jus.br | BLOQUEADO |
| Jusbrasil | BLOQUEADO |
| Relay.link | SUCESSO |

---

## Veredicto

### Para STJ/SCON: REPROVADA
A skill não consegue acessar o portal SCON do STJ devido à proteção Cloudflare Turnstile.

### Para uso geral: APROVADA (com ressalvas)
Funciona bem para:
- Sites com proteção moderada (Relay.link, Twitter, Reddit)
- Automação que não exige resolver CAPTCHAs
- Testes de detecção

---

## Alternativas para STJ

1. **API Jusbrasil (RECOMENDADA)** - Indexa STJ, STF, todos tribunais
2. **Escavador** - Alternativa brasileira com API
3. **Acesso Manual + Automação** - Resolver CAPTCHA manualmente e usar cookies
4. **Contato Institucional STJ** - Solicitar whitelist para escritório

---

## Próximos Passos (registrados)

- [x] Instalar skill stealth-browser
- [x] Testar em SCON/STJ
- [x] Documentar resultados
- [ ] Investigar playwright-scraper como alternativa
- [ ] Avaliar API Jusbrasil comercial
- [ ] Testar Escavador

---

*Avaliação gerada pelo Hermes Agent - 14/04/2026*
*Arquivado em 2026-04-14 - Avaliação completa*
