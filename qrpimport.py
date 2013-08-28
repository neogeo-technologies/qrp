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

from helpers import catch_httperrors
from gui import ui_import

import os
import tempfile

class LayerGroup(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "lg:%s" % self.name

    def setup(self, main):
        lnames = main.map["layergroups"][self.name]

        # Fetch sld for layer group.
        sld = None

        legend = qgis.utils.iface.legendInterface()

        # # Setup group.
        if self.name in legend.groups():
            i = 1
            while "%s%d" % (self.name, i) in legend.groups():
                i += 1
            self.name += "%s%d" % (self.name, i)
        group_idx = legend.addGroup(self.name)

        for lname in lnames:
            l = Layer(lname)
            qlayer = l.setup(main, sld=sld)
            legend.moveLayer(qlayer, group_idx)


class Layer(object):
    def __init__(self, name, style=None):
        self.name = name
        self.style = style

    def __str__(self):
        if self.style:
            return "l:%s (style:%s)" % (self.name, self.style)
        else:
            return "l:%s (default style)" % self.name

    def setup(self, main, sld=None):
        # Fetch info

        layer = main.api.map_layer(self.name)
        clazz = {"featuretypes": FeatureType, "coverages": Coverage}[layer["resource"]["type"]]

        # If no sld, fetch our own.

        if sld == None:
            sld = main.api.get_style_sld(self.style or layer["default_style"])

        sld_fd, sld_path = tempfile.mkstemp(suffix=".sld")
        os.write(sld_fd, sld)
        os.close(sld_fd)

        # Build a FeatureType or Coverage
        resource = clazz(layer["resource"]["workspace"], layer["resource"]["store"], layer["resource"]["name"])
        layer = resource.setup(main, sld=sld)

        layer.loadSldStyle(sld_path)
        os.remove(sld_path)

        return layer

class FeatureType(object):
    def __init__(self, ws, ds, name):
        self.ws, self.ds, self.name = ws, ds, name

    def __str__(self):
        return "ws:%s:ds:%s:%s" % (self.ws, self.ds, self.name)

    def setup(self, main, sld=None):
        # Fetch info
        # Apply sld.

        ds = main.api.get_datastore(self.ws, self.ds)[1]
        ft = main.api.get_featuretype(self.ws, self.ds, self.name)[1]

        cp = ds["connectionParameters"]

        uri = QgsDataSourceURI()

        try:
            host, port, db, user = cp["host"], cp["port"], cp["database"], cp["user"]
        except KeyError:
            raise NotImplemented("Only Database importation is implemented.")


        password = cp.get("passwd", cp.get("password", ""))
        text, ok = QInputDialog.getText(main, "password", "Please enter password for user %s on database %s on %s:%s" %
                                        (user, db, host, port), QLineEdit.Password)
        assert ok

        password = text
        print "Using password: %s" % password

        uri.setConnection(host, port, db, user, password)

        schema = cp.get("schema")
        if schema:
            table = ft.get("nativeName", ft["name"])
        else:
            split = ft.get("nativeName", ft["name"]).split(".", 2)
            schema, table = split if len(split) == 2 else ("", split[0])

        # TODO: Figure out the_geom.
        uri.setDataSource(schema, table, "the_geom")

        print "Creating layer:", uri.uri()
        vlayer = QgsVectorLayer(uri.uri(), self.name, "postgres")

        # Finaly add it to the registery for rendering.
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)

        return vlayer

class Coverage(object):
    def __init__(self, ws, cs, name):
        self.ws, self.cs, self.name = ws, cs, name

    def __str__(self):
        return "ws:%s:cs:%s:%s" % (self.ws, self.cs, self.name)

    def setup(self, main, sld=None):
        # Fetch info
        # Apply sld.
        raise NotImplemented("Coverage importation is not yet implemented..")


