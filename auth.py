import json
import os
import bcrypt
from InquirerPy import inquirer
from utils import clear
from rich.console import Console

USERS_FILE = "data/users.json"

console = Console()

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def register():
    users = load_users()
    clear()
    console.print("[bold yellow]\n=== Cadastro de novo usuário ===\n[/bold yellow]")
    name = inquirer.text(message="Digite seu nome completo:", qmark="").execute()
    username = inquirer.text(message="Escolha um nome de usuário:", qmark="",).execute()

    if any(u["username"] == username for u in users):
        input("Usuário já existe! Pressione Enter para voltar.")
        return None

    password = inquirer.secret(message="Crie uma senha:", qmark="",).execute()
    confirm = inquirer.secret(message="Confirme a senha:", qmark="",).execute()

    if password != confirm:
        input("Senhas não coincidem! Pressione Enter para voltar.")
        return None

    user = {
        "name": name,
        "username": username,
        "password": hash_password(password)
    }

    users.append(user)
    save_users(users)
    print("\nUsuário registrado com sucesso!")
    return user


def login():
    users = load_users()
    clear()
    console.print("[bold yellow]\n=== Login ===\n[/bold yellow]")
    username = inquirer.text(message="Usuário:", qmark="").execute()
    password = inquirer.secret(message="Senha:", qmark="").execute()

    for user in users:
        if user["username"] == username and check_password(password, user["password"]):
            print(f"\nLogin bem-sucedido. Bem-vindo(a), {user['name']}!")
            return user["username"]

    input("Credenciais inválidas. Pressione [Enter] para tentar novamente.")
    return None


def login_or_register():
    while True:
        opcao = inquirer.select(
            message="Escolha uma opção:",
            choices=["Login", "Cadastro", "Sair"],
            default="Login"
        ).execute()

        if opcao == "Login":
            user = login()
            if user:
                return user
        elif opcao == "Cadastro":
            user = register()
            if user:
                return user
        else:
            return None
