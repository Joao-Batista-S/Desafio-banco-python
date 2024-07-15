def menu():
    menu = input("""

[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Usuário
[5] Nova conta
[6] Listar Contas
[7] Sair
=> """)
    #Retornar o numero que foi escolhido no menu
    return menu

def deposito(saldo, valor,extrato, /): #/ barra para passar os argumentos de forma posicional
    #se o valor for maior que 0 executa a função de deposito, adicionando dinheiro ao saldo 
    if valor > 0:
        saldo += valor
        extrato = f"Depósito no valor de R$:{valor}\n"
        print("---Depósito realizado com sucesso!---")
    #Se o valor for menor que 0 ou diferente retorna um ERRO
    else:
        print("[ERRO]O valor informado não é valido!")
    #retorna o saldo e o extrato informado nessa função
    return saldo, extrato
def saque(*, saldo, valor, extrato,limite,qtd_saques,limite_saques): # usando * como primeiro parametroa para passar de forma nomeada
    #Atribuindo valor as possiveis erros que podem ocorrer no saque
    sem_saldo = valor > saldo
    sem_limite = valor > limite
    saque_diarios = qtd_saques >= limite_saques
    
    if sem_saldo:
        print("[ERRO] VOCÊ NÃO TEM SALDO SUFICIENTE!")
    elif sem_limite:
        print("[ERRO] SEU LIMITE DE VALOR DE SAQUE É DE R$500,00")
    elif saque_diarios:
        print("[ERRO] NÚMERO MÁXIMO DE SAQUES DIARIOS ATINGIDO")
    #Caso nenhum erro ocorra, vamos calcular a função de saque e adicionar-mos o valor ao extrato
    elif valor > 0:
        saldo -= valor
        extrato += f"Você realizou um saque no valor de R$:{valor:.2f}\n"
        qtd_saques += 1
        print("---Saque realizado com sucesso!---")
    #Default para valores não reconhecidos
    else:
        print("[ERRO] O VALOR INFORMADO NÃO É UM VALOR VALIDO")
    return saldo, extrato, qtd_saques
def exibir_extrato(saldo, /, *, extrato):
        print("\n------------ EXTRATO ---------------")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"Saldo: RS: {saldo:.2f}")
        print("-------------------------------------")

def filtrar_usuarios(cpf,usuarios):
    #verificar se o cpf do usuário que está na listaé igual ao cpf que foi passado, se sim ele retorna o usuário
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    #verifica se usuarios_filtrados não é uma lista vazia
    return usuarios_filtrados[0] if usuarios_filtrados else None

def novo_usuario(usuarios):
    #pergunto primeiro o cpf para saber se esse usuário já está cadastrado
    cpf = input("Informe seu CPF(Somente números):")
    usuario = (filtrar_usuarios(cpf,usuarios))
    #Se o usuário já existir
    if usuario:
        print("[ERRO] JÁ EXISTE UM USUÁRIO COM ESSE CPF")
        return
    
    nome = str(input("Informe seu nome:"))
    data_nascimento = input("Informe sua data de nascimento(dd-mm-aaaa)")
    endereco = input("Informe seu Endereço:")

    usuarios.append({"nome":nome, "data_nascimento":data_nascimento, "cpf": cpf, "endereco": endereco})
    print("---Usuário cadastrado com sucesso!---")

def criar_contas(agencia,numero_conta,usuarios):
    cpf = input("Informe o CPF do usuário (Somente numeros):")
    usuario = filtrar_usuarios(cpf, usuarios)
    if usuario:
        print("---Conta criada com sucesso!---")
        return{"agencia":agencia,"numero_conta": numero_conta, "usuario": usuario}
    print("[ERRO] Usuário não encontrado")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(linha)
def banco():
    #Constante da quantidade limite de saques
    LIMITE_DE_SAQUES = 3
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    qtd_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        #Se opcao receber o valor 1, pergunte o valor do depósito e execute a função deposito
        if opcao == "1":
            valor = float(input("Informe o valor de depósito:"))
            #saldo e extrato vão receber os valores que a função depósito vai retornar
            saldo, extrato = deposito(saldo,valor,extrato)
        elif opcao == "2":
            valor = float(input("Informe o valor que deseja sacar:"))
            saldo, extrato, qtd_saques = saque(saldo = saldo,
                                   valor = valor,
                                   extrato = extrato,
                                   limite = limite,
                                   qtd_saques = qtd_saques,
                                   limite_saques=LIMITE_DE_SAQUES
                                )
        elif opcao == "3":
            exibir_extrato(saldo, extrato = extrato)
        elif opcao == "4":
            novo_usuario(usuarios)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_contas(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            print("Saindo...")
            break
    
banco()