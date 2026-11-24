from dataclasses import dataclass, field

@dataclass
class Carteira:
    dono: str
    movimentos: list = field(default_factory=list)



    def receber(self,valor,descricao="receita"):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError (f"Valor invalido: {valor}")
        movimento = {"tipo": "receita", "valor": valor, "descricao": descricao}
        self.movimentos.append(movimento)


    def gastar(self, valor, descricao="Gasto"):
            if not isinstance(valor, (int, float)) or valor <= 0:
                raise ValueError(f"valor inválido: {valor}")
            if valor > self.saldo:
                raise ValueError("saldo insuficiente")
            movimento = {"tipo": "gasto", "valor": valor, "descricao": descricao}
            self.movimentos.append(movimento)


    @property
    def saldo(self):
        soma_receitas = 0
        soma_gastos = 0
        for m in self.movimentos:
            if m["tipo"] == "receita":
                soma_receitas += m["valor"]
            elif m["tipo"] == "gasto":
                soma_gastos += m["valor"]
        return round(soma_receitas - soma_gastos, 2)


    @property
    def total_gasto(self):
        total = 0
        for m in self.movimentos:
            if m["tipo"] == "gasto":
             total += m["valor"]
        return round(total, 2)


    @property
    def maior_gasto(self):
        maior = None
        for m in self.movimentos:
            if m["tipo"] == "gasto" and(maior == None or m["valor"] > maior["valor"]):
                maior = m
        return maior

    def resumo(self):
     return f"Carteira: {self.dono}| Saldo: {self.saldo} | Gastos: {self.total_gasto} "






c = Carteira("Ana")
c.receber(1000, "Salário")
c.gastar(250.5, "Mercado")
c.gastar(100, "Transporte")

print(c.saldo)
print(c.total_gasto)
print(c.maior_gasto)

try:
    c.gastar(5000, "Notebook")
except ValueError as erro:
    print(erro)

try:
    c.receber(-10)
except ValueError as erro:
    print(erro)

print(len(c.movimentos))
print(c.resumo())

vazia = Carteira("Bruno")
print(vazia.saldo, vazia.maior_gasto)