from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyQt5 import QtSql
import os
from datetime import datetime
import var

class Printer():
    def cabecera():
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
            Printer.cabecera()
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

    def reportProduc(listado):
        try:
            var.rep=canvas.Canvas('informes/listadoproductos.pdf', pagesize=A4)
            listado="Listado Productos"
            Printer.cabecera()
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
                        Printer.cabecera()
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