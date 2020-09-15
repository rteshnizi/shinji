import flask
from flask_cors import CORS
from src.Parser import Parser
from src.GroupService import GroupService
from src.Utils.FlaskErrors import GenericError, NotInitialized

app = flask.Flask(__name__)
CORS(app)
app.parser = None
app.groupService: GroupService = None

@app.errorhandler(GenericError)
def handleError(error):
	response = flask.jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route("/init")
def init():
	app.parser = Parser()
	app.groupService = GroupService(load=False, parser=app.parser)
	return flask.jsonify(repr(app.groupService))

@app.route("/")
def getAll():
	"""
	Returns
	===
	JSON object of all groups and words
	"""
	if app.groupService is None:
		raise NotInitialized()
	return flask.jsonify(app.groupService.groups)

@app.route("/group/<groupName>")
def getGroup(groupName):
	"""
	Returns
	===
	JSON object of the group if it exists, empty object otherwise.
	"""
	if app.groupService is None:
		raise NotInitialized()
	if groupName not in app.groupService.groups.keys(): return flask.jsonify(dict())
	return flask.jsonify({ groupName: app.groupService.groups[groupName] })


@app.route("/save")
def save():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	if app.groupService is None:
		raise NotInitialized()
	return flask.jsonify(app.groupService.save())

@app.route("/load")
def load():
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	try:
		app.groupService = GroupService(load=True)
	except Exception as err:
		raise GenericError(err.message if hasattr(err, "message") else repr(err))
	return flask.jsonify()

@app.route("/add/<groupName>/<word>")
def addToGroup(groupName, word):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	if app.groupService is None:
		raise NotInitialized()
	return flask.jsonify(app.groupService.addToGroup(groupName, word))

@app.route("/createGroup/<groupName>")
def createGroup(groupName):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	if app.groupService is None:
		raise NotInitialized()
	return flask.jsonify(app.groupService.createGroup(groupName))

@app.route("/deleteGroup/<groupName>")
def deleteGroup(groupName):
	"""
	Returns
	===
	A JSON string of the error if an exception occurred, empty string otherwise.
	"""
	if app.groupService is None:
		raise NotInitialized()
	return flask.jsonify(app.groupService.deleteGroup(groupName))
