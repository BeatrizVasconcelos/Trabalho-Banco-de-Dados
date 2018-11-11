from getpass import getpass
from cripto import crip
from database import Database
from menus import (menu_inicial, menu_principal, menu_busca, menu_alt_user)
from aux import (login,
                 cadastro,
                 get_receitas,
                 insere_receita,
                 sim_ou_nao,
                 alterar_cadastro)


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
                imprime_receitas(db, usuario[0])
            # caso o usuario escolha a opcao 2
            # exibe menu para inserir receita
            # e insere
            elif(opcao == 2):
                insere_receita(db, usuario[0])
            # caso o usuario escolha a opcao 3
            # exibe a lista das receitas dele
            elif(opcao == 3):
                cond = " WHERE id_autor={}".format(usuario[0])
                imprime_receitas(db, usuario[0], cond)
            # caso o usuário escolha a opção 4
            # exibe o menu de busca e busca
            elif(opcao == 4):
                print('Pelo que deseja buscar?')
                resposta = menu_busca()
                # busca por ingredientes
                if(resposta == 1):
                    # lê o ingrediente que será buscado
                    print('Digite o nome do ingrediente')
                    ing = input()
                    # busca pelo ingrediente e imprime
                    cond = " INNER JOIN utilizado_em ON id_receita=id WHERE" \
                        " id_ingrediente IN (SELECT id FROM ingrediente" \
                        " WHERE nome='{}')".format(ing)
                    imprime_receitas(db, usuario[0], cond)
                # busca por autor
                elif(resposta == 2):
                    # lê o autor que será buscado
                    print('Digite o nome ou sobrenome do autor: (não ambos)')
                    aut = input()
                    # busca pelo autor e imprime
                    cond = " WHERE id_autor IN (SELECT id FROM autor WHERE " \
                        "nome LIKE '%{}%' or sobrenome LIKE '%{}%')"
                    cond = cond.format(aut, aut)
                    imprime_receitas(db, usuario[0], cond)
                # busca por categoria
                else:
                    print('Digite a categoria:')
                    cat = input()
                    cond = " WHERE categoria = '{}'".format(cat)
                    imprime_receitas(db, usuario[0], cond)
            # caso o usuario escolha a opcao 5
            # altera seus dados
            elif(opcao == 5):
                resposta = menu_alt_user(usuario)
                # caso ele deseje alterar o nome
                if(resposta == 1):
                    cond = cond_alteracao('nome')
                # caso ele deseje alterar o sobrenome
                elif(resposta == 2):
                    cond = cond_alteracao('sobrenome')
                # caso ele deseje alterar o email
                elif(resposta == 3):
                    cond = cond_alteracao('email')
                # caso ele deseje alterar a senha
                elif(resposta == 4):
                    # lê a senha atual, por segurança
                    while(True):
                        senha = getpass('Digite sua senha atual:\n')
                        senha = crip(senha)
                        if(senha == usuario[4]):
                            break
                        else:
                            print('Senha incorreta')

                    # pede a senho nova duas vezes
                    while(True):
                        nova = getpass('Digite uma nova senha:\n')
                        nova2 = getpass('Digite novamente:\n')

                        if(nova == nova2):
                            nova = crip(nova)
                            break
                        else:
                            print('Senhas não correspondem.')
                    cond = "usuario SET senha='{}'".format(nova)
                # caso ele deseje alterar o tipo de autor
                else:
                    print('Digite seu novo nível:')
                    while(True):
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
                    cond = "autor SET tipo_autor='{}'".format(tipo)

                alterar_cadastro(db, usuario[0], cond)
                print('Feito! Reinicie para aplicar alterações.')
            elif(opcao == 6):
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
                imprime_receitas(db, usuario[0])
            # caso o usuario escolha a opcao 2
            # altera seus dados
            elif(opcao == 2):
                resposta = menu_alt_user(usuario)
                # caso ele deseje alterar o nome
                if(resposta == 1):
                    cond = cond_alteracao('nome')
                # caso ele deseje alterar o sobrenome
                elif(resposta == 2):
                    cond = cond_alteracao('sobrenome')
                # caso ele deseje alterar o email
                elif(resposta == 3):
                    cond = cond_alteracao('email')
                # caso ele deseje alterar a senha
                else:
                    # lê a senha atual, por segurança
                    while(True):
                        senha = getpass('Digite sua senha atual:\n')
                        senha = crip(senha)
                        if(senha == usuario[4]):
                            break
                        else:
                            print('Senha incorreta')

                    # pede a senho nova duas vezes
                    while(True):
                        nova = getpass('Digite uma nova senha:\n')
                        nova2 = getpass('Digite novamente:\n')

                        if(nova == nova2):
                            nova = crip(nova)
                            break
                        else:
                            print('Senhas não correspondem.')
                    cond = "usuario SET senha='{}'".format(nova)
                # executa a query
                alterar_cadastro(db, usuario[0], cond)
                print('Feito! Reinicie para aplicar alterações.')
            elif(opcao == 3):
                print('Volte sempre, {}'.format(nome_completo))
                break


