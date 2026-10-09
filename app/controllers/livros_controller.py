from app.models.livros import Livro, carregar_livros
from app.models.pessoa import Pessoa

# Inicializa o "banco de dados" em memória deste controller
banco_livros = carregar_livros()

# REGRA: _para_dicionario convertendo o objeto
def _para_dicionario(livro: Livro) -> dict:
    return {
        "id": livro.mostrar_id(),
        "titulo": livro.mostrar_titulo(),
        "ano_publicacao": livro.mostrar_ano_publicacao(),
        "disponivel": livro.mostrar_disponivel()
    }


# REGRA: Um método por caso de uso
def listar_todos_os_livros() -> list:
    """Caso de uso para a rota GET /api/livros"""
    # REGRA: Pelo menos um filtro com compreensão de lista
    return [_para_dicionario(l) for l in banco_livros]


def listar_livros_disponiveis() -> list:
    """Caso de uso para a rota GET /api/livros/disponiveis"""
    # Compreensão de lista filtrando apenas os disponíveis
    # REGRA: Devolve lista vazia quando não encontra
    return [_para_dicionario(l) for l in banco_livros if l.mostrar_disponivel()]


def buscar_livro_por_id(id_livro: int) -> Livro:
    """Caso de uso para a rota GET /api/livros/{id}"""
    resultados = [l for l in banco_livros if l.mostrar_id() == id_livro]
    
    # REGRA: Devolve None quando não encontra; nunca código HTTP
    return resultados[0] if resultados else None


def cadastrar_novo_livro(id_livro: int, titulo: str, ano_publicacao: int, usuario: Pessoa) -> dict:
    """Caso de uso extra para justificar a regra de permissão do Bibliotecário"""
    
    # REGRA OBRIGATÓRIA: Só quem tem a permissão cadastrar_livro pode incluir um título novo
    if not usuario.tem_permissao("cadastrar_livro"):
        raise ValueError(f"Usuário '{usuario.mostrar_nome()}' não tem permissão para cadastrar livros.")
    
    # Verifica se o ID já existe para não sobrepor
    if buscar_livro_por_id(id_livro):
        raise ValueError(f"Já existe um livro com o ID {id_livro}.")
        
    # Instancia o novo livro (estará disponível por padrão).
    # Se o ano_publicacao for maior que o atual, a classe Livro vai disparar um ValueError aqui.
    novo_livro = Livro(id_livro, titulo, ano_publicacao, disponivel=True)
    banco_livros.append(novo_livro)
    
    return _para_dicionario(novo_livro)
