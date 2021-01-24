import var, conexion

class Products():

    def altaProducto(self):
        '''
        cargará los proudctos en la tabla y en la base de datos
        en las búsquedas mostrará los datos del cliente
        :return: none
        '''
        try:
            newprod = []
            producto = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            k = 0
            for i in producto:
                newprod.append(i.text())  #cargamos los valores que hay en los editline
            if producto:
                conexion.Conexion.altaProducto(newprod)
            else:
                print('Faltan Datos')
        except Exception as error:
            print('Error en la alta del producto : %s ' % str(error))


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
            cod = fila[0]
            for i, dato in enumerate(prod):
                dato.setText(fila[i])
            conexion.Conexion.cargarProd(cod)
        except Exception as error:
            print('Error cargar productos en productos: %s ' % str(error))

    def limpiarProd():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            product = [var.ui.editNomeProducto, var.ui.EditPrecio, var.ui.EditStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblProd.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def BajaProd(self):
        """
        módulos para dar de baja un cliente
        :return:
        """
        try:
            codigo = var.ui.lblProd.text()
            conexion.Conexion.BajaProducto(codigo)
            Products.limpiarProd()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def ModificarProd(self):
            """Módulos para modificar datos de un cliente con determinado código
            :return: None
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