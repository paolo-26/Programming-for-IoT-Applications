#!/usr/bin/env python3
"""
@author = Paolo Grasso

How to use:
    Send a PUT request with Postman with:

        destination = 0.0.0.0:8080/operation
        body (raw) = {"command": "add","operands": [10, 9, 8, 5, 3, 2, 1]}

Valid commands:
    add, mul, val, div
"""
import json
import cherrypy


class WebServer():
    exposed = True

    def GET(self):
        pass

    def POST(self):
        pass

    def PUT (self, *uri, **params):
        body = json.loads(cherrypy.request.body.read())  # Read body data
        my_calc = Calculator()

        if body["command"] == "add":
            res = my_calc.add(body["operands"])
            my_json = my_calc.printjson('add', body["operands"], res)

        if body["command"] == "sub":
            res = my_calc.sub(body["operands"])
            my_json = my_calc.printjson('sub', body["operands"], res)

        if body["command"] == "mul":
            res = my_calc.mul(body["operands"])
            my_json = my_calc.printjson('mul', body["operands"], res)

        if body["command"] == "div":
            res = my_calc.div(body["operands"])
            my_json = my_calc.printjson('div', body["operands"], res)

        return my_json

    def DELETE(self):
        pass


class Calculator():

    def add(self, vect):
        self.vect = vect
        res = 0

        for i in range(len(self.vect)):
            res += int(self.vect[i])

        return res

    def sub(self, vect):
        self.vect = vect
        res = self.vect[0]

        for i in range(1,len(self.vect)):
            res = res - int(self.vect[i])

        return res

    def mul(self, vect):
        self.vect = vect
        res = 1

        for i in range(len(self.vect)):
            res *= int(self.vect[i])

        return res

    def div(self, vect):
        self.vect = vect

        for i in range(1,len(self.vect)):

            if int(self.vect[i]) == 0:  # Predict division by 0
                res = "ERR DIV0"
                return res

        self.vect = vect
        res = int(self.vect[0])

        for i in range(1,len(self.vect)):
            res /= int(self.vect[i])

        return res

    def printjson(self, operator, operands, result):
        self.operands = [int(i) for i in operands]
        self.data = {'operands':self.operands,
            'operator':operator,
            'result':result}
        return json.dumps(self.data)


if __name__ == '__main__':
    conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True
		}
	}

    cherrypy.tree.mount (WebServer(), '/operation', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
