from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.controllers import pessoas_controller, emprestimos_controller

router = APIRouter(prefix="/api", tags=["Pessoas e Login"])

# DTO para receber apenas o ID na simulação de login
class LoginDTO(BaseModel):
    id_pessoa: int

@router.post("/login")
def login(dados: LoginDTO):
    """Rota: POST /api/login - perfil e permissões"""
    perfil = pessoas_controller.realizar_login(dados.id_pessoa)
    
    # REGRA: 404 quando não encontra
    if not perfil:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        
    return perfil

@router.get("/pessoas/{id_pessoa}/emprestimos")
def listar_emprestimos_pessoa(id_pessoa: int):
    """Rota: GET /api/pessoas/{id}/emprestimos - o livro e a pessoa que está com ele"""
    emprestimos = emprestimos_controller.listar_emprestimos_por_pessoa(id_pessoa)
    
    # REGRA: 404 quando não encontra
    if emprestimos is None:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        
    return emprestimos
