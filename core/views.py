from django.db.models import Q
from rest_framework import viewsets

from core.models import Endpoint
from core.tables.pagination import DataTablePagination
from tables.endpoints.serializers import EndpointSerializer


class EndpointViewSet(viewsets.ModelViewSet):
	pagination_class = DataTablePagination
	search_parameters = ()
	default_order_by = ''
	unfiltered_query_set = None

	def get_queryset(self):
		self.unfiltered_query_set = query_set = super(EndpointViewSet, self).get_queryset()

		order_by_index = int(self.request.query_params.get('order[0][column]', 0))
		orderable = bool(self.request.query_params.get('columns[{}][orderable]'.format(order_by_index), 'false'))

		if order_by_index == 0 or not orderable:
			order_by_index = 1

		order_by = self.request.query_params.get('columns[{}][data]'.format(order_by_index),
		                                         self.default_order_by).replace('.', '__')
		order_by_dir = self.request.query_params.get('order[0][dir]', 'asc')
		if order_by_dir == 'desc':
			order_by = '-{}'.format(order_by)

		search_queries = self.request.query_params.get('search[value]', '').strip().split(' ')
		q = Q()

		if len(search_queries) > 0 and search_queries[0] != u'':
			for params in self.search_parameters:

				for query in search_queries:
					temp = {
						'{}__contains'.format(params): query,
					}
					q |= Q(**temp)

		query_set = query_set.filter(q)

		if order_by == '':
			return query_set

		return query_set.order_by(order_by)


def get(self, request, *args, **kwargs):
        result = super(EndpointViewSet, self).get(request, *args, **kwargs)
        result.data['draw'] = int(request.query_params.get('draw', 0))

        result.data['recordsFiltered'] = result.data['count']
        result.data['recordsTotal'] = self.unfiltered_query_set.count()
        del result.data['count']

        result.data['data']= result.data['results']
        del result.data['results']
        return result

