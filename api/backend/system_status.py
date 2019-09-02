
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
		"""
		This method  creates  system status for monitoring purposes
		:param kwargs:
		:return: system_status
		"""
		if self.system_status is None:
			try:
				self.system_status = SystemMonitorService().create(**kwargs)  # creates a system_status object
				self.analyse_system_status(system_status = self.system_status)  # analyse whether to create an event
				# based on the logged status
				return self.system_status
			except Exception as e:
				lgr.exception("Status Log exception: %s" % e)

	@staticmethod
	def analyse_system_status(system_status, desired_time=20, **kwargs):
		"""
		This method analyses the created system_status is it okay, down or in a failed state
		:param system_status:
		:param desired_time: a set time that a response_time must meet for it's request to be considered okay
		:param kwargs:
		:return: event
		"""
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
