# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AdminPanelUI.ui'
#
# Created: Sun May 25 13:07:19 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(804, 817)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.tabWidgetPermitidos = QtGui.QTabWidget(self.centralwidget)
        self.tabWidgetPermitidos.setObjectName(_fromUtf8("tabWidgetPermitidos"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout = QtGui.QGridLayout(self.tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setMouseTracking(False)
        self.groupBox_2.setAutoFillBackground(False)
        self.groupBox_2.setStyleSheet(_fromUtf8(""))
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tableViewPermitidos = QtGui.QTableView(self.groupBox_2)
        self.tableViewPermitidos.setMaximumSize(QtCore.QSize(738, 591))
        self.tableViewPermitidos.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tableViewPermitidos.setAutoFillBackground(True)
        self.tableViewPermitidos.setObjectName(_fromUtf8("tableViewPermitidos"))
        self.tableViewPermitidos.horizontalHeader().setStretchLastSection(True)
        self.tableViewPermitidos.verticalHeader().setCascadingSectionResizes(True)
        self.gridLayout_5.addWidget(self.tableViewPermitidos, 3, 0, 1, 3)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_5.addWidget(self.label_3, 0, 0, 1, 2)
        self.lineEditPermitidos = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditPermitidos.setObjectName(_fromUtf8("lineEditPermitidos"))
        self.gridLayout_5.addWidget(self.lineEditPermitidos, 1, 0, 1, 1)
        self.pushButtonPermitir = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonPermitir.setObjectName(_fromUtf8("pushButtonPermitir"))
        self.gridLayout_5.addWidget(self.pushButtonPermitir, 1, 1, 1, 1)
        self.botonEliminarPermitido = QtGui.QPushButton(self.groupBox_2)
        self.botonEliminarPermitido.setEnabled(True)
        self.botonEliminarPermitido.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.botonEliminarPermitido.setObjectName(_fromUtf8("botonEliminarPermitido"))
        self.gridLayout_5.addWidget(self.botonEliminarPermitido, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 4, 1, 1, 1)
        self.labelErrorPermitidos = QtGui.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelErrorPermitidos.setFont(font)
        self.labelErrorPermitidos.setStyleSheet(_fromUtf8("background-color:yellow"))
        self.labelErrorPermitidos.setObjectName(_fromUtf8("labelErrorPermitidos"))
        self.gridLayout_5.addWidget(self.labelErrorPermitidos, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.tabWidgetPermitidos.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.groupBox.setFont(font)
        self.groupBox.setMouseTracking(False)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(_fromUtf8(""))
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 7, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 2)
        self.lineEditDenegados = QtGui.QLineEdit(self.groupBox)
        self.lineEditDenegados.setStyleSheet(_fromUtf8(""))
        self.lineEditDenegados.setText(_fromUtf8(""))
        self.lineEditDenegados.setObjectName(_fromUtf8("lineEditDenegados"))
        self.gridLayout_2.addWidget(self.lineEditDenegados, 4, 0, 1, 1)
        self.pushButtonDenegar = QtGui.QPushButton(self.groupBox)
        self.pushButtonDenegar.setObjectName(_fromUtf8("pushButtonDenegar"))
        self.gridLayout_2.addWidget(self.pushButtonDenegar, 4, 1, 1, 1)
        self.tableViewDenegados = QtGui.QTableView(self.groupBox)
        self.tableViewDenegados.setObjectName(_fromUtf8("tableViewDenegados"))
        self.tableViewDenegados.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.tableViewDenegados, 6, 0, 1, 2)
        self.botonEliminarDenegado = QtGui.QPushButton(self.groupBox)
        self.botonEliminarDenegado.setEnabled(True)
        self.botonEliminarDenegado.setObjectName(_fromUtf8("botonEliminarDenegado"))
        self.gridLayout_2.addWidget(self.botonEliminarDenegado, 7, 0, 1, 1)
        self.labelErrorDenegados = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelErrorDenegados.setFont(font)
        self.labelErrorDenegados.setStyleSheet(_fromUtf8("background-color:yellow"))
        self.labelErrorDenegados.setTextFormat(QtCore.Qt.AutoText)
        self.labelErrorDenegados.setObjectName(_fromUtf8("labelErrorDenegados"))
        self.gridLayout_2.addWidget(self.labelErrorDenegados, 5, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tabWidgetPermitidos.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_4.addWidget(self.tabWidgetPermitidos, 0, 0, 1, 3)
        self.botonCancelar = QtGui.QPushButton(self.centralwidget)
        self.botonCancelar.setObjectName(_fromUtf8("botonCancelar"))
        self.gridLayout_4.addWidget(self.botonCancelar, 2, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(601, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 2, 0, 1, 1)
        self.botonGuardar = QtGui.QPushButton(self.centralwidget)
        self.botonGuardar.setObjectName(_fromUtf8("botonGuardar"))
        self.gridLayout_4.addWidget(self.botonGuardar, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionAgregar_Dominios_Permtidos_Denegados = QtGui.QAction(MainWindow)
        self.actionAgregar_Dominios_Permtidos_Denegados.setObjectName(_fromUtf8("actionAgregar_Dominios_Permtidos_Denegados"))
        self.actionListar_Dominios_Permtidos_Denegados = QtGui.QAction(MainWindow)
        self.actionListar_Dominios_Permtidos_Denegados.setObjectName(_fromUtf8("actionListar_Dominios_Permtidos_Denegados"))

        self.retranslateUi(MainWindow)
        self.tabWidgetPermitidos.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Kerberus Control Parental - Admin Panel", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Agregar nuevo dominio permitido", None))
        self.label_3.setText(_translate("MainWindow", "Dominio:", None))
        self.lineEditPermitidos.setPlaceholderText(_translate("MainWindow", "www.dominiopermitido.com", None))
        self.pushButtonPermitir.setText(_translate("MainWindow", "Permitir", None))
        self.botonEliminarPermitido.setText(_translate("MainWindow", "Eliminar", None))
        self.labelErrorPermitidos.setText(_translate("MainWindow", "El dominio debe ser de la forma: www.dominio.com", None))
        self.tabWidgetPermitidos.setTabText(self.tabWidgetPermitidos.indexOf(self.tab), _translate("MainWindow", "Dominios Permitidos", None))
        self.groupBox.setTitle(_translate("MainWindow", "Agregar nuevo dominio denegado", None))
        self.label_2.setText(_translate("MainWindow", "Dominio:", None))
        self.lineEditDenegados.setPlaceholderText(_translate("MainWindow", "www.dominiodenegado.com", None))
        self.pushButtonDenegar.setText(_translate("MainWindow", "Denegar", None))
        self.botonEliminarDenegado.setText(_translate("MainWindow", "Eliminar", None))
        self.labelErrorDenegados.setText(_translate("MainWindow", "El dominio debe ser de la forma: www.dominio.com", None))
        self.tabWidgetPermitidos.setTabText(self.tabWidgetPermitidos.indexOf(self.tab_2), _translate("MainWindow", "Dominios Denegados", None))
        self.botonCancelar.setText(_translate("MainWindow", "Salir", None))
        self.botonGuardar.setText(_translate("MainWindow", "Aplicar", None))
        self.actionAgregar_Dominios_Permtidos_Denegados.setText(_translate("MainWindow", "Agregar Dominios Permtidos/Denegados", None))
        self.actionListar_Dominios_Permtidos_Denegados.setText(_translate("MainWindow", "Listar Dominios Permtidos/Denegados", None))

