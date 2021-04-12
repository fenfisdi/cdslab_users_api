from dataclasses import dataclass


@dataclass
class UserMessage:
    created: str = 'User has been created'
    exist: str = 'User exist'
    found: str = 'User Found'
    not_found: str = 'User not found'
    validated: str = 'User has been validated'
    updated: str = 'User updated'
    deleted: str = 'User deleted'
