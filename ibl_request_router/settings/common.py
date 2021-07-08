"""
Settings for the ibl_request_router app.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


USE_TZ = True

INSTALLED_APPS = (
    'ibl_request_router',
)

def plugin_settings(settings):  # pylint: disable=unused-argument
    """
    Defines ibl_request_router-specific settings when app is used as a plugin to edx-platform.
    """
    settings.MANAGER_BASE_URL = "https://studio.iblopen.ibl.dev"
    settings.MANAGER_AUTH_ENABLED = True
    settings.MANAGER_AUTH_APP_ID = "manager"
    settings.MANAGER_DEFAULT_ORG = "main"
    settings.MANAGER_MAX_TRIES = 5
    settings.MANAGER_MULTITENANCY_ENABLED = False
    settings.MANAGER_PROXY_TIMEOUT = 10
    settings.MANAGER_REQUEST_TIMEOUT = 10
    settings.MANAGER_VERIFY_SSL = True