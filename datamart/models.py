from django.db import connection
from django.db import DatabaseError
from .decorators import autoassign


# Join if not None
def joinnn(char, lista):
    items = [x for x in lista if x is not None]
    return char.join(items)


class Session():
    @staticmethod
    def set_login(user_cod):
        if user_cod is None:
            return False

        cursor = connection.cursor()
        query = "DELETE FROM logadoagora"
        cursor.execute(query)

        query = ''.join(["INSERT INTO logadoagora VALUES (", user_cod, ')'])
        cursor.execute(query)
        return True

    @staticmethod
    def get_login():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM logadoagora")
        return cursor.fetchall()[0][0]


class Base:
    def get_code(self):
        cursor = connection.cursor()
        query = "SELECT MAX(codigo) FROM {}".format(self.__class__.__name__)
        cursor.execute(query)
        current = cursor.fetchall()[0][0]
        return current + 1

    @staticmethod
    def delete(self, codigo):
        cursor = connection.cursor()
        query = "DELETE FROM {}\
            WHERE codigo=\'{}\'".format(self.__class__.__name__, codigo)
        cursor.execute(query)


class Cliente(Base):

    @autoassign
    def __init__(self, sufixo, nomedomeio, primeironome, sobrenome, senha, tratamento):
        self.codigo = self.get_code()

    def save(self):
        cursor = connection.cursor()
        query = "INSERT INTO Cliente (\
                codigo, sufixo, nomedomeio, primeironome, sobrenome, senha, tratamento\
            )\
            VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')".format(
                self.codigo, self.sufixo, self.nomedomeio, self.primeironome, self.sobrenome, self.senha, self.tratamento
            )
        print(query)
        cursor.execute(query)

    @staticmethod
    def all():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Cliente")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM Cliente WHERE codigo = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        query = Cliente.get_by_id(id)
        query = list(query)[0]
        dictionary = {
            'CODIGO': query[0],
            'TRATAMENTO': query[1],
            'PRIMEIRONOME': query[2],
            'NOMEDOMEIO': query[3],
            'SOBRENOME': query[4],
            'SUFIXO': query[5],
            'SENHA': query[6],
            'NOMECONCATENADO': joinnn(' ', query[2:6]),
        }

        return dictionary

    @staticmethod
    def get_all_as_choice():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Cliente ORDER BY primeironome ASC, nomedomeio ASC, sobrenome ASC")
        query = cursor.fetchall()
        query = list(query)
        choices = []
        for item in query:
            choices.append((str(item[0]), joinnn(' ', item[2:6])))

        return choices


class Endereco(Base):

    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM Endereco WHERE id = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        query = Endereco.get_by_id(id)
        query = list(query)[0]
        dictionary = {
            'ID': query[0],
            'LOGRADOURO': query[1],
            'COMPLEMENTO': query[2],
            'CIDADE': query[3],
            'ESTADO': query[4],
            'PAIS': query[5],
            'CODIGOPOSTAL': query[6],
            'ENDERECOCONCATENADO': joinnn(' - ', query[1:7]),
        }

        return dictionary

    @staticmethod
    def get_all_as_choice():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Endereco")
        query = cursor.fetchall()
        query = list(query)
        choices = []
        for item in query:
            choices.append((str(item[0]), joinnn(' - ', item[1:7])))

        return choices


class ClienteEndereco(Base):

    @autoassign
    def __init__(self, cliente_codigo, endereco, tipoendereco):
        pass

    def save(self):
        cursor = connection.cursor()
        query = "INSERT INTO ClienteEndereco (\
                codigocliente, idendereco, tipoendereco\
            )\
            VALUES (\'{}\', \'{}\', \'{}\')".format(
                self.cliente_codigo, self.endereco, self.tipoendereco
            )
        print(query)
        cursor.execute(query)

    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM ClienteEndereco WHERE codigoCliente = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        querylist = ClienteEndereco.get_by_id(id)
        querylist = list(querylist)
        detalhes = []

        for query in querylist:
            detalhes.append({
                'CODIGOCLIENTE': query[0],
                'IDENDERECO': Endereco.get_by_id_as_dict(query[1]),
                'TIPOENDERECO': query[2],
            })

        return detalhes


class Produto(Base):
    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM Produto WHERE codigo = \'", str(id), "\' ORDER BY nome ASC"]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        query = Produto.get_by_id(id)
        query = list(query)[0]

        dictionary = {
            'CODIGO': query[0],
            'NOME': query[1],
            'COR': query[2],
            'CUSTOPRODUCAO': query[3],
            'PRECO': query[4],
            'TAMANHO': query[5],
            'PESO': query[6],
            'CODIGOCATEGORIA': query[7],
            'CODIGOMODELO': query[8],
            'DTINICIOVENDA': query[9],
            'DTFIMVENDA': query[10],
            # 'NOMECONCATENADO': joinnn(' ', [query[1:3], query[5]])
            'NOMECONCATENADO': joinnn(' ', (query[1], query[2], query[5]))
        }

        return dictionary

    @staticmethod
    def get_all_as_choice():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Produto ORDER BY nome ASC")
        query = cursor.fetchall()
        query = list(query)
        choices = []
        for item in query:
            choices.append((str(item[0]), joinnn(' ', [item[1], item[2], item[5]])))
        return choices

    @staticmethod
    def get_all_as_pricelist():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Produto ORDER BY nome ASC")
        query = cursor.fetchall()
        query = list(query)
        choices = []
        for item in query:
            choices.append((str(item[0]), float(item[4])))
        return choices


