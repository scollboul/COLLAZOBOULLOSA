import unittest
import clients, conexion, var
from PyQt5 import QtSql

class MyTestCase(unittest.TestCase):

    def test_conexion(self):
        value=conexion.Conexion.db_connect(var.filebd)
        msg='Conexion no valida'
        self.assertTrue(value, msg)

    def test_dni(self):
        dni="00000000T"
        value=clients.Clientes.validarDni(str(dni))
        msg='Proba Erronea'
        self.assertTrue(value, msg)

    def test_fact(self):
        valor = 94.54
        codfact = 91
        try:
            msg = 'Calculos incorrectos'
            var.subfact = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfact')
            query.bindValue(':codfact', int(codfact))
            if query.exec_():
                while query.next():
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    query1.prepare('select producto, precio from productos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            precio = query1.value(1)
                            subtotal = round(float(cantidad) * float(precio), 2)
                    var.subfact = round(float(subtotal) + float(var.subfact), 2)
            var.iva = round(float(var.subfact) * 0.21, 2)
            var.fact = round(float(var.iva) + float(var.subfact), 2)
        except Exception as error:
            print('Error listado de la tabla ventas: %s' % str(error))
        self.assertEqual(round(float(valor), 2), round(float(var.fact), 2), msg)

    def test_venta(self):
        valor = 27.22
        codfact = 101
        codigoVenta=1082
        try:
            msg = 'Calculos incorrectos'
            var.subfact = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query2 = QtSql.QSqlQuery()
            query.prepare('delete from ventas where codventa = :codigoVenta')
            query.bindValue(':codigoVenta', int(codigoVenta))
            if query.exec_():
                print('Venta Eliminada')
            query1.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfact')
            query1.bindValue(':codfact', int(codfact))
            if query1.exec_():
                while query1.next():
                    codarticventa = query1.value(1)
                    cantidad = query1.value(2)
                    query2.prepare('select producto, precio from productos where codigo = :codarticventa')
                    query2.bindValue(':codarticventa', int(codarticventa))
                    if query2.exec_():
                        while query2.next():
                            precio = query2.value(1)
                            subtotal = round(float(cantidad) * float(precio), 2)
                    var.subfact = round(float(subtotal) + float(var.subfact), 2)
            var.iva = round(float(var.subfact) * 0.21, 2)
            var.fact = round(float(var.iva) + float(var.subfact), 2)
        except Exception as error:
            print('Error listado de la tabla ventas: %s' % str(error))
        self.assertEqual(round(float(valor), 2), round(float(var.fact), 2), msg)


if __name__ == '__main__':
    unittest.main()
