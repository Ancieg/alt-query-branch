import requests
import requests_cache

from .constants import (
    ALLOWED_BRANCHES,
    CACHING,
    REQUEST_ROUTE,
)


def _restapi_request(request: str):
    if CACHING['enabled']:
        session = requests_cache.CachedSession(
            cache_name=CACHING['path'],
            backend=CACHING['backend'],
            expire_after=CACHING['lifetime'],
        )
    else:
        session = requests.Session()
    return session.get(request, headers={"Accept": "application/json"}).json()


def branch_binary_packages(branch: str):
    if branch not in ALLOWED_BRANCHES:
        raise ValueError("Branch {} is not available".format(branch))
    return _restapi_request(REQUEST_ROUTE.format(branch))


def branch_binary_packages_list(branch='sisyphus'):
    structured_response = branch_binary_packages(branch)
    return structured_response['packages']


def branch_binary_packages_list_with_source_package_only(branch='sisyphus'):
    packages = branch_binary_packages_list(branch)
    return [package for package in packages if package['source'] != '']


__all__ = [
    "branch_binary_packages",
    "branch_binary_packages_list",
    "branch_binary_packages_list_with_source_package_only"
]
