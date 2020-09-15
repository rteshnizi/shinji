import flask
from flask_cors import CORS
from src.Parser import Parser
from src.GroupService import GroupService
from src.Utils.FlaskErrors import GenericError, NotInitialized

app = flask.Flask(__name__)
CORS(app)
app.parser = None
app.GroupService: GroupService = None

@app.errorhandler(GenericError)
def handle_invalid_usage(error):
	response = flask.jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route("/init")
def init():
	app.parser = Parser()
	app.GroupService = GroupService(load=False, parser=app.parser)
	return flask.jsonify(repr(app.GroupService))

@app.route("/")
def getAll():
	"""
	Returns
	===
	JSON object of all groups and words
	"""
	try:
		app.GroupService = GroupService(load=not app.parser, parser=app.parser)
	except Exception as err:
		raise GenericError(err.message if hasattr(err, "message") else repr(err))
	return flask.jsonify(app.GroupService.groups)

@app.route("/group/<groupName>")
def getGroup(groupName):
	"""
	Returns
	===
	JSON object of the group if it exists, empty object otherwise.
	"""
	if groupName not in app.GroupService.groups.keys(): return flask.jsonify(dict())
	return flask.jsonify({ groupName: app.GroupService.groups[groupName] })


@app.route("/save")
def save():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.GroupService.save())

@app.route("/load")
def load():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.GroupService.load())

@app.route("/add/<groupName>/<word>")
def addToGroup(groupName, word):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.GroupService.addToGroup(groupName, word))

@app.route("/createGroup/<groupName>")
def createGroup(groupName):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.GroupService.createGroup(groupName))

@app.route("/deleteGroup/<groupName>")
def deleteGroup(groupName):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	return flask.jsonify(app.GroupService.deleteGroup(groupName))
