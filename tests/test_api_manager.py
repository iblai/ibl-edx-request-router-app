import json
from unittest import mock
from uuid import uuid4

import pytest
from django.http import Http404

from ibl_request_router.api.manager import manager_api_request

MANAGER_BASE_URL_PKG_PATH = "ibl_request_router.api.manager.MANAGER_BASE_URL"
MANAGER_MAX_TRIES_PKG_PATH = "ibl_request_router.api.manager.MANAGER_MAX_TRIES"

MANAGER_BASE_URL = "http://sleipnir.asgard.local"
MANAGER_BASE_API_URL = MANAGER_BASE_URL + "/api"

OAUTH_TOKEN = uuid4().hex


@pytest.mark.django_db
class TestAPIManager:
    endpoint = "knock_knock"
    full_url = f"{MANAGER_BASE_API_URL}/{endpoint}"

    @mock.patch(MANAGER_BASE_URL_PKG_PATH, None)
    def test_on_empty_base_url_returns_404(self):
        with pytest.raises(Http404):
            manager_api_request("get", self.endpoint)

    @mock.patch(MANAGER_BASE_URL_PKG_PATH, MANAGER_BASE_URL)
    @mock.patch(MANAGER_MAX_TRIES_PKG_PATH, 0)
    def test_when_max_retries_is_zero_returns_none(self):
        resp = manager_api_request("get", self.endpoint)

        assert resp is None

    @pytest.mark.parametrize("http_method", ("get", "post", "put", "delete", "patch"))
    @mock.patch(
        "ibl_request_router.api.manager.get_app_access_token", return_value=OAUTH_TOKEN
    )
    @mock.patch(MANAGER_BASE_URL_PKG_PATH, MANAGER_BASE_URL)
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_API_URL", MANAGER_BASE_API_URL
    )
    @mock.patch("ibl_request_router.api.manager.MANAGER_MAX_TRIES", 1)
    @mock.patch("ibl_request_router.api.manager.MANAGER_AUTH_ENABLED", True)
    def test_good_request_returns_response(self, _gaat, http_method, requests_mock):
        def request_data_check(request):
            j = json.loads(request.text)
            return j["detail"] == "hi"

        requests_mock.request(
            http_method,
            self.full_url,
            request_headers={"Authorization": f"Bearer {OAUTH_TOKEN}"},
            json={"detail": "success"},
            additional_matcher=request_data_check,
        )

        resp = manager_api_request(
            http_method, self.endpoint, data={"detail": "hi"}
        )

        assert resp.status_code == 200
        assert resp.json()["detail"] == "success"
