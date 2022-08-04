import pytest
from django.shortcuts import reverse

from .utils import auth_info


@pytest.mark.django_db
class TestManagerProxyView:
    endpoint = "/knock_knock/"
    url = reverse("ibl_request_router:manager_proxy_view", args=(None, ))

    @pytest.mark.parametrize(
        "http_method",
        [
            "GET",
            "POST",
            "PUT",
            "DELETE",
        ],
    )
    def test_no_endpoint_returns_404(self, http_method, client):
        _, token_header, _ = auth_info()

        resp = getattr(client, http_method.lower())(
            self.url, HTTP_AUTHORIZATION=token_header
        )

        assert resp.status_code == 404
