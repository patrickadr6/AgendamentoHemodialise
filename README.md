# Agendador de Hemodiálise 3.000

Este repositório contém um script desenvolvido para o agendamento de transporte sanitário no sistema da Rangsaude Atibaia, com foco em pacientes que realizam hemodiálises. O sistema coordena viagens para os dias de segunda, quarta e sexta, além de terça, quinta e sábado, garantindo a logística de transporte necessária para os tratamentos regulares.

Nota: Ao executar o código, deve-se passar parâmetros --usuario e --senha para logar no sistema. O arquivo viagens.py, que contém os dados dos pacientes e detalhes das viagens para o devido agendamento, está faltando neste repositório por motivos de segurança. O programa ainda não está salvando os pacientes nas viagens.

## Sugestões para o futuro
* Adicionar logging em um arquivo ao invés de print
* Colocar ID para as viagens e chave nome para os pacientes
* Continuar agendamento a partir de alguma viagem e dia específico?

* Agendamento das vans fixas
  - Criar dados das viagens
  - Reutilizar função criarviagem, calendário de segunda a sexta
* Agendamento de fisioterapia?
