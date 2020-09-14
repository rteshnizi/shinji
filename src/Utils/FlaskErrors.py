from flask import jsonify

class GenericError(Exception):
	"""
	https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
	"""
	status_code = 500

	def __init__(self, message, status_code=None, payload=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.payload = payload

	def to_dict(self):
		rv = dict(self.payload or ())
		rv["status_code"] = self.status_code
		rv["message"] = self.message
		return rv

class NotInitialized(GenericError):
	def __init__(self):
		super().__init__("Groupizer is not intialized. You might want to call /init first.")
