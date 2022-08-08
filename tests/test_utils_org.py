from unittest import mock

import pytest
from ibl_request_router.utils.org import get_org

DEFAULT_ORG_PKG_PATH = "ibl_request_router.utils.org.DEFAULT_ORG"
DEFAULT_ORG = "UCL Psychopath Academy"

MULTITENANCY_ENABLED_PKG_PATH = "ibl_request_router.utils.org.MULTITENANCY_ENABLED"

MY_ORG = "UCLA Computing Department"


@pytest.mark.django_db
class TestUtilsOrg:
    @pytest.mark.parametrize(
        "my_org",
        (
            MY_ORG,
            None,
        ),
    )
    @pytest.mark.parametrize(
        "multitenancy_enabled",
        (
            True,
            False,
        ),
    )
    @mock.patch(DEFAULT_ORG_PKG_PATH, DEFAULT_ORG)
    def test_get_org(self, multitenancy_enabled, my_org):
        with mock.patch(MULTITENANCY_ENABLED_PKG_PATH, multitenancy_enabled):
            result = get_org(my_org)
        if my_org is not None and multitenancy_enabled:
            assert result == my_org
        else:
            assert result == DEFAULT_ORG
