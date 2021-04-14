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


@dataclass
class CredentialMessage:
    invalid: str = 'Invalid User or Password'
    logged: str = 'User Logged'


@dataclass
class QuestionMessage:
    found: str = 'Questions found'
    not_found: str = 'Questions not found'
    updated: str = 'Questions updated'
