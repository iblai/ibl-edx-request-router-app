"""
Views for extended API (LMS)
"""
import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from openedx.core.lib.api.view_utils import view_auth_classes

from ibl_request_router.utils.heartbeat import celery_ping


log = logging.getLogger(__name__)


@view_auth_classes(is_authenticated=False)
class CeleryHeartbeatView(APIView):
    """
    **Use Case**

        Celery heartbeat endpoint.

    **Example Request**

        GET /api/ibl/heartbeat/celery/

    **Response Values**

        * 200 on success.
        * 500 on failure.

    """

    def get(self, request, format=None):
        try:
            status = celery_ping()
            if status:
                return Response(status=200)
            
            return Response(status=500)
        except Exception:
            log.exception("Could not get celery heartbeat status")
            return Response(status=500)
