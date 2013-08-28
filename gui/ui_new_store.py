# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_store.ui'
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
        Dialog.resize(532, 343)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.currentLayerLabel = QtGui.QLabel(Dialog)
        self.currentLayerLabel.setObjectName(_fromUtf8("currentLayerLabel"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.currentLayerLabel)
        self.currentLayerLineEdit = QtGui.QLineEdit(Dialog)
        self.currentLayerLineEdit.setReadOnly(True)
        self.currentLayerLineEdit.setObjectName(_fromUtf8("currentLayerLineEdit"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.currentLayerLineEdit)
        self.storeNameLabel = QtGui.QLabel(Dialog)
        self.storeNameLabel.setObjectName(_fromUtf8("storeNameLabel"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.storeNameLabel)
        self.storeNameLineEdit = QtGui.QLineEdit(Dialog)
        self.storeNameLineEdit.setReadOnly(True)
        self.storeNameLineEdit.setObjectName(_fromUtf8("storeNameLineEdit"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.storeNameLineEdit)
        self.storeDetailsLabel = QtGui.QLabel(Dialog)
        self.storeDetailsLabel.setObjectName(_fromUtf8("storeDetailsLabel"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.storeDetailsLabel)
        self.storeDetailsTextBrowser = QtGui.QTextBrowser(Dialog)
        self.storeDetailsTextBrowser.setObjectName(_fromUtf8("storeDetailsTextBrowser"))
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.storeDetailsTextBrowser)
        self.verticalLayout_2.addLayout(self.formLayout_4)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.formLayout_2 = QtGui.QFormLayout(self.tab)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.nameLabel = QtGui.QLabel(self.tab)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.nameComboBox = QtGui.QComboBox(self.tab)
        self.nameComboBox.setObjectName(_fromUtf8("nameComboBox"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameComboBox)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.formLayout_5 = QtGui.QFormLayout(self.tab_2)
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.nameLabel_2 = QtGui.QLabel(self.tab_2)
        self.nameLabel_2.setObjectName(_fromUtf8("nameLabel_2"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel_2)
        self.nameLineEdit = QtGui.QLineEdit(self.tab_2)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameLineEdit)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.alwaysReUseThisStoreForThisDataSourceCheckBox = QtGui.QCheckBox(Dialog)
        self.alwaysReUseThisStoreForThisDataSourceCheckBox.setObjectName(_fromUtf8("alwaysReUseThisStoreForThisDataSourceCheckBox"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.alwaysReUseThisStoreForThisDataSourceCheckBox)
        self.alwaysReUseThisStoreForThisDataSourceLabel = QtGui.QLabel(Dialog)
        self.alwaysReUseThisStoreForThisDataSourceLabel.setObjectName(_fromUtf8("alwaysReUseThisStoreForThisDataSourceLabel"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.alwaysReUseThisStoreForThisDataSourceLabel)
        self.verticalLayout_2.addLayout(self.formLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.currentLayerLabel.setText(_translate("Dialog", "current layer", None))
        self.storeNameLabel.setText(_translate("Dialog", "store name", None))
        self.storeDetailsLabel.setText(_translate("Dialog", "store details", None))
        self.label.setText(_translate("Dialog", "What remote datastore should we use for this data source?", None))
        self.nameLabel.setText(_translate("Dialog", "name", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Existing Store", None))
        self.nameLabel_2.setText(_translate("Dialog", "name", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "New Store", None))
        self.alwaysReUseThisStoreForThisDataSourceLabel.setText(_translate("Dialog", "Always use this store for this data source.", None))

