import logging

from django.contrib.auth.models import User
from django.db.models import F

from base.backend.services import StateService, EscalationLevelService, NotificationTypeService, EventTypeService, \
	EndpointTypeService, IncidentTypeService
from core.backend.services import SystemService

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
			data = {}
			state = list(StateService().filter().values('id', 'name'))
			notification_type = list(NotificationTypeService().filter().values('id', 'name'))
			escalation_level = list(EscalationLevelService().filter().values('id', 'name'))
			event_type = list(EventTypeService().filter().values('id', 'name'))
			endpoint_type = list(EndpointTypeService().filter().values('id', 'name'))
			incident_type = list(IncidentTypeService().filter().values('id', 'name'))
			user = list(User.objects.all().values('id', 'username'))
			system = list(SystemService().filter().values('id', 'name'))

			data.update(states = state, incident_types = incident_type, escalation_levels = escalation_level,
			            notification_types = notification_type, endpoint_types = endpoint_type,
			            event_types = event_type, users = user, systems = system)

			return {"code": "800.200.001", "data": data}

		except Exception as ex:
			lgr.exception("Look up interface Exception:  %s" % ex)
		return {"code": "800.400.001", "message": "Error while fetching data"}
