"""
@author = Paolo Grasso
Examples
0.0.0.0:8080/add?op1=5&op2=9.5
0.0.0.0:8080/mul?op1=5&op2=9.5
0.0.0.0:8080/sub?op1=5&op2=9.5
0.0.0.0:8080/div?op1=5&op2=9.5
"""
import json
import random
import string
import cherrypy


class Calculator():
    
    def __init__(self):
        pass
                
    def add(self, op1, op2):
        return op1 + op2 

    def sub(self, op1, op2):
        return op1 - op2

    def mul(self, op1, op2):
        return op1 * op2

    def div(self, op1, op2):
        if (op2 == 0):
            return 'ERR div by 0'
        else:
            return op1 / op2

    def printjson(self, operator, operand1, operand2, result):
        dict = {'operator':operator, 'operand1':operand1, 'operand2':operand2, 'result':result}
        return json.dumps(dict)


class add(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator()
        res = ad.add(float(uri[0]), float(uri[1]))
        json = ad.printjson('add', uri[0], uri[1], res)
        return json

class sub(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator()
        res = ad.sub(float(uri[0]), float(uri[1]))
        json = ad.printjson('sub', uri[0], uri[1], res)
        return json

class mul(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator()
        res = ad.mul(float(uri[0]), float(uri[1]))
        json = ad.printjson('mul', uri[0], uri[1], res)
        return json

class div(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator()
        res = ad.div(float(uri[0]), float(uri[1]))
        json = ad.printjson('div', uri[0], uri[1], res)
        return json

if __name__ == '__main__':

    conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        }
    }

    cherrypy.tree.mount (add(), '/add', conf)
    cherrypy.tree.mount (sub(), '/sub', conf)
    cherrypy.tree.mount (mul(), '/mul', conf)
    cherrypy.tree.mount (div(), '/div', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()