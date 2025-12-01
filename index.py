# ------------------------------------------------------
# --- ESTRUTURA DE DADOS GLOBAL 
# ------------------------------------------------------

# Guarda todos os clientes cadastrados (CPF, email, nome, senha, crédito e carrinho)
clientes_db = {}

# Lista de produtos disponíveis (produtos que podem ser comprados)
produtos_disponiveis = {
    1: {'nome': 'Carne 1kg', 'preco': 490.00},
    2: {'nome': 'Arroz 5kg', 'preco': 10.00},
    3: {'nome': 'Feijão 1kg', 'preco': 4.00},
    4: {'nome': 'Açúcar 1kg', 'preco': 2.00},
    5: {'nome': 'Café 500g', 'preco': 15.00},
    6: {'nome': 'Leite 1L', 'preco': 4.50},
    7: {'nome': 'Óleo de Soja', 'preco': 7.00},
    8: {'nome': 'Macarrão', 'preco': 3.50},
    9: {'nome': 'Sabonete', 'preco': 2.50},
    10: {'nome': 'Shampoo', 'preco': 12.00},
    11: {'nome': 'Pasta de dente', 'preco': 5.00},
    12: {'nome': 'Detergente', 'preco': 2.80},
    13: {'nome': 'Esponja de cozinha', 'preco': 1.50},
    14: {'nome': 'Farinha de Trigo 1kg', 'preco': 4.20},
    15: {'nome': 'Sal 1kg', 'preco': 2.30},
    16: {'nome': 'Biscoito recheado', 'preco': 3.00},
    17: {'nome': 'Refrigerante 2L', 'preco': 8.50},
    18: {'nome': 'Manteiga 200g', 'preco': 6.00},
    19: {'nome': 'Queijo 500g', 'preco': 18.00},
    20: {'nome': 'Presunto 200g', 'preco': 7.50},
}

# Variável para armazenar e rastrear o usuário logado
usuario_logado = None


# ------------------------------------------------------
# --- FUNÇÕES AUXILIARES 
# ------------------------------------------------------

# Função para separar seções visualmente no terminal
def separar():
    print("\n" + "-" * 60 + "\n")


# Remove caracteres não numéricos, checa tamanho e valida dígitos do CPF
def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Cálculo do 1º dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    if int(cpf[9]) != digito1:
        return False

    # Cálculo do 2º dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    return int(cpf[10]) == digito2


# Verifica se o email contém formato mínimo válido
def validar_email(email):
    return "@" in email and "." in email and len(email) >= 5


# ------------------------------------------------------
# --- FUNÇÕES DO SISTEMA 
# ------------------------------------------------------

# Cadastra um novo cliente no sistema
def cadastrar_cliente():
    separar()
    print("CADASTRO DE CLIENTE")
    separar()
    
    nome = input("Digite o nome: ").strip()
    if not nome.replace(" ", "").isalpha():
        print("Erro: O nome deve conter apenas letras.")
        return

    cpf = input("Digite o CPF: ").strip()
    cpf = ''.join(filter(str.isdigit, cpf))

    if cpf in clientes_db:
        print("Erro: CPF já cadastrado.")
        return

    if not validar_cpf(cpf):
        print("Erro: CPF inválido.")
        return

    email = input("Digite o e-mail: ").strip()
    if not validar_email(email):
        print("Erro: E-mail inválido.")
        return

    senha = input("Digite a senha (6 dígitos): ")
    if len(senha) != 6:
        print("Erro: A senha deve ter exatamente 6 dígitos.")
        return

    clientes_db[cpf] = {
        'nome': nome,
        'senha': senha,
        'email': email,
        'credito': 1000.00,
        'carrinho': []
    }

    global usuario_logado
    usuario_logado = cpf

    print("Cliente cadastrado com sucesso!")


# Realiza o login do cliente verificando CPF e senha
def realizar_login():
    global usuario_logado

    separar()
    print("LOGIN NO SISTEMA")
    separar()

    cpf = input("Digite seu CPF: ").strip()
    cpf = ''.join(filter(str.isdigit, cpf))

    if cpf not in clientes_db:
        print("\nUsuário não encontrado.")
        return

    senha = input("Digite sua senha: ")
    if clientes_db[cpf]['senha'] == senha:
        usuario_logado = cpf
        print(f"\nBem-vindo(a), {clientes_db[cpf]['nome']}!")
    else:
        print("\nSenha incorreta.")


