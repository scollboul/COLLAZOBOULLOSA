from reportlab.pdfgen import canvas
import os, var
from datetime import datetime

class Printer():
    def cabecera(self):
        logo='.\\img\logo.logo'
        var.rep.setTitle('INFORMES')
        var.rep.drawImage(logo,'450','752')
        var.rep.setAuthor('Administracion Teis')
        var.rep.setFont('Helvetica',size=10)
        var.rep.line(45,820,525,820)
        textocif= 'CIF: A00000000H'
        textnom='IMFORMACIONES Y EXPORTACIONES TEIS S.L.'
        textdir='Avda. De Galicia, 101 - Vigo'
        texttlfo='886 12 04 64'
        var.rep.drawString(54,805, textocif)
        var.rep.drawString(54, 790,textnom)
        var.rep.drawString(54, 775, textdir)
        var.rep.drawString(54, 760, texttlfo)

    def Pie(self):
        var.rep.line(50,50,525,50)
        fecha=datetime.today()
        fecha=fecha.strftime('%d.%m.%Y.%H.%M.%S')
        var.rep.setFont('Helvetica-Oblique', size=6)
        var.rep.drawString(460,40, str(fecha))
        var.rep.drawString(270,40, str('Pagina %s' % var.rep.getPageNumber()))
    def reportCli(self):
        try:
            var.rep= canvas.Canvas('informes/listadoclientes.pdf')
            Printer.cabecera()
            Printer.Pie()
            var.rep.save()
            rootPath = ".\\informes"
            cont = 0
            for file in os.listdir(rootPath):
                if file.endswith('.pdf'):
                    os.startfile("%s/%s" % (rootPath, file))
                cont = cont + 1

        except Exception as error:
            print('Error reporcli %s' % str(error))