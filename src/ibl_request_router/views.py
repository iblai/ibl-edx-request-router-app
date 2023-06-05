import logging
import requests
import six

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, parser_classes
from rest_framework.parsers import FileUploadParser
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

from ibl_request_router.api.manager import manager_proxy_request
from ibl_request_router.utils.access import check_request_permissions


log = logging.getLogger(__name__)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
@parser_classes((FileUploadParser))
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
            message = {}
            if response.ok:
                # Only log when the response is expected to be valid
                message['code'] = response.status_code
                message['content'] = response.content

        return Response(message, status=response.status_code)
        #return HttpResponse(response.text, status=response.status_code)
    except Exception:
        log.exception("Bad proxy request: %s", endpoint_path)
        raise Http404