class Vendedor(Base):

    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM Vendedor WHERE codigo = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        query = Vendedor.get_by_id(id)
        query = list(query)[0]
        dictionary = {
            'CODIGO': query[0],
            'PRIMEIRONOME': query[1],
            'NOMEDOMEIO': query[2],
            'SOBRENOME': query[3],
            'SENHA': query[4],
            'DTNASCIMENTO': query[5],
            'DTCONTRATACAO': query[6],
            'SEXO': query[7],
            'QUOTA': query[8],
            'BONUS': query[9],
            'COMISSAO': query[10],
            'NOMECONCATENADO': joinnn(' ', query[1:4])
        }

        return dictionary

    @staticmethod
    def get_all_as_choice():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Vendedor ORDER BY primeironome")
        query = cursor.fetchall()
        query = list(query)
        choices = []
        for item in query:
            choices.append((str(item[0]), joinnn(' ', item[1:4])))
        return choices


class Transportadora(Base):
    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM Transportadora WHERE codigo = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        query = Transportadora.get_by_id(id)
        query = list(query)[0]
        dictionary = {
            'CODIGO': query[0],
            'NOME': query[1],
            'TAXABASE': query[2],
            'TAXAENVIO': query[3],
        }

        return dictionary

    @staticmethod
    def get_all_as_choice():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Transportadora")
        query = cursor.fetchall()
        query = list(query)
        choices = []
        for item in query:
            choices.append((str(item[0]), str(item[1])))
        return choices


