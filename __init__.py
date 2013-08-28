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

def classFactory(iface):
    from main import QRP
    return QRP(iface)
