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

import functools
import httplib
import urlparse
import json
import pdb
import inspect
import sys
import textwrap
import collections
import urllib2
import pprint
import contextlib
import base64
import pyxml
from pyxml import Entries

class HTTPError(httplib.HTTPException):
    def __init__(self, response, body=None):
        self.response = response
        self.body = body
        httplib.HTTPException.__init__(self, "[%d] %s" % (self.response.status, self.response.reason))

# Some small helpers.
def rmOuterDict(data):
    req, data = data
    if isinstance(data, dict) and len(data) == 1:
        data = next(data.itervalues())
    return req, data

class apixml():
    def dumps(self, x):
        if isinstance(x, dict) and len(x) == 1:
            return pyxml.dumps(next(x.itervalues()), root=next(x.iterkeys()))
        return x
    def loads(self, x):
        return pyxml.loads(x)

apixml = apixml()

# This API aims to be CRUD.
# The main verbs used are: create, get, update, delete

class RestAPI(object):

    def __init__(self, baseurl, encoding="xml", verbose=False, username=None, password=None):
        if not baseurl.endswith("/"):
            baseurl += "/"

        self.baseurl = httplib.urlsplit(baseurl)
        self.verbose = verbose

        self.username = username
        self.password = password

        if encoding == "json":
            self.encoding = json
            self.extension = ".json"
            self.content_type = "application/json"
        elif encoding == "xml":
            self.encoding = apixml
            self.extension = ".xml"
            self.content_type = "application/xml"
        else:
            raise ValueError("Unsupported encoding: %s" % encoding)

    # Request helpers

    def path(self, url, addext=True):
        path = urlparse.urljoin(self.baseurl.path, url)
        if addext:
            path += self.extension
        return path

    def check_response(self, response):
        if response.status < 300:
            return
        print >>sys.stderr, "Generating HTTP Exception, body:"
        print >>sys.stderr, "="*75
        body = response.read()
        print >>sys.stderr, body[:4096]
        if len(body) > 4096:
            print >>sys.stderr, "... response was cut because too long."
        print "="*75
        raise HTTPError(response, body)

    def HTTPConnection(self):
        return httplib.HTTPConnection(self.baseurl.hostname, self.baseurl.port, timeout=6000)

    def request(self, method, url, data=None, headers={}, addext=True, query=None):
        conn = self.HTTPConnection()
        url = urllib2.quote(self.path(url, addext))
        if query: url += "?%s" % query

        if self.username and self.password:
            headers["Authorization"] = "Basic %s" % base64.b64encode('%s:%s' % (self.username, self.password))

        if self.verbose:
            print >>sys.stderr, "%s %s" % (method, urlparse.urljoin(self.baseurl.geturl(), url))
            print >>sys.stderr, headers
            print >>sys.stderr, "-"*60

        conn.request(method, url, body=data, headers=headers)
        return conn.getresponse()

    def POST(self, url, data=None, content_type="text/plain", addext=True):
        return self.request("POST", url, data=data, headers={"Content-Type": content_type}, addext=addext)

    def GET(self, url, addext=True):
        return self.request("GET", url, addext=addext)

    def PUT(self, url, data, content_type="text/plain", addext=True):
        return self.request("PUT", url, data=data, headers={"Content-Type": content_type}, addext=addext)

    def DELETE(self, url, addext=True):
        return self.request("DELETE", url, addext=addext)

    def POSTpython(self, url, data, addext=True):
        response = self.POST(url, self.encoding.dumps(data), self.content_type, addext)
        self.check_response(response)
        data = response.read()
        return response, self.encoding.loads(data) if data else None

    def GETpython(self, url, addext=True):
        response = self.GET(url, addext)
        self.check_response(response)
        data = response.read()
        return response, self.encoding.loads(data) if data else None

    def PUTpython(self, url, data, addext=True):
        response = self.PUT(url, self.encoding.dumps(data), self.content_type, addext)
        self.check_response(response)
        data = response.read()
        return response, self.encoding.loads(data) if data else None

    def DELETEpython(self, url, addext=True):
        response = self.DELETE(url, addext)
        self.check_response(response)
        data = response.read()
        return response, self.encoding.loads(data) if data else None

    # API

    def get_workspaces(self):
        return rmOuterDict(self.GETpython("workspaces"))
    def create_workspace(self, ws_name):
        data = {"workspace": {"name": ws_name}}
        return self.POSTpython("workspaces", data)
    def get_workspace(self, ws_name):
        return rmOuterDict(self.GETpython("workspaces/%s" % (ws_name,)))

    def get_styles(self):
        return rmOuterDict(self.GETpython("styles"))
    def create_style(self, s_name, sld):
        response = self.request("POST", "styles", data=sld,
                                headers={"Content-Type": "application/vnd.ogc.sld+xml"},
                                addext=False, query="name=%s" % s_name)
        self.check_response(response)

    def get_style(self, s_name):
        return rmOuterDict(self.GETpython("styles/%s" % (s_name,)))
    def get_style_sld(self, s_name):
        response = self.GET("styles/%s.sld" % s_name, addext=False)
        self.check_response(response)
        return response.read()

    def get_layers(self):
        return rmOuterDict(self.GETpython("layers"))
    def create_layer(self, l_name, ws_name, ds_name=None, ft_name=None, cs_name=None, c_name=None):
        if (not ((not ds_name) ^ (not cs_name))) or (ds_name and not ft_name) or (cs_name and not c_name):
            raise TypeError("Expected [ds_name ft_name | cs_name c_name].")
        if ds_name:
            resource = self.path("workspaces/%s/datastores/%s/featuretypes/%s" % (ws_name, ds_name, ft_name))
        else:
            resource = self.path("workspaces/%s/coveragestores/%s/coverages/%s" % (ws_name, cs_name, c_name))
        data = {
            "layer": {
                "name": l_name,
                "resource": {"href":resource},
                }
            }
        return self.POSTpython("layers", data)
    def get_layer(self, l_name):
        return rmOuterDict(self.GETpython("layers/%s" % (l_name,)))
    def update_layer(self, l_name):
        # TODO: Fix the stuff that is sent.
        data = {
            "layer": {
                }
            }
        return self.PUTpython("layers/%s" % (l_name,), data)
    def delete_layer(self, l_name):
        return self.DELETEpython("layers/%s" % (l_name,))

    def get_layergroups(self):
        return rmOuterDict(self.GETpython("layergroups"))
    def create_layergroup(self, lg_name, layers):
        data = {
            "layerGroup": {
                "name": lg_name,
                "layers": layers,
                }
            }
        return self.POSTpython("layergroups", data)
    def get_layergroup(self, lg_name):
        return rmOuterDict(self.GETpython("layergroups/%s" % (lg_name,)))
    def update_layergroup(self, lg_name):
        # TODO: Fix the stuff that is sent.
        data = {
            "layergroup": {
                }
            }
        return self.PUTpython("layergroups/%s" % (lg_name,), data)
    def delete_layergroup(self, lg_name):
        return self.DELETEpython("layergroups/%s" % (lg_name,))

    def get_coveragestores(self, ws_name):
        return rmOuterDict(self.GETpython("workspaces/%s/coveragestores" % (ws_name,)))
    def create_coveragestore(self, ws_name, cs_name):
        data = {"coverageStore": {"name": cs_name}}
        return self.POSTpython("workspaces/%s/coveragestores" % (ws_name,), data)
    def get_coveragestore(self, ws_name, cs_name):
        return rmOuterDict(self.GETpython("workspaces/%s/coveragestores/%s" % (ws_name, cs_name)))
    def update_coveragestore(self, ws_name, cs_name):
        data = {"coverageStore": {"name": cs_name}}
        return self.PUTpython("workspaces/%s/coveragestores/%s" % (ws_name, cs_name), data)
    def delete_coveragestore(self, ws_name, cs_name):
        return self.DELETEpython("workspaces/%s/coveragestores/%s" % (ws_name, cs_name))

    def get_datastores(self, ws_name):
        return rmOuterDict(self.GETpython("workspaces/%s/datastores" % (ws_name,)))
    def create_datastore(self, ws_name, ds_name, cparam=None):
        if cparam:
            data = {"dataStore": {"name": ds_name, "connectionParameters": Entries(cparam, tag_name="entry")}}
        else:
            data = {"dataStore": {"name": ds_name}}

        return self.POSTpython("workspaces/%s/datastores" % (ws_name,), data)
    def get_datastore(self, ws_name, ds_name):
        return rmOuterDict(self.GETpython("workspaces/%s/datastores/%s" % (ws_name, ds_name)))
    def update_datastore(self, ws_name, ds_name):
        # TODO: Fix the stuff that is sent.
        data = {
            "style": {
                }
            }
        return self.PUTpython("workspaces/%s/datastores/%s" % (ws_name, ds_name), data)
    def delete_datastore(self, ws_name, ds_name):
        return self.DELETEpython("workspaces/%s/datastores/%s" % (ws_name, ds_name))

    def get_styles(self, l_name):
        return rmOuterDict(self.GETpython("layers/%s/styles" % (l_name,)))
    def update_layerstyle(self, l_name, style_name):
        data = {
            "layer": {
                "defaultStyle": {
                    "name": style_name,
                    }
                }
            }
        return self.PUTpython("layers/%s" % (l_name,), data)

    def get_layerfields(self, l_name):
        return rmOuterDict(self.GETpython("layers/%s/layerfields" % (l_name,)))

    def create_file(self, st_type, ws_name, st_name, file, ext="", content_type="text/plain"):
        response = self.PUT("workspaces/%s/%s/%s/file%s" % (ws_name, st_type, st_name, ext), file,
                            content_type=content_type, addext=False)
        self.check_response(response)
        data = response.read()
        return response, self.encoding.loads(data) if data else None

    def create_ffile(self, ws_name, ds_name, ffile, ext="", content_type="text/plain"):
        return self.create_file("datastores", ws_name, ds_name, ffile, ext, content_type)

    def create_cfile(self, ws_name, cs_name, cfile, ext="", content_type="text/plain"):
        return self.create_file("coveragestores", ws_name, cs_name, cfile, ext, content_type)

    def get_coverages(self, ws_name, cs_name):
        return rmOuterDict(self.GETpython("workspaces/%s/coveragestores/%s/coverages" % (ws_name, cs_name)))
    def create_coverage(self, ws_name, cs_name, c_name):
        data = {"coverage": {"name": cs_name}}
        return self.POSTpython("workspaces/%s/coveragestores/%s/coverages" % (ws_name, cs_name), data)
    def get_coverage(self, ws_name, cs_name, c_name):
        return rmOuterDict(self.GETpython("workspacse/%s/coveragestores/%s/coverages/%s" % (ws_name, cs_name, c_name)))
    def update_coverage(self, ws_name, cs_name, c_name):
        data = {"coverage": {"name": cs_name}}
        return self.PUTpython("workspaces/%s/coveragestores/%s/coverages/%s" % (ws_name, cs_name, c_name), data)
    def delete_coverage(self, ws_name, cs_name, c_name):
        return self.DELETEpython("workspaces/%s/coveragestores/%s/coverages/%s" % (ws_name, cs_name, c_name))

    def get_featuretypes(self, ws_name, ds_name):
        return rmOuterDict(self.GETpython("workspaces/%s/datastores/%s/featuretypes" % (ws_name, ds_name)))
    def create_featuretype(self, ws_name, ds_name, ft_name):
        data = {"featureType": {"name": ft_name}}
        return self.POSTpython("workspaces/%s/datastores/%s/featuretypes" % (ws_name, ds_name), data)
    def get_featuretype(self, ws_name, ds_name, ft_name):
        return rmOuterDict(self.GETpython("workspaces/%s/datastores/%s/featuretypes/%s" % (ws_name, ds_name, ft_name)))
    def update_featuretype(self, ws_name, ds_name, ft_name):
        data = {"featureType": {"name": ft_name}}
        return self.PUTpython("workspaces/%s/datastores/%s/featuretypes/%s" % (ws_name, ds_name, ft_name), data)
    def delete_featuretype(self, ws_name, ds_name, ft_name):
        return self.DELETEpython("workspaces/%s/datastores/%s/featuretypes/%s" % (ws_name, ds_name, ft_name))

    #
    # Other features, not directly exposed by the REST API.
    #

    def map_datastore(self, ws_name, ds_name):
        return [ft["name"] for ft in self.get_featuretypes(ws_name, ds_name)[1]]

    def map_datastores(self, ws_name):
        dss = {}
        for ds in self.get_datastores(ws_name)[1]:
            dss[ds["name"]] = self.map_datastore(ws_name, ds["name"])
        return dss

    def map_coveragestore(self, ws_name, cs_name):
        return [c["name"] for c in self.get_coverages(ws_name, cs_name)[1]]

    def map_coveragestores(self, ws_name):
        css = {}
        for cs in self.get_coveragestores(ws_name)[1]:
            css[cs["name"]] = self.map_coveragestore(ws_name, cs["name"])
        return css

    def map_workspace(self, ws_name):
        return {
            "datastores": self.map_datastores(ws_name),
            "coveragestores": self.map_coveragestores(ws_name),
            }

    def map_workspaces(self):
        wss = {}
        for ws in self.get_workspaces()[1]:
            wss[ws["name"]] = self.map_workspace(ws["name"])
        return wss

    def map_styles(self):
        return [l["name"] for l in self.get_layers()[1]]

    def map_layer(self, l_name):
        l = self.get_layer(l_name)[1]

        url = urlparse.urlparse(l["resource"]["href"])
        _, _, ws_name, st_type, st_name, r_type, r_name = url.path.split("/")[-7:]
        # The last one might have a format extention. (.json, .xml)
        r_name = r_name.rsplit(".", 1)[0]

        styles = [s["name"] for s in l["styles"]] if "styles" in l else []
        if l["defaultStyle"]["name"] not in styles:
            styles.append(l["defaultStyle"]["name"])

        return {
            "default_style": l["defaultStyle"]["name"],
            "styles": styles,
            "resource": {"name": r_name,
                         "type": r_type,
                         "store": st_name,
                         "store_type": st_type,
                         "workspace": ws_name,
                         }
            }

    def map_layers(self):
        ls = {}
        for l in self.get_layers()[1]:
            ls[l["name"]] = self.map_layer(l["name"])
        return ls

    def map_layergroup(self, lg_name):
        lg = self.get_layergroup(lg_name)[1]
        return [l["name"] for l in lg["publishables"]]

    def map_layergroups(self):
        lgs = {}
        for lg in self.get_layergroups()[1]:
            lgs[lg["name"]] = self.map_layergroup(lg["name"])
        return lgs

    def map(self):
        return {
            "workspaces": self.map_workspaces(),
            "layers": self.map_layers(),
            "layergroups": self.map_layergroups(),
            }