class Pedido(Base):

    @autoassign
    def __init__(
        self,
        codigocliente,
        dtenvio,
        enderecoentrega,
        dtpedido,
        contacliente,
        codigotransportadora,
        enderecofatura,
        imposto,
        dtrecebimento,
        numerocartaocredito):
        self.codigo = self.get_code()

    def save(self):
        cursor = connection.cursor()
        vendedor = Session.get_login()
        query = "INSERT INTO Pedido (\
                codigo, \
                codigocliente, \
                dtenvio, \
                enderecoentrega, \
                dtpedido, \
                contacliente, \
                codigotransportadora, \
                enderecofatura, \
                imposto, \
                dtrecebimento, \
                numerocartaocredito, \
                codigovendedor\
            )\
            VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')".format(
                self.codigo,
                self.codigocliente,
                self.dtenvio.strftime('%Y-%m-%d'),
                self.enderecoentrega,
                self.dtpedido.strftime('%Y-%m-%d'),
                self.contacliente,
                self.codigotransportadora,
                self.enderecofatura,
                self.imposto,
                self.dtrecebimento.strftime('%Y-%m-%d'),
                self.numerocartaocredito,
                vendedor,
            )
        print(query)
        cursor.execute(query)

    def update(self):
        cursor = connection.cursor()
        query = "UPDATE Pedido SET\
                codigocliente=\'{}\', \
                dtenvio=\'{}\', \
                enderecoentrega=\'{}\', \
                dtpedido=\'{}\', \
                contacliente=\'{}\', \
                codigotransportadora=\'{}\', \
                enderecofatura=\'{}\', \
                imposto=\'{}\', \
                dtrecebimento=\'{}\', \
                numerocartaocredito=\'{}\'\
                WHERE codigo=\'{}\'".format(
                self.codigocliente,
                self.dtenvio.strftime('%Y-%m-%d'),
                self.enderecoentrega,
                self.dtpedido.strftime('%Y-%m-%d'),
                self.contacliente,
                self.codigotransportadora,
                self.enderecofatura,
                self.imposto,
                self.dtrecebimento.strftime('%Y-%m-%d'),
                self.numerocartaocredito,
                self.codigo
            )
        print(query)
        cursor.execute(query)

    @staticmethod
    def delete(codigo):
        cursor = connection.cursor()
        query = "DELETE FROM Pedido\
            WHERE codigo=\'{}\'".format(codigo)
        cursor.execute(query)

    @staticmethod
    def all():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Pedido")
        return cursor.fetchall()

    def _cursor():
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Pedido")
        return cursor

    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM Pedido WHERE codigo = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        query = Pedido.get_by_id(id)
        query = list(query)[0]
        dictionary = {
            'CODIGO': query[0],
            'DTPEDIDO': query[1],
            'DTENVIO': query[2],
            'DTRECEBIMENTO': query[3],
            'CODIGOCLIENTE': query[4],
            'CONTACLIENTE': query[5],
            'NUMEROCARTAOCREDITO': query[6],
            'CODIGOCONFIRMACAO': query[7],
            'CODIGOVENDEDOR': query[8],
            'IMPOSTO': query[9],
            'ENDERECOFATURA': query[10],
            'ENDERECOENTREGA': query[11],
            'CODIGOTRANSPORTADORA': query[12],
        }

        dictionary['CODIGOCLIENTE'] = Cliente.get_by_id_as_dict(dictionary['CODIGOCLIENTE'])
        try:
            dictionary['CODIGOVENDEDOR'] = Vendedor.get_by_id_as_dict(dictionary['CODIGOVENDEDOR'])
        except DatabaseError:
            dictionary['CODIGOVENDEDOR'] = None
        dictionary['ENDERECOFATURA'] = Endereco.get_by_id_as_dict(dictionary['ENDERECOFATURA'])
        dictionary['ENDERECOENTREGA'] = Endereco.get_by_id_as_dict(dictionary['ENDERECOENTREGA'])
        dictionary['CODIGOTRANSPORTADORA'] = Transportadora.get_by_id_as_dict(dictionary['CODIGOTRANSPORTADORA'])
        return dictionary

    @staticmethod
    def dictfetchall():
        cursor = connection.cursor()
        cursor.execute("SELECT P.codigo AS codigo, P.dtpedido AS dtpedido, P.valorbruto AS total, (C.primeiroNome || ' ' || C.nomedoMeio || ' ' || C.sobrenome) as nome FROM Pedido P INNER JOIN Cliente C ON C.codigo = P.codigocliente RIGHT JOIN logadoagora L ON P.codigovendedor = L.codigo ORDER BY C.primeironome ASC;")
        '''https://docs.djangoproject.com/en/1.8/topics/db/sql/#executing-custom-sql-directly'''  # noqa
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class DetalhesPedido(Base):

    @autoassign
    def __init__(
            self,
            codigopedido,
            quantidade,
            codigoproduto,
            desconto):
        cursor = connection.cursor()
        cursor.execute("SELECT preco FROM Produto WHERE codigo=\'{}\'".format(codigoproduto))
        self.precounitario = cursor.fetchall()[0][0]

    def save(self):
        cursor = connection.cursor()
        query = "INSERT INTO DetalhesPedido (\
                codigopedido, \
                quantidade, \
                codigoproduto, \
                desconto, \
                precounitario \
            )\
            VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\')".format(
                self.codigopedido,
                self.quantidade,
                self.codigoproduto,
                self.desconto,
                self.precounitario
            )
        print(query)
        cursor.execute(query)

    def update(self, novo_produto):
        cursor = connection.cursor()
        query = "UPDATE DetalhesPedido SET\
                quantidade=\'{}\', \
                desconto=\'{}\', \
                precounitario=\'{}\', \
                codigoproduto=\'{}\' \
                WHERE codigoproduto=\'{}\' AND codigopedido=\'{}\'".format(
                self.quantidade,
                self.desconto,
                self.precounitario,
                novo_produto,
                self.codigoproduto,
                self.codigopedido
            )
        print(query)
        cursor.execute(query)

    @staticmethod
    def get_by_id(id):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM DetalhesPedido WHERE codigoPedido = ", str(id)]))
        return cursor.fetchall()

    @staticmethod
    def get_by_pk(venda, produto):
        cursor = connection.cursor()
        cursor.execute(''.join(["SELECT * FROM DetalhesPedido WHERE codigoPedido = ", str(venda), " AND codigoProduto = \'", str(produto), "\'"]))
        return cursor.fetchall()

    @staticmethod
    def get_by_id_as_dict(id):
        querylist = DetalhesPedido.get_by_id(id)
        querylist = list(querylist)
        detalhes = []

        for query in querylist:
            detalhes.append({
                'CODIGOPEDIDO': query[0],
                'CODIGOPRODUTO': Produto.get_by_id_as_dict(query[1]),
                'QUANTIDADE': query[2],
                'PRECOUNITARIO': query[3],
                'DESCONTO': query[4],
                'TOTAL': float(query[3]) * int(query[2]) * (1 - float(query[4])),
            })

        return detalhes

    @staticmethod
    def get_by_pk_as_dict(venda_pk, produto_codigo):
        query = DetalhesPedido.get_by_pk(venda_pk, produto_codigo)
        query = list(query)[0]
        dictionary = {
            'CODIGOPEDIDO': query[0],
            'CODIGOPRODUTO': Produto.get_by_id_as_dict(query[1]),
            'QUANTIDADE': query[2],
            'PRECOUNITARIO': query[3],
            'DESCONTO': query[4],
            'TOTAL': float(query[3]) * int(query[2]) * (1 - float(query[4])),
        }

        return dictionary
