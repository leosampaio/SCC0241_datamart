from django.db import models
from django.db import connection
from django.db import DatabaseError


class Cliente:

    def __init__(self):
        pass

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
            if item[3] is not None:
                choices.append((str(item[0]), ' '.join([str(item[2]), str(item[3]), str(item[4])])))
            else:
                choices.append((str(item[0]), ' '.join([str(item[2]), str(item[4])])))

        return choices


class Endereco():
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
            if item[2] is not None:
                choices.append((str(item[0]), ' - '.join([str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6])])))
            else:
                choices.append((str(item[0]), ' - '.join([str(item[1]), str(item[3]), str(item[4]), str(item[5]), str(item[6])])))

        return choices


class ClienteEndereco():
    pass


class Modelo():
    pass


class Categoria():
    pass


class Produto():
    pass


class Vendedor():
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
        }

        return dictionary


class Transportadora():
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


class Idioma():
    pass


class Descricao():
    pass


class Pedido():
    def __init__(self):
        pass

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
        # cursor.execute("SELECT P.codigo AS codigo, P.dtpedido AS dtpedido, P.valorbruto AS total, (C.primeiroNome || ' ' || C.nomedoMeio || ' ' || C.sobrenome) as nome FROM Pedido P INNER JOIN Cliente C ON C.codigo = P.codigocliente ORDER BY C.primeironome ASC;")
        cursor.execute("SELECT P.codigo AS codigo, P.dtpedido AS dtpedido, P.valorbruto AS total, C.primeironome AS nome FROM Pedido P, Cliente C WHERE C.codigo = P.codigocliente ORDER BY C.primeironome ASC")
        '''https://docs.djangoproject.com/en/1.8/topics/db/sql/#executing-custom-sql-directly'''  # noqa
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class DetalhesPedido():
    pass
