from django.conf import settings


MANAGER_BASE_URL = getattr(settings, "MANAGER_BASE_URL", "")
MANAGER_BASE_API_URL = MANAGER_BASE_URL + "/api"

# Request retries
MANAGER_MAX_TRIES = getattr(settings, 'MANAGER_MAX_TRIES', 1)
# Request certificate verification
MANAGER_VERIFY_SSL = getattr(settings, 'MANAGER_VERIFY_SSL', True)
# Request default timeout
MANAGER_REQUEST_TIMEOUT = getattr(settings, 'MANAGER_REQUEST_TIMEOUT', 20)
# Request proxy timeout
MANAGER_PROXY_TIMEOUT = getattr(settings, "MANAGER_PROXY_TIMEOUT", MANAGER_REQUEST_TIMEOUT)

# Allow proxy requests to the manager through edX
MANAGER_PROXY_ENABLED = getattr(settings, "MANAGER_PROXY_ENABLED", True)

MANAGER_AUTH_ENABLED = getattr(settings, 'MANAGER_AUTH_ENABLED', True)
MANAGER_AUTH_APP_ID = getattr(settings, 'MANAGER_AUTH_APP_ID', 'manager')


DEFAULT_ORG = getattr(settings, 'MANAGER_DEFAULT_ORG', None)
MULTITENANCY_ENABLED = getattr(settings, 'MANAGER_MULTITENANCY_ENABLED', False)

