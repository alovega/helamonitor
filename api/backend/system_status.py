
import logging

from core.backend.services import SystemMonitorService

lgr = logging.getLogger(__name__)


class SystemStatusLogger(object):
	"""
	class for logging status  of  system micro-services
	"""

	def __init__(self, **kwargs):
		pass

	system_status = None

	def create_system_status(self, **kwargs):
		if self.system_status is None:
			try:
				self.system_status = SystemMonitorService().create(**kwargs) # creates a system_status object
				return self.system_status
			except Exception as e:
				lgr.exception("Monitor Log exception: %s" % e)

	def analyse_system_status(self, system_status):
		if system_status.status != 200:
			system = system_status.system
			endpoint = system_status.endpoint

	def generate_status_report(self):
		pass
