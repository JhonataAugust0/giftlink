# Configuração do Projeto

Este repositório foi configurado utilizando o gerenciador de pacotes e dependências [Poetry](https://python-poetry.org), visando sua fácil configuração e gerenciamento de diferentes grupos de dependências, como desenvolvimento, documentação e testes.

## Estrutura do Projeto

1. Para criar o diretório e estrutura básica do projeto:
  ```
  bash
  poetry new GiftLink
  ```

2. Para instalar as dependências de desenvolvimento:
  ```
  bash
  poetry add --group dev pytest pytest-cov blue isort taskipy python-dotenv fastapi pydantic blue isort taskipy python-dotenv uvicorn pytest-asyncio httpx alembic asyncpg psycopg2-binary sqlalchemy = {extras = ["asyncio"], version = "^2.0.36"}
  ```

3. Para instalar as dependências de documentação:
  ```
  bash
  poetry add --group dev mkdocs-material mkdocstrings mkdocstrings-python
  ```
****

4. Para rodar os testes:
  ```
  bash
  task test
  ```

5. Para rodar os linters:
  ```
  bash
  task lint
  ```

## Como Executar

1. Clone o repositório
```
bash 
git clone https://github.com/JhonataAugust0/giftlink.git
```

2. Acesse o repositório
```
bash 
cd ./giftlink/
```

3. Configure suas credenciais do banco de dados local no arquivo .env e adicione-as em um arquivo alembic.ini no mesmo modelo do arquivo alembic.ini.example.

4. Execute o script principal:
```bash
poetry run python giftlink/app/main.py
```
ou   
5. Execute no docker:
```bash
docker-compose up -d --build
```