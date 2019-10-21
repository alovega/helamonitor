# coding=utf-8
"""
Class for Escalation Rules Administration
"""
from datetime import timedelta
import logging
import dateutil.parser
from django.contrib.auth.models import User
from django.db.models import F, Q

from api.backend.interfaces.notification_interface import NotificationLogger
from core.backend.services import IncidentLogService, IncidentEventService, SystemService, \
	SystemRecipientService, RecipientService, EscalationRuleService
from base.backend.services import StateService, EscalationLevelService, EventTypeService, IncidentTypeService

lgr = logging.getLogger(__name__)


class EscalationRuleAdministrator(object):
	"""
	Class for Escalation Rules Administration
	"""

	@staticmethod
	def create_rule(name, description, system, nth_event, state, escalation_level, duration, **kwargs):
		"""
		Creates an escalation rule for a selected system.
		@param name: Name of the escalation rule to be created
		@type name: str
		@param system: The system which the escalation rule will be applied in
		@type system: str
		@param description: Details on the Escalation Rule
		@type description: str
		@param nth_event: Number of event of a certain type that need to be logged to raise an escalation
		@type nth_event: str
		@param duration:Time period within which certain events muct occur to trigger an escalation.
		@type duration: str
		@param state: State of the incident. Defaults to Active
		@type state: str
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(name = system, state__name = "Active")
			state = StateService().get(name = state)
			escalation_level = EscalationLevelService().get(name = escalation_level, state__name = "Active")

			if system is None or state is None or escalation_level is None:
				return {"code": "800.400.002"}
			escalation_rule = EscalationRuleService().create(
				name = name, description = description, system = system, nth_event = int(nth_event),
				duration = timedelta(seconds = int(duration)), state = state, escalation_level = escalation_level
			)

			if escalation_rule is not None:
				rule = EscalationRuleService().filter(pk = escalation_rule.id, system = system).values(
					'name', 'description', 'date_created', 'date_modified', 'system_id',
					'nth_event', rule_id = F('id'), escalation = F('escalation_level__name'),
					eventtype = F('event_type__name'), status = F('state__name'), system_name = F('system__name')
				).first()
				rule.update(duration = str(escalation_rule.duration))
				return {'code': '800.200.001', 'data': rule}
		except Exception as ex:
			lgr.exception("Escalation Rule Creation exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_rule(
			rule_id, name = None, description = None, nth_event = None, state = None,
			escalation_level = None, duration = None, event_type = None, **kwargs):
		"""
		Updates an escalation rule for a selected system.
		@param rule_id: The id of the rule to be updated
		@type rule_id: str
		@param name: Name of the escalation rule to be created
		@type name: str | None
		@param description: Details on the Escalation Rule
		@type description: str | None
		@param nth_event: Number of event of a certain type that need to be logged to raise an escalation
		@type nth_event: str | None
		@param duration:Time period within which certain events must occur to trigger an escalation.
		@type duration: str | None
		@param event_type: The event type to be applied for an escalation with the rule.
		@type event_type: str | None
		@param state: State of the incident. Defaults to Active
		@type state: str | None
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			escalation_rule = EscalationRuleService().filter(pk = rule_id, state__name = 'Active').first()
			if escalation_rule is None:
				return {"code": "800.400.002"}
			name = name if name is not None else escalation_rule.name
			description = description if description is not None else escalation_rule.description
			nth_event = int(nth_event) if nth_event is not None else escalation_rule.nth_event
			duration = timedelta(seconds = int(duration)) if duration is not None else escalation_rule.duration
			escalation_level = EscalationLevelService().filter(
				name = escalation_level, state__name = 'Active').first() if escalation_level is not None else \
				escalation_rule.escalation_level
			event_type = EventTypeService().filter(
				name = event_type, state__name = 'Active').first() if event_type is not None else \
				escalation_rule.event_type
			state = StateService().filter(name = state).first() if state is not None else escalation_rule.state

			updated_escalation_rule = EscalationRuleService().update(
				pk = escalation_rule.id, name = name, description = description, nth_event = int(nth_event),
				duration = duration, state = state, escalation_level = escalation_level, event_type = event_type
			)

			if updated_escalation_rule is not None:
				rule = EscalationRuleService().filter(pk = escalation_rule.id).values(
					'name', 'description', 'date_created', 'date_modified', 'system_id',
					'nth_event',  rule_id = F('id'), escalation = F('escalation_level__name'), eventtype = F(
						'event_type__name'), status = F('state__name'), system_name = F('system__name')
				).first()
				rule.update(duration = str(updated_escalation_rule.duration))
				return {'code': '800.200.001', 'data': rule}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_rule(rule_id, system_id, **kwargs):
		"""
		Retrieves an escalation rule for a selected system.
		@param rule_id: The id of the rule to be updated
		@type rule_id: str
		@param system_id: System where the rule is defined
		@type system_id: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').first()

			if system is None:
				return {"code": "800.400.002"}
			escalation_rule = EscalationRuleService().filter(pk = rule_id, system = system).first()
			if escalation_rule:
				rule = EscalationRuleService().filter(pk = escalation_rule.id).values(
					'name', 'description', 'date_created', 'date_modified', 'system_id',
					'nth_event',  rule_id = F('id'), escalation = F('escalation_level__name'), eventtype = F(
						'event_type__name'), status = F('state__name'), system_name = F('system__name')
				).first()
				rule.update(duration = str(escalation_rule.duration))
				return {'code': '800.200.001', 'data': rule}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def get_rules(system_id, **kwargs):
		"""
		Retrieves all escalation rule for a selected system.
		@param system_id: System where the rule is defined
		@type system_id: str | None
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').first()
			if system is None:
				return {"code": "800.400.002"}
			escalation_rules = list(EscalationRuleService().filter(system = system).values(
				'name', 'description', 'date_created', 'duration', 'date_modified', 'system_id',
				'nth_event',  rule_id = F('id'), escalation = F('escalation_level__name'), eventtype = F(
					'event_type__name'), status = F('state__name'), system_name = F('system__name')))
			if escalation_rules:
				return {'code': '800.200.001', 'data': escalation_rules}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def delete_rule(rule_id, system_id, **kwargs):
		"""
		Deletes an escalation rule for a selected system.
		@param rule_id: The id of the rule to be deleted
		@type rule_id: str
		@param system_id: System where the escalation rule is defined in
		@type system_id: str
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().filter(pk = system_id, state__name = 'Active').first()
			if system is None:
				return {"code": "800.400.002"}
			escalation_rule = EscalationRuleService().filter(pk = rule_id, system = system).first()
			if escalation_rule:
				if escalation_rule.delete():
					return {'code': '800.200.001', 'Message': 'Rule deleted successfully'}
		except Exception as ex:
			lgr.exception("Escalation Rule Update exception %s" % ex)
		return {"code": "800.400.001"}
