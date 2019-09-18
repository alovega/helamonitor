"""
Services for Api module
"""
from base.backend.services import ServiceBase
from api.models import ApiUser, App


class AppService(ServiceBase):
	"""
	Class for App CRUD
	"""
	manager = App.objects


class ApiUserService(ServiceBase):
	"""
	Class for ApiUser CRUD
	"""
	manager = ApiUser.objects
