from datetime import timedelta

from common.djangoapps.student.tests.factories import UserFactory
from django.utils import timezone
from openedx.core.djangoapps.oauth_dispatch.tests import factories


def auth_info(**kwargs):
    user = UserFactory(**kwargs)
    application = factories.ApplicationFactory(user=user)
    expires = timezone.now() + timedelta(days=1)
    access_token = factories.AccessTokenFactory(
        user=application.user, application=application, expires=expires
    )
    return (
        user,
        f"Bearer {access_token}",
        getattr(UserFactory, "_DEFAULT_PASSWORD"),
    )
