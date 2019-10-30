from rest_framework import serializers
from core.models import Endpoint


class EndpointSerializer(serializers.ModelSerializer):

	class Meta:
		model = Endpoint
		fields = (
			'id', 'name', 'description', 'endpoint', 'system__id', 'optimal_response_time', 'endpoint_type__name',
			'state__name', 'date_created'
		)
