import logging
from django.core.paginator import Paginator
from django.db.models import Q

lgr = logging.getLogger(__name__)


def paginate_data(data, page_size, page_number):
	"""

	@param page_number: the page to be obtained
	@param page_size: the number of items each page will have
	@param data: data given to be paginated
	@type: dict
	@return: returns paginated data
	"""
	try:
		for index, value in enumerate(data):
			value.update(item_index = index + 1)
		paginator = Paginator(data, page_size)
		table_data = {'row': paginator.page(page_number).object_list}
		if table_data.get('row'):
			item_range = [table_data.get('row')[0].get('item_index'), table_data.get('row')[-1].get('item_index')]
		else:
			item_range = [0, 0]
		item_description = 'Showing %s to %s of %s items' % (
			str(item_range[0]), str(item_range[1]), str(paginator.count))
		table_data.update(
			size = paginator.num_pages, totalElements = paginator.count, totalPages = paginator.num_pages,
			range = item_description)

		return table_data
	except Exception as e:
		lgr.exception('Pagination Exception: %s', e)
	return {"code": "800.400.001"}


def build_search_query(search_value, columns, extra_columns = None):
	"""
	Builds a search query using Q objects, ORed together.
	@param search_value: The value to search for.
	@param columns: Columns to carry out searching in.
	@type columns: list
	@param extra_columns: A list of Extra columns that we don't want to include on the main columns.
	@type extra_columns: list | None
	@return: Q objects
	@rtype: Q
	"""
	try:
		if isinstance(extra_columns, list):
			columns += extra_columns
		if len(str(search_value)) > 0:
			if len(columns) > 0:
				field, fields = pop_first_none_empty_from_list(columns)
				query = Q(('%s__icontains' % str(field), str(search_value)))
				for fl in fields:
					if fl != '' and str(search_value) != '':
						query |= Q(('%s__icontains' % fl, str(search_value)))
				return query
	except Exception as e:
		lgr.exception('build_search_query Exception: %s', e)
	return ~Q(date_created = None)


def pop_first_none_empty_from_list(list_items):
	"""
	Gets the fist item in the list that's not empty then removes that item from the list.
	Awesome.
	@param list_items: The items to check.
	@type list_items: list
	@return: The item that's not empty and the list with the item removed.
	@rtype: tuple
	"""
	try:
		length = len(list_items)
		local_list = list_items
		for _ in range(0, length):
			field = local_list.pop(0)  # Always pop the first item as other items might have already been removed.
			if len(str(field)) > 0:
				return field, local_list
	except Exception as e:
		lgr.exception('pop_first_none_empty_from_list Exception: %s', e)
	return '', list_items

def extract_order(order_dir, order_column, data):
	"""
	General function to perform ordering of columns
	@param data: Queryset to be ordered
	@param order_dir: string representing the direction of ordering descending or ascending
	@type:str
	@param order_column: the column to perform ordering
	@type: str
	@return: a dictionary containing ordered data
	"""
	try:
		if order_dir == 'desc':
			data = data.order_by('-' + str(order_column))
		else:
			data = data.order_by(str(order_column))
		return data
	except Exception as e:
		lgr.exception('Extract order exception: %s' % e)
