import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Pedido:
    codigo: str
    cliente: str
    itens: list = field(default_factory=list)

    def adicionar_item(self, produto, preco, quantidade=1):
        self.itens.append({"produto": produto, "preco": preco, "quantidade": quantidade})

    def total(self):
        return sum(item.get("preco", 0) * item.get("quantidade", 1) for item in self.itens)


@dataclass
class Loja:
    nome: str
    pedidos: list = field(default_factory=list)

    def adicionar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def faturamento(self):
        return round(sum(p.total() for p in self.pedidos), 2)

    def resumo(self):
        return f"Loja: {self.nome} | Pedidos: {len(self.pedidos)} | Faturamento: R$ {self.faturamento()}"

    def salvar(self, caminho):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(asdict(self), arquivo, ensure_ascii=False, indent=2)
    

def carregar_loja(caminho) -> Optional[Loja]:
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return None

    pedidos = []

    for p in dados.get("pedidos", []):
        codigo = p.get("codigo", "Sem código")
        cliente = p.get("cliente", "Sem nome")
        itens = p.get("itens", [])

        pedido = Pedido(codigo, cliente, itens)
        pedidos.append(pedido)

    nome = dados.get("nome", "Sem nome")
    return Loja(nome, pedidos)
    
        
# --- Preparação (não mexa) ---
with open("norte.json", "w", encoding="utf-8") as arquivo:
    json.dump({
        "nome": "Loja Norte",
        "pedidos": [
            {"codigo": "N1", "cliente": "Dora", "itens": [{"produto": "Lápis", "preco": 2, "quantidade": 10}]},
            {"cliente": "Eva"},
            {"codigo": "N3"},
        ],
    }, arquivo, ensure_ascii=False, indent=2)

with open("quebrado.json", "w", encoding="utf-8") as arquivo:
    arquivo.write("{ isso nao e json")

# --- Execução (não mexa) ---
p1 = Pedido("P1", "Ana")
p1.adicionar_item("Teclado", 150, 2)
p1.adicionar_item("Mouse", 80)
p2 = Pedido("P2", "Bruno")
p2.adicionar_item("Monitor", 200)

loja = Loja("Loja Centro")
loja.adicionar_pedido(p1)
loja.adicionar_pedido(p2)
loja.salvar("loja.json")

copia = carregar_loja("loja.json")
assert copia is not None
print(copia.resumo())
print(copia == loja)

print(carregar_loja("nao_existe.json"))
print(carregar_loja("quebrado.json"))

norte = carregar_loja("norte.json")
assert norte is not None
print(norte.resumo())
print([(p.codigo, p.cliente) for p in norte.pedidos])