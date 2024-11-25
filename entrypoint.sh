#!/bin/bash

# Inicializa o banco de dados e aplica as migrações
echo "Inicializando o banco de dados e aplicando migrações..."

# Executa o script de inicialização do banco de dados
python ./app/adapters/data/orm/config/db_config.py

# Aguarda 5 segundos para garantir que a inicialização do banco foi concluída
echo "Aguardando a inicialização do banco de dados..."

# Aplica as migrações com o aerich
aerich upgrade

# Inicia a aplicação com o Uvicorn
echo "Iniciando o servidor..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
