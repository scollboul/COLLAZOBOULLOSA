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
    #
    # def altafactura(self):
    #     '''
    #     cargará los proudctos en la tabla y en la base de datos
    #     en las búsquedas mostrará los datos del cliente
    #     :return: none
    #     '''
    #     try:
    #         newFact = []
    #         factura = [var.ui.EditFechaFact]
    #         k = 0
    #         for i in factura:
    #             newFact.append(factura)  # cargamos los valores que hay en los editline
    #         if factura:
    #             conexion.Conexion.altaProducto(newFact)
    #         else:
    #             print('Faltan Datos')
    #     except Exception as error:
    #         print('Error cargar producto : %s ' % str(error))