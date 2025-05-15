# tasks.py

from InquirerPy import inquirer
from utils import carregar_json, salvar_json, clear
from rich.console import Console
import os

console = Console()

def menu_tarefas(username):
    tasks = carregar_json("data/tasks.json")
    progresso = carregar_json(f"data/progress/{username}.json")
    if progresso is None:
        progresso = {}


    if not tasks:
        print("Nenhuma tarefa disponível no momento.")
        return

    # Lista de títulos de tarefas concluídas
    concluidas = []
    for tarefa in tasks:
        titulo = tarefa["titulo"]
        etapas = tarefa.get("etapas", [])
        progresso_tarefa = progresso.get(titulo, {})
        
        concluido = all(
            progresso_tarefa.get(etapa["titulo"], {}).get("concluida", False)
            for etapa in etapas
        )
        
        if concluido:
            concluidas.append(titulo)


    # Filtra tarefas não concluídas
    tarefas_disponiveis = [t for t in tasks if t["titulo"] not in concluidas]

    if not tarefas_disponiveis:
        clear()
        print("🎉 Parabéns! Você concluiu todas as tarefas disponíveis.")
        input("\nPressione Enter para voltar ao menu...")
        return

    clear()
    console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')

    escolha_tarefa = inquirer.select(
        message="Escolha um conteúdo para aprender:",
        qmark="",
        choices=[t["titulo"] for t in tarefas_disponiveis] + ["\n◀️ Voltar"],
    ).execute()

    if escolha_tarefa == "\n◀️ Voltar":
        return

    clear()

    tarefa = next(t for t in tarefas_disponiveis if t["titulo"] == escolha_tarefa)
    mostrar_etapas(tarefa, username)



def mostrar_etapas(tarefa, username):
    progresso_path = f"data/progress/{username}.json"
    progresso = carregar_json(progresso_path)

    while True:
        etapas = tarefa["etapas"]

        # Obtem progresso da tarefa atual
        progresso_tarefa = progresso.get(tarefa["titulo"], {})

        # Filtra etapas não concluídas
        etapas_pendentes = [
            (i, e) for i, e in enumerate(etapas)
            if e["titulo"] not in progresso_tarefa or not progresso_tarefa[e["titulo"]].get("concluida", False)
        ]

        if not etapas_pendentes:
            console.print(f"\n[bold green]🎉 Você já concluiu todas as etapas da tarefa: {tarefa['titulo']}![/bold green]\n")
            input("Pressione Enter para voltar...")
            return

        opcoes = [f'{i+1} - {e["titulo"]}' for i, e in etapas_pendentes] + ["\n◀️ Voltar"]

        clear()

        console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')

        escolha = inquirer.select(
            message=f"Tarefa: {tarefa['titulo']} - Escolha uma etapa:",
            qmark="",
            choices=opcoes
        ).execute()

        if escolha == "\n◀️ Voltar":
            return

        index = int(escolha.split("-")[0]) - 1
        etapa = etapas[index]
        executar_etapa(etapa, tarefa["titulo"], username, progresso)
        salvar_json(progresso_path, progresso)



def executar_etapa(etapa, tarefa_titulo, username, progresso):
    clear()

    console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')

    print(f"\n📘 Etapa: {etapa['titulo']}\n")
    
    partes = etapa["conteudos"]
    indice = 0

    while True:
        os.system("clear" if os.name != "nt" else "cls")  # limpa o terminal
        print(f"\n📘 Etapa: {etapa['titulo']}\n")
        print(f"📖 {partes[indice]['parte']}\n")

        opcoes = []
        if indice > 0:
            opcoes.append("🔙 Voltar")
        if indice < len(partes) - 1:
            opcoes.append("▶️ Prosseguir")
        else:
            opcoes.append("✅ Iniciar Quiz")

        escolha = inquirer.select(
            message="Escolha uma opção:",
            qmark="",
            choices=opcoes
        ).execute()

        if escolha == "🔙 Voltar":
            indice -= 1
        elif escolha == "▶️ Prosseguir":
            indice += 1
        elif escolha == "✅ Iniciar Quiz":
            break


    acertos = 0
    total = len(etapa["quiz"])
    clear()

    console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')
    
    for i, q in enumerate(etapa["quiz"], start=1):
        clear()
        console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')
        console.print(f"\n[bold yellow]Pergunta {i} de {total}[/bold yellow]\n")

        resposta = inquirer.select(
            message=f"{i} - {q['pergunta']}",
            choices=q["opcoes"]
        ).execute()

        if resposta == q["correta"]:
            print("✅ Correto!")
            acertos += 1
        else:
            print(f"❌ Errado! Resposta correta: {q['correta']}")

        input("\nPressione Enter para continuar...")

    clear()
    console.print('''[bold yellow]\
███████╗██████╗ ██╗   ██╗████████╗███████╗██████╗ ███╗   ███╗
██╔════╝██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
█████╗  ██║  ██║██║   ██║   ██║   █████╗  ██████╔╝██╔████╔██║
██╔══╝  ██║  ██║██║   ██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
███████╗██████╔╝╚██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚══════╝╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝\n[/bold yellow]''')
    nota = round(acertos / total * 10, 2)
    print(f"\n🎯 Nota da etapa: {nota}/10\n")

    input("\nPressione Enter para continuar...")

    # Salvar progresso
    if tarefa_titulo not in progresso:
        progresso[tarefa_titulo] = {}

    progresso[tarefa_titulo][etapa["titulo"]] = {
        "nota": nota,
        "concluida": True
    }
