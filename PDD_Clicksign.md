# PDD - Documento de Descrição do Projeto: Multas ClickSign

## 1. Visão Geral do Sistema

O **Multas ClickSign** é um projeto de automação desenvolvido em Python para integração com a API v3 da Clicksign, com foco na criação, configuração, ativação e notificação de envelopes digitais para assinatura de documentos relacionados ao processo de multas.

O sistema tem como objetivo automatizar etapas que hoje exigiriam operação manual na plataforma Clicksign, estruturando um fluxo programático capaz de:

- Criar envelopes na Clicksign;
- Criar documentos a partir de templates;
- Adicionar signatários;
- Vincular requisitos de assinatura e autenticação;
- Ativar envelopes;
- Notificar signatários;
- Servir futuramente como base para envio em lote de múltiplas multas.

A aplicação está em fase de testes e validação técnica, com estrutura modular já iniciada para facilitar manutenção, expansão e reutilização por outros fluxos internos.

---

## 2. Modelo de Negócio e Proposta de Valor

- **Público-alvo atual:** equipe interna responsável pelo processamento, envio e gestão de documentos de multa que precisam ser assinados digitalmente.

- **Proposta de valor:** substituir etapas manuais de criação e configuração de documentos na Clicksign por um fluxo automatizado, reduzindo retrabalho, erros operacionais e tempo de processamento.

- **Benefício operacional esperado:** permitir que cada documento de multa seja automaticamente transformado em um envelope Clicksign com signatário, documento, requisitos e notificação configurados.

- **Diretriz de evolução futura:** o projeto deverá evoluir para processar múltiplas multas em lote, criando um envelope individual por documento ou por conjunto lógico de documentos, conforme regra de negócio definida posteriormente.

---

## 3. Escopo Atual do Projeto

O escopo atual contempla a validação técnica do fluxo completo de assinatura via API Clicksign v3.

### 3.1. Etapas já desenvolvidas ou em validação

1. **Envelope**
   - Criar envelope;
   - Guardar `envelope_id`;
   - Consultar detalhes do envelope;
   - Tentar ativar envelope via endpoint dedicado.

2. **Documento**
   - Criar documento dentro do envelope;
   - Testes com upload via Base64;
   - Migração para uso de template Clicksign;
   - Validação de tags de assinatura no template.

3. **Signatário**
   - Criar signatário;
   - Guardar `signer_id`;
   - Configurar `key` do signatário para vínculo com template.

4. **Requisitos**
   - Criar requisito de assinatura (`agree`);
   - Criar requisito de autenticação (`provide_evidence`);
   - Vincular documento e signatário;
   - Garantir que `role` corresponde à tag de assinatura do template.

5. **Notificação**
   - Notificar signatário após ativação do envelope.

6. **Debug e validação**
   - Listar documentos;
   - Listar requisitos;
   - Consultar detalhes do envelope;
   - Verificar status e erros retornados pela API.

---

## 4. Stack Tecnológica Base

- **Linguagem:** Python 3
- **Biblioteca HTTP:** requests
- **Manipulação de arquivos:** pathlib
- **Manipulação de Base64:** base64
- **Serialização JSON:** json
- **Ambiente de desenvolvimento:** PyCharm
- **API externa:** Clicksign API v3
- **Ambiente Clicksign:** Sandbox
- **Formato de documento usado nos testes:** DOCX com template Clicksign

---

## 5. Estrutura Arquitetural Base

A estrutura atual do projeto segue uma divisão modular por responsabilidade, separando funções de domínio em arquivos específicos dentro da pasta `services`.

```text
MultasClickSign/
│
├── .venv/
│
├── clicksign_api/
│   │
│   ├── Documento/
│   │   ├── documento.docx
│   │   └── documento.pdf
│   │
│   ├── services/
│   │   ├── documento.py
│   │   ├── envelope.py
│   │   ├── notificacao.py
│   │   ├── requisitos.py
│   │   └── signatario.py
│   │
│   ├── testes/
│   │   └── teste_main.py
│   │
│   ├── utils/
│   │   └── base64_utils.py
│   │
│   ├── config.py
│   └── main.py
│
├── planejamento.txt
├── README.md
└── requirements.txt
```

