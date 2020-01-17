import logging
import requests

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from .utils.manager import manager_proxy_request


log = logging.getLogger(__name__)


def manager_proxy_view(request, endpoint_path=None):
    """
    Manager proxy view
    """
    if endpoint_path is None:
        raise Http404
    
    # Check staff 
    if not (request.user.is_authenticated and
        (request.user.is_staff or request.user.is_superuser)):
        raise Http404
    
    try:
        response = manager_proxy_request(request, endpoint_path)
        
        try:
            log.info("Response: %s", response.text)
            # "In order to allow non-dict objects to be serialized set the safe parameter to False"
            return JsonResponse(
                response.json(), status=response.status_code, safe=False
            )
        except ValueError:
            log.error("Non-JSON response", exc_info=True)
            pass
        
        log.info("Response code: %s", response.status_code)
        return JsonResponse({}, status=response.status_code)
        #return HttpResponse(response.text, status=response.status_code)
    except Exception as exc:
        log.error("Bad proxy request", exc_info=True)
        raise Http404
