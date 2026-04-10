
 Planejamento – Integração Clicksign (API v1)

## Objetivo
Desenvolver e validar um script em Python para integração com a API da Clicksign (v1), com foco em testes iniciais e posterior implementação em produção para assinatura de múltiplas multas.

---

## Etapas do Desenvolvimento

### 1. Envelope ✅
Responsável por agrupar documentos e participantes do fluxo de assinatura.

- Criar envelope
- Configurar envelope
- Armazenar o `ID` para uso em endpoints futuros  
**Status:** ✅ Concluído

---

### 2. Documento ✅
Adicionar documentos ao envelope.

- Converter arquivo para Base64
- Anexar documento ao envelope  
**Status:** ✅ Concluído

---

### 3. Signatários ⬜
Gerenciar as pessoas que irão assinar o documento.

- Criar signatário  
**Status:** ⬜ Pendente

---

### 4. Requisitos de Assinatura ⬜
Definir critérios de validação da assinatura.

- Qualificação do documento
- Autenticação por e-mail
- Autenticação por telefone  
**Status:** ⬜ Pendente

---

### 5. Observadores (Opcional) ⬜
Adicionar entidades que não assinam, mas acompanham o processo.

- Configurar observadores
- Definir notificações  
**Status:** ⬜ Opcional

---

### 6. Notificações ⬜
Notificar signatários sobre documentos pendentes de assinatura.

- Enviar notificação ao signatário  
**Status:** ⬜ Pendente

---

### 7. Encerramento dos Testes ⬜
Concluir validações e iniciar planejamento da implementação real.

- Avaliar fluxo completo de assinatura
- Planejar assinatura de múltiplas multas
- Definir configuração ideal de cada etapa  
**Status:** ⬜ Planejado
``
