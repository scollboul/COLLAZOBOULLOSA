from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport
from ventana import *
from vensalir import *
from vencalendar import *
from datetime import datetime, date
import sys, var, events, clients, conexion, printer, Products, ventas

class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgsalir= Ui_dlgsalir()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        #var.dlgsadlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.closeSalir)
        #no es neceasario no quiero que haga nada

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_dlgCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual,mesactual,diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)
        var.dlgcalendar.Calendar.clicked.connect(ventas.Ventas.cargarFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()
        self.setWindowTitle('Abrir Archivo')
        self.setModal(True)

class PrintDialogAbrir(QtPrintSupport.QPrintDialog):
    def __init__(self):
        super(PrintDialogAbrir, self).__init__()

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgsalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()
        var.dlgImprimir = PrintDialogAbrir()

        '''
        colección de datos
        '''
        var.rbtsex = (var.ui.rbtFem, var.ui.rbtMasc)
        var.chkpago = (var.ui.chkEfec, var.ui.chkTar, var.ui.chkTrans)
        clients.Clientes.valoresSpin()
        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        events.Eventos.cargarProv(self)
        '''
        conexion de eventos con los objetos
        estamos conectando el código con la interfaz gráfico
        botones formulario cliente
        '''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarCli)
        var.ui.btnBajaCli.clicked.connect(clients.Clientes.bajaCliente)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCliente)
        var.ui.btnReloadCli.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnBuscarCli.clicked.connect(clients.Clientes.buscarCli)
        '''
        Conecion eventos de productos
        '''
        var.ui.btnAltaProd.clicked.connect(Products.Products.altaProducto)
        var.ui.btnLimpiarProd.clicked.connect(Products.Products.limpiarProd)
        var.ui.btnBajaProd.clicked.connect(Products.Products.BajaProd)
        var.ui.btnModifProd.clicked.connect(Products.Products.ModificarProd)
        var.ui.btnSalirProd.clicked.connect(events.Eventos.Salir)

        '''
        Conexion a eventos de facturacion
        '''
        var.ui.btnCalendario.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnFacturar.clicked.connect(ventas.Ventas.altafactura)
        var.ui.btnAnular.clicked.connect(ventas.Ventas.BajaFactura)
        var.ui.btnRefresh.clicked.connect(ventas.Ventas.reloadFact)
        var.ui.btnBuscarFact.clicked.connect(ventas.Ventas.buscarfacClientes)
        var.ui.btnAceptarventa.clicked.connect(ventas.Ventas.venta)
        var.ui.btnCancelar.clicked.connect(ventas.Ventas.BajaVenta)

        '''Tabla clientes eventos'''
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        '''Tabla Productos eventos'''
        var.ui.tableProd.clicked.connect(Products.Products.cargarProd)
        var.ui.tableProd.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        '''Tabla Facturas eventos'''
        var.ui.tableFechaFact.clicked.connect(ventas.Ventas.cargarFactura)
        var.ui.tableFechaFact.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tableFechaFact.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabFact.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tableFechaFact.clicked.connect(ventas.Ventas.mostrarVentasfac)

        ''' ToolBar'''
        var.ui.ToolbarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.ToolBarBackup.triggered.connect(events.Eventos.Backup)
        var.ui.ToolBarAbrirDir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.ToolBarPrinter.triggered.connect(events.Eventos.AbrirPrinter)
        var.ui.ToollBarRecBackup.triggered.connect(events.Eventos.restaurarBD)

        '''Menu bar'''
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        #var.ui.editDni.editingFinished.connect(lambda: clients.Clientes.validoDni)

        '''Status Bar'''
        var.ui.statusBar.addPermanentWidget(var.ui.lblstatus, 1)
        var.ui.statusBar.addPermanentWidget(var.ui.lblstatusdate, 2)
        var.ui.lblstatus.setStyleSheet('QLabel {color: red; font: bold;}')
        var.ui.lblstatus.setText('Bienvenido a 2º DAM')
        fecha = date.today()
        var.ui.lblstatusdate.setStyleSheet('QLabel {color: black; font: bold;}')
        var.ui.lblstatusdate.setText(fecha.strftime('%A %d de %B del %Y'))
        var.ui.btnBajaCli.clicked.connect(Products.Products.altaProducto)


        '''
        módulos de impresión
        '''
        var.ui.menubarReportCli.triggered.connect(printer.Printer.reportCli)
        var.ui.MenuBarReportProd.triggered.connect(printer.Printer.reportProduc)
        var.ui.MenuBarReportFac.triggered.connect(printer.Printer.reportFac)
        '''
        
        módulos conexion base datos
        '''
        conexion.Conexion.db_connect(var.filebd)
        # conexion.Conexion()
        conexion.Conexion.mostrarClientes()
        conexion.Conexion.mostrarProducts()
        conexion.Conexion.mostrarFacturas()
        var.ui.TabWidget.setCurrentIndex(0)

    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
