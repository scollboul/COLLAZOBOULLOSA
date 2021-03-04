import var, conexion
from PyQt5 import QtWidgets

class Ventas:
    def cargarFecha(qDate):
        ''''
        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
        '''
        try:
            if var.ui.TabWidget.currentIndex() == 1:
                data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
                var.ui.EditFechaFact.setText(str(data))
                var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altafactura(self):
        '''
        cargará los proudctos en la tabla y en la base de datos
        en las búsquedas mostrará los datos del cliente
        :return: none
        '''
        try:
            newFact = []
            factura = [var.ui.EditDNICli, var.ui.EditFechaFact, var.ui.EditApelCli]
            k = 0
            for i in factura:
                newFact.append(i.text())  # cargamos los valores que hay en los editline
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
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
        try:
            var.subfact=0.00
            var.fact=0.00
            var.iva=0.00
            fila = var.ui.tableFechaFact.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            var.ui.lblFactura.setText(str(fila[0]))
            var.ui.EditFechaFact.setText(str(fila[1]))
            conexion.Conexion.cargarFact(str(fila[0]))
        except Exception as error:
            print("Error al cargar factura: "+str(error))

    def BajaFactura(self):
        """
        módulos para dar de baja un cliente
        :return:
        """
        try:
            codigo = var.ui.lblFactura.text()
            conexion.Conexion.BajaFactura(codigo)
        except Exception as error:
            print('Error en la baja de facturas: %s ' % str(error))

    def reloadFact():
        '''
        Limpia datos formulario y recarga la tabla de clientes
        :return: None
        '''
        try:
            Factura=[var.ui.EditDNICli,var.ui.EditApelCli,var.ui.EditFechaFact,var.ui.lblFactura]
            for i,data in enumerate(Factura):
                Factura[i].setText('')
            conexion.Conexion.mostrarFacturas()
        except Exception as error:
            print('Error recargar facturas: %s ' % str(error))

    def buscarfacClientes():
        try:
            dni = var.ui.EditDNICli.text()
            conexion.Conexion.BuscarfactCli(dni)
        except Exception as error:
            print('Error buscar clientes: %s ' % str(error))

    def PrepararVentas(index):
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
            codigoventa = str(fila[0])
            print(codigoventa)
            conexion.Conexion.BajaVen(codigoventa)
            conexion.Conexion.mostrarventas(self)
        except Exception as error:
            print('Error baja venta: %s' % str(error))

    def venta(self):
        try:
            var.subfact=0.00
            var.venta= []
            codigofact=var.ui.lblFactura.text()
            var.venta.append(str(codigofact))
            art=var.cmbVenta.currentText()
            codPrec = conexion.Conexion.ObterPrecio(art)
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
                var.subfact=round(float(var.subfact) + float(subtot),2)
                var.ui.lblSubtotal.setText(str(subtot))
                var.iva=round(float(subtot)*0.21,2)
                var.ui.lblIVA.setText(str(var.iva))
                var.fact=round(float(var.subfact)+float(var.iva),2)
                var.ui.lblTotal.setText(str(var.fact))
                Ventas.mostrarVentas(self)
            else:
                var.ui.lblstatus.setText("Faltan Datos")
        except Exception as error:
            print('Error ventas '+str(error))

    def mostrarVentas(self):
        try:
            var.cmbVenta = QtWidgets.QComboBox()
            conexion.Conexion.cargarcmbVenta(var.cmbVenta)
            codigoFact = var.ui.lblFactura.text()
            conexion.Conexion.mostrarventas(codigoFact)
        except Exception as error:
            print('Error proceso mostrar ventas: %s' % str(error))