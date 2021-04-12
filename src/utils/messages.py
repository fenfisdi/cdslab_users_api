from dataclasses import dataclass


@dataclass
class UserMessage:
    created: str = 'User has been created'
    exist: str = 'User exist'
    found: str = 'User Found'
    not_found: str = 'User not found'
