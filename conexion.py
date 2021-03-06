from PyQt5 import QtWidgets, QtSql
import var
import ventas
from ventana import *


class Conexion():
    def db_connect(filename):
        """

        Modulo que realiza la conexión de la aplicacion con la BBDD

        :param filename: nombre de la BBDD
        :type: string
        :return: True o false
        :rtype: bool

        Utiliza la libreria de QtSql y el gestor de la BDDD es QSQLite. En caso de que no se conecta
        mustra pantalla de aviso. Se lanza al lazanzarse el programa.

        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(filename))
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer conexion.\n'
                                           'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True

    def altaCli(cliente):
        """

        Modulo que da de alta un cliente cuyos datos se pasan a traves de una lista.

        :param: cliente
        :type: lista
        :return: None
        :rtype: None

        Muestra mensaje de resultado en la barra de estado.
        Recarga la tabla actulizada de clientes llamdiço al modulo Conexion.mostrarClientes()
        Se insterta en el ordeb de la base de datos

        """

        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago, edad)'
            'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')

        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', int(cliente[8]))
        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Alta Cliente con dni ' + str(cliente[0]))
            Conexion.mostrarClientes()
        else:
            print("Error: ", query.lastError().text())

    def cargarCliente():
        """

        Muestra los datos del cliente cargados en los widgets del formulario al clickar sobre la tabla

        :return:
        :rtype:

        """

        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.editClialta.setText(query.value(4))
                var.ui.editDir.setText(query.value(5))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(int(query.value(9)))

    def mostrarClientes():
        """
        Modulo que carga los datos del cliente en la tablaCli por orden alfabetico

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes order by apellidos, nombre')
        if query.exec_():
            while query.next():
                # cojo los valores
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                # crea la fila
                var.ui.tableCli.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def bajaCli(dni):
        """
        Modulo que dar de baja un cliente recibiendo como parametro el dni del Ciente a
        eliminar.

        :param dni
        :type string
        :return: None
        :rtype: None

        Muestra un mensaje en la barra de estado y recarga la TablaCli con los cliente actualizados

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def modifCli(codigo, newdata):
        """

        Modulo que actualiza los datos del cliente

        :param codigo: codigo del cliente
        :type codigo: int
        :param newdata: Lista de datos del cliente
        :type newdata: lista
        :return: None
        :rtype: None

        Recibe como parametro el codigo del cliente a modificar y los datos que queremos modifiar
        en forma de lista. En realidad toma los datos que hay en los widgets.

        """
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, formaspago=:formaspago, edad=:edad where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formaspago', str(newdata[7]))
        query.bindValue(':edad', int(newdata[8]))
        if query.exec_():
            var.ui.lblstatus.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar cliente: ", query.lastError().text())
        Conexion.mostrarClientes()

    def buscaCli(dni):
        """
        :return:
        :rtype:
        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.editApel.setText(str(query.value(1)))
                var.ui.editNome.setText(str(query.value(2)))
                var.ui.editClialta.setText(query.value(4))
                var.ui.editDir.setText(query.value(5))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                   var.ui.rbtFem.setChecked(True)
                   var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(query.value(9))

                var.ui.tableCli.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))

    '''
    Gestion de articulos
    '''

    def altaProducto(producto):
        """
        Da de alta un producto cuyos datos son pasados por una lista.

        :param: producto
        :type: lista
        :return: None
        :rtype: None

        Muestra un mensaje en la barra de estrado
        Recarga la tablaProd actualizada llamando al modulo  Conexion.mostrarProducts()

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into productos (producto, precio, stock)'
            'VALUES (:producto, :precio, :stock)')
        query.bindValue(':producto', str(producto[0]))
        query.bindValue(':precio', round(float(producto[1]), 2))
        query.bindValue(':stock', int(producto[2]))
        if query.exec_():
            var.ui.lblstatus.setText('Alta de producto  ' + str(producto[0]))
        else:
            print("Erro"+query.lastError().text())
        Conexion.mostrarProducts()

    def mostrarProducts():
        """

        Modulo que carga los datos de la informacion en la TablaProd en orden alfabetico

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, producto, precio from productos order by producto')
        if query.exec_():
            while query.next():
                codigo = query.value(0)
                producto = query.value(1)
                precio = query.value(2)
                var.ui.tableProd.setRowCount(index + 1)
                var.ui.tableProd.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tableProd.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                var.ui.tableProd.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                index += 1
        else:
            print("Error mostrar productos"": ", query.lastError().text())

    def cargarProd(cod):
        """

        Muestra los datos del producto en los widgets cuando se clicka en la tabla sobre el

        :param cod: código del producto
        :type cod: entero
        :return: None
        :rtype: None

        """

        query = QtSql.QSqlQuery()
        query.prepare('select producto, precio, stock from productos where codigo = :cod')
        query.bindValue(':cod', cod)
        if query.exec_():
            while query.next():
                var.ui.lblProd.setText(str(cod))
                var.ui.editNomeProducto.setText(str(query.value(0)))
                var.ui.EditPrecio.setText(str(query.value(1)))
                var.ui.EditStock.setText(str(query.value(2)))

    def BajaProducto(codigo):
        """

        Modulo que da de baja un producto pasandole el codigo de dicho producto

        :param cod
        :type: int
        :return None
        :rtype None

        Recarga la tablaProd actualizada y muestra un mensaje en la barra de estado

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from productos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            var.ui.lblstatus.setText('Baja del producto con el codigo ' + codigo )
        else:
            print("Error eliminar Producto: ", query.lastError().text())
        Conexion.mostrarProducts()

    def ModificarProducto(codigo, newprod):
        """

        Modulo que actualiza los productos

        :param newprod:
        :type newprod:
        :return:
        :rtype:

        Recibe como parametros el codigo del producto a modificar y como los datos que
        deseamos modificar en forma de lista.
        En realidad tomo los valores que hay en los widgets de la pantlla productos.
        Muestra estadi en la barra de estado

        """
        query = QtSql.QSqlQuery()
        codigo = codigo
        query.prepare('update productos set producto=:producto, precio=:precio, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', codigo)
        query.bindValue(':producto', str(newprod[0]))
        newprod[1] = newprod[1].replace(',', '.')
        query.bindValue(':precio', round(float(newprod[1]), 2))
        query.bindValue(':stock', str(newprod[2]))
        if query.exec_():
            var.ui.lblstatus.setText('Modificado el producto con el codigo ' + codigo )
        else:
            print("Error al modificar el Producto",+query.lastError().text())

    """
    Gestion de factura
    """

    def altaFactura(factura):
        """

        Modulo que da de alta una factura previa al proceso de venta

        :param factura: los datos de la factura
        :type factura: lista
        :return:
        :rtype:

        Recibe los datos para insetar en la factura en la  BBDD. Obtiene el codigo de la factura
        para cargar en la label lblFact.
        Recarga la tabla tabFechaFact con las facturas actualizadas.

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into facturas (dni, fecha, apellidos)'
            'VALUES (:dni, :fecha, :apellidos)')
        query.bindValue(':dni', str(factura[0]))
        query.bindValue(':fecha', str(factura[1]))
        query.bindValue(':apellidos', str(factura[2]))
        if query.exec_():
            var.ui.lblstatus.setText('Alta factura del cliente con el DNI ' + str(factura[0]))
        else:
            print("Erro"+query.lastError().text())
        query1=QtSql.QSqlQuery()
        query1.prepare("select max(codfac) from facturas")
        if query1.exec_():
            while query1.next():
                var.ui.lblFactura.setText(str(query.value(0)))
        Conexion.mostrarFacturas()

    def mostrarFacturas():
        """

        Modulo que carga los datos de las facturas en la tabla tabFechaFact
        por orden numerico descenciente

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas order by codfac desc')
        if query.exec_():
            while query.next():
                # cojo los valores
                codigo = query.value(0)
                fecha = query.value(1)
                # crea la fila
                var.ui.tableFechaFact.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableFechaFact.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tableFechaFact.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            ventas.Ventas.PrepararVentas(0)
        else:
            print("Error mostrar Facturas"": ", query.lastError().text())

    def cargarFact(cod):
        """

        Modulo que carga los datos de la factura clickada en los widgets del panel de
        facturacion

        :param cod: codigo de la factura
        :type cod: int
        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('select dni, fecha, apellidos from facturas where codfac = :cod')
        query.bindValue(':cod', cod)
        if query.exec_():
            while query.next():
                var.ui.lblFactura.setText(str(cod))
                var.ui.EditDNICli.setText(str(query.value(0)))
                var.ui.EditFechaFact.setText(str(query.value(1)))
                var.ui.EditApelCli.setText(str(query.value(2)))

    def BajaFactura(codigo):
        ''''
        modulo para eliminar cliente. se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where codfac = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            var.ui.lblstatus.setText('Baja de la factura con el codigo: ' + codigo)
        else:
            print("Error eliminar factura: ", query.lastError().text())
        ventas.Ventas.mostrarVentas()
        var.ui.lblSubtotal.setText('0.00')
        var.ui.lblIva.setText('0.00')
        var.ui.lblTotal.setText('0.00')

    def BuscarfactCli(dni):
        """

        Modulo que busca las facturas del cliente segun el dni pasado como parametro.
        En caso de que no tenga muestra mensaje en la barra de estado

        :param dni: dni del cliente a buscar
        :tupe dni: string
        :return:
        :rtype:

        """
        index = 0
        cont = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas where dni = :dni order by codfac desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                # cojo los valores
                cont = cont + 1
                codfac = query.value(0)
                fecha = query.value(1)
                # crea la fila
                var.ui.tableFechaFact.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableFechaFact.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.tableFechaFact.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            if cont == 0:
                var.ui.tableFechaFact.setRowCount(0)
                var.ui.lblstatus.setText('Cliente sin Facturas')
        else:
            print("Error mostrar facturas cliente: ", query.lastError().text())

    def altaVenta():
        """

        Modulo que da de alta una venta añadiendo lineas en una factura ya creada

        :return: None
        :rtype: None

        Inserta una nueva linea que se va mostrando cada vez que se hace una venta
        Tras realizar la venta se crea una nueva linea cargando el combobox en la seccion de
        articulos

        """
        query=QtSql.QSqlQuery()
        query.prepare('insert into ventas(codfacventa, codarticventa, cantidad, precio)'
                      'VALUES(:codfacventa, :codarticventa, :cantidad, :precio)')
        query.bindValue(':codfacventa', int(var.venta[0]))
        query.bindValue(':codarticventa', int(var.venta[1]))
        query.bindValue(':cantidad', int(var.venta[3]))
        query.bindValue(':precio', float(var.venta[4]))
        row = var.ui.tabFact.currentRow()
        if query.exec_():
            var.ui.lblstatus.setText('Venta Realizada')
            var.ui.tabFact.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
            var.ui.tabFact.setItem(row, 2, QtWidgets.QTableWidgetItem(str(var.venta[3])))
            var.ui.tabFact.setItem(row, 3, QtWidgets.QTableWidgetItem(str(var.venta[4])))
            var.ui.tabFact.setItem(row, 4, QtWidgets.QTableWidgetItem(str(var.venta[5])))
            row=row+1
            var.ui.tabFact.insertRow(row)
            var.ui.tabFact.setCellWidget(row, 1, var.cmbVenta)
            var.ui.tabFact.scrollToBottom()
            Conexion.cargarcmbVenta(var.cmbVenta)
        else:
            print("Error en la alta venta", query.lastError().text())

    def BajaVen(codigoVenta):
        """

        Modulo que elimina una venta de la factura

        :param codigoVenta: coodigo de la venta a eliminar
        :type codigoVenta: int
        :return:
        :rtype:

        Muestra mensaje en la barra de estado

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codventa = :codigoVenta')
        query.bindValue(':codigoVenta', codigoVenta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta eliminda')
        else:
            print("Error baja venta: ", query.lastError().text())

    def mostrarventas(codfac):
        """

        Modulo que muestra las ventas de una factura

        :param codfac: codigo de la factura que se cargaran las ventas
        :type codfac: int
        :return: None
        :rtype: None

        Recibe el codigo de la factura para seleccionar los datos de las ventas de esa factura
        Toma el nombre del producto y su precio para cada linea de venta. El Subtotal lo obtine de
        multiplicar el precio por la cantidad .
        Despues Carga en las tabla tavFact el codigo de la venta, el nombre del producto, las unidades y el subtotal de
        cada producto.
        Finalmente suma el subfact, que es la suma de todas las ventas de esa factur, le aplica el IVA de 21% en este
        caso y el importe total de la factura. Los valores subfact, iva y fact de la factura los muestra en sus
        respectivos labels

        """
        try:
            var.ui.tabFact.clearContents()
            var.subfact = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                index = 0
                while query.next():
                    codventa = query.value(0)
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    precio = query.value(3)
                    var.ui.tabFact.setRowCount(index + 1)
                    var.ui.tabFact.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query1.prepare('select producto from productos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            var.ui.tabFact.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tabFact.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tabFact.setItem(index, 3,QtWidgets.QTableWidgetItem("{0:.2f}".format(float(precio)) + ' €'))
                            var.ui.tabFact.setItem(index, 4, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(subtotal)) + ' €'))
                    index += 1
                    var.subfact = round(float(subtotal) + float(var.subfact), 2)
            if int(index) > 0:
                ventas.Ventas.PrepararVentas(index)
            else:
                var.ui.tabFact.setRowCount(0)
                ventas.Ventas.PrepararVentas(0)
            var.ui.lblSubtotal.setText("{0:.2f}".format(float(var.subfact)))
            var.iva = round(float(var.subfact) * 0.21, 2)
            var.ui.lblIVA.setText("{0:.2f}".format(float(var.iva)))
            var.fact = round(float(var.iva) + float(var.subfact), 2)
            var.ui.lblTotal.setText("{0:.2f}".format(float(var.fact)))

        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))

    def cargarcmbVenta(cmbVenta):
        """

        Modulo que carga los productos en un combobox llamdando a la BBDD

        :param cmbVenta: Combobox de los productos
        :type cmbVenta: ComboBox
        :return: None
        :rtype: None

        """
        var.cmbVenta.clear()
        query= QtSql.QSqlQuery()
        var.cmbVenta.addItem('')
        query.prepare('select codigo, producto from productos order by producto')
        if query.exec_():
            while query.next():
                var.cmbVenta.addItem(str(query.value(1)))

