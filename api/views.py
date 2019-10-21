# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import calendar
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

from api.models import token_expiry
from api.backend.interfaces.event_log import EventLog
from api.backend.interfaces.incident_administration import IncidentAdministrator
from api.backend.interfaces.rules_administration import EscalationRuleAdministrator
from api.backend.interfaces.health_monitor import MonitorInterface
from api.backend.interfaces.system_administration import SystemAdministrator
from api.backend.services import OauthService, AppUserService
from api.backend.decorators import ensure_authenticated
from base.backend.utilities import get_request_data, generate_access_token
from base.backend.services import StateService
from core.backend.services import SystemService


lgr = logging.getLogger(__name__)


@csrf_exempt
@ensure_authenticated
def report_event(request):
	"""
	Creates an event reported from an external system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful event creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		event = EventLog.log_event(
			event_type = data.get('event_type'), system = data.get('system'), interface = data.get('interface'),
			response = data.get('response'), request = data.get('request'), code = data.get('code'),
			description = data.get('description')
		)
		return JsonResponse(event)
	except Exception as ex:
		lgr.exception("Event logging Exception: %s" % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def create_incident(request):
	"""
	Creates incidents from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful incident creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident = IncidentAdministrator.log_incident(
			incident_type = data.get('incident_type'), system = data.get('system'), name = data.get('name'),
			escalation_level = data.get('escalation_level'), description = data.get('description'),
			priority_level = data.get('priority_level'), event_type = data.get('event_type', None),
			state = data.get('state', 'Investigating'), escalated_events = data.get('escalated_events', None),
			scheduled_for = data.get('scheduled_for'), scheduled_until = data.get('scheduled_until')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def update_incident(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful incident creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_incident = IncidentAdministrator.update_incident(
			incident_id = data.get('incident_id'), escalation_level = data.get('escalation_level'),
			state = data.get('state'), description = data.get('description'), user = data.get('user'),
			priority_level = data.get('priority_level'), name = data.get('name')
		)
		return JsonResponse(updated_incident)
	except Exception as ex:
		lgr.exception('Incident update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def health_check(request):
	"""
	Performs health check for all registered systems
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code of a success/fail and a data containing dictionary containing a list of registered
	system statuses
	@rtype:dict
	"""
	try:
		data = MonitorInterface.perform_health_check()
		return JsonResponse(data)
	except Exception as ex:
		lgr.exception('Health check interface  Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_incident(request):
	"""
	Get a specific incident
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested incident or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident = IncidentAdministrator.get_incident(
			system = data.get('system'), incident_id = data.get('incident_id')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_incidents(request):
	"""
	Get incidents within a specified date range
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested incidents or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident = IncidentAdministrator.get_incidents(
			system = data.get('system'), start_date = data.get('start_date'), end_date = data.get('end_date')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
def get_access_token(request):
	"""
	Generates an access token for valid app users
	@param request:
	@type request: DJANGO WSGIRequest
	@return: An access token and its expiry time or a response code indicating invalid credentials supplied
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		app_user = AppUserService().get(app__id = data.get('client_id'), user__username = data.get('username'))
		if app_user is not None:
			user = check_password(data.get('password'), app_user.user.password)
			if user:
				oauth = OauthService().filter(
					app_user = app_user, expires_at__gt = timezone.now(), state__name = 'Active').first()
				if oauth:
					oauth = OauthService().update(pk = oauth.id, expires_at = token_expiry())
				else:
					oauth = OauthService().create(
						app_user = app_user, token = generate_access_token(), state = StateService().get(name = 'Active')
					)
				if not oauth:
					return JsonResponse({'code': '800.400.001'})
				return JsonResponse({'code': '800.200.001', 'data': {
					'token': str(oauth.token), 'expires_at': calendar.timegm(oauth.expires_at.timetuple())}
				})
		return JsonResponse({'code': '800.403.001'})
	except Exception as ex:
		lgr.exception("Get Access token Exception %s " % ex)
	return JsonResponse({'code': '800.400.001'})


@csrf_exempt
@ensure_authenticated
def create_rule(request):
	"""
	Creates Escalation rules
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rule = EscalationRuleAdministrator.create_rule(
			name = data.get('name'), description = data.get('description'), system = data.get('system'),
			nth_event = data.get('nth_event'), state = data.get('state'), duration = data.get('duration'),
			escalation_level = data.get('escalation_level')
		)
		return JsonResponse(rule)
	except Exception as ex:
		lgr.exception('Rule creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def update_rule(request):
	"""
	Updates Escalation rules
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rule = EscalationRuleAdministrator.update_rule(
			rule_id = data.get('rule_id'), name = data.get('name'), description = data.get('description'),
			nth_event = data.get('nth_event'), state = data.get('state'), duration = data.get('duration'),
			escalation_level = data.get('escalation_level'), event_type = data.get('event_type')
		)
		return JsonResponse(rule)
	except Exception as ex:
		lgr.exception('Rule creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_rule(request):
	"""
	Retrieves an Escalation rule
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rule = EscalationRuleAdministrator.get_rule(
			rule_id = data.get('rule_id'), system_id = data.get('system_id')
		)
		return JsonResponse(rule)
	except Exception as ex:
		lgr.exception('Rule creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_rules(request):
	"""
	Retrieves all rules for a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rules = EscalationRuleAdministrator.get_rules(system_id = data.get('system_id'))
		return JsonResponse(rules)
	except Exception as ex:
		lgr.exception('Rule creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_rule(request):
	"""
	Delete a rule for a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rules = EscalationRuleAdministrator.delete_rule(
			rule_id = data.get('rule_id'), system_id = data.get('system_id'))
		return JsonResponse(rules)
	except Exception as ex:
		lgr.exception('Rule creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def create_system(request):
	"""
	Creates a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rules = SystemAdministrator.create_system(
			name = data.get('name'), description = data.get('description'))
		return JsonResponse(rules)
	except Exception as ex:
		lgr.exception('System creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def update_system(request):
	"""
	Updates a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		rules = SystemAdministrator.update_system(
			system_id = data.get('system_id'), name = data.get('name'), description = data.get('description'))
		return JsonResponse(rules)
	except Exception as ex:
		lgr.exception('System creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_system(request):
	"""
	Retrieve a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return:The system or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		system = SystemAdministrator.get_system(system_id = data.get('system_id'))
		return JsonResponse(system)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_systems(request):
	"""
	Retrieve a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return:The system or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		systems = SystemAdministrator.get_systems()
		return JsonResponse(systems)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_system(request):
	"""
	Deletes a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return:The system or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		deleted_system = SystemAdministrator.delete_system(system_id = data.get('system_id'))
		return JsonResponse(deleted_system)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})
