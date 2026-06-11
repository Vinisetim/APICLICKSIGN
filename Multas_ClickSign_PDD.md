# PDD - Documento de Descrição do Projeto: Multas ClickSign

## 1. Finalidade deste documento
Este PDD descreve o estado atual do projeto **Multas ClickSign**, suas regras de negócio, arquitetura, decisões técnicas, fluxo técnico validado, erros conhecidos e próximos passos.  
Este documento foi atualizado para servir como contexto de continuidade para novos chats de IA, pessoas desenvolvedoras que precisem assumir o projeto, revisão técnica futura e documentação interna da automação.

## 2. Visão geral do sistema
O **Multas ClickSign** é uma automação em Python para envio de documentos de autorização de desconto de multas para assinatura digital via **Clicksign API v3**.  
O projeto saiu de um fluxo unitário de teste e evoluiu para um fluxo orientado por planilha. Cada linha válida representa uma multa que pode gerar um envelope individual.

### 🎯 Objetivo
- Reduzir etapas manuais
- Diminuir retrabalho
- Evitar erros
- Permitir envio em lote controlado

## 3. Estado atual validado
O fluxo está validado localmente em ambiente **sandbox**.

### 3.1 Etapas funcionando
1. Ler planilha Excel local
2. Filtrar status_vale = "Não enviado"
3. Validar campos mínimos
4. Criar envelope
5. Criar signatário (telefone)
6. Enviar assinatura via SMS
7. Criar documento via template
8. Preencher template.data
9. Criar requisitos de assinatura
10. Criar requisito de autenticação (SMS/WhatsApp)
11. Aguardar processamento Clicksign
12. Ativar envelope
13. Notificar signatário
14. Atualizar status_vale = "Enviado"

### 3.2 Validação recente importante
✔ SMS funcionando com telefone da planilha  
✔ Não é necessário prefixo +55

**Formato validado:**
```
11975649922
```

**Payload validado:**
```json
{
  "data": {
    "type": "signers",
    "attributes": {
      "has_documentation": false,
      "refusable": false,
      "group": 1,
      "location_required_enabled": false,
      "communicate_events": {
        "signature_request": "sms",
        "signature_reminder": "none",
        "document_signed": "whatsapp"
      },
      "name": "Vinicius Gomes",
      "phone_number": "11975649922"
    }
  }
}
```

✔ SMS entregue com sucesso

## 4. Escopo atual

### ✅ Incluído
- Automação local
- Processamento em lote
- Controle por status_vale
- Criação de envelope
- Signatário por telefone
- Envio SMS
- Documento via template
- Requisitos de assinatura
- Ativação e notificação
- Atualização da planilha
- Uso de .env
- Preparação para SharePoint e Azure

### 🚫 Fora do escopo
- Execução em Azure Functions
- Upload para SharePoint
- Webhooks
- Fila de processamento
- Validação comercial SMS/WhatsApp

## 5. Regras de negócio

### 5.1 Controle por status_vale
**Valores possíveis:**
- Não enviado
- Enviado
- Vale assinado
- Vale negado

**Regra atual:**
- "Não enviado" → processa
- Outros → ignora

**Após sucesso:**
- Enviado

**Futuro (webhook):**
- Vale assinado
- Vale negado

### 5.2 Linhas incompletas
- Pular linha incompleta
- Não quebrar execução
- Manter como "Não enviado"

### 5.3 Planilha oficial
- Mesmo formato da atual
- Coluna telefone já preenchida
- Código não faz enriquecimento

## 6. Campos da planilha

### Campos disponíveis
AIT, centro_de_custo, motorista, matricula, telefone, placa, data_infracao, cod_infracao, gravidade, valor, data_limite, indicacao, valeassinado, cpf, status_vale, PARCELAS, DESCONTORAPARTIR

### Campos usados
AIT, motorista, telefone, placa, data_infracao, valor, cpf, PARCELAS, DESCONTORAPARTIR, status_vale

