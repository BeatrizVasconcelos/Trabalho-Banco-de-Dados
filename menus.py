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
            else:
                print('Digite um valor válido')
