---
status: pending
created: 2026-04-14
tipo: proposta
tags: [docker, kali, openclaw, osint, inspirion, hermes]
related:
  - "[[FLUXO_INBOX]]"
  - "[[INSTALACAO_SKILL_STEALTH_BROWSER_20260414]]"
proximos_passos:
  - Avaliar necessidade vs API Jusbrasil
  - Configurar Docker no Inspirion
  - Implementar skill deep-osint
---

# Docker Kali no Inspirion via Hermes

**Fonte:** Conversa com Gemini sobre vídeo do OpenClaw
**Vídeo:** [I Built an AI Agent That Hacks for Me | OpenClaw + Kali Linux](https://youtu.be/C5ir_rQ4L4g?si=KbBTIfUZTuaDX4_o)

---

## Proposta Original

Usar o OpenClaw em um container Docker no Inspirion para que o Hermes interaja e faça buscas OSINT, distribuindo a carga de trabalho entre os nós da rede Tailscale.

---

## Análise do Gemini

Essa arquitetura é não apenas possível, mas é a implementação ideal do conceito de **computação distribuída** que você vem estruturando. Delegar a carga de trabalho de OSINT (que exige bibliotecas pesadas de rede e processamento de dados brutos) para o **Inspirion**, enquanto o **Hermes** mantém a orquestração e o raciocínio jurídico no **Aspire**, preserva a performance de ambos os nós.

---

## Arquitetura Proposta

### I - Configuração do Ambiente no Inspirion

#### 1. Preparação do Host via Hermes
```bash
ssh user@inspirion-tailscale-ip << 'EOF'
sudo apt update && sudo apt install -y docker.io docker-compose git
sudo systemctl enable --now docker
EOF
```

#### 2. Implantação do Container Kali/OpenClaw
```dockerfile
FROM kalilinux/kali-rolling
RUN apt update && apt install -y curl git python3 python3-pip npm nodejs
RUN npm install -g @openclaw/cli
WORKDIR /app
ENTRYPOINT ["openclaw"]
```

### II - Orquestração de Chaves e Segurança

O Hermes lê o .env local no Aspire e passa para o Docker no Inspirion:
- TAVILY_API_KEY
- SHODAN_API_KEY
- OPENCLAW_TOKEN

### III - Integração ao Fluxo LKE 5.0

Criar tool "Deep_OSINT":
- **User → Hermes (Aspire):** "Pesquise a pegada digital da empresa X."
- **Hermes → SSH (Inspirion):** `docker exec openclaw-worker openclaw run skill-osint-deep "empresa X"`
- **Inspirion → Hermes:** Retorno do JSON/Markdown

---

## Nota de Segurança

⚠️ Certificar que a política de ACL do Tailscale permite comunicação na porta 22 entre Aspire e Inspirion, mas bloqueia acessos externos ao container do OpenClaw.

---

## Status Atual

| Item | Status |
|------|--------|
| Análise conceitual | ✅ Feita |
| Necessidade avaliada | ❌ Pendente |
| Docker configurado | ❌ Não |
| Skill implementada | ❌ Não |

---

## Consideração Importante

A skill `stealth-browser` já foi avaliada como **REPROVADA para STJ**. O OpenClaw pode ser uma alternativa para OSINT mais profundo, mas deve ser comparado com:

1. API Jusbrasil (comercial, mais confiável)
2. Escavador (alternativa brasileira)
3. Acesso manual + automação com cookies

---

*Proposta registrada em 2026-04-14*
