import json
import logging
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404


log = logging.getLogger(__name__)


MANAGER_BASE_URL = getattr(settings, "MANAGER_BASE_URL", "")
MANAGER_BASE_API_URL = MANAGER_BASE_URL + "/api"
MANAGER_PROXY_TIMEOUT = getattr(settings, "MANAGER_PROXY_TIMEOUT", 10)


def manager_request(method, endpoint_path, params=None, data=None):
    if not MANAGER_BASE_URL:
        raise Http404
    
    url = "{}/{}".format(MANAGER_BASE_API_URL, endpoint_path.lstrip('/'))
    
    kwargs = {
        "params": params,
        "json": data,
        "timeout": MANAGER_PROXY_TIMEOUT
    }
    
    log.info("Manager Request: %s %s", method, url)
    return requests.request(
        method, url, **kwargs
    )
    
    
def convert_manager_proxy_params(params):
    new_params = dict(params)
    
    # Convert username to user_id
    if 'username' in params:
        try:
            user = User.objects.get(username=params.get('username'))
            new_params['user_id'] = user.id
        except Exception as exc:
            log.error("Error converting username to user_id", exc_info=True)
    
    return new_params


def manager_proxy_request(request, endpoint_path=''):
    if not MANAGER_BASE_URL:
        raise Http404
    
    url = "{}/{}".format(MANAGER_BASE_API_URL, endpoint_path.lstrip('/'))
    
    # Assume nothing in headers and cookies need to be passed
    kwargs = {
        "params": convert_manager_proxy_params(request.query_params),
        "json": convert_manager_proxy_params(request.data),
        "timeout": MANAGER_PROXY_TIMEOUT
    }
    
    log.info("Manager Proxy Request: %s %s", request.method, url)
    return requests.request(
        request.method, url, **kwargs
    )
