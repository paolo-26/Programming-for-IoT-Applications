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

FILENAME = "info.json"


class MyCatalog(object):
    exposed = True

    def __init__(self, filename):
        self.filename = filename

    @cherrypy.tools.json_out()
    def GET(self, *uri, **params):

        with open(self.filename, "r") as f:
            data = json.loads(f.read())

        if len(uri) > 1:
            raise cherrypy.HTTPError(404, "Resource not found")

        json_in = json.loads(params['json'])
        if json_in['par'] == 'broker':
            info = data["broker"]

        if json_in['par'] == 'devices':
            id = json_in['id']

            if id == 'all':
                info = data["devices"]

            else:
                info = [d for d in data["devices"] if d["id"] == id]

                try:
                    info = info[0]
                except:
                    raise cherrypy.HTTPError(404, "Device not found")

        if json_in['par'] == 'users':
            id = json_in['id']

            if  id == 'all':
                info = data["users"]

            else:
                info = [d for d in data["users"] if d["id"] == id]

                try:
                    info = info[0]
                except:
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

                if uri[1] == 'user':
                    with open(self.filename, "r") as f:
                        data = json.loads(f.read())
                        
                    try:
                        dict = json.loads(cherrypy.request.body.read())
                    except:
                        raise SyntaxError

                    try:
                        id = dict['id']
                        name = dict['name']
                        surname = dict['surname']
                        email = dict['email']

                    except:
                        raise SyntaxError

                    check = [d['id'] for d in data['users']]
                    if id in check:
                        raise FileExistsError

                    data["users"].append(dict)

                    with open(self.filename, "w") as f:
                        json.dump(data, f, ensure_ascii=False)





                elif uri[1] == 'device':
                    with open(self.filename, "r") as f:
                        data = json.loads(f.read())
                    try:
                        dict = json.loads(cherrypy.request.body.read())
                    except:
                        raise SyntaxError

                    try:
                        id = dict['id']
                        endpoints = dict['end-points']
                        res = dict['res']
                        timestamp = {"timestamp": str(time.time())}

                    except:
                        raise SyntaxError

                    check = [d['id'] for d in data['devices']]

                    if id in check:
                        raise FileExistsError

                    dict.update(timestamp)
                    data["devices"].append(dict)

                    with open(self.filename, "w") as f:
                        json.dump(data, f, ensure_ascii=False)

                else:
                    raise SyntaxError

            else:
                raise SyntaxError

        except FileExistsError:
            print("ex1")
            raise cherrypy.HTTPError(400, "userID already present")

        except SyntaxError:
            print("ex2")
            raise cherrypy.HTTPError(422, "Wrong syntax")

        cherrypy.response.status = "200"
        return "OK"

    def DELETE(self):
        pass


if __name__ == '__main__':
    conf = {
        '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': True,
        }
    }
    cherrypy.tree.mount (MyCatalog(FILENAME), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
