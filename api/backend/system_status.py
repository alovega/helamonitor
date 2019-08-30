
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
				self.system_status = SystemMonitorService().create(**kwargs)
				return self.system_status
			except Exception as e:
				lgr.exception("Monitor Log exception: %s" % e)
