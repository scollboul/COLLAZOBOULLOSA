import var, conexion
from ventana import *

class Productos():
    def altaProductos(self):
        try:
            newProd = []
            product = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            for i in product:
                newProd.append(i.text())
            if product:
                conexion.Conexion.altaProd(newProd)
            else:
                print('Faltan Datos')
        except Exception as error:
            print('Error alta productos : %s ' % str(error))

    def cargarProd():
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
        try:
            fila = var.ui.tableProd.selectedItems()
            prod = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 1
            cod= fila[0]
            for i, dato in enumerate(prod):
                dato.setText(fila[i])
            conexion.Conexion.cargarProd(cod)
        except Exception as error:
            print('Error cargar productos: %s ' % str(error))

