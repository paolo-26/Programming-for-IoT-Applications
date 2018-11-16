#!/usr/bin/env python3
"""
@author = Paolo Grasso
Examples
0.0.0.0:8080/add/2/9.5
0.0.0.0:8080/mul/3/21
0.0.0.0:8080/sub/7/4.7
0.0.0.0:8080/div/10/4.2
"""
import json
import random
import string
import cherrypy


class WebServer():
    exposed = True

    def GET(self, *uri, **params):
        try:
            calc = Calculator()
            if uri[0] == 'add':
                res = calc.add(float(uri[1]), float(uri[2]))

            elif uri[0] == 'sub':
                res = calc.sub(float(uri[1]), float(uri[2]))

            elif uri[0] == 'mul':
                res = calc.mul(float(uri[1]), float(uri[2]))

            elif uri[0] == 'div':
                res = calc.div(float(uri[1]), float(uri[2]))

            return calc.printjson(uri[0], uri[1], uri[2], res)

        except:
            raise cherrypy.HTTPError(404, "Error, uri[0] must be an operator")

    def POST(self):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass


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
        dict = {'operator':operator, 'operand1':operand1,
            'operand2':operand2,
            'result':result}
        return json.dumps(dict)


if __name__ == '__main__':

    conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        }
    }

    cherrypy.tree.mount (WebServer(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
