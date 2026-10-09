from datetime import date
from app.data.livros_mock import livros

class Livro:
    def __init__(self, id_livro: int, titulo: str, ano_publicacao: int, disponivel: bool):
        # REGRA: Todos os atributos protegidos e nenhum alterar_id
        self._id = id_livro
        
        # REGRA: O construtor chama os alterar_
        self.alterar_titulo(titulo)
        self.alterar_ano_publicacao(ano_publicacao)
        self.alterar_disponivel(disponivel)

    def alterar_titulo(self, titulo: str):
        # Mais um raise ValueError para a cota exigida (2/4 do projeto)
        if not titulo or not str(titulo).strip():
            raise ValueError("O título do livro não pode ser vazio.")
        self._titulo = str(titulo).strip()

    def alterar_ano_publicacao(self, ano: int):
        # REGRA OBRIGATÓRIA: O ano de publicação não pode ser maior que o ano atual
        ano_atual = date.today().year
        if ano > ano_atual:
            raise ValueError(f"O ano de publicação ({ano}) não pode ser maior que o ano atual ({ano_atual}).")
        self._ano_publicacao = ano

    def alterar_disponivel(self, status: bool):
        if not isinstance(status, bool):
            raise ValueError("O status de disponibilidade deve ser do tipo booleano (True/False).")
        self._disponivel = status

    # REGRA: Um mostrar_ para cada leitura necessária
    def mostrar_id(self) -> int:
        return self._id

    def mostrar_titulo(self) -> str:
        return self._titulo

    def mostrar_ano_publicacao(self) -> int:
        return self._ano_publicacao

    def mostrar_disponivel(self) -> bool:
        return self._disponivel

    # REGRA: __repr__ em todas as classes
    def __repr__(self) -> str:
        return f"Livro(id={self._id}, titulo='{self._titulo}', ano={self._ano_publicacao}, disponivel={self._disponivel})"


# REGRA: Uma função carregar_*() por entidade, no fim do arquivo
def carregar_livros() -> list:
    livros_carregados = []
    
    for dado in livros:
        novo_livro = Livro(
            id_livro=dado["id"],
            titulo=dado["titulo"],
            ano_publicacao=dado["ano_publicacao"],
            disponivel=dado["disponivel"]
        )
        livros_carregados.append(novo_livro)
        
    return livros_carregados
