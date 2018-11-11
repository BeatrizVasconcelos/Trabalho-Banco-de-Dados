from database import Database
from menus import (menu_inicial, menu_principal)
from aux import (login, cadastro, get_receitas, insere_receita)


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
            # exibe o menu de autor
            # resoista do usuario
            opcao = menu_principal(1)
            # caso o usuario escolha a opcao 1
            # exibe a lista total de receitas
            if(opcao == 1):
                # imprime a lista de receitas
                imprime_receitas(db)
            # caso o usuario escolha a opcao 2
            # exibe menu para inserir receita
            # e insere
            elif(opcao == 2):
                insere_receita(db, usuario[0])
            # caso o usuario escolha a opcao 3
            # exibe a lista das receitas dele
            elif(opcao == 3):
                cond = " WHERE id_autor={}".format(usuario[0])
                imprime_receitas(db, cond)
            elif(opcao == 5):
                print('Volte sempre, {}'.format(nome_completo))
                break
        # usuario é ademir
        else:
            # exibe o menu de ademir
            # resposta do usuario
            opcao = menu_principal(0)
            # caso o usuario escolha a opcao 1
            # exibe a lista total de receitas
            if(opcao == 1):
                # imprime a lista de receitas
                imprime_receitas(db)
            # caso o usuario escolha a opcao 2
            # altera seus dados
            elif(opcao == 2):
                pass
            elif(opcao == 3):
                print('Volte sempre, {}'.format(nome_completo))
                break


def get_nome(usuario):
    return ' '.join((usuario[1], usuario[2]))


def imprime_receitas(db, *argv):
    # retorna a lista de receitas
    if(len(argv) > 0):
        receitas = get_receitas(db, argv[0])
        print('\nMinhas receitas:')
    else:
        receitas = get_receitas(db)
        print('\nLista de receitas:')
    # caso a lista esteja vazia, imprime uma mensagem informando
    if(len(receitas) == 0):
        print('Nenhuma receita encontrada')
    # caso haja elementos, imprime todos
    else:
        # imprime as receitas
        for receita in receitas:
            # busca o autor
            q = "SELECT nome, sobrenome, tipo_autor FROM autor WHERE id={}"
            q = q.format(receita[3])
            autor = (db.select(q))[0]

            # busca os ingredientes
            q = "SELECT nome, quantidade, medida FROM ingrediente INNER JOIN" \
                " utilizado_em ON id=id_ingrediente WHERE id_receita={}" \
                " ORDER BY nome;".format(receita[0])
            ingredientes = db.select(q)

            # busca o modo de preparo
            q = "SELECT num_passo, passo FROM preparo WHERE id_receita={}" \
                " ORDER BY num_passo;".format(receita[0])
            passos = db.select(q)

            # imprime informações da receita
            print('=======================')
            print('ID: {}'.format(receita[0]))
            print('Nome: {}'.format(receita[1]))
            print('Autor: {}'.format(autor[0] + ' ' + autor[1]))
            print('Nível do Autor: {}'.format(autor[2]))
            print('Avaliação Média: {}'.format(receita[2]))
            print('---')
            print('Ingredientes:')
            for ing in ingredientes:
                print('{} - {} {}'.format(ing[0], ing[1], ing[2]))
            print('\nModo de Preparo:')
            for n, passo in passos:
                print('{} - {}'.format(n, passo))
            print('=======================')
        print()


if(__name__ == '__main__'):
    main()
