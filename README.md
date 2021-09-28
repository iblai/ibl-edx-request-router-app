# ibl-request-router

Request router for edX

## Setup
### Dependencies
* [IBL API Auth](https://gitlab.com/iblstudios/ibl-api-auth)


### Tutor
#### Install
```
cd $(tutor config printroot)"/env/build/openedx/requirements
git clone --branch koa-tutor-plugin https://gitlab.com/deeplms/ibl-request-router.git

#Enter the lms shell 
tutor local run lms bash
pip install -e ../requirement/ibl-request-router
```

#### Uninstall
```
#Enter the lms shell 
tutor local run lms bash
pip uninstall ibl_request_router
```

### Django
#### App registration

`ibl_request_router` will be added to `INSTALLED_APPS` in `lms/envs/common.py` & `cms/envs/common.py` automatically. 

```python
INSTALLED_APPS = (
    # ...
    'ibl_request_router'
    # ...
)
```

#### Routing
The apps `urlpatterns` will be added to `lms/urls.py`  automatically (this should be last, or towards the end)
`lms/urls.py`
```python
urlpatterns += (
    url(r'', include('ibl_request_router.urls.lms_urls')),
)
```


#### Settings

* Add these variables to `ibl-request-router.yml` and enable the plugin `tutor plugins enable ibl-request-router` to be applied to `common.py`:

##### Required (for manager proxy)
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
* `MANAGER_DEFAULT_ORG`
* `MANAGER_MULTITENANCY_ENABLED`

##### Sample Config
```
MANAGER_BASE_URL = "https://manager.ibleducation.com"
MANAGER_AUTH_ENABLED = True
MANAGER_AUTH_APP_ID = "manager"
MANAGER_DEFAULT_ORG = "main"
MANAGER_MAX_TRIES = 1
MANAGER_MULTITENANCY_ENABLED = False
MANAGER_PROXY_TIMEOUT = 10
MANAGER_REQUEST_TIMEOUT = 10
MANAGER_VERIFY_SSL = True
```

##### Note
* If `MANAGER_MAX_TRIES` is set to 0, all manager requests will be blocked.

Activate the plugin `tutor plugins enable ibl-request-router`
save the new configuration as shown in the terminal `config save`

Rebuild the image to apply the new config changes 

```tutor images build openedx --build-arg EDX_PLATFORM_REPOSITORY=https://github.com/edx/edx-platform.git --build-arg EDX_PLATFORM_VERSION=open-release/koa.3```
