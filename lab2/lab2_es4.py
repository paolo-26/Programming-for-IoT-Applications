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
    cherrypy.tree.mount (Index(), '/', config='conf')
    cherrypy.config.update('conf')
    cherrypy.engine.start()
    cherrypy.engine.block()
