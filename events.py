import sys, var, clients, conexion, zipfile, os, shutil
from datetime import datetime
from PyQt5 import QtWidgets

from PyQt5.uic.properties import QtWidgets


class Eventos():

    def Salir(event):
        """

        Modulo para salir del programa.Muestra una venta de aviso

        :return: None
        :rtype:

        """
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

        Modulo que nos permite carga las provincias en el ComboBox de provinicas cmbProv

        :return: None
        :rtype: None

        Se carga al lazar el programa

        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error: %s' % str(error))

    def Backup(self):
        """

        Modulo que hace una copia de seguridad de la base de datos

        :return:None
        :rtype: None

        Usa la libreria zipfile, añade la fecha y hora al nombre y al realizar la copia se elige el diretorio
        deseado. Para ello se abrira una venta de deialogo.
        Muestra mensaje en la barra de estado.

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            directorio, filename = var.filedlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip')
            if var.filedlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                var.ui.lblstatus.setText('COPIA DE SEGURIDAD DE BASE DE DATOS CREADA')
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error: %s' % str(error))

    def AbrirDir(self):
        """

        Modulo que abre uns ventada de dialogo

        :return: None
        :rtype: None

        """
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))

    def AbrirPrinter(self):
        """
        Modulo que abre la venta de dialogo de la impresora

        :return: None
        :rtype: None

        """
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))

    def restaurarBD(self):
        """

        Modulo que restaura la base de datos

        :return: None
        :rtype: None

        Abre la ventaba de dialogo para buscar su localizacion y las restaura usanso la libreria
        zipfile.
        Muestra mensaje de comfirmacion en la barra de estado

        """

        try:

            filename = var.filedlgabrir.getOpenFileName(None, 'Restaurar Copia de Seguridade', '', '*.zip;;All Files')
            if var.filedlgabrir.Accepted and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
            conexion.Conexion.db_connect(var.filebd)
            conexion.Conexion.mostrarClientes()
            conexion.Conexion.mostrarProducts()
            conexion.Conexion.mostrarFacturas()
            var.ui.lblstatus.setText('COPIA DE SEGURIDAD RESTAURDA')
        except Exception as error:
            print('Error restaurar base de datos: %s ' % str(error))