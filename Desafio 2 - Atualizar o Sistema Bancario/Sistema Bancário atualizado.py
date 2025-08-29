from datetime import datetime

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


def depositar(saldo, valor, extrato, /):
    """Depósito (parâmetros apenas por POSIÇÃO). Retorna saldo e extrato."""
    if valor > 0:
        saldo += valor
        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{hora} - Depósito: R${valor:.2f}\n"
        print(f"Muito obrigado, seu depósito de R${valor:.2f} foi realizado com sucesso!")
    else:
        print("Operação negada! O valor informado não é válido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Saque (parâmetros apenas por NOME).
    Retorna saldo, extrato e numero_saques (atualizado).
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if valor <= 0:
        print("Operação negada! O valor informado é inválido.")
    elif excedeu_saldo:
        print("Operação negada! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação negada! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação negada! Quantidade máxima de saques diária excedida, retorne amanhã.")
    else:
        saldo -= valor
        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        extrato += f"{hora} - Saque: R${valor:.2f}\n"
        numero_saques += 1
        print(f"O valor de R${valor:.2f} foi sacado com sucesso!")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    """Extrato (saldo por POSIÇÃO, extrato por NOME). Não retorna nada; apenas imprime."""
    conteudo = extrato if extrato else "Não foram realizadas movimentações."
    print("\n================ EXTRATO ================\n")
    print(f"{conteudo}", end="")
    print(f"\n=============Saldo: R${saldo:.2f}=============\n")
    print("=========================================\n")


def criar_usuario_cliente(usuarios, /):
    """
    Cadastra um novo cliente.
    Armazena: nome, data_nascimento, cpf (somente dígitos) e endereço (string completa).
    Exige CPF único.
    """
    print("\n=== Cadastro de Usuário ===")
    nome = input("Nome completo: ").strip()
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()

    # Normaliza CPF para apenas dígitos
    cpf_informado = input("CPF (com ou sem máscara): ").strip()
    cpf = "".join(ch for ch in cpf_informado if ch.isdigit())

    if not cpf:
        print("CPF inválido.")
        return

    # 🔎 Verifica unicidade do CPF diretamente aqui
    for u in usuarios:
        if u["cpf"] == cpf:
            print("Erro: já existe um usuário cadastrado com esse CPF.")
            return

    # Endereço em uma única string no formato pedido
    logradouro = input("Logradouro: ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    uf = input("UF (sigla do estado): ").strip().upper()

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{uf}"

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,                  # armazenado só com dígitos
        "endereco": endereco
    })

    print("Usuário cadastrado com sucesso!")


def conta_corrente(usuarios, contas, /):

    AGENCIA_PADRAO = "0001"

    """
    Cria uma nova conta corrente vinculada a um usuário existente.
    A conta é composta por: agencia, numero_conta, usuario.
    """
    cpf_informado = input("Informe o CPF do titular da conta: ").strip()
    cpf = "".join(ch for ch in cpf_informado if ch.isdigit())

    # Verifica se usuário existe
    usuario = None
    for u in usuarios:
        if u["cpf"] == cpf:
            usuario = u
            break

    if not usuario:
        print("Erro: não existe usuário com esse CPF. Cadastre o usuário primeiro.")
        return

    # Número da conta sequencial
    numero_conta = len(contas) + 1

    conta = {
        "agencia": AGENCIA_PADRAO,
        "numero_conta": numero_conta,
        "usuario": usuario
    }

    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {AGENCIA_PADRAO}, Conta: {numero_conta:04d}, Titular: {usuario['nome']}")


def listar_usuarios(usuarios, /):

    
    """Exibe todos os usuários cadastrados."""
    if not usuarios:
        print("\nNenhum usuário cadastrado ainda.")
        return

    print("\n=== Lista de Usuários ===")
    for i, usuario in enumerate(usuarios, start=1):
        print(f"[{i}] Nome: {usuario['nome']}")
        print(f"    CPF: {usuario['cpf']}")
        print(f"    Data Nascimento: {usuario['data_nascimento']}")
        print(f"    Endereço: {usuario['endereco']}")
        print("-" * 40)


def listar_contas(contas, /):

    """Exibe todas as contas criadas."""
    if not contas:
        print("\nNenhuma conta cadastrada ainda.")
        return

    print("\n=== Lista de Contas ===")
    for i, conta in enumerate(contas, start=1):
        titular = conta["usuario"]["nome"]
        print(f"[{i}] Agência: {conta['agencia']} | Conta: {conta['numero_conta']:04d} | Titular: {titular}")
    print("-" * 40)



# ===================== Aplicação =====================

def main():

    LIMITE = 500
    LIMITE_SAQUES = 3

    saldo = 0.0
    extrato = ""
    numero_saques = 0

    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            try:
                valor = float(input("Informe o valor que gostaria de depositar: ").replace(",", "."))
            except ValueError:
                print("Valor inválido.")
                continue
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            try:
                valor = float(input("Informe o valor que deseja sacar: ").replace(",", "."))
            except ValueError:
                print("Valor inválido.")
                continue
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=LIMITE,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario_cliente(usuarios)

        elif opcao == "5":
            conta_corrente(usuarios, contas)

        elif opcao == "6":
            listar_usuarios(usuarios)

        elif opcao == "7":
            listar_contas(contas)

        elif opcao == "0":
            print("\nObrigado por utilizar nosso banco! Até logo 👋")
            break

        else:
            print("Operação inválida, por gentileza selecione novamente a opção desejada.")



if __name__ == "__main__":
    main()


