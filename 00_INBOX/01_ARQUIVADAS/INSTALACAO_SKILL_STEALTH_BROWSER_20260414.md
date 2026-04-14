---
status: resolved
created: 2026-04-14
resolved: 2026-04-14
tipo: demanda
tags: [skill, stealth-browser, instalacao, osint]
related:
  - "[[AVALIACAO_STEALTH_BROWSER_20260414]]"
  - "[[FLUXO_INBOX]]"
commits:
  - d0fdadd
  - fd09e62
---

# Instalação: Skill Stealth Browser

**Data:** 14/04/2026 
**Sessão:** T1.x (instalação via Telegram) 
**Fonte:** ClawHub - https://clawhub.ai/b0tresch/b0tresch-stealth-browser 
**Versão:** v1.1.0 

---

## Status da Instalação

✅ **INSTALADA COM SUCESSO**

**Local:** `~/.hermes/skills/b0tresch-stealth-browser/` 
**Nome no sistema:** `stealth-browser` 
**Dependências:** puppeteer-extra, puppeteer-extra-plugin-stealth, puppeteer (instaladas via npm)

---

## O Que a Skill Faz

Navegação web com anti-detecção que:

1. **Burla bot detection** - Remove flag `navigator.webdriver`, spoofa user agent
2. **Burla Cloudflare/Vercel protection** - Aplica evasões stealth automáticas
3. **Funciona em sites que detectam automação:**
 - Reddit (bloqueio de IP datacenter)
 - Twitter/X profiles
 - Fluxos de signup
 - Faucet sites com proteção
 - Relay.link (testado - bloqueio Vercel ultrapassado)

4. **Suporte opcional a proxy residencial Smartproxy** - Para bypass de bloqueios baseados em IP

---

## Comandos Básicos

```bash
# Uso básico (stealth only, sem proxy)
node ~/.hermes/skills/b0tresch-stealth-browser/scripts/browser.js "https://example.com"

# Com proxy residencial (recomendado para IP blocks)
node ~/.hermes/skills/b0tresch-stealth-browser/scripts/browser.js "https://example.com" --proxy

# Capturar screenshot
node ~/.hermes/skills/b0tresch-stealth-browser/scripts/browser.js "https://example.com" --proxy --screenshot output.png

# Extrair HTML
node ~/.hermes/skills/b0tresch-stealth-browser/scripts/browser.js "https://example.com" --proxy --html

# Extrair texto
node ~/.hermes/skills/b0tresch-stealth-browser/scripts/browser.js "https://example.com" --proxy --text
```

---

## Resultado da Avaliação

Ver [[AVALIACAO_STEALTH_BROWSER_20260414]] para detalhes completos.

**Para STJ/SCON:** REPROVADA - Cloudflare Turnstile bloqueia
**Para uso geral:** APROVADA com ressalvas

---

*Arquivado em 2026-04-14 - Instalação e avaliação completas*
