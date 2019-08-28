from base.models import State

from servicebase import ServiceBase


class StateService(ServiceBase):
    """
    Service for State CRUD
    """
    manager = State.objects