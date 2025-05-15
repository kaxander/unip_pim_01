# main.py

from InquirerPy import inquirer
from auth import register, login
from tasks import menu_tarefas
from utils import clear
from rich.console import Console
import os

console = Console()

def menu_principal(username):
    while True:
        clear()
        console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')
        escolha = inquirer.select(
            message=f"Bem-vindo(a), {username}! O que deseja fazer?",
            qmark="",
            choices=[
                "📚 Acessar conteúdo",
                "📊 Ver meu progresso",
                "🚪 Deslogar"
            ],
        ).execute()

        if escolha == "📚 Acessar conteúdo":
            menu_tarefas(username)

        elif escolha == "📊 Ver meu progresso":
            mostrar_progresso(username)

        elif escolha == "🚪 Deslogar":
            print("Até logo!")
            break


def mostrar_progresso(username):
    from utils import carregar_json
    import os

    progresso_path = f"data/progress/{username}.json"
    tasks_path = "data/tasks.json"

    progresso = carregar_json(progresso_path)
    todas_tasks = carregar_json(tasks_path)

    clear()
    console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')

    if not progresso or not todas_tasks:
        print("\n📭 Nenhum progresso encontrado ou tarefas disponíveis.")
        input("\nPressione Enter para voltar...")
        return

    tarefas_incompletas = []

    for task in todas_tasks:
        titulo = task["titulo"]
        etapas = task["etapas"]

        progresso_tarefa = progresso.get(titulo, {})
        etapas_concluidas = [e for e in etapas if e["titulo"] in progresso_tarefa and progresso_tarefa[e["titulo"]]["concluida"]]
        etapas_pendentes = [e for e in etapas if e["titulo"] not in progresso_tarefa or not progresso_tarefa[e["titulo"]]["concluida"]]

        if etapas_pendentes:
            tarefas_incompletas.append({
                "titulo": titulo,
                "concluidas": etapas_concluidas,
                "pendentes": etapas_pendentes,
                "progresso_tarefa": progresso_tarefa
            })

    if not tarefas_incompletas:
        print("\n🎉 Parabéns! Você concluiu todas as tarefas disponíveis.")
        input("\nPressione Enter para voltar...")
        return

    for task in tarefas_incompletas:
        print(f"\n📘 Tarefa: {task['titulo']}")
        notas = []

        for etapa in task["concluidas"]:
            nota = task["progresso_tarefa"][etapa["titulo"]]["nota"]
            notas.append(nota)
            print(f"   ✅ Etapa: {etapa['titulo']} - Nota: {nota}/10")

        for etapa in task["pendentes"]:
            print(f"   ⏳ Etapa: {etapa['titulo']} - [pendente]")

        if len(task["concluidas"]) == len(task["concluidas"]) + len(task["pendentes"]):
            media = round(sum(notas) / len(notas), 2)
            print(f"   📊 Média da tarefa: {media}/10")
        else:
            print("   🔒 A média será exibida após a conclusão de todas as etapas.")

    input("\nPressione Enter para voltar...")




def main():
    # Criação de pastas se não existirem
    os.makedirs("data/progress", exist_ok=True)

    while True:
        clear()
        console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')
        escolha = inquirer.select(
            message="=== 🎓 Bem-vindo ao EduTerm ===",
            qmark="",
            choices=[
                "🔐 Login",
                "📝 Cadastro",
                "❌ Sair"
            ],
        ).execute()

        if escolha == "🔐 Login":
            username = login()
            if username:
                menu_principal(username)

        elif escolha == "📝 Cadastro":
            register()

        elif escolha == "❌ Sair":
            print("👋 Saindo do sistema...")
            break


if __name__ == "__main__":
    main()