from database import Database
from menus import menu_inicial
from aux import (login, cadastro)


# linha de execução do programa
def main():
    # conexão com banco de dados
    db = Database()
    # executa programa
    while(True):
        # executa o menu inicial e recebe a resposta do usuario
        opcao = menu_inicial()
        # abre menu de login
        if(opcao == 1):
            # retorna o usuario logado
            usuario = login(db)
            print(usuario)

        # abre menu de cadastro
        elif(opcao == 2):
            # retorna o usuario cadastrado
            usuario = cadastro(db)
            print(usuario)

        # encerra programa
        else:
            print('Programa encerrado')
            break


if(__name__ == '__main__'):
    main()
