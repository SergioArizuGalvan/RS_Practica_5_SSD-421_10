import argparse
import json
from pathlib import Path

try:
    from models import Task
except ImportError:
    from src.models import Task

FITXER_TASQUES = Path("data") / "tasks.json"


def carregar_tasques():
    FITXER_TASQUES.parent.mkdir(parents=True, exist_ok=True)
    if not FITXER_TASQUES.exists():
        desar_tasques([])
    with FITXER_TASQUES.open(encoding="utf-8") as fitxer:
        return json.load(fitxer)


def desar_tasques(tasques):
    FITXER_TASQUES.parent.mkdir(parents=True, exist_ok=True)
    with FITXER_TASQUES.open("w", encoding="utf-8") as fitxer:
        json.dump(tasques, fitxer, ensure_ascii=False, indent=2)
        fitxer.write("\n")


def afegir_tasca(titol, assignatura):
    tasques = carregar_tasques()
    nou_id = max((tasca["id"] for tasca in tasques), default=0) + 1
    tasca = Task(nou_id, titol, assignatura)
    tasques.append(tasca.to_dict())
    desar_tasques(tasques)
    return tasca


def llistar_tasques():
    return [Task.from_dict(dades) for dades in carregar_tasques()]


def main():
    parser = argparse.ArgumentParser(
        description="Eina CLI per gestionar tasques acadèmiques."
    )
    subordres = parser.add_subparsers(dest="ordre", required=True)

    afegir = subordres.add_parser("add", help="Crea una nova tasca")
    afegir.add_argument("--title", required=True, help="Títol de la tasca")
    afegir.add_argument(
        "--subject", required=True, help="Assignatura de la tasca"
    )

    subordres.add_parser("list", help="Mostra totes les tasques registrades")

    args = parser.parse_args()

    if args.ordre == "add":
        tasca = afegir_tasca(args.title, args.subject)
        print(f"Tasca [ID: {tasca.id}] creada amb èxit")
    else:
        tasques = llistar_tasques()
        if not tasques:
            print("Registre de tasques buit.")
        else:
            for tasca in tasques:
                print(tasca)


if __name__ == "__main__":
    main()
