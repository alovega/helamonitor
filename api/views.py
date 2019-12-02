# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import calendar

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

from api.backend.interfaces.recipient_administration import RecipientAdministrator
from api.models import token_expiry
from api.backend.interfaces.event_log import EventLog
from api.backend.interfaces.incident_administration import IncidentAdministrator
from api.backend.interfaces.rules_administration import EscalationRuleAdministrator
from api.backend.interfaces.endpoint_administration import EndpointAdministrator
from api.backend.interfaces.health_monitor import MonitorInterface
from api.backend.interfaces.system_administration import SystemAdministrator
from api.backend.interfaces.user_administration import UserAdministrator
from api.backend.interfaces.notification_interface import NotificationLogger
from api.backend.interfaces.look_up_interface import LookUpInterface
from api.backend.interfaces.dashboard_administration import DashboardAdministration
from api.backend.interfaces.table_interface import TableData
from api.backend.services import OauthService, AppUserService
from api.backend.decorators import ensure_authenticated
from base.backend.utilities import get_request_data, generate_access_token
from base.backend.services import StateService

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
			event_type = data.get('event_type'), system = data.get('system_id'), interface = data.get('interface'),
			response = data.get('response'), request = data.get('request'), code = data.get('code'),
			description = data.get('description'), stack_trace = data.get('stack_trace'), method = data.get('method')
		)
		return JsonResponse(event)
	except Exception as ex:
		lgr.exception("Event logging Exception: %s" % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_events(request):
	"""
	Get events of a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested recipient or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		recipient = EventLog.get_events(
			system_id = data.get('system_id')
		)
		return JsonResponse(recipient)
	except Exception as ex:
		lgr.exception('Get events Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_event(request):
	"""
	Get an event from a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested recipient or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		event = EventLog.get_event(
			event_id = data.get('event_id'), system_id = data.get('system_id')
		)
		return JsonResponse(event)
	except Exception as ex:
		lgr.exception('Get Event Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_error_rates(request):
	"""
	Retrieves error rates for a system
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful error rate retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		event = DashboardAdministration.get_error_rate(
			system_id = data.get('system_id'), start_date = data.get('start_date'),  end_date = data.get('end_date')
		)
		return JsonResponse(event)
	except Exception as ex:
		lgr.exception("Event error rate get Exception: %s" % ex)
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
		print(data)
		incident = IncidentAdministrator.log_incident(
			incident_type = data.get('incident_type'), system = data.get('system_id'), name = data.get('name'),
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
def past_incidents(request):
	"""
	Retrieves past incidents within a system grouped by into dates
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: dict
	"""
	try:
		data = get_request_data(request)
		incidents = DashboardAdministration.past_incidents(
			system = data.get('system_id'), date_from = data.get('date_from'), date_to = data.get('date_to'))
		return JsonResponse(incidents)
	except Exception as ex:
		lgr.exception('Retrieve past incidents exception %s ' % ex)
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
	return JsonResponse({'code': '800.500.001 %s' % ex})


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
			system = data.get('system_id'), incident_id = data.get('incident_id')
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
			system = data.get('system_id'), incident_type = data.get('incident_type'), states = data.get('states')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_incident(request):
	"""
	Deletes an incident
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A message and a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident = IncidentAdministrator.delete_incident(
			incident_id = data.get('incident_id'), system_id = data.get('system_id')
		)
		return JsonResponse(incident)
	except Exception as ex:
		lgr.exception('Incident delete Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_incident_events(request):
	"""
	Retrieves the events that have caused the incident in a selected system.
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested incident_events or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		incident_events = IncidentAdministrator.get_incident_events(
			system_id = data.get('system_id'), incident_id = data.get('incident_id')
		)
		return JsonResponse(incident_events)
	except Exception as ex:
		lgr.exception('Incident events get Exception: %s' % ex)
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
						app_user = app_user, token = generate_access_token(),
						state = StateService().get(name = 'Active')
					)
				if not oauth:
					return JsonResponse({'code': '800.400.001'})
				return JsonResponse({
					                    'code': '800.200.001', 'data': {
						'token': str(oauth.token), 'expires_at': calendar.timegm(oauth.expires_at.timetuple())
					}
				                    })
		return JsonResponse({'code': '800.403.001'})
	except Exception as ex:
		lgr.exception("Get Access token Exception %s " % ex)
	return JsonResponse({'code': '800.400.001'})


@csrf_exempt
def verify_token(request):
	"""
	Verifies an access token granted to a user
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code and the token with its expiry time
	@rtype: dict
	@param request:
	@return:
	"""
	try:
		data = get_request_data(request)
		token = UserAdministrator.verify_token(data.get('token'))
		return JsonResponse(token)
	except Exception as ex:
		lgr.exception('Verify access token exception %s' % ex)
	return {'code': '800.500.001'}


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
			name = data.get('name'), description = data.get('description'), system = data.get('system_id'),
			nth_event = data.get('nth_event'), duration = data.get('duration'),
			escalation_level = data.get('escalation_level'), event_type = data.get('event_type')
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
			nth_event = data.get('nth_event'), duration = data.get('duration'),
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
			name = data.get('name'), description = data.get('description'), admin_id = data.get('admin'), version =
			data.get('version'))
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
			system = data.get('id'), name = data.get('name'), description = data.get('description'),
			admin_id = data.get('admin'), version = data.get('version')
		)
		return JsonResponse(rules)
	except Exception as ex:
		lgr.exception('System creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
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
		system = SystemAdministrator.get_system(system = data.get('id'))
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
		deleted_system = SystemAdministrator.delete_system(system = data.get('id'))
		return JsonResponse(deleted_system)
	except Exception as ex:
		lgr.exception('Incident get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def create_user(request):
	"""
	Creates a user
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		user = UserAdministrator.create_user(
			username = data.get('username'), password = data.get('password'), email = data.get('email'), first_name =
			data.get('firstname'), last_name = data.get('lastname'))
		return JsonResponse(user)
	except Exception as ex:
		lgr.exception('User creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_user(request):
	"""
	Retrieves a user
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful user retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		user = UserAdministrator.get_user(user_id = data.get('user_id'))
		return JsonResponse(user)
	except Exception as ex:
		lgr.exception('Get User Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_user(request):
	"""
	Deletes a user
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful user deletion or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		user = UserAdministrator.delete_user(user_id = data.get('user_id'))
		return JsonResponse(user)
	except Exception as ex:
		lgr.exception('Delete User Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_users(request):
	"""
	Retrieves all users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful users retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		users = UserAdministrator.get_users()
		return JsonResponse(users)
	except Exception as ex:
		lgr.exception('Get User Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def create_endpoints(request):
	"""
	Creates endpoints from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful endpoint creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		endpoint = EndpointAdministrator.create_endpoint(
			state_id = data.get('state'), endpoint_type_id = data.get('endpoint_type'),
			system_id = data.get('system_id'), name = data.get('name'), description = data.get('description'),
			url = data.get('url'), response_time = data.get('optimal_response_time')
		)
		return JsonResponse(endpoint)
	except Exception as ex:
		lgr.exception('Endpoint creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def update_endpoint(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful endpoint update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_endpoint = EndpointAdministrator.update_endpoint(
			endpoint_id = data.get('endpoint_id'), state_id = data.get('State'),
			response_time = data.get('OptimalResponseTime'), description = data.get('Description'),
			url = data.get('Url'), name = data.get('EndpointName')
		)
		return JsonResponse(updated_endpoint)
	except Exception as ex:
		lgr.exception('Endpoint update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def create_recipient(request):
	"""
	Creates endpoints from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful recipient creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		recipient = RecipientAdministrator.create_recipient(
			state_id = data.get('stateId'), phone_number = data.get('phoneNumber'), user_id = data.get('userId')
		)
		return JsonResponse(recipient)
	except Exception as ex:
		lgr.exception('Recipient creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def create_system_recipient(request):
	"""
	Creates endpoints from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful recipient creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		system_recipient = RecipientAdministrator.create_system_recipient(
			system_id = data.get('systemId'), recipient_id = data.get('Recipient'),
			escalations = data.get('escalations')
		)
		return JsonResponse(system_recipient)
	except Exception as ex:
		lgr.exception('Recipient creation Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def update_recipient(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful recipient update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_recipient = RecipientAdministrator.update_recipient(
			recipient_id = data.get('recipientId'), state_id = data.get('State'),
			phone_number = data.get('PhoneNumber')
		)
		return JsonResponse(updated_recipient)
	except Exception as ex:
		lgr.exception('Recipient update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def update_system_recipient(request):
	"""
	Updates an existing incident's priority, resolution status or user assignment
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful recipient update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		updated_recipient = RecipientAdministrator.update_system_recipient(
			system_recipient_id = data.get('systemRecipientId'), state_id = data.get('State'),
			notification_type_id = data.get('NotificationType')
		)
		return JsonResponse(updated_recipient)
	except Exception as ex:
		lgr.exception('Recipient update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_endpoint(request):
	"""
	Get a specific endpoint
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested endpoint or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		endpoint = EndpointAdministrator.get_endpoint(endpoint_id = data.get('endpoint_id'))
		return JsonResponse(endpoint)
	except Exception as ex:
		lgr.exception('Endpoint get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_recipient(request):
	"""
	Get a specific endpoint
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested recipient or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		recipient = RecipientAdministrator.get_recipient(
			recipient_id = data.get('recipientId')
		)
		return JsonResponse(recipient)
	except Exception as ex:
		lgr.exception('recipient get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_system_recipient(request):
	"""
	Get a specific system recipient
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: The requested recipient or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		recipient = RecipientAdministrator.get_system_recipient(system_recipient_id = data.get('systemRecipientId'))
		return JsonResponse(recipient)
	except Exception as ex:
		lgr.exception('Look up data get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_look_up_data(request):
	"""
	Get a specific endpoint
	@return: The requested recipient or a status code indicating errors if any.
	@rtype: dict
	"""
	try:
		data = LookUpInterface.get_look_up_data()
		return JsonResponse(data)
	except Exception as ex:
		lgr.exception('Look up data get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_recipient(request):
	"""
	Delete a specific Recipient
	@param request:The Django WSGI Request to process
	@return:dict
	"""
	try:
		data = get_request_data(request)
		recipient = RecipientAdministrator.delete_recipient(
			recipient_id = data.get('recipientId')
		)
		return JsonResponse(recipient)

	except Exception as ex:
		lgr.exception('recipient get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_system_recipient(request):
	"""
	Delete a specific Recipient
	@param request:The Django WSGI Request to process
	@return:dict
	"""
	try:
		data = get_request_data(request)
		recipient = RecipientAdministrator.delete_system_recipient(
			system_recipient_id = data.get('systemRecipientId')
		)
		return JsonResponse(recipient)

	except Exception as ex:
		lgr.exception('recipient get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def delete_endpoint(request):
	"""
	Delete a specific Recipient
	@param request:The Django WSGI Request to process
	@return:dict
	"""
	try:
		data = get_request_data(request)
		endpoint = EndpointAdministrator.delete_endpoint(endpoint_id = data.get('endpoint_id'))
		return JsonResponse(endpoint)

	except Exception as ex:
		lgr.exception('recipient get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_notifications(request):
	"""
	Delete a specific Recipient
	@param request:The Django WSGI Request to process
	@return:dict
	"""
	try:
		data = get_request_data(request)
		notifications = NotificationLogger.get_system_notification(system_id = data.get('system_id'))
		return JsonResponse(notifications)

	except Exception as ex:
		lgr.exception('notifications get Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_logged_in_user_details(request):
	"""
	@param request:The Django WSGI Request to process
	@return: dict
	"""
	try:
		data = get_request_data(request)
		user = UserAdministrator.get_logged_in_user_details(token = data.get('token'))
		return JsonResponse(user)
	except Exception as ex:
		lgr.exception('logged in user Details Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def edit_logged_in_user_details(request):
	"""
	@param request: The Django WSGI Request to process
	@return: dict
	"""
	try:
		data = get_request_data(request)
		user = UserAdministrator.edit_logged_in_user_details(
			token = data.get('token'), first_name = data.get('firstName'), last_name = data.get('lastName'),
			email = data.get('email'), password = data.get('password'), phone_number = data.get('phoneNumber'),
			username = data.get('userName'))
		return JsonResponse(user)
	except Exception as ex:
		lgr.exception('edit logged in user Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_logged_in_user_recent_notifications(request):
	"""
	@param request:  The Django WSGI Request to process
	@return: dict
	"""
	try:
		data = get_request_data(request)
		notifications = NotificationLogger.get_logged_in_user_recent_notifications(token = data.get('token'))
		return JsonResponse(notifications)
	except Exception as ex:
		lgr.exception('get logged in user recent notification Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def get_logged_in_user_notifications(request):
	"""
	@param request:  The Django WSGI Request to process
	@return: dict
	"""
	try:
		data = get_request_data(request)
		notifications = NotificationLogger.get_logged_in_user_notifications(token = data.get('token'))
		return JsonResponse(notifications)
	except Exception as ex:
		lgr.exception('get logged in user recent notification Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def edit_logged_in_user_password(request):
	"""
	@param request: The Django WSGI Request to process
	@return: dict
	"""
	try:
		data = get_request_data(request)
		password = UserAdministrator.edit_logged_in_user_password(
			token = data.get('token'), current_password = data.get('currentPassword'), new_password = data.get(
				'password'))
		return JsonResponse(password)
	except Exception as ex:
		lgr.exception('edit logged in user password update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001 %s'})


@csrf_exempt
def get_system_status(request):
	"""
	Retrieves current status of registered endpoints and any current incidents, if any
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code and a dictionary with the current status of a system and any current incidents
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		system_status = DashboardAdministration.get_current_status(system = data.get('system_id'))
		return JsonResponse(system_status)
	except Exception as ex:
		lgr.exception('Get System status exception %s' % ex)
	return {'code': '800.500.001'}


@csrf_exempt
@ensure_authenticated
def get_system_response_time_data(request):
	"""
	@param request: The Django WSGI Request to process
	@return: dict
	"""
	try:
		data = get_request_data(request)
		data = MonitorInterface.get_system_endpoint_response_time(system_id = data.get('system_id'))
		return JsonResponse(data)
	except Exception as ex:
		lgr.exception('edit logged in user password update Exception: %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def edit_user(request):
	"""
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: dict
	"""
	try:
		data = get_request_data(request)
		user = UserAdministrator.update_user(
			user_id = data.get('user_id'), username = data.get('username'), password = data.get('password'),
			email = data.get('email'), first_name = data.get('first_name'), last_name = data.get('last_name'))
		return JsonResponse(user)
	except Exception as ex:
		lgr.exception('Edit User Exception %s ' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def dashboard_widgets_data(request):
	"""
	Retrieves  Dashboard widgets data
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		widget_data = DashboardAdministration.dashboard_widgets_data(
			system = data.get('system_id'), date_from = data.get('date_from'), date_to = data.get('date_to')
		)
		return JsonResponse(widget_data)
	except Exception as ex:
		lgr.exception('Get Dashboard widgets data exception %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def endpoint_table_data(request):
	"""
	Retrieves Endpoint   Table data
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		# parameters = data.get('body')
		data_source = TableData.get_endpoints(
			parameters = data.get('body'), system_id = data.get('system_id')
		)
		return JsonResponse(data_source)
	except Exception as ex:
		lgr.exception('Get Table data %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def recipient_table_data(request):
	"""
	Retrieves  Recipients Table data
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		data_source = TableData.get_recipients(
			parameters = data.get('body')
		)
		return JsonResponse(data_source)
	except Exception as ex:
		lgr.exception('Get Table data %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def system_recipient_table_data(request):
	"""
	Retrieves  System Recipients Table data
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful rule creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		data_source = TableData.get_system_recipients(
			parameters = data.get('body'), system_id = data.get('system_id')
		)
		return JsonResponse(data_source)
	except Exception as ex:
		lgr.exception('Get Table data %s' % ex)
	return JsonResponse({'code': '800.500.001'})


@csrf_exempt
@ensure_authenticated
def event_table_data(request):
	"""
	Retrieves Events table data
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate status and the events table data
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		data_source = TableData.get_events(
			system = data.get('system_id'), parameters = data.get('body')
		)
		return JsonResponse(data_source)
	except Exception as ex:
		lgr.exception('Get events table data %s' % ex)
	return JsonResponse({'code': '800.500.001'})
