# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pick_target.ui'
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
        Dialog.resize(660, 390)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.newEntryButton = QtGui.QPushButton(Dialog)
        self.newEntryButton.setObjectName(_fromUtf8("newEntryButton"))
        self.verticalLayout_2.addWidget(self.newEntryButton)
        self.targetList = QtGui.QListWidget(Dialog)
        self.targetList.setObjectName(_fromUtf8("targetList"))
        self.verticalLayout_2.addWidget(self.targetList)
        self.debugCheckBox = QtGui.QCheckBox(Dialog)
        self.debugCheckBox.setObjectName(_fromUtf8("debugCheckBox"))
        self.verticalLayout_2.addWidget(self.debugCheckBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.commonConfig = QtGui.QFormLayout()
        self.commonConfig.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.commonConfig.setObjectName(_fromUtf8("commonConfig"))
        self.nameLabel = QtGui.QLabel(Dialog)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.commonConfig.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.nameLineEdit = QtGui.QLineEdit(Dialog)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.commonConfig.setWidget(0, QtGui.QFormLayout.FieldRole, self.nameLineEdit)
        self.urlLabel = QtGui.QLabel(Dialog)
        self.urlLabel.setObjectName(_fromUtf8("urlLabel"))
        self.commonConfig.setWidget(1, QtGui.QFormLayout.LabelRole, self.urlLabel)
        self.urlLineEdit = QtGui.QLineEdit(Dialog)
        self.urlLineEdit.setObjectName(_fromUtf8("urlLineEdit"))
        self.commonConfig.setWidget(1, QtGui.QFormLayout.FieldRole, self.urlLineEdit)
        self.tweakForLabel = QtGui.QLabel(Dialog)
        self.tweakForLabel.setObjectName(_fromUtf8("tweakForLabel"))
        self.commonConfig.setWidget(2, QtGui.QFormLayout.LabelRole, self.tweakForLabel)
        self.tweakForComboBox = QtGui.QComboBox(Dialog)
        self.tweakForComboBox.setObjectName(_fromUtf8("tweakForComboBox"))
        self.tweakForComboBox.addItem(_fromUtf8(""))
        self.tweakForComboBox.addItem(_fromUtf8(""))
        self.tweakForComboBox.addItem(_fromUtf8(""))
        self.commonConfig.setWidget(2, QtGui.QFormLayout.FieldRole, self.tweakForComboBox)
        self.useBasicAuthLabel = QtGui.QLabel(Dialog)
        self.useBasicAuthLabel.setObjectName(_fromUtf8("useBasicAuthLabel"))
        self.commonConfig.setWidget(3, QtGui.QFormLayout.LabelRole, self.useBasicAuthLabel)
        self.useBasicAuthCheckBox = QtGui.QCheckBox(Dialog)
        self.useBasicAuthCheckBox.setObjectName(_fromUtf8("useBasicAuthCheckBox"))
        self.commonConfig.setWidget(3, QtGui.QFormLayout.FieldRole, self.useBasicAuthCheckBox)
        self.userLabel = QtGui.QLabel(Dialog)
        self.userLabel.setObjectName(_fromUtf8("userLabel"))
        self.commonConfig.setWidget(5, QtGui.QFormLayout.LabelRole, self.userLabel)
        self.userLineEdit = QtGui.QLineEdit(Dialog)
        self.userLineEdit.setObjectName(_fromUtf8("userLineEdit"))
        self.commonConfig.setWidget(5, QtGui.QFormLayout.FieldRole, self.userLineEdit)
        self.passwordLabel = QtGui.QLabel(Dialog)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.commonConfig.setWidget(6, QtGui.QFormLayout.LabelRole, self.passwordLabel)
        self.passwordLineEdit = QtGui.QLineEdit(Dialog)
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.commonConfig.setWidget(6, QtGui.QFormLayout.FieldRole, self.passwordLineEdit)
        self.verticalLayout.addLayout(self.commonConfig)
        self.tweakText = QtGui.QTextBrowser(Dialog)
        self.tweakText.setObjectName(_fromUtf8("tweakText"))
        self.verticalLayout.addWidget(self.tweakText)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.resetButton = QtGui.QPushButton(Dialog)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.horizontalLayout_3.addWidget(self.resetButton)
        self.closeButton = QtGui.QPushButton(Dialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_3.addWidget(self.closeButton)
        self.deleteButton = QtGui.QPushButton(Dialog)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout_3.addWidget(self.deleteButton)
        self.importButton = QtGui.QPushButton(Dialog)
        self.importButton.setObjectName(_fromUtf8("importButton"))
        self.horizontalLayout_3.addWidget(self.importButton)
        self.publishButton = QtGui.QPushButton(Dialog)
        self.publishButton.setObjectName(_fromUtf8("publishButton"))
        self.horizontalLayout_3.addWidget(self.publishButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.newEntryButton.setText(_translate("Dialog", "New", None))
        self.debugCheckBox.setText(_translate("Dialog", "debug", None))
        self.nameLabel.setText(_translate("Dialog", "name", None))
        self.urlLabel.setText(_translate("Dialog", "url", None))
        self.tweakForLabel.setText(_translate("Dialog", "tweak for", None))
        self.tweakForComboBox.setItemText(0, _translate("Dialog", "none", None))
        self.tweakForComboBox.setItemText(1, _translate("Dialog", "mra", None))
        self.tweakForComboBox.setItemText(2, _translate("Dialog", "geoserver", None))
        self.useBasicAuthLabel.setText(_translate("Dialog", "use basic auth", None))
        self.userLabel.setText(_translate("Dialog", "user", None))
        self.passwordLabel.setText(_translate("Dialog", "password", None))
        self.resetButton.setText(_translate("Dialog", "Reset", None))
        self.closeButton.setText(_translate("Dialog", "Close", None))
        self.deleteButton.setText(_translate("Dialog", "Delete", None))
        self.importButton.setText(_translate("Dialog", "Import", None))
        self.publishButton.setText(_translate("Dialog", "Publish", None))

