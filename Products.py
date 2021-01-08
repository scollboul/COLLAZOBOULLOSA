import var, conexion
from ventana import *

class Productos():
    def altaProductos(self):
        try:
            newProd = []
            product = [var.ui.editNomeProducto, var.ui.EditPrecio]
            for i in product:
                newProd.append(i.text())
            if product:
                conexion.Conexion.altaProd(newProd)
            else:
                print('Faltan Datos')
        except Exception as error:
            print('Error alta productos : %s ' % str(error))