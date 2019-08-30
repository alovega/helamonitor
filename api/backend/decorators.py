# -*- coding: utf-8 -*-
"""
Decorators used in the API
"""
import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import available_attrs
from django.utils.six import wraps

from core.backend.services import SystemCredentialService
from base.backend.utilities import get_request_data, get_client_ip


def ensure_authenticated(view_func):
	"""
	Checks if the request is from a valid System. Checks the originating IP as well as supplied password.
	If successful, sets the `request.system` variable accordingly.
	"""

	def wrapped_view(*args, **kwargs):
		"""This method wraps the decorated method."""
		is_checked = False
		for k in args:
			if isinstance(k, WSGIRequest):
				request_data = get_request_data(k)
				ip = get_client_ip(k)
				code = request_data.get("code", None)
				password = request_data.get("password", None)
				if code and password:
					is_checked = True
					oauth = SystemCredentialService().filter(
						system__code = code, password = password, allowed_ip = ip.strip(),
						state__name = "Active").first()
					if not oauth:
						response = HttpResponse(
							json.dumps({
								'status': 'failed', 'message': 'Unauthorized. Invalid credentials.', 'code': '401'
							}),
							content_type = 'application/json', status = 401)
						response['WWW-Authenticate'] = 'Bearer realm=api'
						return response
					setattr(k, 'system', oauth.system)
				else:
					return JsonResponse({
						'status': 'failed', 'message': 'Unauthorized. Authorization parameters not Found!',
						'code': '401'
					}, status = 401)
		if not is_checked:
			response = HttpResponse(
				json.dumps({'status': 'failed', 'message': 'Unauthorized. Credentials not Provided.', 'code': '401'}),
				content_type = 'application/json', status = 401)
			response['WWW-Authenticate'] = 'Bearer realm=api'
			return response
		return view_func(*args, **kwargs)

	return wraps(view_func, assigned = available_attrs(view_func))(wrapped_view)
