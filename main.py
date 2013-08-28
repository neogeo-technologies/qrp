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

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources
import qrpconfig

from restclient import HTTPError

class QRP(object):

    #
    # Methods called by QGIS
    #

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface



    def initGui(self):
        # Create action that will start plugin configuration
        self.configure_action = QAction(QIcon(":/plugins/qrp/qrp.png"), "Configure QRP", self.iface.mainWindow())
        self.configure_action.setWhatsThis("Configuration for QRP")
        self.iface.addWebToolBarIcon(self.configure_action)
        self.iface.addPluginToWebMenu("&QRP", self.configure_action)

        QObject.connect(self.iface, SIGNAL("currentThemeChanged (QString)"), self.changetheme)

        QObject.connect(self.configure_action, SIGNAL("triggered()"), self.configure)


    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginWebMenu("&QRP", self.configure_action)
        self.iface.removeWebToolBarIcon(self.configure_action)


    #
    # Callbacks
    #

    def configure(self):
        print "QRP Configure."
        dlg_config = qrpconfig.QRPConfig(self.iface)
        result = dlg_config.exec_()

    def changetheme(self, name):
        print "Changing theme for: %s" % name
        return QIcon(":/plugins/qrp/qrp.png")
