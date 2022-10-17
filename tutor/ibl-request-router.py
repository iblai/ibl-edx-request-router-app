from tutor import hooks

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_BASE_URL =  'https://manager.devlms.socialgoodplatform.com'"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_AUTH_ENABLED = True"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_AUTH_APP_ID = 'manager'"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_DEFAULT_ORG = 'main'"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_MAX_TRIES = 5"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_MULTITENANCY_ENABLED = False"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_PROXY_TIMEOUT = 10"
    )
)

hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_REQUEST_TIMEOUT = 10"
    )
)
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "MANAGER_VERIFY_SSL = True"
    )
)


