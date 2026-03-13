# sc-empreendimentos-api

## Descrição da solução
O projeto **sc-empreendimentos-api** é uma aplicação CRUD para gerenciamento de empreendimentos catarinenses. A solução foi dividida em duas partes: um backend responsável pela API REST e persistência de dados, e um frontend simples para operação manual dos registros. O backend foi construído com **Python**, **FastAPI**, **PyMongo**, **MongoDB Atlas** e **python-dotenv**. O frontend foi desenvolvido com **HTML**, **CSS** e **JavaScript puro**, consumindo a API local via `fetch()`.

A proposta desta entrega é atender ao escopo do desafio com código simples, organizado e preparado para evolução posterior, sem adicionar complexidade desnecessária. O sistema permite cadastrar, listar, buscar por identificador, editar e excluir empreendimentos.

## Contexto do desafio
Este projeto foi desenvolvido como parte do desafio prático da trilha **IA para DEVs**. O foco desta etapa foi estruturar uma base funcional para uma aplicação CRUD, respeitando o escopo definido no enunciado, com separação básica de responsabilidades, validação de dados e integração entre interface web e API.

## Funcionalidades implementadas
- Cadastro de empreendimento
- Listagem de empreendimentos
- Busca de empreendimento por ID
- Atualização total ou parcial de empreendimento
- Exclusão de empreendimento
- Validação de campos obrigatórios
- Validação de `segment` e `status` com base em regras de domínio
- Serialização do `_id` do MongoDB para `id` em string
- Endpoint de health check no backend
- Interface web simples para operação do CRUD
- Feedback visual de sucesso e erro no frontend

## Tecnologias utilizadas
### Backend
- Python
- FastAPI
- PyMongo
- MongoDB Atlas
- python-dotenv
- Uvicorn
- Pydantic

### Frontend
- HTML5
- CSS3
- JavaScript puro

## Estrutura do projeto
```text
sc-empreendimentos-api/
|-- backend/
|   |-- app/
|   |   |-- config.py
|   |   |-- constants.py
|   |   |-- database.py
|   |   |-- main.py
|   |   |-- routes/
|   |   |   `-- enterprise_routes.py
|   |   |-- schemas/
|   |   |   `-- enterprise.py
|   |   |-- services/
|   |   |   `-- enterprise_service.py
|   |   `-- utils/
|   |       `-- serializer.py
|   |-- .env.example
|   `-- requirements.txt
|-- frontend/
|   |-- app.js
|   |-- index.html
|   `-- style.css
|-- .gitignore
`-- README.md
```

# Como obter o projeto

Clone este repositório:

```bash
git clone https://github.com/eliandrolima/sc-empreendimentos-api.git
cd sc-empreendimentos-api
````

## Instruções de execução do backend
### 1. Acessar a pasta do backend
```bash
cd backend
```

### 2. Criar e ativar um ambiente virtual
No Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux ou macOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Crie um arquivo `.env` dentro de `backend/` com base no arquivo `.env.example`:

```env
MONGODB_URI=
DB_NAME=
COLLECTION_NAME=
```

### 5. Executar a API
```bash
uvicorn app.main:app --reload
```

A API ficará disponível em:
- `http://127.0.0.1:8000`

Documentação automática da API:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Instruções de execução do frontend
O frontend é estático e não depende de build.

### Opção simples
Abra o arquivo `frontend/index.html` no navegador.

### Opção recomendada
Servir a pasta `frontend` com um servidor local simples para evitar problemas de ambiente e facilitar os testes. Exemplo com Python:

```bash
cd frontend
python -m http.server 5500
```

Depois, acesse no navegador:
- `http://127.0.0.1:5500`

Importante: o backend deve estar em execução em `http://127.0.0.1:8000` para que o frontend consiga consumir a API.

## Endpoints principais da API
### Health check
- `GET /health`

Resposta esperada:
```json
{
  "status": "ok",
  "message": "API running"
}
```

### Empreendimentos
- `POST /enterprises`
- `GET /enterprises`
- `GET /enterprises/{enterprise_id}`
- `PUT /enterprises/{enterprise_id}`
- `DELETE /enterprises/{enterprise_id}`

### Exemplo de payload
```json
{
  "business_name": "Empresa Exemplo",
  "owner_name": "Fulano de Tal",
  "city": "Florianopolis",
  "segment": "Tecnologia",
  "contact": "contato@empresa.com",
  "status": "ativo",
  "description": "Descricao opcional"
}
```

## Decisões técnicas adotadas
- Uso do **FastAPI** para criação rápida da API com bom suporte a validação e documentação automática.
- Uso do **Pydantic** para validação de entrada, incluindo regras para campos obrigatórios e valores válidos de domínio.
- Uso do **PyMongo** de forma direta, sem camada extra de abstração, para manter a implementação aderente ao escopo do desafio.
- Separação básica entre `schemas`, `services`, `routes` e `utils`, suficiente para manter o projeto legível e preparado para crescimento.
- Conversão do `_id` do MongoDB para `id` string no serializer, evitando expor detalhes internos do banco para o frontend.
- Frontend em JavaScript puro para manter simplicidade, transparência da integração e baixo acoplamento.

## Melhorias futuras
- Adicionar testes automatizados para backend e frontend
- Implementar paginação na listagem de empreendimentos
- Criar filtros por cidade e segmento
- Melhorar tratamento de erros no frontend
- Adicionar máscaras e validações adicionais nos campos de contato
- Criar confirmação visual mais robusta para exclusões
- Substituir campo livre de cidade por **select com municípios de Santa Catarina**
- Validar municípios também no backend
- Adicionar autenticação e controle de acesso
- Criar pipeline de deploy e configuração de ambiente para produção

## Vídeo pitch
https://youtu.be/h-Cj-EIitB0
