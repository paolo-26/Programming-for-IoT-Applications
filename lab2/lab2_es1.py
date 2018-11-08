import random
import cherrypy


class Calculator(objet):
	@cherrypy.expose
	def index(self):
		return "Error 404: Not found"