# The following classes are here to provide an easy way to patch
# the protocols beeing used, in order to fix some disparities
# between MRA and the Geoserver REST API before they are beeing
# changed in either one of those.

class MRA(RestAPI):
    # Everything is the same \o/ (Should be.)
    pass

class geoserverREST(RestAPI):
    # As long as we supose geoserver is the standart this should be
    # empty, patches should be made to MRA or to the MRA class above.

    # Correction, some things have to be fixed where they are broken.

    # geoserver returns a 500 status way to often.
    # lets fix that.
    def check_response(self, response):

        try:
            return RestAPI.check_response(self, response)
        except HTTPError as e:
            if e.response.status in [500, 403] and "already exists" in e.body:
                e.response.status = 409

            raise e

# If this is used as a stand alone client we need to get arguments
# from the command line and have some application logic.

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    action = parser.add_argument_group("actions", "This options indicate the main action to be performed. "
                                       "It basically mirrors the CRUD API."
                                       ).add_mutually_exclusive_group()
    action.add_argument("--create", action="store_const", const="create", dest="action")
    action.add_argument("--get", action="store_const", const="get", dest="action")
    action.add_argument("--update", action="store_const", const="update", dest="action")
    action.add_argument("--delete", action="store_const", const="delete", dest="action")
    action.add_argument("--map", action="store_const", const="map", dest="action")
    action.set_defaults(action="get")

    selection = parser.add_argument_group("specifiers", "This options can be used to specify on what "
                                          "resources you want to operate.")
    selection.add_argument("-ws", "--workspace", dest="ws_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-s", "--style", dest="s_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-l", "--layer", dest="l_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-lg", "--layergroup", dest="lg_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-cs", "--coveragestore", dest="cs_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-ds", "--datastore", dest="ds_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-c", "--coverage", dest="c_name", nargs="?", default=argparse.SUPPRESS)
    selection.add_argument("-ft", "--featuretype", dest="ft_name", nargs="?", default=argparse.SUPPRESS)

    selection.add_argument("-ff", "--ffile", dest="ffile", default=argparse.SUPPRESS, type=argparse.FileType("r"))
    selection.add_argument("-cf", "--cfile", dest="cfile", default=argparse.SUPPRESS, type=argparse.FileType("r"))

    data = parser.add_argument_group("data", "This options allow for input data to be specified. "
                                     "It is intended to be used with actions such as --create")
    data.add_argument("-f", "--file", type=argparse.FileType("r"))
    data.add_argument("-i", "--input", choices=["json", "xml"], default="xml")

    data.add_argument("-ct", "--content-type", default=argparse.SUPPRESS)
    data.add_argument("--ext", default=argparse.SUPPRESS)
    data.add_argument("-r", "--resource", default=argparse.SUPPRESS)

    api = parser.add_argument_group("api", "This arguments are used when comunicating with the remote API.")
    api.add_argument("url")
    api.add_argument("-o", "--output", choices=["json", "xml"], default="xml")
    api.add_argument("-t", "--tweak-for", choices=["mra", "geoserver"])
    api.add_argument("-v", "--verbose", action="store_true")

    api.add_argument("-u", "--user", default=None)
    api.add_argument("-p", "--password", default=None)

    args = parser.parse_args()

    if not args.url.endswith("/"):
        print >> sys.stderr, "Warning: Appending '/' to base url."
        args.url += "/"

    # Build the API.
    tweakers = {"mra": MRA, "geoserver": geoserverREST}
    tweaker = tweakers.get(args.tweak_for, RestAPI)
    api = tweaker(args.url, encoding=args.output, verbose=args.verbose, username=args.user, password=args.password)

    # Now I am not really interested in a bunch of ifs. Lets do it the easy way.

    # This dict is used to translate argument names to object names.
    possible = collections.OrderedDict((("ws_name", "workspace"),
                                        ("s_name",  "style"),
                                        ("lg_name", "layergroup"),
                                        ("cs_name",  "coveragestore"),
                                        ("ds_name", "datastore"),
                                        ("c_name",  "coverage"),
                                        ("ft_name", "featuretype"),
                                        ("l_name",  "layer"),
                                        ("ffile", "ffile"),
                                        ("cfile", "cfile"),
                                        ))

    # First we need to know what the user is interested in, that's the most deep level of specifier.
    what = next((x for x in reversed(possible) if x in args), None)
    if what:
        # Now, which of what do we want?
        which = getattr(args, what)
        # But, what is what?
        whatis = possible[what]

        # If we don't know which which we want as what, we watch for all whats that might be which.
        # Unless what we want is to create that which does not yet exists.
        if not which and args.action != "create":
            whatis += "s"

        # Now lets fish for the method.
        method = getattr(api, "%s_%s" % (args.action, whatis))

    else:
        # We don't want anything in particular, lets see if that is possible.
        method = getattr(api, "%s" % (args.action))


    # Now it gets really tricky, we need to get the right arguments.
    # Simply forwarding everything from the user might work but its not complicated enough.
    # Actually this way allows us to do error checking, which is always better, isn't it ?
    argspec = inspect.getargspec(method)
    try:
        methodargs = inspect.getcallargs(method, **dict((arg, getattr(args, arg)) for arg in argspec.args if arg in args))
    except TypeError as e:

        if argspec.defaults:
            missing = [x for x in argspec.args[1:-len(argspec.defaults)] if x not in args]
        else:
            missing = [x for x in argspec.args[1:] if x not in args]

        parser.error("Missing parameters: %s" % ", ".join(x.upper() for x in missing))

    # dirty fix, but self should not yet be present.
    del methodargs["self"]

    print >>sys.stderr, "="*70
    print >>sys.stderr, "%s(%s)" % (method.__name__, ", ".join("%s=%s" % (n, v) for n, v in methodargs.iteritems()))
    print >>sys.stderr, "="*70

    try:
        # As simple as that.
        content = method(**methodargs)
        if args.action != "map":
            response, content = content
    except HTTPError as e:
        # Error will have been printed already.
        exit(1)

    if args.verbose:
        print >>sys.stderr, "="*70

    pprint.pprint(content)
