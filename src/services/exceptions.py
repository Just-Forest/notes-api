class ServiceError(Exception):
    """Base for all service-layer failures."""


class NotFound(ServiceError):
    pass


class AlreadyExists(ServiceError):
    pass


class InvalidCredentials(ServiceError):
    pass
