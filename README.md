# Academia Tech - Oficina 0001

Uma introdução ao cloud computing: como arquitetar uma API 100% escalável usando AWS.

[Marcel Nicolay](github.com/marcelnicolay), [Gustavo Barbosa](github.com/barbosa), [Paulo ALem](github.com/pauloalem), [Rodrigo Machado](github.com/rcmachado)

## Descrição

O que pode ser mais legal do que arquitetar uma solução que tem como requisito não cair nunca, além de atender 10 usuários da mesma maneira que atende 100.000, sem nenhuma intervenção manual? 

É isso que iremos ver, como arquitetar uma API de alta disponibilidade, que escala automaticamente de acordo com o consumo, utilizando os serviços do [AWS](aws.amazon.com).

## Resumo

O foco da oficina será em como configurar e utilizar os serviços de `EC2`, `ELB`, `DynamoDB`, `Cloud Cache` e `Cloud Watch` da Amazon bem com automatizar os scripts de setup e deploy, a fim de criar uma poderosa solução que pode, e deve, ser replicada para diversos tipos de problema.

Nessa oficina iremos resolver o problema de criar uma API que armazena e exibe bookmarks de um determinado usuário. Como o foco é na arquitetura, o desenvolvimento da API não será necessário, ela já estará pronta.

A oficina terá 2 horas de duração e terá a seguinte pauta:

#### Abertura (15 minutos):

- Apresentação do projeto da Academia Tech
- Agradecimentos
- Apresentação do tema da ofina
- Introdução ao AWS

#### Demonstração da solução (10 minutos)

- com o painel da amazon aberto, rodar um teste de carga contra a API para mostrar o autoscalling acontencendo

#### Mão na massa (70 minutos)

- Introdução ao console do AWS
- Setup da máquina da aplicação com [fabric](fabfile.org)
- Configuração do DynamoDB
- Confuguração do Cloud Cache
- Configuração do auto scalling (ELB e Cloud Cache)
- Deploy da aplicação
- Teste funcional
- Teste de carga

#### Demonstração final (5 minutos)

- com o painel da amazon aberto, rodar um teste de carga contra a API para mostrar o autoscalling acontencendo

### Considerações finais (20 minutos)