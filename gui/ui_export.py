# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export.ui'
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
        Dialog.resize(658, 287)
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.selectVisibleButton = QtGui.QPushButton(Dialog)
        self.selectVisibleButton.setObjectName(_fromUtf8("selectVisibleButton"))
        self.horizontalLayout_2.addWidget(self.selectVisibleButton)
        self.selectAllButton = QtGui.QPushButton(Dialog)
        self.selectAllButton.setObjectName(_fromUtf8("selectAllButton"))
        self.horizontalLayout_2.addWidget(self.selectAllButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.layerList = QtGui.QListWidget(Dialog)
        self.layerList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.layerList.setObjectName(_fromUtf8("layerList"))
        self.verticalLayout.addWidget(self.layerList)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.reUseCreatedStoresLabel = QtGui.QLabel(Dialog)
        self.reUseCreatedStoresLabel.setObjectName(_fromUtf8("reUseCreatedStoresLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.reUseCreatedStoresLabel)
        self.reUseCreatedStoresCheckBox = QtGui.QCheckBox(Dialog)
        self.reUseCreatedStoresCheckBox.setChecked(True)
        self.reUseCreatedStoresCheckBox.setObjectName(_fromUtf8("reUseCreatedStoresCheckBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.reUseCreatedStoresCheckBox)
        self.askBeforeChoosingStoresLabel = QtGui.QLabel(Dialog)
        self.askBeforeChoosingStoresLabel.setObjectName(_fromUtf8("askBeforeChoosingStoresLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.askBeforeChoosingStoresLabel)
        self.askBeforeChoosingStoresCheckBox = QtGui.QCheckBox(Dialog)
        self.askBeforeChoosingStoresCheckBox.setObjectName(_fromUtf8("askBeforeChoosingStoresCheckBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.askBeforeChoosingStoresCheckBox)
        self.workspaceLabel = QtGui.QLabel(Dialog)
        self.workspaceLabel.setObjectName(_fromUtf8("workspaceLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.workspaceLabel)
        self.workspaceComboBox = QtGui.QComboBox(Dialog)
        self.workspaceComboBox.setEditable(True)
        self.workspaceComboBox.setObjectName(_fromUtf8("workspaceComboBox"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.workspaceComboBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setEnabled(False)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout_2.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.selectVisibleButton.setText(_translate("Dialog", "visible layers", None))
        self.selectAllButton.setText(_translate("Dialog", "all layers", None))
        self.reUseCreatedStoresLabel.setText(_translate("Dialog", "Auto create stores", None))
        self.askBeforeChoosingStoresLabel.setText(_translate("Dialog", "Manual store selection", None))
        self.workspaceLabel.setText(_translate("Dialog", "workspace", None))
        self.progressBar.setFormat(_translate("Dialog", "%p%", None))

