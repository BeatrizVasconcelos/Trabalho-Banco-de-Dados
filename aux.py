from getpass import getpass
from cripto import crip


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

        # caso o usuario seja um autor, busca pela tupla correspondente
        if(tuplas[0][5] == 'Autor'):
            # executa query para buscar email digitado
            q = "SELECT * FROM autor WHERE email='{}';".format(email)
            tuplas = db.select(q)  # lista de tuplas

        # usuario
        usuario = tuplas[0]

        # lê a senha do usuário
        senha = getpass('Digite sua senha:\n')
        senha = crip(senha)

        # checa se a senha foi digitada corretamente
        # caso sim, retorna uma lista com as funções do usuario
        if(senha == usuario[4]):
            print('Logado com sucesso.')
            return usuario
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
        senha = getpass('Digite uma senha:\n')
        senha2 = getpass('Digite novamente:\n')

        if(senha == senha2):
            senha = crip(senha)
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
    q = "INSERT INTO autor" \
        " (nome, sobrenome, email, senha, permissao, tipo_autor)" \
        " VALUES ('{}', '{}', '{}', '{}', 'Autor', '{}');"
    q = q.format(nome, sobrenome, email, senha, tipo)

    # executa a query
    db.execute_query(q)

    # query para buscar o usuario inserido
    q = "SELECT * FROM autor WHERE email='{}';".format(email)
    tuplas = db.select(q)

    # retorna o usuario cadastrado
    return tuplas[0]


# busca as receitas
def get_receitas(db, *argv):
    # query basica para buscar receitas
    q = "SELECT * FROM Receita"
    # caso seja passado um argumento adicional,
    # adiciona na query
    if(len(argv) > 0):
        q += argv[0]

    # adicionada condição para ordenar por avaliacao_media
    # do maior para o menor
    q += " ORDER BY avaliacao_media DESC;"

    return db.select(q)


# função para inserir uma receita
def insere_receita(db, id_autor):
    meds = ('kg', 'g', 'colher de chá', 'colher de sopa', 'l', 'ml', 'unidade')
    cats = ('Lanche', 'Acompanhamento',
            'Prato Principal', 'Sobremesa', 'Entrada')
    # lê o nome da receita
    print('Digite o nome da receita:')
    nome = input()

    # lê a categoria da receita
    print('Digite a categoria:')
    print(cats)
    while(True):
        categoria = input()
        if(categoria in cats):
            break
        print('Digite uma categoria válida')

    # lê os ingredientes
    print('Digite os ingredientes:')
    ingredientes = []
    qtdes = []

    while(True):
        # lê o nome do ingrediente
        print('Qual ingrediente você deseja adicionar?')
        ingrediente = input()
        # busca pelo ingrediente
        q = "SELECT * FROM ingrediente WHERE nome='{}';".format(ingrediente)
        tuplas = db.select(q)
        # caso encontre o ingrediente
        if(len(tuplas) > 0):
            # adiciona o id do ingrediente na lista
            ingredientes.append(tuplas[0][0])
        # caso não encontre o ingrediente
        else:
            # insere o ingrediente na tabela
            q = "INSERT INTO ingrediente (nome)" \
                " VALUES ('{}');".format(ingrediente)
            db.execute_query(q)

            # busca pelo ingrediente inserido
            q = "SELECT * FROM ingrediente" \
                " WHERE nome='{}';".format(ingrediente)
            tuplas = db.select(q)
            # adiciona o id do ingrediente na lista
            ingredientes.append(tuplas[0][0])

        # lê a quantidade de cada ingrediente
        print('Digite a quantidade:')
        while(True):
            try:
                resp1 = float(input())
            except ValueError:
                resp1 = None
            finally:
                if(resp1):
                    break
                print('Valor inválido')

        # lê a medida de cada ingrediente
        print('Digite a unidade de medida:')
        print(meds)
        while(True):
            try:
                resp2 = input()
            except ValueError:
                resp2 = None
            finally:
                if(resp2 in meds):
                    break
                print('Valor inválido')

        # adiciona na lista de quantidades
        qtdes.append((resp1, resp2))

        # lê do usuario se ele deseja inserir ou não outro ingrediente
        print('Deseja adicionar outro ingrediente?')
        resposta = sim_ou_nao()

        # sai do while caso a resposta seja 2
        if(resposta == 2):
            break

    # query para inserir na tabela receita
    q1 = "INSERT INTO receita (nome, id_autor, categoria)" \
        " VALUES ('{}', {}, '{}');".format(nome, id_autor, categoria)
    # insere na tabela receita
    db.execute_query(q1)

    # recupera o id da receita inserida
    q = "SELECT id FROM receita WHERE id_autor='{}' ORDER BY id DESC;"
    q = q.format(id_autor)
    id_rec = (db.select(q))[0][0]
    # insere na tabela Utilizado_em
    for i in range(len(ingredientes)):
        q2 = "INSERT INTO utilizado_em (id_receita, id_ingrediente, " \
            "quantidade, medida) VALUES ({}, {}, {}, '{}');"
        q2 = q2.format(id_rec, ingredientes[i], qtdes[i][0], qtdes[i][1])
        db.execute_query(q2)

    # modo de preparo
    print('Digite o modo de preparo:')
    num_passo = 0
    while(True):
        num_passo += 1
        print('Digite o {}º passo:'.format(num_passo))
        passo = input()
        q3 = "INSERT INTO preparo VALUES ({}, {}, '{}');"
        q3 = q3.format(id_rec, num_passo, passo)
        db.execute_query(q3)

        # continua ou não
        print('Deseja adicionar mais um passo?')
        resposta = sim_ou_nao()

        # sai do while
        if(resposta == 2):
            break

    # print fim
    print('Receita cadastrada!')


