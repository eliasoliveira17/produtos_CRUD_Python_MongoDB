from bson import errors as berrors
from bson.objectid import ObjectId
from pymongo import MongoClient, errors


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = MongoClient('localhost', 27017)
    return conn

    # Não há necessidade de tratamento de excessões nesta etapa.
    # Neste caso, excessões acontecem na tentativa de utilização de conexão ativa

def desconectar(conn):
    """ 
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()


def listar():
    """
    Função para listar os produtos
    """
    conn = conectar()
    # 'pyMongo' é o nome do banco de dados a ser utilizado
    db = conn.pyMongo

    try:
        if db.produtos.count_documents({}) > 0:
            produtos = db.produtos.find()
            print('Listando produtos ...')
            print('---------------------')
            for produto in produtos:
                print(f"ID: {produto['_id']}")
                print(f"Produto: {produto['nome']}")
                print(f"Preço: {produto['preco']}")
                print(f"Estoque: {produto['estoque']}")
                print('---------------------')
        else:
            print("Não existem produtos a serem listados!")
    except errors.PyMongoError as e:
        print(f"Erro ao acessar o bando de dados: {e}")
    
    desconectar(conn)

def inserir():
    """
    Função para inserir um produto
    """  
    conn = conectar()
    # 'pyMongo' é o nome do banco de dados a ser utilizado
    db = conn.pyMongo

    nome = input("Informe o nome do produto: ")
    preco = float(input("Informe o preço do produto: "))
    estoque = int(input("Informe a quantidade de produtos em estoque: "))

    try:
        db.produtos.insert_one(
            {
                "nome": nome,
                "preco": preco,
                "estoque": estoque
            }
        )
        print(f"O produto {nome} foi adicionado na coleção com sucesso.")
    except errors.PyMongoError as e:
        print(f"Não foi possível inserir o produto. Erro: {e}")
    
    desconectar(conn)

def atualizar():
    """
    Função para atualizar um produto
    """
    conn = conectar()
    # 'pyMongo' é o nome do banco de dados a ser utilizado
    db = conn.pyMongo

    _id = input('Informe o ID do produto: ')
    nome = input('Informe o nome atualizado do produto: ')
    preco = float(input('Informe o preço atualizado do produto: '))
    estoque = int(input('Informe a quantidade atualizada de produtos em estoque: '))

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "nome": nome,
                        "preco": preco,
                        "estoque": estoque
                    }
                }
            )
            if res.modified_count == 1:
                print(f'O produto {nome} foi atualizado com sucesso')
            else:
                print('Não foi possível atualizar o produto')
        else:
            print('Não existem produtos a serem atualizados')
    except errors.PyMongoError as e:
        print(f'Não foi possível acessar o banco de dados. Erro: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido. Erro: {f}')

    desconectar(conn)

def deletar():
    """
    Função para deletar um produto
    """  
    conn = conectar()
    # 'pyMongo' é o nome do banco de dados a ser utilizado
    db = conn.pyMongo

    _id = input('Informe o ID do produto a ser deletado: ')

    try:
        if db.produtos.count_documents({}) > 0:
            res = db.produtos.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            
            if res.deleted_count > 0:
                print('O produto foi deletado com sucesso')
            else:
                print('O produto não foi deletado')
        else:
            print('Não existem produtos a serem deletados')
    except errors.PyMongoError as e:
        print(f'Não foi possível acessar o bando de dados. Erro: {e}')
    except berrors.InvalidId as f:
        print(f'ObjectId inválido. Erro: {f}')

    desconectar(conn)


def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
