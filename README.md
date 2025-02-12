## Setup env
python -m venv env or python3 -m venv env

## Activate env
### Linux
`source env/bin/activate`
### Windows
`env\Scripts\activate`


## install libraries
pip install -r requirements.txt

## migration
alembic upgrade head

## Fastapi standard installation
pip install fastapi[standard]

## Run server
fastapi dev app/main.py



## .env PASSWORD_SECRET and JWT_SECRET
### We can use the python module secrets to generate random password or secret

#### Via terminal
type:`python3`
terminal: `import secrets`
terminal: `print(secrets.token_urlsafe(32))`