import logging

import six
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes

try:
    from openedx.core.lib.api.authentication import (
        BearerAuthentication as OAuth2Authentication,
    )
except ImportError:
    from rest_framework_oauth.authentication import OAuth2Authentication
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from rest_framework.response import Response

from ibl_request_router.api.manager import manager_api_request
from ibl_request_router.config import (
    MANAGER_CONSOLIDATED_TOKEN_ENDPOINT_PATH,
    MANAGER_TOKEN_ENDPOINT_PATH,
)


log = logging.getLogger(__name__)


# Token views

@api_view(["POST"])
@csrf_exempt
@authentication_classes(
    (SessionAuthentication, OAuth2Authentication, JwtAuthentication)
)
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
            "POST", MANAGER_TOKEN_ENDPOINT_PATH, data={"user_id": request.user.id}
        )

        try:
            log.info("Token proxy response %s", response.status_code)
            return Response(response.json(), status=response.status_code)
        except ValueError:
            if response.ok:
                # Only log when the response is expected to be valid
                log.exception(
                    "Non-JSON token proxy response: %s %s",
                    response.status_code,
                    response.text,
                )

        return Response({}, status=response.status_code)
    except Exception:
        log.exception("Token proxy request error")
        raise Http404


@api_view(["POST"])
@csrf_exempt
@authentication_classes(
    (SessionAuthentication, OAuth2Authentication, JwtAuthentication)
)
def manager_consolidated_token_proxy_view(request):
    """
    Same as manager_token_proxy_view above but requires platform and posts to the
    new consolidated endpoint

    User must be authenticated.
    """
    # Check request user
    if not (request.user and request.user.is_authenticated and request.user.is_active):
        log.warning("Invalid user cannot request token.")
        raise Http404

    platform_key = request.data.get("platform_key")
    if not platform_key:
        return Response({"error": "Missing platform_key"}, status=400)

    try:
        response = manager_api_request(
            "POST",
            MANAGER_CONSOLIDATED_TOKEN_ENDPOINT_PATH,
            data={"user_id": request.user.id, "platform_key": platform_key},
        )

        try:
            log.info("Consolidated Token proxy response %s", response.status_code)
            return Response(response.json(), status=response.status_code)
        except ValueError:
            if response.ok:
                # Only log when the response is expected to be valid
                log.exception(
                    "Non-JSON consolidated token proxy response: %s %s",
                    response.status_code,
                    response.text,
                )

        return Response({}, status=response.status_code)
    except Exception as e:
        log.exception("Consolidated Token proxy request error: %s", e)
        raise Http404
