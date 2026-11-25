from dataclasses import dataclass, asdict

@dataclass
class Aluno:
    nome: str
    nota: float = 0

    @classmethod
    def from_dict(cls, dados):
        nome = dados["nome"].strip().title()
        nota = dados.get("nota", 0)
        return cls(nome, nota)

    def to_dict(self):
        return asdict(self)


a = Aluno.from_dict({"nome": " lia ", "nota": 8.5})
print(a)             # Aluno(nome='Lia', nota=8.5)
print(a.to_dict())   # {'nome': 'Lia', 'nota': 8.5}