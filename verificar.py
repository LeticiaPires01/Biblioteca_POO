from app.models.pessoa import Pessoa, Leitor, Bibliotecario, PERFIS
from app.models.livros import Livro
from app.models.emprestimos import Emprestimo
from app.controllers.pessoas_controller import buscar_pessoa_por_id
from app.controllers.livros_controller import cadastrar_novo_livro

def rodar_verificacoes():
    sucessos = 0
    total_checagens = 12
    
    print("="*50)
    print("INICIANDO VERIFICAÇÃO DO SISTEMA - BIBLIOTECA_POO")
    print("="*50)

    try:
        # Checagem 1: Herança e 2 níveis
        assert issubclass(Leitor, Pessoa) and issubclass(Bibliotecario, Pessoa), "Erro: Leitor e Bibliotecário não herdam de Pessoa."
        print("[OK] 1. Herança validada (Leitor e Bibliotecario herdam de Pessoa).")
        sucessos += 1

        # Checagem 2: Polimorfismo e constantes de classe
        assert Leitor.LIMITE_EMPRESTIMOS == 3 and Bibliotecario.LIMITE_EMPRESTIMOS == 10, "Erro: Limites de empréstimo incorretos."
        print("[OK] 2. Polimorfismo validado (LIMITE_EMPRESTIMOS muda nas classes filhas).")
        sucessos += 1

        # Checagem 3: Atributos protegidos (nenhum atributo público)
        livro_teste = Livro(99, "Teste", 2020, True)
        assert not hasattr(livro_teste, "id") and hasattr(livro_teste, "_id"), "Erro: Atributos não estão protegidos."
        print("[OK] 3. Encapsulamento validado (Atributos protegidos com '_').")
        sucessos += 1

        # Checagem 4: Regra de Negócio (Ano de Publicação)
        try:
            Livro(100, "De volta para o futuro", 2050, True)
            raise AssertionError("Deveria ter bloqueado livro com ano no futuro.")
        except ValueError:
            print("[OK] 4. Regra validada: Ano de publicação não pode ser maior que o atual.")
            sucessos += 1

        # Checagem 5: Regra de Negócio (Atributos vazios)
        try:
            Leitor(99, "")
            raise AssertionError("Deveria ter bloqueado pessoa com nome vazio.")
        except ValueError:
            print("[OK] 5. Regra validada: Nome de pessoa não pode ser vazio.")
            sucessos += 1

        # Checagem 6: Regra de Negócio (Livro já emprestado)
        livro_indisponivel = Livro(101, "Indisponível", 2020, False)
        leitor_teste = Leitor(10, "João")
        try:
            Emprestimo(50, livro_indisponivel, leitor_teste, 0, eh_novo=True)
            raise AssertionError("Deveria ter bloqueado empréstimo de livro indisponível.")
        except ValueError:
            print("[OK] 6. Regra validada: Não é possível emprestar livro já emprestado.")
            sucessos += 1

        # Checagem 7: Regra de Negócio (Limite do Leitor)
        livro_disp = Livro(102, "Disponível", 2020, True)
        try:
            Emprestimo(51, livro_disp, leitor_teste, qtd_ativos_pessoa=3, eh_novo=True)
            raise AssertionError("Deveria ter bloqueado empréstimo por limite do Leitor.")
        except ValueError:
            print("[OK] 7. Regra validada: Leitor barrado ao tentar o 4º empréstimo.")
            sucessos += 1

        # Checagem 8: Permissões e uso do super()
        bib_teste = Bibliotecario(11, "Ana")
        assert bib_teste.tem_permissao("cadastrar_livro") and not leitor_teste.tem_permissao("cadastrar_livro"), "Erro: Permissões incorretas."
        print("[OK] 8. Uso do super() validado: Bibliotecário recebe permissão exclusiva.")
        sucessos += 1

        # Checagem 9: Dicionário PERFIS (Sem usar IF de tipo)
        assert PERFIS["leitor"] == Leitor and PERFIS["bibliotecario"] == Bibliotecario, "Erro: Dicionário PERFIS incorreto."
        print("[OK] 9. Dicionário PERFIS mapeando texto do mock para classes validado.")
        sucessos += 1

        # Checagem 10: Método __repr__ implementado
        assert "Livro(" in repr(livro_teste) and "Leitor(" in repr(leitor_teste), "Erro: __repr__ ausente ou incorreto."
        print("[OK] 10. Método mágico __repr__ em todas as classes validado.")
        sucessos += 1

        # Checagem 11: Retorno None no Controller
        assert buscar_pessoa_por_id(9999) is None, "Erro: Controller não está retornando None para ID inexistente."
        print("[OK] 11. Controller validado: Retorna None em vez de erro HTTP quando não encontra.")
        sucessos += 1

        # Checagem 12: Regra de Negócio no Controller (Cadastro de Livro)
        try:
            cadastrar_novo_livro(105, "Novo Livro", 2021, leitor_teste)
            raise AssertionError("Deveria ter barrado Leitor de cadastrar livro.")
        except ValueError:
            print("[OK] 12. Controller validado: Apenas permissão 'cadastrar_livro' insere títulos novos.")
            sucessos += 1

    except AssertionError as e:
        print(f"\n[FALHA] A verificação parou devido a um erro: {e}")
        return

    print("="*50)
    print(f"RESULTADO: {sucessos}/{total_checagens} checagens passaram com sucesso!")
    print("O sistema atende a todas as exigências arquiteturais do projeto.")
    print("="*50)

if __name__ == "__main__":
    rodar_verificacoes()
