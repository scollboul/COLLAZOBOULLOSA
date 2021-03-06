import var, conexion

class Products():

    def altaProducto(self):
        """

        Modulo que da de alta los datos productos

        :return: none

         Se crea una lista newprod que contendra todos los datos del producto que se introduzcan en los widgets
         esta lista se pasa como argumento al modulo altaProd del modulo conexion.

        """
        try:
            newprod = []
            producto = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            for i in producto:
                newprod.append(i.text())
            if producto:
                conexion.Conexion.altaProducto(newprod)
            else:
                print('Faltan Datos')

        except Exception as error:
            print('Error en la alta del producto : %s ' % str(error))

    def cargarProd():
        """

        carga en widgets los datos del productos clickado en la tabla

        :return: none
        :rtype: none

        """
        try:
            fila = var.ui.tableProd.selectedItems()
            prod = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 1
            cod = fila[0]
            for i, dato in enumerate(prod):
                dato.setText(fila[i])
            conexion.Conexion.cargarProd(cod)
        except Exception as error:
            print('Error cargar productos en productos: %s ' % str(error))

    def limpiarProd():
        """

        limpia los datos del formulario producto

        :return: none
        :rtype: none

        """
        try:
            product = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblProd.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def BajaProd(self):
        """

        Modulo para dar de baja un producto clickado en la tabla de productos
        Limpia los datos del furmolario y muestra la tabla actualizada

        :return:
        :rtype: none

        """
        try:
            codigo = var.ui.lblProd.text()
            conexion.Conexion.BajaProducto(codigo)
            Products.limpiarProd()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def ModificarProd(self):
        """

        Modulo para modifar datos de un proucto por un determinado codigo

        :return: None
        :rtype: None

        A partir del codigo del producto lee los nuevos datos de los widgets que se han cargado y modificado,
        llama al modilo Conexion.ModificarProducto para actualizar los datos en la BBDD pasandole una lista con los
        nuevos datos y el codigo del producto a modificar.

        """
        try:
            newprod = []
            product = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            for i in product:
                newprod.append(i.text())  # cargamos los valores que hay en los editline
            cod = var.ui.lblProd.text()
            conexion.Conexion.ModificarProducto(cod, newprod)
            conexion.Conexion.mostrarProducts()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))
