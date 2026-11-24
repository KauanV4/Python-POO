class Pagamento:
    nome = "Pagamento"

    def __init__(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError (f"Valor inválido: {valor}")
        self.valor = valor


    def taxa(self):
        return 0

    def total(self):
        return round(self.valor + self.taxa(), 2)

    def resumo(self):
        return f"Nome: {self.nome} | Valor: R${self.valor} | Taxa: R${self.taxa()} | Total: R${self.total()}"


class Pix(Pagamento):
    nome = "Pix"


class Dinheiro(Pagamento):
    nome = "Dinheiro"



class Boleto(Pagamento):
    nome = "Boleto"

    def taxa(self):
        return 3.5


class Cartao(Pagamento):
    nome = "Cartão"


    def taxa(self):
        return self.valor * 0.03


class CartaoParcelado(Cartao):
    nome = "Cartão parcelado"

    def __init__(self, valor, parcelas):
        super().__init__(valor)
        if not isinstance(parcelas, int) or parcelas < 2:
            raise ValueError(f"Parcelas Inválidas: {parcelas}")
        self.parcelas = parcelas

    def taxa(self):
      return super().taxa() + (self.valor * 0.01 * (self.parcelas - 1))


def total_geral(pagamentos):
    total = 0
    for p in pagamentos:
        total += p.total()
    return round(total, 2)


# Testes
pagamentos = [
    Pix(100),
    Cartao(200),
    Boleto(150),
    CartaoParcelado(300, 3),
    Dinheiro(50),
]

for p in pagamentos:
    print(p.resumo())

print(total_geral(pagamentos))

try:
    Cartao(-5)
except ValueError as erro:
    print(erro)

try:
    CartaoParcelado(100, 1)
except ValueError as erro:
    print(erro)

print(isinstance(pagamentos[3], Cartao))
print(isinstance(pagamentos[0], Cartao))