# coding=utf-8
"""
Class for Escalation Rules Administration
"""
import logging
from datetime import timedelta

from django.db.models import F

from core.backend.services import SystemService, EscalationRuleService
from base.backend.services import StateService, EscalationLevelService, EventTypeService, IncidentTypeService

lgr = logging.getLogger(__name__)


class EscalationRuleAdministrator(object):
	"""
	Class for Escalation Rules Administration
	"""

	@staticmethod
	def create_rule(name, description, system, event_type, nth_event, escalation_level, duration, **kwargs):
		"""
		Creates an escalation rule for a selected system.
		@param name: Name of the escalation rule to be created
		@type name: str
		@param system: The system which the escalation rule will be applied in
		@type system: str
		@param description: Details on the Escalation Rule
		@type description: str
		@param event_type: Type of the event(s) to be affected by the rule
		@type event_type: str
		@param nth_event: Number of event of a certain type that need to be logged to raise an escalation
		@type nth_event: str
		@param duration: Time period within which certain events must occur to trigger an escalation.
		@type duration: int
		@param escalation_level: Level at which an escalation is configured with a set of recipients
		@type escalation_level: str
		@param kwargs: Extra key-value arguments to pass for incident logging
		@return: Response code dictionary to indicate if the incident was created or not
		@rtype: dict
		"""
		try:
			system = SystemService().get(pk = system, state__name = "Active")
			escalation_level = EscalationLevelService().get(pk = escalation_level, state__name = "Active")
			event_type = EventTypeService().get(pk = event_type, state__name = 'Active')
			if system is None or escalation_level is None or event_type is None:
				return {"code": "800.400.002"}

			escalation_rule = EscalationRuleService().create(
				name = name, description = description, system = system, nth_event = int(nth_event),
				duration = timedelta(seconds = duration), state = StateService().get(name = 'Active'),
				escalation_level = escalation_level, event_type = event_type
			)
			if escalation_rule is not None:
				rule = EscalationRuleService().filter(pk = escalation_rule.id, system = system).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name')).first()
				rule.update(duration = timedelta.total_seconds(rule.get('duration')))
				return {'code': '800.200.001', 'data': rule}
		except Exception as ex:
			lgr.exception("Escalation Rule Creation exception %s" % ex)
		return {"code": "800.400.001"}

	@staticmethod
	def update_rule(
			rule_id, name = None, description = None, nth_event = None, escalation_level = None,
			duration = None, event_type = None, **kwargs):
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
		@type duration: int | None
		@param event_type: The event type to be applied for an escalation with the rule.
		@type event_type: str | None
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
			duration = timedelta(seconds = duration) if duration is not None else escalation_rule.duration
			escalation_level = EscalationLevelService().filter(
				pk = escalation_level, state__name = 'Active').first() if escalation_level is not None else \
				escalation_rule.escalation_level
			event_type = EventTypeService().filter(
				pk = event_type, state__name = 'Active').first() if event_type is not None else \
				escalation_rule.event_type
			state = escalation_rule.state

			updated_escalation_rule = EscalationRuleService().update(
				pk = escalation_rule.id, name = name, description = description, nth_event = int(nth_event),
				duration = duration, state = state, escalation_level = escalation_level, event_type = event_type
			)
			if updated_escalation_rule is not None:
				rule = EscalationRuleService().filter(pk = escalation_rule.id).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name')).first()
				rule.update(duration = timedelta.total_seconds(rule.get('duration')))
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
			escalation_rule = EscalationRuleService().filter(pk = rule_id, system = system).first()
			if system is None or escalation_rule is None:
				return {"code": "800.400.002"}
			if escalation_rule:
				rule = EscalationRuleService().filter(pk = escalation_rule.id).values(
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name')).first()
				rule.update(duration = timedelta.total_seconds(rule.get('duration')))
				return {'code': '800.200.001', 'data': rule}
		except Exception as ex:
			lgr.exception("Get Escalation rule exception %s" % ex)
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
					'id', 'name', 'description', 'duration', 'date_created', 'date_modified', 'nth_event',
					system_id = F('system'), escalation_level_name = F('escalation_level__name'), state_name = F(
						'state__name'), event_type_name = F('event_type__name')).order_by('-date_created'))
			for rule in escalation_rules:
				rule.update(duration = timedelta.total_seconds(rule.get('duration')))
			return {'code': '800.200.001', 'data': escalation_rules}
		except Exception as ex:
			lgr.exception("Get Escalation Rules exception %s" % ex)
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
			escalation_rule = EscalationRuleService().filter(pk = rule_id, system = system).first()
			if system is None or escalation_rule is None:
				return {"code": "800.400.002"}
			if escalation_rule.delete():
				return {'code': '800.200.001', 'Message': 'Rule deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete Escalation Rule exception %s" % ex)
		return {"code": "800.400.001"}
