## Automação 1 PDD:

## Visão Geral:
O processo de documentação consiste em uma base de controle para facilitar a identificação de pendencias e permitir automações. Para identificar e enviar avisos sobre pendências urgentes de documentações solicitadas por um advogado.

## Ferramentas usadas:
* Excel
* Power Automate
* PowerBI
* Outlook

##Segue as etapas da execução da automação 1:


## passo 1: 
Utilizar a tabela com a lista normalizada de documentos solicitados pelo advogado separando por kit admissional e kit demissional. Normalização consiste em utilizar tabelas auxiliares que tem as informações de quais documentos 
são do kit admissional e quais são do demissional e separar os documentos listados pelo advogado com base nelas (os documentos vem listados por extenso). Deve ser feito um cruzamento para definir que essa linha de solicitação pertence 
a qual colaborador através da matrícula .

## passo 2: 
Com a tabela normalizada, criar uma coluna de verificação de status desse documento em específico. A verificação atual será baseada no  princípio que, a maioria dos documentos não estão normalizados para serem reconhecidos na 
base de dados ou literalmente não estão em nenhuma base. Portanto, todos serão dados como pendentes a primeiro momento (a partir de uma normalização maior, será adicionada futuramente uma etapa de verificação real que pode dizer se o 
documento existe na base e o modelo atual rodará sem por questão de urgência).

## passo 3: 
A partir de uma tabela que identifique as informações de: colaborador, matricula, data de vencimento (provavelmente baseada na auditoria), tipo de documentação (coluna para admissional ou demissional), contendo uma linha por
documento. Fazer uma automação simples para envio de email notificando a garagem responsável da ausência desse documento, destacando a data de vencimento como um motivo de urgência.
