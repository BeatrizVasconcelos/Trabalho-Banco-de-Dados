# from database import Database


def main():
    pass


def login(db):
    success = False
    while(not success):
        print('Digite seu e-mail:')
        email = input()

        q = 'SELECT * FROM usuario WHERE email={};'.format(email)
        tuplas = db.select(q)

        if(len(tuplas) < 1):
            print('Email não cadastrado.')
            continue

        print('Digite sua senha:')
        senha = input()

        if(senha == tuplas[0][4]):
            print('Logado com sucesso.')
            return tuplas
        else:
            print('Senha incorreta.')
            continue


def cadastro(db):
    print('Digite seu nome:')
    nome = input()

    print('Digite seu sobrenome:')
    sobrenome = input()

    while(True):
        print('Digite seu e-mail:')
        email = input()
        q = 'SELECT email FROM usuario WHERE email={};'.format(email)
        tuplas = db.select(q)

        if(len(tuplas) == 0):
            break
        else:
            print('Email já cadastrado.')

    while(True):
        print('Digite uma senha:')
        senha = input()

        print('Digite novamente:')
        senha2 = input()

        if(senha == senha2):
            break
        else:
            print('Senhas não correspondem.')

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

    q = "INSERT INTO Autor"
    " (nome, sobrenome, email, senha, permissao, tipo_autor)"
    " VALUES ({}, {}, {}, {}, Autor, {});"
    q = q.format(nome, sobrenome, email, senha, tipo)

    db.execute_query(q)


if(__name__ == '__main__'):
    main()
