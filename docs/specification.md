# Especificação do projeto

GiftLink é uma API desenvolvida para gerenciar sorteios de Amigo Secreto de forma simples e eficiente. O sistema permite a criação de grupos de participantes, a associação de pessoas a esses grupos, o sorteio entre os membros, e garante que ninguém seja sorteado para si mesmo. Além disso, o projeto inclui funcionalidades de cadastro, edição, remoção e consulta tanto de grupos quanto de pessoas. A API requer autenticação segura utilizando JWT e possui um sistema de recuperação de senha para os usuários. O objetivo principal do GiftLink é facilitar e organizar sorteios de Amigo Secreto de maneira automatizada e sem erros.

## Personas

 - **Organizador de Evento**: Pessoa responsável por criar o grupo, adicionar os participantes, e gerenciar o sorteio. Necessita de uma interface simples e intuitiva para gerenciar as informações e realizar o sorteio.

- **Participante**: Usuário que faz parte do grupo e deseja consultar seu sorteio. Ele precisa de acesso rápido ao seu "amigo secreto" e sugestões de presentes.

 - **Administrador da API**: Responsável por gerenciar a integridade do sistema, mantendo as informações seguras e garantindo que os requisitos de autenticação e segurança sejam cumpridos. Este perfil não interage diretamente com o sorteio, mas precisa controlar o sistema de gerenciamento de usuários e grupos.

## Histórias de Usuários

Com base na análise das personas forma identificadas as seguintes histórias de usuários:

|EU COMO... `PERSONA`| QUERO/PRECISO ... `FUNCIONALIDADE` |PARA ... `MOTIVO/VALOR`                 |
|--------------------|------------------------------------|----------------------------------------|
|Organizador de Evento | Criar um grupo de amigo secreto | Organizar um evento com amigos ou colegas de trabalho |
|Organizador de Evento | Editar o grupo e adicionar ou remover pessoas | Manter a flexibilidade e poder alterar a composição do grupo conforme necessário |
|Participante | Alterar minha senha em caso de esquecimento | Ter acesso ao sistema novamente e saber quem eu devo presentear |'
|Administrador da API | garantir que a senha do usuário seja armazenada de forma segura | proteger os dados dos usuários e garantir a segurança da plataforma |


### Requisitos Funcionais

|ID    | Descrição do Requisito  | Prioridade | 
|------|-----------------------------------------|----| 
|RF-001| A API deve permitir o cadastro de grupos  | ALTA |
|RF-002| A API deve permitir a remoção de grupos por ID  | ALTA |
|RF-003| A API deve permitir a edição de grupos por ID  | ALTA |
|RF-004| A API deve permitir a listagem de grupos por ID e seus participantes | ALTA |
|RF-005| A API deve permitir a listagem de todos os grupos | ALTA |
|RF-006| A API deve permitir o cadastro de pessoas e associação à grupos   | ALTA |
|RF-007| A API deve permitir a remoção de pessoas por ID  | ALTA |
|RF-008| A API deve permitir a edição de pessoas por ID  | ALTA |
|RF-009| A API deve permitir a listagem de pessoas por ID com a pessoa que devem sortear | ALTA |
|RF-010| A API deve permitir a listagem de todas as pessoas de um grupo | ALTA |
|RF-011| A API deve sortear os participantes de um grupo entre si | ALTA |
|RF-012| A API deve exigir autenticação JWT SHA-256 usando o email e senha do usuário | ALTA |
|RF-013| A API deve exigir gerar um SALT aleatório para armazenar o hash da senha do usuário	| ALTA |
|RF-014| A API deve fornecer ao usuário a possibilidade de alterar sua senha em caso de esquecimento enviando um link de recuperação ao email do mesmo | ALTA | 


### Requisitos não Funcionais

|ID     | Descrição do Requisito  |Prioridade |
|-------|-------------------------|----|
|RNF-001| A API deve garantir alta disponibilidade (99,9% de uptime)	| ALTA |
|RNF-002| A API deve ser escalável, suportando aumentos de tráfego sem comprometimento de desempenho	| ALTA |
|RNF-003| A API deve ter baixo tempo de resposta, idealmente inferior a 1 segundo por requisição	| ALTA |
|RNF-004| A API deve ser documentada com exemplos de uso e descrições claras das funcionalidades	| ALTA |
|RNF-005| A API deve ser compatível com integração de outras aplicações que precisem consumir os dados	| MÉDIA |

## Restrições

O projeto está restrito pelos itens apresentados na tabela a seguir:

|ID| Restrição                                             |
|--|-------------------------------------------------------|
|R-001|	O sistema deve ser desenvolvido utilizando Python FASTAPI |
|R-002|	O sistema deve utilizar autenticação via JWT para todos os acessos, sem exceções |
|R-003|	O sistema deve ser hospedado em um ambiente que garanta conformidade com as leis de proteção de dados |
|R-004|	A API deve ser desenvolvida seguindo práticas de segurança como criptografia de dados sensíveis |
|R-005|	A API deve ser compatível com a versão 3.8 ou superior do Python |