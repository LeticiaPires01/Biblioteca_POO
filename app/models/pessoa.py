from app.data.pessoas_mock import pessoas

class Pessoa:
    # REGRA: constante de classe com valor diferente nas filhas
    LIMITE_EMPRESTIMOS = 0

    def __init__(self, id_pessoa: int, nome: str):
        # REGRA: todos os atributos protegidos; nenhum alterar_id
        self._id = id_pessoa
        self._permissoes = []
        
        # REGRA: O construtor chama os alterar_
        self.alterar_nome(nome)

    def alterar_nome(self, nome: str):
        # REGRA: Pelo menos 4 regras de negócio com raise ValueError (1/4 aqui)
        if not nome or not nome.strip():
            raise ValueError("O nome da pessoa não pode ser vazio.")
        self._nome = nome.strip()

    # REGRA: Um mostrar_ para cada leitura necessária
    def mostrar_id(self) -> int:
        return self._id

    def mostrar_nome(self) -> str:
        return self._nome

    def mostrar_permissoes(self) -> list:
        return self._permissoes

    def tem_permissao(self, permissao: str) -> bool:
        return permissao in self._permissoes

    # REGRA: __repr__ em todas as classes
    def __repr__(self) -> str:
        return f"Pessoa(id={self._id}, nome='{self._nome}')"


# REGRA: Uma hierarquia com no mínimo 3 classes e 2 níveis
class Leitor(Pessoa):
    # REGRA: constante com valor diferente nas filhas
    LIMITE_EMPRESTIMOS = 3

    def __repr__(self) -> str:
        return f"Leitor(id={self.mostrar_id()}, nome='{self.mostrar_nome()}')"


class Bibliotecario(Pessoa):
    LIMITE_EMPRESTIMOS = 10

    # REGRA: Pelo menos um método sobrescrito que usa super() para estender
    def __init__(self, id_pessoa: int, nome: str):
        super().__init__(id_pessoa, nome)
        # Bibliotecário ganha a permissão exigida no tema 1
        self._permissoes.append("cadastrar_livro")

    def __repr__(self) -> str:
        return f"Bibliotecario(id={self.mostrar_id()}, nome='{self.mostrar_nome()}')"


# REGRA: Um dicionário no estilo PERFIS, mapeando texto do mock para classe
# REGRA: Nenhum if comparando tipo ou nome de classe
PERFIS = {
    "leitor": Leitor,
    "bibliotecario": Bibliotecario
}

# REGRA: Uma função carregar_*() por entidade, no fim do arquivo
def carregar_pessoas() -> list:
    pessoas_carregadas = []
    
    for dado in pessoas:
        # Aqui está a mágica: em vez de fazer "if dado['perfil'] == 'leitor'",
        # nós buscamos a classe no dicionário e já a instanciamos direto.
        classe_instanciar = PERFIS.get(dado["perfil"])
        
        if not classe_instanciar:
            raise ValueError(f"Perfil desconhecido: {dado['perfil']}")
            
        # Instancia Leitor ou Bibliotecario passando id e nome
        nova_pessoa = classe_instanciar(dado["id"], dado["nome"])
        pessoas_carregadas.append(nova_pessoa)
        
    return pessoas_carregadas
