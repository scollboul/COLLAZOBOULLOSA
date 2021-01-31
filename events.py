import sys, var, clients, conexion, zipfile, os, shutil
from datetime import datetime
from PyQt5 import QtWidgets

from PyQt5.uic.properties import QtWidgets


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
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))

    def AbrirPrinter(self):
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))