# Faz logout do usuário logado
def fazer_logout():
    global usuario_logado
    print(f"\nAté logo, {clientes_db[usuario_logado]['nome']}!")
    usuario_logado = None


# Área de compras: adiciona produtos ao carrinho
def fazer_compras():
    cliente = clientes_db[usuario_logado]

    separar()
    print("ÁREA DE COMPRAS")
    separar()

    while True:
        print(f"Crédito disponível: R$ {cliente['credito']:.2f}\n")

        print("CÓDIGO | PRODUTO                         | PREÇO")
        print("-" * 60)

        for codigo, produto in produtos_disponiveis.items():
            print(f"{codigo:<6} | {produto['nome']:<30} | R$ {produto['preco']:.2f}")

        try:
            opcao = int(input("\nDigite o código do item (ou 0 para voltar): "))
        except ValueError:
            print("Digite um número válido.")
            continue

        if opcao == 0:
            break

        if opcao in produtos_disponiveis:
            item = produtos_disponiveis[opcao]

            if cliente['credito'] >= item['preco']:
                cliente['credito'] -= item['preco']
                cliente['carrinho'].append(item)

                print(f"\n{item['nome']} adicionado! Crédito restante: R$ {cliente['credito']:.2f}")
            else:
                print("Compra negada: Limite de crédito excedido.")
        else:
            print("Item inválido.")


# Exibe os itens do carrinho do cliente
def mostrar_carrinho():
    cliente = clientes_db[usuario_logado]
    carrinho = cliente['carrinho']

    separar()
    print("MEU CARRINHO")
    separar()

    if not carrinho:
        print("Seu carrinho está vazio.\n")
        return

    total = 0
    print("ITENS:")

    for i, item in enumerate(carrinho, start=1):
        print(f"{i}. {item['nome']} - R$ {item['preco']:.2f}")
        total += item['preco']

    print(f"\nValor total: R$ {total:.2f}\n")


# Permite pagar a conta, esvaziar o carrinho e restaurar crédito
def pagar_conta():
    cliente = clientes_db[usuario_logado]
    carrinho = cliente['carrinho']

    separar()
    print("PAGAMENTO DA CONTA")
    separar()

    if not carrinho:
        print("Seu carrinho está vazio. Nada para pagar.\n")
        print(f"Seu crédito atual é: R$ {cliente['credito']:.2f}\n")
        return

    total = sum(item['preco'] for item in carrinho)
    print(f"Total da compra: R$ {total:.2f}")

    confirm = input("Deseja confirmar o pagamento? (s/n): ").lower()
    print(f"Crédito disponível: R$ {cliente['credito']:.2f}")

    if confirm == "s":
        cliente['carrinho'] = []
        cliente['credito'] = 1000.00

        print("\nPagamento realizado com sucesso!")
        print("Seu carrinho foi esvaziado.")
        print("Seu crédito foi restaurado para R$ 1.000,00.\n")
    else:
        print("\nPagamento cancelado.")
        print(f"Seu crédito continua sendo: R$ {cliente['credito']:.2f}\n")


# ------------------------------------------------------
# --- MENU PRINCIPAL 
# ------------------------------------------------------

while True:

    # Caso não haja usuário logado
    if usuario_logado is None:
        separar()
        print("AMAZONCC - VISITANTE")
        separar()

        print("1 - Cadastrar-se")
        print("2 - Fazer Login")

        opcao = input("\nEscolha: ")

        if opcao == '1':
            cadastrar_cliente()
        elif opcao == '2':
            realizar_login()
        else:
            print("Opção inválida.")

    # Caso já esteja logado
    else:
        nome_user = clientes_db[usuario_logado]['nome']

        separar()
        print(f"AMAZONCC - LOGADO COMO: {nome_user}")
        separar()

        print("1 - Fazer Compras")
        print("2 - Mostrar Carrinho")
        print("3 - Pagar Conta")
        print("4 - Logout")

        opcao = input("\nEscolha: ")

        if opcao == '1':
            fazer_compras()
        elif opcao == '2':
            mostrar_carrinho()
        elif opcao == '3':
            pagar_conta()
        elif opcao == '4':
            fazer_logout()
        else:
            print("Opção inválida.")
