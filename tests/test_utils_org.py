from unittest import mock

import pytest
from django.test import RequestFactory
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import ToyCourseFactory

from ibl_request_router.utils.org import (get_org, get_org_from_course,
                                          get_org_from_course_key_string,
                                          get_org_from_request)

from .utils import course_key

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

    @pytest.mark.parametrize(
        "multitenancy_enabled",
        (
            True,
            False,
        ),
    )
    @mock.patch(DEFAULT_ORG_PKG_PATH, DEFAULT_ORG)
    def test_get_org_from_request(self, multitenancy_enabled):
        request = RequestFactory()
        request.get_host = lambda: "127.0.0.1"
        with mock.patch(MULTITENANCY_ENABLED_PKG_PATH, multitenancy_enabled):
            org = get_org_from_request(request)
        if multitenancy_enabled:
            assert org is None  # no microsite
        else:
            assert org == DEFAULT_ORG


@pytest.mark.django_db
class TestGetOrgFromCourses(ModuleStoreTestCase):
    @mock.patch(DEFAULT_ORG_PKG_PATH, DEFAULT_ORG)
    def test_get_org_from_course_or_key_or_string(self):
        toy_course = ToyCourseFactory()
        course_key_string = str(course_key(toy_course))

        with mock.patch(MULTITENANCY_ENABLED_PKG_PATH, True):
            org_from_course = get_org_from_course(toy_course)
            org_from_string = get_org_from_course_key_string(course_key_string)
            assert org_from_string == toy_course.org
            assert org_from_course == toy_course.org

        with mock.patch(MULTITENANCY_ENABLED_PKG_PATH, False):
            org_from_course = get_org_from_course(toy_course)
            org_from_string = get_org_from_course_key_string(course_key_string)
            assert org_from_string == DEFAULT_ORG
            assert org_from_course == DEFAULT_ORG