---

## 6. Responsabilidade dos Arquivos e Módulos

### 6.1. `main.py`

Arquivo responsável por orquestrar a execução principal do fluxo.

Deve conter a sequência de execução das etapas:

```text
criar envelope
→ adicionar signatário
→ criar documento
→ criar requisitos
→ ativar envelope
→ notificar signatário
```

O `main.py` não deve concentrar regras complexas de payload ou lógica de API. Ele deve apenas coordenar chamadas aos módulos da pasta `services`.

---

### 6.2. `config.py`

Arquivo responsável por centralizar configurações globais da integração.

Deve conter:

- URL base da API Clicksign;
- Headers padrão;
- Token de autenticação;
- Eventuais constantes globais;
- Chaves de template, quando aplicável.

Exemplo conceitual:

```python
BASE_URL = "https://sandbox.clicksign.com/api/v3"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/vnd.api+json",
    "Authorization": "TOKEN"
}
```

> Observação: tokens reais não devem ser versionados em repositórios públicos ou compartilhados em chats externos.

---

### 6.3. `services/envelope.py`

Responsável por operações relacionadas ao envelope.

Funções esperadas:

- `criar_envelope()`
- `detalhes_envelope(envelope_id)`
- `ativar_envelope(envelope_id)`
- Futuramente: `editar_envelope(envelope_id)`

O envelope é o agrupador principal do processo de assinatura. Todos os documentos, signatários e requisitos estão associados a ele.

---

### 6.4. `services/documento.py`

Responsável por operações relacionadas ao documento.

Funções esperadas:

- `criar_documento(envelope_id)`
- `listar_documentos(envelope_id)`

O projeto iniciou com testes de documento via Base64, mas a abordagem mais adequada passou a ser a criação de documentos via **template Clicksign**, pois o template permite que as tags de assinatura sejam reconhecidas corretamente.

---

### 6.5. `services/signatario.py`

Responsável por operações relacionadas aos signatários.

Funções esperadas:

- `adicionar_signatario(envelope_id, nome, email, key)`
- `listar_signatarios(envelope_id)`

O campo `key` é crítico no fluxo com templates, pois deve corresponder ao identificador usado na tag de assinatura do documento.

Exemplo:

```text
Tag no documento: {{~position_sign_signer1}}
key do signer: signer1
role do requisito: signer1
```

---

### 6.6. `services/requisitos.py`

Responsável pela criação dos requisitos de assinatura e autenticação.

Funções esperadas:

- `criar_requisito_assinatura(envelope_id, document_id, signer_id, role)`
- `criar_requisito_autenticacao(envelope_id, document_id, signer_id)`
- `listar_requisitos(envelope_id)`
- `ver_requirement(envelope_id, requirement_id)`

O projeto utiliza dois requisitos principais:

1. `agree`
   - Define que o signatário deve assinar/concordar com o documento.

2. `provide_evidence`
   - Define o método de autenticação do signatário, como e-mail.

---

### 6.7. `services/notificacao.py`

Responsável pela notificação do signatário.

Funções esperadas:

- `notificar_signatario(envelope_id, signer_id)`

Essa etapa só deve ser executada após a ativação bem-sucedida do envelope.

---

### 6.8. `utils/base64_utils.py`

Responsável por conversões auxiliares de arquivo para Base64.

Embora o fluxo atual esteja migrando para templates, esse utilitário permanece útil para cenários futuros em que seja necessário enviar documentos diretamente por Base64.

Atenção: na API Clicksign, para envio Base64, o campo `content_base64` pode exigir Data URI completo, como:

```text
data:application/pdf;base64,CONTEUDO_BASE64
```

---

## 7. Fluxo Funcional Atual

O fluxo de execução recomendado é:

```text
1. Criar envelope
2. Criar signatário com key compatível com template
3. Criar documento via template
4. Criar requirement de assinatura
5. Criar requirement de autenticação
6. Aguardar processamento interno da API
7. Ativar envelope
8. Notificar signatário
```

Exemplo conceitual:

