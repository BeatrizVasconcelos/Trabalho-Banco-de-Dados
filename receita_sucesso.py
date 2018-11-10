from database import Database
from menus import (menu_inicial, menu_principal)
from aux import (login, cadastro)


# linha de execução do programa
def main():
    # conexão com banco de dados
    db = Database()
    # executa o menu de login / cadastro
    while(True):
        # executa o menu inicial e recebe a resposta do usuario
        opcao = menu_inicial()
        # abre menu de login
        if(opcao == 1):
            # retorna o usuario logado
            usuario = login(db)
            break

        # abre menu de cadastro
        elif(opcao == 2):
            # retorna o usuario cadastrado
            usuario = cadastro(db)
            break

        # encerra programa
        else:
            print('Programa encerrado')
            db.encerrar()
            exit()

    # mensagem de boas vindas
    nome_completo = get_nome(usuario)
    print('Bem-vindo(a), {}!'.format(nome_completo))

    while(True):
        # usuario logado é autor
        if(len(usuario) > 6):
            opcao = menu_principal(1)
            if(opcao == 5):
                print('Volte sempre, {}'.format(nome_completo))
                break
        # usuario é ademir
        else:
            opcao = menu_principal(0)
            if(opcao == 3):
                print('Volte sempre, {}'.format(nome_completo))
                break


def get_nome(usuario):
    return ' '.join((usuario[1], usuario[2]))


if(__name__ == '__main__'):
    main()
