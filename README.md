# Desafio_e-commerce_Desenvolvedor_Python
## Introdução
Projeto foi realizado utilizando Flask e AWS RDS (Amazon Web Service / Relational Database Sistem). Também foi utilizada linguagem SQL para interagir com o banco de dados.

## Metodologia
### Banco de Dados
O banco de dados `desafio_ecommerce_db` foi criado manualmente na prataforma AWS. Um banco de dados PostgreSQL.

### Criando tabelas no banco de dados
Para a criação das tabelas necessárias foi construído o script [setup_database.py](https://github.com/mickaelyoshua7674/Desafio_e-commerce_Desenvolvedor_Python/blob/main/setup_database.py) para a criação das tabelas de usuário, informação do usuário e produtos, como também para inserir os dados dos produtos na sua devida tabela.

### API
Na rota '/products' retorna todos os produtos registrados no banco de dados, '/register' é feito o cadastro do usuário no banco de dados e '/login' verificar seu cadastro.

## Resultado
Como não possuo pouco conhecimento em frontend foquei mais em backend e na parte de dados (que é onde possuo mais experiência). Gostaria de ter feito mais como liberar essa aplicação numa instância EC2 no AWS, porém acabei encontrando erros no processo e o tempo não me permitiu realizar mais do que está aqui.

## Como executar
As bibliotecas que devem estar instaladas para a aplicação funcionar são `sqlalchemy, psycopg2, flask, sys, traceback, requests, os e werkzeug`. Após isso bastar deixar os arquivos dispostos da mesma forma que este repositório e executar o script [main.py](https://github.com/mickaelyoshua7674/Desafio_e-commerce_Desenvolvedor_Python/blob/main/main.py).
