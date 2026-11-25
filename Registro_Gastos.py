from dataclasses import dataclass, field, asdict
import json
import time


@dataclass
class Gasto:
    descricao: str
    valor: float
    categoria: str = "Outros"

    def __post_init__(self):
        if not isinstance(self.descricao, str):
            raise ValueError("Descrição inválida")

        self.descricao = self.descricao.strip()

        if not self.descricao:
            raise ValueError("Descrição vazia")

        if not isinstance(self.valor, (int, float)) or isinstance(self.valor, bool) or self.valor <= 0:
            raise ValueError("Valor inválido")

        self.categoria = self.categoria.strip().title()

        if not self.categoria:
            self.categoria = "Outros"

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["descricao"],
            dados["valor"],
            dados.get("categoria", "Outros")
        )

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        return (
            f"{self.descricao} | "
            f"R$ {self.valor:.2f} | "
            f"{self.categoria}"
        )


@dataclass
class Extrato:
    gastos: list = field(default_factory=list)

    @classmethod
    def from_lista(cls, registros):
        gastos = []
        erros = []

        for registro in registros:
            try:
                gastos.append(Gasto.from_dict(registro))
            except (KeyError, ValueError) as erro:
                erros.append(str(erro))

        return cls(gastos), erros

    def __len__(self):
        return len(self.gastos)

    def __str__(self):
        if not self.gastos:
            return "Extrato vazio"

        return "\n".join(
            f"{i + 1}. {gasto}"
            for i, gasto in enumerate(self.gastos)
        )

    @property
    def total(self):
        return round(sum(g.valor for g in self.gastos), 2)

    def por_categoria(self):
        totais = {}

        for gasto in self.gastos:
            categoria = gasto.categoria
            totais[categoria] = totais.get(categoria, 0) + gasto.valor

        return {
            categoria: round(valor, 2)
            for categoria, valor in totais.items()
        }


# FUNÇÕES DO SISTEMA

def cadastrar_gasto(extrato):
    try:
        descricao = input("Descrição: ")
        valor = float(input("Valor: ").replace(",", "."))
        categoria = input("Categoria: ")

        gasto = Gasto(descricao, valor, categoria)
        extrato.gastos.append(gasto)

        print("\nGasto cadastrado com sucesso!")

    except ValueError as erro:
        print(f"\nErro: {erro}")


def mostrar_extrato(extrato):
    print("\n--- EXTRATO ---")
    print(extrato)


def mostrar_total(extrato):
    print(f"\nTotal de gastos: R$ {extrato.total:.2f}")


def mostrar_categorias(extrato):
    print("\n--- GASTOS POR CATEGORIA ---")

    for categoria, valor in extrato.por_categoria().items():
        print(f"{categoria}: R$ {valor:.2f}")


def remover_gasto(extrato):
    if not extrato.gastos:
        print("\nNão existem gastos cadastrados.")
        return

    mostrar_extrato(extrato)

    try:
        indice = int(input("\nNúmero do gasto para remover: ")) - 1

        gasto = extrato.gastos.pop(indice)
        print(f"\nGasto '{gasto.descricao}' removido.")

    except (ValueError, IndexError):
        print("\nOpção inválida.")


def salvar_json(extrato):
    dados = [gasto.to_dict() for gasto in extrato.gastos]

    with open("gastos.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    print("\nDados salvos!")


def carregar_json():
    try:
        with open("gastos.json", "r", encoding="utf-8") as arquivo:
            registros = json.load(arquivo)

        extrato, erros = Extrato.from_lista(registros)

        if erros:
            print(f"\nForam encontrados {len(erros)} registros inválidos.")

        return extrato

    except FileNotFoundError:
        return Extrato()

    except (json.JSONDecodeError, OSError) as erro:
        print(f"\nErro ao carregar arquivo: {erro}")
        return Extrato()



# MENU DE INTERAÇÃO!!!


def main():
    extrato = carregar_json()

    while True:
        print("""
========== CONTROLE DE GASTOS ==========

1 - Cadastrar gasto
2 - Mostrar extrato
3 - Mostrar total
4 - Gastos por categoria
5 - Remover gasto
6 - Salvar dados
0 - Sair

========================================
""")
        time.sleep(2)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_gasto(extrato)
            time.sleep(1.5)

        elif opcao == "2":
            mostrar_extrato(extrato)
            time.sleep(2)
            input("\nPressione ENTER para voltar ao menu")

        elif opcao == "3":
            mostrar_total(extrato)
            input("\nPressione ENTER para voltar ao menu")

        elif opcao == "4":
            mostrar_categorias(extrato)
            input("\nPressione ENTER para voltar ao menu")

        elif opcao == "5":
            remover_gasto(extrato)
            input("\nPressione ENTER para voltar ao menu")

        elif opcao == "6":
            salvar_json(extrato)

        elif opcao == "0":
            salvar_json(extrato)
            print("\nEncerrando sistema...")
            break

        else:
            print("\nOpção inválida!")


if __name__ == "__main__":
    main()