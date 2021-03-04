from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyQt5 import QtSql
import os
from datetime import datetime
import var

class Printer():
    def cabecera(self):
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
                i=55 #eje x
                j=690 #eje y
                while query.next():
                    if j <=80:
                        var.rep.drawString(440, 70, 'Página siguiente...')
                        var.rep.showPage()
                        Printer.cabecera()
                        Printer.Pie(listado)
                        Printer.CabeceraCliente()
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
            rootPath=".\\informes"
            cont=0
            for file in os.listdir(rootPath):
                if file.endswith('listadoclientes.pdf'):
                    os.startfile("%s %s" % (rootPath,file))
                cont= cont+1
        except Exception as error:
            print('Error reporcli %s' % str(error))

    def CabeceraProducto(listado):
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

    def reportProduc(self, listado):
        try:
            var.rep=canvas.Canvas('informes/listadoproductos.pdf', pagesize=A4)
            listado="Listado Productos"
            Printer.cabecera(self)
            Printer.Pie(listado)
            Printer.CabeceraProducto(listado)
            query = QtSql.QSqlQuery()
            query.prepare('select codigo, nombre, precio , stock from productos order by codigo')
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
                if file.endswith('listadoproductos.pdf'):
                    os.startfile("%s %s" % (rootPath, file))
                cont = cont + 1
        except Exception as error:
            print("Error en report Productos "+ str(error))


    def cabecerafac(codfac):
        '''
        Módulo que carga la cabecera de página del informe factura
        :param codfac: el código de la factura
        :type: int
        :return: None
        :rtype: None
        Toma datos de dos tablas. Los del cliente a la que está asociado el código factura y la de la tabla
        facturas para tomar los datos de dni y fecha.
        '''
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
                    var.rep.drawString(300, 695, 'Formas de Pago: ')
                    var.rep.drawString(55, 680, str(query1.value(2)) + ' - ' + str(query1.value(3)))
                    var.rep.drawString(300, 680, str(query1.value(4).strip('[]').replace('\'', '').replace(',', ' -')))  #\ caracter escape indica que lo siguiente tiene un significado especial
            var.rep.line(45, 625, 525, 625)
            var.rep.setFont('Helvetica-Bold', size=10)
            temven = ['CodVenta', 'Artículo', 'Cantidad', 'Precio-Unidad(€)', 'Subtotal(€)']
            var.rep.drawString(50, 630, temven[0])
            var.rep.drawString(140, 630, temven[1])
            var.rep.drawString(275, 630, temven[2])
            var.rep.drawString(360, 630, temven[3])
            var.rep.drawString(470, 630, temven[4])
            var.rep.setFont('Helvetica-Bold', size=12)
            var.rep.drawRightString(500, 160, 'Subtotal:   ' + "{0:.2f}".format(float(
                var.ui.lblSubtotal.text())) + ' €')
            var.rep.drawRightString(500, 140, 'IVA:     ' + "{0:.2f}".format(float(var.ui.lblIva.text())) + ' €')
            var.rep.drawRightString(500, 115, 'Total Factura: ' + "{0:.2f}".format(float(
                var.ui.lblTotal.text())) + ' €')
        except Exception as error:
            print('Error cabecfac %s' % str(error))

    def reportFac(self):
        '''
        Módulo que carga el cuerpo del informe de la factura
        :return: None
        :rtype: None
        Selecciona todas las ventas de esa factura y las va anotando línea a línea:
        la variable i represnta los valores del eje X,
        la variable j representa los valores del eje Y
        Además tiene un pié de informe para mostrar los subtotales, iva y total
        '''
        try:
            textlistado = 'FACTURA'
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
                    articulo = Printer.artLinVenta(str(query.value(1)))
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

    def artLinVenta(codigo):
        '''
        Módulo que toma el nombre del artículo a partir de su código
        :param: codigo código del artículo
        :type: int
        :return: artículo
        :rtype: string
        Este módulo permite en el cuerpo de la factura que se muestre el nombre del artículo y no su código
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare('select producto from productos where codigo = :codigo')
            query.bindValue(':codigo', int(codigo))
            if query.exec_():
                while query.next():
                    articulo = query.value(0)
            return articulo

        except Exception as error:
            print('Error artículo según código:  %s ' % str(error))