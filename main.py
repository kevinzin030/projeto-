from usuarios.json import init_db
from auth import register_user, login_user

init_db()

print("== Plataforma Educacional ==")
print("1. Cadastrar")
print("2. Entrar")

op = input("Escolha uma opção: ")

if op == '1':
    username = input("Usuário: ")
    password = input("Senha: ")
    register_user(username, password)

elif op == '2':
    username = input("Usuário: ")
    password = input("Senha: ")
    login_user(username, password)
