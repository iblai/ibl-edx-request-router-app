import logging

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from opaque_keys.edx.keys import CourseKey


log = logging.getLogger(__name__)

DEFAULT_ORG = getattr(settings, 'MANAGER_DEFAULT_ORG', None)
MULTITENANCY_ENABLED = getattr(settings, 'MANAGER_MULTITENANCY_ENABLED', False)


def get_effective_org(org=None):
    if org is not None and MULTITENANCY_ENABLED:
        return org
    else:
        return DEFAULT_ORG

def get_org_from_request(request):
    if MULTITENANCY_ENABLED:
        site = get_current_site(request)
        
        # FUTURE: May have to change when microsites are removed
        microsite = getattr(site, 'microsite', None)
        if microsite:
            # There should only be one org mapped to a microsite in multitenancy
            return microsite.get_organizations().first()
        else:
            return None
    else:
        return DEFAULT_ORG

def get_org_from_course(course):
    if MULTITENANCY_ENABLED:
        return course.org
    else:
        return DEFAULT_ORG

def get_org_from_course_key(course_key):
    if MULTITENANCY_ENABLED:
        return course_key.org
    else:
        return DEFAULT_ORG

def get_org_from_course_key_string(course_key_string):
    ckey = CourseKey.from_string(course_key_string)
    return get_org_from_course_key(ckey)
