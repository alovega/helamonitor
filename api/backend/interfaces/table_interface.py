import datetime
import logging
from django.core.paginator import Paginator

from django.db.models import F

from core.backend.services import SystemService, EndpointService, SystemMonitorService
from base.backend.services import StateService, EndpointTypeService

lgr = logging.getLogger(__name__)


class TableData(object):
	"""
	class for getting data for table elements
	"""

	@staticmethod
	def get_endpoints(parameters):
		"""
		@param parameters: a dictionary containing parameters used for fetching endpoint data
		@type: dict
		@return:a dictionary containing response code and data to be used for data table
		@rtype: dict
		"""
		try:
			if not parameters:
				return {
					"code": "800.400.002 %s" % parameters, "message": "invalid required parameters"
				}
			if parameters.get('orderColumn'):
				if parameters.get('orderDir') == 'desc':
					data = list(SystemMonitorService().filter().values(
						description = F('endpoint__description'), dateCreated = F('date_created'),
						name = F('endpoint__name'),
						Url = F('endpoint__url'), responseTime = F('response_time'), status = F('state__name'),
						Id = F('endpoint__id'), type = F('endpoint__endpoint_type__name')).order_by(
						'-' + str(parameters.get('orderColumn'))))
				else:
					data = list(SystemMonitorService().filter().values(
						description = F('endpoint__description'), dateCreated = F('date_created'),
						name = F('endpoint__name'),
						Url = F('endpoint__url'), responseTime = F('response_time'), status = F('state__name'),
						Id = F('endpoint__id'), type = F('endpoint__endpoint_type__name')).order_by(
						str(parameters.get('orderColumn'))))
			else:
				data = list(SystemMonitorService().filter().values(
					description = F('endpoint__description'), dateCreated = F('date_created'),
					name = F('endpoint__name'),
					Url = F('endpoint__url'), responseTime = F('response_time'), status = F('state__name'),
					Id = F('endpoint__id'), type = F('endpoint__endpoint_type__name')).order_by(
					'-date_created'))
			for value in data:
				time = datetime.timedelta.total_seconds(value.get('responseTime'))
				del value["responseTime"]
				value.update(responseTime = time)
			paginator = Paginator(data, parameters.get('pageSize'))
			table_data = {"data": paginator.page(parameters.get('pageNumber')).object_list}
			table_data.update(size = paginator.num_pages, totalElements = paginator.count,
			                  totalPages = paginator.num_pages)
			return {'code': '800.200.001', 'data': table_data}
		except Exception as ex:
			lgr.exception("Endpoint Administration exception: %s" % ex)
		return {"code": "800.400.001 %s" % ex, "message": "Error while getting table data"}
