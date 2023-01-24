from .algorithms import search_matching_packages, order_packages  # noqa: F401
from .constants import CACHING  # noqa: F401
from .rdb import branch_binary_packages_with_source_package  # noqa: F401


def enable_caching(path: str = '~/.cache/alt-query-branch',
                   backend: str = 'sqlite',
                   lifetime: int = 300):
    global CACHING
    CACHING['enabled'] = True
    CACHING['path'] = path
    CACHING['backend'] = backend
    CACHING['lifetime'] = lifetime


def disable_caching():
    global CACHING
    CACHING['enabled'] = False
