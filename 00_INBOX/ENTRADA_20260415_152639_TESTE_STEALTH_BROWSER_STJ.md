# Relatório de Teste: Stealth Browser vs STJ

**Data:** 14/04/2026
**Sessão:** T1.x (validação via Telegram)
**Responsável:** Hermes Agent

---

## Sumário Executivo

**RESULTADO: SKILL REPROVADA**

A skill `b0tresch-stealth-browser` não consegue acessar o portal SCON do STJ devido à proteção Cloudflare Turnstile (CAPTCHA JavaScript interativo).

---

## Testes Realizados

### 1. Teste de Detecção (Sannysoft)

```
URL: https://bot.sannysoft.com
Status: Screenshot capturada (aguardando análise visual)
Arquivo: teste_detecao_sannysoft.png
```

### 2. Teste SCON/STJ (alvo principal)

```
URL: https://scon.stj.jus.br/SCON/
Status: BLOQUEADO
Proteção: Cloudflare Turnstile
Resposta: "Just a moment..." - página de verificação
```

### 3. Teste Relay.link (controle positivo)

```
URL: https://relay.link
Status: SUCESSO
HTML capturado: 880 linhas
```

### 4. Sites Adicionais Testados

| Site | Resultado |
|------|-----------|
| stj.jus.br (principal) | BLOQUEADO |
| Jusbrasil | BLOQUEADO |
| Relay.link | SUCESSO |

---

## Diagnóstico Técnico

### Por que a skill falhou:

1. **Cloudflare Turnstile**: CAPTCHA JavaScript que requer interação humana ou solving service
2. **IP Datacenter**: Sem proxy residencial, IPs de servidor são automaticamente suspeitos
3. **Fingerprinting avançado**: STJ usa múltiplas camadas de detecção

### O que a skill faz bem:

- Remove flag `navigator.webdriver`
- Spoofa user agent realista
- Funciona em sites com proteção moderada (ex: Relay.link)

### O que falta:

- Resolver CAPTCHAs (requer 2captcha ou similar)
- IP residencial (requer Smartproxy ou similar)
- Evasões mais avançadas para fingerprinting

---

## Alternativas para Pesquisa STJ

### Opção 1: Serviços de API de Jurisprudência

Serviços que já indexam STJ e oferecem API:

- **Jusbrasil Pro**: API comercial (requer assinatura)
- **Escavador**: API de jurisprudência
- **InJuria**: Base de dados jurídica

### Opção 2: e-SAJ Alternativo

Alguns tribunais usam e-SAJ que pode ter API menos restritiva:
- Verificar se STJ tem endpoint alternativo

### Opção 3: Acesso Manual + Automação

1. Abrir sessão manualmente no browser
2. Exportar cookies/session
3. Usar automação com sessão já autenticada

### Opção 4: Solução Combinada

Investir em:
1. Proxy residencial (Smartproxy ~$7.50/GB)
2. CAPTCHA solving (2captcha ~$3/1000 solves)
3. Configurar na infraestrutura

---

## Conclusão

A skill `stealth-browser` serve para sites com proteção moderada, mas **não é solução para STJ/SCON**.

**Recomendação:** Buscar solução de API comercial ou configurar infraestrutura completa (proxy + CAPTCHA solver).

---

## Alternativas Concretas para Pesquisa STJ

### 1. API Jusbrasil (RECOMENDADA)

**Vantagens:**
- Indexa STJ, STF, todos os tribunais
- API REST oficial
- Sem bloqueio Cloudflare
- Dados estruturados

**Como usar:**
```bash
# Documentação: https://api.jusbrasil.com.br/
# Requer conta comercial
```

**Custo:** Assinatura mensal (verificar valores atuais)

### 2. Escavador

**Site:** https://www.escavador.com
**API:** https://api.escavador.com

- Alternativa brasileira ao Jusbrasil
- Busca em jurisprudência
- API disponível

### 3. Acesso Manual + Automação de Sessão

**Workflow:**
1. Abrir browser manual (Firefox/Chrome)
2. Resolver CAPTCHA Cloudflare
3. Exportar cookies de sessão
4. Usar cookies em automação posterior

**Ferramentas:**
- `browser-cookie3` (Python) - extrai cookies
- Selenium/Playwright com cookies injetados

### 4. Contato Institucional com STJ

**CSID/STJ (Coordenadoria de Segurança e Defesa Cibernética):**
- Telefone: (61) 3319-9393
- Email: sac@stj.jus.br
- Atendimento: Seg-Sex, 7h-20h

**Solicitação possível:**
- Acesso institucional para escritório de advocacia
- Whitelist de IP para pesquisa acadêmica
- API oficial (se disponível)

### 5. Solução Técnica Completa (custo)

Se automatização for crítica:

| Componente | Serviço | Custo |
|------------|---------|-------|
| Proxy Residencial | Smartproxy | ~$7.50/GB |
| CAPTCHA Solver | 2captcha | ~$3/1000 |
| Browser Automation | Puppeteer | Gratuito |

**Investimento inicial:** ~$50-100/mês para uso moderado

---

## Recomendação Final

**PARA USO IMEDIATO:**
1. Usar Jusbrasil/Escavador para pesquisa de jurisprudência STJ
2. Acesso manual ao SCON quando necessário

**PARA AUTOMAÇÃO:**
1. Avaliar API Jusbrasil comercial
2. Ou investir em infraestrutura completa (proxy + CAPTCHA solver)

---

## Próximos Passos

1. [x] Documentar skill como REPROVADA para STJ
2. [ ] Testar API Jusbrasil (requer cadastro)
3. [ ] Testar Escavador como alternativa
4. [ ] Avaliar contato com CSID/STJ para acesso institucional

---

*Relatório gerado pelo Hermes Agent - 14/04/2026*
