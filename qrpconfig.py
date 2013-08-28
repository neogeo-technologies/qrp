#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                       #
#   QGIS Rest Publisher is a QGIS plugin that facilitates exporting or  #
#   importing from remote servers with a REST API.                      #
#                                                                       #
#   Copyright (C) 2011-2013 Neogeo Technologies.                        #
#                                                                       #
#   This file is part of QGIS Rest Publisher.                           #
#                                                                       #
#   QGIS Rest Publisher is free software: you can redistribute it       #
#   and/or modify it under the terms of the GNU General Public License  #
#   as published by the Free Software Foundation, either version 3 of   #
#   the License, or (at your option) any later version.                 #
#                                                                       #
#   QGIS Rest Publisher is distributed in the hope that it will be      #
#   useful, but WITHOUT ANY WARRANTY; without even the implied warranty #
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the     #
#   GNU General Public License for more details.                        #
#                                                                       #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
import qgis.utils

import os.path

import qrpimport
import qrpexport
from helpers import catch_httperrors

from gui import ui_pick_target

import remote
import restclient

def log(f):
    def w(*a, **k):
        print "Entering %s(%s)" % (f.__name__, ", ".join([str(v) for v in a] + ["%s=%s" % (n, v) for n, v in k]))
        r = f(*a, **k)
        print "Exiting %s" % f.__name__
        return r
    return w

