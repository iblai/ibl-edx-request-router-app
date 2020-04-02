import json
import logging
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404

try:
    from ibl_api_auth.utils.oauth import get_app_access_token
except ImportError:
    pass


log = logging.getLogger(__name__)


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

MANAGER_AUTH_ENABLED = getattr(settings, 'MANAGER_AUTH_ENABLED', True)
MANAGER_AUTH_APP_ID = getattr(settings, 'MANAGER_AUTH_APP_ID', 'manager')


def manager_api_request(method, endpoint_path, params=None, data=None,
                        max_tries=MANAGER_MAX_TRIES,
                        verify=MANAGER_VERIFY_SSL,
                        timeout=MANAGER_REQUEST_TIMEOUT):
    """
    Submit API request to manager with proper authentication

    Return:
    Manager request response
    """
    if not MANAGER_BASE_URL:
        raise Http404
    
    if not max_tries:
        return None
    
    url = "{}/{}".format(MANAGER_BASE_API_URL, endpoint_path.lstrip('/'))
    
    # Auth headers
    headers = {}
    if MANAGER_AUTH_ENABLED:
        headers['Authorization'] = 'Bearer {}'.format(get_app_access_token(MANAGER_AUTH_APP_ID))
    
    # Request config
    request_kwargs = {
        "params": params,
        "json": data,
        "timeout": timeout,
        "verify": verify,
        "headers": headers
    }
    
    # Try request
    response = None
    for req in range(max_tries):
        try:
            # TODO: Make this DEBUG
            log.info("Manager request: %s %s %s", method, url, params)
            response = requests.request(
                method, url, **request_kwargs
            )
        except Exception as exc:
            log.error("Manager response exception: %s %s %s", method, url, params, exc_info=True)
            continue
    
    return response
    
    
def convert_manager_proxy_params(params):
    """
    Transforms proxy parameters
    """
    new_params = dict(params)
    
    # Convert username to user_id
    if 'username' in params:
        try:
            username = params.get('username')
            user = User.objects.get(username=username)
            new_params['user_id'] = user.id
        except User.DoesNotExist as dne_exc:
            log.error("Error converting username to user_id (User does not exist): %s", username)
        except Exception as exc:
            log.error("Error converting username to user_id: %s", username, exc_info=True)
    
    return new_params


def manager_proxy_request(request, endpoint_path=''):
    """
    Passes request to manager.
    Permission checks performed elsewhere.
    """
    if not MANAGER_BASE_URL:
        raise Http404
    
    url = "{}/{}".format(MANAGER_BASE_API_URL, endpoint_path.lstrip('/'))
    
    # Auth headers
    headers = {}
    if MANAGER_AUTH_ENABLED:
        headers['Authorization'] = 'Bearer {}'.format(get_app_access_token(MANAGER_AUTH_APP_ID))
    
    # Assume nothing in original headers and cookies need to be passed
    request_kwargs = {
        "params": convert_manager_proxy_params(request.query_params),
        "json": convert_manager_proxy_params(request.data),
        "timeout": MANAGER_PROXY_TIMEOUT,
        "headers": headers
    }
    
    log.info("Manager proxy request: %s %s", request.method, url)
    return requests.request(
        request.method, url, **request_kwargs
    )
