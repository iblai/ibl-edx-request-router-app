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
    pass