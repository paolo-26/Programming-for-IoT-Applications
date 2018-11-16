#!/usr/bin/env python3
"""
@author = Paolo Grasso
Examples
0.0.0.0:8080/add?op1=5&op2=9.5
0.0.0.0:8080/mul?op1=5&op2=9.5
0.0.0.0:8080/sub?op1=5&op2=9.5
0.0.0.0:8080/div?op1=5&op2=9.5
"""
import json
import cherrypy


class WebServer():
    exposed = True

    def GET(self, *uri, **params):
        try:
            if uri[0] == 'add':
                calc = Calculator()
                res = calc.add(float(params['op1']), float(params['op2']))


            elif uri[0] == 'sub':
                calc = Calculator()
                res = calc.sub(float(params['op1']), float(params['op2']))

            elif uri[0] == 'mul':
                calc = Calculator()
                res = calc.mul(float(params['op1']), float(params['op2']))

            elif uri[0] == 'div':
                calc = Calculator()
                res = calc.div(float(params['op1']), float(params['op2']))

            return calc.printjson(uri[0], params['op1'], params['op2'], res)

        except:
            raise cherrypy.HTTPError(404, "Error, uri[0] must be an operator")

    def POST(self):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass


class Calculator():

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
