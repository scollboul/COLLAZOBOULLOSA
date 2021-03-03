from PyQt5 import QtWidgets, QtSql
import var
import ventas
from ventana import *


class Conexion():
    def db_connect(filename):
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
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago, edad)'
            'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')
        #en el orden de la base de datos
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        # pagos = ' '.join(cliente[7]) si quiesesemos un texto, pero nos viene mejor meterlo como una lista
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', int(cliente[8]))
        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Alta Cliente con dni ' + str(cliente[0]))
            Conexion.mostrarClientes()
        else:
            print("Error: ", query.lastError().text())

    def cargarCliente():
        '''
        Módulo que carga el resto de widgets con los datos del cliente dni
        :return: None
        '''
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
        '''
        Carga los datos principales del cliente en la tabla
        se ejecuta cuando lanzamos el programa, actualizamos, insertamos y borramos un cliente
        :return: None
        '''
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
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
        ''''
        modulo para eliminar cliente. se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def modifCli(codigo, newdata):
        ''''
        modulo para modificar cliente. se llama desde fichero clientes.py
        :return None
        '''
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
            print('Cliente modificado')
            var.ui.lblstatus.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar cliente: ", query.lastError().text())

    def buscaCli(dni):
        """
        select un cliente a partir de su dni.
        :return:
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
        Conexion a la tabla articulos
        '''

    def altaProducto(producto):
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
        '''
        Carga los datos principales del productos la tabla
        se ejecuta cuando lanzamos el programa, actualizamos, insertamos y borramos un producto
        :return: None
        '''
        # while var.ui.tableCli.rowCount() > 0:
        #     var.ui.tableCli.removeRow(0)
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, producto, precio from productos order by producto')
        if query.exec_():
            while query.next():
                # cojo los valores
                codigo = query.value(0)
                producto = query.value(1)
                precio = query.value(2)
                # crea la fila
                var.ui.tableProd.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableProd.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tableProd.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                var.ui.tableProd.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                index += 1
        else:
            print("Error mostrar productos"": ", query.lastError().text())

    def cargarProd(cod):
        '''
        Módulo que carga el resto de widgets con los datos del prodc
        :return: None
        '''
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
        ''''
        modulo para eliminar cliente. se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        query.prepare('delete from productos where codigo = :codigo')
        query.bindValue(':codigo', codigo)
        if query.exec_():
            var.ui.lblstatus.setText('Baja del producto con el codigo ' + codigo )
        else:
            print("Error eliminar Producto: ", query.lastError().text())
        Conexion.mostrarProducts()

    def ModificarProducto(codigo, newprod):
        ''''
        modulo para modificar cliente. se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        codigo = codigo
        query.prepare('update productos set producto=:producto, precio=:precio, stock=:stock where codigo=:codigo')
        query.bindValue(':codigo', codigo)
        query.bindValue(':producto', str(newprod[0]))
        query.bindValue(':precio', str(newprod[1]))
        query.bindValue(':stock', str(newprod[2]))
        if query.exec_():
            var.ui.lblstatus.setText('Modificado el producto con el codigo ' + codigo )
        else:
            print("Error al modificar el Producto",+query.lastError().text())

    def altaFactura(factura):
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
        '''
        Carga los datos principales del Facturas la tabla
        se ejecuta cuando lanzamos el programa, actualizamos, insertamos y borramos un producto
        :return: None
        '''
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas')
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
        '''
        Módulo que carga el resto de widgets con los datos del prodc
        :return: None
        '''
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
        Conexion.mostrarFacturas()
        var.ui.lblSubtotal.setText('0.00')
        var.ui.lblIva.setText('0.00')
        var.ui.lblTotal.setText('0.00')

    def BuscarfactCli(dni):
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
        query=QtSql.QSqlQuery()
        query.prepare('insert into ventas(codfacventa, codarticventa, cantidad, precio)'
                      'VALUES(:codfacventa, :codarticventa, :cantidad, :precio)')
        query.bindValue(':codfacventa', int(var.venta[0]))
        query.bindValue(':codarticventa', int(var.venta[1]))
        query.bindValue(':cantidad', int(var.venta[3]))
        query.bindValue(':precio', float(var.venta[4]))
        row = var.ui.tabFact.currentRow()
        if query.exec_():
            var.ui.tabFact.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
            var.ui.tabFact.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[3])))
            var.ui.tabFact.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[4])))
            var.ui.tabFact.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[5])))
            row +=1
            var.ui.tabFact.insertRow(row)
            var.ui.tabFact.setCellWidget(row, 1, var.cmbVenta)
            Conexion.cargarcmbVenta(var.cmbVenta)
            var.ui.tabFact.scrollToBottom()
        else:
            print("Error en la alta venta", query.lastError().text())

    def BajaVen(codigoventa):
        query=QtSql.QSqlQuery()
        query.prepare('delete from ventas where codventa = :codigoventa')
        if query.exec_():
            var.ui.lblstatus.setText("Venta eliminada")
        else:
            print("Error eliminar venta: ",query.lastError().text())

    def mostrarventas(codigoFact):
        '''
        Carga los datos principales del productos la tabla
        se ejecuta cuando lanzamos el programa, actualizamos, insertamos y borramos un producto
        :return: None
        '''
        try:
            var.subfact=0.00
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfacventa = :codigoFact')
            query.bindValue(':codfac', str(codigoFact))
            if query.exec_():
                index = 0
                while query.next():
                    # cojo los valores
                    codventa = query.value(0)
                    codarticulo = query.value(1)
                    cant = query.value(2)
                    precio = query.value(3)
                    # crea la fila
                    var.ui.tabFact.setRowCount(index + 1)
                    # voy metiendo los datos en cada celda de la fila
                    var.ui.tabFact.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query2=QtSql.QSqlQuery()
                    query2.prepare('select producto from productos where codigo= :codarticulo')
                    if query2.exec_():
                        while query2.next():
                            art= query2.value(0)
                            var.ui.tabFact.setItem(index, 1, QtWidgets.QTableWidgetItem(str(art)))
                            var.ui.tabFact.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cant)))
                            subtot = round(float(cant) * float(precio), 2)
                            var.ui.tabFact.setItem(index, 3, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(precio)) + ' €'))
                            var.ui.tabFact.setItem(index, 4, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(subtot))+ ' €'))
                    index += 1
                    var.subfact=round(float(subtot)+float(var.subfact), 2)
                if int(index)>0:
                    ventas.Ventas.PrepararVentas(index)
                else:
                    var.ui.tabFact.setRowCount(0)
                    ventas.Ventas.PrepararVentas(0)
                var.ui.lblSubtotal.setText("{0:.2f}".format(float(var.subfact)))
                var.iva = round(float(var.subfact) * 0.21, 2)
                var.ui.lblIVA.setText("{0:.2f}".format(float(var.iva)))
                var.fac = round(float(var.iva) + float(var.subfact), 2)
                var.ui.lblTotal.setText("{0:.2f}".format(float(var.fact)))
            else:
                print("Error mostrar productos"":  ", query.lastError().text())
        except Exception as error:
            print("Error al mostrar la tabla de ventas", str(error))

    def cargarcmbVenta(cmbVenta):
        var.cmbVenta.clear()
        query= QtSql.QSqlQuery()
        var.cmbVenta.addItem('')
        query.prepare('select codigo, producto from productos order by producto')
        if query.exec_():
            while query.next():
                var.cmbVenta.addItem(str(query.value(1)))

    def ObterPrecio(art):
        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio from productos where producto = :art')
        query.bindValue(':art',str(art))
        if query.exec_():
            while query.next():
                dato=[str(query.value(0)), str(query.value(1))]
        return dato

# class Conexion():
#     HOST='localhost'
#     PORT='27017'
#     URI_CONNECTION='mongodb://'+HOST+':'+PORT+'/'
#     var.DATABASE='empresa'
#     try:
#         print('Conexión al servidor %s' %HOST)
#     except:
#         print('error de conexion')