## 7. Validação de multa
```python
pode_processar, motivo = validar_multa_processavel(multa)
if not pode_processar:
    print(f"Pulando AIT {multa.get('AIT')} - motivo: {motivo}")
    continue
```

### Campos mínimos
AIT, motorista, telefone, cpf, valor, status_vale

## 8. Arquitetura
```
MultasClickSign/
├── clicksign_api/
│   ├── services/
│   │   ├── documento.py
│   │   ├── envelope.py
│   │   ├── notificacao.py
│   │   ├── planilha.py
│   │   ├── requisitos.py
│   │   ├── sharepoint.py
│   │   └── signatario.py
│   ├── utils/
│   │   └── base64_utils.py
│   ├── config.py
│   └── main.py
```

## 9. Módulos

### config.py
Responsável por:
- .env
- Clicksign config
- SharePoint e Azure config

**Exemplo:**
```
CLICKSIGN_BASE_URL=https://sandbox.clicksign.com/api/v3
CLICKSIGN_TOKEN=...
CLICKSIGN_TEMPLATE_KEY=...
```

### planilha.py
- Ler Excel
- Filtrar status
- Validar multa
- Atualizar status

### envelope.py
```
return envelope_id, envelope_name
```

### signatario.py
```python
def adicionar_signatario(envelope_id, nome, telefone):
    ...
```

### documento.py
```json
{
  "AIT": "12345",
  "DATA_MULTA": "01/01/2036",
  "PLACA": "ABC1234",
  "NOME": "Nome Motorista",
  "CPF": "000.000.000-00",
  "VALOR": "200,00",
  "DATA_DOCUMENTO": "09/06/2026",
  "PARCELAS": "12"
}
```

### requisitos.py
- agree
- provide_evidence
- auth = sms | whatsapp

### notificacao.py
- Notificar somente após ativação

### sharepoint.py
- Microsoft Graph
- Download de planilha
- Ainda não validado

## 10. Fluxo principal
```python
for multa in multas:
    if not validar:
        continue

    envelope_id = criar_envelope()
    if not envelope_id:
        continue

    signer_id = adicionar_signatario()
    if not signer_id:
        continue

    document_id = criar_documento()
    criar_requisitos()

    time.sleep(5)

    if ativar_envelope():
        if notificar():
            atualizar_status_vale()
```

## 11. SharePoint + Azure
1. Autenticar Graph
2. Baixar planilha
3. Processar local
4. Atualizar status
5. Subir planilha
6. Azure Functions

## 12. SMS e WhatsApp
✔ SMS funcionando  
✔ Sem +55

Atenções:
- Custo por envio
- Limite de envio
- Configuração do canal

## 13. Template
```
{{~position_sign_signer1}}
```

Mapeamento:
- tag → signer1
- key → signer1
- role → signer1

## 14. Erros conhecidos (a maioria já tratados)
- .env no commit
- retorno None em funções
- erro 404 (URL)
- filename inválido
- data não estruturada
- telefone com +55

## 15. Segurança
Nunca versionar:
- .env
- tokens
- client secrets

## 16. Custos SMS/WhatsApp
Verificar:
- cobrança por SMS
- limites
- diferença sandbox vs produção

Regra:
- Não disparar em lote sem validação

## 17. Próximas etapas
- Estabilizar SMS
- Validar custos
- Ajustar signatário
- Validar múltiplas linhas
- Integrar SharePoint
- Azure Functions
- Webhook
- Melhorar logs

## 18. Decisões técnicas
- Desenvolvimento incremental
- Testes isolados
- Commits pequenos
- Uso de .env
- Linhas incompletas são ignoradas
- SMS prioritário
- Telefone sem +55

## 19. Conclusão
O projeto está em fase **avançada e funcional localmente**.

✔ Cria envelopes  
✔ Usa template  
✔ Envia SMS  
✔ Atualiza status

### Próximos focos:
- Escalar para múltiplas linhas
- Validar custos
- Integrar SharePoint
- Migrar para Azure
- Implementar webhook
