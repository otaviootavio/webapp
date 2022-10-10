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
<code>git clone https://github.com/otaviootavio/webapp.git </code>

Em seguida entre na pasta do projeto e crie e acesse o ambiente virtual \
<code>cd webapp</code>\
<code>python -m venv env</code>\
<code>.\env\bin\Activate.ps1</code>

Instale as dependências do projeto e execute-o.\
<code>pip install -r requirements.txt</code>\
<code>cd mysite</code>\
<code>python manage.py runserver</code>

Agora, para ver o projeto rodando acesse a url <code>localhost:8000/olamundo/</code>

# Testagem
Para testar é necessário estar no ambiente virtual. Dado isso, acesse a pasta com o app:
```cd webapp```
Em seguida, execute os testes:
```python manage.py test```
