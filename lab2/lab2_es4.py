"""
@author = Paolo Grasso
"""
import json
import cherrypy

class Index(object):
    exposed = True
    def GET(self):
        return open("./freeboard/index.html", "r").read()

if __name__ == '__main__':

    cherrypy.tree.mount (Index(), '/index', 'dash.conf')
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
