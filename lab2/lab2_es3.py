"""
@author = Paolo Grasso

How to use:
    Send a PUT request with Postman with:

        destination = 0.0.0.0:8080/operation
        body (raw) = {"command": "add","operands": [10, 9, 8, 7, 6, 5, 3, 2, 1]}

Valid commands:
    add, mul, val, div
"""
import json
import cherrypy


class Calculator():

    def add(self, vect):
        self.vect = vect
        res = 0

        for i in range(len(self.vect)):
            res += int(self.vect[i])

        return res

    def sub(self, vect):
        self.vect = vect
        res = 0

        for i in range(len(self.vect)):
            res -= int(self.vect[i])

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
        self.data = {'operands':self.operands, 'operator':operator, 'result':result}
        return json.dumps(self.data)


class Operation(Calculator):
    exposed = True

    def PUT (self, *uri, **params):
        body = json.loads(cherrypy.request.body.read())  # Read body data
        myCalc = Calculator()

        if body["command"] == "add":
            res = myCalc.add(body["operands"])
            myJson = myCalc.printjson('add', body["operands"], res)

        if body["command"] == "sub":
            res = myCalc.sub(body["operands"])
            myJson = myCalc.printjson('sub', body["operands"], res)

        if body["command"] == "mul":
            res = myCalc.mul(body["operands"])
            myJson = myCalc.printjson('mul', body["operands"], res)

        if body["command"] == "div":
            res = myCalc.div(body["operands"])
            myJson = myCalc.printjson('div', body["operands"], res)

        return myJson


if __name__ == '__main__':
    conf = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True
		}
	}

    cherrypy.tree.mount (Operation(), '/operation', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
