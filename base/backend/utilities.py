import json
import logging

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


def get_client_ip(request):
	"""
	Gets the client IP address.
	@param request: The request we received from the request pipeline.
	@type request: WSGIRequest
	@return: The IP address of the client.
	@rtype: str
	"""
	try:
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', False)
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR', None)
		return ip
	except Exception as e:
		lgr.exception('get_client_ip Exception: %s' % e)
	return ''


def format_duration(duration):
	seconds = int(duration.total_seconds())
	periods = [
		('year', 60 * 60 * 24 * 365),
		('month', 60 * 60 * 24 * 30),
		('day', 60 * 60 * 24),
		('hour', 60 * 60),
		('minute', 60),
		('second', 1)
	]

	strings = []
	for period_name, period_seconds in periods:
		if seconds > period_seconds:
			period_value, seconds = divmod(seconds, period_seconds)
			is_plural = 's' if period_value > 1 else ''
			strings.append("%s %s%s" % (period_value, period_name, is_plural))

	return ", ".join(strings)
