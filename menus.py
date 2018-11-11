def menu_inicial():
    print('Seja bem vindo(a) ao Receita de sucesso!')
    print('Selecione uma opção:')
    print('(1) Fazer Login')
    print('(2) Cadastrar-se')
    print('(3) Sair')

    while(True):
        try:
            resposta = int(input())
        except ValueError:
            resposta = -1
        finally:
            if(resposta in (1, 2, 3)):
                return resposta
            print('Digite um valor válido')


def menu_principal(tipo_usuario):
    # usuario é autor
    if(tipo_usuario == 1):
        print('Selecione uma opção:')
        print('(1) Visualizar todas as receitas')
        print('(2) Enviar receita')
        print('(3) Minhas receitas')
        print('(4) Buscar receita')
        print('(5) Alterar Cadastro')
        print('(6) Sair')
        opcoes = range(6)
    # usuario é ademir
    elif(tipo_usuario == 0):
        print('Selecione uma opção:')
        print('(1) Visualizar todas as receitas')
        print('(2) Alterar Cadastro')
        print('(3) Sair')
        opcoes = range(3)
    # usuario não existe
    else:
        return None

    while(True):
        try:
            resposta = int(input())
        except ValueError:
            resposta = -1
        finally:
            if((resposta - 1) in opcoes):
                return resposta
            print('Digite uma opção válida')


def menu_busca():
    print('Selecione uma opção:')
    print('(1) Ingrediente')
    print('(2) Autor')
    print('(3) Categoria')
    while(True):
        try:
            resposta = int(input())
        except Exception as e:
            resposta = -1
        finally:
            if(resposta in (1, 2, 3)):
                return resposta
            print('Digite uma opção válida')


def menu_alt_user(user):
    # exibe dados do usuário
    print('Selecione uma opção:')
    print("Seus dados atuais:")
    print("(1) - Nome: {}".format(user[1]))
    print("(2) - Sobrenome: {}".format(user[2]))
    print("(3) - Email: {}".format(user[3]))
    print("(4) - Senha")
    # caso ele seja autor, exibe o tipo
    if(len(user) > 6):
        print("(5) - Tipo de autor: {}".format(user[6]))
        opcoes = (1, 2, 3, 4, 5)
    else:
        opcoes = (1, 2, 3, 4)

    # lê a resposta do usuario
    while(True):
        try:
            resposta = int(input())
        except ValueError:
            resposta = -1
        finally:
            if(resposta in opcoes):
                return resposta
            print('Digite uma opção válida')
