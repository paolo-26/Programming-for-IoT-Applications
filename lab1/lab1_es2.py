#!/usr/bin/env python3
"""
@author = Paolo Grasso
"""
import json


def callMethod(str):
    return getattr(sys.module[__name__], str)


class Calculator():

    def __init__(self, filename):
        self.exitflag = 0
        self.filename = filename
        self.data = {}
        self.data['operations'] = []

    def run(self):
        self.f_list = ["add", "sub", "mul", "div", "exit", "printjson"]

        while True:
            x = input("What do you want to do?\n")

            if (x == "exit" or x == "quit"):
                self.exit()
                break

            #try:
            x = x.split()
            #if len(x) < 3:
            #   raise Exception()
            y = [x[i+1] for i in range(len(x)-1)]
            #print('y=',y)
            #print('function=',x[0])

            if (x[0] not in self.f_list):
                raise Exception("Invalid command")

            else:
                function = getattr(self, x[0])
                res = function(y)
                #print(res)
                self.printjson(x[0], y, res, self.filename)
                break

            #except Exception:
                #print("Command not found")

    def add(self, vect):
        self.vect = vect
        res = 0

        for i in range(len(self.vect)):
            res += float(self.vect[i])

        return res

    def sub(self, vect):
        self.vect = vect
        res = 0

        for i in range(len(self.vect)):
            res -= float(self.vect[i])

        return res

    def mul(self, vect):
        self.vect = vect
        res = 1

        for i in range(len(self.vect)):
            res *= float(self.vect[i])

        return res

    def div(self, vect):
        self.vect = vect

        for i in range(1,len(self.vect)):

            if float(self.vect[i]) == 0:
                res="ERR DIV0"
                return res

        self.vect = vect
        res = float(self.vect[0])

        for i in range(1,len(self.vect)):
            res /= float(self.vect[i])

        return res


    def exit(self):
        print("Quitting program...")
        self.exitflag = 1

    def printjson(self, operator, operands, result, filename):
        self.operands = [float(i) for i in operands]

        self.data['operations'].append({'operator':operator,
            'operands':self.operands,
            'result':result})
        #print(json.dumps(dict))

        with open(filename, 'w') as outfile:
            #print("File aperto")
            json.dump(self.data, outfile, ensure_ascii=False)
        #print("File chiuso")


if __name__ == '__main__':
    mycalculator=Calculator("calculator.json")
    while mycalculator.exitflag == 0:
        mycalculator.run()
