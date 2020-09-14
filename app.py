import flask
from src.Parser import Parser
from src.Groupizer import Groupizer
from src.Utils.FlaskErrors import GenericError, NotInitialized

app = flask.Flask(__name__)
app.groupizer: Groupizer = None

@app.errorhandler(GenericError)
def handle_invalid_usage(error):
	response = flask.jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route("/init")
def init():
	parser = Parser()
	app.groupizer = Groupizer(load=False, parser=parser)
	return flask.jsonify(repr(app.groupizer))

@app.route("/")
def getGroups():
	"""
	Returns
	===
	JSON object of all groups and words
	"""
	if app.groupizer is None:
		raise NotInitialized()
	return flask.jsonify(app.groupizer.groups)

@app.route("/save")
def save():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.groupizer.save())

@app.route("/load")
def load():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.groupizer.load())

@app.route("/add/<groupName>/<word>")
def addToGroup(groupName, word):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.groupizer.addToGroup(groupName, word))
