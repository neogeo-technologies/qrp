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

from gui import ui_export, ui_new_store

from helpers import catch_httperrors
from restclient import HTTPError
import datasource

import os
import tempfile

class QRPNewStore(QDialog, ui_new_store.Ui_Dialog):
    def __init__(self, iface, api, ws_name, l_name, st_type, st_name, r_name, ds):
        # First init QDialogand Ui_Dialog
        QDialog.__init__(self)
        self.setupUi(self)

        self.iface = iface
        self.api = api
        self.ws = ws

        self.ok = False

        self.st_type = st_type
        self.st_name = st_name
        self.r_name = r_name

        self.connect(self.buttonBox, SIGNAL("rejected()"), self.close)
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.btn_ok)

        # init texts;

        self.currentLayerLineEdit.setText(l_name)
        self.storeNameLineEdit.setText(st_name)
        self.storeDetailsTextBrowser.setText(ds.provider.dataSourceUri())

        self.nameLineEdit.setText(st_name)

        if st_type == "datastores":
            _, stores = api.get_datastores(ws_name)
        elif st_type == "coveragestores":
            _, stores = api.get_coveragestore(ws_name)
        else:
            stores = []

        store_names = [store["name"] for store in stores]
        self.nameComboBox.insertItems(0, store_names)
        if st_name in store_names:
            self.nameComboBox.setCurrentIndex(store_names.index(st_name))

    def get_info(self):
        if self.tabWidget.currentIndex() == 0:
            name = self.nameComboBox.currentText().strip()
        else:
            name = self.nameLineEdit.text().strip()

            # this is a new DS, we should create it.

        return self.st_type, name, self.r_name

    def get_reuse(self):
        return self.alwaysReUseThisStoreForThisDataSourceCheckBox.isChecked()

    #
    # Callbacks
    #

    def btn_ok(self):
        self.ok = True
        self.close()