def cond_alteracao(campo):
    # lê o novo email
    print('Digite o novo {}:'.format(campo))
    new = input()
    return "usuario SET {}='{}'".format(campo, new)


def get_nome(usuario):
    return ' '.join((usuario[1], usuario[2]))


def imprime_receitas(db, usuario, *argv):
    # retorna a lista de receitas
    if(len(argv) > 0):
        receitas = get_receitas(db, argv[0])
    else:
        receitas = get_receitas(db)

    print('\nLista de receitas:')
    # caso a lista esteja vazia, imprime uma mensagem informando
    if(len(receitas) == 0):
        print('Nenhuma receita encontrada\n')
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

            # busca avaliações
            q = "SELECT * FROM avaliacao WHERE id_receita={} ORDER BY id DESC;"
            q = q.format(receita[0])
            reviews = db.select(q)

            # checa se o usuario ja avaliou
            q = "SELECT COUNT(id) FROM avaliacao WHERE id_autor={}" \
                " AND id_receita={}".format(usuario, receita[0])
            review_user = (db.select(q))[0][0]

            # imprime informações da receita
            print('=======================')
            print('Nome: {}'.format(receita[1]))
            print('Categoria: {}'.format(receita[4]))
            print('Autor: {}'.format(autor[0] + ' ' + autor[1]))
            print('Nível do Autor: {}'.format(autor[2]))
            print('Avaliação Média: {}'.format(receita[2]))
            print('---')
            print('Última avaliação:')
            if(len(reviews) > 0):
                print('Nota: {}'.format(reviews[0][3]))
                print('Texto: {}'.format(reviews[0][4]))
            else:
                print('Nenhuma avaliação disponível')
            print('---')
            print('Ingredientes:')
            for ing in ingredientes:
                print('{} - {} {}'.format(ing[0], ing[1], ing[2]))
            print('\nModo de Preparo:')
            for n, passo in passos:
                print('{} - {}'.format(n, passo))
            print('=======================')

            # pergunta se o usuaŕio deseja avaliar a receita
            if(review_user == 0):
                print('Deseja avaliar essa receita?')
                resp = sim_ou_nao()
                if(resp == 1):
                    avaliar_receita(db, usuario, receita[0])
        print()


# avalia uma receita
def avaliar_receita(db, autor, rec):
    # lê uma nota de 1 à 5
    print('Digite uma nota: (de 1 à 5)')
    while(True):
        try:
            stars = int(input())
        except ValueError:
            stars = -1
        finally:
            if(stars >= 1 and stars <= 5):
                break
            print("Resposta inválida")

    print('Faça um comentário:')
    comment = input()

    # insere a avaliação na tabela
    q = "INSERT INTO avaliacao (id_autor,id_receita, num_estrelas, texto)" \
        " VALUES ({}, {}, {}, '{}');".format(autor, rec, stars, comment)
    db.execute_query(q)
    # busca a nova media de estrelas daquela receita
    q = "SELECT AVG(num_estrelas) FROM avaliacao" \
        " WHERE id_receita={}".format(rec)
    media = (db.select(q))[0][0]

    # atualiza a avaliacao media da receita
    q = "UPDATE receita SET avaliacao_media={} WHERE id={};".format(media, rec)
    db.execute_query(q)


if(__name__ == '__main__'):
    main()
