class ServiceError(Exception):
    pass


class NotFoundError(ServiceError):
    pass


class AlreadyExistsError(ServiceError):
    pass


class AuthenticationError(ServiceError):
    pass


class CredentialsError(ServiceError):
    pass



