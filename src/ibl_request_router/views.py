import logging
import requests
import six

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes
try:
    from openedx.core.lib.api.authentication import BearerAuthentication as OAuth2Authentication
except ImportError:
    from rest_framework_oauth.authentication import OAuth2Authentication
from rest_framework.response import Response

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication

from ibl_request_router.api.manager import (
    manager_api_request, manager_proxy_request
)
from ibl_request_router.config import MANAGER_TOKEN_ENDPOINT_PATH
from ibl_request_router.utils.access import check_request_permissions


log = logging.getLogger(__name__)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
@authentication_classes((SessionAuthentication, OAuth2Authentication, JwtAuthentication))
def manager_proxy_view(request, endpoint_path=None):
    """
    Manager proxy view
    """
    if endpoint_path is None:
        log.info("No endpoint path")
        raise Http404
    
    # Check staff
    if not check_request_permissions(request, endpoint_path):
        log.warning("Not authorized for %s: %s", endpoint_path, six.text_type(request.user))
        raise Http404
    
    try:
        response = manager_proxy_request(request, endpoint_path)
        
        try:
            log.info("Response %s: %s %s", endpoint_path, response.status_code, response.text)
            return Response(
                response.json(), status=response.status_code
            )
        except ValueError:
            if response.ok:
                # Only log when the response is expected to be valid
                log.error(
                    "Non-JSON response %s: %s %s",
                    endpoint_path, response.status_code, response.text, exc_info=True
                )
        
        return Response({}, status=response.status_code)
        #return HttpResponse(response.text, status=response.status_code)
    except Exception:
        log.exception("Bad proxy request: %s", endpoint_path)
        raise Http404


# Token view

@api_view(['POST'])
@csrf_exempt
@authentication_classes((SessionAuthentication, OAuth2Authentication, JwtAuthentication))
def manager_token_proxy_view(request):
    """
    Manager token proxy view
    
    User must be authenticated.
    """
    # Check request user
    if not (request.user and request.user.is_authenticated and request.user.is_active):
        log.warning("Invalid user cannot request token.")
        raise Http404
    
    try:
        response = manager_api_request(
            'POST', MANAGER_TOKEN_ENDPOINT_PATH,
            data={
                "user_id": request.user.id
            }
        )
        
        try:
            log.info("Token proxy response %s", response.status_code)
            return Response(
                response.json(), status=response.status_code
            )
        except ValueError:
            if response.ok:
                # Only log when the response is expected to be valid
                log.exception(
                    "Non-JSON token proxy response: %s %s",
                    response.status_code, response.text
                )
        
        return Response({}, status=response.status_code)
    except Exception:
        log.exception("Token proxy request error")
        raise Http404

