class FastNeoError(Exception):
    pass


class ValidationError(FastNeoError):
    pass


class UnknownPropertyError(ValidationError):
    pass


class MissingPropertyError(ValidationError):
    pass
