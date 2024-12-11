#!/bin/bash

# Inicializa o banco de dados e aplica as migrações
echo "Inicializando o banco de dados e aplicando migrações..."

# Inicia a aplicação com o Uvicorn
echo "Iniciando o servidor..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
