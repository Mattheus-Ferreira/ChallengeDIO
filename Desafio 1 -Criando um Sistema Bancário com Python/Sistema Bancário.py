from datetime import datetime

menu = """

[1] Deposito
[2] Saque
[3] Extrato
[0] Sair

--> """

saldo = 0
LIMITE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor que gostaria de depositar: "))

        if valor > 0:
            saldo += valor
            hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            extrato += f"{hora} - Depósito: R$ {valor:.2f}\n"
            print (f"Muito obrigado, seu deposito de R${valor:.2f}, foi realizado com sucesso! ")

        else:
            print("Operação Negada! O valor informado não é válido.")

    elif opcao == "2":
        valor = float(input("Informe o valor que deseja sacar: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > LIMITE

        excedeu_saques = numero_saques >= LIMITE_SAQUES


        if valor <= 0:
            print("Operação Negado! O valor informado é invalido")

        elif excedeu_saldo:
            print("Operação Negada! Você não tem saldo suficiente")

        elif excedeu_limite:
            print("Operação Negada! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação Negada! Quantidade máxima de saques diario excedido, retorne amanhã.")

        else:          
            saldo -= valor
            hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            extrato += f"{hora} - Saque: R${valor:.2f}\n"
            numero_saques += 1
            print(f"O valor de R${valor} foi retirado com sucesso!")

    elif opcao == "3":
        conteudo = extrato if extrato else "Não foram realizadas movimentações."
        
       
        print( "================ EXTRATO ================\n")
        print(conteudo)
        print(f"           Saldo: R${saldo:.2f}\n          ")
        print( "==========================================\n")
                                                                       

     

    elif opcao == "0":
        print("\nObrigado por utilizar nosso banco! Até logo 👋")
        break

    else:
        print("Operação inválida, por gentileza selecione novamente a opção desejada.")