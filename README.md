# Biblioteca_POO

# Prova em grupo — Construa o backend do seu sistema

Disciplina: Programação Orientada a Objetos
Integrante: Letícia Pires do Rosário.

Diagrama de classes
    %% Hierarquia de Herança
    
  class Pessoa {
        -_id: int
        -_nome: str
        -_permissoes: list
        +LIMITE_EMPRESTIMOS: int = 0
        +__init__(id: int, nome: str)
        +mostrar_id() int
        +mostrar_nome() str
        +mostrar_permissoes() list
        +tem_permissao(permissao: str) bool
        +__repr__() str
    }

  class Leitor {
        +LIMITE_EMPRESTIMOS: int = 3
        +__init__(id: int, nome: str)
        +__repr__() str
    }

  class Bibliotecario {
        +LIMITE_EMPRESTIMOS: int = 10
        +__init__(id: int, nome: str)
        +__repr__() str
    }

  Pessoa <|-- Leitor
  Pessoa <|-- Bibliotecario

  %% Entidade Principal 1
    class Livro {
        -_id: int
        -_titulo: str
        -_ano_publicacao: int
        -_disponivel: bool
        +__init__(id: int, titulo: str, ano_publicacao: int, disponivel: bool)
        +mostrar_id() int
        +mostrar_titulo() str
        +mostrar_ano_publicacao() int
        +mostrar_disponivel() bool
        +alterar_ano_publicacao(ano: int)
        +alterar_disponivel(status: bool)
        +__repr__() str
    }

  %% Entidade Principal 2 (Registro)
    class Emprestimo {
        -_id: int
        -_livro: Livro
        -_pessoa: Pessoa
        +__init__(id: int, livro: Livro, pessoa: Pessoa)
        +mostrar_id() int
        +mostrar_livro() Livro
        +mostrar_pessoa() Pessoa
        +__repr__() str
    }

  %% Associações e Multiplicidades
    Emprestimo "*" --> "1" Livro : contem
    Emprestimo "*" --> "1" Pessoa : pertence a

  %% Elementos de Módulo (Exigências soltas da camada Models)
    namespace Modulos_Models {
        class funcoes_e_dicionarios {
            +PERFIS: dict
            +carregar_pessoas() list
            +carregar_livros() list
            +carregar_emprestimos() list
        }
    }
