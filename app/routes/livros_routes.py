from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.controllers import livros_controller, pessoas_controller

# Criamos o roteador com o prefixo base
router = APIRouter(prefix="/api/livros", tags=["Livros"])

# DTO (Data Transfer Object) para receber o JSON do POST
class NovoLivroDTO(BaseModel):
    id: int
    titulo: str
    ano_publicacao: int
    id_usuario: int  # Usado para validar quem está tentando cadastrar (Leitor ou Bibliotecário)

@router.get("")
def listar_livros():
    """Rota: GET /api/livros"""
    return livros_controller.listar_todos_os_livros()

# IMPORTANTE: Rotas com texto fixo (/disponiveis) devem vir ANTES de rotas com variáveis (/{id_livro}).
# Se ficar embaixo, o FastAPI vai achar que "disponiveis" é um ID.
@router.get("/disponiveis")
def listar_disponiveis():
    """Rota: GET /api/livros/disponiveis"""
    return livros_controller.listar_livros_disponiveis()

@router.get("/{id_livro}")
def buscar_livro(id_livro: int):
    """Rota: GET /api/livros/{id}"""
    livro = livros_controller.buscar_livro_por_id(id_livro)
    
    # REGRA: 404 quando não encontra
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
        
    return livros_controller._para_dicionario(livro)

# REGRA: 201 na criação
@router.post("", status_code=201)
def cadastrar_livro(dados: NovoLivroDTO):
    """Rota para testar a regra: Só quem tem permissão cadastrar_livro pode incluir título."""
    
    # Busca quem está tentando fazer a ação
    usuario = pessoas_controller.buscar_pessoa_por_id(dados.id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário responsável pelo cadastro não encontrado.")
        
    # REGRA: try/except traduzindo o ValueError da model
    try:
        novo_livro = livros_controller.cadastrar_novo_livro(
            id_livro=dados.id,
            titulo=dados.titulo,
            ano_publicacao=dados.ano_publicacao,
            usuario=usuario
        )
        return novo_livro
        
    except ValueError as erro:
        mensagem = str(erro)
        
        # O try/except precisa decidir se o erro de negócio é um Conflito ou Entidade Improcessável
        if "Já existe" in mensagem:
            # REGRA: 409 quando conflita com o estado atual (ID repetido)
            raise HTTPException(status_code=409, detail=mensagem)
        else:
            # REGRA: 422 quando a regra de negócio é violada (Ex: Ano no futuro ou Sem permissão)
            raise HTTPException(status_code=422, detail=mensagem)
