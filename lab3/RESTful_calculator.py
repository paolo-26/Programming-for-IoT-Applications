#!/usr/bin/env python3
"""
@author = Paolo Grasso
"""
import json
import cherrypy

class Calculator(object):

    def __init__(self, op1=None, op2=None):
        self.op1 = op1
        self.op2 = op2

    def add(self):
        return self.op1 + self.op2

    def sub(self):
        return self.op1 - self.op2

    def mul(self):
        return self.op1 * self.op2

    def div(self):
        if (self.op2 == 0):
            return 'ERR div by 0'
        else:
            return self.op1 / self.op2

    def printjson(self, operator, result):
        dict = {'operator':operator, 'operand 1':self.op1,
            'operand 2':self.op2,
            'result':result}
        return json.dumps(dict)

class Add(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator(float(params['op1']), float(params['op2']))
        res = ad.add()
        json = ad.printjson('add', res)
        return json

class Sub(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator(float(params['op1']), float(params['op2']))
        res = ad.sub()
        json = ad.printjson('sub', res)
        return json

class Mul(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator(float(params['op1']), float(params['op2']))
        res = ad.mul()
        json = ad.printjson('mul', res)
        return json

class Div(Calculator):
    exposed = True
    def GET (self, *uri, **params):
        ad = Calculator(float(params['op1']), float(params['op2']))
        res = ad.div()
        json = ad.printjson('div', res)
        return json

if __name__ == '__main__':

    conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        }
    }

    cherrypy.tree.mount (Add(), '/add', conf)
    cherrypy.tree.mount (Sub(), '/sub', conf)
    cherrypy.tree.mount (Mul(), '/mul', conf)
    cherrypy.tree.mount (Div(), '/div', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
