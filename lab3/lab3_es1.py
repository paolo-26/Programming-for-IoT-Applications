#!/usr/bin/env python3
"""
@author = Paolo Grasso
Run 'calculator.py' in order to use this script.
"""
import json
import requests

OP = ' - add\n - sub\n - mul\n - div'
INP = '\n > '


class Application(object):

    def __init__(self):
        self.run()

    def run(self):

        while True:
            inp = input('What do you want to do?\n'+OP+INP)
            inp = inp.split()
            operand = inp[0]

            if (operand == 'exit') or (operand == 'quit'):
                print('Quitting program...\a')
                break

            else:
                try:
                    op1 = inp[1]
                    op2 = inp[2]
                    res = requests.get('http://0.0.0.0:8080/'+operand+
                                       '?op1='+op1+'&op2='+op2)
                    try:
                        res_json = res.json()
                        self.print_results(res_json)

                    except:
                        print("HTTP error: - Status code: %d" % res.status_code)

                except:
                    print("You must insert two operands")


    def print_results(self,res_json):
        operator = res_json['operator']
        op1 = float(res_json['operand 1'])
        op2 = float(res_json['operand 2'])
        res = float(res_json['result'])
        print('\n  First operand: %.2f\n  Second operand: %.2f\n'
        '  Operator: %s\n  Result: %.2f\n' %(op1, op2, operator, res))


if __name__ == '__main__':
    app = Application()
