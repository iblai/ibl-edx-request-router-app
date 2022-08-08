from unittest import mock

import pytest
from django.http import Http404

from ibl_request_router.api.manager import manager_api_request

MANAGER_BASE_URL_PKG_PATH = "ibl_request_router.api.manager.MANAGER_BASE_URL"


@pytest.mark.django_db
class TestAPIManager:
    endpoint = "knock_knock"

    @mock.patch(MANAGER_BASE_URL_PKG_PATH, None)
    def test_on_empty_base_url_returns_404(self):
        with pytest.raises(Http404):
            manager_api_request("get", self.endpoint)
