from abc import ABC, abstractmethod
from datetime import datetime

# ========================= MODELO DE CLIENTE =========================

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []  # lista de Conta

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf  # armazenado só com dígitos


# ========================= MODELO DE CONTA ==========================

class Conta:
    def __init__(self, numero: int, cliente: PessoaFisica):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: PessoaFisica, numero: int):
        return cls(numero, cliente)

    # --------- propriedades somente leitura
    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> PessoaFisica:
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # --------- operações
    def sacar(self, valor: float) -> bool:
        excedeu_saldo = valor > self._saldo

        if valor <= 0:
            print("Operação negada! O valor informado é inválido.")
            return False
        if excedeu_saldo:
            print("Operação negada! Você não tem saldo suficiente.")
            return False

        self._saldo -= valor
        print(f"O valor de R${valor:.2f} foi sacado com sucesso!")
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Operação negada! O valor informado não é válido.")
            return False

        self._saldo += valor
        print(f"Muito obrigado, seu depósito de R${valor:.2f} foi realizado com sucesso!")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: PessoaFisica, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        # conta quantos saques já existem no histórico
        total_saques = sum(1 for t in self.historico.transacoes if t["tipo"] == "Saque")

        if valor > self._limite:
            print("Operação negada! O valor do saque excede o limite.")
            return False
        if total_saques >= self._limite_saques:
            print("Operação negada! Quantidade máxima de saques diária excedida, retorne amanhã.")
            return False

        return super().sacar(valor)

    def __str__(self) -> str:
        return (
            f"Agência: {self.agencia}\n"
            f"C/C:     {self.numero:04d}\n"
            f"Titular: {self.cliente.nome}"
        )


# ========================= HISTÓRICO & TRANSACOES ====================

class Historico:
    def __init__(self):
        self._transacoes = []  # lista de dicts

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        ...

    @abstractmethod
    def registrar(self, conta: Conta) -> None:
        ...


class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: Conta) -> None:
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ========================= FUNÇÕES DE INTERFACE ======================

def menu():
    opcoes = """
[1] Depósito
[2] Saque
[3] Extrato
[4] Cadastrar Usuário
[5] Criar Conta Corrente
[6] Listar Usuários
[7] Listar Contas
[0] Sair
--> """
    return input(opcoes).strip()

def normalizar_cpf(cpf_str: str) -> str:
    return "".join(ch for ch in cpf_str if ch.isdigit())

def filtrar_cliente(cpf: str, clientes: list[PessoaFisica]) -> PessoaFisica | None:
    cpf = normalizar_cpf(cpf)
    for c in clientes:
        if c.cpf == cpf:
            return c
    return None

def recuperar_conta_cliente(cliente: PessoaFisica) -> Conta | None:
    if not cliente.contas:
        print("Cliente não possui conta!")
        return None
    # aqui você pode escolher por índice; por enquanto usa a primeira
    return cliente.contas[0]

# --------- operações de negócio (mantendo seus textos)

def operacao_deposito(clientes: list[PessoaFisica]):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor que gostaria de depositar: ").replace(",", "."))
    except ValueError:
        print("Valor inválido.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, Deposito(valor))

def operacao_saque(clientes: list[PessoaFisica]):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor que deseja sacar: ").replace(",", "."))
    except ValueError:
        print("Valor inválido.")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, Saque(valor))

def operacao_extrato(clientes: list[PessoaFisica]):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================\n")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['data']} - {t['tipo']}: R${t['valor']:.2f}")
    print(f"\n=============Saldo: R${conta.saldo:.2f}=============\n")
    print("=========================================\n")

def criar_usuario_cliente(clientes: list[PessoaFisica]):
    print("\n=== Cadastro de Usuário ===")
    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()

    cpf = normalizar_cpf(input("CPF (com ou sem máscara): ").strip())
    if len(cpf) != 11:
        print("CPF inválido.")
        return
    if filtrar_cliente(cpf, clientes):
        print("Erro: já existe um usuário cadastrado com esse CPF.")
        return

    logradouro = input("Logradouro: ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    uf = input("UF (sigla do estado): ").strip().upper()
    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("Usuário cadastrado com sucesso!")

def criar_conta_corrente(clientes: list[PessoaFisica], contas: list[ContaCorrente]):
    cpf = input("Informe o CPF do titular da conta: ").strip()
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("Erro: não existe usuário com esse CPF. Cadastre o usuário primeiro.")
        return

    numero_conta = len(contas) + 1  # sequencial
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print(f"Conta criada com sucesso! Agência: {conta.agencia}, Conta: {conta.numero:04d}, Titular: {cliente.nome}")

def listar_usuarios(clientes: list[PessoaFisica]):
    if not clientes:
        print("\nNenhum usuário cadastrado ainda.")
        return
    print("\n=== Lista de Usuários ===")
    for i, u in enumerate(clientes, start=1):
        print(f"[{i}] Nome: {u.nome}")
        print(f"    CPF: {u.cpf}")
        print(f"    Data Nascimento: {u.data_nascimento}")
        print(f"    Endereço: {u.endereco}")
        print("-" * 40)

def listar_contas(contas: list[ContaCorrente]):
    if not contas:
        print("\nNenhuma conta cadastrada ainda.")
        return
    print("\n=== Lista de Contas ===")
    for i, c in enumerate(contas, start=1):
        print(f"[{i}]")
        print(c)
        print("-" * 40)

# ========================= APLICAÇÃO ================================

def main():
    clientes: list[PessoaFisica] = []
    contas: list[ContaCorrente] = []

    while True:
        opcao = menu()

        if opcao == "1":
            operacao_deposito(clientes)
        elif opcao == "2":
            operacao_saque(clientes)
        elif opcao == "3":
            operacao_extrato(clientes)
        elif opcao == "4":
            criar_usuario_cliente(clientes)
        elif opcao == "5":
            criar_conta_corrente(clientes, contas)
        elif opcao == "6":
            listar_usuarios(clientes)
        elif opcao == "7":
            listar_contas(contas)
        elif opcao == "0":
            print("\nObrigado por utilizar nosso banco! Até logo 👋")
            break
        else:
            print("Operação inválida, por gentileza selecione novamente a opção desejada.")

if __name__ == "__main__":
    main()
