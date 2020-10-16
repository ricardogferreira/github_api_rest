# GITHUB API REST
Api para retornar dados de usuários e repositórios públicos do github

### Docker
Fazer o build da imagem: `docker build --tag github_api_rest:0.1 .`
Para subir a imagem utilize o comando:
`docker run --publish 5000:5000 --rm --name nome_da_aplicacao github_api_rest:0.1`
A aplicação vai rodar na porta 5000

## Docker-compose
### Com o docker-compose você consegue subir o ambiente completo, com persistência de dados.

Primeiramente é preciso fazer o build, utilize o comando `docker-compose build`
Para subir o ambiente execute o comando `docker-compose up`
A aplicação vai rodar na porta 5000

## Instalação local sem docker e docker-compose
Utilizando o pyenv ou virtualenv crie um ambiente virtual, utilize o python3.6

#### Comando virtualenv
Criar ambiente: `virutalenv -p python3.6 .venv`
Ativar ambiente: `source .venv/bin/activate`

#### Comando pyenv
Criar ambiente `pyenv virtualenv 3.6.12 github_api_rest_env`
Ativar ambiente: `pyenv activate github_api_rest_env`

Instale as dependências: `pip install -r requirements.txt`

para rodar o server utilize o comando `make serve`
Obs: Executando dessa forma o banco de dados a ser utilizado por padrão vai ser o sqlite.
A conexão com o banco de dados pode ser alterado via variáveis de ambiente ou dentro do arquivo config.py

## Comandos Uteis
Rodar validação do pep8: `make pep8`
Fazer correção de imports: `make fix-import`
Executar teste sem coverage: `make test`
Executar teste e coverage: `make coverage`
Executar coverage com detalhes: `make coverage-report`

## Variáveis de ambiente disponíveis para configuração
```
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_ADDRESS
POSTGRES_DB
SECRET_KEY
FLASK_APP
FLASK_ENV
```
Obs: Para utilizar o POSTGRES todas variáveis deve ser preenchidas.
