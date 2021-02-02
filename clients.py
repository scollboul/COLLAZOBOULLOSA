import var, conexion
from ventana import *


class Clientes():

    def validarDni(dni):
        """
        Modulo que valida la letra de un dni segun sea nacional o extranjero

        :param a: dni formato texto
        :type: string
        :return: None
        :rtype: bool

        Pone la letra en mayusculas, comprueba que son nueve caracteres.Toma los 8 primeros, si es extranjero cambia la letra a su numero correspondiente.
        Una vez hace esto suma los numero y los divide entre 23 y coje el resto para comprbar si el dni es correcto

        """
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control

        except Exception as error:
            print('Error módulo validar DNI %s' % str(error))
            return None

    def validoDni():
        """

        Modulo que segun el dni sea correcto o no muestra una cosa o otra

        :return: none

        Si es correcto muestra un label con forma de tick verde y si es falso lo como muestra una X roja

        """
        try:
            dni = var.ui.editDni.text()
            print(dni)
            if Clientes.validarDni(dni):
                var.ui.lblValidar.setStyleSheet('QLabel {color: green;}')
                var.ui.lblValidar.setText('V')
                var.ui.editDni.setText(dni.upper())
            else:
                var.ui.lblValidar.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValidar.setText('X')
                var.ui.editDni.setText(dni.upper())

        except:
            print('Error módulo escribir valido DNI')
            return None

    def selSexo(self):
        """
        Modulo para definir el sexo del cliente

        :return: none
        :rtype: none

        Modulo para añadir en la variable var.sex el sexo del cliente mediante un radiobutton.
        Si esta seleccionado Femenino se añadira mujer y si esta Masculino se añadira hombre

        """
        try:
            if var.ui.rbtFem.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbtMasc.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error: %s' % str(error))

    def selPago():
        """

        Modulo para seleccionar los metodos de pago del cliente

        :return: Una lista de valores
        :rtype: List

        Añade en la variable var.pay los distisntos metodos de pago del cliente mediante ChekGroups


        """
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grpbtnPay.buttons()):
                if data.isChecked() and i == 0:
                   var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                   var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                   var.pay.append('Transferencia')
            return var.pay
        except Exception as error:
            print('Error: %s' % str(error))

    def selProv(prov):
        """

        Al sleccionar una provincia en el combo de provincias

        :param a: provincia seleccionada
        :return:
        :rtype:


        """
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error: %s' % str(error))

    def abrirCalendar(self):
        """

        Modulo que abre la ventana calendario

        """



        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    def cargarFecha(qDate):
        """

        Modulo que carga la fecha marcada en el widget Calendar

        :param a Libreria Python para el formateo de fechas
        :return: None
        :rtype: formato de fechas

        A partir del evento Calendar.clicked.connect al clickear una fecha , caprtura y la carga en el
        editFecha

        """
        try:
            if var.ui.TabWidget.currentIndex() == 0:
                data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
                var.ui.editClialta.setText(str(data))
                var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altaCliente(self):
        """

        Modulo qu carga los datos del cliente

         :param a:None
         :param b:None
         :return:None

         Se crea una lista newcli que contendra todos los datos del cliente que se introduzcan en los widgets
         esta lista se pasa como argumento al modulo altaCli del modulo conexion.
         El modulo llama a la funcion mostrarClientes que recarga la tabla con todos los clientes ademas del nuevo
         EL modulo llama a la funcion limpiarCli que limpia el contenido de los widgets

         """
        try:
            newcli = []
            clitab = []
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            k = 0
            for i in client:
                newcli.append(i.text())
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            newcli.append(var.sex)
            var.pay2 = Clientes.selPago()
            newcli.append(var.pay2)
            edad = var.ui.spinEdad.value()
            newcli.append(edad)
            if client:
                row = 0
                column = 0
                var.ui.tableCli.insertRow(row)
                for registro in clitab:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.tableCli.setItem(row, column, cell)
                    column +=1
                conexion.Conexion.altaCli(newcli)
                conexion.Conexion.mostrarClientes()
                Clientes.limpiarCli()
            else:
                print('Faltan Datos')
        except Exception as error:
            print('Error alta cliente : %s ' % str(error))

    def limpiarCli():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grpbtnSex.setExclusive(False)  #necesario para los radiobutton
            for dato in var.rbtsex:
                dato.setChecked(False)
            for data in var.chkpago:
                data.setChecked(False)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.lblValidar.setText('')
            var.ui.lblCodcli.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def cargarCli():
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
        try:
            fila = var.ui.tableCli.selectedItems()
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome ]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
                if i==0:
                    var.ui.EditDNICli.setText(fila[0])
                if i==1:
                    var.ui.EditApelCli.setText(fila[1])
            conexion.Conexion.cargarCliente()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def bajaCliente(self):
        """
        módulos para dar de baja un cliente
        :return:
        """
        try:
            dni = var.ui.editDni.text()
            conexion.Conexion.bajaCli(dni)
            conexion.Conexion.mostrarClientes()
            Clientes.limpiarCli()
        except Exception as error:
            print('Error baja clientes: %s ' % str(error))


    def modifCliente(self):
        """Módulos para modificar datos de un cliente con determinado código
        :return: None
        """
        try:
            newdata = []
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in client:
                newdata.append(i.text())  # cargamos los valores que hay en los editline
            newdata.append(var.ui.cmbProv.currentText())
            newdata.append(var.sex)
            var.pay = Clientes.selPago()
            newdata.append(var.pay)
            edad = var.ui.spinEdad.value()
            newdata.append(edad)
            cod = var.ui.lblCodcli.text()
            conexion.Conexion.modifCli(cod, newdata)
            conexion.Conexion.mostrarClientes()

        except Exception as error:
            print('Error modifcar clientes: %s ' % str(error))

    def reloadCli():
        '''
        Limpia datos formulario y recarga la tabla de clientes
        :return: None
        '''
        try:
            print(var.ui.spinEdad.value())
            Clientes.limpiarCli()
            conexion.Conexion.mostrarClientes()
        except Exception as error:
            print('Error recargar clientes: %s ' % str(error))

    def buscarCli(self):
        """
        Busca un Cliente a partir de un dni que escribe el usuario
        :return: mensaje
        """
        try:
            #Clientes.limpiarCli()
            dni = var.ui.editDni.text()
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error buscar clientes: %s ' % str(error))

    def valoresSpin():
        try:
            var.ui.spinEdad.setValue(16)
        except Exception as error:
            print('Error valores spin: %s ' % str(error))

