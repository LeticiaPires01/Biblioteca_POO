from app.data.emprestimos_mock import emprestimos
from app.models.livros import Livro
from app.models.pessoa import Pessoa

class Emprestimo:
    def __init__(self, id_emprestimo: int, livro: Livro, pessoa: Pessoa, qtd_ativos_pessoa: int = 0, eh_novo: bool = False):
        self._id = id_emprestimo
        self._livro = livro
        self._pessoa = pessoa

        # Apenas aplicamos as validações de regra de negócio se for uma criação de um NOVO empréstimo pela API
        if eh_novo:
            # REGRA OBRIGATÓRIA: Não é possível emprestar um livro já emprestado (4/4 das regras com ValueError)
            if not livro.mostrar_disponivel():
                raise ValueError(f"O livro '{livro.mostrar_titulo()}' já está emprestado.")
            
            # REGRA OBRIGATÓRIA: Limite de empréstimos
            # Usa o polimorfismo da constante de classe (LIMITE_EMPRESTIMOS) sem precisar de "if tipo == Leitor"
            if qtd_ativos_pessoa >= pessoa.LIMITE_EMPRESTIMOS:
                raise ValueError(
                    f"A pessoa '{pessoa.mostrar_nome()}' atingiu o limite máximo de {pessoa.LIMITE_EMPRESTIMOS} empréstimos."
                )

    # REGRA: Um mostrar_ para cada leitura necessária
    def mostrar_id(self) -> int:
        return self._id

    def mostrar_livro(self) -> Livro:
        return self._livro

    def mostrar_pessoa(self) -> Pessoa:
        return self._pessoa

    # REGRA: __repr__ em todas as classes
    def __repr__(self) -> str:
        return f"Emprestimo(id={self._id}, livro={self._livro.mostrar_titulo()}, pessoa={self._pessoa.mostrar_nome()})"


# REGRA: Uma função carregar_*() por entidade, no fim do arquivo
def carregar_emprestimos(livros_existentes: list, pessoas_existentes: list) -> list:
    emprestimos_carregados = []
    
    for dado in emprestimos:
        # Busca a referência real do objeto Livro pelo ID
        livro_encontrado = None
        for l in livros_existentes:
            if l.mostrar_id() == dado["id_livro"]:
                livro_encontrado = l
                break
                
        # Busca a referência real do objeto Pessoa pelo ID
        pessoa_encontrada = None
        for p in pessoas_existentes:
            if p.mostrar_id() == dado["id_pessoa"]:
                pessoa_encontrada = p
                break
                
        # Instancia o Emprestimo vinculando os dois objetos
        if livro_encontrado and pessoa_encontrada:
            novo_emprestimo = Emprestimo(
                id_emprestimo=dado["id"],
                livro=livro_encontrado,
                pessoa=pessoa_encontrada,
                eh_novo=False  # Como é carregamento de mock inicial, não dispara a trava de livro já emprestado
            )
            emprestimos_carregados.append(novo_emprestimo)
            
    return emprestimos_carregados
