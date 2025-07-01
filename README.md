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
├── .env.example # Variáveis de ambiente (DB_USAGE=True caso seja usado)
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
| Método     | Rota       | Descrição |
| :--------: | :--------- | :---------- |
| GET        | /          | Messagem de Boas-Vindas |
| GET        | /info      | Retorna informações gerais da aplicação |
| GET        | /mock      | Redireciona para a rota de dados |
| GET        | /mock/data | Retorna os dados |
| GET        | /health    | Retorna a saude da conexao com o DB |

## ☁️ Implantação no Azure App Service
Este servidor pode ser implantado diretamente no Azure App Service como backend temporário/mock para testes. Você pode configurar variáveis de ambiente no portal do Azure, caso deseje testar o health check.

# ⚠️ Atenção: 
### Este projeto não possui autenticação ou persistência. É destinado apenas para testes e validação funcional.


# ===== EXEMPLOS DE USO =====

# GET /stats/basic-counts
# GET /stats/basic-counts?year=2024
# GET /stats/basic-counts?year=2024&month=12
# GET /stats/basic-counts?customer_id=123
# GET /stats/basic-counts?year=2024&month=12&customer_id=123

# GET /stats/purchase-values?year=2024
# GET /stats/products-per-purchase?month=12
# GET /stats/customer-stats?customer_id=123
# GET /stats/period-stats?year=2024&month=6

# GET /stats/complete-summary?year=2024&month=12
# GET /stats/available-years
# GET /stats/available-customers