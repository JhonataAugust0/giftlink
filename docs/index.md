# GiftLink

## Objetivo do projeto

O GiftLink é uma API para gerenciar sorteios de Amigo Secreto, permitindo a criação de grupos, cadastro e sorteio de participantes, com segurança e fácil acesso. 

### Sumário
- [Configuração do projeto](./config.md)
- [Especificação do projeto](./specification.md)
- [Testes](./tests.md)

## Estrutura do Projeto
A arquitetura do projeto segue o padrão de arquitetura hexagonal (Ports and Adapters), o que permite um design desacoplado e fácil de manter.

1. /adapters
    - Implementações externas (FASTAPI e persistência de dados [ORM]) 

2. /domain 
    - Lógica central do projeto 

3. /ports 
    - Interfaces (Portas) que conectam o domínio às dependências externas 

4. Testes do projeto 
    - /tests 

5. main.py 
    - Ponto de entrada da aplicação