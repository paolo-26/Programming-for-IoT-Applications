#!/usr/bin/env python3
"""
@author = Paolo Grasso
"""

import json
import cherrypy
import requests

OP = ' - add\n - sub\n - mul\n - div'
INP = '\n > '

class Application(object):

    def __init__(self, filename):
        self.filename = filename

        with open(self.filename, 'r') as infile:
            self.data = json.load(infile)

        self.options = ['search', 'insert', 'print_all',
                        'exit', 'quit', 'delete']

    def run(self):

        while True:
            inp = input('\nWhat do you want to do?\n - search\n'
            ' - insert\n - print_all\n - delete\n - exit\n-> ')
            inp = inp.split()

            if inp[0] not in self.options:
                print("Invalid command")

            if inp[0] == 'exit' or inp == 'quit':
                print("Quitting program...\a")
                break

            if inp[0] == 'print_all':
                r = requests.get('http://0.0.0.0:8080/print')
                print(json.dumps(r.json(), indent=4))

            if inp[0] == 'insert':
                chk = requests.get('http://0.0.0.0:8080/check?title='+inp[2])

                if int(chk.text) == 0:
                    r = requests.put('http://0.0.0.0:8080/insert?artist='+
                                      inp[1]+
                                     '&title='+inp[2]+
                                     '&year='+inp[3]+
                                     '&tracks='+inp[4])
                    print("\n-> New album inserted\a")

                else:
                    print("Disk %s is already present in the discography"
                           %inp[2])

                    while True:
                        up = input("Do you want to update data about %s? "
                        "(y/n)\n-> " % inp[2])

                        if up == 'y' or up == 'Y':
                            print('Updating data...')
                            r = requests.put('http://0.0.0.0:8080'+
                                             '/update?artist='+inp[1]+
                                             '&title='+inp[2]+
                                             '&year='+inp[3]+
                                             '&tracks='+inp[4])
                            break

                        elif up == 'n' or up == 'N':
                            break

            if inp[0] == 'search':
                r = requests.get('http://0.0.0.0:8080/search?by='+inp[1])
                print(json.dumps(r.json(), indent=4))

            if inp[0] == 'delete':
                r = requests.delete('http://0.0.0.0:8080/'+
                                   '?title='+inp[1])
                print('\n-> Album deleted!\a')


if __name__ == '__main__':
    app = Application('discography.json')
    app.run()
