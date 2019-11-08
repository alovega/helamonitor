import logging

from django.db.models import F, Q
from core.models import User

from base.backend.services import StateService, EscalationLevelService, NotificationTypeService, EventTypeService, \
	EndpointTypeService, IncidentTypeService
from core.backend.services import SystemService, RecipientService

lgr = logging.getLogger(__name__)


class LookUpInterface(object):
	"""
	class for defining look up data
	"""

	@staticmethod
	def get_look_up_data():
		"""
		@return: a dictionary containing a success code and a list of dictionaries containing  system
							recipient data
		@rtype:dict
		"""
		try:
			state = list(StateService().filter().values('id', 'name'))
			notification_type = list(NotificationTypeService().filter().values('id', 'name'))
			escalation_level = list(EscalationLevelService().filter().values('id', 'name'))
			event_type = list(EventTypeService().filter().values('id', 'name'))
			endpoint_type = list(EndpointTypeService().filter().values('id', 'name'))
			incident_type = list(IncidentTypeService().filter().values('id', 'name'))
			user = list(User.objects.all().values('id', 'username'))
			system = list(SystemService().filter().values('id', 'name'))
			recipient = list(RecipientService().filter().values('id', userName=F('user__username')))
			endpoint_states = list(StateService().filter(
				Q(name = 'Operational') | Q(name = 'Minor Outage') | Q(name = 'Major Outage') |
				Q(name = 'Under Maintenance') | Q(name = 'Degraded Performance')).values('id', 'name'))
			lookups = {
				'states': state, 'incident_types': incident_type, 'escalation_levels': escalation_level,
				'notification_types': notification_type, 'endpoint_types': endpoint_type, 'event_types': event_type,
				'users': user, 'systems': system, 'recipients': recipient, 'endpoint_states': endpoint_states}

			return {"code": "800.200.001", "data": lookups}

		except Exception as ex:
			lgr.exception("Look up interface Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while fetching data %s" % str(ex)}
