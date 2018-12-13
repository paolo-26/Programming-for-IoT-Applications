#!/usr/bin/env python3
"""
@author = Paolo Grasso
"""

import json
import cherrypy
import paho.mqtt.client as PahoMQTT

FILENAME = "info.json"

class MyCatalog(object):
    exposed = True
    #@cherrypy.tools.json_out()

    def __init__(self, filename):
        self.filename = filename

    def GET(self, *uri, **params):

        with open(self.filename, "r") as f:
            data = json.loads(f.read())

        if len(uri) > 2:
            raise cherrypy.HTTPError(404, "Resource not found")

        if uri[0] == 'broker':
            info = data["broker"]

        if uri[0] == 'devices':

            if uri[1] == 'all':
                info = data["devices"]
            else:
                id = uri[1]
                info = [d for d in data["devices"] if d["id"] == id]
                try:
                    info = info[0]
                except:
                    raise cherrypy.HTTPError(404, "Device not found")

        if uri[0] == 'users':

            if uri[1] == 'all':
                info = data["users"]
            else:
                id = uri[1]
                info = [d for d in data["users"] if d["id"] == id]
                try:
                    info = info[0]
                except:
                    raise cherrypy.HTTPError(404, "User not found")

        return json.dumps(info)


    def POST(self,):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass








if __name__ == '__main__':
    conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        }
    }
    cherrypy.tree.mount (MyCatalog(FILENAME), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
