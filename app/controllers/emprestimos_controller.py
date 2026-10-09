from app.models.emprestimos import Emprestimo, carregar_emprestimos
# Importamos as listas instanciadas e as funções de busca dos outros controllers
from app.controllers.livros_controller import banco_livros, buscar_livro_por_id
from app.controllers.pessoas_controller import banco_pessoas, buscar_pessoa_por_id

# Inicializa o "banco de dados" em memória cruzando os dados
banco_emprestimos = carregar_emprestimos(banco_livros, banco_pessoas)

# REGRA: _para_dicionario convertendo o objeto
def _para_dicionario(emprestimo: Emprestimo) -> dict:
    """Converte o Emprestimo trazendo informações do livro e da pessoa anexadas."""
    return {
        "id": emprestimo.mostrar_id(),
        "livro": {
            "id": emprestimo.mostrar_livro().mostrar_id(),
            "titulo": emprestimo.mostrar_livro().mostrar_titulo()
        },
        "pessoa": {
            "id": emprestimo.mostrar_pessoa().mostrar_id(),
            "nome": emprestimo.mostrar_pessoa().mostrar_nome()
        }
    }


# REGRA: Um método por caso de uso
def listar_emprestimos_por_pessoa(id_pessoa: int) -> list:
    """Caso de uso para a rota GET /api/pessoas/{id}/emprestimos"""
    # Verifica se a pessoa existe primeiro
    pessoa = buscar_pessoa_por_id(id_pessoa)
    
    # REGRA: Devolve None quando não encontra (a rota se encarregará do 404)
    if not pessoa:
        return None 
        
    # REGRA: Pelo menos um filtro com compreensão de lista
    return [_para_dicionario(e) for e in banco_emprestimos if e.mostrar_pessoa().mostrar_id() == id_pessoa]


def registrar_emprestimo(id_emprestimo: int, id_livro: int, id_pessoa: int) -> dict:
    """Caso de uso para a rota POST /api/emprestimos"""
    pessoa = buscar_pessoa_por_id(id_pessoa)
    livro = buscar_livro_por_id(id_livro)
    
    # Se um dos dois não existir, retornamos None (vai gerar 404 na rota)
    if not pessoa or not livro:
        return None
        
    # REGRA: Filtro com compreensão de lista para contar quantos empréstimos ativos a pessoa tem
    ativos_da_pessoa = [e for e in banco_emprestimos if e.mostrar_pessoa().mostrar_id() == id_pessoa]
    qtd_ativos = len(ativos_da_pessoa)
    
    # Cria o objeto. O parâmetro eh_novo=True faz a Model disparar os ValueErrors se:
    # 1. O Livro já estiver emprestado (livro.mostrar_disponivel() == False)
    # 2. A pessoa estourou seu limite (qtd_ativos >= pessoa.LIMITE_EMPRESTIMOS)
    novo_emprestimo = Emprestimo(id_emprestimo, livro, pessoa, qtd_ativos_pessoa=qtd_ativos, eh_novo=True)
    
    # Se o construtor acima rodou sem estourar nenhum ValueError, o empréstimo foi aprovado!
    # Então precisamos marcar o livro como indisponível:
    livro.alterar_disponivel(False)
    
    # Salvamos na lista e retornamos o dicionário
    banco_emprestimos.append(novo_emprestimo)
    
    return _para_dicionario(novo_emprestimo)
