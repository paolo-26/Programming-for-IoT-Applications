#!/usr/bin/env python3
"""
@author = Paolo Grasso
"""
import json
import cherrypy

class CalculatorWS(object):  # RESTful web server
    exposed = True

    def GET(self, *uri, **params):
        try:
            calc = Calculator(float(params['op1']), float(params['op2']))

            if uri[0] == 'add':
                res = calc.add()

            elif uri[0] == 'sub':
                res = calc.sub()

            elif uri[0] == 'mul':
                res = calc.mul()

            elif uri[0] == 'div':
                res = calc.div()
                if res == 'ERR':
                    raise ZeroDivisionError("Can't divide by 0")

            else:
                raise SyntaxError

            return calc.printjson('add', res)  # Print results

        except ZeroDivisionError:
                raise cherrypy.HTTPError(422, "Can't divide by 0")

        except SyntaxError:
                raise cherrypy.HTTPError(400, "Syntax error")

    def POST(self):
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass


class Calculator(object):  # Calculator

    def __init__(self, op1, op2):
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
            return 'ERR'

        else:
            return self.op1 / self.op2

    def printjson(self, operator, result):
        dict = {'operator':operator, 'operand 1':self.op1,
            'operand 2':self.op2,
            'result':result}
        return json.dumps(dict)


if __name__ == '__main__':
    conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        }
    }
    cherrypy.tree.mount (CalculatorWS(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
