from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyQt5 import QtSql
import os
from datetime import datetime
import var

class Printer():
    def cabecera(self):
        """

        Modulo que imprimir la cabecera de todos los informes de la empresa

        :return: None
        :rtype: None

        """
        try:
            logo='.\\img\logo.png'
            var.rep.setTitle('INFORMES')
            var.rep.setAuthor('Administracion Teis')
            var.rep.setFont('Helvetica',size=10)
            var.rep.line(45,820,525,820)
            var.rep.line(45,745,525,745)
            textocif= 'CIF: A00000000H'
            textnom='IMFORMACIONES Y EXPORTACIONES TEIS S.L.'
            textdir='Avda. De Galicia, 101 - Vigo'
            texttlfo=' Tlfo: 886 12 04 64'
            var.rep.drawString(54,805, textocif)
            var.rep.drawString(54, 790,textnom)
            var.rep.drawString(54, 775, textdir)
            var.rep.drawString(54, 760, texttlfo)
            var.rep.drawImage(logo, 450, 752)
        except Exception as error:
            print("Error cabercera informe: %s" %str(error))


    def Pie(listado):
        """

        Modulo para imprimir el pie del imforme. Es igual sempre execpto el nombre pasado
        a traves de listado

        :param listado: segun de lo que se vaya a hacer el informe
        :type listado:String
        :return: None
        :rtype: None

        """
        try:
            var.rep.line(50,50,525,50)
            fecha=datetime.today()
            fecha=fecha.strftime('%d.%m.%Y %H.%M.%S')
            var.rep.setFont('Helvetica-Oblique', size=6)
            var.rep.drawString(460,40, str(fecha))
            var.rep.drawString(270,40, str('Pagina %s' % var.rep.getPageNumber()))
            var.rep.drawString(60,40,str(listado))
        except Exception as error:
            print("Errorenel pie de pagina: %s" % str(error))

    def CabeceraCliente(listado):
        """

        Modulo que carga la cabecera del cliente

        :return: None
        rtype: None

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            var.rep.drawString(255,735, listado)
            var.rep.line(45,730,525,730)
            itemcli=['CODIGO','DNI','APELIDOS','NOMBRE', 'FECHA ALTA']
            var.rep.drawString(45,710,itemcli[0])
            var.rep.drawString(130, 710,itemcli[1])
            var.rep.drawString(215, 710, itemcli[2])
            var.rep.drawString(350, 710, itemcli[3])
            var.rep.drawString(455, 710, itemcli[4])
            var.rep.line(45,703,525,703)
        except Exception as error:
            print("Error en cabecera cliente : %s " % str(error))

    def reportCli(self):
        """

        Modulo para hacer el informe del cliente. Llama a la base de datos y captura
        los datos y los muiestra enel informe

        :return:
        :rtype:

        La variable i son los valores del eje X
        La variable J son los valores del eje Y
        Los imformes se guardan en lac carpeta informe y los muetsra con el lector de PDF´s
        por defecto en el sistema

        """
        try:
            var.rep = canvas.Canvas('informes/listadoclientes.pdf', pagesize=A4)
            listado = 'LISTADO DE CLIENTES'
            Printer.cabecera(self)
            Printer.CabeceraCliente(listado)
            Printer.Pie(listado)
            query=QtSql.QSqlQuery()
            query.prepare('select codigo, dni, apellidos , nombre, fechalta  from clientes order by  nombre')
            var.rep.setFont('Helvetica',size=10)
            if query.exec_():
                i=55
                j=690
                while query.next():
                    if j <=80:
                        var.rep.drawString(440, 70, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera(self)
                        Printer.Pie(listado)
                        Printer.CabeceraCliente(listado)
                        i = 55
                        j = 690
                    var.rep.setFont('Helvetica',size=10)
                    var.rep.drawString(i,j, str(query.value(0)))
                    var.rep.drawString(i+75, j, str(query.value(1)))
                    var.rep.drawString(i+170, j, str(query.value(2)))
                    var.rep.drawString(i+315, j, str(query.value(3)))
                    var.rep.drawRightString(i+465,j, str(query.value(4)))
                    j=j-25
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('clientes.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print('Error reporcli %s' % str(error))

    def CabeceraProducto(listado):
        """

        Modulo que imprime la cabecera de imforme de productos.


        :param listado: es el nombre que se va imprimir
        :type listado : String
        :return: None
        :rtype: None

        """

        try:
            var.rep.setFont('Helvetica-Bold', size=9)
            var.rep.drawString(255, 735, listado)
            var.rep.line(45, 730, 525, 730)
            itemProd= ['CODIGO', 'NOMBRE', 'PRECIO', 'STOCK']
            var.rep.drawString(45, 710, itemProd[0])
            var.rep.drawString(190, 710, itemProd[1])
            var.rep.drawString(320, 710, itemProd[2])
            var.rep.drawString(455, 710, itemProd[3])
            var.rep.line(45, 703, 525, 703)
        except Exception as error:
          print("Error en ls cabecera del cliente %s" %str(error))

    def reportProduc(self):
        try:
            var.rep=canvas.Canvas('informes/listadoproductos.pdf', pagesize=A4)
            listado="Listado Productos"
            Printer.cabecera(self)
            Printer.Pie(listado)
            Printer.CabeceraProducto(listado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, producto, precio, stock from productos order by codigo')
            var.rep.setFont('Helvetica', size=10)
            if query.exec_():
                i = 55
                j = 690
                while query.next():
                    if j <=80:
                        var.rep.drawString(440, 70, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera(self)
                        Printer.Pie(listado)
                        Printer.CabeceraProducto(listado)
                        i = 55
                        j = 690
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    var.rep.drawString(i+135, j, str(query.value(1)))
                    var.rep.drawString(i+270, j, str(query.value(2)))
                    var.rep.drawString(i+410, j, str(query.value(3)))
                    j=j-25
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('productos.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print("Error en report Productos "+ str(error))


    def cabecerafac(codfac):
        """

        Módulo que carga la cabecera  informe factura
        :param codfac: el código de la factura
        :type: int
        :return: None
        :rtype: None

        Toma datos de las tablas cliente a la que está asociado el código factura
        y de la tabla facturas para tomar los datos de dni y fecha.
        Recibe el codfac de reportfact.

        """
        try:
            var.rep.setFont('Helvetica-Bold', size=11)
            var.rep.drawString(55, 725, 'Cliente: ')
            var.rep.setFont('Helvetica', size=10)
            var.rep.drawString(50, 650, 'Factura nº : %s' % str(codfac))
            var.rep.line(45, 665, 525, 665)
            var.rep.line(45, 640, 525, 640)
            var.rep.setFont('Helvetica', size=10)
            query = QtSql.QSqlQuery()
            query.prepare('select dni, fecha from facturas where codfac = :codfac')
            query.bindValue(':codfac', str(codfac))
            if query.exec_():
                while query.next():
                    dni = str(query.value(0))
                    var.rep.drawString(55, 710, 'DNI: %s' % str(dni))
                    var.rep.drawString(420, 650, 'Fecha: %s' % str(query.value(1)))
            query1 = QtSql.QSqlQuery()
            query1.prepare('select apellidos, nombre, direccion, provincia, formaspago from clientes where dni = :dni')
            query1.bindValue(':dni', str(dni))
            if query1.exec_():
                while query1.next():
                    var.rep.drawString(55, 695, str(query1.value(0)) + ', ' + str(query1.value(1)))
                    var.rep.drawString(55, 680, str(query1.value(2)) + ' - ' + str(query1.value(3)))
                    var.rep.drawString(400, 695, 'Formas de Pago: ')
                    var.rep.drawString(375, 680, str(query1.value(4).strip('[]').replace('\'', '').replace(',', ' -')))
            var.rep.line(45, 625, 525, 625)
            var.rep.setFont('Helvetica-Bold', size=10)
            itenventa = ['CodVenta', 'Artículo', 'Cantidad', 'Precio-Unidad(€)', 'Subtotal(€)']
            var.rep.drawString(45, 630, itenventa[0])
            var.rep.drawString(130, 630, itenventa[1])
            var.rep.drawString(270, 630, itenventa[2])
            var.rep.drawString(350, 630, itenventa[3])
            var.rep.drawString(455, 630, itenventa[4])
            var.rep.setFont('Helvetica-Bold', size=12)
            var.rep.drawRightString(500, 160, 'Subtotal:' + "{0:.2f}".format(float(var.ui.lblSubtotal.text())) + ' €')
            var.rep.drawRightString(500, 140, 'IVA:' + "{0:.2f}".format(float(var.ui.lblIVA.text())) + ' €')
            var.rep.drawRightString(500, 115, 'Total Factura: ' + "{0:.2f}".format(float(
                var.ui.lblTotal.text())) + ' €')
        except Exception as error:
            print('Error cabecfac %s' % str(error))

    def reportFac(self):
        """
        Modulo que hace el imforme de la factura por cliente

        :return: None
        :rtype: None

        Selecciona todas las ventas de la factura seleccionada  y las las muestra
        la variable i represnta los valores del eje X,
        la variable j representa los valores del eje Y
        En el pie del imforme de la factura tiene el subtotal, el iva y el total

        """
        try:
            textlistado = 'FACTURA CLIENTE'
            var.rep = canvas.Canvas('informes/factura.pdf', pagesize=A4)
            Printer.cabecera(self)
            Printer.Pie(textlistado)
            codfac = var.ui.lblFactura.text()
            Printer.cabecerafac(codfac)
            query = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', str(codfac))
            if query.exec_():
                i = 55
                j = 600
                while query.next():
                    if j <= 100:
                        var.rep.drawString(440, 110, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera(self)
                        Printer.Pie(textlistado)
                        Printer.cabecerafac(codfac)
                        i = 50
                        j = 600
                    var.rep.setFont('Helvetica', size=10)
                    var.rep.drawString(i, j, str(query.value(0)))
                    cod= str(query.value(1))
                    articulo = Printer.articulo(cod)
                    var.rep.drawString(i + 85, j, str(articulo))
                    var.rep.drawRightString(i + 245, j, str(query.value(2)))
                    var.rep.drawRightString(i + 355, j, "{0:.2f}".format(float(query.value(3))))
                    subtotal = round(float(query.value(2)) * float(query.value(3)),2)
                    var.rep.drawRightString(i + 450, j, "{0:.2f}".format(float(subtotal)) + ' €')
                    j = j - 20

            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('factura.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporfac %s' % str(error))

    def articulo(codigo):
        """

        Módulo que toma el nombre del artículo a partir del codigo para que los muestre la factura

        :param: codigo: código del artículo
        :type: int
        :return: artículo
        :rtype: string


        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select producto from productos where codigo = :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec_():
                while query.next():
                    dato = query.value(0)
            return dato
        except Exception as error:
            print('Error artículo según código:  %s ' % str(error))