class QRPExport(QDialog, ui_export.Ui_Dialog):
    def __init__(self, iface, api):
        # First init QDialogand Ui_Dialog
        QDialog.__init__(self)
        self.setupUi(self)

        # Then our own stuff:

        self.iface = iface
        self.api = api

        self.layers = []

        self.connect(self.buttonBox, SIGNAL("rejected()"), self.close)
        self.connect(self.buttonBox, SIGNAL("accepted()"), self.btn_ok)

        self.selectAllButton.clicked.connect(self.btn_selectAll)
        self.selectVisibleButton.clicked.connect(self.btn_selectVisible)

        self.progressBar.hide()

        # Init the layer list.
        self.btn_selectVisible()

        self.workspaces = [ws["name"] for ws in self.api.get_workspaces()[1]]
        self.workspaceComboBox.addItems(self.workspaces)

    #
    # Application Helpers
    #

    def setLayers(self, layers):
        self.layers = layers
        self.layerList.clear()
        self.layerList.addItems(sorted(l.name() for l in self.layers))

    def get_remote_store_info(self, l_name, ws, ds, whitelist):

        # What does the data source tells us?
        st_type, st_name, r_name = ds.getinfo()

        # Do we know what to do with this?
        if (st_type, st_name) in whitelist:
            cached = whitelist[(st_type, st_name)]
            return cached[0], cached[1], r_name

        if self.askBeforeChoosingStoresCheckBox.isChecked():
            dlg_new_store = QRPNewStore(self.iface, self.api, ws, l_name, st_type, st_name, r_name, ds)

            dlg_new_store.exec_()
            if not dlg_new_store.ok:
                return None

            st_type, st_name, r_name = dlg_new_store.get_info()
            reuse = dlg_new_store.get_reuse()
        else:
            # Otherwise we'll just assume the same names.
            reuse = self.reUseCreatedStoresCheckBox.isChecked()

        try:
            ds.export(self.api, ws, st_name)
        except HTTPError as e:
            # Except only conflict.
            if e.response.status != 409:
                raise

        if reuse:
            whitelist[(st_type, st_name)] = st_type, st_name, r_name

        return st_type, st_name, r_name

    def get_layer_map(self):
        def expand_group(name):
            for i, (parent, children) in enumerate(relations):
                if parent == name:
                    break
            else: # This childname is not a group.
                return name

            parent, children = relations.pop(i)
            return (parent, [expand_group(child) for child in children])

        relations = qgis.utils.iface.legendInterface().groupLayerRelationship()

        layer_map = []
        while relations:
            parent, children = relations.pop(0)
            layer_map.append((parent, [expand_group(child) for child in children]))

        return layer_map


    #
    # Callbacks
    #

    @catch_httperrors
    def btn_ok(self):


        self.progressBar.show()

        skipped = []
        whitelist = {}

        ws = self.workspaceComboBox.currentText()
        if ws not in self.workspaces:
            self.api.create_workspace(ws)

        for i, layer in enumerate(self.layers):
            self.progressBar.setValue(i * 98 / len(self.layers))
            self.progressBar.setFormat("%%p%% - exporting '%s'" % layer.name())
            qApp.processEvents()

            try:
                ds = datasource.dataProviderHandler(layer.dataProvider())
            except ValueError as e:
                skipped.append(layer)
                continue

            info = self.get_remote_store_info(layer.name(), ws, ds, whitelist)
            if not info:
                # User canceled, we skip.
                continue

            st_type, st_name, name = info

            print "EXPORTING: layer %s, info:" % layer.name(), st_type, st_type, name

            # Now we have all the information.
            # We might need to do updates if conflicts :(

            create_funcs = {
                "coveragestores": self.api.create_coverage,
                "datastores": self.api.create_featuretype,
                }

            # Try to create the c/ft.
            try:
                create_funcs[st_type](ws, st_name, name)
            except HTTPError as e:
                # Except only conflict.
                if e.response.status != 409:
                    raise

                reply = QMessageBox.question(self, "Exisiting data", "The data for this layer (%s) already exists "
                                             "on the server, should we try to update its style?" % layer.name(),
                                             QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    continue

            # The layer is now auto-created, we can add the style.

            sld_fd, sld_path = tempfile.mkstemp(suffix=".sld")
            os.close(sld_fd)

            layer.saveSldStyle(sld_path)

            sld = open(sld_path).read()
            os.remove(sld_path)

            if sld.strip():
                style_name = "%s_qgis_style" % layer.name()

                try:
                    self.api.create_style(style_name, sld)
                except HTTPError as e:
                    # Except only conflict.
                    if e.response.status != 409:
                        raise

                self.api.update_layerstyle(name, style_name)

        self.progressBar.setValue(98)
        self.progressBar.setFormat("mirroring groups")
        qApp.processEvents()

        # Ok, now lets put the layers in groups.

        all_layers = QgsMapLayerRegistry.instance().mapLayers()
        lmap = self.get_layer_map()

        for parent, children in lmap:
            if parent == "": continue
            # Now we are left with the first level groups.

            layers = []
            group_children = children[:]
            while group_children:
                child = group_children.pop(0)
                if isinstance(child, tuple):
                    nested_group, nested_children = child
                    group_children.extend(nested_children)
                else:
                    layers.append(child)

            layers = [all_layers[l] for l in layers]
            layers = [l.name() for l in layers if l in self.layers and l not in skipped]

            if layers:
                print "ADDING GROUP %s (%s)" % (parent, layers)

                try:
                    self.api.create_layergroup(parent, layers)
                except HTTPError as e:
                    # Except only conflict.
                    if e.response.status != 409:
                        raise

        if skipped:
            QMessageBox.information(self, "Published", "The folowing layers could not be published: %s"
                                    % [l.name() for l in skipped]);
        else:
            QMessageBox.information(self, "Published", "All layers where published.")

        self.progressBar.hide()

        self.close()



    def btn_selectAll(self):
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        self.setLayers(layers)

    def btn_selectVisible(self):
        layers = self.iface.mapCanvas().layers()
        self.setLayers(layers)
