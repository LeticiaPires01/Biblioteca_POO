from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.controllers import emprestimos_controller

router = APIRouter(prefix="/api/emprestimos", tags=["Empréstimos"])

class NovoEmprestimoDTO(BaseModel):
    id_emprestimo: int
    id_livro: int
    id_pessoa: int

# REGRA: 201 na criação
@router.post("", status_code=201)
def registrar_emprestimo(dados: NovoEmprestimoDTO):
    """Rota: POST /api/emprestimos - registra, 201 ou 409"""
    
    # REGRA: try/except traduzindo o ValueError da model
    try:
        novo_emprestimo = emprestimos_controller.registrar_emprestimo(
            id_emprestimo=dados.id_emprestimo,
            id_livro=dados.id_livro,
            id_pessoa=dados.id_pessoa
        )
        
        # Se controller retornou None, é porque o livro ou pessoa não existem na memória
        if not novo_emprestimo:
            raise HTTPException(status_code=404, detail="Livro ou Pessoa informados não existem.")
            
        return novo_emprestimo
        
    except ValueError as erro:
        mensagem = str(erro)
        
        # Tradução exata do erro de domínio para HTTP
        if "já está emprestado" in mensagem:
            # REGRA: 409 quando conflita com o estado atual
            raise HTTPException(status_code=409, detail=mensagem)
        else:
            # REGRA: 422 quando a regra de negócio é violada (limite de 3 ou 10 empréstimos atingido)
            raise HTTPException(status_code=422, detail=mensagem)
