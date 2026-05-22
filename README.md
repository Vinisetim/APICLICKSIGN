# Multas ClickSign — Automação de Vale (Clicksign API v3)

Este repositório contém uma automação em **Python** para integração com a **Clicksign API v3 (Sandbox)**, com foco em **gerar um Vale (documento)** a partir de um **template Clicksign** e montar o fluxo técnico de assinatura:
**envelope → documento (via template) → signatário → requisitos**. 

>  Estado atual (resumo): o fluxo técnico já está funcional para criar o Vale via template e montar os requisitos.
> Ainda NÃO existe a implementação completa de negócio para:
> - criar um registro “vale por vale” no banco interno;
> - identificar/vincular o **responsável pela multa** ao Vale;
> - disparar a **notificação do responsável** de forma integrada ao processo de multas.

---

##  Estado atual do projeto (maio/2026)

###  O que já funciona
- **Envelope**: criação e consulta de detalhes do envelope (ID armazenado para as próximas etapas).
- **Documento (Vale) via Template**: criação de documento usando **template Clicksign** (DOCX) com tags de assinatura.
- **Signatário**: criação do signatário com configuração compatível com o template.
- **Requisitos**:
  - requisito de assinatura (`agree`)
  - requisito de autenticação (`provide_evidence`, ex.: e-mail)
- **Ativação do envelope**: atualização de `status` para `running` após requisitos completos.
- **Notificação** : envio de notificação de solicitação de assinatura após ativação.
  - A resposta da API retorna um `summary` com `notified: true` para os signatários notificados.

###  Notificações (como funciona)
As notificações via API devem ser executadas **após o envelope estar em `running`**.  
Elas são entregues ao signatário pelo canal configurado em `communicate_events.signature_request`.  

> Observação: existe rate-limit de **1 notificação por minuto por endpoint**.

>  Observação: a ativação é a etapa mais sensível e depende do alinhamento entre tag do template, `key` do signatário e `role` do requisito.

###  Parcial / em consolidação
- **Notificação**: existe implementação do endpoint de notificação, mas:
  - o fluxo “notificar o responsável pela multa” ainda não está integrado ao processo de negócio;
  - e o `signer` pode estar configurado com `signature_request: "none"` (sem canal de envio) dependendo do módulo/versão em uso.

###  Ainda não implementado (lacunas de negócio)
- **Persistência em banco (Vale por Vale)**:
  - criar/atualizar um registro por multa (rastreabilidade) com IDs gerados (`envelope_id`, `document_id`, `signer_id`, requirements etc.) e status do processo.
- **Vinculação ao responsável pela multa**:
  - identificar quem é o responsável na base interna e criar/vincular esse signatário ao Vale.


##  Regra crítica do Template (tag ↔ key ↔ role)

Para a assinatura aparecer corretamente e o envelope ativar sem erro, **três valores precisam estar alinhados**:

- **Tag no DOCX**: `{{~position_sign_signer1}}`
- **Signer.key**: `signer1`
- **Requirement.role**: `signer1`

Se qualquer um deles divergir, o envelope pode ser criado, mas a ativação e/ou assinatura podem falhar.

---

##  Estrutura do projeto

- `main.py` — orquestra o fluxo (sem payloads complexos)
- `config.py` — URL base, headers, token e constantes (ex.: template)
- `clicksign_api/services/`
  - `envelope.py`
  - `documento.py`
  - `signatario.py`
  - `requisitos.py`
  - `notificacao.py`
- `clicksign_api/utils/base64_utils.py` — utilitário legado (Base64), apesar do foco atual ser template
- `clicksign_api/testes/teste_main.py` — testes do fluxo

---

##  Requisitos

- Python 3.x
- `requests`
- Conta Clicksign **Sandbox**
- Template Clicksign publicado com tags de assinatura (`{{~position_sign_*}}`)

Instale dependências:
```bash
pip install -r requirements.txt
