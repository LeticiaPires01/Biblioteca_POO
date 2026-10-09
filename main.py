from fastapi import FastAPI

# Importando os roteadores da camada de rotas
from app.routes import livros_routes, pessoas_routes, emprestimos_routes

# Inicializando a aplicação FastAPI
app = FastAPI(
    title="API Biblioteca Comunitária",
    description="Sistema de controle de acervo e empréstimos de um ponto de leitura de bairro.",
    version="1.0.0"
)

# Registrando os roteadores no app principal
app.include_router(livros_routes.router)
app.include_router(pessoas_routes.router)
app.include_router(emprestimos_routes.router)

# Rota raiz opcional apenas para testar se a API está no ar
@app.get("/")
def home():
    return {"mensagem": "API da Biblioteca Comunitária está rodando. Acesse /docs para ver o Swagger."}
