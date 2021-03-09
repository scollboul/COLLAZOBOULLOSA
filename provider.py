import var, conexion

class Provider():

    def altaProveedor(self):
        try:
            newProv = []
            Provedor = [var.ui.editNomeProv, var.ui.EditTelProv]
            for i in Provedor:
                newProv.append(i.text())
            if Provedor:
                conexion.Conexion.altaproveedor(newProv)
            else:
                print('Faltan Datos')

        except Exception as error:
            print('Error en la alta del producto : %s ' % str(error))

    def BajaProv(self):
        try:
            codigo = var.ui.lblProve.text()
            conexion.Conexion.BajaProveedor(codigo)
        except Exception as error:
            print('Error Eliminar Proveedor: %s ' % str(error))

    def limpiarProv():
        try:
            proveedor = [var.ui.editNomeProv, var.ui.EditTelProv]
            for i in range(len(proveedor)):
                proveedor[i].setText('')
            var.ui.lblProve.setText('')
        except Exception as error:
            print('Error limpiar widgets proveedores: %s ' % str(error))

    def ModificarProd(self):
        try:
            newProv = []
            Proveedor = [var.ui.editNomeProv, var.ui.EditTelProv]
            for i in Proveedor:
                newProv.append(i.text())  # cargamos los valores que hay en los editline
            cod = var.ui.lblProve.text()
            conexion.Conexion.ModificarProveedores(cod, newProv)
            conexion.Conexion.mostrarProvedrores()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def cargarProd():
        try:
            fila = var.ui.TableProveedores.selectedItems()
            prov = [var.ui.editNomeProv, var.ui.EditTelProv]
            if fila:
                fila = [dato.text() for dato in fila]
            cod = fila[0]
            for i, dato in enumerate(prov):
                dato.setText(fila[i])
            conexion.Conexion.cargarProv(cod)
        except Exception as error:
            print('Error cargar productos en productos: %s ' % str(error))
