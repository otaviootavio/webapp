# Autores

Grupo 9 - Turma 02-2022

NUSP 11322900 - Lucas Alexandre Tavares \
NUSP 11808130 - Otávio Vacari Martins \
NUSP 11804081 - Thiago Moreira Yanitchkis Couto

# Sobre o projeto

Nosso projeto tem o objetivo de desenvolver um sistema de monitoramento de voos de aviões.

# Pré-requisitos

python>=3.6 \
git

# Instalação para windows

Para rodar a aplicação localmente siga as instruções abaixo:

Primeiro baixe o projeto na sua máquina local\
```git clone https://github.com/otaviootavio/webapp.git```

Em seguida entre na pasta do projeto e crie e acesse o ambiente virtual \
```cd webapp```\
```python -m venv env```\
```.\env\bin\Activate.ps1```

Instale as dependências do projeto, lembrando de fazer o migrate, e execute-o.\
```pip install -r requirements.txt```\
```cd mysite```\
```python manage.py makemigrations```\
```python manage.py migrate```\
```python manage.py runserver```

Agora, para ver o projeto rodando acesse a url ```localhost:8000/olamundo/```

# Popular o banco de dados
Para inserir dados no banco de dados é necessário rodar o comando abaixo:
```python manage.py seed```\
Assim, podemos seguir para a testagem. O login e senha de um certo grupo será o seu login e senha. Exemplo: Para simular um usuário que pertence ao grupo ```funcionarios``` é possível faze-lo acessando o sistema com as credenciais ```(funcionario, funcionario )```

# Testagem
Para testar é necessário estar no ambiente virtual e com o banco de dados diferente de vazio. Dado isso, acesse a pasta com o app:
```cd webapp```
Em seguida, execute os testes:
```python manage.py test```

# Autenticação

Utilizaremos a autenticação padrão do django. Assim, deveremos executar os seguintes passos para criar o usuário mestre ( super user )
```python manage.py createsuperuser```
Assim, criaremos nosso usuário que terá todas as permissões.

Para simular usuários com os grupos é possível configurá-los manualmente através da página Django Admin ou basta utilizar o método para popular o banco de dados.