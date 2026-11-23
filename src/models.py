import json


class Task:
    ESTAT_PENDENT = "pendent"

    def __init__(self, id, titol, assignatura, estat=ESTAT_PENDENT):
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat

    def to_dict(self):
        return {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    @classmethod
    def from_dict(cls, dades):
        return cls(
            dades["id"],
            dades.get("titol", dades.get("title")),
            dades.get("assignatura", dades.get("subject")),
            dades.get("estat", dades.get("status", cls.ESTAT_PENDENT)),
        )

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, text):
        return cls.from_dict(json.loads(text))

    def __str__(self):
        return (
            f"[{self.id}] {self.titol} ({self.assignatura}) "
            f"- estat: {self.estat}"
        )
