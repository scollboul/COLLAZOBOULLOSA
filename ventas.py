import var, conexion

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
            #Products.limpiarProd()
        except Exception as error:
            print('Error en la baja de facturas: %s ' % str(error))