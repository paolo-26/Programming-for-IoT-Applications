#!/usr/bin/env python3
"""
@author = Paolo Grasso
http://0.0.0.0:8080/?json={%22par%22:%20%22users%22,%22id%22:%20%22001%22}
http://0.0.0.0:8080/?json={%22par%22:%20%22users%22,%22id%22:%20%22all%22}

"""

import json
import cherrypy
import time
import datetime
import requests
from threading import Thread

FILENAME = "info.json"


class MyCatalog(object):

    def __init__(self, filename):
        self.filename = filename

    def load_file(self):

        with open(self.filename, "r") as f:
            self.data = json.loads(f.read())

    def save_file(self):

        with open(self.filename, "w") as f:
            json.dump(self.data, f, ensure_ascii=False)

    def get_broker(self):
        self.load_file()
        res = self.data["broker"]
        return res

    def get_device(self, id):
        self.load_file()

        if id == 'all':
            res = self.data["devices"]

        else:
            res = [d for d in self.data["devices"] if d["id"] == id]

            try:
                res = res[0]

            except:
                pass

        return res

    def get_user(self, id):
        self.load_file()

        if id == 'all':
            res = self.data["users"]

        else:
            res = [u for u in self.data["users"] if u["id"] == id]

            try:
                res = res[0]

            except:
                pass

        return res

    def insert(self, ud, dict):
        self.load_file()

        if ud == 'user':
            b = self.check_id('user', dict['id'])

            if b:
                self.data["users"].append(dict)

        if ud == 'device':
            b = self.check_id('device', dict['id'])

            if b:
                self.data["devices"].append(dict)

        self.save_file()
        return b

    def check_id(self, ud, id):
        b = 1

        if ud == 'user':
            ids = [u['id'] for u in self.data['users']]

            if id in ids:
                b = 0

        if ud == 'device':
            ids = [d['id'] for d in self.data['devices']]

            if id in ids:
                b = 0

        return b

    def delete(self):
        self.load_file()
        old = [d['id'] for d in self.data['devices'] if time.time()-float(d['timestamp']) > 120]
        if len(old) > 0:
            self.data['devices'] = [d in self.data['devices'] for d in self.data['devices'] if not d['id'] in old]
            self.save_file()

class WebServer(object):
    exposed = True

    def __init__(self, filename):
        self.calc = MyCatalog(filename)

    @cherrypy.tools.json_out()
    def GET(self, *uri, **params):

        if len(uri) > 1:
            raise cherrypy.HTTPError(404, "Resource not found")

        json_in = json.loads(params['json'])

        if json_in['par'] == 'broker':
            info = self.calc.get_broker()

        if json_in['par'] == 'devices':
            id = json_in['id']
            info = self.calc.get_device(id)

            if len(info) == 0:
                raise cherrypy.HTTPError(404, "Device not found")

        if json_in['par'] == 'users':
            id = json_in['id']
            info = self.calc.get_user(id)

            if len(info) == 0:
                raise cherrypy.HTTPError(404, "User not found")
        try:
            return info

        except:
            raise cherrypy.HTTPError(422, "Incorrect search parameter")

    def POST(self):
        pass

    def PUT(self, *uri, **params):

        try:

            if uri[0] == 'add':

                try:
                    dict = json.loads(cherrypy.request.body.read())
                    par = dict['par']

                except:
                    raise SyntaxError

                if par == 'user':

                    try:
                        del dict['par']
                        id = dict['id']
                        name = dict['name']
                        surname = dict['surname']
                        email = dict['email']

                    except:
                        raise SyntaxError

                    b = self.calc.insert('user',dict)

                    if b == 0:
                        print ("exist")
                        raise FileExistsError

                elif par == 'device':

                    try:
                        del dict['par']
                        id = dict['id']
                        endpoints = dict['end-points']
                        res = dict['res']
                        timestamp = {"timestamp": str(time.time())}
                        dict.update(timestamp)

                    except:
                        raise SyntaxError
                    b = self.calc.insert('device',dict)

                    if b == 0:
                        raise FileExistsError

                else:
                    raise SyntaxError

            #raise SyntaxError

            else:
                raise SyntaxError

        except FileExistsError:
            print("ex1")
            raise cherrypy.HTTPError(400, "ID already present")

        except SyntaxError:
            print("ex2")
            raise cherrypy.HTTPError(422, "Wrong syntax")

        cherrypy.response.status = "200"
        return "OK"

    def DELETE(self, *uri, **params):

        if uri[0] == 'del':
            self.calc.delete()
            print("deleted")

class OtherThread(Thread):
    def __init__(self, ThreadID):
        Thread.__init__(self)
        self.ThreadID = ThreadID

    def run(self):
        while True:
            print("Ciao")
            r = requests.delete('http://0.0.0.0:8080/del')
            time.sleep(60)

class MainThread(Thread):
    def __init__(self, ThreadID):
        Thread.__init__(self)
        self.ThreadID = ThreadID

    def run(self):
        conf = {
            '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            }
        }
        cherrypy.tree.mount (WebServer(FILENAME), '/', conf)
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        cherrypy.config.update({'server.socket_port': 8080})
        cherrypy.engine.start()
        cherrypy.engine.block()

if __name__ == '__main__':
    main_thread = MainThread(1)
    other_thread = OtherThread(2)
    main_thread.start()
    time.sleep(5)
    other_thread.start()