```python
envelope_id = criar_envelope()

signer_id = adicionar_signatario(
    envelope_id=envelope_id,
    nome="Nome do Signatário",
    email="email@exemplo.com",
    key="signer1"
)

document_id = criar_documento(envelope_id)

criar_requisito_assinatura(
    envelope_id=envelope_id,
    document_id=document_id,
    signer_id=signer_id,
    role="signer1"
)

criar_requisito_autenticacao(
    envelope_id=envelope_id,
    document_id=document_id,
    signer_id=signer_id
)

time.sleep(2)

ativar_envelope(envelope_id)

notificar_signatario(envelope_id, signer_id)
```

---

## 8. Integração com Template Clicksign

### 8.1. Conceito

O projeto utiliza templates da Clicksign para resolver a definição de campos de assinatura no documento.

No arquivo `.docx`, a posição da assinatura é definida por tags especiais.

Exemplo:

```text
{{~position_sign_signer1}}
```

Essa tag indica à Clicksign onde deve ser posicionada a assinatura.

---

### 8.2. Estrutura da Tag

A tag segue a estrutura:

```text
{{~position_sign_ID}}
```

Onde:

- `~position_sign_` é o prefixo técnico obrigatório;
- `ID` é o identificador simbólico do papel/signatário.

Exemplos:

```text
{{~position_sign_1}}
{{~position_sign_signer1}}
{{~position_sign_cliente}}
{{~position_sign_empresa}}
```

---

### 8.3. Regra Crítica de Vínculo

Para que a assinatura funcione, três elementos precisam estar alinhados:

```text
Tag no DOCX      → {{~position_sign_signer1}}
key do signer    → signer1
role requirement → signer1
```

Se qualquer um desses valores não corresponder, a Clicksign pode criar o envelope, o documento e os requisitos, mas não conseguirá ativar corretamente o envelope.

---

### 8.4. Payload de Documento com Template

Exemplo conceitual:

```python
payload = {
    "data": {
        "type": "documents",
        "attributes": {
            "filename": "modelo_vale.docx",
            "template": {
                "key": "TEMPLATE_KEY",
                "data": {}
            }
        }
    }
}
```

O campo `template.data` deve ser usado para preencher variáveis dinâmicas do template, caso existam.

Exemplo:

```python
"data": {
    "nome_colaborador": "Vinicius Gomes",
    "valor_multa": "R$ 250,00",
    "placa": "ABC1D23"
}
```

O campo `template.data` não deve ser usado para substituir tags de assinatura. Tags de assinatura são resolvidas pela Clicksign através de `key` e `role`.

---

## 9. Requisitos de Assinatura

### 9.1. Requirement de Assinatura

Usado para definir que o signatário deve assinar o documento.

Exemplo:

```python
payload = {
    "data": {
        "type": "requirements",
        "attributes": {
            "action": "agree",
            "role": "signer1"
        },
        "relationships": {
            "document": {
                "data": {
                    "type": "documents",
                    "id": document_id
                }
            },
            "signer": {
                "data": {
                    "type": "signers",
                    "id": signer_id
                }
            }
        }
    }
}
```

---

### 9.2. Requirement de Autenticação

Usado para definir a forma de autenticação do signatário.

Exemplo com autenticação por e-mail:

```python
payload = {
    "data": {
        "type": "requirements",
        "attributes": {
            "action": "provide_evidence",
            "auth": "email"
        },
        "relationships": {
            "document": {
                "data": {
                    "type": "documents",
                    "id": document_id
                }
            },
            "signer": {
                "data": {
                    "type": "signers",
                    "id": signer_id
                }
            }
        }
    }
}
```

---

## 10. Signatários

### 10.1. Payload base do signatário

Exemplo conceitual:

```python
payload = {
    "data": {
        "type": "signers",
        "attributes": {
            "key": "signer1",
            "name": "Nome do Signatário",
            "email": "email@exemplo.com",
            "has_documentation": False,
            "refusable": False,
            "group": 1,
            "location_required_enabled": False,
            "communicate_events": {
                "signature_request": "none",
                "signature_reminder": "none",
                "document_signed": "email"
            }
        }
    }
}
```

