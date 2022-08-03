import logging

from opaque_keys.edx.keys import CourseKey

from ibl_request_router.config import MANAGER_API_AUTH_ALLOWLIST, MANAGER_API_UNAUTH_ALLOWLIST


log = logging.getLogger(__name__)


def check_request_permissions(request, endpoint_path):
    """
    Returns whether user is authorized to access endpoint
    """
    # Remove leading/trailing slashes
    path = endpoint_path.strip("/")
    
    if path in MANAGER_API_UNAUTH_ALLOWLIST:
        return True
    elif path in MANAGER_API_AUTH_ALLOWLIST:
        return request.user.is_authenticated
    else:
        return (
            request.user.is_authenticated and
            (request.user.is_staff or request.user.is_superuser)
        )
