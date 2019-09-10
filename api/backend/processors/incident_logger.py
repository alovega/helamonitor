# coding=utf-8
"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import SystemService, IncidentService
from base.backend.services import IncidentTypeService, StateService
lgr = logging.getLogger(__name__)


class IncidentLogger(object):
	"""
	Class for logging incidents
	"""
	@staticmethod
	def create_incident(incident_type, system, **kwargs):
		try:
			system = SystemService().get(name=system, state__name = "Active")
			incident_type = IncidentTypeService().get(name=incident_type, state__name="Active")
			if system is None or incident_type is None:
				return {"code": "800.400.002"}
			incident = IncidentService().create(
				name=kwargs.get("name", None), description=kwargs.get("description", None),
				state=StateService().get(name="Active"), incident_type=incident_type, system=system,
				priority_level = kwargs.get("priority_level", 1)
			)  # Creates an incident from an escalated event or direct creation
			if incident is not None:
				return IncidentLogger.send_notification(incident, kwargs.get("escalation_level", None))
			return {"code": "200.400.002"}
		except Exception as ex:
			lgr.exception("Incident Logger exception %s" % ex)
		return {"code": "200.400.002"}

	def log_incident(self):
		pass

	@staticmethod
	def send_notification(incident, escalation_level):
		pass