class QRPConfig(QDialog, ui_pick_target.Ui_Dialog):
    def __init__(self, iface):
        # First init QDialogand Ui_Dialog
        QDialog.__init__(self)
        self.setupUi(self)

        # Then our own stuff:

        self.iface = iface
        # TODO: Find a way to put this file somewhere where it is not disturbing.
        self.remotes = remote.Storage(os.path.join(os.path.dirname(__file__), "qrpdb"))
        self.remote = None

        # Init the rest of the interface.
        self.targetList.addItems(self.remotes.keys())

        # Init tweaking.
        self.setTweakFor()

        # Now we are ready to setup some callbacks.

        self.newEntryButton.clicked.connect(self.btn_new)

        self.resetButton.clicked.connect(self.btn_reset)
        self.closeButton.clicked.connect(self.btn_close)
        self.deleteButton.clicked.connect(self.btn_delete)
        self.importButton.clicked.connect(self.btn_fetch)
        self.publishButton.clicked.connect(self.btn_publish)

        self.targetList.currentItemChanged.connect(self.changeRemote)
        self.tweakForComboBox.currentIndexChanged.connect(self.tweakFor)

        if self.remotes:
            self.targetList.setCurrentRow(0)

    #
    # Application Helpers
    #

    @log
    def saveRemote(self):
        """Sync current remote with forms values and save it."""

        name = self.nameLineEdit.text().strip()
        if not name:
            if not self.urlLineEdit.text():
                return
            name = "New Remote"

        print "saving name = %s" % name
        if not self.remote:
            self.remote = remote.Remote()

        # Make sure the name is not used.
        if name != self.remote.name and name in self.remotes:
            i = 1
            while True:
                newname = "%s_%d" % (name, i)
                if newname not in self.remotes:
                    break
                i += 1
            self.nameLineEdit.setText(newname)
            name = newname

        self.remote.name = name
        self.remote.url = self.urlLineEdit.text()

        self.remote.basicauth = self.useBasicAuthCheckBox.isChecked()
        self.remote.user = self.userLineEdit.text()
        self.remote.password = self.passwordLineEdit.text()

        flavour = self.tweakForComboBox.currentText()
        self.remote.flavour = None if flavour == "none" else flavour

        if name not in self.remotes:
            self.targetList.addItem(name)

        assert self.remote.name == name
        self.remotes[name] = self.remote
        self.remotes.save()

    @log
    def loadRemote(self, name):
        """Load a new remote from name, sync form with it."""

        print "Loading remote %s:" % name
        print "DB == %s" % self.remotes
        self.remote = self.remotes[name]
        assert self.remote.name == name
        print "\t new name %s" % (self.remote.name)
        self.nameLineEdit.setText(self.remote.name)
        self.urlLineEdit.setText(self.remote.url)

        self.useBasicAuthCheckBox.setChecked(self.remote.basicauth)
        self.userLineEdit.setText(self.remote.user)
        self.passwordLineEdit.setText(self.remote.password)

        self.setTweakFor(self.remote.flavour)

    @log
    def newRemote(self):
        """Clear form and set a blank remote."""

        self.nameLineEdit.clear()
        self.urlLineEdit.clear()
        self.useBasicAuthCheckBox.setChecked(False)
        self.userLineEdit.clear()
        self.passwordLineEdit.clear()

        self.remote = None
        self.targetList.clearSelection()

        self.nameLineEdit.setFocus()

    def setTweakFor(self, name=None):
        self.tweakForComboBox.setCurrentIndex(self.tweakForComboBox.findText(name or "none"))

    def getAPI(self):
        url = self.urlLineEdit.text().strip()

        verbose = self.debugCheckBox.isChecked()

        clazz = {"mra": restclient.MRA, "geoserver": restclient.geoserverREST}.get(self.remote.flavour, restclient.RestAPI)
        try:
            api = clazz(url, verbose=verbose, username=self.userLineEdit.text(), password=self.passwordLineEdit.text())
        except BaseException:
            QMessageBox.warning("error", "We couldn't access the API, maybe the information (url, ...) is wrong.")
            return None
        return api

    #
    # Callbacks
    #

    @log
    def changeRemote(self, curr, prev):
        print "[remotes]:", self.remotes
        if curr:
            self.saveRemote()
            self.loadRemote(curr.text())

    @log
    def tweakFor(self, idx):
        name = self.tweakForComboBox.currentText()

        if name == "none":
            txt = "By <b>default</b> the \"standard\" RESTful API used by geoserver " \
                "and MRA is used, if for some reason something does not work, you " \
                "might try to tweak the API for your specific publishing platform."
        elif name == "mra":
            txt = "<b>MapServer REST API</b> is a python wrapper around MapServer " \
                "which allows to manipulate a mapfile in a RESTFul way. It " \
                "has been developped to match as close as possible the way " \
                "the GeoServer REST API acts."
        elif name == "geoserver":
            txt = "<b>GeoServer</b> is an open source software server written in "  \
                "Java that allows users to share and edit geospatial data. " \
                "Designed for interoperability, it publishes data from any " \
                "major spatial data source using open standards."
        else:
            txt = ""

        self.tweakText.setText(txt)

    @log
    @catch_httperrors
    def btn_new(self, _):
        print "[remotes]:", self.remotes
        self.saveRemote()
        self.newRemote()

    @log
    @catch_httperrors
    def btn_reset(self, _):
        print "[remotes]:", self.remotes
        curr = self.targetList.selectedItems()
        if curr:
            self.loadRemote(curr[0].text())
        else:
            self.newRemote()

    @log
    @catch_httperrors
    def btn_close(self, _):
        print "[remotes]:", self.remotes
        self.saveRemote()
        super(QRPConfig, self).close()

    @log
    @catch_httperrors
    def btn_delete(self, _):
        print "[remotes]:", self.remotes
        if self.remote and self.remote.name in self.remotes:
            del self.remotes[self.remote.name]
            self.remote = None
            self.remotes.save()
            self.targetList.clear()
            self.targetList.addItems(self.remotes.keys())

        self.newRemote()

    @log
    @catch_httperrors
    def btn_fetch(self, _):
        print "[remotes]:", self.remotes
        self.saveRemote()

        api = self.getAPI()
        if not api: return

        dlg_import = qrpimport.QRPImport(self.iface, api)
        result = dlg_import.exec_()

    @log
    @catch_httperrors
    def btn_publish(self, _):
        print "[remotes]:", self.remotes
        self.saveRemote()

        api = self.getAPI()
        if not api: return

        dlg_export = qrpexport.QRPExport(self.iface, api)
        result = dlg_export.exec_()