class QRPImport(QDialog, ui_import.Ui_Dialog):
    def __init__(self, iface, api):
        # First init QDialogand Ui_Dialog
        QDialog.__init__(self)
        self.setupUi(self)

        # Then our own stuff:

        self.iface = iface
        self.api = api


        self.progressBar.hide()

        self.addGroupButton.clicked.connect(self.btn_addGroup)
        self.addLayerButton.clicked.connect(self.btn_addLayer)
        self.addResourceButton.clicked.connect(self.btn_addResource)
        self.removeFromCartButton.clicked.connect(self.btn_remove)

        self.layergroupComboBox.currentIndexChanged.connect(self.cbox_layergroup)
        self.workspaceComboBox.currentIndexChanged.connect(self.cbox_workspace)

        self.layerList.itemSelectionChanged.connect(self.change_layer)
        self.storeList.itemSelectionChanged.connect(self.change_store)

        self.connect(self.buttonBox, SIGNAL("rejected()"), self.close)
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.btn_ok)

        # init texts;

        self.map = api.map()
        self.cart = {}

        self.layergroupComboBox.addItem("(all)")
        self.layergroupComboBox.addItems(self.map["layergroups"].keys())

        self.workspaceComboBox.addItem("(all)")
        self.workspaceComboBox.addItems(self.map["workspaces"].keys())

        workspaces = {}

    #
    # Helpers
    #

    def add_to_cart(self, item):
        listItem = QListWidgetItem("%s" % item)
        self.cart[listItem] = item
        self.cartList.addItem(listItem)


    #
    # Callbacks
    #

    def btn_addGroup(self):
        self.add_to_cart(LayerGroup(self.layergroupComboBox.currentText()))

    def btn_addLayer(self):
        layers = self.layerList.selectedItems()
        styles = self.styleList.selectedItems()

        if len(layers) == 1 and styles:
            self.add_to_cart(Layer(layers[0].text(), styles[0].text()))
        else:
            for layer in layers:
                self.add_to_cart(Layer(layer.text()))

    def btn_addResource(self):
        selected = self.storeList.selectedItems()
        resources = self.resourceList.selectedItems()

        if self.workspaceComboBox.currentIndex():
            globalws = self.workspaceComboBox.currentText()
        else:
            globalws = None

        stores = []
        for store in selected:
            if globalws:
                st_type, st_name = store.text().split(":", 1)
                ws = globalws
            else:
                ws, st_type, st_name = store.text().split(":", 2)

            clazz = {"ds": FeatureType, "cs": Coverage}[st_type]
            st_type = {"ds": "datastores", "cs": "coveragestores"}[st_type]

            if len(selected) > 1 or not resources:
                allres = self.map["workspaces"][ws][st_type][st_name]
            else:
                allres = (res.text() for res in resources)

            for res in allres:
                self.add_to_cart(clazz(ws, st_name, res))

    def btn_remove(self):
        selected = self.cartList.selectedItems()
        items = [item for (listItem, item) in self.cart.iteritems() if listItem not in selected]

        self.cart.clear()
        self.cartList.clear()

        for item in items:
            self.add_to_cart(item)

    def cbox_layergroup(self, idx):
        self.layerList.clear()

        if idx == 0:
            self.layerList.addItems(sorted(self.map["layers"].keys()))
            self.addGroupButton.setEnabled(False)
        else:
            lg = self.layergroupComboBox.currentText()
            self.layerList.addItems(sorted(self.map["layergroups"][lg]))
            self.addGroupButton.setEnabled(True)

    def change_layer(self):
        self.styleList.clear()

        selected = self.layerList.selectedItems()
        if len(selected) == 1:
            self.styleList.addItems(sorted(self.map["layers"][selected[0].text()]["styles"]))
            self.styleList.setEnabled(True)
        elif selected:
            self.styleList.addItem("Default styles will be used.")
            self.styleList.setEnabled(False)

    def cbox_workspace(self, idx):
        self.storeList.clear()

        stores = []

        if idx == 0:
            for ws, details in self.map["workspaces"].iteritems():
                stores.extend(["%s:cs:%s" % (ws, c) for c in details["coveragestores"]])
                stores.extend(["%s:ds:%s" % (ws, c) for c in details["datastores"]])
        else:
            ws = self.workspaceComboBox.currentText()
            stores.extend(["cs:%s" % (c) for c in self.map["workspaces"][ws]["coveragestores"]])
            stores.extend(["ds:%s" % (c) for c in self.map["workspaces"][ws]["datastores"]])

        self.storeList.addItems(sorted(stores))

    def change_store(self):
        self.resourceList.clear()

        selected = self.storeList.selectedItems()
        if len(selected) == 1:
            if self.workspaceComboBox.currentIndex() == 0:
                ws, prefix, name = selected[0].text().split(":", 2)
            else:
                ws = self.workspaceComboBox.currentText()
                prefix, name = selected[0].text().split(":", 1)
            st_type = {"ds": "datastores", "cs": "coveragestores"}[prefix]
            self.resourceList.addItems(sorted(self.map["workspaces"][ws][st_type][name]))
            self.resourceList.setEnabled(True)
        elif selected:
            self.resourceList.addItem("All feature types or coverages will be imported.")
            self.resourceList.setEnabled(False)

    @catch_httperrors
    def btn_ok(self):

        self.progressBar.show()

        for i, (label, item) in enumerate(self.cart.iteritems()):
            self.progressBar.setValue(i * 98 / len(self.cart))
            self.progressBar.setFormat("%%p%% - importing '%s'" % label.text())
            qApp.processEvents()

            item.setup(self)

        self.progressBar.hide()

        self.close()
