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
			if kwargs:
				escalation_level = kwargs.get("escalation_level", None)
				events = kwargs.get("events", None)
				event_type = kwargs.get("event_type", None)
				escalation_data.update(
					escalation_level = escalation_level, events = events
				)
				if events.exists() and event_type is not None:
					# Check previous incidents to avoid duplicating any incident caused by re-occurring events of the
					# same type
					try:
						incident_events = IncidentEventService().filter(event__type = event_type)
						open_incident = IncidentService().filter(incident__in = incident_events).exclude(
							status = "Resolved").order_by("-date_created").first()
						# Query for any unresolved any incident that was created as a result of events of that type
						# and increment the priority level
						if open_incident.exists():
							open_incident.update(priority_level = priority_level + 1)
							return self.send_notification(open_incident, **escalation_data)  # Alert users on the
							# this priority_level update
						else:
							incident = IncidentService().create(**incident_data)  # Create a new Incident
							for event in events:
								IncidentEventService().create(incident=incident, event=event)
								# Associate new events with the incident in an incident-event instance
							return incident
					except Exception as ex:
						lgr.exception("Incident Processor exception %s" % ex)
			try:
				incident = IncidentService().create(**incident_data)  # Create a new Incident
				return incident
			except Exception as ex:
				lgr.exception("Incident Processor exception %s" % ex)

	def log_incident(self):
		pass

	@staticmethod
	def send_notification(incident, **kwargs):
		pass
