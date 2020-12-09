import sys, var, vensalir, clients


class Eventos():

    def Salir(event):
        '''
        Módulo para cerrar el programa
        :return:
        '''
        try:
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
                # print(event)
                sys.exit()
            else:
                var.dlgsalir.hide()
                event.ignore()

        except Exception as error:
            print('Error %s' % str(error))

    def cargarProv(self):
        """
        carga las provincias al iniciar el programa
        :return:
        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error: %s' % str(error))

    def Backup(self):
        try:
            print('hará copia de seguidad de la BBDD')
        except Exception as error:
            print('Error: %s' % str(error))

    def AbrirDir(self):
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))

    def AbrirPrinter(self):
        try:
            var.dlgimprimir.setWindowTitle('Imprimir')
            var.dlgimprimir.setModal(True)
            var.dlgimprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))

    def AbrirAviso(men):
        try:
            if var.dlgsalir.exec_() and var.salir:
                pass
            else:
                var.lblsaviso.setText(men)
                var.dlgsalir.show()

        except Exception as error:
            print('Error abrir ventana aviso: %s ' % str(error))

    def Confirmar():
        try:
            clients.Clientes.bajaCliente()
            var.dlgaviso.hide()
        except Exception as error:
            print('Error botón confirma: %s ' % str(error))

    def Anular():
        try:
            var.dlgaviso.hide()
        except Exception as error:
            print('Error botón anula: %s ' % str(error))

    def mostrarAviso():
        try:
            var.dlgaviso.show()
        except Exception as error:
            print('Error mostrar aviso: %s ' % str(error))