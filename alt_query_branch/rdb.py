from requests import Session
from requests_cache import CachedSession

from .constants import (
    ALLOWED_BRANCHES,
    CACHING,
    REQUEST_ROUTE,
)


def _restapi_request(request: str):
    if CACHING['enabled']:
        session = CachedSession(
            cache_name=CACHING['path'],
            backend=CACHING['backend'],
            expire_after=CACHING['lifetime'],
        )
    else:
        session = Session()
    return session.get(request, headers={"Accept": "application/json"}).json()


def _branch_binary_packages_response(branch: str):
    if branch not in ALLOWED_BRANCHES:
        raise ValueError(f"Branch {branch} is not available")
    return _restapi_request(f"{REQUEST_ROUTE}/{branch}")


def branch_binary_packages(branch='sisyphus'):
    structured_response = _branch_binary_packages_response(branch)
    return structured_response['packages']


def branch_binary_packages_with_source_package(branch='sisyphus'):
    """
    Removing "non-sources" packages leads to:
    - workarounding for bug on p9 (see: https://bugzilla.altlinux.org/44725)
    - removing packages with "x86_64-i586" arch
    """
    packages = branch_binary_packages(branch)
    return [package for package in packages if package['source'] != '']