### 10.2. Regra sobre `key`

O campo `key` deve ser tratado como identificador técnico do signatário dentro do fluxo.

Para templates com tag:

```text
{{~position_sign_signer1}}
```

o signatário deve ser criado com:

```python
"key": "signer1"
```

---

## 11. Ativação do Envelope

A ativação do envelope é uma das etapas mais sensíveis da integração.

O endpoint dedicado de ativação só funciona quando a Clicksign considera o envelope internamente válido.

Para isso, o envelope deve possuir:

- Documento válido;
- Documento com campo de assinatura reconhecido;
- Signatário válido;
- Requirement de assinatura;
- Requirement de autenticação;
- Vínculos corretos entre documento, signatário e role;
- Tag do template corretamente reconhecida.

### 11.1. Indício de documento configurado corretamente

Ao listar documentos do envelope, o retorno deve conter algo semelhante a:

```json
"metadata": {
  "position_sign_fields": ["position_sign_signer1"]
}
```

Se `position_sign_fields` vier vazio, o documento não possui campo de assinatura reconhecido.

---

## 12. Notificação

A notificação do signatário deve ocorrer apenas após a ativação do envelope.

Caso a notificação seja chamada antes da ativação, a API pode retornar erro de regra de negócio, como:

```text
422 - Não foi possível notificar o(s) signatário(s)
```

Payload mínimo recomendado:

```python
payload = {
    "data": {
        "type": "notifications",
        "attributes": {}
    }
}
```

Também é possível customizar o conteúdo do e-mail com `email_customization`, mas isso deve ser tratado como melhoria posterior.

---

## 13. Erros Conhecidos e Diagnósticos

### 13.1. Erro 400 - `content_base64`

Possível causa:

- Base64 inválido;
- Caminho do arquivo incorreto;
- Data URI ausente quando exigida;
- Documento vazio.

Exemplo de mensagem já encontrada:

```text
content_base64 Formatação do campo inválida. O valor deve ser um Data URI completo.
```

---

### 13.2. Erro 403 - Ativação do envelope

Possíveis causas:

- Envelope ainda incompleto;
- Documento sem tag de assinatura reconhecida;
- `position_sign_fields` vazio;
- Requirement sem vínculo correto;
- `role` diferente do identificador da tag;
- `key` do signer ausente ou incompatível;
- API ainda processando vínculos internos.

Ação recomendada:

```python
time.sleep(2)
```

antes da ativação, além de validar todos os vínculos.

---

### 13.3. Erro 422 - Notificação

Possíveis causas:

- Envelope ainda em `draft`;
- Envelope não ativado;
- Signatário sem ação válida de assinatura;
- Requirements incompletos.

---

### 13.4. Erro 404 HTML

Possíveis causas:

- URL incorreta;
- `envelope_id` inválido;
- Uso de variável `None` na URL;
- Endpoint montado incorretamente.

---

## 14. Diretrizes Críticas para Desenvolvimento

### 14.1. Evitar variáveis globais críticas

Funções devem receber IDs como parâmetros.

Evitar:

```python
def criar_documento():
    url = f".../{id_envelope}/documents"
```

Preferir:

```python
def criar_documento(envelope_id):
    url = f".../{envelope_id}/documents"
```

Isso reduz risco de usar IDs antigos, vazios ou de execuções anteriores.

---

### 14.2. Usar `json=payload` nas requisições

Sempre que possível, preferir:

```python
requests.post(url, json=payload, headers=headers)
```

em vez de:

```python
requests.post(url, data=json.dumps(payload), headers=headers)
```

Isso reduz erros de serialização e melhora a compatibilidade com estruturas JSON complexas, principalmente `relationships`.

---

### 14.3. Sempre imprimir erro completo em ambiente de teste

Durante desenvolvimento, nunca imprimir apenas:

```python
print("Erro")
```

Preferir:

```python
print(response.status_code)
print(response.text)
```

Isso é essencial para depurar respostas não documentadas da API.

---

### 14.4. Não versionar tokens

Tokens de autenticação devem ser tratados como segredo.

Recomenda-se futuramente usar:

