# ibl-request-router

Request router for edX

## Setup
### Dependencies
* [IBL API Auth](https://gitlab.com/iblstudios/ibl-api-auth)


### Installation
#### Install
```
sudo -Hu edxapp /edx/bin/pip.edxapp install -v git+https://gitlab.com/deeplms/ibl-request-router
```
#### Reinstall
```
sudo -Hu edxapp /edx/bin/pip.edxapp install --upgrade --no-deps --force-reinstall git+https://gitlab.com/deeplms/ibl-request-router
```
#### Uninstall
```
sudo -Hu edxapp /edx/bin/pip.edxapp uninstall ibl_request_router
```

### Django
#### App registration
`lms/envs/common.py`
`cms/envs/common.py`

Add to `INSTALLED_APPS`
```
INSTALLED_APPS = (
    'ibl_request_router',
)
```

#### Routing
Add to the end of `urlpatterns` (this should be last, or towards the end)

`lms/urls.py`
```
urlpatterns += (
    url(r'', include('ibl_request_router.urls.lms_urls')),
)
```


#### Settings

##### Required
* `MANAGER_BASE_URL`: The manager URL

##### Optional
* `MANAGER_AUTH_APP_ID`: The auth manager app ID - corresponds to `ibl-api-auth` (Default: `manager`)
* `MANAGER_AUTH_ENABLED`: The whether manager auth is enabled (Default: `True`)
* `MANAGER_MAX_TRIES`: Request max tries (Default: 1)
* `MANAGER_PROXY_ENABLED`: Whether the manager proxy is enabled (Default: `True`)
* `MANAGER_PROXY_TIMEOUT`: How long it takes for proxy requests to timeout (in seconds)
* `MANAGER_REQUEST_TIMEOUT`: How long it takes for requests to timeout (in seconds)
* `MANAGER_VERIFY_SSL`: Verify SSL on requests (Default: `True`)

##### Additional
`MANAGER_DEFAULT_ORG`
`MANAGER_MULTITENANCY_ENABLED`

##### Sample Config
```
MANAGER_BASE_URL = "https://manager.ibleducation.com"
MANAGER_AUTH_ENABLED = True
MANAGER_AUTH_APP_ID = "manager"
MANAGER_DEFAULT_ORG = "default"
MANAGER_MAX_TRIES = 1
MANAGER_MULTITENANCY_ENABLED = False
MANAGER_PROXY_TIMEOUT = 10
MANAGER_REQUEST_TIMEOUT = 20
MANAGER_VERIFY_SSL = True
```
