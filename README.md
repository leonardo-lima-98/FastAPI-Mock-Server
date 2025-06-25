# FastAPI Mock Server

Este projeto é um servidor **FastAPI simples**, com o objetivo de **fornecer rotas mockadas** para testes e validação de funcionalidades do portal web. O foco **não é a lógica do servidor em si**, mas sim permitir que o portal interaja com uma API estável durante o desenvolvimento ou testes no **Azure App Service**.

## 🔧 Funcionalidades

- ✅ Rotas REST que retornam dados mockados diretamente do código
- ✅ Rota `/health` para checagem de conexão com banco de dados PostgreSQL
- ✅ Configuração via `.env` com `pydantic-settings`
- ✅ Suporte a execução com `uvicorn` ou `gunicorn` para produção
- ✅ Pronto para ser implantado no **Azure App Services**

## 📦 Requisitos

- Python 3.9+
- Pip
- Banco PostgreSQL para health check (opcional em testes locais)

## 📁 Estrutura do Projeto
```
FastAPI Mock Server/
|
├── app/
| |
│ ├── init.py
│ ├── config.py # Leitura de variáveis de ambiente com pydantic-settings
│ ├── main.py # Ponto de entrada do FastAPI
│ └── routes.py # Rotas da API
|
├── .env.example # Variáveis de ambiente (DATABASE caso seja usado)
├── requirements.txt # Dependências Python
└── run.sh # Script para rodar com Uvicorn com Reload para testes locais
```

## 🚀 Executando localmente

Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute o servidor com:
```bash
. run.sh
```

## 📌 Endpoints disponíveis
Método	Rota	Descrição
GET	/mock/data	Retorna dados mockados em JSON
GET	/health	Verifica conexão com o banco

| Método | Rota | Descrição |
| :-------: | :---- | :---------- |
| GET        | / | Messagem de Boas-Vindas |
| GET        | /info | Retorna informações gerais da aplicação |
| GET        | /mock | Redireciona para a rota de dados |
| GET        | /mock/data | Retorna os dados |
| GET        | /health | Retorna a saude da conexao com o DB |

## ☁️ Implantação no Azure App Service
Este servidor pode ser implantado diretamente no Azure App Service como backend temporário/mock para testes. Você pode configurar variáveis de ambiente no portal do Azure, caso deseje testar o health check.

## ⚠️ Atenção: este projeto não possui autenticação ou persistência. É destinado apenas para testes e validação funcional.
