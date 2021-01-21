from dataclasses import dataclass


@dataclass(frozen=True)
class RecaptchaException(Exception):
    message: str

    def __post_init__(self):
        super().__init__(self.message)


class RecaptchaConnectionServerError(RecaptchaException):
    pass
