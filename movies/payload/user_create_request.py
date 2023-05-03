from dataclasses import dataclass


@dataclass
class UserCreateRequest:
    username: str
    password: str

    def __init__(self, **kwargs) -> None:
        self.username = kwargs['username']
        self.password = kwargs['password']

