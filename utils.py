import json
import os

def carregar_json(caminho):

    if not os.path.exists(caminho):
        if caminho.endswith("users.json") or caminho.endswith("tasks.json"):
            return []
        else:
            return {}


    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_json(caminho, dados):

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def clear():
    os.system("clear")