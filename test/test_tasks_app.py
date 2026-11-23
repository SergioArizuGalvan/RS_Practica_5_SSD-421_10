import json
import subprocess
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
APP = ARREL / "src" / "tasks_app.py"


def executar(tmp_path, *arguments):
    resultat = subprocess.run(
        [sys.executable, str(APP), *arguments],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    )
    return resultat.stdout.strip()


def llegir_tasques(tmp_path):
    fitxer = tmp_path / "data" / "tasks.json"
    return json.loads(fitxer.read_text(encoding="utf-8"))


def test_crear_tasca(tmp_path):
    sortida = executar(
        tmp_path, "add", "--title", "Pràctica 1", "--subject", "RS"
    )
    assert sortida == "Tasca [ID: 1] creada amb èxit"
    assert llegir_tasques(tmp_path) == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_llistat_buit(tmp_path):
    assert executar(tmp_path, "list") == "Registre de tasques buit."
    assert llegir_tasques(tmp_path) == []


def test_llistat_amb_tasques(tmp_path):
    fitxer = tmp_path / "data" / "tasks.json"
    fitxer.parent.mkdir(parents=True, exist_ok=True)
    fitxer.write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "titol": "Examen parcial",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    assert executar(tmp_path, "list") == (
        "[1] Pràctica 1 (RS) - estat: pendent\n"
        "[2] Examen parcial (SO) - estat: pendent"
    )
