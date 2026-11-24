from dataclasses import dataclass




registros = [
    {"descricao": "  mercado ", "valor": 120.5, "categoria": " alimentação "},
    {"descricao": "Ônibus", "valor": 4.5},
    {"descricao": "Cinema", "valor": -30},
    {"descricao": "   ", "valor": 10},
    {"valor": 50},
    {"descricao": "Livro", "valor": "abc"},
]






@dataclass
class gasto:
    descricao: str
    valor: float
    categoria: str = "Outros"

    def __post_init__(self):
        if not isinstance(self.descricao, str):
            raise ValueError (f"Descrição invalida")
        self.descricao = self.descricao.strip()
        if self.descricao == "":
            raise ValueError (f"Descrição vazia")
        if not isinstance(self.valor, (float, int)) or self.valor <= 0:
            raise ValueError (f"Valor invalido: {self.valor}")
        self.categoria = self.categoria.strip().title()
        if self.categoria == "":
            self.categoria = "Outros"



def criar_gastos(registros):
    gastos = []
    erros = []
    for r in registros:
        try:
            gastos.append(gasto(r["descricao"], r["valor"], r.get("categoria", "Outros")))
        except ValueError as erro:
            erros.append(str(erro))
        except KeyError as erro:
            erros.append(f"Campo ausente: {erro}")
    return gastos, erros






gastos, erros = criar_gastos(registros)

for g in gastos:
    print(g)

print(len(erros))
for e in erros:
    print(e)

print(sum(g.valor for g in gastos))
print(criar_gastos([]))