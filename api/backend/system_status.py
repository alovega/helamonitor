
import logging

from core.backend.services import SystemMonitorService, EventService

lgr = logging.getLogger(__name__)


class SystemStatusLogger(object):
	"""
	class for logging status  of  system micro-services
	"""

	def __init__(self, **kwargs):
		pass

	system_status = None

	def save_system_status(self, **kwargs):
		if self.system_status is None:
			try:
				self.system_status = SystemMonitorService().create(**kwargs) # creates a system_status object
				self.analyse_system_status(system_status = self.system_status)
				return self.system_status
			except Exception as e:
				lgr.exception("Status Log exception: %s" % e)

	@staticmethod
	def analyse_system_status(system_status, desired_time=20, **kwargs):
		if system_status.status_code != 200:
			try:
				event = EventService().create(**kwargs)
				return event
			except Exception as e:
				lgr.exception("Event Log exception: %s" %e)
		elif system_status.response_time > desired_time:
			try:
				event = EventService().create(**kwargs)
				return event
			except Exception as e:
				lgr.exception("Event Log exception: %s" %e)

	def generate_status_report(self):
		pass
