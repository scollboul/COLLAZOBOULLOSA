import var, conexion
from PyQt5 import QtWidgets,  QtSql

class Ventas:
    def cargarFecha(qDate):

        """

        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar

        """

        try:
            if var.ui.TabWidget.currentIndex() == 1:
                data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
                var.ui.EditFechaFact.setText(str(data))
                var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altafactura(self):
        """

        Modulo que da de alta las facturas

        :return: none
        :rtype None

        carga de los widgets los valores para dar de alta una factura y muestra la tabla facturas actualizada
        y prepara la tabla para las ventas

        """
        try:
            newFact = []
            factura = [var.ui.EditDNICli, var.ui.EditFechaFact, var.ui.EditApelCli]
            for i in factura:
                newFact.append(i.text())
            if factura:
                conexion.Conexion.altaFactura(newFact)
                conexion.Conexion.mostrarFacturas()
                Ventas.PrepararVentas(0)
            else:
                print('Faltan Datos')
            conexion.Conexion.mostrarFacturas()
        except Exception as error:
            print('Error alta de la factura : %s ' % str(error))

    def cargarFactura():
        """

        carga en los widgets del formulario factura los datos de la factura clickada en
        en la tabla

        :return: none
        :rtype None

        """

        try:
            var.subfact=0.00
            var.fact=0.00
            var.iva=0.00
            fila = var.ui.tableFechaFact.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            var.ui.lblFactura.setText(str(fila[0]))
            var.ui.EditFechaFact.setText(str(fila[1]))
            codigo=str(fila[0])
            conexion.Conexion.cargarFact(codigo)
        except Exception as error:
            print("Error al cargar factura: "+str(error))

    def BajaFactura(self):
        """

        módulos para dar de baja una factura segun su codigo

        :return: none
        :rtype None

        """
        try:
            codigo = var.ui.lblFactura.text()
            conexion.Conexion.BajaFactura(codigo)
        except Exception as error:
            print('Error en la baja de facturas: %s ' % str(error))

    def reloadFact():
        """

        Limpia datos del formulario de facturas y de las ventas

        :return: none
        :rtype None

        """
        try:
            Factura=[var.ui.EditDNICli,var.ui.EditApelCli,var.ui.EditFechaFact,var.ui.lblFactura]
            for i,data in enumerate(Factura):
                Factura[i].setText('')
            conexion.Conexion.mostrarFacturas()
        except Exception as error:
            print('Error recargar facturas: %s ' % str(error))

    def buscarfacClientes():
        """

        Buscar facturas de un cliente por su DNI

        return: none
        :rtype None

        """
        try:
            dni = var.ui.EditDNICli.text()
            conexion.Conexion.BuscarfactCli(dni)
        except Exception as error:
            print('Error buscar clientes: %s ' % str(error))

    def PrepararVentas(index):
        """

        Modulo que prepara la tabla tabFact.

        :param: index es la fila de la tabla
        :type: int
        :return: None
        :rtype: None

        Carga el combobox de de articulos e inserta una vila en la tabla tabFact

        """
        try:
            var.cmbVenta=QtWidgets.QComboBox()
            conexion.Conexion.cargarcmbVenta(var.cmbVenta)
            var.ui.tabFact.setRowCount(index + 1)
            var.ui.tabFact.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tabFact.setCellWidget(index, 1, var.cmbVenta)
            var.ui.tabFact.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tabFact.setItem(index, 3, QtWidgets.QTableWidgetItem())
            var.ui.tabFact.setItem(index, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error en la preparecion de ventas: %s' % str(error))

    def BajaVenta(self):
        try:
            fila = var.ui.tabFact.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codigoventa = int(fila[0])
            conexion.Conexion.BajaVen(codigoventa)
            Ventas.mostrarVentas(self)
        except Exception as error:
            print('Error en la baja de la venta: %s' % str(error))

    def venta(self):
        """

        Modulo para el proceso de alta de una venta

        :return: None
        :rtype: None

        Recoge en la variable venta todos los datos necesarios para su alta, recogiendo el codigo de facturacion
        del lblFactura,el precio y codigo del producto de la tabla de productos, asi como la cantidad que
        se recoge directamente de la tabla TabFact y el prodeucto que se recoge del combobox cmbVenta que contiene
        los artiulos.
        Antes de hacer el proceso del alta se comprueba que se han añadido los campos necesarios, si no es asi muestra
        un mensaje en la barra de estado.
        Mostrara la tabla de las ventas actualizadas.
        Y de alta la venta y añade una nueva fila a la tabal de ventas

        """
        try:
            var.subfact=0.00
            var.venta= []
            codigofact=var.ui.lblFactura.text()
            var.venta.append(str(codigofact))
            art=var.cmbVenta.currentText()
            codPrec = Ventas.ObterCodPrecio(art)
            var.venta.append(int(codPrec[0]))
            var.venta.append(art)
            row= var.ui.tabFact.currentRow()
            cant= var.ui.tabFact.item(row, 2).text()
            cant=cant.replace(',', '.')
            var.venta.append(int(cant))
            precio = codPrec[1].replace(',', '.')
            var.venta.append(round(float(precio), 2))
            subtot= round(int(cant)*float(codPrec[1]), 2)
            var.venta.append(subtot)
            var.venta.append(row)
            if codigofact !='' and art !='' and cant !='':
                conexion.Conexion.altaVenta()
                Ventas.mostrarVentas(self)
            else:
                var.ui.lblstatus.setText("Faltan Datos")
        except Exception as error:
            print('Error ventas '+str(error))

    def mostrarVentas(self):
        """

        Modulo para mostrar las ventas en la tabla tabFact

        :return:
        :rtype:

        Recoge el codigo de la factura y se lo pasa a Conexion.mostrarventas

        """
        try:
            var.cmbVenta = QtWidgets.QComboBox()
            conexion.Conexion.cargarcmbVenta(var.cmbVenta)
            codigoFact = var.ui.lblFactura.text()
            conexion.Conexion.mostrarventas(codigoFact)
        except Exception as error:
            print('Error mostrar ventas: %s' % str(error))

    def Descuento():
        try:
            codigoFact = var.ui.lblFactura.text()
            conexion.Conexion.mostrarventascondescuento(codigoFact)
        except Exception as error:
            print('Error descuento ventas: %s' % str(error))

    def ObterCodPrecio(art):
        """

        Modulo que nos permite averiguar el codigo y precio de un articulo pasado

        :param art: articulo del cual queremos saber el codigo y el precio
        :type art:
        :return: dato
        :rtype: Lista

        """
        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio from productos where producto = :art')
        query.bindValue(':art',str(art))
        if query.exec_():
            while query.next():
                dato=[str(query.value(0)), str(query.value(1))]
        return dato