from dataclasses import dataclass


@dataclass
class UserMessage:
    '''
        Messages used in endpoint responses for users 
    '''
    created: str = 'User has been created'
    exist: str = 'User exist'
    found: str = 'User Found'
    not_found: str = 'User not found'
    validated: str = 'User has been validated'
    updated: str = 'User updated'
    deleted: str = 'User deleted'
    disabled: str = 'User disabled'
    enabled: str = 'User enabled'


@dataclass
class CredentialMessage:
    '''
        Messages used in endpoint responses for credential 
    '''
    invalid: str = 'Invalid User or Password'
    logged: str = 'User Logged'
    pass_updated: str = 'Password updated'
    code_updated: str = 'Security code updated'
    code_found: str = 'Security Code Found'


@dataclass
class QuestionMessage:
    '''
        Messages used in endpoint responses for question
    '''
    found: str = 'Questions found'
    not_found: str = 'Questions not found'
    updated: str = 'Questions updated'
