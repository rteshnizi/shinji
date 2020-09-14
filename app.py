import flask
from src.Parser import Parser
from src.Groupizer import Groupizer

app = flask.Flask(__name__)
parser = Parser()
groupizer = Groupizer(load=False, parser=parser)

@app.route("/")
def getGroups():
	"""
	Returns
	===
	JSON object of all groups and words
	"""
	return flask.jsonify(groupizer.groups)

@app.route("/save")
def save():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(groupizer.save())

@app.route("/load")
def load():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(groupizer.load())

@app.route("/add/<groupName>/<word>")
def addToGroup(groupName, word):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(groupizer.addToGroup(groupName, word))
