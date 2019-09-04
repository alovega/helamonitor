"""
Class for creating new incidents and logging incident updates
"""
import logging

from core.backend.services import SystemService, IncidentService, IncidentEventService
from base.backend.services import IncidentTypeService, StateService
lgr = logging.getLogger(__name__)


class IncidentProcessor(object):
	"""
	Class for logging incidents
	"""
	def __init__(self):
		super(IncidentProcessor, self).__init__()

	def create_incident(self, name, description, incident_type, system, state, priority_level, **kwargs):
		incident_data = None
		escalation_data = {}
		try:
			incident_type = IncidentTypeService().get(name=incident_type)
			system = SystemService().get(name=system)
			state = StateService().get(name=state)
			incident_data = {
				"name": name, "description": description, "incident_type": incident_type, "system": system,
				"state": state, "priority_level": priority_level
			}  # kwargs format for data required to create an incident

		except Exception as ex:
			lgr.exception("Incident Processor exception %s" % ex)

		if incident_data is not None:
			try:
				incident = IncidentService().create(**incident_data)  # Create the Incident
				if kwargs:
					escalation_level = kwargs.get("escalation_level", None)
					events = kwargs.get("events", None)
					escalation_data.update(
						escalation_level = escalation_level, events = events
					)
					if events.exists():
						for event in events:
							IncidentEventService().create(incident=incident, event=event)
				if incident.exists():
					return self.send_notification(incident, **escalation_data)
			except Exception as ex:
				lgr.exception("Incident Processor exception %s" % ex)

	def log_incident(self):
		pass

	@staticmethod
	def send_notification(incident, **kwargs):
		pass
