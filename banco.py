menu = -1
saldo = float()
extrato = ""
contagem_saques = []
while menu != 0:
    menu = int(input("[1]Deposito \n[2]Sacar \n[3]Extrato \n[0]Sair \n:"))
    saldo 
    extrato 
    contagem_saques
    if menu == 1:
        deposito = float(input("Informe o valor que deseja depositar "))
        if deposito > 0:
            print(f"Você acabou de realizar o deposito de R${deposito}")
        saldo += deposito
        continue
    elif menu == 2:
        contagem_saques
        saque = float(input("Informe o valor que deseja sacar:"))
        if saque > saldo:    
            print("Seu saldo é insuficiente")
            continue
        elif saque > 500:
            print("Limite de saque maior que o permitido")
            continue
        elif len(contagem_saques) > 2:
            print("Você chegou ao limite de saques diarios")
        elif saque < deposito:
            saldo -= saque 
            extrato = f"Saque no valor de {saque}"
            contagem_saques.append(f"\n{extrato}")
            print(f"você acabou de relizar um saque no valor de R${saque}, seu novo saldo é de R${saldo}")
            continue
        else:
            print("Limite de saques diarios atingidos")
            continue           
    elif menu == 3:
        print(f"Exibindo extrato...\nSeu saldo total é de {saldo}\n E você realizou os seguintes saques - {contagem_saques}")   
        continue
    elif menu == 0:
        print("Saindo")
        break
    else:
        print("Escolha uma opção valida")