from .algorithms import (  # noqa: F401
    group_packages_by_sources,
    sort_groupped_packages_by_sources,
    order_groupped_packages_by_arches,
    search_matching_packages
)
from .constants import CACHING  # noqa: F401
from .rdb import (  # noqa: F401
    branch_binary_packages,
    branch_binary_packages_with_source_package,
)


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
