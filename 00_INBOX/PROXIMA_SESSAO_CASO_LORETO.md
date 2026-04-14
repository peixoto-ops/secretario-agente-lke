# PRÓXIMA SESSÃO - NOTA

**Data:** 2026-04-14
**Repositório alvo:** caso-loreto-vivas

---

## Planejamento

Testar as ferramentas do Secretário-Agente no repositório `/media/peixoto/Portable/caso-loreto-vivas`:

1. Verificar atividade recente (`git log`, commits, branches)
2. Registrar o repositório no banco (se não estiver cadastrado)
3. Criar sessão de trabalho com resumo Fabric
4. Registrar artefatos e atividades no banco
5. Testar query SQL para recuperar histórico

---

## Comandos para iniciar

```bash
cd /media/peixoto/Portable/caso-loreto-vivas
git log --oneline -10
git status

cd /media/peixoto/Portable/secretario-agente-lke
source venv/bin/activate
python 30_IMPLEMENTACAO/secretario_cli.py status
python 30_IMPLEMENTACAO/secretario_cli.py repos
```

---

## Objetivo

Validar na prática o fluxo de registro de sessões e consultas, usando um caso real do portfólio.
