from .constants import (
    ALLOWED_BRANCHES, REQUEST_ROUTE, CACHE_ENABLED, CACHE_LIFETIME, CACHE_PATH
)


import requests
import requests_cache


class RDBNoSuchBranchError(RuntimeError):
    pass

class RDBExportBranchBinaryPackages:
    def __init__(self) -> None:
        if not CACHE_ENABLED:
            self._session = requests.Session()
        else:
            self._session = requests_cache.CachedSession(cache_name=CACHE_PATH, expire_after=CACHE_LIFETIME)

    def _request_api(self, request):
        return self._session.get(request, headers={'Accept': 'application/json'}).json()

    def execute(self, branch='sisyphus'):
        if branch not in ALLOWED_BRANCHES:
            raise RDBNoSuchBranchError('Branch {} is not available'.format(branch))
        return self._request_api(REQUEST_ROUTE.format(branch))