- `.env`;
- variáveis de ambiente;
- arquivo de configuração local ignorado pelo Git.

---

### 14.5. Manter o fluxo modular

A lógica deve permanecer separada em módulos:

- envelope;
- documento;
- signatário;
- requisitos;
- notificação;
- utilitários.

O `main.py` deve permanecer como orquestrador.

---

## 15. Estado Atual do Projeto

O projeto já avançou por várias etapas de validação e aprendizado da API Clicksign.

### 15.1. Pontos já compreendidos

- O envelope precisa ser criado antes de qualquer outra entidade;
- O ID retornado no POST do envelope deve ser usado diretamente;
- Não se deve buscar `data[0]` em listagem de envelopes para obter o envelope atual;
- Documento via Base64 exige cuidados com Data URI;
- Templates são mais adequados para assinatura automatizada;
- Tags `{{~position_sign_*}}` precisam estar no DOCX;
- `position_sign_fields` precisa retornar preenchido;
- `key`, `role` e tag precisam estar alinhados;
- Existem dois requisitos essenciais: assinatura e autenticação;
- Notificação só deve ocorrer depois da ativação.

---

## 16. Próximos Passos Técnicos

### 16.1. Curto prazo

- Finalizar ativação do envelope com template;
- Validar notificação após ativação;
- Padronizar funções com parâmetros;
- Remover dependência de variáveis globais;
- Melhorar logs de execução.

### 16.2. Médio prazo

- Implementar processamento de múltiplos documentos;
- Criar um envelope por documento ou por lote, conforme regra de negócio;
- Ler dados de uma fonte estruturada;
- Preencher `template.data` dinamicamente;
- Registrar resultado de cada envio.

### 16.3. Longo prazo

- Criar integração com banco de dados;
- Implementar fila de processamento;
- Implementar retry automático;
- Criar dashboard de acompanhamento;
- Integrar com sistemas internos de multas;
- Padronizar ambiente de produção e sandbox.

---

## 17. Possível Fluxo Futuro para Múltiplas Multas

Em uma versão futura, o sistema deverá iterar sobre uma lista de multas/documentos.

Fluxo esperado:

```text
para cada multa:
    criar envelope
    adicionar signatário
    criar documento via template
    preencher dados variáveis do template
    criar requisito de assinatura
    criar requisito de autenticação
    ativar envelope
    notificar signatário
    registrar resultado
```

Cada execução deve registrar:

- ID da multa;
- ID do envelope;
- ID do documento;
- ID do signatário;
- IDs dos requirements;
- status final;
- erro, se houver;
- data/hora de envio.

---

## 18. Considerações sobre Templates

O template é um componente central da automação.

Para que funcione corretamente:

1. O arquivo `.docx` deve conter a tag de assinatura;
2. A tag deve seguir a sintaxe correta;
3. O template deve estar cadastrado na Clicksign;
4. O payload deve usar a `template.key`;
5. O retorno do documento deve mostrar `position_sign_fields` preenchido.

Exemplo de tag válida:

```text
{{~position_sign_signer1}}
```

Exemplo de retorno esperado:

```json
"metadata": {
  "position_sign_fields": ["position_sign_signer1"]
}
```

---

## 19. Considerações de Segurança

- O token da Clicksign não deve ser exposto no código final;
- Dados pessoais de signatários devem ser tratados com cuidado;
- Logs não devem expor informações sensíveis em produção;
- Em ambiente produtivo, deve haver controle de acesso ao sistema;
- Deve existir separação clara entre sandbox e produção.

---

## 20. Conclusão

O projeto **Multas ClickSign** está em fase avançada de validação técnica da integração com a API Clicksign v3.

A arquitetura modular já permite separar responsabilidades e facilitar manutenção. O maior ponto técnico identificado durante o desenvolvimento foi a correta configuração de documentos via template e o vínculo entre:

```text
tag de assinatura
key do signer
role do requirement
```

Com esse padrão consolidado, o projeto pode evoluir para um fluxo produtivo de assinatura digital de múltiplas multas, com maior segurança, rastreabilidade e redução de esforço operacional.
