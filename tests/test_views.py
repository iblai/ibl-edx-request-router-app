import json
from unittest import mock
from uuid import uuid4

import pytest
from django.shortcuts import reverse

from .utils import RandomException, auth_info

MANAGER_BASE_URL = "http://sleipnir.asgard.local"
MANAGER_BASE_API_URL = MANAGER_BASE_URL + "/api"
HTTP_METHODS = [
    "get",
    "post",
    "put",
    "delete",
]


@pytest.mark.django_db
class TestManagerProxyView:
    endpoint = "knock_knock"
    url_name = "ibl_request_router:manager_proxy_view"
    full_url = f"{MANAGER_BASE_API_URL}/{endpoint}"

    @pytest.mark.parametrize("http_method", HTTP_METHODS)
    def test_random_endpoint_returns_404(self, http_method, client):
        _, token_header, _ = auth_info()

        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(uuid4().hex,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == 404

    @pytest.mark.parametrize(
        "status_code",
        (
            200,
            400,
        ),
    )
    @pytest.mark.parametrize(
        "is_response_json",
        (
            True,
            False,
        ),
    )
    @pytest.mark.parametrize("http_method", HTTP_METHODS)
    @mock.patch(
        "ibl_request_router.utils.access.MANAGER_API_UNAUTH_ALLOWLIST",
        ("knock_knock",),
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_URL",
        MANAGER_BASE_URL,
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_API_URL",
        MANAGER_BASE_API_URL,
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_AUTH_ENABLED",
        False,
    )
    def test_unprivileged_user_can_access_unauth_endpoints(
        self,
        http_method,
        is_response_json,
        status_code,
        client,
        requests_mock,
    ):
        if is_response_json:
            mocked_resp = {
                "json": {"detail": "success" if status_code == 200 else "not 200"}
            }
        else:
            mocked_resp = {"text": "success"}

        _, token_header, _ = auth_info()
        requests_mock.request(
            http_method, self.full_url, status_code=status_code, **mocked_resp
        )

        resp = client.generic(
            http_method,
            reverse(self.url_name, args=(self.endpoint,)),
            HTTP_AUTHORIZATION=token_header,
        )

        assert resp.status_code == status_code
        if is_response_json:
            if status_code == 200:
                assert resp.json()["detail"] == "success"
            else:
                assert resp.json()["detail"] == "not 200"
        else:
            assert resp.json() == dict()

    @pytest.mark.parametrize("http_method", HTTP_METHODS)
    @mock.patch(
        "ibl_request_router.utils.access.MANAGER_API_UNAUTH_ALLOWLIST",
        ("knock_knock",),
    )
    def test_manager_proxy_request_raises_random_exception_returns_404_from_views(
        self, http_method, client
    ):
        _, token_header, _ = auth_info()
        with mock.patch(
            "ibl_request_router.views.manager_proxy_request",
            side_effect=RandomException(),
        ):
            resp = client.generic(
                http_method,
                reverse(
                    self.url_name,
                    args=(self.endpoint,),
                ),
                HTTP_AUTHORIZATION=token_header,
            )

        assert resp.status_code == 404

    @pytest.mark.parametrize(
        "scenario",
        (
            "ok",
            "user_non_existent",
            "random_exception",
        ),
    )
    @pytest.mark.parametrize("http_method", HTTP_METHODS)
    @mock.patch(
        "ibl_request_router.utils.access.MANAGER_API_UNAUTH_ALLOWLIST",
        ("knock_knock",),
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_URL",
        MANAGER_BASE_URL,
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_BASE_API_URL",
        MANAGER_BASE_API_URL,
    )
    @mock.patch(
        "ibl_request_router.api.manager.MANAGER_AUTH_ENABLED",
        False,
    )
    def test_params_conversion(self, http_method, scenario, client, request_mock):
        if scenario == "ok":
            user, token_header, _ = auth_info()
            request_mock.request(
                http_method,
                f"{self.full_url}?username={user.username}&user_id={user.id}",
                json={"detail": "success"},
            )

            def additional_matcher(request):
                j = json.loads(request)
                is_username_good = j["username"] == user.username
                is_user_id_good = j["user_id"] == user.id
                return is_username_good and is_user_id_good

            request_mock.request(
                http_method,
                f"{self.full_url}",
                json={"detail": "success"},
                additional_matcher=additional_matcher,
            )

            resp = client.generic(
                http_method,
                reverse(
                    self.url_name,
                    args=(self.endpoint,),
                )
                + f"?username={user.username}",
                data=json.dumps({"username": user.username}),
                content_type="application/json",
                HTTP_AUTHORIZATION=token_header,
            )

            assert resp.json()["detail"] == "success"

