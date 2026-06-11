# Clicksign Batch Sender (Python)

Automação em **Python** para envio de documentos para assinatura digital utilizando a **Clicksign API v3**.

O projeto lê dados de uma **planilha (Excel)** e, para cada linha válida, cria um fluxo completo de assinatura:

> envelope → documento (template) → signatário → requisitos → ativação → notificação

---

## Objetivo

- Automatizar envio de documentos para assinatura
- Processar múltiplas linhas de uma planilha
- Reduzir trabalho manual e erros
- Permitir integração futura com outros sistemas

---

## Como funciona

Para cada linha da planilha:

1. Valida dados obrigatórios
2. Cria um envelope na Clicksign
3. Adiciona um signatário
4. Cria um documento a partir de um template
5. Define requisitos de assinatura
6. Ativa o envelope
7. Envia notificação ao signatário

---

## Arquitetura

```
clicksign_batch_sender/
├── clicksign_api/
│   ├── services/
│   │   ├── envelope.py
│   │   ├── documento.py
│   │   ├── signatario.py
│   │   ├── requisitos.py
│   │   ├── notificacao.py
│   │   └── planilha.py
│   ├── utils/
│   ├── config.py
│   └── main.py
```

---

## Planilha de entrada

O sistema utiliza uma planilha Excel como entrada.

### Campos esperados (exemplo)

- nome
- cpf
- telefone
- valor
- data
- status

### Regra de processamento

- Apenas linhas com `status = "Não enviado"` são processadas
- Linhas inválidas são ignoradas
- Após sucesso → status atualizado para `Enviado`

---

## Template (Clicksign)

Para funcionar corretamente, é necessário um template configurado na Clicksign.

### Regra crítica

Os seguintes valores devem estar alinhados:

- Tag no documento:
  ```
  {{~position_sign_signer1}}
  ```
- Signer key: `signer1`
- Requirement role: `signer1`

---

##  Stack utilizada

### Linguagem
- Python 3

### Bibliotecas principais
- `requests` → comunicação com API
- `pandas` → leitura e manipulação da planilha
- `openpyxl` → suporte a Excel
- `python-dotenv` → variáveis de ambiente

### Outras dependências
- `msal` → autenticação (caso integração futura com Microsoft)
- `cryptography` / `PyJWT` → segurança e tokens

---

## ⚙️ Configuração

Crie um arquivo `.env`:

```
CLICKSIGN_BASE_URL=https://sandbox.clicksign.com/api/v3
CLICKSIGN_TOKEN=seu_token
CLICKSIGN_TEMPLATE_KEY=seu_template
```

Instale as dependências:

```
pip install -r requirements.txt
```

---

## Execução

```
python main.py
```

---

## Regras importantes

- Notificação só pode ser enviada após ativação do envelope
- Existe rate limit na API da Clicksign
- Telefones devem estar no formato correto (ex: 11999999999)


---

## 📄 Licença

Uso livre para fins educacionais e projetos pessoais.
