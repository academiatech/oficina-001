# [Academia Tech](http://academiatech.com.br) - Oficina 001

Uma introdução ao cloud computing: **Arquitetar uma API 100% escalável usando AWS**.

[Marcel Nicolay](http://github.com/marcelnicolay), [Gustavo Barbosa](http://github.com/barbosa), [Paulo Alem](http://github.com/pauloalem), [Rodrigo Machado](http://github.com/rcmachado)

## Descrição

O que pode ser mais legal do que arquitetar uma solução que tem como requisito não cair nunca, além de atender 10 usuários da mesma maneira que atende 100.000, sem nenhuma intervenção manual? 

É isso que iremos ver, como arquitetar uma API de alta disponibilidade, que escala automaticamente de acordo com o consumo, utilizando os serviços do [AWS](http://aws.amazon.com).

## Resumo

O foco da oficina será em como configurar e utilizar os serviços de `EC2`, `ELB`, `DynamoDB`, `Cloud Cache` e `Cloud Watch` da Amazon bem com automatizar os scripts de setup e deploy, a fim de criar uma poderosa solução que pode, e deve, ser replicada para diversos tipos de problema.

Nessa oficina iremos resolver o problema de criar uma API que armazena e exibe bookmarks de um determinado usuário. Como o foco é na arquitetura, o desenvolvimento da API não será necessário, ela já estará pronta.

A oficina terá 2 horas de duração:

#### Abertura (15 minutos):

- Apresentação do projeto da Academia Tech
- Agradecimentos
- Apresentação do tema da oficina
- Introdução ao AWS

#### Demonstração da solução (10 minutos)

- com o painel da Amazon aberto, rodar um teste de carga contra a API para mostrar o autoscalling acontencendo

#### Mão na massa (70 minutos)

- Introdução ao console do AWS
- Setup da máquina da aplicação com [fabric](http://fabfile.org)
- Configuração do DynamoDB
- Confuguração do Cloud Cache
- Configuração do auto scalling (ELB e Cloud Cache)
- Deploy da aplicação
- Teste funcional
- Teste de carga

#### Demonstração final (5 minutos)

- com o painel da amazon aberto, rodar um teste de carga contra a API para mostrar o autoscalling acontencendo

#### Considerações finais (20 minutos)

## Pré-requisitos

Não teremos instruções específicas para Windows. Utilizaremos Mac OSX ou Linux. Preparar o ambiente local com:

1. python 2.7, ou superior, com o pip instalado
2. instalar o [fake dynamo](https://github.com/academiatech/oficina-001/wiki/Fake-Dynamo)
3. executar no terminal:

```bash
mkdir -p ~/academiatech && cd ~/academiatech

git clone git@github.com:academiatech/oficina-001.git
cd oficina-001

pip install virtualenv-wrapper
mkvirtualenv academiatech
pip install -r requirements-dev.txt

make test
```
