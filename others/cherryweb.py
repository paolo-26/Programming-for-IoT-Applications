import cherrypy
import random
import string

class HelloWorld(object):
	@cherrypy.expose
	def index(self):
		return "Error 404: Not found"

	@cherrypy.expose
	def generate(self):
		return ''.join(random.sample(string.hexdigit,8))

if __name__ == '__main__':
	cherrypy.tree.mount(HelloWorld())
	cherrypy.engine.start()
	cherrypy.engine.block()