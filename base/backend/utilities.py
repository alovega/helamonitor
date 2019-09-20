import json
import logging
import base64

lgr = logging.getLogger(__name__)


def get_request_data(request):
	"""
	Retrieves the request data irrespective of the method and type it was send.
	@param request: The Django HttpRequest.
	@type request: WSGIRequest
	@return: The data from the request as a dict
	@rtype: dict
	"""
	try:
		data = None
		if request is not None:
			request_meta = getattr(request, 'META', {})
			request_method = getattr(request, 'method', None)
			if request_meta.get('CONTENT_TYPE', '') == 'application/json':
				data = json.loads(request.body)
			elif str(request_meta.get('CONTENT_TYPE', '')).startswith('multipart/form-data;'):  # Special handling for
				# Form Data?
				data = request.POST.copy()
				data = data.dict()
			elif request_method == 'GET':
				data = request.GET.copy()
				data = data.dict()
			elif request_method == 'POST':
				data = request.POST.copy()
				data = data.dict()
			if not data:
				request_body = getattr(request, 'body', None)
				if request_body:
					data = json.loads(request_body)
				else:
					data = dict()
			return data
	except Exception as e:
		lgr.exception('get_request_data Exception: %s', e)
	return dict()


def generate_access_token():
	"""
	Generates an unique token to be used for authorizing access of api endpoints
	@return: The token to be used for api authentication
	@rtype: str | None
	"""
	import os
	token = None
	try:
		token = base64.b64encode(os.urandom(15).encode('hex'))
	except Exception as ex:
		lgr.exception('Generate access token exception %s' % ex)
	return token
