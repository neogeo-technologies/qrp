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

import json

class Storage(dict):

    def __init__(self, backend):
        dict.__init__(self)
        self.backend = backend
        try:
            data = json.load(open(backend))
        except:
            data = {}
        self.update((k, Remote.unserialize(v)) for k, v in data.iteritems())

    def save(self):
        print "Saving storages: %s" % (self.keys())
        json.dump(dict((k, v.serialize()) for k, v in self.iteritems()), open(self.backend, "w"))


class Remote(object):

    store = ["name", "url", "flavour", "basicauth", "user", "password"]

    def __init__(self):
        for var in self.store:
            setattr(self, var, None)

    def serialize(self):
        return {var:getattr(self, var) for var in self.store}

    @classmethod
    def unserialize(clazz, serialized):
        remote = clazz()
        for var in clazz.store:
            setattr(remote, var, serialized[var])
        return remote




