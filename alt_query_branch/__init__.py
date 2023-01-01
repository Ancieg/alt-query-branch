from .internal.core_algorithms import search_matching_packages


def cache_enabled(enable = None):
    """
    - when 'enable' is None -> return CACHE_ENABLED;
    - when 'enable' is type(bool) -> set CACHE_ENABLED = enable;
    """
    global CACHE_ENABLED

    if enable is None:
        return CACHE_ENABLED

    if type(enable) is bool:
        CACHE_ENABLED = enable

def cache_lifetime(lifetime = None):
    """
    - when 'lifetime' is None -> return CACHE_LIFETIME;
    - when 'lifetime' is type(int) -> set CACHE_LIFETIME = lifetime;
    """
    global CACHE_LIFETIME

    if lifetime is None:
        return CACHE_LIFETIME

    if type(lifetime) is int:
        CACHE_LIFETIME = lifetime

def cache_path(path = None):
    """
    - when 'path' is None -> return CACHE_PATH;
    - when 'path' is type(str) -> set CACHE_PATH = path;
    """
    global CACHE_PATH

    if path is None:
        return CACHE_PATH

    if type(path) is int:
        CACHE_PATH = path

__all__ = [
    'search_matching_packages',
    'cache_enabled',
    'cache_lifetime',
    'cache_path'
]
