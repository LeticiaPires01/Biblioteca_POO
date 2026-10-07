# Biblioteca_POO

# Prova em grupo — Construa o backend do seu sistema

Disciplina: Programação Orientada a Objetos
Integrante: Letícia Pires do Rosário.

  1. O que é esta prova
Cada grupo recebe, por sorteio, o tema de um sistema. O trabalho é construir o backend
desse sistema do zero, seguindo a mesma arquitetura em quatro camadas do repositório
modelo.
O escopo é propositalmente menor que o KiOferta: três a quatro classes, uma hierarquia de
herança, e de cinco a sete rotas. Dá para fazer em uma semana sem virar noite.
O que está sendo avaliado não é o tamanho do sistema. É se você consegue:
- decidir quais classes existem no domínio que recebeu
- proteger o estado delas e colocar a regra no lugar certo
- usar herança onde ela se justifica, e polimorfismo para evitar if
- separar data, models, controllers e routes sem vazamento
- traduzir erro de negócio em resposta HTTP
Por que um tema diferente por grupo
Porque o domínio muda, mas a estrutura não. Quando você vir que a sua clínica veterinária e a
locadora do grupo vizinho têm exatamente o mesmo esqueleto, o padrão deixa de ser uma
receita decorada e vira uma ferramenta.

  2. Os 12 temas
Todos seguem a mesma forma: uma entidade principal, uma hierarquia, um registro que
liga as duas.
Tema 1 — Biblioteca comunitária
Controle de acervo e empréstimos de um ponto de leitura de bairro.
Camada - O que criar
Entidades - Livro, Emprestimo
Hierarquia - Pessoa → Leitor → Bibliotecario
Liga as duas Emprestimo guarda um Livro e uma
Pessoa
Regras obrigatórias
- Leitor pode ter no máximo 3 empréstimos; bibliotecário, 10 (constante de classe)
- Não é possível emprestar um livro já emprestado
- O ano de publicação não pode ser maior que o ano atual
- Só quem tem a permissão cadastrar_livro pode incluir um título novo
Rotas mínimas
GET /api/livros - lista o acervo
GET /api/livros/{id} - um livro, ou 404
GET /api/livros/disponiveis - só os que não estão emprestados
POST /api/emprestimos - registra, 201 ou 409
GET /api/pessoas/{id}/emprestimos - o livro e a pessoa que está com ele
POST /api/login - perfil e permissões

  3. O que todo grupo precisa entregar
Independentemente do tema sorteado.
Estrutura de pastas
nome-do-sistema/
├── main.py
├── requirements.txt
├── verificar.py
├── README.md
└── app/
├── __init__.py
├── data/ mocks, um arquivo por entidade
├── models/ classes e regras
├── controllers/ casos de uso
└── routes/ endereços e códigos HTTP
Não invente outra organização. Copie a do repositório modelo.

  Camada data
Um arquivo *_mock.py por entidade, com lista de dicionários
Pelo menos 5 registros por entidade principal
Nenhuma classe, nenhum import, nenhuma regra nesses arquivos

  Camada models
De 3 a 5 classes, contando a hierarquia
Todos os atributos protegidos, com um sublinhado
Um mostrar_ para cada leitura necessária
alterar_ só onde o valor pode mudar; nenhum alterar_id
O construtor chama os alterar_
No mínimo 4 regras de negócio com raise ValueError
__repr__ em todas as classes
Uma função carregar_*() por entidade, no fim do arquivo
Nenhum import do FastAPI

  Herança e polimorfismo
Uma hierarquia com no mínimo 3 classes e 2 níveis
Pelo menos um método sobrescrito que usa super() para estender
Pelo menos uma constante de classe com valor diferente nas filhas
Um dicionário no estilo PERFIS, mapeando texto do mock para classe
Nenhum if comparando tipo ou nome de classe em todo o projeto
Camada controllers
Um controller por entidade principal
Um método por caso de uso
_para_dicionario convertendo o objeto
Pelo menos um filtro com compreensão de lista
Devolve None ou lista vazia quando não encontra; nunca código HTTP

  Camada routes
De 5 a 7 rotas, conforme o tema
404 quando não encontra
409 quando conflita com o estado atual
422 quando a regra de negócio é violada
201 na criação
try/except traduzindo o ValueError da model
Verificação
Um verificar.py com no mínimo 12 checagens, no formato do modelo
Ele precisa passar inteiro antes da entrega

  README
Como rodar
O diagrama de classes, mesmo que em texto ou foto de desenho à mão
A tabela de rotas
Quem fez o quê

  5. Diagrama de classes
Entregue um diagrama UML com:
- as 3 a 5 classes, com atributos e métodos
- os sinais - para protegido e + para público
- o triângulo vazio da herança
- a linha da associação, com as multiplicidades
Pode ser feito no Draw.io, no Mermaid dentro do README, ou à mão e fotografado. O que vale
é estar correto, não bonito.

Como entregar
1. Um repositório público por grupo, no GitHub
2. Commits de todos os integrantes ao longo da semana, e não um commit único no fim
3. O link na planilha da turma
4. Na raiz: o README.md e a saída do verificar.py colada nele
