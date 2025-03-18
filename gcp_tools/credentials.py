from google.oauth2.service_account import Credentials


def get_credentials(service_account: str | dict, scopes=None):
    if isinstance(service_account, dict):
        service_account_credentials = Credentials.from_service_account_info(service_account, scopes=scopes)
    elif isinstance(service_account, str):
        service_account_credentials = Credentials.from_service_account_file(service_account, scopes=scopes)
    else:
        service_account_credentials = None
    return service_account_credentials
