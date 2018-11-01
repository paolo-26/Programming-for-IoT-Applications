"""
@author = Paolo Grasso
"""
import json


def callMethod(str):
    return getattr(sys.module[__name__], str)


class Calculator():
    
    def __init__(self):
        self.exitflag=0

    def run(self):
        self.f_list=["add","sub","mul","div","exit","printjson"]

        while True:
            x = input("What do you want to do?\n")
            if (x == "exit"):
                self.exit()
                break

            try:
                x=x.split()
                if len(x) != 3:
                    raise Exepction()

                self.num1=int(x[1])
                self.num2=int(x[2])

                if (x[0] not in self.f_list):
                    raise Exception()

                else:
                    function=getattr(self,x[0])
                    res=function()
                    self.printjson(x[0],x[1],x[2],res)
                    break

            except:
                print("Command not found")
                
    def add(self):
        return self.num1 + self.num2 

    def sub(self):
        return self.num1 - self.num2

    def mul(self):
        return self.num1 * self.num2

    def div(self):
        if (self.num2 == 0):
            return 'ERR div by 0'
        else:
            return self.num1 / self.num2

    def exit(self):
        print("Quitting program...")
        self.exitflag=1

    def printjson(self, operator, operand1, operand2, result):
        dict = {'operator':operator, 'operand1':operand1, 'operand2':operand2, 'result':result}
        print(json.dumps(dict))
        pass


if __name__ == '__main__':
    mycalculator = Calculator()
    while mycalculator.exitflag == 0:
        mycalculator.run()