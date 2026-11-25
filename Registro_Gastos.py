from dataclasses import dataclass, field, asdict




registros = [
    {"descricao": "  mercado ", "valor": 120.5, "categoria": " alimentação "},
    {"descricao": "Ônibus", "valor": 4.5},
    {"descricao": "Cinema", "valor": -30},
    {"descricao": "   ", "valor": 10},
    {"valor": 50},
    {"descricao": "Livro", "valor": "abc"},
]






@dataclass
class Gasto:
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

    @classmethod
    def from_dict(cls, dados):
        descricao = dados["descricao"]
        valor = dados["valor"]
        categoria = dados.get("categoria", "Outros")
        return cls(descricao, valor, categoria)

    def to_dict(self):
        return asdict(self)


    def __str__(self):
        return f"descricao: {self.descricao} | valor: R${self.valor} | categoria: {self.categoria}"




@dataclass
class Extrato:
    gastos: list = field(default_factory=list)




    @classmethod
    def from_lista(cls,registro):
        gastos = []
        erros = []
        for r in registro:
            try:
             gasto = Gasto.from_dict(r)
             gastos.append(gasto)
            except KeyError as erro:
                erros.append(f"campo ausente: {erro}")
            except ValueError as erro:
                erros.append(str(erro))
        return cls(gastos), erros


    def __len__(self):
        return len(self.gastos)


    def __str__(self):
        if not self.gastos:
            return "Extrato Vazio"
        return "\n".join(str(gasto) for gasto in self.gastos)




    @property
    def total(self):
        return round(sum(gasto.valor for gasto in self.gastos), 2)




    def por_categoria(self):
        totais = {}
        for gasto in self.gastos:
            if gasto.categoria in totais:
                totais[gasto.categoria] += gasto.valor
            else:
                totais[gasto.categoria] = gasto.valor
        for categoria, valor in totais.items():
            totais[categoria] = round(valor, 2)
        return totais



def criar_gastos(registros):
    gastos = []
    erros = []
    for r in registros:
        try:
            gastos.append(Gasto(r["descricao"], r["valor"], r.get("categoria", "Outros")))
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



extrato, erros = Extrato.from_lista(registros)

print(len(extrato))
print(extrato)
print(extrato.total)
print(extrato.por_categoria())
print(erros)
print(Gasto.from_dict({"descricao": "Livro", "valor": 40}).to_dict())

vazio, erros_vazio = Extrato.from_lista([])
print(vazio, len(vazio), erros_vazio)