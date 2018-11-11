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
    while(True):
        try:
            resposta = int(input())
        except Exception as e:
            resposta = -1
        finally:
            if(resposta in (1, 2)):
                return resposta
            print('Digite uma opção válida')
