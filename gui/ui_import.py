# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import.ui'
#
# Created: Wed Aug 28 14:20:26 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(805, 570)
        Dialog.setMaximumSize(QtCore.QSize(805, 570))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.layergroupComboBox = QtGui.QComboBox(self.tab)
        self.layergroupComboBox.setObjectName(_fromUtf8("layergroupComboBox"))
        self.horizontalLayout_5.addWidget(self.layergroupComboBox)
        self.addGroupButton = QtGui.QToolButton(self.tab)
        self.addGroupButton.setEnabled(False)
        self.addGroupButton.setObjectName(_fromUtf8("addGroupButton"))
        self.horizontalLayout_5.addWidget(self.addGroupButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.layerList = QtGui.QListWidget(self.tab)
        self.layerList.setEnabled(True)
        self.layerList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.layerList.setObjectName(_fromUtf8("layerList"))
        self.horizontalLayout_2.addWidget(self.layerList)
        self.styleList = QtGui.QListWidget(self.tab)
        self.styleList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.styleList.setObjectName(_fromUtf8("styleList"))
        self.horizontalLayout_2.addWidget(self.styleList)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.addLayerButton = QtGui.QPushButton(self.tab)
        self.addLayerButton.setObjectName(_fromUtf8("addLayerButton"))
        self.verticalLayout_3.addWidget(self.addLayerButton)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.workspaceComboBox = QtGui.QComboBox(self.tab_2)
        self.workspaceComboBox.setObjectName(_fromUtf8("workspaceComboBox"))
        self.verticalLayout_2.addWidget(self.workspaceComboBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.storeList = QtGui.QListWidget(self.tab_2)
        self.storeList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.storeList.setObjectName(_fromUtf8("storeList"))
        self.horizontalLayout_3.addWidget(self.storeList)
        self.resourceList = QtGui.QListWidget(self.tab_2)
        self.resourceList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.resourceList.setObjectName(_fromUtf8("resourceList"))
        self.horizontalLayout_3.addWidget(self.resourceList)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.addResourceButton = QtGui.QPushButton(self.tab_2)
        self.addResourceButton.setObjectName(_fromUtf8("addResourceButton"))
        self.verticalLayout_2.addWidget(self.addResourceButton)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.cartList = QtGui.QListWidget(self.groupBox)
        self.cartList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.cartList.setObjectName(_fromUtf8("cartList"))
        self.verticalLayout_5.addWidget(self.cartList)
        self.removeFromCartButton = QtGui.QPushButton(self.groupBox)
        self.removeFromCartButton.setObjectName(_fromUtf8("removeFromCartButton"))
        self.verticalLayout_5.addWidget(self.removeFromCartButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.layergroupComboBox, self.tabWidget)
        Dialog.setTabOrder(self.tabWidget, self.layerList)
        Dialog.setTabOrder(self.layerList, self.styleList)
        Dialog.setTabOrder(self.styleList, self.workspaceComboBox)
        Dialog.setTabOrder(self.workspaceComboBox, self.storeList)
        Dialog.setTabOrder(self.storeList, self.resourceList)
        Dialog.setTabOrder(self.resourceList, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.addGroupButton.setText(_translate("Dialog", "Add group", None))
        self.addLayerButton.setText(_translate("Dialog", "Add to Cart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Layers", None))
        self.addResourceButton.setText(_translate("Dialog", "Add to Cart", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Workspaces", None))
        self.groupBox.setTitle(_translate("Dialog", "Cart ", None))
        self.removeFromCartButton.setText(_translate("Dialog", "Remove from Cart", None))

