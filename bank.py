#Atualizar a implementação do sistemaa bancário, para armazenar os dados de clientes e contas bancárias em objetos ao invés de dicionários. 
import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        #Iniciando contas como lista vazia
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    #adiciona a conta recebida por parametro, na lista de contas 
    def adicionar_conta(self, conta):
            self.contas.append(conta)

class Pessoa_fisica(Cliente):
     def __init__(self, nome, data_nascimento, cpf, endereco):
          #Chamando costrutor da classe pai passando o endereço que é o argumento pedido.
          super().__init__(endereco)
          self.nome = nome
          self.data_nascimento = data_nascimento
          self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        #Classe conta vai receber os seguintes atributos
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        #Histórico é do tipo historico
        self._historico = Historico()

    #Mapear o class method de nova conta
    @classmethod
    #ao transfomar um método de classes a convenção usada é (cls) e não (self) como é de costume
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    #Definindo as próriedades 
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    #Operações - saque
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo 
        
        if excedeu_saldo:
            print("ERRO --- Operação falhou! Você não tem saldo suficiente!")
        
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            #Para retornar que a operação de saque que eu estou realizando deu certo
            return True
        
        else:
            print("ERRO --- Operação falhou! Valor informado inválido!")
        #Retornar falso caso a operação de saque não de certo
        return False
    
    #Operações - depósito
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso")
        else:
            print("ERRO --- Operação falhou! Valor informa é inválido!")
            return False
        
        return True 

class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        #Chamando construtor da classe conta, passando o que é pedido (numero e cliente)
        super().__init__(numero, cliente)
        #Criando os atributos limite e limite de saques
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        #Analisando a classe histórico para ver quantas operações de deposito/saque foram feitas na conta.
        #verificando o numero de saques para ver se excede o limite, e pegando o tamanho da lista para verificar se não excedeu o limite de saques que é igual a 3
        numero_saques = len(
            #verificando todas as transações do histórico e vendo se o tipo dessa transação é igual a saque
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("ERRO --- Operação falhou! O valor de saque excede o limite.")

        elif excedeu_saques:
            print("ERRO --- Opereção falhou! Número máximo de saques excedido!")
        #Caso ele não entre no if e elif vai retornar o boleano de saque.
        else:
            return super().sacar(valor)
        
        #caso não entre nos itens acima retorna um false
        return False
    #Método str que é a representação da classe.
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C: \t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        #Lista de transações do histórico
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    #método para adicionar transações
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {   #qual que é o nome da transação (saque/deposito)
                "tipo": transacao.__class__.__name__,
                #valor da transação
                "valor": transacao.valor,
                #módulo date time, para saber a data que a transação foi feita
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%¨M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

#Mapeando o saque.
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        #se der true eu adiciono a transição no histórico da conta
        if sucesso_transacao:
            conta.historico.adcionar_transacao(self)

#Mapeando o deposito.
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

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

def recuperar_conta_cliente(cliente):
    #verificando se  o cliente possui conta
    if not cliente.contas:
        print("ERRO --- Cliente não possui conta!")
        return
    
    # FIXME: não permiete o cliente escolher a conta
    #pega a primeira conta do cliente
    return cliente.contas[0]

def deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuarios(cpf,clientes)

    if not cliente:
            print("ERRO --- Cliente não encontrado!")
            return
    
    valor = float(input("Informe o valor do depósito:"))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    #Caso encontre o cliente eu passoa a conta e a transação 
    cliente.realizar_transacao(conta, transacao)

def filtrar_usuarios(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def saque(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("ERRO --- Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor) 

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente:")
    cliente = filtrar_usuarios(cpf, clientes)

    if not cliente:
        print("ERRO --- Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("########## EXTRATO ##########")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("#############################")

def criar_contas(numero_conta, clientes ,contas):
    cpf = input("Informe o CPF do usuário (Somente numeros):")
    cliente = filtrar_usuarios(cpf, clientes)
    if not cliente:
        print("ERRO --- Cliente não encontrado!")
        return

    conta = Conta_corrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("#" * 80)
        print(textwrap.dedent(str(conta)))

def novo_usuario(clientes):
    #pergunto primeiro o cpf para saber se esse usuário já está cadastrado
    cpf = input("Informe seu CPF(Somente números):")
    cliente = (filtrar_usuarios(cpf,clientes))
    #Se o usuário já existir
    if cliente:
        print("[ERRO] JÁ EXISTE UM USUÁRIO COM ESSE CPF")
        return
    
    nome = str(input("Informe seu nome:"))
    data_nascimento = input("Informe sua data de nascimento(dd-mm-aaaa)")
    endereco = input("Informe seu Endereço:")

    cliente = Pessoa_fisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)

    clientes.append(cliente)
    print("---Usuário cadastrado com sucesso!---")

def banco():
    clientes = []
    contas = []

    while True:
        opcao = menu()
        #Se opcao receber o valor 1, pergunte o valor do depósito e execute a função deposito
        if opcao == "1":
            deposito(clientes)
        elif opcao == "2":
            saque(clientes)
        elif opcao == "3":
            exibir_extrato(clientes)
        elif opcao == "4":
            novo_usuario(clientes)
        elif opcao == "5":
            numero_conta = len(contas) + 1
            criar_contas(numero_conta, clientes, contas)
        elif opcao == "6":
            listar_contas(contas)
        elif opcao == "7":
            print("Saindo...")
            break
    
banco()