from app.models.pessoa import Pessoa, carregar_pessoas

# Inicializa o "banco de dados" em memória deste controller
banco_pessoas = carregar_pessoas()

# REGRA: _para_dicionario convertendo o objeto
def _para_dicionario(pessoa: Pessoa) -> dict:
    """Converte a instância de Pessoa (ou suas filhas) para um dicionário seguro para a API."""
    # Como não podemos usar 'if' para saber o tipo, pegamos o nome da classe dinamicamente
    perfil = pessoa.__class__.__name__.lower()
    
    return {
        "id": pessoa.mostrar_id(),
        "nome": pessoa.mostrar_nome(),
        "perfil": perfil,
        "permissoes": pessoa.mostrar_permissoes(),
        "limite_emprestimos": pessoa.LIMITE_EMPRESTIMOS
    }


# REGRA: Um método por caso de uso
def buscar_pessoa_por_id(id_pessoa: int) -> Pessoa:
    """
    Busca a instância de uma pessoa pelo ID.
    REGRA: Devolve None quando não encontra; nunca código HTTP.
    REGRA: Pelo menos um filtro com compreensão de lista.
    """
    # A exigência da compreensão de lista aplicada aqui:
    resultados = [p for p in banco_pessoas if p.mostrar_id() == id_pessoa]
    
    # Se a lista tiver algo, retorna o primeiro item. Se estiver vazia, retorna None.
    return resultados[0] if resultados else None


def realizar_login(id_pessoa: int) -> dict:
    """
    Caso de uso para a rota POST /api/login.
    Retorna os dados do perfil e as permissões.
    """
    pessoa = buscar_pessoa_por_id(id_pessoa)
    
    # REGRA: Devolve None ou lista vazia quando não encontra
    if not pessoa:
        return None
        
    return _para_dicionario(pessoa)
