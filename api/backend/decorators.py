# -*- coding: utf-8 -*-
"""
Decorators used in the API
"""
import json
from django.utils import timezone

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import available_attrs
from django.utils.six import wraps

from api.backend.services import OauthService
from api.models import token_expiry
from base.backend.utilities import get_request_data


def ensure_authenticated(view_func):
	"""
	Checks if the request is from a valid System. Checks the originating client_id as well as supplied token.
	If successful, sets the `request.system` variable accordingly.
	"""

	def wrapped_view(*args, **kwargs):
		"""This method wraps the decorated method."""
		is_checked = False
		for k in args:
			if isinstance(k, WSGIRequest):
				request_data = get_request_data(k)
				token = request_data.get("token", None)
				if token:
					is_checked = True
					oauth = OauthService().filter(
						token = token, expires_at__gt = timezone.now(),
						state__name = "Active").first()
					if not oauth:
						response = HttpResponse(
							json.dumps({
								'status': 'failed', 'message': 'Unauthorized. Invalid credentials.', 'code':
									'800.403.001'
							}),
							content_type = 'application/json', status = 401)
						response['WWW-Authenticate'] = 'Bearer realm=api'
						return response
					OauthService().update(oauth.id, expires_at= token_expiry())
					setattr(k, 'app_user', oauth.app_user)
				else:
					return JsonResponse({
						'status': 'failed', 'message': 'Unauthorized. Authorization parameters not Found!',
						'code': '800.403.001'
					}, status = 401)
		if not is_checked:
			response = HttpResponse(
				json.dumps({'status': 'failed', 'message': 'Unauthorized. Credentials not Provided.',
					           'code': '800.403.001'}),
				content_type = 'application/json', status = 401)
			response['WWW-Authenticate'] = 'Bearer realm=api'
			return response
		return view_func(*args, **kwargs)

	return wraps(view_func, assigned = available_attrs(view_func))(wrapped_view)