# lê do usuario uma resposta entre sim e não
def sim_ou_nao():
    print('(1) - Sim')
    print('(2) - Não')
    while(True):
        try:
            resposta = int(input())
        except ValueError:
            resposta = -1
        finally:
            if(resposta in (1, 2)):
                return resposta
            print('Resposta inválida')


# altera os dados do usuario
def alterar_cadastro(db, user, cond):
    # altera o usuario
    q = "UPDATE {} WHERE id={};".format(cond, user)
    db.execute_query(q)


# altera receitas
def editar_receita(db, tbs, opc, rec):
    q1 = "UPDATE "
    q2 = "INSERT INTO "
    q3 = "DELETE FROM "
    # alterar dados da receita
    if(len(tbs) == 1):
        q = q1 + "{} SET {} = '{}' WHERE id={};"
        # alterar nome
        if(opc == 1):
            print('Digite o novo nome da receita:')
            campo = 'nome'
            novo = input()
        # alterar categoria
        else:
            campo = 'categoria'
            cats = ('Lanche', 'Acompanhamento',
                    'Prato Principal', 'Sobremesa', 'Entrada')
            print('Digite a nova categoria da receita:')
            print(cats)
            while(True):
                try:
                    novo = input()
                except ValueError:
                    novo = ''
                finally:
                    if(novo in cats):
                        break
                    print('Digite uma opção válida')
        # possui todas as informações para completar a query
        q = q.format(tbs[0], campo, novo, rec)
    # alterar modo de preparo
    elif(len(tbs) == 2):
        # adicionar passo
        if(opc == 1):
            q = q2 + "{} (id_receita, num_passo, passo) " \
                "VALUES ({}, {}, '{}');"
            print('Informe o novo passo:')
            novo = input()
            # query para buscar o numero de passos
            temp = "SELECT COUNT(num_passo) FROM preparo WHERE id_receita={};"
            temp = temp.format(rec)
            # numero do novo passo
            num = (db.select(temp))[0][0] + 1
            q = q.format(tbs[0], rec, num, novo)
        # remover o ultimo passo
        elif(opc == 2):
            q = q3 + "{} WHERE id_receita={} AND num_passo IN " \
                "(SELECT MAX(num_passo) FROM {} WHERE id_receita={});"
            q = q.format(rec, tbs[0], rec)
        # editar passo
        else:
            # recupera a lista de passos da receita
            temp = "SELECT * FROM preparo WHERE id_receita={}".format(rec)
            passos = db.select(temp)
            # percorre a lista de passos
            for passo in passos:
                print(passo[2])
                print('Deseja alterar este passo?')
                resp = sim_ou_nao()
                # caso o usuario deseje alterar
                if(resp == 1):
                    print('Digite o novo passo:')
                    novo = input()
                    q = q1 + "{} SET passo='{}' WHERE id_receita={}" \
                        "AND num_passo={};".format(tbs[0], novo, rec, passo[1])
                    db.execute_query(q)
                    return True
    # alterar ingredientes
    elif(len(tbs) == 3):
        # add ingrediente
        if(opc == 1):
            meds = ('kg', 'g', 'colher de chá', 'colher de sopa', 'l',
                    'ml', 'unidade')
            # lê o nome do ingrediente
            print('Qual ingrediente você deseja adicionar?')
            novo = input()
            # busca pelo ingrediente
            q = "SELECT * FROM utilizado_em WHERE nome='{}';".format(novo)
            ingredientes = db.select(q)
            # caso encontre o ingrediente
            if(len(ingredientes) > 0):
                i = ingredientes[0][0]
            # caso não encontre
            else:
                # insere o ingrediente
                temp = q2 + "{} (nome) VALUES ('{}')".format(tbs[2], novo)
                db.execute_query(temp)
                # busca pelo ingrediente inserido
                i = (db.select(q))[0][0]

            # lê a quantidade de cada ingrediente
            print('Digite a quantidade:')
            while(True):
                try:
                    qtd = float(input())
                except ValueError:
                    qtd = None
                finally:
                    if(qtd):
                        break
                    print('Valor inválido')

            # lê a medida de cada ingrediente
            print('Digite a unidade de medida:')
            print(meds)
            while(True):
                try:
                    med = input()
                except ValueError:
                    med = None
                finally:
                    if(med in meds):
                        break
                    print('Valor inválido')
            # query para inserir em utilizado_em
            q = q2 + " (id_receita, id_ingrediente, quantidade, medida) " \
                "VALUES ({}, {}, {}, '{}');"
            q = q.format(rec, i, qtd, med)
        # remover ingrediente
        elif(opc == 2):
            print('Qual ingrediente você deseja remover?')
            while(True):
                ing = input()
                # busca pelo ingrediente
                q = "SELECT id_ingrediente FROM ingrediente INNER JOIN " \
                    "utilizado_em ON id_ingrediente=id WHERE nome='{} " \
                    "AND id_receita={}';".format(ing, rec)
                ingredientes = db.select(q)
                # caso encontre o ingrediente
                if(len(ingredientes) > 0):
                    i = ingredientes[0][0]
                    break
                else:
                    print('Ingrediente não utilizado')
            q = q3 + "{} WHERE id_receita={} AND id_ingrediente={};"
            q = q.format(tbs[1], rec, i)
        # alterar medida
        else:
            q = "SELECT nome, quantidade, medida, id FROM ingrediente " \
                "INNER JOIN utilizado_em ON id=id_ingrediente WHERE " \
                "id_receita={} ORDER BY nome;".format(rec)
            utilizados = db.select(q)
            for ing in utilizados:
                print('{} - {} {}'.format(ing[0], ing[1], ing[2]))
                print('Deseja alterar a medida desse ingrediente?')
                resp = sim_ou_nao()
                # caso sim, lê a nova quantidade
                if(resp == 1):
                    print('Digite um novo valor:')
                    while(True):
                        try:
                            qtd = float(input())
                        except ValueError:
                            qtd = None
                        finally:
                            if(qtd):
                                break
                            print('Valor inválido')
                    # query para alterar quantidade
                    q = q1 + "{} SET quantidade={} WHERE id_receita={} AND " \
                        "id_ingrediente={};".format(tbs[1], qtd, rec, ing[3])
                    db.execute_query(q)
                    return True
    else:
        return None
    db.execute_query(q)
    return True
