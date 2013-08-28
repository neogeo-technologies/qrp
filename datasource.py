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

import os
import tempfile

import tempfile
import zipfile
import shlex

from qgis.core import *
import qgis.utils

class FileDataProviderHandler(object):
    searchfiles = False

    def __init__(self, provider):
        self.provider = provider
        self.name, self.files, self.ext = self.listfiles()

        if not self.files:
            raise ValueError("Didn't find any known files in dataProvider.")

    def listfiles(self):
        uri = self.provider.dataSourceUri()
        path, args = uri.rsplit("|", 1) if "|" in uri else (uri, "")
        noext, ext = os.path.splitext(path)
        dirn, name = os.path.split(noext)

        if not self.searchfiles:
            files = [path]
        else:
            files = [os.path.join(dirn, f) for f in os.listdir(dirn) if os.path.splitext(os.path.split(f)[1])[0] == name]

        print "Found files:", files
        return name, files, ext

    def getinfo(self):
        return self.st_type, self.name, self.name

    def export(self, api, ws_name, ds_name=None):
        files, ext = self.files, self.ext
        if not ds_name:
            ds_name = self.ds_name

        # Lets default to some basic files that need to be uploaded.
        if len(files) > 1:
            content_type = "application/zip"

            buf = tempfile.TemporaryFile()
            with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as archive:
                for f in files:
                    archive.write(filename=f, arcname=os.path.split(f)[1])

            # Reset file pointer
            buf.seek(0)

        else:
            # TODO: lulz, fix this content type :)
            content_type = "restclient/" + ext[1 if ext.startswith(".") else 0:]
            ext = ""
            buf = open(files[0], "r")

        api.create_file(self.st_type, ws_name, self.name, buf, ext, content_type)

class SHPDataProviderHandler(FileDataProviderHandler):
    st_type = "datastores"
    searchfiles = True

class IMGDataProviderHandler(FileDataProviderHandler):
    st_type = "coveragestores"
    searchfiles = True

class PGISDataProviderHandler(object):
    st_type = "datastores"

    def __init__(self, provider):
        self.provider = provider

        # This is silly because it will probably be put in the same format
        # again by the remote, but we have to comply to JSON/XML.
        uri = self.provider.dataSourceUri()
        tokens = (token.split("=", 1) for token in shlex.split(uri))
        tokens = dict(tuple(pair) for pair in tokens if len(pair) == 2 and pair[1])

        self.params = dict((x, tokens[x]) for x in ["host", "port", "user", "password"] if x in tokens)

        self.params["database"] = tokens["dbname"]
        self.params["dbtype"] = "postgis"

        schema, ft_name = tokens["table"].split(".", 1)
        if not ft_name:
            schema, ft_name = "public", schema

        self.params["schema"] = schema
        self.ft_name = ft_name

        self.ds_name = "%s_%s" % (self.params["database"], self.params["schema"])

    def getinfo(self):
        return self.st_type, self.ds_name, self.ft_name

    def export(self, api, ws_name, ds_name=None):
        if not ds_name:
            ds_name = self.ds_name

        api.create_datastore(ws_name, ds_name, cparam=self.params)


def dataProviderHandler(provider):

    if isinstance(provider, QgsRasterDataProvider):
        return IMGDataProviderHandler(provider)

    typ = getattr(provider, "storageType", lambda: "")()
    typl = typ.lower()

    if "shapefile" in typl or "shp" in typl:
        return SHPDataProviderHandler(provider)

    if "postgis" in typl:
        return PGISDataProviderHandler(provider)

    raise ValueError("Unknown datasource.")
