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
                row = 0
                column = 0
                var.ui.tableProd.insertRow(row)
                for registro in newProd:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.tableProd.setItem(row, column, cell)
                    column += 1
                print(newProd)
                conexion.Conexion.altaCli(newProd)
            else:
                print('Faltan Datos')
        except Exception as error:
            print('Error alta productos : %s ' % str(error))