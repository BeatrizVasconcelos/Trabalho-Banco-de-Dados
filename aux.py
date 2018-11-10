# função que realiza login
def login(db):
    while(True):
        # lê email do usuário
        print('Digite seu e-mail:')
        email = input()

        # executa query para buscar email digitado
        q = "SELECT * FROM usuario WHERE email='{}';".format(email)
        tuplas = db.select(q)  # lista de tuplas

        # caso o email não esteja cadastrado, retorna ao inicio
        if(len(tuplas) < 1):
            print('Email não cadastrado.')
            continue

        # lê a senha do usuário
        print('Digite sua senha:')
        senha = input()

        # checa se a senha foi digitada corretamente
        # caso sim, retorna uma lista com as funções do usuario
        if(senha == tuplas[0][4]):
            print('Logado com sucesso.')
            return tuplas[0]
        # caso não, retorna ao começo
        else:
            print('Senha incorreta.')
            continue


# função que realiza cadastro de usuários
def cadastro(db):
    # lê nome e sobrenome do usuário
    print('Digite seu nome:')
    nome = input()

    print('Digite seu sobrenome:')
    sobrenome = input()

    # lê o email do usuário até que ele digite um email não cadastrado
    while(True):
        print('Digite seu e-mail:')
        email = input()
        q = "SELECT email FROM usuario WHERE email='{}';".format(email)
        tuplas = db.select(q)

        if(len(tuplas) == 0):
            break
        else:
            print('Email já cadastrado.')

    # lê a senha até que o usuario digite a mesma senha duas vezes
    while(True):
        print('Digite uma senha:')
        senha = input()

        print('Digite novamente:')
        senha2 = input()

        if(senha == senha2):
            break
        else:
            print('Senhas não correspondem.')

    # lê o tipo de autor até que o usuário selecione uma opção válida
    while(True):
        print('Digite qual sua qualificação na cozinha! :)')
        print('1 - Amador')
        print('2 - Estudante')
        print('3 - Profissional')
        tipo = int(input())

        if(tipo in (1, 2, 3)):
            if(tipo == 1):
                tipo = 'Amador'
            elif(tipo == 2):
                tipo = 'Estudante'
            else:
                tipo = 'Profissional'
            break
        else:
            print('Digite uma opção válida.')

    # query que insere um novo usuario
    q = "INSERT INTO Autor" \
        " (nome, sobrenome, email, senha, permissao, tipo_autor)" \
        " VALUES ('{}', '{}', '{}', '{}', 'Autor', '{}');"
    q = q.format(nome, sobrenome, email, senha, tipo)

    # executa a query
    db.execute_query(q)

    # query para buscar o usuario inserido
    q = "SELECT * FROM usuario WHERE email='{}';".format(email)
    tuplas = db.select(q)

    # retorna o usuario cadastrado
    return tuplas[0]
